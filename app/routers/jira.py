from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.services.jira_services import (
    get_all_tasks,
    get_task,
    delete_task
)

router = APIRouter(
    prefix="/jira-tasks",
    tags=["Jira Tasks"]
)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    return get_all_tasks(db)

@router.get("/{task_id}")
def get_by_id(task_id: int,db: Session = Depends(get_db)):
    return get_task(db,task_id)

@router.delete("/{task_id}")
def delete(task_id: int,db: Session = Depends(get_db)):
    return delete_task(db,task_id)

