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
