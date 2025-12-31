import requests
from pathlib import Path
import argparse

def upload_product(xml_file, api_url, api_key):
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        response = requests.post(
            api_url,
            auth=(api_key, ''),
            data=xml_content.encode('utf-8'),
            headers={'Content-Type': 'application/xml'},
            verify='../../apache-conf/certs/server.crt'
        )

        if response.status_code >= 400:
            raise Exception(f"API error {response.status_code}: {response.text}")

        return True, xml_file.name, None, response.text

    except Exception as e:
        return False, xml_file.name, str(e), None


def main():
    parser = argparse.ArgumentParser(
        description="Upload products to PrestaShop via WebService API (synchronously)"
    )
    parser.add_argument(
        "--api-url",
        default="https://localhost:8443/api/products",
        help="PrestaShop API URL (e.g., https://yourshop.com/api/products)"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="PrestaShop API key (32 characters)"
    )
    parser.add_argument(
        "--xml-dir",
        default="../data/products_xml",
        help="Directory containing XML files (default: ../data/products_xml)"
    )
    
    args = parser.parse_args()
    
    xml_dir = Path(args.xml_dir)
    if not xml_dir.exists():
        print(f"Error: Directory {xml_dir} does not exist")
        return
    
    xml_files = sorted(list(xml_dir.glob('*.xml')))
    
    if not xml_files:
        print(f"No XML files found in {xml_dir}")
        return
    
    print(f"=== PrestaShop Product Upload (Synchronous) ===")
    print(f"Found {len(xml_files)} XML files")
    print(f"API URL: {args.api_url}\n")
    
    success_count = 0
    failed_count = 0
    failed_files = []

    for xml_file in xml_files:
        success, filename, error, response_text = upload_product(xml_file, args.api_url, args.api_key)
        if success:
            success_count += 1
            print(f"✓ {filename}")
        else:
            failed_count += 1
            failed_files.append((filename, error))
            print(f"✗ {filename}: {error}")

    print(f"\n=== Summary ===")
    print(f"Success: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {len(xml_files)}")
    
    if failed_files:
        print(f"\nFailed files:")
        for filename, error in failed_files:
            print(f"  - {filename}: {error}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user, exiting.")
    except Exception as e:
        print(f"\nError: {e}")
