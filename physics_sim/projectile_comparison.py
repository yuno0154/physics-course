import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 레이아웃
st.set_page_config(layout="wide")

st.title("🧪 자유 낙하 vs 수평 투사 운동 비교 (3중 비교)")
st.markdown("""
제공해주신 VPython 시뮬레이션의 로직을 바탕으로 구현되었습니다. 
서로 다른 수평 속도를 가진 세 물체의 운동을 통해 **연직 방향 운동의 동일성**과 **수평 방향 운동의 독립성**을 비교 분석합니다.
""")

# --- 사이드바: 입력 파라미터 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    h0 = st.number_input("📏 초기 높이 h (m)", min_value=1.0, max_value=200.0, value=20.0, step=1.0)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        v1 = st.number_input("v1 (m/s)", value=0.0, step=1.0)
    with col2:
        v2 = st.number_input("v2 (m/s)", value=5.0, step=1.0)
    with col3:
        v3 = st.number_input("v3 (m/s)", value=10.0, step=1.0)
        
    g = 9.8
    t_land = np.sqrt(2 * h0 / g)
    
    st.markdown("---")
    t_show = st.slider("⏱️ 시각 t (s)", 0.0, float(t_land), 0.0, 0.01)

# --- 데이터 생성 함수 ---
def get_ball_pos(v, t):
    x = v * t
    y = h0 - 0.5 * g * t**2
    return x, max(y, 0)

def get_ball_vel(v, t):
    vx = v
    vy = -g * t
    return vx, vy

colors = ['red', 'green', 'blue']
v_list = [v1, v2, v3]
labels = ['v1 (0 m/s)', 'v2 (5 m/s)', 'v3 (10 m/s)'] # 기본값이지만 실제 입력값 반영

# --- 시각화: 궤적 및 현재 위치 ---
fig_main = go.Figure()

# 격자 및 범위 설정
xmax = max(v_list) * t_land + 5
fig_main.update_xaxes(range=[-2, xmax], title="수평 거리 x (m)")
fig_main.update_yaxes(range=[-2, h0 + 5], title="높이 y (m)")

for i, v in enumerate(v_list):
    # 궤적
    t_range = np.linspace(0, t_land, 100)
    tx = v * t_range
    ty = h0 - 0.5 * g * t_range**2
    fig_main.add_trace(go.Scatter(x=tx, y=ty, mode='lines', 
                                 name=f"v{i+1}: {v} m/s", 
                                 line=dict(color=colors[i], dash='dot', width=1)))
    
    # 현재 위치의 공
    cx, cy = get_ball_pos(v, t_show)
    fig_main.add_trace(go.Scatter(x=[cx], y=[cy], mode='markers', 
                                 marker=dict(size=15, color=colors[i]),
                                 showlegend=False))

# 바닥 표시
fig_main.add_shape(type="rect", x0=-5, y0=-1, x1=xmax+5, y1=0, fillcolor="gray", opacity=0.3)

fig_main.update_layout(height=500, plot_bgcolor='white', title="실시간 운동 위치 비교")
st.plotly_chart(fig_main, use_container_width=True)

# --- 하단: 속도 그래프 (v_x, v_y) ---
st.divider()
st.subheader("📉 속도 분석 그래프")

col_left, col_right = st.columns(2)

# 공통 시간 축
t_graph = np.linspace(0, t_land, 50)

with col_left:
    # vx - t 그래프
    fig_vx = go.Figure()
    for i, v in enumerate(v_list):
        fig_vx.add_trace(go.Scatter(x=t_graph, y=[v]*len(t_graph), mode='lines', 
                                   name=f"v{i+1}", line=dict(color=colors[i])))
    # 현재 시점 표시
    fig_vx.add_vline(x=t_show, line_dash="dash", line_color="gray")
    fig_vx.update_layout(title="수평 속도(vx) - 시간(t)", xtitle="시간 (s)", ytitle="vx (m/s)", height=350)
    st.plotly_chart(fig_vx, use_container_width=True)

with col_right:
    # vy - t 그래프
    fig_vy = go.Figure()
    for i, v in enumerate(v_list):
        fig_vy.add_trace(go.Scatter(x=t_graph, y=-g*t_graph, mode='lines', 
                                   name=f"v{i+1}", line=dict(color=colors[i])))
    # 현재 시점 표시
    fig_vy.add_vline(x=t_show, line_dash="dash", line_color="gray")
    fig_vy.update_layout(title="연직 속도(vy) - 시간(t)", xtitle="시간 (s)", ytitle="vy (m/s)", height=350)
    st.plotly_chart(fig_vy, use_container_width=True)

# --- 분석 데이터 ---
st.divider()
st.subheader("📊 수치 데이터 (t = %.2f s)" % t_show)
cols = st.columns(3)
for i, v in enumerate(v_list):
    cx, cy = get_ball_pos(v, t_show)
    vx, vy = get_ball_vel(v, t_show)
    with cols[i]:
        st.markdown(f"**🔴 물체 {i+1} (v={v}m/s)**")
        st.write(f"- 위치: ({cx:.2f}, {cy:.2f})")
        st.write(f"- 속도: ({vx:.2f}, {vy:.2f})")

with st.expander("💡 시뮬레이션 결론"):
    st.markdown(f"""
    1. **연직 방향 속도 및 위치의 동일성**: 세 물체의 수평 속도가 다르더라도, 임의의 시각 $t$에서 세 물체의 **높이($y$)**와 **연직 속도($v_y$)**는 항상 같습니다.
    2. **낙하 시간의 동일성**: 모든 물체는 수평 속도와 상관없이 **동시에 지면에 도달**합니다. ($t = {t_land:.2f}$초)
    3. **수평 속도의 독립성**: 수평 속도는 시간에 따라 변하지 않으며(등속), 연직 이동 거리($y$)에도 영향을 주지 않습니다.
    """)
