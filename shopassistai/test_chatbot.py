#!/usr/bin/env python3
"""
Quick test script for the Travel Planning Chatbot.
Run this to test the chatbot without the web interface.
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from travel_tools import get_hotel_recommendations, get_itinerary_suggestion


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def test_hotel_recommendations():
    """Test hotel recommendation tool."""
    print_section("Testing Hotel Recommendations")
    
    destinations = ["Paris", "Tokyo", "New York", "Barcelona", "Dubai"]
    
    for destination in destinations:
        print(f"\n🔍 Fetching hotels for {destination}...")
        result = get_hotel_recommendations(destination)
        print(result)
        print("\n" + "-"*60)


def test_itinerary_suggestions():
    """Test itinerary suggestion tool."""
    print_section("Testing Itinerary Suggestions")
    
    test_cases = [
        ("Paris", "3 days"),
        ("Tokyo", "5 days"),
        ("New York", "7 days"),
        ("Barcelona", "3 days"),
        ("Dubai", "5 days"),
    ]
    
    for destination, duration in test_cases:
        print(f"\n🗓️ Fetching {duration} itinerary for {destination}...")
        result = get_itinerary_suggestion(destination, duration)
        print(result)
        print("\n" + "-"*60)


def test_invalid_inputs():
    """Test error handling with invalid inputs."""
    print_section("Testing Error Handling")
    
    # Invalid destination
    print("Testing invalid destination...")
    result = get_hotel_recommendations("Atlantis")
    print(result)
    print("\n" + "-"*60)
    
    # Invalid duration
    print("\nTesting invalid duration...")
    result = get_itinerary_suggestion("Paris", "10 days")
    print(result)
    print("\n" + "-"*60)


def test_langchain_agent():
    """Test the LangChain agent (requires OPENAI_API_KEY)."""
    print_section("Testing LangChain Agent")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️  OPENAI_API_KEY not set. Skipping agent test.")
        print("   Run: export OPENAI_API_KEY='your-key'")
        return
    
    try:
        from travel_chatbot import TravelChatbot
        
        print("Initializing chatbot...")
        chatbot = TravelChatbot(api_key=api_key)
        
        print("\nChatbot ready! Testing with sample messages...\n")
        
        test_messages = [
            "What are the best hotels in Paris?",
            "Give me a 5-day itinerary for Tokyo",
            "I'm planning a week-long trip to Barcelona. What should I do?",
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n📨 User: {message}")
            print("-" * 60)
            response = chatbot.chat(message)
            print(f"🤖 Bot: {response}\n")
            print("=" * 60)
    
    except ImportError as e:
        print(f"❌ Error importing TravelChatbot: {e}")
        print("   Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        print("   Check that OPENAI_API_KEY is valid")


def main():
    """Run all tests."""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║           Travel Chatbot - Component Tests                   ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    # Test core tools
    test_hotel_recommendations()
    test_itinerary_suggestions()
    test_invalid_inputs()
    
    # Test LangChain agent
    test_langchain_agent()
    
    print_section("Tests Complete")
    print("✅ All component tests finished!")
    print("\nNext steps:")
    print("1. Set OPENAI_API_KEY: export OPENAI_API_KEY='your-key'")
    print("2. Run the Flask app: python app.py")
    print("3. Open browser: http://localhost:5000")


if __name__ == "__main__":
    main()
