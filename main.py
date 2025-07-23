import streamlit as st
import random

st.set_page_config(page_title="오늘 점심 뭐 먹지?", page_icon="🍱")

st.title("🍱 오늘 점심 뭐 먹지?")
st.write("점심 메뉴 고민은 이제 그만! 아래에서 메뉴를 추천받아보세요.")

# 카테고리별 메뉴 리스트
menu_dict = {
    "한식": ["김치찌개", "된장찌개", "비빔밥", "불고기", "제육볶음", "칼국수"],
    "중식": ["짜장면", "짬뽕", "탕수육", "마라탕", "양장피"],
    "일식": ["스시", "우동", "돈까스", "가츠동", "라멘"],
    "양식": ["파스타", "피자", "스테이크", "햄버거", "리조또"],
    "분식": ["떡볶이", "김밥", "순대", "라면", "튀김"],
}

# 선택 옵션
category = st.selectbox("먹고 싶은 음식 종류를 골라보세요 🍽️", list(menu_dict.keys()))

# 사용자 정의 메뉴 추가 (옵션)
with st.expander("👉 직접 메뉴를 추가하고 싶다면 여기를 클릭!"):
    new_menu = st.text_input("추가할 메뉴 이름")
    if st.button("메뉴 추가"):
        if new_menu:
            menu_dict[category].append(new_menu)
            st.success(f"'{new_menu}' 메뉴가 '{category}' 카테고리에 추가되었습니다!")
        else:
            st.warning("메뉴 이름을 입력해주세요.")

# 추천 버튼
if st.button("✨ 점심 메뉴 추천 받기"):
    selected_menu = random.choice(menu_dict[category])
    st.subheader(f"✅ 추천 메뉴: **{selected_menu}**")
    st.balloons()
