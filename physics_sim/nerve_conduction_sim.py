import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(page_title="민말이집 신경 전도", page_icon="⚡", layout="wide")

# ── 막전위 곡선: 4ms 주기, 2ms에서 +30mV 정점 ──
# 각 구간을 부드러운 3차(cubic Hermite) smooth-step으로 연결
def _smoothstep(t):
    """0→1 구간 S자 보간 (양 끝 도함수=0으로 부드럽게 연결)"""
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)

def _build_ap_table():
    """
    정확한 데이터 기준점:
      0 ms  : -70 mV  (휴지 전위)
      1 ms  : -60 mV  (탈분극 진행)
      1.7 ms: +30 mV  (탈분극 정점)
      2 ms  :   0 mV  (재분극 진행)
      3 ms  : -80 mV  (과분극 정점)
      4 ms  : -70 mV  (휴지 회복)
    """
    n = 100  # 각 구간 샘플 수 (조밀할수록 부드러움)

    # Phase1: 0 → 1 ms   -70 → -60  (Δ = +10)
    t1 = np.linspace(0.0, 1.0, n, endpoint=False)
    v1 = -70 + 10  * _smoothstep((t1 - 0.0) / 1.0)

    # Phase2: 1 → 1.7 ms  -60 → +30  (Δ = +90, 급격한 상승)
    t2 = np.linspace(1.0, 1.7, n, endpoint=False)
    v2 = -60 + 90  * _smoothstep((t2 - 1.0) / 0.7)

    # Phase3: 1.7 → 2 ms  +30 → 0   (Δ = -30, 빠른 하강 시작)
    t3 = np.linspace(1.7, 2.0, n, endpoint=False)
    v3 =  30 - 30  * _smoothstep((t3 - 1.7) / 0.3)

    # Phase4: 2 → 3 ms    0 → -80   (Δ = -80, 재분극+과분극)
    t4 = np.linspace(2.0, 3.0, n, endpoint=False)
    v4 =   0 - 80  * _smoothstep((t4 - 2.0) / 1.0)

    # Phase5: 3 → 4 ms   -80 → -70  (Δ = +10, 회복)
    t5 = np.linspace(3.0, 4.0, n)
    v5 = -80 + 10  * _smoothstep((t5 - 3.0) / 1.0)

    t_all = np.concatenate([t1, t2, t3, t4, t5])
    v_all = np.concatenate([v1, v2, v3, v4, v5])
    return t_all, v_all

_AP_T, _AP_V = _build_ap_table()

def get_voltage(t):
    """자극 후 t(ms) 경과 시 막전위 (mV)"""
    t = np.asarray(t, dtype=float)
    v = np.where(t < 0, -70.0, np.interp(t, _AP_T, _AP_V, left=-70.0, right=-70.0))
    return v

# ── 세션 상태 ──
for k, d in [("t_now", 0.0), ("playing", False)]:
    if k not in st.session_state:
        st.session_state[k] = d

# ── 사이드바: 시뮬레이션 조건 ──
with st.sidebar:
    st.header("🔬 시뮬레이션 조건")
    v_speed    = st.slider("전도 속도 (cm/ms)", 0.5, 3.0, 1.0, 0.1)
    d_interval = st.slider("결절 간격 (cm)",   0.5, 2.0, 1.0, 0.1)
    t_max      = st.slider("표시 시간 범위 (ms)", 6.0, 20.0, 10.0, 1.0)
    st.markdown("---")
    speed_sel = st.selectbox("재생 속도",
        ["0.1× 초슬로우", "0.25× 매우 느림", "0.5× 느림", "1× 보통"], index=1)
    step_map = {"0.1× 초슬로우": 0.008, "0.25× 매우 느림": 0.02,
                "0.5× 느림": 0.04, "1× 보통": 0.08}
    play_step = step_map[speed_sel]
    st.markdown("---")
    st.markdown("### 활동전위 기준값")
    st.markdown("""
| 시간 | 전위 | 상태 |
|------|------|------|
| 0 ms | −70 mV | 휴지 전위 |
| 1 ms | −60 mV | 탈분극 진행 |
| **1.7 ms** | **+30 mV** | **탈분극 정점** |
| 2 ms | 0 mV | 재분극 진행 |
| 3 ms | −80 mV | 과분극 정점 |
| 4 ms | −70 mV | 휴지 회복 |
""")

# ── 파라미터 ──
N = 5
positions = [i * d_interval for i in range(N)]
labels    = [f"d{i+1}" for i in range(N)]
COLORS    = ["#ef4444", "#f97316", "#22c55e", "#38bdf8", "#a78bfa"]
T_FULL    = np.linspace(0, t_max, 600)

