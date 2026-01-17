from constants import *
from dotenv import load_dotenv
from reader import Reader

load_dotenv()
    
reader = Reader()

categories = reader.read_categories(True)

all_categories = []

for cat in categories:
    all_categories.extend(cat.unpack())

categories_map = {cat.name: cat for cat in all_categories}

products = reader.read_products(categories_map, False)

for product in products:
    print(products)