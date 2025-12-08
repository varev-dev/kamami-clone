import json
import requests
import os

API_URL = "http://localhost:8080/api"
API_KEY = "35TNU98SNJ8X79J3T338I84M4GE9M9PU"

HEADERS = {
    "Output-Format": "JSON"
}

def add_image_to_product(product_id, image_path_or_url):
    """
    Dodaje zdjęcie do istniejącego produktu w PrestaShop.
    image_path_or_url może być lokalną ścieżką lub URL.
    """
    if image_path_or_url.startswith("http"):
        # Pobierz obraz z URL
        response = requests.get(image_path_or_url, stream=True)
        if response.status_code != 200:
            print(f"Nie udało się pobrać obrazu {image_path_or_url}")
            return False
        files = {'image': ('image.jpg', response.raw, 'image/jpeg')}
    else:
        # Plik lokalny
        if not os.path.exists(image_path_or_url):
            print(f"Nie znaleziono pliku {image_path_or_url}")
            return False
        files = {'image': open(image_path_or_url, 'rb')}

    url = f"{API_URL}/images/products/{product_id}"
    r = requests.post(url, auth=(API_KEY, ''), files=files)
    
    # Zamknij plik jeśli to lokalny
    if not image_path_or_url.startswith("http"):
        files['image'].close()

    if r.status_code in (200, 201):
        print(f"✓ Zdjęcie dodane do produktu {product_id}")
        return True
    else:
        print(f"✗ Błąd przy dodawaniu zdjęcia do produktu {product_id}: {r.status_code}")
        print(r.text)
        return False

def process_products(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    for prod in products:
        ps_id = prod.get("ps_id")
        if not ps_id:
            print(f"Produkt {prod.get('name')} nie ma ps_id, pomijam")
            continue

        local_images = prod.get("local_images", [])
        if local_images:
            for img_path in local_images:
                add_image_to_product(ps_id, img_path)
        else:
            images = prod.get("images", [])
            for img_url in images:
                add_image_to_product(ps_id, img_url)

if __name__ == "__main__":
    process_products("../data/products_all.json")
