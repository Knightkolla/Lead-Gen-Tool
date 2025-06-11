from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .api.search import router as search_router
from .api.enrich import router as enrich_router
from .api.insights import router as insights_router
from .api.auth import router as auth_router
from .api.crm import router as crm_router
from .database import get_mongo_db

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(search_router, prefix="/api", tags=["search"])
app.include_router(enrich_router, prefix="/api", tags=["enrich"])
app.include_router(insights_router, prefix="/api", tags=["insights"])
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(crm_router, prefix="/api", tags=["crm"])

@app.post("/api/add_dummy_data", summary="Add dummy company data to the database")
async def add_dummy_data(db = Depends(get_mongo_db)):
    dummy_companies = [
        {
            "name": "Tech Solutions Inc.",
            "industry": "Technology",
            "location": "San Francisco, CA",
            "employee_count": 500,
            "revenue": "$500M",
            "website": "techsolutions.com",
            "description": "A leading software development company.",
            "contact_info": "info@techsolutions.com",
            "probability_score": 8.5,
        },
        {
            "name": "Global Innovations Ltd.",
            "industry": "Manufacturing",
            "location": "New York, NY",
            "employee_count": 1200,
            "revenue": "$1.2B",
            "website": "globalinnovations.com",
            "description": "Innovating in industrial automation.",
            "contact_info": "contact@globalinnovations.com",
            "probability_score": 7.8,
        },
        {
            "name": "Green Energy Corp.",
            "industry": "Renewable Energy",
            "location": "Austin, TX",
            "employee_count": 250,
            "revenue": "$150M",
            "website": "greenenergycorp.com",
            "description": "Developing sustainable energy solutions.",
            "contact_info": "sales@greenenergycorp.com",
            "probability_score": 9.1,
        },
        {
            "name": "MediCare Pharma",
            "industry": "Healthcare",
            "location": "Boston, MA",
            "employee_count": 700,
            "revenue": "$800M",
            "website": "medicarepharma.com",
            "description": "Pharmaceutical research and development.",
            "contact_info": "hr@medicarepharma.com",
            "probability_score": 8.9,
        },
        {
            "name": "Future Retail",
            "industry": "Retail",
            "location": "Los Angeles, CA",
            "employee_count": 3000,
            "revenue": "$2.5B",
            "website": "futureretail.com",
            "description": "Online and offline retail solutions.",
            "contact_info": "support@futureretail.com",
            "probability_score": 7.0,
        },
    ]

    try:
        for company_data in dummy_companies:
            # Check if company already exists to avoid duplicates
            if not db.companies.find_one({"name": company_data["name"]}):
                db.companies.insert_one(company_data)
        return {"message": "Dummy data added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
