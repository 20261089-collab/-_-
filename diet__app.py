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

# 🏃 [대개편] BMI + 운동 부위 + 오늘 컨디션 기반 추천 시스템
with tab2:
    st.write("🏋️ **오늘 나의 상태에 딱 맞는 맞춤형 운동 프로그램**")
    
    # 입력 UI 세분화
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        target_part = st.selectbox("운동 부위 설정 🎯", ["전신", "상체 (가슴/팔)", "하체 (엉덩이/허벅지)", "코어 (복부/허리)"])
    with ex_col2:
        condition = st.selectbox("오늘의 컨디션 🌡️", ["컨디션 최고! 🔥", "보통이에요 🙂", "피곤하고 무거워요 😴"])
    with ex_col3:
        exercise_time = st.slider("운동 시간 선택(분) ⏳", 10, 120, 30)

    # 1단계: BMI 기반 강도 조절 (고체중자는 관절 부담을 줄이는 유산소/맨몸 운동 유도)
    if user_bmi >= 25.0:
        bmi_status = "고체중 (관절 보호 필요)"
        intensity_modifier = 0.7  # 운동 개수나 세트 수를 유연하게 하향 조정
    elif user_bmi < 18.5:
        bmi_status = "저체중 (근력 강화 중심)"
        intensity_modifier = 0.8  # 과도한 칼로리 소모 방지, 고중량 저반복 지향
    else:
        bmi_status = "정상 체중"
        intensity_modifier = 1.0

    # 2단계: 컨디션 계수 설정
    if condition == "컨디션 최고! 🔥":
        cond_bonus = "고강도 트레이닝 가능"
        set_count = int(4 * intensity_modifier) or 1
    elif condition == "보통이에요 🙂":
        cond_bonus = "적정 강도 유지"
        set_count = int(3 * intensity_modifier) or 1
    else:  # 피곤함
        cond_bonus = "컨디션 조절 및 스트레칭 중심"
        set_count = int(2 * intensity_modifier) or 1

    # 3단계: 부위별 운동 풀(Pool) 정의
    routines = {
        "전신": ["버피 테스트", "점핑잭(팔벌려뛰기)", "슬로우 버피", "마운틴 클라이머"],
        "상체 (가슴/팔)": ["푸쉬업", "무릎 대고 푸쉬업", "덤벨 숄더 프레스", "체어 딥스"],
        "하체 (엉덩이/허벅지)": ["스쿼트", "와이드 스쿼트", "런지", "힙 브릿지"],
        "코어 (복부/허리)": ["플랭크", "크런치", "레그 레이즈", "버드독"]
    }

    # 고체중(BMI >= 25) 관절 보호를 위한 운동 대체 로직
    if user_bmi >= 25.0:
        if "버피 테스트" in routines["전신"]: routines["전신"][0] = "슬로우 버피 (관절 보호)"
        if "푸쉬업" in routines["상체 (가슴/팔)"]: routines["상체 (가슴/팔)"][0] = "무릎 대고 푸쉬업"
        if "스쿼트" in routines["하체 (엉덩이/허벅지)"]: routines["하체 (엉덩이/허벅지)"][0] = "하프 스쿼트"

    # 컨디션이 나쁘면 무조건 가벼운 맨몸/스트레칭 형태로 멘트 변경
    selected_exercises = routines[target_part]
    
    st.info(f"📋 **분석 리포트**: {bmi_status} 상태이며, 오늘의 컨디션은 [{cond_bonus}]입니다.")
    
    st.write(f"💪 **추천 {target_part} 루틴 ({exercise_time}분 코스)**")
    if condition == "피곤하고 무거워요 😴":
        st.write(f"1️⃣ 가벼운 전신 스트레칭 및 폼롤러 루틴 (10분)")
        st.write(f"2️⃣ 저강도 {selected_exercises[1]} 및 {selected_exercises[3]} (각 {set_count}세트, 무리하지 않기)")
        st.write(f"3️⃣ 심호흡 및 마무리 걷기 ({exercise_time - 15 if exercise_time > 15 else 5}분)")
    else:
        st.write(f"1️⃣ 웜업: 제자리 걷기 또는 가벼운 스트레칭 (5분)")
        st.write(f"2️⃣ 메인 운동: 아래 동작을 순서대로 진행하세요!")
        for ex in selected_exercises[:3]:
            st.write(f"   - **{ex}**: 15회씩 총 {set_count}세트 수행")
        st.write(f"3️⃣ 유산소 마무리: 설정하신 시간에 맞춰 남은 **{max(10, exercise_time - 25)}분** 동안 유산소(걷기/인터벌)를 진행하세요.")
