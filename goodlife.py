import streamlit as st
import json
import os
from datetime import datetime, date, time, timedelta
import random
import pandas as pd

# 데이터 파일 설정
DATA_FILE = "gatseng_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

today_str = date.today().isoformat()

cheer_messages = [
    "오늘도 살아있는 것만으로 대단해! ✨",
    "게으름은 잠깐, 갓생은 평생 🔥",
    "어제보다 1% 나아진 당신, 갓생이다 💪",
    "오늘도 파이팅! 넌 할 수 있어 😎",
    "조금씩 가는 것도 충분히 잘하고 있어 🐢"
]

# --- 사이드바 ---
st.set_page_config(page_title="갓생살기 플래너", layout="wide")
with st.sidebar:
    st.title("🌟 갓생 설정")
    record_date = st.date_input("📅 날짜", value=date.today())
    dday_target = st.date_input("⏳ 디데이 설정 (예: 시험일)", value=date.today())
    dday_count = (dday_target - date.today()).days
    st.markdown(f"**D-{dday_count}**")
    mood = st.selectbox("오늘 기분은?", ["😊", "😐", "😩", "😠", "😭"])
    st.markdown("---")

# --- 본문 ---
st.title("🌞 갓생살기 플래너")
st.markdown(f"#### 💬 {random.choice(cheer_messages)}")

st.subheader("⏰ 오늘의 기상 시간")
wake_time = st.time_input("몇 시에 일어났나요?", time(7, 0))

st.subheader("🎯 오늘의 목표")

if "goal_list" not in st.session_state:
    st.session_state.goal_list = []

goal_input = st.text_input("✏️ 목표를 입력하세요")
if st.button("➕ 목표 추가") and goal_input:
    st.session_state.goal_list.append(goal_input)
    # 입력칸 초기화는 streamlit이 기본 제공

if st.session_state.goal_list:
    for idx, g in enumerate(st.session_state.goal_list):
        st.checkbox(g, key=f"goal_{idx}")

if st.button("🗑️ 목표 초기화"):
    st.session_state.goal_list = []


if "timeline" not in st.session_state:
    st.session_state.timeline = []

with st.form("timeline_form", clear_on_submit=True):
    st.markdown("## 📘 오늘 한 일 기록")
    start_time = st.time_input("시작 시간", time(9, 0))
    end_time = st.time_input("종료 시간", time(10, 0))
    activity = st.text_input("활동 내용 (예: 영어 단어 외우기)")
    submitted = st.form_submit_button("➕ 추가하기")
    if submitted and activity and start_time < end_time:
        duration = int((datetime.combine(date.today(), end_time) -
                        datetime.combine(date.today(), start_time)).seconds / 600)  # 10분 단위
        st.session_state.timeline.append({
            "start": start_time.strftime("%H:%M"),
            "end": end_time.strftime("%H:%M"),
            "activity": activity,
            "blocks": "🟩" * duration
        })

# 타임라인 출력
if st.session_state.timeline:
    st.markdown("## 📊 오늘의 활동 타임라인")
    for item in st.session_state.timeline:
        st.write(f"🕒 `{item['start']} ~ {item['end']}` | {item['activity']} | {item['blocks']}")


st.subheader("📝 오늘의 일지")
diary = st.text_area("오늘 하루를 한 줄로 요약해보세요")

st.subheader("📌 자유 메모")
notes = st.text_area("생각나는 것을 자유롭게 적어보세요")

score = st.slider("오늘의 갓생 점수는?", 1, 5, 3)

if st.button("✅ 저장하기"):
    record = {
        "date": record_date.isoformat(),
        "wake_time": wake_time.strftime("%H:%M"),
        "goals": st.session_state.goal_list,
        "selected_blocks": selected_blocks,
        "mood": mood,
        "diary": diary,
        "notes": notes,
        "score": score,
        "dday": dday_count
    }
    records.append(record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    st.success("기록이 저장되었어요! 🎉")

st.subheader("📋 누적 기록 보기")
if records:
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", ascending=False)
    st.dataframe(df[["date", "wake_time", "score", "mood", "diary", "dday"]], use_container_width=True)
else:
    st.info("아직 기록이 없어요. 오늘부터 갓생 시작해볼까요? 🐣")
