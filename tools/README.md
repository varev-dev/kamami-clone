# PrestaShop Data Import via API

This project allows scraping product and category data from Kamami and adding it to PrestaShop via its API.  

## Generate Prestashop API Key
Go to Prestashop admin dashboard → Advanced Parameters → API/Webservice → Generate Key → Full access to `categories`, `images`, `products`, `stocks` → Save → Enable Webservices → Save 

## Installation

Go to `scraper` folder and install required dependencies:

```bash
pip3 install -r requirements.txt
```
## Scraping Data

Use `main.py` to scrape categories and/or products. You must provide your PrestaShop API key for all scripts except the XML converters.

```bash
python3 main.py --api-key YOUR_API_KEY [OPTIONS]
```

### Available Arguments

- `--mode`: Select what to scrape:
    - categories → only scrape categories
    - products → only scrape products
    - all → scrape both categories and products (default)
- `-i, --items`: Limit total number of products to scrape (useful for testing).
- `-p, --per-category`: Limit number of products per category (useful for sampling).

#### Example

```bash
python3 main.py --api-key YOUR_API_KEY --mode all --items 100 --per-category 20
```

## Converting JSON to XML

After scraping, convert the JSON output to XML:
```bash
python3 xml_categories.py
python3 xml_products.py
```

## Adding Data to PrestaShop

Once JSON/XML files are ready, add them to PrestaShop:
```bash
python3 add_categories.py --api-key YOUR_API_KEY
python3 add_products.py --api-key YOUR_API_KEY
```

## Post-Product Addition Tasks

After adding products, you can update stock and download images:
```bash
python3 change_stock.py --api-key YOUR_API_KEY
python3 add_images.py --api-key YOUR_API_KEY
```