# ── 상단 제어 ──
st.title("⚡ 민말이집 신경 흥분 전도 시뮬레이터")

c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 4, 1.5])
with c1:
    if st.button("▶ 재생" if not st.session_state.playing else "⏸ 정지"):
        st.session_state.playing = not st.session_state.playing
with c2:
    if st.button("⏮ 처음"):
        st.session_state.t_now  = 0.0
        st.session_state.playing = False
with c3:
    if st.button("⏭ 끝"):
        st.session_state.t_now  = t_max
        st.session_state.playing = False
with c4:
    sv = st.slider("경과 시간 (ms)", 0.0, float(t_max),
                   float(st.session_state.t_now), 0.05, label_visibility="collapsed")
    if abs(sv - st.session_state.t_now) > 1e-4:
        st.session_state.t_now   = sv
        st.session_state.playing = False
with c5:
    nv = st.number_input("ms", 0.0, float(t_max),
                         float(st.session_state.t_now), 0.1, label_visibility="collapsed")
    if abs(nv - st.session_state.t_now) > 1e-4:
        st.session_state.t_now   = nv
        st.session_state.playing = False

t_now = st.session_state.t_now
v_now_list = [float(get_voltage(t_now - p / v_speed)) for p in positions]

# ── 1. 축삭돌기 모식도 ──
st.markdown("### 🧬 민말이집 축삭 실시간 상태")
fig_ax = go.Figure()

# 축삭 본체
fig_ax.add_shape(type="rect", x0=-0.3, y0=-0.55, x1=positions[-1]+0.3, y1=0.55,
                 fillcolor="#dbeafe", line=dict(color="#1e40af", width=2), layer="below")
# 말이집 구간
for i in range(N - 1):
    fig_ax.add_shape(type="rect",
        x0=positions[i]+0.14, y0=-0.45, x1=positions[i+1]-0.14, y1=0.45,
        fillcolor="#1e3a5f", line=dict(color="#2563eb", width=0.5), layer="below")

# 색상 그라데이션 (전위 분포)
fx = np.linspace(0, positions[-1], 200)
fv = get_voltage(t_now - fx / v_speed)
fig_ax.add_trace(go.Scatter(
    x=fx, y=np.zeros_like(fx), mode='markers',
    marker=dict(size=20, color=fv,
                colorscale=[[0,"#1e3a8a"],[0.4,"#3b82f6"],[0.7,"#fbbf24"],[1,"#ef4444"]],
                cmin=-82, cmax=35, showscale=True,
                colorbar=dict(title="mV", thickness=10, len=0.5, tickvals=[-80,-70,-55,0,30])),
    hoverinfo='none', showlegend=False))

# 결절 마커
for i, (pos, lab, col) in enumerate(zip(positions, labels, COLORS)):
    vp = v_now_list[i]
    fig_ax.add_shape(type="circle", x0=pos-0.13, y0=-0.6, x1=pos+0.13, y1=0.6,
                     fillcolor=col, line=dict(color="white", width=2), layer="above")
    fig_ax.add_annotation(x=pos, y=0.95, text=f"<b>{lab}</b>",
                          font=dict(size=14, color=col), showarrow=False)
    fig_ax.add_annotation(x=pos, y=-1.1, text=f"<b>{vp:.1f} mV</b>",
                          font=dict(size=11, color=col),
                          bgcolor="white", bordercolor=col, borderwidth=1.5,
                          borderpad=3, showarrow=False)

