import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

st.set_page_config(
    page_title="민말이집 신경 흥분 전도 시뮬레이터",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Noto Sans KR', sans-serif; }
    .main { background: #0f172a; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }
    section[data-testid="stSidebar"] { background: #1e293b; }
    section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
    h1, h2, h3 { color: #f8fafc !important; }
    .param-box {
        background: #1e293b; border-radius: 12px;
        padding: 14px 18px; margin-bottom: 10px;
        border: 1px solid #334155;
    }
    .ap-table {
        background: #1e293b; border-radius: 10px;
        padding: 10px; border: 1px solid #334155;
        font-size: 0.85rem; color: #e2e8f0;
    }
    .ap-table td, .ap-table th { padding: 4px 10px; }
    .ap-table th { color: #7dd3fc; border-bottom: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────
# 1. 막전위 함수 — 사진의 데이터값 기반
#    0ms: -70, 1ms: -60, 1.7ms: +30, 2ms: 0, 3ms: -80, 4ms: -70
# ──────────────────────────────────────────
AP_TIMES = np.array([0.0, 1.0, 1.7, 2.0, 3.0, 4.0])
AP_VOLTS = np.array([-70.0, -60.0, 30.0, 0.0, -80.0, -70.0])

def get_voltage(t):
    """단일 활동전위 파형 (제시된 데이터 기반, 부드러운 보간)"""
    if np.isscalar(t):
        if t < 0:
            return -70.0
        return float(np.interp(t, AP_TIMES, AP_VOLTS, left=-70.0, right=-70.0))
    else:
        t = np.asarray(t, dtype=float)
        v = np.interp(t, AP_TIMES, AP_VOLTS, left=-70.0, right=-70.0)
        v[t < 0] = -70.0
        return v

# ──────────────────────────────────────────
# 2. 사이드바 — 시뮬레이션 파라미터
# ──────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔬 시뮬레이션 조건")

    st.markdown("### ⚡ 활동전위 기준값")
    st.markdown("""
    <div class='ap-table'>
    <table>
    <tr><th>시간</th><th>상태</th><th>전위 (mV)</th></tr>
    <tr><td>0 ms</td><td>자극 직후 (휴지)</td><td style='color:#60a5fa'>-70</td></tr>
    <tr><td>1 ms</td><td>탈분극 진행 중</td><td style='color:#fbbf24'>-60</td></tr>
    <tr><td>1.7 ms</td><td>탈분극 정점</td><td style='color:#ef4444'>+30</td></tr>
    <tr><td>2 ms</td><td>재분극 진행 중</td><td style='color:#a78bfa'>0</td></tr>
    <tr><td>3 ms</td><td>과분극 정점</td><td style='color:#06b6d4'>-80</td></tr>
    <tr><td>4 ms</td><td>휴지 전위 복귀</td><td style='color:#60a5fa'>-70</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📐 전도 조건")
    v_speed = st.slider("전도 속도 (cm/ms)", 0.5, 3.0, 1.0, 0.1,
                        help="민말이집 신경의 경우 1~3 cm/ms 수준")
    d_interval = st.slider("결절 간격 (cm)", 0.5, 2.0, 1.0, 0.1,
                           help="결절과 결절 사이의 거리")
    t_max = st.slider("그래프 표시 최대 시간 (ms)", 6.0, 20.0, 10.0, 1.0)

    n_nodes = 5  # d1~d5 고정

    st.markdown("---")
    st.markdown("### 🎮 재생 제어")
    speed_option = st.selectbox(
        "재생 속도",
        ["0.1× (초슬로우)", "0.25× (매우 느림)", "0.5× (느림)", "1× (보통)"],
        index=1
    )
    play_step_map = {
        "0.1× (초슬로우)": 0.008,
        "0.25× (매우 느림)": 0.02,
        "0.5× (느림)": 0.04,
        "1× (보통)": 0.08,
    }
    play_step = play_step_map[speed_option]

# ──────────────────────────────────────────
# 3. 세션 상태
# ──────────────────────────────────────────
if "t_now"    not in st.session_state: st.session_state.t_now    = 0.0
if "playing"  not in st.session_state: st.session_state.playing  = False

# 위치 계산
positions = [i * d_interval for i in range(n_nodes)]
labels    = [f"d{i+1}" for i in range(n_nodes)]
COLORS    = ["#ef4444", "#f97316", "#22c55e", "#38bdf8", "#a78bfa"]
T_FULL    = np.linspace(0, t_max, 500)

# ──────────────────────────────────────────
# 4. 상단 컨트롤 바
# ──────────────────────────────────────────
st.markdown("# ⚡ 민말이집 신경 흥분 전도 시뮬레이터")

b1, b2, b3, sl_col, num_col = st.columns([1, 1, 1, 4, 1.5])
with b1:
    if st.button("▶ 재생" if not st.session_state.playing else "⏸ 일시정지", use_container_width=True):
        st.session_state.playing = not st.session_state.playing
with b2:
    if st.button("⏮ 처음", use_container_width=True):
        st.session_state.t_now   = 0.0
        st.session_state.playing = False
with b3:
    if st.button("⏭ 끝", use_container_width=True):
        st.session_state.t_now   = t_max
        st.session_state.playing = False

with sl_col:
    slider_val = st.slider("경과 시간 (ms)", 0.0, float(t_max),
                           float(st.session_state.t_now), 0.05,
                           key="slider_main", label_visibility="collapsed")
    if abs(slider_val - st.session_state.t_now) > 1e-4:
        st.session_state.t_now   = slider_val
        st.session_state.playing = False

with num_col:
    t_num = st.number_input("직접 입력 (ms)", 0.0, float(t_max),
                            float(st.session_state.t_now), 0.1,
                            key="num_main", label_visibility="collapsed")
    if abs(t_num - st.session_state.t_now) > 1e-4:
        st.session_state.t_now   = t_num
        st.session_state.playing = False

t_now = st.session_state.t_now

# 현재 각 지점 전위
v_now_list = [get_voltage(t_now - pos / v_speed) for pos in positions]

# ──────────────────────────────────────────
# 5. 축삭 모식도
# ──────────────────────────────────────────
st.markdown("#### 🧬 축삭돌기 실시간 전위 상태")

fig_axon = go.Figure()

# 세밀한 전위 분포 계산
fine_x = np.linspace(0, positions[-1], 300)
fine_v = get_voltage(t_now - fine_x / v_speed)

# 축삭 본체 (긴 캡슐)
fig_axon.add_shape(type="rect",
    x0=-0.2, y0=-0.6, x1=positions[-1]+0.2, y1=0.6,
    fillcolor="#0f172a", line=dict(color="#334155", width=2), layer="below"
)
# 말이집(미엘린) 구간 표현 (결절 사이)
for i in range(n_nodes - 1):
    x_left  = positions[i] + 0.15
    x_right = positions[i+1] - 0.15
    fig_axon.add_shape(type="rect",
        x0=x_left, y0=-0.5, x1=x_right, y1=0.5,
        fillcolor="#1e3a5f", line=dict(color="#2563eb", width=1), layer="below"
    )

# 전위 색상 그라데이션 (마커 점들)
fig_axon.add_trace(go.Scatter(
    x=fine_x, y=np.zeros_like(fine_x),
    mode='markers',
    marker=dict(
        size=22,
        color=fine_v,
        colorscale=[
            [0.00, "#1e3a8a"],   # -80 mV: 짙은 파랑 (과분극)
            [0.12, "#3b82f6"],   # -70 mV: 파랑 (휴지)
            [0.25, "#fbbf24"],   # -60 mV: 노랑 (역치 근접)
            [0.55, "#f97316"],   # 0 mV: 주황
            [1.00, "#ef4444"],   # +30 mV: 빨강 (활동전위)
        ],
        cmin=-82, cmax=35,
        showscale=True,
        colorbar=dict(
            title=dict(text="막전위(mV)", font=dict(color="#94a3b8")),
            tickvals=[-80, -70, -60, 0, 30],
            ticktext=["-80", "-70(휴지)", "-60", "0", "+30"],
            tickfont=dict(color="#94a3b8", size=10),
            thickness=12, len=0.7, x=1.02
        )
    ),
    hoverinfo='none', showlegend=False
))

# 결절 마커 + 라벨(위) + 전위값(아래)
for i, (pos, label, color) in enumerate(zip(positions, labels, COLORS)):
    v_pt = v_now_list[i]
    # 결절 원형
    fig_axon.add_shape(type="circle",
        x0=pos-0.12, y0=-0.65, x1=pos+0.12, y1=0.65,
        fillcolor=color, line=dict(color="white", width=2), layer="above"
    )
    # 라벨 (위)
    fig_axon.add_annotation(
        x=pos, y=1.1, text=f"<b>{label}</b>",
        font=dict(size=14, color=color), showarrow=False, bgcolor="rgba(0,0,0,0)"
    )
    # 전위 값 (아래 — 박스)
    fig_axon.add_annotation(
        x=pos, y=-1.25, text=f"<b>{v_pt:.1f} mV</b>",
        font=dict(size=12, color=color),
        bgcolor="#0f172a", bordercolor=color, borderwidth=1.5, borderpad=3,
        showarrow=False
    )
    # 간격 표시 (첫 번째 결절 제외)
    if i > 0:
        fig_axon.add_annotation(
            x=(positions[i-1]+pos)/2, y=-0.9,
            text=f"<i>{d_interval}cm</i>",
            font=dict(size=10, color="#64748b"), showarrow=False
        )

fig_axon.update_layout(
    height=210, margin=dict(l=10, r=80, t=20, b=20),
    xaxis=dict(range=[-0.5, positions[-1]+0.5], showgrid=False,
               zeroline=False, showticklabels=False),
    yaxis=dict(range=[-1.8, 1.7], showgrid=False, zeroline=False, showticklabels=False),
    plot_bgcolor="#0f172a", paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_axon, use_container_width=True)

# ──────────────────────────────────────────
# 6. 세로 스택 그래프 (d1 맨 위, 공유 x축)
# ──────────────────────────────────────────
st.markdown("#### 📈 지점별 막전위 변화 (d1 ~ d5 순서, 동일 시간 축)")
st.caption("세로 점선이 현재 시간 위치이며, ● 는 현재 막전위 값을 나타냅니다. 각 그래프의 파형 지연으로 흥분 전도 속도를 확인하세요.")

fig_stack = make_subplots(
    rows=n_nodes, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.04,
    row_titles=[f"<b>{lab}</b> ({pos:.1f}cm)" for lab, pos in zip(labels, positions)]
)

for i, (label, pos, color) in enumerate(zip(labels, positions, COLORS)):
    row = i + 1
    t_arr = pos / v_speed   # 자극 도달 시간
    v_full = get_voltage(T_FULL - pos / v_speed)
    v_pt   = v_now_list[i]

    # 과분극/역치 배경
    fig_stack.add_hrect(y0=-55, y1=35, fillcolor="rgba(239,68,68,0.06)",
                        line_width=0, row=row, col=1)

    # 휴지 전위선
    fig_stack.add_shape(type="line",
        x0=0, x1=t_max, y0=-70, y1=-70,
        line=dict(color="#475569", width=1, dash="dot"),
        row=row, col=1
    )
    # 역치선
    fig_stack.add_shape(type="line",
        x0=0, x1=t_max, y0=-55, y1=-55,
        line=dict(color="#fbbf2480", width=1, dash="dot"),
        row=row, col=1
    )

    # 전체 파형
    fig_stack.add_trace(go.Scatter(
        x=T_FULL, y=v_full, name=label,
        line=dict(color=color, width=2.5),
        hovertemplate=f"<b>{label}</b><br>시간: %{{x:.2f}}ms<br>전위: %{{y:.1f}}mV<extra></extra>"
    ), row=row, col=1)

    # 현재 시간 수직선
    fig_stack.add_shape(type="line",
        x0=t_now, x1=t_now, y0=-90, y1=45,
        line=dict(color="#f8fafc", width=1.5, dash="dash"),
        row=row, col=1
    )

    # 현재 전위 마커
    fig_stack.add_trace(go.Scatter(
        x=[t_now], y=[v_pt],
        mode='markers+text',
        text=[f" {v_pt:.1f}mV"],
        textposition="middle right",
        textfont=dict(color=color, size=11),
        marker=dict(color=color, size=12, line=dict(width=2, color='white')),
        showlegend=False,
        hovertemplate=f"{label}: %{{y:.1f}}mV<extra></extra>"
    ), row=row, col=1)

    # 자극 도달 시점 표시
    if t_arr <= t_max:
        fig_stack.add_shape(type="line",
            x0=t_arr, x1=t_arr, y0=-90, y1=45,
            line=dict(color=color + "80", width=1, dash="dot"),
            row=row, col=1
        )

    fig_stack.update_yaxes(
        range=[-90, 50],
        tickvals=[-80, -70, -55, 0, 30],
        tickfont=dict(size=9, color="#94a3b8"),
        gridcolor="#1e293b", gridwidth=1,
        zeroline=False,
        title_text="mV", title_font=dict(size=10, color="#64748b"),
        row=row, col=1
    )

# x축 공통 설정 (마지막 행만 라벨 표시)
fig_stack.update_xaxes(
    range=[0, t_max],
    gridcolor="#1e293b",
    tickfont=dict(size=10, color="#94a3b8"),
    zeroline=False,
)
fig_stack.update_xaxes(
    title_text="시간 (ms)", title_font=dict(size=11, color="#94a3b8"),
    row=n_nodes, col=1
)

fig_stack.update_layout(
    height=160 * n_nodes,
    margin=dict(l=60, r=60, t=20, b=40),
    plot_bgcolor="#0f172a",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e2e8f0"),
    showlegend=False,
)
st.plotly_chart(fig_stack, use_container_width=True)

# ──────────────────────────────────────────
# 7. 하단 — 현재 전위 요약 표
# ──────────────────────────────────────────
st.markdown("#### 📊 현재 시점 측정값 요약")
cols = st.columns(n_nodes)
for i, (label, pos, color) in enumerate(zip(labels, positions, COLORS)):
    v_pt   = v_now_list[i]
    t_arr  = pos / v_speed
    arrived = t_now >= t_arr
    if not arrived:
        state = "자극 미도달"
        s_color = "#475569"
    elif t_now - t_arr < 1.7:
        state = "탈분극 ↑"
        s_color = "#ef4444"
    elif t_now - t_arr < 3.0:
        state = "재분극 ↓"
        s_color = "#f97316"
    elif t_now - t_arr < 4.0:
        state = "과분극"
        s_color = "#38bdf8"
    else:
        state = "휴지 회복"
        s_color = "#64748b"

    with cols[i]:
        st.markdown(f"""
        <div style="background:#1e293b; border-radius:10px; padding:12px 10px;
                    text-align:center; border-top: 4px solid {color}; border: 1px solid #334155;">
            <div style="font-size:1.1rem; font-weight:700; color:{color};">{label}</div>
            <div style="font-size:0.8rem; color:#94a3b8;">{pos:.1f} cm</div>
            <div style="font-size:1.5rem; font-weight:800; color:{color};
                        margin: 6px 0;">{v_pt:.1f}<span style="font-size:0.75rem;"> mV</span></div>
            <div style="font-size:0.8rem; font-weight:600; color:{s_color};">{state}</div>
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────
# 8. 재생 루프
# ──────────────────────────────────────────
if st.session_state.playing:
    new_t = st.session_state.t_now + play_step
    if new_t >= t_max:
        new_t = t_max
        st.session_state.playing = False
    st.session_state.t_now = new_t
    time.sleep(0.05)
    st.rerun()
