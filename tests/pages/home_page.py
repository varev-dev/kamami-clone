from typing import List
from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class HomePage(BasePage):
    CATEGORY_LINKS = (By.CSS_SELECTOR, ".top_catlink a")
    SEARCH_INPUT = (By.ID, "jss-search-input-text")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = BASE_URL

    def navigate(self) -> None:
        self.navigate_to(self.url)

    def get_category_urls(self, amount: int) -> List[str]:
        category_elements = self.find_elements(self.CATEGORY_LINKS)[:amount]
        return [cat.get_attribute("href") for cat in category_elements]

    def search(self, query: str) -> None:
        search_input = self.find_element(self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(query)
        search_input.submit()
