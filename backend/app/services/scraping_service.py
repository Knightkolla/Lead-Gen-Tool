import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from pymongo.collection import Collection
import os
from dotenv import load_dotenv
import logging
import asyncio
import aiohttp
from urllib.parse import quote_plus
import re
import json

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to the .env file
dotenv_path = os.path.join(current_dir, os.pardir, '.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)

class ScrapingService:
    def __init__(self, companies_collection: Collection):
        self.companies_collection = companies_collection
        self.scraper_api_key = os.getenv("SCRAPER_API_KEY")
        if not self.scraper_api_key:
            logger.warning("Warning: SCRAPER_API_KEY not set. Scraping via ScraperAPI will be skipped.")
        else:
            print(f"SCRAPER_API_KEY loaded: {self.scraper_api_key[:5]}...") # Print partial key for security

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    async def _fetch_html_with_scraper_api(self, url: str) -> Optional[str]:
        """Fetch HTML content using ScraperAPI with basic parameters"""
        if not self.scraper_api_key:
            logger.error("ScraperAPI key not configured")
            return None

        try:
            # Build the query string with basic parameters only
            params = {
                'api_key': self.scraper_api_key,
                'url': url,
                'country_code': 'US',
                'render': 'true',
                'retry': '3',
                'keep_headers': 'true',
                'bypass': 'cloudflare',
                'wait': '5000'  # Wait 5 seconds for JavaScript to load
            }
            
            # Build the query string
            query_string = '&'.join(f"{k}={v}" for k, v in params.items())
            scraper_url = f"http://api.scraperapi.com/?{query_string}"
            
            request_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            logger.info(f"Fetching URL with ScraperAPI: {url}")
            logger.debug(f"ScraperAPI request URL: {scraper_url}")
            async with aiohttp.ClientSession() as session:
                async with session.get(scraper_url, headers=request_headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        logger.info(f"Successfully fetched HTML from {url}")
                        return html
                    else:
                        error_msg = f"Error fetching {url} with ScraperAPI: {response.status}, message='{response.reason}', url={response.url}"
                        logger.error(error_msg)
                        return None
        except Exception as e:
            logger.error(f"Error in _fetch_html_with_scraper_api: {str(e)}")
            return None

    async def scrape_b2b_leads(self, industry: str = "", location: str = "") -> List[Dict[str, Any]]:
        """
        Scrapes B2B leads from multiple sources.
        
        Args:
            industry (str): The industry to search for.
            location (str): The location to search for.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries, each representing a scraped company.
        """
        print(f"Starting web scraping for leads with industry: {industry}, location: {location}")
        
        # List of sources to scrape from
        sources = [
            self.scrape_business_directory
        ]
        
        # Gather results from all sources
        tasks = [source(industry, location) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Flatten results and filter out exceptions
        all_leads = []
        for result in results:
            if isinstance(result, list):
                all_leads.extend(result)
            else:
                logger.error(f"Error scraping from source: {str(result)}")

        # Filter leads if industry or location are provided
        final_leads = all_leads

        # Save scraped data to MongoDB
        for lead in final_leads:
            # Use update_one with upsert=True to insert if not exists, or update if exists
            update_result = await self.companies_collection.update_one(
                {"name": lead["name"]},
                {"$set": lead},
                upsert=True
            )
            if update_result.upserted_id:
                logger.info(f"Scraped and added: {lead['name']} (new entry added to MongoDB) with ID: {update_result.upserted_id}")
            elif update_result.modified_count > 0:
                logger.info(f"Scraped: {lead['name']} (existing entry updated in MongoDB)")
            else:
                logger.info(f"Scraped: {lead['name']} (already exists in MongoDB, no changes needed)")

        return final_leads

    # Removed placeholder functions for LinkedIn and Crunchbase
    # async def scrape_linkedin_companies(self, query: str) -> List[Dict[str, Any]]:
    #    ...

    # async def scrape_crunchbase(self, query: str) -> List[Dict[str, Any]]:
    #    ...

    async def scrape_angellist(self, industry: str, location: str) -> List[Dict[str, Any]]:
        """Scrape company information from Wellfound (formerly AngelList) using ScraperAPI"""
        logger.info(f"scrape_angellist received: industry='{industry}', location='{location}'")
        try:
            # Clean and normalize the input parameters
            industry = industry.strip() if industry else ""
            location = location.strip() if location else ""
            
            if industry and location:
                # Reverting to the companies endpoint, as jobs might not have __NEXT_DATA__
                url = f"https://wellfound.com/companies?q={quote_plus(industry.strip())}&location={quote_plus(location.strip())}"
            elif industry:
                url = f"https://wellfound.com/companies?q={quote_plus(industry.strip())}"
            elif location:
                url = f"https://wellfound.com/companies?location={quote_plus(location.strip())}"
            else:
                logger.info("No industry or location provided for Wellfound scraping. Skipping.")
                return []
            
            # Fetch HTML using the simplified _fetch_html_with_scraper_api
            html = await self._fetch_html_with_scraper_api(url)
            
            if not html:
                logger.error("Failed to fetch HTML from Wellfound")
                return []

            soup = BeautifulSoup(html, 'html.parser')
            companies = []
            
            # ONLY try to find the __NEXT_DATA__ script tag - remove HTML fallback
            next_data_script = soup.find('script', {'id': '__NEXT_DATA__'})
            
            if next_data_script:
                try:
                    json_data = json.loads(next_data_script.string)
                    apollo_state = json_data.get('props', {}).get('pageProps', {}).get('apolloState', {}).get('data', {})
                    
                    if apollo_state:
                        # Extract companies from apollo_state that start with "StartupResult:"
                        for key, value in apollo_state.items():
                            if key.startswith("StartupResult:"):
                                try:
                                    company_name = value.get('name', 'N/A')
                                    industry = 'N/A'
                                    location = 'N/A'
                                    
                                    location_names_json = value.get('locationNames', {}).get('json')
                                    if location_names_json and isinstance(location_names_json, list):
                                        location = ", ".join(location_names_json) or 'N/A'
                                        
                                    employee_count_str = value.get('companySize')
                                    employee_count = 0
                                    if employee_count_str:
                                        match = re.search(r'\d+', employee_count_str)
                                        if match:
                                            employee_count = int(match.group(0))
                                        elif 'SIZE_1_10' in employee_count_str:
                                            employee_count = 10
                                        elif 'SIZE_1000_PLUS' in employee_count_str:
                                            employee_count = 1000
                                    
                                    website = value.get('companyUrl', 'https://example.com')
                                    if website and not website.startswith(('http://', 'https://')):
                                        website = 'https://' + website
                                    
                                    description = value.get('highConcept', 'No description available.')
                                    
                                    company = {
                                        "name": company_name,
                                        "industry": industry,
                                        "location": location,
                                        "employeeCount": employee_count,
                                        "website": website,
                                        "description": description,
                                        "revenue": "N/A",
                                        "contactInfo": "N/A",
                                        "probabilityScore": 8.0
                                    }
                                    companies.append(company)
                                    logger.info(f"Successfully scraped company from JSON: {company_name}")
                                    
                                except Exception as e:
                                    logger.error(f"Error parsing company data from JSON for key {key}: {str(e)}")
                                    continue
                    else:
                        logger.warning("Apollo state data not found in __NEXT_DATA__. Check structure.")
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error in scrape_angellist: {e}")
                except Exception as e:
                    logger.error(f"Error extracting data from __NEXT_DATA__ script: {e}")
            else:
                logger.warning("No __NEXT_DATA__ script tag found on the page. Website structure might have changed or rendering failed.")

            logger.info(f"Found {len(companies)} companies after parsing.")
            return companies

        except Exception as e:
            logger.error(f"Error in scrape_angellist: {str(e)}")
            return []

    async def scrape_business_directory(self, industry: str, location: str) -> List[Dict[str, Any]]:
        """Scrape company information from a business directory using ScraperAPI"""
        logger.info(f"scrape_business_directory received: industry='{industry}', location='{location}'")
        try:
            # Clean and normalize the input parameters
            industry = industry.strip() if industry else ""
            location = location.strip() if location else ""
            
            if not industry and not location:
                logger.info("No industry or location provided for business directory scraping. Skipping.")
                return []

            # Construct the search URL for the business directory
            base_url = "https://www.yellowpages.com"
            search_query = f"{industry} {location}".strip()
            url = f"{base_url}/search?search_terms={quote_plus(search_query)}"
            
            # Fetch HTML using ScraperAPI
            html = await self._fetch_html_with_scraper_api(url)
            
            if not html:
                logger.error("Failed to fetch HTML from business directory")
                return []

            soup = BeautifulSoup(html, 'html.parser')
            companies = []
            
            # Find all business listings
            business_cards = soup.find_all('div', class_='result')
            logger.info(f"Found {len(business_cards)} company cards on the page.")
            
            if not business_cards:
                logger.warning("No company cards found with current selectors. Check website HTML.")
                return []

            for card in business_cards:
                try:
                    # Extract company name
                    name_elem = card.find('a', class_='business-name')
                    name = name_elem.text.strip() if name_elem else 'N/A'
                    
                    # Extract website
                    website_elem = card.find('a', class_='track-visit-website')
                    website = website_elem.get('href', '') if website_elem else 'N/A'
                    
                    # Extract address
                    address_elem = card.find('div', class_='street-address')
                    address = address_elem.text.strip() if address_elem else 'N/A'
                    
                    # Extract phone
                    phone_elem = card.find('div', class_='phones phone primary')
                    phone = phone_elem.text.strip() if phone_elem else 'N/A'
                    
                    # Create company object
                    company = {
                        "name": name,
                        "industry": industry or 'N/A',
                        "location": location or address,
                        "employeeCount": 0,  # Not available from basic listing
                        "website": website,
                        "description": f"Business in {location}" if location else 'N/A',
                        "revenue": "N/A",
                        "contactInfo": phone,
                        "probabilityScore": 7.0  # Default score for basic listings
                    }
                    
                    companies.append(company)
                    logger.info(f"Successfully scraped company: {name}")
                    
                except Exception as e:
                    logger.error(f"Error parsing company card: {str(e)}")
                    continue

            logger.info(f"Successfully scraped {len(companies)} companies from business directory")
            return companies

        except Exception as e:
            logger.error(f"Error in scrape_business_directory: {str(e)}")
            return []

