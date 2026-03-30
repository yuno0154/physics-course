import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="centered")

st.title("🧩 포물선 운동 실전 연습 문제")
st.markdown("""
본 연습 문제는 개념 원리를 묻는 **서술형 문제**와 수치 계산을 위한 **단계별 문제**로 구성되어 있습니다. 
""")

# --- 벡터 도식 생성 함수 ---
def get_diagram_independence(h=30):
    fig = go.Figure()
    # 지면
    fig.add_shape(type="line", x0=-5, y0=0, x1=50, y1=0, line=dict(color="black", width=2))
    # 절벽
    fig.add_shape(type="rect", x0=-2, y0=0, x1=0, y1=h, fillcolor="lightgray", line=dict(color="black"))
    
    # 공 1 (자유 낙하 - 빨간색)
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=14, color='red', line=dict(width=2, color='black')), name="공 A (자유낙하)"))
    # 공 2 (수평 투사 - 파란색)
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=14, color='blue', line=dict(width=2, color='black')), name="공 B (수평투사)"))
    
    # 공 B의 수평 속도 벡터
    fig.add_annotation(x=10, y=h, ax=0, ay=h, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=3)
    
    # 궤적 표시 (점선)
    t = np.linspace(0, np.sqrt(2*h/10), 20)
    fig.add_trace(go.Scatter(x=np.zeros_like(t), y=h-0.5*10*t**2, mode='lines', line=dict(color='red', dash='dot'), showlegend=False))
    fig.add_trace(go.Scatter(x=15*t, y=h-0.5*10*t**2, mode='lines', line=dict(color='blue', dash='dot'), showlegend=False))

    fig.update_layout(xaxis=dict(visible=False, range=[-10, 55]), yaxis=dict(visible=False, range=[-5, h+10]),
                      height=320, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def get_diagram_cliff(h=20, v0=10):
    fig = go.Figure()
    fig.add_shape(type="rect", x0=-2, y0=0, x1=0, y1=h, fillcolor="lightgray", line=dict(color="black"))
    fig.add_shape(type="line", x0=-5, y0=0, x1=40, y1=0, line=dict(color="black", width=2))
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=14, color='red', line=dict(width=2, color='black')), showlegend=False))
    fig.add_annotation(x=10, y=h, ax=0, ay=h, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=4)
    fig.add_annotation(x=5, y=h+2.5, text=f"<b>v₀ = {v0}m/s</b>", showarrow=False, font=dict(size=16, color="blue"))
    fig.add_annotation(x=-6, y=h/2, text=f"<b>h = {h}m</b>", showarrow=False, textangle=-90, font=dict(size=16))
    t = np.linspace(0, 2, 20)
    fig.add_trace(go.Scatter(x=v0*t, y=h-0.5*10*t**2, mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-10, 45]), yaxis=dict(visible=False, range=[-5, h+10]), height=320, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white")
    return fig

def get_diagram_oblique(v0=30, theta_deg=30):
    theta = np.radians(theta_deg)
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=100, y1=0, line=dict(color="black", width=2))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=14, color='orange', line=dict(width=2, color='black')), showlegend=False))
    vx = v0 * np.cos(theta); vy = v0 * np.sin(theta)
    fig.add_annotation(x=vx*0.6, y=vy*0.6, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="darkorange", arrowwidth=4)
    fig.add_annotation(x=vx*0.6 + 8, y=vy*0.6 + 5, text=f"<b>v₀ = {v0}m/s</b>", showarrow=False, font=dict(size=16, color="darkorange"))
    fig.add_annotation(x=12, y=3, text=f"<b>θ = {theta_deg}°</b>", showarrow=False, font=dict(size=15))
    t_land = 2 * vy / 10; t = np.linspace(0, t_land, 30)
    fig.add_trace(go.Scatter(x=vx*t, y=vy*t-0.5*10*t**2, mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-10, 100]), yaxis=dict(visible=False, range=[-5, 30]), height=320, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white")
    return fig

# --- [서술형 문제] ---
st.divider()
st.subheader("🖋️ [서술형 핵심 문제] 운동의 독립성")
st.plotly_chart(get_diagram_independence(), use_container_width=True, config={'staticPlot': True})

