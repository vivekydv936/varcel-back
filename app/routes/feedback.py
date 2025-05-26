from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from textblob import TextBlob

# Import the Feedback model from the new models.py file
from ..models import Feedback

# We can reuse the Feedback model from main.py or redefine if needed
# from ..main import Feedback # Assuming Feedback model is in main for now
from ..main import get_database

router = APIRouter()

@router.post("/", response_description="Add new feedback")
async def create_feedback(request: Request, feedback: Feedback = Body(...)):
    """Submit new feedback."""
    feedback_dict = jsonable_encoder(feedback)
    
    # Perform sentiment analysis
    analysis = TextBlob(feedback_dict["feedback_text"])
    sentiment_score = analysis.sentiment.polarity
    
    # Add sentiment score to the feedback dictionary
    feedback_dict["sentiment_score"] = sentiment_score
    
    # Insert feedback into the database
    # Replace 'feedback_collection' with your actual collection name
    new_feedback = await request.app.mongodb["feedback_collection"].insert_one(feedback_dict)
    
    # Retrieve the inserted feedback to return
    created_feedback = await request.app.mongodb["feedback_collection"].find_one(
        {"_id": new_feedback.inserted_id}
    )
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_feedback)

@router.get(
    "/", response_description="Get all feedback", response_model=List[dict] # Use dict for now, can create response model later
)
async def list_feedback(request: Request):
    """List all feedback."""
    # Replace 'feedback_collection' with your actual collection name
    feedbacks = []
    for doc in await request.app.mongodb["feedback_collection"].find().to_list(length=100):
        feedbacks.append(doc) # Append the raw document for now
        
    return feedbacks

# Note: You might want to add error handling and more sophisticated responses
# Also consider adding endpoints for getting feedback by event, user, etc. 