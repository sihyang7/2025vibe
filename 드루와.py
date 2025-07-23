import streamlit as st
import json
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="바이브코딩 1기 단톡방 💬", layout="centered")
st.title("💬 바이브코딩 1기 단톡방")

CHAT_FILE = "chat.json"

# 1️⃣ 입력 중 여부를 저장할 상태 변수
if "typing" not in st.session_state:
    st.session_state.typing = False

# 2️⃣ 자동 새로고침: 입력 중이 아니면 1초마다 새로고침
if not st.session_state.typing:
    st_autorefresh(interval=1000, key="auto_refresh")

# 3️⃣ 채팅 파일 없으면 생성
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(CHAT_FILE, "r", encoding="utf-8") as f:
    chat_history = json.load(f)

# 4️⃣ 닉네임 입력
nickname = st.text_input("닉네임을 입력해주세요 ✨", key="nickname_input")

# 5️⃣ 메시지 입력
if nickname:
    def on_typing():
        st.session_state.typing = True

    def on_send():
        st.session_state.typing = False

    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("메시지를 입력하세요 ✍️", key="msg_input", on_change=on_typing)
        submitted = st.form_submit_button("보내기", on_click=on_send)
        if submitted and message:
            new_msg = {
                "nickname": nickname,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            chat_history.append(new_msg)
            with open(CHAT_FILE, "w", encoding="utf-8") as f:
                json.dump(chat_history, f, ensure_ascii=False, indent=2)

# 6️⃣ 채팅 출력
st.subheader("💬 채팅 기록")
for chat in reversed(chat_history[-50:]):
    st.markdown(f"**[{chat['timestamp']}] {chat['nickname']}**: {chat['message']}")