fig_ax.update_layout(height=190, margin=dict(l=10, r=90, t=10, b=10),
    xaxis=dict(range=[-0.5, positions[-1]+0.5], showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(range=[-1.7, 1.5], showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_ax, use_container_width=True)

# ── 2. 세로 스택 그래프 (d1 맨 위, 공유 x축) ──
st.markdown("### 📈 지점별 막전위 변화 — 동일 시간 축 (d1 → d5)")
st.caption("세로 점선: 현재 시간 | ●: 현재 전위 | 컬러 점선: 자극 도달 시점")

fig_st = make_subplots(
    rows=N, cols=1, shared_xaxes=True, vertical_spacing=0.03,
    row_titles=[f"<b>{lab}</b>  {pos:.1f}cm" for lab, pos in zip(labels, positions)]
)

for i, (lab, pos, col) in enumerate(zip(labels, positions, COLORS)):
    row   = i + 1
    t_arr = pos / v_speed
    vf    = get_voltage(T_FULL - pos / v_speed)
    vp    = v_now_list[i]

    # 활동전위 영역 배경
    fig_st.add_hrect(y0=-55, y1=35, fillcolor="rgba(239,68,68,0.05)",
                     line_width=0, row=row, col=1)
    # 기준선
    fig_st.add_hline(y=-70, line=dict(color="#94a3b8", width=1, dash="dot"),
                     row=row, col=1)
    fig_st.add_hline(y=-55, line=dict(color="rgba(251,191,36,0.6)", width=1, dash="dot"),
                     row=row, col=1)
    fig_st.add_hline(y=30, line=dict(color="rgba(239,68,68,0.4)", width=1, dash="dot"),
                     row=row, col=1)

    # 파형
    fig_st.add_trace(go.Scatter(
        x=T_FULL, y=vf, name=lab,
        line=dict(color=col, width=2.2),
        hovertemplate=f"<b>{lab}</b> %{{x:.2f}}ms → %{{y:.1f}}mV<extra></extra>"
    ), row=row, col=1)

    # 현재 시간 선
    fig_st.add_vline(x=t_now,
        line=dict(color="rgba(30,30,30,0.7)", width=1.5, dash="dash"),
        row=row, col=1)

    # 현재 전위 마커
    fig_st.add_trace(go.Scatter(
        x=[t_now], y=[vp], mode='markers+text',
        text=[f"  {vp:.1f}mV"], textposition="middle right",
        textfont=dict(color=col, size=10),
        marker=dict(color=col, size=11, line=dict(width=2, color='white')),
        showlegend=False,
        hovertemplate=f"{lab}: %{{y:.1f}}mV<extra></extra>"
    ), row=row, col=1)

    # 자극 도달 시점
    if t_arr <= t_max:
        fig_st.add_vline(x=t_arr,
            line=dict(color=col, width=1, dash="dot"),
            row=row, col=1)

    fig_st.update_yaxes(
        range=[-90, 50], tickvals=[-80, -70, -55, 0, 30],
        tickfont=dict(size=9), gridcolor="#e2e8f0",
        title_text="mV", title_font=dict(size=10),
        row=row, col=1)

fig_st.update_xaxes(range=[0, t_max], gridcolor="#e2e8f0", tickfont=dict(size=9), zeroline=False)
fig_st.update_xaxes(title_text="시간 (ms)", title_font=dict(size=11), row=N, col=1)
fig_st.update_layout(
    height=155 * N, margin=dict(l=60, r=80, t=20, b=40),
    plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False)
st.plotly_chart(fig_st, use_container_width=True)

# ── 3. 하단 요약 ──
st.markdown("### 📊 현재 측정값")
cols = st.columns(N)
state_lut = [
    (lambda dt: dt < 0,        "자극 미도달",   "#94a3b8"),
    (lambda dt: dt < 1.0,      "탈분극 초기 ↑", "#fbbf24"),
    (lambda dt: dt < 2.0,      "탈분극 진행 ↑", "#ef4444"),
    (lambda dt: dt < 3.0,      "재분극 ↓",      "#f97316"),
    (lambda dt: dt < 4.0,      "과분극 회복",   "#38bdf8"),
    (lambda dt: True,          "휴지 전위",      "#94a3b8"),
]
for i, (lab, pos, col) in enumerate(zip(labels, positions, COLORS)):
    dt   = t_now - pos / v_speed
    vp   = v_now_list[i]
    slab, scol = next((s, c) for fn, s, c in state_lut if fn(dt))
    with cols[i]:
        st.markdown(f"""
<div style="background:white;border-radius:10px;padding:10px;text-align:center;
            border-top:4px solid {col};box-shadow:0 2px 6px rgba(0,0,0,0.07);">
  <div style="font-weight:700;color:{col};font-size:1rem;">{lab}</div>
  <div style="font-size:0.8rem;color:#64748b;">{pos:.1f} cm</div>
  <div style="font-size:1.5rem;font-weight:800;color:{col};margin:4px 0;">
    {vp:.1f}<span style="font-size:0.7rem"> mV</span></div>
  <div style="font-size:0.75rem;font-weight:600;color:{scol};">{slab}</div>
</div>""", unsafe_allow_html=True)

# ── 재생 루프 ──
if st.session_state.playing:
    nxt = st.session_state.t_now + play_step
    if nxt >= t_max:
        nxt = t_max
        st.session_state.playing = False
    st.session_state.t_now = nxt
    time.sleep(0.05)
    st.rerun()
