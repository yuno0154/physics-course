import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="centered")

st.title("🧩 포물선 운동 실전 연습 문제")
st.markdown("""
지금까지 학습한 내용을 바탕으로 연습 문제를 풀어봅시다. 
각 문제 위에 제시된 **수치 도표**를 보고 상황을 분석해 보세요!
""")

# --- 벡터 도식 생성 함수 (이미지 대용) ---
def get_diagram_cliff(h=20, v0=10):
    fig = go.Figure()
    # 절벽 그리기
    fig.add_shape(type="rect", x0=-2, y0=0, x1=0, y1=h, fillcolor="lightgray", line=dict(color="black"))
    # 지면 그리기
    fig.add_shape(type="line", x0=-5, y0=0, x1=40, y1=0, line=dict(color="black", width=2))
    # 공 위치
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers+text', marker=dict(size=12, color='red'),
                             text=["발사 지점"], textposition="top left"))
    # 수평 속도 벡터 화살표
    fig.add_annotation(x=5, y=h, ax=0, ay=h, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=3, text=f"v₀ = {v0}m/s")
    # 높이 표시
    fig.add_annotation(x=-3, y=h/2, text=f"h = {h}m", showarrow=False, textangle=-90)
    
    # 예상 궤적 (점선)
    t = np.linspace(0, 2, 20)
    fig.add_trace(go.Scatter(x=v0*t, y=h-0.5*10*t**2, mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))

    fig.update_layout(xaxis=dict(visible=False, range=[-10, 40]), yaxis=dict(visible=False, range=[-5, h+10]),
                      height=300, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

def get_diagram_oblique(v0=30, theta_deg=30):
    theta = np.radians(theta_deg)
    fig = go.Figure()
    # 지면
    fig.add_shape(type="line", x0=-5, y0=0, x1=100, y1=0, line=dict(color="black", width=2))
    # 발사 지점 공
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='orange')))
    # 초기 속도 벡터 (화살표)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    fig.add_annotation(x=vx*0.5, y=vy*0.5, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowcolor="orange", arrowwidth=3, text=f"v₀ = {v0}m/s")
    # 각도 표시
    fig.add_annotation(x=10, y=2, text=f"θ = {theta_deg}°", showarrow=False)
    
    # 궤적 점선
    t_land = 2 * vy / 10
    t = np.linspace(0, t_land, 30)
    fig.add_trace(go.Scatter(x=vx*t, y=vy*t-0.5*10*t**2, mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))
    
    fig.update_layout(xaxis=dict(visible=False, range=[-10, 100]), yaxis=dict(visible=False, range=[-5, 30]),
                      height=300, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

# --- 문제 1: 수평 투사 ---
st.divider()
st.subheader("📝 문제 1. 수평 절벽에서의 투사")
st.plotly_chart(get_diagram_cliff(), use_container_width=True, config={'staticPlot': True})

st.markdown("""
높이가 **20m**인 절벽 끝에서 공을 수평 방향으로 **10m/s**의 속도로 던졌습니다. 
(단, 중력 가속도 $g = 10m/s^2$, 공기 저항은 무시함)
""")

q1 = st.radio(
    "1) 공이 지면에 도달하는 데 걸리는 시간(초)은?",
    ["1초", "2초", "3초", "4초"],
    index=None, key="p1"
)

if q1:
    if q1 == "2초":
        st.success("✅ 정답입니다! (연직 방향 자유 낙하 $h = \\frac{1}{2}gt^2$ 에서 $20 = 5t^2$, $t=2$s)")
    else:
        st.error("❌ 다시 생각해 보세요. 연직 방향은 자유 낙하와 같습니다.")

# --- 문제 2: 비스듬한 투사 ---
st.divider()
st.subheader("📝 문제 2. 비스듬히 차올린 공")
st.plotly_chart(get_diagram_oblique(), use_container_width=True, config={'staticPlot': True})

st.markdown("""
지면에서 어떤 물체를 **30m/s**의 속도로 지면과 **30도** 각도로 던졌습니다. 
(단, $\sin 30^\circ = 0.5$, $g = 10m/s^2$)
""")

q2 = st.radio(
    "2) 물체의 최고점 도달 시간(초)은 얼마인가요?",
    ["0.5초", "1초", "1.5초", "3초"],
    index=None, key="p2"
)

if q2:
    if q2 == "1.5초":
        st.success("✅ 정답입니다! (연직 속도 성분 $v_y = v_0 \sin\theta = 30 \\times 0.5 = 15m/s$ 이므로, 최고점($v_y=0$)까지 시간은 $15/10 = 1.5$s)")
    else:
        st.error("❌ 연직 방향 초기 속도 성분을 먼저 구해보세요.")

st.divider()
st.info("💡 팁: 그래프가 보이지 않는 문제는 완벽하게 해결되었으며, 이제 '벡터 도식'을 통해 더 명확하게 문제를 푸실 수 있습니다!")
