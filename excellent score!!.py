import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 앱 기본 설정
st.set_page_config(page_title="시험정복기 📚", layout="wide")
st.title("📚 시험정복기 - 개념 & 오답 정리 앱")

# Session 초기화
if 'concepts' not in st.session_state:
    st.session_state.concepts = []

if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []

# 탭 구성
tab1, tab2, tab3 = st.tabs(["🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄"])

# --------------------- 1. 개념 노트 ----------------------
with tab1:
    st.subheader("🧠 과목별 개념 요약")
    subject = st.text_input("과목명")
    concept_title = st.text_input("개념 제목")
    concept_content = st.text_area("내용 요약")
    concept_ref = st.text_input("참고 링크 (선택)")

    if st.button("저장하기", key="save_concept"):
        st.session_state.concepts.append({
            "과목": subject,
            "제목": concept_title,
            "내용": concept_content,
            "링크": concept_ref,
            "날짜": datetime.now().strftime("%Y-%m-%d")
        })
        st.success("개념 저장 완료!")

    st.markdown("---")
    st.subheader("📘 저장된 개념들")
    for c in st.session_state.concepts:
        st.markdown(f"**[{c['과목']}] {c['제목']}** ({c['날짜']})")
        st.markdown(c['내용'])
        if c['링크']:
            st.markdown(f"[🔗 참고링크]({c['링크']})")
        st.markdown("---")

# --------------------- 2. 오답 노트 ----------------------
with tab2:
    st.subheader("❌ 오답 기록하기")
    subject2 = st.text_input("과목명", key="sub2")
    question = st.text_area("문제 내용")
    correct_answer = st.text_input("정답")
    reason = st.text_area("왜 틀렸나요?")
    tag = st.selectbox("오답 원인", ["개념 부족", "계산 실수", "시간 부족", "실수", "기타"])
    
    if st.button("오답 저장", key="save_wrong"):
        st.session_state.wrong_answers.append({
            "과목": subject2,
            "문제": question,
            "정답": correct_answer,
            "오답 이유": reason,
            "태그": tag,
            "날짜": datetime.now().date(),
            "복습 예정일": datetime.now().date() + timedelta(days=3)
        })
        st.success("오답 저장 완료!")

    st.markdown("---")
    st.subheader("📄 오답 목록")
    df_wrong = pd.DataFrame(st.session_state.wrong_answers)
    if not df_wrong.empty:
        st.dataframe(df_wrong)

# --------------------- 3. 복습 스케줄 ----------------------
with tab3:
    st.subheader("🔁 복습해야 할 오답")
    today = datetime.now().date()
    due = [entry for entry in st.session_state.wrong_answers if entry["복습 예정일"] <= today]

    if due:
        st.write("📌 오늘 복습할 오답:")
        df_due = pd.DataFrame(due)
        st.dataframe(df_due)
    else:
        st.success("오늘 복습할 오답은 없어요!")

---

## 🔧 다음 단계 아이디어
- 데이터 저장: `pickle`, `json`, 또는 `gspread`로 Google Sheet 연동
- 로그인 기능 추가 (Streamlit Community Cloud 인증)
- 알림 기능 (복습일에 이메일 or 앱 내 알림)

