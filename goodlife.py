# app.py

import streamlit as st
import json
import os
from datetime import datetime, date, time
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# 파일 경로
DATA_FILE = "gatseng_data.json"

# 초기 데이터 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

# 데이터 불러오기
with open(DATA_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

today_str = date.today().isoformat()

# 응원 멘트 리스트
cheer_messages = [
    "오늘도 살아있는 것만으로 대단해! ✨",
    "게으름은 잠깐, 갓생은 평생 🔥",
    "어제보다 1% 나아진 당신, 갓생이다 💪",
    "오늘도 파이팅! 넌 할 수 있어 😎",
    "조금씩 가는 것도 충분히 잘하고 있어 🐢"
]

# 앱 설정
st.set_page_config(page_title="갓생살기 플래너", layout="centered")
st.title("🌞 갓생살기 플래너")
st.markdown(f"#### 💬 {random.choice(cheer_messages)}")

# ⏰ 기상 시간
st.subheader("⏰ 오늘의 기상 시간")
wake_time = st.time_input("몇 시에 일어났나요?", time(7, 0))

# 🎯 목표
st.subheader("🎯 오늘의 목표")
goals = []
for i in range(1, 4):
    g = st.text_input(f"목표 {i}", key=f"goal_{i}")
    if g:
        goals.append(g)

# 📝 오늘의 일지
st.subheader("📝 오늘의 일지")
mood = st.selectbox("오늘 기분은?", ["😊", "😐", "😩", "😠", "😭"])
diary = st.text_area("오늘 하루를 한 줄로 요약해보세요")
score = st.slider("오늘의 갓생 점수는?", 1, 5, 3)

# ✅ 저장 버튼
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

# 📈 누적 통계
st.subheader("📈 누적 갓생 기록")
if records:
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])

    st.markdown("**📊 갓생 점수 변화 그래프**")
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["score"], marker="o", color="#4CAF50")
    ax.set_title("갓생 점수 추이", fontsize=14)
    ax.set_xlabel("날짜")
    ax.set_ylabel("점수")
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("아직 기록이 없어요. 오늘부터 갓생을 시작해볼까요? 🐣")
