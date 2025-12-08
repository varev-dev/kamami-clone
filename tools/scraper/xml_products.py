import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import re
import random

JSON_FILE = '../data/products_all.json'
OUTPUT_DIR = '../data/products_xml'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def create_product_xml(product):
    prestashop = Element('prestashop')
    prestashop.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    product_el = SubElement(prestashop, 'product')

    SubElement(product_el, 'id')

    SubElement(product_el, 'active').text = '1'
    SubElement(product_el, 'state').text = '1'
    
    SubElement(product_el, 'id_tax_rules_group').text = '1' # 23%

    SubElement(product_el, 'id_shop_default').text = '1'
    SubElement(product_el, 'advanced_stock_management').text = '1'

    price_value = product.get('price_netto', '0').replace(' zł', '').replace(' Netto', '').replace(',', '.')
    try:
        price_value = f"{float(price_value):.6f}"
    except:
        price_value = "0.000000"

    SubElement(product_el, 'price').text = price_value

    name = SubElement(product_el, 'name')
    for lang_id in ["1", "2"]:
        lang_el = SubElement(name, 'language', id=lang_id)
        lang_el.text = product.get('name')

    slug = slugify(product.get('name', 'product'))
    link_rewrite = SubElement(product_el, 'link_rewrite')
    for lang_id in ["1", "2"]:
        lr = SubElement(link_rewrite, 'language', id=lang_id)
        lr.text = slug

    description_long = product.get('description', product.get('short_description', ''))
    description_short = product.get('short_description', '')

    desc = SubElement(product_el, 'description')
    for lang_id in ["1", "2"]:
        SubElement(desc, 'language', id=lang_id).text = description_long

    desc_short = SubElement(product_el, 'description_short')
    for lang_id in ["1", "2"]:
        SubElement(desc_short, 'language', id=lang_id).text = description_short

    meta_keywords_el = SubElement(product_el, 'meta_keywords')
    for lang_id in ["1", "2"]:
        SubElement(meta_keywords_el, 'language', id=lang_id).text = product.get('meta_keywords', 'test')

    category_id = str(product.get('category_id', 2))

    SubElement(product_el, 'id_category_default').text = category_id
    SubElement(product_el, 'show_price').text = str(product.get('show_price', 1))
    SubElement(product_el, 'on_sale').text = str(product.get('on_sale', 0))
    
    associations = SubElement(product_el, 'associations')

    categories_el = SubElement(associations, 'categories')
    category_el = SubElement(categories_el, 'category')
    SubElement(category_el, 'id').text = category_id
    category_el = SubElement(categories_el, 'category')
    SubElement(category_el, 'id').text = '2'

    return prestashop

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    products = json.load(f)

for product in products:
    try:
        xml_element = create_product_xml(product)
        xml_data = tostring(xml_element, encoding='utf-8')
        dom = xml.dom.minidom.parseString(xml_data)
        pretty_xml = dom.toprettyxml(indent="  ", encoding="utf-8")

        product_id = product.get('id', slugify(product.get('name', 'product')))

        product_id = re.sub(r'[^\w\-]+', '_', product_id)
        xml_path = os.path.join(OUTPUT_DIR, f"{product_id}.xml")

        with open(xml_path, 'wb') as f:
            f.write(pretty_xml)

        print(f"Saved XML for '{product.get('name', 'unknown')}' -> {xml_path}")
    except Exception as e:
        print(f"Error processing product {product.get('id', product.get('name', 'unknown'))}: {e}")

