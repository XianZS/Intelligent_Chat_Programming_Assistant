import streamlit as st
from typing import Optional
from .config import CHARS_PER_TOKEN, TOKEN_WARNING_THRESHOLD


def get_all_message() -> list[dict]:
    # 返回所有的历史对话内容
    init_message()
    return st.session_state.message


def init_message():
    # 消息列表初始化函数
    if "message" not in st.session_state:
        st.session_state.message = []
    else:
        pass


def get_message_count() -> int:
    # 获取当前的消息数
    init_message()
    return len(st.session_state.message)


def add_user_message(text: str) -> None:
    # 添加用户消息到历史对话列表之中
    init_message()
    st.session_state.message.append(
        {
            "role": "user",
            "content": text,
        }
    )


def add_assistant_message(
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    # 添加助手消息到历史对话消息列表之中
    init_message()
    st.session_state.message.append(
        {
            "role": "assistant",
            "content": content,
            "reasoning_content": reasoning_content,
        }
    )


def clear_history() -> None:
    init_message()
    st.session_state.message = []


# === API 消息构建
def build_api_message() -> list[dict[str, str]]:
    # 构建发送给 DeepSeek API 的消息列表
    init_message()
    api_message = []
    for message in st.session_state.message:
        clean_message = {
            "role": message["role"],
            "content": message["content"],
        }
        api_message.append(clean_message)
    return api_message


def estimate_token_count() -> int:
    init_message()
    total_chars = 0
    for message in st.session_state.message:
        total_chars += len(message.get("content", ""))
        if message.get("reasoning_content"):
            total_chars += len(message.get("reasoning_content"))
    return total_chars // CHARS_PER_TOKEN


def should_warn_token_limit() -> bool:
    return estimate_token_count() >= TOKEN_WARNING_THRESHOLD
