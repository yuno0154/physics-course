import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
st.set_page_config(layout="centered")

# 인쇄용 CSS 설정
st.markdown("""
    <style>
    @media print {
        @page { margin: 10mm; }
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stActionButton { display: none !important; }
        .main .block-container { padding: 0 !important; }
        .stMarkdown, .stPlotlyChart { page-break-inside: avoid; margin-bottom: 0px !important; }
        h1 { font-size: 1.3rem !important; margin-bottom: 10px !important; }
        h3 { font-size: 1.0rem !important; margin-top: 5px !important; margin-bottom: 5px !important; }
        p, li { font-size: 0.9rem !important; line-height: 1.2 !important; }
        .stDivider { margin-top: 5px !important; margin-bottom: 5px !important; }
    }
    .print-header { font-size: 0.9rem; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid black; padding-bottom: 5px; }
    .answer-space { border-bottom: 1px solid #ccc; height: 25px; margin-bottom: 5px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 포물선 운동 실전 연습 문제")

# --- 출력 모드 선택 ---
is_print_mode = st.toggle("🖨️ 학습지 출력 모드 전환 (인쇄 후 PDF 저장 권장)", value=False)

if is_print_mode:
    # 실시간 인쇄 버튼 (JS 활용)
    if st.button("🖨️ 바로 인쇄 / PDF 저장"):
        st.components.v1.html("<script>window.print()</script>", height=0)
        
    st.markdown('<div class="print-header">📝 포물선 운동 실전 연습 학습지 &nbsp; [ 학년: ____ &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ ]</div>', unsafe_allow_html=True)

st.markdown("""
본 연습 문제는 개념 원리를 묻는 **서술형 문제**와 학습지 기반 **응용 문제**로 구성되어 있습니다. 
""")

# --- 벡터 도식 생성 함수군 ---
def get_diagram_independence(h=30):
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=50, y1=0, line=dict(color="black", width=2))
    fig.add_shape(type="rect", x0=-2, y0=0, x1=0, y1=h, fillcolor="lightgray", line=dict(color="black"))
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=14, color='red', line=dict(width=2, color='black')), name="공 A (자유낙하)"))
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=14, color='blue', line=dict(width=2, color='black')), name="공 B (수평투사)"))
    fig.add_annotation(x=10, y=h, ax=0, ay=h, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=3)
    t = np.linspace(0, np.sqrt(2*h/10), 20)
    fig.add_trace(go.Scatter(x=np.zeros_like(t), y=h-0.5*10*t**2, mode='lines', line=dict(color='red', dash='dot'), showlegend=False))
    fig.add_trace(go.Scatter(x=15*t, y=h-0.5*10*t**2, mode='lines', line=dict(color='blue', dash='dot'), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-10, 55]), yaxis=dict(visible=False, range=[-5, h+10]), height=180, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def get_diagram_q3(v0=10, theta_deg=30):
    theta = np.radians(theta_deg); vx = v0 * np.cos(theta); vy = v0 * np.sin(theta)
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=20, y1=0, line=dict(color="black", width=2))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=14, color='skyblue', line=dict(width=2, color='black')), showlegend=False))
    fig.add_annotation(x=vx*0.8, y=vy*0.8, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="blue", arrowwidth=4)
    fig.add_annotation(x=vx+2, y=vy+2, text=f"<b>v₀=10m/s, θ=30°</b>", showarrow=False, font=dict(size=14))
    t_land = 2*vy/10; t = np.linspace(0, t_land, 30); fig.add_trace(go.Scatter(x=vx*t, y=vy*t-0.5*10*t**2, mode='lines', line=dict(color='gray', dash='dot'), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-5, 15]), yaxis=dict(visible=False, range=[-2, 5]), height=180, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

def get_diagram_q5():
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=30, y1=0, line=dict(color="black", width=2))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='orange'), showlegend=False))
    # 0s to 1s path
    t = np.linspace(0, 1, 10); vx=5; v_y0=30; g=9.8; x=vx*t; y=v_y0*t-0.5*g*t**2
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='orange', width=2), showlegend=False))
    fig.add_annotation(x=vx*1+3, y=y[-1], text="<b>1초 (25m)</b>", showarrow=False, font=dict(size=14))
    fig.add_shape(type="line", x0=vx*1, y0=0, x1=vx*1, y1=y[-1], line=dict(color="blue", dash="dash"))
    fig.update_layout(xaxis=dict(visible=False, range=[-5, 30]), yaxis=dict(visible=False, range=[-5, 50]), height=180, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

# --- [서술형 문제 1] ---
st.divider()
st.subheader("🖋️ [서술형] 운동의 독립성 이해")
st.plotly_chart(get_diagram_independence(), use_container_width=True, config={'staticPlot': True})
st.markdown("동일한 높이에서 공 A(자유낙하)와 공 B(수평투사)를 동시에 발사했습니다. 왜 동시에 지면에 도달하는지 설명하시오.")

if is_print_mode:
    for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
else:
    with st.expander("🔍 모범 답안 보기"):
        st.info("수평과 연직 방향의 운동은 서로 **독립적**이며, 연직 방향으로는 공의 종류와 상관없이 동일한 **중력**만 작용하여 연직 가속도가 같기 때문입니다.")

# --- [연습 문제 3] ---
st.divider()
st.subheader("📝 [문제 3] 비스듬히 던진 물체의 정밀 분석")
st.plotly_chart(get_diagram_q3(), use_container_width=True, config={'staticPlot': True})
st.markdown("처음 속도 **10m/s**, 각도 **30도**로 던졌습니다. ($g=10m/s^2$) 아래 질문에 답하세요.")

if is_print_mode:
    st.markdown("1) 최고점 도달 시간(s)은? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
    st.markdown("2) 최고점의 높이(m)는? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
    st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
else:
    ans3_t = st.text_input("1) 최고점 도달 시간(s)은?", key="q3_1")
    ans3_h = st.text_input("2) 최고점의 높이(m)는?", key="q3_2")
    if st.button("결과 확인", key="b3"):
        st.success(f"**[정답 및 풀이]**\n- 시간: $v_{{y0}}/g = (10 \sin 30^\circ)/10 = 0.5$초\n- 높이: $v_{{y0}}^2/2g = 5^2/20 = 1.25$m")

# --- [연습 문제 4] ---
st.divider()
st.subheader("📝 [문제 4] 수평 속도의 역추적")
st.markdown("""
물체를 비스듬히 던져 올렸더니 **4초 후** 수평으로 **39.2m** 떨어진 곳에 도달했습니다. 
처음 발사 속도의 **수평 방향 성분**은 몇 m/s인가요? ($g=9.8m/s^2$)
""")

if is_print_mode:
    st.markdown("정답 및 풀이 과정:")
    for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
else:
    ans4 = st.text_input("수평 속도(m/s) 입력", key="q4")
    if st.button("결과 확인", key="b4"):
        st.success("**[정답] 9.8 m/s** (수평 방향은 등속 운동이므로 $v_x = x/t = 39.2/4 = 9.8$ m/s)")

# --- [연습 문제 5] ---
st.divider()
st.subheader("🔥 [심화 문제 5] 최고점 도달 시간 추론")
st.plotly_chart(get_diagram_q5(), use_container_width=True, config={'staticPlot': True})
st.markdown("""
비스듬히 던진 야구공이 **0초부터 1초까지** 연직 방향으로 이동한 거리(변위)가 **25m**입니다. 
이 공이 **최고점에 도달할 때까지** 걸리는 시간은 약 몇 초인가요? ($g=9.8m/s^2$)
""")

if is_print_mode:
    st.markdown("정답 및 풀이 과정:")
    for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
else:
    ans5 = st.text_input("최고점 시간(초) 입력", key="q5")
    if st.button("결과 확인", key="b5"):
        st.success("""
        **[정답 및 풀이] 약 3.05초**
        1. $y = v_{y0}t - 1/2gt^2$ 공식에 대입: $25 = v_{y0}(1) - 4.9(1)^2$
        2. 연직 초기 속도 $v_{y0} = 29.9$ m/s 도출
        3. 최고점 시간 $t_H = v_{y0}/g = 29.9 / 9.8 \approx 3.05$초
        """)

st.divider()
st.info("💡 모든 도표는 벡터로 직접 그려졌습니다. 문제를 풀며 상황을 머릿속으로 그려보세요!")
