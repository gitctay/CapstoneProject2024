# Get the database using the method we defined in pymongo_test_insert file
from database.pymongo_get_database import get_database
from datetime import datetime, timedelta

dbname = get_database()
event_data_table = dbname["event_data"]


def insert_event_data(event_dict):
    event = {
        "event_title": event_dict.get("event_title"),
        "event_date": event_dict.get("event_date"),
        "event_meeting": event_dict.get("event_meeting"),
        "event_link": event_dict.get("event_link"),
        "lastAddedAt": datetime.now(),
        "expireAt": datetime.now() + timedelta(days=7)
    }

    event_data_table.insert_one(event)
    event_data_table.create_index("expireAt", expireAfterSeconds=0)

# def insert_date_time():
#     item = {
#         "lastAddedAt": datetime.now(),
#         "expireAt": datetime.now() + timedelta(days=7)
#     }
#     event_data_table.insert_one(item)
#
# event_data_table.create_index("expireAt", expireAfterSeconds=0)

def add_dummy_data():
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


# Event Pull Method - COMPLETE
def query_event_data():
    events = event_data_table.find().limit(5)  # Limit to the latest 5 events

    event_list = []
    for event in events:
        event_list.append({
            "title": event.get("event_title"),
            "date": event.get("event_date"),
            "meeting": event.get("event_meeting"),
            "link": event.get("event_link"),
        })
    return event_list

def update_event_data():
    result = event_data_table.update_one({"event_title": "test_update"}, {"$set": {"event_title": "title updated"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_event_data(event_dict):
    event_data_table.delete_one({"event_title": event_dict.event_title})

if __name__ == "__main__":
    filter_dict = {"event_title": "test",
                   "event_date": "2021-07-13T00:00:00.000Z",
                   "event_meeting": "test",
                   "event_link": "test"}
    update_dict = {"$set": {"event_title": "new title"}}
    add_dummy_data()
    query_event_data()
    # delete_event_data(event_dict)
    update_event_data()