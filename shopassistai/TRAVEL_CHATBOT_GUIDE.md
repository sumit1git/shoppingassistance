# 🌍 Travel Planning Chatbot - Step-by-Step Development Guide

## Project Overview

This project builds an **AI-powered Travel Planning Chatbot** using:
- **LangChain** - For agent orchestration and tool management
- **OpenAI GPT-3.5** - For natural language understanding and generation
- **Flask** - For web server and API endpoints
- **Python** - Backend logic

The chatbot assists travelers by:
- 🏨 Recommending top hotels for destinations
- 📅 Suggesting detailed itineraries
- ✈️ Providing travel planning tips

---

## Project Structure

```
shopassistai/
├── app.py                    # Flask application with chatbot integration
├── travel_chatbot.py         # LangChain chatbot agent
├── travel_tools.py           # Hotel & itinerary recommendation tools
├── requirements.txt          # Python dependencies
├── templates/
│   └── travel_chat.html      # Interactive chat UI
└── .venv/                    # Virtual environment
```

---

## Step-by-Step Development Approach

### **Phase 1: Setup & Installation**

#### Step 1.1: Create Virtual Environment
```bash
cd /Users/sumitkapoor/Desktop/genaiproject/shopassistai
python3 -m venv .venv
source .venv/bin/activate
```

#### Step 1.2: Install Required Packages
```bash
pip install flask openai langchain langchain-community tiktoken
```

**What each package does:**
- `flask` - Web framework for routes and API
- `openai` - OpenAI API client
- `langchain` - Agent & tool orchestration framework
- `langchain-community` - Community integrations for LangChain
- `tiktoken` - Token counter for OpenAI models

#### Step 1.3: Set OpenAI API Key
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Get your API key from: https://platform.openai.com/account/api-keys

---

### **Phase 2: Create Core Tools**

#### Step 2.1: Travel Tools Module (`travel_tools.py`)

This module contains:

**Hotel Database Structure:**
```python
HOTELS_DATABASE = {
    "destination_name": [
        {
            "name": "Hotel Name",
            "rating": 4.8,
            "price_per_night": "$500-800",
            "description": "Description..."
        }
    ]
}
```

**Key Functions:**
- `get_hotel_recommendations(destination)` - Returns formatted hotel list
- `get_itinerary_suggestion(destination, duration)` - Returns day-by-day itinerary

**Supported Destinations:**
- Paris
- Tokyo
- New York
- Barcelona
- Dubai

**How it works:**
1. User specifies destination
2. Function looks up in `HOTELS_DATABASE`
3. Formats data with ratings, prices, descriptions
4. Returns formatted string to chatbot

---

### **Phase 3: Build LangChain Agent**

#### Step 3.1: Travel Chatbot Module (`travel_chatbot.py`)

**Key Components:**

**1. Tool Definition:**
```python
@tool
def recommend_hotels(destination: str) -> str:
    """Recommend top hotels for a given destination."""
    return get_hotel_recommendations(destination)

@tool
def suggest_itinerary(destination: str, duration: str) -> str:
    """Suggest a detailed itinerary for a destination."""
    return get_itinerary_suggestion(destination, duration)
```

**2. LLM Initialization:**
```python
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=api_key
)
```

**3. Agent Creation:**
Uses `create_openai_tools_agent` to create an agent that:
- Understands user intent
- Decides which tools to use
- Orchestrates tool execution
- Generates responses

**System Prompt:**
```
You are a helpful travel planning assistant...
- Hotels/accommodations -> recommend_hotels tool
- Itineraries/activities -> suggest_itinerary tool
- General questions -> Provide travel advice
```

**4. Agent Execution:**
```python
def chat(self, user_message, chat_history=None):
    result = self.agent_executor.invoke({
        "input": user_message,
        "chat_history": chat_history
    })
    return result.get("output")
```

---

### **Phase 4: Flask Integration**

#### Step 4.1: Flask Application (`app.py`)

**Key Routes:**

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display chatbot interface |
| `/chat` | POST | Handle user messages (API) |
| `/clear` | POST | Clear conversation history |
| `/end_conv` | POST | End session |

**Session Management:**
```python
conversation_history = {}  # {session_id: [messages]}

# Each session has isolated chat history
conversation_history[session_id].append({
    'type': 'user',
    'message': user_message
})
```

**Chat Flow:**
1. User sends message via `/chat` API
2. Message added to session history
3. Chatbot processes with full history context
4. Response returned as JSON
5. JavaScript updates UI

---

### **Phase 5: Frontend Development**

#### Step 5.1: Interactive Chat UI (`travel_chat.html`)

**Key Features:**

1. **Chat Container:**
   - Displays messages in conversation format
   - User messages on right (purple)
   - Bot messages on left (gray)
   - Auto-scrolls to latest message

2. **Input Section:**
   - Text input field
   - Send button
   - Clear conversation button
   - Enter key sends message

3. **Real-time Updates:**
   - Loading animation while bot thinks
   - Message count tracker
   - Status indicator (Ready/Thinking/Error)

4. **Styling:**
   - Gradient purple theme
   - Responsive design (mobile-friendly)
   - Smooth animations
   - Professional look

