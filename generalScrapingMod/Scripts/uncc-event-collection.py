import time
import schedule
from selenium.common import ElementNotVisibleException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from generalScrapingMod.Scripts.logging_setup import log_setup
from Database.event_insertion import insert_event_data

MAIN_SITE = "https://campusevents.charlotte.edu/"
SUB_SITE = "https://campusevents.charlotte.edu/calendar/week?card_size=small&order=date&experience="


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


def run_event_collection():
    global driver
    logger = log_setup('event_collection_log.txt')
    driver = Chrome()
    load_site()
    wait_for_element = WebDriverWait(driver, 10)
    
    # Get maximum number of pages for events
    max_page_elem = driver.find_element(By.XPATH,
                                        '(//a[@class="em-pagination-item" and not(contains(@class, "em-pagination-item arrow"))])[last()]')
    max_page_num = int(max_page_elem.get_attribute("innerText").strip())
    current_page_num = 1

    while current_page_num <= max_page_num:
        events = driver.find_elements(By.XPATH, ".//div[contains(@class,'em-event-instance')]")
        if len(events) == 0:
            logger.warning(f"No events found on site {SUB_SITE}")
            break
        next_page_elem = find_element_casual(driver, By.XPATH, ".//a[@aria-label='Next page']")
        for event in events:
            try:
                event_text = event.find_element(By.XPATH, './/div[@class="em-card_text"]')
                event_a_tag = event.find_element(By.XPATH, './/div[@class="em-card_text"]//h3/a')
                event_link = event_a_tag.get_attribute('href')
                event_title = event_a_tag.text.strip()
                event_date = event.find_element(By.XPATH, "(.//p[@class='em-card_event-text'])[1]").text.strip()
                event_meeting = find_element_casual(event, By.XPATH, './/p[@class="em-card_event-text"][2]')

                if event_meeting is None:
                    logger.info("The event meeting location is not found Defaulting to None")
                    event_meeting = "None"
                else:
                    logger.info(f'The event {event_title} will be held at {event_date} at {(event_meeting)}')
                    event_meeting = event_meeting.get_attribute('innerText').strip()

                event_dict = {
                    "event_title": event_title,
                    "event_date": event_date,
                    "event_meeting": event_meeting,
                    "event_link": event_link
                }

                insert_event_data(event_dict)

            except (ElementNotVisibleException, NoSuchElementException) as ex:
                logger.error(
                    f'There was an issue grabbing an element because the element is not visible or does not exist --> {ex}')
                continue
            except Exception as ex:
                logger.error(f'There was an issue grabbing an element because of an unknown exception {ex}')
                continue
        current_page_num += 1
        if next_page_elem is not None:
            next_page_elem.click()
            time.sleep(5)
    
    driver.quit()  # Close the browser after collection
    return True

# Function to run the event collection and log its success
def job():
    print("Starting event collection...")
    run_event_collection()
    print("Event collection completed.")

# Schedule the job every 12 hours
schedule.every(12).hours.do(job)

if __name__ == "__main__":
    # Initial run
    job()  # Run immediately on startup
    while True:
        schedule.run_pending()  # Keep checking for scheduled jobs
        time.sleep(1)  # Wait for a while before checking again