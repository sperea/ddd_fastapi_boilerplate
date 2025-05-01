from fastapi import APIRouter, Depends
from sqlmodel import Session
from infrastructure.database import get_session
from backend.infrastructure.orm.sqlmodel_repo import SQLModelItemRepository
from app.use_cases.operations import list_items

router = APIRouter()

@router.get("/")
def get_items(session: Session = Depends(get_session)):
    repo = SQLModelItemRepository(session)
    return list_items(repo)
