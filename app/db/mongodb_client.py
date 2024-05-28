from pymongo import MongoClient
from app.core.config import Settings

config = Settings()

mongodb_client = MongoClient(config.MONGO_URI)
mongodb = mongodb_client[config.MONGO_DB]
