from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.progress_services import (
    create_analysis,
    get_all_analysis,
    get_analysis,
    delete_analysis
    
)

router = APIRouter(
    prefix="/progress-analysis",
    tags=["Progress Analysis"]
)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_analysis(db)

@router.get("/{analysis_id}")
def get_by_id(analysis_id: int,db: Session = Depends(get_db)):
    return get_analysis(db,analysis_id)

@router.delete("/{analysis_id}")
def delete(analysis_id: int,db: Session = Depends(get_db)):
    return delete_analysis(db,analysis_id)

@router.post("/{employee_id}")
def create(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return create_analysis(db, employee_id)