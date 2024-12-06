from fastapi import APIRouter, Depends, Response
from motor.motor_asyncio import AsyncIOMotorCollection
from src.leads.schemas import LeadCreateSchema, LeadUpdateSchema, LeadStatus, LeadSource, Interaction
from src.leads.models import LeadModel, LeadListSchema
from src.database import get_leads_collection
from src.models import PyObjectId
from src.leads.service import LeadService
from typing import Optional, Dict

leads_router = APIRouter()

# Create CRUD path operations for Lead
@leads_router.post("/", response_model=LeadModel, status_code=201, response_model_by_alias=False)
async def create_lead(
     lead: LeadCreateSchema, 
     leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    return await LeadService.create_lead(leads_collection, lead)

# Get all leads
@leads_router.get("/", response_model=LeadListSchema, response_model_by_alias=False)
async def get_leads(
    response: Response,
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
    leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    leads, total_count =  await LeadService.get_leads(
        leads_collection,
        first_name=first_name,
        last_name=last_name,
        email=email,
        status=status,
        source=source,
        company=company,
        job_title=job_title,
        phone=phone,
        skip=skip,
        limit=limit,
    )

    response.headers["X-Total-Count"] = str(total_count)
    return leads

# Get a single lead by id
@leads_router.get("/{lead_id}", response_model=LeadModel, response_model_by_alias=False)
async def get_lead(
    lead_id: PyObjectId,
    leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    return await LeadService.get_lead_by_id(leads_collection, lead_id)
    

# Update lead 
@leads_router.put("/{lead_id}", response_model=LeadModel, response_model_by_alias=False)
async def update_lead(
    lead_id: PyObjectId, 
    lead_update: LeadUpdateSchema,
    leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    return await LeadService.update_lead(leads_collection, lead_id, lead_update)

# Delete a lead
@leads_router.delete("/{lead_id}", response_model=Dict[str, str], response_model_by_alias=False)
async def delete_lead(
    lead_id: PyObjectId,
    leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    return await LeadService.delete_lead(leads_collection, lead_id)

# Add lead interaction
@leads_router.post("/{lead_id}/interactions", response_model=LeadModel, response_model_by_alias=False)
async def add_lead_interaction(
    lead_id: PyObjectId, 
    interaction_data: Interaction,
    leads_collection: AsyncIOMotorCollection = Depends(get_leads_collection)
):
    return await LeadService.add_lead_interaction(leads_collection, lead_id, interaction_data)
   
