import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.set_page_config(page_title="수면 단계 자가 진단", page_icon="💤")

st.title("💤 수면 단계 자가 설문 및 분석")

st.markdown("잠자기 전과 일어난 후 느낀 점을 선택하고, 취침/기상 시간을 입력하면 수면 질을 평가해줍니다.")

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
# 설문지
# -----------------------------
st.subheader("📝 수면 자가 설문지")

q1 = st.radio("잠들기 전에 기분은 어땠나요?", 
              ["매우 편안했다", "보통이었다", "불안했다"], key="q1")
q2 = st.radio("밤중에 몇 번이나 깼나요?", 
              ["전혀 깨지 않았다", "1~2번 깼다", "3번 이상 깼다"], key="q2")
q3 = st.radio("아침에 눈을 떴을 때 기분은?", 
              ["개운하다", "보통이다", "여전히 피곤하다"], key="q3")
q4 = st.radio("일어난 후 집중력이 어떤가요?", 
              ["매우 좋다", "보통이다", "좋지 않다"], key="q4")

# -----------------------------
# 분석 버튼
# -----------------------------
if st.button("📊 결과 보기", key="result_btn"):

    total_sleep = (wake_dt - sleep_dt).seconds / 3600  # 총 수면 시간(시간 단위)

    # 점수 계산 (간단히 가중치 적용)
    score = 100
    if q1 == "불안했다": score -= 15
    if q2 == "1~2번 깼다": score -= 10
    if q2 == "3번 이상 깼다": score -= 25
    if q3 == "여전히 피곤하다": score -= 20
    if q4 == "좋지 않다": score -= 15

    if total_sleep < 6: score -= 20
    elif total_sleep > 9: score -= 10

    score = max(0, min(100, score))  # 0~100 사이로 제한

    st.success(f"🌙 총 수면 시간: {total_sleep:.1f} 시간")
    st.success(f"✨ 수면의 질 점수: **{score}점 / 100점**")

    # -----------------------------
    # 수면 단계 시뮬레이션 그래프
    # -----------------------------
    st.subheader("📈 예상 수면 단계 변화")

    # 단계: 0=깊은수면, 1=얕은수면, 2=REM, 3=각성
    cycle = [1,0,1,2]  # 얕은 → 깊은 → 얕은 → REM (90분 주기)
    stages = []
    timestamps = []

    t = sleep_dt
    while t < wake_dt:
        for c in cycle:
            stages.append(c)
            timestamps.append(t)
            t += timedelta(minutes=90/len(cycle))  # 각 단계는 약 22.5분
            if t >= wake_dt:
                break

    plt.figure(figsize=(10,4))
    plt.step(timestamps, stages, where="post")
    plt.yticks([0,1,2,3], ["깊은 수면", "얕은 수면", "REM", "각성"])
    plt.gca().invert_yaxis()
    plt.xlabel("시간")
    plt.ylabel("수면 단계")
    plt.title("예상 수면 주기 그래프")
    st.pyplot(plt)

