import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# 페이지 레이아웃
st.set_page_config(layout="wide")

st.title("🧪 자유 낙하 vs 수평 투사 운동 비교 (3중 비교)")
st.markdown("""
서로 다른 수평 속도를 가진 세 물체의 운동을 통해 **연직 방향 운동의 동일성**과 **수평 방향 운동의 독립성**을 비교 분석합니다.
우측 상단의 **'시뮬레이션 시작'** 버튼을 누르면 실시간 애니메이션을 볼 수 있습니다.
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
    play_btn = st.button("▶️ 시뮬레이션 시작")
    t_slider = st.slider("⏱️ 시각 t (s) 분석", 0.0, float(t_land), 0.0, 0.01)

# --- 데이터 생성 및 시각화 함수 ---
def draw_plots(t_current):
    v_list = [v1, v2, v3]
    colors = ['red', 'green', 'blue']
    
    # 1. 메인 궤적 그래프
    fig_main = go.Figure()
    xmax = max(v_list) * t_land + 5
    fig_main.update_xaxes(range=[-2, xmax], title="수평 거리 x (m)")
    fig_main.update_yaxes(range=[-2, h0 + 5], title="높이 y (m)")
    
    for i, v in enumerate(v_list):
        # 전체 궤적 (점선)
        t_range = np.linspace(0, t_land, 100)
        fig_main.add_trace(go.Scatter(x=v*t_range, y=h0-0.5*g*t_range**2, mode='lines', 
                                     showlegend=False, line=dict(color=colors[i], dash='dot', width=1)))
        # 현재 위치
        cx = v * t_current
        cy = max(h0 - 0.5 * g * t_current**2, 0)
        fig_main.add_trace(go.Scatter(x=[cx], y=[cy], mode='markers', 
                                     name=f"v{i+1}: {v}m/s", marker=dict(size=15, color=colors[i])))
    
    fig_main.add_shape(type="rect", x0=-5, y0=-1, x1=xmax+5, y1=0, fillcolor="gray", opacity=0.3)
    fig_main.update_layout(height=450, margin=dict(l=0, r=0, t=30, b=0))

    # 2. 속도 그래프
    t_graph = np.linspace(0, t_land, 50)
    
    fig_vx = go.Figure()
    for i, v in enumerate(v_list):
        fig_vx.add_trace(go.Scatter(x=t_graph, y=[v]*len(t_graph), mode='lines', showlegend=False, line=dict(color=colors[i])))
    fig_vx.add_vline(x=t_current, line_dash="dash", line_color="black")
    fig_vx.update_layout(title="수평 속도(vx)", xaxis_title="시간(s)", yaxis_title="m/s", height=250, margin=dict(l=0, r=0, t=30, b=0))

    fig_vy = go.Figure()
    for i, v in enumerate(v_list):
        fig_vy.add_trace(go.Scatter(x=t_graph, y=-g*t_graph, mode='lines', showlegend=False, line=dict(color=colors[i])))
    fig_vy.add_vline(x=t_current, line_dash="dash", line_color="black")
    fig_vy.update_layout(title="연직 속도(vy)", xaxis_title="시간(s)", yaxis_title="m/s", height=250, margin=dict(l=0, r=0, t=30, b=0))
    
    return fig_main, fig_vx, fig_vy

# --- 실시간 렌더링 영역 ---
place_main = st.empty()
col_a, col_b = st.columns(2)
place_vx = col_a.empty()
place_vy = col_b.empty()

if play_btn:
    for t in np.arange(0, t_land + 0.05, 0.05):
        f_main, f_vx, f_vy = draw_plots(min(t, t_land))
        place_main.plotly_chart(f_main, use_container_width=True, key=f"main_{t}")
        place_vx.plotly_chart(f_vx, use_container_width=True, key=f"vx_{t}")
        place_vy.plotly_chart(f_vy, use_container_width=True, key=f"vy_{t}")
        time.sleep(0.01)
else:
    f_main, f_vx, f_vy = draw_plots(t_slider)
    place_main.plotly_chart(f_main, use_container_width=True)
    place_vx.plotly_chart(f_vx, use_container_width=True)
    place_vy.plotly_chart(f_vy, use_container_width=True)

# --- 하단 결론 (정적) ---
st.divider()
st.info("💡 모든 물체는 수평 속도와 상관없이 **동시에 지면에 도달**합니다. 연직 방향으로는 모두 동일한 중력 가속도를 받기 때문입니다.")
