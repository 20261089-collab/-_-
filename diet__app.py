import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="수룡이와 함께하는 맞춤형 다이어트",
    page_icon="🐉",
    layout="centered"
)

# [계산 함수 정의] ---------------------------------------------
def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h**2), 1)

def calculate_bmr(weight, height, age, gender):
    if gender == "남자":
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    return round(10 * weight + 6.25 * height - 5 * age - 161)

def calculate_tdee(bmr, activity):
    factors = {
        "거의 안 움직임": 1.2,
        "가벼운 활동": 1.375,
        "보통": 1.55,
        "활발함": 1.725,
        "매우 활발": 1.9
    }
    return round(bmr * factors[activity])
# -----------------------------------------------------------------

# 2. 음식 데이터 정의
foods = {
    "김밥": {"calorie": 450, "type": "한식", "is_healthy": True},
    "참치김밥": {"calorie": 500, "type": "한식", "is_healthy": True},
    "치즈김밥": {"calorie": 530, "type": "한식", "is_healthy": False},
    "샐러드": {"calorie": 250, "type": "가벼운식단", "is_healthy": True},
    "닭가슴살": {"calorie": 165, "type": "단백질", "is_healthy": True},
    "고구마": {"calorie": 130, "type": "가벼운식단", "is_healthy": True},
    "현미밥": {"calorie": 320, "type": "한식", "is_healthy": True},

    "라면": {"calorie": 500, "type": "분식", "is_healthy": False},
    "불닭볶음면": {"calorie": 530, "type": "분식", "is_healthy": False},
    "짜장면": {"calorie": 700, "type": "중식", "is_healthy": False},
    "짬뽕": {"calorie": 650, "type": "중식", "is_healthy": False},
    "햄버거": {"calorie": 550, "type": "패스트푸드", "is_healthy": False},
    "치킨": {"calorie": 700, "type": "패스트푸드", "is_healthy": False},
    "피자": {"calorie": 800, "type": "패스트푸드", "is_healthy": False},
    "떡볶이": {"calorie": 450, "type": "분식", "is_healthy": False},
    "순대": {"calorie": 300, "type": "분식", "is_healthy": False},

    "계란": {"calorie": 80, "type": "단백질", "is_healthy": True},
    "바나나": {"calorie": 90, "type": "간식", "is_healthy": True},
    "사과": {"calorie": 100, "type": "간식", "is_healthy": True},
    "요거트": {"calorie": 120, "type": "간식", "is_healthy": True},
    "연어": {"calorie": 250, "type": "단백질", "is_healthy": True},
    "스테이크": {"calorie": 600, "type": "단백질", "is_healthy": True},
    "파스타": {"calorie": 650, "type": "양식", "is_healthy": False},
    "샌드위치": {"calorie": 400, "type": "간단식", "is_healthy": True},
    "초밥": {"calorie": 500, "type": "일식", "is_healthy": True}
}

# 앱 제목
st.title("🐉 핏메이트")
st.caption("식단의 질과 칼로리를 모두 분석하는 똑똑한 다이어트 앱")

st.divider()

# 3. 사용자 정보 입력
st.header("👤 사용자 정보 입력")
name = st.text_input("이름")
gender = st.selectbox("성별", ["여자", "남자"])

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("나이", min_value=1, step=1, value=25)
with col2:
    height = st.number_input("키(cm)", min_value=1.0, value=165.0)
with col3:
    weight = st.number_input("몸무게(kg)", min_value=1.0, value=60.0)

activity = st.selectbox("활동량", ["거의 안 움직임", "가벼운 활동", "보통", "활발함", "매우 활발"])
goal = st.selectbox("목표", ["감량", "유지", "근육증가"])

allergy = st.text_input("알레르기 음식", value="없음")
dislike = st.text_input("싫어하는 음식", value="없음")
food_style = st.selectbox("선호 식단", ["한식", "가벼운식단", "단백질", "간단식", "분식", "중식", "양식", "일식", "간식", "패스트푸드"])

# 건강 지표 계산
user_bmi = calculate_bmi(weight, height)
user_bmr = calculate_bmr(weight, height, age, gender)
user_tdee = calculate_tdee(user_bmr, activity)

if goal == "감량":
    daily_calorie = user_tdee - 300
elif goal == "근육증가":
    daily_calorie = user_tdee + 300
else:
    daily_calorie = user_tdee

st.divider()

# 4. 음식 기록 섹션
st.header("🍽️ 오늘 먹은 음식 기록")
selected_foods = st.multiselect("오늘 어떤 음식을 드셨나요?", list(foods.keys()))

