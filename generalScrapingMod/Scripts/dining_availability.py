from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

MAIN_SITE = "https://dineoncampus.com/unccharlotte/"
driver = Chrome()
wait_for_element = WebDriverWait(driver, 10)

def load_site():
    try:
        driver.get(MAIN_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")

    # try:
    #     upcoming_events = driver.find_element(By.XPATH,".//a[contains(text(),'Upcoming')]")
    #     upcoming_events.click()
    # except (NoSuchElementException,ElementClickInterceptedException) as ex:
    #     #log a warning here
    #     print(f"There was an exception {ex}")
    driver.implicitly_wait(5)

    #outline = driver.find_element(By.XPATH, ".//div[contains(@class, 'col')]")
    dining = driver.find_elements(By.XPATH, ".//div[contains(@class,'row whats-open-tile_hours')]")
    #driver.implicitly_wait(3)

    if len(dining) == 0:
        print(f"Dining information unavailable from {MAIN_SITE}")
    else:
        for event in dining:
            #Will get the general text div that we can then parse
            try:
                print(event.text, '\n')

            except Exception as ex:
                print(ex)
load_site()
