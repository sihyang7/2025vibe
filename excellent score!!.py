# 시험정복기 전체 앱
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

st.set_page_config(page_title="시험정복기 📚", layout="wide")
st.title("📚 시험정복기 - 개념/오답/디데이 앱")

# 상태 초기화
if 'concepts' not in st.session_state:
    st.session_state.concepts = []
if 'wrong_answers_by_subject' not in st.session_state:
    st.session_state.wrong_answers_by_subject = defaultdict(lambda: defaultdict(list))
if 'ddays' not in st.session_state:
    st.session_state.ddays = []

# 공부 팁
study_tips = {
    "국어": "📖 비문학은 구조 파악, 문학은 자주 나오는 작품 암기!",
    "수학": "🧮 개념이해 + 유형 반복 + 실전 속도 연습!",
    "영어": "📘 단어 암기 + 문장 구조 파악 + 기출 반복!",
    "과학": "🔬 핵심 개념 요약 + 그림/모식도 자주 보기!",
    "사회": "🗺️ 흐름 위주 암기 + 시대/원인-결과 정리!",
    "기타": "✍️ 스스로 요약 노트 만들기 + 퀴즈 활용!",
}

# 탭 구성
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🧠 개념 노트", "❌ 오답 정리", "🔁 복습 스케줄", "📅 D-Day", "💡 공부 팁", "📊 분석 리포트"])

# 1. 개념 노트
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

# 2. 오답 정리
with tab2:
    st.subheader("❌ 오답 노트")
    subject2 = st.text_input("과목", key="sub2")
    question = st.text_area("문제 내용")
    image = st.file_uploader("문제 사진 업로드 (선택)", type=["png", "jpg", "jpeg"], key="img_upload")
    my_answer = st.text_input("내가 쓴 답은?")
    why_that_answer = st.text_area("왜 그렇게 썼나요?")
    correct = st.text_input("정답")
    reason = st.text_area("왜 틀렸나요?")
    tags = st.multiselect("오답 원인 (복수 선택 가능)", ["개념 부족", "계산 실수", "시간 부족", "문제 해석 오류", "기타"])
    concept_related = st.text_area("이 문제와 관련된 개념 정리")

    if st.button("오답 저장", key="save_wrong"):
        data = {
            "날짜": datetime.now().date(),
            "문제": question,
            "이미지": image.read() if image else None,
            "내 답": my_answer,
            "그렇게 쓴 이유": why_that_answer,
            "정답": correct,
            "오답 이유": reason,
            "태그": tags,
            "관련 개념": concept_related,
            "복습 예정일": datetime.now().date() + timedelta(days=3)
        }
        today_str = datetime.now().strftime("%Y-%m-%d")
        st.session_state.wrong_answers_by_subject[subject2][today_str].append(data)
        st.success("오답이 저장되었습니다!")

    st.subheader("📁 저장된 오답 보기")
    for subject, by_date in st.session_state.wrong_answers_by_subject.items():
        with st.expander(f"📚 {subject}"):
            for date, entries in by_date.items():
                st.markdown(f"### 📅 {date}")
                for idx, wa in enumerate(entries):
                    with st.expander(f"오답 {idx+1}"):
                        st.markdown(f"**문제**: {wa['문제']}")
                        if wa["이미지"]:
                            st.image(wa["이미지"], caption="문제 사진", use_column_width=True)
                        st.markdown(f"**내 답**: {wa['내 답']}")
                        st.markdown(f"**그렇게 쓴 이유**: {wa['그렇게 쓴 이유']}")
                        st.markdown(f"**정답**: {wa['정답']}")
                        st.markdown(f"**오답 이유**: {wa['오답 이유']}")
                        st.markdown(f"**오답 원인**: {', '.join(wa['태그'])}")
                        st.markdown(f"**관련 개념**: {wa['관련 개념']}")
                        st.markdown(f"📅 복습 예정일: {wa['복습 예정일']}")

# 3. 복습 스케줄
with tab3:
    st.subheader("🔁 복습할 오답 목록")
    today = datetime.now().date()
    due = []
    for subject, by_date in st.session_state.wrong_answers_by_subject.items():
        for date, entries in by_date.items():
            for entry in entries:
                if entry["복습 예정일"] <= today:
                    due.append({
                        "과목": subject,
                        "날짜": date,
                        "문제": entry["문제"],
                        "복습 예정일": entry["복습 예정일"]
                    })
    if due:
        st.write("오늘 복습할 오답입니다:")
        st.dataframe(pd.DataFrame(due))
    else:
        st.success("오늘 복습할 항목이 없어요!")

# 4. 디데이
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
    sorted_ddays = sorted(st.session_state.ddays, key=lambda x: x["날짜"])
    for d in sorted_ddays:
        delta = (d["날짜"] - datetime.now().date()).days
        if delta > 0:
            st.markdown(f"🗓️ **{d['이름']}**: <span style='color:green;'>D-{delta}</span>일 남음", unsafe_allow_html=True)
        elif delta == 0:
            st.markdown(f"📣 **{d['이름']}**: <span style='color:red;'>오늘이 디데이!</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"✅ **{d['이름']}**: <span style='color:gray;'>{-delta}일 전 종료</span>", unsafe_allow_html=True)

# 5. 공부 팁
with tab5:
    st.subheader("💡 과목별 공부법 추천")
    selected_subject = st.selectbox("과목을 선택하세요", list(study_tips.keys()))
    st.markdown(study_tips[selected_subject])

# 6. 분석 리포트
with tab6:
    st.subheader("📊 맞춤 분석 리포트")
    subject_stats = {s: sum(len(entries) for entries in by_date.values()) for s, by_date in st.session_state.wrong_answers_by_subject.items()}
    if subject_stats:
        st.write("📌 과목별 오답 개수")
        st.bar_chart(pd.DataFrame(subject_stats.values(), index=subject_stats.keys(), columns=["오답 수"]))
    else:
        st.info("아직 저장된 오답 데이터가 없습니다.")
    
    tag_counts = defaultdict(int)
    for by_date in st.session_state.wrong_answers_by_subject.values():
        for entries in by_date.values():
            for e in entries:
                for tag in e["태그"]:
                    tag_counts[tag] += 1
    if tag_counts:
        st.write("📌 오답 원인 통계")
        st.bar_chart(pd.DataFrame(tag_counts.values(), index=tag_counts.keys(), columns=["건수"]))
    else:
        st.info("오답 원인 데이터가 아직 없습니다.")
