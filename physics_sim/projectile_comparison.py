import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="wide")

st.title("🏃 수평 속도에 따른 포물선 운동 비교")
st.markdown("""
세 가지 서로 다른 수평 속도를 가진 물체의 운동을 비교합니다. 
그래프 내의 **'Play'** 버튼을 누르면 끊김 없이 부드러운 애니메이션을 감상할 수 있습니다.
""")

# --- 사이드바: 속도 및 높이 설정 ---
with st.sidebar:
    st.header("⚙️ 시뮬레이션 설정")
    v1 = st.slider("물체 1 속도 (m/s)", 0, 20, 0)
    v2 = st.slider("물체 2 속도 (m/s)", 0, 20, 5)
    v3 = st.slider("물체 3 속도 (m/s)", 0, 20, 10)
    h = st.slider("초기 높이 (m)", 10, 100, 50)
    g = 9.8
    st.info("💡 팁: 그래프 하단의 Play 버튼을 누르세요!")

# --- 데이터 계산 ---
t_max = np.sqrt(2 * h / g)
t_steps = np.linspace(0, t_max, 50) # 50프레임 생성

# 프레임별 데이터 생성 함수
def get_frame_data(t_curr):
    objs = []
    colors = ['red', 'green', 'blue']
    vels = [v1, v2, v3]
    
    for i, v in enumerate(vels):
        x = v * t_curr
        y = h - 0.5 * g * t_curr**2
        objs.append(go.Scatter(x=[x], y=[y], mode='markers', 
                               marker=dict(size=15, color=colors[i]),
                               name=f"물체 {i+1} (v={v}m/s)"))
    return objs

# --- Plotly 애니메이션 구성 ---
# 1. 초기 상태 (Base Traces)
initial_data = get_frame_data(0)

# 2. 프레임 리스트 (Frames)
frames = [go.Frame(data=get_frame_data(t), name=str(i)) for i, t in enumerate(t_steps)]

# 3. 레이아웃 (Layout with Play Button)
fig = go.Figure(
    data=initial_data,
    layout=go.Layout(
        xaxis=dict(range=[-2, max(v1, v2, v3) * t_max * 1.1], title="수평 거리 x (m)"),
        yaxis=dict(range=[-2, h * 1.1], title="높이 y (m)"),
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

# 그리드 추가
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

# 출력
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown(f"""
### 📊 시뮬레이션 결과 요약
- **지면 도달 시간**: 약 `{t_max:.2f}`초 (모든 물체 동일)
- **최대 수평 도달 거리**: `{max(v1, v2, v3) * t_max:.2f}`m
""")
