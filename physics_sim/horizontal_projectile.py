import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏹 수평으로 던진 물체의 운동 분석")
st.markdown("""
높은 곳에서 수평으로 던진 물체의 운동을 실시간 애니메이션으로 관찰합니다.
자유 낙하하는 물체(빨간색 자취)와 수평 투사되는 물체(노란색 자취)의 연직 방향 위치를 실시간으로 비교해 보세요.
""")

# --- 사이드바: 입력 파라미터 ---
with st.sidebar:
    st.header("⚙️ 실험 조건 설정")
    h0 = st.slider("초기 높이 h (m)", 10.0, 100.0, 50.0, 5.0)
    v0 = st.slider("수평 초기 속도 v₀ (m/s)", 5.0, 30.0, 15.0, 1.0)
    g = 9.8
    
    st.markdown("---")
    st.subheader("📸 섬광 설정")
    dt_strobe = st.select_slider("섬광 간격 Δt (s)", options=[0.1, 0.2, 0.5, 1.0], value=0.5)
    
    st.markdown("---")
    play_btn = st.button("▶️ 시뮬레이션 시작")
    t_analysis = st.slider("⏱️ 시각 t (s) 분석", 0.0, float(np.sqrt(2 * h0 / g)), 0.0, 0.01)

# --- 물리 정보 계산 ---
t_land = np.sqrt(2 * h0 / g)

# --- 시각화 함수 ---
def draw_horizontal_frame(t_current):
    # 섬광 지점 (현재 시점까지의 섬광들)
    t_strobe = np.arange(0, t_current + 0.01, dt_strobe)
    # 1. 수평 투사체 (노란색)
    x_proj = v0 * t_strobe
    y_proj = h0 - 0.5 * g * t_strobe**2
    # 2. 자유 낙하체 (빨간색)
    x_fall = np.zeros_like(t_strobe)
    y_fall = h0 - 0.5 * g * t_strobe**2
    
    # 실시간 현재 위치
    curr_x = v0 * t_current
    curr_y = max(h0 - 0.5 * g * t_current**2, 0)

    fig = go.Figure()
    xmax = v0 * t_land * 1.2
    fig.update_xaxes(range=[-5, xmax], title="수평 거리 x (m)")
    fig.update_yaxes(range=[-5, h0 * 1.1], title="높이 y (m)")

    # 1. 궤적 점선
    t_line = np.linspace(0, t_land, 100)
    fig.add_trace(go.Scatter(x=v0*t_line, y=h0-0.5*g*t_line**2, mode='lines', showlegend=False, 
                             line=dict(color='lightgray', width=1, dash='dot')))
    
    # 2. 과거 섬광들 (자국)
    fig.add_trace(go.Scatter(x=x_fall, y=y_fall, mode='markers', name='자유 낙하 (Strobe)', 
                             marker=dict(size=12, color='rgba(255, 0, 0, 0.4)', symbol='circle')))
    fig.add_trace(go.Scatter(x=x_proj, y=y_proj, mode='markers', name='수평 투사 (Strobe)', 
                             marker=dict(size=12, color='rgba(255, 215, 0, 0.6)', symbol='circle')))

    # 3. 현재 위치 공 실시간
    fig.add_trace(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', name='수평 투사 (실시간)', 
                             marker=dict(size=20, color='gold', line=dict(width=2, color='black'))))
    fig.add_trace(go.Scatter(x=[0], y=[curr_y], mode='markers', name='자유 낙하 (실시간)', 
                             marker=dict(size=20, color='red', line=dict(width=2, color='black'))))

    # 4. 연직 방향 보조선 (같은 높이임을 강조)
    fig.add_trace(go.Scatter(x=[0, curr_x], y=[curr_y, curr_y], mode='lines', showlegend=False,
                             line=dict(color='gray', width=1, dash='dash')))

    fig.update_layout(height=500, plot_bgcolor='white', margin=dict(l=0, r=0, t=30, b=0))
    return fig

# --- 렌더링 ---
placeholder = st.empty()

if play_btn:
    for t in np.arange(0, t_land + 0.05, 0.05):
        placeholder.plotly_chart(draw_horizontal_frame(min(t, t_land)), use_container_width=True, key=f"hori_{t}")
        time.sleep(0.01)
else:
    placeholder.plotly_chart(draw_horizontal_frame(min(t_analysis, t_land)), use_container_width=True)

# --- 분석 데이터 ---
st.divider()
st.subheader("🏁 지면 도달 분석")
c1, c2 = st.columns(2)
with c1:
    st.metric("낙하 소요 시간 (t_land)", f"{t_land:.2f} s")
with c2:
    st.metric("수평 도달 거리 (R)", f"{v0 * t_land:.2f} m")
    
st.info("💡 실시간 애니메이션을 통해 **자유 낙하하는 공**과 **수평으로 던진 공**이 매 순간 **같은 높이**에 있음을 확인하세요.")
