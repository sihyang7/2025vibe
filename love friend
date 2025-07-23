import streamlit as st
import random
from datetime import date

# 놀릴 멘트 템플릿
MENT_TEMPLATES = {
    "귀엽게": [
        "{name}이는 왜 이렇게 귀엽고 멍청해~ 햇살 맞고 자란 감자같이 생겼네~ 🍠",
        "오늘도 {name}이는 뇌 대신 솜사탕을 넣고 다니는구나~ ☁️",
    ],
    "약올리게": [
        "{name}, 너는 멍청이 대회 나가면 대상 받을 듯. 안 나가도 줘야 할 정도야.",
        "진심으로 {name}을 보면 뇌세포가 도망갈 것 같아.",
    ],
    "진지하게 장난": [
        "{name}, 넌 진짜 천재야. 멍청한 쪽으로는.",
        "{name}, 네 아이큐는 방 온도랑 친구하더라. 겨울 기준으로.",
    ],
    "시처럼": [
        "이름하여 {name}, 고요한 아침의 나라에서… 제일 시끄러운 존재여라…",
        "{name}이여, 그대는 마치… 종이컵에 담긴 철학 같도다. 약하고 쓸모 없다.",
    ],
}

# 앱 UI
st.title("🎯 오늘의 친구 놀리기")

name = st.text_input("👤 친구 이름을 입력하세요", value="인영이")
style = st.selectbox("놀릴 스타일을 골라봐요", list(MENT_TEMPLATES.keys()))
generate = st.button("🎲 놀릴 멘트 생성하기")

if generate:
    # 날짜 기반으로 고정 놀림말 생성 (매일 바뀜)
    today = date.today().isoformat()
    random.seed(today + name + style)
    ment = random.choice(MENT_TEMPLATES[style])
    ment_filled = ment.format(name=name)

    st.success("오늘의 놀림 멘트 🎉")
    st.markdown(f"**🗯️ {ment_filled}**")
    st.code(ment_filled, language="text")
    st.button("📋 복사하기", on_click=st.toast, args=("클립보드 복사 기능은 브라우저에서 지원돼요! 😊",))
