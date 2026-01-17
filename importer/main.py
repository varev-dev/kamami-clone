from reader import Reader
from loader import Loader
from dotenv import load_dotenv

import asyncio
import argparse

load_dotenv()

async def main(args):
    reader = Reader()
    loader = Loader()
    
    top_categories = reader.read_categories(args.categories)

    if args.categories:
        await loader.load_categories(top_categories)
        
    all_categories = []

    for cat in top_categories:
        all_categories.extend(cat.unpack())
        
    if args.category_images:
        await loader.load_category_images(all_categories)
    
    if not args.products and not args.stocks and not args.images and not args.related:
        return
    
    categories_map = {cat.name: cat for cat in all_categories}
    
    products = reader.read_products(categories_map, args.products)
    
    products = [product for product in products if product.variant_group is not None]
    
    products_map = {prod.kamami_id: prod for prod in products}

    if args.products:
        await loader.load_products(products_map, args.variants)
    
    if args.related:
        await loader.load_related(products_map)
    
    if not products:
        return
    
    if args.stocks:
        await loader.load_stock(products)
        
    if args.images:
        await loader.load_product_images(products)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("data_loader")
    parser.add_argument(
        "-i",
        "--images",
        action="store_true",
        default=False,
        required=False, 
        help="Products' images will be loaded"
    )
    
    parser.add_argument(
        "-c",
        "--categories",
        action="store_true",
        default=False,
        required=False,
        help="Categories will be loaded"
    )
    
    parser.add_argument(
        "-x",
        "--category-images",
        action="store_true",
        default=False,
        required=False,
        help="Category images will be loaded"
    )
    
    parser.add_argument(
        "-p",
        "--products",
        action="store_true",
        default=False,
        required=False, 
        help="Products will be loaded"
    )
    
    parser.add_argument(
        "-r",
        "--related",
        action="store_true",
        default=False,
        required=False, 
        help="Related products will be loaded"
    )
    
    parser.add_argument(
        "-v",
        "--variants",
        action="store_true",
        default=False,
        required=False, 
        help="Variants will be loaded"
    )
    
    parser.add_argument(
        "-s",
        "--stocks",
        action="store_true",
        default=False,
        required=False, 
        help="Stocks will be updated"
    )
    
    parser.add_argument(
        "-a",
        "--attributes",
        action="store_true",
        default=False,
        required=False, 
        help="Attributes will be created and updated"
    )
    
    args = parser.parse_args()
    
    asyncio.run(main(args))