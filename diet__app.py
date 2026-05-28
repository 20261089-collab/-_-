import streamlit as st

# 1. 페이지 설정
st.set_page_config(
    page_title="수룡이와 함께하는 맞춤형 다이어트",
    page_icon="🐉",
    layout="centered"
)

# 2. 음식 데이터 정의 (다이어트 건강도 태그 'is_healthy' 반영)
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
st.title("🐉 수룡이 다이어트 메이트")
st.caption("식단의 질과 칼로리를 모두 분석하는 똑똑한 다이어트 앱")

st.divider()

# 3. 사용자 정보 입력
st.header("👤 사용자 정보 입력")
name = st.text_input("이름")
gender = st.selectbox("성별", ["여자", "남자"])

col1, col2, col3 = st.columns(3)
with col1:
    age = st.number_input("나이", min_value=1, step=1)
with col2:
    height = st.number_input("키(cm)", min_value=1.0)
with col3:
    weight = st.number_input("몸무게(kg)", min_value=1.0)

activity = st.selectbox("활동량", ["거의 안 움직임", "보통", "운동 자주 함"])
goal = st.selectbox("목표", ["감량", "유지", "근육증가"])

allergy = st.text_input("알레르기 음식", value="없음")
dislike = st.text_input("싫어하는 음식", value="없음")
food_style = st.selectbox("선호 식단", ["한식", "가벼운식단", "단백질", "간단식", "분식", "중식", "양식", "일식", "간식", "패스트푸드"])

# 기초대사량 및 권장 칼로리 계산
if gender == "남자":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

if activity == "거의 안 움직임":
    daily_calorie = bmr * 1.2
elif activity == "보통":
    daily_calorie = bmr * 1.55
else:
    daily_calorie = bmr * 1.725

if goal == "감량":
    daily_calorie -= 300
elif goal == "근육증가":
    daily_calorie += 300
daily_calorie = int(daily_calorie)

st.divider()

# 4. 음식 기록 섹션
st.header("🍽️ 오늘 먹은 음식 기록")
st.caption("💡 불닭볶음면, 치킨 등 배달 음식도 여기에 솔직하게 기록해서 수룡이의 반응을 살펴보세요!")
selected_foods = st.multiselect("오늘 어떤 음식을 드셨나요?", list(foods.keys()))

total = 0
healthy_count = 0
unhealthy_count = 0

# 먹은 음식 분류 시스템
for food in selected_foods:
    total += foods[food]["calorie"]
    if foods[food]["is_healthy"]:
        healthy_count += 1
    else:
        unhealthy_count += 1

# 음식 분류 결과 화면에 예쁘게 갈라주기
if selected_foods:
    col_h, col_uh = st.columns(2)
    with col_h:
        st.write("🍏 **다이어트에 좋은 식단**")
        for food in selected_foods:
            if foods[food]["is_healthy"]:
                st.write(f"- {food} ({foods[food]['calorie']} kcal)")
    with col_uh:
        st.write("😈 **다이어트를 방해하는 식단**")
        for food in selected_foods:
            if not foods[food]["is_healthy"]:
                st.write(f"- {food} ({foods[food]['calorie']} kcal)")

# 5. 수룡이 게임화면 🐉
st.divider()
st.header("🎮 수룡이의 현재 상태")

# 수룡이 상태 결정 로직 (칼로리 오차 범위 밸런스 패치 적용!)
if total == 0:
    suryong_img = "normal_suryong.jpg"
    suryong_msg = "배가 고파요! 오늘 먹은 음식을 기록해주세요."
    status_color = "info"
elif total > daily_calorie + 150:  # 🚀 단 1칼로리가 아니라 150kcal 초과 시 살찜 처리
    suryong_img = "fat_suryong.jpg"
    suryong_msg = f"앗! 권장 칼로리({daily_calorie}kcal)를 많이 초과했어요! 수룡이가 포동포동하게 살이 쪘습니다. 😭"
    status_color = "error"
elif unhealthy_count > 0 and unhealthy_count >= healthy_count:  # 🚀 칼로리가 맞아도 불량 식단이 많을 때 살찜
    suryong_img = "fat_suryong.jpg"
    suryong_msg = f"식단에 다이어트를 방해하는 음식을 많이 먹었어요! 수룡이 몸이 붓고 살이 찌려고 해요! 👿"
    status_color = "error"
elif total < daily_calorie - 400:  # 🚀 400kcal 이상 극단적으로 안 먹으면 홀쭉이 처리
    suryong_img = "slim_suryong.jpg"
    suryong_msg = "영양이 너무 부족해요! 수룡이가 배가 고파 기운 없이 홀쭉해졌어요.. 🥺"
    status_color = "warning"
