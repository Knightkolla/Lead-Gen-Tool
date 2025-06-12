from typing import List, Dict, Any, Optional
from .ml_service import MLService

class LeadsService:
    def __init__(self):
        self.leads = []
        self.ml_service = MLService()
        self.ml_service.train_models(self.leads)  # Train models with initial data

    def add_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new lead and update ML models"""
        self.leads.append(lead)
        self.ml_service.train_models(self.leads)  # Retrain models with new data
        return lead

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

    def delete_lead(self, lead_id: str) -> bool:
        """Delete a lead and retrain ML models"""
        for i, lead in enumerate(self.leads):
            if lead.get('id') == lead_id:
                self.leads.pop(i)
                self.ml_service.train_models(self.leads)  # Retrain models after deletion
                return True
        return False

    def get_analytics(self) -> Dict[str, Any]:
        """Get analytics data using ML service"""
        return self.ml_service.get_analytics_data(self.leads)

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