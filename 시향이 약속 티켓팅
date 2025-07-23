import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="시향이와 놀기 예약", page_icon="🎀")

st.title("🎀 시향이와 놀기 예약하기")
st.write("시향이와 놀고 싶다면 여기에 약속을 남겨주세요!")

# 날짜 선택
date = st.date_input("📅 언제 놀고 싶나요?", min_value=datetime.today())

# 시간대 선택
time_slot = st.radio(
    "⏰ 시간대를 골라주세요!",
    ["오전 (9시~12시)", "오후 (1시~5시)", "저녁 (6시~9시)"]
)

# 하고 싶은 놀이 입력
activity = st.text_input("🎠 무엇을 하고 놀까요?", placeholder="예: 같이 고양이 카페 가기, 보드게임 하기 등")

# 예약하기 버튼
if st.button("✅ 시향이와 약속 예약하기"):
    if activity.strip() == "":
        st.warning("무엇을 하고 놀지 입력해 주세요!")
    else:
        st.success("🎉 시향이와의 놀이 약속이 예약되었어요!")
        st.markdown(f"""
        **📅 날짜:** {date.strftime('%Y-%m-%d')}  
        **⏰ 시간대:** {time_slot}  
        **🎠 놀기 내용:** {activity}
        """)
        st.balloons()
