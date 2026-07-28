import streamlit as st
from ui.styles import HUMAN_AVATAR, ROBOT_AVATAR, WELCOME_SCREEN_HTML

def render_welcome_screen():
    st.markdown(WELCOME_SCREEN_HTML, unsafe_allow_html=True)

def _bubble_html(role: str, content: str) -> str:
    """Renders a single chat bubble as custom HTML."""
    is_user = role == "user"
    avatar   = HUMAN_AVATAR if is_user else ROBOT_AVATAR
    direction = "row-reverse" if is_user else "row"
    bubble_bg     = "rgba(56,189,248,0.15)"     if is_user else "rgba(22,25,43,0.75)"
    bubble_border = "1px solid rgba(56,189,248,0.35)" if is_user else "1px solid #252940"
    bubble_radius = "18px 4px 18px 18px"        if is_user else "4px 18px 18px 18px"
    margin        = "margin-left:auto; margin-right:0;" if is_user else "margin-right:auto; margin-left:0;"
    # Escape HTML entities in content
    safe = content.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")
    return f"""
<div style="display:flex; flex-direction:{direction}; align-items:flex-start; gap:10px; padding:6px 0;">
    <img src="{avatar}" width="36" height="36"
         style="border-radius:50%; border:1.5px solid #444; background:#fff; flex-shrink:0;"/>
    <div style="{margin} max-width:75%; background:{bubble_bg};
                border:{bubble_border}; border-radius:{bubble_radius};
                padding:10px 14px; color:#e2e8f0; font-size:14.5px; line-height:1.65;">
        {safe}
    </div>
</div>"""

def render_messages(history):
    """Renders all chat history as styled HTML bubbles."""
    html_blocks = "".join(_bubble_html(m["role"], m["content"]) for m in history)
    st.markdown(html_blocks, unsafe_allow_html=True)

def render_telemetry():
    if st.session_state.retrieved_memories_log:
        with st.expander("Recalled Memory Context", expanded=False):
            for fact in st.session_state.retrieved_memories_log:
                st.caption(f"• {fact}")
