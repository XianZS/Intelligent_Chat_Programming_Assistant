# streamlit 主程序入口 app.py
import streamlit as st
from src.ui.utils import inject_custom_css
from src.config import get_api_key, set_api_key, validate_config
from src.ui.chat_area import render_all_message, render_welcome
from src.chat_manager import init_message, get_message_count
from src.ui.sidebar import render as render_sidebar

st.set_page_config(
    page_title="DeepSeek AI 助手 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    init_message()
    if get_message_count() == 0:
        render_welcome()
    else:
        render_all_message()
    settings = render_sidebar()
    api_key = settings["api_key"] or get_api_key()


if __name__ == "__main__":
    main()
