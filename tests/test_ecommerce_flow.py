import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    location = ChromeDriverManager().install()
    service = Service(location)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_ecommerce_flow(driver):
    driver.get("https://www.google.com")
    assert 1 == 1
