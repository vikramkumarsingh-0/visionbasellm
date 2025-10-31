from typing import List, Dict, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from loguru import logger
import os

class WebAction(BaseModel):
    """Single web automation action"""
    step_number: int = Field(description="Step sequence number")
    website: str = Field(description="Website URL to visit")
    action_type: str = Field(description="Type: search, click, fill, extract, compare")
    action_description: str = Field(description="What to do on the website")
    data_to_extract: List[str] = Field(description="What information to collect")
    expected_result: str = Field(description="What result to expect")

class AutomationPlan(BaseModel):
    """Complete automation plan"""
    user_intent: str = Field(description="Original user request")
    plan_summary: str = Field(description="Brief summary of the plan")
    total_steps: int = Field(description="Total number of steps")
    actions: List[WebAction] = Field(description="List of actions to perform")
    final_output_format: str = Field(description="How to present final results")

class IntelligentPlanner:
    """
    Converts natural language requests into structured web automation plans
    Uses Groq + LangChain for intelligent task decomposition
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.groq_api_key = groq_api_key or os.getenv('GROQ_API_KEY')
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        # Initialize Groq LLM
        self.llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama3-70b-8192",
            temperature=0.1
        )
        
        # Setup output parser
        self.parser = PydanticOutputParser(pydantic_object=AutomationPlan)
        
        # Create planning prompt
        self.planning_prompt = PromptTemplate(
            template="""You are an expert web automation planner. Convert user requests into structured automation plans.

User Request: {user_request}

Your task:
1. Understand what the user wants to accomplish
2. Break it down into specific web automation steps
3. Identify which websites to visit
4. Determine what data to extract
5. Plan how to compare and present results

Guidelines:
- Be specific about websites (use real URLs like google.com, booking.com, etc.)
- Each step should be a single, clear action
- Extract relevant data at each step
- Consider multiple options (flights, trains, hotels, etc.)
- Think about comparisons and recommendations

{format_instructions}

Generate a complete automation plan:""",
            input_variables=["user_request"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        # Create LangChain
        self.planning_chain = LLMChain(
            llm=self.llm,
            prompt=self.planning_prompt
        )
    
    def create_plan(self, user_request: str) -> AutomationPlan:
        """
        Convert user request into structured automation plan
        
        Examples:
        - "Plan a holiday to Paris"
        - "Buy clothes for summer"
        - "Book movie tickets for this weekend"
        - "Compare laptop prices"
        """
        logger.info(f"Creating automation plan for: {user_request}")
        
        try:
            # Generate plan using LLM
            result = self.planning_chain.run(user_request=user_request)
            
            # Parse into structured format
            plan = self.parser.parse(result)
            
            logger.info(f"Plan created with {plan.total_steps} steps")
            return plan
            
        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            # Fallback to simple plan
            return self._create_fallback_plan(user_request)
    
    def _create_fallback_plan(self, user_request: str) -> AutomationPlan:
        """Simple fallback plan if LLM fails"""
        return AutomationPlan(
            user_intent=user_request,
            plan_summary="Simple search and extract plan",
            total_steps=1,
            actions=[
                WebAction(
                    step_number=1,
                    website="https://google.com",
                    action_type="search",
                    action_description=f"Search for: {user_request}",
                    data_to_extract=["search results", "top links"],
                    expected_result="List of relevant results"
                )
            ],
            final_output_format="List of search results"
        )
    
    def execute_plan(self, plan: AutomationPlan, automation_agent) -> Dict:
        """
        Execute the automation plan step by step
        """
        results = []
        
        for action in plan.actions:
            logger.info(f"Executing step {action.step_number}: {action.action_description}")
            
            try:
                # Execute automation
                result = automation_agent.execute_task(
                    url=action.website,
                    task=action.action_description
                )
                
                results.append({
                    'step': action.step_number,
                    'action': action.action_description,
                    'website': action.website,
                    'success': result.get('success', False),
                    'data': result
                })
                
            except Exception as e:
                logger.error(f"Step {action.step_number} failed: {e}")
                results.append({
                    'step': action.step_number,
                    'action': action.action_description,
                    'success': False,
                    'error': str(e)
                })
        
        return {
            'plan_summary': plan.plan_summary,
            'total_steps': plan.total_steps,
            'completed_steps': len([r for r in results if r.get('success')]),
            'results': results,
            'final_output_format': plan.final_output_format
        }


class ConversationalPlanner:
    """
    Interactive planner that can refine plans through conversation
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.planner = IntelligentPlanner(groq_api_key)
        self.conversation_history = []
    
    def chat(self, user_message: str) -> str:
        """
        Have a conversation to refine the automation plan
        """
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Build context from history
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history[-5:]  # Last 5 messages
        ])
        
        # Generate response
        prompt = f"""You are a helpful automation assistant. Help the user plan their web automation task.

Conversation:
{context}

Provide a helpful response. If the user's request is clear, confirm the plan. If unclear, ask clarifying questions.

Response:"""
        
        response = self.planner.llm.predict(prompt)
        
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def finalize_plan(self) -> AutomationPlan:
        """
        Create final plan from conversation
        """
        # Extract user intent from conversation
        user_intent = " ".join([
            msg['content'] for msg in self.conversation_history 
            if msg['role'] == 'user'
        ])
        
        return self.planner.create_plan(user_intent)
