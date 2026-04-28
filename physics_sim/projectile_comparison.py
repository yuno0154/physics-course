import streamlit as st
import plotly.graph_objects as go
import numpy as np


st.title("🏃 수평 속도에 따른 포물선 운동 비교")
st.markdown("""
세 가지 서로 다른 수평 속도를 가진 물체의 운동을 비교합니다. 
공이 움직이는 동안 **각각의 경로(궤적)**가 실시간으로 그려집니다.
하단의 **'Play'** 버튼을 클릭하여 실험을 시작하세요!
""")

# --- 시뮬레이션 설정 (메인 페이지 상단) ---
with st.container(border=True):
    st.markdown("### ⚙️ 시뮬레이션 설정")
    coll1, coll2, coll3 = st.columns(3)
    with coll1:
        v1 = st.number_input("물체 1 (Red) 속도 (m/s)", 0, 50, 0, step=1)
    with coll2:
        v2 = st.number_input("물체 2 (Green) 속도 (m/s)", 0, 50, 10, step=1)
    with coll3:
        v3 = st.number_input("물체 3 (Blue) 속도 (m/s)", 0, 50, 20, step=1)
    
    coll4, coll5 = st.columns([2, 1])
    with coll4:
        h = st.slider("초기 높이 h (m)", 10, 100, 50)
    with coll5:
        g = st.radio("🌍 중력 가속도 g (m/s²)", options=[9.8, 10.0], index=0, horizontal=True)
    
    st.info("💡 팁: 그래프 상단의 ▶️ 재생(Play) 버튼을 누르세요!")

# --- 데이터 계산 ---
t_max = np.sqrt(2 * h / g)
t_steps = np.linspace(0, t_max, 50) # 50프레임 (부드러운 주사율)

# 프레임별 데이터 생성 함수
def get_frame_data(t_curr):
    traces = []
    colors = ['red', 'green', 'blue']
    vels = [v1, v2, v3]
    
    # 각 물체에 대해 궤적(Path)과 현재 위치(Ball) 추가
    for i, v in enumerate(vels):
        # 1. 시각 t_curr까지의 궤적 데이터
        t_path = np.linspace(0, t_curr, 30)
        x_path = v * t_path
        y_path = h - 0.5 * g * t_path**2
        
        # 궤적 선 (Trace)
        traces.append(go.Scatter(x=x_path, y=y_path, mode='lines', 
                                 line=dict(color=colors[i], width=2), 
                                 showlegend=False))
        
        # 2. 현재 시점의 공 위치 (Ball)
        curr_x = v * t_curr
        curr_y = h - 0.5 * g * t_curr**2
        traces.append(go.Scatter(x=[curr_x], y=[curr_y], mode='markers', 
                                 marker=dict(size=15, color=colors[i], line=dict(width=1, color='black')),
                                 name=f"물체 {i+1} (v={v}m/s)"))
        
    return traces

# --- Plotly 애니메이션 구성 ---
# 1. 초기 상태 (Base Data)
initial_data = get_frame_data(0)

# 2. 프레임 리스트 (Frames)
frames = [go.Frame(data=get_frame_data(t), name=str(i)) for i, t in enumerate(t_steps)]

# 3. 레이아웃 (Layout)
max_x = max(v1, v2, v3) * t_max
fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        xaxis=dict(range=[-2, max_x * 1.1 + 5], title="수평 거리 x (m)", gridcolor='LightGray'),
        yaxis=dict(range=[-2, h * 1.1], title="높이 y (m)", gridcolor='LightGray'),
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="▶️ 재생 (Play)",
                          method="animate",
                          args=[None, {"frame": {"duration": 40, "redraw": False},
                                       "fromcurrent": True, "transition": {"duration": 0}}])
            ]
        )],
        height=600,
        plot_bgcolor='white',
        margin=dict(l=0, r=0, t=30, b=0)
    ),
    frames=frames
)

# 출력
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(f"""
### 📊 핵심 분석
- **지면 도달 시간**: 약 `{t_max:.2f}`초 (수평 속도와 무관)
- **수평 도달 거리 차이**: 수평 속도가 클수록 궤적이 더 완만하고 멀리 도달합니다.
- **연직 방향 비교**: 세 물체 모두 낙하하는 동안의 **그림자(연직 위치)**는 항상 일치한다는 것을 관찰해 보세요.
""")
