from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from typing import Dict, List, Optional
from pathlib import Path
from loguru import logger
from config import settings
import json
import hashlib
import random

class BrowserEngine:
    SUPPORTED_BROWSERS = ['chromium', 'firefox', 'webkit']
    
    def __init__(self, browser_type: str = 'chromium', headless: bool = False, 
                 proxy: Optional[Dict] = None, session_id: Optional[str] = None):
        if browser_type not in self.SUPPORTED_BROWSERS:
            raise ValueError(f"Unsupported browser: {browser_type}. Choose from {self.SUPPORTED_BROWSERS}")
        
        self.browser_type = browser_type
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.headless = headless
        self.proxy = proxy
        self.session_id = session_id
        self.session_dir = settings.data_dir / "sessions"
        
    def __enter__(self):
        self.playwright = sync_playwright().start()
        
        # Launch with proxy support
        launch_options = {'headless': self.headless}
        if self.proxy:
            launch_options['proxy'] = self.proxy
        
        # Launch selected browser
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(**launch_options)
        logger.info(f"Launched {self.browser_type} browser")
        
        # Create context with anti-fingerprinting
        context_options = self._get_stealth_context_options()
        self.context = self.browser.new_context(**context_options)
        
        # Restore session if exists
        if self.session_id:
            self._restore_session()
        
        self.page = self.context.new_page()
        self._apply_stealth_scripts()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Save session before closing
        if self.session_id:
            self._save_session()
        
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def navigate(self, url: str):
        logger.info(f"Navigating to {url}")
        self.page.goto(url, wait_until='networkidle')
    
    def capture_screenshot(self, filename: str = None) -> Path:
        if not filename:
            import re
            clean_url = re.sub(r'[^a-zA-Z0-9]', '_', self.page.url)
            filename = f"screenshot_{clean_url[:100]}.png"
        screenshot_path = settings.screenshots_dir / filename
        self.page.screenshot(path=str(screenshot_path), full_page=True)
        logger.info(f"Screenshot saved to {screenshot_path}")
        return screenshot_path
    
    def extract_dom_elements(self) -> List[Dict]:
        js_code = """
        () => {
            const elements = document.querySelectorAll('button, a, input, textarea, select, [role="button"]');
            return Array.from(elements).map(el => {
                const rect = el.getBoundingClientRect();
                return {
                    tag: el.tagName.toLowerCase(),
                    text: el.innerText?.substring(0, 100) || el.value || '',
                    type: el.type || '',
                    bbox: [rect.left, rect.top, rect.right, rect.bottom],
                    selector: el.id ? `#${el.id}` : el.className ? `.${el.className.split(' ')[0]}` : el.tagName.toLowerCase(),
                    visible: rect.width > 0 && rect.height > 0
                };
            }).filter(el => el.visible);
        }
        """
        elements = self.page.evaluate(js_code)
        logger.info(f"Extracted {len(elements)} DOM elements")
        return elements
    
    def click_at_coordinates(self, x: int, y: int):
        logger.info(f"Clicking at coordinates ({x}, {y})")
        self.page.mouse.click(x, y)
    
    def click_element(self, selector: str):
        logger.info(f"Clicking element: {selector}")
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str):
        logger.info(f"Filling input {selector} with text")
        self.page.fill(selector, text)
    
    def get_current_url(self) -> str:
        return self.page.url
    
    def wait_for_navigation(self, timeout: int = 5000):
        try:
            self.page.wait_for_load_state('networkidle', timeout=timeout)
            return True
        except:
            return False
    
    def _get_stealth_context_options(self) -> Dict:
        """Anti-fingerprinting browser context options"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        return {
            'user_agent': random.choice(user_agents),
            'viewport': {'width': 1920, 'height': 1080},
            'locale': 'en-US',
            'timezone_id': 'America/New_York',
            'permissions': ['geolocation'],
            'geolocation': {'latitude': 40.7128, 'longitude': -74.0060},
            'color_scheme': 'light',
            'accept_downloads': True
        }
    
    def _apply_stealth_scripts(self):
        """Remove webdriver detection"""
        stealth_js = """
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = {runtime: {}};
        """
        self.page.add_init_script(stealth_js)
    
    def _save_session(self):
        """Save cookies and storage"""
        if not self.session_id:
            return
        
        self.session_dir.mkdir(exist_ok=True)
        session_file = self.session_dir / f"{self.session_id}.json"
        
        session_data = {
            'cookies': self.context.cookies(),
            'storage': self.page.evaluate('() => JSON.stringify(localStorage)')
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f)
        
        logger.info(f"Session saved: {self.session_id}")
    
    def _restore_session(self):
        """Restore cookies and storage"""
        session_file = self.session_dir / f"{self.session_id}.json"
        
        if not session_file.exists():
            logger.warning(f"Session not found: {self.session_id}")
            return
        
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # Restore cookies
        if session_data.get('cookies'):
            self.context.add_cookies(session_data['cookies'])
        
        logger.info(f"Session restored: {self.session_id}")
    
    def set_cookies(self, cookies: List[Dict]):
        """Set cookies manually"""
        self.context.add_cookies(cookies)
    
    def get_cookies(self) -> List[Dict]:
        """Get current cookies"""
        return self.context.cookies()
    
    def clear_cookies(self):
        """Clear all cookies"""
        self.context.clear_cookies()
    
    def set_storage(self, key: str, value: str):
        """Set localStorage item"""
        self.page.evaluate(f'localStorage.setItem("{key}", "{value}")')
    
    def get_storage(self, key: str) -> str:
        """Get localStorage item"""
        return self.page.evaluate(f'localStorage.getItem("{key}")')

    # ---- v3 agent compatibility layer -------------------------------------
    def current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def click(self, selector: str):
        self.page.click(selector, timeout=8000)

    def type_text(self, selector: str, text: str):
        self.page.fill(selector, text, timeout=8000)

    def select_option(self, selector: str, value: str):
        self.page.select_option(selector, value, timeout=8000)

    def scroll(self, direction: str = "down"):
        delta = 600 if direction != "up" else -600
        self.page.mouse.wheel(0, delta)

    def press_key(self, key: str = "Enter"):
        self.page.keyboard.press(key)

    def wait_for_network_idle(self, timeout: float = 5):
        try:
            self.page.wait_for_load_state('networkidle', timeout=int(timeout * 1000))
        except Exception:
            pass

    def dom_fingerprint(self) -> str:
        return hashlib.sha256(self.page.content().encode()).hexdigest()[:16]

    def visible_text(self) -> str:
        try:
            return self.page.evaluate("() => document.body ? document.body.innerText : ''")
        except Exception:
            return ""
