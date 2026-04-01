# Travel Chatbot - Visual Architecture & Flow Diagrams

## 1. User Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERACTION FLOW                    │
└─────────────────────────────────────────────────────────────┘

User Opens Browser
       │
       ▼
Load http://localhost:5000
       │
       ▼
┌─────────────────────────────────────────┐
│  Flask Returns travel_chat.html         │
│  - Shows welcome message                │
│  - Displays empty chat box              │
│  - Loads JavaScript                     │
└─────────────────────────────────────────┘
       │
       ▼
User Types Message & Presses Send
       │
       ▼
JavaScript Sends POST /chat (JSON)
       │
       ▼
┌─────────────────────────────────────────┐
│  Shows Loading Animation                │
│  "Bot is thinking..."                   │
└─────────────────────────────────────────┘
       │
       ▼
Flask /chat Route Receives Request
       │
       ▼
Passes to TravelChatbot Agent
       │
       ▼
Agent Processes & Returns Response
       │
       ▼
Flask Sends JSON Response
       │
       ▼
JavaScript Removes Loading Animation
       │
       ▼
JavaScript Displays Bot Response
       │
       ▼
User Sees Message in Chat
       │
       ▼
User Can Send Another Message
```

---

## 2. Message Processing Pipeline

```
┌──────────────────────────────────────────────────────────────┐
│                MESSAGE PROCESSING PIPELINE                   │
└──────────────────────────────────────────────────────────────┘

Input:  "What are the best hotels in Paris?"

    ▼

┌────────────────────────────────────────┐
│  FLASK LAYER (app.py)                  │
│  - Receives POST request                │
│  - Validates input                      │
│  - Gets/creates session ID              │
│  - Passes to chatbot                    │
└────────────────────────────────────────┘

    ▼

┌────────────────────────────────────────┐
│  LANGCHAIN AGENT (travel_chatbot.py)   │
│                                        │
│  INPUT: "Hotels in Paris?"             │
│                                        │
│  1. LLM Analyzes Input                 │
│     "This is about hotels"             │
│                                        │
│  2. LLM Selects Tool                   │
│     "Use: recommend_hotels"            │
│                                        │
│  3. LLM Extracts Parameters            │
│     destination = "Paris"              │
│                                        │
│  4. Calls Tool                         │
│     recommend_hotels("Paris")          │
└────────────────────────────────────────┘

    ▼

┌────────────────────────────────────────┐
│  TOOLS LAYER (travel_tools.py)         │
│                                        │
│  recommend_hotels("Paris")             │
│  ├─ Look up in HOTELS_DATABASE        │
│  ├─ Find: Le Meurice, Plaza Athénée   │
│  ├─ Get ratings, prices, descriptions │
│  └─ Format as string                  │
│                                        │
│  OUTPUT:                               │
│  "🏨 Top Hotels in Paris:             │
│   1. Le Meurice                       │
│      ⭐ 4.8/5                         │
│      💰 $500-800 per night"           │
└────────────────────────────────────────┘

    ▼

┌────────────────────────────────────────┐
│  LANGCHAIN AGENT (Continued)           │
│                                        │
│  5. Receives Tool Result               │
│     (Hotel list with details)          │
│                                        │
│  6. LLM Generates Response             │
│     Enhances tool output with:         │
│     - Friendly tone                    │
│     - Additional tips                  │
│     - Questions to refine              │
│                                        │
│  FINAL OUTPUT:                         │
│  "Great question! Here are the best   │
│   hotels in Paris... [hotel list]...  │
│   Would you like to know about        │
│   itineraries too?"                   │
└────────────────────────────────────────┘

    ▼

┌────────────────────────────────────────┐
│  FLASK RESPONSE (app.py)               │
│  ├─ Serialize to JSON                  │
│  ├─ Include session info               │
│  └─ Send to client                     │
└────────────────────────────────────────┘

    ▼

┌────────────────────────────────────────┐
│  FRONTEND RENDERING (travel_chat.html) │
│  ├─ Parse JSON response                │
│  ├─ Create message bubble              │
│  ├─ Animate into view                  │
│  ├─ Scroll to bottom                   │
│  └─ Re-enable input field              │
└────────────────────────────────────────┘

Output: Bot response displayed in chat
```

---

## 3. Tool Selection Logic

```
┌─────────────────────────────────────────────────────────────┐
│              LANGCHAIN TOOL SELECTION LOGIC                 │
└─────────────────────────────────────────────────────────────┘

System Prompt to LLM:
"You are a travel assistant with two tools:
 1. recommend_hotels(destination)
    → Use when: Hotels, accommodations, places to stay
 2. suggest_itinerary(destination, duration)
    → Use when: Itineraries, activities, things to do"

Example Decisions:

