from fastapi import APIRouter, HTTPException
from services.feedback_service import update_confidence_scores
from models.schemas import FeedbackRequest

router = APIRouter()

@router.post("/update-feedback")
def update_feedback(feedback: FeedbackRequest):
    try:
        result = update_confidence_scores(feedback)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
