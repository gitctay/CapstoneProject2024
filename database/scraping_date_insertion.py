from os.path import exists

from database.pymongo_get_database import get_database
from datetime import datetime, timedelta, timezone

dbname = get_database()
scraping_date = dbname["scraping_date_insertion"]

def insert_last_scraping_date_event():

    data = {
        "event_last_scraping_date": datetime.now(timezone.utc).isoformat(),
        "expireAt": datetime.now(timezone.utc) + timedelta(hours=7)
    }
    scraping_date.insert_one(data)
    scraping_date.create_index("expireAt", expireAfterSeconds=0)

def insert_last_scraping_date_parking():

    data = {
        "parking_last_scraping_date": datetime.now(timezone.utc).isoformat(),
        "expireAt": datetime.now(timezone.utc) + timedelta(minutes=5)
    }
    scraping_date.insert_one(data)
    scraping_date.create_index("expireAt", expireAfterSeconds=0)

def insert_last_scraping_date_dinning():
    data = {
        "dinning_last_scraping_date": datetime.now(timezone.utc).isoformat(),
        "expireAt": datetime.now(timezone.utc) + timedelta(minutes=30)
    }
    scraping_date.insert_one(data)
    scraping_date.create_index("expireAt", expireAfterSeconds=0)

def query_event_data_last_scrapped():
    data = scraping_date.find({"event_last_scraping_date": {"$exists": True}})
    return data

def query_parking_data_last_scraped():
    data = scraping_date.find({"parking_last_scraping_date": {"$exists": True}})
    return data

def query_dining_data_last_scrapped():
    data = scraping_date.find({"dinning_last_scraping_date": {"$exists": True}})
    return data

if __name__ == "__main__":
    insert_last_scraping_date_parking()
    insert_last_scraping_date_dinning()
    insert_last_scraping_date_event()
    query_event_data_last_scrapped()
    query_parking_data_last_scraped()
    query_dining_data_last_scrapped()