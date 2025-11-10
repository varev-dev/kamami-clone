import argparse
import sys
from categories import scrape_categories
from products import scrape_all_products

DEFAULT_OUTPUT_DIR = 'data/'
DEFAULT_OUTPUT_FILE = 'products.json'

def main():
    parser = argparse.ArgumentParser(
        description="Kamami.pl scraper — fetch categories and products data"
    )
    parser.add_argument(
        "--mode",
        choices=["categories", "products", "all"],
        default="all",
        help="Select what to scrape: only categories, only products, or all (default)"
    )
    parser.add_argument(
        "-i", "--items",
        type=int,
        default=None,
        help="Limit total number of products to scrape (useful for testing)"
    )
    args = parser.parse_args()

    print("=== Kamami Scraper ===")

    if args.mode in ("categories", "all"):
        print("\n[STEP 1] Scraping categories...")
        scrape_categories()

    if args.mode in ("products", "all"):
        print("\n[STEP 2] Scraping products...")
        scrape_all_products(limit=args.items)

    print("\nDone! All data saved to ./data directory.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
        sys.exit(0)