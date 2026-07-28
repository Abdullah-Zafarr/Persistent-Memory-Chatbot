"""
UI package for Personal GPT.
"""
from ui.styles import GLOBAL_CSS
from ui.navigation import render_icon_bar
from ui.sidebar import render_sidebar
from ui.chat import render_welcome_screen, render_messages, render_telemetry, ROBOT_AVATAR
from ui.stream_handler import stream_and_save_response

__all__ = [
    "GLOBAL_CSS",
    "render_icon_bar",
    "render_sidebar",
    "render_welcome_screen",
    "render_messages",
    "render_telemetry",
    "ROBOT_AVATAR",
    "stream_and_save_response",
]
