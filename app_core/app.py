# ═══ IMPORTS ═══
import os
import sys
import time

# Ensure parent directory (src/) is in sys.path
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

import streamlit as st
from dotenv import load_dotenv

from app_core.memory_handler import MemoryHandler
from app_core.llm_connector import LLMConnector
from ui import GLOBAL_CSS, render_icon_bar, render_sidebar, render_welcome_screen, render_messages, render_telemetry, stream_and_save_response

# ═══ APP CONFIG: Page title, layout, and environment setup ═══
load_dotenv(override=True)
st.set_page_config(page_title="Personal GPT", layout="wide", initial_sidebar_state="expanded")

# ── 1. Session State Init ──────────────────────────────────────────────────────
defaults = {
    "memory_handler": MemoryHandler(),
    "user_id": "alex",
    "workspace": "Default Workspace",
    "provider": "Groq",
    "temperature": 0.7,
    "inject_memories": True,
    "sessions": [],
    "active_session_id": None,
    "retrieved_memories_log": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ── 2. Core Business Logic Helpers ─────────────────────────────────────────────
# ── GET ACTIVE HISTORY: Fetches chat messages of the current session ──
def get_active_history():
    if st.session_state.active_session_id is None:
        return []
    for s in st.session_state.sessions:
        if s["id"] == st.session_state.active_session_id:
            return s["history"]
    return []

# ── SAVE MESSAGE: Appends a message to the session; creates a new session if none exists ──
def save_active_message(role, content):
    if st.session_state.active_session_id is None:
        sid = str(int(time.time()))
        title = " ".join(content.split()[:5]) + ("..." if len(content.split()) > 5 else "")
        st.session_state.active_session_id = sid
        st.session_state.sessions.append({"id": sid, "title": title, "history": [{"role": role, "content": content}]})
    else:
        for s in st.session_state.sessions:
            if s["id"] == st.session_state.active_session_id:
                s["history"].append({"role": role, "content": content})
                break

# ── NAMESPACE UID: Builds a unique user+workspace ID to isolate memories per workspace ──
def get_namespace_uid():
    ws = st.session_state.workspace.lower().replace(" ", "_").replace(".", "")
    return f"{st.session_state.user_id}_{ws}"

# ── 3. Render UI & Layout ──────────────────────────────────────────────────────
active_tab = st.query_params.get("tab", "chat")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
render_icon_bar(active_tab)
render_sidebar(active_tab, get_namespace_uid)

history = get_active_history()
if not history:
    render_welcome_screen()
else:
    render_messages(history)
    render_telemetry()

# ── 4. Response Generation & Chat Input Logic ─────────────────────────────────
if st.session_state.get("pending_query"):
    connector = LLMConnector(provider=st.session_state.provider)
    stream_and_save_response(
        st.session_state.pending_query,
        st.session_state.get("pending_memories", []),
        history,
        connector,
        save_active_message,
        get_namespace_uid,
    )

# ═══ CHAT INPUT: Captures user message, fetches relevant memories, triggers response ═══
if query := st.chat_input("Send a message..."):
    save_active_message("user", query)
    ns_uid = get_namespace_uid()
    retrieved = st.session_state.memory_handler.get_memories(query, user_id=ns_uid) if st.session_state.inject_memories else []
    st.session_state.retrieved_memories_log = retrieved
    st.session_state.pending_query = query
    st.session_state.pending_memories = retrieved
    st.rerun()
