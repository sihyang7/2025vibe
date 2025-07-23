import streamlit as st
import time
import pandas as pd

RANKING_FILE = "ranking.csv"
GAME_DURATION = 10  # 게임 시간 (초)

st.set_page_config(page_title="하마 따라잡기", layout="centered")

st.title("🧗 하마 따라잡기 게임")
st.markdown("제한 시간 동안 `잡기!` 버튼을 클릭해 하마를 따라잡아보세요!")

nickname = st.text_input("닉네임을 입력하세요:", max_chars=20)

# 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False
    st.session_state.steps = 0
    st.session_state.start_time = None
    st.session_state.end_time = None

# 하마 위치 표시
st.markdown("### 🦛 하마가 도망친다!")

# 게임 시작
if nickname and not st.session_state.game_started:
    if st.button("🎮 게임 시작"):
        st.session_state.game_started = True
        st.session_state.steps = 0
        st.session_state.start_time = time.time()
        st.session_state.end_time = st.session_state.start_time + GAME_DURATION
        st.success("게임 시작! 하마를 잡아라!")

# 게임 중
if st.session_state.game_started:
    now = time.time()
    if now < st.session_state.end_time:
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("🐾 잡기!"):
                st.session_state.steps += 1

        # 사람 위치 출력 (높이 표현)
        st.markdown("### 당신의 위치")
        st.text("\n" * (20 - st.session_state.steps) + "🧍‍♂️")  # 위로 올라가는 느낌
        remaining = int(st.session_state.end_time - now)
        st.info(f"남은 시간: {remaining}초 | 현재 높이: {st.session_state.steps}칸")

    else:
        # 게임 종료
        st.session_state.game_started = False
        total_time = round(now - st.session_state.start_time, 2)
        speed = round(st.session_state.steps / total_time, 2)
        st.success(f"🎉 게임 종료! 총 이동: {st.session_state.steps}칸 / 평균 속도: {speed}칸/초")

        # 점수 저장
        new_score = pd.DataFrame([{
            "닉네임": nickname,
            "칸 수": st.session_state.steps,
            "평균 속도": speed,
            "시간": total_time,
            "시각": time.strftime('%Y-%m-%d %H:%M:%S')
        }])

        try:
            df = pd.read_csv(RANKING_FILE)
            df = pd.concat([df, new_score], ignore_index=True)
        except FileNotFoundError:
            df = new_score

        df = df.sort_values(by="칸 수", ascending=False)
        df.to_csv(RANKING_FILE, index=False)

        st.subheader("🏆 실시간 랭킹 (Top 10)")
        st.dataframe(df.reset_index(drop=True).head(10))
else:
    if not nickname:
        st.warning("닉네임을 입력하세요!")
