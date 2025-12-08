
import os
import threading

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Get MongoDB connection URL from environment
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017/")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "alex_file_store")

# Initialize MongoDB client and database
try:
    client = MongoClient(MONGO_URL)
    # Test the connection
    client.admin.command('ping')
    db = client[DATABASE_NAME]
    collection = db["database"]
    print(f"Connected to MongoDB: {DATABASE_NAME}")
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

INSERTION_LOCK = threading.RLock()


class Database:
    """Database document model for MongoDB"""
    
    def __init__(self, id, up_name):
        self.id = str(id)
        self.up_name = up_name
    
    def to_dict(self):
        """Convert to dictionary for MongoDB insertion"""
        return {
            "_id": self.id,
            "up_name": self.up_name
        }
    
    @staticmethod
    def from_dict(data):
        """Create Database object from MongoDB document"""
        if not data:
            return None
        db_obj = Database(data.get("_id"), data.get("up_name", False))
        return db_obj


async def update_as_name(id, mode):
    """Update or insert a document with the given id and mode"""
    with INSERTION_LOCK:
        # Use upsert to update if exists, insert if not
        collection.update_one(
            {"_id": str(id)},
            {"$set": {"up_name": mode}},
            upsert=True
        )


async def get_data(id):
    """Get data for the given id, create if doesn't exist"""
    user_data_dict = collection.find_one({"_id": str(id)})
    
    if not user_data_dict:
        # Create new document
        new_user = Database(str(id), False)
        collection.insert_one(new_user.to_dict())
        user_data_dict = collection.find_one({"_id": str(id)})
    
    return Database.from_dict(user_data_dict)
