from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model import Blockers
from app.telemetry import tracer, logger


def get_all_blockers(
    db: Session
):

    with tracer.start_as_current_span("get_all_blockers"):
        blockers = db.query(Blockers).all()

        logger.info(f"{len(blockers)} blockers retrieved")
        return blockers


def get_blocker(
    db: Session,
    blocker_id: int
):

    with tracer.start_as_current_span("get_blocker"):
        blocker = (
            db.query(Blockers)
            .filter(Blockers.blocker_id == blocker_id)
            .first()
        )

        if not blocker:
            logger.warning(f"Blocker {blocker_id} not found")

            raise HTTPException(
                status_code=404,
                detail="Blocker not found"
            )

        logger.info(f"Blocker {blocker_id} found")
        return blocker