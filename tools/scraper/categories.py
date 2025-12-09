from bs4 import BeautifulSoup as BS
from utils import fetch_page
import json
import requests

ID_CTR = 3
BASE_URL = 'https://kamami.pl/'

def scrape_categories():
    print("[INFO] Fetching main page...")
    html = fetch_page(BASE_URL)
    if not html:
        print("[ERROR] Failed to fetch main page")
        return []

    soup = BS(html, "lxml")

    menu_items = soup.select_one("#left-column > div > .block-categories > ul > li#main-categories > ul.category-sub-menu")
    if not menu_items:
        print("[ERROR] Could not find category list")
        return []

    categories = parse_category_list(menu_items)

    with open("../data/categories.json", "w", encoding="utf-8") as f:
        json.dump(categories, f, ensure_ascii=False, indent=2)

    print(f"[DONE] Saved {len(categories)} top-level categories to ../data/categories.json")
    return categories

def parse_category_list(ul_element):
    result = []
    for li in ul_element.select(":scope > li"):
        link = li.select_one(":scope > a")
        if not link:
            continue

        name = link.get_text(strip=True)
        url = link.get("href")
        if not url.startswith("http"):
            url = BASE_URL + url

        # update global ID_CTR
        global ID_CTR
        cat_id = ID_CTR
        ID_CTR += 1

        # check for subcategories
        sub_ul = li.select_one(":scope > div.collapse > ul.category-sub-menu")
        subcategories = parse_category_list(sub_ul) if sub_ul else []

        result.append({
            "id": cat_id,
            "name": name,
            "url": url,
            "subcategories": subcategories
        })

    return result