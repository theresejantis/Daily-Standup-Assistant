from sqlalchemy.orm import Session
from datetime import datetime
from app.telemetry import tracer,logger
from app.model import (
    Employee,
    StandupUpdates,
    Blockers,
    TeamSummary 
)

from app.agents.summary_agent import summary_agent
def generate_summary(db: Session):

    standups = db.query(StandupUpdates).all()

    if not standups:
        logger.warning(
            "No standups available for summary generation"
        )
        return {
            "message": "No standups available."
        }

    employee_count = (
        db.query(Employee)
        .filter(Employee.role != "Manager")
        .count()
    )

    submitted_count = len(standups)

    if submitted_count < employee_count:
        logger.warning(
            f"Only {submitted_count} out of {employee_count} employees have submitted."
        )

        return {
            "message":
            f"Only {submitted_count} out of {employee_count} employees have submitted today's standup."
        }

    blockers = db.query(Blockers).all()

    if not blockers:
        logger.warning(
            "No blockers available for summary generation"
        )
        return {
            "message": "No blockers available."
        }

    yesterday_list = []
    today_list = []
    blocker_list = []

    for standup in standups:
        yesterday_list.append(
            standup.yesterdays_work
        )
        today_list.append(
            standup.todays_work
        )

    for blocker in blockers:
        blocker_list.append(
            blocker.blocker_description
        )

    input_text = f"""

Yesterday's Work:
{chr(20).join(yesterday_list)}

Today's Work:
{chr(20).join(today_list)}

Blockers:
{chr(20).join(blocker_list)}
"""

    with tracer.start_as_current_span("team_summary"):
        try:
            response = summary_agent.run(input_text)

            logger.info(
                "Team summary generated"
            )

        except Exception as e:

            logger.error(
                f"Summary generation failed: {str(e)}"
            )

            raise

    summary = TeamSummary(
        summary_date=datetime.utcnow(),
        summary_text=response.content
    )

    with tracer.start_as_current_span("save_team_summary"):

        db.add(summary)
        db.commit()
        db.refresh(summary)

        logger.info(
            f"Summary {summary.summary_id} created"
        )

    return summary


def get_all_summaries(db: Session):

    with tracer.start_as_current_span("get_all_summaries"):
        summaries = db.query(TeamSummary).all()

        logger.info(f"{len(summaries)} summaries retrieved")
        return summaries


def get_summary(db: Session, summary_id: int):

    with tracer.start_as_current_span("get_summary"):
        summary = db.query(TeamSummary).filter(
            TeamSummary.summary_id == summary_id
        ).first()

        if not summary:
            logger.warning(f"Summary {summary_id} not found")
            return None

        logger.info(f"Summary {summary_id} found")
        return summary


def delete_summary(db: Session, summary_id: int):

    with tracer.start_as_current_span("delete_summary"):
        summary = db.query(TeamSummary).filter(
            TeamSummary.summary_id == summary_id
        ).first()

        if not summary:
            logger.warning(f"Summary {summary_id} not found")
            return {"message": "Summary not found"}

        db.delete(summary)
        db.commit()

        logger.info(f"Summary {summary_id} deleted")
        return {"message": "Deleted Successfully"}