else:  # 🚀 그 사이의 안정적인 칼로리 섭취 구간은 성공!
    suryong_img = "normal_suryong.jpg"
    suryong_msg = "완벽해요! 클린하고 건강하게 목표 칼로리 채우기 성공! 수룡이가 따봉을 날립니다! 👍"
    status_color = "success"

# 화면 레이아웃 분할
col_char, col_info = st.columns([1, 1])

with col_char:
    try:
        st.image(suryong_img, use_container_width=True)
    except:
        st.error(f"⚠️ 저장소에서 '{suryong_img}' 파일을 찾을 수 없습니다.")

with col_info:
    # 📛 이름 조사 가독성 패치 (받침 유무 판단하여 '이' 자동 선택)
    if name:
        last_char = name[-1]
        if (ord(last_char) - 0xAC00) % 28 > 0:
            name_with_josa = f"{name}님"
        else:
            name_with_josa = name
        st.subheader(f"🐲 {name_with_josa}의 수룡이")
    else:
        st.subheader("🐲 사용자님의 수룡이")

    if status_color == "info":
        st.info(suryong_msg)
    elif status_color == "error":
        st.error(suryong_msg)
    elif status_color == "warning":
        st.warning(suryong_msg)
    else:
        st.success(suryong_msg)

    st.metric("목표 칼로리", f"{daily_calorie} kcal")
    st.metric("현재 섭취량", f"{total} kcal", delta=total - daily_calorie, delta_color="inverse")

st.divider()

# 6. 추천 기능들 (하단 배치)
tab1, tab2 = st.tabs(["🍱 추천 식단", "🏃 추천 운동"])

with tab1:
    st.write("✨ **수룡이가 엄선한 건강한 다이어트 추천 메뉴**")

    # 🚀 'is_healthy': True 인 건강한 식단만 골라 추천하는 철벽 방어 시스템!
    recommended = [
        f for f in foods
        if foods[f]["type"] == food_style
           and foods[f]["is_healthy"] == True
           and allergy not in f
           and dislike not in f
    ]

    # 예외 처리: 패스트푸드 같은 카테고리를 골라 건강한 추천 요리가 0개일 때
    if not recommended:
        st.warning(f"선택하신 '{food_style}' 카테고리에는 다이어트 전용 추천 식단이 없습니다. 대신 수룡이의 추천 클린 식단을 제공합니다!")
        recommended = ["샐러드", "닭가슴살", "고구마", "계란", "현미밥"]

    for f in recommended:
        st.write(f"- {f}: {foods[f]['calorie']} kcal")

with tab2:
    exercise_time = st.slider("운동 시간 선택(분)", 10, 120, 30, key="ex_slider")

    # 🚀 사용자가 설정한 '분' 단위 시간에 정밀 매칭되는 실시간 분배 운동 로직
    if goal == "감량":
        if exercise_time <= 20:
            exercise = f"빠르게 걷기 {exercise_time}분 (가볍게 땀 흘리기!)"
        elif exercise_time <= 40:
            exercise = f"유산소 번갈아 뛰기 {exercise_time - 10}분 + 스쿼트 20개 + 플랭크 1분"
        else:
            exercise = f"러닝 {exercise_time - 20}분 + 스쿼트 30개 + 런지 20개 + 플랭크 2분"
    elif goal == "근육증가":
        if exercise_time <= 20:
            half = exercise_time // 2
            exercise = f"스쿼트 {half}분 + 푸쉬업 {half}분 (맨몸 근력 집중!)"
        elif exercise_time <= 40:
            exercise = f"스쿼트 30개 + 푸쉬업 20개 + 런지 20개"
        else:
            exercise = f"부위별 웨이트 트레이닝 {exercise_time - 10}분 + 전신 스트레칭 10분"
    else:  # 유지
        if exercise_time <= 20:
            exercise = f"가벼운 전신 스트레칭 및 제자리 걷기 {exercise_time}분"
        elif exercise_time <= 40:
            exercise = f"동네 가볍게 산책하기 {exercise_time - 10}분 + 요가 10분"
        else:
            exercise = f"빠르게 걷기 {exercise_time - 15}분 + 마무리 스트레칭 15분"

    st.info(f"🏃 {name if name else '사용자'}님을 위한 {exercise_time}분 맞춤 운동 가이드")
    st.success(f"추천 루틴: {exercise}")
