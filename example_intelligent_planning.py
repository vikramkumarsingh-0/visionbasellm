"""
Intelligent Planning Examples
Demonstrates complex task decomposition using LangChain + Groq
"""

from core.intelligent_planner import IntelligentPlanner, ConversationalPlanner
from automation_agent import AutomationAgent
from loguru import logger
import json

# Set your Groq API key
import os
os.environ['GROQ_API_KEY'] = 'your_groq_api_key_here'  # Replace with actual key

def example_holiday_planning():
    """Example: Complex holiday planning"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Holiday Planning")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    I want to plan a holiday this summer. List me the places to visit:
    1. First in my state (California)
    2. Then in my country (USA)
    3. Then out of country
    
    For each location, suggest:
    - Places to visit
    - Estimated expenses
    - Time needed
    - Cost of travel (own vehicle, rent, train, flight)
    - Hotel booking options
    - Best season to visit
    """
    
    # Create automation plan
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print(f"  Extract: {', '.join(action.data_to_extract)}")
        print()
    
    print(f"Final Output: {plan.final_output_format}")
    
    # Execute plan (optional)
    # agent = AutomationAgent(use_groq=True, headless=True)
    # results = planner.execute_plan(plan, agent)
    # print(json.dumps(results, indent=2))


def example_shopping():
    """Example: Shopping for clothes"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Shopping for Clothes")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    Buy summer clothes for me:
    - T-shirts (5 pieces)
    - Shorts (3 pieces)
    - Sandals (1 pair)
    
    Compare prices from:
    - Amazon
    - Walmart
    - Target
    
    Show me the best deals and total cost.
    """
    
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print()


def example_movie_booking():
    """Example: Book movie tickets"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Movie Ticket Booking")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    Book movie tickets for this weekend:
    - Find movies playing near me (zip code: 90210)
    - Show timings for Saturday and Sunday
    - Compare ticket prices
    - Check seat availability
    - Suggest best theaters with good ratings
    """
    
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print()


def example_laptop_comparison():
    """Example: Compare laptop prices"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Laptop Price Comparison")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    I want to buy a laptop for programming:
    - Budget: $1000-1500
    - Requirements: 16GB RAM, 512GB SSD, good processor
    
    Compare options from:
    - Best Buy
    - Amazon
    - Newegg
    
    Show specifications, prices, reviews, and delivery time.
    """
    
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print()


def example_conversational_planning():
    """Example: Interactive conversation to refine plan"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Conversational Planning")
    print("="*60)
    
    conv_planner = ConversationalPlanner()
    
    # User starts conversation
    response1 = conv_planner.chat("I want to plan a trip")
    print(f"Assistant: {response1}\n")
    
    # User provides more details
    response2 = conv_planner.chat("To Europe, for 2 weeks, budget is $5000")
    print(f"Assistant: {response2}\n")
    
    # User confirms
    response3 = conv_planner.chat("Yes, please create the plan")
    print(f"Assistant: {response3}\n")
    
    # Finalize plan
    final_plan = conv_planner.finalize_plan()
    print(f"\nFinal Plan: {final_plan.plan_summary}")
    print(f"Total Steps: {final_plan.total_steps}")


def example_restaurant_booking():
    """Example: Restaurant reservation"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Restaurant Booking")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    Find and book a restaurant for dinner:
    - Cuisine: Italian
    - Location: Downtown Los Angeles
    - Date: This Friday
    - Party size: 4 people
    - Budget: $200
    
    Show me:
    - Top rated restaurants
    - Available time slots
    - Menu highlights
    - Reviews
    """
    
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print()


def example_job_search():
    """Example: Job search and application"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Job Search")
    print("="*60)
    
    planner = IntelligentPlanner()
    
    user_request = """
    Help me find a job:
    - Position: Software Engineer
    - Location: Remote or San Francisco
    - Experience: 3-5 years
    - Skills: Python, Machine Learning, Web Development
    
    Search on:
    - LinkedIn
    - Indeed
    - Glassdoor
    
    For each job:
    - Company name and rating
    - Salary range
    - Job description
    - Application deadline
    - Required skills match
    """
    
    plan = planner.create_plan(user_request)
    
    print(f"\nPlan Summary: {plan.plan_summary}")
    print(f"Total Steps: {plan.total_steps}\n")
    
    for action in plan.actions:
        print(f"Step {action.step_number}: {action.action_description}")
        print(f"  Website: {action.website}")
        print()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("INTELLIGENT WEB AUTOMATION PLANNER")
    print("Powered by LangChain + Groq + HuggingFace")
    print("="*60)
    
    # Check if API key is set
    if os.getenv('GROQ_API_KEY') == 'your_groq_api_key_here':
        print("\n⚠️  WARNING: Please set your GROQ_API_KEY in the script or environment")
        print("Get your key from: https://console.groq.com/keys\n")
        exit(1)
    
    try:
        # Run examples
        example_holiday_planning()
        example_shopping()
        example_movie_booking()
        example_laptop_comparison()
        example_restaurant_booking()
        example_job_search()
        
        # Interactive example (commented out - requires user input)
        # example_conversational_planning()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set GROQ_API_KEY environment variable")
        print("2. Installed: pip install langchain langchain-groq")
