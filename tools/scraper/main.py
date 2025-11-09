import json
import time
import os
from random import uniform
from categories import scrape_categories

DEFAULT_OUTPUT_DIR = 'data/'
DEFAULT_OUTPUT_FILE = 'products.json'

def main():
    print("=== Kamami Scraper ===")
    scrape_categories()

if __name__ == '__main__':
    main()