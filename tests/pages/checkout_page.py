from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .base_page import BasePage
from config import BASE_URL


class CheckoutPage(BasePage):
    # Registration form container
    CUSTOMER_FORM = (By.ID, "customer-form")
    
    # Registration form locators (scoped within customer-form)
    FIRST_NAME_INPUT = (By.ID, "field-firstname")
    LAST_NAME_INPUT = (By.ID, "field-lastname")
    EMAIL_INPUT = (By.ID, "field-email")
    PASSWORD_INPUT = (By.ID, "field-password")
    PRIVACY_CHECKBOX = (By.NAME, "customer_privacy")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "[data-link-action='register-new-customer']")

    # Address form locators
    ADDRESS_INPUT = (By.ID, "field-address1")
    POSTCODE_INPUT = (By.ID, "field-postcode")
    CITY_INPUT = (By.ID, "field-city")
    CONFIRM_ADDRESSES_BUTTON = (By.NAME, "confirm-addresses")

    # Delivery form locators
    CONFIRM_DELIVERY_BUTTON = (By.NAME, "confirmDeliveryOption")

    # Payment form locators
    TERMS_CHECKBOX = (By.ID, "conditions_to_approve[terms-and-conditions]")
    PAYMENT_CONFIRMATION_BUTTON = (By.CSS_SELECTOR, "#payment-confirmation button[type='submit']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = f"{BASE_URL}zamówienie"

    def navigate(self) -> None:
        self.navigate_to(self.url)

    def fill_registration_form(self, first_name: str, last_name: str, email: str, password: str) -> None:
        customer_form = self.find_element(self.CUSTOMER_FORM)
        customer_form.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        customer_form.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)
        customer_form.find_element(*self.EMAIL_INPUT).send_keys(email)
        customer_form.find_element(*self.PASSWORD_INPUT).send_keys(password)
        customer_form.find_element(*self.PRIVACY_CHECKBOX).click()

    def submit_registration_form(self) -> None:
        self.click(self.REGISTER_BUTTON)

    def fill_address_form(self, address: str, postcode: str, city: str) -> None:
        self.send_keys(self.ADDRESS_INPUT, address)
        self.send_keys(self.POSTCODE_INPUT, postcode)
        self.send_keys(self.CITY_INPUT, city)

    def submit_address_form(self) -> None:
        self.click(self.CONFIRM_ADDRESSES_BUTTON)

    def select_delivery_option(self, option_id: int) -> None:
        selector = (By.CSS_SELECTOR, f"label[for='delivery_option_{option_id}']")
        try:
            self.click(selector)
        except NoSuchElementException:
            # Fallback to option 1 if selected option is not found
            # (e.g., when cart weight exceeds carrier limits)
            fallback_selector = (By.CSS_SELECTOR, "label[for='delivery_option_1']")
            self.click(fallback_selector)

    def submit_delivery_form(self) -> None:
        self.click(self.CONFIRM_DELIVERY_BUTTON)

    def select_payment_option(self, payment_option_id: int) -> None:
        payment_selector = (By.ID, f"payment-option-{payment_option_id}")
        self.click(payment_selector)
        self.click(self.TERMS_CHECKBOX)

    def submit_payment_form(self) -> None:
        self.click(self.PAYMENT_CONFIRMATION_BUTTON)
