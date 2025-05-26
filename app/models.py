from pydantic import BaseModel

class Feedback(BaseModel):
    feedback_text: str
    # sentiment_score: float = None # We will add this after analysis 