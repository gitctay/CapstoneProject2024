from Database.pymongo_get_database import get_database
from datetime import datetime, timedelta

dbname = get_database()
scraping_date = dbname["scraping_date_insertion"]

def insert_last_scraping_date_event():
    data = {
        "event_last_scraping_date": datetime.now()
    }
    scraping_date.insert_one(data)

def insert_last_scraping_date_parking():
    data = {
        "parking_last_scraping_date": datetime.now()
    }
    scraping_date.insert_one(data)

def insert_last_scraping_date_dinning():
    data = {
        "dinning_last_scraping_date": datetime.now()
    }
    scraping_date.insert_one(data)