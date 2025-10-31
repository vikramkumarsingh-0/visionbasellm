# Project Analysis Report - Part 2: API & Authentication

## 5. API MODULE (Continued)

### 5.2 Enterprise Upgrades Needed

**Priority 1: Authentication & Authorization**

```python
# JWT Authentication
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

class AuthManager:
    SECRET_KEY = "your-secret-key"
    
    def create_token(self, user_id, role):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")

# Protected endpoint
@app.post("/automate")
async def automate(
    request: AutomationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    user = auth_manager.verify_token(credentials.credentials)
    
    # Check permissions
    if not has_permission(user, 'automate'):
        raise HTTPException(403, "Insufficient permissions")
    
    # Execute with user context
    result = agent.execute_task(request.url, request.task, user_id=user['user_id'])
    return result
```

**Priority 2: User Management**

```python
# User model
class User(BaseModel):
    id: str
    email: str
    role: str  # admin, user, viewer
    api_quota: int
    created_at: datetime

# User endpoints
@app.post("/auth/register")
async def register(email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    user = User(
        id=str(uuid.uuid4()),
        email=email,
        role='user',
        api_quota=1000
    )
    db.users.insert_one(user.dict())
    return {"user_id": user.id}

@app.post("/auth/login")
async def login(email: str, password: str):
    user = db.users.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode(), user['password']):
        raise HTTPException(401, "Invalid credentials")
    
    token = auth_manager.create_token(user['id'], user['role'])
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user = auth_manager.verify_token(credentials.credentials)
    return db.users.find_one({"id": user['user_id']})
```

**Priority 3: API Versioning**

```python
from fastapi import APIRouter

# Version 1
v1_router = APIRouter(prefix="/api/v1")

@v1_router.post("/automate")
async def automate_v1(request: AutomationRequest):
    # V1 implementation
    pass

# Version 2 with enhanced features
v2_router = APIRouter(prefix="/api/v2")

@v2_router.post("/automate")
async def automate_v2(request: AutomationRequestV2):
    # V2 with additional features
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

**Priority 4: Request Queuing**

```python
from celery import Celery
from redis import Redis

celery_app = Celery('tasks', broker='redis://localhost:6379')
redis_client = Redis()

@app.post("/automate/async")
async def automate_async(request: AutomationRequest, user: dict = Depends(get_current_user)):
    # Create job
    job_id = str(uuid.uuid4())
    
    # Queue task
    task = celery_app.send_task(
        'automation_agent.execute',
        args=[request.url, request.task],
        kwargs={'user_id': user['id']},
        task_id=job_id
    )
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str, user: dict = Depends(get_current_user)):
    task = celery_app.AsyncResult(job_id)
    return {
        "job_id": job_id,
        "status": task.state,
        "result": task.result if task.ready() else None
    }
```

**Priority 5: WebSocket Support**

```python
from fastapi import WebSocket

