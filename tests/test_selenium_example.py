"""Optional browser test. Start the app first and install Chrome + ChromeDriver."""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

@pytest.mark.skipif(os.getenv("RUN_SELENIUM") != "1",
                    reason="Set RUN_SELENIUM=1 to run browser tests.")
def test_home_page_opens_in_chrome():
    driver = webdriver.Chrome()
    try:
        driver.get(os.getenv("APP_URL", "http://127.0.0.1:5000"))
        assert "CarePoint" in driver.title
        assert driver.find_element(By.LINK_TEXT, "Book").is_displayed()
    finally:
        driver.quit()
