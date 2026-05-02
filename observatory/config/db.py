from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv
# Load variables from .env
load_dotenv()


class MongoDBConfig:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    DB_NAME = os.getenv('DB_NAME', 'spectrum_observatory')


def get_db():
    try:
        # Set a very short timeout so we don't hang if MongoDB is missing
        client = MongoClient(MongoDBConfig.MONGO_URI, serverSelectionTimeoutMS=2000)
        client.server_info() # Trigger a connection check
        return client[MongoDBConfig.DB_NAME]
    except errors.ServerSelectionTimeoutError:
        return None
