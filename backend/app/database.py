from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
import os

# MongoDB Connection Details
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017/company_db")

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None

async def connect_to_mongo():
    global client, db
    try:
        client = AsyncIOMotorClient(MONGO_DETAILS)
        db = client.company_db  # Your database name
        await client.admin.command('ping')
        print("MongoDB connection successful!")
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise

async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("MongoDB connection closed.")

async def get_mongo_db() -> AsyncIOMotorDatabase:
    global db
    if db is None:
        # This should ideally not happen if lifespan events are correctly configured
        # but provides a fallback for direct dependency injection outside of lifespan
        await connect_to_mongo()
    return db 