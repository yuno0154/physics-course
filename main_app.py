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
vector_page = st.Page("physics_sim/vector_sim.py", title="\u00A0\u00A0\u00A0\u00A0└ 📍 위치 벡터와 변위")
velocity_page = st.Page("physics_sim/velocity_sim.py", title="\u00A0\u00A0\u00A0\u00A0└ 🚀 평균 속도 탐구")

# 2. 가속도와 포물선 운동 섹션 (3단계 트리 구조)
# --- 기초 이론 ---
accel_page = st.Page("physics_sim/projectile_sim.py", title="├─ 📘 기초: 가속도의 정의")

# --- 시뮬레이션 실습 ---
horizontal_page = st.Page("physics_sim/horizontal_projectile.py", title="├─ 🏹 [분석1] 수평 투사")
compare_page = st.Page("physics_sim/projectile_comparison.py", title="\u00A0\u00A0\u00A0\u00A0└ 🧪 수평 속도 비교")
oblique_page = st.Page("physics_sim/oblique_projectile.py", title="├─ 🏹 [분석2] 사방 투사")

# --- 데이터 통합 분석 ---
excel_page = st.Page("physics_sim/projectile_analysis_excel.py", title="├─ 📊 정밀 데이터 분석")
video_analysis_page = st.Page("physics_sim/video_analysis.py", title="\u00A0\u00A0\u00A0\u00A0└ 📹 영상 분석 보고서")

# --- 마무리 ---
practice_page = st.Page("physics_sim/projectile_practice.py", title="└─ 📝 확인: 연습 문제")

# 3. 수행평가 섹션
video_analysis_eval_page = st.Page("physics_sim/video_analysis_eval.py", title="\u00A0\u00A0\u00A0\u00A0└ 📑 [수행평가 1-1] 제출")

# 2. 네비게이션 구성 (3단계 트리 구조 시각화)
pg = st.navigation({
    "🏠 메인": [home_page],
    "📍 [학습주제 1] 위치와 속도": [vector_page, velocity_page],
    "🏀 [학습주제 2] 가속도와 포물선 운동": [
        accel_page, 
        horizontal_page, 
        compare_page, 
        oblique_page, 
        excel_page, 
        video_analysis_page, 
        practice_page
    ],
    "📑 [수행평가] 기록 및 제출": [video_analysis_eval_page]
})

# 공통 사이드바 설정 (예: 학교 로고 등)
st.sidebar.text("사곡고등학교 물리실")

# 3. 실행
pg.run()
