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
                cat = Category(name, [], root_category_id)
                
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
    
    def process_products(self, data, categories_map, load_products):
        products = []
        for product in data:
            if load_products:
                prod = Product(
                    product['name'], 
                    float(product['price_netto'].replace(" zł Netto", "").replace(',', '.').replace(' ', '')),
                    product['short_description'],
                    product['full_description_html'],
                    categories_map[product['breadcrumb_category']].id,
                    product['id'],
                    related_products=product['related_products']
                )
            else:
                prod = Product.from_dict(product)
            
            products.append(prod)
        
        return products
    
    def read_products(self, categories_map, load_products):
        if load_products:
            json_path = os.getenv('PRODUCTS_JSON_PATH')
        else:
            json_path = LOADED_PRODUCTS_JSON 
        
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return self.process_products(data, categories_map, load_products)
            
        