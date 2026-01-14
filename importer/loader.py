import ssl
import aiohttp
import asyncio
import os
import xml.etree.ElementTree as ET

from category import Category
from constants import CERTIFICATE_PATH, LOADED_CATEGORIES_JSON, LOADED_PRODUCTS_JSON, IMAGES_PATH

class Loader:
    def __init__(self, concurrent_requests=1):
        self.connector = aiohttp.TCPConnector(
            ssl=ssl.create_default_context(cafile=CERTIFICATE_PATH)
        )
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.semaphore = asyncio.Semaphore(concurrent_requests)

        self.api_key = os.getenv("API_KEY")
        self.api_url = os.getenv("API_URL")

    async def upload_category(self, session, category: Category):
        async with self.semaphore:
            try:
                xml_content = category.to_xml()

                async with session.post(
                    f"{self.api_url}/categories",
                    data=xml_content.encode("utf-8"),
                    auth=aiohttp.BasicAuth(self.api_key, ""),
                    headers={"Content-Type": "application/xml"},
                ) as response:

                    status = response.status
                    response_text = await response.text()
                    
                    if status >= 400:
                        raise Exception(f"HTTP {status}: {response_text.strip()}")

                    root = ET.fromstring(response_text)
                    category_id = root.find(".//id")    
                    
                    if category_id is not None:
                        category.id = int(category_id.text)
                    else:
                        raise ValueError("No category id in response")  

                    print(f"Category {category.id}: {category.name}, loaded")
                    return True

            except Exception as e:
                print(f"ERROR [{category.id}: {category.name}]: {e}")
                return False


    async def load_category_tree(self, session, category: Category):
        success = await self.upload_category(session, category)

        if not success:
            return

        if not category.subcategories:
            return

        for cat in category.subcategories:
            cat.parent_id = category.id

        tasks = [
            self.load_category_tree(session, subcategory)
            for subcategory in category.subcategories
        ]

        await asyncio.gather(*tasks)

    async def load_categories(self, top_categories):
        if not top_categories:
            print("No categories provided")
            return

        print("Loading categories...")
        
        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            tasks = [
                self.load_category_tree(session, category)
                for category in top_categories
            ]

            await asyncio.gather(*tasks)
        
        import json
        with open(LOADED_CATEGORIES_JSON, "w", encoding="utf-8") as f:
            data = [cat.to_dict() for cat in top_categories]
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Categories loaded and saved to categories.json file!")

    async def load_product(self, session, product):
        async with self.semaphore:
            try:
                xml_content = product.to_xml()

                async with session.post(
                    f"{self.api_url}/products",
                    data=xml_content.encode("utf-8"),
                    auth=aiohttp.BasicAuth(self.api_key, ""),
                    headers={"Content-Type": "application/xml"},
                ) as response:
                    status = response.status
                    response_text = await response.text()
                    
                    if status >= 400:
                        raise Exception(f"HTTP {status}: {response_text.strip()}")

                    root = ET.fromstring(response_text)
                    product_id = root.find(".//id")    
                    
                    if product_id is not None:
                        product.id = int(product_id.text)
                    else:
                        raise ValueError("No product id in response")  

                    print(f"Product {product.id}: {product.name}, loaded")
                    return True

            except Exception as e:
                print(f"ERROR [{product.id}: {product.name}]: {e}")
                return False

    async def load_products(self, products):
        print('Loading products...')
        
        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            tasks = [
                self.load_product(session, product)
                for product in products
            ]

            await asyncio.gather(*tasks)

        import json
        with open(LOADED_PRODUCTS_JSON, "w", encoding="utf-8") as f:
            data = [prod.to_dict() for prod in products]
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Products loaded and saved to products.json!")
        
    async def load_stock(self, products):
        print("Loading stock...")

        stock_semaphore = asyncio.Semaphore(1)

        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            for product in products:
                async with stock_semaphore:
                    try:
                        product_id = product.id
                        quantity = product.quantity

                        params = {
                            "filter[id_product]": f"[{product_id}]",
                            "display": "full"
                        }

                        async with session.get(
                            f"{self.api_url}/stock_availables",
                            params=params,
                            auth=aiohttp.BasicAuth(self.api_key, ""),
                            headers={"Content-Type": "application/xml"},
                        ) as response:

                            if response.status != 200:
                                raise Exception("Failed to fetch stock_available")

                            xml = await response.text()
                            root = ET.fromstring(xml)

                            stock_id_el = root.find(".//stock_available/id")
                            if stock_id_el is None:
                                raise ValueError("No stock_available id found")

                            stock_id = stock_id_el.text

                        prestashop = ET.Element(
                            "prestashop",
                            {"xmlns:xlink": "http://www.w3.org/1999/xlink"}
                        )

                        stock_el = ET.SubElement(prestashop, "stock_available")

                        ET.SubElement(stock_el, "id").text = stock_id
                        ET.SubElement(stock_el, "id_product").text = str(product_id)
                        ET.SubElement(stock_el, "id_product_attribute").text = "0"
                        ET.SubElement(stock_el, "id_shop").text = "1"
                        ET.SubElement(stock_el, "quantity").text = str(quantity)
                        ET.SubElement(stock_el, "depends_on_stock").text = "0"
                        ET.SubElement(stock_el, "out_of_stock").text = "2"

                        xml_payload = ET.tostring(
                            prestashop,
                            encoding="utf-8",
                            xml_declaration=True
                        )

                        async with session.put(
                            f"{self.api_url}/stock_availables/{stock_id}",
                            data=xml_payload,
                            auth=aiohttp.BasicAuth(self.api_key, ""),
                            headers={"Content-Type": "application/xml"},
                        ) as response:

                            if response.status not in (200, 201):
                                text = await response.text()
                                raise Exception(f"Stock update failed: {text}")

                        print(f"Product {product_id}: stock set to {quantity}")

                    except Exception as e:
                        print(f"ERROR [STOCK {product.id}]: {e}")
                        
    async def _upload_image(self, session, product_id, image_path):
        async with self.semaphore:
            try:
                with open(image_path, "rb") as f:
                    data = aiohttp.FormData()
                    data.add_field(
                        "image",
                        f,
                        filename=os.path.basename(image_path),
                        content_type="image/jpeg"
                    )

                    async with session.post(
                        f"{self.api_url}/images/products/{product_id}",
                        data=data,
                        auth=aiohttp.BasicAuth(self.api_key, ""),
                    ) as response:

                        if response.status not in (200, 201):
                            text = await response.text()
                            raise Exception(f"{response.status}: {text}")

                    print(f"Product {product_id}: image uploaded → {os.path.basename(image_path)}")

            except Exception as e:
                print(f"ERROR [IMAGE {product_id}]: {e}")
                        
    async def load_images(self, products):
        print("Loading images...")

        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            tasks = []

            for product in products:
                if not product.id:
                    print(f"Skipping images for product without id: {product.name}")
                    continue

                image_dir = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        f"{IMAGES_PATH}/{product.images_id}"
                    )
                )

                if not os.path.isdir(image_dir):
                    print(f"No image directory for product {product.id}: {image_dir}")
                    continue

                for filename in os.listdir(image_dir):
                    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
                        continue

                    image_path = os.path.join(image_dir, filename)

                    tasks.append(
                        self._upload_image(
                            session,
                            product.id,
                            image_path
                        )
                    )

            await asyncio.gather(*tasks)

        print("Images loaded")
