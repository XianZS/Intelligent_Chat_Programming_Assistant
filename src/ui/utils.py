import streamlit as st


def inject_custom_css() -> None:
    # 注入自定义 css 样式
    st.markdown(
        """
            <style>
                footer { display: none; }
                .block-container{
                    padding-top: 2rem;
                }
                .streamlit-expanderHeader {
                    font-size: 0.9em;
                    color: #888;
                }
                [data-testid="stSidebar"] [data-testid="stTextInput"] input{
                    font-family: monospace;
                }
                .stChatMessage {
                    padding: 0.5rem 1rem;
                }
                [data-testid="stMarkdownContainer"]
                div[style*="cursor: pointer"]:hover {
                    border-color: #4a9eff !important;
                    transition: border-color 0.3s;
                }
            </style>
            """,
        unsafe_allow_html=True,
    )
