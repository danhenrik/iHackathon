from pymongo import MongoClient
from env import MONGO_DB_URL

""" Módulo de conexão com o banco de dados """

# Usando a função MongoClient da biblioteca pymongo conectamos a aplicação ao banco de dados (MongoDBAtlas).
cluster = MongoClient(MONGO_DB_URL)
db = cluster.iSpirito

# Puxa as 3 tabelas criadas no cluster até então.
reminders = db.reminders
birthdays = db.birthdays
faq = db.FAQ
