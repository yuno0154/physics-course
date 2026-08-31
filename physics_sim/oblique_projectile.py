import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🏀 비스듬히 던진 물체의 운동")
st.markdown("""
포물선 운동의 수평 성분과 연직 성분을 분리하여 속도와 가속도의 변화를 분석합니다. 
하단의 **Play/Pause** 버튼을 사용하거나 슬라이더를 움직여 각 지점의 물리량을 관찰해 보세요!
""")

# --- 발사 조건 및 시각화 설정 ---
with st.container(border=True):
    st.markdown("### 🚀 발사 조건 및 시각화 설정")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])
    with col1:
        v0 = st.number_input("초기 속도 v₀ (m/s) [5.0~50.0]", min_value=5.0, max_value=50.0, value=20.0, step=1.0)
    with col2:
        theta_deg = st.number_input("발사 각도 θ (도) [10~85]", min_value=10, max_value=85, value=45, step=1)
    with col3:
        g = st.radio("🌍 중력 가속도 g (m/s²)", options=[9.8, 10.0], index=0, horizontal=True)
    with col4:
        st.markdown("<p style='font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;'>🏹 벡터 시각화</p>", unsafe_allow_html=True)
        show_vectors = st.toggle("속도 벡터 ($v_x, v_y$)", value=False, help="운동 중인 물체의 수평 속도(초록) 및 연직 속도(빨강) 벡터 화살표를 표시합니다.")
        show_accel = st.toggle("가속도 벡터 ($a_y = -g$)", value=False, help="물체에 작용하는 중력 가속도(주황색 아래 화살표)를 표시합니다.")
    st.info("💡 팁: 재생 중 Pause를 누르면 현재 위치에서 멈춥니다.")

theta = np.radians(theta_deg)

# --- 물리 정보 계산 ---
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
t_H = vy0 / g # 최고점 도달 시간
H = (vy0**2) / (2 * g) # 최고점 높이
t_R = 2 * t_H # 지면 도달 시간
R = vx0 * t_R # 수평 도달 거리

# --- [활동 1 위치 지정 컨트롤] ---
with st.container(border=True):
    st.markdown("### 🎯 [활동 1] 세 관찰 위치 (A: 상승 중, B: 최고점, C: 하강 중) 설정")
    st.caption("아래 슬라이더를 조절하여 원하는 시각의 관찰 지점(A, C)을 지정하면, 그래프와 활동지 데이터 표에 실시간으로 반영됩니다.")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("🔵 **위치 A (상승 중)**")
        max_ta = max(0.05, float(round(t_H - 0.05, 2)))
        default_ta = float(round(t_H * 0.5, 2))
        t_A = st.slider("A 지점 시각 $t_A$ (s)", min_value=0.0, max_value=max_ta, value=min(default_ta, max_ta), step=0.05, key="t_A_slider")
    with col_b:
        st.markdown("⭐ **위치 B (최고점)**")
        t_B = float(round(t_H, 2))
        st.info(f"최고점 시각 $t_B = t_H = {t_B:.2f}$ s (자동 고정)")
    with col_c:
        st.markdown("🟢 **위치 C (하강 중)**")
        min_tc = float(round(t_H + 0.05, 2))
        max_tc = float(round(t_R, 2))
        default_tc = float(round(t_H + (t_R - t_H) * 0.5, 2))
        if min_tc >= max_tc:
            min_tc = t_B
        t_C = st.slider("C 지점 시각 $t_C$ (s)", min_value=min_tc, max_value=max_tc, value=max(min_tc, min(default_tc, max_tc)), step=0.05, key="t_C_slider")
    
    show_abc_markers = st.checkbox("📌 그래프 상에 A, B, C 지점 마커 표시하기", value=True)

# A, B, C 지점 물리량 계산
xA = vx0 * t_A
yA = max(vy0 * t_A - 0.5 * g * t_A**2, 0)
vxA = vx0
vyA = vy0 - g * t_A
axA = 0.0
ayA = -g

xB = vx0 * t_B
yB = H
vxB = vx0
vyB = 0.0
axB = 0.0
ayB = -g

xC = vx0 * t_C
yC = max(vy0 * t_C - 0.5 * g * t_C**2, 0)
vxC = vx0
vyC = vy0 - g * t_C
axC = 0.0
ayC = -g

