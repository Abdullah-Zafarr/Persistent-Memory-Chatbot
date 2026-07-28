import os

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

def _load_asset(filename: str) -> str:
    path = os.path.join(ASSETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()

import base64

HUMAN_SVG = _load_asset("human.svg")
ROBOT_SVG = _load_asset("robot.svg")
LOGO_SVG  = _load_asset("logo.svg")

human_b64 = base64.b64encode(HUMAN_SVG.encode("utf-8")).decode("utf-8")
robot_b64 = base64.b64encode(ROBOT_SVG.encode("utf-8")).decode("utf-8")

HUMAN_AVATAR = f"data:image/svg+xml;base64,{human_b64}"
ROBOT_AVATAR = f"data:image/svg+xml;base64,{robot_b64}"

WELCOME_SCREEN_HTML = f"""
<div class="welcome-screen">
    {LOGO_SVG}
    <h2 style="letter-spacing: 0.5px; font-size: 24px; margin-top: 8px;">Personal GPT</h2>
    <p>Your AI with long-term memory. Start a conversation below.</p>
</div>
"""

GLOBAL_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0e0f12 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #d1d5db !important;
    }
    #MainMenu, footer, header { visibility: hidden !important; }
    div.block-container { padding-top: 0 !important; }

    .stBottom, .stBottom > div, .stBottom > div > div,
    [data-testid="stBottom"], [data-testid="stBottomBlockContainer"],
    .stChatInputContainer, [data-testid="stChatInputContainer"] {
        background-color: #0e0f12 !important;
        border-color: #1e2130 !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #13151c !important;
        background-image: 
            repeating-linear-gradient(
                45deg,
                rgba(255, 255, 255, 0.015) 0px,
                rgba(255, 255, 255, 0.015) 2px,
                transparent 2px,
                transparent 14px
            ) !important;
        border-right: 1px solid #1e2130 !important;
        margin-left: 60px !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 20px !important;
    }
    div[data-testid="stSidebarUserContent"] {
        padding: 0 12px !important;
    }

    .stMain, section.stMain, .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0e0f12 !important;
        background-image: 
            repeating-linear-gradient(
                -45deg,
                rgba(255, 255, 255, 0.02) 0px,
                rgba(255, 255, 255, 0.02) 2px,
                transparent 2px,
                transparent 16px
            ),
            radial-gradient(circle at 50% 0%, rgba(37, 41, 64, 0.3) 0%, transparent 70%) !important;
        background-attachment: fixed !important;
    }
    .stMainBlockContainer {
        padding: 24px 48px !important;
        max-width: 860px !important;
        margin: 0 auto !important;
    }

    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 8px 0 !important;
    }
    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] {
        display: flex !important;
        background-color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 50% !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4) !important;
        overflow: hidden !important;
    }
    [data-testid="stChatMessage"] [data-testid="stChatMessageAvatar"] img {
        background-color: #ffffff !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        background-color: rgba(22, 25, 43, 0.6) !important;
        border: 1px solid #252940 !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {
        font-size: 15px !important;
        line-height: 1.65 !important;
        color: #e2e8f0 !important;
        margin: 0 !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-baseweb="textarea"],
    [data-baseweb="base-input"] {
        background-color: transparent !important;
        background-image: none !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        color: #e2e8f0 !important;
        font-size: 15px !important;
        outline: none !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"] textarea:focus,
    [data-baseweb="textarea"]:focus-within {
        border-color: rgba(255, 255, 255, 0.2) !important;
        box-shadow: none !important;
    }
    [data-testid="stChatInput"],
    [data-testid="stChatInputContainer"],
    .stChatFloatingInputContainer,
    .stBottom,
    .stBottom > div {
        background-color: transparent !important;
        background-image: 
            repeating-linear-gradient(
                -45deg,
                rgba(255, 255, 255, 0.02) 0px,
                rgba(255, 255, 255, 0.02) 2px,
                transparent 2px,
                transparent 16px
            ) !important;
        border-top: 1px solid #1e2130 !important;
    }

    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #1a1d2e !important;
        border: 1px solid #252940 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-size: 13px !important;
    }
    section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
        background-color: #1a1d2e !important;
        border: 1px solid #252940 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] label {
        color: #64748b !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    section[data-testid="stSidebar"] button {
        background-color: #1a1d2e !important;
        border: 1px solid #252940 !important;
        color: #d1d5db !important;
        border-radius: 8px !important;
        font-size: 13px !important;
        transition: all 0.15s ease !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background-color: #252940 !important;
        color: #f8fafc !important;
        border-color: #374163 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #1e2130 !important;
        margin: 12px 0 !important;
    }

    .session-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 7px 10px;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.15s;
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 2px;
    }
    .session-item:hover { background-color: #1a1d2e; color: #e2e8f0; }
    .session-item.active { background-color: #1e2438; color: #f8fafc; font-weight: 500; }

    .welcome-screen {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 80px 0 40px;
        color: #4b5563;
        text-align: center;
    }
    .welcome-screen h2 {
        font-size: 26px;
        font-weight: 600;
        color: #9ca3af;
        margin: 16px 0 8px;
        letter-spacing: -0.3px;
    }
    .welcome-screen p {
        font-size: 14px;
        color: #4b5563;
    }
</style>
"""
