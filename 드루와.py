import streamlit as st
from datetime import datetime

st.set_page_config(page_title="바이브코딩 1기 단톡방 💬", layout="centered")

st.title("💬 바이브코딩 1기 단톡방")

# 닉네임 설정
if 'nickname' not in st.session_state:
    st.session_state.nickname = st.text_input("닉네임을 입력해주세요 ✨", "")
    st.stop()

# 채팅 기록 저장 공간 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 채팅 입력창
with st.form("chat_form", clear_on_submit=True):
    message = st.text_input("메시지를 입력하세요 ✍️")
    submitted = st.form_submit_button("보내기")
    if submitted and message:
        st.session_state.chat_history.append({
            "nickname": st.session_state.nickname,
            "message": message,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })

# 채팅 출력
st.subheader("💬 채팅 기록")
for chat in reversed(st.session_state.chat_history):
    st.markdown(f"**[{chat['timestamp']}] {chat['nickname']}**: {chat['message']}")

