from google import genai
import streamlit as st
from typing import Optional
from typing_extensions import TypedDict
from langgraph.graph import StateGraph

# ======================================================
# Configure Gemini Client
# ======================================================

client = genai.Client(
    api_key="AQ.Ab8RN6LJiJp-Y5E3x_ROwo05sCpsiAZZlhQIwAHMO_ER0jy1JQ"
)

MODEL_NAME = "gemini-2.5-flash"

# ======================================================
# Chat History Memory
# ======================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ======================================================
# Gemini Response Function
# ======================================================

def ask_gemini(prompt: str):

    try:

        conversation = []

        # Last 10 messages for context
        for msg in st.session_state.history[-10:]:

            if msg["role"] == "user":
                conversation.append(
                    {
                        "role": "user",
                        "parts": [{"text": msg["content"]}]
                    }
                )

            else:
                conversation.append(
                    {
                        "role": "model",
                        "parts": [{"text": msg["content"]}]
                    }
                )

        conversation.append(
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=conversation
        )

        return response.text

    except Exception as e:

        return f"❌ Error : {str(e)}"


# ======================================================
# LangGraph State
# ======================================================

class GraphState(TypedDict):

    question: Optional[str]
    classification: Optional[str]
    response: Optional[str]


# ======================================================
# Greeting Detection
# ======================================================

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


# ======================================================
# Response Node
# ======================================================

def respond(state):

    question = state["question"]

    if state["classification"] == "greeting":

        answer = """
👋 Hello!

I'm your Gemini AI Assistant.

I can help you with:

• Programming
• Machine Learning
• SQL
• Data Science
• Interview Preparation
• General Questions
• Code Debugging

How can I assist you today?
"""

    else:

        answer = ask_gemini(question)

    return {

        **state,

        "response": answer

    }


# ======================================================
# Build LangGraph
# ======================================================

builder = StateGraph(GraphState)

builder.add_node("classify", classify)

builder.add_node("respond", respond)

builder.set_entry_point("classify")

builder.add_edge("classify", "respond")

builder.set_finish_point("respond")

app = builder.compile()


# ======================================================
# Wrapper Function
# ======================================================

def get_response(prompt):

    result = app.invoke(

        {
            "question": prompt
        }

    )

    return result["response"]
