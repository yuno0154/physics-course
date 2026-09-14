import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 인쇄 및 스타일 CSS 설정 ---
st.markdown("""
    <style>
    @media print {
        @page { margin: 10mm; }
        .stApp { height: auto !important; overflow: visible !important; }
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stActionButton, button, [data-testid="stRadio"] { display: none !important; }
        .main .block-container { padding: 0 !important; }
        .stMarkdown, .stPlotlyChart { page-break-inside: avoid; margin-bottom: 0px !important; }
        h1 { font-size: 1.3rem !important; margin-bottom: 8px !important; }
        h2 { font-size: 1.1rem !important; margin-top: 10px !important; margin-bottom: 6px !important; }
        h3 { font-size: 0.95rem !important; margin-top: 5px !important; margin-bottom: 5px !important; }
        p, li { font-size: 0.85rem !important; line-height: 1.25 !important; }
        .stDivider { margin-top: 4px !important; margin-bottom: 4px !important; }
        .no-print { display: none !important; }
    }
    .print-header { font-size: 0.95rem; font-weight: bold; margin-bottom: 12px; border-bottom: 2px solid #1e293b; padding-bottom: 6px; }
    .answer-space { border-bottom: 1px solid #94a3b8; height: 28px; margin-bottom: 6px; width: 100%; }
    .exam-box { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; }
    .badge-primary { background-color: #eff6ff; color: #1d4ed8; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-success { background-color: #ecfdf5; color: #047857; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-purple { background-color: #faf5ff; color: #7e22ce; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-amber { background-color: #fffbeb; color: #b45309; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    
    /* 인쇄용 에너지 막대그래프 틀 */
    .bar-chart-container { display: flex; gap: 24px; justify-content: center; margin: 12px 0; }
    .bar-chart-card { border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; background: white; text-align: center; width: 220px; }
    .bar-chart-title { font-size: 0.82rem; font-weight: bold; margin-bottom: 6px; }
    .bar-chart-frame { height: 120px; border-left: 2px solid #334155; border-bottom: 2px solid #334155; display: flex; justify-content: space-around; align-items: flex-end; padding: 0 4px; position: relative; }
    .bar-chart-bar-outline { width: 42px; border: 1.5px dashed #64748b; height: 105px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #64748b; font-weight: bold; background: #f8fafc; }
    .bar-chart-labels { display: flex; justify-content: space-around; margin-top: 4px; font-size: 0.72rem; color: #475569; }
    .tick-50 { position: absolute; top: 8px; left: -24px; font-size: 0.65rem; color: #64748b; }
    .tick-0 { position: absolute; bottom: 0px; left: -16px; font-size: 0.65rem; color: #64748b; }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 포물선 운동 실전 연습 문제")

# --- 출력 모드 선택 ---
col_mode1, col_mode2 = st.columns([1.8, 1])
with col_mode1:
    is_print_mode = st.toggle("🖨️ 학습지 출력 모드 전환 (인쇄 및 PDF 저장용)", value=False)
with col_mode2:
    if is_print_mode:
        if st.button("🖨️ 브라우저 바로 인쇄 / PDF 저장", use_container_width=True):
            st.components.v1.html("<script>parent.window.print()</script>", height=0)

if is_print_mode:
    st.markdown('<div class="print-header">📝 포물선 운동 실전 연습 학습지 &nbsp; [ 학년: ____ &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["🎯 실전 기출 & 활동지 연계 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    본 페이지는 **기본 개념 점검 문항**부터 활동 6 연계 **에너지 막대그래프 분석**, **수능·내신 빈출 유형 심화 문항**까지 단계별로 구성되어 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["🎯 실전 기출 & 활동지 연계 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 벡터 도식 생성 함수군
# =========================================================================

def get_diagram_independence(h=30):
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=50, y1=0, line=dict(color="#334155", width=2.5))
    fig.add_shape(type="rect", x0=-2, y0=0, x1=0, y1=h, fillcolor="#e2e8f0", line=dict(color="#475569"))
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=13, color='#ef4444', line=dict(width=2, color='black')), name="공 A (자유낙하)"))
    fig.add_trace(go.Scatter(x=[0], y=[h], mode='markers', marker=dict(size=13, color='#3b82f6', line=dict(width=2, color='black')), name="공 B (수평투사)"))
    fig.add_annotation(x=10, y=h, ax=0, ay=h, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#2563eb", arrowwidth=3)
    t = np.linspace(0, np.sqrt(2*h/10), 20)
    fig.add_trace(go.Scatter(x=np.zeros_like(t), y=h-0.5*10*t**2, mode='lines', line=dict(color='#ef4444', dash='dot', width=2), showlegend=False))
    fig.add_trace(go.Scatter(x=15*t, y=h-0.5*10*t**2, mode='lines', line=dict(color='#3b82f6', dash='dot', width=2), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-10, 55]), yaxis=dict(visible=False, range=[-5, h+10]), height=180, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig

def get_diagram_q3(v0=10, theta_deg=30):
    theta = np.radians(theta_deg); vx = v0 * np.cos(theta); vy = v0 * np.sin(theta)
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=20, y1=0, line=dict(color="#334155", width=2.5))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=13, color='#0ea5e9', line=dict(width=2, color='black')), showlegend=False))
    fig.add_annotation(x=vx*0.8, y=vy*0.8, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#0284c7", arrowwidth=3.5)
    fig.add_annotation(x=vx+2.5, y=vy+1.5, text="<b>v₀=10m/s, θ=30°</b>", showarrow=False, font=dict(size=13, color="#0369a1"))
    t_land = 2*vy/10; t = np.linspace(0, t_land, 30); fig.add_trace(go.Scatter(x=vx*t, y=vy*t-0.5*10*t**2, mode='lines', line=dict(color='#94a3b8', dash='dot', width=2), showlegend=False))
    fig.update_layout(xaxis=dict(visible=False, range=[-5, 15]), yaxis=dict(visible=False, range=[-2, 5]), height=170, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

def get_diagram_q5():
    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=30, y1=0, line=dict(color="#334155", width=2.5))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=11, color='#f97316'), showlegend=False))
    t = np.linspace(0, 1, 15); vx=5; v_y0=30; g=9.8; x=vx*t; y=v_y0*t-0.5*g*t**2
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#ea580c', width=2.5), showlegend=False))
    fig.add_annotation(x=vx*1+3.5, y=y[-1], text="<b>1초 (25m)</b>", showarrow=False, font=dict(size=13, color="#c2410c"))
    fig.add_shape(type="line", x0=vx*1, y0=0, x1=vx*1, y1=y[-1], line=dict(color="#3b82f6", dash="dash", width=1.5))
    fig.update_layout(xaxis=dict(visible=False, range=[-5, 30]), yaxis=dict(visible=False, range=[-5, 50]), height=170, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor="white")
    return fig

# --- [신규 실전 문항 도식 함수] ---

def get_diagram_prob1():
    """문제 1: 질량 2kg, 30도, 40m/s 도식"""
    v0 = 40.0; theta = np.radians(30.0); g = 10.0
    vx = v0 * np.cos(theta); vy = v0 * np.sin(theta)
    t_h = vy / g; H = (vy**2) / (2 * g)
    t_land = 2 * t_h; R = vx * t_land

    t = np.linspace(0, t_land, 60)
    x = vx * t; y = vy * t - 0.5 * g * t**2

    fig = go.Figure()
    # 지면
    fig.add_shape(type="line", x0=-15, y0=0, x1=R+25, y1=0, line=dict(color="#1e293b", width=3))
    # 궤적
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#475569', dash='dash', width=2), showlegend=False))
    # 발사 지점 공
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=14, color='#2563eb', line=dict(width=2, color='black')), showlegend=False))
    # 초기 속도 화살표
    fig.add_annotation(x=vx*0.7, y=vy*0.7, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#1d4ed8", arrowwidth=3.5)
    fig.add_annotation(x=vx*0.7+8, y=vy*0.7+2, text="<b>v₀ = 40 m/s<br>(30°)</b>", showarrow=False, font=dict(size=13, color="#1e40af"))
    # 각도 호 (Arc)
    arc_angles = np.linspace(0, theta, 20)
    arc_r = 18.0
    fig.add_trace(go.Scatter(x=arc_r*np.cos(arc_angles), y=arc_r*np.sin(arc_angles), mode='lines', line=dict(color='#d97706', width=2), showlegend=False))
    fig.add_annotation(x=arc_r*1.3, y=arc_r*0.35, text="30°", showarrow=False, font=dict(size=12, color="#b45309", weight="bold"))
    # 최고점 마커 및 H 표시선
    x_H = vx * t_h
    fig.add_trace(go.Scatter(x=[x_H], y=[H], mode='markers', marker=dict(size=10, color='#dc2626'), showlegend=False))
    fig.add_shape(type="line", x0=x_H, y0=0, x1=x_H, y1=H, line=dict(color="#ef4444", dash="dot", width=1.5))
    fig.add_annotation(x=x_H, y=H*0.5, text="<b>H (최고점)</b>", ax=25, ay=0, showarrow=True, arrowhead=2, arrowcolor="#dc2626", font=dict(size=12, color="#b91c1c"))
    # 수평 도달 거리 R 표시
    fig.add_annotation(x=R*0.5, y=-5, text="<b>R (수평 도달 거리)</b>", showarrow=False, font=dict(size=12, color="#334155"))
    fig.add_shape(type="line", x0=0, y0=-3, x1=R, y1=-3, line=dict(color="#475569", width=1.5))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-20, R+30]), 
        yaxis=dict(visible=False, range=[-10, H+10]), 
        height=220, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white"
    )
    return fig

def get_diagram_prob2():
    """문제 2: A(0m), B(3.2m), C(1.6m) 궤적 도식"""
    # vx0 = 6, vy0 = 8, g = 10 -> t_h = 0.8s, H = 3.2m, t_land = 1.6s, R = 9.6m
    vx = 6.0; vy0 = 8.0; g = 10.0
    t_land = 1.6; R = 9.6
    t = np.linspace(0, t_land, 60)
    x = vx * t; y = vy0 * t - 0.5 * g * t**2

    # A: t=0, x=0, y=0
    # B: t=0.8, x=4.8, y=3.2
    # C: y=1.6 => 8t - 5t^2 = 1.6 => 5t^2 - 8t + 1.6 = 0 => t = (8 + sqrt(64 - 32))/10 = (8 + sqrt(32))/10 = 0.8 + 0.5657 = 1.3657s
    t_C = 0.8 + np.sqrt(32)/10; x_C = vx * t_C; y_C = 1.6

    fig = go.Figure()
    # 지면 및 축
    fig.add_shape(type="line", x0=-1, y0=0, x1=11.5, y1=0, line=dict(color="#1e293b", width=2.5))
    fig.add_shape(type="line", x0=0, y0=0, x1=0, y1=4.0, line=dict(color="#1e293b", width=1.5))
    # 궤적
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#0f172a', dash='dash', width=2), showlegend=False))
    
    # 지점 A
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+text', marker=dict(size=14, color='#2563eb', line=dict(width=2, color='black')), text=["<b>A</b>"], textposition="top left", textfont=dict(size=14, color="#1e3a8a"), showlegend=False))
    fig.add_annotation(x=1.5, y=2.0, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#2563eb", arrowwidth=3)
    fig.add_annotation(x=1.8, y=2.2, text="v₀", showarrow=False, font=dict(size=13, color="#1e40af", weight="bold"))

    # 지점 B
    fig.add_trace(go.Scatter(x=[4.8], y=[3.2], mode='markers+text', marker=dict(size=14, color='#dc2626', line=dict(width=2, color='black')), text=["<b>B</b>"], textposition="top center", textfont=dict(size=14, color="#991b1b"), showlegend=False))
    fig.add_shape(type="line", x0=4.8, y0=0, x1=4.8, y1=3.2, line=dict(color="#ef4444", dash="dash", width=1.5))
    fig.add_shape(type="line", x0=0, y0=3.2, x1=4.8, y1=3.2, line=dict(color="#94a3b8", dash="dot", width=1))
    fig.add_annotation(x=4.8, y=1.6, text="<b>3.2 m</b>", ax=22, ay=0, showarrow=True, arrowhead=2, arrowcolor="#dc2626", font=dict(size=11, color="#b91c1c"))

    # 지점 C
    fig.add_trace(go.Scatter(x=[x_C], y=[y_C], mode='markers+text', marker=dict(size=14, color='#16a34a', line=dict(width=2, color='black')), text=["<b>C</b>"], textposition="top right", textfont=dict(size=14, color="#166534"), showlegend=False))
    fig.add_shape(type="line", x0=x_C, y0=0, x1=x_C, y1=y_C, line=dict(color="#16a34a", dash="dash", width=1.5))
    fig.add_shape(type="line", x0=0, y0=1.6, x1=x_C, y1=1.6, line=dict(color="#94a3b8", dash="dot", width=1))
    fig.add_annotation(x=x_C, y=0.8, text="<b>1.6 m</b>", ax=22, ay=0, showarrow=True, arrowhead=2, arrowcolor="#16a34a", font=dict(size=11, color="#15803d"))

    # 축 라벨
    fig.add_annotation(x=10.5, y=-0.35, text="수평 방향 (m)", showarrow=False, font=dict(size=11, color="#334155"))
    fig.add_annotation(x=-0.5, y=3.8, text="높이 (m)", showarrow=False, font=dict(size=11, color="#334155"))

    fig.update_layout(
        xaxis=dict(visible=True, range=[-1, 11.5], showgrid=False, zeroline=False), 
        yaxis=dict(visible=True, range=[-0.6, 4.2], showgrid=False, zeroline=False), 
        height=220, margin=dict(l=20, r=20, t=20, b=20), plot_bgcolor="white"
    )
    return fig

def get_energy_barchart_prob2(show_answer=True):
    """문제 2: 지점 B와 C의 에너지 막대그래프"""
    fig = go.Figure()
    categories = ['B (최고점, 3.2m)', 'C (하강 중, 1.6m)']
    
    if show_answer:
        fig.add_trace(go.Bar(
            name='운동에너지 (Ek)',
            x=categories,
            y=[18.0, 34.0],
            marker_color='#3b82f6',
            text=['18.0 J', '34.0 J'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='퍼텐셜에너지 (Ep)',
            x=categories,
            y=[32.0, 16.0],
            marker_color='#ef4444',
            text=['32.0 J', '16.0 J'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='역학적에너지 (E_total)',
            x=categories,
            y=[50.0, 50.0],
            marker_color='#10b981',
            text=['50.0 J', '50.0 J'],
            textposition='auto'
        ))
    else:
        fig.add_trace(go.Bar(name='운동에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))
        fig.add_trace(go.Bar(name='퍼텐셜에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))
        fig.add_trace(go.Bar(name='역학적에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))

    fig.update_layout(
        barmode='group',
        yaxis=dict(title='에너지 (J)', range=[0, 55], dtick=10),
        height=260,
        margin=dict(l=10, r=10, t=25, b=10),
        plot_bgcolor='#f8fafc',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

def get_diagram_prob3():
    """문제 3: (가) 30°, v0 vs (나) 60°, 2v0 비교 도식"""
    v0 = 10.0; g = 10.0
    # (가) 30, v0
    vx1 = v0 * np.cos(np.radians(30)); vy1 = v0 * np.sin(np.radians(30))
    t1 = np.linspace(0, 2*vy1/g, 40)
    x1 = vx1 * t1; y1 = vy1 * t1 - 0.5 * g * t1**2

    # (나) 60, 2v0
    vx2 = 2*v0 * np.cos(np.radians(60)); vy2 = 2*v0 * np.sin(np.radians(60))
    t2 = np.linspace(0, 2*vy2/g, 50)
    x2 = vx2 * t2; y2 = vy2 * t2 - 0.5 * g * t2**2

    fig = go.Figure()
    fig.add_shape(type="line", x0=-5, y0=0, x1=max(x1[-1], x2[-1])+10, y1=0, line=dict(color="#1e293b", width=2.5))
    
    # (가)
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines', line=dict(color='#2563eb', width=2.5), name='(가) v₀, 30°'))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='#2563eb'), showlegend=False))
    fig.add_annotation(x=vx1*0.8, y=vy1*0.8, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#2563eb", arrowwidth=2.5)
    fig.add_annotation(x=x1[len(x1)//2], y=max(y1)+1.2, text=f"<b>(가) H₁</b>", showarrow=False, font=dict(color="#1e40af", size=11))

    # (나)
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', line=dict(color='#dc2626', width=2.5, dash='dash'), name='(나) 2v₀, 60°'))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='#dc2626'), showlegend=False))
    fig.add_annotation(x=vx2*0.8, y=vy2*0.8, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#dc2626", arrowwidth=2.5)
    fig.add_annotation(x=x2[len(x2)//2], y=max(y2)+1.2, text=f"<b>(나) H₂ (최고점)</b>", showarrow=False, font=dict(color="#991b1b", size=11))

    fig.update_layout(
        xaxis=dict(visible=False), 
        yaxis=dict(visible=False), 
        height=220, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def get_diagram_prob4():
    """문제 4: 60도, 속력 v, 최고점 및 점 p 마킹 도식"""
    v = 15.0; theta = np.radians(60); g = 10.0
    vx = v * np.cos(theta); vy = v * np.sin(theta)
    t_h = vy / g; t_land = 2 * t_h
    t = np.linspace(0, t_land, 60)
    x = vx * t; y = vy * t - 0.5 * g * t**2

    # 점 p: 하강 중 t = t_h * 1.5 지점
    t_p = t_h * 1.45; x_p = vx * t_p; y_p = vy * t_p - 0.5 * g * t_p**2
    vx_p = vx; vy_p = vy - g * t_p

    fig = go.Figure()
    fig.add_shape(type="line", x0=-3, y0=0, x1=x[-1]+5, y1=0, line=dict(color="#1e293b", width=2.5))
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#475569', dash='dot', width=2), showlegend=False))
    
    # 발사 위치
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='#3b82f6'), showlegend=False))
    fig.add_annotation(x=vx*0.7, y=vy*0.7, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#2563eb", arrowwidth=3)
    fig.add_annotation(x=vx*0.7+2, y=vy*0.7+1, text="<b>v (60°)</b>", showarrow=False, font=dict(size=12, color="#1e40af"))
    
    # 최고점
    x_H = vx * t_h; H = vy**2 / (2*g)
    fig.add_trace(go.Scatter(x=[x_H], y=[H], mode='markers+text', marker=dict(size=10, color='#1e293b'), text=["<b>최고점</b>"], textposition="top center", textfont=dict(size=12, color="#0f172a"), showlegend=False))
    
    # 점 p
    fig.add_trace(go.Scatter(x=[x_p], y=[y_p], mode='markers+text', marker=dict(size=14, color='#2563eb', line=dict(width=2, color='black')), text=["<b>p</b>"], textposition="top right", textfont=dict(size=15, color="#1e3a8a"), showlegend=False))
    # 점 p에서의 속도 화살표
    fig.add_annotation(x=x_p + vx_p*0.5, y=y_p + vy_p*0.5, ax=x_p, ay=y_p, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#1d4ed8", arrowwidth=2.5)

    fig.update_layout(
        xaxis=dict(visible=False), 
        yaxis=dict(visible=False, range=[-2, H+4]), 
        height=200, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white"
    )
    return fig

def get_diagram_prob5():
    """문제 5: 60도, 10m/s 다중 스트로브(점묘) 포물선 도식"""
    v0 = 10.0; theta = np.radians(60); g = 10.0
    vx = v0 * np.cos(theta); vy0 = v0 * np.sin(theta)
    t_h = vy0 / g; H = vy0**2 / (2*g)
    t_land = 2 * t_h; R = vx * t_land

    t_curve = np.linspace(0, t_land, 60)
    x_curve = vx * t_curve; y_curve = vy0 * t_curve - 0.5 * g * t_curve**2

    # 스트로브 위치 (7개 구)
    t_strobe = np.linspace(0, t_land, 7)
    x_strobe = vx * t_strobe; y_strobe = vy0 * t_strobe - 0.5 * g * t_strobe**2

    fig = go.Figure()
    fig.add_shape(type="line", x0=-1.5, y0=0, x1=R+2, y1=0, line=dict(color="#1e293b", width=3))
    fig.add_trace(go.Scatter(x=x_curve, y=y_curve, mode='lines', line=dict(color='#64748b', dash='dash', width=2), showlegend=False))
    
    # 다중 스트로브 볼
    fig.add_trace(go.Scatter(x=x_strobe, y=y_strobe, mode='markers', marker=dict(size=14, color='#f43f5e', line=dict(width=1.5, color='#9f1239')), showlegend=False))
    
    # 발사 벡터
    fig.add_annotation(x=vx*0.7, y=vy0*0.7, ax=0, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#2563eb", arrowwidth=3)
    fig.add_annotation(x=vx*0.7+0.8, y=vy0*0.7+0.3, text="<b>10 m/s<br>(60°)</b>", showarrow=False, font=dict(size=11, color="#1e40af"))

    # 최고점 H 점선 및 화살표
    fig.add_shape(type="line", x0=R/2, y0=0, x1=R/2, y1=H, line=dict(color="#e11d48", dash="dot", width=1.5))
    fig.add_annotation(x=R/2, y=H*0.5, text="<b>H</b>", ax=18, ay=0, showarrow=True, arrowhead=2, arrowcolor="#e11d48", font=dict(size=13, color="#9f1239"))
    
    # 1/2 H 기준선
    fig.add_shape(type="line", x0=0, y0=H/2, x1=R, y1=H/2, line=dict(color="#3b82f6", dash="dot", width=1))
    fig.add_annotation(x=R*0.88, y=H/2 + 0.35, text="<b>1/2 H</b>", showarrow=False, font=dict(size=11, color="#2563eb"))

    # 수평 도달 거리 R
    fig.add_shape(type="line", x0=0, y0=-0.35, x1=R, y1=-0.35, line=dict(color="#334155", width=1.5))
    fig.add_annotation(x=R/2, y=-0.8, text="<b>R</b>", showarrow=False, font=dict(size=13, color="#1e293b"))

    fig.update_layout(
        xaxis=dict(visible=False, range=[-2, R+3]), 
        yaxis=dict(visible=False, range=[-1.2, H+1.0]), 
        height=220, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor="white"
    )
    return fig

# =========================================================================
# 섹션 1: 신규 실전 기출 및 활동지 연계 문항 (5종)
# =========================================================================

if view_category in ["🎯 실전 기출 & 활동지 연계 5문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"]:
    st.header("🎯 실전 기출 & 활동지 연계 심화 문제")
    st.caption("수능/내신 빈출 유형 및 [활동 6] 포물선 운동의 역학적 에너지 보존 탐구 문항입니다.")

    # ---------------------------------------------------------------------
    # [문제 1] 30도 방향 40m/s 포물선 운동 (질량 2kg)
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [문제 1] 비스듬히 던진 물체의 기본 포물선 운동 계산")
    st.markdown("""
    <span class="badge-primary">기출 빈출</span> &nbsp;
    지면에서 질량이 **2 kg**인 물체를 수평면과 **30°**를 이루는 방향으로 **40 m/s**의 속력으로 던진 물체의 운동 경로를 나타낸 것이다. 
    (단, 중력 가속도는 $10\\text{ m/s}^2$이고, 공기 저항은 무시한다.)
    """, unsafe_allow_html=True)
    
    st.plotly_chart(get_diagram_prob1(), use_container_width=True, config={'staticPlot': True})

    if is_print_mode:
        st.markdown("**1) 최고점에 도달할 때까지 걸린 시간(s)을 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2) 최고점의 높이(m)를 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3) 수평 도달 거리(m)를 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            ans1_1 = st.text_input("1) 최고점 도달 시간 (s)", key="p1_1", placeholder="예: 2")
        with c2:
            ans1_2 = st.text_input("2) 최고점 높이 (m)", key="p1_2", placeholder="예: 20")
        with c3:
            ans1_3 = st.text_input("3) 수평 도달 거리 (m)", key="p1_3", placeholder="예: 80루트3 또는 138.6")

        if st.button("결과 및 단계별 풀이 확인", key="btn_p1"):
            st.success("""
            **[정답 및 모범 풀이]**
            - **초기 속도 성분 분해**:
              - 수평 초기 속도: $v_{x0} = 40 \\cos 30^\\circ = 40 \\times \\frac{\\sqrt{3}}{2} = 20\\sqrt{3}\\text{ m/s} \\approx 34.64\\text{ m/s}$
              - 연직 초기 속도: $v_{y0} = 40 \\sin 30^\\circ = 40 \\times \\frac{1}{2} = 20\\text{ m/s}$
            
            1. **최고점 도달 시간**:
               - 최고점에서 연직 속도 $v_y = 0$ 이므로, $v_y = v_{y0} - gt = 20 - 10t = 0 \\implies \\mathbf{t = 2\\text{초}}$
            
            2. **최고점의 높이**:
               - $H = v_{y0}t - \\frac{1}{2}gt^2 = 20(2) - \\frac{1}{2}(10)(2^2) = 40 - 20 = \\mathbf{20\\text{ m}}$
               - (에너지 보존: $\\frac{1}{2}m v_{y0}^2 = mgH \\implies H = \\frac{20^2}{20} = 20\\text{ m}$)
            
            3. **수평 도달 거리**:
               - 전체 체공 시간 $T = 2t = 4\\text{초}$
               - 수평 방향은 등속도 운동이므로, $R = v_{x0} \\times T = 20\\sqrt{3} \\times 4 = \\mathbf{80\\sqrt{3}\\text{ m}} \\approx \\mathbf{138.6\\text{ m}}$
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 2] 활동 6 연계: 포물선 운동 에너지 분석 및 막대그래프
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("⚡ [문제 2 / 활동6 연계] 포물선 운동의 역학적 에너지 보존 & 막대그래프")
    st.markdown("""
    <span class="badge-success">활동지 연계</span> &nbsp;
    질량이 **1 kg**인 공이 운동하는 도중 세 지점 **A, B, C**에서의 높이 및 수평/연직 방향 속력을 나타낸 것이다. 
    *(단, 공기 저항은 무시하고 중력 가속도의 크기는 $10\\text{ m/s}^2$, 지면의 중력 퍼텐셜에너지는 0으로 한다.)*
    """, unsafe_allow_html=True)

    col_p2_diag, col_p2_table = st.columns([1.2, 1])
    with col_p2_diag:
        st.plotly_chart(get_diagram_prob2(), use_container_width=True, config={'staticPlot': True})
    with col_p2_table:
        st.markdown("""
        | 지점 | 높이(m) | 수평 속력(m/s) | 연직 속력(m/s) |
        | :---: | :---: | :---: | :---: |
        | **A** | **0** | **6** | **8** |
        | **B (최고점)** | **3.2** | **6** | **0** |
        | **C (하강 중)** | **1.6** | **6** | **-** |
        """)
        st.caption("💡 힌트: 수평 방향으로는 알짜힘이 없으므로 수평 속력은 6 m/s로 일정하게 유지됩니다.")

    st.markdown("---")

    if is_print_mode:
        st.markdown("**1) A와 B에서 공의 운동에너지, 중력에 의한 퍼텐셜에너지, 역학적 에너지를 각각 구하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

        st.markdown("**2) (1)의 계산 결과를 바탕으로 아래 B(최고점, 3.2m), C(하강 중, 1.6m)의 에너지 막대그래프를 완성하시오.**")
        st.markdown("""
        <div class="bar-chart-container">
            <div class="bar-chart-card">
                <div class="bar-chart-title">B (최고점, 3.2 m)</div>
                <div class="bar-chart-frame">
                    <span class="tick-50">50J</span>
                    <span class="tick-0">0J</span>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                </div>
                <div class="bar-chart-labels">
                    <span>운동E</span>
                    <span>위치E</span>
                    <span>역학적E</span>
                </div>
            </div>
            <div class="bar-chart-card">
                <div class="bar-chart-title">C (하강 중, 1.6 m)</div>
                <div class="bar-chart-frame">
                    <span class="tick-50">50J</span>
                    <span class="tick-0">0J</span>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                </div>
                <div class="bar-chart-labels">
                    <span>운동E</span>
                    <span>위치E</span>
                    <span>역학적E</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**3) 계산 결과를 근거로 하여, A에서 B까지 운동하는 동안 운동에너지와 퍼텐셜에너지가 어떻게 변하는지 서술하고, 역학적 에너지가 일정하게 유지되는 이유를 에너지 전환 관점에서 설명하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

        st.markdown("**4) C에서의 역학적 에너지를 계산 없이 예측하고, 그 근거를 서술하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

    else:
        st.markdown("**1) A와 B에서의 에너지 구하기**")
        c2_1, c2_2 = st.columns(2)
        with c2_1:
            st.text_input("A 지점: 운동E / 위치E / 역학적E (J)", key="p2_ans_A", placeholder="예: 50, 0, 50")
        with c2_2:
            st.text_input("B 지점: 운동E / 위치E / 역학적E (J)", key="p2_ans_B", placeholder="예: 18, 32, 50")

        st.markdown("**2) B와 C 지점의 에너지 막대그래프 완성하기**")
        show_bar_ans = st.checkbox("📊 정답 막대그래프 노출하기", value=False)
        st.plotly_chart(get_energy_barchart_prob2(show_answer=show_bar_ans), use_container_width=True)

        st.markdown("**3) 서술형 질문: 에너지 전환과 역학적 에너지 보존**")
        st.text_area("A에서 B까지 운동하는 동안의 에너지 변화와 역학적 에너지가 보존되는 이유", key="p2_desc1", height=70, placeholder="운동에너지 감소량과 퍼텐셜에너지 증가량의 관계를 에너지 전환 관점에서 서술하세요.")
        
        st.markdown("**4) 서술형 질문: C에서의 역학적 에너지 예측**")
        st.text_input("C에서의 역학적 에너지 및 그 이유", key="p2_desc2", placeholder="예: 50 J, 외력이 없고 보존력(중력)만 작용하므로 역학적 에너지가 보존됨")

        if st.button("결과 및 모범 해설 확인", key="btn_p2"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            1. **A와 B에서의 에너지**:
               - **A 지점 ($h=0\\text{ m}$)**:
                 - 전체 속력 $v_A = \\sqrt{6^2 + 8^2} = 10\\text{ m/s}$
                 - 운동에너지 $E_k = \\frac{1}{2}(1)(10^2) = \\mathbf{50\\text{ J}}$ (수평 18 J + 연직 32 J)
                 - 퍼텐셜에너지 $E_p = mgh = 1 \\times 10 \\times 0 = \\mathbf{0\\text{ J}}$
                 - 역학적 에너지 $E_{total} = E_k + E_p = \\mathbf{50\\text{ J}}$
               - **B 지점 ($h=3.2\\text{ m}$, 최고점)**:
                 - 전체 속력 $v_B = v_x = 6\\text{ m/s}$ ($v_y = 0$)
                 - 운동에너지 $E_k = \\frac{1}{2}(1)(6^2) = \\mathbf{18\\text{ J}}$
                 - 퍼텐셜에너지 $E_p = mgh = 1 \\times 10 \\times 3.2 = \\mathbf{32\\text{ J}}$
                 - 역학적 에너지 $E_{total} = 18 + 32 = \\mathbf{50\\text{ J}}$
            
            2. **에너지 막대그래프 (B, C)**:
               - **B 지점**: 운동E = **18 J**, 위치E = **32 J**, 역학적E = **50 J**
               - **C 지점 ($h=1.6\\text{ m}$)**:
                 - 위치에너지: $E_p = 1 \\times 10 \\times 1.6 = \\mathbf{16\\text{ J}}$
                 - 역학적 에너지가 50 J로 보존되므로, 운동에너지 $E_k = 50 - 16 = \\mathbf{34\\text{ J}}$
                 - 막대그래프: 운동E = **34 J**, 위치E = **16 J**, 역학적E = **50 J**
            
            3. **에너지 전환 서술 모범 답안**:
               - A에서 B로 상승하는 동안 높이가 증가하여 퍼텐셜에너지는 0 J에서 32 J로 **32 J 증가**하고, 연직 속력이 8 m/s에서 0으로 줄어들어 운동에너지는 50 J에서 18 J로 **32 J 감소**한다.
               - 공기 저항이 없을 때 **운동에너지 감소량(32 J)이 그대로 퍼텐셜에너지 증가량(32 J)으로 1:1 전환**되므로, 두 에너지의 합인 역학적 에너지는 **50 J로 일정하게 유지**된다.
            
            4. **C 지점 역학적 에너지 예측**:
               - **답: 50 J**
               - **근거**: 공기 저항과 같은 비보존력이 작용하지 않고 중력(보존력)만 작용하므로, 물체의 운동 경로 상 모든 지점에서 역학적 에너지는 항상 50 J로 일정하게 보존되기 때문이다.
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 3] 두 물체의 포물선 운동 비교 ((가) 30°, v0 vs (나) 60°, 2v0)
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📊 [문제 3] 두 물체의 포물선 운동 비교 ((가) 30°, v₀ vs (나) 60°, 2v₀)")
    st.markdown("""
    <span class="badge-purple">수능 빈출</span> &nbsp;
    그림 (가), (나)는 각각 수평면과 **30°, 60°**의 각을 이루는 방향으로 속력 **$v_0, 2v_0$**으로 던져진 **동일한 물체**가 포물선 운동하는 모습을 나타낸 것이다.
    """, unsafe_allow_html=True)

    st.plotly_chart(get_diagram_prob3(), use_container_width=True, config={'staticPlot': True})

    if is_print_mode:
        st.markdown("**1) 물체를 던진 순간부터 최고점 도달할 때까지 걸린 시간을 비교하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2) 최고점에서 중력에 의한 위치 에너지를 비교하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3) (나)에서 최고점에서 물체의 중력에 의한 위치 에너지는 운동에너지의 몇 배인지 구하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c3_1, c3_2, c3_3 = st.columns(3)
        with c3_1:
            ans3_1 = st.text_input("1) 최고점 도달 시간 비 t(가) : t(나)", key="p3_1", placeholder="예: 1:2루트3 또는 (나)가 2루트3배")
        with c3_2:
            ans3_2 = st.text_input("2) 최고점 위치에너지 비 Ep(가) : Ep(나)", key="p3_2", placeholder="예: 1:12 또는 (나)가 12배")
        with c3_3:
            ans3_3 = st.text_input("3) (나) 최고점 Ep는 Ek의 몇 배?", key="p3_3", placeholder="예: 3배")

        if st.button("결과 및 상세 풀이 확인", key="btn_p3"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            1. **최고점 도달 시간 비교**:
               - 최고점 도달 시간은 연직 초기 속도 성분에 비례합니다 ($t_H = \\frac{v_y}{g}$):
                 - (가): $v_{y1} = v_0 \\sin 30^\\circ = \\frac{1}{2}v_0 \\implies t_1 = \\frac{v_0}{2g}$
                 - (나): $v_{y2} = 2v_0 \\sin 60^\\circ = 2v_0 \\times \\frac{\\sqrt{3}}{2} = \\sqrt{3}v_0 \\implies t_2 = \\frac{\\sqrt{3}v_0}{g}$
               - **비율: $t_{(가)} : t_{(나)} = \\frac{1}{2} : \\sqrt{3} = \\mathbf{1 : 2\\sqrt{3}}$ ((나)가 $2\\sqrt{3} \\approx 3.46$배)**
            
            2. **최고점에서의 위치 에너지 비교**:
               - 최고점 높이 $H = \\frac{v_y^2}{2g}$이므로, $E_p = mgH = \\frac{1}{2}mv_y^2$
                 - (가): $E_{p1} = \\frac{1}{2}m (\\frac{1}{2}v_0)^2 = \\frac{1}{8}mv_0^2$
                 - (나): $E_{p2} = \\frac{1}{2}m (\\sqrt{3}v_0)^2 = \\frac{3}{2}mv_0^2 = \\frac{12}{8}mv_0^2$
               - **비율: $E_{p(가)} : E_{p(나)} = \\frac{1}{8} : \\frac{3}{2} = \\mathbf{1 : 12}$ ((나)가 12배)**
            
            3. **(나)에서 최고점 위치에너지는 운동에너지의 몇 배인가?**:
               - (나) 최고점에서의 속력은 수평 방향 속도만 남으므로:
                 $v_x = 2v_0 \\cos 60^\\circ = 2v_0 \\times \\frac{1}{2} = v_0$
               - 최고점 운동에너지: $E_k = \\frac{1}{2}m v_x^2 = \\frac{1}{2}mv_0^2$
               - 최고점 위치에너지: $E_p = \\frac{3}{2}mv_0^2$
               - **배수: $\\frac{E_p}{E_k} = \\frac{\\frac{3}{2}mv_0^2}{\\frac{1}{2}mv_0^2} = \\mathbf{3\\text{배}}$**
               *(참고 공식: $\\frac{E_p}{E_k} = \\tan^2 \\theta = \\tan^2 60^\\circ = (\\sqrt{3})^2 = 3$배)*
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 4] 에너지 관계를 이용한 점 p에서의 운동에너지 추론
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🔍 [문제 4] 최고점을 지난 임의의 점 p에서의 운동에너지 추론")
    st.markdown("""
    <span class="badge-amber">역학적 에너지 관계 추론</span> &nbsp;
    그림은 수평면과 **60°**의 각을 이루며 속력 **$v$**로 던져진 질량 **$m$**인 물체가 포물선 운동 하여 최고점을 지나 **점 p**를 통과한 모습을 나타낸 것이다. 
    **수평면에서 던져진 순간 물체의 운동 에너지는 물체가 최고점에서 p까지 운동하는 동안 물체의 중력에 의한 위치 에너지 감소량의 2배이다.**
    
    **점 p에서 물체의 운동 에너지는?** *(단, 물체의 크기 및 공기 저항은 무시한다.)*
    """, unsafe_allow_html=True)

    st.plotly_chart(get_diagram_prob4(), use_container_width=True, config={'staticPlot': True})

    if is_print_mode:
        st.markdown("**풀이 과정과 답을 쓰시오.**")
        for _ in range(3): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans4 = st.text_input("점 p에서의 운동에너지 입력 (던진 순간 운동에너지 E₀ 또는 mv²으로 표현)", key="p4_ans", placeholder="예: 3/4 E0 또는 3/8 mv^2")
        if st.button("정답 및 풀이 과정 확인", key="btn_p4"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            - **정답**: $\\mathbf{\\frac{3}{4} E_{k0}}$ (또는 $\\mathbf{\\frac{3}{8} mv^2}$)
            
            - **단계별 풀이 과정**:
              1. **던진 순간(지면)의 초기 운동에너지**:
                 $E_{k0} = \\frac{1}{2}mv^2$
              
              2. **최고점에서의 운동에너지**:
                 - 최고점에서는 연직 속도 $v_y = 0$이고 수평 속도 $v_x = v \\cos 60^\\circ = \\frac{1}{2}v$ 만 존재합니다.
                 - $E_{k,top} = \\frac{1}{2}m v_x^2 = \\frac{1}{2}m \\left(\\frac{1}{2}v\\right)^2 = \\frac{1}{8}mv^2 = \\mathbf{\\frac{1}{4} E_{k0}}$
              
              3. **문제 조건 해석**:
                 - "던져진 순간 운동에너지($E_{k0}$)는 최고점에서 p까지의 위치에너지 감소량($\\Delta E_p$)의 2배이다."
                 - $E_{k0} = 2 \\times \\Delta E_p \\implies \\mathbf{\\Delta E_p = \\frac{1}{2} E_{k0}}$
              
              4. **역학적 에너지 보존에 의한 점 p의 운동에너지 계산**:
                 - 최고점에서 p까지 낙하하면서 감소한 위치에너지는 고스란히 운동에너지 증가량($\\Delta E_k$)이 됩니다:
                   $\\Delta E_k = \\Delta E_p = \\frac{1}{2} E_{k0}$
                 - 따라서 점 p에서의 운동에너지 $E_k(p)$는 최고점 운동에너지에 증가량을 더한 값입니다:
                   $$E_k(p) = E_{k,top} + \\Delta E_k = \\frac{1}{4} E_{k0} + \\frac{1}{2} E_{k0} = \\mathbf{\\frac{3}{4} E_{k0}} = \\mathbf{\\frac{3}{8} mv^2}$$
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 5] 60도, 10m/s 포물선 운동의 7단계 종합 분석
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🌟 [문제 5] 60°, 10 m/s 포물선 운동과 1/2 H 지점의 7단계 종합 탐구")
    st.markdown("""
    <span class="badge-primary">종합 탐구</span> &nbsp;
    그림은 수평면과 **60°**의 각으로 속력 **10 m/s**로 던져진 물체가 운동하는 모습을 나타낸 것이다. 
    *(단, 중력 가속도는 $10\\text{ m/s}^2$이고, 물체의 질량은 $m$이라 하자. 수치 계산 시 $m=1\\text{ kg}$ 기준으로 계산할 수 있다. 물체의 크기 및 공기 저항은 무시한다.)*
    """, unsafe_allow_html=True)

    st.plotly_chart(get_diagram_prob5(), use_container_width=True, config={'staticPlot': True})

    if is_print_mode:
        q_list_p5 = [
            "(1) 속력 10 m/s로 비스듬히 던져진 물체가 최고점에 도달할 때까지 걸린 시간은?",
            "(2) 최고점의 높이는?",
            "(3) 수평도달 거리는?",
            "(4) 물체를 던진 순간의 역학적 에너지는?",
            "(5) 최고점에서 운동에너지는?",
            "(6) 1/2 H 지점에서의 운동에너지와 위치에너지를 각각 구하시오.",
            "(7) 1/2 H 지점에서의 속도의 크기를 구하시오."
        ]
        for q in q_list_p5:
            st.markdown(f"**{q}**")
            st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        col_5a, col_5b = st.columns(2)
        with col_5a:
            ans5_1 = st.text_input("(1) 최고점 도달 시간 (s)", key="p5_1", placeholder="예: 루트3/2 또는 0.87")
            ans5_2 = st.text_input("(2) 최고점 높이 (m)", key="p5_2", placeholder="예: 3.75")
            ans5_3 = st.text_input("(3) 수평도달 거리 (m)", key="p5_3", placeholder="예: 5루트3 또는 8.66")
            ans5_4 = st.text_input("(4) 던진 순간 역학적에너지 (J, m=1kg)", key="p5_4", placeholder="예: 50")
        with col_5b:
            ans5_5 = st.text_input("(5) 최고점에서 운동에너지 (J, m=1kg)", key="p5_5", placeholder="예: 12.5")
            ans5_6 = st.text_input("(6) 1/2 H 지점의 운동E / 위치E (J, m=1kg)", key="p5_6", placeholder="예: 31.25 / 18.75")
            ans5_7 = st.text_input("(7) 1/2 H 지점에서의 속력 (m/s)", key="p5_7", placeholder="예: 루트62.5 또는 7.91")

        if st.button("전체 7문항 모범 해설 확인", key="btn_p5"):
            st.success("""
            **[7단계 상세 정답 및 해설]**
            - **초기 속도 성분**:
              - $v_{x} = 10 \\cos 60^\\circ = 5\\text{ m/s}$
              - $v_{y0} = 10 \\sin 60^\\circ = 5\\sqrt{3}\\text{ m/s} \\approx 8.66\\text{ m/s}$
            
            1. **최고점 도달 시간**:
               - $t_H = \\frac{v_{y0}}{g} = \\frac{5\\sqrt{3}}{10} = \\mathbf{\\frac{\\sqrt{3}}{2}\\text{초}} \\approx \\mathbf{0.87\\text{초}}$
            
            2. **최고점의 높이 ($H$)**:
               - $H = \\frac{v_{y0}^2}{2g} = \\frac{(5\\sqrt{3})^2}{20} = \\frac{75}{20} = \\mathbf{3.75\\text{ m}}$ (또는 $\\frac{15}{4}\\text{ m}$)
            
            3. **수평도달 거리 ($R$)**:
               - $R = v_x \\times (2t_H) = 5 \\times \\sqrt{3} = \\mathbf{5\\sqrt{3}\\text{ m}} \\approx \\mathbf{8.66\\text{ m}}$
            
            4. **던진 순간의 역학적 에너지**:
               - 지면에서 $E_p = 0$이므로, $E_{total} = \\frac{1}{2}mv_0^2 = \\frac{1}{2}m(10^2) = \\mathbf{50m\\text{ J}}$ ($m=1\\text{kg}$일 때 **50 J**)
            
            5. **최고점에서 운동에너지**:
               - 최고점에서는 수평 속도($v_x = 5\\text{ m/s}$)만 존재하므로:
                 $E_k(top) = \\frac{1}{2}mv_x^2 = \\frac{1}{2}m(5^2) = \\mathbf{12.5m\\text{ J}}$ ($m=1\\text{kg}$일 때 **12.5 J**)
            
            6. **1/2 H 지점에서의 운동에너지와 위치에너지**:
               - 높이 $h = \\frac{1}{2}H = \\frac{3.75}{2} = 1.875\\text{ m}$
               - 위치에너지: $E_p = mgh = mg(\\frac{1}{2}H) = \\frac{1}{2}E_p(top) = \\mathbf{18.75m\\text{ J}}$ ($m=1\\text{kg}$일 때 **18.75 J**)
               - 운동에너지: 역학적 에너지 보존에 의해
                 $E_k = E_{total} - E_p = 50m - 18.75m = \\mathbf{31.25m\\text{ J}}$ ($m=1\\text{kg}$일 때 **31.25 J**)
            
            7. **1/2 H 지점에서의 속도의 크기**:
               - $E_k = \\frac{1}{2}mv^2 = 31.25m \\implies v^2 = 62.5$
               - $\\mathbf{v = \\sqrt{62.5}\\text{ m/s} = \\frac{5\\sqrt{10}}{2}\\text{ m/s}} \\approx \\mathbf{7.91\\text{ m/s}}$
               - *(성분 검산: $v_x = 5$, $v_y^2 = v_{y0}^2 - 2g(H/2) = 75 - 37.5 = 37.5 \\implies v = \\sqrt{25 + 37.5} = \\sqrt{62.5}\\text{ m/s}$)*
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 섹션 2: 기초 개념 확인 문제 (4종)
# =========================================================================

if view_category in ["🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"]:
    st.header("🌱 포물선 운동 기초 개념 확인 문제")
    st.caption("운동의 독립성, 수평/연직 속도 성분 분해 및 등가속도 운동 공식의 기본 적용 문항입니다.")

    # --- [서술형 1] 운동의 독립성 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🖋️ [기초 1] 운동의 독립성 이해 (자유낙하 vs 수평투사)")
    st.plotly_chart(get_diagram_independence(), use_container_width=True, config={'staticPlot': True})
    st.markdown("동일한 높이에서 공 A(자유낙하)와 공 B(수평투사)를 동시에 발사했습니다. **왜 동시에 지면에 도달하는지 설명하시오.**")

    if is_print_mode:
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("🔍 모범 답안 보기"):
            st.info("수평과 연직 방향의 운동은 서로 **독립적**이며, 연직 방향으로는 공의 종류나 수평 속력과 무관하게 오직 동일한 **중력**만 작용하여 연직 가속도가 $g$로 같기 때문입니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 2] 10m/s, 30도 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [기초 2] 비스듬히 던진 물체의 정밀 분석 (10m/s, 30°)")
    st.plotly_chart(get_diagram_q3(), use_container_width=True, config={'staticPlot': True})
    st.markdown("처음 속도 **10m/s**, 각도 **30도**로 던졌습니다. ($g=10m/s^2$) 아래 질문에 답하세요.")

    if is_print_mode:
        st.markdown("1) 최고점 도달 시간(s)은? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
        st.markdown("2) 최고점의 높이(m)는? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c_k1, c_k2 = st.columns(2)
        with c_k1:
            ans3_t = st.text_input("1) 최고점 도달 시간(s)", key="q3_1", placeholder="예: 0.5")
        with c_k2:
            ans3_h = st.text_input("2) 최고점의 높이(m)", key="q3_2", placeholder="예: 1.25")
        if st.button("정답 확인", key="b3"):
            st.success(f"**[정답 및 풀이]**\n- 시간: $v_{{y0}}/g = (10 \\sin 30^\\circ)/10 = 0.5$초\n- 높이: $v_{{y0}}^2/2g = 5^2/20 = 1.25$m")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 3] 수평 속도의 역추적 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [기초 3] 수평 속도의 역추적")
    st.markdown("""
    물체를 비스듬히 던져 올렸더니 **4초 후** 수평으로 **39.2m** 떨어진 곳에 도달했습니다. 
    처음 발사 속도의 **수평 방향 성분**은 몇 m/s인가요? ($g=9.8m/s^2$)
    """)

    if is_print_mode:
        st.markdown("정답 및 풀이 과정:")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans4 = st.text_input("수평 속도(m/s) 입력", key="q4", placeholder="예: 9.8")
        if st.button("정답 확인", key="b4"):
            st.success("**[정답] 9.8 m/s** (수평 방향은 등속도 운동이므로 $v_x = x/t = 39.2/4 = 9.8$ m/s)")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 4] 최고점 시간 추론 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🔥 [기초 4] 연직 변위를 통한 최고점 도달 시간 추론")
    st.plotly_chart(get_diagram_q5(), use_container_width=True, config={'staticPlot': True})
    st.markdown("""
    비스듬히 던진 야구공이 **0초부터 1초까지** 연직 방향으로 이동한 거리(변위)가 **25m**입니다. 
    이 공이 **최고점에 도달할 때까지** 걸리는 시간은 약 몇 초인가요? ($g=9.8m/s^2$)
    """)

    if is_print_mode:
        st.markdown("정답 및 풀이 과정:")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans5 = st.text_input("최고점 시간(초) 입력", key="q5", placeholder="예: 3.05")
        if st.button("정답 확인", key="b5"):
            st.success("""
            **[정답 및 풀이] 약 3.05초**
            1. $y = v_{y0}t - 1/2gt^2$ 공식에 대입: $25 = v_{y0}(1) - 4.9(1)^2$
            2. 연직 초기 속도 $v_{y0} = 29.9$ m/s 도출
            3. 최고점 시간 $t_H = v_{y0}/g = 29.9 / 9.8 \\approx 3.05$초
            """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.info("💡 모든 도표는 벡터로 직접 정밀 렌더링되었습니다. 상단의 **'🖨️ 학습지 출력 모드'**를 켜면 인쇄 및 학생용 배포 PDF 저장이 가능합니다.")
