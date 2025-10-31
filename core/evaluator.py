from typing import Dict
from loguru import logger
import time

class ActionEvaluator:
    def __init__(self):
        self.success_count = 0
        self.failure_count = 0
        self.action_history = []
    
    def evaluate(self, action: Dict, initial_state: Dict, final_state: Dict) -> Dict:
        result = {
            'action': action,
            'success': False,
            'timestamp': time.time(),
            'metrics': {}
        }
        
        if action['action'] == 'click':
            result['success'] = self._evaluate_click(initial_state, final_state)
        elif action['action'] == 'fill':
            result['success'] = self._evaluate_fill(initial_state, final_state)
        else:
            result['success'] = True
        
        if result['success']:
            self.success_count += 1
        else:
            self.failure_count += 1
        
        self.action_history.append(result)
        logger.info(f"Action evaluated: {result['success']}")
        
        return result
    
    def _evaluate_click(self, initial_state: Dict, final_state: Dict) -> bool:
        url_changed = initial_state.get('url') != final_state.get('url')
        dom_changed = initial_state.get('dom_hash') != final_state.get('dom_hash')
        return url_changed or dom_changed
    
    def _evaluate_fill(self, initial_state: Dict, final_state: Dict) -> bool:
        return True
    
    def get_metrics(self) -> Dict:
        total = self.success_count + self.failure_count
        return {
            'success_count': self.success_count,
            'failure_count': self.failure_count,
            'success_rate': self.success_count / total if total > 0 else 0,
            'total_actions': total
        }
    
    def should_retrain(self, threshold: int = None) -> bool:
        threshold = threshold or 3
        recent_failures = sum(
            1 for action in self.action_history[-10:]
            if not action['success']
        )
        return recent_failures >= threshold