User Input                    Tool Selected       Parameter
───────────────────────────────────────────────────────────
"Hotels in Paris?"      →   recommend_hotels    destination="Paris"
"What to do in Tokyo?"  →   suggest_itinerary  destination="Tokyo"
                                                duration="unknown"
"5 days in Barcelona"   →   suggest_itinerary  destination="Barcelona"
                                                duration="5 days"
"Best hotels + plans    →   BOTH TOOLS         (chain requests)
 for Dubai?"

"Tell me about Paris"   →   NO TOOL            (general knowledge)
                            (LLM responds directly)

Error Cases:
─────────────────────────────────────────────────────────────
Invalid Destination: Agent asks for clarification
Missing Duration: Agent provides default or asks
Invalid Tool Call: Error handling + fallback response
```

---

## 4. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                        │
└──────────────────────────────────────────────────────────────┘

                    Web Browser
                         │
                         │ HTTP/WebSocket
                         ▼
                    ┌─────────────┐
                    │ Flask App   │
                    │ (Jinja2)    │
                    └─────────────┘
                    │              │
          GET /     │              │ POST /chat
                    ▼              ▼
            travel_chat.html   /chat Route
                │              │
                │              ├─ Request.json
                │              ├─ session_id
                │              └─ message
                │
                │              ▼
                │         ┌──────────────┐
                │         │ TravelChatbot│
                │         │  .chat()     │
                │         └──────────────┘
                │              │
                │         ┌────┴────┐
                │         ▼         ▼
                │       Tool1     Tool2
                │    recommend  suggest
                │    _hotels   _itinerary
                │         │         │
                │         ▼         ▼
                │    ┌──────────────────┐
                │    │ travel_tools.py  │
                │    ├─ HOTELS_DATABASE │
                │    ├─ ITINERARIES_DB  │
                │    └─ Functions       │
                │         │
                │         ▼
                │    Formatted Output
                │         │
                │         ▼
                │    LLM Response
                │         │
                │         └─────┐
                │               │
                ▼               ▼
            HTML UI         JSON API
            (Display)       (Response)
```

---

## 5. Session Management

```
┌──────────────────────────────────────────────────────────────┐
│                  SESSION MANAGEMENT FLOW                      │
└──────────────────────────────────────────────────────────────┘

Client 1                    Client 2
   │                           │
   │ POST /chat                │ POST /chat
   │ session_id: "12345"      │ session_id: "67890"
   ▼                           ▼
┌────────────────────────────────────────────┐
│         Flask conversation_history         │
│                                            │
│ {                                          │
│   "12345": [                               │
│     {"type": "user", "msg": "..."},       │
│     {"type": "bot", "msg": "..."},        │
│     {"type": "user", "msg": "..."}        │
│   ],                                       │
│   "67890": [                               │
│     {"type": "user", "msg": "..."},       │
│     {"type": "bot", "msg": "..."}         │
│   ]                                        │
│ }                                          │
└────────────────────────────────────────────┘

Benefits:
- Users don't see each other's conversations
- Full context maintained for follow-up questions
- Independent session histories
- Can scale to multiple servers with session store
```

---

## 6. Error Handling Flow

```
┌──────────────────────────────────────────────────────────────┐
│                   ERROR HANDLING FLOW                         │
└──────────────────────────────────────────────────────────────┘

User Input
    │
    ▼
Validate Input
    │
    ├─ Empty message? ──────┐
    │                        │
    ├─ Invalid JSON? ───────┐│
    │                        ││
    └─ Valid? ────────┐     ││
                      │     ││
                      │     │└─► Return Error
                      │     └──► Return Error
                      │
                      ▼
                Send to Agent
                    │
                    ├─ API Key Missing? ──────┐
                    │                         │
                    ├─ API Error? ───────────┐│
                    │                         ││
                    ├─ Tool Not Found? ──────┐││
                    │                         │││
                    └─ Success? ────────┐    │││
                                        │    │││
                                        │    ││└─ "Chatbot not configured"
                                        │    │└──► "OpenAI API error"
                                        │    └───► "Tool execution failed"
                                        │
                                        ▼
                                   Return Response
                                        │
                                        ▼
                                   Display to User
                                   (Error in red)
```

---

## 7. Component Interaction

