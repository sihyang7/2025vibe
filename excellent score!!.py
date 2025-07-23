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
                "오답 원인": reason_multi,
                "날짜": date_wrong,
                "복습 예정일": date_wrong + timedelta(days=3),
                "이미지": image.name if image else None
            }
            st.session_state.wrong_answers.append(entry)
            st.success("오답이 저장되었습니다!")

    st.markdown("### 📄 오답 목록")
    if st.session_state.wrong_answers:
        for i, entry in enumerate(st.session_state.wrong_answers[::-1]):
            st.markdown(f"#### ❌ {entry['과목']} - {entry['날짜']}")
            if entry["이미지"]:
                st.image(entry["이미지"], caption="업로드된 문제 이미지", width=400)
            st.markdown(f"**문제 설명:** {entry['문제 설명']}")
            st.markdown(f"**내가 쓴 답:** {entry['내 답']}")
            st.markdown(f"**왜 그렇게 썼나:** {entry['왜 그렇게 썼는가']}")
            st.markdown(f"**정답:** {entry['정답']}")
            st.markdown(f"**오답 원인:** {', '.join(entry['오답 원인'])}")
            st.markdown(f"📅 복습 예정일: {entry['복습 예정일']}")
            st.markdown("---")
    else:
        st.info("아직 오답이 없습니다.")
