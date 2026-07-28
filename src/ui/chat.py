import streamlit as st
from ui.styles import HUMAN_AVATAR, ROBOT_AVATAR, WELCOME_SCREEN_HTML

def render_welcome_screen():
    """
    Renders the empty state welcome screen with LLM logo.
    """
    st.markdown(WELCOME_SCREEN_HTML, unsafe_allow_html=True)

def render_messages(history):
    """
    Renders conversation message history using custom avatars.
    """
    for msg in history:
        avatar_img = HUMAN_AVATAR if msg["role"] == "user" else ROBOT_AVATAR
        with st.chat_message(msg["role"], avatar=avatar_img):
            st.markdown(msg["content"])

def render_telemetry():
    """
    Renders recalled memories expander if memories log is present.
    """
    if st.session_state.retrieved_memories_log:
        with st.expander(" Recalled Memory Context", expanded=False):
            for fact in st.session_state.retrieved_memories_log:
                st.caption(f"• {fact}")
