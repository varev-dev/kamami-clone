from slugify import slugify
from utils import prettify_xml
from constants import LANG_IDS

class Product:
    def __init__(self, name, price, description, htmlDescription, categoryId):
        self.name = name
        self.price = price
        self.description = description
        self.htmlDescription = htmlDescription
        self.categoryId = categoryId
        self.link = slugify(name)
        
    def __str__(self):
        return f"""Product (
    name: {self.name}
    price: {self.price}
    category: {self.categoryId}
    link: {self.link}
)"""

    def to_xml(self):
        from xml.etree.ElementTree import Element, SubElement

        prestashop = Element('prestashop')
        prestashop.set('xmlns:xlink', 'http://www.w3.org/1999/xlink')

        product_el = SubElement(prestashop, 'product')

        SubElement(product_el, 'id')

        SubElement(product_el, 'active').text = '1'
        SubElement(product_el, 'state').text = '1'
        
        SubElement(product_el, 'id_tax_rules_group').text = '1' # 23%

        SubElement(product_el, 'id_shop_default').text = '1'
        SubElement(product_el, 'advanced_stock_management').text = '1'

        name = SubElement(product_el, 'name')
        for lang_id in LANG_IDS:
            SubElement(name, "language", {"id": str(lang_id)}).text = self.name

        link_rewrite = SubElement(product_el, 'link_rewrite')
        for lang_id in LANG_IDS:
            SubElement(link_rewrite, "language", {"id": str(lang_id)}).text = self.link

        desc = SubElement(product_el, 'description')
        for lang_id in LANG_IDS:
            SubElement(desc, "language", {"id": str(lang_id)}).text = self.htmlDescription

        desc_short = SubElement(product_el, 'description_short')
        for lang_id in LANG_IDS:
            SubElement(desc_short, "language", {"id": str(lang_id)}).text = self.description

        # meta_keywords_el = SubElement(product_el, 'meta_keywords')
        # for lang_id in LANG_IDS:
        #     SubElement(meta_keywords_el, 'language', id=lang_id).text = keywords 

        SubElement(product_el, 'id_category_default').text = str(self.categoryId)
        SubElement(product_el, 'show_price').text = "1"
        SubElement(product_el, 'on_sale').text = "0"
        
        associations = SubElement(product_el, 'associations')

        categories_el = SubElement(associations, 'categories')
        category_el = SubElement(categories_el, 'category')
        SubElement(category_el, 'id').text = str(self.categoryId)
        category_el = SubElement(categories_el, 'category')
        SubElement(category_el, 'id').text = '2'

        return prettify_xml(prestashop)