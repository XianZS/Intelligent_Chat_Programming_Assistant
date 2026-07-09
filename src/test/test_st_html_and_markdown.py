# 理解并学习 markdown 和 html
import streamlit as st

# --- markdown 的基本用法
st.markdown("## 二级标题")
st.markdown("**粗体**")
st.markdown("*斜体*")

# --- HTML 用法
st.markdown(
    "<div style='color:#ff6b6b; font-size: 1.5em;'>红色字体</div>",
    unsafe_allow_html=True,
)

# --- markdown 和 html 混合搭配使用
st.markdown(
    """
            ## Python学习
            Python是一门**解释型**语言
            <div style="background: #333; padding: 10px;">
                python是一门很好使用的语言。
            </div>
            """,
    unsafe_allow_html=True,
)
