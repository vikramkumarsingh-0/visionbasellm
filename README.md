# 🤖 Vision-Based Web Automation System

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/yourusername/vision-based-web-automation)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-enterprise--grade-red.svg)](SECURITY.md)
[![Browsers](https://img.shields.io/badge/browsers-chromium%20%7C%20firefox%20%7C%20webkit-purple.svg)](MULTI_BROWSER_GUIDE.md)

Self-learning AI agent for autonomous web automation using computer vision and LLM reasoning.

> 🌟 **New in v2.0**: Multi-browser support, intelligent planning, enterprise security, and self-learning capabilities!

## ✨ Features

### Core Capabilities
- 👁️ **Vision Detection**: YOLOv8 for UI element recognition - no brittle CSS selectors
- 🌐 **Multi-Browser Support**: Chromium, Firefox, WebKit via Playwright with intelligent pooling
- 🧠 **AI Reasoning**: Ollama (LLaMA3) + Groq for intelligent decision-making
- 📚 **Self-Learning**: Auto-retraining on failures with DVC versioning
- 🎯 **Intelligent Planning**: Multi-step task decomposition with context awareness
- 💾 **Session Management**: Persistent sessions with state recovery
- ⚡ **Distributed**: Celery for async task processing
- 📊 **Monitoring**: Prometheus + Grafana dashboards
- 🔒 **Security**: Enterprise-grade ML injection protection (94+ patterns, 5 layers)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
# Install all browsers (chromium, firefox, webkit)
playwright install
# Or install specific browsers
playwright install chromium firefox webkit
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start Ollama (Local LLM)

```bash
ollama pull llama3
ollama serve
```

### 4. Run with Docker

```bash
docker-compose up -d
```

### 5. Run Locally

```bash
# Start API
uvicorn api:app --reload

# Start Celery Worker
celery -A tasks worker --loglevel=info
```

## 💻 Usage

### Python API

```python
from automation_agent import AutomationAgent

# Use Chromium (default)
agent = AutomationAgent(browser_type='chromium', use_groq=False, headless=True)

# Or use Firefox
agent = AutomationAgent(browser_type='firefox', use_groq=False, headless=True)

# Or use WebKit (Safari engine)
agent = AutomationAgent(browser_type='webkit', use_groq=False, headless=True)

result = agent.execute_task(
    url="https://example.com",
    task="Click the login button"
)
print(result)
```

### REST API

```bash
# Chromium (default)
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "task": "Click the login button",
    "browser_type": "chromium",
    "use_groq": false,
    "headless": true
  }'

# Firefox
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "task": "Click login", "browser_type": "firefox"}'

# WebKit
curl -X POST http://localhost:8000/automate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "task": "Click login", "browser_type": "webkit"}'
```

### Test All Browsers

```bash
python test_all_browsers.py
```

## 🏗️ Architecture

```
┌─────────────────┐
│  Browser Engine │ → Playwright
└────────┬────────┘
         │
┌────────▼────────┐
│ Vision Detector │ → YOLOv8
└────────┬────────┘
         │
┌────────▼────────┐
│  Element Matcher│ → IoU Matching
└────────┬────────┘
         │
┌────────▼────────┐
│   AI Reasoner   │ → Ollama/Groq
└────────┬────────┘
         │
┌────────▼────────┐
│ Action Executor │
└────────┬────────┘
         │
┌────────▼────────┐
│    Evaluator    │ → Success/Failure
└────────┬────────┘
         │
    ┌────▼────┐
    │ Retrain?│ → Training Pipeline
    └─────────┘
```

## 🧪 Self-Learning Process

1. **Execute Task**: Agent performs automation
2. **Evaluate**: Check if action succeeded
3. **Log Failures**: Store failed actions with context
4. **Trigger Retraining**: After N failures (default: 3)
5. **Fine-tune Model**: YOLOv8 retraining on failed samples
6. **Deploy Updated Model**: Auto-reload new weights

## Security 🔒

**Enterprise-grade protection against ML injection attacks:**

- ✅ **94+ attack patterns blocked** across 17 categories
- ✅ Prompt injection prevention (7 patterns)
- ✅ SQL injection blocking (10 patterns)
- ✅ XSS/HTML protection (12 patterns)
- ✅ Code injection prevention (6 patterns)
- ✅ Command injection blocking (6 patterns)
- ✅ Data poisoning protection
- ✅ Model integrity verification
- ✅ SSRF protection (5 patterns)
- ✅ Jailbreak prevention (6 patterns)
- ✅ And 30+ more attack vectors

**Quick Start**: See [SECURITY_QUICKSTART.md](SECURITY_QUICKSTART.md)

**Full Documentation**: See [SECURITY.md](SECURITY.md)

**Test Security**:
```bash
pytest test_security.py -v
```

## 📊 Monitoring

- **Metrics**: http://localhost:9090 (Prometheus)
- **Dashboard**: http://localhost:3000 (Grafana, admin/admin)
- **API Health**: http://localhost:8000/health
- **Security Metrics**: http://localhost:8000/metrics (includes `security_blocks_total`)

### Key Metrics
- `automation_tasks_total` - Total tasks executed
- `automation_task_duration_seconds` - Task execution time
- `security_blocks_total{category}` - Blocked attacks by type
- `browser_pool_size` - Active browser instances
- `model_inference_time_seconds` - Vision model latency

## ⚙️ Configuration

Edit `config.py` or `.env`:

- `GROQ_API_KEY`: For Groq LLM (optional)
- `OLLAMA_BASE_URL`: Local Ollama endpoint
- `RETRAIN_THRESHOLD`: Failures before retraining
- `MODEL_VERSION`: Current model version tag

## 📦 Project Structure

```
├── core/
│   ├── browser_engine.py    # Playwright wrapper
│   ├── vision_detector.py   # YOLOv8 detection
│   ├── ai_reasoner.py       # LLM decision engine
│   ├── matcher.py           # Vision-DOM sync
│   ├── evaluator.py         # Success evaluation
│   ├── training_pipeline.py # Auto-retraining
│   └── security.py          # 🔒 ML injection protection
├── automation_agent.py      # Main orchestrator
├── api.py                   # FastAPI service
├── tasks.py                 # Celery tasks
├── config.py                # Settings
├── test_security.py         # Security test suite
├── SECURITY.md              # Security documentation
└── docker-compose.yml       # Full stack
```

## 📚 Documentation

> 🌟 **Featured**: [GITHUB_SHOWCASE.md](GITHUB_SHOWCASE.md) - Complete showcase for GitHub!
> 📚 **Index**: [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Navigate all 40+ documents
> 📊 **Summary**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Quick project overview

### Core Documentation
- 📖 [README.md](README.md) - Main documentation (this file)
- 🎯 [GITHUB_SHOWCASE.md](GITHUB_SHOWCASE.md) - **Complete GitHub showcase** ⭐
- 🏢 [ENTERPRISE_ARCHITECTURE.md](ENTERPRISE_ARCHITECTURE.md) - **Enterprise-grade architecture** 🆕
- 📊 [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Project overview
- 📚 [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - All documentation index
- 🚀 [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) - Development roadmap
- 📈 [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) - High-level overview

### Browser Documentation
- 🌐 [MULTI_BROWSER_GUIDE.md](MULTI_BROWSER_GUIDE.md) - Browser usage guide
- 🏗️ [MULTI_BROWSER_ARCHITECTURE.md](MULTI_BROWSER_ARCHITECTURE.md) - Technical architecture
- 📝 [MULTI_BROWSER_SUMMARY.md](MULTI_BROWSER_SUMMARY.md) - Feature summary

### Security Documentation
- 🔒 [SECURITY.md](SECURITY.md) - Complete security guide
- ⚡ [SECURITY_QUICKSTART.md](SECURITY_QUICKSTART.md) - Quick start
- ✅ [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) - Deployment checklist
- 🎯 [ATTACK_PATTERNS.md](ATTACK_PATTERNS.md) - Attack pattern reference

### Advanced Features
- 🧠 [INTELLIGENT_PLANNER_README.md](INTELLIGENT_PLANNER_README.md) - Multi-step planning
- 📊 [REPORTS_INDEX.md](REPORTS_INDEX.md) - Project reports index

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Quick Start**:
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

**Resources**:
- 📖 [Contributing Guide](CONTRIBUTING.md) - Complete guidelines
- 📝 [Changelog](CHANGELOG.md) - Version history
- 🐛 [Issues](https://github.com/yourusername/vision-based-web-automation/issues) - Report bugs

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ultralytics** - YOLOv8 framework
- **Playwright** - Cross-browser automation
- **Ollama** - Local LLM inference
- **FastAPI** - Modern web framework
- **Community** - All our amazing contributors

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discord: [Join our community](https://discord.gg/example)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/vision-based-web-automation/issues)
- 📖 Docs: [Documentation Index](DOCUMENTATION_INDEX.md)

## 📊 Project Stats

- **Version**: 2.0.0
- **Status**: Production Ready
- **Security Patterns**: 94+
- **Browsers Supported**: 3
- **Documentation Files**: 40+
- **Test Coverage**: 100% (security)

---

<div align="center">

**⭐ Star this repository if you find it useful! ⭐**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Security](#-security) • [Showcase](GITHUB_SHOWCASE.md)

**Made with ❤️ by the Vision Automation Team**

</div>