t_steps = np.linspace(0, t_R, 100) # 더 세밀한 분석을 위해 100단계로 증가

# 프레임별 데이터 및 텍스트 데이터 생성 함수
def get_oblique_frame_data(t_curr):
    t_path = np.linspace(0, t_curr, 40)
    path_x = vx0 * t_path
    path_y = vy0 * t_path - 0.5 * g * t_path**2
    curr_x = vx0 * t_curr
    curr_y = max(vy0 * t_curr - 0.5 * g * t_curr**2, 0)
    curr_vx = vx0
    curr_vy = vy0 - g * t_curr
    v_total = np.sqrt(curr_vx**2 + curr_vy**2)
    
    trace_path = go.Scatter(x=path_x, y=path_y, mode='lines', line=dict(color='blue', width=2), name="궤적")
    trace_ball = go.Scatter(x=[curr_x], y=[curr_y], mode='markers', 
                            marker=dict(size=18, color='orange', line=dict(width=2, color='black')), 
                            name="현재 위치")
    
    traces = [trace_path, trace_ball]
    
    scale = 0.5
    if show_vectors:
        trace_vx = go.Scatter(x=[curr_x, curr_x + curr_vx*scale], y=[curr_y, curr_y], 
                              mode='lines+markers', line=dict(color='green', width=3), 
                              marker=dict(symbol="arrow-right", size=10), name="수평 속도 (vx)")
        trace_vy = go.Scatter(x=[curr_x, curr_x], y=[curr_y, curr_y + curr_vy*scale], 
                              mode='lines+markers', line=dict(color='red', width=3), 
                              marker=dict(symbol="arrow-up" if curr_vy > 0 else "arrow-down", size=10), name="연직 속도 (vy)")
        traces.extend([trace_vx, trace_vy])
    
    if show_accel:
        scale_a = 0.5
        trace_ay = go.Scatter(x=[curr_x, curr_x], y=[curr_y, curr_y - g*scale_a],
                              mode='lines+markers', line=dict(color='darkorange', width=4),
                              marker=dict(symbol="arrow-down", size=11), name="중력 가속도 (ay)")
        traces.append(trace_ay)
    
    # --- 실시간 수치 데이터 어노테이션 (차트 내 표시용) ---
    telemetry_text = (
        f"<b>📊 실시간 데이터</b><br>"
        f"시간 (t): {t_curr:.2f} s<br>"
        f"수평 거리 (x): {curr_x:.2f} m<br>"
        f"높이 (y): {curr_y:.2f} m<br>"
        f"수평 속도 (vx): {curr_vx:.2f} m/s<br>"
        f"연직 속도 (vy): {curr_vy:+.2f} m/s<br>"
        f"합성 속도 (v): {v_total:.2f} m/s<br>"
        f"수평 가속도 (ax): 0.00 m/s²<br>"
        f"연직 가속도 (ay): -{g:.2f} m/s²"
    )
    
    return traces, telemetry_text

# --- Plotly 애니메이션 구성 (재생/정지/슬라이더 복구) ---
# 초기 데이터 및 텔레메트리
initial_traces, initial_text = get_oblique_frame_data(0)

# 정적 마커 추가 (최고점 및 A, B, C 지점)
initial_traces.append(go.Scatter(x=[vx0 * t_H], y=[H], mode='markers', marker=dict(size=12, color='red', symbol='star'), name='최고점'))

if show_abc_markers:
    trace_mA = go.Scatter(x=[xA], y=[yA], mode='markers+text', text=["A (상승)"], textposition="top left",
                          marker=dict(size=13, color='blue', symbol='circle', line=dict(width=2, color='white')), name='A (상승 중)')
    trace_mB = go.Scatter(x=[xB], y=[yB], mode='markers+text', text=["B (최고점)"], textposition="top center",
                          marker=dict(size=15, color='crimson', symbol='star', line=dict(width=2, color='white')), name='B (최고점)')
    trace_mC = go.Scatter(x=[xC], y=[yC], mode='markers+text', text=["C (하강)"], textposition="top right",
                          marker=dict(size=13, color='green', symbol='circle', line=dict(width=2, color='white')), name='C (하강 중)')
    initial_traces.extend([trace_mA, trace_mB, trace_mC])

