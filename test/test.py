from generalScrapingMod.Scripts.uncc_event_collection import test_event_collect
from generalScrapingMod.Scripts.dining_availability import test_dining_scrape
from generalScrapingMod.Scripts.parking_availability import test_parking_run
import pytest
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

@pytest.fixture
def database():
        dbname = get_database()
        yield dbname
        dbname['dinning_data'].delete_many({})
        dbname['parking_data'].delete_many({})
        dbname['event_data'].delete_many({})
        dbname['scraping_date_insertion'].delete_many({})

def test_dining(database):
        dining_table = database['dinning_data']
        mock_data = {
                "availability": "availability",
                "food_hall_name": "food_hall_name",
                "status": "status"
        }
        mock_data_update = {
                "availability": "availability",
                "food_hall_name": "test_update",
                "status": "status"
        }
        insert_food_hall_data(mock_data)
        query_result = list(dining_table.find({"food_hall_name": {"$eq": "food_hall_name"}}))
        assert len(query_result) == 1
        assert query_result[0]["availability"] == "availability"
        delete_food_hall_data(mock_data)
        query_result = list(dining_table.find({"food_hall_name": {"$eq": "food_hall_name"}}))
        assert len(query_result) == 0
        insert_food_hall_data(mock_data_update)
        update_food_hall_data()
        query_result = list(dining_table.find({"food_hall_name": {"$eq": "title updated"}}))
        assert query_result[0]["food_hall_name"] == "title updated"

def test_parking(database):
        parking_table = database['parking_data']
        mock_data = {
                "parking_name": "parking_name",
                "availability": "availability"
        }
        mock_data_update = {
                "parking_name": "test_update",
                "availability": "availability"
        }
        insert_parking_data(mock_data)
        query_result = list(parking_table.find({"parking_name": {"$eq": "parking_name"}}))
        assert len(query_result) == 1
        assert query_result[0]["availability"] == "availability"
        delete_parking_data(mock_data)
        query_result = list(parking_table.find({"parking_name": {"$eq": "parking_name"}}))
        assert len(query_result) == 0
        insert_parking_data(mock_data_update)
        update_parking_data()
        query_result = list(parking_table.find({"parking_name": {"$eq": "title updated"}}))
        assert query_result[0]["parking_name"] == "title updated"

def test_event(database):
        event_table = database['event_data']
        mock_data = {
                "event_title": "event_title",
                "event_date": "event_date",
                "event_meeting": "event_meeting",
                "event_link": "event_link",
                "is_recurring": "is_recurring"
        }
        mock_data_update = {
                "event_title": "test_update",
                "event_date": "event_date",
                "event_meeting": "event_meeting",
                "event_link": "event_link",
                "is_recurring": "is_recurring"
        }
        insert_event_data(mock_data)
        query_result = list(event_table.find({"event_title": {"$eq": "event_title"}}))
        assert len(query_result) == 1
        assert query_result[0]["event_date"] == "event_date"
        delete_event_data(mock_data)
        query_result = list(event_table.find({"event_title": {"$eq": "event_title"}}))
        assert len(query_result) == 0
        insert_event_data(mock_data_update)
        update_event_data()
        query_result = list(event_table.find({"event_title": {"$eq": "title updated"}}))
        assert query_result[0]["event_title"] == "title updated"

def test_last_updated(database):
        scraping_date_insertion_data = database['scraping_date_insertion']
        insert_last_scraping_date_dinning()
        query_result = query_dining_data_last_scrapped()
        size_val = query_result.__sizeof__()
        assert size_val == 16
        insert_last_scraping_date_dinning()
        query_result = query_event_data_last_scrapped()
        size_val = query_result.__sizeof__()
        assert size_val == 16
        insert_last_scraping_date_parking()
        query_result = query_parking_data_last_scraped()
        size_val = query_result.__sizeof__()
        assert size_val == 16
