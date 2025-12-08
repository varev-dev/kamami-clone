import json
import requests
import os
import argparse

API_URL = "http://localhost:8080/api"
HEADERS = {
    "Output-Format": "JSON"
}

def add_image_to_product(product_id, image_path_or_url, api_key):
    if image_path_or_url.startswith("http"):
        response = requests.get(image_path_or_url, stream=True)
        if response.status_code != 200:
            print(f"Failed to fetch image {image_path_or_url}")
            return False
        files = {'image': ('image.jpg', response.raw, 'image/jpeg')}
    else:
        if not os.path.exists(image_path_or_url):
            print(f"File not found {image_path_or_url}")
            return False
        files = {'image': open(image_path_or_url, 'rb')}

    url = f"{API_URL}/images/products/{product_id}"
    r = requests.post(url, auth=(api_key, ''), files=files)

    if not image_path_or_url.startswith("http"):
        files['image'].close()

    if r.status_code in (200, 201):
        print(f"✓ Image added to product {product_id}")
        return True
    else:
        print(f"✗ Failed to add image to product {product_id}: {r.status_code}")
        print(r.text)
        return False

def process_products(json_file, api_key):
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for prod in products:
        ps_id = prod.get("ps_id")
        if not ps_id:
            print(f"Product {prod.get('name')} has no ps_id, skipping")
            continue

        local_images = prod.get("local_images", [])
        if local_images:
            for img_path in local_images:
                add_image_to_product(ps_id, img_path, api_key)
        else:
            images = prod.get("images", [])
            for img_url in images:
                add_image_to_product(ps_id, img_url, api_key)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Adding images to PrestaShop products")
    parser.add_argument(
        "--api-key",
        required=True,
        help="PrestaShop API key (32 characters)"
    )
    args = parser.parse_args()
    API_KEY = args.api_key

    process_products("../data/products_all.json", API_KEY)
