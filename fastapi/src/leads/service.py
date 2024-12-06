from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
from src.leads.schemas import LeadCreateSchema, LeadUpdateSchema, LeadStatus, LeadSource, Interaction
from src.leads.models import LeadModel, LeadListSchema
from typing import Optional
from src.models import PyObjectId
from src.leads.exceptions import LeadAlreadyExistsException
from src.leads.scorer import LeadScorer
from pymongo.errors import DuplicateKeyError
from datetime import datetime

# Define business logic for LeadService
class LeadService:
    @staticmethod
    async def create_lead(
        leads_collection: AsyncIOMotorCollection,
        lead: LeadCreateSchema
    ):
        lead_dict = lead.model_dump(exclude="id", exclude_unset=True)

        now = datetime.now()
        lead_dict["updated_at"] = now
    
        try:
            existing_lead = await leads_collection.find_one({"$or": [
                {"email": lead.email},
                {"phone": lead.phone}
            ]})
    
            if existing_lead:
                # merge existing lead data with updat data to calculate the lead score and category
                lead_for_scoring = {**existing_lead, **lead_dict}
                # print(f"lead for scoring create {lead_for_scoring}")
                # print(f"existing lead {existing_lead}")
                # print(f"update lead {lead_dict}")   
                score = LeadScorer.calculate_score(lead_for_scoring)
                lead_dict["score"] = score
                lead_dict["category"] = LeadScorer.categorize_lead(score)
                
                # Update lead if already existing for data integrity reasons
                result = await leads_collection.find_one_and_update(
                    {"_id": existing_lead["_id"]},
                    {"$set": lead_dict},
                    return_document=True
                )
                updated_lead = LeadModel(**result)
                updated_lead.id = result["_id"]
                return updated_lead
            else:
                # Create a new lead
                lead_dict["created_at"] = now
                score = LeadScorer.calculate_score(lead_dict)
                lead_dict["score"] = score
                lead_dict["category"] = LeadScorer.categorize_lead(score)


                result = await leads_collection.insert_one(lead_dict)
                lead_dict["id"] = result.inserted_id
                return LeadModel(**lead_dict)
        except DuplicateKeyError as e:
            raise LeadAlreadyExistsException(f"Lead with email {lead.email} already exists")
        
    
    @staticmethod
    async def get_leads(
        lead_collection: AsyncIOMotorCollection,
        skip: int = 0,
        limit: int = 100,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        status: Optional[LeadStatus] = None,
        source: Optional[LeadSource] = None,
        company: Optional[str] = None,
        job_title: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        
        # query filters
        query = {}
        if first_name:
            query["first_name"] = {"$regex": first_name, "$options": "i"}
        if last_name:
            query["last_name"] = {"$regex": last_name, "$options": "i"}
        if email:
            query["email"] = email
        if status:
            query["status"] = status
        if source:
            query["source"] = source
        if company:
            query["company"] = {"$regex": company, "$options": "i"}
        if job_title:
            query["job_title"] = {"$regex": job_title, "$options": "i"}
        if phone:
            query["phone"] = phone

        total_count = await lead_collection.count_documents(query)
        
        leads_cursor = lead_collection.find(query).skip(skip).limit(limit)
        leads = await leads_cursor.to_list(length=limit)

        return LeadListSchema.from_mongo_cursor(leads), total_count
    
    @staticmethod
    async def get_lead_by_id(
        leads_collection: AsyncIOMotorCollection,
        lead_id: PyObjectId,
    ):
        lead = await leads_collection.find_one({"_id": lead_id})
        
        if not lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        
        return lead
    
    @staticmethod
    async def update_lead(
        leads_collection: AsyncIOMotorCollection,
        lead_id: PyObjectId,
        lead_update: LeadUpdateSchema
    ):
        lead_data = lead_update.model_dump(exclude_unset=True)

        now = datetime.now()
        lead_data["updated_at"] = now
        
        if not lead_data:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No update fields provided")
        
        existing_lead = await leads_collection.find_one({"_id": lead_id})
        if not existing_lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lead not found.")
        
        # merge existing lead data with updat data to calculate the lead score and category
        lead_for_scoring = {**existing_lead, **lead_data}
        # print(f"lead for scoring update {lead_for_scoring}")
        # print(f"existing lead {existing_lead}")
        # print(f"update lead {lead_data}")
        score = LeadScorer.calculate_score(lead_for_scoring)
        lead_data["score"] = score
        lead_data["category"] = LeadScorer.categorize_lead(score)
        
        result = await leads_collection.find_one_and_update(
            {"_id": lead_id},
            {"$set": lead_data},
            return_document=True
        )
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")
        
        return result

    @staticmethod
    async def delete_lead(
        leads_collection: AsyncIOMotorCollection, 
        lead_id: PyObjectId
    ):
        result = await leads_collection.find_one_and_delete({"_id": lead_id})
        
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found or already deleted")
        
        return {"detail": "Lead deleted successfully"}
    
    @staticmethod
    async def add_lead_interaction(
        leads_collection: AsyncIOMotorCollection, 
        lead_id: PyObjectId, 
        interaction_data: Interaction
    ):
        interaction_dict = interaction_data.model_dump(exclude_unset=True)

        if not interaction_dict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No interaction data provided")
        
        now = datetime.now()

        existing_lead = await leads_collection.find_one({"_id": lead_id})
        if not existing_lead:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Lead not found.")
        
        # merge existing lead data with updat data to calculate the lead score and category
        # lead_for_scoring = {**existing_lead, **interaction_data}
        lead_for_scoring = existing_lead.copy()
        lead_for_scoring["interactions"] = existing_lead.get("interactions", []) + [interaction_dict]
        # print(f"lead for scoring update {lead_for_scoring}")
        # print(f"existing lead {existing_lead}")
        # print(f"update lead {lead_data}")
        score = LeadScorer.calculate_score(lead_for_scoring)
        category = LeadScorer.categorize_lead(score)

        result = await leads_collection.find_one_and_update(
            {"_id": lead_id},
            {
                "$push": {"interactions": interaction_dict}, 
                "$set": {"score": score, "category": category, "updated_at": now}
            },
            return_document=True
        )

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead not found")

        return LeadModel(**result)