from typing import List, Dict, Any, Optional
from .ml_service import MLService
from app.database import get_mongo_db

class LeadsService:
    def __init__(self):
        self.leads = []
        self.ml_service = MLService()
        self._is_initialized = False

    async def initialize(self):
        """Initialize the service by loading leads from DB and training ML models"""
        if not self._is_initialized:
            try:
                db = await get_mongo_db()
                companies = await db.companies.find().to_list(length=1000)
                self.leads = companies
                if self.leads:
                    self.ml_service.train_models(self.leads)
                    print(f"Loaded {len(self.leads)} leads from DB and trained ML models")
                else:
                    print("No leads found in database")
            except Exception as e:
                print(f"Error loading leads from DB: {e}")
            self._is_initialized = True

    async def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data"""
        if not self._is_initialized:
            await self.initialize()
        
        if not self.leads:
            return {
                "lead_distribution": {},
                "lead_projection": [],
                "top_leads": []
            }

        # Convert MongoDB ObjectId to string in leads
        processed_leads = []
        for lead in self.leads:
            lead_copy = lead.copy()
            if '_id' in lead_copy:
                lead_copy['_id'] = str(lead_copy['_id'])
            processed_leads.append(lead_copy)

        analytics_data = self.ml_service.get_analytics_data(processed_leads)
        
        # Convert ObjectId to string in top_leads if they exist
        if 'top_leads' in analytics_data:
            for lead in analytics_data['top_leads']:
                if '_id' in lead:
                    lead['_id'] = str(lead['_id'])
        
        return analytics_data

    async def add_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new lead"""
        if not self._is_initialized:
            await self.initialize()
        
        self.leads.append(lead)
        self.ml_service.train_models(self.leads)
        return lead

    async def delete_lead(self, lead_id: str) -> bool:
        """Delete a lead by ID"""
        if not self._is_initialized:
            await self.initialize()
        
        initial_length = len(self.leads)
        self.leads = [lead for lead in self.leads if lead.get("id") != lead_id]
        
        if len(self.leads) < initial_length:
            self.ml_service.train_models(self.leads)
            return True
        return False

    async def search_leads(self, query: str) -> List[Dict[str, Any]]:
        """Search leads using ML service"""
        if not self._is_initialized:
            await self.initialize()
        
        if not self.leads:
            return []
            
        return self.ml_service.search_leads(self.leads, query)

    def get_leads(self, sort_by: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all leads, optionally sorted by ML score"""
        if sort_by == 'ml_score':
            return self.ml_service.rank_leads(self.leads)
        return self.leads

    def get_lead_by_id(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific lead by ID"""
        for lead in self.leads:
            if lead.get('id') == lead_id:
                return lead
        return None

    def update_lead(self, lead_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a lead and retrain ML models"""
        for lead in self.leads:
            if lead.get('id') == lead_id:
                lead.update(updates)
                self.ml_service.train_models(self.leads)  # Retrain models after update
                return lead
        return None

    def search_leads(self, query: str) -> List[Dict[str, Any]]:
        """Search leads and rank results using ML"""
        if not query:
            return self.leads

        # Basic search
        results = []
        query = query.lower()
        for lead in self.leads:
            if any(query in str(value).lower() for value in lead.values()):
                results.append(lead)

        # Rank results using ML
        return self.ml_service.rank_leads(results) 