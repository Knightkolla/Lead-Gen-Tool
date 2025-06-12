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
            # Extract numerical features
            employee_count = float(lead.get('employeeCount', 0))
            revenue = self._parse_revenue(lead.get('revenue', '0'))
            website_score = self._score_website(lead.get('website', ''))
            description_score = self._score_description(lead.get('description', ''))
            industry_score = self._score_industry(lead.get('industry', ''))
            location_score = self._score_location(lead.get('location', ''))
            
            features.append([
                employee_count,
                revenue,
                website_score,
                description_score,
                industry_score,
                location_score
            ])
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
        """Generate analytics data for the frontend"""
        if not leads:
            return {
                'total_leads': 0,
                'potential_distribution': {'high': 0, 'medium': 0, 'low': 0},
                'industry_distribution': {},
                'location_distribution': {},
                'employee_size_distribution': {},
                'revenue_distribution': {},
                'trends': {
                    'daily_leads': [],
                    'potential_trend': []
                }
            }
        
        # Get cluster statistics
        _, cluster_stats = self.cluster_leads(leads)
        
        # Calculate distributions
        industry_dist = {}
        location_dist = {}
        employee_size_dist = {
            '1-10': 0,
            '11-50': 0,
            '51-200': 0,
            '201-1000': 0,
            '1000+': 0
        }
        revenue_dist = {
            '0-1M': 0,
            '1M-10M': 0,
            '10M-100M': 0,
            '100M+': 0
        }
        
        for lead in leads:
            # Industry distribution
            industry = lead.get('industry', 'Unknown')
            industry_dist[industry] = industry_dist.get(industry, 0) + 1
            
            # Location distribution
            location = lead.get('location', 'Unknown')
            location_dist[location] = location_dist.get(location, 0) + 1
            
            # Employee size distribution
            emp_count = float(lead.get('employeeCount', 0))
            if emp_count <= 10:
                employee_size_dist['1-10'] += 1
            elif emp_count <= 50:
                employee_size_dist['11-50'] += 1
            elif emp_count <= 200:
                employee_size_dist['51-200'] += 1
            elif emp_count <= 1000:
                employee_size_dist['201-1000'] += 1
            else:
                employee_size_dist['1000+'] += 1
            
            # Revenue distribution
            revenue = self._parse_revenue(lead.get('revenue', '0'))
            if revenue <= 1_000_000:
                revenue_dist['0-1M'] += 1
            elif revenue <= 10_000_000:
                revenue_dist['1M-10M'] += 1
            elif revenue <= 100_000_000:
                revenue_dist['10M-100M'] += 1
            else:
                revenue_dist['100M+'] += 1
        
        # Generate trend data (last 7 days)
        today = datetime.now()
        daily_leads = []
        potential_trend = []
        
        for i in range(7):
            date = (today - pd.Timedelta(days=i)).strftime('%Y-%m-%d')
            daily_leads.append({
                'date': date,
                'count': len([l for l in leads if l.get('created_at', '').startswith(date)])
            })
            potential_trend.append({
                'date': date,
                'high': len([l for l in leads if l.get('created_at', '').startswith(date) and l.get('potential') == 'high']),
                'medium': len([l for l in leads if l.get('created_at', '').startswith(date) and l.get('potential') == 'medium']),
                'low': len([l for l in leads if l.get('created_at', '').startswith(date) and l.get('potential') == 'low'])
            })
        
        return {
            'total_leads': len(leads),
            'potential_distribution': cluster_stats,
            'industry_distribution': industry_dist,
            'location_distribution': location_dist,
            'employee_size_distribution': employee_size_dist,
            'revenue_distribution': revenue_dist,
            'trends': {
                'daily_leads': daily_leads,
                'potential_trend': potential_trend
            }
        } 