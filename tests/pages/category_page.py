from typing import List
from selenium.webdriver.common.by import By
from .base_page import BasePage


class CategoryPage(BasePage):
    PRODUCT_LINKS = (
        By.CSS_SELECTOR,
        ".redfoxProductGrid .product_desc:not(:has(.product-unavailable)) a",
    )

    def get_product_urls(self, amount: int) -> List[str]:
        product_elements = self.find_elements(self.PRODUCT_LINKS)
        urls = [prod.get_attribute("href") for prod in product_elements]
        return urls[:amount]
