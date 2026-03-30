import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(page_title="포물선 운동 정밀 데이터 분석", layout="wide")

# CSS를 활용한 엑셀 스타일링
st.markdown("""
    <style>
    .excel-header {
        background-color: #3b82f6;
        color: white;
        padding: 5px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #ddd;
    }
    .excel-value {
        background-color: #f3f4f6;
        padding: 5px;
        text-align: center;
        border: 1px solid #ddd;
    }
    .result-header {
        background-color: #fecaca;
        color: black;
        padding: 5px;
        text-align: center;
        font-weight: bold;
        border: 1px solid #ddd;
    }
    .result-value {
        background-color: #fee2e2;
        padding: 5px;
        text-align: center;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 포물선 운동 정밀 데이터 분석 (Excel 스타일)")

# --- 상단 입력부 및 주요 결과값 ---
col_in1, col_in2, col_res = st.columns([1, 1, 2])

with col_in1:
    theta_deg = st.number_input("발사각 (θ, 도)", min_value=0.0, max_value=90.0, value=30.0, step=1.0)
    v0 = st.number_input("초기 속도 (v₀, m/s)", min_value=1.0, max_value=100.0, value=40.0, step=1.0)

theta = np.radians(theta_deg)
g = 9.8

# 물리량 계산
vx0 = v0 * np.cos(theta)
vy0 = v0 * np.sin(theta)
t_H = vy0 / g  # 최고점 도달 시간
H = (vy0**2) / (2 * g)  # 최고점 높이
t_R = 2 * t_H  # 지면 도달 시간
R = vx0 * t_R  # 수평 도달 거리

with col_in2:
    st.markdown(f'<div class="excel-header">x방향 처음 속도</div><div class="excel-value">{vx0:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="excel-header">y방향 처음 속도</div><div class="excel-value">{vy0:.2f}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="excel-header">중력 가속도</div><div class="excel-value">{g}</div>', unsafe_allow_html=True)

with col_res:
    r_c1, r_c2 = st.columns(2)
    with r_c1:
        st.markdown('<div class="result-header">최고점 도달시간</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-header">최고점의 높이</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-header">수평도달 거리</div>', unsafe_allow_html=True)
    with r_c2:
        st.markdown(f'<div class="result-value">{t_H:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-value">{H:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-value">{R:.2f}</div>', unsafe_allow_html=True)

st.divider()

# --- 데이터 생성 (0.1초 단위) ---
t_steps = np.arange(0, t_R + 0.1, 0.1)
x_vals = vx0 * t_steps
y_vals = np.maximum(vy0 * t_steps - 0.5 * g * t_steps**2, 0)
vx_vals = np.full_like(t_steps, vx0)
vy_vals = vy0 - g * t_steps
ay_vals = np.full_like(t_steps, -g)

df = pd.DataFrame({
    "시간(t)": t_steps,
    "x위치(m)": x_vals,
    "y위치(m)": y_vals,
    "v_x(속도)": vx_vals,
    "v_y(속도)": vy_vals,
    "a_y(가속도)": ay_vals
})

# --- 메인 레이아웃: 표(좌) + 그래프(우) ---
col_table, col_graphs = st.columns([2, 3])

with col_table:
    st.subheader("📋 데이터 시트")
    st.dataframe(df.style.format("{:.2f}"), height=600, use_container_width=True)

with col_graphs:
    st.subheader("📈 물리량 그래프 분석")
    
    # 2x2 서브플롯 생성
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("시간 - x위치", "시간 - y위치", "시간 - vx", "시간 - vy"),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    # Graph 1: x-t
    fig.add_trace(go.Scatter(x=t_steps, y=x_vals, mode='lines+markers', name='x(t)', line=dict(color='blue')), row=1, col=1)
    # Graph 2: y-t
    fig.add_trace(go.Scatter(x=t_steps, y=y_vals, mode='lines+markers', name='y(t)', line=dict(color='red')), row=1, col=2)
    # Graph 3: vx-t
    fig.add_trace(go.Scatter(x=t_steps, y=vx_vals, mode='lines+markers', name='vx(t)', line=dict(color='green')), row=2, col=1)
    # Graph 4: vy-t
    fig.add_trace(go.Scatter(x=t_steps, y=vy_vals, mode='lines+markers', name='vy(t)', line=dict(color='orange')), row=2, col=2)

    fig.update_layout(height=600, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)

st.info("💡 각 수치를 변경하면 표와 그래프가 실시간으로 업데이트됩니다.")
