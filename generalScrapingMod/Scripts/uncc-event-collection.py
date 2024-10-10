from selenium.webdriver.remote.remote_connection import LOGGER

from loggingTest import log_setup


from selenium.common import ElementNotVisibleException
from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from pymongo_insert import insert_event_data

MAIN_SITE = "https://campusevents.charlotte.edu/"
SUB_SITE = "https://campusevents.charlotte.edu/calendar"

def find_element_casual(driver: WebDriver | WebElement, locator, locator_string):
    try:
        element = driver.find_element(locator, locator_string)
        return element
    except NoSuchElementException:
        return None


def load_site():
    try:
        driver.get(SUB_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")


def run_event_collection(logger):
    logger = log_setup('event_collection_log.txt')
    global driver
    driver = Chrome()
    wait_for_element = WebDriverWait(driver, 10)
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
                #all of the event-meeting data tags are located in the second index.
                event_meeting = find_element_casual(event,By.XPATH,'.//p[@class="em-card_event-text"][2]')
                event_dict = {
                    "event_text": event_text,
                    "event_title": event_title,
                    "event_date": event_date,
                    "event_meeting": event_meeting,
                    "event_a_tag": event_a_tag
                }
                if event_meeting is None:
                    print("The event meeting location is not found Defaulting to None")
                else:
                    print(f'The event {event_title} will be held at {event_date} at {str(event_meeting.text)}')

                insert_event_data(event_dict)

            except (ElementNotVisibleException,NoSuchElementException) as ex:
                logger.error(f'There was an issue grabbing an element because the element is not visible or does not exist --> {ex}')
            except Exception as ex:
                logger.error(f'There was an issue grabbing an element because of an unknown exception {ex}')

