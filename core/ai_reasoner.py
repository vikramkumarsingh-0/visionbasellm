from typing import Dict, List
# import ollama  # Commented out - using HuggingFace + LangChain instead
from groq import Groq
from loguru import logger
from config import settings
from core.security import SecurityValidator
import json

class AIReasoner:
    def __init__(self, use_groq: bool = True):  # Default to Groq
        self.use_groq = use_groq
        if use_groq and settings.groq_api_key:
            self.groq_client = Groq(api_key=settings.groq_api_key)
        else:
            self.groq_client = None
            logger.warning("Groq API key not found, using fallback")
    
    def decide_action(self, task: str, visual_elements: List[Dict], dom_elements: List[Dict]) -> Dict:
        # Sanitize task input
        safe_task = SecurityValidator.validate_task(task)
        prompt = self._build_prompt(safe_task, visual_elements, dom_elements)
        
        if self.use_groq and self.groq_client:
            response = self._query_groq(prompt)
        else:
            # Fallback to simple rule-based system
            response = self._fallback_response()
        
        parsed = self._parse_response(response)
        # Validate LLM output
        return SecurityValidator.validate_llm_response(parsed)
    
    def _build_prompt(self, task: str, visual_elements: List[Dict], dom_elements: List[Dict]) -> str:
        visual_summary = "\n".join([
            f"- {el['class_name']} at {el['center']} (conf: {el['confidence']:.2f})"
            for el in visual_elements[:10]
        ])
        
        dom_summary = "\n".join([
            f"- {el['tag']} '{el['text'][:50]}' at {el['bbox']}"
            for el in dom_elements[:10]
        ])
        
        # Use secured prompt template
        base_prompt = f"""Task: {task}

Visual Elements Detected:
{visual_summary}

DOM Elements:
{dom_summary}

Respond with JSON only:
{{
    "action": "click|fill|scroll|wait",
    "target": {{"x": 0, "y": 0}} or {{"selector": "..."}},
    "value": "text to fill (if applicable)",
    "reasoning": "brief explanation"
}}"""
        return SecurityValidator.sanitize_llm_prompt(base_prompt)
    
    # def _query_ollama(self, prompt: str) -> str:
    #     """Ollama integration commented out - using Groq instead"""
    #     try:
    #         response = ollama.chat(
    #             model='llama3',
    #             messages=[{'role': 'user', 'content': prompt}]
    #         )
    #         return response['message']['content']
    #     except Exception as e:
    #         logger.error(f"Ollama error: {e}")
    #         return self._fallback_response()
    
    def _query_groq(self, prompt: str) -> str:
        try:
            response = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
            return self._fallback_response()
    
    def _parse_response(self, response: str) -> Dict:
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except:
            logger.warning("Failed to parse LLM response, using fallback")
            return self._fallback_response()
    
    def _fallback_response(self) -> Dict:
        return {
            "action": "wait",
            "target": {},
            "value": "",
            "reasoning": "Unable to determine action"
        }
