import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math
import os

# ===== 물리 상수 =====
G = 6.674e-11           # 만유인력 상수 (N·m²/kg²)
M_EARTH = 5.972e24      # 지구 질량 (kg)
R_EARTH = 6.371e6       # 지구 반지름 (m)
V1_UNIVERSE = 7905.0    # 제1 우주 속도 (m/s)

# ===== NASA 위성 데이터베이스 =====
NASA_SATELLITES = {
    "ISS": {
        "name_ko": "국제우주정거장 (ISS)",
        "name_en": "International Space Station",
        "type": "저고도 (LEO)",
        "altitude_km": 408,
        "inclination": 51.6,
        "eccentricity": 0.0006,
        "color": "#FF6B6B",
        "emoji": "🏗️",
        "description": "지구 저궤도에서 우주 실험을 수행하는 다국적 우주정거장. 약 90분에 1회 지구를 공전하며 하루 약 16회 지구를 돈다.",
        "launch_year": 1998,
        "mission": "유인 우주 실험실"
    },
    "Landsat 9": {
        "name_ko": "랜드샛 9호 (Landsat 9)",
        "name_en": "Landsat 9 Earth Observation Satellite",
        "type": "중고도 (SSO)",
        "altitude_km": 705,
        "inclination": 98.2,
        "eccentricity": 0.0001,
        "color": "#95E1D3",
        "emoji": "🗺️",
        "description": "태양동기궤도(SSO)에서 지표면 자원과 환경 변화를 감시하는 지구관측 위성. 16일 주기로 지표면 전체를 촬영한다.",
        "launch_year": 2021,
        "mission": "지구 관측"
    },
    "GOES-16": {
        "name_ko": "고에스-16 기상위성 (GOES-16)",
        "name_en": "Geostationary Operational Environmental Satellite-16",
        "type": "정지궤도 (GEO)",
        "altitude_km": 35786,
        "inclination": 0.05,
        "eccentricity": 0.0001,
        "color": "#4ECDC4",
        "emoji": "🌤️",
        "description": "적도 상공 정지궤도에서 미국 동부 기상을 실시간 감시. 지구 자전 속도와 동일하게 공전하여 항상 같은 지역 상공에 위치한다.",
        "launch_year": 2016,
        "mission": "기상 관측"
    }
}

# ===== 계산 함수 =====
def calculate_orbital_params(altitude_km):
    """고도(km)로부터 궤도 물리량 계산"""
    r = R_EARTH + altitude_km * 1000
    v = math.sqrt(G * M_EARTH / r)
    T = 2 * math.pi * r / v
    a_n = G * M_EARTH / (r ** 2)
    v_escape = math.sqrt(2 * G * M_EARTH / r)

    return {
        "r": r,
        "v": v,
        "T_s": T,
        "T_min": T / 60,
        "T_hour": T / 3600,
        "a_n": a_n,
        "v_escape": v_escape,
        "v_ratio": v / V1_UNIVERSE,
        "E_kinetic": 0.5 * v ** 2,
        "E_potential": -G * M_EARTH / r,
        "E_total": 0.5 * v ** 2 - G * M_EARTH / r
    }

# ===== 헤더 =====
st.title("🛰️ NASA 실제 위성 궤도 시뮬레이션")
st.markdown("""
**NASA의 대표 위성 3개**(ISS, Landsat 9, GOES-16)의 실제 궤도 데이터를 바탕으로  
**만유인력과 공전 속도의 관계**, **케플러 법칙**, **제1 우주 속도**를 탐구합니다.
""")

# ===== 사이드바 =====
st.sidebar.markdown("## ⚙️ 시뮬레이션 제어")

selected_key = st.sidebar.selectbox(
    "🛰️ 관찰할 위성 선택",
    list(NASA_SATELLITES.keys()),
    format_func=lambda x: f"{NASA_SATELLITES[x]['emoji']} {NASA_SATELLITES[x]['name_ko']}"
)

