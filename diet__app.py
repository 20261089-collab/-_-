import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import os
import calendar

# 1. 페이지 설정
st.set_page_config(
    page_title="수룡이와 함께하는 맞춤형 다이어트",
    page_icon="🐉",
    layout="centered"
)

# 데이터 저장을 위한 파일 경로
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
    factors = {"거의 안 움직임": 1.2, "가벼운 활동": 1.375, "보통": 1.55, "활발함": 1.725, "매우 활발": 1.9}
    return round(bmr * factors[activity])
# -----------------------------------------------------------------

# 음식 데이터 정의
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

# 🔘 상단 로고 및 제목 레이아웃
title_col1, title_col2 = st.columns([1.3, 4])
with title_col1:
    try: st.image("icon.png", width=150)
    except: st.error("⚠️ 'icon.png' 없음")
with title_col2:
    st.write("")
    st.title("핏메이트")
    st.caption("식단과 운동 기록을 매일 매일 누적하는 똑똑한 다이어트 다이어리")

st.divider()

# 🧭 사이드바 페이지 분리 시스템
st.sidebar.header("📋 메뉴 선택")
page = st.sidebar.radio("이동할 페이지를 선택하세요", ["👤 사용자 정보 입력", "🎮 수룡이 키우기"])

# -----------------------------------------------------------------
# [PAGE 1] 사용자 정보 입력
# -----------------------------------------------------------------
if page == "👤 사용자 정보 입력":
    st.header("👤 사용자 정보 및 목표 설정")
    
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

    st.subheader("🎯 운동 목표 설정")
    weekly_target = st.number_input("1주일에 운동을 몇 번 하실 건가요?", min_value=1, max_value=7, step=1, value=3)

    st.subheader("🥗 식단 선호도")
    allergy = st.text_input("알레르기 음식", value="없음")
    dislike = st.text_input("싫어하는 음식", value="없음")
    food_style = st.selectbox("선호 식단", ["한식", "가벼운식단", "단백질", "간단식", "분식", "중식", "양식", "일식", "간식", "패스트푸드"])

    # 입력된 데이터 세션 상태에 저장 (페이지 이동 시 유지용)
    st.session_state['user_info'] = {
        "name": name, "gender": gender, "age": age, "height": height, "weight": weight,
        "activity": activity, "goal": goal, "weekly_target": weekly_target,
        "allergy": allergy, "dislike": dislike, "food_style": food_style
    }
    
    st.success("✅ 정보가 임시 저장되었습니다! 왼쪽 메뉴에서 '🎮 수룡이 키우기'로 이동하여 분석을 확인하세요.")

