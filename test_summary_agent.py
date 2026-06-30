from app.agents.summary_agent import summary_agent

response = summary_agent.run("""
Employee 1

Yesterday:
Completed Employee CRUD APIs

Today:
Working on Standup APIs

Blockers:
Waiting for Jira access approval


Employee 2

Yesterday:
Completed Login Integration

Today:
Payment testing and bug fixing

Blockers:
Waiting for production API approval


Employee 3

Yesterday:
Completed Authentication APIs

Today:
Dashboard integration

Blockers:
None
""")

print(response.content)