import os
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

summary_agent = Agent(
    model=Groq(
        id=os.getenv("MODEL_ID"),
        api_key=os.getenv("GROQ_API_KEY")
    ),
    description="Team Standup Summary Agent",
    instructions=[
    "Create a clean team standup summary.",
    "Group all Yesterday's Work items together.",
    "Group all Today's Work items together.",
    "Group all Blockers together.",
    "Use bullet points.",
    "Do not repeat headings.",
    "Return plain text only."
],
    markdown=True
) 
