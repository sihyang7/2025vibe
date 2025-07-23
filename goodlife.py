import streamlit as st
import json
import os
from datetime import datetime, date, time
import random

# ---------------------------
# 1. 데이터 파일 설정
# ---------------------------
DATA_FILE = "gatseng_grid_data.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    records = json.load(f)

# ---------------------------
# 2. Streamlit 기본 설정
# ---------------------------
st.set_page_config(page_title="갓생 모눈 플래너", layout="wide")
st.title("📘 갓생 모눈 플래너")

# ---------------------------
# 3. 응원 멘트
# ---------------------------
cheer_messages = [
    "오늘도 살아있는 것만으로 대단해! ✨",
    "게으름은 잠깐, 갓생은 평생 🔥",
    "어제보다 1% 나아진 당신, 갓생이다 💪",
    "오늘도 파이팅! 넌 할 수 있어 😎",
    "조금씩 가는 것도 충분히 잘하고 있어 🐢",
    "포기하지 않는 당신이 진짜 멋져요 💖",
    "계획만 해도 절반은 성공한 거야! 🗓️"
]
st.markdown(f"### 💬 {random.choice(cheer_messages)}")

# ---------------------------
# 4. 사이드바 - 날짜, 디데이, 기분, 목표
# ---------------------------
with st.sidebar:
    st.header("🗓️ 기본 설정")
    record_date = st.date_input("날짜", value=date.today())
    dday_name = st.text_input("디데이 이름", value="시험일")
    dday_target = st.date_input("디데이 날짜", value=date.today())
    dday_count = (dday_target - record_date).days
    st.markdown(f"**{dday_name}까지 D-{dday_count}**")

    mood = st.selectbox("오늘 기분은?", ["😊", "😐", "😩", "😠", "😭"])
    wake_time = st.time_input("기상 시간", value=time(7, 0))

    # 목표 입력
    st.subheader("🎯 오늘의 목표")
    if "goal_list" not in st.session_state:
        st.session_state.goal_list = []
    goal_input = st.text_input("✏️ 목표 입력")
    if st.button("➕ 목표 추가") and goal_input:
        st.session_state.goal_list.append(goal_input)
    if st.session_state.goal_list:
        for idx, g in enumerate(st.session_state.goal_list):
            st.checkbox(g, key=f"goal_{idx}")
    if st.button("🗑️ 목표 초기화"):
        st.session_state.goal_list = []

# ---------------------------
# 5. 활동 기록 (모눈 종이)
# ---------------------------
st.subheader("🕒 오늘 한 일 기록하기")
if "blocks" not in st.session_state:
    st.session_state.blocks = ["⬜"] * 144  # 24시간 * 6칸 (10분 단위)

with st.form("activity_form", clear_on_submit=True):
    activity = st.text_input("활동 내용", placeholder="예: 영어 단어 외우기")
    start = st.time_input("시작 시간", value=time(9, 0))
    end = st.time_input("종료 시간", value=time(10, 0))
    diary = st.text_area("오늘 한 줄 요약")
    notes = st.text_area("자유 메모")
    score = st.slider("오늘의 갓생 점수", 1, 5, 3)
    submitted = st.form_submit_button("➕ 추가")

    if submitted and activity and start < end:
        start_index = (start.hour * 60 + start.minute) // 10
        end_index = (end.hour * 60 + end.minute) // 10
        for i in range(start_index, end_index):
            st.session_state.blocks[i] = "🟩"

        # 기록 저장
        records.append({
            "date": record_date.isoformat(),
            "wake_time": wake_time.strftime("%H:%M"),
            "activity": activity,
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M"),
            "mood": mood,
            "goals": st.session_state.goal_list,
            "diary": diary,
            "notes": notes,
            "score": score,
            "dday": dday_count,
            "dday_name": dday_name
        })
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
        st.success(f"{activity} 기록이 저장되었어요!")

# ---------------------------
# 6. 모눈 타임라인 출력
# ---------------------------
st.subheader("📊 하루 타임라인 (모눈 스타일)")
rows = [st.session_state.blocks[i:i+6] for i in range(0, 144, 6)]
for hour, row in enumerate(rows):
    col_text = f"{hour:02d}:00"
    line = " ".join(row)
    st.markdown(f"`{col_text}`  {line}")

# ---------------------------
# 7. 기록 보기
# ---------------------------
st.markdown("---")
st.subheader("📋 활동 기록 목록")
if records:
    for r in reversed(records[-10:]):  # 최근 10개만 보기
        st.write(
            f"📅 {r['date']} | 🕒 {r['start']}~{r['end']} | ✏️ {r['activity']} | "
            f"{r['mood']} | {r['dday_name']} D-{r['dday']}"
        )
else:
    st.info("기록이 아직 없어요. 활동을 입력해보세요!")
