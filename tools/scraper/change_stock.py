import requests
import random
from lxml import etree
import argparse

API_URL = "https://localhost:8443/api"
API_KEY = ""
HEADERS = {"Content-Type": "application/xml"}

parser = argparse.ArgumentParser(
    description="Adding images"
)
parser.add_argument(
    "--api-key",
    required=True,
    help="PrestaShop API key (32 characters)"
)
args = parser.parse_args()
API_KEY = args.api_key.replace(' ', '')
print(API_KEY)

r = requests.get(f"{API_URL}/products", auth=(API_KEY, ""), verify='../../apache-conf/certs/server.crt')
r.raise_for_status()
root = etree.fromstring(r.content)
product_ids = [int(prod.get("id")) for prod in root.xpath(".//product")]

print(f"Found {len(product_ids)} products")

for product_id in product_ids:
    new_quantity = random.randint(0, 10)

    params = {"filter[id_product]": f"[{product_id}]", "display": "full"}
    response = requests.get(f"{API_URL}/stock_availables", auth=(API_KEY, ""), headers=HEADERS, params=params, verify='../../apache-conf/certs/server.crt')
    if response.status_code != 200:
        print(f"Failed to fetch stock_available for product {product_id}")
        continue

    stock_root = etree.fromstring(response.content)
    stock_ids = stock_root.xpath("//stock_available/id/text()")
    if not stock_ids:
        print(f"No stock_available record for product {product_id}")
        continue

    stock_id = stock_ids[0]

    prestashop = etree.Element("prestashop", nsmap={"xlink": "http://www.w3.org/1999/xlink"})
    stock_available = etree.SubElement(prestashop, "stock_available")

    etree.SubElement(stock_available, "id").text = etree.CDATA(str(stock_id))
    etree.SubElement(stock_available, "id_product").text = etree.CDATA(str(product_id))
    etree.SubElement(stock_available, "id_product_attribute").text = etree.CDATA("0")
    etree.SubElement(stock_available, "id_shop").text = etree.CDATA("1")
    etree.SubElement(stock_available, "quantity").text = etree.CDATA(str(new_quantity))
    etree.SubElement(stock_available, "depends_on_stock").text = etree.CDATA("0")
    etree.SubElement(stock_available, "out_of_stock").text = etree.CDATA("2")

    xml_payload = etree.tostring(prestashop, encoding="utf-8", xml_declaration=True, pretty_print=True)

    patch_url = f"{API_URL}/stock_availables/{stock_id}"
    patch_response = requests.put(patch_url, auth=(API_KEY, ""), headers=HEADERS, data=xml_payload, verify='../../apache-conf/certs/server.crt')

    if patch_response.status_code in (200, 201):
        print(f"Product {product_id}: quantity set to {new_quantity}")
    else:
        print(f"Failed to update product {product_id}: {patch_response.status_code}")
        print(patch_response.text)
