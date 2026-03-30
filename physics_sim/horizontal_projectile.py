import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 레이아웃 설정
st.set_page_config(layout="wide")

st.title("🎯 수평으로 던진 물체의 운동 분석 탐구")
st.markdown("""
이 시뮬레이션은 높은 곳에서 수평 방향으로 던진 물체의 운동을 분석하기 위한 학습 도구입니다.
좌측의 다중 섬광 사진(Strobe Photo) 효과를 통해 **수평 방향의 등속 직선 운동**과 **연직 방향의 자유 낙하 운동**의 독립성을 탐구해 보세요.
""")

# --- 사이드바: 초기 조건 설정 ---
with st.sidebar:
    st.header("⚙️ 실험 조건 설정")
    h0 = st.slider("초기 높이 h (m)", 10.0, 100.0, 50.0, 5.0)
    v0 = st.slider("수평 초기 속도 v₀ (m/s)", 5.0, 30.0, 15.0, 1.0)
    g = 9.8
    
    st.markdown("---")
    st.subheader("📸 섬광 간격 설정")
    dt_strobe = st.select_slider("섬광 간격 Δt (s)", options=[0.1, 0.2, 0.5, 1.0], value=0.5)

# --- 물리 엔진 데이터 생성 ---
t_land = np.sqrt(2 * h0 / g)
t_max = t_land * 1.05

# 궤적 생성 (선)
t_line = np.linspace(0, t_land, 200)
x_line = v0 * t_line
y_line = h0 - 0.5 * g * t_line**2

# 섬광 지점 생성 (점)
t_strobe = np.arange(0, t_land + 0.01, dt_strobe)
# 1. 수평 투사체 (노란색)
x_proj = v0 * t_strobe
y_proj = h0 - 0.5 * g * t_strobe**2
# 2. 자유 낙하체 (빨간색 - 위치 비교용)
x_fall = np.zeros_like(t_strobe)
y_fall = h0 - 0.5 * g * t_strobe**2

# --- 상단: 실시간 분석 슬라이더 ---
st.divider()
st.subheader("🔍 특정 시점에서의 상태 분석")
t_analysis = st.slider("분석할 시각 t (s) 선택", 0.0, float(t_land), 1.0, 0.05)

curr_x = v0 * t_analysis
curr_y = h0 - 0.5 * g * t_analysis**2
vx = v0
vy = -g * t_analysis
v_total = np.sqrt(vx**2 + vy**2)

# --- 시각화 (Plotly) ---
fig = go.Figure()

# 1. 배경 설정
fig.update_xaxes(range=[-5, max(x_proj)*1.2 if len(x_proj)>0 else 20], title="수평 거리 x (m)", gridcolor='lightgray')
fig.update_yaxes(range=[-5, h0*1.1], title="높이 y (m)", gridcolor='lightgray')

# 2. 자유 낙하 점 (이미지의 왼쪽 빨간 공)
fig.add_trace(go.Scatter(x=x_fall, y=y_fall, mode='markers', name='자유 낙하 (연직)', 
                         marker=dict(size=12, color='rgba(255, 0, 0, 0.6)', symbol='circle')))

# 3. 수평 투사 점 (이미지의 노란 공)
fig.add_trace(go.Scatter(x=x_proj, y=y_proj, mode='markers', name='수평 투사 (합성)', 
                         marker=dict(size=12, color='rgba(255, 215, 0, 0.8)', symbol='circle',
                                    line=dict(color='black', width=1))))

# 4. 수평 등속 운동 투영 (이미지의 상단 노란 공)
fig.add_trace(go.Scatter(x=x_proj, y=np.full_like(t_strobe, h0), mode='markers', name='수평 등속 (투영)', 
                         marker=dict(size=8, color='rgba(128, 128, 128, 0.4)', symbol='circle')))

# 5. 현재 선택된 위치 강조 및 데이터 표시
fig.add_trace(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', name='분석 지점',
                         marker=dict(size=18, color='purple', symbol='cross', line=dict(width=2, color='white'))))

# 현재 데이터 주석
fig.add_annotation(x=curr_x, y=curr_y, text=f"({curr_x:.1f}, {curr_y:.1f})<br>v={v_total:.1f}m/s",
                   showarrow=True, arrowhead=2, ax=40, ay=-40, bgcolor="white", bordercolor="purple")

# 6. 바닥 및 절벽
fig.add_shape(type="rect", x0=-10, y0=-5, x1=500, y1=0, fillcolor="lightgray", opacity=0.5, line_width=0)
fig.add_shape(type="line", x0=0, y0=0, x1=0, y1=h0, line=dict(color="black", width=2, dash="dash"))

fig.update_layout(height=600, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0),
                  legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))

st.plotly_chart(fig, use_container_width=True)

# --- 하단: 분석표 및 단계별 도출 절차 ---
st.divider()
st.subheader("📋 운동 분석표 및 도출 과정")

tab1, tab2 = st.columns(2)

with tab1:
    st.info("📉 **x축 방향 운동 분석** (수평 방향)")
    data_x = {
        "구분": ["운동의 종류", "알짜힘", "가속도", "처음 속도", "t초 때의 속도", "t초 때의 변위"],
        "분석 내용": [
            "**등속 직선 운동**", 
            "0 (공기 저항 무시)", 
            "0", 
            f"{v0} m/s", 
            f"v_x = {v0} m/s (일정)", 
            f"x = {v0} · t = {curr_x:.2f} m"
        ]
    }
    st.table(data_x)

with tab2:
    st.error("📉 **y축 방향 운동 분석** (연직 방향)")
    data_y = {
        "구분": ["운동의 종류", "알짜힘", "가속도", "처음 속도", "t초 때의 속도", "t초 때의 변위"],
        "분석 내용": [
            "**등가속도 운동 (자유 낙하)**", 
            "중력 (mg)", 
            f"g = {g} m/s² (아래)", 
            "0", 
            f"v_y = g · t = {g * t_analysis:.2f} m/s", 
            f"y = 1/2 · g · t² = {0.5 * g * t_analysis**2:.2f} m (낙하 거리)"
        ]
    }
    st.table(data_y)

st.divider()
st.subheader("🏁 최종 결과값 구하기")

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 1️⃣ 지면 도달 시간 (t_land)")
    st.latex(r"h = \frac{1}{2}gt^2 \rightarrow t = \sqrt{\frac{2h}{g}}")
    st.success(f"시간(t) = sqrt(2 · {h0} / 9.8) = **{t_land:.2f} 초**")

with col2:
    st.markdown("### 2️⃣ 수평 도달 거리 (Range)")
    st.latex(r"R = v_0 \cdot t_{land}")
    st.success(f"거리(R) = {v0} · {t_land:.2f} = **{v0 * t_land:.2f} m**")

with st.expander("📝 학습 가이드: 섬광 사진의 의미", expanded=True):
    st.markdown(f"""
    1. **연직 위치의 동일성**: 빨간 공(자유 낙하)과 노란 공(수평 투사)의 높이가 매 순간($\Delta t$ 마다) **동일함**을 알 수 있습니다.
       - 이는 수평 방향의 속도가 연직 방향의 낙하 운동에 아무런 영향을 주지 않음을 증명합니다.
    2. **수평 간격의 일정함**: 노란 공의 수평 간격은 시간 간격이 일정할 때 항상 **일정한 거리**만큼 이동합니다.
       - 이는 수평 방향으로는 힘이 작용하지 않아 속도가 변하지 않는 **등속 직선 운동**을 함을 보여줍니다.
    3. **합성 운동**: 수평 투사 운동은 이 두 독립적인 운동이 합쳐진 결과입니다.
    """)
