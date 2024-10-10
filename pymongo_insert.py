# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database


def insert_event_data(event_dict):
    dbname = get_database()
    event_data_table = dbname["event_data"]
    item = {
        "event_title": event_dict.event_title,
        "event_date": event_dict.event_date,
        "event_meeting": event_dict.event_meeting,
        "event_text": event_dict.event_text,
        "event_a_tag": event_dict.event_a_tag
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
    event_data_table.insert_one(item)

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

    result = event_data_table.update_one({"event_title": "test"}, {"$set": {"event_title": "new title"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_event_data():
    dbname = get_database()
    event_data_table = dbname["event_data"]
    event_data_table.delete_one({"event_title": "test"})

if __name__ == "__main__":
    filter_dict = {"event_title": "test"}
    update_dict = {"$set": {"event_title": "new title"}}
    add_dummy_data()
    query_event_data()
    delete_event_data()
    update_event_data()
    
    

# from dateutil import parser
# dbname = get_database()
# collection_name = dbname["user_1_items"]
# event_data_table = dbname["event_data"]


# item2 = {
#     "event_title": event_dict.event_title,
#     "event_date": event_date,
#     "event_meeting": generalScrapingMod.event_meeting,
#     "event_text": generalScrapingMod.event_text,
#     "event_a_tag": generalScrapingMod.event_a_tag
# }
# event_data_table.insert_one(item2)

# item = {
#   "id": 4,
#   "title": "test",
#   "time": "Saturday",
# }

# event_data_table.insert_one(item)



# expiry_date = '2021-07-13T00:00:00.000Z'
# expiry = parser.parse(expiry_date)
#
# item_3 = {
#   "item_name" : "Bread",
#   "quantity" : 2,
#   "ingredients" : "all-purpose flour",
#   "expiry_date" : expiry
# }
# collection_name.insert_one(item_3)
#
# item_1 = {
#   "_id" : "U1IT00001",
#   "item_name" : "Blender",
#   "max_discount" : "10%",
#   "batch_number" : "RR450020FRG",
#   "price" : 340,
#   "category" : "kitchen appliance"
# }
#
# item_2 = {
#   "_id" : "U1IT00002",
#   "item_name" : "Egg",
#   "category" : "food",
#   "quantity" : 12,
#   "price" : 36,
#   "item_description" : "brown country eggs"
# }
# collection_name.insert_many([item_1,item_2])