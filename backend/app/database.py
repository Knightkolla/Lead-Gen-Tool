from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# MongoDB Connection
MONGO_DETAILS = "mongodb://localhost:27017"

try:
    client = MongoClient(MONGO_DETAILS)
    db = client.company_db  # This is your database name
    # Ping the database to ensure connection
    client.admin.command('ping')
    print("MongoDB connection successful!")
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    raise

def get_mongo_db():
    return db 