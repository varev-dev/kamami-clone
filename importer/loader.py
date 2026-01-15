import ssl
import aiohttp
import asyncio
import os
import xml.etree.ElementTree as ET

from category import Category
from constants import CERTIFICATE_PATH, LOADED_CATEGORIES_JSON, LOADED_PRODUCTS_JSON, PRODUCT_IMAGES_PATH, CATEGORY_IMAGES_PATH

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

    async def load_product(self, session, product, load_variants):
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
                    
                    if load_variants:
                        await self.load_variants(session, product)

                    print(f"Product {product.id}: {product.name}, loaded")
                    return True

            except Exception as e:
                print(f"ERROR [{product.id}: {product.name}]: {e}")
                return False

    async def load_products(self, products_map, load_variants):
        print('Loading products...')

        # delete variants from map
        to_delete = []
        if load_variants:
            for product in products_map.values():
                if product.variant_group is None or product in to_delete:
                    continue
                
                product.variants = [
                    products_map[v['id']]
                    for v in product.variants
                    if v['id'] in products_map and v['name'] != product.variant_name
                ]
                
                for variant in product.variants:
                    to_delete.append(variant)
                    
        for variant in to_delete:
            products_map.pop(variant.kamami_id, None)
        
        products = products_map.values()
        
        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            tasks = [
                self.load_product(session, product, load_variants)
                for product in products
            ]

            await asyncio.gather(*tasks)

        import json
        with open(LOADED_PRODUCTS_JSON, "w", encoding="utf-8") as f:
            data = [prod.to_dict() for prod in products]
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Products loaded and saved to products.json!")
        
    async def load_related(self, products_map):
        print('Loading related products...')
        
        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:
            tasks = []
            for product in products_map.values():
                related = []
                for rel in product.related_products:
                    if rel['id'] in products_map.keys():
                        related.append(products_map[rel['id']])
                        
                if related:
                    tasks.append(self.load_related_products(session, product, related))

            await asyncio.gather(*tasks)

        # import json
        # with open(LOADED_PRODUCTS_JSON, "w", encoding="utf-8") as f:
        #     data = [prod.to_dict() for prod in products]
        #     json.dump(data, f, indent=4, ensure_ascii=False)

        print("Related products loaded!")
        
    async def load_related_products(self, session, product, related_products):
        async with self.semaphore:
            try:
                xml = product.to_xml()
                root = ET.fromstring(xml)
                id_elem = root.find(".//id")
                id_elem.text = str(product.id)
                
                # 2. Usuń istniejące accessories (opcjonalnie)
                associations = root.find(".//associations")
                if associations is None:
                    associations = ET.SubElement(root.find(".//product"), "associations")
                accessories = associations.find("accessories")
                if accessories is not None:
                    associations.remove(accessories)
                accessories = ET.SubElement(associations, "accessories")

                # 3. Dodaj powiązane produkty
                for p in related_products:
                    prod_el = ET.SubElement(accessories, "product")
                    ET.SubElement(prod_el, "id").text = str(p.id)

                # 4. Wyślij PUT z pełnym XML
                xml_str = ET.tostring(root, encoding="utf-8", method="xml")
                async with session.put(
                    f"{self.api_url}/products/{product.id}",
                    data=xml_str,
                    auth=aiohttp.BasicAuth(self.api_key, ""),
                    headers={"Content-Type": "application/xml"},
                ) as resp_put:
                    text = await resp_put.text()
                    if resp_put.status >= 400:
                        raise Exception(f"PUT failed {resp_put.status}: {text}")

                print(f"Product {product.id}: {product.name}, related products updated")
                return True

            except Exception as e:
                print(f"ERROR [{product.id}: {product.name}]: {e}")
                return False

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
                        
    async def load_variants(self, session, product):
        if not product.variant_group or not product.variants:
            return

        group_id = await self.create_attribute_group(session, product.variant_group)

        for variant in product.variants:
            value_id = await self.create_attribute_value(
                session, group_id, variant.variant_name
            )

            await self.create_combination(
                session,
                product,
                variant,
                value_id
            )
            
    async def set_default_combination(self, session, product, combination_id):
        xml = f"""
        <prestashop>
        <product>
            <id_product_attribute>{combination_id}</id_product_attribute>
        </product>
        </prestashop>
        """

        async with session.put(
            f"{self.api_url}/products/{product.id}",
            data=xml.encode(),
            auth=aiohttp.BasicAuth(self.api_key, ""),
            headers={"Content-Type": "application/xml"},
        ) as resp:
            if resp.status >= 400:
                text = await resp.text()
                raise Exception(f"Error setting default combination: {resp.status} {text}")
                        
    async def create_combination(self, session, product, variant, option_value_id):
        xml = f"""
        <prestashop>
            <product_combination>
                <id_product>{product.id}</id_product>
                <quantity>{variant.quantity or 0}</quantity>
                <price>{variant.price - product.price}</price>
                <reference>{variant.name}</reference>
                <associations>
                    <product_option_values>
                        <product_option_value>
                            <id>{option_value_id}</id>
                        </product_option_value>
                    </product_option_values>
                </associations>
            </product_combination>
        </prestashop>
        """

        async with session.post(
            f"{self.api_url}/combinations",
            data=xml.encode(),
            auth=aiohttp.BasicAuth(self.api_key, ""),
            headers={"Content-Type": "application/xml"},
        ):
            pass

    async def create_attribute_value(self, session, group_id, value_name):
        xml = f"""
        <prestashop>
            <product_option_value>
                <id_attribute_group>{group_id}</id_attribute_group>
                <name>
                    <language id="1">{value_name}</language>
                    <language id="2">{value_name}</language>
                </name>
            </product_option_value>
        </prestashop>
        """

        async with session.post(
            f"{self.api_url}/product_option_values",
            data=xml.encode(),
            auth=aiohttp.BasicAuth(self.api_key, ""),
            headers={"Content-Type": "application/xml"},
        ) as resp:
            root = ET.fromstring(await resp.text())
            return int(root.find(".//id").text)
                    
    async def create_attribute_group(self, session, group_name):
        public_name = group_name if len(group_name) <= 64 else group_name[:64] # 64 to max liczba znakow dla public_name

        xml = f"""
        <prestashop>
            <product_option>
                <name>
                    <language id="1">{group_name}</language>
                    <language id="2">{group_name}</language>
                </name>
                <public_name>
                    <language id="1">{public_name}</language>
                    <language id="2">{public_name}</language>
                </public_name>
                <group_type>radio</group_type>
            </product_option>
        </prestashop>
        """

        async with session.post(
            f"{self.api_url}/product_options",
            data=xml.encode(),
            auth=aiohttp.BasicAuth(self.api_key, ""),
            headers={"Content-Type": "application/xml"},
        ) as resp:
            root = ET.fromstring(await resp.text())
            return int(root.find('.//id').text)
                    
    async def _upload_product_image(self, session, product_id, image_path):
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
                
    async def _upload_category_image(self, session, category_id, image_path):
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
                        f"{self.api_url}/images/categories/{category_id}",
                        data=data,
                        auth=aiohttp.BasicAuth(self.api_key, ""),
                    ) as response:

                        if response.status not in (200, 201):
                            text = await response.text()
                            raise Exception(f"{response.status}: {text}")

                    print(f"Product {category_id}: image uploaded → {os.path.basename(image_path)}")

            except Exception as e:
                print(f"ERROR [IMAGE {category_id}]: {e}")
                                
    async def load_product_images(self, products):
        print("Loading products images...")

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
                        f"{PRODUCT_IMAGES_PATH}/{product.images_id}"
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
                        self._upload_product_image(
                            session,
                            product.id,
                            image_path
                        )
                    )

            await asyncio.gather(*tasks)

        print("Product images loaded")

    async def load_category_images(self, categories):
        print("Loading category images...")

        async with aiohttp.ClientSession(
            connector=self.connector,
            timeout=self.timeout
        ) as session:

            tasks = []

            for category in categories:
                if not category.image:
                    continue
                
                image_file = f"{CATEGORY_IMAGES_PATH}/{category.image}"

                if not os.path.isfile(image_file):
                    print(f"No image for category {category.id}: {image_file}")
                    continue

                tasks.append(
                    self._upload_category_image(
                        session,
                        category.id,
                        image_file
                    )
                )

            await asyncio.gather(*tasks)

        print("Category images loaded")