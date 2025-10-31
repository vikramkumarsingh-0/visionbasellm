from automation_agent import AutomationAgent
from loguru import logger
import os

os.environ['GROQ_API_KEY'] = 'gsk_your_key_here'

logger.add("logs/demo.log")

agent = AutomationAgent(use_groq=True, headless=False)

result = agent.execute_task(
    url="https://example.com",
    task="Click the 'More information' link"
)

print("\n=== GROQ DEMO RESULT ===")
print(f"Success: {result['success']}")
print(f"Action: {result['decision']['action']}")
print(f"Reasoning: {result['decision']['reasoning']}")
print(f"Metrics: {result['metrics']}")
