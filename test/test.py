from generalScrapingMod.Scripts.uncc_event_collection import test_event_collect
from generalScrapingMod.Scripts.dining_availability import test_dining_scrape
from generalScrapingMod.Scripts.parking_availability import test_parking_run
from database.pymongo_get_database import get_database
from database.dining_insertion import insert_food_hall_data, query_food_hall_data, delete_food_hall_data, update_food_hall_data
from database.event_insertion import insert_event_data, query_event_data, delete_event_data, update_event_data
from database.scraping_date_insertion import insert_last_scraping_date_event, insert_last_scraping_date_dinning, \
        insert_last_scraping_date_parking, query_event_data_last_scrapped, query_parking_data_last_scraped, \
        query_parking_data_last_scraped, query_dining_data_last_scrapped
from database.parking_insertion import insert_parking_data, query_parking_data, delete_parking_data, update_parking_data


test_parking_run()
test_dining_scrape()
test_event_collect()

dbname = get_database()
dining_data_table = dbname['dinning_data']

test_insert_dining = {
        "availability": 'availability',
        "food_hall_name": 'food_hall_name',
        "status": 'status'
}
test_update_dining = {
        "availability": 'availability',
        "food_hall_name": 'test_update',
        "status": 'status'
}
test_delete_dining = {
        "availability": 'availability',
        "food_hall_name": 'test_update',
        "status": 'status'
}
insert_food_hall_data(test_insert_dining)
insert_food_hall_data(test_update_dining)
insert_food_hall_data(test_delete_dining)
update_food_hall_data()
query_food_hall_data()
delete_food_hall_data(test_delete_dining)


event_data_table = dbname["event_data"]
test_insert_event = {
        "event_title": "event_title",
        "event_date": "event_date",
        "event_meeting":"event_meeting",
        "event_link": "event_link",
        "is_recurring": "is_recurring"
}
test_update_event = {
        "event_title": "event_title",
        "event_date": "event_date",
        "event_meeting":"event_meeting",
        "event_link": "event_link",
        "is_recurring": "is_recurring"
}
test_delete_event = {
        "event_title": "test_update",
        "event_date": "event_date",
        "event_meeting":"event_meeting",
        "event_link": "event_link",
        "is_recurring": "is_recurring"
}
insert_event_data(test_insert_event)
insert_event_data(test_update_event)
insert_event_data(test_delete_event)
query_event_data()
update_event_data()
delete_event_data(test_delete_event)


parking_data_table = dbname["parking_data"]
test_insert_parking = {
        "parking_name": "parking_name",
        "availability": "availability"
}
test_update_parking = {
        "parking_name": "test_update",
        "availability": "availability"
}
test_delete_parking = {
        "parking_name": "parking_name",
        "availability": "availability"
}
insert_parking_data(test_insert_parking)
insert_parking_data(test_update_parking)
insert_parking_data(test_delete_parking)
query_parking_data()
update_parking_data()
delete_parking_data(test_delete_parking)


scraping_date = dbname["scraping_date_insertion"]
insert_last_scraping_date_event()
insert_last_scraping_date_dinning()
insert_last_scraping_date_parking()
query_event_data_last_scrapped()
query_parking_data_last_scraped()
query_dining_data_last_scrapped()