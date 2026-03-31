import streamlit as st
import plotly.graph_objects as go
import numpy as np

# 페이지 설정
# st.set_page_config(page_title="물리학 I/II 가속도와 포물선 운동", layout="wide")

st.title("🏀 가속도의 정의와 포물선 운동 탐구")
st.markdown("""
이 시뮬레이션은 비스듬히 던진 물체의 운동을 통해 **가속도의 정의($\\vec{a} = \\Delta\\vec{v}/\\Delta t$)**와 
**중력 가속도의 방향**을 시각적으로 학습하기 위해 제작되었습니다.
""")

# --- 사이드바: 초기 조건 및 시각 설정 ---
with st.sidebar:
    st.header("⚙️ 발사 조건 설정")
    v0 = st.slider("초기 속도 v₀ (m/s)", 5.0, 20.0, 12.0, 0.5)
    theta_deg = st.slider("발사 각도 θ (도)", 15, 75, 45, 5)
    theta = np.radians(theta_deg)
    g = st.radio("🌍 중력 가속도 g (m/s²)", options=[9.8, 10.0], index=0, horizontal=True, help="계산의 편의를 위해 10으로 설정해 보세요.")
    
    st.markdown("---")
    st.subheader("⏱️ 분석 시각 설정")
    t1 = st.slider("처음 시각 t₁ (s)", 0.0, 2.0, 0.4, 0.1)
    t2 = st.slider("나중 시각 t₂ (s)", 0.1, 3.0, 1.2, 0.1)
    
    if t1 >= t2:
        st.error("나중 시각 t₂는 t₁보다 커야 합니다!")

# --- 물리 엔진 (포물선 운동) ---
def get_state(t):
    x = v0 * np.cos(theta) * t
    y = v0 * np.sin(theta) * t - 0.5 * g * t**2
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta) - g * t
    return np.array([x, y]), np.array([vx, vy])

# 궤적 데이터 생성
t_max = (2 * v0 * np.sin(theta)) / g  # 지면에 닿는 시간
t_range = np.linspace(0, t_max if t_max > 0 else 1, 100)
trajectory = np.array([get_state(t)[0] for t in t_range])

# 선택된 두 지점의 데이터
pos1, vel1 = get_state(t1)
pos2, vel2 = get_state(t2)
dt = t2 - t1
dv = vel2 - vel1
a_avg = dv / dt if dt > 0 else np.array([0, 0])

# --- Plotly 시각화 ---
fig = go.Figure()

# 1. 격자 및 축 설정
max_x = max(trajectory[:, 0]) * 1.1 if len(trajectory) > 0 else 10
max_y = max(trajectory[:, 1]) * 1.2 if len(trajectory) > 0 else 10
fig.update_xaxes(range=[-1, max_x], showgrid=True, gridcolor='lightgray', zerolinecolor='black', title="x (m)")
fig.update_yaxes(range=[-1, max_y], showgrid=True, gridcolor='lightgray', zerolinecolor='black', title="y (m)")

# 2. 궤적 표시
fig.add_trace(go.Scatter(x=trajectory[:, 0], y=trajectory[:, 1], 
                         mode='lines', name='운동 궤적', 
                         line=dict(color='gray', width=1, dash='dot')))

# 3. 속도 벡터 vA (at t1)
scale = 0.3 # 속도 벡터 시각화 스케일
fig.add_annotation(x=pos1[0] + vel1[0]*scale, y=pos1[1] + vel1[1]*scale, 
                   ax=pos1[0], ay=pos1[1], xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="blue")
fig.add_annotation(x=pos1[0] + vel1[0]*scale, y=pos1[1] + vel1[1]*scale, 
                   text="<b><i>v</i>&#x20d7;<sub>A</sub></b>", showarrow=False, 
                   font=dict(color="blue", size=14), xshift=10, yshift=10)

# 4. 속도 벡터 vB (at t2)
fig.add_annotation(x=pos2[0] + vel2[0]*scale, y=pos2[1] + vel2[1]*scale, 
                   ax=pos2[0], ay=pos2[1], xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="red")
fig.add_annotation(x=pos2[0] + vel2[0]*scale, y=pos2[1] + vel2[1]*scale, 
                   text="<b><i>v</i>&#x20d7;<sub>B</sub></b>", showarrow=False, 
                   font=dict(color="red", size=14), xshift=10, yshift=10)

# 5. 별도 구역: 벡터 차(Subtraction) 시각화 (이미지 컨셉 재현)
# 시점을 한 곳(중앙 상단 등)으로 모아서 Δv 유도
base_x, base_y = max_x * 0.7, max_y * 0.8
fig.add_annotation(x=base_x + vel1[0]*scale, y=base_y + vel1[1]*scale, 
                   ax=base_x, ay=base_y, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="blue", opacity=0.5)
