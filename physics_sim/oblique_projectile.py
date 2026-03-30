import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏀 비스듬히 위로 던진 물체의 운동 분석")
st.markdown("""
지면에서 비스듬히 던진 물체의 포물선 운동을 실시간 애니메이션으로 관찰합니다.
사이드바의 **'시뮬레이션 시작'** 버튼을 누르면 VPython처럼 공이 날아가는 모습을 볼 수 있습니다.
""")

# --- 사이드바: 초기 조건 설정 ---
with st.sidebar:
    st.header("🚀 발사 조건 설정")
    v0 = st.slider("초기 속도 v₀ (m/s)", 5.0, 50.0, 20.0, 1.0)
    theta_deg = st.slider("발사 각도 θ (도)", 10, 85, 45, 5)
    theta = np.radians(theta_deg)
    g = 9.8
    
    st.markdown("---")
    play_btn = st.button("▶️ 시뮬레이션 시작")
    t_analysis = st.slider("⏱️ 시각 t (s) 분석", 0.0, 10.0, 0.0, 0.05)

# --- 물리 정보 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
t_H = vy0 / g # 최고점 도달 시간
H = (vy0**2) / (2 * g) # 최고점 높이
t_R = 2 * t_H # 지면 도달 시간
R = vx0 * t_R # 수평 도달 거리

# --- 시각화 함수 ---
def draw_oblique_frame(t_current):
    # 궤적 데이터
    t_range = np.linspace(0, t_R, 100)
    traj_x = vx0 * t_range
    traj_y = vy0 * t_range - 0.5 * g * t_range**2
    
    # 현재 상태
    curr_x = vx0 * t_current
    curr_y = max(vy0 * t_current - 0.5 * g * t_current**2, 0)
    curr_vx = vx0
    curr_vy = vy0 - g * t_current

    fig = go.Figure()
    fig.update_xaxes(range=[-2, R * 1.2], title="수평 거리 x (m)")
    fig.update_yaxes(range=[-2, H * 1.3], title="높이 y (m)")
    
    # 1. 고정 요소: 전체 궤적 점선
    fig.add_trace(go.Scatter(x=traj_x, y=traj_y, mode='lines', name='예상 궤적', 
                             line=dict(color='lightgray', width=1, dash='dot')))
    
    # 2. 최고점 별표 (이미 지났거나 도달했을 때)
    if t_current >= t_H:
        fig.add_trace(go.Scatter(x=[vx0 * t_H], y=[H], mode='markers', name='최고점', 
                                 marker=dict(size=12, color='red', symbol='star')))
    
    # 3. 실시간 궤적 (현시점까지의 자취)
    t_path = np.linspace(0, t_current, 50)
    fig.add_trace(go.Scatter(x=vx0 * t_path, y=vy0 * t_path - 0.5 * g * t_path**2, 
                             mode='lines', name='이동 경로', line=dict(color='blue', width=2)))

    # 4. 현재 위치 공
    fig.add_trace(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', name='현재 위치', 
                             marker=dict(size=18, color='orange', line=dict(width=2, color='black'))))

    # 5. 속도 성분 화살표
    scale = 0.4
    fig.add_annotation(x=curr_x + curr_vx*scale, y=curr_y, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowcolor="green", arrowwidth=3, text="vx")
    fig.add_annotation(x=curr_x, y=curr_y + curr_vy*scale, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowcolor="red", arrowwidth=3, text="vy")

    fig.update_layout(height=500, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0))
    return fig

# --- 렌더링 ---
placeholder = st.empty()

if play_btn:
    for t in np.arange(0, t_R + 0.05, 0.05):
        placeholder.plotly_chart(draw_oblique_frame(min(t, t_R)), use_container_width=True, key=f"oblique_{t}")
        time.sleep(0.01)
else:
    placeholder.plotly_chart(draw_oblique_frame(min(t_analysis, t_R)), use_container_width=True)

# --- 분석 표 (정적) ---
st.divider()
st.subheader("📋 실시간 데이터 및 분석 (t = %.2f s)" % min(t_analysis if not play_btn else t_R, t_R))
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("수평 위치 (x)", f"{vx0 * min(t_analysis, t_R):.2f} m")
with c2:
    st.metric("연직 위치 (y)", f"{max(vy0 * min(t_analysis, t_R) - 0.5 * g * min(t_analysis, t_R)**2, 0):.2f} m")
with c3:
    st.metric("연직 속도 (vy)", f"{vy0 - g * min(t_analysis, t_R):.2f} m/s")

with st.expander("📝 공식 및 도출 과정 보기"):
    st.latex(r"t_H = \frac{v_0 \sin\theta}{g}, \quad R = v_0 \cos\theta \times 2t_H")
    st.write(f"최고점 도달 시간: **{t_H:.2f} s**, 수평 도달 거리: **{R:.2f} m**")
