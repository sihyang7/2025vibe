import streamlit as st
import json
import os
from datetime import datetime, date, time
import random
import pandas as pd

# 기본 데이터 파일
DATA_FILE = "gatseng_grid_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    try:
        records = json.load(f)
    except json.JSONDecodeError:
        records = []

# 응원 멘트
CHEER_MESSAGES = [
    "오늘도 살아있는 것만으로 대단해! ✨",
    "게으름은 잠깐, 갓생은 평생 🔥",
    "어제보다 1% 나아진 당신, 갓생이다 💪",
    "오늘도 파이팅! 넌 할 수 있어 😎",
    "조금씩 가는 것도 충분히 잘하고 있어 🐢",
    "포기하지 않는 당신이 진짜 멋져요 💖",
    "계획만 해도 절반은 성공한 거야! 🗓️",
]

# 저장 함수
def save_records():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

# 타임블록 계산
def blocks_for_date(day_iso: str):
    blocks = ["⬜"] * 144
    for r in records:
        if r.get("date") != day_iso:
            continue
        try:
            sh, sm = map(int, r["start"].split(":"))
            eh, em = map(int, r["end"].split(":"))
            s_idx = (sh * 60 + sm) // 10
            e_idx = (eh * 60 + em) // 10
            for i in range(max(0, s_idx), min(144, e_idx)):
                blocks[i] = "🟩"
        except:
            continue
    return blocks

# 페이지 설정
st.set_page_config(page_title="갓생 모눈 플래너", layout="wide")
st.title("📘 갓생 모눈 플래너")
st.markdown(f"### 💬 {random.choice(CHEER_MESSAGES)}")

# 사이드바 설정
with st.sidebar:
    st.header("🗓️ 기본 설정")

    record_date = st.date_input("날짜", value=date.today())
    record_date_iso = record_date.isoformat()

    st.markdown("#### 📌 디데이 설정 (여러 개 가능)")
    if "dday_list" not in st.session_state:
        st.session_state.dday_list = []
    dday_name = st.text_input("디데이 이름", placeholder="예: 자격증 시험")
    dday_target = st.date_input("디데이 날짜", value=record_date)
    if st.button("➕ 디데이 추가") and dday_name:
        days_left = (dday_target - record_date).days
        st.session_state.dday_list.append({
            "name": dday_name,
            "target": dday_target.isoformat(),
            "dday": days_left
        })
    for d in st.session_state.dday_list:
        st.markdown(f"- {d['name']} → D-{d['dday']}")

    mood = st.selectbox("오늘 기분은?", ["😊", "😐", "😩", "😠", "😭"])
    wake_time = st.time_input("기상 시간", value=time(7, 0), step=300)

    st.subheader("🎯 오늘의 목표")
    if "goal_list" not in st.session_state:
        st.session_state.goal_list = []
    goal_input = st.text_input("✏️ 목표 입력")
    if st.button("➕ 목표 추가") and goal_input:
        st.session_state.goal_list.append(goal_input)

    if st.session_state.goal_list:
        goal_states = []
        for idx, g in enumerate(st.session_state.goal_list):
            checked = st.checkbox(g, key=f"goal_chk_{idx}")
            goal_states.append({"text": g, "done": checked})
    else:
        goal_states = []

    if st.button("🗑️ 목표 초기화"):
        st.session_state.goal_list = []
        st.experimental_rerun()

# 활동 기록 폼
st.subheader("🕒 오늘 한 일 기록하기")
with st.form("activity_form", clear_on_submit=True):
    activity = st.text_input("활동 내용", placeholder="예: 영어 단어 외우기")
    start_t = st.time_input("시작 시간", value=time(9, 0), step=300)
    end_t   = st.time_input("종료 시간", value=time(10, 0), step=300)
    diary   = st.text_area("오늘 한 줄 요약")
    notes   = st.text_area("자유 메모")
    score   = st.slider("오늘의 갓생 점수", 1, 5, 3)
    submitted = st.form_submit_button("➕ 기록 추가")

    if submitted:
        if not activity:
            st.warning("활동 내용을 입력해주세요.")
        elif start_t >= end_t:
            st.warning("시작 시간이 종료 시간보다 앞서야 해요.")
        else:
            record = {
                "date": record_date_iso,
                "wake_time": wake_time.strftime("%H:%M"),
                "activity": activity,
                "start": start_t.strftime("%H:%M"),
                "end": end_t.strftime("%H:%M"),
                "mood": mood,
                "goals": goal_states,
                "diary": diary,
                "notes": notes,
                "score": score,
                "dday_list": st.session_state.dday_list
            }
            records.append(record)
            save_records()
            st.success(f"'{activity}' 기록이 저장되었어요! ✅")

# 모눈 타임라인
st.subheader(f"📊 {record_date_iso} 하루 타임라인 (10분 단위)")
blocks = blocks_for_date(record_date_iso)
for hour in range(24):
    row = blocks[hour*6 : hour*6 + 6]
    st.markdown(f"`{hour:02d}:00`  {' '.join(row)}")

# 최근 기록
st.markdown("---")
st.subheader("📋 최근 활동 기록")
if records:
    for r in reversed(records[-10:]):
        dday_summary = ", ".join(
            [f"{d['name']} D-{d['dday']}" for d in r.get("dday_list", [])]
        )
        st.write(
            f"📅 {r['date']} | 🕒 {r['start']}~{r['end']} | "
            f"✏️ {r['activity']} | {r['mood']} | {dday_summary}"
        )
else:
    st.info("기록이 아직 없어요. 활동을 추가해보세요!")
