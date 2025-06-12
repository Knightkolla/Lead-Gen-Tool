from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from .database import connect_to_mongo, close_mongo_connection, get_mongo_db
from .api import search, enrich, insights, scrape, crm, auth  # Import new scraper router
from dotenv import load_dotenv
import os
import logging
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from .services.leads_service import LeadsService
from .services.insights_service import get_company_insights
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

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
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
    ],
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

# Initialize services
leads_service = LeadsService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await leads_service.initialize()

class LeadCreate(BaseModel):
    name: str
    industry: str
    size: str
    location: str
    website: Optional[str] = None
    description: Optional[str] = None

@app.get("/api/leads")
async def get_leads(sort_by: Optional[str] = None):
    """Get all leads"""
    return leads_service.get_leads(sort_by)

@app.get("/api/leads/{lead_id}")
async def get_lead(lead_id: str):
    lead = leads_service.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@app.post("/api/leads")
async def create_lead(lead: LeadCreate):
    """Create a new lead"""
    try:
        db = await get_mongo_db()
        lead_dict = lead.dict()
        result = await db.companies.insert_one(lead_dict)
        lead_dict["id"] = str(result.inserted_id)
        await leads_service.add_lead(lead_dict)
        return lead_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/leads/{lead_id}")
async def update_lead(lead_id: str, lead: Dict[str, Any]):
    updated_lead = leads_service.update_lead(lead_id, lead)
    if not updated_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return updated_lead

@app.delete("/api/leads/{lead_id}")
async def delete_lead(lead_id: str):
    """Delete a lead"""
    try:
        db = await get_mongo_db()
        result = await db.companies.delete_one({"_id": lead_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Lead not found")
        success = await leads_service.delete_lead(lead_id)
        if not success:
            raise HTTPException(status_code=404, detail="Lead not found")
        return {"message": "Lead deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leads/search")
async def search_leads(q: str):
    """Search leads"""
    try:
        results = await leads_service.search_leads(q)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/leads/{lead_id}/insights")
async def get_lead_insights(lead_id: str):
    lead = leads_service.get_lead_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return get_company_insights(lead)

@app.get("/api/analytics")
async def get_analytics():
    """Get analytics data"""
    try:
        return await leads_service.get_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    return {"message": "OK"}

@app.get("/")
async def root():
    return {"message": "Welcome to the CRM Lead Enrichment API!"}
