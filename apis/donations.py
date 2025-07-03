from fastapi import APIRouter, Depends
from models.models import Donation
from repositories.donation import DonationRepository
from apis.security.security import get_api_key
from http import HTTPStatus
from pydantic import BaseModel

class DonationRequest(BaseModel):
    person_name: str
    amount: float
    goal_category_id: int
    foundation_id: int
    description: str

donation_app = APIRouter(
    prefix="/donations",
    tags=["Donations"]
)

@donation_app.post("/")
def create_donation(
    request: DonationRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Create a new donation and associate it with a goal
    """
    donation = Donation(
        person_name=request.person_name,
        amount=request.amount
    )
    
    donation_repository = DonationRepository()
    created_donation = donation_repository.create(
        donation=donation,
        description=request.description,
        goal_category_id=request.goal_category_id,
        foundation_id=request.foundation_id
    )
    
    return donation_repository.create_response_body(
        {'donation': created_donation},
        "Donation created successfully",
        HTTPStatus.CREATED.value
    )
