import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

st.set_page_config(page_title="수면 단계 & 질 평가", page_icon="💤", layout="centered")

st.title("😴 수면 단계 자가 설문 & 수면 질 평가")

st.markdown("""
간단한 체크리스트와 수면 시간을 입력하면, 
수면 단계 그래프와 수면의 질 점수를 알려줍니다.

**⚠️ 주의: 본 앱은 의료적 진단이 아닌 참고용입니다.**
""")

# ------------------
# 1. 설문지 체크리스트
# ------------------
st.subheader("📋 수면 단계 자가 설문")

questions = [
    "눈꺼풀이 무겁고, 깜빡거리다 눈이 감기려고 한다.",
    "몸이 점점 느려지고, 근육이 풀린 느낌이 든다.",
    "갑자기 깜짝 놀라거나, 떨어지는 듯한 느낌을 경험했다.",
    "시간 감각이 흐려지고, 생각이 이어지지 않는다.",
    "꿈을 꾸는 듯한 장면이 어렴풋이 떠오른다.",
    "방금까지 무슨 생각/꿈을 했는지 기억이 애매하다.",
    "호흡이 일정하고 느려졌다.",
    "심장이 차분해지고, 몸이 무거워졌다.",
    "가끔 몸이 움찔거린다."
]

responses = []
for q in questions:
    res = st.checkbox(q)
    responses.append(1 if res else 0)

survey_score = sum(responses)

# ------------------
# 2. 취침 & 기상 시각 입력
# ------------------
st.subheader("⏰ 수면 시간 입력")

sleep_time = st.time_input("취침 시각", value=datetime.now().time())
wake_time = st.time_input("기상 시각", value=datetime.now().time())

# 수면 시간 계산
sleep_dt = datetime.combine(datetime.today(), sleep_time)
wake_dt = datetime.combine(datetime.today(), wake_time)
if wake_dt < sleep_dt:
    wake_dt = wake_dt.replace(day=wake_dt.day + 1)

sleep_duration = (wake_dt - sleep_dt).seconds / 3600  # 시간 단위

# ------------------
# 3. 수면 단계 추정 및 점수 계산
# ------------------

if st.button("📊 결과 보기"):
    # 수면 단계 추정
    if survey_score <= 3:
        stage = "각성"
    elif survey_score <= 7:
        stage = "얕은 수면"
    elif survey_score <= 10:
        stage = "깊은 수면"
    else:
        stage = "REM 수면"

    # 수면 질 점수 (단순 모델)
    quality_score = min(100, survey_score * 5 + int(sleep_duration * 10))

    st.success(f"현재 추정 수면 단계: **{stage}** 💤")
    st.metric("수면 질 점수 (100점 만점)", f"{quality_score}점")

    # ------------------
    # 4. 수면 단계 그래프 (주기적 시뮬레이션)
    # ------------------
    st.subheader("📈 수면 단계 추정 그래프")

    # 수면 단계 코드: 0=각성, 1=얕은, 2=깊은, 3=REM
    stage_labels = {0: "각성", 1: "얕은", 2: "깊은", 3: "REM"}

    hours = np.linspace(0, sleep_duration, int(sleep_duration*6))  # 10분 단위
    stages = []

    # 간단한 수면 주기 모델 (약 90분 주기)
    cycle_length = 1.5  # 시간
    for h in hours:
        cycle_pos = (h % cycle_length) / cycle_length
        if cycle_pos < 0.1:
            stages.append(0)  # 각성
        elif cycle_pos < 0.5:
            stages.append(2)  # 깊은 수면
        elif cycle_pos < 0.8:
            stages.append(1)  # 얕은 수면
        else:
            stages.append(3)  # REM 수면

    fig, ax = plt.subplots(figsize=(8,4))
    ax.plot(hours, stages, drawstyle='steps-post')
    ax.set_yticks([0,1,2,3])
    ax.set_yticklabels(["각성","얕은","깊은","REM"])
    ax.set_xlabel("수면 시간 (시간)")
    ax.set_ylabel("수면 단계")
    ax.set_title("수면 단계 변화 추정 그래프")
    st.pyplot(fig)

