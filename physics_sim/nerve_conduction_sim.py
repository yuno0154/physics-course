import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# 페이지 설정
st.set_page_config(
    page_title="신경 흥분 전도 정밀 시뮬레이터",
    page_icon="🧠",
    layout="wide"
)

# --- 커스텀 CSS ---
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stNumberInput, .stSlider {
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1 {
        color: #0F172A;
        font-weight: 800;
        text-align: center;
    }
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 신경 흥분 전도 정밀 시뮬레이터")

# --- 데이터 정의 ---
def get_voltage(t):
    """4ms 주기의 막전위 변화 곡선 (표준형)"""
    # t=0: -70, t=1: -60, t=1.5: +30, t=2: 0, t=3: -80, t=4: -70
    times = [0, 1, 1.5, 2, 3, 4, 10]
    volts = [-70, -60, 30, 0, -80, -70, -70]
    if t < 0: return -70
    return np.interp(t, times, volts)

v = 1.0  # 전도 속도: 1 cm/ms
positions = [0, 1, 2, 3, 4]  # d1, d2, d3, d4, d5 (1cm 간격)
labels = ["d1", "d2", "d3", "d4", "d5"]

# --- 사이드바 및 컨트롤 ---
with st.sidebar:
    st.header("🎮 시뮬레이션 제어")
    
    # 시간 제어 (슬라이더와 입력창 동기화)
    if 'current_t' not in st.session_state:
        st.session_state.current_t = 0.0
    
    def update_slider():
        st.session_state.current_t = st.session_state.t_input

    def update_input():
        st.session_state.t_input = st.session_state.current_t

    t_current = st.slider(
        "경과 시간 (ms)", 
        0.0, 10.0, 
        key='current_t', 
        on_change=update_input,
        step=0.1
    )
    
    t_input = st.number_input(
        "직접 시간 입력 (ms)", 
        0.0, 10.0, 
        key='t_input', 
        on_change=update_slider,
        step=0.1
    )

    st.divider()
    st.info("""
    **💡 시뮬레이션 설정:**
    - **전도 속도:** 1 cm/ms
    - **측정 지점:** d1~d5 (1cm 간격)
    - **자극 시작:** d1 (0ms 시점)
    """)

# --- 메인 화면 구성 ---

# 1. 뉴런 구조 이미지 표시
st.subheader("🔬 뉴런 축삭 전도 모식도")
# 이미지 경로 설정 (생성된 이미지 사용)
image_path = "physics_sim/assets/neuron_axon.png"
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True, caption="신경 축삭을 통한 흥분 전도 및 이온 이동 모식도 (1cm 간격 지점 d1~d5)")
else:
    # 텍스트 대체
    st.warning("이미지를 로드할 수 없습니다. 경로를 확인해주세요.")

# 2. 5개 지점별 막전위 변화 그래프 (동시 표시)
st.subheader("📈 각 지점별 막전위 변화 (d1 ~ d5)")

# 그래프 데이터 생성
t_range = np.linspace(0, 10, 500)
fig = make_subplots(
    rows=5, cols=1, 
    shared_xaxes=True,
    vertical_spacing=0.05,
    subplot_titles=[f"지점 {label} (위치: {pos}cm)" for label, pos in zip(labels, positions)]
)

colors = ['#EF4444', '#10B981', '#3B82F6', '#F59E0B', '#8B5CF6']

for i, (pos, label) in enumerate(zip(positions, labels)):
    t_arrival = pos / v
    # 전체 시간 축에 대한 전압 데이터
    v_values = [get_voltage(t - t_arrival) for t in t_range]
    
    # 현재 시점의 전압
    v_now = get_voltage(t_current - t_arrival)
    
    # 곡선 추가
    fig.add_trace(
        go.Scatter(
            x=t_range, y=v_values, 
            name=label, 
            line=dict(color=colors[i], width=2),
            hovertemplate="시간: %{x}ms<br>전압: %{y}mV<extra></extra>"
        ),
        row=i+1, col=1
    )
    
    # 현재 시간 수직선 표시
    fig.add_vline(x=t_current, line_dash="dash", line_color="gray", row=i+1, col=1)
    
    # 현재 시점 포인트 표시
    fig.add_trace(
        go.Scatter(
            x=[t_current], y=[v_now],
            mode='markers',
            marker=dict(color='black', size=10, symbol='x'),
            showlegend=False
        ),
        row=i+1, col=1
    )
    
    # y축 범위 및 가이드라인
    fig.update_yaxes(range=[-90, 50], title_text="mV", row=i+1, col=1)
    fig.add_hline(y=-70, line_dash="dot", line_color="rgba(0,0,0,0.2)", row=i+1, col=1)

fig.update_layout(
    height=1000,
    showlegend=False,
    template="plotly_white",
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis5_title="경과 시간 (ms)"
)

st.plotly_chart(fig, use_container_width=True)

# 3. 실시간 요약 데이터
st.divider()
cols = st.columns(5)
for i, (pos, label) in enumerate(zip(positions, labels)):
    t_arrival = pos / v
    v_now = get_voltage(t_current - t_arrival)
    status = "자극 미도달" if t_current < t_arrival else ("회복 중" if t_current - t_arrival > 4 else "흥분 중")
    
    with cols[i]:
        st.metric(label=f"📍 지점 {label}", value=f"{round(v_now, 1)} mV")
        st.caption(f"도착 예정: {t_arrival}ms")
        if status == "흥분 중":
            st.error(status)
        elif status == "회복 중":
            st.success(status)
        else:
            st.info(status)

st.caption("※ 본 시뮬레이션은 전도 속도 1cm/ms, 막전위 변화 주기 4ms를 기준으로 제작되었습니다.")
