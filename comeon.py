import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="바이브코딩 1기 단톡방 💬", layout="centered")
st.title("💬 바이브코딩 1기 단톡방")

CHAT_FILE = "chat.json"

# 초기 채팅 데이터 불러오기
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(CHAT_FILE, "r", encoding="utf-8") as f:
    chat_history = json.load(f)

# 닉네임 입력
nickname = st.text_input("닉네임을 입력해주세요 ✨", key="nickname_input")

# 메시지 입력
if nickname:
    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input("메시지를 입력하세요 ✍️", key="msg_input")
        submitted = st.form_submit_button("보내기")
        if submitted and message:
            new_msg = {
                "nickname": nickname,
                "message": message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            chat_history.append(new_msg)
            with open(CHAT_FILE, "w", encoding="utf-8") as f:
                json.dump(chat_history, f, ensure_ascii=False, indent=2)

# 채팅 출력
st.subheader("💬 채팅 기록")
for chat in reversed(chat_history[-50:]):  # 최근 50개만 보여줌
    st.markdown(f"**[{chat['timestamp']}] {chat['nickname']}**: {chat['message']}")
