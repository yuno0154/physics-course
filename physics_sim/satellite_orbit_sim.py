import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import math

# ============================================================
#  수행평가: 포물선 운동과 인공위성 궤도의 역학적 연결 탐구
# ============================================================

G = 6.674e-11
M_EARTH = 5.972e24
R_EARTH = 6.371e6
GEO_R = 4.2164e7
V1 = math.sqrt(G * M_EARTH / R_EARTH)  # 제1 우주 속도

PRESETS = {
    "사용자 지정": None,
    "지표면 (r = Rₑ)": 1.0,
    "저궤도 LEO (r ≈ 1.064Rₑ, h=408km)": 1.0 + 408e3/R_EARTH,
    "태양동기 SSO (r ≈ 1.111Rₑ, h=705km)": 1.0 + 705e3/R_EARTH,
    "중궤도 MEO (r ≈ 3.1Rₑ)": 3.1,
    "정지궤도 GEO (r ≈ 6.6Rₑ)": GEO_R/R_EARTH,
}

def calc(r_mult):
    r = r_mult * R_EARTH
    v = math.sqrt(G * M_EARTH / r)
    T = 2 * math.pi * r / v
    a_n = v**2 / r
    F_u = G * M_EARTH / r**2
    v_esc = math.sqrt(2 * G * M_EARTH / r)
    return dict(r=r, v=v, T=T, a_n=a_n, F_u=F_u, v_esc=v_esc,
                T_min=T/60, T_hr=T/3600, v_ratio=v/V1)

# ---------- 헤더 ----------
st.title("🛰️ 수행평가 : 포물선 운동과 인공위성 궤도의 역학적 연결 탐구")
st.markdown("""
**[수행평가 안내]** 평가 요소: 궤도 반지름·속도 해석 / 방식: 시뮬레이션 실험·서술형·개별

지구를 공전하는 인공위성의 **궤도 반지름(r)** 을 변화시키며 **공전 속도(v)** 가 어떻게 변하는지 분석하세요.
시뮬레이션 결과를 바탕으로 **v = √(GM/r)** 를 스스로 유도해 보세요!
""")

# ---------- 공통 제어 사이드바 ----------
st.sidebar.markdown("## ⚙️ 시뮬레이션 제어")
preset = st.sidebar.selectbox("🎯 대표 궤도 프리셋", list(PRESETS.keys()))
if PRESETS[preset] is not None:
    r_mult = PRESETS[preset]
else:
    r_mult = st.sidebar.slider("궤도 반지름 r (×Rₑ)", 1.0, 8.0, 1.0, 0.05)

p = calc(r_mult)

st.sidebar.markdown("---")
st.sidebar.markdown("**🎬 애니메이션 옵션**")
n_frames = st.sidebar.slider("프레임 수", 30, 120, 60, step=10)
frame_dur = st.sidebar.select_slider(
    "재생 속도",
    options=[30, 50, 80, 120, 200],
    value=80,
    format_func=lambda x: {30:"매우 빠름",50:"빠름",80:"보통",120:"느림",200:"매우 느림"}[x]
)
st.sidebar.markdown("---")
st.sidebar.markdown("**📐 벡터 옵션**")
show_v = st.sidebar.checkbox("✅ 속도 벡터 (녹색)", value=True)
show_f = st.sidebar.checkbox("✅ 만유인력 벡터 (주황)", value=True)
show_trail = st.sidebar.checkbox("✅ 궤도 경로 (점선)", value=True)

# ---------- 탭 ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 궤도 애니메이션",
    "📊 대표 궤도 비교",
    "📈 r-v 관계 그래프",
    "📋 물리량 상세 & 보고서"
])

