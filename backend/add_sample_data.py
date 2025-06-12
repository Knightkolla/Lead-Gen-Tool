import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path=dotenv_path, override=True)

MONGO_DETAILS = os.getenv("MONGO_DETAILS")

if not MONGO_DETAILS:
    print("Error: MONGO_DETAILS environment variable not set. Please set it in your .env file.")
    exit()

def get_mongo_client():
    client = MongoClient(MONGO_DETAILS)
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("MongoDB connection successful!")
        return client
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return None

def add_sample_companies():
    client = get_mongo_client()
    if not client:
        return

    db = client.company_db
    companies_collection = db.companies

    sample_companies = [
        {
            "name": "TechInnovate Solutions",
            "industry": "Software Development",
            "location": "San Francisco, CA",
            "employee_count": 750,
            "revenue": "$150M",
            "website": "techinnovate.com",
            "description": "Leading provider of innovative software solutions.",
            "contact_info": "info@techinnovate.com",
            "probability_score": 8.9,
            "insights_summary": "Strong growth in AI and cloud services."
        },
        {
            "name": "GreenLife Organics",
            "industry": "Agriculture & Food",
            "location": "Boulder, CO",
            "employee_count": 200,
            "revenue": "$50M",
            "website": "greenlifeorganics.com",
            "description": "Sustainable organic food producer.",
            "contact_info": "sales@greenlifeorganics.com",
            "probability_score": 7.5,
            "insights_summary": "Expanding into new sustainable farming techniques."
        },
        {
            "name": "Future Mobility Inc.",
            "industry": "Automotive",
            "location": "Detroit, MI",
            "employee_count": 1500,
            "revenue": "$500M",
            "website": "futuremobility.io",
            "description": "Developing next-generation electric vehicles.",
            "contact_info": "careers@futuremobility.io",
            "probability_score": 9.2,
            "insights_summary": "Recently secured major investment for EV battery research."
        }
    ]

    for company_data in sample_companies:
        if not companies_collection.find_one({"name": company_data["name"]}):
            companies_collection.insert_one(company_data)
            print(f"Added: {company_data['name']}")
        else:
            print(f"Skipped: {company_data['name']} (already exists)")
    
    client.close()
    print("Sample data addition complete.")

if __name__ == "__main__":
    add_sample_companies() 