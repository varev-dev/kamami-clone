import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, choice, sample
from os import getenv
import time
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = getenv("BASE_URL", "https://localhost:8443/pl/")

CATEGORY_COUNT = 2
PRODUCTS_PER_CATEGORY = 10
QUANTITY_RANGE = (1, 3)
SEARCH_QUERY = "druk"
PRODUCTS_TO_REMOVE = 3

# Registration form data
TEST_FIRST_NAME = "John"
TEST_LAST_NAME = "Doe"
TEST_EMAIL = "john.doe@example.com"
TEST_PASSWORD = "password"


@pytest.fixture(scope="function")
def driver():
    location = ChromeDriverManager().install()
    service = Service(location)
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--accept-lang=pl")
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)


def get_category_urls(driver, amount):
    category_selector = (By.CSS_SELECTOR, ".top_catlink a")
    category_elems = driver.find_elements(*category_selector)[:amount]
    urls = [cat.get_attribute("href") for cat in category_elems]
    return urls


def add_product(driver, wait, quantity):
    quantity_input = driver.find_element(By.ID, "quantity_wanted")
    quantity_input.clear()
    quantity_input.send_keys(quantity)
    driver.find_element(By.CLASS_NAME, "addcart_text").click()

    # Wait for cart modal to be displayed
    cart_selector = (By.ID, "blockcart-sideview")
    # fully load not present
    wait.until(EC.visibility_of_element_located(cart_selector))


def get_product_urls(driver, amount):
    products_selector = (
        By.CSS_SELECTOR,
        ".redfoxProductGrid .product_desc:not(:has(.product-unavailable)) a",
    )
    products = driver.find_elements(*products_selector)
    urls = [prod.get_attribute("href") for prod in products]
    return urls[:amount]


def search_products(driver, query):
    search_input = driver.find_element(By.ID, "jss-search-input-text")
    search_input.clear()
    search_input.send_keys(query)
    search_input.submit()


def fill_registration_form(driver, first_name, last_name, email, password):
    first_name_input = driver.find_element(By.ID, "field-firstname")
    last_name_input = driver.find_element(By.ID, "field-lastname")
    email_input = driver.find_element(By.ID, "field-email")
    password_input = driver.find_element(By.ID, "field-password")
    privacy_checkbox = driver.find_element(By.NAME, "customer_privacy")

    first_name_input.send_keys(first_name)
    last_name_input.send_keys(last_name)
    email_input.send_keys(email)
    password_input.send_keys(password)
    privacy_checkbox.click()


def submit_registration_form(driver):
    driver.find_element(By.CLASS_NAME, "form-control-submit").click()


def get_cart_item_ids(driver):
    cart_item_ids = driver.find_elements(
        By.CSS_SELECTOR, ".cart-grid .remove-from-cart"
    )

    return [item.get_attribute("data-id-product") for item in cart_item_ids]


def remove_products_from_cart(driver, wait, product_ids):
    for product_id in product_ids:
        selector = (
            By.CSS_SELECTOR,
            f".cart-grid a.remove-from-cart[data-id-product='{product_id}']",
        )
        href = driver.find_element(*selector).get_attribute("href")
        driver.get(href)


def test_ecommerce_flow(driver, wait):
    # 1. Home page
    driver.get(BASE_URL)
    assert driver.current_url.startswith(BASE_URL), "Could not navigate to home page"

    # 1.1. Get category URLs
    category_urls = get_category_urls(driver, CATEGORY_COUNT)
    assert len(category_urls) >= CATEGORY_COUNT, (
        f"Expected at least {CATEGORY_COUNT} categories, got {len(category_urls)}"
    )

    for category_url in category_urls:
        # 2. Listing page
        driver.get(category_url)

        # 2.1. Get product URLs
        product_urls = get_product_urls(driver, PRODUCTS_PER_CATEGORY)
        assert len(product_urls) >= PRODUCTS_PER_CATEGORY, (
            f"Expected at least {PRODUCTS_PER_CATEGORY} products, got {len(product_urls)}"
        )

        for product_url in product_urls:
            # 3. Product page
            quantity = randint(*QUANTITY_RANGE)
            driver.get(product_url)

            # 3.1. Add product to cart
            add_product(driver, wait, quantity)

    # 4.1. Search for products
    search_products(driver, SEARCH_QUERY)
    assert (
        driver.current_url == f"{BASE_URL}szukaj?controller=search&s={SEARCH_QUERY}"
    ), f"Expected to be on search page, got {driver.current_url} instead"

    # 5. Search page (very similar to listing page)
    found_product_urls = get_product_urls(driver, PRODUCTS_PER_CATEGORY)
    assert found_product_urls, "No products found"

    random_product_url = choice(found_product_urls)

    # 5.1. Product page
    driver.get(random_product_url)

    # 5.2. Add the product to cart
    quantity = randint(*QUANTITY_RANGE)
    add_product(driver, wait, quantity)

    # 6. Cart page
    cart_url = f"{BASE_URL}koszyk?action=show"
    driver.get(cart_url)

    # 6.1. Get cart item IDs
    cart_item_ids = get_cart_item_ids(driver)
    assert cart_item_ids, "The cart is empty"

    # 6.2. Remove some products from cart
    product_ids_to_remove = sample(cart_item_ids, PRODUCTS_TO_REMOVE)
    remove_products_from_cart(driver, wait, product_ids_to_remove)

    # TODO: add an assert that checks if proper products were removed

    # 7. Checkout page
    checkout_url = f"{BASE_URL}koszyk?action=checkout"
    driver.get(checkout_url)
