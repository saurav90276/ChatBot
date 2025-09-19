import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="AI Assistant", layout="centered")
st.title("🧠 Personal Assistant Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful personal assistant."}
    ]

def get_openrouter_response(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # Replace with any available model on OpenRouter
        "messages": messages
    }

    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"API error: {e}")
        return "Sorry, something went wrong."

# Chat UI
user_input = st.text_input("You:", placeholder="Ask me anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_openrouter_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Display chat history
for msg in st.session_state.messages[1:]:  # Skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
