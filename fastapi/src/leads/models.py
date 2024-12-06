from pydantic import Field, ConfigDict, BaseModel
from src.leads.schemas import LeadBase
from typing import Literal, List
from datetime import datetime

# Define Lead model
class LeadModel(LeadBase):
    score: float = Field(default=0.0,ge=0,le=100,description="A score indicating the lead's potential value (0 to 100).",example=85.0)
    category: Literal["Premium", "Hot", "Warm", "Cold"] = Field(default=None, description=" The category of the lead (hot,warm, cold, or premium)", example="Premium")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": "64c8e71f9b1a8f0012d4f8c9",
                "first_name": "Jane",
                "last_name": "Doe",
                "company": "TechCorp",
                "company_size": 250,
                "email": "user@techcorp.com",
                "job_title": "CTO",
                "phone": "203467546034",
                "source": "website",
                "status": "new",
                "interactions": [
                    {
                    "date": "2024-11-25T15:30:00Z",
                    "notes": "Reviewed the proposal and discussed next steps.",
                    "owner": "jane.doe@company.com",
                    "type": "call"
                    }
                ],
                "score": 52,
                "category": "Hot",
                "created_at": "2024-11-30T13:14:38.895Z",
                "updated_at": "2024-11-30T13:14:38.895Z"
                

            }
        }
    )

# Define Lead list model
class LeadListSchema(BaseModel):
    leads: List[LeadModel]

    @classmethod
    def from_mongo_cursor(cls, cursor):
        return cls(leads=[LeadModel(**doc) for doc in cursor])