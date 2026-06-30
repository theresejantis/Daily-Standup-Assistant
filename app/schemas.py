from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmployeeCreate(BaseModel):

    employee_name: str
    email: str
    role: str
    teams_user_id: Optional[str] = None
    jira_user_id: Optional[str] = None

class EmployeeResponse(BaseModel):

    employee_id: int
    employee_name: str
    email: str
    role: str
    teams_user_id: str | None
    jira_user_id: str | None
    created_at: datetime
    class Config:
        from_attributes = True

class StandupCreate(BaseModel):
    employee_id:int
    raw_msg: str

class StandupResponse(BaseModel):
    update_id:int
    employee_id:int
    raw_msg:str
    yesterdays_work:str
    todays_work:str
    submitted_at:datetime
    class Config:
        from_attributes = True



class BlockerResponse(BaseModel):

    blocker_id: int
    updated_id: int
    blocker_description: str
    status: str | None
    priority: str | None
    detected_at: datetime
    resolved_at: datetime | None

    class Config:
        from_attributes = True

class JiraTaskResponse(BaseModel):

    task_id: int
    employee_id: int
    jira_ticket_id: str
    task_title: str
    task_description: str | None
    sprint_name: str | None
    task_status: str | None
    assigned_date: datetime | None
    due_date: datetime | None
    completed_date: datetime | None
    last_synced: datetime

    class Config:
        from_attributes = True


class ProgressAnalysisResponse(BaseModel):

    analysis_id: int
    update_id: int
    task_id: int | None
    jira_task: str | None
    previous_progress: str | None
    current_progress: str | None
    work_status: str | None
    jira_alignment: str | None
    delay_detected: str | None
    analyzed_at: datetime

    class Config:
        from_attributes = True

class TeamSummaryResponse(BaseModel):

    summary_id: int
    summary_date: datetime
    summary_text: str

    class Config:
        from_attributes = True