import streamlit as st
import time
import pandas as pd
import random

# 랭킹 저장용 CSV 파일
RANKING_FILE = "ranking.csv"

# 타이머 설정
GAME_DURATION = 5  # 게임 시간 (초)

# 하마 이모지 or 이미지
HIPPO = "🦛💨"

# 페이지 설정
st.set_page_config(page_title="인영이 잡기 게임", layout="centered")

st.title("🏃‍♂️ 인영이 잡기 게임")
st.markdown("하마를 클릭해서 인영이를 따라잡아라! 클릭할수록 속도 UP! ⏱️")

# 닉네임 입력
nickname = st.text_input("닉네임을 입력하세요:", max_chars=20)

if nickname:
    if st.button("게임 시작"):
        st.write("🔫 준비...")
        time.sleep(1)
        st.write("🔥 시작!")

        # 클릭 수 초기화
        click_count = 0

        # 시작 시간
        start_time = time.time()
        end_time = start_time + GAME_DURATION

        # 클릭 버튼
        while time.time() < end_time:
            if st.button(f"{HIPPO} 클릭해서 잡아라! ({click_count})"):
                click_count += 1
            time.sleep(0.1)  # 무한루프 속도 제어

        # 결과 계산
        total_time = round(time.time() - start_time, 2)
        speed = round(click_count / total_time, 2)

        st.success(f"🎉 게임 종료! 총 클릭 수: {click_count}회 / 평균 속도: {speed}회/초")

        # 랭킹 저장
        new_score = pd.DataFrame([{
            "닉네임": nickname,
            "클릭 수": click_count,
            "평균 속도": speed,
            "시간": total_time,
            "시각": time.strftime('%Y-%m-%d %H:%M:%S')
        }])

        try:
            df = pd.read_csv(RANKING_FILE)
            df = pd.concat([df, new_score], ignore_index=True)
        except FileNotFoundError:
            df = new_score

        df = df.sort_values(by="클릭 수", ascending=False)
        df.to_csv(RANKING_FILE, index=False)

        st.subheader("🏆 실시간 랭킹")
        st.dataframe(df.reset_index(drop=True).head(10))

else:
    st.warning("닉네임을 입력해야 게임을 시작할 수 있어요!")

