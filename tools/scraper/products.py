import os
import json
import time
from bs4 import BeautifulSoup
from utils import fetch_page
from categories import scrape_categories

BASE_URL = "https://kamami.pl"
DATA_DIR = "data/products"

os.makedirs(DATA_DIR, exist_ok=True)

def scrape_all_products(categories_json="data/categories.json", limit=None):
    """Scrape all products from all categories (with optional global limit)"""
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

        print(f"\n[INFO] Scraping category: {cat['name']} ({cat['url']})")
        products = scrape_category_products(cat["url"], limit=limit - total_scraped if limit else None)

        if products:
            total_scraped += len(products)
            save_json(products, os.path.join(DATA_DIR, sanitize_filename(cat["name"]) + ".json"))
            all_products.extend(products)

        # Rekurencyjnie subkategorie
        for sub in cat.get("subcategories", []):
            if limit is not None and total_scraped >= limit:
                return
            process_category(sub)

    for category in categories:
        if limit is not None and total_scraped >= limit:
            break
        process_category(category)

    print(f"\n[FINISHED] Total products scraped: {len(all_products)} (limit={limit})")
    return all_products


def scrape_category_products(category_url, limit=None):
    """Scrape products from a single category with pagination and optional limit"""
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

            time.sleep(1)

        if limit is not None and len(products) >= limit:
            break
        next_page = soup.select_one("ul.pagination a[rel='next']")
        if not next_page:
            break
        page += 1

    return products

def scrape_product_details(product_url):
    """Scrape single product details"""
    html = fetch_page(product_url)
    if not html:
        return None

    soup = BeautifulSoup(html, "lxml")
    main = soup.select_one("div#main")
    if not main:
        return None

    # --- podstawowe dane ---
    name = get_text(main, "h1.page-title")
    short_desc = get_text(main, "div.product-details-information div.product-description p")
    price_brutto = get_text(main, "span.current-price-value")
    price_netto = get_text(main, "p.product-without-taxes")
    prod_id = get_text(main, "div.prod-id_product").replace("ID:", "").strip()

    # --- pełny opis (HTML zachowujemy) ---
    desc_div = main.select_one(".product-description")
    full_description = desc_div.decode_contents() if desc_div else ""

    # --- zdjęcia ---
    images = []
    main_img = main.select_one("img.js-qv-product-cover.img-fluid")
    if main_img and main_img.get("src"):
        images.append(main_img["src"])

    thumbs = main.select("ul.product-images li.thumb-container img.thumb")
    for t in thumbs:
        if t.get("data-image-large-src"):
            images.append(t["data-image-large-src"])
        elif t.get("src"):
            images.append(t["src"])

    # --- atrybuty (opcjonalne) ---
    attributes = {}
    for row in main.select(".product-features tr"):
        cells = row.select("td")
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            attributes[key] = value

    return {
        "name": name,
        "id": prod_id,
        "url": product_url,
        "short_description": short_desc,
        "full_description_html": full_description,
        "price_brutto": price_brutto,
        "price_netto": price_netto,
        "attributes": attributes,
        "images": images[:2],  # tylko dwa zdjęcia, jak w wymaganiach
    }


# --- helpery ---
def get_text(soup, selector):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else ""


def sanitize_filename(name):
    return name.lower().replace(" ", "_").replace("/", "_").replace("\\", "_")


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[SAVED] {len(data)} products → {path}")
