from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

MAIN_SITE = "https://campusevents.charlotte.edu/"
SUB_SITE = "https://campusevents.charlotte.edu/calendar"
driver = Chrome()
wait_for_element = WebDriverWait(driver, 10)


def load_site():
    try:
        driver.get(SUB_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")

    # try:
    #     upcoming_events = driver.find_element(By.XPATH,".//a[contains(text(),'Upcoming')]")
    #     upcoming_events.click()
    # except (NoSuchElementException,ElementClickInterceptedException) as ex:
    #     #log a warning here
    #     print(f"There was an exception {ex}")

    events = driver.find_elements(By.XPATH, ".//div[contains(@class,'em-event-instance')]")
    if len(events) == 0:
        print(f"No events found on site {SUB_SITE}")
    else:
        for event in events:
            #Will get the general text div that we can then parse
            try:
                event_text = event.find_element(By.XPATH,'.//div[@class="em-card_text"]')
                event_title = event.find_element(By.XPATH,".//div[@class='em-card_text']//h3/a").text
                print(event_title)
            except Exception as ex:
                print(ex)
load_site()


