import pytest

from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_ecommerce_flow(driver):
    driver.get("https://www.google.com")
    assert 1 == 1
