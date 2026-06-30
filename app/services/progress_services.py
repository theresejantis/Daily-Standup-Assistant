from sqlalchemy.orm import Session
import json
from pathlib import Path
from app.telemetry import tracer,logger
from app.model import ProgressAnalysis, StandupUpdates
from app.agents.standup_agent import standup_agent


def get_all_analysis(db: Session):

    with tracer.start_as_current_span("get_all_analysis"):
        analysis = db.query(ProgressAnalysis).all()

        logger.info(f"{len(analysis)} analyses retrieved")
        return analysis


def get_analysis(db: Session, analysis_id: int):

    with tracer.start_as_current_span("get_analysis"):
        analysis = db.query(ProgressAnalysis).filter(
            ProgressAnalysis.analysis_id == analysis_id
        ).first()

        if not analysis:
            logger.warning(f"Analysis {analysis_id} not found")
            return None

        logger.info(f"Analysis {analysis_id} found")
        return analysis


def delete_analysis(db: Session, analysis_id: int):

    with tracer.start_as_current_span("delete_analysis"):
        analysis = db.query(ProgressAnalysis).filter(
            ProgressAnalysis.analysis_id == analysis_id
        ).first()

        if not analysis:
            logger.warning(
                f"Analysis {analysis_id} not found")
            return {"message": "Analysis not found"}

        try:

            db.delete(analysis)
            db.commit()

            logger.info(
                f"Analysis {analysis_id} deleted")
            return {"message": "Deleted Successfully"}

        except Exception as e:

            db.rollback()

            logger.error(
                f"Failed to delete analysis {analysis_id}: {str(e)}")

            raise 


def create_analysis(db: Session, employee_id: int):

    logger.info(
        f"Starting progress analysis for employee {employee_id}"
    )

    standup = (
        db.query(StandupUpdates)
        .filter(
            StandupUpdates.employee_id == employee_id
        )
        .order_by(
            StandupUpdates.submitted_at.desc()
        )
        .first()
    )

    if not standup:
        logger.warning(
            f"No standup found for employee {employee_id}"
        )
        return {
            "message": "No standup found for employee"
        }

    existing_analysis = (
        db.query(ProgressAnalysis)
        .filter(
            ProgressAnalysis.update_id == standup.update_id
        )
        .first()
    )

    json_path = Path("jira_tasks.json")

    with open(json_path, "r") as f:
        jira_tasks = json.load(f)

    task = next(
        (
            t for t in jira_tasks
            if t["employee_id"] == employee_id
        ),
        None
    )

    if not task:
        logger.warning(
            f"No Jira task found for employee {employee_id}"
        )
        return {
            "message": "No Jira task found for employee"
        }

    prompt = f"""
You are a project progress analysis assistant.

Assigned Jira Task:
{task["task_title"]}

Yesterday's Work:
{standup.yesterdays_work}

Today's Work:
{standup.todays_work}

Analyze:

1. Compare yesterday's work and today's work against the Jira task.

2. jira_alignment must be one of:
   - Aligned
   - Partially Aligned
   - Not Aligned

3. work_status should be a professional sentence explaining progress.

4. delay_detected must be one of:
   - No Delay
   - Potential Delay
   - Delay Detected

5. Return meaningful explanations.

Return ONLY JSON:

{{
    "jira_task": "",
    "previous_progress": "",
    "current_progress": "",
    "jira_alignment": "",
    "work_status": "",
    "delay_detected": ""
}}
"""

    with tracer.start_as_current_span("progress_analysis"):
        try:
            response = standup_agent.run(prompt)
            logger.info("Progress analysis completed")

        except Exception as e:
            logger.error(
            f"Progress analysis failed: {str(e)}"
            )
            raise


    
    data = json.loads(response.content)
    with tracer.start_as_current_span("save_progress_analysis"):

        if existing_analysis:

            existing_analysis.jira_task = data["jira_task"]
            existing_analysis.previous_progress = data["previous_progress"]
            existing_analysis.current_progress = data["current_progress"]
            existing_analysis.jira_alignment = data["jira_alignment"]
            existing_analysis.work_status = data["work_status"]
            existing_analysis.delay_detected = data["delay_detected"]

            db.commit()
            db.refresh(existing_analysis)

            logger.info(
                f"Analysis {existing_analysis.analysis_id} updated"
            )

            return existing_analysis

        analysis = ProgressAnalysis(
            update_id=standup.update_id,
            task_id=None,
            jira_task=data["jira_task"],
            previous_progress=data["previous_progress"],
            current_progress=data["current_progress"],
            jira_alignment=data["jira_alignment"],
            work_status=data["work_status"],
            delay_detected=data["delay_detected"]
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        logger.info(
            f"Analysis {analysis.analysis_id} created"
        )

        return analysis