total = 0
healthy_count = 0
unhealthy_count = 0

for food in selected_foods:
    total += foods[food]["calorie"]
    if foods[food]["is_healthy"]: healthy_count += 1
    else: unhealthy_count += 1

if selected_foods:
    col_h, col_uh = st.columns(2)
    with col_h:
        st.write("🍏 **다이어트에 좋은 식단**")
        for food in selected_foods:
            if foods[food]["is_healthy"]: st.write(f"- {food} ({foods[food]['calorie']} kcal)")
    with col_uh:
        st.write("😈 **다이어트를 방해하는 식단**")
        for food in selected_foods:
            if not foods[food]["is_healthy"]: st.write(f"- {food} ({foods[food]['calorie']} kcal)")

# 5. 수룡이 게임화면
st.divider()
st.header("🎮 수룡이의 현재 상태")

if total == 0:
    suryong_img = "normal_suryong.jpg"
    suryong_msg = f"배가 고파요! 오늘 먹은 음식을 기록해주세요. (현재 BMI: {user_bmi})"
    status_color = "info"
elif total > daily_calorie + 150:
    suryong_img = "fat_suryong.jpg"
    suryong_msg = f"앗! 권장 칼로리({daily_calorie}kcal)를 많이 초과했어요! 수룡이가 포동포동하게 살이 쪘습니다. 😭"
    status_color = "error"
elif unhealthy_count > 0 and unhealthy_count >= healthy_count:
    suryong_img = "fat_suryong.jpg"
    suryong_msg = f"식단에 다이어트를 방해하는 음식을 많이 먹었어요! 수룡이 몸이 붓고 살이 찌려고 해요! 👿"
    status_color = "error"
elif total < daily_calorie - 400:
    suryong_img = "slim_suryong.jpg"
    suryong_msg = "영양이 너무 부족해요! 수룡이가 배가 고파 기운 없이 홀쭉해졌어요.. 🥺"
    status_color = "warning"
else:
    suryong_img = "normal_suryong.jpg"
    suryong_msg = "완벽해요! 클린하고 건강하게 목표 칼로리 채우기 성공! 수룡이가 따봉을 날립니다! 👍"
    status_color = "success"

col_char, col_info = st.columns([1, 1])
with col_char:
    try: st.image(suryong_img, use_container_width=True)
    except: st.error(f"⚠️ 저장소에서 '{suryong_img}' 파일을 찾을 수 없습니다.")

with col_info:
    if name:
        last_char = name[-1]
        name_with_josa = f"{name}님" if (ord(last_char) - 0xAC00) % 28 > 0 else name
        st.subheader(f"🐲 {name_with_josa}의 수룡이")
    else:
        st.subheader("🐲 사용자님의 수룡이")

    if status_color == "info": st.info(suryong_msg)
    elif status_color == "error": st.error(suryong_msg)
    elif status_color == "warning": st.warning(suryong_msg)
    else: st.success(suryong_msg)

    st.metric("나의 BMI 지수", f"{user_bmi}")
    st.metric("목표 권장 칼로리", f"{daily_calorie} kcal")
    st.metric("현재 섭취량", f"{total} kcal", delta=total - daily_calorie, delta_color="inverse")

st.divider()

# 6. 추천 기능들
tab1, tab2 = st.tabs(["🍱 추천 식단", "🏃 추천 운동"])

with tab1:
    st.write("✨ **수룡이가 엄선한 건강한 다이어트 추천 메뉴**")
    recommended = [f for f in foods if foods[f]["type"] == food_style and foods[f]["is_healthy"] == True and allergy not in f and dislike not in f]
    if not recommended:
        st.warning(f"선택하신 '{food_style}' 카테고리에는 다이어트 전용 추천 식단이 없습니다. 대신 수룡이의 추천 클린 식단을 제공합니다!")
        recommended = ["샐러드", "닭가슴살", "고구마", "계란", "현미밥"]
    for f in recommended:
        st.write(f"- {f}: {foods[f]['calorie']} kcal")

