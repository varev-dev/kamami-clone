# PrestaShop Data Import via API

This project allows scraping product and category data from Kamami and adding it to PrestaShop via its API.  

## Generate Prestashop API Key

Go to Prestashop admin dashboard → Advanced Parameters → API/Webservice → Generate Key → Full access to `categories`, `images`, `products`, `stocks_availables` → Save → Enable Webservices → Save. After that in `dataloader` copy `example.env` and rename it to `.env`. In this file set the `API_KEY` argument to the key you just created.

## Installation

Go to `scraper` **AND** `dataloader` folders and install required dependencies:

```bash
pip3 install -r requirements.txt
```
## Scraping Data

Use `scarper/main.py` to scrape categories and/or products.

### Available Arguments

- `--mode`: Select what to scrape:
    - categories → only scrape categories
    - products → only scrape products
    - all → scrape both categories and products (default)
- `-i, --items`: Limit total number of products to scrape (useful for testing).
- `-p, --per-category`: Limit number of products per category (useful for sampling).

#### Example

```bash
python3 main.py --mode all --items 100 --per-category 20
```

## Loading Data via API

Use `dataloader/main.py` to load categories, products, stocks and images. The data has to be loaded in correct order: `Categories → Products → Stocks or/and Images`.

### Available arguments

- `-c, --categories`: Load categories
- `-p, --products`: Load products
- `-s, --stocks`: Load stocks
- `-i, --images`: Load images

#### Example

```bash
python3 main.py -cpsi
```
