from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_serializer
from enum import Enum
from typing import Optional, Literal, List
from datetime import datetime
from src.models import PyObjectId
from bson.objectid import ObjectId
from zoneinfo import ZoneInfo

# Define leads source schema
class LeadSource(str, Enum):
    WEBSITE = "website"
    LINKEDIN = "linkedin"
    CONFERENCE = "conference"
    COLD_EMAIL = "cold_email"
    REFERRAL = "referral"
    OTHER = "Other"

# Define leads status schema
class LeadStatus(str, Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won" 
    CLOSED_LOST = "closed_lost"

# Define interaction model
class Interaction(BaseModel):
    date: datetime = Field(...)
    type: Literal["email", "call", "meeting", "demo", "follow-up"] = Field(
        ...,
        description="The type of interaction with the lead.",
        example="email"
    )
    notes: Optional[str] = Field(None)
    owner: Optional[str] = Field(..., description="The owner or team member responsible ")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            datetime: lambda v: v.isoformat()
        },
        json_schema_extra={
            "example": {
                "date": "2024-11-25T15:30:00Z",
                "type": "call",
                "notes": "Reviewed the proposal and discussed next steps.",
                "owner": "jane.doe@company.com"
            }
        }
    )

# Define the lead model
class LeadBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    company: str = Field(..., min_length=2, max_length=100)
    company_size: int = Field(..., gt=0, description="The size of the lead's company (number of employees).")
    email: EmailStr = Field(...)
    job_title: Optional[str] = Field(None, description="The lead's job title.", example="CTO")
    phone: Optional[str] = Field(None, pattern=r'^\+?[0-9]{1,15}$')
    source: LeadSource = Field(...)
    status: LeadStatus = Field(default=LeadStatus.NEW)
    interactions:Optional[List[Interaction]] = Field(None)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
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
                        "type": "email",
                        "notes": "Initial contact",
                        "owner": "john.doe@example.com"
                    }
                ],
            }
        }
    )

    @field_serializer("id")
    def serialize_id(self, id: Optional[ObjectId], _info):
        return str(id) if id else None

# Define Lead in DB schema
class LeadInDB(LeadBase):
    score: Optional[float] = Field(default=0.0,ge=0,le=100,description="A score indicating the lead's potential value (0 to 100).",example=85.0)
    category: Optional[str] = Field(default=None, description=" The category of the lead (hot,warm, cold, or premium)")

# Define Lead creation schema
class LeadCreateSchema(LeadBase):
    pass
    
# Define Lead update schema
class LeadUpdateSchema(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    company: Optional[str] = Field(None, min_length=2, max_length=100)
    company_size: Optional[int] = None
    email: Optional[EmailStr] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[LeadSource] = None
    status: Optional[LeadStatus] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "company": "TechCorp",
                "company_size": 250,
                "email": "john.doe@example.com",
                "job_title": "CTO",
                "phone": "+1234567890",
                "source": "website",
                "status": "new",
                "score": 85.0,
                "category": "warm"
            }
        }
    )

# # Define Lead list model
# class LeadListSchema(BaseModel):
#     leads: List[LeadInDB]

#     @classmethod
#     def from_mongo_cursor(cls, cursor):
#         return cls(leads=[LeadInDB(**doc) for doc in cursor])

   