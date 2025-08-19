import streamlit as st

# MBTI별 직업 추천 데이터 (간단 예시)
mbti_jobs = {
    "INTJ": ["과학자", "전략 기획자", "데이터 분석가"],
    "ENTP": ["기업가", "마케터", "변호사"],
    "INFJ": ["심리상담사", "작가", "교사"],
    "ESFP": ["배우", "연예 기획자", "이벤트 플래너"],
    # 필요한 만큼 추가
}

st.set_page_config(page_title="MBTI 직업 추천", page_icon="💼")

# 타이틀
st.title("💼 MBTI 기반 직업 추천 웹앱")

# 설명
st.write("당신의 MBTI를 입력하면 적합한 직업을 추천해드려요!")

# MBTI 입력 받기
user_mbti = st.text_input("MBTI를 입력하세요 (예: INFP, ESTJ)").upper()

# 추천 버튼
if st.button("직업 추천 받기"):
    if user_mbti in mbti_jobs:
        st.success(f"✅ {user_mbti} 유형에 어울리는 직업 추천 리스트:")
        for job in mbti_jobs[user_mbti]:
            st.write(f"- {job}")
    else:
        st.warning("❌ 해당 MBTI에 대한 정보가 없어요. 다시 입력해 주세요.")
