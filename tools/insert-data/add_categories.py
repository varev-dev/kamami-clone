import requests
from pathlib import Path
import argparse
from datetime import datetime


def upload_category(xml_file, api_url, api_key):
    """Upload a single category XML file via PrestaShop WebService"""
    try:
        with open(xml_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

        response = requests.post(
            api_url,
            data=xml_content.encode("utf-8"),
            auth=(api_key, ""),
            headers={"Content-Type": "application/xml"},
            timeout=30
        )

        status = response.status_code
        response_text = response.text

        # Print to console
        print(f"{status} {xml_file.name}")

        # If API reports error → raise exception
        if status >= 400:
            raise Exception(f"API error {status}: {response_text}")

        return True, xml_file.name, None, response_text

    except Exception as e:
        return False, xml_file.name, str(e), None


def main():
    parser = argparse.ArgumentParser(
        description="Upload categories to PrestaShop via WebService API"
    )

    parser.add_argument(
        "--api-url",
        default="http://localhost:8080/api/categories",
        help="PrestaShop API URL (e.g., https://yourshop.com/api/categories)",
    )

    parser.add_argument("--api-key", required=True,
                        help="PrestaShop API key (32 characters)")

    parser.add_argument(
        "--xml-dir",
        default="../data/categories_xml",
        help="Directory containing category XML files",
    )

    args = parser.parse_args()

    xml_dir = Path(args.xml_dir)

    if not xml_dir.exists():
        print(f"Error: Directory {xml_dir} does not exist")
        return

    xml_files = sorted(
        xml_dir.glob("*.xml"),
        key=lambda p: int(p.stem)
    )


    if not xml_files:
        print(f"No XML files found in {xml_dir}")
        return

    print("=== PrestaShop Category Upload (Sequential) ===")
    print(f"Found {len(xml_files)} XML files")
    print(f"API URL: {args.api_url}")
    print("\nUploading categories one by one...\n")

    # Log file
    log_path = Path("upload_log.txt")
    with log_path.open("a", encoding="utf-8") as log:

        log.write("\n===========================================\n")
        log.write(f"UPLOAD START: {datetime.now()}\n")
        log.write("===========================================\n\n")

        success_count = 0
        failed_count = 0
        failed_files = []

        # Upload sequentially (IMPORTANT!)
        for xml_file in xml_files:

            success, filename, error, response = upload_category(
                xml_file, args.api_url, args.api_key
            )

            if success:
                msg = f"✓ {filename}"
                print(msg)
                log.write(msg + "\n")
                success_count += 1
            else:
                msg = f"✗ {filename}: {error}"
                print(msg)
                log.write(msg + "\n")
                failed_files.append((filename, error))
                failed_count += 1

        # Summary
        summary = (
            f"\n=== SUMMARY ===\n"
            f"Success: {success_count}\n"
            f"Failed: {failed_count}\n"
            f"Total: {len(xml_files)}\n"
        )

        print(summary)
        log.write(summary + "\n")

        # Failed file list
        if failed_files:
            print("Failed files:")
            log.write("Failed files:\n")

            for filename, error in failed_files:
                msg = f"  - {filename}: {error}"
                print(msg)
                log.write(msg + "\n")

        log.write("\nUPLOAD END\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\nFatal Error: {e}")
