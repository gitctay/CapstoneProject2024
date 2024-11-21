# Get the database using the method we defined in pymongo_test_insert file
from datetime import datetime, timedelta, timezone

from database.pymongo_get_database import get_database

dbname = get_database()
parking_data_table = dbname["parking_data"]

def insert_parking_data(parking_dict):
    item = {
        "parking_name": parking_dict.get("parking_name"),
        "availability": parking_dict.get("availability"),
        "lastAddedAt": datetime.now(timezone.utc),
        "expireAt": datetime.now(timezone.utc) + timedelta(minutes=5)
    }

    parking_data_table.insert_one(item)
    parking_data_table.create_index("expireAt", expireAfterSeconds=0)

def add_dummy_data():
    item = {
        "parking_name": "East Deck",
        "availability": "50",
    }
    item2 = {
        "parking_name": "test_delete",
        "availability": "50",
    }
    item3 = {
        "parking_name": "test_update",
        "availability": "50",
    }
    parking_data_table.insert_many([item, item2, item3])

def query_parking_data():
    parking_data = parking_data_table.find()
    parking_list = []
    for parking in parking_data:
        parking_list.append({
            "parking_name": parking.get("parking_name"),
            "availability": parking.get("availability")
        })
    return parking_list

    # for parking in parking_data:
    #     print(parking)
    #
    # specific_event = parking_data_table.find_one({"event_title": "test"})
    # if specific_event is not None:
    #     print(specific_event)
    # else:
    #     print("No event found with that title")
    #
    # limited_events = parking_data_table.find().limit(5)
    # for event in limited_events:
    #   print(event)

def update_parking_data():
    result = parking_data_table.update_one({"parking_name": "test_update"}, {"$set": {"parking_name": "title updated"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_parking_data(parking_dict):
    parking_data_table.delete_one({"parking_name": parking_dict.event_title})

if __name__ == "__main__":
    filter_dict = {"parking_name": "test"}
    update_dict = {"$set": {"parking_name": "new title"}}
    add_dummy_data()
    query_parking_data()
    # delete_parking_data(event_dict)
    update_parking_data()