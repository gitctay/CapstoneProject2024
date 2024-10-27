# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database


def insert_event_data(event_dict):
    dbname = get_database()
    event_data_table = dbname["event_data"]
    item = {
        "event_title": event_dict.get("event_title"),
        "event_date": event_dict.get("event_date"),
        "event_meeting": event_dict.get("event_meeting"),
        "event_link": event_dict.get("event_link")
    }

    event_data_table.insert_one(item)

def add_dummy_data():
    dbname = get_database()
    event_data_table = dbname["event_data"]
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
    event_data_table.insert_many([item, item2, item3])

def query_event_data():
    dbname = get_database()
    event_data_table = dbname["event_data"]
    event_data = event_data_table.find()
    for event in event_data:
        print(event)

    specific_event = event_data_table.find_one({"event_title": "test"})
    if specific_event is not None:
        print(specific_event) 
    else:
        print("No event found with that title")

    limited_events = event_data_table.find().limit(5)
    for event in limited_events:
      print(event)

def update_event_data():
    dbname = get_database()
    event_data_table = dbname["event_data"]

    result = event_data_table.update_one({"event_title": "test_update"}, {"$set": {"event_title": "title updated"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_event_data(event_dict):
    dbname = get_database()
    event_data_table = dbname["event_data"]
    event_data_table.delete_one({"event_title": event_dict.event_title})

if __name__ == "__main__":
    filter_dict = {"event_title": "test"}
    update_dict = {"$set": {"event_title": "new title"}}
    add_dummy_data()
    query_event_data()
    # delete_event_data(event_dict)
    update_event_data()