from automation_agent import AutomationAgent
from loguru import logger

logger.add("logs/test.log")

agent = AutomationAgent(use_groq=False, headless=False)

result = agent.execute_task(
    url="https://www.google.com",
    task="Find the search box"
)

print("\n=== RESULT ===")
print(f"Success: {result['success']}")
print(f"Decision: {result['decision']}")
print(f"Metrics: {result['metrics']}")
