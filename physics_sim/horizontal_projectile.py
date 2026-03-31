import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏹 수평으로 던진 물체의 정밀 분석")
st.markdown("""
높은 절벽에서 수평으로 던진 물체의 운동을 분석합니다. 
하단의 **Play/Pause** 버튼을 사용하여 자유 낙하 성분과 수평 성분의 차이를 관찰해 보세요!
""")

# --- 사이드바: 입력 파라미터 ---
with st.sidebar:
    st.header("⚙️ 실험 조건 설정")
    h0 = st.slider("초기 높이 h (m)", 10.0, 100.0, 50.0, 5.0)
    v0 = st.slider("수평 초기 속도 v₀ (m/s)", 5.0, 40.0, 20.0, 1.0)
    g = st.radio("🌍 중력 가속도 g (m/s²)", options=[9.8, 10.0], index=0, horizontal=True, help="계산의 편의를 위해 10으로 설정해 보세요.")
    st.divider()
    dt_strobe = st.select_slider("📸 섬광 간격 Δt (s)", options=[0.1, 0.2, 0.5, 1.0], value=0.5)
    st.info("💡 팁: 그래프 위 Play/Pause 버튼으로 제어하세요.")

# --- 물리 정보 계산 ---
t_land = np.sqrt(2 * h0 / g)
t_steps = np.linspace(0, t_land, 60) # 60프레임

# 프레임별 데이터 생성 함수
def get_horizontal_frame_data(t_curr):
    t_strobe = np.arange(0, t_curr + 0.01, dt_strobe)
    x_proj_strobe = v0 * t_strobe
    y_proj_strobe = h0 - 0.5 * g * t_strobe**2
    x_fall_strobe = np.zeros_like(t_strobe)
    y_fall_strobe = h0 - 0.5 * g * t_strobe**2
    
    curr_x = v0 * t_curr
    curr_y = max(h0 - 0.5 * g * t_curr**2, 0)
    
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
        yaxis=dict(range=[-5, h0 * 1.2], title="높이 y (m)", gridcolor='LightGray'),
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

# 애니메이션 시각적 어노테이션
fig.add_annotation(x=v0*t_land, y=0, text=f"수평 도달 거리 R={v0*t_land:.2f}m", showarrow=True, arrowhead=1)

st.plotly_chart(fig, use_container_width=True)

# --- [학습지 기반 단계별 분석 표] ---
st.divider()
st.subheader("📋 수평 투사 운동의 성분별 분석표")

analysis_data = {
    "구분": ["알짜힘(F)", "운동의 종류", "가속도(a)", "처음 속도", "t초 후 속도", "t초 후 위치", "운동 경로", "지면 도달 시간", "수평 도달 거리"],
    "수평 방향(x)": [
        "0 (Fx = 0)",
        "등속 직선 운동",
        "ax = 0",
        "v0x = v0",
        "vx = v0",
        "x = v0 * t",
        "포물선",
        "-",
        "R = v0 * t_land"
    ],
    "연직 방향(y)": [
        "중력 (Fy = -mg)",
        "등가속도 직선 운동 (자유 낙하)",
        "ay = -g",
        "v0y = 0",
        "vy = -gt",
        "y = h0 - 1/2gt²",
        "포물선 (자유 낙하와 동일)",
        "t_land = √(2h0/g)",
        "-"
    ]
}

st.table(analysis_data)

# --- 시뮬레이션 결과 요약 ---
st.subheader("📝 시뮬레이션 결과 리포트")
c1, c2, c3 = st.columns(3)
with c1:
    st.info(f"**낙하 완료 시간 (t)**: `{t_land:.2f}`초")
with c2:
    st.info(f"**수평 도달 거리 (R)**: `{v0 * t_land:.2f}`m")
with c3:
    st.info(f"**지면 도달 연직 속도 (vy)**: `{g * t_land:.2f}`m/s")

with st.expander("📚 수평 투사 핵심 개념"):
    st.latex(r"x = v_0 t, \quad y = h_0 - \frac{1}{2}gt^2")
    st.latex(r"t_{land} = \sqrt{\frac{2h_0}{g}}")
    st.latex(r"R = v_0 \sqrt{\frac{2h_0}{g}}")
