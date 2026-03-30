import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏹 수평으로 던진 물체의 운동 분석")
st.markdown("""
높은 곳에서 수평으로 던진 물체(노란색)와 자유 낙하하는 물체(빨간색)를 동시에 비교합니다. 
하단의 **'Play'** 버튼을 누르면 부드러운 애니메이션을 감상할 수 있습니다.
""")

# --- 사이드바: 입력 파라미터 ---
with st.sidebar:
    st.header("⚙️ 실험 조건 설정")
    h0 = st.slider("초기 높이 h (m)", 10.0, 100.0, 50.0, 5.0)
    v0 = st.slider("수평 초기 속도 v₀ (m/s)", 5.0, 30.0, 15.0, 1.0)
    g = 9.8
    st.divider()
    dt_strobe = st.select_slider("📸 섬광 간격 Δt (s)", options=[0.1, 0.2, 0.5, 1.0], value=0.5)
    st.info("💡 팁: 그래프 하단의 Play 버튼을 누르세요!")

# --- 물리 정보 계산 ---
t_land = np.sqrt(2 * h0 / g)
t_steps = np.linspace(0, t_land, 60) # 60프레임 (약 1.5초)

# 프레임별 데이터 생성 함수
def get_horizontal_frame_data(t_curr):
    # 섬광 지점 (현재 시점까지의 섬광들)
    t_strobe = np.arange(0, t_curr + 0.01, dt_strobe)
    
    # 1. 수평 투사체 (자취)
    x_proj_strobe = v0 * t_strobe
    y_proj_strobe = h0 - 0.5 * g * t_strobe**2
    # 2. 자유 낙하체 (자취)
    x_fall_strobe = np.zeros_like(t_strobe)
    y_fall_strobe = h0 - 0.5 * g * t_strobe**2
    
    # 실시간 현재 위치
    curr_x = v0 * t_curr
    curr_y = max(h0 - 0.5 * g * t_curr**2, 0)
    
    # 데이터 리스트
    # [노란색 실시간, 빨간색 실시간, 노란색 자취, 빨간색 자취, 수평 보조선]
    return [
        go.Scatter(x=[curr_x], y=[curr_y], mode='markers', marker=dict(size=20, color='gold', line=dict(width=2, color='black')), name="수평 투사 (실시간)"),
        go.Scatter(x=[0], y=[curr_y], mode='markers', marker=dict(size=20, color='red', line=dict(width=2, color='black')), name="자유 낙하 (실시간)"),
        go.Scatter(x=x_proj_strobe, y=y_proj_strobe, mode='markers', marker=dict(size=12, color='rgba(255, 215, 0, 0.6)'), name="수평 투사 자취"),
        go.Scatter(x=x_fall_strobe, y=y_fall_strobe, mode='markers', marker=dict(size=12, color='rgba(255, 0, 0, 0.4)'), name="자유 낙하 자취"),
        go.Scatter(x=[0, curr_x], y=[curr_y, curr_y], mode='lines', line=dict(color='gray', width=1, dash='dash'), showlegend=False)
    ]

# --- Plotly 애니메이션 구성 ---
initial_data = get_horizontal_frame_data(0)
xmax = v0 * t_land * 1.2
frames = [go.Frame(data=get_horizontal_frame_data(t), name=str(i)) for i, t in enumerate(t_steps)]

fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        xaxis=dict(range=[-5, xmax], title="수평 거리 x (m)", gridcolor='LightGray'),
        yaxis=dict(range=[-5, h0 * 1.1], title="높이 y (m)", gridcolor='LightGray'),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶️ 재생 (Play)",
                          method="animate",
                          args=[None, {"frame": {"duration": 30, "redraw": False},
                                       "fromcurrent": True, "transition": {"duration": 0}}])
            ]
        )],
        height=600,
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=30, b=0)
    ),
    frames=frames
)

st.plotly_chart(fig, use_container_width=True)

# 결론 분석 정보
st.divider()
st.subheader("📋 물리 핵심 개념 학습")
st.info("💡 **수평 방향 운동의 독립성**: 수평 속도와 상관없이 모든 물체는 연직 방향(중력 방향)으로 동일한 가속도`g`를 받으며 낙하합니다. 두 공의 그림자가 항상 수평선상에 놓인다는 것을 확인하세요.")
c1, c2 = st.columns(2)
with c1:
    st.metric("낙하 시간 (t_land)", f"{t_land:.2f} s")
with c2:
    st.metric("수평 도달 거리 (R)", f"{v0 * t_land:.2f} m")
