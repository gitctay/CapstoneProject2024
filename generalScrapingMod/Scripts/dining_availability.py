from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from database.dining_insertion import insert_food_hall_data

MAIN_SITE = "https://dineoncampus.com/unccharlotte/"
driver = Chrome()
wait_for_element = WebDriverWait(driver, 10)

def load_site():
    try:
        driver.get(MAIN_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")
    driver.implicitly_wait(5)

    #outline = driver.find_element(By.XPATH, ".//div[contains(@class, 'col')]")
    dining = driver.find_elements(By.XPATH, ".//div[contains(@class,'row whats-open-tile_hours')]")
    #driver.implicitly_wait(3)

    if len(dining) == 0:
        print(f"Dining information unavailable from {MAIN_SITE}")
    else:
        for event in dining:
            try:
                dining_dict = {
                    "food_hall_name": event.text,
                }
                insert_food_hall_data(dining_dict)
                # print(event.text)
                # hall = driver.find_elements(By.XPATH, "../span[contains(@class,'whats-open-tile_location')]")
                # print(hall, '\n')

            except Exception as ex:
                print(ex)
load_site()
