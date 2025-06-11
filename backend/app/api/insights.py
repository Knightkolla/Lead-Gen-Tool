from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from ..services.insights_service import get_company_insights

router = APIRouter()

class CompanyInsightsRequest(BaseModel):
    company: Dict[str, Any]

@router.post("/insights")
async def get_insights_for_company(request: CompanyInsightsRequest) -> Dict[str, str]:
    insights = get_company_insights(request.company)
    return insights 