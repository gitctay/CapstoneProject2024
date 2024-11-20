import re
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from generalScrapingMod.Scripts.logging_setup import log_setup
from database.dining_insertion import insert_food_hall_data
'selenium.webdriver.support.select.Select'

MAIN_SITE = "https://dineoncampus.com/unccharlotte/"
MENU_SITE = "https://dineoncampus.com/unccharlotte/whats-on-the-menu"
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = Chrome(options=chrome_options)
wait_for_element = WebDriverWait(driver, 10)

def load_site():
    try:
        driver.get(MAIN_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")
        driver.get(MAIN_SITE)
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'.//span[@class="see-more" and contains(text(),"Show 2 closed locations")]').click()


    #outline = driver.find_element(By.XPATH, ".//div[contains(@class, 'col')]")
    dining = driver.find_elements(By.XPATH, ".//div[contains(@class,'row whats-open-tile_hours')]")
    #driver.implicitly_wait(3)

    if len(dining) == 0:
        print(f"Dining information unavailable from {MAIN_SITE}")
    else:
        for event in dining:
            try:
                x = re.search(r"(^.+)\n(Open|Closed)\.(.*)", event.text)
                if (x := re.search(r"(^.+)\n(Open|Closed)\.(.*)", event.text)) is None:
                    return None

                dining_dict = {
                    "food_hall_name": x.group(1),
                    "availability": x.group(2),
                    "status": x.group(3)
                }
                insert_food_hall_data(dining_dict)
                print(x.group(1), '\n', x.group(2), '\n',x.group(3))
                # hall = driver.find_elements(By.XPATH, "../span[contains(@class,'whats-open-tile_location')]")
                # print(hall, '\n')


            except Exception as ex:
                print(ex)

# def load_menu():
#     try:
#         driver.get(MENU_SITE)

load_site()

