from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model import Employee
from app.schemas import EmployeeCreate
from app.telemetry import tracer, logger


def create_employee(
    db: Session,
    employee: EmployeeCreate
):
    with tracer.start_as_current_span("create_employee"):

        db_employee = Employee(
            employee_name=employee.employee_name,
            email=employee.email,
            role=employee.role,
            teams_user_id=employee.teams_user_id,
            jira_user_id=employee.jira_user_id
        )

        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)

        logger.info(
            f"Employee {db_employee.employee_id} created"
        )

        return db_employee


def get_all_employees(
    db: Session
):
    with tracer.start_as_current_span("get_all_employees"):

        employees = db.query(Employee).all()

        logger.info(
            f"{len(employees)} employees retrieved"
        )

        return employees


def get_employee(
    db: Session,
    employee_id: int
):
    with tracer.start_as_current_span("get_employee"):

        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:

            logger.warning(
                f"Employee {employee_id} not found"
            )

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        logger.info(
            f"Employee {employee_id} found"
        )

        return employee


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeCreate
):
    with tracer.start_as_current_span("update_employee"):

        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:

            logger.warning(
                f"Employee {employee_id} not found"
            )

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        employee.employee_name = employee_data.employee_name
        employee.email = employee_data.email
        employee.role = employee_data.role
        employee.teams_user_id = employee_data.teams_user_id
        employee.jira_user_id = employee_data.jira_user_id

        db.commit()
        db.refresh(employee)

        logger.info(
            f"Employee {employee_id} updated"
        )

        return employee


def delete_employee(
    db: Session,
    employee_id: int
):
    with tracer.start_as_current_span("delete_employee"):

        employee = (
            db.query(Employee)
            .filter(Employee.employee_id == employee_id)
            .first()
        )

        if not employee:

            logger.warning(
                f"Employee {employee_id} not found"
            )

            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        try:

            db.delete(employee)
            db.commit()

            logger.info(
                f"Employee {employee_id} deleted"
            )

            return {
                "message": "Deleted Successfully"
            }

        except Exception as e:

            logger.error(
                f"Failed to delete employee {employee_id}: {str(e)}"
            )

            raise