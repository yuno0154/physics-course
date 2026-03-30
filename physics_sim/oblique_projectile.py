import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏀 비스듬히 위로 던진 물체의 운동 분석")
st.markdown("""
이 시뮬레이션은 지면에서 비스듬히 던진 물체의 포물선 운동을 분석하기 위해 제작되었습니다.
제공된 학습지의 분석 항목에 따라 **수평 방향**과 **연직 방향**의 운동을 개별적으로 탐구해 보세요.
""")

# --- 사이드바: 초기 조건 설정 ---
with st.sidebar:
    st.header("🚀 발사 조건 설정")
    v0 = st.slider("초기 속도 v₀ (m/s)", 5.0, 50.0, 20.0, 1.0)
    theta_deg = st.slider("발사 각도 θ (도)", 10, 85, 45, 5)
    theta = np.radians(theta_deg)
    g = 9.8
    st.markdown("---")
    t_analysis = st.slider("⏱️ 시각 t (s) 분석", 0.0, 10.0, 1.0, 0.05)

# --- 물리 정보 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)

t_H = vy0 / g # 최고점 도달 시간
H = (vy0**2) / (2 * g) # 최고점 높이
t_R = 2 * t_H # 지면 도달 시간
R = vx0 * t_R # 수평 도달 거리

t_current = min(t_analysis, t_R)
curr_x = vx0 * t_current
curr_y = vy0 * t_current - 0.5 * g * t_current**2
curr_vx = vx0
curr_vy = vy0 - g * t_current

# 궤적 데이터
t_range = np.linspace(0, t_R, 100)
traj_x = vx0 * t_range
traj_y = vy0 * t_range - 0.5 * g * t_range**2

# --- 시각화 ---
fig = go.Figure()

# 축 범위
fig.update_xaxes(range=[-2, R * 1.2], title="수평 거리 x (m)")
fig.update_yaxes(range=[-2, H * 1.3], title="높이 y (m)")

# 궤적
fig.add_trace(go.Scatter(x=traj_x, y=traj_y, mode='lines', name='운동 궤적', 
                         line=dict(color='blue', width=2, dash='dot')))

# 최고점 표시
fig.add_trace(go.Scatter(x=[vx0 * t_H], y=[H], mode='markers', name='최고점', 
                         marker=dict(size=12, color='red', symbol='star')))

# 현재 위치 공
fig.add_trace(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', name='현재 위치', 
                         marker=dict(size=18, color='orange', line=dict(width=2, color='black'))))

# 현재 속도 성분 표시
scale = 0.5
fig.add_annotation(x=curr_x + curr_vx*scale, y=curr_y, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowcolor="green", arrowwidth=3, text="vx")
fig.add_annotation(x=curr_x, y=curr_y + curr_vy*scale, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowcolor="red", arrowwidth=3, text="vy")

fig.update_layout(height=600, plot_bgcolor='white', title="실시간 포물선 운동 분석 시뮬레이션")
st.plotly_chart(fig, use_container_width=True)

# --- 하단: 학습지 기반 분석 섹션 ---
st.divider()
st.subheader("📋 포물선 운동 분석표 (학습지 연계)")

left_col, right_col = st.columns(2)

with left_col:
    st.info("📉 **수평 방향(x) 운동 분석**")
    st.table({
        "구분": ["알짜힘 (Fx)", "운동의 종류", "가속도 (ax)", "처음 속도 (v0x)", f"{t_current:.1f}초 때의 속도 (vx)", f"{t_current:.1f}초 때의 위치 (x)"],
        "분석 내용": [
            "0", 
            "**등속 직선 운동**", 
            "0", 
            f"v₀ cos θ = {vx0:.2f} m/s", 
            f"{curr_vx:.2f} m/s (일정)", 
            f"x = v₀ cos θ · t = {curr_x:.2f} m"
        ]
    })

with right_col:
    st.error("📉 **연직 방향(y) 운동 분석**")
    st.table({
        "구분": ["알짜힘 (Fy)", "운동의 종류", "가속도 (ay)", "처음 속도 (v0y)", f"{t_current:.1f}초 때의 속도 (vy)", f"{t_current:.1f}초 때의 위치 (y)"],
        "분석 내용": [
            "-mg (중력)", 
            "**연직 상방 운동 (등가속도)**", 
            "-g (9.8 m/s²)", 
            f"v₀ sin θ = {vy0:.2f} m/s", 
            f"vy = v₀ sin θ - gt = {curr_vy:.2f} m/s", 
            f"y = v₀ sin θ · t - 1/2 gt² = {curr_y:.2f} m"
        ]
    })

st.divider()
st.subheader("🏁 고유 결과값 분석")
c1, c2, c3 = st.columns(3)

with c1:
    st.success("⏱️ **최고점 도달 시간 (tH)**")
    st.latex(r"t_H = \frac{v_0 \sin\theta}{g}")
    st.write(f"결과: **{t_H:.2f} s**")

with c2:
    st.success("⛰️ **최고점의 높이 (H)**")
    st.latex(r"H = \frac{v_0^2 \sin^2\theta}{2g}")
    st.write(f"결과: **{H:.2f} m**")

with c3:
    st.success("📏 **수평 도달 거리 (R)**")
    st.latex(r"R = v_0 \cos\theta \times 2t_H")
    st.write(f"결과: **{R:.2f} m**")

with st.expander("📝 학습 가이드: 운동 경로 방정식", expanded=True):
    st.markdown("""
    포물선 운동을 하는 물체의 궤적은 공기 저항을 무시할 때 다음과 같은 이차함수(포물선)를 따릅니다.
    """)
    st.latex(r"y = \tan\theta \times x - \frac{g}{2v_0^2 \cos^2\theta} x^2")
    st.info("시뮬레이션에서도 물체가 위 경로를 따라 이동하는지 확인해 보세요.")
