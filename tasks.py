from celery import Celery
from automation_agent import AutomationAgent
from core.training_pipeline import TrainingPipeline
from loguru import logger
from config import settings

app = Celery('vision_automation', broker=settings.redis_url)

@app.task
def execute_automation_task(url: str, task: str, use_groq: bool = False):
    logger.info(f"Celery task started: {task}")
    agent = AutomationAgent(use_groq=use_groq, headless=True)
    result = agent.execute_task(url, task)
    return result

@app.task
def retrain_model_task(failed_actions: list):
    logger.info("Celery retraining task started")
    pipeline = TrainingPipeline()
    pipeline.retrain_model(failed_actions)
    return {"status": "completed"}
