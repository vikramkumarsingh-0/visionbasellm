# Multi-Browser Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Automation Agent                          │
│                  (automation_agent.py)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ browser_type parameter
                     │
┌────────────────────▼────────────────────────────────────────┐
│                  Browser Engine                              │
│               (browser_engine.py)                            │
│                                                              │
│  SUPPORTED_BROWSERS = ['chromium', 'firefox', 'webkit']     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     │ Dynamic browser selection
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼──────┐
│   Chromium   │ │ Firefox │ │ WebKit  │
│   (Blink)    │ │ (Gecko) │ │(WebKit) │
└──────────────┘ └─────────┘ └─────────┘
```

## Request Flow

```
User Request
    │
    ├─ Python API
    │   └─> AutomationAgent(browser_type='firefox')
    │
    └─ REST API
        └─> POST /automate {"browser_type": "webkit"}
            │
            ▼
    ┌───────────────────┐
    │  API Validation   │
    │   (api.py)        │
    │                   │
    │  - Validate URL   │
    │  - Validate task  │
    │  - Validate       │
    │    browser_type   │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │ Automation Agent  │
    │                   │
    │  - Initialize     │
    │    with browser   │
    │  - Execute task   │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │  Browser Engine   │
    │                   │
    │  - Launch browser │
    │  - Navigate       │
    │  - Screenshot     │
    │  - Extract DOM    │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │  Vision Detector  │
    │  (YOLOv8)         │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │   AI Reasoner     │
    │  (LLM)            │
    └─────────┬─────────┘
              │
              ▼
    ┌───────────────────┐
    │  Action Executor  │
    └─────────┬─────────┘
              │
              ▼
         Result
```

## Browser Selection Logic

```python
# In browser_engine.py

class BrowserEngine:
    SUPPORTED_BROWSERS = ['chromium', 'firefox', 'webkit']
    
    def __init__(self, browser_type='chromium', ...):
        # Validate browser type
        if browser_type not in self.SUPPORTED_BROWSERS:
            raise ValueError(f"Unsupported browser: {browser_type}")
        
        self.browser_type = browser_type
    
    def __enter__(self):
        # Dynamic browser launcher
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(**launch_options)
        
        # chromium -> self.playwright.chromium.launch()
        # firefox  -> self.playwright.firefox.launch()
        # webkit   -> self.playwright.webkit.launch()
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│                      User Interface                          │
├──────────────────────────────────────────────────────────────┤
│  Python API          │  REST API          │  CLI             │
│  agent.execute()     │  POST /automate    │  python script   │
└──────────┬───────────┴──────────┬─────────┴──────────────────┘
           │                      │
           └──────────┬───────────┘
                      │
           ┌──────────▼──────────┐
           │  Automation Agent   │
           │  - browser_type     │
           │  - use_groq         │
           │  - headless         │
           │  - proxy            │
           │  - session_id       │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │   Browser Engine    │
           │  - Validate browser │
           │  - Launch browser   │
           │  - Manage context   │
           └──────────┬──────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼──────┐ ┌───▼──────┐ ┌───▼──────┐
│  Chromium    │ │ Firefox  │ │ WebKit   │
│              │ │          │ │          │
│ - Navigate   │ │- Navigate│ │- Navigate│
│ - Screenshot │ │- Screenshot│- Screenshot│
│ - Extract    │ │- Extract │ │- Extract │
│ - Execute    │ │- Execute │ │- Execute │
└──────────────┘ └──────────┘ └──────────┘
```

## Data Flow

```
Input
  │
  ├─ url: "https://example.com"
  ├─ task: "Click login button"
  └─ browser_type: "firefox"
      │
      ▼
┌─────────────────┐
│ Browser Launch  │
│  Firefox        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Navigation    │
│  Load page      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Screenshot     │
│  Capture UI     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vision Detection│
│  YOLOv8         │
│  Find elements  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DOM Extraction │
│  Get selectors  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Reasoning   │
│  Decide action  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Action Execute  │
│  Click/Fill     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Evaluation    │
│  Success check  │
└────────┬────────┘
         │
         ▼
      Result
```

## Browser Comparison Matrix

```
┌──────────────┬───────────┬──────────┬─────────┐
│   Feature    │ Chromium  │ Firefox  │ WebKit  │
├──────────────┼───────────┼──────────┼─────────┤
│ Engine       │ Blink     │ Gecko    │ WebKit  │
│ Speed        │ Fast      │ Medium   │ Fast    │
│ Memory       │ High      │ Low      │ Low     │
│ Compatibility│ Excellent │ Good     │ Good    │
│ Privacy      │ Medium    │ High     │ Medium  │
│ Extensions   │ Yes       │ Yes      │ Limited │
│ Mobile       │ Android   │ Android  │ iOS     │
│ Best For     │ General   │ Privacy  │ Safari  │
└──────────────┴───────────┴──────────┴─────────┘
```

## Configuration Hierarchy

```
Default Values
    │
    ├─ browser_type: 'chromium'
    ├─ headless: False
    ├─ use_groq: False
    ├─ proxy: None
    └─ session_id: None
        │
        ▼
Environment Variables (.env)
    │
    ├─ GROQ_API_KEY
    ├─ OLLAMA_BASE_URL
    └─ RETRAIN_THRESHOLD
        │
        ▼
Runtime Parameters
    │
    ├─ AutomationAgent(browser_type='firefox')
    ├─ AutomationAgent(headless=True)
    └─ AutomationAgent(proxy={...})
        │
        ▼
API Request
    │
    └─ POST /automate
        {
          "browser_type": "webkit",
          "headless": true,
          ...
        }
```

## Error Handling Flow

```
User Input
    │
    ▼
┌─────────────────┐
│  Validation     │
│  - URL valid?   │
│  - Task valid?  │
│  - Browser OK?  │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
         │
    ┌────▼────┐
    │   No    │───> ValueError: "Unsupported browser"
    └─────────┘
         │
    ┌────▼────┐
    │   Yes   │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│ Browser Launch  │
└────────┬────────┘
         │
    ┌────┴────┐
    │Success? │
    └────┬────┘
         │
    ┌────▼────┐
    │   No    │───> Exception: "Browser not installed"
    └─────────┘
         │
    ┌────▼────┐
    │   Yes   │
    └────┬────┘
         │
         ▼
    Continue...
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Production Stack                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   FastAPI    │  │    Celery    │  │    Redis     │ │
│  │   (API)      │  │   (Tasks)    │  │   (Queue)    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────────────┘ │
│         │                 │                             │
│         └────────┬────────┘                             │
│                  │                                      │
│         ┌────────▼────────┐                            │
│         │ Automation Agent│                            │
│         │  Multi-Browser  │                            │
│         └────────┬────────┘                            │
│                  │                                      │
│         ┌────────┼────────┐                            │
│         │        │        │                             │
│  ┌──────▼──┐ ┌──▼───┐ ┌──▼────┐                       │
│  │Chromium │ │Firefox│ │WebKit │                       │
│  └─────────┘ └──────┘ └───────┘                        │
│                                                          │
├─────────────────────────────────────────────────────────┤
│                    Monitoring                            │
├─────────────────────────────────────────────────────────┤
│  Prometheus (Metrics) │ Grafana (Dashboard)            │
└─────────────────────────────────────────────────────────┘
```

## Summary

- ✅ **3 browsers supported**: Chromium, Firefox, WebKit
- ✅ **Dynamic selection**: Runtime browser choice
- ✅ **Validated input**: API validates browser type
- ✅ **Backward compatible**: Defaults to Chromium
- ✅ **Flexible**: Works with all existing features
- ✅ **Production ready**: Full error handling