@app.websocket("/ws/automate")
async def websocket_automate(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive task
            data = await websocket.receive_json()
            
            # Execute with streaming updates
            async for update in agent.execute_task_stream(data['url'], data['task']):
                await websocket.send_json({
                    "type": "progress",
                    "data": update
                })
            
            # Send final result
            await websocket.send_json({
                "type": "complete",
                "data": result
            })
    except WebSocketDisconnect:
        pass
```

**Priority 6: API Documentation**

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Vision-Based Automation API",
        version="2.0.0",
        description="Enterprise-grade web automation with AI",
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 6. TRAINING PIPELINE MODULE

### 6.1 Current Implementation

**File**: `core/training_pipeline.py`

**Purpose**: Auto-retraining on failures

**Key Functions**:
```python
class TrainingPipeline:
    def prepare_dataset(failed_actions)
    def create_data_yaml()
    def retrain_model(failed_actions, epochs=30)
```

**How It Works**:
1. Collects failed automation attempts
2. Validates training data
3. Creates YOLO dataset
4. Retrains model
5. Saves new model version

**Current Limitations**:
- Manual trigger only
- No A/B testing
- No model versioning
- No rollback mechanism
- No performance tracking

### 6.2 Enterprise Upgrades Needed

**Priority 1: Automated Training Pipeline**

```python
class AutoTrainingPipeline:
    def __init__(self):
        self.failure_threshold = 10
        self.training_scheduler = BackgroundScheduler()
        
    def start_monitoring(self):
        # Check every hour
        self.training_scheduler.add_job(
            self.check_and_train,
            'interval',
            hours=1
        )
        self.training_scheduler.start()
    
    def check_and_train(self):
        failures = db.failures.count({'trained': False})
        
        if failures >= self.failure_threshold:
            logger.info(f"Triggering training with {failures} samples")
            self.train_new_model()
```

**Priority 2: Model Versioning**

```python
class ModelVersionManager:
    def __init__(self):
        self.versions = {}
        
    def save_model(self, model, metrics):
        version = f"v{len(self.versions) + 1}.0.0"
        
        model_info = {
            'version': version,
            'path': f"models/yolo_{version}.pt",
            'metrics': metrics,
            'timestamp': datetime.now(),
            'status': 'testing'
        }
        
        model.save(model_info['path'])
        self.versions[version] = model_info
        
        return version
    
    def promote_to_production(self, version):
        self.versions[version]['status'] = 'production'
        # Update symlink
        os.symlink(
            self.versions[version]['path'],
            'models/yolo_production.pt'
        )
```

**Priority 3: A/B Testing**

```python
class ABTestManager:
    def __init__(self):
        self.model_a = VisionDetector('models/yolo_v1.pt')
        self.model_b = VisionDetector('models/yolo_v2.pt')
        self.split_ratio = 0.5
        
    def get_model(self, user_id):
        # Consistent assignment
        if hash(user_id) % 100 < self.split_ratio * 100:
            return self.model_a, 'A'
        return self.model_b, 'B'
    
    def log_result(self, user_id, model_version, success):
        db.ab_tests.insert_one({
            'user_id': user_id,
            'model': model_version,
            'success': success,
            'timestamp': datetime.now()
        })
    
    def analyze_results(self):
        results_a = db.ab_tests.find({'model': 'A'})
        results_b = db.ab_tests.find({'model': 'B'})
        
        success_rate_a = sum(r['success'] for r in results_a) / len(results_a)
        success_rate_b = sum(r['success'] for r in results_b) / len(results_b)
        
        return {
            'model_a': success_rate_a,
            'model_b': success_rate_b,
            'winner': 'B' if success_rate_b > success_rate_a else 'A'
        }
```

**Priority 4: Performance Tracking**

```python
class ModelPerformanceTracker:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    def track_inference(self, model_version, duration, confidence, success):
        self.metrics[model_version].append({
            'duration': duration,
            'confidence': confidence,
            'success': success,
            'timestamp': datetime.now()
        })
    
    def get_metrics(self, model_version, window_hours=24):
        cutoff = datetime.now() - timedelta(hours=window_hours)
        recent = [
            m for m in self.metrics[model_version]
            if m['timestamp'] > cutoff
        ]
        
        return {
            'avg_duration': np.mean([m['duration'] for m in recent]),
            'avg_confidence': np.mean([m['confidence'] for m in recent]),
            'success_rate': np.mean([m['success'] for m in recent]),
            'total_requests': len(recent)
        }
```

---

## 7. DATABASE & STORAGE

### 7.1 Current Implementation

**Status**: Not implemented (file-based only)

**Current Storage**:
- Screenshots: `data/screenshots/`
- Models: `models/`
- Logs: `logs/`

### 7.2 Enterprise Implementation Needed

**Priority 1: Database Schema**

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(String)
    api_quota = Column(Integer)
    created_at = Column(DateTime)

class AutomationJob(Base):
    __tablename__ = 'automation_jobs'
    id = Column(String, primary_key=True)
    user_id = Column(String)
    url = Column(String)
    task = Column(String)
    status = Column(String)  # queued, running, completed, failed
    result = Column(JSON)
    created_at = Column(DateTime)
    completed_at = Column(DateTime)

class ModelVersion(Base):
    __tablename__ = 'model_versions'
    version = Column(String, primary_key=True)
    path = Column(String)
    metrics = Column(JSON)
    status = Column(String)  # testing, production, deprecated
    created_at = Column(DateTime)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    action = Column(String)
    details = Column(JSON)
    ip_address = Column(String)
    timestamp = Column(DateTime)

# Initialize
engine = create_engine('postgresql://user:pass@localhost/automation_db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

**Priority 2: Object Storage**

```python
import boto3

class S3Storage:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket = 'automation-screenshots'
        
    def upload_screenshot(self, job_id, image_path):
        key = f"screenshots/{job_id}/{Path(image_path).name}"
        self.s3.upload_file(image_path, self.bucket, key)
        return f"s3://{self.bucket}/{key}"
    
    def upload_model(self, version, model_path):
        key = f"models/{version}/model.pt"
        self.s3.upload_file(model_path, self.bucket, key)
        return f"s3://{self.bucket}/{key}"
    
    def download_model(self, version, local_path):
        key = f"models/{version}/model.pt"
        self.s3.download_file(self.bucket, key, local_path)
```

**Priority 3: Caching Layer**

```python
import redis
import pickle

class CacheManager:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.ttl = 3600  # 1 hour
        
    def cache_detection_result(self, image_hash, result):
        key = f"detection:{image_hash}"
        self.redis.setex(key, self.ttl, pickle.dumps(result))
    
    def get_cached_detection(self, image_hash):
        key = f"detection:{image_hash}"
        cached = self.redis.get(key)
        return pickle.loads(cached) if cached else None
    
    def cache_llm_response(self, prompt_hash, response):
        key = f"llm:{prompt_hash}"
        self.redis.setex(key, self.ttl, pickle.dumps(response))
```

---

## 8. MONITORING & OBSERVABILITY

### 8.1 Current Implementation

**File**: `monitoring/prometheus.yml`

**Metrics**:
- `automation_requests_total`
- `automation_success_total`
- `automation_failures_total`
- `security_blocks_total`

### 8.2 Enterprise Upgrades Needed

**Priority 1: Comprehensive Metrics**

```python
from prometheus_client import Counter, Histogram, Gauge, Info

# Business metrics
automation_requests = Counter('automation_requests_total', 'Total requests', ['user_id', 'endpoint'])
automation_duration = Histogram('automation_duration_seconds', 'Duration', ['task_type'])
automation_success = Counter('automation_success_total', 'Successful', ['task_type'])
automation_failures = Counter('automation_failures_total', 'Failed', ['error_type'])

# System metrics
active_browsers = Gauge('active_browsers', 'Active browser instances')
queue_size = Gauge('queue_size', 'Pending jobs')
model_inference_time = Histogram('model_inference_seconds', 'Inference time', ['model_version'])

# Security metrics
security_blocks = Counter('security_blocks_total', 'Blocked requests', ['attack_type'])
rate_limit_hits = Counter('rate_limit_hits_total', 'Rate limit hits', ['user_id'])

# Model metrics
model_confidence = Histogram('model_confidence', 'Detection confidence', ['model_version'])
model_accuracy = Gauge('model_accuracy', 'Current accuracy', ['model_version'])
```

**Priority 2: Distributed Tracing**

```python
from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Setup tracing
trace.set_tracer_provider(TracerProvider())
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

tracer = trace.get_tracer(__name__)

# Trace automation flow
@tracer.start_as_current_span("execute_automation")
def execute_task(url, task):
    with tracer.start_as_current_span("capture_screenshot"):
        screenshot = browser.capture_screenshot()
    
    with tracer.start_as_current_span("detect_elements"):
        elements = detector.detect_elements(screenshot)
    
    with tracer.start_as_current_span("llm_reasoning"):
        decision = reasoner.decide_action(task, elements)
    
    with tracer.start_as_current_span("execute_action"):
        result = browser.execute(decision)
    
    return result
```

**Priority 3: Logging Infrastructure**

```python
import structlog

# Structured logging
logger = structlog.get_logger()

logger.info(
    "automation_started",
    user_id=user_id,
    job_id=job_id,
    url=url,
    task=task
)

logger.error(
    "automation_failed",
    user_id=user_id,
    job_id=job_id,
    error=str(e),
    traceback=traceback.format_exc()
)

# ELK Stack integration
from elasticsearch import Elasticsearch

es = Elasticsearch(['localhost:9200'])

def log_to_elasticsearch(level, message, **kwargs):
    doc = {
        'timestamp': datetime.now(),
        'level': level,
        'message': message,
        **kwargs
    }
    es.index(index='automation-logs', document=doc)
```

Continue in PROJECT_REPORT_PART3.md...
