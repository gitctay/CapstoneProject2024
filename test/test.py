from generalScrapingMod.Scripts.uncc_event_collection import test_event_collect
from generalScrapingMod.Scripts.dining_availability import test_dining_scrape
from generalScrapingMod.Scripts.parking_availability import test_parking_run
import pytest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
import mongomock
from database.dining_insertion import insert_food_hall_data, add_dummy_data, query_food_hall_data, update_food_hall_data, delete_food_hall_data

# test_parking_run()
# test_dining_scrape()
# test_event_collect()

@pytest.fixture
def mock_db():
    with patch("database.pymongo_get_database.get_database") as mock_get_db:
        mock_get_db.return_value = mongomock.MongoClient().db
        yield mock_get_db.return_value

# mock_db['dinning_data'].delete_many({})

def test_insert_food_hall_data(mock_db):
    food_hall_dict = {
        "food_hall_name": "Test Hall",
        "availability": "Available",
        "status": "Open"
    }

    # Call the function
    insert_food_hall_data(food_hall_dict)

    # Verify the insertion
    inserted_data = mock_db['dinning_data'].find_one({"food_hall_name": "Test Hall"})
    assert inserted_data is not None
    assert inserted_data["availability"] == "Available"
    assert inserted_data["status"] == "Open"

def test_query_food_hall_data(mock_db):
    # Clear database
    mock_db['dinning_data'].delete_many({})

    # Add dummy data
    mock_db['dinning_data'].insert_one({"food_hall_name": "Sample Hall", "availability": "Full", "status": "Closed"})

    # Query
    result = query_food_hall_data()

    # Assert
    assert len(result) == 1
    assert result[0]["food_hall_name"] == "Sample Hall"
    assert result[0]["status"] == "Closed"


def test_update_food_hall_data(mock_db):
    # Add test data
    mock_db['dinning_data'].insert_one({"food_hall_name": "test_update", "availability": "50", "location": "Student Union"})

    # Perform update
    update_food_hall_data()

    # Verify update
    updated_data = mock_db['dinning_data'].find_one({"food_hall_name": "title updated"})
    assert updated_data is not None
    assert updated_data["availability"] == "50"

def test_delete_food_hall_data(mock_db):
    # Add test data
    mock_db['dinning_data'].insert_one({"food_hall_name": "test_delete", "availability": "50", "location": "Student Union"})

    # Perform deletion
    food_hall_dict = {"food_hall_name": "test_delete"}
    delete_food_hall_data(food_hall_dict)

    # Verify deletion
    deleted_data = mock_db['dinning_data'].find_one({"food_hall_name": "test_delete"})
    assert deleted_data is None