# 프레임 생성 (데이터 + 어노테이션 텍스트 포함)
frames = []
for i, t in enumerate(t_steps):
    f_traces, f_text = get_oblique_frame_data(t)
    frames.append(go.Frame(
        data=f_traces, 
        name=f"frame_{i}",
        layout=go.Layout(annotations=[
            dict(x=0.02, y=0.98, xref="paper", yref="paper", text=f_text, showarrow=False, align="left", 
                 bgcolor="rgba(255,255,255,0.75)", bordercolor="black", borderwidth=1, font=dict(family="Courier New, monospace", size=12))
        ])
    ))

# 슬라이더 설정
sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {"font": {"size": 14}, "prefix": "시간: ", "visible": True, "xanchor": "right"},
    "transition": {"duration": 30, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9, "x": 0.05, "y": 0,
    "steps": []
}

for i, t in enumerate(t_steps):
    sliders_dict["steps"].append({
        "args": [[f"frame_{i}"], {"frame": {"duration": 30, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
        "label": f"{t:.2f}s", "method": "animate"
    })

fig = go.Figure(
    data=initial_traces,
    layout=go.Layout(
        xaxis=dict(range=[-2, R * 1.2], title="수평 거리 x (m)", gridcolor='LightGray'),
        yaxis=dict(range=[-2, H * 1.5], title="높이 y (m)", gridcolor='LightGray'),
        updatemenus=[dict(
            type="buttons", direction="left", showactive=False, x=0.05, y=1.2,
            buttons=[
                dict(label="▶️ 재생 (Play)", method="animate", args=[None, {"frame": {"duration": 30, "redraw": False}, "fromcurrent": True}]),
                dict(label="⏸️ 정지 (Pause)", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}])
            ]
        )],
        sliders=[sliders_dict],
        height=680,
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=100, b=100),
        annotations=[
            dict(x=0.02, y=0.98, xref="paper", yref="paper", text=initial_text, showarrow=False, align="left", 
                 bgcolor="rgba(255,255,255,0.75)", bordercolor="black", borderwidth=1, font=dict(family="Courier New, monospace", size=12))
        ]
    ),
    frames=frames
)

# 최고점/도달거리 어노테이션 추가
fig.add_annotation(x=vx0 * t_H, y=H, text=f"최고점 H={H:.2f}m", showarrow=True, arrowhead=1)
fig.add_annotation(x=R, y=0, text=f"도달 거리 R={R:.2f}m", showarrow=True, arrowhead=1)

st.plotly_chart(fig, use_container_width=True)

# --- [활동지: 세 위치에서 속도와 가속도 관찰 데이터 표] ---
st.divider()
st.subheader("📋 1. 세 위치에서 속도와 가속도를 관찰하자.")
st.markdown("""
위에서 지정한 **세 위치(A 상승 중, B 최고점, C 하강 중)**의 시뮬레이션 측정값을 확인하고 활동지를 완성해 보세요.
""")

# 활동지 표 1: 정밀 수치 데이터 표
st.markdown("#### 📊 [정밀 측정값] 각 위치별 물리량 데이터 표")
table_md = f"""
| 위치 | 시각 $t$ (s) | 위치 $(x, y)$ (m) | 수평 속도 $v_x$ (m/s) | 연직 속도 $v_y$ (m/s) | 수평 가속도 $a_x$ (m/s²) | 연직 가속도 $a_y$ (m/s²) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **A 상승 중** | `{t_A:.2f}` | `({xA:.2f}, {yA:.2f})` | `{vxA:.2f}` | `{vyA:+.2f}` | `{axA:.2f}` | `{ayA:.2f}` |
| **B 최고점** | `{t_B:.2f}` | `({xB:.2f}, {yB:.2f})` | `{vxB:.2f}` | `{vyB:.2f}` | `{axB:.2f}` | `{ayB:.2f}` |
| **C 하강 중** | `{t_C:.2f}` | `({xC:.2f}, {yC:.2f})` | `{vxC:.2f}` | `{vyC:+.2f}` | `{axC:.2f}` | `{ayC:.2f}` |
"""
st.markdown(table_md)

