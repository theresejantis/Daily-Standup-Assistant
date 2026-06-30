from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.model import Employee
from app.schemas import EmployeeCreate
from app.services.employee_services import (
    create_employee,get_all_employees,get_employee,delete_employee,update_employee
)

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.post("/")
def create(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return create_employee(db, employee)


@router.get("/")
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_employees(db)


@router.get("/{employee_id}")
def get_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return get_employee(db, employee_id)


@router.delete("/{employee_id}")
def delete(
    employee_id: int,
    db: Session = Depends(get_db)
):
    return delete_employee(db, employee_id)

@router.put("/{employee_id}")
def update(
    employee_id:int,
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    return update_employee(db, employee_id, employee)