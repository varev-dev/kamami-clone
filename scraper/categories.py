import os
import json
import requests
from bs4 import BeautifulSoup as BS
from image_downloader import download_image

ID_CTR = 3
BASE_URL = 'https://kamami.pl/'
ROOT_CAT_URL = 'https://kamami.pl/2-kategorie-glowne'
IMAGES_DIR = "../data/categories/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

# Session setup
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
})

def fetch_page_session(url):
    try:
        resp = session.get(url, timeout=10)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

def scrape_categories():
    print("[INFO] Phase 1: Building category tree structure...")
    html = fetch_page_session(BASE_URL)
    if not html:
        return []

    soup = BS(html, "lxml")
    menu_items = soup.select_one("#left-column > div > .block-categories > ul > li#main-categories > ul.category-sub-menu")
    
    if not menu_items:
        print("[ERROR] Could not find category list")
        return []

    categories = parse_category_list(menu_items)
    
    print(f"[INFO] Phase 1.5: Fetching images for TOP-LEVEL categories from {ROOT_CAT_URL}...")
    root_html = fetch_page_session(ROOT_CAT_URL)
    if root_html:
        root_soup = BS(root_html, "lxml")
        _match_and_download_images(root_soup, categories)

    print(f"[INFO] Phase 2: Enriching {len(categories)} main categories (deep scrape & discovery)...")
    visited_urls = set()
    enrich_categories_recursive(categories, visited_urls)

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

        global ID_CTR
        cat_id = ID_CTR
        ID_CTR += 1

        sub_ul = li.select_one(":scope > div.collapse > ul.category-sub-menu")
        subcategories = parse_category_list(sub_ul) if sub_ul else []

        result.append({
            "id": cat_id,
            "name": name,
            "url": url,
            "description": "",
            "image_url": None,
            "local_image": None,
            "subcategories": subcategories
        })

    return result

def _match_and_download_images(soup, categories_list):
    grid_items_map = {} 
    
    sub_list = soup.select_one("div#subcategories ul.subcategories-list")
    if sub_list:
        items = sub_list.select(":scope > li")
        for item in items:
            link_tag = item.select_one("h3 > a.subcategory-name")
            img_tag = item.select_one("div.subcategory-image img")
            
            if link_tag and img_tag:
                href = link_tag.get("href")
                name = link_tag.get_text(strip=True)
                src = img_tag.get("src")
                
                if href and src:
                    if not href.startswith("http"):
                        href = BASE_URL + href
                    
                    grid_items_map[href] = {
                        "src": src,
                        "name": name
                    }

    matched_urls = set()
    matched_count = 0
    
    for cat in categories_list:
        if cat['url'] in grid_items_map:
            data = grid_items_map[cat['url']]
            img_url = data['src']
            
            cat['image_url'] = img_url
            matched_urls.add(cat['url'])
            
            ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
            filename = f"cat_{cat['id']}{ext}"
            dest_path = os.path.join(IMAGES_DIR, filename)
            
            if download_image(img_url, dest_path):
                cat['local_image'] = dest_path
                matched_count += 1

    new_items_count = 0
    global ID_CTR
    
    for url, data in grid_items_map.items():
        if url not in matched_urls:
            cat_id = ID_CTR
            ID_CTR += 1
            
            img_url = data['src']
            ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
            filename = f"cat_{cat_id}{ext}"
            dest_path = os.path.join(IMAGES_DIR, filename)
            local_image = None
            
            if download_image(img_url, dest_path):
                local_image = dest_path

            new_category = {
                "id": cat_id,
                "name": data['name'],
                "url": url,
                "description": "", 
                "image_url": img_url,
                "local_image": local_image,
                "subcategories": []
            }
            
            categories_list.append(new_category)
            new_items_count += 1

    if matched_count > 0 or new_items_count > 0:
        print(f"     [+] Processed grid: {matched_count} updated, {new_items_count} new discovered.")

def enrich_categories_recursive(categories_list, visited_urls):
    for cat in categories_list:
        url = cat['url']

        if url in visited_urls:
            continue
        visited_urls.add(url)
        
        print(f"   > Processing: {cat['name']}...")
        
        html = fetch_page_session(url)
        if not html:
            continue
            
        soup = BS(html, "lxml")
        
        desc_p = soup.select_one("#category-description p")
        if not desc_p:
            desc_p = soup.select_one("#main > div:first-of-type > p")
        
        if desc_p:
            cat['description'] = desc_p.get_text(strip=True)

        _match_and_download_images(soup, cat['subcategories'])

        enrich_categories_recursive(cat['subcategories'], visited_urls)
