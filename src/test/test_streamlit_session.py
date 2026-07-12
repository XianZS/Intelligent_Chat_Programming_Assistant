import streamlit as st

count_normal = 0

if "count_persistent" not in st.session_state:
    st.session_state.count_persistent = 0

if st.button("+1"):
    # 普通变量
    count_normal += 1
    # 持久变量
    st.session_state.count_persistent += 1

st.write(f"普通变量:{count_normal}")
st.write(f"持久变量:{st.session_state.count_persistent}")
