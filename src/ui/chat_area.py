import streamlit as st
from typing import Optional
from ..chat_manager import get_all_message


def render_message(
    role: str,
    content: str,
    reasoning_content: Optional[str] = None,
) -> None:
    if role == "user":
        avatar = "👨‍💻"
    else:
        avatar = "🤖"
    with st.chat_message(role, avatar=avatar):
        if reasoning_content and role == "assistant":
            with st.expander("🧠 查看思考过程", expanded=False):
                st.markdown(
                    f"<div style='color:#888;font-size:0.9em;line-height:1.6;'>{reasoning_content}<div>",
                    unsafe_allow_html=True,
                )
        st.markdown(content)


def render_all_message():
    # 渲染全部的历史消息
    message = get_all_message()
    for msg in message:  # type:ignore
        role = msg.get("role", "user")
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content")
        render_message(role, content, reasoning)


def render_welcome():
    # 渲染欢迎界面
    st.markdown(
        """
            <div style='text-align:center;padding:40px 20px;'>
                <h1 style="font-size: 2.5em;margin-bottom:10px;">
                    🤖 DeepSeek AI 聊天助手
                </h1>
                <p style='color=#888,font-size:1.1em;margin-bottom:30px'>
                    基于 DeepSeek V4 大模型，支持流式对话与思维链路推理
                </p>
            </div>
            """,
        unsafe_allow_html=True,
    )
    st.markdown("#### 💡 试试这些：")
    # 设计3个提示词卡片
    cols = st.columns(3)
    suggestions = [
        ("✍", "帮我写一段Python代码", "用 Python 实现一个简单的 HTTP 服务器"),
        ("🔍", "解释概念", "请通俗易懂地解释什么是机器学习"),
        ("💡", "头脑风暴", "我想做一个个人博客网站，给我一些技术选型建议"),
    ]
    for i, (icon, title, desc) in enumerate(suggestions):
        with cols[i]:
            st.markdown(
                f"""
                    <div style='
                        border: 1px solid #333;
                        border-radius:10px;
                        padding:15px;
                        height:100%;
                        cursor:pointer;
                    '>
                        <div style='font-size:1.5em;'>
                            {icon}
                        </div>
                        <div style='font-weight:bold;margin:8px 0;'>
                            {title}
                        </div>
                        <div style='color:#888;font-size:0.85em;'>
                            {desc}
                        </div>
                    </div>
                    """,
                unsafe_allow_html=True,
            )
