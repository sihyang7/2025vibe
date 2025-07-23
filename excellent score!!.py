# 시험정복기 전체 앱 (D-Day 강조 + 분석 조언 포함)
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

st.set_page_config(page_title="시험정복기 📚", layout="wide")
st.title("📚 시험정복기 - 개념/오답/디데이 앱")

# -------------------- 세션 상태 초기화 --------------------
if 'concepts' not in st.session_state:
    st.session_state.concepts = []
if 'wrong_answers_by_subject' not in st.session_state:
    st.session_state.wrong_answers_by_subject = defaultdict(lambda: defaultdict(list))
if 'ddays' not in st.session_state:
    st.session_state.ddays = []
if 'scores' not in st.session_state:
    st.session_state.scores = []

# -------------------- 상단 중요 D-Day 강조 표시 --------------------
important_ddays = [d for d in st.session_state.ddays if d.get("중요")]
if important_ddays:
    upcoming = sorted(important_ddays, key=lambda x: x["날짜"])[0]
    delta = (upcoming["날짜"] - datetime.now().date()).days
    if delta > 0:
        st.markdown(f"### 🎯 중요한 일정: **{upcoming['이름']}** (D-{delta})")
    elif delta == 0:
        st.markdown(f"### 🚨 오늘은 **{upcoming['이름']}** 디데이!")
    else:
        st.markdown(f"### ✅ **{upcoming['이름']}** 디데이는 {-delta}일 전에 끝났어요")

# -------------------- 공부 팁 --------------------
study_tips = {
    "국어": "📖 비문학은 구조 파악, 문학은 자주 나오는 작품 암기!",
    "수학": "🧮 개념이해 + 유형 반복 + 실전 속도 연습!",
    "영어": "📘 단어 암기 + 문장 구조 파악 + 기출 반복!",
    "과학": "🔬 핵심 개념 요약 + 그림/모식도 자주 보기!",
    "사회": "🗺️ 흐름 위주 암기 + 시대/원인-결과 정리!",
    "기타": "✍️ 스스로 요약 노트 만들기 + 퀴즈 활용!",
}

# -------------------- 탭 구성 --------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄", "📅 D-Day", "💡 공부 팁", "📊 분석 리포트", "📈 성적 관리"])

# -------------------- 1. 개념 노트 --------------------
# ... (기존 내용 유지)

# -------------------- 7. 성적 관리 --------------------
with tab7:
    st.subheader("📈 성적 관리 / 백분위 계산")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        score_subject = st.text_input("과목", key="score_subject")
    with col2:
        score = st.number_input("점수", min_value=0.0, max_value=100.0, step=0.1, key="score")
    with col3:
        rank = st.number_input("내 등수", min_value=1, step=1, key="rank")
    with col4:
        total_students = st.number_input("전교생 수", min_value=1, step=1, key="total_students")

    if st.button("저장", key="save_score"):
        percentile = round(100 * (1 - (rank - 1) / total_students), 2)
        st.session_state.scores.append({
            "과목": score_subject,
            "점수": score,
            "등수": rank,
            "전체 인원": total_students,
            "백분위": percentile
        })
        st.success(f"{score_subject} 성적 저장 완료! 백분위: {percentile}점")

    if st.session_state.scores:
        st.markdown("### 📊 저장된 성적")
        st.dataframe(pd.DataFrame(st.session_state.scores))
