"""
Multi-Browser Example - Vision-Based Web Automation
Demonstrates using Chromium, Firefox, and WebKit
"""
from automation_agent import AutomationAgent

def example_chromium():
    """Example using Chromium browser"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Chromium Browser")
    print("="*60)
    
    agent = AutomationAgent(
        browser_type='chromium',
        use_groq=False,
        headless=True
    )
    
    result = agent.execute_task(
        url="https://example.com",
        task="Find the 'More information' link"
    )
    
    print(f"Success: {result['success']}")
    print(f"Action: {result['decision']['action']}")
    print(f"Reasoning: {result['decision']['reasoning']}")

def example_firefox():
    """Example using Firefox browser"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Firefox Browser")
    print("="*60)
    
    agent = AutomationAgent(
        browser_type='firefox',
        use_groq=False,
        headless=True
    )
    
    result = agent.execute_task(
        url="https://example.com",
        task="Find the 'More information' link"
    )
    
    print(f"Success: {result['success']}")
    print(f"Action: {result['decision']['action']}")

def example_webkit():
    """Example using WebKit browser"""
    print("\n" + "="*60)
    print("EXAMPLE 3: WebKit Browser (Safari Engine)")
    print("="*60)
    
    agent = AutomationAgent(
        browser_type='webkit',
        use_groq=False,
        headless=True
    )
    
    result = agent.execute_task(
        url="https://example.com",
        task="Find the 'More information' link"
    )
    
    print(f"Success: {result['success']}")
    print(f"Action: {result['decision']['action']}")

def example_with_options():
    """Example with advanced options"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Advanced Options")
    print("="*60)
    
    # With proxy
    agent = AutomationAgent(
        browser_type='firefox',
        use_groq=False,
        headless=True,
        proxy={'server': 'http://proxy.example.com:8080'},  # Optional
        session_id='my_session_123'  # Optional: Save/restore session
    )
    
    print("Agent configured with:")
    print(f"  - Browser: firefox")
    print(f"  - Headless: True")
    print(f"  - Proxy: Configured")
    print(f"  - Session: my_session_123")

def example_comparison():
    """Compare same task across all browsers"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Cross-Browser Comparison")
    print("="*60)
    
    url = "https://example.com"
    task = "Find the 'More information' link"
    
    browsers = ['chromium', 'firefox', 'webkit']
    results = {}
    
    for browser in browsers:
        print(f"\nTesting {browser}...")
        agent = AutomationAgent(browser_type=browser, headless=True)
        result = agent.execute_task(url, task)
        results[browser] = result['success']
    
    print("\n" + "-"*60)
    print("Results:")
    for browser, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"  {browser.upper()}: {status}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Multi-Browser Automation Examples")
    print("="*60)
    
    # Run examples
    try:
        example_chromium()
    except Exception as e:
        print(f"Chromium example failed: {e}")
    
    try:
        example_firefox()
    except Exception as e:
        print(f"Firefox example failed: {e}")
    
    try:
        example_webkit()
    except Exception as e:
        print(f"WebKit example failed: {e}")
    
    try:
        example_with_options()
    except Exception as e:
        print(f"Advanced options example failed: {e}")
    
    try:
        example_comparison()
    except Exception as e:
        print(f"Comparison example failed: {e}")
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")
