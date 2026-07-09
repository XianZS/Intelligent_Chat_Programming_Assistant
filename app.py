# streamlit 主程序入口 app.py
import streamlit as st
from src.ui.utils import inject_custom_css
from src.config import get_api_key, validate_config

st.set_page_config(
    page_title="DeepSeek AI 助手 🤖",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 注入自定义 css 样式
inject_custom_css()

# 接收值 >>> (状态，状态描述)
valid, status_msg = validate_config()
# 设置聊天框是否禁用
chat_disabled = not valid

if prompt := st.chat_input(
    "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
    disabled=chat_disabled,
):
    # 接收用户输入
    with st.chat_message("user", avatar="💻"):
        st.markdown(prompt)
if valid:
    st.sidebar.success(status_msg)
else:
    st.sidebar.warning(status_msg)
