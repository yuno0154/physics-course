import streamlit as st

st.set_page_config(
    page_title="물리학습 지원 포털",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. 페이지 정의
home_page = st.Page("home.py", title="🏠 홈 (Home)", default=True)

# 1. 위치와 속도 섹션 (트리 구조)
vector_page = st.Page("physics_sim/vector_sim.py", title="📍 [기학] 위치 벡터와 변위")
velocity_page = st.Page("physics_sim/velocity_sim.py", title="🚀 [기학] 평균 속도 탐구")

# 2. 가속도와 포물선 운동 섹션
accel_page = st.Page("physics_sim/projectile_sim.py", title="📘 [기학] 가속도의 정의")
horizontal_page = st.Page("physics_sim/horizontal_projectile.py", title="🏹 [분석1] 수평 투사")
compare_page = st.Page("physics_sim/projectile_comparison.py", title="🧪 [보조] 수평 속도 비교")
oblique_page = st.Page("physics_sim/oblique_projectile.py", title="🏹 [분석2] 사방 투사")
excel_page = st.Page("physics_sim/projectile_analysis_excel.py", title="📊 [정밀] 데이터 분석")
video_analysis_page = st.Page("physics_sim/video_analysis.py", title="📹 [영상] 분석 보고서")
practice_page = st.Page("physics_sim/projectile_practice.py", title="📝 [마무리] 연습 문제")

# 3. 등속 원운동 섹션
circular_motion_page = st.Page("physics_sim/circular_motion_sim.py", title="🎡 [개념1] 원운동의 기초")
circular_motion_adv_page = st.Page("physics_sim/circular_motion_adv.py", title="🎡 [개념2] 원운동의 표현")
circular_motion_accel_page = st.Page("physics_sim/circular_motion_accel_vec.py", title="🎡 [분석1] 가속도와 벡터")
circular_motion_components_page = st.Page("physics_sim/circular_motion_adv_v3.py", title="🎡 [분석2] 속도 성분과 수동 조작")

# 4. 수행평가 섹션
video_analysis_eval_page = st.Page("physics_sim/video_analysis_eval.py", title="📑 [기록] 수행평가 제출")

# 네비게이션 구성
pg = st.navigation({
    "🏠 메인": [home_page],
    "📍 학습주제 1: 위치와 속도": [vector_page, velocity_page],
    "🏀 학습주제 2: 포물선 운동": [
        accel_page, 
        horizontal_page, 
        compare_page, 
        oblique_page, 
        excel_page, 
        video_analysis_page, 
        practice_page
    ],
    "📑 수행평가 지원": [
        video_analysis_eval_page
    ],
    "🎡 학습주제 3: 등속 원운동": [
        circular_motion_page,
        circular_motion_adv_page,
        circular_motion_accel_page,
        circular_motion_components_page
    ]
})

# 사이드바 카드 푸터
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center;">
        <div style="font-size: 1.6rem; margin-bottom: 8px;">⚛️</div>
        <div style="font-weight: 700; color: #1e293b; font-size: 0.9rem;">사곡고등학교 물리실</div>
        <div style="color: #64748b; font-size: 0.7rem;">Student Learning Portal v2.0</div>
    </div>
""", unsafe_allow_html=True)

# 공통 헤더
st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
        <span style="font-size: 1.2rem;">⚛️</span>
        <span style="font-size: 0.9rem; font-weight: 600; color: #64748b;">사곡고등학교 물리실</span>
    </div>
""", unsafe_allow_html=True)

pg.run()
