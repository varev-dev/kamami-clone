from typing import List
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class CartPage(BasePage):
    CART_ITEMS = (By.CSS_SELECTOR, ".cart-grid .remove-from-cart")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{BASE_URL}koszyk?action=show"

    def navigate(self) -> None:
        self.navigate_to(self.url)

    def get_cart_item_ids(self) -> List[str]:
        cart_items = self.find_elements(self.CART_ITEMS)
        return [item.get_attribute("data-id-product") for item in cart_items]

    def remove_products_by_ids(self, product_ids: List[str]) -> None:
        for product_id in product_ids:
            selector = (
                By.CSS_SELECTOR,
                f".cart-grid a.remove-from-cart[data-id-product='{product_id}']",
            )
            href = self.get_attribute(selector, "href")
            self.navigate_to(href)
