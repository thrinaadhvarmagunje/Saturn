import streamlit as st
import time
from chatbot import get_response

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Saturn AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# LOAD CSS
# =====================================================

def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

load_css()

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            🤖 Saturn AI
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### 💡 About")

    st.info(
        """
Powered by

✅ Gemini 2.5 Flash

✅ LangGraph

✅ Streamlit

Designed by Thrinaadh Varma
"""
    )

    st.markdown("---")

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("### ⚙ Settings")

    st.selectbox(
        "Theme",
        ["Dark", "Light"],
        key="theme",
    )

    st.markdown("---")

    total = len(st.session_state.messages)

    users = len(
        [
            m
            for m in st.session_state.messages
            if m["role"] == "user"
        ]
    )

    bots = len(
        [
            m
            for m in st.session_state.messages
            if m["role"] == "assistant"
        ]
    )

    st.metric("Messages", total)
    st.metric("Questions", users)
    st.metric("Responses", bots)

    st.markdown("---")

    st.success("🟢 Online")
    # =====================================================
# HERO SECTION
# =====================================================

st.markdown(
    """
    <div class="hero-card">

        <div class="hero-title">
            🤖 Saturn AI Assistant
        </div>

        <div class="hero-subtitle">
            Powered by Gemini 2.5 Flash • LangGraph • Streamlit
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# CHAT HISTORY
# =====================================================

chat_container = st.container()

with chat_container:

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message(
                "user",
                avatar="👨‍💻"
            ):

                st.markdown(message["content"])

        else:

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):

                st.markdown(message["content"])
st.markdown(
"""
<div class="footer">

Made with ❤️ by <b>Thrinaadh Varma</b>

</div>
""",
unsafe_allow_html=True
)
