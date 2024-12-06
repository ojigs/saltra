from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from src.users.models import PyObjectId
from src.users.schemas import UserBase, UserCreateSchema, UserUpdateSchema, UserListSchema
from src.database import get_users_collection
from src.users.service import UserService
from typing import Optional, Dict

users_router = APIRouter()

# Create CRUD path operations for User
@users_router.post("/", response_model=UserBase, status_code=201, response_model_by_alias=False)
async def create_user(
     user: UserCreateSchema, 
     users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    return await UserService.create_user(users_collection, user)

# Get all users
@users_router.get("/", response_model=UserListSchema, response_model_by_alias=False)
async def get_users(
    skip: int = 0, 
    limit: int = 100,
    min_age: Optional[int] = None,
    users_collection = Depends(get_users_collection)
):
    return await UserService.get_users(
        users_collection,
        skip=skip,
        limit=limit,
        min_age=min_age
    )

# Get a single user by id
@users_router.get("/{user_id}", response_model=UserBase, response_model_by_alias=False)
async def get_user(
    user_id: PyObjectId,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    return await UserService.get_user_by_id(users_collection, user_id)
    

# Update user 
@users_router.put("/{user_id}", response_model=UserBase, response_model_by_alias=False)
async def update_user(
    user_id: PyObjectId, 
    user_update: UserUpdateSchema,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    return await UserService.update_user(users_collection, user_id, user_update)

# Delete a user
@users_router.delete("/{user_id}", response_model=Dict[str, str], response_model_by_alias=False)
async def delete_user(
    user_id: PyObjectId,
    users_collection: AsyncIOMotorCollection = Depends(get_users_collection)
):
    return await UserService.delete_user(users_collection, user_id)
   
