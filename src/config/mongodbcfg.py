from pymongo import MongoClient
from envcfg import MONGO_DB_URL

cluster = MongoClient(MONGO_DB_URL)
db = cluster.iSpirito
reminders = db.reminders
birthdays = db.birthdays
