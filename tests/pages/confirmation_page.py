from selenium.webdriver.common.by import By
from .base_page import BasePage


class ConfirmationPage(BasePage):
    INVOICE_LINK = (By.CSS_SELECTOR, "#content-hook_order_confirmation a")

    def download_invoice(self) -> None:
        self.click(self.INVOICE_LINK)
