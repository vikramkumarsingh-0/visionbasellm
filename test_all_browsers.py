"""
Test script to verify all browser support (Chromium, Firefox, WebKit)
"""
from automation_agent import AutomationAgent
from loguru import logger

def test_browser(browser_type: str):
    """Test automation with specific browser"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Testing {browser_type.upper()} browser")
    logger.info(f"{'='*60}")
    
    try:
        agent = AutomationAgent(
            browser_type=browser_type,
            use_groq=False,
            headless=True
        )
        
        result = agent.execute_task(
            url="https://example.com",
            task="Find the 'More information' link"
        )
        
        logger.success(f"✓ {browser_type} test completed: {result['success']}")
        return True
        
    except Exception as e:
        logger.error(f"✗ {browser_type} test failed: {e}")
        return False

def main():
    """Test all supported browsers"""
    browsers = ['chromium', 'firefox', 'webkit']
    results = {}
    
    logger.info("Starting multi-browser test suite...")
    
    for browser in browsers:
        results[browser] = test_browser(browser)
    
    # Summary
    logger.info(f"\n{'='*60}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*60}")
    
    for browser, success in results.items():
        status = "✓ PASSED" if success else "✗ FAILED"
        logger.info(f"{browser.upper()}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    logger.info(f"\nTotal: {passed}/{total} browsers working")

if __name__ == "__main__":
    main()
