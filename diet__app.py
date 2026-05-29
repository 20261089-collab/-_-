import streamlit as st
import pandas as pd
from datetime import datetime
import os
from streamlit_calendar import calendar  # 👈 달력 라이브러리 추가

# 1. 페이지 설정
st.set_page_config(
    page_title="수룡이와 함께하는 맞춤형 다이어트",
    page_icon="🐉",
    layout="centered"
)

# 데이터 영구 저장을 위한 파일 경로 설정
LOG_FILE = "diet_exercise_log.csv"

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
st.caption("식단과 운동 기록을 매일 매일 누적하는 똑똑한 다이어트 다이어리")

st.divider()

# 3. 사용자 정보 입력
st.header("👤 사용자 정보 입력")
name = st.text_input("이름", value="수룡이")
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

# 6. 추천 기능 및 다이어트 일지 (달력 템플릿 연동)
tab1, tab2, tab3 = st.tabs(["🍱 추천 식단", "🏃 추천 운동 및 설정", "📅 나의 캘린더 일지"])

with tab1:
    st.write("✨ **수룡이가 엄선한 건강한 다이어트 추천 메뉴**")
    recommended = [f for f in foods if foods[f]["type"] == food_style and foods[f]["is_healthy"] == True and allergy not in f and dislike not in f]
    if not recommended:
        st.warning(f"선택하신 '{food_style}' 카테고리에는 다이어트 전용 추천 식단이 없습니다. 대신 수룡이의 추천 클린 식단을 제공합니다!")
        recommended = ["샐러드", "닭가슴살", "고구마", "계란", "현미밥"]
    for f in recommended:
        st.write(f"- {f}: {foods[f]['calorie']} kcal")

with tab2:
    st.write("🏋️ **오늘 나의 상태에 딱 맞는 맞춤형 운동 프로그램**")
    
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    with ex_col1:
        place_style = st.selectbox("운동 장소 선택 🏢", ["홈트레이닝 (집)", "헬스장 (Gym)"])
    with ex_col2:
        target_part = st.selectbox("운동 부위 설정 🎯", ["전신", "상체 (가슴/팔)", "하체 (엉덩이/허벅지)", "코어 (복부/허리)"])
    with ex_col3:
        condition = st.selectbox("오늘의 컨디션 🌡️", ["컨디션 최고! 🔥", "보통이에요 🙂", "피곤하고 무거워요 😴"])

    bmi_status = "고체중 (관절 보호)" if user_bmi >= 25.0 else ("저체중 (근력 강화)" if user_bmi < 18.5 else "정상 체중")
    st.info(f"📋 **분석 리포트**: {bmi_status} 상태에 맞춤형 [{place_style} - {target_part}] 프로그램을 제안합니다.")

    if condition == "컨디션 최고! 🔥":
        cond_msg = "영상의 동작을 **최대 강도**로 완주하고 아래 추가 미션까지 도전해보세요!"
        gym_set = "4세트"
        home_mission = "💡 맨몸 스쿼트 20회 + 플랭크 1분 추가 진행!"
    elif condition == "보통이에요 🙂":
        cond_msg = "영상의 페이스를 그대로 유지하며 **정석 자세**에 집중하세요."
        gym_set = "3세트"
        home_mission = "💡 영상 가이드를 80% 이상 끈기 있게 따라하기!"
    else:
        cond_msg = "영상의 **속도를 낮추거나, 무리한 동작은 건너뛰고 스트레칭 위주**로 진행하세요."
        gym_set = "2세트 (자극 중심)"
        home_mission = "💡 너무 힘들다면 영상을 앞쪽 10분만 따라 한 뒤 휴식하기!"

    st.warning(f"🌡️ **오늘의 컨디션 케어 멘트**: {cond_msg}")

    if place_style == "홈트레이닝 (집)":
        st.success(f"🏠 오늘의 추천 홈트 영상")
        if target_part == "전신": st.markdown("- [추천 영상 1](https://youtu.be/gSz5n4sLENI) / [추천 영상 2](https://youtu.be/dZbPtAgofwI)")
        elif target_part == "상체 (가슴/팔)": st.markdown("- [추천 영상 1](https://youtu.be/2swcod5RYvU) / [추천 영상 2](https://youtu.be/T-bVqdhqW2U)")
        elif target_part == "하체 (엉덩이/허벅지)": st.markdown("- [추천 영상 1](https://youtu.be/dpBYYEhdofI) / [추천 영상 2](https://youtu.be/NDsjmxTROEo)")
        elif target_part == "코어 (복부/허리)": st.markdown("- [추천 영상 1](https://youtu.be/jpTQdM7okkI) / [추천 영상 2](https://youtu.be/iOSYLKBk894)")
        with st.expander("ℹ️ 홈트 가이드 설명 보기"): st.write(home_mission)
    else:
        st.success(f"💪 오늘의 헬스장 추천 머신 루틴 ({gym_set}씩 수행)")
        if target_part == "상체 (가슴/팔)": st.markdown("- [추천 강좌 보기](https://youtu.be/Dw8PbebpF9w)")
        elif target_part == "하체 (엉덩이/허벅지)": st.markdown("- [추천 강좌 보기](https://youtu.be/Na0Dhue1oqk)")
        elif target_part == "코어 (복부/허리)": st.markdown("- [추천 숏츠 1](https://youtube.com/shorts/ocMkMZya3ac) / [추천 숏츠 2](https://youtube.com/shorts/bAFDWHA7fG8)")
        elif target_part == "전신": st.markdown("- [추천 숏츠 1](https://youtube.com/shorts/ul5GqyTSSIk) / [추천 숏츠 2](https://youtube.com/shorts/1FZYk9OyxV0)")

    st.subheader("💾 오늘의 다이어트 기록 최종 저장")
    
    if st.button("🔥 오늘의 기록 저장하기"):
        new_data = {
            "날짜": datetime.now().strftime("%Y-%m-%d"), # 캘린더 연동을 위해 날짜 포맷 최적화
            "이름": name if name else "사용자",
            "체중(kg)": weight,
            "BMI": user_bmi,
            "목표 칼로리": daily_calorie,
            "오늘 섭취량": total,
            "운동 장소": place_style,
            "운동 부위": target_part,
            "오늘 컨디션": condition
        }
        
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE)
        else:
            df = pd.DataFrame(columns=new_data.keys())
            
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
        st.success("🎉 기록이 성공적으로 일지에 저장되었습니다! '나의 캘린더 일지' 탭을 누르면 달력에서 볼 수 있습니다.")

