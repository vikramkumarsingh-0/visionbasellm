"""
Advanced usage examples for Vision-Based Web Automation
Demonstrates: proxy, sessions, cookies, browser pool
"""

from automation_agent import AutomationAgent
from core.browser_pool import BrowserPool, AutoScalingBrowserPool
from loguru import logger

# Example 1: Using Proxy
def example_with_proxy():
    """Use automation with proxy server"""
    proxy_config = {
        'server': 'http://proxy.example.com:8080',
        'username': 'user',
        'password': 'pass'
    }
    
    agent = AutomationAgent(
        use_groq=False,
        headless=True,
        proxy=proxy_config
    )
    
    result = agent.execute_task(
        url="https://example.com",
        task="Click the login button"
    )
    print(f"Result: {result}")


# Example 2: Session Management
def example_with_session():
    """Maintain session across multiple tasks"""
    session_id = "user_123_session"
    
    # First task - login
    agent1 = AutomationAgent(
        headless=True,
        session_id=session_id
    )
    
    result1 = agent1.execute_task(
        url="https://example.com/login",
        task="Fill username with 'testuser' and password with 'testpass', then click login"
    )
    print(f"Login result: {result1}")
    
    # Second task - use same session (cookies preserved)
    agent2 = AutomationAgent(
        headless=True,
        session_id=session_id  # Same session ID
    )
    
    result2 = agent2.execute_task(
        url="https://example.com/dashboard",
        task="Click on profile settings"
    )
    print(f"Dashboard result: {result2}")


# Example 3: Manual Cookie Management
def example_manual_cookies():
    """Set cookies manually before automation"""
    from core.browser_engine import BrowserEngine
    
    with BrowserEngine(headless=True) as browser:
        # Set cookies
        cookies = [
            {
                'name': 'session_token',
                'value': 'abc123xyz',
                'domain': 'example.com',
                'path': '/'
            }
        ]
        browser.set_cookies(cookies)
        
        # Navigate with cookies
        browser.navigate("https://example.com/dashboard")
        
        # Get current cookies
        current_cookies = browser.get_cookies()
        print(f"Current cookies: {len(current_cookies)}")


# Example 4: Browser Pool for Concurrent Tasks
def example_browser_pool():
    """Use browser pool for multiple concurrent automations"""
    pool = BrowserPool(pool_size=5, headless=True)
    
    tasks = [
        ("https://example.com", "Click login"),
        ("https://example.org", "Fill search box"),
        ("https://example.net", "Click menu"),
    ]
    
    results = []
    for url, task in tasks:
        # Acquire browser from pool
        browser = pool.acquire(timeout=30)
        
        if browser:
            try:
                browser.navigate(url)
                screenshot = browser.capture_screenshot()
                results.append({'url': url, 'success': True})
            finally:
                # Always release back to pool
                pool.release(browser)
    
    # Get pool statistics
    stats = pool.get_stats()
    print(f"Pool stats: {stats}")
    
    # Shutdown pool
    pool.shutdown()


# Example 5: Auto-Scaling Browser Pool
def example_auto_scaling_pool():
    """Browser pool that scales automatically based on load"""
    pool = AutoScalingBrowserPool(
        min_size=3,
        max_size=20,
        headless=True
    )
    
    # Simulate high load
    browsers = []
    for i in range(15):
        browser = pool.acquire()
        if browser:
            browsers.append(browser)
            print(f"Acquired {i+1} browsers. Stats: {pool.get_stats()}")
    
    # Release all
    for browser in browsers:
        pool.release(browser)
    
    print(f"Final stats: {pool.get_stats()}")
    pool.shutdown()


# Example 6: Anti-Fingerprinting
def example_stealth_mode():
    """Browser with anti-fingerprinting enabled (automatic)"""
    from core.browser_engine import BrowserEngine
    
    with BrowserEngine(headless=False) as browser:
        browser.navigate("https://bot.sannysoft.com/")
        
        # Check if webdriver is detected
        is_detected = browser.page.evaluate("navigator.webdriver")
        print(f"Webdriver detected: {is_detected}")  # Should be False
        
        # Take screenshot to verify
        browser.capture_screenshot("stealth_test.png")


# Example 7: Storage Management
def example_storage():
    """Manage localStorage and sessionStorage"""
    from core.browser_engine import BrowserEngine
    
    with BrowserEngine(headless=True) as browser:
        browser.navigate("https://example.com")
        
        # Set localStorage
        browser.set_storage("user_preference", "dark_mode")
        browser.set_storage("language", "en")
        
        # Get localStorage
        preference = browser.get_storage("user_preference")
        print(f"User preference: {preference}")
        
        # Navigate to another page (storage persists)
        browser.navigate("https://example.com/settings")
        preference = browser.get_storage("user_preference")
        print(f"Preference still available: {preference}")


if __name__ == "__main__":
    print("=== Example 1: Proxy ===")
    # example_with_proxy()  # Uncomment if you have a proxy
    
    print("\n=== Example 2: Session Management ===")
    example_with_session()
    
    print("\n=== Example 3: Manual Cookies ===")
    example_manual_cookies()
    
    print("\n=== Example 4: Browser Pool ===")
    print("Note: Browser pool requires separate process. See browser_pool.py for usage.")
    # example_browser_pool()  # Skip - requires separate process
    
    print("\n=== Example 5: Auto-Scaling Pool ===")
    print("Note: Auto-scaling pool requires separate process.")
    # example_auto_scaling_pool()  # Skip - requires separate process
    
    print("\n=== Example 6: Stealth Mode ===")
    example_stealth_mode()
    
    print("\n=== Example 7: Storage Management ===")
    example_storage()
