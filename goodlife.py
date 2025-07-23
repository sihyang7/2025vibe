import streamlit as st
import json
import os
from datetime import datetime, date, time
import random
import pandas as pd

# 데이터 파일 설정
DATA_FILE = "gatseng_data.json"

# 초기 데이터 파일 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# 데이터 로드
with open(DATA_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

today_str = date.today().isoformat()

# 응원 멘트
cheer_messages = [
    "오늘도 살아있는 것만으로 대단해! ✨",
    "게으름은 잠깐, 갓생은 평생 🔥",
    "어제보다 1% 나아진 당신, 갓생이다 💪",
    "오늘도 파이팅! 넌 할 수 있어 😎",
    "조금씩 가는 것도 충분히 잘하고 있어 🐢"
]

# Streamlit 설정
st.set_page_config(page_title="갓생살기 플래너", layout="centered")
st.title("🌞 갓생살기 플래너")

# 응원 멘트
st.markdown(f"#### 💬 {random.choice(cheer_messages)}")

# 기상 시간 입력
st.subheader("⏰ 오늘의 기상 시간")
wake_time = st.time_input("몇 시에 일어났나요?", time(7, 0))

# 하루 목표 설정
st.subheader("🎯 오늘의 목표")
goals = []
for i in range(1, 4):
    goal = st.text_input(f"목표 {i}", key=f"goal_{i}")
    if goal:
        goals.append(goal)

# 일지 작성
st.subheader("📝 오늘의 일지")
mood = st.selectbox("오늘 기분은 어땠나요?", ["😊", "😐", "😩", "😠", "😭"])
diary = st.text_area("오늘 하루를 한 줄로 요약해보세요")
score = st.slider("오늘의 갓생 점수는?", 1, 5, 3)

# 저장
if st.button("✅ 저장하기"):
    record = {
        "date": today_str,
        "wake_time": wake_time.strftime("%H:%M"),
        "goals": goals,
        "mood": mood,
        "diary": diary,
        "score": score
    }
    records.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    st.success("기록이 저장되었어요! 🎉")

# 기록 보기
st.subheader("📋 누적 갓생 기록")
if records:
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", ascending=False)

    # 간단한 테이블 형식으로 보여주기
    st.dataframe(df[["date", "wake_time", "score", "mood", "diary"]], use_container_width=True)
else:
    st.info("아직 기록이 없어요. 오늘부터 갓생 시작해볼까요? 🐣")
