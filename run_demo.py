from automation_agent import AutomationAgent
from loguru import logger

logger.add("logs/demo.log")

print("Starting Vision-Based Web Automation Demo...")
print("=" * 50)

agent = AutomationAgent(use_groq=False, headless=False)

print("\nTest 1: Google Search")
result = agent.execute_task(
    url="https://www.google.com",
    task="Click the search box"
)

print(f"\nSuccess: {result['success']}")
print(f"Action: {result['decision']['action']}")
print(f"Reasoning: {result['decision']['reasoning']}")
print(f"Metrics: {result['metrics']}")
print("\nDemo completed!")
