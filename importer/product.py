from slugify import slugify
from utils import prettify_xml
from constants import LANG_IDS

import random

class Product:
    def __init__(self, kamami_id, name, price, description, html_description, category_id, images_id, 
                 variants=[], variant_group=None, variant_name=None, related_products=[], id=None, quantity=None):
        self.id = None if id is None else id
        self.kamami_id = kamami_id
        self.name = name
        self.price = price
        self.description = description
        self.html_description = html_description
        self.category_id = category_id
        self.link = slugify(name)
        self.images_id = images_id
        self.quantity = random.randint(0, 10) if quantity is None else quantity
        self.related_products = related_products
        self.variant_group = variant_group
        self.variant_name = variant_name
        self.variants = variants
        
    def __str__(self):
        return f"""Product (
    name: {self.name}
    price: {self.price}
    category: {self.category_id}
    link: {self.link}
    related_count: {len(self.related_products)}
    variant_group: {self.variant_group}
    variant_name: {self.variant_name}
    variants: {self.variants}
)"""

    def to_dict(self):
        variants = []
        for variant in self.variants:
            if isinstance(variant, Product):
                variants.append(variant.to_dict())
            else:
                variants.append(variant)
        
        return {
            "id": self.id,
            "kamami_id": self.kamami_id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "html_description": self.html_description,
            "category_id": self.category_id,
            "link": self.link,
            "images_id": self.images_id,
            "quantity": self.quantity,
            "related_products": self.related_products,
            "variant_group": self.variant_group,
            "variant_name": self.variant_name,
            "variants": variants
        }

    @classmethod
    def from_dict(cls, data):
        variants = []
        for variant_data in data.get('variants', []):
            try:
                variant = cls.from_dict(variant_data)
                variants.append(variant)
            except Exception as e:
                continue
                    
        product = cls(
            id=data['id'],
            kamami_id=data['kamami_id'],
            name=data["name"],
            price=data["price"],
            description=data["description"],
            html_description=data["html_description"],
            category_id=data["category_id"],
            images_id=data["images_id"],
            quantity=data['quantity'],
            related_products=data['related_products'],
            variant_group=data['variant_group'],
            variant_name=data['variant_name'],
            variants=variants
        )
        
        return product

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
        
        SubElement(product_el, 'price').text = str(self.price)
        SubElement(product_el, 'available_for_order').text = '1'
        
        SubElement(product_el, 'weight').text = str(random.randint(0, 50))

        name = SubElement(product_el, 'name')
        for lang_id in LANG_IDS:
            SubElement(name, "language", {"id": str(lang_id)}).text = self.name

        link_rewrite = SubElement(product_el, 'link_rewrite')
        for lang_id in LANG_IDS:
            SubElement(link_rewrite, "language", {"id": str(lang_id)}).text = self.link

        desc = SubElement(product_el, 'description')
        for lang_id in LANG_IDS:
            SubElement(desc, "language", {"id": str(lang_id)}).text = self.html_description

        desc_short = SubElement(product_el, 'description_short')
        for lang_id in LANG_IDS:
            SubElement(desc_short, "language", {"id": str(lang_id)}).text = self.description

        # meta_keywords_el = SubElement(product_el, 'meta_keywords')
        # for lang_id in LANG_IDS:
        #     SubElement(meta_keywords_el, 'language', id=lang_id).text = keywords 

        SubElement(product_el, 'id_category_default').text = str(self.category_id)
        SubElement(product_el, 'show_price').text = "1"
        SubElement(product_el, 'on_sale').text = "0"
        
        associations = SubElement(product_el, 'associations')

        categories_el = SubElement(associations, 'categories')
        category_el = SubElement(categories_el, 'category')
        SubElement(category_el, 'id').text = str(self.category_id)
        category_el = SubElement(categories_el, 'category')
        SubElement(category_el, 'id').text = '2'

        return prettify_xml(prestashop)