import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# 페이지 설정
st.set_page_config(
    page_title="신경 흥분 전도 시뮬레이터",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Noto Sans KR', sans-serif; }
    .main { background: #f0f4f8; }
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    div[data-testid="stMetric"] {
        background: white; border-radius: 10px;
        padding: 8px 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .node-badge {
        display: inline-block; width: 24px; height: 24px;
        border-radius: 50%; text-align: center; line-height: 24px;
        font-weight: 700; font-size: 11px; color: white;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 1. 사실적인 막전위 곡선 (piecewise – scipy 불필요)
# ─────────────────────────────────────────────
def _sigmoid(t, t0, k):
    return 1.0 / (1.0 + np.exp(-k * (t - t0)))

def action_potential(t):
    """단일 활동전위 파형 (ms 단위). 범위: -82 ~ +35 mV"""
    if np.isscalar(t):
        t = np.array([float(t)])
        scalar = True
    else:
        t = np.array(t, dtype=float)
        scalar = False

    v = np.full_like(t, -70.0)

    # 탈분극 상승 (0.0 → 1.2 ms): -70 → +35
    rise  = (_sigmoid(t, 0.6, 12) - _sigmoid(t, 0.0, 60)) * (35 - (-70)) + (-70)
    # 재분극 하강 (1.2 → 2.6 ms): +35 → -82
    fall  = (_sigmoid(t, 1.8, 8)  - _sigmoid(t, 1.2, 60)) * (-82 - 35) + 35
    # 과분극 회복 (2.6 → 5.0 ms): -82 → -70
    recov = (_sigmoid(t, 3.8, 5)  - _sigmoid(t, 2.6, 30)) * (-70 - (-82)) + (-82)

    mask1 = (t >= 0.0) & (t < 1.2)
    mask2 = (t >= 1.2) & (t < 2.6)
    mask3 = (t >= 2.6) & (t < 5.5)

    v[mask1] = rise[mask1]
    v[mask2] = fall[mask2]
    v[mask3] = recov[mask3]

    return float(v[0]) if scalar else v

def get_voltage(t):
    """특정 지점에서 자극 후 t ms 경과 시 막전위"""
    if t < 0:
        return -70.0
    return float(action_potential(float(t)))

# ─────────────────────────────────────────────
# 2. 설정
# ─────────────────────────────────────────────
V_SPEED  = 1.0          # 전도 속도 cm/ms
POSITIONS = [0, 1, 2, 3, 4]   # d1~d5 위치 (cm)
LABELS    = ["d1", "d2", "d3", "d4", "d5"]
COLORS    = ["#ef4444", "#f97316", "#22c55e", "#3b82f6", "#a855f7"]
T_MAX     = 10.0        # 최대 시간
T_FULL    = np.linspace(0, T_MAX, 400)  # 전체 시간 축

# 사전 계산: 각 지점 전체 파형
WAVEFORMS = {
    lab: action_potential(T_FULL - pos / V_SPEED)
    for lab, pos in zip(LABELS, POSITIONS)
}

# ─────────────────────────────────────────────
# 3. 세션 상태 (재생 제어)
# ─────────────────────────────────────────────
if "t_play"    not in st.session_state: st.session_state.t_play    = 0.0
if "playing"   not in st.session_state: st.session_state.playing   = False
if "play_step" not in st.session_state: st.session_state.play_step = 0.03  # ms per frame

# ─────────────────────────────────────────────
# 4. 상단 컨트롤
# ─────────────────────────────────────────────
st.title("⚡ 신경 흥분 전도 시뮬레이터 (민말이집 신경)")

ctrl1, ctrl2, ctrl3, ctrl4, ctrl5 = st.columns([2, 1, 1, 1, 2])

with ctrl1:
    slider_t = st.slider("⏱️ 경과 시간 (ms)", 0.0, T_MAX, st.session_state.t_play, step=0.05,
                         key="slider_t")
    # 슬라이더 변경 시 재생 중지 & 시간 업데이트
    if abs(slider_t - st.session_state.t_play) > 1e-6:
        st.session_state.t_play = slider_t
        st.session_state.playing = False

with ctrl2:
    t_num = st.number_input("직접 입력 (ms)", 0.0, T_MAX, st.session_state.t_play,
                            step=0.1, key="num_t")
    if abs(t_num - st.session_state.t_play) > 1e-6:
        st.session_state.t_play = t_num
        st.session_state.playing = False

with ctrl3:
    if st.button("▶ 재생" if not st.session_state.playing else "⏸ 일시정지"):
        st.session_state.playing = not st.session_state.playing
    if st.button("⏮ 처음"):
        st.session_state.t_play = 0.0
        st.session_state.playing = False

with ctrl4:
    speed_label = st.selectbox("재생 속도", ["0.25× (매우 느림)", "0.5× (느림)", "1× (보통)", "2× (빠름)"], index=0)
    speed_map = {"0.25× (매우 느림)": 0.015, "0.5× (느림)": 0.03, "1× (보통)": 0.06, "2× (빠름)": 0.12}
    st.session_state.play_step = speed_map[speed_label]

with ctrl5:
    st.info(f"🕐 현재 시간: **{st.session_state.t_play:.2f} ms** &nbsp;|&nbsp; 전도 속도: **1 cm/ms**")

t_current = st.session_state.t_play

# ─────────────────────────────────────────────
# 5. 축삭돌기 모식도 (Plotly 그림)
# ─────────────────────────────────────────────
st.markdown("### 🧬 민말이집 신경 축삭 — 실시간 전위 상태")

fig_axon = go.Figure()

# 축삭 몸체
fig_axon.add_shape(type="rect",
    x0=-0.3, y0=-1.0, x1=4.3, y1=1.0,
    fillcolor="#dbeafe", line=dict(color="#1e40af", width=3),
    layer="below"
)
# 왼쪽 말이집 마디
fig_axon.add_shape(type="circle",
    x0=-0.5, y0=-1.0, x1=-0.1, y1=1.0,
    fillcolor="#1e40af", line=dict(color="#1e40af"), layer="below"
)
fig_axon.add_shape(type="circle",
    x0=4.1, y0=-1.0, x1=4.5, y1=1.0,
    fillcolor="#1e40af", line=dict(color="#1e40af"), layer="below"
)

# 색상 그라데이션: 현재 시점의 각 위치 전위
fine_x = np.linspace(0, 4, 150)
fine_v = np.array([get_voltage(t_current - x / V_SPEED) for x in fine_x])

fig_axon.add_trace(go.Scatter(
    x=fine_x, y=np.zeros_like(fine_x),
    mode='markers',
    marker=dict(
        size=44, color=fine_v,
        colorscale=[
            [0.0,  "#312e81"],   # -82 mV: 진한 남색
            [0.1,  "#1d4ed8"],   # -70 mV: 파란색 (휴지)
            [0.35, "#7dd3fc"],   # -55 mV: 하늘색 (역치)
            [0.65, "#fde68a"],   # 0 mV
            [1.0,  "#ef4444"],   # +35 mV: 빨간 (활동전위)
        ],
        cmin=-82, cmax=35,
        showscale=True,
        colorbar=dict(title="막전위 (mV)", thickness=12, len=0.6,
                      tickvals=[-82, -70, -55, 0, 35],
                      ticktext=["-82", "-70(휴지)", "-55(역치)", "0", "+35(최고점)"])
    ),
    hoverinfo='none', showlegend=False, name=""
))

# 측정 지점 마커 & 라벨
for i, (pos, label, color) in enumerate(zip(POSITIONS, LABELS, COLORS)):
    v_now = get_voltage(t_current - pos / V_SPEED)

    # 마디 원형
    fig_axon.add_shape(type="circle",
        x0=pos-0.12, y0=-1.05, x1=pos+0.12, y1=1.05,
        fillcolor=color, line=dict(color="white", width=2), layer="above"
    )
    # 지점 이름 (위)
    fig_axon.add_annotation(x=pos, y=1.7, text=f"<b>{label}</b>",
        font=dict(size=13, color=color), showarrow=False)
    # 막전위 값 (아래 – 충분히 내려서 겹치지 않게)
    bg_color = color + "22"
    fig_axon.add_annotation(
        x=pos, y=-1.9,
        text=f"<b>{v_now:.1f} mV</b>",
        font=dict(size=12, color=color),
        bgcolor="white",
        bordercolor=color, borderwidth=1,
        borderpad=3, showarrow=False
    )

fig_axon.update_layout(
    height=200,
    margin=dict(l=10, r=80, t=30, b=50),
    xaxis=dict(range=[-0.7, 4.7], showgrid=False, zeroline=False,
               showticklabels=False, title=""),
    yaxis=dict(range=[-2.8, 2.5], showgrid=False, zeroline=False,
               showticklabels=False),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_axon, use_container_width=True)

# ─────────────────────────────────────────────
# 6. 5개 지점 개별 막전위 그래프 (가로 배치, 컬럼 5개)
# ─────────────────────────────────────────────
st.markdown("### 📈 지점별 막전위 변화 (각 측정점)")
st.caption("각 지점 그래프의 세로 점선이 현재 시간이며, ● 가 현재 막전위를 나타냅니다.")

graph_cols = st.columns(5)

for i, (label, pos, color) in enumerate(zip(LABELS, POSITIONS, COLORS)):
    v_full = WAVEFORMS[label]
    v_now  = get_voltage(t_current - pos / V_SPEED)

    with graph_cols[i]:
        fig_i = go.Figure()

        # 배경 영역 (활동전위 영역 강조)
        fig_i.add_hrect(y0=-55, y1=40, fillcolor="rgba(254,226,226,0.3)",
                        line_width=0, annotation_text="활동전위 구간",
                        annotation_font_size=9, annotation_position="top left")

        # 휴지 전위 기준선
        fig_i.add_hline(y=-70, line_dash="dot", line_color="#94a3b8",
                        annotation_text="-70mV", annotation_font_size=9)
        # 역치 기준선
        fig_i.add_hline(y=-55, line_dash="dot", line_color="#fbbf24",
                        annotation_text="-55mV", annotation_font_size=9)

        # 전체 파형
        fig_i.add_trace(go.Scatter(
            x=T_FULL, y=v_full, name=label,
            line=dict(color=color, width=2.5),
            hovertemplate="시간: %{x:.2f}ms<br>전위: %{y:.1f}mV<extra></extra>"
        ))

        # 현재 시간 수직선
        fig_i.add_vline(x=t_current, line_dash="dash", line_color="#475569", line_width=1.5)

        # 현재 값 마커
        fig_i.add_trace(go.Scatter(
            x=[t_current], y=[v_now],
            mode='markers',
            marker=dict(color=color, size=11, line=dict(width=2, color='white')),
            showlegend=False,
            hovertemplate=f"{label}: %{{y:.1f}}mV<extra></extra>"
        ))

        fig_i.update_layout(
            title=dict(text=f"<b>{label}</b>  ({pos} cm)", font=dict(size=13, color=color),
                       x=0.5, xanchor='center'),
            xaxis=dict(title="시간 (ms)", range=[0, T_MAX], showgrid=True,
                       gridcolor="#f1f5f9", tickfont=dict(size=9)),
            yaxis=dict(title="mV", range=[-90, 50], showgrid=True,
                       gridcolor="#f1f5f9", tickfont=dict(size=9)),
            height=280,
            margin=dict(l=40, r=10, t=45, b=40),
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.plotly_chart(fig_i, use_container_width=True)

# ─────────────────────────────────────────────
# 7. 거리에 따른 막전위 스냅샷 (현재 시점)
# ─────────────────────────────────────────────
st.markdown("### 📏 거리별 막전위 분포 — 스냅샷 (현재 시점)")
st.caption("현재 시간에서 축삭 전체의 막전위 공간 분포를 나타냅니다.")

snap_x = np.linspace(0, 4, 300)
snap_v = np.array([get_voltage(t_current - x / V_SPEED) for x in snap_x])

fig_snap = go.Figure()

# 구역 색상 채우기
fig_snap.add_trace(go.Scatter(
    x=snap_x, y=snap_v,
    fill='tonexty', fillcolor='rgba(59,130,246,0.1)',
    line=dict(color='#3b82f6', width=3),
    name='막전위 분포',
    hovertemplate="거리: %{x:.2f}cm<br>전위: %{y:.1f}mV<extra></extra>"
))
fig_snap.add_hline(y=-70, line_dash="dot", line_color="#94a3b8", annotation_text="휴지전위 -70mV")
fig_snap.add_hline(y=-55, line_dash="dot", line_color="#fbbf24", annotation_text="역치 -55mV")

# 측정 지점 마커
for pos, label, color in zip(POSITIONS, LABELS, COLORS):
    v_p = get_voltage(t_current - pos / V_SPEED)
    fig_snap.add_trace(go.Scatter(
        x=[pos], y=[v_p], mode='markers+text',
        text=[f"{label}<br>{v_p:.1f}mV"],
        textposition="top center",
        marker=dict(size=14, color=color, line=dict(width=2, color='white')),
        showlegend=False,
        hovertemplate=f"{label}: {v_p:.1f}mV<extra></extra>"
    ))

fig_snap.update_layout(
    xaxis=dict(title="거리 (cm)", showgrid=True, gridcolor="#f1f5f9"),
    yaxis=dict(title="막전위 (mV)", range=[-90, 50], showgrid=True, gridcolor="#f1f5f9"),
    height=320, template="plotly_white",
    margin=dict(l=50, r=30, t=20, b=50),
    showlegend=False
)
st.plotly_chart(fig_snap, use_container_width=True)

# ─────────────────────────────────────────────
# 8. 재생 루프 (슬로우모션)
# ─────────────────────────────────────────────
if st.session_state.playing:
    new_t = st.session_state.t_play + st.session_state.play_step
    if new_t >= T_MAX:
        new_t = T_MAX
        st.session_state.playing = False
    st.session_state.t_play = new_t
    time.sleep(0.05)   # 0.05초 딜레이 → 슬로우모션 효과
    st.rerun()