# 🏃 [대개편] 헬스장 여부 필터링 및 유튜브 가이드 연동 시스템
with tab2:
    st.write("🏋️ **오늘 나의 상태에 딱 맞는 맞춤형 운동 프로그램**")
    
    # 운동 입력 세분화 (헬스장 여부 추가!)
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        place_style = st.selectbox("운동 장소 선택 🏢", ["홈트레이닝 (집)", "헬스장 (Gym)"])
    with ex_col2:
        target_part = st.selectbox("운동 부위 설정 🎯", ["전신", "상체 (가슴/팔)", "하체 (엉덩이/허벅지)", "코어 (복부/허리)"])
    with ex_col3:
        condition = st.selectbox("오늘의 컨디션 🌡️", ["컨디션 최고! 🔥", "보통이에요 🙂", "피곤하고 무거워요 😴"])

    # 가벼운 분석 안내
    bmi_status = "고체중 (관절 보호)" if user_bmi >= 25.0 else ("저체중 (근력 강화)" if user_bmi < 18.5 else "정상 체중")
    st.info(f"📋 **분석 리포트**: {bmi_status} 상태에 맞춤형 [{place_style} - {target_part}] 프로그램을 제안합니다.")

    # -------------------------------------------------------------
    # Case A: 홈트레이닝 (집) 루틴 분기
    # -------------------------------------------------------------
    if place_style == "홈트레이닝 (집)":
        st.success(f"🏠 수룡이가 추천하는 오늘의 홈트 영상 리스트입니다. 원하는 영상을 선택해 따라해보세요!")
        
        if target_part == "전신":
            st.markdown("- [추천 영상 1] [체지방 불태우는 전신 유산소 운동](https://youtu.be/gSz5n4sLENI?si=cF8UNYcY7O51vv3P)")
            st.markdown("- [추천 영상 2] [층간소음 없는 전신 다이어트 루틴](https://youtu.be/dZbPtAgofwI?si=fGf1KFgcRwkiR2LU)")
            with st.expander("ℹ️ 운동 가이드 설명 보기"):
                st.write("집에서 별도의 기구 없이 체지방을 걷어낼 수 있는 맨몸 전신 루틴입니다. 컨디션에 맞춰 속도를 조절하세요.")
                
        elif target_part == "상체 (가슴/팔)":
            st.markdown("- [추천 영상 1] [매끈하고 탄력 있는 상체 라인 만들기](https://youtu.be/2swcod5RYvU?si=PiprFfrdaW4POwqI)")
            st.markdown("- [추천 영상 2] [초보자도 쉽게 따라하는 상체 무기구 루틴](https://youtu.be/T-bVqdhqW2U?si=O7RwqaDiVpioeKs7)")
            with st.expander("ℹ️ 운동 가이드 설명 보기"):
                st.write("굽은 등과 어깨를 펴주고 상체 탄력을 잡아주는 홈트레이닝입니다. 호흡에 집중하며 동작을 수행하세요.")
                
        elif target_part == "하체 (엉덩이/허벅지)":
            st.markdown("- [추천 영상 1] [하체 비만 탈출 최고의 하체 스트레칭 & 운동](https://youtu.be/dpBYYEhdofI?si=OGiy3ZdSSRCdd__q)")
            st.markdown("- [추천 영상 2] [허벅지 안쪽 살 파괴 맨몸 하체 루틴](https://youtu.be/NDsjmxTROEo?si=Kx28BPvmyhy8FS4u)")
            with st.expander("ℹ️ 운동 가이드 설명 보기"):
                st.write("골반 교정과 허벅지 라인 정리에 효과적인 운동입니다. 고체중이신 경우 무릎 관절 통증에 유의해 가동 범위를 조절하세요.")
                
        elif target_part == "코어 (복부/허리)":
            st.markdown("- [추천 영상 1] [복부 지방 태우는 뱃살 타파 코어 루틴](https://youtu.be/jpTQdM7okkI?si=Iul-MhU62OggKOCP)")
            st.markdown("- [추천 영상 2] [허리 통증 없이 안전하게 코어 강화하기](https://youtu.be/iOSYLKBk894?si=B606cM5LgWwS1T5j)")
            with st.expander("ℹ️ 운동 가이드 설명 보기"):
                st.write("단순히 윗몸일으키기 대신 허리를 안전하게 보호하면서 복부 심층 근육을 자극하는 똑똑한 코어 훈련입니다.")

    # -------------------------------------------------------------
    # Case B: 헬스장 (Gym) 루틴 분기
    # -------------------------------------------------------------
    else:
        st.success(f"💪 수룡이가 추천하는 오늘의 헬스장 기구 루틴입니다. 기구 이름과 자세를 꼭 확인하세요!")
        
        if target_part == "상체 (가슴/팔)":
            st.markdown("- [추천 강좌] [헬스장 상체 머신 완벽 가이드](https://youtu.be/Dw8PbebpF9w?si=5NIbj8CspBo_FwZl)")
            
            with st.expander("🏋️ [기구 1] 랫 풀 다운 (Lat Pull Down) - 등 운동"):
                st.write("**자세한 설명 및 팁:**")
                st.write("1. 바를 잡고 앉아 패드에 허벅지를 단단히 고정합니다.")
                st.write("2. 가슴을 위로 활짝 열어준 상태에서 쇄골 방향으로 바를 당깁니다.")
                st.write("3. 팔의 힘이 아니라 견갑골(날개뼈)을 아래로 접는다는 느낌으로 당겨야 등에 자극이 옵니다.")
                st.write("⚠️ 주의: 허리가 과도하게 꺾이거나 어깨가 으쓱 올라가지 않도록 고정하세요.")
                
            with st.expander("🏋️ [기구 2] 체스트 프레스 (Chest Press) - 가슴 운동"):
                st.write("**자세한 설명 및 팁:**")
                st.write("1. 의자 높이를 조절하여 손잡이가 가슴 중앙 라인에 오도록 맞춥니다.")
                st.write("2. 겨드랑이에 힘을 주고 손잡이를 앞으로 강하게 밀어줍니다.")
                st.write("3. 버티면서 천천히 이완하며 처음 자세로 돌아옵니다.")
                
        elif target_part == "하체 (엉덩이/허벅지)":
            st.markdown("- [추천 강좌] [헬스장 하체 머신 완벽 가이드](https://youtu.be/Na0Dhue1oqk?si=4VvIt7heeGHHV4Yd)")
            
            with st.expander("🏋️ [기구 1] 레그 프레스 (Leg Press) - 하체 전반"):
                st.write("**자세한 설명 및 팁:**")
                st.write("1. 발판에 발을 어깨너비로 올리고 엉덩이와 등을 등받이에 완전히 밀착시킵니다.")
                st.write("2. 안전바를 풀고 무릎이 직각이 될 때까지 천천히 내렸다가, 발바닥 전체로 밀어 올립니다.")
                st.write("⚠️ 주의: 무릎을 펼 때 관절을 튕기듯 끝까지 다 펴면 부상 위험이 있으니 95%만 펴주세요.")
                
            with st.expander("🏋️ [기구 2] 레그 익스텐션 (Leg Extension) - 허벅지 앞쪽"):
                st.write("**자세한 설명 및 팁:**")
                st.write("1. 의자에 앉아 발목 패드를 조절하여 정강이 아래쪽에 위치시킵니다.")
                st.write("2. 손잡이를 꽉 쥐고 허벅지 앞쪽 힘으로 패드를 밀어 올리며 다리를 쭉 폅니다.")
                st.write("3. 내릴 때도 무게를 버티며 천천히 내려옵니다.")

        elif target_part == "코어 (복부/허리)":
            st.markdown("- [추천 숏츠 1] [행잉 레그 레이즈 꿀팁](https://youtube.com/shorts/ocMkMZya3ac?si=p89Dw6--vfRyqRNT)")
            st.markdown("- [추천 숏츠 2] [케이블 크런치로 복근 만들기](https://youtube.com/shorts/bAFDWHA7fG8?si=ez9Av_2x54NiKXtj)")
            with st.expander("ℹ️ 코어 운동 기구 및 자세 설명 보기"):
                st.write("- **행잉 레그 레이즈**: 철봉에 매달려 복부 하부 힘으로 다리를 들어 올리는 상급자 코어 운동입니다. 반동을 줄여야 효과가 큽니다.")
                st.write("- **케이블 크런치**: 케이블 머신의 무게를 활용해 무릎을 꿇고 복부를 수축시키는 상복부 기구 운동입니다. 허리가 아닌 명치를 쥐어짜는 느낌으로 진행하세요.")

        elif target_part == "전신":
            st.markdown("- [추천 숏츠 1] [헬스장 전신 버닝 루틴 추천](https://youtube.com/shorts/ul5GqyTSSIk?si=8NaZLXCPr0ykjo4M)")
            st.markdown("- [추천 숏츠 2] [머신을 활용한 전신 서킷 트레이닝](https://youtube.com/shorts/1FZYk9OyxV0?si=ZtGUBllTgPrKHTcM)")
            with st.expander("ℹ️ 전신 운동 기구 및 가이드 보기"):
                st.write("짧고 굵게 심폐지구력과 전신 근력을 동시에 사용하여 칼로리 소모를 극대화하는 서킷 프로그램입니다. 기구 간 휴식 시간을 30초 이내로 유지해 보세요.")
