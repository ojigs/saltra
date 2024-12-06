from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.config import settings
from src.logger_config import get_logger
from pymongo import IndexModel, ASCENDING
from pymongo.errors import PyMongoError
from src.exceptions import DatabaseConnectionException, DatabaseCloseError, IndexCreationError

logger = get_logger(__name__)

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    async def connect(cls):
        try:
            cls.client = AsyncIOMotorClient(settings.MONGO_URI)
            cls.db = cls.client.get_default_database()
            logger.info("Successfully connected to database")

            await cls.create_users_indexes()
            await cls.create_leads_indexes()

        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseConnectionException(str(e))

    @classmethod
    async def create_users_indexes(cls):
        try:
            """Create indexes in the users collection"""
            email_index = IndexModel("email", unique=True, name="unique_email_index", background=True)
            name_index = IndexModel([("name", ASCENDING)])
            users_collection = cls.db.get_collection("users")
            await users_collection.create_indexes([email_index, name_index])
            logger.info("Unique index created for 'email' and 'name' fields in 'users' collection")
            
        except PyMongoError as index_error:
            logger.error(f"Error creating indexes: {index_error}")
            raise IndexCreationError(f"Error creating unique email index: {index_error}")
        
    @classmethod
    async def create_leads_indexes(cls):
        try:
            """Create indexes in the leads collection"""
            email_index = IndexModel("email", unique=True, name="unique_email_index_leads", background=True)
            phone_index = IndexModel("phone", unique=True, name="unique_phone_index_leads", background=True)
            leads_collection = cls.db.get_collection("leads")
            await leads_collection.create_indexes([email_index, phone_index])
            logger.info("Unique indexes created for 'email' and 'phone' fields in 'leads' collection")
    
        except PyMongoError as index_error:
            logger.error(f"Error creating indexes: {index_error}")
            raise IndexCreationError(f"Error creating unique email and phone index in leads collection: {index_error}")
    

    @classmethod
    async def close(cls):
        try:
            if cls.client:
                cls.client.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
            raise DatabaseCloseError(str(e))

def get_database():
    return DatabaseManager.db

def get_users_collection():
    return DatabaseManager.db.get_collection("users")

def get_leads_collection():
    return DatabaseManager.db.get_collection("leads")

@asynccontextmanager
async def db_lifespan(app: FastAPI):
    await DatabaseManager.connect()
    try:
        yield
    finally:
        await DatabaseManager.close()