from sqlalchemy import Column, Integer, String,DateTime,Text,ForeignKey
from datetime import datetime
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"
    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String,nullable=False)
    teams_user_id = Column(String,nullable=False)
    jira_user_id = Column(String,nullable=False)
    created_at = Column(DateTime ,default=datetime.utcnow,nullable=False)

class StandupUpdates(Base):
    __tablename__ = "standup_updates"

    update_id = Column(Integer,primary_key=True,index=True)
    employee_id= Column(Integer,ForeignKey ("employees.employee_id"),nullable=False)
    raw_msg= Column(Text,nullable=False)
    yesterdays_work=Column(Text,nullable=False)
    todays_work= Column(Text,nullable=False)
    submitted_at=Column(DateTime ,default=datetime.utcnow)
    progress_status= Column(Text)
    current_work_stage=Column(Text)

class Blockers(Base):
    __tablename__ = "blockers"
    blocker_id = Column(Integer,primary_key=True,index=True)
    updated_id = Column(Integer,ForeignKey("standup_updates.update_id"),nullable=False)
    blocker_description = Column(Text,nullable=False)
    status = Column(String)
    priority=Column(String)
    detected_at = Column(DateTime,default=datetime.utcnow)
    resolved_at = Column(DateTime)

class JiraTasks(Base):
    __tablename__ = "jira_tasks"

    task_id = Column(Integer,primary_key=True,index=True)
    employee_id = Column(Integer,ForeignKey("employees.employee_id"),nullable=False)
    jira_ticket_id = Column(String,nullable=False)
    task_title = Column(String,nullable=False)
    task_description = Column(Text)
    sprint_name = Column(String)
    task_status = Column(String)
    assigned_date = Column(DateTime)
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    last_synced = Column(DateTime,default=datetime.utcnow)

class ProgressAnalysis(Base):
    __tablename__ = "progress_analysis"

    analysis_id = Column(Integer,primary_key= True,index=True)
    update_id = Column(Integer,ForeignKey("standup_updates.update_id"),nullable=True)
    task_id = Column(Integer,ForeignKey("jira_tasks.task_id"),nullable=True)
    jira_task = Column(String)
    previous_progress = Column(Text)
    current_progress = Column(Text)
    work_status = Column(Text)
    jira_alignment = Column(String)
    delay_detected = Column(String)
    analyzed_at = Column(DateTime,default=datetime.utcnow)

class TeamSummary(Base):
    __tablename__ = "team_summaries"

    summary_id = Column(Integer,primary_key=True,index=True)
    summary_date = Column(DateTime,nullable=False)
    summary_text = Column(Text,nullable=False)
