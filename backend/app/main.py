from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from .database import connect_to_mongo, close_mongo_connection
from .api import search, enrich, insights, scrape, crm, auth  # Import new scraper router
from dotenv import load_dotenv
import os
import logging
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file at the backend directory
load_dotenv(override=True) # Ensure .env is loaded at app startup

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB
    await connect_to_mongo()
    yield
    # Close MongoDB connection
    await close_mongo_connection()

app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Allow both Vite ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(search.router, prefix="/api")
app.include_router(enrich.router, prefix="/api")
app.include_router(insights.router, prefix="/api")
app.include_router(scrape.router, prefix="/api") # Include the scrape router
app.include_router(crm.router, prefix="/api") # CRM router already has /crm prefix
app.include_router(auth.router, prefix="/api") # Include the authentication router

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"message": "OK"}

@app.get("/")
async def root():
    return {"message": "Welcome to the CRM Lead Enrichment API!"}
