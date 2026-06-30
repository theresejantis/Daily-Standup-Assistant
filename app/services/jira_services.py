from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.model import JiraTasks
from app.telemetry import tracer, logger


def get_all_tasks(db: Session):

    with tracer.start_as_current_span("get_all_tasks"):
        tasks = db.query(JiraTasks).all()

        logger.info(f"{len(tasks)} tasks fetched")
        return tasks


def get_task(db: Session, task_id: int):

    with tracer.start_as_current_span("get_task"):
        task = db.query(JiraTasks).filter(
            JiraTasks.task_id == task_id
        ).first()

        if not task:
            logger.warning(f"Task {task_id} not found")
            return None

        logger.info(f"Task {task_id} found")
        return task


def delete_task(db: Session, task_id: int):

    with tracer.start_as_current_span("delete_task"):
        task = db.query(JiraTasks).filter(
            JiraTasks.task_id == task_id
        ).first()

        if not task:
            logger.warning(f"Task {task_id} not found")

            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        db.delete(task)
        db.commit()

        logger.info(f"Task {task_id} deleted")
        return {"message":"Task deleted successfully"}