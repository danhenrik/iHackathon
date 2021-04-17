from pymongo import MongoClient
from config.env import MONGO_DB_URL

cluster = MongoClient(MONGO_DB_URL)
db = cluster.iSpirito
reminders = db.reminders
birthdays = db.birthdays