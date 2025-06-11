from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from ..crm.models import CrmLead, CrmContact
from ..services.crm_service import CRMService

router = APIRouter()
crm_service = CRMService()

@router.post("/crm/lead", summary="Create a new CRM Lead")
async def create_crm_lead(lead_data: CrmLead):
    try:
        response = await crm_service.send_to_crm(lead_data.model_dump(), "lead")
        return {"message": "Lead created successfully", "crm_response": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/crm/contact", summary="Create a new CRM Contact")
async def create_crm_contact(contact_data: CrmContact):
    try:
        response = await crm_service.send_to_crm(contact_data.model_dump(), "contact")
        return {"message": "Contact created successfully", "crm_response": response}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)) 