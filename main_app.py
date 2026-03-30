import streamlit as st

# 1. 페이지 정의
home_page = st.Page("home.py", title="홈", icon="🏠", default=True)

# 학습 자료 섹션
vector_page = st.Page("physics_sim/vector_sim.py", title="위치 벡터와 변위", icon="📍")
velocity_page = st.Page("physics_sim/velocity_sim.py", title="평균 속도 탐구", icon="🚀")
projectile_page = st.Page("physics_sim/projectile_sim.py", title="가속도와 포물선 운동", icon="🏀")

# 2. 네비게이션 구성 (섹션별로 그룹화)
pg = st.navigation({
    "General": [home_page],
    "Physics Learning": [vector_page, velocity_page, projectile_page]
})

# 공통 사이드바 설정 (예: 학교 로고 등)
st.sidebar.text("사곡고등학교 물리실")

# 3. 실행
pg.run()
