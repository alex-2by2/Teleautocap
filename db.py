import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = os.getenv("MONGODB_URI")

client = None
db = None
channels = None

def init_db():
    global client, db, channels
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000
        )
        db = client["captionbot"]
        channels = db.channels

        # test connection
        client.admin.command("ping")
        print("✅ MongoDB connected")

    except ServerSelectionTimeoutError as e:
        print("❌ MongoDB connection failed:", e)
        channels = None
