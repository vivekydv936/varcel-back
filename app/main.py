from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
# Removed BaseModel import as Feedback model is moved
from .routes.api import router
from .routes.feedback import router as feedback_router
from .middleware.logging import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
# from textblob import TextBlob # Or use VADER

# Load environment variables
load_dotenv()

# Database connection details
MONGO_DETAILS = os.getenv("MONGO_DETAILS")

class Database: # Renamed from MongoDB to avoid confusion
    client: AsyncIOMotorClient = None

db = Database() # Instantiated the Database class

async def get_database() -> AsyncIOMotorClient:
    return db.client

# Removed Pydantic model for Feedback
# class Feedback(BaseModel):
#     feedback_text: str
#     # sentiment_score: float = None # We will add this after analysis

app = FastAPI(
    title=os.getenv("APP_NAME", "FastAPI Backend"),
    version=os.getenv("API_VERSION", "v1")
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add logging middleware
app.add_middleware(LoggingMiddleware)

# Include routes
app.include_router(router, prefix="/api")
app.include_router(feedback_router, tags=["Feedback"], prefix="/feedback")

@app.on_event("startup")
async def startup_db_client():
    db.client = AsyncIOMotorClient(MONGO_DETAILS)
    # Access the database instance from app state
    app.mongodb = db.client[os.getenv("MONGO_DATABASE_NAME", "feedback_db")]
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_db_client():
    db.client.close()
    print("Disconnected from MongoDB")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Event Feedback Hub Backend!"}

# Placeholder for feedback routes
# app.include_router(feedback_router, tags=["Feedback"], prefix="/feedback") 