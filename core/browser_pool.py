from typing import Optional, Dict
from queue import Queue, Empty
from threading import Lock
from loguru import logger
from core.browser_engine import BrowserEngine
import time

class BrowserPool:
    """Manages a pool of browser instances for concurrent automation"""
    
    def __init__(self, pool_size: int = 5, headless: bool = True):
        self.pool_size = pool_size
        self.headless = headless
        self.available = Queue(maxsize=pool_size)
        self.in_use = set()
        self.lock = Lock()
        self.total_created = 0
        
        # Pre-create browsers
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Create initial browser instances"""
        logger.info(f"Initializing browser pool with {self.pool_size} instances")
        for i in range(self.pool_size):
            browser = self._create_browser()
            self.available.put(browser)
            self.total_created += 1
        logger.info(f"Browser pool initialized: {self.pool_size} browsers ready")
    
    def _create_browser(self) -> BrowserEngine:
        """Create a new browser instance"""
        try:
            browser = BrowserEngine(headless=self.headless)
            browser.__enter__()
            return browser
        except Exception as e:
            logger.error(f"Failed to create browser: {e}")
            raise
    
    def acquire(self, timeout: int = 30) -> Optional[BrowserEngine]:
        """Get a browser from the pool"""
        try:
            browser = self.available.get(timeout=timeout)
            with self.lock:
                self.in_use.add(id(browser))
            logger.debug(f"Browser acquired. Available: {self.available.qsize()}, In use: {len(self.in_use)}")
            return browser
        except Empty:
            logger.error("No browser available in pool (timeout)")
            return None
    
    def release(self, browser: BrowserEngine):
        """Return a browser to the pool"""
        if not browser:
            return
        
        with self.lock:
            browser_id = id(browser)
            if browser_id in self.in_use:
                self.in_use.remove(browser_id)
        
        # Check if browser is still healthy
        if self._is_browser_healthy(browser):
            self.available.put(browser)
            logger.debug(f"Browser released. Available: {self.available.qsize()}, In use: {len(self.in_use)}")
        else:
            # Replace unhealthy browser
            logger.warning("Browser unhealthy, creating replacement")
            browser.__exit__(None, None, None)
            new_browser = self._create_browser()
            self.available.put(new_browser)
    
    def _is_browser_healthy(self, browser: BrowserEngine) -> bool:
        """Check if browser is still functional"""
        try:
            if not browser.page or not browser.browser:
                return False
            # Simple health check
            browser.page.evaluate('1 + 1')
            return True
        except:
            return False
    
    def get_stats(self) -> Dict:
        """Get pool statistics"""
        return {
            'pool_size': self.pool_size,
            'available': self.available.qsize(),
            'in_use': len(self.in_use),
            'total_created': self.total_created,
            'utilization': len(self.in_use) / self.pool_size * 100
        }
    
    def scale_up(self, additional: int = 2):
        """Add more browsers to the pool"""
        logger.info(f"Scaling up browser pool by {additional}")
        for _ in range(additional):
            browser = self._create_browser()
            self.available.put(browser)
            self.pool_size += 1
            self.total_created += 1
        logger.info(f"Pool scaled to {self.pool_size} browsers")
    
    def scale_down(self, remove: int = 1):
        """Remove browsers from the pool"""
        if self.pool_size <= 1:
            logger.warning("Cannot scale down below 1 browser")
            return
        
        logger.info(f"Scaling down browser pool by {remove}")
        for _ in range(min(remove, self.pool_size - 1)):
            try:
                browser = self.available.get_nowait()
                browser.__exit__(None, None, None)
                self.pool_size -= 1
            except Empty:
                break
        logger.info(f"Pool scaled to {self.pool_size} browsers")
    
    def shutdown(self):
        """Close all browsers and shutdown pool"""
        logger.info("Shutting down browser pool")
        
        # Close all available browsers
        while not self.available.empty():
            try:
                browser = self.available.get_nowait()
                browser.__exit__(None, None, None)
            except Empty:
                break
        
        logger.info("Browser pool shutdown complete")


class AutoScalingBrowserPool(BrowserPool):
    """Browser pool with automatic scaling based on utilization"""
    
    def __init__(self, min_size: int = 3, max_size: int = 20, headless: bool = True):
        self.min_size = min_size
        self.max_size = max_size
        self.scale_up_threshold = 0.8  # 80% utilization
        self.scale_down_threshold = 0.3  # 30% utilization
        super().__init__(pool_size=min_size, headless=headless)
    
    def acquire(self, timeout: int = 30) -> Optional[BrowserEngine]:
        """Acquire with auto-scaling"""
        browser = super().acquire(timeout)
        
        # Check if we need to scale up
        stats = self.get_stats()
        if stats['utilization'] > self.scale_up_threshold * 100:
            if self.pool_size < self.max_size:
                self.scale_up(2)
        
        return browser
    
    def release(self, browser: BrowserEngine):
        """Release with auto-scaling"""
        super().release(browser)
        
        # Check if we need to scale down
        stats = self.get_stats()
        if stats['utilization'] < self.scale_down_threshold * 100:
            if self.pool_size > self.min_size:
                self.scale_down(1)
