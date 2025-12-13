from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGO_URI)
db = client["captionbot"]

channels = db.channels
schedules = db.schedules
