import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
try:
    from scipy.interpolate import interp1d
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

# 페이지 설정
st.set_page_config(
    page_title="신경 흥분 전도 동적 시뮬레이터",
    page_icon="⚡",
    layout="wide"
)

# --- 커스텀 CSS (프리미엄 & 슬림 디자인) ---
st.markdown("""
<style>
    .main {
        background-color: #f1f5f9;
    }
    .stNumberInput, .stSlider {
        background: white;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    .metric-container {
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    h2, h3 {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# 1. 사실적인 막전위 곡선 정의
def get_voltage_fn():
    # 주요 지점: t(ms), V(mV)
    # 0:자극, 0.8:역치(-55), 1.2:정점(+35), 2.0:재분극(-70), 3.0:과분극(-80), 4.5:회복(-70)
    times = [0, 0.8, 1.2, 1.6, 2.2, 3.2, 5.0]
    volts = [-70, -55, 35, 10, -70, -82, -70]
    
    if HAS_SCIPY:
        f = interp1d(times, volts, kind='cubic', fill_value=(-70, -70), bounds_error=False)
        return f
    else:
        # Scipy가 없을 경우 Numpy 선형 보간으로 대체
        return lambda t: np.interp(t, times, volts, left=-70, right=-70)

ap_func = get_voltage_fn()

def get_voltage(t):
    if t < 0: return -70.0
    return float(ap_func(t))

# --- 컨트롤 영역 (상단 고정) ---
st.title("⚡ 신경 흥분 전도 동적 시뮬레이터")

c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    t_current = st.slider("⏱️ 경과 시간 (ms)", 0.0, 8.0, 2.0, step=0.05)
with c2:
    t_input = st.number_input("시간 직접 입력 (ms)", 0.0, 8.0, t_current, step=0.1)
    # 입력 시 동기화 (단순화)
    if t_input != t_current:
        t_current = t_input
with c3:
    v_speed = st.slider("🏃 전도 속도 (cm/ms)", 0.5, 2.0, 1.0, step=0.1)

# --- 파라미터 ---
positions = np.array([0, 1, 2, 3, 4])  # d1, d2, d3, d4, d5
labels = ["d1", "d2", "d3", "d4", "d5"]
current_voltages = [get_voltage(t_current - pos/v_speed) for pos in positions]

# --- 시각화 1: 동적 뉴런 모식도 (실시간 전위 반영) ---
st.subheader("🧬 뉴런 축삭(Axon) 실시간 상태")

# Axon 베이스라인
axon_x = np.linspace(-0.5, 4.5, 200)
# 각 지점의 색상 결정 (막전위에 따라)
# -70: 파란색(휴지), +35: 빨간색(흥분), -82: 보라색(과분극)
def val_to_color(v):
    # Normalized value for color mapping (-82 to 40)
    norm = (v + 82) / (40 + 82)
    return f"interpolateRdBu({1 - norm})" # Plotly logic simplified later

fig_axon = go.Figure()

# Axon 몸체 (직사각형 형태)
fig_axon.add_shape(type="rect", x0=-0.5, y0=-0.2, x1=4.5, y1=0.2, 
                   fillcolor="#f8fafc", line=dict(color="#cbd5e1", width=2))

# 전위 변화를 나타내는 그라데이션 (현재 시간에 따른 축삭 전체 전위)
fine_x = np.linspace(-0.5, 4.5, 100)
fine_v = [get_voltage(t_current - x/v_speed) for x in fine_x]
fig_axon.add_trace(go.Scatter(
    x=fine_x, y=[0]*len(fine_x),
    mode='markers',
    marker=dict(
        size=40,
        color=fine_v,
        colorscale='RdBu',
        cmin=-85, cmax=40,
        reversescale=True,
        showscale=True,
        colorbar=dict(title="막전위 (mV)", orientation='h', y=-0.5)
    ),
    hoverinfo='none',
    name='전위 분포'
))

# 측정 지점 표시 (d1~d5)
for i, (pos, label) in enumerate(zip(positions, labels)):
    v_now = current_voltages[i]
    fig_axon.add_trace(go.Scatter(
        x=[pos], y=[0],
        mode='markers+text',
        text=[f"<b>{label}</b><br>{round(v_now,1)}mV"],
        textposition="top center",
        marker=dict(size=15, color="black", line=dict(width=2, color="white")),
        name=label,
        showlegend=False
    ))

fig_axon.update_layout(
    height=250,
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(showgrid=False, zeroline=False, range=[-0.7, 4.7], title="거리 (cm)"),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1, 1]),
    plot_bgcolor='rgba(0,0,0,0)',
    title="축삭 내부의 실시간 흥분 전파 상태"
)
st.plotly_chart(fig_axon, use_container_width=True)

# --- 시각화 2: 그래프 분석 ---
st.divider()
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📉 시간에 따른 막전위 변화 (V-t)")
    # 5개 지점의 V-t 그래프를 하나의 차트에 오버레이
    fig_vt = go.Figure()
    t_range = np.linspace(0, 8, 300)
    colors = ['#ef4444', '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6']
    
    for i, (pos, label) in enumerate(zip(positions, labels)):
        v_vals = [get_voltage(t - pos/v_speed) for t in t_range]
        fig_vt.add_trace(go.Scatter(
            x=t_range, y=v_vals, name=label, 
            line=dict(color=colors[i], width=2)
        ))
    
    # 현재 시간 수직선
    fig_vt.add_vline(x=t_current, line_dash="dash", line_color="#334155", 
                     annotation_text=f"현재: {t_current}ms")
    
    fig_vt.update_layout(
        xaxis_title="시간 (ms)",
        yaxis_title="막전위 (mV)",
        template="plotly_white",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_vt, use_container_width=True)

with col_right:
    st.subheader("📏 거리에 따른 막전위 분포 (V-x)")
    # 현재 시점 t에서 거리 x에 따른 전위 분포
    x_range = np.linspace(-0.5, 4.5, 200)
    v_dist = [get_voltage(t_current - x/v_speed) for x in x_range]
    
    fig_vx = go.Figure()
    fig_vx.add_trace(go.Scatter(
        x=x_range, y=v_dist, fill='tozeroy', 
        name='거리별 전위', line=dict(color='#3b82f6', width=3)
    ))
    
    # 지점별 마커
    fig_vx.add_trace(go.Scatter(
        x=positions, y=current_voltages, 
        mode='markers', 
        marker=dict(size=12, color=colors, symbol='circle'),
        name='측정 지점'
    ))

    fig_vx.update_layout(
        xaxis_title="거리 (cm)",
        yaxis_title="막전위 (mV)",
        template="plotly_white",
        height=400,
        yaxis=dict(range=[-90, 50]),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_vx, use_container_width=True)

# --- 하단 측정 데이터 ---
st.markdown("### 📊 실시간 측정 데이터 요약")
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.markdown(f"""
        <div style="background:white; padding:10px; border-radius:10px; text-align:center; border-top: 4px solid {colors[i]};">
            <p style="margin:0; font-weight:bold; color:#64748b;">{labels[i]}</p>
            <p style="margin:0; font-size:1.4rem; font-weight:800;">{round(current_voltages[i], 1)} <span style="font-size:0.8rem;">mV</span></p>
        </div>
        """, unsafe_allow_html=True)

st.info(f"💡 **현재 상태 요약:** {t_current}ms 시점에서 흥분은 자극 원점(d1)으로부터 약 {round(t_current * v_speed, 2)}cm 지점을 지나고 있습니다.")
