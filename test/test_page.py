from flask import redirect
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

from pathlib import Path
import os

PATH = "/Users/avneetsekhon/Documents/CMPT 473/chromedriver"


def construct_headless_chrome_driver():
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    return webdriver.Chrome(PATH)


def get_landing_page_url():
    test_dir = os.getcwd()
    index_path = os.path.join(test_dir, "..", "page", "index.html")
    index_uri = Path(index_path).as_uri()
    return index_uri



# As demonstrated in the linked web page from the course assignment
@contextmanager
def wait_for_page_load(driver, timeout=30):
    old_page = driver.find_element_by_tag_name('html')
    yield
    WebDriverWait(driver, timeout).until( staleness_of(old_page) )


def test_nonsecret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    # You can place additional test code here to drive this one test
    driver.get(landing_page)
    driver.find_element_by_id("preferredname").send_keys("Avneet")
    driver.find_element_by_id("food").send_keys("Pizza")
    driver.find_element_by_id("secret").send_keys("Test")
    driver.find_element_by_id("submit").click()
    assert driver.find_element_by_id("thankname").text == "Avneet"
    assert driver.find_element_by_id("foodploy").text == "Pizza"
    with pytest.raises(NoSuchElementException):
        assert driver.find_element_by_id("secretButton").click()
    driver.quit()


# You may want to add additional tests....
def test_secret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    # You can place additional test code here to drive this one test
    driver.get(landing_page)
    driver.find_element_by_id("preferredname").send_keys("Avneet")
    driver.find_element_by_id("food").send_keys("Pizza")
    driver.find_element_by_id("secret").send_keys("magic")
    driver.find_element_by_id("submit").click()
    assert driver.find_element_by_id("secretButton").click() is not NoSuchElementException
    assert driver.find_element_by_id("thankname").text == "Avneet"
    #assert driver.find_element_by_id("secret").text == "magic"
    driver.quit()

def test_secondSecret_scenario():
    landing_page = get_landing_page_url()
    driver = construct_headless_chrome_driver()

    # You can place additional test code here to drive this one test
    driver.get(landing_page)
    driver.find_element_by_id("preferredname").send_keys("Avneet")
    driver.find_element_by_id("food").send_keys("Pizza")
    driver.find_element_by_id("secret").send_keys("abracadabra")
    driver.find_element_by_id("submit").click()
    assert driver.find_element_by_id("secretButton").click() is not NoSuchElementException
    assert driver.find_element_by_id("thankname").text == "Avneet"
    #assert driver.find_element_by_id("secret").text == "abracadabra"
    driver.quit()

