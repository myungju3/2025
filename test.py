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
    if q2 == "3번 이상 깼다": score -= 20
    if q3 == "여전히 피곤하다": score -= 15
    if q4 == "좋지 않다": score -= 10
    if q5 == "1시간 이상": score -= 12
    if q6 == "자주 그렇다": score -= 8
    if q7 == "예": score -= 5
    if q8 == "자주 있다": score -= 15
    if q9 == "자주 꾼다": score -= 5
    if q10 == "거의 없다": score -= 10

    # 수면 시간 보정
    if total_sleep < 6: score -= 15
    elif total_sleep > 9: score -= 8

    score = max(0, min(100, score))  # 0~100 사이로 제한

    # 결과 출력
    st.success(f"🌙 총 수면 시간: {total_sleep:.1f} 시간")
    st.success(f"✨ 수면의 질 점수: **{score}점 / 100점**")

    # 해석 메시지
    if score >= 80:
        st.info("✅ 수면의 질이 매우 좋습니다. 지금 생활 습관을 유지하세요!")
    elif score >= 60:
        st.info("😐 수면의 질이 보통 수준입니다. 카페인 섭취나 전자기기 사용을 줄이면 더 좋아질 수 있습니다.")
    else:
        st.info("⚠️ 수면의 질이 낮습니다. 규칙적인 취침 시간, 전자기기 줄이기, 수면 환경 개선이 필요합니다.")

    # -----------------------------
    # 수면 단계 시뮬레이션 그래프
    # -----------------------------
    st.subheader("📈 예상 수면 단계 변화")

    # 단계: 0=깊은수면, 1=얕은수면, 2=REM, 3=각성
    cycle = [1, 0, 1, 2]  # 얕은 → 깊은 → 얕은 → REM (90분 주기)
    stages = []
    timestamps = []

    t = sleep_dt
    while t < wake_dt:
        for c in cycle:
            stages.append(c)
            timestamps.append(t)
            t += timedelta(minutes=90/len(cycle))  # 각 단계 약 22.5분
            if t >= wake_dt:
                break

    fig, ax = plt.subplots(figsize=(10,4))
    ax.step(timestamps, stages, where="post", linewidth=2)

    # 색상과 라벨 정의
    colors = {0:"navy", 1:"skyblue", 2:"orange", 3:"red"}
    labels = {0:"깊은 수면", 1:"얕은 수면", 2:"REM", 3:"각성"}

    for i in range(len(stages)-1):
        # 색상 영역 채우기
        ax.fill_between([timestamps[i], timestamps[i+1]], stages[i], stages[i+1],
                        step="post", color=colors[stages[i]], alpha=0.3)
        # 구간 중앙에 라벨 표시
        mid_time = timestamps[i] + (timestamps[i+1] - timestamps[i]) / 2
        ax.text(mid_time, stages[i]+0.05, labels[stages[i]], 
                ha='center', va='bottom', fontsize=8, color=colors[stages[i]])

    ax.set_yticks([0,1,2,3])
    ax.set_yticklabels(["깊은 수면", "얕은 수면", "REM", "각성"])
    ax.invert_yaxis()
    ax.set_xlabel("시간")
    ax.set_ylabel("수면 단계")
    ax.set_title("예상 수면 주기 그래프")

    st.pyplot(fig)

    # 그래프 설명 (코드 보관용)
    # st.markdown("""
    # ### 📌 그래프 해설
    # - **깊은 수면 (파란색)**: 신체 회복과 성장 호르몬 분비가 활발히 일어나는 단계입니다.  
    # - **얕은 수면 (하늘색)**: 쉽게 깰 수 있는 단계로, 전체 수면의 절반 이상을 차지합니다.  
    # - **REM 수면 (주황색)**: 꿈을 꾸는 단계이며, 뇌가 활발히 활동하면서 기억과 감정을 정리합니다.  
    # - **각성 (빨간색)**: 깨어 있는 상태로, 중간중간 짧은 각성이 나타나는 것은 정상입니다.  
    #
    # 일반적으로 **90분 주기로 얕은 수면 → 깊은 수면 → REM → 얕은 수면**이 반복됩니다.  
    # 이 그래프는 입력된 취침/기상 시간을 기준으로 **예상되는 전형적인 수면 패턴**을 시뮬레이션한 것입니다.
    # """)

    # 실제 출력
    st.markdown("""
    ### 📌 그래프 해설
    - **깊은 수면 (파란색)**: 신체 회복과 성장 호르몬 분비가 활발히 일어나는 단계입니다.  
    - **얕은 수면 (하늘색)**: 쉽게 깰 수 있는 단계로, 전체 수면의 절반 이상을 차지합니다.  
    - **REM 수면 (주황색)**: 꿈을 꾸는 단계이며, 뇌가 활발히 활동하면서 기억과 감정을 정리합니다.  
    - **각성 (빨간색)**: 깨어 있는 상태로, 중간중간 짧은 각성이 나타나는 것은 정상입니다.  

    일반적으로 **90분 주기로 얕은 수면 → 깊은 수면 → REM → 얕은 수면**이 반복됩니다.  
    이 그래프는 입력된 취침/기상 시간을 기준으로 **예상되는 전형적인 수면 패턴**을 시뮬레이션한 것입니다.
    """)

