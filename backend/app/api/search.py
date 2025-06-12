from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.search import SearchParams, CompanyResponse
from ..database import get_mongo_db
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def calculate_probability_score(company: dict) -> float:
    """Calculate a probability score for the company based on available data."""
    score = 0.0
    
    # Base score for having basic information
    if company.get("name"):
        score += 2.0
    if company.get("industry"):
        score += 1.5
    if company.get("location"):
        score += 1.5
    if company.get("website"):
        score += 1.0
    if company.get("description"):
        score += 1.0
    if company.get("employeeCount"):
        score += 1.0
    if company.get("revenue"):
        score += 1.0
    
    return min(score, 10.0)  # Cap at 10

@router.post("/search", response_model=List[CompanyResponse])
async def search_companies(params: SearchParams, db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> List[CompanyResponse]:
    try:
        # Build query based on provided parameters
        query = {}
        if params.companyName:
            query["name"] = {"$regex": params.companyName, "$options": "i"}
        if params.industry:
            query["industry"] = {"$regex": params.industry, "$options": "i"}
        if params.location:
            query["location"] = {"$regex": params.location, "$options": "i"}
        if params.minEmployees:
            query["employeeCount"] = {"$gte": int(params.minEmployees)}
        if params.maxEmployees:
            query["employeeCount"] = {"$lte": int(params.maxEmployees)}

        # Execute search and convert cursor to list
        results = await db.companies.find(query).to_list(length=None)
        
        # Calculate probability scores and sort
        for result in results:
            result["probabilityScore"] = calculate_probability_score(result)
        
        results.sort(key=lambda x: x.get("probabilityScore", 0), reverse=True)
        
        # Convert to response model
        return [CompanyResponse(**company) for company in results]
        
    except Exception as e:
        logger.error(f"Error searching companies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.options("/search")
async def options_search():
    return {"message": "OK"} 