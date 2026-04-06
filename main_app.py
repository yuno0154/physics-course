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

# 3. 등속 원운동 섹션
circular_motion_page = st.Page("physics_sim/circular_motion_sim.py", title="🎡 [개념] 등속 원운동 기초 탐구")
circular_motion_advanced_page = st.Page("physics_sim/circular_motion_adv_v2.py", title="🏀 [심화] 등속 원운동 심화 탐구")

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
    "📑 [수행평가] 기록 및 제출": [
        video_analysis_eval_page
    ],
    "🎡 [학습주제 3] 등속 원운동": [
        circular_motion_page,
        circular_motion_advanced_page
    ]
})

# 공통 사이드바 설정 (디자인 카드 푸터)
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="
        background-color: #f8fafc; 
        border: 1px solid #e2e8f0; 
        border-radius: 12px; 
        padding: 16px; 
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    ">
        <div style="font-size: 1.6rem; margin-bottom: 8px;">⚛️</div>
        <div style="font-weight: 700; color: #1e293b; font-size: 0.95rem; margin-bottom: 2px;">
            사곡고등학교 물리실
        </div>
        <div style="color: #64748b; font-size: 0.75rem; font-weight: 500;">
            by 수석교사 최연호
        </div>
    </div>
""", unsafe_allow_html=True)

# 상단 공통 브랜딩 헤더
st.markdown("""
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
        <span style="font-size: 1.2rem;">⚛️</span>
        <span style="font-size: 0.9rem; font-weight: 600; color: #64748b; letter-spacing: -0.025em;">
            사곡고등학교 물리실
        </span>
    </div>
""", unsafe_allow_html=True)

# 3. 실행
pg.run()
