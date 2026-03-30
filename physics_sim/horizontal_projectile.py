import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🏹 수평으로 던진 물체의 운동 분석")
st.markdown("""
이 시뮬레이션은 높은 곳에서 수평 방향으로 던진 물체의 운동을 분석합니다.
수평 방향의 **등속 직선 운동**과 연직 방향의 **자유 낙하 운동**이 결합된 형태를 탐구해 보세요.
""")

# --- 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 초기 조건 설정")
    h0 = st.slider("초기 높이 h (m)", 10, 100, 50, 5)
    v0 = st.slider("수평 초기 속도 v₀ (m/s)", 5.0, 30.0, 15.0, 1.0)
    g = 9.8
    
    st.markdown("---")
    t_show = st.slider("현재 시각 t (s)", 0.0, 5.0, 1.0, 0.1)

# --- 물리 계산 ---
t_land = np.sqrt(2 * h0 / g)
t_max = t_land * 1.1 # 바닥에 닿은 후 조금 더 보여줌
t_current = min(t_show, t_land)

def get_pos(t):
    x = v0 * t
    y = h0 - 0.5 * g * t**2
    return x, max(y, 0)

def get_vel(t):
    vx = v0
    vy = -g * t
    return vx, vy

# 궤적 생성
t_range = np.linspace(0, t_land, 100)
traj_x = v0 * t_range
traj_y = h0 - 0.5 * g * t_range**2

curr_x, curr_y = get_pos(t_current)
vx, vy = get_vel(t_current)

# --- 시각화 ---
fig = go.Figure()

# 1. 배경 및 격자
fig.update_xaxes(range=[-2, max(traj_x)*1.2], title="수평 거리 x (m)")
fig.update_yaxes(range=[-2, h0*1.1], title="높이 y (m)")

# 2. 건물/절벽 표현
fig.add_shape(type="rect", x0=-5, y0=0, x1=0, y1=h0, fillcolor="gray", opacity=0.3, line_width=0)

# 3. 전체 궤적
fig.add_trace(go.Scatter(x=traj_x, y=traj_y, mode='lines', name='예상 궤적', line=dict(color='gray', dash='dot')))

# 4. 현재 물체 위치
fig.add_trace(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', name='현재 위치', marker=dict(size=15, color='red')))

# 5. 속도 벡터 시각화
scale = 0.5
# 수평 속도 vx
fig.add_annotation(x=curr_x + vx*scale, y=curr_y, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=3)
fig.add_annotation(x=curr_x + vx*scale, y=curr_y, text="vx", showarrow=False, font=dict(color="blue"), yshift=10)

# 연직 속도 vy
fig.add_annotation(x=curr_x, y=curr_y + vy*scale, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowcolor="green", arrowwidth=3)
fig.add_annotation(x=curr_x, y=curr_y + vy*scale, text="vy", showarrow=False, font=dict(color="green"), xshift=15)

# 합성 속도 v
fig.add_annotation(x=curr_x + vx*scale, y=curr_y + vy*scale, ax=curr_x, ay=curr_y, xref="x", yref="y", axref="x", ayref="y",
                   showarrow=True, arrowhead=2, arrowcolor="purple", arrowwidth=3)

fig.update_layout(height=600, plot_bgcolor='white')
st.plotly_chart(fig, use_container_width=True)

# --- 데이터 분석 섹션 ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 실시간 데이터")
    st.write(f"- **현재 위치:** (x: {curr_x:.2f}m, y: {curr_y:.2f}m)")
    st.write(f"- **수평 속도 (vx):** {vx:.2f} m/s (일정)")
    st.write(f"- **연직 속도 (vy):** {vy:.2f} m/s (증가 중)")
    st.write(f"- **합성 속도 크기:** {np.sqrt(vx**2 + vy**2):.2f} m/s")

with col2:
    st.subheader("📐 운동 분석식")
    st.latex(r"x(t) = v_0 \cdot t")
    st.latex(r"y(t) = h - \frac{1}{2}gt^2")
    st.info(f"낙하 예상 시간: {t_land:.2f}초")

with st.expander("💡 학습 포인트"):
    st.markdown("""
    1. **수평 방향**: 작용하는 힘이 없으므로 **등속 직선 운동**을 합니다. ($a_x = 0$)
    2. **연직 방향**: 중력($mg$)이 일정하게 작용하여 **등가속도 운동(자유 낙하)**을 합니다. ($a_y = -g$)
    3. **독립성**: 두 방향의 운동은 서로 영향을 주지 않으며 독립적으로 진행됩니다.
    """)
