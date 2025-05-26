from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, index=True)
    feedback_text = Column(String)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)  # Positive, Negative, or Neutral
    created_at = Column(DateTime, default=datetime.utcnow)
    student_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    student = relationship("User", back_populates="feedbacks") 