**JavaScript Flow:**
```javascript
// 1. User types message
// 2. sendMessage() is called
// 3. Message shown locally (optimistic)
// 4. POST to /chat endpoint
// 5. Wait for response
// 6. Display bot response
// 7. Scroll to bottom
```

---

## Usage Guide

### **Running the Application**

```bash
# Activate virtual environment
source /Users/sumitkapoor/Desktop/genaiproject/shopassistai/.venv/bin/activate

# Set API key
export OPENAI_API_KEY="your-key-here"

# Run Flask app
python app.py
```

**Output:**
```
* Running on http://127.0.0.1:5000/
```

### **Using the Chatbot**

Open browser and go to: `http://localhost:5000`

**Example Interactions:**

**Example 1: Hotel Recommendations**
```
User: I'm planning a trip to Paris. Can you recommend some hotels?
Bot: [Uses recommend_hotels tool]
     Returns top 3 hotels with ratings and prices
```

**Example 2: Itinerary Planning**
```
User: I have 5 days in Tokyo. What should I visit?
Bot: [Uses suggest_itinerary tool]
     Returns day-by-day itinerary with activities
```

**Example 3: Combined Planning**
```
User: I'm going to Barcelona for a week. I need hotel ideas and things to do.
Bot: [Uses both tools]
     Provides hotels and itinerary with recommendations
```

---

## Architecture Diagram

```
┌─────────────────────────────────────┐
│   User Interface (travel_chat.html) │
│   - Chat messages                   │
│   - Input field                     │
│   - Real-time updates               │
└──────────────┬──────────────────────┘
               │ JSON POST /chat
               ▼
┌─────────────────────────────────────┐
│   Flask App (app.py)                │
│   - Route handlers                  │
│   - Session management              │
│   - Request validation              │
└──────────────┬──────────────────────┘
               │ user_message
               ▼
┌─────────────────────────────────────┐
│   LangChain Agent (travel_chatbot)  │
│   - Understands intent              │
│   - Selects tools                   │
│   - Orchestrates execution          │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
    ┌────────┐   ┌──────────┐
    │ Hotels │   │Itinerary │
    │ Tool   │   │ Tool     │
    └────────┘   └──────────┘
        │             │
        ▼             ▼
┌─────────────────────────────────────┐
│   Data & Tools (travel_tools.py)    │
│   - Hotel database                  │
│   - Itinerary templates             │
│   - Formatting functions            │
└─────────────────────────────────────┘
```

---

## Key Concepts Explained

### **1. LangChain Agents**
- **Agent** = AI that can use tools
- **Tools** = Functions the agent can call
- **Executor** = Runs the agent in a loop
- **Prompt** = Instructions for the agent

### **2. OpenAI Function Calling**
- Agent gets list of available tools with descriptions
- LLM decides which tool to use
- LLM provides tool parameters
- Tool executes and returns result
- LLM processes result and generates response

### **3. Session Management**
- Each user gets unique session ID
- Chat history maintained per session
- Provides context for follow-up questions
- Prevents message leakage between users

### **4. Stateless vs Stateful**
- **Stateless:** Each request independent (REST principles)
- **Stateful:** Session remembers conversation history
- Our app uses in-memory sessions (memory lost on restart)

---

## Extending the Chatbot

### **Add New Tool:**

1. Create function in `travel_tools.py`:
```python
def get_flight_prices(origin, destination, date):
    # Flight search logic
    return formatted_result
```

2. Create LangChain tool in `travel_chatbot.py`:
```python
@tool
def find_flights(origin: str, destination: str, date: str) -> str:
    """Find flight prices for a trip."""
    return get_flight_prices(origin, destination, date)
```

3. Add to tools list:
```python
self.tools = [recommend_hotels, suggest_itinerary, find_flights]
```

4. Update system prompt to mention when to use it.

### **Add New Destination:**

1. Add to `HOTELS_DATABASE` in `travel_tools.py`
2. Add to `ITINERARIES_DATABASE` in `travel_tools.py`
3. Tools automatically work with new data

### **Improve Responses:**

- Adjust `temperature` in `ChatOpenAI` (0=deterministic, 1=creative)
- Enhance system prompt with more detailed instructions
- Add tool result validation and error handling

---

## Troubleshooting

### **Issue: "OpenAI API key not found"**
```bash
export OPENAI_API_KEY="your-key"
echo $OPENAI_API_KEY  # Verify it's set
```

### **Issue: Module not found errors**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### **Issue: Port 5000 already in use**
```bash
python app.py --port 5001
# Or kill existing process
lsof -i :5000
kill -9 <PID>
```

### **Issue: Chatbot not responding**
- Check API key is valid
- Check OpenAI account has credits
- Check internet connection
- Review Flask error logs

---

## Requirements File

Create `requirements.txt`:
```
flask==2.3.0
openai==0.27.0
langchain==0.0.200
langchain-community==0.0.15
tiktoken==0.4.0
```

Install: `pip install -r requirements.txt`

---

## Summary

This chatbot demonstrates:
✅ LangChain agent patterns
✅ OpenAI function calling
✅ Tool orchestration
✅ REST API design
✅ Real-time web UI
✅ Session management
✅ Error handling
✅ Scalable architecture

Start with the tools, build the agent, integrate with Flask, and polish the UI!

Happy travels! 🌍✈️