# ============================================================
# TAB 1: 궤도 애니메이션
# ============================================================
with tab1:
    st.markdown(f"### 🌍 인공위성 궤도 운동 — r = {r_mult:.3f} Rₑ")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("궤도 반지름 r", f"{p['r']/1e6:.3f} ×10⁶ m")
    c2.metric("공전 속도 v", f"{p['v']:,.1f} m/s", f"{p['v_ratio']*100:.1f}% × v₁")
    c3.metric("공전 주기 T", f"{p['T_min']:.2f} 분" if p['T_hr']<1 else f"{p['T_hr']:.2f} 시간")
    c4.metric("구심가속도 aₙ", f"{p['a_n']:.4f} m/s²", f"g의 {p['a_n']/9.8*100:.1f}%")

    theta_e = np.linspace(0, 2*np.pi, 100)
    ex, ey = np.cos(theta_e), np.sin(theta_e)
    theta_o = np.linspace(0, 2*np.pi, 200)
    ox = r_mult * np.cos(theta_o)
    oy = r_mult * np.sin(theta_o)

    def make_traces(sx, sy, ang):
        vx_d, vy_d = -np.sin(ang), np.cos(ang)
        fx_d, fy_d = -np.cos(ang), -np.sin(ang)
        vl = r_mult * 0.25
        trs = [go.Scatter(x=ex, y=ey, mode='lines', name='🌍 지구',
                          line=dict(color='#1E90FF', width=2),
                          fill='toself', fillcolor='rgba(30,144,255,0.4)', hoverinfo='skip')]
        if show_trail:
            trs.append(go.Scatter(x=ox, y=oy, mode='lines', name='궤도',
                                  line=dict(color='rgba(200,200,200,0.3)', width=1.5, dash='dash'),
                                  hoverinfo='skip'))
        trs.append(go.Scatter(x=[sx], y=[sy], mode='markers', name='🛰️ 위성',
                              marker=dict(size=16, color='#FF6B6B', line=dict(color='white',width=2))))
        if show_v:
            trs.append(go.Scatter(x=[sx, sx+vx_d*vl], y=[sy, sy+vy_d*vl],
                                  mode='lines+markers', name='속도 v',
                                  line=dict(color='#00FF7F', width=4),
                                  marker=dict(size=[0,10], symbol='triangle-up', color='#00FF7F')))
        if show_f:
            trs.append(go.Scatter(x=[sx, sx+fx_d*vl*0.7], y=[sy, sy+fy_d*vl*0.7],
                                  mode='lines+markers', name='만유인력 F',
                                  line=dict(color='#FFA500', width=4),
                                  marker=dict(size=[0,10], symbol='triangle-left', color='#FFA500')))
        return trs

    frames = []
    steps = []
    for i in range(n_frames):
        ang = 2*np.pi*i/n_frames
        sx = r_mult*np.cos(ang); sy = r_mult*np.sin(ang)
        t_el = (i/n_frames)*p['T']
        t_str = f"{t_el/60:.1f} 분" if p['T_hr']<1 else f"{t_el/3600:.2f} 시간"
        telemetry = (f"<b>🛰️ 인공위성</b><br>"
                     f"r = {r_mult:.2f} Rₑ<br>"
                     f"v = {p['v']:,.0f} m/s<br>"
                     f"경과: {t_str}<br>"
                     f"진행: {i/n_frames*100:.0f}%")
        frames.append(go.Frame(
            data=make_traces(sx, sy, ang), name=f"f{i}",
            layout=go.Layout(annotations=[dict(
                x=0.02, y=0.98, xref="paper", yref="paper",
                text=telemetry, showarrow=False, align="left",
                bgcolor="rgba(20,20,30,0.85)", bordercolor="#FF6B6B",
                borderwidth=2, font=dict(family="monospace", size=12, color="white")
            )])
        ))
        steps.append(dict(
            args=[[f"f{i}"], dict(frame=dict(duration=frame_dur, redraw=True), mode="immediate")],
            label=f"{int(i/n_frames*100)}%", method="animate"
        ))

    lim = r_mult * 1.35
    fig1 = go.Figure(data=make_traces(r_mult, 0, 0), frames=frames)
    fig1.update_layout(
        title=f"인공위성 궤도 운동  r={r_mult:.2f}Rₑ  v={p['v']:,.0f}m/s  T={p['T_min']:.1f}분",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14', font=dict(color='white'),
        xaxis=dict(range=[-lim,lim], title="X (Rₑ 단위)", gridcolor='rgba(100,100,100,0.2)'),
        yaxis=dict(range=[-lim,lim], title="Y (Rₑ 단위)", scaleanchor="x", scaleratio=1,
                   gridcolor='rgba(100,100,100,0.2)'),
        height=640,
        updatemenus=[dict(type="buttons", direction="left", x=0.05, y=-0.07,
                          showactive=False, bgcolor='#1a1a2e',
                          buttons=[
                              dict(label="▶ 재생", method="animate",
                                   args=[None, dict(frame=dict(duration=frame_dur, redraw=True),
                                                    fromcurrent=True, mode="immediate")]),
                              dict(label="⏸ 정지", method="animate",
                                   args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])
                          ])],
        sliders=[dict(active=0, currentvalue=dict(prefix="진행: ", font=dict(size=13)),
                      pad=dict(b=10, t=40), len=0.85, x=0.1, y=-0.07, steps=steps)]
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.info(f"💡 **제1 우주 속도** v₁ = {V1:.1f} m/s  |  현재 위성 v / v₁ = **{p['v_ratio']:.4f}**  "
            f"|  r/Rₑ = {r_mult:.3f}")

