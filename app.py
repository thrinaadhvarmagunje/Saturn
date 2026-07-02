import streamlit as st
import time
from chatbot import get_response

# ============================
# PAGE CONFIG
# ============================

st.set_page_config(
    page_title="Saturn AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# LOAD CSS
# ============================

def load_css():

    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>",
                    unsafe_allow_html=True)

load_css()

# ============================
# SESSION STATE
# ============================

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "theme" not in st.session_state:
    st.session_state.theme="Dark"

# ============================
# SIDEBAR
# ============================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
        Saturn AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 💡 About")

    st.info(
        """
Powered by

Gemini 2.5 Flash

LangGraph

Streamlit

Designed by Thrinaadh Varma
"""
    )

    st.markdown("---")

    if st.button(" Clear Chat"):

        st.session_state.messages=[]

        st.rerun()

    st.markdown("---")

    st.markdown("### ⚙ Settings")

    st.selectbox(

        "Theme",

        [

            "Dark",
            "Light"

        ],

        key="theme"

    )

    st.markdown("---")

    st.markdown("### 📊 Statistics")

    total=len(st.session_state.messages)

    users=len(
        [i for i in st.session_state.messages
         if i["role"]=="user"]
    )

    bots=len(
        [i for i in st.session_state.messages
         if i["role"]=="assistant"]
    )

    st.metric("Messages",total)

    st.metric("Questions",users)

    st.metric("Responses",bots)

    st.markdown("---")

    st.success("🟢 Online")

# ============================
# HEADER
# ============================

st.markdown(
"""
<div class="title">
Saturn AI Assistant
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Powered by Gemini 2.5 Flash • LangGraph • Streamlit
</div>
""",
unsafe_allow_html=True
)

st.write("")

# ============================
# CHAT HISTORY
# ============================

for message in st.session_state.messages:

    avatar="🤖"

    if message["role"]=="user":
        avatar="👨‍💻"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(message["content"])

# ============================
# USER INPUT
# ============================

prompt=st.chat_input(
    "Ask me anything..."
)

if prompt:

    st.session_state.messages.append(

        {

            "role":"user",

            "content":prompt

        }

    )

    with st.chat_message(

        "user",

        avatar="👨‍💻"

    ):

        st.markdown(prompt)

    with st.chat_message(

        "assistant",

        avatar="🤖"

    ):

        typing=st.empty()

        response_placeholder=st.empty()

        typing.markdown(
            """
<div class='typing'>
Thinking...
</div>
""",
            unsafe_allow_html=True
        )

        response=get_response(prompt)

        typing.empty()

        streamed=""

        for word in response.split():

            streamed+=word+" "

            response_placeholder.markdown(
                streamed+"▌"
            )

            time.sleep(0.03)

        response_placeholder.markdown(streamed)

        st.session_state.messages.append(

            {

                "role":"assistant",

                "content":response

            }

        )
st.markdown(
"""
<div class='footer'>
Made with ❤️ by Thrinaadh Varma using Gemini 2.5 Flash
</div>
""",
unsafe_allow_html=True
)
