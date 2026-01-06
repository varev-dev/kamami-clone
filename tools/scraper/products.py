import os
import json
import time
from bs4 import BeautifulSoup
from utils import fetch_page
from categories import scrape_categories
from image_downloader import download_product_images

BASE_URL = "https://kamami.pl"
DATA_DIR = "../data"
OUTPUT_FILE = "products_all.json"
ID = 0

os.makedirs(DATA_DIR, exist_ok=True)

def scrape_all_products(categories_json="../data/categories.json", limit=None, per_category_limit=None):
    if not os.path.exists(categories_json):
        print("[INFO] Categories file not found. Scraping categories first...")
        scrape_categories()

    with open(categories_json, "r", encoding="utf-8") as f:
        categories = json.load(f)
    
    categories_lookup_map = build_category_path_map(categories)

    products_map = {}
    url_to_id = {}

    total_unique_scraped = 0

    def process_category(cat):
        nonlocal total_unique_scraped

        for sub in cat.get("subcategories", []):
            if limit is not None and total_unique_scraped >= limit:
                return
            process_category(sub)

        if limit is not None and total_unique_scraped >= limit:
            return

        print(f"\n[INFO] Scraping category: {cat['name']} ({cat['url']})")

        current_limit = limit - total_unique_scraped if limit else None
        new_items_count = scrape_category_products(
            category_url=cat["url"], 
            category_id=cat["id"],
            products_map=products_map,
            url_to_id=url_to_id,
            per_category_limit=per_category_limit, 
            limit=current_limit, 
        )

        total_unique_scraped += new_items_count

    for category in categories:
        if limit is not None and total_unique_scraped >= limit:
            break
        process_category(category)

    all_products_list = list(products_map.values())

    print("[INFO] Assigning final category IDs based on breadcrumb paths...")
    final_products = assign_final_category_ids(all_products_list, categories_lookup_map)
    
    output_path = os.path.join(DATA_DIR, OUTPUT_FILE)
    save_json(all_products_list, output_path)

    print(f"\n[FINISHED] Total products scraped: {len(all_products_list)} (limit={limit})")
    return final_products

def scrape_category_products(category_url, category_id, per_category_limit,  limit=None, products_map=None, url_to_id=None):
    page = 1
    items_found_in_cat = 0
    new_unique_items = 0

    while True:
        if per_category_limit is not None and items_found_in_cat >= per_category_limit:
            break
        if limit is not None and new_unique_items >= limit:
            break

        url = f"{category_url}?page={page}"
        html = fetch_page(url)
        if not html:
            break

        soup = BeautifulSoup(html, "lxml")
        product_articles = soup.select("div.products.rows article")

        if not product_articles:
            break

        for art in product_articles:
            if per_category_limit is not None and items_found_in_cat >= per_category_limit:
                break
            if limit is not None and new_unique_items >= limit:
                break

            link_tag = art.select_one(
                "div.thumbnail-container div.product_desc div.product-description div.product-title a.name"
            )
            if not link_tag:
                continue

            product_url = link_tag.get("href")

            if product_url in url_to_id:
                existing_id = url_to_id[product_url]
                if existing_id in products_map:
                    product = products_map[existing_id]
                    
                    if product.get('category_id') != category_id:
                        if category_id not in product['subcategories']:
                            product['subcategories'].append(category_id)
                
                items_found_in_cat += 1
                continue

            product_name = link_tag.get_text(strip=True)
            print(f"  > {product_name}")

            product_data = scrape_product_details(product_url)
            if product_data:
                kamami_id = product_data['id']
                
                product_data['category_id'] = category_id
                product_data['subcategories'] = []
                
                products_map[kamami_id] = product_data
                url_to_id[product_url] = kamami_id
                
                items_found_in_cat += 1
                new_unique_items += 1

            time.sleep(0.25)

        next_page = soup.select_one("ul.pagination a[rel='next']")
        if not next_page:
            break
        page += 1

    return new_unique_items

