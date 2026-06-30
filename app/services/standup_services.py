from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import json
from app.schemas import StandupCreate
from app.agents.standup_agent import standup_agent
from app.services.progress_services import create_analysis
from app.telemetry import tracer, logger

from app.model import (
    StandupUpdates,
    Blockers,
    Employee
)


def create_standup(db: Session, standup: StandupCreate):

    logger.info(
        f"Starting standup creation for employee {standup.employee_id}"
    )

    if not standup.raw_msg.strip():

        logger.warning("Standup message is empty")

        return {
            "message": "Standup message cannot be empty"
        }

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == standup.employee_id)
        .first()
    )

    if not employee:

        logger.warning(
            f"No employee with ID {standup.employee_id}"
        )

        return {
            "message": "No employee found"
        }

    today = datetime.utcnow().date()

    existing_standup = (
        db.query(StandupUpdates)
        .filter(
            StandupUpdates.employee_id == standup.employee_id,
            func.date(StandupUpdates.submitted_at) == today
        )
        .first()
    )

    if existing_standup:

        logger.warning(
            f"Employee {standup.employee_id} has already submitted today's standup"
        )

        return {
            "message": "Standup already submitted today.",
            "already_submitted": True,
            "update_id": existing_standup.update_id
        }

    with tracer.start_as_current_span("standup_analysis"):

        try:

            response = standup_agent.run(
                standup.raw_msg
            )

            logger.info(
                "Standup analysis completed"
            )

        except Exception as e:

            logger.error(
                f"Standup analysis failed: {str(e)}"
            )

            raise

    logger.info("RAW RESPONSE")
    logger.info(response.content)

    data = json.loads(response.content)

    with tracer.start_as_current_span("save_standup"):

        standup_update = StandupUpdates(
            employee_id=standup.employee_id,
            raw_msg=standup.raw_msg,
            yesterdays_work=data["yesterdays_work"],
            todays_work=data["todays_work"]
        )

        db.add(standup_update)
        db.commit()
        db.refresh(standup_update)

        logger.info(
            f"Standup saved with ID {standup_update.update_id}"
        )

    with tracer.start_as_current_span("save_blocker"):

        blocker = Blockers(
            updated_id=standup_update.update_id,
            blocker_description=data["blockers"]
        )

        db.add(blocker)
        db.commit()

        logger.info(
            "Blocker saved successfully"
        )

        logger.info(
            "Generating progress analysis"
        )
        create_analysis(
            db,
            standup.employee_id
        )



    return {
        "update_id": standup_update.update_id,
        "employee_id": standup_update.employee_id,
        "raw_msg": standup_update.raw_msg,
        "yesterdays_work": standup_update.yesterdays_work,
        "todays_work": standup_update.todays_work,
        "submitted_at": standup_update.submitted_at
    }



def get_all_standups(db: Session):

    with tracer.start_as_current_span("get_all_standups"):

        standups = db.query(StandupUpdates).all()

        logger.info(
            f"{len(standups)} standups retrieved")
        return standups


def get_standup(db: Session, update_id: int):

    with tracer.start_as_current_span("get_standup"):
        standup = db.query(StandupUpdates).filter( StandupUpdates.update_id == update_id).first()

        if not standup:
            logger.warning(
                f"Standup {update_id} not found")

            return None

        logger.info(f"Standup {update_id} found")

        return standup


def delete_standup(db: Session, update_id: int):

    with tracer.start_as_current_span("delete_standup"):
        standup = db.query(StandupUpdates).filter(
            StandupUpdates.update_id == update_id
        ).first()

        if not standup:

            logger.warning(
                f"Standup {update_id} not found")
            return {"message": "Standup not found"}

        blockers = db.query(Blockers).filter(
            Blockers.updated_id == update_id
        ).all()

        try:

            for blocker in blockers:
                db.delete(blocker)

            db.delete(standup)
            db.commit()

            logger.info(
                f"Standup {update_id} deleted")
            return {"message": "Deleted standup Successfully"}

        except Exception as e:

            db.rollback()

            logger.error(
                f"Failed to delete standup {update_id}: {str(e)}")

            raise


def update_standup(
    db: Session,
    update_id: int,
    standup: StandupCreate
):

    with tracer.start_as_current_span("update_standup"):

        db_standup = (
            db.query(StandupUpdates)
            .filter(
                StandupUpdates.update_id == update_id
            )
            .first()
        )

        if not db_standup:

            logger.warning(
                f"Standup {update_id} not found"
            )

            return {
                "message": "Standup not found"
            }

        try:

            response = standup_agent.run(
                standup.raw_msg
            )

            logger.info(
                "Standup re-analysis completed"
            )

        except Exception as e:

            logger.error(
                f"Standup re-analysis failed: {str(e)}"
            )

            raise

        logger.info("RAW RESPONSE")
        logger.info(response.content)
        data = json.loads(response.content)

        with tracer.start_as_current_span(
            "update_standup_data"
        ):

            db_standup.raw_msg = standup.raw_msg
            db_standup.yesterdays_work = data["yesterdays_work"]
            db_standup.todays_work = data["todays_work"]
            logger.info(
                f"Standup {update_id} updated"
            )

        blocker = (
            db.query(Blockers)
            .filter(
                Blockers.updated_id == update_id
            )
            .first()
        )

        if blocker:
            blocker.blocker_description = data["blockers"]
            logger.info(
                f"Blocker updated for standup {update_id}"
            )

        else:
            blocker = Blockers(
                updated_id=update_id,
                blocker_description=data["blockers"]
            )

            db.add(blocker)
            logger.info(
                f"New blocker created for standup {update_id}"
            )
        db.commit()
        db.refresh(db_standup)

        logger.info(
            "Updating progress analysis"
        )

        create_analysis(
            db,
            db_standup.employee_id
        )

        return {
            "update_id": db_standup.update_id,
            "employee_id": db_standup.employee_id,
            "raw_msg": db_standup.raw_msg,
            "yesterdays_work": db_standup.yesterdays_work,
            "todays_work": db_standup.todays_work,
            "submitted_at": db_standup.submitted_at
        }