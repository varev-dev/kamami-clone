from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import EXPLICIT_WAIT


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Tuple[By, str]) -> List[WebElement]:
        return self.driver.find_elements(*locator)

    def wait_for_element_visible(self, locator: Tuple[By, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: Tuple[By, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: Tuple[By, str]) -> None:
        self.find_element(locator).click()

    def send_keys(self, locator: Tuple[By, str], text: str) -> None:
        self.find_element(locator).send_keys(text)

    def clear_and_send_keys(self, locator: Tuple[By, str], text: str) -> None:
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        return self.find_element(locator).get_attribute(attribute)
