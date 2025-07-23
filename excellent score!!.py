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
# 닉네임 설정
st.sidebar.subheader("👤 닉네임 설정")
if 'nickname' not in st.session_state:
    st.session_state.nickname = st.sidebar.text_input("닉네임을 입력하세요", value="익명")
else:
    st.session_state.nickname = st.sidebar.text_input("닉네임을 입력하세요", value=st.session_state.nickname)

if 'comments' not in st.session_state:
    st.session_state.comments = []
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄", "📅 D-Day", "💡 공부 팁", "📊 오답 분석", "💬 피드백 게시판", "📈 성적 기록"
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

# 중요 D-Day를 앱 상단 우측에 강조 표시 (사용자 설정 기준)
important_dday = next((d for d in st.session_state.ddays if d.get('중요')), None)
if important_dday:
    delta = (important_dday['날짜'] - datetime.now().date()).days
    box_color = "#ffe6e6" if delta <= 3 else "#f0f0f0"
    st.sidebar.markdown(
        f"""
        <div style='padding: 20px; background-color: {box_color}; border-radius: 10px; border: 2px solid #ccc;'>
            <h3 style='color: #d6336c;'>🎯 시험 디데이</h3>
            <p style='font-size: 24px; font-weight: bold;'>
                {important_dday['이름']}<br>D-{delta if delta >= 0 else 'DAY!'}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# D-Day 상단에 크게 표시
if st.session_state.ddays:
    nearest = min(st.session_state.ddays, key=lambda d: abs((d['날짜'] - datetime.now().date()).days))
    days_left = (nearest['날짜'] - datetime.now().date()).days
    if days_left > 0:
        st.markdown(f"""<div style='text-align: center; font-size: 36px; font-weight: bold;'>⏳ {nearest['이름']} - D-{days_left}일</div>""", unsafe_allow_html=True)
    elif days_left == 0:
        st.markdown(f"""<div style='text-align: center; font-size: 36px; font-weight: bold; color: red;'>📣 오늘은 {nearest['이름']}!</div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style='text-align: center; font-size: 28px;'>✅ {nearest['이름']}는 {-days_left}일 전에 지나갔어요</div>""", unsafe_allow_html=True)

with tab4:
    st.subheader("📅 D-Day 관리")
    col1, col2 = st.columns([3, 1])
    with col1:
        dday_name = st.text_input("디데이 이름")
    with col2:
        is_important = st.checkbox("중요 D-Day로 설정")

    dday_date = st.date_input("날짜 선택")

    if st.button("디데이 추가"):
        st.session_state.ddays.append({
            "중요": is_important,
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

# -------------------- 성적 기록 --------------------
with tab8:
    st.subheader("📈 나의 성적 기록")

    if 'scores' not in st.session_state:
        st.session_state.scores = []
    if 'score_subjects' not in st.session_state:
        st.session_state.score_subjects = ["국어", "영어", "수학", "사회", "과학", "역사"]

    st.markdown("#### 과목 추가 / 삭제")
    with st.form("subject_form", clear_on_submit=True):
        new_subject = st.text_input("새 과목 추가")
        remove_subject = st.selectbox("삭제할 과목 선택", [""] + st.session_state.score_subjects)
        submitted_sub = st.form_submit_button("변경 적용")
        if submitted_sub:
            if new_subject and new_subject not in st.session_state.score_subjects:
                st.session_state.score_subjects.append(new_subject)
            if remove_subject and remove_subject in st.session_state.score_subjects:
                st.session_state.score_subjects.remove(remove_subject)
            st.success("과목 리스트가 업데이트되었습니다.")

    subject = st.selectbox("과목 선택", st.session_state.score_subjects)
    grade = st.selectbox("등급 (5등급제)", ["1", "2", "3", "4", "5"])
    total_students = st.number_input("전교생 수", min_value=1, value=100)
    my_rank = st.number_input("전체 등수", min_value=1, value=1)
    percent = round((1 - (my_rank - 1) / total_students) * 100, 2)
    st.markdown(f"👉 계산된 백분위: **{percent}%**")

   
    if st.button("성적 저장"):
    st.session_state.scores.append({
        "과목": subject,
        "5등급": grade,
                "퍼센트": percent,
        "날짜": datetime.now().strftime("%Y-%m-%d")
    })
    st.success("성적이 저장되었습니다!")

    if st.session_state.scores:
    df_score = pd.DataFrame(st.session_state.scores)
    st.markdown("### 📋 저장된 성적")
    st.dataframe(df_score)

    st.markdown("### 📈 평균 백분위")
    avg_percent = df_score["퍼센트"].mean()
    st.metric(label="전체 평균 백분위", value=f"{avg_percent:.2f}%")

# -------------------- 피드백 게시판 --------------------
st.sidebar.markdown("---")
st.sidebar.subheader("💬 피드백 게시판")
new_comment = st.sidebar.text_area("댓글을 남겨보세요 ✍️")
if st.sidebar.button("댓글 등록") and new_comment:
    st.session_state.comments.append({
        "닉네임": st.session_state.nickname,
        "내용": new_comment,
        "시간": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    st.sidebar.success("댓글이 등록되었습니다!")
with tab7:
    st.subheader("💬 전체 피드백")
    for c in reversed(st.session_state.comments):
        st.markdown(f"**{c['닉네임']}** ({c['시간']})")
        st.markdown(f"{c['내용']}")
        st.markdown("---")
    st.subheader("💬 피드백 게시판")
    new_comment = st.text_area("댓글을 남겨보세요 ✍️")
    if st.button("댓글 등록") and new_comment:
        st.session_state.comments.append({
            "닉네임": st.session_state.nickname,
            "내용": new_comment,
            "시간": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.success("댓글이 등록되었습니다!")

    st.markdown("### 📋 전체 댓글")
    for i, c in enumerate(reversed(st.session_state.comments)):
        index = len(st.session_state.comments) - 1 - i
        st.markdown(f"**{c['닉네임']}** ({c['시간']})")
        st.markdown(f"{c['내용']}")
        if st.button(f"🗑️ 삭제", key=f"delete_comment_{index}"):
            st.session_state.comments.pop(index)
            st.experimental_rerun()
        st.markdown("---")
