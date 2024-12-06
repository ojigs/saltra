from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_serializer
from bson import ObjectId
from typing import Optional, List
from src.users.models import PyObjectId
    
# Define base user model
class UserBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr = Field(...)
    age: int = Field(..., gt=0, le=120)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "age": 30
            }
        }
    )

    @field_serializer("id")
    def serialize_id(self, id: Optional[ObjectId], _info):
        return str(id) if id else None
    
# Define User creation schema
class UserCreateSchema(UserBase):
    pass
    
# Define User update schema
class UserUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None)
    age: Optional[int] = Field(None, gt=0, le=120)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "email": "johndoe@example.com",
                "age": 30
            }
        }
    )

# Define User list model
class UserListSchema(BaseModel):
    users: List[UserBase]

    @classmethod
    def from_mongo_cursor(cls, cursor):
        return cls(users=[UserBase(**doc) for doc in cursor])