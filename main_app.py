import streamlit as st

st.set_page_config(
    page_title="물리학습 지원 포털",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. 페이지 정의
home_page = st.Page("home.py", title="홈", icon="🏠", default=True)

# 1. 위치와 속도 섹션
vector_page = st.Page("physics_sim/vector_sim.py", title="위치 벡터와 변위", icon="📍")
velocity_page = st.Page("physics_sim/velocity_sim.py", title="평균 속도 탐구", icon="🚀")

# 2. 가속도와 포물선 운동 섹션
accel_page = st.Page("physics_sim/projectile_sim.py", title="가속도의 정의와 방향", icon="🏀")
horizontal_page = st.Page("physics_sim/horizontal_projectile.py", title="수평으로 던진 물체 분석", icon="🏹")
oblique_page = st.Page("physics_sim/oblique_projectile.py", title="비스듬히 던진 물체 분석", icon="🏹")
practice_page = st.Page("physics_sim/projectile_practice.py", title="연습 문제", icon="📝")

# 2. 네비게이션 구성 (섹션별로 그룹화)
pg = st.navigation({
    "🏠 메인": [home_page],
    "📍 위치와 속도": [vector_page, velocity_page],
    "🏀 가속도와 포물선 운동": [accel_page, horizontal_page, oblique_page, practice_page]
})

# 공통 사이드바 설정 (예: 학교 로고 등)
st.sidebar.text("사곡고등학교 물리실")

# 3. 실행
pg.run()
