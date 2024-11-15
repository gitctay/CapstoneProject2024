# Get the database using the method we defined in pymongo_test_insert file
from pymongo_get_database import get_database


def insert_food_hall_data(food_hall_dict):
    dbname = get_database()
    food_hall_data_table = dbname["food_hall_data"]
    item = {
        "food_hall_name": food_hall_dict.get("food_hall_name"),
        "availability": food_hall_dict.get("availability"),
        "location": food_hall_dict.get("location"),
    }

    food_hall_data_table.insert_one(item)

def add_dummy_data():
    dbname = get_database()
    food_hall_data_table = dbname["food_hall_data"]
    item = {
        "food_hall_name": "Social",
        "availability": "50",
        "location": "Student Union",
    }
    item2 = {
        "food_hall_name": "test_delete",
        "availability": "50",
        "location": "Student Union",
    }
    item3 = {
        "food_hall_name": "test_update",
        "availability": "50",
        "location": "Student Union",
    }
    food_hall_data_table.insert_many([item, item2, item3])

def query_food_hall_data():
    dbname = get_database()
    food_hall_data_table = dbname["food_hall_data"]
    food_hall_data = food_hall_data_table.find().limit(5)
    food_hall_list = []
    for parking in food_hall_data:
        food_hall_list.append({
            "food_hall_name": parking.get("food_hall_name"),
            "availability": parking.get("availability"),
            "location": parking.get("location")
        })
    return food_hall_list

    # for event in food_hall_data:
    #     print(event)
    #
    # specific_event = food_hall_data_table.find_one({"event_title": "test"})
    # if specific_event is not None:
    #     print(specific_event)
    # else:
    #     print("No event found with that title")
    #
    # limited_events = food_hall_data_table.find().limit(5)
    # for event in limited_events:
    #   print(event)

def update_food_hall_data():
    dbname = get_database()
    food_hall_data_table = dbname["food_hall_data"]

    result = food_hall_data_table.update_one({"food_hall_name": "test_update"}, {"$set": {"food_hall_name": "title updated"}})
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents")

def delete_food_hall_data(food_hall_dict):
    dbname = get_database()
    food_hall_data_table = dbname["food_hall_data"]
    food_hall_data_table.delete_one({"food_hall_name": food_hall_dict.event_title})

if __name__ == "__main__":
    filter_dict = {"food_hall_name": "test"}
    update_dict = {"$set": {"food_hall_name": "new title"}}
    add_dummy_data()
    query_food_hall_data()
    # delete_food_hall_data(event_dict)
    update_food_hall_data()