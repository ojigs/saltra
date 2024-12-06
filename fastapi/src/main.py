from fastapi import FastAPI, Depends
from src.database import db_lifespan
from src.users.routes import users_router
from src.leads.routes import leads_router
from fastapi.middleware.cors import CORSMiddleware

version  = "v1"

app: FastAPI = FastAPI(
    lifespan=db_lifespan,
    title="Sales Tracker Fast API"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    users_router, 
    prefix=f"/api/{version}/users", tags=["users"], 
)

app.include_router(
    leads_router, 
    prefix=f"/api/{version}/leads", tags=["leads"], 
)