fig.add_annotation(x=base_x + vel2[0]*scale, y=base_y + vel2[1]*scale, 
                   ax=base_x, ay=base_y, xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor="red", opacity=0.5)

# 속도 변화량 Δv (v1의 끝에서 v2의 끝으로 잇는 벡터)
fig.add_annotation(x=base_x + vel2[0]*scale, y=base_y + vel2[1]*scale, 
                   ax=base_x + vel1[0]*scale, ay=base_y + vel1[1]*scale, 
                   xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=4, arrowcolor="orange")
fig.add_annotation(x=base_x + (vel1[0]+vel2[0])*scale/2, y=base_y + (vel1[1]+vel2[1])*scale/2, 
                   text="<b>Δ<i>v</i>&#x20d7;</b>", showarrow=False, 
                   font=dict(color="orange", size=18), xshift=30)

# 6. 평균 가속도 벡터 a_avg (B 지점에서 표시)
fig.add_annotation(x=pos2[0], y=pos2[1] + a_avg[1]*0.1, # 연직 아래 강조를 위해 스케일 조정
                   ax=pos2[0], ay=pos2[1], xref="x", yref="y", axref="x", ayref="y",
                   text="", showarrow=True, arrowhead=3, arrowsize=1, arrowwidth=5, arrowcolor="darkorange")
fig.add_annotation(x=pos2[0], y=pos2[1] + a_avg[1]*0.1, 
                   text="<b><i>a</i>&#x20d7;<sub>avg</sub></b>", showarrow=False, 
                   font=dict(color="darkorange", size=18), yshift=-20)

# 7. 점 A, B 및 바닥 표시
fig.add_trace(go.Scatter(x=[pos1[0], pos2[0]], y=[pos1[1], pos2[1]], mode='markers+text', 
                         text=['A', 'B'], textposition="bottom center",
                         marker=dict(color=['blue', 'red'], size=10), showlegend=False))
fig.add_shape(type="rect", x0=-1, y0=-0.5, x1=max_x+1, y1=0, fillcolor="tan", line_width=0)

fig.update_layout(height=600, showlegend=True, plot_bgcolor='white', title="포물선 운동에서의 속도 변화와 가속도",
                  legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.8)"))

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 계산 결과 및 학습 콘텐츠 ---
st.subheader("📚 가속도의 이해")

if dt > 0:
    col1, col2 = st.columns(2)
    with col1:
        st.write("📊 **지점별 속도 성분**")
        st.markdown(f"- **점 A ($t_1={t1}s$):** $\\vec{{v}}_A = ({vel1[0]:.2f}, {vel1[1]:.2f})$")
        st.markdown(f"- **점 B ($t_2={t2}s$):** $\\vec{{v}}_B = ({vel2[0]:.2f}, {vel2[1]:.2f})$")
        
    with col2:
        st.write("📐 **속도 변화량 ($\\Delta\\vec{v}$)**")
        st.latex(r"\Delta\vec{v} = \vec{v}_B - \vec{v}_A = (0, %.2f)" % (-g*dt))
        st.info("실험 결과: x방향 속도는 일정하므로 성분 차이는 0이며, y방향으로만 변화가 발생합니다.")

    with st.expander("💡 핵심 원리 탐구: 가속도의 방향", expanded=True):
        st.markdown(f"""
        1. **가속도의 정의**: 가속도는 단위 시간당 **속도의 변화량**입니다. 
           따라서 가속도의 방향은 항상 **속도 변화량($\\Delta\\vec{{v}}$)의 방향**과 같습니다.
        2. **포물선 운동의 특징**: 공기 저항을 무시할 때, 물체에는 오직 **중력**만이 연직 아래로 작용합니다.
        3. **실제 계산 결과**:
           - $\\Delta v_x = v_{{Bx}} - v_{{Ax}} = 0$
           - $\\Delta v_y = v_{{By}} - v_{{Ay}} = -g \\cdot \\Delta t$
        
        따라서 평균 가속도는 다음과 같이 항상 연직 아래 방향의 중력 가속도 $-%.1f m/s^2$이 됩니다.
        """ % g)
        # 가속도 계산 수식 (f-string 에러 방지를 위해 % 포맷팅 사용)
        accel_formula = r"\vec{a}_{avg} = \frac{\Delta\vec{v}}{\Delta t} = \frac{(0, %.2f)}{%.1f} = (0, -%.1f) \text{ m/s}^2" % (-g*dt, dt, g)
        st.latex(accel_formula)
        st.success("✨ 탐구 결론: 포물선 운동을 하는 물체의 가속도 방향은 항상 **연직 아래 방향(중력 방향)**입니다!")
else:
    st.warning("t₁과 t₂를 서로 다르게 설정해 주세요.")

st.sidebar.markdown("---")
st.sidebar.caption("사곡고등학교 물리학 시뮬레이션 v1.4")
