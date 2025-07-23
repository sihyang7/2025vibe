import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="바이브코딩 1기 단톡방 💬", layout="centered")
st.title("💬 바이브코딩 1기 단톡방")

# 🔔 공지
st.warning("⚠️ 새 메시지를 확인하려면 새로고침(F5 또는 Ctrl+R)이 필요해요!", icon="⚠️")

CHAT_FILE = "chat.json"

# 채팅 파일 초기화
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(CHAT_FILE, "r", encoding="utf-8") as f:
    chat_history = json.load(f)

# 닉네임 입력
nickname = st.text_input("닉네임을 입력해주세요 ✨", key="nickname_input")

# 이모지 선택 버튼
emoji_col1, emoji_col2, emoji_col3, emoji_col4 = st.columns(4)
if "emoji_text" not in st.session_state:
    st.session_state.emoji_text = ""

with emoji_col1:
    if st.button("😀"):
        st.session_state.emoji_text += "😀"
with emoji_col2:
    if st.button("😂"):
        st.session_state.emoji_text += "😂"
with emoji_col3:
    if st.button("❤️"):
        st.session_state.emoji_text += "❤️"
with emoji_col4:
    if st.button("🔥"):
        st.session_state.emoji_text += "🔥"

# 메시지 입력
if nickname:
    with st.form("chat_form", clear_on_submit=True):
        message = st.text_input(
            "메시지를 입력하세요 ✍️",
            value=st.session_state.emoji_text,
            key="msg_input"
        )
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
            st.session_state.emoji_text = ""  # 입력창 초기화
            st.experimental_rerun()

# 채팅 출력
st.subheader("💬 채팅 기록")
for chat in reversed(chat_history[-50:]):
    st.markdown(f"**[{chat['timestamp']}] {chat['nickname']}**: {chat['message']}")

