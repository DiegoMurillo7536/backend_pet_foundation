from fastapi import APIRouter, Depends
from models.models import Foundation
from repositories.foundation import FoundationRepository
from apis.security.security import get_api_key
from http import HTTPStatus

foundation_app = APIRouter(
    prefix="/foundations",
    tags=["Foundations"]
)

@foundation_app.get("/")
def get_foundations(api_key: str = Depends(get_api_key)):
    repository = FoundationRepository()
    foundations = repository.get_all()
    return repository.create_response_body(
        {'foundations': foundations},
        "Foundations fetched successfully",
        HTTPStatus.OK.value
    )

@foundation_app.post("/")
def create_foundation(foundation: Foundation, api_key: str = Depends(get_api_key)):
    repository = FoundationRepository()
    created_foundation = repository.create(foundation)
    return repository.create_response_body(
        {'foundation': created_foundation},
        "Foundation created successfully",
        HTTPStatus.CREATED.value
    )

@foundation_app.delete("/{foundation_id}")
def delete_foundation(foundation_id: int, api_key: str = Depends(get_api_key)):
    repository = FoundationRepository()
    repository.delete(foundation_id)
    return repository.create_response_body(
        {},
        "Foundation deleted successfully",
        HTTPStatus.OK.value
    )

@foundation_app.put("/{foundation_id}")
def update_foundation(foundation_id: int, foundation: Foundation, api_key: str = Depends(get_api_key)):
    repository = FoundationRepository()
    repository.update(foundation_id, foundation)
    return repository.create_response_body(
        {},
        "Foundation updated successfully",
        HTTPStatus.OK.value
    )
    

@foundation_app.get("/{foundation_id}/goals")
def get_goals_by_foundation_id(foundation_id: int, api_key: str = Depends(get_api_key)):
    repository = FoundationRepository()
    goals = repository.get_all_with_goals_and_actual_amount_by_id(foundation_id)
    response = repository.create_response_body(
        {'goals': goals},
        "Goals fetched successfully",
        HTTPStatus.OK.value
    )
    return response