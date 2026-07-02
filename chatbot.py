from google import genai
import streamlit as st
from typing import Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

# =====================================================
# Gemini Configuration
# =====================================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL_NAME = "gemini-2.5-flash"

# =====================================================
# Session State
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# Gemini Chat Function
# =====================================================

def ask_gemini(prompt: str):

    try:

        conversation = []

        # Use last 10 messages for context
        for msg in st.session_state.messages[-10:]:

            if msg["role"] == "user":

                conversation.append({
                    "role": "user",
                    "parts": [{"text": msg["content"]}]
                })

            else:

                conversation.append({
                    "role": "model",
                    "parts": [{"text": msg["content"]}]
                })

        # Current Prompt
        conversation.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation
        )

        return response.text

    except Exception as e:

        return f"❌ Error : {e}"

# =====================================================
# LangGraph State
# =====================================================

class GraphState(TypedDict):

    question: Optional[str]
    classification: Optional[str]
    response: Optional[str]

# =====================================================
# Greeting Detection
# =====================================================

def classify(state):

    question = state["question"].lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "good night"
    ]

    if question in greetings:
        category = "greeting"
    else:
        category = "gemini"

    return {
        **state,
        "classification": category
    }

# =====================================================
# Response Node
# =====================================================

def respond(state):

    question = state["question"]

    if state["classification"] == "greeting":

        answer = """
👋 Hello!

I'm your Saturn AI Assistant.

I can help you with:

• Programming
• Python
• SQL
• Machine Learning
• Data Science
• Interview Preparation
• Code Debugging
• General Knowledge

How can I help you today?
"""

    else:

        answer = ask_gemini(question)

    return {
        **state,
        "response": answer
    }

# =====================================================
# Build LangGraph
# =====================================================

builder = StateGraph(GraphState)

builder.add_node("classify", classify)
builder.add_node("respond", respond)

builder.set_entry_point("classify")
builder.add_edge("classify", "respond")
builder.set_finish_point("respond")

app = builder.compile()

# =====================================================
# Wrapper Function
# =====================================================

def get_response(prompt):

    result = app.invoke({
        "question": prompt
    })

    return result["response"]
