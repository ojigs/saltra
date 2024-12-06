from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from src.users.schemas import UserCreateSchema, UserUpdateSchema, UserListSchema
from typing import Optional
from src.users.models import PyObjectId
from src.users.exceptions import UserAlreadyExistsException
from pymongo.errors import DuplicateKeyError

# Define business logic for UserService
class UserService:
    @staticmethod
    async def create_user(
        users_collection: AsyncIOMotorCollection,
        user: UserCreateSchema
    ):
        user_dict = user.model_dump(exclude="id")

        try:
            existing_user = await users_collection.find_one({"email": user.email})
            if existing_user:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User with email {user.email} already exists")
            
            result = await users_collection.insert_one(user_dict)
            user.id = result.inserted_id

            return user
        except DuplicateKeyError as e:
            raise UserAlreadyExistsException(f"User with email {user.email} already exists")
        
    
    @staticmethod
    async def get_users(
        user_collection: AsyncIOMotorCollection,
        skip: int = 0,
        limit: int = 100,
        min_age: Optional[int] = None
    ):
        query = {}
        if min_age is not None:
            query["age"] = {"$gte": min_age}
        
        users_cursor = user_collection.find(query).skip(skip).limit(limit)
        users = await users_cursor.to_list(length=limit)

        return UserListSchema.from_mongo_cursor(users)
    
    @staticmethod
    async def get_user_by_id(
        users_collection: AsyncIOMotorCollection,
        user_id: PyObjectId,
    ):
        user = await users_collection.find_one({"_id": user_id})
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return user
    
    @staticmethod
    async def update_user(
        users_collection: AsyncIOMotorCollection,
        user_id: PyObjectId,
        user_update: UserUpdateSchema
    ):
        user_data = user_update.model_dump(exclude_unset=True)
        
        if not user_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update fields provided")
        
        result = await users_collection.find_one_and_update(
            {"_id": user_id},
            {"$set": user_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return result

    @staticmethod
    async def delete_user(
        users_collection: AsyncIOMotorCollection, 
        user_id: PyObjectId
    ):
        result = await users_collection.find_one_and_delete({"_id": user_id})
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or already deleted")
        
        return {"detail": "User deleted successfully"}
        