# -----------------------------------------------------------------
# [PAGE 2] 수룡이 키우기 & 다이어트 분석/일지
# -----------------------------------------------------------------
else:
    # Page 1을 거치지 않고 바로 들어왔을 때 기본값 설정
    if 'user_info' not in st.session_state:
        st.warning("⚠️ 사용자 정보가 없습니다. 기본값으로 세팅됩니다. 정확한 분석을 위해 '사용자 정보 입력' 페이지를 먼저 채워주세요.")
        st.session_state['user_info'] = {
            "name": "수룡이", "gender": "여자", "age": 25, "height": 165.0, "weight": 60.0,
            "activity": "보통", "goal": "감량", "weekly_target": 3,
            "allergy": "없음", "dislike": "없음", "food_style": "한식"
        }

    info = st.session_state['user_info']

    st.header("🍽️ 오늘 먹은 음식 기록")
    selected_foods = st.multiselect("오늘 어떤 음식을 드셨나요?", list(foods.keys()))

    st.write("")
    analyze_button = st.button("🔍 나의 맞춤형 다이어트 분석 및 수룡이 확인하기", use_container_width=True)
    st.divider()

    if not analyze_button:
        st.info("💡 **[나의 맞춤형 다이어트 분석 및 수룡이 확인하기]** 버튼을 누르면 계산된 정보와 수룡이의 진화 상태가 나타납니다!")
    else:
        # 1. 신체 데이터 연산
        user_bmi = calculate_bmi(info["weight"], info["height"])
        user_bmr = calculate_bmr(info["weight"], info["height"], info["age"], info["gender"])
        user_tdee = calculate_tdee(user_bmr, info["activity"])

        if info["goal"] == "감량":
            daily_calorie = user_tdee - 300
        elif info["goal"] == "근육증가":
            daily_calorie = user_tdee + 300
        else:
            daily_calorie = user_tdee

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

        # 2. 데이터베이스(CSV) 분석을 통한 수룡이 레벨/퇴보 시스템 연산
        st.header("🎮 수룡이의 진화 상태창")

        # 운동 기록 계산 변수 초기화
        week_count = 0
        month_count = 0
        three_month_count = 0

        if os.path.exists(LOG_FILE):
            df_log = pd.read_csv(LOG_FILE)
            df_log["날짜_DT"] = pd.to_datetime(df_log["날짜"], errors="coerce")
            df_log = df_log.dropna(subset=["날짜_DT"])
            
            today_dt = datetime.now()
            
            # 기간별 운동 횟수 카운트 (기록이 누적되어 있는지 확인)
            week_ago = today_dt - timedelta(days=7)
            month_ago = today_dt - timedelta(days=30)
            three_month_ago = today_dt - timedelta(days=90)

            week_count = len(df_log[df_log["날짜_DT"] >= week_ago])
            month_count = len(df_log[df_log["날짜_DT"] >= month_ago])
            three_month_count = len(df_log[df_log["날짜_DT"] >= three_month_ago])

        # ⭐ [진화 및 강등(Return) 조건 엔진]
        # 기본 상태는 알 수룡이
        suryong_level = "알 수룡이"
        suryong_img = "a.jpg"
        evolution_msg = "아직 운동 횟수가 부족하여 껍질 속에 숨어있습니다. 이번 주 목표를 달성해 부화시켜 주세요!"

        # 조건 체크 (상위 단계부터 체크하여 만족 못 하면 자동 아래 단계로 강등 유지됨)
        if three_month_count >= 45:
            suryong_level = "전설 수룡이"
            suryong_img = "d.jpg"
            evolution_msg = "🏆 대박! 3달간 45회 이상 운동을 달성하여 최종 형태인 [전설 수룡이]로 신화적 진화를 이뤄냈습니다!"
        elif month_count >= 15:
            if three_month_count < 45 and suryong_level == "전설 수룡이": # 전설 조건 미달 시 강등
                suryong_level = "성장 수룡이"
                suryong_img = "c.jpg"
                evolution_msg = "⚠️ 앗! 3달 기준(45회)을 채우지 못해 전설에서 [성장 수룡이] 단계로 패널티 강등되었습니다!"
            else:
                suryong_level = "성장 수룡이"
                suryong_img = "c.jpg"
                evolution_msg = "🔥 대단해요! 한 달간 15회 이상 운동을 꾸준히 수행하여 무럭무럭 자란 [성장 수룡이]가 되었습니다!"
        elif week_count >= info["weekly_target"]:
            if month_count < 15: # 한달 조건 미달 시 강등
                suryong_level = "아기 수룡이"
                suryong_img = "b.jpg"
                evolution_msg = "⚠️ 앗! 한 달 기준(15회)을 채우지 못해 성장 단계에서 [아기 수룡이]로 한 단계 내려왔습니다!"
            else:
                suryong_level = "아기 수룡이"
                suryong_img = "b.jpg"
                evolution_msg = "👶 축하합니다! 설정하신 주간 운동 목표를 달성하여 껍질을 깨고 [아기 수룡이]로 부화했습니다!"
        else:
            # 주간 목표조차 실패했을 때 (알 수룡이로 리턴)
            suryong_level = "알 수룡이"
            suryong_img = "a.jpg"
            if week_count < info["weekly_target"] and (week_count > 0 or month_count > 0):
                evolution_msg = "😭 주간 운동 목표를 채우지 못해 수룡이가 다시 [알 수룡이] 상태로 퇴보해버렸습니다.. 다시 힘내봐요!"

        # 화면 출력
        col_char, col_info = st.columns([1, 1])
        with col_char:
            try: st.image(suryong_img, use_container_width=True, caption=f"현재 형태: {suryong_level}")
            except: st.error(f"⚠️ 폴더 내에 '{suryong_img}' 파일이 존재하지 않습니다. 이미지를 준비해주세요.")

        with col_info:
            st.subheader(f"🐲 {info['name']}님의 동반자 ({suryong_level})")
            st.info(evolution_msg)
            
            st.write(f"📊 **실시간 수룡이 진화 레이더**")
            st.write(f"- 이번주 운동 횟수: **{week_count}회** / 목표: {info['weekly_target']}회")
            st.write(f"- 30일 누적 운동 횟수: **{month_count}회** / 성장 조건: 15회")
            st.write(f"- 90일 누적 운동 횟수: **{three_month_count}회** / 전설 조건: 45회")

            st.metric("나의 BMI 지수", f"{user_bmi}")
            st.metric("목표 권장 칼로리", f"{daily_calorie} kcal")
            st.metric("오늘 섭취량", f"{total} kcal", delta=total - daily_calorie, delta_color="inverse")

        st.divider()

        # 4. 추천 기능 및 다이어트 일지 (탭 구성)
        tab1, tab2, tab3 = st.tabs(["🍱 추천 식단", "🏃 추천 운동 동영상 및 기록 저장", "📅 나의 누적 다이어트 일지"])

        with tab1:
            st.write("✨ **수룡이가 엄선한 건강한 다이어트 추천 메뉴**")
            recommended = [f for f in foods if foods[f]["type"] == info["food_style"] and foods[f]["is_healthy"] == True and info["allergy"] not in f and info["dislike"] not in f]
            if not recommended:
                st.warning(f"선택하신 '{info['food_style']}' 카테고리에는 조건에 맞는 전용 식단이 없습니다. 대신 추천 클린 식단을 제공합니다!")
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

            if place_style == "홈트레이닝 (집)":
                st.success(f"🏠 오늘의 추천 홈트 영상 링크")
                st.markdown("- [전신 홈트레이닝 영상 보러가기](https://youtu.be/gSz5n4sLENI)")
            else:
                st.success(f"💪 오늘의 헬스장 추천 루틴 강좌")
                st.markdown("- [하체 머신 사용법 강좌 보러가기](https://youtu.be/Na0Dhue1oqk)")

            st.subheader("💾 오늘의 다이어트 기록 최종 저장")
            record_date = st.date_input("기록을 저장할 날짜를 선택하세요 📆", value=date.today())

            if st.button("🔥 오늘의 운동 완료 및 기록 저장하기"):
                new_data = {
                    "날짜": record_date.strftime("%Y-%m-%d"),
                    "이름": info["name"],
                    "체중(kg)": info["weight"],
                    "BMI": user_bmi,
                    "목표 칼로리": daily_calorie,
                    "오늘 섭취량": total,
                    "운동 장소": place_style,
                    "운동 부위": target_part,
                    "오늘 컨디션": condition
                }

                if os.path.exists(LOG_FILE): df = pd.read_csv(LOG_FILE)
                else: df = pd.DataFrame(columns=new_data.keys())

                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(LOG_FILE, index=False, encoding="utf-8-sig")
                st.success("🎉 기록이 일지에 누적 저장되었습니다! 수룡이가 진화하는 데 반영됩니다.")

        with tab3:
            st.write("📅 **나의 누적 다이어트 일지**")
            if os.path.exists(LOG_FILE):
                df_log = pd.read_csv(LOG_FILE)
                st.dataframe(df_log.iloc[::-1], use_container_width=True)

                st.subheader("🗓️ 월별 운동 캘린더")
                df_log["날짜_DT"] = pd.to_datetime(df_log["날짜"], errors="coerce")
                df_log = df_log.dropna(subset=["날짜_DT"])
                
                if len(df_log) > 0:
                    latest_date = df_log["날짜_DT"].max()
                    years = sorted(df_log["날짜_DT"].dt.year.unique())
                    selected_year = st.selectbox("연도 선택", years, index=years.index(latest_date.year))
                    selected_month = st.selectbox("월 선택", list(range(1, 13)), index=latest_date.month - 1)

                    month_data = df_log[(df_log["날짜_DT"].dt.year == selected_year) & (df_log["날짜_DT"].dt.month == selected_month)]
                    exercise_days = set(month_data["날짜_DT"].dt.day)

                    cal = calendar.monthcalendar(selected_year, selected_month)
                    days_kor = ["월", "화", "수", "목", "금", "토", "일"]
                    header = st.columns(7)
                    for i, d in enumerate(days_kor): header[i].markdown(f"**{d}**")

                    for week in cal:
                        cols = st.columns(7)
                        for i, day in enumerate(week):
                            if day == 0: cols[i].write("")
                            else:
                                if day in exercise_days: cols[i].markdown(f"🟢 **{day}**")
                                else: cols[i].markdown(f"{day}")
            else:
                st.info("아직 누적된 일지 데이터가 없습니다.")
