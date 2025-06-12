import os
from typing import Dict, Any
import httpx
import asyncio
from app.database import get_mongo_db
import random
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging
from dotenv import load_dotenv

# Get the directory of the current file (enrichment_service.py)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file, assuming it's in the backend/ directory
dotenv_path = os.path.join(current_dir, os.pardir, '.env')

load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

class EnrichmentService:
    def __init__(self):
        self.hunter_api_key = os.getenv("HUNTER_API_KEY")
        self.apollo_api_key = os.getenv("APOLLO_API_KEY")
        self.newsapi_api_key = os.getenv("NEWSAPI_API_KEY")

        if not self.hunter_api_key:
            logger.warning("Warning: HUNTER_API_KEY not set.")
        if not self.apollo_api_key:
            logger.warning("Warning: APOLLO_API_KEY not set. Apollo.io integration will be skipped.")
        if not self.newsapi_api_key:
            logger.warning("Warning: NEWSAPI_API_KEY not set.")

    async def _fetch_external_data(self, domain_or_company_name: str) -> Dict[str, Any]:
        """
        Fetches raw external data from Hunter.io, Apollo.io, and NewsAPI.
        Uses domain for Hunter/Apollo, and company name for NewsAPI.
        """
        hunter_data = None
        apollo_data = None
        news_data = None

        async with httpx.AsyncClient() as client:
            tasks = []

            # Hunter.io (prefers domain)
            if self.hunter_api_key:
                hunter_url = f"https://api.hunter.io/v2/email-finder?domain={domain_or_company_name}&api_key={self.hunter_api_key}"
                tasks.append(client.get(hunter_url))

            # Apollo.io Organization Enrichment (prefers domain/website)
            if self.apollo_api_key:
                apollo_url = "https://api.apollo.io/api/v1/organizations/enrich"
                tasks.append(client.get(
                    apollo_url,
                    params={"website": domain_or_company_name},
                    headers={"X-Api-Key": self.apollo_api_key}
                ))

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
                        logger.error(f"Hunter.io API error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        logger.error(f"Error parsing Hunter.io response for {domain_or_company_name}: {e}")
                else:
                    logger.error(f"Hunter.io API call failed for {domain_or_company_name}: {hunter_response}")
                current_task_index += 1

            if self.apollo_api_key:
                apollo_response = responses[current_task_index]
                if not isinstance(apollo_response, Exception):
                    try:
                        apollo_response.raise_for_status()
                        apollo_data = apollo_response.json()
                    except httpx.HTTPStatusError as e:
                        logger.error(f"Apollo.io API error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        logger.error(f"Error parsing Apollo.io response for {domain_or_company_name}: {e}")
                else:
                    logger.error(f"Apollo.io API call failed for {domain_or_company_name}: {apollo_response}")
                current_task_index += 1

            if self.newsapi_api_key:
                news_response = responses[current_task_index]
                if not isinstance(news_response, Exception):
                    try:
                        news_response.raise_for_status()
                        news_data = news_response.json()
                    except httpx.HTTPStatusError as e:
                        logger.error(f"NewsAPI error for {domain_or_company_name}: {e}")
                    except Exception as e:
                        logger.error(f"Error parsing NewsAPI response for {domain_or_company_name}: {e}")
                else:
                    logger.error(f"NewsAPI call failed for {domain_or_company_name}: {news_response}")
                current_task_index += 1

        return {
            "hunter_data": hunter_data,
            "apollo_data": apollo_data,
            "news_data": news_data,
        }

    async def enrich_single_lead(self, company_name: str, db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """Enrich a single lead with additional data"""
        try:
            # First check if we already have enriched data in MongoDB
            existing_data = await db.companies.find_one({"name": company_name})
            if existing_data and existing_data.get("is_enriched"): # Check if already explicitly enriched
                return {
                    "name": existing_data["name"],
                    "industry": existing_data.get("industry", ""),
                    "location": existing_data.get("location", ""),
                    "employeeCount": existing_data.get("employee_count", 0),
                    "revenue": existing_data.get("revenue", ""),
                    "website": existing_data.get("website", ""),
                    "description": existing_data.get("description", ""),
                    "contactInfo": existing_data.get("contact_info", ""),
                    "probabilityScore": existing_data.get("probability_score", 0),
                }

            # If no existing data or not enriched, fetch external data
            external_data = await self._fetch_external_data(company_name) # Pass company_name as domain/query

            enriched_data = {
                "name": company_name,
                "is_enriched": True,
                "industry": "",
                "location": "",
                "employee_count": 0,
                "revenue": "",
                "website": "",
                "description": "",
                "contact_info": "",
                "probability_score": 0
            }

            # Process Apollo.io data
            apollo_data = external_data.get("apollo_data")
            if apollo_data and apollo_data.get("organization"):
                org_info = apollo_data["organization"]
                enriched_data["industry"] = org_info.get("industry", "")
                enriched_data["location"] = org_info.get("public_info", {}).get("headquarters", {}).get("city", "") or \
                                           (org_info.get("locations") and org_info["locations"][0].get("city", "")) or ""
                enriched_data["employee_count"] = org_info.get("num_employees", 0)
                enriched_data["revenue"] = org_info.get("annual_revenue", "")
                enriched_data["website"] = org_info.get("website_url", "")
                enriched_data["description"] = org_info.get("short_description", "") or org_info.get("description", "")

            # Process Hunter.io data (for contact info, if available)
            hunter_data = external_data.get("hunter_data")
            if hunter_data and hunter_data.get("data") and hunter_data["data"].get("emails"):
                # Try to find a relevant contact email and name
                email_found = hunter_data["data"]["emails"][0] # Take the first email
                contact_name = f"{email_found.get('first_name', '')} {email_found.get('last_name', '')}".strip()
                if contact_name:
                    enriched_data["contact_info"] = f"{contact_name} ({email_found.get('value', '')})"
                else:
                    enriched_data["contact_info"] = email_found.get('value', '')

            # Process NewsAPI data (for insights)
            news_data = external_data.get("news_data")
            if news_data and news_data.get("articles"):
                # Simple summary of the first article title
                if len(news_data["articles"]) > 0:
                    enriched_data["insights_summary"] = news_data["articles"][0].get("title", "")

            # Save enriched data to MongoDB
            await db.companies.update_one(
                {"name": company_name},
                {"$set": enriched_data},
                upsert=True
            )

            # Return data in the format expected by the frontend
            return {
                "name": enriched_data["name"],
                "industry": enriched_data["industry"],
                "location": enriched_data["location"],
                "employeeCount": enriched_data["employee_count"],
                "revenue": enriched_data["revenue"],
                "website": enriched_data["website"],
                "description": enriched_data["description"],
                "contactInfo": enriched_data["contact_info"],
                "probabilityScore": enriched_data["probability_score"]
            }

        except Exception as e:
            logger.error(f"Error enriching lead {company_name}: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to enrich lead: {str(e)}"
            ) 