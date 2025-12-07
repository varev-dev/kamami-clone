import aiohttp
import asyncio
from pathlib import Path
import argparse

async def upload_product_async(session, xml_file, api_url, api_key):
    """Async upload"""
    try:
        with open(xml_file, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        auth = aiohttp.BasicAuth(api_key, '')

        async with session.post(
            api_url,
            auth=auth,
            data=xml_content.encode('utf-8'),
            headers={'Content-Type': 'application/xml'}
        ) as response:

            response_text = await response.text()
            status = response.status

            print(status, xml_file.name)
            print(response_text)

            if status >= 400:
                raise Exception(f"API error {status}: {response_text}")

            return True, xml_file.name, None, response_text

    except Exception as e:
        return False, xml_file.name, str(e), None

async def upload_all_async(xml_files, api_url, api_key, max_concurrent=10):
    """Upload all products asynchronously"""
    connector = aiohttp.TCPConnector(limit=max_concurrent)
    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [upload_product_async(session, xml_file, api_url, api_key) 
                 for xml_file in xml_files]
        results = await asyncio.gather(*tasks)
        return results

def main():
    parser = argparse.ArgumentParser(
        description="Upload products to PrestaShop via WebService API"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:8080/api/products",
        help="PrestaShop API URL (e.g., https://yourshop.com/api/products)"
    )
    parser.add_argument(
        "--api-key",
        required=True,
        help="PrestaShop API key (32 characters)"
    )
    parser.add_argument(
        "--max-concurrent",
        type=int,
        default=10,
        help="Maximum concurrent requests (default: 10)"
    )
    parser.add_argument(
        "--xml-dir",
        default="../data/products/xml",
        help="Directory containing XML files (default: ../data/products/xml)"
    )
    
    args = parser.parse_args()
    
    # Find all XML files
    xml_dir = Path(args.xml_dir)
    if not xml_dir.exists():
        print(f"Error: Directory {xml_dir} does not exist")
        return
    
    xml_files = sorted(list(xml_dir.glob('*.xml')))
    
    if not xml_files:
        print(f"No XML files found in {xml_dir}")
        return
    
    print(f"=== PrestaShop Product Upload ===")
    print(f"Found {len(xml_files)} XML files")
    print(f"API URL: {args.api_url}")
    print(f"Max concurrent requests: {args.max_concurrent}")
    print(f"\nUploading products...\n")
    
    # Upload all products
    results = asyncio.run(upload_all_async(
        xml_files, 
        args.api_url, 
        args.api_key, 
        args.max_concurrent
    ))
    
    # Process results
    success_count = 0
    failed_count = 0
    failed_files = []
    
    for success, filename, error, response_text in results:
        if success:
            success_count += 1
            print(f"✓ {filename}")
        else:
            failed_count += 1
            failed_files.append((filename, error))
            print(f"✗ {filename}: {error}")
    
    # Summary
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