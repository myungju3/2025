import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="수면 단계 자가 진단", page_icon="💤")

st.title("💤 수면 단계 자가 설문 및 분석")

st.markdown("잠자기 전과 일어난 후 느낀 점, 수면 습관을 선택하고, 취침/기상 시간을 입력하면 수면 질을 평가하고 그래프로 보여줍니다.")

# -----------------------------
# 수면 시간 입력
# -----------------------------
st.subheader("🕒 수면 시간 입력")

sleep_date = st.date_input("취침 날짜", key="sleep_date")
sleep_time = st.time_input("취침 시각", key="sleep_time")
wake_date = st.date_input("기상 날짜", key="wake_date")
wake_time = st.time_input("기상 시각", key="wake_time")

sleep_dt = datetime.combine(sleep_date, sleep_time)
wake_dt = datetime.combine(wake_date, wake_time)

if wake_dt <= sleep_dt:
    st.warning("⚠️ 기상 시각은 반드시 취침 시각 이후여야 합니다!")

# -----------------------------
# 설문지 (10문항)
# -----------------------------
st.subheader("📝 수면 자가 설문지")

q1 = st.radio("1. 잠들기 전에 기분은 어땠나요?", ["매우 편안했다", "보통이었다", "불안했다"], key="q1")
q2 = st.radio("2. 밤중에 몇 번이나 깼나요?", ["전혀 깨지 않았다", "1~2번 깼다", "3번 이상 깼다"], key="q2")
q3 = st.radio("3. 아침에 눈을 떴을 때 기분은?", ["개운하다", "보통이다", "여전히 피곤하다"], key="q3")
q4 = st.radio("4. 일어난 후 집중력은 어떤가요?", ["매우 좋다", "보통이다", "좋지 않다"], key="q4")
q5 = st.radio("5. 평소 잠들기까지 걸리는 시간은?", ["10분 이내", "30분 이내", "1시간 이상"], key="q5")
q6 = st.radio("6. 스마트폰/TV를 보며 잠들었나요?", ["전혀 그렇지 않다", "가끔 그렇다", "자주 그렇다"], key="q6")
q7 = st.radio("7. 잠자기 전 카페인(커피, 차, 음료)을 섭취했나요?", ["아니오", "가끔", "예"], key="q7")
q8 = st.radio("8. 수면 중 코골이나 무호흡이 있나요?", ["없다", "가끔 있다", "자주 있다"], key="q8")
q9 = st.radio("9. 꿈을 많이 꾼다고 느끼나요?", ["거의 없다", "가끔 꾼다", "자주 꾼다"], key="q9")
q10 = st.radio("10. 아침에 일어나 활동할 의욕은?", ["매우 높다", "보통이다", "거의 없다"], key="q10")

# -----------------------------
# 분석 버튼
# -----------------------------
if st.button("📊 결과 보기", key="result_btn"):

    total_sleep = (wake_dt - sleep_dt).total_seconds() / 3600  # 총 수면 시간(시간 단위)

    # 점수 계산 (문항별 가중치)
    score = 100
    if q1 == "불안했다": score -= 10
    if q2 == "1~2번 깼다": score -= 8
    if q2 == "3번 이상 깼다": sco