st.markdown("""
높이가 동일한 곳에서 **공 A는 자유 낙하**시키고, **공 B는 수평 방향**으로 던졌습니다.
두 공의 수평 속도가 다름에도 불구하고 왜 **동시에** 지면에 도달하는지, 각 방향(수평, 연직)의 힘과 가속도 관점에서 서술하시오.
""")

user_answer = st.text_area("여기에 답안을 작성하세요 (250자 내외)", placeholder="예: 수평 방향은 힘이 작용하지 않아.. 연직 방향은 중력에 의해..")

if st.button("🔍 모범 답안 보기"):
    st.success("""
    **[모범 답안]**
    수평 방향으로는 힘이 작용하지 않아 **등속 직선 운동**을 하고, 연직 방향으로는 오직 **중력**만 작용하여 **등가속도 운동(자유 낙하)**을 합니다. 
    두 방향의 운동은 서로 **독립적**이므로, 수평 속도와 상관없이 연직 방향으로 작용하는 중력 가속도가 동일하기 때문에 두 공은 같은 시간 동안 같은 높이를 이동하여 지면에 동시에 도달합니다.
    """)

# --- 문제 1: 수평 투사 ---
st.divider()
st.subheader("📝 [문제 1] 수평 던지기 분석")
st.plotly_chart(get_diagram_cliff(), use_container_width=True, config={'staticPlot': True})
st.markdown("높이 **20m**인 절벽에서 공을 수평 방향으로 **10m/s**로 던졌습니다. ($g=10m/s^2$)")

q1_1 = st.radio("**(1) 지면에 도달할 때까지 걸리는 시간은?**", ["1초", "2초", "3초"], index=None, key="p1_1")
if q1_1 == "2초": st.success("✅ 정답 (h=1/2gt² → 20=5t², t=2s)")

q1_2 = st.radio("**(2) 던진 지 1초 후 속도의 크기(m/s)는?**", ["10", "10√2", "20"], index=None, key="p1_2")
if q1_2 == "10√2": st.success("✅ 정답 (vx=10, vy=gt=10이므로 v = √(10²+10²) = 10√2 m/s)")

q1_3 = st.radio("**(3) 수평 도달 거리(m)는?**", ["10m", "20m", "40m"], index=None, key="p1_3")
if q1_3 == "20m": st.success("✅ 정답 (x = vx * t_land = 10 * 2 = 20m)")

# --- 문제 2: 비스듬한 투사 ---
st.divider()
st.subheader("📝 [문제 2] 비스듬히 던지기 분석")
st.plotly_chart(get_diagram_oblique(), use_container_width=True, config={'staticPlot': True})
st.markdown("지면에서 **30m/s**의 속도로 **30도** 각도로 던졌습니다. ($\sin 30^\circ=0.5, \cos 30^\circ=0.87, g=10m/s^2$)")

q2_1 = st.radio("**(1) 최고점 도달 시간(초)은?**", ["1초", "1.5초", "3초"], index=None, key="p2_1")
if q2_1 == "1.5초": st.success("✅ 정답 (vy0 = 15, t = vy0/g = 1.5s)")

q2_2 = st.radio("**(2) 던진 지 1초 후 속도의 크기(m/s)는?**", ["약 26.5m/s", "10m/s", "30m/s"], index=None, key="p2_2")
if q2_2 == "약 26.5m/s": st.success("✅ 정답 (vx=26, vy=15-10=5 이므로 v = √(26²+5²) ≈ 26.5m/s)")

q2_3 = st.radio("**(3) 최고점의 높이(m)는?**", ["11.25m", "15.0m", "22.5m"], index=None, key="p2_3")
if q2_3 == "11.25m": st.success("✅ 정답 (H = vy²/2g = 15²/(2*10) = 11.25m)")

q2_4 = st.radio("**(4) 수평 도달 거리(m)는?**", ["40m", "78m", "90m"], index=None, key="p2_4")
if q2_4 == "78m": st.success("✅ 정답 (x = vx * t_total = 26 * 3 = 78m)")
