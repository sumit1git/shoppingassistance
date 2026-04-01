"""
LangChain-based Travel Planning Chatbot.
Uses LLM with tools for hotel recommendations and itinerary suggestions.
"""

import os
from typing import Any
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOpenAI
from travel_tools import get_hotel_recommendations, get_itinerary_suggestion


# Define tools for LangChain
@tool
def recommend_hotels(destination: str) -> str:
    """
    Recommend top hotels for a given destination.
    Use this when the user asks about hotels, accommodations, or places to stay.
    
    Args:
        destination: The city or destination name (e.g., 'Paris', 'Tokyo', 'New York')
    
    Returns:
        Hotel recommendations with ratings and prices
    """
    return get_hotel_recommendations(destination)


@tool
def suggest_itinerary(destination: str, duration: str) -> str:
    """
    Suggest a detailed itinerary for a destination based on trip duration.
    Use this when the user asks about what to do, things to visit, or travel plans.
    
    Args:
        destination: The city or destination name (e.g., 'Paris', 'Tokyo', 'New York')
        duration: How long the trip is (e.g., '3 days', '5 days', '7 days')
    
    Returns:
        Detailed itinerary with day-by-day activities
    """
    return get_itinerary_suggestion(destination, duration)


class TravelChatbot:
    """Travel Planning Chatbot powered by LangChain and OpenAI."""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the chatbot with OpenAI API key.
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env variable
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please provide it or set OPENAI_API_KEY environment variable."
            )
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=api_key
        )
        
        # Define tools
        self.tools = [recommend_hotels, suggest_itinerary]
        
        # Create the agent
        self._create_agent()
    
    def _create_agent(self):
        """Create the LangChain agent with tools."""
        # System prompt for the chatbot
        system_prompt = """You are a helpful travel planning assistant that helps users plan their trips. 
        You have access to tools that provide hotel recommendations and itinerary suggestions.
        
        When users ask about:
        - Hotels, accommodations, or places to stay -> Use the recommend_hotels tool
        - Things to do, itineraries, or travel plans -> Use the suggest_itinerary tool
        - General travel questions -> Provide helpful advice and ask clarifying questions
        
        Always be friendly, enthusiastic, and provide detailed recommendations.
        If the user mentions a destination and duration, gather both pieces of information before calling tools.
        Combine the tool outputs with your own travel knowledge to provide comprehensive assistance."""
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        # Create the agent
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        
        # Create the executor
        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def chat(self, user_message: str, chat_history: list = None) -> str:
        """
        Process user message and return chatbot response.
        
        Args:
            user_message: The user's input message
            chat_history: Previous chat messages for context (optional)
        
        Returns:
            The chatbot's response
        """
        if chat_history is None:
            chat_history = []
        
        try:
            result = self.agent_executor.invoke({
                "input": user_message,
                "chat_history": chat_history
            })
            return result.get("output", "I apologize, I couldn't process your request.")
        except Exception as e:
            return f"I encountered an error: {str(e)}"
    
    def get_welcome_message(self) -> str:
        """Get a welcome message for new users."""
        return """🌍 Welcome to Travel Planning Assistant!

I'm here to help you plan your perfect trip! I can assist you with:
- 🏨 Finding the best hotels and accommodations
- 📅 Creating detailed itineraries based on your trip duration
- ✈️ Providing travel tips and recommendations

Which destination would you like to explore? (e.g., Paris, Tokyo, New York, Barcelona, Dubai)"""
