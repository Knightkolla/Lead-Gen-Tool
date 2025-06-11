from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Any

from ..services.enrichment_service import EnrichmentService
from ..database import get_mongo_db # Import the get_mongo_db function

router = APIRouter()

enrichment_service = EnrichmentService()

class EnrichRequest(BaseModel):
    companyName: str

@router.post('/enrich')
async def enrich_lead(request: EnrichRequest, db: Any = Depends(get_mongo_db)): # Add db dependency
    if not request.companyName:
        raise HTTPException(status_code=400, detail="Company name not provided for enrichment.")

    # Use the enrichment service to process the lead, passing the db object
    enriched_result = await enrichment_service.enrich_single_lead(request.companyName, db)
    
    if not enriched_result:
        raise HTTPException(status_code=404, detail="Company not found or could not be enriched.")

    return enriched_result 