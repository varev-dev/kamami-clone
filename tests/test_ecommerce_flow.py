import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from random import randint
from selenium.webdriver.support import expected_conditions as EC
from os import getenv


BASE_URL = getenv("BASE_URL", "https://localhost:8443/pl/")

CATEGORY_COUNT = 2
PRODUCTS_PER_CATEGORY = 10
QUANTITY_RANGE = (1, 3)


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


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)


def get_category_urls(driver, amount):
    category_selector = ".top_catlink a"
    category_elems = driver.find_elements(By.CSS_SELECTOR, category_selector)[:amount]
    urls = [cat.get_attribute("href") for cat in category_elems]
    return urls


def add_product(driver, quantity):
    quantity_input = driver.find_element(By.ID, "quantity_wanted")
    quantity_input.clear()
    quantity_input.send_keys(quantity)
    driver.find_element(By.CLASS_NAME, "addcart_text").click()


def get_product_urls(driver, amount):
    products_selector = ".redfoxProductGrid:has(.avail_quantity) a.thumbnail"
    products = driver.find_elements(By.CSS_SELECTOR, products_selector)
    urls = [prod.get_attribute("href") for prod in products]
    return urls[:amount]


def test_ecommerce_flow(driver, wait):
    # 1. Home page
    driver.get(BASE_URL)
    assert driver.current_url.startswith(BASE_URL)

    # 1.1. Get category URLs
    category_urls = get_category_urls(driver, CATEGORY_COUNT)
    assert len(category_urls) >= CATEGORY_COUNT, AssertionError(
        f"Expected at least {CATEGORY_COUNT} categories, got {len(category_urls)}"
    )

    for category_url in category_urls:
        # 2. Category page
        driver.get(category_url)

        # 2.1. Get product URLs
        product_urls = get_product_urls(driver, PRODUCTS_PER_CATEGORY)
        assert len(product_urls) >= PRODUCTS_PER_CATEGORY, AssertionError(
            f"Expected at least {PRODUCTS_PER_CATEGORY} products, got {len(product_urls)}"
        )

        for product_url in product_urls:
            # 3. Product page
            quantity = randint(*QUANTITY_RANGE)
            driver.get(product_url)

            # 3.1. Add product to cart
            add_product(driver, quantity)
