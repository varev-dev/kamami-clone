import json
import re
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def create_slug(name):
    """Convert name into SEO-friendly slug."""
    slug = re.sub(r'[^\w\s-]', '', name.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:128]

def prettify_xml(element):
    rough = tostring(element, encoding='utf-8')
    return minidom.parseString(rough).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8")

def create_category_xml(cat_id, parent_id, name, lang_ids=[1,2]):
    prestashop = Element("prestashop")
    prestashop.set("xmlns:xlink", "http://www.w3.org/1999/xlink")

    category = SubElement(prestashop, "category")

    SubElement(category, "id_parent").text = str(parent_id)
    SubElement(category, "active").text = "1"
    SubElement(category, "is_root_category").text = "0"

    # NAME
    name_el = SubElement(category, "name")
    for lang_id in lang_ids:
        SubElement(name_el, "language", {"id": str(lang_id)}).text = name

    # LINK REWRITE
    link = SubElement(category, "link_rewrite")
    for lang_id in lang_ids:
        SubElement(link, "language", {"id": str(lang_id)}).text = create_slug(name)

    # DESCRIPTION
    desc = SubElement(category, "description")
    for lang_id in lang_ids:
        SubElement(desc, "language", {"id": str(lang_id)}).text = ""

    # META TITLE
    meta_title = SubElement(category, "meta_title")
    for lang_id in lang_ids:
        SubElement(meta_title, "language", {"id": str(lang_id)}).text = name

    # META DESCRIPTION
    meta_desc = SubElement(category, "meta_description")
    for lang_id in lang_ids:
        SubElement(meta_desc, "language", {"id": str(lang_id)}).text = ""

    # META KEYWORDS
    meta_keywords = SubElement(category, "meta_keywords")
    for lang_id in lang_ids:
        SubElement(meta_keywords, "language", {"id": str(lang_id)}).text = ""

    return prettify_xml(prestashop)


def process_categories(categories, parent_id, id_counter, xml_dir):
    for cat in categories:
        current_id = id_counter[0]
        id_counter[0] += 1

        xml = create_category_xml(
            cat_id=current_id,
            parent_id=parent_id,
            name=cat["name"]
        )

        # Save as file
        filename = xml_dir / f"{current_id}.xml"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(xml)

        print(f"✓ Created category XML: {current_id} → {cat['name']}")

        # Recursive processing of subcategories
        if cat.get("subcategories"):
            process_categories(cat["subcategories"], current_id, id_counter, xml_dir)


if __name__ == "__main__":
    input_file = Path("../data/categories.json")
    xml_dir = Path("../data/categories_xml")
    xml_dir.mkdir(exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Starting category conversion...\n")

    id_counter = [3]

    process_categories(data, parent_id=2, id_counter=id_counter, xml_dir=xml_dir)

    print("\nDONE!")
    print(f"Saved XML categories to: {xml_dir}")
