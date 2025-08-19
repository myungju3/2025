import streamlit as st

# MBTI별 직업 추천 데이터 (예시)
mbti_jobs = {
    "INTJ": ["🧑‍🔬 과학자", "📊 데이터 분석가", "🧭 전략 기획자"],
    "ENTP": ["💡 기업가", "📢 마케터", "⚖️ 변호사"],
    "INFJ": ["🧘 심리상담사", "✍️ 작가", "👩‍🏫 교사"],
    "ESFP": ["🎭 배우", "🎤 연예 기획자", "🎉 이벤트 플래너"],
    "ISTJ": ["📑 회계사", "🛡️ 군인", "🏛️ 공무원"],
    "ENFP": ["🎨 크리에이터", "🌍 여행 가이드", "🤝 사회 활동가"],
    "ESTJ": ["📈 경영자", "👮 경찰관", "⚙️ 프로젝트 매니저"],
    "ISFP": ["🎶 음악가", "🎨 디자이너", "🌱 환경운동가"],
}

# 페이지 설정
st.set_page_config(page_title="MBTI 직업 추천 💼", page_icon="🌟")

# 메인 타이틀
st.markdown("<h1 style='text-align: center; color: #ff69b4;'>🌟 MBTI 기반 직업 추천 🌟</h1>", unsafe_allow_html=True)
st.write("✨ 당신의 MBTI 유형을 선택하면 어울리는 직업을 추천해드려요! ✨")

# MBTI 선택 (드롭다운)
user_mbti = st.selectbox("🔮 당신의 MBTI는 무엇인가요?", options=list(mbti_jobs.keys()))

# 추천 버튼
if st.button("🚀 직업 추천 받기!"):
    st.markdown(f"<h3 style='color: #4CAF50;'>✅ {user_mbti} 유형에 어울리는 직업 리스트 💡</h3>", unsafe_allow_html=True)
    for job in mbti_jobs[user_mbti]:
        st.markdown(f"- {job}")

    st.balloons()  # 🎈 풍선 효과!
