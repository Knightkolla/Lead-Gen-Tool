from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from app.database import get_mongo_db
from app.services.scraping_service import ScrapingService # Import the new scraping service

router = APIRouter()

class ScrapeParams(BaseModel):
    industry: Optional[str] = None
    location: Optional[str] = None

@router.post("/scrape_leads", response_model=List[Dict[str, Any]], summary="Scrape B2B leads from the internet")
async def scrape_leads(params: ScrapeParams, db = Depends(get_mongo_db)) -> List[Dict[str, Any]]:
    companies_collection = db.companies
    scraping_service = ScrapingService(companies_collection)
    try:
        scraped_data = await scraping_service.scrape_b2b_leads(industry=params.industry, location=params.location)
        return scraped_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to scrape leads: {e}")

@router.options("/scrape_leads")
async def options_scrape_leads():
    return {"message": "OK"} 