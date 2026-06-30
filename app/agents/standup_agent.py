import os
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

standup_agent = Agent(
    model=Groq(
        id=os.getenv("MODEL_ID"),
        api_key=os.getenv("GROQ_API_KEY")
    ),
    instructions=[
        """
Extract:
- yesterdays_work
- todays_work
- blockers

Return ONLY a JSON object.

Do not explain.
Do not write code.
Do not use markdown.
Do not use ```json.

Example:

{
    "yesterdays_work": "Employee CRUD APIs",
    "todays_work": "Standup APIs",
    "blockers": "Waiting for Jira approval"
}
"""
    ],
    markdown=False
)