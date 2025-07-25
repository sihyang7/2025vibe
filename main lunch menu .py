import streamlit as st
import random

st.set_page_config(page_title="🍱 건강한 점심 추천기", page_icon="🥗")

st.title("🍱 오늘 점심 뭐 먹지?")
st.write("기분, 체중, 칼로리에 맞는 건강한 식사를 추천해드려요!")

# 1. 체중 입력
st.sidebar.header("⚖️ 체중 정보")
current_weight = st.sidebar.number_input("현재 체중 (kg)", min_value=30.0, max_value=200.0, step=0.5)
goal_weight = st.sidebar.number_input("목표 체중 (kg)", min_value=30.0, max_value=200.0, step=0.5)

# 2. 기분 및 다이어트 선택
moods = ["기분 좋음 😊", "기분 별로 😕", "피곤함 😩", "스트레스 😤", "신남 😆"]
category = st.selectbox("🍱 음식 카테고리를 선택하세요", ["한식", "중식", "일식", "양식", "분식", "저칼로리"])
mood = st.radio("😌 오늘의 기분은 어떤가요?", moods)
diet_mode = st.checkbox("🥗 다이어트 모드 (저칼로리 메뉴만 추천)", value=False)

# 3. 메뉴 데이터 (메뉴명, 칼로리)
menu_dict = {
    "한식": {
        "기분 좋음 😊": [("불고기", 600), ("삼계탕", 550)],
        "기분 별로 😕": [("김치찌개", 500), ("된장찌개", 450)],
        "피곤함 😩": [("죽", 350), ("칼국수", 520)],
        "스트레스 😤": [("제육볶음", 650), ("부대찌개", 700)],
        "신남 😆": [("비빔밥", 550), ("떡갈비", 620)],
    },
    "중식": {
        "기분 좋음 😊": [("마라탕", 650), ("깐풍기", 600)],
        "기분 별로 😕": [("짜장면", 550), ("볶음밥", 500)],
        "피곤함 😩": [("계란탕", 300), ("중식죽", 350)],
        "스트레스 😤": [("짬뽕", 700), ("마라샹궈", 720)],
        "신남 😆": [("탕수육", 750), ("멘보샤", 680)],
    },
    "일식": {
        "기분 좋음 😊": [("초밥", 500), ("가이센동", 550)],
        "기분 별로 😕": [("가츠동", 580), ("우동", 450)],
        "피곤함 😩": [("유부우동", 400), ("연어덮밥", 520)],
        "스트레스 😤": [("매운라멘", 700), ("카레우동", 600)],
        "신남 😆": [("규동", 560), ("치킨가라아게", 650)],
    },
    "양식": {
        "기분 좋음 😊": [("스테이크", 750), ("까르보나라", 800)],
        "기분 별로 😕": [("감자스프", 400), ("그릴치킨", 550)],
        "피곤함 😩": [("오믈렛", 450), ("리조또", 600)],
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

# 4. 메뉴 추가 기능
with st.expander("➕ 직접 메뉴 추가하기"):
    new_menu = st.text_input("메뉴 이름")
    new_kcal = st.number_input("칼로리 (kcal)", min_value=0, max_value=2000, step=10)
    if st.button("✅ 메뉴 추가"):
        if new_menu and mood in menu_dict[category]:
            menu_dict[category][mood].append((new_menu, new_kcal))
            st.success(f"'{new_menu}' 메뉴가 추가되었습니다!")
        else:
            st.warning("메뉴 이름을 입력하거나 기분을 선택해주세요.")

# 5. 추천 버튼
if st.button("✨ 메뉴 추천 받기"):
    try:
        if diet_mode:
            selected_list = menu_dict["저칼로리"][mood]
        else:
            selected_list = menu_dict[category][mood]
        if not selected_list:
            st.error("메뉴가 없습니다. 새 메뉴를 추가해 주세요.")
        else:
            menu, kcal = random.choice(selected_list)
            st.subheader(f"🥗 추천 메뉴: **{menu}**")
            st.write(f"🔥 칼로리: **{kcal} kcal**")

            # 6. 운동 추천
            st.markdown("🏃 **식사 후 운동 추천:**")
            if kcal < 400:
                st.write("➡️ 가벼운 산책 30분 또는 스트레칭")
            elif kcal < 600:
                st.write("➡️ 빠르게 걷기 40분 또는 요가 1시간")
            elif kcal < 800:
                st.write("➡️ 자전거 40분 또는 홈트 30분")
            else:
                st.write("➡️ 러닝 30분 또는 헬스장 유산소 40분")

            # 체중 관련 조언
            if current_weight > 0 and goal_weight > 0:
                delta = current_weight - goal_weight
                if delta > 5:
                    st.info("📉 체중 감량 목표가 있으시군요! 식단과 운동을 함께 병행해 보세요.")
                elif delta < -2:
                    st.info("📈 체중 증가가 목표라면 충분한 영양 섭취도 중요해요!")
                else:
                    st.info("💪 현재 목표와 체중의 차이가 적어요. 유지 모드로 꾸준히 관리해 보세요.")
            st.balloons()
    except KeyError:
        st.error("선택한 조건에 맞는 메뉴가 없어요. 메뉴를 추가해 주세요.")
