import streamlit as st

def render_sidebar(active_tab: str, get_namespace_uid_fn):
    """
    Renders secondary sidebar controls depending on active tab.
    """
    with st.sidebar:
        # Workspace selector at top
        ws_options = ["Default Workspace", "Dev Environment", "Personal Notes"]
        ws_idx = ws_options.index(st.session_state.workspace) if st.session_state.workspace in ws_options else 0
        ws = st.selectbox("Workspace", ws_options, index=ws_idx, label_visibility="collapsed")
        if ws != st.session_state.workspace:
            st.session_state.workspace = ws
            st.session_state.retrieved_memories_log = []
            st.rerun()

        st.divider()

        # ── CHAT TAB ──
        if active_tab == "chat":
            if st.button("＋ New Chat", use_container_width=True):
                st.session_state.active_session_id = None
                st.session_state.retrieved_memories_log = []
                st.rerun()

            search = st.text_input("Search", placeholder="Search chats...", label_visibility="collapsed")
            st.divider()

            filtered = [
                s for s in st.session_state.sessions
                if not search or search.lower() in s["title"].lower()
            ]
            if filtered:
                st.caption("HISTORY")
                for s in filtered:
                    is_active = s["id"] == st.session_state.active_session_id
                    c1, c2 = st.columns([9, 1])
                    with c1:
                        btn_label = ("▸ " if is_active else "") + s["title"]
                        if st.button(btn_label, key=f"s_{s['id']}", use_container_width=True):
                            st.session_state.active_session_id = s["id"]
                            st.session_state.retrieved_memories_log = []
                            st.rerun()
                    with c2:
                        if st.button("×", key=f"d_{s['id']}"):
                            st.session_state.sessions = [x for x in st.session_state.sessions if x["id"] != s["id"]]
                            if st.session_state.active_session_id == s["id"]:
                                st.session_state.active_session_id = None
                            st.rerun()
            else:
                st.caption("No chats yet.")

        # ── MEMORIES TAB ──
        elif active_tab == "memories":
            st.caption("STORED MEMORIES")
            uid_input = st.text_input("User ID", value=st.session_state.user_id)
            if uid_input != st.session_state.user_id:
                st.session_state.user_id = uid_input
                st.session_state.retrieved_memories_log = []
                st.rerun()

            st.divider()
            ns_uid = get_namespace_uid_fn()
            all_mems = st.session_state.memory_handler.get_all_memories(ns_uid)
            if all_mems:
                st.caption(f"{len(all_mems)} facts stored")
                for idx, m in enumerate(all_mems):
                    c1, c2 = st.columns([8, 2], vertical_alignment="center")
                    with c1:
                        st.write(f"• {m['memory']}")
                    with c2:
                        if st.button("×", key=f"dm_{m['id']}_{idx}"):
                            st.session_state.memory_handler.delete_memory(m['id'])
                            st.rerun()
            else:
                st.caption("No memories yet. Chat to build memory.")

            st.divider()
            if st.button("Clear All Memories", use_container_width=True):
                st.session_state.memory_handler.clear_all(ns_uid)
                st.session_state.retrieved_memories_log = []
                st.rerun()

        # ── CONFIG TAB ──
        elif active_tab == "config":
            st.caption("LLM PROVIDER")
            prov_options = ["Groq", "Gemini", "OpenAI"]
            prov_idx = prov_options.index(st.session_state.provider) if st.session_state.provider in prov_options else 0
            prov = st.selectbox("Provider", prov_options, index=prov_idx)
            if prov != st.session_state.provider:
                st.session_state.provider = prov
                st.rerun()

            st.divider()
            st.caption("GENERATION")
            st.session_state.temperature = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.05)
            st.session_state.inject_memories = st.toggle("Inject Memories into Prompt", value=st.session_state.inject_memories)

        # ── FILES TAB ──
        elif active_tab == "files":
            st.caption("INDEX DOCUMENTS")
            st.write("Upload a text file to extract and store facts into long-term memory.")
            uploaded = st.file_uploader("Upload TXT or MD", type=["txt", "md"], label_visibility="collapsed")
            if uploaded:
                content = uploaded.read().decode("utf-8")
                st.caption(f"{len(content)} characters")
                if st.button("Parse & Remember", use_container_width=True):
                    st.session_state.memory_handler.add_memory(
                        f"Document '{uploaded.name}': {content}",
                        user_id=get_namespace_uid_fn()
                    )
                    st.success(f"'{uploaded.name}' memorized!")
