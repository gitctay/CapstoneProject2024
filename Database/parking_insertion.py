# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database


def insert_parking_data(parking_dict):
    dbname = get_database()
    parking_data_table = dbname["parking_data"]
    item = {
        "parking_name": parking_dict.get("event_title"),
        "availability": parking_dict.get("event_date"),
        "location": parking_dict.get("event_meeting")
    }

    parking_data_table.insert_one(item)

def add_dummy_data():
    dbname = get_database()
    parking_data_table = dbname["parking_data"]
    item = {
        "event_title": "test",
        "event_date": "2021-07-13T00:00:00.000Z",
        "event_meeting": "test",
        "event_text": "test",
        "event_a_tag": "test"
    }
    item2 = {
        "event_title": "test_delete",
        "event_date": "2021-07-13T00:00:00.000Z",
        "event_meeting": "test",
        "event_text": "test",
        "event_a_tag": "test"
    }
    item3 = {
        "event_title": "test_update",
        "event_date": "2021-07-13T00:00:00.000Z",
        "event_meeting": "test",
        "event_text": "test",
        "event_a_tag": "test"
    }
    parking_data_table.insert_many([item, item2, item3])

def query_parking_data():
    dbname = get_database()
    parking_data_table = dbname["parking_data"]
    parking_data = parking_data_table.find().limit(5)
    parking_list = []
    for parking in parking_data:
        parking_list.append({
            "parking_name": parking.get("parking_name"),
            "availability": parking.get("availability"),
            "location": parking.get("location"),
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
    dbname = get_database()
    parking_data_table = dbname["parking_data"]

    result = parking_data_table.update_one({"event_title": "test_update"}, {"$set": {"event_title": "title updated"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_parking_data(parking_dict):
    dbname = get_database()
    parking_data_table = dbname["parking_data"]
    parking_data_table.delete_one({"event_title": parking_dict.event_title})

if __name__ == "__main__":
    filter_dict = {"event_title": "test"}
    update_dict = {"$set": {"event_title": "new title"}}
    add_dummy_data()
    query_parking_data()
    # delete_parking_data(event_dict)
    update_parking_data()