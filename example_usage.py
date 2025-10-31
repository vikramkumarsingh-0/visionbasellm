from automation_agent import AutomationAgent
from loguru import logger

logger.add("logs/automation.log", rotation="500 MB")

def example_1_basic_automation():
    agent = AutomationAgent(use_groq=False, headless=False)
    
    result = agent.execute_task(
        url="https://www.google.com",
        task="Click the search button"
    )
    
    logger.info(f"Result: {result}")

def example_2_with_groq():
    agent = AutomationAgent(use_groq=True, headless=True)
    
    result = agent.execute_task(
        url="https://example.com",
        task="Find and click the 'More information' link"
    )
    
    logger.info(f"Result: {result}")

def example_3_form_filling():
    agent = AutomationAgent(use_groq=False, headless=False)
    
    result = agent.execute_task(
        url="https://www.google.com",
        task="Type 'AI automation' in the search box"
    )
    
    logger.info(f"Result: {result}")

if __name__ == "__main__":
    example_1_basic_automation()
