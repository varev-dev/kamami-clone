import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from os import getenv

BASE_URL = getenv("BASE_URL", "https://localhost:8443/")


@pytest.fixture(scope="function")
def driver():
    location = ChromeDriverManager().install()
    service = Service(location)
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--accept-lang=pl")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_ecommerce_flow(driver):
    driver.get(BASE_URL)
    assert driver.current_url.startswith(BASE_URL)
