import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="시험정복기 📚", layout="wide")
st.title("📚 시험정복기 - 개념/오답/디데이 앱")

# -------------------- 초기 상태 --------------------
if 'concepts' not in st.session_state:
    st.session_state.concepts = []
if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []
if 'ddays' not in st.session_state:
    st.session_state.ddays = []

study_tips = {
    "국어": "📖 비문학은 구조 파악, 문학은 자주 나오는 작품 암기!",
    "수학": "🧮 개념이해 + 유형 반복 + 실전 속도 연습!",
    "영어": "📘 단어 암기 + 문장 구조 파악 + 기출 반복!",
    "과학": "🔬 핵심 개념 요약 + 그림/모식도 자주 보기!",
    "사회": "🗺️ 흐름 위주 암기 + 시대/원인-결과 정리!",
    "기타": "✍️ 스스로 요약 노트 만들기 + 퀴즈 활용!",
}

# -------------------- 탭 설정 --------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄", "📅 D-Day", "💡 공부 팁", "📊 오답 분석"
])

# -------------------- 개념 노트 --------------------
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

    subjects = sorted(set(c['과목'] for c in st.session_state.concepts))
    for subj in subjects:
        st.markdown(f"### 📘 {subj}")
        for c in [c for c in st.session_state.concepts if c['과목'] == subj]:
            st.markdown(f"**{c['제목']}** ({c['날짜']})")
            st.markdown(c["내용"])
            if c["링크"]:
                st.markdown(f"[🔗 링크]({c['링크']})")
            st.markdown("---")

# -------------------- 오답 정리 --------------------
with tab2:
    st.subheader("❌ 오답 노트")

    with st.form("wrong_note_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            subject2 = st.text_input("과목", key="sub2")
        with col2:
            date_wrong = st.date_input("틀린 날짜", value=datetime.now().date())

        image = st.file_uploader("📷 문제 사진 업로드", type=["jpg", "png", "jpeg"])
        question = st.text_area("문제 설명 (텍스트)", placeholder="문제가 어떤 내용이었는지 간략히 써주세요")
        my_answer = st.text_area("내가 쓴 답")
        why_that_answer = st.text_area("왜 그렇게 생각했나요?")
        correct = st.text_input("정답")
        related_concept = st.text_area("관련 개념 정리")

        reason_multi = st.multiselect(
            "오답 원인 선택 (복수 선택 가능)",
            ["개념 부족", "계산 실수", "문제 이해 오류", "시간 부족", "실수", "기타"]
        )

        submitted = st.form_submit_button("오답 저장")

        if submitted:
            entry = {
                "과목": subject2,
                "문제 설명": question,
                "내 답": my_answer,
                "왜 그렇게 썼는가": why_that_answer,
                "정답": correct,
                "관련 개념": related_concept,
                "오답 원인": reason_multi,
                "날짜": date_wrong,
                "복습 예정일": date_wrong + timedelta(days=3),
                "이미지": image.read() if image else None,
                "이미지 이름": image.name if image else None
            }
            st.session_state.wrong_answers.append(entry)
            st.success("오답이 저장되었습니다!")

    st.markdown("### 📄 오답 목록")
    if st.session_state.wrong_answers:
        grouped = {}
        for e in st.session_state.wrong_answers:
            key = (e['과목'], e['날짜'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(e)

        for (subject, date), entries in sorted(grouped.items(), key=lambda x: (x[0][0], x[0][1]), reverse=True):
            st.markdown(f"## 📘 {subject} - {date}")
            for entry in entries:
                if entry["이미지"]:
                    st.image(entry["이미지"], caption=entry["이미지 이름"], width=400)
                st.markdown(f"**문제 설명:** {entry['문제 설명']}")
                st.markdown(f"**내가 쓴 답:** {entry['내 답']}")
                st.markdown(f"**왜 그렇게 썼나:** {entry['왜 그렇게 썼는가']}")
                st.markdown(f"**정답:** {entry['정답']}")
                st.markdown(f"**관련 개념:** {entry['관련 개념']}")
                st.markdown(f"**오답 원인:** {', '.join(entry['오답 원인'])}")
                st.markdown(f"📅 복습 예정일: {entry['복습 예정일']}")
                st.markdown("---")
    else:
        st.info("아직 오답이 없습니다.")

# -------------------- 복습 스케줄 --------------------
with tab3:
    st.subheader("🔁 복습 스케줄")
    today = datetime.now().date()
    due = [e for e in st.session_state.wrong_answers if e["복습 예정일"] <= today]
    if due:
        st.success(f"오늘 복습할 오답 {len(due)}개 있어요!")
        for d in due:
            st.markdown(f"**📘 {d['과목']}** - {d['문제 설명'][:30]}... / 복습일: {d['복습 예정일']}")
    else:
        st.info("오늘 복습할 오답은 없어요!")

# -------------------- D-Day --------------------
with tab4:
    st.subheader("📅 D-Day 관리")
    dday_name = st.text_input("디데이 이름")
    dday_date = st.date_input("날짜 선택")

    if st.button("디데이 추가"):
        st.session_state.ddays.append({
            "이름": dday_name,
            "날짜": dday_date
        })
        st.success("디데이가 등록되었습니다!")

    st.markdown("### 📌 등록된 D-Day")
    for d in st.session_state.ddays:
        delta = (d["날짜"] - datetime.now().date()).days
        if delta > 0:
            st.markdown(f"🗓️ **{d['이름']}**: D-{delta}일 남음")
        elif delta == 0:
            st.markdown(f"📣 **{d['이름']}**: 오늘이 디데이!")
        else:
            st.markdown(f"✅ **{d['이름']}**: {-delta}일 전 종료")

# -------------------- 공부 팁 --------------------
with tab5:
    st.subheader("💡 과목별 공부 팁 추천")
    selected = st.selectbox("과목을 선택하세요", list(study_tips.keys()))
    st.markdown(study_tips[selected])

# -------------------- 오답 분석 --------------------
with tab6:
    st.subheader("📊 오답 분석 및 맞춤형 조언")

    if st.session_state.wrong_answers:
        df = pd.DataFrame(st.session_state.wrong_answers)

        # 1. 오답 원인 분석
        all_reasons = sum(df['오답 원인'], [])
        reason_counts = pd.Series(all_reasons).value_counts()
        st.markdown("### 📌 오답 원인 분석")
        st.bar_chart(reason_counts, use_container_width=True)

        st.markdown("### 🧠 맞춤형 조언")
        if '개념 부족' in reason_counts and reason_counts['개념 부족'] >= 3:
            st.warning("'개념 부족' 오답이 많아요. 개념 노트를 자주 복습하고, 단원별로 요약해보세요.")
        if '계산 실수' in reason_counts and reason_counts['계산 실수'] >= 2:
            st.info("계산 실수가 반복되네요. 실전 연습 시 계산 후 검산 습관을 들이세요.")
        if '문제 이해 오류' in reason_counts:
            st.info("문제 자체를 잘못 해석하는 경향이 있어요. 문제를 두 번 읽는 습관을 들이세요.")

        # 2. 과목별 오답 분석
        subject_counts = df['과목'].value_counts()
        st.markdown("### 📚 과목별 오답 빈도")
        st.bar_chart(subject_counts, use_container_width=True)

        if subject_counts.max() > 5:
            worst_subject = subject_counts.idxmax()
            st.warning(f"'{worst_subject}' 과목에서 오답이 많아요. 이 과목 복습을 집중하세요.")
    else:
        st.info("분석할 오답이 아직 충분하지 않아요.")

