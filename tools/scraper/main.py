import argparse
import sys
from categories import scrape_categories
from products import scrape_all_products

DEFAULT_OUTPUT_DIR = '../data/'
DEFAULT_OUTPUT_FILE = 'products.json'

def main():
    parser = argparse.ArgumentParser(
        description="Kamami.pl scraper – fetch categories and products data"
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
    parser.add_argument(
        "-p", "--per-category",
        type=int,
        default=None,
        dest="per_category",
        help="Limit number of products per category (useful for sampling)"
    )
    parser.add_argument(
        "--no-variants",
        action="store_true",
        help="Skip scraping product variants"
    )
    parser.add_argument(
        "--no-related",
        action="store_true",
        help="Skip scraping related products"
    )
    parser.add_argument(
        "-r", "--related-limit",
        type=int,
        default=None,
        dest="related_limit",
        help="Limit number of related products to scrape per product (e.g., 2 = max 2 related products per item)"
    )
    args = parser.parse_args()

    print("=== Kamami Scraper ===")

    if args.mode in ("categories", "all"):
        print("\n[STEP 1] Scraping categories...")
        scrape_categories()

    if args.mode in ("products", "all"):
        print("\n[STEP 2] Scraping products...")
        
        # Display scraping configuration
        print(f"\nConfiguration:")
        print(f"  - Total products limit: {args.items if args.items else 'unlimited'}")
        print(f"  - Per category limit: {args.per_category if args.per_category else 'unlimited'}")
        print(f"  - Scrape variants: {not args.no_variants}")
        print(f"  - Scrape related products: {not args.no_related}")
        if not args.no_related and args.related_limit:
            print(f"  - Related products limit per product: {args.related_limit}")
        
        scrape_all_products(
            limit=args.items, 
            per_category_limit=args.per_category,
            scrape_variants=not args.no_variants,
            scrape_related=not args.no_related,
            related_limit=args.related_limit
        )

    print("\nDone! All data saved to ../data directory.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
        sys.exit(0)