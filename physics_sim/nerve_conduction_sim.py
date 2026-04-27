import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="신경 흥분 전도 및 전달 시뮬레이터",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 커스텀 CSS (프리미엄 디자인) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3B82F6;
    }
    
    .status-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .highlight {
        color: #1E40AF;
        font-weight: 700;
    }
    
    h1 {
        background: linear-gradient(to right, #1E3A8A, #3B82F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. 막전위 데이터 구성
def get_voltage(t):
    """경과 시간 t(ms)에 따른 막전위(mV) 반환"""
    # 문제 이미지의 전형적인 막전위 곡선 매핑
    times = [0, 1, 1.5, 2, 3, 4, 10]
    volts = [-70, -60, 30, 0, -80, -70, -70]
    
    if t < 0:
        return -70
    return np.interp(t, times, volts)

# --- 헤더 섹션 ---
st.title("⚡ 신경 흥분 전도 및 전달 시뮬레이터")
st.markdown("""
<div style='background-color: rgba(255, 255, 255, 0.7); padding: 20px; border-radius: 10px; margin-bottom: 25px;'>
    <p style='font-size: 1.1rem; color: #374151;'>
        뉴런의 한 지점에 역치 이상의 자극이 주어졌을 때 발생하는 <b>흥분 전도(Conduction)</b>와 
        시냅스를 통해 다음 뉴런으로 신호가 넘어가는 <b>흥분 전달(Transmission)</b>을 시뮬레이션합니다.
    </p>
</div>
""", unsafe_allow_html=True)

# --- 사이드바 제어 ---
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Neuron3.svg/500px-Neuron3.svg.png", width=200)
    st.header("🎮 컨트롤 패널")
    
    v_conduction = st.slider("🏃 전도 속도 (cm/ms)", 0.5, 3.0, 1.0, step=0.1, help="뉴런 내에서 흥분이 이동하는 속도입니다.")
    t_current = st.slider("⏱️ 경과 시간 (ms)", 0.0, 6.0, 4.0, step=0.1, help="자극이 주어진 후 현재까지 흐른 시간입니다.")
    stimulus_origin = st.selectbox("📍 자극 지점", ["d1", "d2", "d3", "d4"], index=1)
    
    st.divider()
    st.write("### 📖 학습 포인트")
    st.info("""
    1. **막전위 변화:** 자극 후 약 1ms에 역치 도달, 1.5ms에 최고점(+30mV)에 도달합니다.
    2. **전도:** 흥분은 양방향으로 이동하며, 속도는 일정하다고 가정합니다.
    3. **전달:** 시냅스에서는 '화학적 신호'로 바뀌어 전달되므로 지연이 발생합니다.
    """)

# --- 데이터 계산 ---
# 위치 정의 (d1=0, d2=1, d3=3, d4=5)
positions = {'d1': 0, 'd2': 1, 'd3': 3, 'd4': 5}
origin_pos = positions[stimulus_origin]

results = []
for name, pos in positions.items():
    dist = abs(pos - origin_pos)
    t_move = dist / v_conduction
    t_graph = t_current - t_move
    voltage = get_voltage(t_graph)
    
    # 실제 자극이 도달했는지 여부
    arrived = t_current >= t_move
    
    results.append({
        "지점": name,
        "위치(cm)": pos,
        "거리(cm)": dist,
        "도착시간(ms)": round(t_move, 2),
        "막전위 변화 시간(ms)": round(max(0, t_graph), 2) if arrived else 0,
        "막전위(mV)": round(voltage, 1) if arrived else -70,
        "상태": "활동전위" if arrived and t_graph < 4 else ("휴지상태" if not arrived else "회복완료")
    })

df_results = pd.DataFrame(results)

# --- 메인 레이아웃: 흥분 전도 시뮬레이션 ---
st.header("1. 민말이집 신경의 흥분 전도")

c1, c2 = st.columns([2, 1])

with c1:
    # Plotly를 이용한 동적 그래프
    t_axis = np.linspace(0, 5, 200)
    v_axis = [get_voltage(t) for t in t_axis]
    
    fig = go.Figure()
    
    # 1. 배경 가이드 라인
    fig.add_trace(go.Scatter(
        x=t_axis, y=v_axis,
        mode='lines',
        name='표준 막전위 곡선',
        line=dict(color='rgba(200, 200, 200, 0.4)', width=3, dash='solid'),
        fill='toself',
        fillcolor='rgba(240, 248, 255, 0.3)'
    ))
    
    # 2. 각 지점의 현재 데이터 포인트
    colors = {'d1': '#EF4444', 'd2': '#10B981', 'd3': '#3B82F6', 'd4': '#F59E0B'}
    for i, row in df_results.iterrows():
        fig.add_trace(go.Scatter(
            x=[row["막전위 변화 시간(ms)"]],
            y=[row["막전위(mV)"]],
            mode='markers+text',
            name=row["지점"],
            marker=dict(size=15, color=colors[row["지점"]], 
                        line=dict(width=2, color='white'),
                        symbol='circle'),
            text=[f"<b>{row['지점']}</b>"],
            textposition="top center",
            hovertemplate=f"지점: {row['지점']}<br>막전위: {row['막전위(mV)']}mV<br>경과시간: {row['막전위 변화 시간(ms)']}ms<extra></extra>"
        ))

    fig.update_layout(
        xaxis_title="<b>자극 후 개별 지점에서의 경과 시간 (ms)</b>",
        yaxis_title="<b>막전위 (mV)</b>",
        yaxis=dict(range=[-90, 50], gridcolor='#E5E7EB'),
        xaxis=dict(range=[-0.5, 5], gridcolor='#E5E7EB'),
        plot_bgcolor='white',
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=40, r=40, t=40, b=40),
        hovermode="closest"
    )
    
    # 임계치 및 주요 선 추가
    fig.add_hline(y=-70, line_dash="dash", line_color="#9CA3AF", annotation_text="휴지 전위 (-70mV)")
    fig.add_hline(y=30, line_dash="dash", line_color="#F87171", annotation_text="활동 전위 정점 (+30mV)")
    fig.add_vline(x=1.5, line_dash="dot", line_color="#3B82F6")

    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.write("### 📊 실시간 측정 데이터")
    st.dataframe(
        df_results[['지점', '막전위(mV)', '상태']],
        use_container_width=True,
        hide_index=True
    )
    
    # 현재 상태 요약 카드
    active_points = df_results[df_results['상태'] == '활동전위']['지점'].tolist()
    status_text = ", ".join(active_points) if active_points else "없음"
    
    st.markdown(f"""
    <div class='status-card'>
        <p style='margin:0; font-size:0.9rem; color:#6B7280;'>현재 자극 위치</p>
        <p style='margin:0; font-size:1.5rem; font-weight:700; color:#1E40AF;'>{stimulus_origin.upper()}</p>
        <hr style='margin:10px 0;'>
        <p style='margin:0; font-size:0.9rem; color:#6B7280;'>활동 전위 발생 지점</p>
        <p style='margin:0; font-size:1.2rem; font-weight:600; color:#EF4444;'>{status_text}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 2. 흥분 전달 (Synaptic Transmission) ---
st.divider()
st.header("2. 시냅스를 통한 흥분 전달")

st.markdown("""
<div style='background-color: #EFF6FF; padding: 20px; border-radius: 10px; border-left: 5px solid #3B82F6;'>
    흥분이 한 뉴런의 <b>축삭 돌기 말단</b>에 도달하면, 시냅스 소포에서 <b>신경 전달 물질</b>(예: 아세틸콜린)이 분비됩니다. 
    이 물질이 다음 뉴런의 가지 돌기에 도달하여 새로운 활동 전위를 일으키기까지는 약 <b>0.5~1.0ms의 지연 시간</b>이 발생합니다.
</div>
""", unsafe_allow_html=True)

col_t1, col_t2 = st.columns([1, 2])

with col_t1:
    st.write("### ⚙️ 전달 파라미터")
    synaptic_delay = st.slider("⏳ 시냅스 지연 시간 (ms)", 0.2, 2.0, 0.8, step=0.1)
    
    # 시냅스 전/후 관계 설정
    st.info("💡 **가정:** 뉴런 A(d1, d2)와 뉴런 B(d3, d4) 사이에 시냅스가 존재함.")
    
    # d2(말단) 도착 시간
    d2_arrival = df_results[df_results['지점'] == 'd2']['도착시간(ms)'].values[0]
    # d3(다음 뉴런 시작) 도착 시간 = d2 도착 + 지연 + (d3-d2)/v (전달 거리가 매우 짧다고 가정하면 delay만 추가)
    d3_arrival_with_delay = d2_arrival + synaptic_delay
    
    st.metric("뉴런 A 말단 도달", f"{d2_arrival} ms")
    st.metric("뉴런 B 자극 발생", f"{round(d3_arrival_with_delay, 2)} ms")

with col_t2:
    st.write("### 📈 전도 vs 전달 비교")
    
    t_range = np.linspace(0, 6, 300)
    
    # 뉴런 A의 말단 (d2) 막전위
    v_d2_list = [get_voltage(t - d2_arrival) if t >= d2_arrival else -70 for t in t_range]
    
    # 뉴런 B의 시작 (d3) 막전위 (전달 지연 포함)
    v_d3_list = [get_voltage(t - d3_arrival_with_delay) if t >= d3_arrival_with_delay else -70 for t in t_range]
    
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Scatter(x=t_range, y=v_d2_list, name="뉴런 A 말단 (d2)", line=dict(color='#10B981', width=3)))
    fig_comp.add_trace(go.Scatter(x=t_range, y=v_d3_list, name="뉴런 B 시작 (d3)", line=dict(color='#EF4444', width=3, dash='dash')))
    
    # 현재 시간 표시선
    fig_comp.add_vline(x=t_current, line_width=2, line_color="#374151", annotation_text="현재 시간")
    
    # 지연 영역 표시
    if t_current > d2_arrival:
        delay_end = min(t_current, d3_arrival_with_delay)
        fig_comp.add_vrect(x0=d2_arrival, x1=d3_arrival_with_delay, fillcolor="#DBEAFE", opacity=0.5, layer="below", line_width=0, annotation_text="시냅스 지연")

    fig_comp.update_layout(
        xaxis_title="전체 경과 시간 (ms)",
        yaxis_title="막전위 (mV)",
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# --- 푸터 ---
st.divider()
st.markdown(f"""
<div style='text-align: center; color: #9CA3AF; font-size: 0.8rem; padding: 20px;'>
    © {datetime.now().year} 신경 흥분 전도 교육용 시뮬레이터 | 물리/생명과학 가상 실험실
</div>
""", unsafe_allow_html=True)
