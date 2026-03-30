import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🏹 비스듬히 던진 물체의 운동 분석")
st.markdown("""
이 시뮬레이션은 지면에서 비스듬히 던진 물체의 포물선 운동을 분석합니다.
**수평 거리**, **최고 높이**, **낙하 시간** 간의 관계를 탐구해 보세요.
""")

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 발사 조건 설정")
    v0 = st.slider("초기 속도 v₀ (m/s)", 5.0, 40.0, 20.0, 1.0)
    theta_deg = st.slider("발사 각도 θ (도)", 0, 90, 45, 5)
    theta = np.radians(theta_deg)
    g = 9.8
    scale = 0.5
    
    st.markdown("---")
    st.caption("초기 속도와 발사 각도를 조절하여 궤적의 변화를 분석하세요.")

# --- 물리 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

t_land = (2 * vy0) / g if vy0 > 0 else 0
t_max_height = vy0 / g if vy0 > 0 else 0
h_max = (vy0**2) / (2 * g) if vy0 > 0 else 0
r_max = vx0 * t_land if vy0 > 0 else 0

# 궤적 생성
t_range = np.linspace(0, t_land if t_land > 0 else 1, 100)
traj_x = vx0 * t_range
traj_y = vy0 * t_range - 0.5 * g * t_range**2

# --- 시각화 ---
fig = go.Figure()

# 1. 배경 및 격자
fig.update_xaxes(range=[-1, max(traj_x)*1.2 if len(traj_x) > 0 else 10], title="수평 거리 x (m)")
fig.update_yaxes(range=[-1, max(h_max*1.2, 5)], title="높이 y (m)")

# 2. 전체 궤적
fig.add_trace(go.Scatter(x=traj_x, y=traj_y, mode='lines', name='포물선 궤적', 
                         line=dict(color='blue', width=3)))

# 3. 최고점 표시
fig.add_trace(go.Scatter(x=[vx0 * t_max_height], y=[h_max], mode='markers', 
                         name='최고점', marker=dict(size=12, color='red', symbol='star')))

# 4. 바닥 표시
fig.add_shape(type="line", x0=-10, y0=0, x1=500, y1=0, line=dict(color="black", width=2))

fig.update_layout(height=600, plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)

# --- 데이터 분석 섹션 ---
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("최대 수평 거리 (Range)", f"{r_max:.2f} m")
    st.latex(r"R = \frac{v_0^2 \sin(2\theta)}{g}")

with col2:
    st.metric("최고 높이 (Height)", f"{h_max:.2f} m")
    st.latex(r"H = \frac{v_0^2 \sin^2\theta}{2g}")

with col3:
    st.metric("체공 시간 (Time)", f"{t_land:.2f} s")
    st.latex(r"T = \frac{2v_0 \sin\theta}{g}")

with st.expander("💡 분석 노트: 각도에 따른 변화"):
    st.markdown("""
    - **최대 수평 거리**: 발사 속도가 일정할 때, 공기 저항이 없다면 **45도**일 때 가장 멀리 날아갑니다.
    - **보각 관계**: $30^\circ$와 $60^\circ$ 처럼 합이 $90^\circ$인 각도로 던지면 수평 거리가 같습니다.
    - **최고 높이와 시간**: 던지는 각도가 클수록(수직에 가까울수록) 최고 높이가 높고 체공 시간도 길어집니다.
    """)
