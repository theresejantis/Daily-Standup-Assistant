from fastapi import FastAPI
import app.telemetry
from app.database import Base
from app.database import engine

from app.routers.employee import router as employee_router
from app.routers.standup_update import router as standup_router
from app.routers.blocker import router as blocker_router
from app.routers.jira import router as jira_router
from app.routers.progress import router as progress_router
from app.routers.summary import router as summary_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(employee_router)
app.include_router(standup_router)
app.include_router(jira_router)
app.include_router(blocker_router)
app.include_router(progress_router)
app.include_router(summary_router)


