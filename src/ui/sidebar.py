import streamlit as st
from ..config import (
    get_api_key,
    set_api_key,
    validate_config,
)


def render() -> dict:
    st.sidebar.markdown("## ⚙  设置")
    st.sidebar.markdown("### 🔑 API 密钥")
    env_key = get_api_key()
    valid, status_msg = validate_config()
    if valid:
        st.sidebar.success(status_msg)
    else:
        st.sidebar.warning(status_msg)
    api_key_input = st.sidebar.text_input(
        "DeepSeek API Key",
        type="password",
        value=env_key or "",
        placeholder="sk-...",
        help="输入你的 DeepSeek API 密钥。可在 platform.deepseek.com/api_keys 获取",
    )
    if api_key_input and api_key_input != env_key:
        set_api_key(api_key_input)
    else:
        pass
    st.sidebar.markdown("---")
    return {
        "api_key": api_key_input,
    }
