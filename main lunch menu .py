import streamlit as st
import random

st.set_page_config(page_title="🍱 다이어터를 위한 점심 메뉴 추천기", page_icon="🥗")

st.title("🍱 오늘 점심 뭐 먹지?")
st.write("기분, 식단, 칼로리에 맞는 점심 메뉴를 추천해드려요!")

# 기분 리스트
moods = ["기분 좋음 😊", "기분 별로 😕", "피곤함 😩", "스트레스 😤", "신남 😆"]

# 음식 데이터: {카테고리: {기분: [(메뉴, 칼로리)]}}
menu_dict = {
    "한식": {
        "기분 좋음 😊": [("불고기", 600), ("삼계탕", 550), ("닭갈비", 580)],
        "기분 별로 😕": [("김치찌개", 500), ("된장찌개", 450)],
        "피곤함 😩": [("죽", 350), ("칼국수", 520)],
        "스트레스 😤": [("제육볶음", 650), ("부대찌개", 700)],
        "신남 😆": [("비빔밥", 550), ("떡갈비", 620)],
    },
    "양식": {
        "기분 좋음 😊": [("스테이크", 750), ("까르보나라", 800)],
        "기분 별로 😕": [("그릴치킨", 550), ("감자스프", 400)],
        "피곤함 😩": [("오믈렛", 450), ("치즈리조또", 600)],
        "스트레스 😤": [("불닭파스타", 700), ("치폴레볼", 650)],
        "신남 😆": [("피자", 750), ("햄버거", 720)],
    },
    "분식": {
        "기분 좋음 😊": [("로제떡볶이", 700), ("치즈김밥", 500)],
        "기분 별로 😕": [("라면", 450), ("김밥", 400)],
        "피곤함 😩": [("순대국", 580), ("부침개", 620)],
        "스트레스 😤": [("매운떡볶이", 650), ("라볶이", 700)],
        "신남 😆": [("튀김", 700), ("쫄면", 600)],
    },
    "저칼로리": {
        "기분 좋음 😊": [("닭가슴살 샐러드", 300), ("연어샐러드", 320)],
        "기분 별로 😕": [("두부김치", 350), ("현미죽", 280)],
        "피곤함 😩": [("야채죽", 250), ("닭죽", 270)],
        "스트레스 😤": [("곤약비빔면", 300), ("고구마샐러드", 320)],
        "신남 😆": [("단백질바 + 요거트", 250), ("그릭요거트볼", 280)],
    },
}

# UI 요소
category = st.selectbox("🍱 음식 카테고리를 선택하세요", list(menu_dict.keys()))
mood = st.radio("😌 오늘의 기분은 어떤가요?", moods)
diet_mode = st.checkbox("🥗 다이어트 모드 (저칼로리 메뉴만 추천)", value=False)

# 사용자 메뉴 추가
with st.expander("➕ 메뉴 추가하기"):
    new_menu = st.text_input("메뉴 이름")
    new_kcal = st.number_input("칼로리 (kcal)", min_value=0, max_value=2000, step=10)
    if st.button("✅ 메뉴 추가"):
        if new_menu and mood in menu_dict[category]:
            menu_dict[category][mood].append((new_menu, new_kcal))
            st.success(f"'{new_menu}' 메뉴가 추가되었습니다!")
        else:
            st.warning("메뉴 이름을 입력하거나 기분을 선택해주세요.")

# 추천 기능
if st.button("✨ 메뉴 추천 받기"):
    try:
        menu_list = menu_dict["저칼로리"][mood] if diet_mode else menu_dict[category][mood]
        if not menu_list:
            st.error("메뉴가 없습니다. 새 메뉴를 추가해 주세요.")
        else:
            menu, kcal = random.choice(menu_list)
            st.subheader(f"🥗 추천 메뉴: **{menu}**")
            st.write(f"🔥 칼로리: {kcal} kcal")
            if kcal < 400:
                st.success("👍 저칼로리 메뉴입니다!")
            elif kcal > 700:
                st.warning("⚠️ 칼로리가 다소 높아요. 참고하세요!")
            st.balloons()
    except KeyError:
        st.error("선택된 조합의 메뉴가 없어요. 메뉴를 추가해 주세요.")
