import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from typing import List, Dict, Any, Tuple
import pandas as pd
from datetime import datetime

class MLService:
    def __init__(self):
        self.scaler = StandardScaler()
        self.ranking_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.clustering_model = KMeans(n_clusters=3, random_state=42)
        self.is_trained = False

    def _prepare_features(self, leads: List[Dict[str, Any]]) -> np.ndarray:
        """Convert lead data into numerical features for ML models"""
        features = []
        for lead in leads:
            try:
                # Extract numerical features with safe defaults
                employee_count = float(lead.get('employeeCount', 0) or 0)
                revenue = self._parse_revenue(lead.get('revenue', '0') or '0')
                website_score = self._score_website(lead.get('website', '') or '')
                description_score = self._score_description(lead.get('description', '') or '')
                industry_score = self._score_industry(lead.get('industry', '') or '')
                location_score = self._score_location(lead.get('location', '') or '')
                
                features.append([
                    employee_count,
                    revenue,
                    website_score,
                    description_score,
                    industry_score,
                    location_score
                ])
            except Exception as e:
                print(f"Error processing lead: {e}")
                # Add default features if processing fails
                features.append([0, 0, 0, 0, 0, 0])
        
        return np.array(features)

    def _parse_revenue(self, revenue_str: str) -> float:
        """Convert revenue string to numerical value"""
        if not revenue_str or revenue_str == 'N/A':
            return 0.0
        
        try:
            # Remove currency symbols and commas
            revenue_str = revenue_str.replace('$', '').replace(',', '')
            
            # Handle different revenue formats (e.g., "1M", "1B", "1K")
            if 'M' in revenue_str:
                return float(revenue_str.replace('M', '')) * 1_000_000
            elif 'B' in revenue_str:
                return float(revenue_str.replace('B', '')) * 1_000_000_000
            elif 'K' in revenue_str:
                return float(revenue_str.replace('K', '')) * 1_000
            else:
                return float(revenue_str)
        except:
            return 0.0

    def _score_website(self, website: str) -> float:
        """Score website quality"""
        if not website or website == 'N/A':
            return 0.0
        
        score = 0.0
        # Check if website is valid
        if website.startswith(('http://', 'https://')):
            score += 1.0
        # Check if it's a professional domain
        if '.com' in website or '.org' in website or '.net' in website:
            score += 1.0
        return score

    def _score_description(self, description: str) -> float:
        """Score description quality"""
        if not description or description == 'N/A':
            return 0.0
        
        # Score based on description length and content
        words = description.split()
        score = min(len(words) / 50, 1.0)  # Normalize by 50 words
        return score

    def _score_industry(self, industry: str) -> float:
        """Score industry relevance"""
        if not industry or industry == 'N/A':
            return 0.0
        
        # Define high-value industries
        high_value_industries = {
            'technology', 'software', 'saas', 'ai', 'artificial intelligence',
            'machine learning', 'data', 'cloud', 'cybersecurity', 'fintech',
            'healthcare', 'biotech', 'medical', 'pharmaceutical'
        }
        
        industry_lower = industry.lower()
        if any(term in industry_lower for term in high_value_industries):
            return 1.0
        return 0.5

    def _score_location(self, location: str) -> float:
        """Score location desirability"""
        if not location or location == 'N/A':
            return 0.0
        
        # Define high-value locations
        high_value_locations = {
            'san francisco', 'new york', 'london', 'boston', 'seattle',
            'austin', 'los angeles', 'chicago', 'toronto', 'berlin'
        }
        
        location_lower = location.lower()
        if any(term in location_lower for term in high_value_locations):
            return 1.0
        return 0.5

    def train_models(self, leads: List[Dict[str, Any]]):
        """Train ranking and clustering models"""
        if not leads:
            return
        
        # Prepare features
        X = self._prepare_features(leads)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train ranking model (using employee count as target for now)
        y = X[:, 0]  # Use employee count as target
        self.ranking_model.fit(X_scaled, y)
        
        # Train clustering model
        self.clustering_model.fit(X_scaled)
        
        self.is_trained = True

    def rank_leads(self, leads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Rank leads based on ML model predictions"""
        if not leads or not self.is_trained:
            return leads
        
        # Prepare features
        X = self._prepare_features(leads)
        X_scaled = self.scaler.transform(X)
        
        # Get predictions
        scores = self.ranking_model.predict(X_scaled)
        
        # Add scores to leads
        for lead, score in zip(leads, scores):
            lead['ml_score'] = float(score)
        
        # Sort leads by score
        return sorted(leads, key=lambda x: x.get('ml_score', 0), reverse=True)

    def cluster_leads(self, leads: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """Cluster leads into high, medium, and low potential"""
        if not leads or not self.is_trained:
            return leads, {'high': 0, 'medium': 0, 'low': 0}
        
        # Prepare features
        X = self._prepare_features(leads)
        X_scaled = self.scaler.transform(X)
        
        # Get cluster assignments
        clusters = self.clustering_model.predict(X_scaled)
        
        # Map clusters to potential levels
        cluster_centers = self.clustering_model.cluster_centers_
        center_scores = np.mean(cluster_centers, axis=1)
        cluster_map = {
            i: 'high' if score > np.percentile(center_scores, 66)
            else 'medium' if score > np.percentile(center_scores, 33)
            else 'low'
            for i, score in enumerate(center_scores)
        }
        
        # Add cluster information to leads
        for lead, cluster in zip(leads, clusters):
            lead['potential'] = cluster_map[cluster]
        
        # Calculate cluster statistics
        cluster_stats = {
            'high': sum(1 for lead in leads if lead['potential'] == 'high'),
            'medium': sum(1 for lead in leads if lead['potential'] == 'medium'),
            'low': sum(1 for lead in leads if lead['potential'] == 'low')
        }
        
        return leads, cluster_stats

    def get_analytics_data(self, leads: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate analytics data for the frontend (dashboard)"""
        try:
            if not leads:
                return {
                    'lead_distribution': {},
                    'lead_projection': [],
                    'top_leads': []
                }

            # Train models if not already trained
            if not self.is_trained:
                self.train_models(leads)

            # 1. Lead Distribution by Industry
            industry_dist = {}
            for lead in leads:
                industry = lead.get('industry', 'Unknown')
                industry_dist[industry] = industry_dist.get(industry, 0) + 1

            # 2. Lead Projection (last 6 months)
            projection = []
            for i in range(6):
                month = (datetime.now().month - i - 1) % 12 + 1
                year = datetime.now().year - ((datetime.now().month - i - 1) // 12)
                projection.append({
                    'month': f"{year}-{month:02d}",
                    'leads': len(leads) // 6  # Simple projection
                })

            # 3. Top Leads (based on ML score)
            try:
                ranked_leads = self.rank_leads(leads)
                top_leads = ranked_leads[:5] if ranked_leads else []
            except Exception as e:
                print(f"Error ranking leads: {e}")
                # Fallback to simple sorting by employee count
                top_leads = sorted(leads, key=lambda x: float(x.get('employeeCount', 0) or 0), reverse=True)[:5]

            return {
                'lead_distribution': industry_dist,
                'lead_projection': projection,
                'top_leads': top_leads
            }
        except Exception as e:
            print(f"Error generating analytics: {e}")
            return {
                'lead_distribution': {},
                'lead_projection': [],
                'top_leads': []
            } 