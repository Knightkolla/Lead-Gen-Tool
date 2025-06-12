from pydantic import BaseModel, HttpUrl, AnyHttpUrl
from typing import Optional

class SearchParams(BaseModel):
    companyName: Optional[str] = None
    industry: Optional[str] = None
    location: Optional[str] = None
    minEmployees: Optional[int] = None
    maxEmployees: Optional[int] = None

class CompanyResponse(BaseModel):
    name: str
    industry: str
    location: str
    employeeCount: Optional[int] = 0
    revenue: str
    website: Optional[str] = None
    description: Optional[str] = None
    contactInfo: Optional[str] = None
    probabilityScore: Optional[float] = None
    rank: Optional[int] = None
    insightsSummary: Optional[str] = None 