from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List, Dict, Any

class CrmLead(BaseModel):
    # Core Lead Information
    company_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    industry: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    employee_count: Optional[int] = None
    revenue: Optional[str] = None
    
    # CRM Specific Fields (example)
    lead_source: Optional[str] = "Company Search App"
    lead_status: Optional[str] = "New"
    
    # Additional fields to capture from enrichment
    description: Optional[str] = None
    contact_info: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "Tech Solutions Inc.",
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane.doe@techsolutions.com",
                "phone": "+1-555-123-4567",
                "website": "http://techsolutions.com",
                "industry": "Software",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "employee_count": 250,
                "revenue": "$50M",
                "lead_source": "Company Search App",
                "lead_status": "New",
                "description": "A leading software company specializing in AI solutions.",
                "contact_info": "info@techsolutions.com"
            }
        }

class CrmContact(BaseModel):
    # Core Contact Information
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    
    # Association with Company/Account
    company_name: Optional[str] = None # To link to a company/account in CRM
    
    # Additional fields
    title: Optional[str] = None
    linkedin_url: Optional[HttpUrl] = None

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Smith",
                "email": "john.smith@example.com",
                "phone": "+1-555-987-6543",
                "company_name": "Example Corp",
                "title": "Sales Manager",
                "linkedin_url": "http://linkedin.com/in/johnsmith"
            }
        } 