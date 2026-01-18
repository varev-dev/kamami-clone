import time
from random import choice, randint, sample

from pages import (
    HomePage,
    CategoryPage,
    ProductPage,
    SearchPage,
    CartPage,
    CheckoutPage,
    ConfirmationPage,
)
from config import (
    CATEGORY_COUNT,
    PRODUCTS_PER_CATEGORY,
    QUANTITY_RANGE,
    SEARCH_QUERY,
    PRODUCTS_TO_REMOVE,
    DELIVERY_OPTION_ID,
    PAYMENT_OPTION_ID,
    TEST_FIRST_NAME,
    TEST_LAST_NAME,
    TEST_EMAIL,
    TEST_PASSWORD,
    TEST_ADDRESS,
    TEST_POSTCODE,
    TEST_CITY,
)


def test_ecommerce_flow(driver, wait):
    # 1. Home page
    home_page = HomePage(driver)
    home_page.navigate()
    assert driver.current_url.startswith(home_page.url), "Could not navigate to home page"

    # 1.1. Get category URLs
    category_urls = home_page.get_category_urls(CATEGORY_COUNT)
    assert len(category_urls) >= CATEGORY_COUNT, (
        f"Expected at least {CATEGORY_COUNT} categories, got {len(category_urls)}"
    )

    for category_url in category_urls:
        # 2. Category listing page
        category_page = CategoryPage(driver)
        category_page.navigate_to(category_url)

        # 2.1. Get product URLs
        product_urls = category_page.get_product_urls(PRODUCTS_PER_CATEGORY)
        assert len(product_urls) >= PRODUCTS_PER_CATEGORY, (
            f"Expected at least {PRODUCTS_PER_CATEGORY} products, got {len(product_urls)}"
        )

        for product_url in product_urls:
            # 3. Product page - Add products to cart
            quantity = randint(*QUANTITY_RANGE)
            product_page = ProductPage(driver)
            product_page.navigate_to(product_url)
            product_page.add_to_cart(quantity)

    # 4. Search for products
    home_page.search(SEARCH_QUERY)
    
    # 4.1. Verify we're on the search page
    search_page = SearchPage(driver)
    expected_url = search_page.get_search_url(SEARCH_QUERY)
    assert driver.current_url == expected_url, (
        f"Expected to be on search page {expected_url}, got {driver.current_url} instead"
    )

    # 5. Search page - Find and add a random product
    found_product_urls = search_page.get_product_urls(PRODUCTS_PER_CATEGORY)
    assert found_product_urls, "No products found"

    random_product_url = choice(found_product_urls)

    # 5.1. Add the random product to cart
    quantity = randint(*QUANTITY_RANGE)
    product_page = ProductPage(driver)
    product_page.navigate_to(random_product_url)
    product_page.add_to_cart(quantity)

    # 6. Cart page
    cart_page = CartPage(driver)
    cart_page.navigate()

    # 6.1. Get cart item IDs
    cart_item_ids = cart_page.get_cart_item_ids()
    assert cart_item_ids, "The cart is empty"

    # 6.2. Remove some products from cart
    product_ids_to_remove = sample(cart_item_ids, PRODUCTS_TO_REMOVE)
    cart_page.remove_products_by_ids(product_ids_to_remove)

    # TODO: add an assert that checks if proper products were removed

    # 7. Checkout page - Complete multi-step checkout
    checkout_page = CheckoutPage(driver)
    checkout_page.navigate()

    # 7.1. Registration
    checkout_page.fill_registration_form(
        TEST_FIRST_NAME, TEST_LAST_NAME, TEST_EMAIL, TEST_PASSWORD
    )
    checkout_page.submit_registration_form()

    # 7.2. Address
    checkout_page.fill_address_form(TEST_ADDRESS, TEST_POSTCODE, TEST_CITY)
    checkout_page.submit_address_form()

    # 7.3. Delivery
    checkout_page.select_delivery_option(DELIVERY_OPTION_ID)
    checkout_page.submit_delivery_form()

    # 7.4. Payment
    checkout_page.select_payment_option(PAYMENT_OPTION_ID)
    checkout_page.submit_payment_form()

    # 8. Order confirmation page
    confirmation_page = ConfirmationPage(driver)
    confirmation_page.download_invoice()

    # Wait for download to complete
    time.sleep(3)
