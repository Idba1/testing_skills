"""INTENTIONALLY FLAWED pseudocode-style Selenium example; do not execute."""

import time


def test_login(driver):
    driver.get("https://example.invalid/login")
    driver.find_element("xpath", "/html/body/div[2]/form/input[1]").send_keys("student")
    driver.find_element("xpath", "/html/body/div[2]/form/input[2]").send_keys("example-password")
    driver.find_element("xpath", "/html/body/div[2]/form/button").click()
    time.sleep(10)
    assert True
