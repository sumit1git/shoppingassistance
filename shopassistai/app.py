from flask import Flask, redirect, url_for, render_template, request, jsonify
import os
from travel_chatbot import TravelChatbot

app = Flask(__name__)

# Initialize the travel chatbot
try:
    chatbot = TravelChatbot(api_key=os.getenv('OPENAI_API_KEY'))
    chatbot_ready = True
except Exception as e:
    chatbot_ready = False
    chatbot_error = str(e)

# Store conversation history per session
conversation_history = {}


@app.route('/')
def default_route():
    """Main page - travel chatbot interface."""
    session_id = request.args.get('session_id', 'default')
    
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    
    welcome_msg = chatbot.get_welcome_message() if chatbot_ready else "ChatBot is not configured properly. Please set OPENAI_API_KEY."
    
    return render_template('travel_chat.html', 
                         welcome_message=welcome_msg,
                         chatbot_ready=chatbot_ready,
                         session_id=session_id)


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages via API."""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        if not chatbot_ready:
            return jsonify({'error': 'Chatbot is not initialized'}), 500
        
        # Get or create conversation history for this session
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Format conversation history for LangChain (use HumanMessage/AIMessage format)
        from langchain.schema import HumanMessage, AIMessage
        
        langchain_history = []
        for msg in conversation_history[session_id]:
            if msg['role'] == 'user':
                langchain_history.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                langchain_history.append(AIMessage(content=msg['content']))
        
        # Get chatbot response
        bot_response = chatbot.chat(
            user_message, 
            chat_history=langchain_history
        )
        
        # Add user message to history with correct format
        conversation_history[session_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Add bot response to history with correct format
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': bot_response
        })
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'conversation_length': len(conversation_history[session_id])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history for a session."""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversation_history:
            conversation_history[session_id] = []
        
        return jsonify({'success': True, 'message': 'Conversation cleared'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/end_conv', methods=['POST'])
def end_conv():
    """End conversation endpoint (for backward compatibility)."""
    session_id = request.args.get('session_id', 'default')
    conversation_history[session_id] = []
    return redirect(url_for('default_route', session_id=session_id))


if __name__ == "__main__":
    app.run(debug=True)