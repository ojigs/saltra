from typing import Dict, Any
from datetime import datetime, timezone
from src.leads.schemas import Interaction
from fastapi.security import OAuth2PasswordBearer

class LeadScorer:
    @staticmethod
    def calculate_score(lead: Dict[str, Any]) -> float:
        """
        calculate lead score based on different factors
        
        Legend:
        - Lead Status (0-30 points)
        - Company Size (0-25 points)
        - Interaction Frequency (0-20 points)
        - Job Title Relevance (0-15 points)
        - Source Quality (0-5 points)
        - Recency of Interaction (0-5 points)
        """
        
        # lead status score
        def lead_status_score(status: str) -> float:
            status_ranking = {
                "new": 5,
                "contacted": 10,
                "qualified": 20,
                "negotiation": 25,
                "closed_won": 30,
                "close_lost": 0
            }
            return status_ranking.get(status.lower(), 0)
        
        # company size score
        def company_size_score(size: int) -> float:
            if not size:
                return 0
            if size <= 50:
                return 5
            elif size <= 500:
                return 15
            else:
                return 25
        
        # interaction frequency score
        def interaction_score(interactions: list) -> float:
            if not interactions:
                return 0
            
            interaction_count = len(interactions)
            if interaction_count == 1:
                return 10
            elif interaction_count <= 3:
                return 15
            elif interaction_count <= 5:
                return 18
            else:
                return 20
        
        # job title relevance score
        def job_title_score(title: str) -> float:
            if not title:
                return 0
            
            keywords = [
                'director', 'vp', 'ceo', 'cto', 'founder', 
                'head of', 'president', 'chief'
            ]
            
            title_lower = title.lower()
            for keyword in keywords:
                if keyword in title_lower:
                    return 15
            
            return 10
        
        # source quality score
        def source_score(source: str) -> float:
            source_ranking = {
                "referral": 5,
                "conference": 4,
                "linkedin": 3,
                "website": 2,
                "cold_email": 1
            }
            return source_ranking.get(source.lower(), 1)
        
        # recency score
        def recency_score(interactions: Interaction) -> float:
            if not interactions:
                return 0
            
            # map through interactions and convert all date objects to utc timezone
            for interaction in interactions:
                interaction['date'] = interaction['date'].astimezone(timezone.utc)
            
            # sort interactions by date (most recent first)
            sorted_interactions = sorted(
                interactions, 
                key=lambda x: x.get('date', datetime.min.replace(tzinfo=timezone.utc)).astimezone(timezone.utc) if x.get('date') and x.get('date').tzinfo else x.get('date', datetime.min.replace(tzinfo=timezone.utc)), 
                reverse=True
            )
            
            # check how recent the most recent interaction is
            now = datetime.now(timezone.utc)
            most_recent = sorted_interactions[0].get('date')
            if isinstance(most_recent, str):
                most_recent = datetime.fromisoformat(most_recent)
            # harmonize datetime objects
            if most_recent.tzinfo is not None:
                most_recent = most_recent.astimezone(timezone.utc)
                now = datetime.now(timezone.utc)
            days_since_interaction = (now - most_recent).days
            
            if days_since_interaction <= 7:
                return 5
            elif days_since_interaction <= 30:
                return 3
            elif days_since_interaction <= 90:
                return 1
            else:
                return 0
        
        # total score calculation
        total_score = (
            lead_status_score(lead.get('status', 'new')) +
            company_size_score(lead.get('company_size', 0)) +
            interaction_score(lead.get('interactions', [])) +
            job_title_score(lead.get('job_title', '')) +
            source_score(lead.get('source', 'cold_email')) +
            recency_score(lead.get('interactions', []))
        )
        
        return min(max(total_score, 0), 100)
    
    @staticmethod
    def categorize_lead(score: float) -> str:
        """
        Categorize lead based on score
        """
        if score < 20:
            return 'Cold'
        elif score < 50:
            return 'Warm'
        elif score < 80:
            return 'Hot'
        else:
            return 'Premium'
