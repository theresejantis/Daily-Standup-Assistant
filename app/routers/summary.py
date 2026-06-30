from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.summary_services import (
    generate_summary,
    get_all_summaries,
    get_summary,
    delete_summary
)

router = APIRouter(
    prefix="/team-summaries",
    tags=["Team Summaries"]
)

@router.post("/")
def create_summary(
    db: Session = Depends(get_db)
):
    return generate_summary(db)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_summaries(db)

@router.get("/{summary_id}")
def get_by_id(summary_id: int,db: Session = Depends(get_db)):
    return get_summary(db,summary_id)

@router.delete("/{summary_id}")
def delete(summary_id: int,db: Session = Depends(get_db)):
    return delete_summary(db,summary_id)