from bs4 import BeautifulSoup as BS
from utils import fetch_page
from image_downloader import download_image

import json
import requests
import os

ID_CTR = 3
BASE_URL = 'https://kamami.pl/'
IMAGES_DIR = "../data/categories/images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def scrape_categories():
    print("[INFO] Phase 1: Building category tree structure...")
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

    print(f"[INFO] Phase 2: Enriching {len(categories)} main categories (deep scrape)...")
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
            "description": "",
            "image_url": None,
            "local_image": None,
            "subcategories": subcategories
        })

    return result

def enrich_categories_recursive(categories_list, visited_urls):
    for cat in categories_list:
        print(f"   > Processing: {cat['name']}...")
        
        url = cat['url']
        if url in visited_urls:
            continue
        visited_urls.add(url)
        
        html = fetch_page(cat['url'])
        if not html:
            continue
            
        soup = BS(html, "lxml")
        
        desc_p = soup.select_one("#category-description p")
        if not desc_p:
            desc_p = soup.select_one("#main > div:first-of-type > p")
        
        if desc_p:
            cat['description'] = desc_p.get_text(strip=True)

        subcat_images_map = {} 
        
        sub_list = soup.select_one("div#subcategories ul.subcategories-list")
        if sub_list:
            items = sub_list.select(":scope > li")
            for item in items:
                link_tag = item.select_one("h3 > a.subcategory-name")
                img_tag = item.select_one("div.subcategory-image img")
                
                if link_tag and img_tag:
                    href = link_tag.get("href")
                    src = img_tag.get("src")
                    
                    if href and src:
                        if not href.startswith("http"):
                            href = BASE_URL + href
                        
                        subcat_images_map[href] = src

        matched_count= 0
        for sub in cat['subcategories']:
            if sub['url'] in subcat_images_map:
                img_url = subcat_images_map[sub['url']]
                sub['image_url'] = img_url
          
                ext = os.path.splitext(img_url.split("?")[0])[1] or ".jpg"
                filename = f"cat_{sub['id']}{ext}"
                dest_path = os.path.join(IMAGES_DIR, filename)
    
                if download_image(img_url, dest_path):
                    sub['local_image'] = dest_path
                    matched_count += 1
            
        if matched_count > 0:
            print(f"     [+] Matched images for {matched_count} subcategories.")

        enrich_categories_recursive(cat['subcategories'], visited_urls)