# 활동지 표 2: 부호 및 변화 분석 표 (활동지 원본 양식)
st.markdown("#### 📝 [활동지 양식] 부호($+$, $0$, $-$) 및 상태 기록용 표")
sign_table_md = f"""
| 위치 | $v_x$ (수평 속도) | $v_y$ (연직 속도) | $a_x$ (수평 가속도) | $a_y$ (연직 가속도) | 운동 상태 설명 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **A 상승 중** | **+ (일정)** | **+ (위쪽, 감소)** | **0** | **- (아래쪽, 일정)** | 수평 등속 + 연직 감속 상승 |
| **B 최고점** | **+ (일정)** | **0 (순간 정지)** | **0** | **- (아래쪽, 일정)** | 수평 방향으로만 운동 ($v = v_x$) |
| **C 하강 중** | **+ (일정)** | **- (아래쪽, 증가)** | **0** | **- (아래쪽, 일정)** | 수평 등속 + 연직 가속 낙하 |
"""
st.markdown(sign_table_md)

with st.expander("💡 핵심 물리 개념 탐구 및 정리", expanded=True):
    st.markdown(f"""
    1. **수평 방향($x$) 분석**:
       - 물체에 작용하는 수평 방향 외력이 없으므로 ($F_x = 0$) 수평 가속도는 항상 **$a_x = 0\\text{{ m/s}}^2$** 입니다.
       - 따라서 수평 속도는 운동이 끝날 때까지 항상 **$v_x = {vx0:.2f}\\text{{ m/s}}$ 로 일정(등속 직선 운동)**합니다.
    2. **연직 방향($y$) 분석**:
       - 물체에는 항상 일정한 크기의 중력이 아래로 작용하므로 ($F_y = -mg$) 연직 가속도는 항상 **$a_y = -{g:.1f}\\text{{ m/s}}^2$ (아래 방향으로 일정)**합니다.
       - 연직 속도 $v_y$는 상승할 때 **양수(+)로 감소**하다가, **최고점(B)에서 $0\\text{{ m/s}}$**이 되고, 하강할 때 **음수(-)로 크기가 증가**합니다.
    3. **최고점에서의 속도**:
       - 최고점에서는 연직 속도 $v_y = 0$이지만, 수평 속도 $v_x$가 살아있으므로 전체 속도는 $0$이 아니라 **$v = v_x = {vx0:.2f}\\text{{ m/s}}$** 입니다.
    """)

# --- [결과 데이터 요약] ---
st.divider()
st.markdown("### 📊 주요 시뮬레이션 결과 요약")
col_res1, col_res2, col_res3 = st.columns(3)
with col_res1:
    st.metric("최고점 도달 시간 ($t_H$)", f"{t_H:.3f} s")
with col_res2:
    st.metric("최고점 높이 ($H$)", f"{H:.2f} m")
with col_res3:
    st.metric("최대 수평 도달 거리 ($R$)", f"{R:.2f} m")

# --- [데이터 분석 및 상세 결과] ---
st.divider()

with st.expander("📊 상세 분석 데이터 및 수치 보기", expanded=False):
    st.subheader("📋 포물선 운동의 수평/연직 성분 분석 단계")
    
    analysis_data = {
        "구분": ["알짜힘(F)", "운동의 종류", "가속도(a)", "처음 속도", "t초 후 속도", "t초 후 위치", "운동 경로", "최고점 도달 시간", "최고점의 높이", "수평 도달 거리"],
        "수평 방향(x)": [
            "0 (Fx = 0)", "등속 직선 운동", "ax = 0", "v0x = v0 cosθ", "vx = v0 cosθ", "x = (v0 cosθ) * t", "포물선", "-", "-", "R = v0cosθ × 2tH"
        ],
        "연직 방향(y)": [
            "중력 (Fy = -mg)", "등가속도 직선 운동", "ay = -g", "v0y = v0 sinθ", "vy = v0 sinθ - gt", "y = (v0 sinθ) * t - 1/2gt²", "포물선", "tH = v0sinθ / g", "H = (v0sinθ)² / 2g", "지면 도달 시간 = 2tH"
        ]
    }
    st.table(analysis_data)
    
    st.divider()
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
