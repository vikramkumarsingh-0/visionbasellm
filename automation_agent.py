from core.browser_engine import BrowserEngine
from core.vision_detector import VisionDetector
from core.ai_reasoner import AIReasoner
from core.matcher import ElementMatcher
from core.evaluator import ActionEvaluator
from core.training_pipeline import TrainingPipeline
from typing import Dict, Optional
from loguru import logger
from config import settings
import hashlib

class AutomationAgent:
    def __init__(self, browser_type: str = 'chromium', use_groq: bool = False, 
                 headless: bool = False, proxy: Optional[Dict] = None, 
                 session_id: Optional[str] = None):
        self.browser_type = browser_type
        self.detector = VisionDetector()
        self.reasoner = AIReasoner(use_groq=use_groq)
        self.matcher = ElementMatcher()
        self.evaluator = ActionEvaluator()
        self.training_pipeline = TrainingPipeline()
        self.headless = headless
        self.proxy = proxy
        self.session_id = session_id
        self.failed_actions = []
    
    def execute_task(self, url: str, task: str) -> Dict:
        # Validate inputs at agent level
        from core.security import SecurityValidator
        url = SecurityValidator.validate_url(url)
        task = SecurityValidator.validate_task(task)
        
        logger.info(f"Starting task: {task} on {url} using {self.browser_type}")
        
        with BrowserEngine(browser_type=self.browser_type, headless=self.headless, 
                          proxy=self.proxy, session_id=self.session_id) as browser:
            browser.navigate(url)
            
            initial_state = self._capture_state(browser)
            screenshot_path = browser.capture_screenshot()
            
            visual_elements = self.detector.detect_elements(str(screenshot_path))
            dom_elements = browser.extract_dom_elements()
            
            matched_elements = self.matcher.match_vision_to_dom(visual_elements, dom_elements)
            logger.info(f"Matched {len(matched_elements)} elements")
            
            decision = self.reasoner.decide_action(task, visual_elements, dom_elements)
            logger.info(f"Decision: {decision['action']} - {decision['reasoning']}")
            
            self._execute_action(browser, decision)
            
            final_state = self._capture_state(browser)
            
            evaluation = self.evaluator.evaluate(decision, initial_state, final_state)
            
            if not evaluation['success']:
                self.failed_actions.append({
                    'task': task,
                    'screenshot': str(screenshot_path),
                    'visual_elements': visual_elements,
                    'dom_elements': dom_elements,
                    'decision': decision,
                    'evaluation': evaluation
                })
                
                if self.evaluator.should_retrain(settings.retrain_threshold):
                    logger.warning("Retraining threshold reached, triggering retraining")
                    self._trigger_retraining()
            
            return {
                'success': evaluation['success'],
                'decision': decision,
                'metrics': self.evaluator.get_metrics()
            }
    
    def _capture_state(self, browser: BrowserEngine) -> Dict:
        url = browser.get_current_url()
        dom_elements = browser.extract_dom_elements()
        dom_hash = hashlib.md5(str(dom_elements).encode()).hexdigest()
        
        return {
            'url': url,
            'dom_hash': dom_hash,
            'dom_elements': dom_elements
        }
    
    def _execute_action(self, browser: BrowserEngine, decision: Dict):
        from core.security import SecurityValidator
        
        # Re-validate decision before execution
        decision = SecurityValidator.validate_llm_response(decision)
        
        action = decision['action']
        target = decision.get('target', {})
        
        if action == 'click':
            if 'x' in target and 'y' in target:
                browser.click_at_coordinates(target['x'], target['y'])
            elif 'selector' in target:
                browser.click_element(target['selector'])
        
        elif action == 'fill':
            if 'selector' in target:
                value = decision.get('value', '')[:1000]  # Limit value length
                browser.fill_input(target['selector'], value)
        
        elif action == 'wait':
            browser.wait_for_navigation()
    
    def _trigger_retraining(self):
        logger.info("Starting retraining process")
        self.training_pipeline.retrain_model(self.failed_actions)
        
        self.detector = VisionDetector()
        self.failed_actions = []
        self.evaluator.failure_count = 0
        
        logger.info("Model reloaded after retraining")
