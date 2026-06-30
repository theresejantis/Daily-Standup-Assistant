from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session


from app.database import get_db
from app.schemas import StandupCreate
from app.services.standup_services import (
    create_standup,
    get_all_standups,
    get_standup,
    update_standup,
    delete_standup
)

router = APIRouter(
    prefix="/standups",
    tags=["Standups"]
)

@router.post("/")
def create(standup: StandupCreate,db: Session = Depends(get_db)):
    return create_standup(db,standup)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_standups(db)

@router.get("/{update_id}")
def get_by_id(update_id: int,db: Session = Depends(get_db)):
    return get_standup(db,update_id)

@router.put("/{update_id}")
def update(update_id: int,standup_data: StandupCreate,db: Session = Depends(get_db)):
    return update_standup(db,update_id,standup_data)

@router.delete("/{update_id}")
def delete(update_id: int,db: Session = Depends(get_db)):
    return delete_standup(db,update_id)

