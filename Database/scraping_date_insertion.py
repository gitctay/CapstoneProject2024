from os.path import exists

from Database.pymongo_get_database import get_database
from datetime import datetime, timedelta

dbname = get_database()
scraping_date = dbname["scraping_date_insertion"]

def insert_last_scraping_date_event():
    data = {
        "event_last_scraping_date": datetime.now().isoformat(),
        "expireAt": datetime.now() + timedelta(days=1)
    }
    scraping_date.insert_one(data)
    scraping_date.create_index("expireAt", expireAfterSeconds=0)

def insert_last_scraping_date_parking():
    data = {
        "parking_last_scraping_date": datetime.now().isoformat()
    }
    scraping_date.insert_one(data)

def insert_last_scraping_date_dinning():
    data = {
        "dinning_last_scraping_date": datetime.now().isoformat()
    }
    scraping_date.insert_one(data)

def query_event_data_last_scrapped():
    data = scraping_date.find({"event_last_scraping_date": {"$exists": True}})
    # cursor = scraping_date.find({"event_last_scraping_date": {"$exists": True}})
    # for dc in cursor:
    #     print(dc)
    #     event_date = datetime.fromisoformat(dc["event_last_scraping_date"])
    #     current_time = datetime.now()
    #     if(event_date > current_time):
    #         print("after")
    #     else:
    #         print("sadas")
    return data

if __name__ == "__main__":
    insert_last_scraping_date_parking()
    insert_last_scraping_date_dinning()
    insert_last_scraping_date_event()
    query_event_data_last_scrapped()