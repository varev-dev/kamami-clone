import os
import json

from category import Category
from product import Product
from constants import LOADED_CATEGORIES_JSON, LOADED_PRODUCTS_JSON

class Reader:
    def __init__(self):
        pass
    
    def process_categories(self, load_categories, categories, root_category_id=2):
        cats = []
        for category in categories:
            name = category['name']
            
            if load_categories:
                image = os.path.basename(category['local_image']) if category['local_image'] else None
                
                cat = Category(name, [], root_category_id, image)
                
                if category.get('subcategories'):
                    cat.subcategories = self.process_categories(
                        load_categories,
                        category['subcategories'],
                        root_category_id
                    )
            else:
                cat = Category.from_dict(category)
                    
            cats.append(cat)
            
        return cats

    def read_categories(self, load_categories):
        if load_categories:
            json_path = os.getenv('CATEGORY_JSON_PATH')
        else:
            json_path = LOADED_CATEGORIES_JSON
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.process_categories(load_categories, data)
    
    def process_products(self, data, categories_map, load_products, limit=1000):
        products = []
        
        for product in data:
            if load_products:
                if product['price_netto'] == "" or product['breadcrumb_category'] not in categories_map.keys():
                    continue
                
                price = float(product['price_netto'].replace(" zł Netto", "").replace(',', '.').replace(' ', ''))
                
                prod = Product(
                    product['id'],
                    product['name'],
                    price,
                    product['short_description'],
                    product['full_description_html'],
                    categories_map[product['breadcrumb_category']].id,
                    product['id'],
                    related_products=product['related_products'],
                    weight=product['weight_kg']
                )
            else:
                prod = Product.from_dict(product)
            
            products.append(prod)
        
        return products, {prod.kamami_id: prod for prod in products}
    
    def read_products(self, categories_map, load_products):
        if load_products:
            json_path = os.getenv('PRODUCTS_JSON_PATH')
        else:
            json_path = LOADED_PRODUCTS_JSON 
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return self.process_products(data, categories_map, load_products)
    
    def limit_products(self, products_map, limit=1000, related_limit=2):
        products = []
        seen = set()

        for product in products_map.values():
            if len(seen) >= limit:
                break
            if product.kamami_id in seen:
                continue

            seen.add(product.kamami_id)
            products.append(product)

            unique_related = []
            for rel in product.related_products:
                if len(unique_related) >= related_limit:
                    break
                if rel['id'] in products_map and rel['id'] not in seen:
                    rp = products_map[rel['id']]
                    unique_related.append(rp)
                    seen.add(rel['id'])
                    products.append(rp)
                    
                    if len(rp.related_products) > 0 and not isinstance(rp.related_products[0], Product):
                        rp.related_products = []
                    
                    rp.related_products.append(product)

            product.related_products = unique_related

        return products, {p.kamami_id: p for p in products}
