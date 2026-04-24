import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 발사 조건 설정 (메인 페이지 최상단) ---
with st.container(border=True):
    st.markdown("### 🚀 발사 조건 설정")
    v0 = st.number_input("초기 속도 v₀ (m/s) [5.0~50.0]", min_value=5.0, max_value=50.0, value=20.0, step=1.0)
    theta_deg = st.number_input("발사 각도 θ (도) [10~85]", min_value=10, max_value=85, value=45, step=1)
    g = st.radio("🌍 중력 가속도 g (m/s²)", options=[9.8, 10.0], index=0, horizontal=True, help="계산의 편의를 위해 10으로 설정해 보세요.")
    st.info("💡 팁: 재생 중 Pause를 누르면 현재 위치에서 멈춥니다.")

theta = np.radians(theta_deg)

st.title("🏀 비스듬히 위로 던진 물체의 정밀 분석")
st.markdown("""
포물선 운동의 수평 성분과 연직 성분을 분리하여 분석합니다. 
하단의 **Play/Pause** 버튼을 사용하여 운동 과정을 멈추어가며 관찰해 보세요!
""")

# --- 물리 정보 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
t_H = vy0 / g # 최고점 도달 시간
H = (vy0**2) / (2 * g) # 최고점 높이
t_R = 2 * t_H # 지면 도달 시간
R = vx0 * t_R # 수평 도달 거리

t_steps = np.linspace(0, t_R, 60) # 60프레임 (약 1~2초 애니메이션)

# 프레임별 데이터 생성 함수
def get_oblique_frame_data(t_curr):
    t_path = np.linspace(0, t_curr, 40)
    path_x = vx0 * t_path
    path_y = vy0 * t_path - 0.5 * g * t_path**2
    curr_x = vx0 * t_curr
    curr_y = max(vy0 * t_curr - 0.5 * g * t_curr**2, 0)
    curr_vx = vx0
    curr_vy = vy0 - g * t_curr
    
    trace_path = go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='blue', width=2), name="궤적")
    trace_ball = go.Scatter(x=[curr_x], y=[curr_y], mode='markers', 
                            marker=dict(size=18, color='orange', line=dict(width=2, color='black')), 
                            name="현재 위치")
    
    scale = 0.5
    trace_vx = go.Scatter(x=[curr_x, curr_x + curr_vx*scale], y=[curr_y, curr_y], 
                          mode='lines+markers', line=dict(color='green', width=3), 
                          marker=dict(symbol="arrow-right", size=10), name="vx")
    trace_vy = go.Scatter(x=[curr_x, curr_x], y=[curr_y, curr_y + curr_vy*scale], 
                          mode='lines+markers', line=dict(color='red', width=3), 
                          marker=dict(symbol="arrow-up" if curr_vy > 0 else "arrow-down", size=10), name="vy")
    
    return [trace_path, trace_ball, trace_vx, trace_vy]

# --- Plotly 애니메이션 구성 (Play / Pause 버튼 포함) ---
initial_data = get_oblique_frame_data(0)
initial_data.append(go.Scatter(x=[vx0 * t_H], y=[H], mode='markers', marker=dict(size=12, color='red', symbol='star'), name='최고점'))

frames = [go.Frame(data=get_oblique_frame_data(t), name=str(i)) for i, t in enumerate(t_steps)]

fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        xaxis=dict(range=[-2, R * 1.2], title="수평 거리 x (m)", gridcolor='LightGray'),
        yaxis=dict(range=[-2, H * 1.5], title="높이 y (m)", gridcolor='LightGray'),
        updatemenus=[dict(
            type="buttons",
            direction="left",
            buttons=[
                dict(label="▶️ 재생 (Play)",
                     method="animate",
                     args=[None, {"frame": {"duration": 30, "redraw": False}, "fromcurrent": True}]),
                dict(label="⏸️ 정지 (Pause)",
                     method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
            ],
            pad={"r": 10, "t": 10},
            showactive=False,
            x=0.1, y=1.2
        )],
        height=600,
        plot_bgcolor='white'
    ),
    frames=frames
)

# 주요 수치 표시(어노테이션)
fig.add_annotation(x=vx0 * t_H, y=H, text=f"최고점 H={H:.2f}m", showarrow=True, arrowhead=1)
fig.add_annotation(x=R, y=0, text=f"도달 거리 R={R:.2f}m", showarrow=True, arrowhead=1)

# 애니메이션 출력
st.plotly_chart(fig, use_container_width=True)

# --- [학습지 기반 단계별 분석 표] ---
st.divider()
st.subheader("📋 포물선 운동의 수평/연직 성분 분석 단계")

analysis_data = {
    "구분": ["알짜힘(F)", "운동의 종류", "가속도(a)", "처음 속도", "t초 후 속도", "t초 후 위치", "운동 경로", "최고점 도달 시간", "최고점의 높이", "수평 도달 거리"],
    "수평 방향(x)": [
        "0 (Fx = 0)",
        "등속 직선 운동",
        "ax = 0",
        "v0x = v0 cosθ",
        "vx = v0 cosθ",
        "x = (v0 cosθ) * t",
        "포물선",
        "-",
        "-",
        "R = v0cosθ × 2tH"
    ],
    "연직 방향(y)": [
        "중력 (Fy = -mg)",
        "등가속도 직선 운동",
        "ay = -g",
        "v0y = v0 sinθ",
        "vy = v0 sinθ - gt",
        "y = (v0 sinθ) * t - 1/2gt²",
        "포물선",
        "tH = v0sinθ / g",
        "H = (v0sinθ)² / 2g",
        "지면 도달 시간 = 2tH"
    ]
}

st.table(analysis_data)

# --- 주요 결과 수치 요약 ---
st.subheader("📝 시뮬레이션 결과 요약")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**최고점 도달 시간 (tH)**: `{t_H:.2f}`초")
with c2:
    st.info(f"**최고점의 높이 (H)**: `{H:.2f}`m")
with c3:
    st.info(f"**수평 도달 거리 (R)**: `{R:.2f}`m")

with st.expander("📝 공식 학습"):
    st.latex(r"t_H = \frac{v_0 \sin\theta}{g}")
    st.latex(r"H = \frac{(v_0 \sin\theta)^2}{2g}")
    st.latex(r"R = v_0 \cos\theta \times (2t_H)")
