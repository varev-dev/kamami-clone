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
    print("\n[TEST] Starting e-commerce flow test")
    
    # 1. Home page
    home_page = HomePage(driver)
    home_page.navigate()
    assert driver.current_url.startswith(home_page.url), "Could not navigate to home page"

    # 1.1. Get category URLs
    category_urls = home_page.get_category_urls(CATEGORY_COUNT)
    assert len(category_urls) >= CATEGORY_COUNT, (
        f"Expected at least {CATEGORY_COUNT} categories, got {len(category_urls)}"
    )

    print(f"[STEP 1] Adding {PRODUCTS_PER_CATEGORY} products from {CATEGORY_COUNT} categories to cart...")
    products_added = 0
    for category_idx, category_url in enumerate(category_urls, 1):
        category_page = CategoryPage(driver)
        category_page.navigate_to(category_url)

        product_urls = category_page.get_product_urls(PRODUCTS_PER_CATEGORY)
        assert len(product_urls) >= PRODUCTS_PER_CATEGORY, (
            f"Expected at least {PRODUCTS_PER_CATEGORY} products, got {len(product_urls)}"
        )

        for product_url in product_urls:
            quantity = randint(*QUANTITY_RANGE)
            product_page = ProductPage(driver)
            product_page.navigate_to(product_url)
            product_page.add_to_cart(quantity)
            products_added += 1
    
    print(f"         Added {products_added} products to cart")

    print(f"[STEP 2] Searching for '{SEARCH_QUERY}' and adding random product to cart...")
    home_page.search(SEARCH_QUERY)
    
    search_page = SearchPage(driver)
    expected_url = search_page.get_search_url(SEARCH_QUERY)
    assert driver.current_url == expected_url, (
        f"Expected to be on search page {expected_url}, got {driver.current_url} instead"
    )

    found_product_urls = search_page.get_product_urls(PRODUCTS_PER_CATEGORY)
    assert found_product_urls, "No products found"

    random_product_url = choice(found_product_urls)
    quantity = randint(*QUANTITY_RANGE)
    product_page = ProductPage(driver)
    product_page.navigate_to(random_product_url)
    product_page.add_to_cart(quantity)
    print(f"         Added 1 product from search results")

    print(f"[STEP 3] Removing {PRODUCTS_TO_REMOVE} products from cart...")
    cart_page = CartPage(driver)
    cart_page.navigate()

    cart_item_ids = cart_page.get_cart_item_ids()
    assert cart_item_ids, "The cart is empty"
    
    items_before = len(cart_item_ids)
    product_ids_to_remove = sample(cart_item_ids, PRODUCTS_TO_REMOVE)
    cart_page.remove_products_by_ids(product_ids_to_remove)
    print(f"         Cart items: {items_before} -> {items_before - PRODUCTS_TO_REMOVE}")

    print(f"[STEP 4] Registering new account ({TEST_EMAIL})...")
    checkout_page = CheckoutPage(driver)
    checkout_page.navigate()
    checkout_page.fill_registration_form(
        TEST_FIRST_NAME, TEST_LAST_NAME, TEST_EMAIL, TEST_PASSWORD
    )
    checkout_page.submit_registration_form()

    print(f"[STEP 5] Filling address information...")
    checkout_page.fill_address_form(TEST_ADDRESS, TEST_POSTCODE, TEST_CITY)
    checkout_page.submit_address_form()

    print(f"[STEP 6] Selecting delivery option (ID: {DELIVERY_OPTION_ID})...")
    checkout_page.select_delivery_option(DELIVERY_OPTION_ID)
    checkout_page.submit_delivery_form()

    print(f"[STEP 7] Selecting payment method (ID: {PAYMENT_OPTION_ID})...")
    checkout_page.select_payment_option(PAYMENT_OPTION_ID)
    checkout_page.submit_payment_form()

    print(f"[STEP 8] Order confirmed - downloading invoice...")
    confirmation_page = ConfirmationPage(driver)
    confirmation_page.download_invoice()

    time.sleep(3)
    print("[TEST] E-commerce flow test completed successfully ✓")
