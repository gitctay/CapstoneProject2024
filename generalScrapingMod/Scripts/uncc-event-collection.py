from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException



MAIN_SITE = "https://campusevents.charlotte.edu/"

driver = Chrome()

def loadSite():
    try:
        driver.get(MAIN_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")