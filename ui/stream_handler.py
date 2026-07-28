import streamlit as st
import threading
from ui.styles import ROBOT_AVATAR
from ui.chat import _bubble_html

def stream_and_save_response(pending, memories, history, connector, save_active_message_fn, get_namespace_uid_fn):
    # Stream live into a placeholder, then save and rerun (history rerender styles it)
    ph = st.empty()
    full_resp = ""
    try:
        for chunk in connector.generate_response_stream(
            prompt=pending,
            chat_history=history[:-1],
            memories=memories,
            temperature=st.session_state.temperature,
        ):
            full_resp += chunk
            ph.markdown(_bubble_html("assistant", full_resp + " ▌"), unsafe_allow_html=True)
        ph.markdown(_bubble_html("assistant", full_resp), unsafe_allow_html=True)
    except Exception as ex:
        full_resp = f"Error: {ex}"
        ph.error(full_resp)

    save_active_message_fn("assistant", full_resp)

    def _add_mem(handler, q, uid):
        try:
            handler.add_memory(q, user_id=uid)
        except Exception as e:
            print(f"Memory save error: {e}")

    threading.Thread(
        target=_add_mem,
        args=(st.session_state.memory_handler, pending, get_namespace_uid_fn()),
        daemon=True,
    ).start()

    st.session_state.pending_query = None
    st.session_state.pending_memories = None
    st.rerun()