```
┌──────────────────────────────────────────────────────────────┐
│               COMPONENT INTERACTION DIAGRAM                   │
└──────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────┐
│         Frontend (JavaScript)          │
│                                        │
│  - Captures user input                 │
│  - Shows loading state                 │
│  - Updates chat display                │
│  - Manages UI state                    │
└────────────────────────────────────────┘
         │                         ▲
         │ Sends JSON              │ Returns JSON
         │ (message, session_id)   │ (response)
         ▼                         │
┌────────────────────────────────────────┐
│      Flask Application (Python)        │
│                                        │
│  - Routes requests                     │
│  - Manages sessions                    │
│  - Calls chatbot                       │
│  - Returns responses                   │
└────────────────────────────────────────┘
         │
         │ Calls
         ▼
┌────────────────────────────────────────┐
│   Travel Chatbot (LangChain Agent)     │
│                                        │
│  - Understands intent                  │
│  - Selects tools                       │
│  - Executes tools                      │
│  - Formats response                    │
└────────────────────────────────────────┘
         │                      ▲
         │ Calls               │ Returns
         │                     │
    ┌────┴────┐────────────┬──┴─────┐
    ▼         ▼            ▼        ▼
┌────────┐┌─────────┐┌──────────┐┌────────┐
│Hotels  ││Itinerary││  OpenAI  ││ Errors │
│Tool    ││Tool     ││  API     ││Handler │
└────────┘└─────────┘└──────────┘└────────┘
    │         │          │
    │         │          │
    └────┬────┴──────────┘
         │
         ▼
┌────────────────────────────────────────┐
│    Data Layer (travel_tools.py)        │
│                                        │
│  - HOTELS_DATABASE                     │
│  - ITINERARIES_DATABASE                │
│  - Format functions                    │
└────────────────────────────────────────┘
```

---

## 8. Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              DEPLOYMENT ARCHITECTURE                          │
└──────────────────────────────────────────────────────────────┘

Production Setup:

                    Users
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌──────────┬──────────┬──────────┐
    │  Server  │  Server  │  Server  │
    │    1     │    2     │    3     │
    └──────────┴──────────┴──────────┘
        │            │            │
        └────────────┼────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌──────────────────────────────────┐
    │   Session Store (Redis/Cache)    │
    │   (Shared across servers)        │
    └──────────────────────────────────┘
         │
         └──────────┬──────────┐
                    │          │
         ┌──────────▼──┐   ┌───▼──────────┐
         │   Database  │   │  File Store  │
         │  (Postgres) │   │  (S3/Cloud)  │
         └─────────────┘   └──────────────┘

Currently: Single server with in-memory sessions
Future: Distributed with shared session store
```

---

## 9. Request/Response Examples

```
┌──────────────────────────────────────────────────────────────┐
│         REQUEST/RESPONSE EXAMPLES                             │
└──────────────────────────────────────────────────────────────┘

REQUEST (Browser → Flask):
─────────────────────────────────────────
POST /chat
Content-Type: application/json

{
  "message": "Hotels in Paris?",
  "session_id": "1704547200000"
}


RESPONSE (Flask → Browser):
─────────────────────────────────────────
{
  "success": true,
  "response": "Great question! Here are the top hotels in Paris...",
  "conversation_length": 3
}


RESPONSE (Error Case):
─────────────────────────────────────────
{
  "success": false,
  "error": "OpenAI API key not configured",
  "code": "API_KEY_MISSING"
}


RESPONSE (Loading State - Frontend Only):
─────────────────────────────────────────
Displays:
"Bot is thinking
 •  •  •"
```

---

## 10. Technology Stack Visualization

```
┌──────────────────────────────────────────────────────────────┐
│                  TECHNOLOGY STACK                             │
└──────────────────────────────────────────────────────────────┘

Frontend Layer:
┌─────────────────────────────────────┐
│ HTML5 + CSS3 + JavaScript (ES6)     │
│ - No build process required         │
│ - Modern browser APIs               │
│ - Responsive design                 │
└─────────────────────────────────────┘

Backend Framework:
┌─────────────────────────────────────┐
│ Flask 2.3.0 (Python Web Framework) │
│ - Lightweight and flexible          │
│ - Perfect for REST APIs             │
│ - Great for prototyping             │
└─────────────────────────────────────┘

AI/ML Layer:
┌─────────────────────────────────────┐
│ LangChain 0.0.200                   │
│ - Agent orchestration               │
│ - Tool management                   │
│ - LLM abstraction                   │
│                                     │
│ OpenAI API                          │
│ - GPT-3.5-turbo model              │
│ - Chat completions                  │
│ - Function calling                  │
└─────────────────────────────────────┘

Data Layer:
┌─────────────────────────────────────┐
│ In-Memory Storage (Python dicts)    │
│ - Hotels database                   │
│ - Itineraries database              │
│ - Session history                   │
│                                     │
│ Extensible to:                      │
│ - PostgreSQL                        │
│ - MongoDB                           │
│ - Redis (for sessions)              │
└─────────────────────────────────────┘

Utilities:
┌─────────────────────────────────────┐
│ tiktoken - Token counting           │
│ python-dotenv - Config management   │
│ requests - HTTP client              │
└─────────────────────────────────────┘
```

---

## Summary

This architecture demonstrates:
✅ **Scalability** - Can be distributed across servers
✅ **Modularity** - Each component is independent
✅ **Extensibility** - Easy to add new tools/features
✅ **Error Handling** - Graceful failure modes
✅ **User Experience** - Real-time interactive chat
✅ **Best Practices** - Session management, API design
