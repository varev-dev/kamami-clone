import os
import json
import time
from bs4 import BeautifulSoup
from utils import fetch_page
from categories import scrape_categories
from image_downloader import download_product_images

BASE_URL = "https://kamami.pl"
DATA_DIR = "../data/products"

os.makedirs(DATA_DIR, exist_ok=True)

def scrape_all_products(categories_json="../data/categories.json", limit=None, per_category_limit=None):
    if not os.path.exists(categories_json):
        print("[INFO] Categories file not found. Scraping categories first...")
        scrape_categories()

    with open(categories_json, "r", encoding="utf-8") as f:
        categories = json.load(f)

    all_products = []
    total_scraped = 0

    def process_category(cat):
        nonlocal total_scraped
        if limit is not None and total_scraped >= limit:
            return

        # Sprawdź czy plik JSON już istnieje
        category_filename = os.path.join(DATA_DIR, sanitize_filename(cat["name"]) + ".json")
        if os.path.exists(category_filename):
            print(f"\n[SKIP] Category already scraped: {cat['name']} (file exists: {category_filename})")
            # Wczytaj istniejące produkty do all_products
            try:
                with open(category_filename, "r", encoding="utf-8") as f:
                    existing_products = json.load(f)
                    all_products.extend(existing_products)
                    total_scraped += len(existing_products)
            except Exception as e:
                print(f"[WARN] Could not load existing file: {e}")
        else:
            print(f"\n[INFO] Scraping category: {cat['name']} ({cat['url']})")
            
            # Określ limit dla tej kategorii
            category_limit = per_category_limit
            if limit is not None:
                remaining = limit - total_scraped
                if category_limit is None:
                    category_limit = remaining
                else:
                    category_limit = min(category_limit, remaining)
            
            products = scrape_category_products(cat["url"], limit=category_limit)

            if products:
                total_scraped += len(products)
                save_json(products, category_filename)
                all_products.extend(products)

        for sub in cat.get("subcategories", []):
            if limit is not None and total_scraped >= limit:
                return
            process_category(sub)

    for category in categories:
        if limit is not None and total_scraped >= limit:
            break
        process_category(category)

    print(f"\n[FINISHED] Total products scraped: {len(all_products)} (limit={limit}, per_category={per_category_limit})")
    return all_products


def scrape_category_products(category_url, limit=None):
    page = 1
    products = []

    while True:
        if limit is not None and len(products) >= limit:
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
            if limit is not None and len(products) >= limit:
                break

            link_tag = art.select_one("div.thumbnail-container div.product_desc div.product-description div.product-title a.name")
            if not link_tag:
                continue
            product_url = link_tag.get("href")
            product_name = link_tag.get_text(strip=True)
            print(f"  > {product_name}")

            product_data = scrape_product_details(product_url)
            if product_data:
                products.append(product_data)

            time.sleep(0.5)

        if limit is not None and len(products) >= limit:
            break
        next_page = soup.select_one("ul.pagination a[rel='next']")
        if not next_page:
            break
        page += 1

    return products

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

    desc_div = main.select_one(".product-description")
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

    # zachowaj tylko 2 największe / unikalne
    # images = images[:2]

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

    return {
        "name": name,
        "id": prod_id,
        "url": product_url,
        "short_description": short_desc,
        "full_description_html": full_description,
        "price_brutto": price_brutto,
        "price_netto": price_netto,
        "attributes": attributes,
        "images": images,
        "local_images": local_images
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