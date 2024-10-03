from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

days_of_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
MAIN_SITE = "https://campusevents.charlotte.edu/"
SUB_SITE = "https://campusevents.charlotte.edu/calendar"
driver = Chrome()
wait_for_element = WebDriverWait(driver, 10)


def find_element_casual(driver:WebDriver | WebElement,locator,locator_string):
    try:
        element = driver.find_element(locator,locator_string)
        return element
    except NoSuchElementException:
        return None



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
                event_a_tag = event.find_element(By.XPATH,'.//div[@class="em-card_text"]//h3/a')
                event_title = event_a_tag.text.strip()
                event_date = event.find_element(By.XPATH,"(.//p[@class='em-card_event-text'])[1]").text.strip()
                event_meeting = find_element_casual(event,By.XPATH,'.//p[@class="em-card_event-text"][2]')
                if event_meeting is None:
                    print("The event meeting location is not found Defaulting to None")
                else:
                    print(event_meeting.text)
            except Exception as ex:
                print(ex)
load_site()





