from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.blocker_services import (
    get_all_blockers,
    get_blocker
)

router = APIRouter(
    prefix="/blockers",
    tags=["Blockers"]
)


@router.get("/")
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_blockers(db)


@router.get("/{blocker_id}")
def get_by_id(
    blocker_id: int,
    db: Session = Depends(get_db)
):
    return get_blocker(
        db,
        blocker_id
    )