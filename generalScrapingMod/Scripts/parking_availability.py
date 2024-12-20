from selenium.webdriver import Chrome
from selenium.common.exceptions import TimeoutException,NoSuchElementException,NoSuchAttributeException,ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database.parking_insertion import insert_parking_data
from selenium.webdriver.chrome.options import Options

MAIN_SITE = "https://parkingavailability.charlotte.edu/"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = Chrome(options=chrome_options)
wait_for_element = WebDriverWait(driver, 10)
def load_site():
    try:
        driver.get(MAIN_SITE)
    except TimeoutException:
        print(f"Loading took too long for site {MAIN_SITE}")

    events = driver.find_elements(By.XPATH, ".//div[contains(@class,'mat-list-item-content')]")
    if len(events) == 0:
        print(f"No events found on site {MAIN_SITE}")
    else:
        for event in events:
            #Will get the general text div that we can then parse
            try:
                event_text = event.find_element(By.XPATH,'.//span[@class="deck-name"]').text
                event_per_tag = event.find_element(By.TAG_NAME,'app-percentage')
                event_per_text = event_per_tag.find_element(By.XPATH,'.//div').text.strip()
               # event_title = event.find_element(By.XPATH,"").text
                parking_dict = {
                    "parking_name": event_text,
                    "availability": event_per_text
                }

                insert_parking_data(parking_dict)
                print(f"Parking Deck: {event_text}")
                print(f"Availability: {event_per_text} \n")
            except Exception as ex:
                print(ex)
    print("Scraping completed.")
    return True




def test_parking_run():
    assert load_site() == True


if __name__ == '__main__':
    load_site()
