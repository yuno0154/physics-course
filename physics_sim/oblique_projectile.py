import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏀 비스듬히 위로 던진 물체의 운동 분석")
st.markdown("""
지면에서 특정 각도로 던진 물체의 포물선 운동을 실시간 애니메이션으로 관찰합니다.
그래프 하단의 **'재생(Play)'** 버튼을 눌러 부드러운 움직임을 확인하세요!
""")

# --- 사이드바: 발사 조건 설정 ---
with st.sidebar:
    st.header("🚀 발사 조건 설정")
    v0 = st.slider("초기 속도 v₀ (m/s)", 5.0, 50.0, 20.0, 1.0)
    theta_deg = st.slider("발사 각도 θ (도)", 10, 85, 45, 5)
    theta = np.radians(theta_deg)
    g = 9.8
    st.info("💡 팁: 그래프 하단의 Play 버튼을 누르세요!")

# --- 물리 정보 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
t_H = vy0 / g # 최고점 도달 시간
H = (vy0**2) / (2 * g) # 최고점 높이
t_R = 2 * t_H # 지면 도달 시간
R = vx0 * t_R # 수평 도달 거리

t_steps = np.linspace(0, t_R, 60) # 60프레임 (약 1~2초 애니메이션)

# 프레임별 데이터 생성 기능 함수
def get_oblique_frame_data(t_curr):
    # 궤적 (지금까지 지난 자국)
    t_path = np.linspace(0, t_curr, 40)
    path_x = vx0 * t_path
    path_y = vy0 * t_path - 0.5 * g * t_path**2
    
    # 현재 상태
    curr_x = vx0 * t_curr
    curr_y = max(vy0 * t_curr - 0.5 * g * t_curr**2, 0)
    curr_vx = vx0
    curr_vy = vy0 - g * t_curr
    
    # 1. 궤적 자취
    trace_path = go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='blue', width=2), name="궤적")
    # 2. 현재 위치 공
    trace_ball = go.Scatter(x=[curr_x], y=[curr_y], mode='markers', 
                            marker=dict(size=18, color='orange', line=dict(width=2, color='black')), 
                            name="현재 위치")
    
    # 3. 속도 화살표 (Annotation은 Frame에 포함되기 어려우므로 Scatter로 벡터 그림)
    scale = 0.5
    trace_vx = go.Scatter(x=[curr_x, curr_x + curr_vx*scale], y=[curr_y, curr_y], 
                          mode='lines+markers', line=dict(color='green', width=3), 
                          marker=dict(symbol="arrow-right", size=10), name="vx")
    trace_vy = go.Scatter(x=[curr_x, curr_x], y=[curr_y, curr_y + curr_vy*scale], 
                          mode='lines+markers', line=dict(color='red', width=3), 
                          marker=dict(symbol="arrow-up" if curr_vy > 0 else "arrow-down", size=10), name="vy")
    
    return [trace_path, trace_ball, trace_vx, trace_vy]

# --- Plotly 애니메이션 구성 ---
initial_data = get_oblique_frame_data(0)
initial_data.append(go.Scatter(x=[vx0 * t_H], y=[H], mode='markers', marker=dict(size=12, color='red', symbol='star'), name='최고점'))

frames = [go.Frame(data=get_oblique_frame_data(t), name=str(i)) for i, t in enumerate(t_steps)]

fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        xaxis=dict(range=[-2, R * 1.2], title="수평 거리 x (m)", gridcolor='LightGray'),
        yaxis=dict(range=[-2, H * 1.3], title="높이 y (m)", gridcolor='LightGray'),
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

# 정적 분석 정보
st.divider()
st.subheader("📝 물리적 분석 결과")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("최고점 높이 (H)", f"{H:.2f} m")
with c2:
    st.metric("수평 도달 거리 (R)", f"{R:.2f} m")
with c3:
    st.metric("총 낙하 시간", f"{t_R:.2f} s")
    
with st.expander("📚 공식 학습"):
    st.latex(r"H = \frac{(v_0 \sin\theta)^2}{2g}")
    st.latex(r"R = \frac{v_0^2 \sin(2\theta)}{g}")