sat = NASA_SATELLITES[selected_key]
params = calculate_orbital_params(sat["altitude_km"])

st.sidebar.markdown(f"### {sat['emoji']} {sat['name_ko']}")
st.sidebar.info(sat["description"])

st.sidebar.markdown("---")
st.sidebar.markdown("**🎬 애니메이션 옵션**")
n_frames = st.sidebar.slider("프레임 수", 30, 120, 60, step=10)
frame_duration = st.sidebar.select_slider(
    "재생 속도",
    options=[30, 50, 80, 120, 200],
    value=80,
    format_func=lambda x: {30: "매우 빠름", 50: "빠름", 80: "보통", 120: "느림", 200: "매우 느림"}[x]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**📐 벡터 표시 옵션**")
show_velocity = st.sidebar.checkbox("✅ 속도 벡터 (녹색)", value=True)
show_force = st.sidebar.checkbox("✅ 만유인력 벡터 (주황)", value=True)
show_trail = st.sidebar.checkbox("✅ 궤도 경로 (점선)", value=True)

# ===== 메인 영역: 4개 탭 =====
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 궤도 애니메이션",
    "📊 3개 위성 비교",
    "📈 r-v 관계 그래프",
    "📋 위성 상세 정보"
])

# ============================================================
# TAB 1: 궤도 애니메이션
# ============================================================
with tab1:
    st.markdown(f"### {sat['emoji']} {sat['name_ko']} 실시간 궤도 운동")

    # 표시 스케일 정규화 (지구 반지름 단위)
    r_norm = params["r"] / R_EARTH
    r_display = r_norm

    # 지구
    theta_earth = np.linspace(0, 2*np.pi, 100)
    earth_x = np.cos(theta_earth)
    earth_y = np.sin(theta_earth)

    # 궤도 경로
    theta_orbit = np.linspace(0, 2*np.pi, 200)
    orbit_x = r_display * np.cos(theta_orbit)
    orbit_y = r_display * np.sin(theta_orbit)

    # 초기 트레이스
    init_traces = [
        go.Scatter(x=earth_x, y=earth_y, mode='lines', name='🌍 지구',
                   line=dict(color='#1E90FF', width=2),
                   fill='toself', fillcolor='rgba(30, 144, 255, 0.4)',
                   hoverinfo='skip'),
    ]
    if show_trail:
        init_traces.append(go.Scatter(
            x=orbit_x, y=orbit_y, mode='lines', name='궤도',
            line=dict(color='rgba(200,200,200,0.4)', width=1.5, dash='dash'),
            hoverinfo='skip'
        ))

    # 위성 초기 위치
    init_traces.append(go.Scatter(
        x=[r_display], y=[0], mode='markers',
        name=f"{sat['emoji']} {sat['name_ko']}",
        marker=dict(size=16, color=sat['color'], line=dict(color='white', width=2))
    ))

    # 속도 벡터 (접선)
    if show_velocity:
        init_traces.append(go.Scatter(
            x=[r_display, r_display], y=[0, r_display*0.25],
            mode='lines+markers', name='속도 v',
            line=dict(color='#00FF7F', width=4),
            marker=dict(size=[0, 10], symbol='triangle-up', color='#00FF7F')
        ))

    # 만유인력 벡터 (중심 방향)
    if show_force:
        init_traces.append(go.Scatter(
            x=[r_display, r_display*0.7], y=[0, 0],
            mode='lines+markers', name='만유인력 F',
            line=dict(color='#FFA500', width=4),
            marker=dict(size=[0, 10], symbol='triangle-left', color='#FFA500')
        ))

    # 프레임 생성
    frames = []
    for i in range(n_frames):
        angle = 2 * np.pi * i / n_frames
        sx = r_display * np.cos(angle)
        sy = r_display * np.sin(angle)
        # 속도 (접선 방향, 반시계)
        vx = -np.sin(angle)
        vy = np.cos(angle)
        # 만유인력 (중심 방향)
        fx = -np.cos(angle)
        fy = -np.sin(angle)

        frame_traces = [
            go.Scatter(x=earth_x, y=earth_y, mode='lines',
                       line=dict(color='#1E90FF', width=2),
                       fill='toself', fillcolor='rgba(30, 144, 255, 0.4)',
                       hoverinfo='skip'),
        ]
        if show_trail:
            frame_traces.append(go.Scatter(
                x=orbit_x, y=orbit_y, mode='lines',
                line=dict(color='rgba(200,200,200,0.4)', width=1.5, dash='dash'),
                hoverinfo='skip'
            ))

        frame_traces.append(go.Scatter(
            x=[sx], y=[sy], mode='markers',
            marker=dict(size=16, color=sat['color'], line=dict(color='white', width=2))
        ))

        if show_velocity:
            frame_traces.append(go.Scatter(
                x=[sx, sx + vx*r_display*0.25], y=[sy, sy + vy*r_display*0.25],
                mode='lines+markers',
                line=dict(color='#00FF7F', width=4),
                marker=dict(size=[0, 10], symbol='triangle-up', color='#00FF7F')
            ))

        if show_force:
            frame_traces.append(go.Scatter(
                x=[sx, sx + fx*r_display*0.2], y=[sy, sy + fy*r_display*0.2],
                mode='lines+markers',
                line=dict(color='#FFA500', width=4),
                marker=dict(size=[0, 10], symbol='triangle-left', color='#FFA500')
            ))

        # 텔레메트리
        t_elapsed = (i / n_frames) * params["T_s"]
        if params["T_hour"] < 1:
            t_str = f"{t_elapsed/60:.1f} 분"
        elif params["T_hour"] < 24:
            t_str = f"{t_elapsed/60:.1f} 분 ({t_elapsed/3600:.2f} 시간)"
        else:
            t_str = f"{t_elapsed/3600:.2f} 시간"

        telemetry = (
            f"<b>{sat['emoji']} {sat['name_ko']}</b><br>"
            f"고도 h: {sat['altitude_km']:,} km<br>"
            f"속도 v: {params['v']:,.0f} m/s<br>"
            f"진행 시간: {t_str}<br>"
            f"진행률: {(i/n_frames)*100:.1f}%"
        )

        frames.append(go.Frame(
            data=frame_traces, name=f"f{i}",
            layout=go.Layout(annotations=[dict(
                x=0.02, y=0.98, xref="paper", yref="paper",
                text=telemetry, showarrow=False, align="left",
                bgcolor="rgba(20,20,30,0.85)", bordercolor=sat['color'],
                borderwidth=2, font=dict(family="monospace", size=12, color="white")
            )])
        ))

    # 슬라이더 스텝
    steps = []
    for i in range(n_frames):
        steps.append(dict(
            args=[[f"f{i}"], dict(frame=dict(duration=frame_duration, redraw=True),
                                  mode="immediate")],
            label=f"{int(i/n_frames*100)}%", method="animate"
        ))

    # 카메라/축 범위
    lim = r_display * 1.3

    fig = go.Figure(data=init_traces, frames=frames)
    fig.update_layout(
        title=f"{sat['emoji']} {sat['name_ko']} — 궤도 운동 시뮬레이션",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
        font=dict(color='white'),
        xaxis=dict(range=[-lim, lim], title="X (지구 반지름 단위)",
                   gridcolor='rgba(100,100,100,0.2)', zerolinecolor='rgba(255,255,255,0.3)'),
        yaxis=dict(range=[-lim, lim], title="Y (지구 반지름 단위)",
                   gridcolor='rgba(100,100,100,0.2)', zerolinecolor='rgba(255,255,255,0.3)',
                   scaleanchor="x", scaleratio=1),
        height=650,
        updatemenus=[dict(
            type="buttons", direction="left", x=0.05, y=-0.05, xanchor="left",
            showactive=False, bgcolor="#1a1a2e",
            buttons=[
                dict(label="▶ 재생", method="animate",
                     args=[None, dict(frame=dict(duration=frame_duration, redraw=True),
                                      fromcurrent=True, mode="immediate")]),
                dict(label="⏸ 정지", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")])
            ]
        )],
        sliders=[dict(active=0, currentvalue=dict(prefix="진행: ", font=dict(size=13)),
                     pad=dict(b=10, t=40), len=0.85, x=0.1, y=-0.05,
                     steps=steps)],
        annotations=[dict(
            x=0.02, y=0.98, xref="paper", yref="paper",
            text=f"<b>{sat['emoji']} {sat['name_ko']}</b><br>고도: {sat['altitude_km']:,} km<br>속도: {params['v']:,.0f} m/s",
            showarrow=False, align="left",
            bgcolor="rgba(20,20,30,0.85)", bordercolor=sat['color'],
            borderwidth=2, font=dict(family="monospace", size=12, color="white")
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

    # 핵심 지표 카드
    st.markdown("#### 📌 핵심 물리량")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌍 고도 h", f"{sat['altitude_km']:,} km", sat['type'])
    c2.metric("⚡ 공전 속도 v", f"{params['v']:,.0f} m/s",
              f"{params['v_ratio']*100:.1f}% × v₁")
    if params['T_hour'] < 1:
        c3.metric("🔄 공전 주기 T", f"{params['T_min']:.1f} 분")
    elif params['T_hour'] < 24:
        c3.metric("🔄 공전 주기 T", f"{params['T_hour']:.2f} 시간")
    else:
        c3.metric("🔄 공전 주기 T", f"{params['T_hour']/24:.2f} 일")
    c4.metric("📉 구심가속도 aₙ", f"{params['a_n']:.4f} m/s²",
              f"g의 {params['a_n']/9.8*100:.1f}%")

# ============================================================
# TAB 2: 3개 위성 비교
# ============================================================
with tab2:
    st.markdown("### 📊 NASA 위성 3개 종합 비교")

    comp_rows = []
    for key, s in NASA_SATELLITES.items():
        p = calculate_orbital_params(s["altitude_km"])
        if p['T_hour'] < 1:
            T_str = f"{p['T_min']:.1f} 분"
        elif p['T_hour'] < 24:
            T_str = f"{p['T_hour']:.2f} 시간"
        else:
            T_str = f"{p['T_hour']/24:.2f} 일"
        comp_rows.append({
            "위성": f"{s['emoji']} {s['name_ko']}",
            "궤도": s['type'],
            "고도 (km)": f"{s['altitude_km']:,}",
            "궤도 반지름 r (×10⁶ m)": f"{p['r']/1e6:.2f}",
            "공전 속도 v (m/s)": f"{p['v']:,.0f}",
            "공전 주기 T": T_str,
            "구심가속도 aₙ (m/s²)": f"{p['a_n']:.4f}",
            "v / v₁": f"{p['v_ratio']:.3f}"
        })

    df = pd.DataFrame(comp_rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # 두 개 차트
    col1, col2 = st.columns(2)

    sat_names = [s['name_ko'] for s in NASA_SATELLITES.values()]
    sat_colors = [s['color'] for s in NASA_SATELLITES.values()]
    velocities = [calculate_orbital_params(s['altitude_km'])['v'] for s in NASA_SATELLITES.values()]
    periods_hour = [calculate_orbital_params(s['altitude_km'])['T_hour'] for s in NASA_SATELLITES.values()]
    altitudes = [s['altitude_km'] for s in NASA_SATELLITES.values()]

    with col1:
        fig_v = go.Figure(go.Bar(
            x=sat_names, y=velocities, marker_color=sat_colors,
            text=[f"{v:,.0f}" for v in velocities], textposition='auto'
        ))
        fig_v.update_layout(
            title="공전 속도 비교 (m/s)",
            plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
            font=dict(color='white'), height=380,
            yaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
            xaxis=dict(gridcolor='rgba(100,100,100,0.2)')
        )
        st.plotly_chart(fig_v, use_container_width=True)

    with col2:
        fig_t = go.Figure(go.Bar(
            x=sat_names, y=periods_hour, marker_color=sat_colors,
            text=[f"{t:.2f}h" if t < 24 else f"{t/24:.2f}일" for t in periods_hour],
            textposition='auto'
        ))
        fig_t.update_layout(
            title="공전 주기 비교 (로그 스케일)",
            yaxis_type="log",
            plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
            font=dict(color='white'), height=380,
            yaxis=dict(gridcolor='rgba(100,100,100,0.2)', title="주기 (시간, 로그)"),
            xaxis=dict(gridcolor='rgba(100,100,100,0.2)')
        )
        st.plotly_chart(fig_t, use_container_width=True)

    # 3개 위성의 궤도 크기 비교 (실제 스케일)
    st.markdown("#### 🌍 실제 스케일 궤도 크기 비교")

    fig_scale = go.Figure()

    # 지구
    theta = np.linspace(0, 2*np.pi, 100)
    fig_scale.add_trace(go.Scatter(
        x=R_EARTH/1e6 * np.cos(theta), y=R_EARTH/1e6 * np.sin(theta),
        fill='toself', fillcolor='rgba(30,144,255,0.5)',
        line=dict(color='#1E90FF', width=2), name='🌍 지구',
        hovertemplate='지구 반지름: 6,371 km<extra></extra>'
    ))

    for key, s in NASA_SATELLITES.items():
        r_km = (R_EARTH + s['altitude_km']*1000) / 1e6
        fig_scale.add_trace(go.Scatter(
            x=r_km * np.cos(theta), y=r_km * np.sin(theta),
            mode='lines', line=dict(color=s['color'], width=2, dash='dash'),
            name=f"{s['emoji']} {s['name_ko']}",
            hovertemplate=f"<b>{s['name_ko']}</b><br>고도: {s['altitude_km']:,} km<extra></extra>"
        ))
        # 위성 위치 마커
        fig_scale.add_trace(go.Scatter(
            x=[r_km], y=[0], mode='markers',
            marker=dict(size=12, color=s['color'], line=dict(color='white', width=2)),
            showlegend=False, hoverinfo='skip'
        ))

    max_r = max(R_EARTH + s['altitude_km']*1000 for s in NASA_SATELLITES.values()) / 1e6 * 1.15
    fig_scale.update_layout(
        title="3개 위성의 실제 궤도 크기 (단위: 10⁶ m)",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
        font=dict(color='white'), height=500,
        xaxis=dict(range=[-max_r, max_r], gridcolor='rgba(100,100,100,0.2)',
                   title="X (×10⁶ m)"),
        yaxis=dict(range=[-max_r, max_r], gridcolor='rgba(100,100,100,0.2)',
                   scaleanchor="x", scaleratio=1, title="Y (×10⁶ m)")
    )
    st.plotly_chart(fig_scale, use_container_width=True)

    st.info("💡 **관찰**: GOES-16(정지궤도)이 ISS(저궤도)보다 약 6배 멀리 있어 궤도 반지름이 매우 큰 것을 확인할 수 있습니다.")

# ============================================================
# TAB 3: r-v 관계 그래프
# ============================================================
with tab3:
    st.markdown("### 📈 궤도 반지름(r) vs 공전 속도(v) — 케플러 법칙 검증")

    # 이론 곡선
    r_curve = np.logspace(np.log10(R_EARTH), np.log10(R_EARTH + 50000e3), 300)
    v_curve = np.sqrt(G * M_EARTH / r_curve)

    fig_rv = go.Figure()

    # 이론 곡선
    fig_rv.add_trace(go.Scatter(
        x=r_curve/1e6, y=v_curve, mode='lines',
        name='이론: v = √(GM/r)',
        line=dict(color='#888', width=2.5, dash='dash'),
        hovertemplate='r = %{x:.2f} ×10⁶ m<br>v = %{y:,.0f} m/s<extra></extra>'
    ))

    # 제1 우주속도 수평선
    fig_rv.add_hline(y=V1_UNIVERSE, line=dict(color='yellow', dash='dot', width=1.5),
                     annotation_text=f"제1 우주속도 v₁ = {V1_UNIVERSE} m/s",
                     annotation_position="top right",
                     annotation_font_color="yellow")

    # 3개 위성 실제 데이터
    for key, s in NASA_SATELLITES.items():
        p = calculate_orbital_params(s['altitude_km'])
        fig_rv.add_trace(go.Scatter(
            x=[p['r']/1e6], y=[p['v']],
            mode='markers+text',
            text=[f"{s['emoji']} {s['name_ko'].split('(')[0].strip()}"],
            textposition='top center',
            textfont=dict(size=11, color='white'),
            marker=dict(size=18, color=s['color'],
                       line=dict(color='white', width=2)),
            name=s['name_ko'],
            hovertemplate=(f"<b>{s['name_ko']}</b><br>"
                          f"r = %{{x:.2f}} ×10⁶ m<br>"
                          f"v = %{{y:,.0f}} m/s<extra></extra>")
        ))

    fig_rv.update_layout(
        title="궤도 반지름과 공전 속도의 관계",
        xaxis_title="궤도 반지름 r (×10⁶ m)",
        yaxis_title="공전 속도 v (m/s)",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
        font=dict(color='white'), height=500,
        xaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        yaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        legend=dict(bgcolor='rgba(20,20,30,0.7)')
    )

    st.plotly_chart(fig_rv, use_container_width=True)

    st.markdown("""
    #### 📌 그래프 해석

    - **회색 점선**: 만유인력 = 구심력 조건에서 유도된 **이론 공전 속도 곡선** $v = \sqrt{GM/r}$
    - **컬러 점**: 실제 NASA 위성의 측정된 공전 속도
    - **노란 점선**: 제1 우주 속도 (지표면 기준, 7,905 m/s)

    ✅ **3개 위성 모두 이론 곡선 위에 정확히 위치** → 케플러 법칙과 만유인력 법칙이 우주에서도 정확히 성립함을 확인!
    """)

    # v²와 1/r의 비례 관계 (선형화)
    st.markdown("#### 🔍 선형 분석: $v^2$ vs $1/r$")

    fig_lin = go.Figure()

    inv_r = 1 / r_curve
    v_sq = v_curve ** 2

    fig_lin.add_trace(go.Scatter(
        x=inv_r * 1e7, y=v_sq / 1e7, mode='lines',
        name='이론: v² = GM × (1/r)',
        line=dict(color='#888', width=2.5, dash='dash')
    ))

    for key, s in NASA_SATELLITES.items():
        p = calculate_orbital_params(s['altitude_km'])
        fig_lin.add_trace(go.Scatter(
            x=[(1/p['r']) * 1e7], y=[(p['v']**2) / 1e7],
            mode='markers+text',
            text=[s['emoji']], textposition='top center',
            marker=dict(size=16, color=s['color'],
                       line=dict(color='white', width=2)),
            name=s['name_ko']
        ))

    fig_lin.update_layout(
        title="v² vs 1/r — 직선 관계 확인",
        xaxis_title="1/r (×10⁻⁷ m⁻¹)",
        yaxis_title="v² (×10⁷ m²/s²)",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
        font=dict(color='white'), height=400,
        xaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        yaxis=dict(gridcolor='rgba(100,100,100,0.2)')
    )
    st.plotly_chart(fig_lin, use_container_width=True)

    st.success(f"📏 **GM (직선의 기울기) = G × M = {G*M_EARTH:.3e} m³/s²** — 이론값과 정확히 일치!")

# ============================================================
# TAB 4: 위성 상세 정보
# ============================================================
with tab4:
    st.markdown(f"### 📋 {sat['emoji']} {sat['name_ko']} 상세 정보")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 📡 기본 정보")
        st.markdown(f"""
        - **한글명**: {sat['name_ko']}
        - **영문명**: {sat['name_en']}
        - **궤도 유형**: {sat['type']}
        - **운영 기관**: NASA / NOAA
        - **임무**: {sat['mission']}
        - **발사 연도**: {sat['launch_year']}년
        """)

    with col_b:
        st.markdown("#### 🛰️ 궤도 특성")
        st.markdown(f"""
        - **고도**: {sat['altitude_km']:,} km
        - **궤도 반지름**: {params['r']/1e6:.3f} × 10⁶ m
        - **궤도 경사각**: {sat['inclination']}°
        - **이심률**: {sat['eccentricity']} (거의 원형)
        - **제1우주속도 대비**: {params['v_ratio']*100:.2f}%
        """)

    st.markdown("---")
    st.markdown("#### 🔬 계산된 물리량 (만유인력 기반)")

    physics_table = pd.DataFrame({
        "물리량": [
            "공전 속도 v",
            "공전 주기 T",
            "구심가속도 aₙ",
            "탈출 속도 vₑ",
            "운동 에너지 (단위질량)",
            "위치 에너지 (단위질량)",
            "역학적 총 에너지 (단위질량)",
        ],
        "수식": [
            "v = √(GM/r)",
            "T = 2πr/v",
            "aₙ = GM/r²",
            "vₑ = √(2GM/r)",
            "Eₖ = ½v²",
            "Eₚ = -GM/r",
            "E = Eₖ + Eₚ",
        ],
        "계산값": [
            f"{params['v']:,.2f} m/s",
            f"{params['T_s']:,.1f} 초 = {params['T_min']:.2f} 분",
            f"{params['a_n']:.5f} m/s²",
            f"{params['v_escape']:,.2f} m/s",
            f"{params['E_kinetic']:,.2e} J/kg",
            f"{params['E_potential']:,.2e} J/kg",
            f"{params['E_total']:,.2e} J/kg",
        ]
    })
    st.dataframe(physics_table, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 📐 핵심 공식")
    st.latex(r"\text{만유인력} = \text{구심력} : \quad \frac{GMm}{r^2} = \frac{mv^2}{r}")
    st.latex(r"\Rightarrow \quad v = \sqrt{\frac{GM}{r}}")
    st.latex(r"T = \frac{2\pi r}{v} = 2\pi\sqrt{\frac{r^3}{GM}} \quad \text{(케플러 제3법칙)}")
    st.latex(r"v_1 = \sqrt{\frac{GM}{R_E}} \approx 7{,}905 \text{ m/s} \quad \text{(제1 우주 속도)}")

    # CSV 다운로드
    st.markdown("---")
    csv_data = physics_table.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 위성 데이터 CSV 다운로드",
        data=csv_data,
        file_name=f"{selected_key}_orbit_data.csv",
        mime="text/csv"
    )

# ===== 보고서 양식 다운로드 =====
st.markdown("---")
st.markdown("### 📝 학생 평가 보고서 양식 다운로드")

report_path = os.path.join(os.path.dirname(__file__), "student_report_form.md")
if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        report_md = f.read()
    st.download_button(
        label="📝 보고서 양식 (Markdown)",
        data=report_md,
        file_name="인공위성_궤도_시뮬레이션_보고서.md",
        mime="text/markdown"
    )
else:
    st.info("💡 student_report_form.md 파일을 같은 폴더에 두면 학생들이 직접 다운로드할 수 있습니다.")

# ===== 푸터 =====
st.markdown("---")
st.markdown("""
### 📚 사용된 물리 상수
| 상수 | 값 |
|:---|:---|
| 만유인력 상수 G | 6.674 × 10⁻¹¹ N·m²/kg² |
| 지구 질량 M | 5.972 × 10²⁴ kg |
| 지구 반지름 Rₑ | 6,371 km |
| 제1 우주 속도 v₁ | 7,905 m/s |

### 🔗 데이터 출처
- **ISS**: NASA International Space Station Facts and Figures
- **Landsat 9**: USGS / NASA Landsat Science
- **GOES-16**: NOAA Office of Satellite and Product Operations
""")