# 📅 [대폭 개편] 캘린더 시각화 탭
with tab3:
    st.write("📅 **수룡이 시각화 다이어트 캘린더**")
    st.caption("저장한 기록들이 날짜별로 달력 위에 배지로 예쁘게 표시됩니다.")
    
    # 달력 기본 설정 값
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
        },
        "initialView": "dayGridMonth",
        "selectable": True,
    }
    
    # 캘린더에 뿌려줄 이벤트 리스트 초기화
    calendar_events = []
    
    if os.path.exists(LOG_FILE):
        df_log = pd.read_csv(LOG_FILE)
        
        # 3-1. CSV 데이터를 풀캘린더가 인식하는 Event 객체 배열로 변환
        for _, row in df_log.iterrows():
            date_str = str(row["날짜"])
            
            # 식단 이벤트 배지 (녹색 계열)
            calendar_events.append({
                "title": f"🍏 식단: {row['오늘 섭취량']}kcal",
                "start": date_str,
                "end": date_str,
                "backgroundColor": "#2ecc71",
                "borderColor": "#2ecc71",
            })
            # 운동 이벤트 배지 (파란색 계열)
            calendar_events.append({
                "title": f"🏋️ {row['운동 장소']}-{row['운동 부위']}",
                "start": date_str,
                "end": date_str,
                "backgroundColor": "#3498db",
                "borderColor": "#3498db",
            })
            
        # 3-2. 달력 컴포넌트 화면에 렌더링
        state = calendar(events=calendar_events, options=calendar_options, key="diet_calendar")
        
        # 하단에 원본 표 데이터와 통계도 깔끔하게 서브로 유지
        st.divider()
        with st.expander("📊 누적 데이터 표 및 상세 통계 보기"):
            st.dataframe(df_log.iloc[::-1], use_container_width=True)
            col_stat1, col_stat2 = st.columns(2)
            with col_stat1:
                st.metric("총 기록 일수", f"{len(df_log)} 일")
            with col_stat2:
                avg_cal = int(df_log["오늘 섭취량"].mean()) if len(df_log) > 0 else 0
                st.metric("평균 하루 섭취 칼로리", f"{avg_cal} kcal")
                
            if st.checkbox("⚠️ 전체 기록 지우기 (초기화)"):
                if st.button("정말 삭제하시겠습니까?"):
                    os.remove(LOG_FILE)
                    st.warning("모든 다이어트 기록이 영구 삭제되었습니다. 페이지를 새로고침 해주세요.")
    else:
        # 데이터가 없을 때는 빈 달력만 기본 노출
        calendar(events=[], options=calendar_options, key="empty_calendar")
        st.info("아직 저장된 다이어트 기록이 없습니다. '추천 운동 및 설정' 탭에서 [오늘의 기록 저장하기]를 먼저 눌러보세요!")
