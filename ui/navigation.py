import streamlit as st

def render_icon_bar(active_tab: str):
    """
    Renders the fixed-position 60px left icon navigation bar.
    Injected directly into the parent window DOM so it remains immune to Streamlit reruns.
    """
    chat_active = "#38bdf8" if active_tab == "chat" else "#4b5563"
    mem_active  = "#38bdf8" if active_tab == "memories" else "#4b5563"
    cfg_active  = "#38bdf8" if active_tab == "config" else "#4b5563"
    file_active = "#38bdf8" if active_tab == "files" else "#4b5563"

    chat_bg = "#1e2638" if active_tab == "chat" else "transparent"
    mem_bg  = "#1e2638" if active_tab == "memories" else "transparent"
    cfg_bg  = "#1e2638" if active_tab == "config" else "transparent"
    file_bg = "#1e2638" if active_tab == "files" else "transparent"

    st.components.v1.html(f"""
    <script>
    (function() {{
        if (window.parent.document.getElementById('pgpt-icon-bar')) return;

        const bar = window.parent.document.createElement('div');
        bar.id = 'pgpt-icon-bar';
        bar.style.cssText = `
            position: fixed;
            left: 0; top: 0; bottom: 0;
            width: 60px;
            background: #0d0e14;
            border-right: 1px solid #1e2130;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px 0;
            gap: 8px;
            z-index: 999999;
        `;

        const icons = [
            {{
                href: '?tab=chat',
                color: '{chat_active}',
                bg: '{chat_bg}',
                title: 'Chats',
                svg: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
            }},
            {{
                href: '?tab=memories',
                color: '{mem_active}',
                bg: '{mem_bg}',
                title: 'Memories',
                svg: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/></svg>'
            }},
            {{
                href: '?tab=config',
                color: '{cfg_active}',
                bg: '{cfg_bg}',
                title: 'Config',
                svg: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="21" x2="14" y1="4" y2="4"/><line x1="10" x2="3" y1="4" y2="4"/><line x1="21" x2="12" y1="12" y2="12"/><line x1="8" x2="3" y1="12" y2="12"/><line x1="21" x2="16" y1="20" y2="20"/><line x1="12" x2="3" y1="20" y2="20"/><line x1="14" x2="14" y1="2" y2="6"/><line x1="8" x2="8" y1="10" y2="14"/><line x1="12" x2="12" y1="18" y2="22"/></svg>'
            }},
            {{
                href: '?tab=files',
                color: '{file_active}',
                bg: '{file_bg}',
                title: 'Files',
                svg: '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg>'
            }}
        ];

        icons.forEach(icon => {{
            const a = window.parent.document.createElement('a');
            a.href = icon.href;
            a.title = icon.title;
            a.style.cssText = `
                display: flex;
                align-items: center;
                justify-content: center;
                width: 40px; height: 40px;
                border-radius: 10px;
                color: ${{icon.color}};
                background: ${{icon.bg}};
                text-decoration: none;
                transition: all 0.15s ease;
            `;
            a.innerHTML = icon.svg;
            a.onmouseenter = () => {{
                if (a.style.background === 'transparent') {{
                    a.style.background = '#1a1d2e';
                    a.style.color = '#e2e8f0';
                }}
            }};
            a.onmouseleave = () => {{
                a.style.background = icon.bg;
                a.style.color = icon.color;
            }};
            bar.appendChild(a);
        }});

        window.parent.document.body.appendChild(bar);

        // Parent DOM override styles & observer for live patching
        const style = window.parent.document.createElement('style');
        style.id = 'pgpt-override-styles';
        style.textContent = `
            [data-testid="stChatInputContainer"],
            [data-testid="stChatInput"] {{
                border: none !important;
                box-shadow: none !important;
                background: transparent !important;
            }}
            [data-testid="stChatInput"] textarea {{
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                outline: none !important;
                color: #e2e8f0 !important;
            }}
        `;
        if (!window.parent.document.getElementById('pgpt-override-styles')) {{
            window.parent.document.head.appendChild(style);
        }}
        function patchChatInput() {{
            const container = window.parent.document.querySelector('[data-testid="stChatInputContainer"], [data-testid="stChatInput"]');
            if (container) {{
                container.style.border = 'none';
                container.style.boxShadow = 'none';
                container.style.backgroundColor = 'transparent';
            }}
            const textareas = window.parent.document.querySelectorAll('[data-testid="stChatInput"] textarea');
            textareas.forEach(ta => {{
                ta.style.border = 'none';
                ta.style.outline = 'none';
                ta.style.backgroundColor = 'transparent';
            }});
        }}
        patchChatInput();
        new window.parent.MutationObserver(patchChatInput).observe(
            window.parent.document.body, {{subtree: true, childList: true}}
        );
    }})();
    </script>
    """, height=0)
