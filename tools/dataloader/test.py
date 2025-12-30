from category import Category
from product import Product

# cat = Category("name", 0)
# cat_xml = cat.to_xml()

# print(cat_xml)

prod = Product("product", 100.12, "description", "<p>description</p>", 2)
prod_xml = prod.to_xml()

print(prod_xml)