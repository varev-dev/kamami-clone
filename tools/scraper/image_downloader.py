import os
import requests

def download_image(url: str, dest_path: str) -> bool:
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"[WARN] Failed to download {url}: {e}")
        return False


def download_product_images(product_id: str, image_urls: list[str], base_dir: str = "data/products/images") -> list[str]:
    saved_files = []
    if not image_urls:
        return saved_files

    product_dir = os.path.join(base_dir, str(product_id))
    os.makedirs(product_dir, exist_ok=True)

    for idx, url in enumerate(image_urls):
        ext = os.path.splitext(url.split("?")[0])[1] or ".jpg"
        filename = f"img_{idx+1}{ext}"
        dest_path = os.path.join(product_dir, filename)

        if download_image(url, dest_path):
            saved_files.append(dest_path)

    return saved_files