def scrape_product_details(product_url):
    html = fetch_page(product_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")
    main = soup.select_one("div#main")
    if not main:
        return None

    name = get_text(main, "h1.page-title")
    short_desc = get_text(main, "div.product-details-information div.product-description p")
    price_brutto = get_text(main, "span.current-price-value")
    price_netto = get_text(main, "p.product-without-taxes")
    prod_id = get_text(main, "div.prod-id_product").replace("ID:", "").strip()
    
    breadcrumb_path = []
    breadcrumb_nav = soup.select_one("nav.breadcrumb ol")
    main_category_name = ""
    
    if breadcrumb_nav:
        items = breadcrumb_nav.select("li span[itemprop='name']")
        breadcrumb_path = [i.get_text(strip=True) for i in items]
        if len(breadcrumb_path) >= 2:
            main_category_name = breadcrumb_path[-2]

    desc_div = main.select_one("#description .product-description")
    full_description = desc_div.decode_contents() if desc_div else ""

    images = []
    thumbs = main.select("ul.product-images li.thumb-container img.thumb")
    for t in thumbs:
        large_src = t.get("data-image-large-src") or t.get("src")
        if large_src and large_src not in images:
            images.append(large_src)

    if not images:
        main_img = main.select_one("img.js-qv-product-cover.img-fluid")
        if main_img and main_img.get("src"):
            images.append(main_img["src"])

    attributes = {}
    data_sheet = main.select_one("section.product-features dl.data-sheet")
    if data_sheet:
        elements = data_sheet.find_all(["dt", "dd"])
        key = None
        for el in elements:
            if el.name == "dt":
                key = el.get_text(strip=True)
            elif el.name == "dd" and key:
                value = el.get_text(strip=True)
                attributes[key] = value
                key = None

    local_images = download_product_images(prod_id, images)
    global ID 
    ID += 1

    weight_kg = None

    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)

            items = data if isinstance(data, list) else [data]

            for item in items:
                if not isinstance(item, dict):
                    continue

                if item.get("@type") == "Product":
                    weight = item.get("weight")
                    if isinstance(weight, dict):
                        value = weight.get("value")
                        unit = weight.get("unitCode", "").lower()

                        if value:
                            value = float(value)

                            if unit == "g":
                                weight_kg = value / 1000
                            elif unit == "kg":
                                weight_kg = value
                            elif unit == "mg":
                                weight_kg = value / 1_000_000

                            break
        except Exception:
            continue

        if weight_kg is not None:
            break
    
    return {
        "ps_id": ID,
        "id": prod_id,
        "name": name,
        "url": product_url,
        "breadcrumb_category": main_category_name, # real main category from breadcrumb
        "breadcrumb_full": breadcrumb_path,
        "short_description": short_desc,
        "full_description_html": full_description,
        "price_brutto": price_brutto,
        "price_netto": price_netto,
        "weight_kg": weight_kg,
        "attributes": attributes,
        "images": images,                # original links
        "local_images": local_images     # paths to downloaded files
    }

def clean_text(text: str) -> str:
    if not text:
        return ""
    return text.replace("\xa0", " ").strip()

def get_text(soup, selector):
    el = soup.select_one(selector)
    if not el:
        return ""
    return clean_text(el.get_text())

def sanitize_filename(name):
    return name.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")

def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] {len(data)} products → {path}")

def assign_final_category_ids(products, category_map, separator=" > "):
    """
    Assigns final category IDs to products based on their breadcrumb paths.
    """
    count_assigned = 0
    count_missing = 0

    for product in products:
        raw_crumb = product.get('breadcrumb_full', [])[:]
        
        if not raw_crumb:
            product['category_id'] = None
            count_missing += 1
            continue

        if raw_crumb and raw_crumb[0].strip() == "Kategorie główne":
            raw_crumb.pop(0)

        if raw_crumb and len(raw_crumb) > 0:
             raw_crumb.pop(-1)

        crumb_key = separator.join([str(x).strip() for x in raw_crumb])
        
        cat_id = category_map.get(crumb_key)

        if cat_id:
            product['category_id'] = cat_id
            count_assigned += 1
        else:
            product['category_id'] = None
            count_missing += 1
   
    print(f"[INFO] Category ID assignment: {count_assigned} assigned, {count_missing} not found.")
    return products

def build_category_path_map(categories, parent_path="", separator=" > "):
    """
    Recursively builds a mapping from full category paths to their IDs.
    """
    mapping = {}
    
    for cat in categories:
        cat_name = cat['name'].strip()
        full_path = f"{parent_path}{separator}{cat_name}" if parent_path else cat_name
        
        mapping[full_path] = cat['id']
        
        if cat.get("subcategories"):
            sub_mapping = build_category_path_map(
                cat["subcategories"], 
                parent_path=full_path, 
                separator=separator
            )
            mapping.update(sub_mapping)
            
    return mapping
