from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring, parse
from xml.dom import minidom
import json
import re

def clean_price(price_str):
    price_clean = re.sub(r'[^\d,.]', '', price_str.replace(',', '.'))
    try:
        return float(price_clean)
    except ValueError:
        return 0.0

def create_slug(name):
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:128]

# --- Wczytaj mapę kategorii ---
categories_dir = Path('../data/categories_xml')
category_map = {}  # link_rewrite -> id
for cat_file in categories_dir.glob('*.xml'):
    tree = parse(cat_file)
    root = tree.getroot()
    cat_el = root.find('category')
    if cat_el is not None:
        link_el = cat_el.find('link_rewrite/language')
        if link_el is not None and link_el.text:
            link = link_el.text.strip()
            category_map[link] = cat_file.stem  # id kategorii = nazwa pliku

def json_to_prestashop_xml(json_data, lang_id=1, category_id=2):
    prestashop = Element('prestashop')
    prestashop.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

    product = SubElement(prestashop, 'product')
    SubElement(product, 'id').text = ''
    SubElement(product, 'price').text = f"{clean_price(json_data.get('price_netto','0')):.6f}"
    SubElement(product, 'active').text = '1'

    # Name
    name_el = SubElement(product, 'name')
    lang_name = SubElement(name_el, 'language', {'id': str(lang_id)})
    lang_name.text = json_data.get('name','')

    # Short description
    desc_short = SubElement(product, 'description_short')
    lang_short = SubElement(desc_short, 'language', {'id': str(lang_id)})
    lang_short.text = json_data.get('short_description','')

    # Full description
    description = SubElement(product, 'description')
    lang_desc = SubElement(description, 'language', {'id': str(lang_id)})
    lang_desc.text = json_data.get('full_description_html','')

    # Link rewrite
    link_rewrite = SubElement(product, 'link_rewrite')
    lang_link = SubElement(link_rewrite, 'language', {'id': str(lang_id)})
    lang_link.text = create_slug(json_data.get('name',''))

    # Associations
    associations = SubElement(product, 'associations')
    categories = SubElement(associations, 'categories')
    category = SubElement(categories, 'category')
    SubElement(category, 'id').text = str(category_id)

    rough_string = tostring(prestashop, encoding='utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')


if __name__ == "__main__":
    products_dir = Path('../data/products')
    xml_dir = products_dir / 'xml'
    xml_dir.mkdir(exist_ok=True)

    json_files = list(products_dir.glob('*.json'))

    total_products = 0
    total_files = 0

    for json_file in json_files:
        try:
            # Pobierz ID kategorii z nazwy pliku
            category_link = json_file.stem
            category_id = category_map.get(category_link, 2)  # default 2 jeśli brak

            print(f"Processing: {json_file.name} -> category ID {category_id}")

            with open(json_file,'r',encoding='utf-8') as f:
                products = json.load(f)

            for product in products:
                xml = json_to_prestashop_xml(product, lang_id=1, category_id=category_id)
                output_file = xml_dir / f"{product['id']}.xml"
                with open(output_file,'w',encoding='utf-8') as f:
                    f.write(xml)
                total_products += 1

            total_files += 1
            print(f"  ✓ Converted {len(products)} products from {json_file.name}\n")

        except Exception as e:
            print(f"  ✗ Error processing {json_file.name}: {e}\n")

    print(f"\n=== Summary ===")
    print(f"Processed {total_files} JSON files")
    print(f"Created {total_products} XML files")
    print(f"XML files saved to: {xml_dir}")
