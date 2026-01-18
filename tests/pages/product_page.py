from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductPage(BasePage):
    QUANTITY_INPUT = (By.ID, "quantity_wanted")
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "addcart_text")
    CART_MODAL = (By.ID, "blockcart-sideview")

    def add_to_cart(self, quantity: int) -> None:
        quantity_input = self.find_element(self.QUANTITY_INPUT)
        quantity_input.clear()
        quantity_input.send_keys(str(quantity))
        self.click(self.ADD_TO_CART_BUTTON)
        self.wait_for_element_visible(self.CART_MODAL)
