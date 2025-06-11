import os
from typing import Dict, Any
import httpx
import asyncio
from app.database import get_mongo_db
import random
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

class EnrichmentService:
    def __init__(self):
        self.hunter_api_key = os.getenv("HUNTER_API_KEY")
        self.clearbit_api_key = os.getenv("CLEARBIT_API_KEY")
        self.newsapi_api_key = os.getenv("NEWSAPI_API_KEY")

        if not self.hunter_api_key:
            print("Warning: HUNTER_API_KEY not set.")
        if not self.clearbit_api_key:
            print("Warning: CLEARBIT_API_KEY not set.")
        if not self.newsapi_api_key:
            print("Warning: NEWSAPI_API_KEY not set.")

    async def _fetch_external_data(self, domain_or_company_name: str) -> Dict[str, Any]:
        """
        Fetches raw external data from Hunter.io, Clearbit, and NewsAPI.
        Uses domain for Hunter/Clearbit, and company name for NewsAPI.
        """
        hunter_data = None
        clearbit_data = None
        news_data = None

        async with httpx.AsyncClient() as client:
            tasks = []

            # Hunter.io (prefers domain)
            if self.hunter_api_key:
                hunter_url = f"https://api.hunter.io/v2/email-finder?domain={domain_or_company_name}&api_key={self.hunter_api_key}"
                tasks.append(client.get(hunter_url))

            # Clearbit (prefers domain, but can search by name if domain is not provided directly)
            if self.clearbit_api_key:
                clearbit_url = f"https://company.clearbit.com/v2/companies/find?domain={domain_or_company_name}"
                tasks.append(client.get(clearbit_url, auth=(self.clearbit_api_key, '')))

            # NewsAPI (uses query, can be company name)
            if self.newsapi_api_key:
                news_url = "https://newsapi.org/v2/everything"
                news_params = {"q": domain_or_company_name, "pageSize": 1, "apiKey": self.newsapi_api_key}
                tasks.append(client.get(news_url, params=news_params))

            responses = await asyncio.gather(*tasks, return_exceptions=True)

            current_task_index = 0

            if self.hunter_api_key:
                hunter_response = responses[current_task_index]
                if not isinstance(hunter_response, Exception):
                    try:
                        hunter_response.raise_for_status()
                        hunter_data = hunter_response.json()
                    except httpx.HTTPStatusError as e:
                        print(f"Hunter.io API error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        print(f"Error parsing Hunter.io response for {domain_or_company_name}: {e}")
                else:
                    print(f"Hunter.io API call failed for {domain_or_company_name}: {hunter_response}")
                current_task_index += 1

            if self.clearbit_api_key:
                clearbit_response = responses[current_task_index]
                if not isinstance(clearbit_response, Exception):
                    try:
                        clearbit_response.raise_for_status()
                        clearbit_data = clearbit_response.json()
                    except httpx.HTTPStatusError as e:
                        print(f"Clearbit API error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        print(f"Error parsing Clearbit response for {domain_or_company_name}: {e}")
                else:
                    print(f"Clearbit API call failed for {domain_or_company_name}: {clearbit_response}")
                current_task_index += 1

            if self.newsapi_api_key:
                news_response = responses[current_task_index]
                if not isinstance(news_response, Exception):
                    try:
                        news_response.raise_for_status()
                        news_data = news_response.json()
                    except httpx.HTTPStatusError as e:
                        print(f"NewsAPI error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        print(f"Error parsing NewsAPI response for {domain_or_company_name}: {e}")
                else:
                    print(f"NewsAPI call failed for {domain_or_company_name}: {news_response}")
                current_task_index += 1

        return {
            "hunter_data": hunter_data,
            "clearbit_data": clearbit_data,
            "news_data": news_data,
        }

    async def enrich_single_lead(self, company_name: str, db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """Enrich a single lead with additional data"""
        try:
            # First check if we already have enriched data in MongoDB
            existing_data = await db.companies.find_one({"name": company_name})
            if existing_data:
                return {
                    "name": existing_data["name"],
                    "industry": existing_data["industry"],
                    "location": existing_data["location"],
                    "employeeCount": existing_data["employee_count"],
                    "revenue": existing_data["revenue"],
                    "website": existing_data["website"],
                    "description": existing_data.get("description", ""),
                    "contactInfo": existing_data.get("contact_info", ""),
                    "probabilityScore": existing_data.get("probability_score", 0),
                }

            # If no existing data, simulate enrichment
            enriched_data = {
                "name": company_name,
                "industry": "Technology",
                "location": "San Francisco, CA",
                "employeeCount": random.randint(50, 1000),
                "revenue": f"${random.randint(1, 100)}M",
                "website": f"https://{company_name.lower().replace(' ', '')}.com",
                "description": f"Leading {company_name} in technology solutions",
                "contactInfo": f"contact@{company_name.lower().replace(' ', '')}.com",
                "probabilityScore": round(random.uniform(1, 10), 1),
            }

            # Store enriched data in MongoDB
            await db.companies.update_one(
                {"name": company_name},
                {"$set": enriched_data},
                upsert=True
            )

            return enriched_data

        except Exception as e:
            logger.error(f"Error enriching lead {company_name}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to enrich lead: {str(e)}"
            ) 