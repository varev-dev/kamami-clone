from os import makedirs
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from config import (
    DOWNLOAD_PATH,
    IMPLICIT_WAIT,
    EXPLICIT_WAIT,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
)


@pytest.fixture(scope="function")
def driver():
    makedirs(DOWNLOAD_PATH, exist_ok=True)

    location = ChromeDriverManager().install()
    service = Service(location)
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--accept-lang=pl")
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": DOWNLOAD_PATH,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        },
    )

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
    driver.maximize_window()
    driver.implicitly_wait(IMPLICIT_WAIT)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, EXPLICIT_WAIT)
