from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, BeforeValidator
from typing import List, Optional, Union, Annotated
from bson import ObjectId
from app.database import get_mongo_db

router = APIRouter()

# Custom type for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class SearchParams(BaseModel):
    companyName: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    minEmployees: Optional[Union[int, str]] = None
    maxEmployees: Optional[Union[int, str]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if isinstance(self.minEmployees, str) and self.minEmployees.strip():
            self.minEmployees = int(self.minEmployees)
        if isinstance(self.maxEmployees, str) and self.maxEmployees.strip():
            self.maxEmployees = int(self.maxEmployees)

class CompanyResponse(BaseModel):
    id: PyObjectId = Field(alias="_id") # Map MongoDB's _id to id
    name: str
    industry: Optional[str] = None
    location: Optional[str] = None
    employee_count: Optional[int] = None
    revenue: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    contact_info: Optional[str] = None
    probability_score: Optional[float] = None
    insights_summary: Optional[str] = None
    rank: Optional[int] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "name": "Example Corp",
                "industry": "Technology",
                "location": "San Francisco, CA",
                "employee_count": 500,
                "revenue": "$500M",
                "website": "example.com",
                "description": "A sample company.",
                "contact_info": "contact@example.com",
                "probability_score": 8.5,
                "insights_summary": "Some insights.",
                "rank": 1,
            }
        }

@router.post("/search", response_model=List[CompanyResponse])
async def search_companies(params: SearchParams, db = Depends(get_mongo_db)) -> List[CompanyResponse]:
    query_filter = {}

    if params.companyName:
        query_filter["name"] = {"$regex": params.companyName, "$options": "i"} # Case-insensitive search
    if params.industry:
        query_filter["industry"] = {"$regex": params.industry, "$options": "i"}
    if params.location:
        query_filter["location"] = {"$regex": params.location, "$options": "i"}
    if params.minEmployees is not None:
        query_filter["employee_count"] = {"$gte": params.minEmployees}
    if params.maxEmployees is not None:
        # If both min and max are present, combine them. Otherwise, just use max.
        if "employee_count" in query_filter:
            query_filter["employee_count"]["$lte"] = params.maxEmployees
        else:
            query_filter["employee_count"] = {"$lte": params.maxEmployees}

    results_cursor = db.companies.find(query_filter)
    all_companies = []
    for doc in results_cursor:
        all_companies.append(doc)

    # Sort by probability score for ranking, if available
    ranked_results = sorted(
        [c for c in all_companies if c.get("probability_score") is not None],
        key=lambda x: x.get("probability_score", 0), reverse=True
    )
    unranked_results = [c for c in all_companies if c.get("probability_score") is None]

    # Assign rank to ranked results
    for i, company in enumerate(ranked_results):
        company["rank"] = i + 1
    
    # Combine and return results, ensuring unranked results are at the end
    final_results = ranked_results + unranked_results

    return [CompanyResponse(**company) for company in final_results] 