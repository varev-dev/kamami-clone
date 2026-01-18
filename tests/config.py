from os import getenv, path

# Base configuration
BASE_URL = getenv("BASE_URL", "https://localhost:8443/pl/")
DOWNLOAD_PATH = path.abspath("./Resources/downloads")

# Test data configuration
CATEGORY_COUNT = int(getenv("CATEGORY_COUNT", "2"))
PRODUCTS_PER_CATEGORY = int(getenv("PRODUCTS_PER_CATEGORY", "10"))
QUANTITY_RANGE = (1, 3)
SEARCH_QUERY = getenv("SEARCH_QUERY", "druk")
PRODUCTS_TO_REMOVE = int(getenv("PRODUCTS_TO_REMOVE", "3"))

# Checkout configuration
DELIVERY_OPTION_ID = int(getenv("DELIVERY_OPTION_ID", "2"))
PAYMENT_OPTION_ID = int(getenv("PAYMENT_OPTION_ID", "2"))

# Registration form data
TEST_FIRST_NAME = getenv("TEST_FIRST_NAME", "John")
TEST_LAST_NAME = getenv("TEST_LAST_NAME", "Doe")
TEST_EMAIL = getenv("TEST_EMAIL", "john.doe@example.com")
TEST_PASSWORD = getenv("TEST_PASSWORD", "password")

# Address form data
TEST_ADDRESS = getenv("TEST_ADDRESS", "123 Main St")
TEST_POSTCODE = getenv("TEST_POSTCODE", "12-345")
TEST_CITY = getenv("TEST_CITY", "Anytown")

# Selenium configuration
IMPLICIT_WAIT = int(getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(getenv("EXPLICIT_WAIT", "10"))
WINDOW_WIDTH = int(getenv("WINDOW_WIDTH", "1920"))
WINDOW_HEIGHT = int(getenv("WINDOW_HEIGHT", "1080"))
