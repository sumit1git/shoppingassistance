# 🌍 Travel Planning Chatbot - Quick Start Guide

## Quick Setup (5 minutes)

### 1. **Activate Virtual Environment**
```bash
cd /Users/sumitkapoor/Desktop/genaiproject/shopassistai
source .venv/bin/activate
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Get OpenAI API Key**
- Go to: https://platform.openai.com/account/api-keys
- Create a new API key
- Copy it

### 4. **Set API Key**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### 5. **Run Flask App**
```bash
python app.py
```

### 6. **Open in Browser**
```
http://localhost:5000
```

---

## Test Without OpenAI Key

You can test the core tools without an API key:

```bash
python test_chatbot.py
```

This tests:
- ✅ Hotel recommendations
- ✅ Itinerary suggestions
- ✅ Error handling
- ⏭️ Skips LangChain agent (requires API key)

---

## What the Chatbot Can Do

Ask it anything like:

1. **"What are the best hotels in Paris?"**
   → Returns top 3 hotels with ratings and prices

2. **"Give me a 5-day itinerary for Tokyo"**
   → Returns day-by-day activities

3. **"I'm going to Barcelona for a week. What should I do?"**
   → Uses both tools to provide complete trip plan

4. **"Show me hotels in Dubai"**
   → Lists luxury options with details

---

## Project Files Explained

| File | Purpose |
|------|---------|
| `app.py` | Flask web server with chat API |
| `travel_chatbot.py` | LangChain agent that uses tools |
| `travel_tools.py` | Hotel & itinerary data + functions |
| `test_chatbot.py` | Test script to verify everything works |
| `templates/travel_chat.html` | Beautiful chat UI |
| `TRAVEL_CHATBOT_GUIDE.md` | Detailed development guide |
| `requirements.txt` | Python packages to install |

---

## Supported Destinations

- 🇫🇷 **Paris** - 3, 5, 7 days
- 🇯🇵 **Tokyo** - 3, 5, 7 days
- 🇺🇸 **New York** - 3, 5, 7 days
- 🇪🇸 **Barcelona** - 3, 5, 7 days
- 🇦🇪 **Dubai** - 3, 5, 7 days

---

## Troubleshooting

### **"Module not found" error**
```bash
pip install -r requirements.txt
```

### **"API key not found" error**
```bash
export OPENAI_API_KEY="your-key"
```

### **Port 5000 already in use**
```bash
# Kill the process
lsof -i :5000
kill -9 <PID>

# Or use different port
python app.py --port 5001
```

### **Can't import langchain**
```bash
pip install langchain langchain-community openai
```

---

## Add New Destinations

1. Open `travel_tools.py`
2. Add to `HOTELS_DATABASE` dictionary
3. Add to `ITINERARIES_DATABASE` dictionary
4. Chatbot automatically works with new data!

Example:
```python
"London": [
    {
        "name": "The Savoy",
        "rating": 4.8,
        "price_per_night": "$400-700",
        "description": "Historic luxury hotel on Thames"
    }
]
```

---

## Architecture at a Glance

```
User Types Message
        ↓
    Flask Route
        ↓
   LangChain Agent
        ↓
    (Decides which tool)
        ↓
   Hotel or Itinerary Tool
        ↓
   OpenAI LLM Formats Response
        ↓
   JavaScript Updates UI
```

---

## Next Steps

1. ✅ Set up environment
2. ✅ Get API key
3. ✅ Run the app
4. 📚 Read `TRAVEL_CHATBOT_GUIDE.md` for deep dive
5. 🔧 Extend with more destinations/features

---

## More Help

See `TRAVEL_CHATBOT_GUIDE.md` for:
- Detailed step-by-step guide
- How to extend the chatbot
- Architecture diagrams
- Concept explanations
- Best practices

Happy travels! 🌍✈️
