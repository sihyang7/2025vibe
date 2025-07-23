import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="시험정복기 📚", layout="wide")
st.title("📚 시험정복기 - 개념/오답/디데이 앱")

# 데이터 저장용 초기화
if 'concepts' not in st.session_state:
    st.session_state.concepts = []
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []
if 'ddays' not in st.session_state:
    st.session_state.ddays = []

# 📚 과목별 공부 팁
study_tips = {
    "국어": "📖 비문학은 구조 파악, 문학은 자주 나오는 작품 암기!",
    "수학": "🧮 개념이해 + 유형 반복 + 실전 속도 연습!",
    "영어": "📘 단어 암기 + 문장 구조 파악 + 기출 반복!",
    "과학": "🔬 핵심 개념 요약 + 그림/모식도 자주 보기!",
    "사회": "🗺️ 흐름 위주 암기 + 시대/원인-결과 정리!",
    "기타": "✍️ 스스로 요약 노트 만들기 + 퀴즈 활용!",
}

# 탭 구분
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄", "📅 D-Day", "💡 공부 팁"])

# -------------------- 1. 개념 노트 --------------------
with tab1:
    st.subheader("🧠 개념 정리")
    subject = st.text_input("과목")
    title = st.text_input("개념 제목")
    content = st.text_area("내용")
    link = st.text_input("참고 링크 (선택)")

    if st.button("저장", key="save_concept"):
        st.session_state.concepts.append({
            "과목": subject,
            "제목": title,
            "내용": content,
            "링크": link,
            "날짜": datetime.now().strftime("%Y-%m-%d")
        })
        st.success("저장되었습니다!")

    for c in st.session_state.concepts:
        st.markdown(f"**[{c['과목']}] {c['제목']}** ({c['날짜']})")
        st.markdown(c["내용"])
        if c["링크"]:
            st.markdown(f"[🔗 링크]({c['링크']})")
        st.markdown("---")

# -------------------- 2. 오답 정리 --------------------
with tab2:
    st.subheader("❌ 오답 노트")
    subject2 = st.text_input("과목", key="sub2")
    question = st.text_area("문제 내용")
    correct = st.text_input("정답")
    reason = st.text_area("왜 틀렸나요?")
    tag = st.selectbox("오답 원인", ["개념 부족", "계산 실수", "시간 부족", "기타"])
    
    if st.button("오답 저장", key="save_wrong"):
        st.session_state.wrong_answers.append({
            "과목": subject2,
            "문제": question,
            "정답": correct,
            "오답 이유": reason,
            "태그": tag,
            "날짜": datetime.now().date(),
            "복습 예정일": datetime.now().date() + timedelta(days=3)
        })
        st.success("오답이 저장되었습니다!")

    if st.session_state.wrong_answers:
        st.dataframe(pd.DataFrame(st.session_state.wrong_answers))

# -------------------- 3. 복습 스케줄 --------------------
with tab3:
    st.subheader("🔁 복습할 오답 목록")
    today = datetime.now().date()
    due = [entry for entry in st.session_state.wrong_answers if entry["복습 예정일"] <= today]
    if due:
        st.write("오늘 복습할 오답입니다:")
        st.dataframe(pd.DataFrame(due))
    else:
        st.success("오늘 복습할 항목이 없어요!")

# -------------------- 4. D-Day --------------------
with tab4:
    st.subheader("📅 디데이 등록")
    dday_name = st.text_input("디데이 이름")
    dday_date = st.date_input("날짜 선택")

    if st.button("디데이 추가"):
        st.session_state.ddays.append({
            "이름": dday_name,
            "날짜": dday_date
        })
        st.success("디데이가 등록되었습니다!")

    st.subheader("📌 등록된 D-Day")
    for d in st.session_state.ddays:
        delta = (d["날짜"] - datetime.now().date()).days
        if delta > 0:
            st.markdown(f"🗓️ **{d['이름']}**: D-{delta}일 남음")
        elif delta == 0:
            st.markdown(f"📣 **{d['이름']}**: 오늘이 디데이!")
        else:
            st.markdown(f"✅ **{d['이름']}**: {-delta}일 전 종료")

# -------------------- 5. 과목별 공부 팁 --------------------
with tab5:
    st.subheader("💡 과목별 공부법 추천")
    selected_subject = st.selectbox("과목을 선택하세요", list(study_tips.keys()))
    st.markdown(study_tips[selected_subject])