# ============================================================
# TAB 2: 대표 궤도 비교
# ============================================================
with tab2:
    st.markdown("### 📊 대표 궤도 5종 종합 비교")

    orbits = {
        "지표면": 1.0,
        "LEO (ISS)": 1.0 + 408e3/R_EARTH,
        "SSO (Landsat)": 1.0 + 705e3/R_EARTH,
        "MEO": 3.1,
        "GEO (정지)": GEO_R/R_EARTH,
    }
    rows = []
    for name, rm in orbits.items():
        q = calc(rm)
        T_str = f"{q['T_min']:.1f} 분" if q['T_hr']<1 else (
            f"{q['T_hr']:.2f} 시간" if q['T_hr']<24 else f"{q['T_hr']/24:.2f} 일")
        rows.append({"궤도": name, "r/Rₑ": f"{rm:.3f}",
                     "r (×10⁶ m)": f"{q['r']/1e6:.3f}",
                     "v (m/s)": f"{q['v']:,.1f}", "T": T_str,
                     "aₙ (m/s²)": f"{q['a_n']:.4f}",
                     "v/v₁": f"{q['v_ratio']:.4f}"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    orbit_names = list(orbits.keys())
    colors = ["#FF6B6B","#FF6B6B","#95E1D3","#F7DC6F","#4ECDC4"]
    vs = [calc(rm)['v'] for rm in orbits.values()]
    Ts = [calc(rm)['T_hr'] for rm in orbits.values()]

    col1, col2 = st.columns(2)
    with col1:
        fig_v = go.Figure(go.Bar(x=orbit_names, y=vs, marker_color=colors,
                                 text=[f"{v:,.0f}" for v in vs], textposition='auto'))
        fig_v.update_layout(title="공전 속도 비교 (m/s)",
                            plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
                            font=dict(color='white'), height=380,
                            yaxis=dict(gridcolor='rgba(100,100,100,0.2)'))
        st.plotly_chart(fig_v, use_container_width=True)
    with col2:
        fig_t = go.Figure(go.Bar(x=orbit_names, y=Ts, marker_color=colors,
                                 text=[f"{t:.2f}h" if t<24 else f"{t/24:.2f}일" for t in Ts],
                                 textposition='auto'))
        fig_t.update_layout(title="공전 주기 비교 (로그, 시간)",
                            yaxis_type="log", plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
                            font=dict(color='white'), height=380,
                            yaxis=dict(gridcolor='rgba(100,100,100,0.2)', title="주기 (시간)"))
        st.plotly_chart(fig_t, use_container_width=True)

    st.markdown("#### 🌍 실제 스케일 궤도 크기 비교")
    fig_sc = go.Figure()
    theta = np.linspace(0, 2*np.pi, 100)
    fig_sc.add_trace(go.Scatter(x=R_EARTH/1e6*np.cos(theta), y=R_EARTH/1e6*np.sin(theta),
                                fill='toself', fillcolor='rgba(30,144,255,0.4)',
                                line=dict(color='#1E90FF', width=2), name='🌍 지구'))
    for (name, rm), col in zip(orbits.items(), colors):
        r_km = (rm * R_EARTH)/1e6
        fig_sc.add_trace(go.Scatter(x=r_km*np.cos(theta), y=r_km*np.sin(theta),
                                    mode='lines', line=dict(color=col, width=2, dash='dash'),
                                    name=name))
    maxr = max(rm*R_EARTH for rm in orbits.values())/1e6*1.15
    fig_sc.update_layout(title="실제 스케일 궤도 (×10⁶ m)",
                         plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14',
                         font=dict(color='white'), height=500,
                         xaxis=dict(range=[-maxr,maxr], gridcolor='rgba(100,100,100,0.2)', title="X (×10⁶ m)"),
                         yaxis=dict(range=[-maxr,maxr], scaleanchor="x", scaleratio=1,
                                    gridcolor='rgba(100,100,100,0.2)', title="Y (×10⁶ m)"))
    st.plotly_chart(fig_sc, use_container_width=True)
    st.info("💡 정지궤도(GEO)가 저궤도(LEO)보다 약 6.6배 멀리 있어 공전 속도는 더 느리지만 주기는 24시간으로 지구 자전과 동기화됩니다.")

# ============================================================
# TAB 3: r-v 관계 그래프
# ============================================================
with tab3:
    st.markdown("### 📈 궤도 반지름(r) vs 공전 속도(v)")

    r_curve = np.linspace(R_EARTH, 8*R_EARTH, 300)
    v_curve = np.sqrt(G * M_EARTH / r_curve)

    fig_rv = go.Figure()
    fig_rv.add_trace(go.Scatter(x=r_curve/1e6, y=v_curve, mode='lines',
                                name='이론: v = √(GM/r)',
                                line=dict(color='#888', width=2.5, dash='dash')))
    fig_rv.add_hline(y=V1, line=dict(color='yellow', dash='dot', width=1.5),
                     annotation_text=f"제1 우주속도 v₁ = {V1:.0f} m/s",
                     annotation_position="top right", annotation_font_color="yellow")

    sample_rm = np.array([1.0, 1.0+408e3/R_EARTH, 1.0+705e3/R_EARTH, 3.1, GEO_R/R_EARTH])
    s_colors  = ["#FF6B6B","#FF9F43","#95E1D3","#F7DC6F","#4ECDC4"]
    s_labels  = ["지표면","LEO(ISS)","SSO(Landsat)","MEO","GEO(정지)"]
    for rm, col, lbl in zip(sample_rm, s_colors, s_labels):
        q = calc(rm)
        fig_rv.add_trace(go.Scatter(x=[q['r']/1e6], y=[q['v']],
                                    mode='markers+text', text=[lbl],
                                    textposition='top center',
                                    textfont=dict(size=11, color='white'),
                                    marker=dict(size=16, color=col, line=dict(color='white',width=2)),
                                    name=lbl))
    # 현재 위성 강조
    fig_rv.add_trace(go.Scatter(x=[p['r']/1e6], y=[p['v']],
                                mode='markers', name='현재 위성',
                                marker=dict(size=20, color='gold', symbol='star',
                                            line=dict(color='black',width=1))))
    fig_rv.update_layout(
        title="궤도 반지름과 공전 속도의 관계", height=520,
        xaxis_title="궤도 반지름 r (×10⁶ m)", yaxis_title="공전 속도 v (m/s)",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14', font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        yaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        legend=dict(bgcolor='rgba(20,20,30,0.7)')
    )
    st.plotly_chart(fig_rv, use_container_width=True)

    st.markdown("""
    #### 📌 그래프 해석
    - **회색 점선**: 만유인력 = 구심력에서 유도된 이론 곡선 $v = \\sqrt{GM/r}$
    - **컬러 점**: 대표 궤도 측정값 → 모두 이론 곡선 위에 위치
    - **⭐ 금색 별**: 현재 슬라이더로 선택된 위성
    - **노란 점선**: 제1 우주 속도 (지표면 기준)
    """)

    st.markdown("#### 🔍 선형 분석: $v^2$ vs $1/r$")
    fig_lin = go.Figure()
    fig_lin.add_trace(go.Scatter(x=(1/r_curve)*1e7, y=(v_curve**2)/1e7, mode='lines',
                                 name='이론: v² = GM/r',
                                 line=dict(color='#888', width=2.5, dash='dash')))
    for rm, col, lbl in zip(sample_rm, s_colors, s_labels):
        q = calc(rm)
        fig_lin.add_trace(go.Scatter(x=[(1/q['r'])*1e7], y=[(q['v']**2)/1e7],
                                     mode='markers+text', text=[lbl],
                                     textposition='top center',
                                     marker=dict(size=14, color=col, line=dict(color='white',width=2)),
                                     name=lbl))
    fig_lin.update_layout(
        title="v² vs 1/r — 직선 관계 확인 (기울기 = GM)", height=420,
        xaxis_title="1/r (×10⁻⁷ m⁻¹)", yaxis_title="v² (×10⁷ m²/s²)",
        plot_bgcolor='#0a0a14', paper_bgcolor='#0a0a14', font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(100,100,100,0.2)'),
        yaxis=dict(gridcolor='rgba(100,100,100,0.2)')
    )
    st.plotly_chart(fig_lin, use_container_width=True)
    st.success(f"📏 **기울기 = GM = {G*M_EARTH:.3e} m³/s²** — 이론값과 정확히 일치!")

# ============================================================
# TAB 4: 물리량 상세 & 보고서
# ============================================================
with tab4:
    st.markdown(f"### 📋 현재 위성 물리량 상세 분석  (r = {r_mult:.3f} Rₑ)")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 🔬 역학적 분석표")
        analysis_df = pd.DataFrame({
            "물리량": ["공전 속도 v","공전 주기 T","구심가속도 aₙ",
                       "단위질량당 만유인력 F/m","탈출 속도 vₑ","v / v₁ (제1우주속도 비)"],
            "수식": ["√(GM/r)","2πr/v","v²/r = GM/r²","GM/r²","√(2GM/r)","v/√(GM/Rₑ)"],
            "계산값": [
                f"{p['v']:,.2f} m/s",
                f"{p['T_min']:.2f} 분 ({p['T_hr']:.3f} 시간)",
                f"{p['a_n']:.5f} m/s²",
                f"{p['F_u']:.5f} N/kg",
                f"{p['v_esc']:,.2f} m/s",
                f"{p['v_ratio']:.5f}"
            ]
        })
        st.dataframe(analysis_df, use_container_width=True, hide_index=True)

    with col_b:
        st.markdown("#### 📐 핵심 공식")
        st.latex(r"\frac{GMm}{r^2} = \frac{mv^2}{r}")
        st.latex(r"\Rightarrow v = \sqrt{\frac{GM}{r}}")
        st.latex(r"T = \frac{2\pi r}{v} = 2\pi\sqrt{\frac{r^3}{GM}}")
        st.latex(r"v_1 = \sqrt{\frac{GM}{R_E}} \approx 7{,}905 \text{ m/s}")

    st.markdown("---")
    st.markdown("#### 📊 전체 궤도 반지름 구간 데이터표")

    exp_rm = np.array([1.0, 1.064, 1.111, 1.5, 2.0, 3.1, 4.5, 6.6])
    exp_r  = exp_rm * R_EARTH
    exp_v  = np.sqrt(G * M_EARTH / exp_r)
    exp_T  = 2*np.pi*exp_r/exp_v
    export_df = pd.DataFrame({
        "회차": np.arange(1, len(exp_rm)+1),
        "r/Rₑ": exp_rm,
        "r (m)": exp_r.round(0),
        "v (m/s)": exp_v.round(2),
        "T (s)": exp_T.round(2),
        "v² (m²/s²)": (exp_v**2).round(2),
        "1/r (m⁻¹)": (1/exp_r).round(12),
    })
    st.dataframe(export_df, use_container_width=True, hide_index=True)
    st.download_button("⬇ 측정 데이터 CSV 다운로드",
                       data=export_df.to_csv(index=False).encode("utf-8-sig"),
                       file_name="satellite_orbit_data.csv", mime="text/csv")

    st.markdown("---")
    st.markdown("""
    > 🔎 **탐구 미션**
    > 1. 위 데이터로 **v² vs 1/r** 그래프를 그리고, 기울기가 무엇을 의미하는지 해석하시오.
    > 2. 시뮬레이션 결과에서 **v = √(GM/r)** 식을 스스로 유도하시오.
    > 3. **제1 우주 속도**가 데이터의 어느 지점에 해당하는지 정량적으로 설명하시오.
    """)
