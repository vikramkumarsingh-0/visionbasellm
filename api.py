from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from automation_agent import AutomationAgent
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
from core.security import SecurityValidator
import time
from loguru import logger

app = FastAPI(title="Vision-Based Web Automation API")

automation_requests = Counter('automation_requests_total', 'Total automation requests')
automation_duration = Histogram('automation_duration_seconds', 'Automation execution time')
automation_success = Counter('automation_success_total', 'Successful automations')
automation_failures = Counter('automation_failures_total', 'Failed automations')
security_blocks = Counter('security_blocks_total', 'Blocked malicious requests')

class AutomationRequest(BaseModel):
    url: str
    task: str
    browser_type: str = 'chromium'
    use_groq: bool = False
    headless: bool = True
    proxy: Optional[dict] = None
    session_id: Optional[str] = None
    
    @validator('browser_type')
    def validate_browser(cls, v):
        allowed = ['chromium', 'firefox', 'webkit']
        if v not in allowed:
            raise ValueError(f"Browser must be one of {allowed}")
        return v
    
    @validator('url')
    def validate_url(cls, v):
        try:
            return SecurityValidator.validate_url(v)
        except ValueError as e:
            raise ValueError(f"Invalid URL: {e}")
    
    @validator('task')
    def validate_task(cls, v):
        try:
            return SecurityValidator.validate_task(v)
        except ValueError as e:
            raise ValueError(f"Invalid task: {e}")

@app.post("/automate")
async def automate(request: AutomationRequest):
    automation_requests.inc()
    start_time = time.time()
    
    try:
        agent = AutomationAgent(
            browser_type=request.browser_type,
            use_groq=request.use_groq,
            headless=request.headless,
            proxy=request.proxy,
            session_id=request.session_id
        )
        result = agent.execute_task(request.url, request.task)
        
        duration = time.time() - start_time
        automation_duration.observe(duration)
        
        if result['success']:
            automation_success.inc()
        else:
            automation_failures.inc()
        
        return result
    except ValueError as e:
        security_blocks.inc()
        logger.warning(f"Security block: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        automation_failures.inc()
        logger.error(f"Automation error: {e}")
        raise HTTPException(status_code=500, detail="Automation failed")

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.get("/health")
async def health():
    return {"status": "healthy"}
