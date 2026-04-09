import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

# ── 물리 상수 ──────────────────────────────────────────────
G = 6.674e-11

PLANETS = {
    "화성 (Mars)":   {"M": 6.39e23,  "R_km": 3389.5, "color": "#c1440e", "emoji": "🔴"},
    "지구 (Earth)":  {"M": 5.972e24, "R_km": 6371.0, "color": "#1a7abf", "emoji": "🌍"},
    "달 (Moon)":     {"M": 7.342e22, "R_km": 1737.4, "color": "#b0b0b0", "emoji": "🌕"},
    "목성 (Jupiter)":{"M": 1.898e27, "R_km": 71492.0,"color": "#c88b3a", "emoji": "🟠"},
}

def calculate_orbit(a_km, e, M):
    a = a_km * 1000
    T = 2 * np.pi * np.sqrt(a**3 / (G * M))
    rp = a * (1 - e)
    ra = a * (1 + e)
    vp = np.sqrt(G * M * (2/rp - 1/a))
    va = np.sqrt(G * M * (2/ra - 1/a))
    return {"T_s": T, "T_h": T/3600, "T_d": T/86400,
            "rp_km": rp/1000, "ra_km": ra/1000,
            "vp": vp, "va": va, "a_km": a_km, "e": e}

def orbit_points(a_km, e, n=300):
    a = a_km * 1000
    b = a * np.sqrt(1 - e**2)
    c = a * e   # 초점 이동
    theta = np.linspace(0, 2*np.pi, n)
    x = a * np.cos(theta) - c
    y = b * np.sin(theta)
    return x/1000, y/1000   # km 단위 반환

def kepler_animation(a_km, e, planet_info, orbit_result):
    """Plotly 타원 궤도 애니메이션 생성"""
    a = a_km * 1000
    b = a * np.sqrt(1 - e**2)
    c = a * e
    R_body = planet_info["R_km"] * 1000

    # 궤도상 행성 위치 (평균 이상점 근사)
    N = 80
    theta_arr = np.linspace(0, 2*np.pi, N, endpoint=False)
    # 실제 케플러 방정식 근사 (뉴턴 반복)
    E_arr = theta_arr.copy()
    for _ in range(50):
        E_arr = E_arr - (E_arr - e * np.sin(E_arr) - theta_arr) / (1 - e * np.cos(E_arr))
    true_theta = 2 * np.arctan2(np.sqrt(1+e)*np.sin(E_arr/2), np.sqrt(1-e)*np.cos(E_arr/2))
    r_arr = a * (1 - e**2) / (1 + e * np.cos(true_theta))
    px = r_arr * np.cos(true_theta) / 1000 - c/1000
    py = r_arr * np.sin(true_theta) / 1000

    # 현재 속력 계산
    v_arr = np.sqrt(G * planet_info["M"] * (2/r_arr - 1/a))

    # 궤도 경로
    ox, oy = orbit_points(a_km, e)

    scale = a_km * 1.6
    frames = []
    for i in range(N):
        frames.append(go.Frame(
            data=[
                go.Scatter(x=ox, y=oy, mode="lines",
                           line=dict(color="rgba(100,148,237,0.5)", width=1.5, dash="dot"),
                           name="궤도", showlegend=False),
                go.Scatter(x=[0], y=[0], mode="markers",
                           marker=dict(size=22, color=planet_info["color"],
                                       line=dict(color="white", width=2)),
                           name=list(PLANETS.keys())[[p["M"] for p in PLANETS.values()].index(planet_info["M"])],
                           showlegend=False),
                go.Scatter(x=[px[i]], y=[py[i]], mode="markers",
                           marker=dict(size=14, color="#38bdf8",
                                       line=dict(color="white", width=2)),
                           showlegend=False, name="탐사선"),
                # 속도 벡터 (접선)
                go.Scatter(
                    x=[px[i], px[i] - r_arr[i]/1000 * np.sin(true_theta[i]) * 0.25 * v_arr[i]/orbit_result["vp"]],
                    y=[py[i], py[i] + r_arr[i]/1000 * np.cos(true_theta[i]) * 0.25 * v_arr[i]/orbit_result["vp"]],
                    mode="lines+markers",
                    line=dict(color="#4ade80", width=3),
                    marker=dict(size=[0, 8], symbol=["circle", "arrow"], color="#4ade80",
                                angleref="previous"),
                    showlegend=False, name="속도"),
                go.Scatter(
                    x=[None], y=[None], mode="markers",
                    marker=dict(color="rgba(0,0,0,0)"),
                    text=[f"v = {v_arr[i]/1000:.2f} km/s"],
                    showlegend=False,
                    textposition="top center"
                ),
            ],
            name=str(i),
            layout=go.Layout(
                annotations=[dict(
                    x=0.02, y=0.97, xref="paper", yref="paper",
                    text=f"<b>현재 속도: {v_arr[i]/1000:.2f} km/s</b><br>"
                         f"거리: {r_arr[i]/1000:.0f} km",
                    showarrow=False, align="left",
                    bgcolor="rgba(15,23,42,0.85)",
                    bordercolor="#38bdf8", borderwidth=1,
                    font=dict(color="white", size=13),
                    borderpad=8
                )]
            )
        ))

    fig = go.Figure(
        data=frames[0].data,
        layout=go.Layout(
            template="plotly_dark",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            xaxis=dict(range=[-scale, scale], zeroline=False,
                       showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       title="x (km)", tickfont=dict(size=11)),
            yaxis=dict(range=[-scale, scale], zeroline=False,
                       showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       scaleanchor="x", title="y (km)", tickfont=dict(size=11)),
            height=500,
            margin=dict(l=50, r=50, t=60, b=50),
            title=dict(text="🛸 타원 궤도 애니메이션 (케플러 제2법칙 시각화)",
                       font=dict(size=16, color="white"), x=0.5),
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                y=1.12, x=1.0, xanchor="right",
                buttons=[
                    dict(label="▶ Play", method="animate",
                         args=[None, {"frame": {"duration": 60, "redraw": True},
                                      "fromcurrent": True, "transition": {"duration": 0}}]),
                    dict(label="⏸ Pause", method="animate",
                         args=[[None], {"frame": {"duration": 0, "redraw": False},
                                        "mode": "immediate", "transition": {"duration": 0}}]),
                ],
                bgcolor="#1e293b", bordercolor="#38bdf8",
                font=dict(color="white", size=13)
            )],
            sliders=[dict(
                steps=[dict(method="animate", args=[[f.name],
                            {"mode": "immediate", "frame": {"duration": 60, "redraw": True},
                             "transition": {"duration": 0}}],
                            label=str(i)) for i, f in enumerate(frames)],
                currentvalue=dict(prefix="프레임: ", font=dict(color="white")),
                pad=dict(t=10),
                bgcolor="#1e293b",
                bordercolor="#334155",
                tickcolor="#64748b",
                font=dict(color="#94a3b8")
            )],
            annotations=[dict(
                x=0.02, y=0.97, xref="paper", yref="paper",
                text=f"<b>현재 속도: {v_arr[0]/1000:.2f} km/s</b><br>"
                     f"거리: {r_arr[0]/1000:.0f} km",
                showarrow=False, align="left",
                bgcolor="rgba(15,23,42,0.85)",
                bordercolor="#38bdf8", borderwidth=1,
                font=dict(color="white", size=13),
                borderpad=8
            )]
        ),
        frames=frames
    )
    return fig


def loglog_plot(a_km, e, planet_info):
    """Log-Log Plot: T² vs a³"""
    M = planet_info["M"]
    a_ref = np.logspace(3.5, 6.5, 200)  # km
    T_ref = 2 * np.pi * np.sqrt((a_ref * 1000)**3 / (G * M)) / 3600  # hours

    a_user = a_km
    T_user = 2 * np.pi * np.sqrt((a_user * 1000)**3 / (G * M)) / 3600

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=a_ref**3, y=T_ref**2,
        mode="lines",
        line=dict(color="#6366f1", width=2.5),
        name="케플러 제3법칙 T² ∝ a³"
    ))
    fig.add_trace(go.Scatter(
        x=[a_user**3], y=[T_user**2],
        mode="markers",
        marker=dict(size=16, color="#f59e0b", symbol="star",
                    line=dict(color="white", width=2)),
        name=f"내 궤도 (a={a_km:,.0f} km)"
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        xaxis=dict(type="log", title="a³ (km³)", gridcolor="rgba(255,255,255,0.07)",
                   tickfont=dict(size=11)),
        yaxis=dict(type="log", title="T² (h²)", gridcolor="rgba(255,255,255,0.07)",
                   tickfont=dict(size=11)),
        title=dict(text="📈 Log-Log Plot: 케플러 제3법칙 검증",
                   font=dict(size=15, color="white"), x=0.5),
        height=380,
        margin=dict(l=60, r=30, t=60, b=50),
        legend=dict(bgcolor="rgba(15,23,42,0.8)", bordercolor="#334155",
                    font=dict(color="white", size=12))
    )
    return fig


def run_sim():
    st.set_page_config(page_title="화성 탐사선 '다누리 2호' 궤도 설계 프로젝트", layout="wide")

    st.title("🚀 프로젝트: 화성 탐사선 '다누리 2호' 궤도 설계")
    st.markdown("""
    대한민국 우주항공청(KASA) 연구원이 되어 화성 관측을 위한 최적의 타원 궤도를 설계하고 물리학적으로 입증하는 수행평가 프로젝트입니다.
    **GRASPS 전략**에 따라 미션을 수행하고 탐구 보고서를 작성해 보세요.
    """)

    react_code = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useEffect } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerProject = () => {
                return (
                    <div className="max-w-5xl mx-auto p-4">
                        <div className="bg-white rounded-[40px] overflow-hidden border border-slate-200 shadow-2xl">
                            <div className="bg-gradient-to-br from-indigo-700 via-blue-800 to-slate-900 p-12 text-white relative">
                                <div className="absolute top-0 right-0 w-64 h-64 bg-blue-400/10 rounded-full blur-3xl"></div>
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-2 bg-white/10 rounded-xl backdrop-blur-md">
                                        <Icon name="lightbulb" size={24} className="text-amber-400" />
                                    </div>
                                    <span className="text-blue-200 font-black uppercase tracking-[0.3em] text-xs">Performance Assessment (GRASPS)</span>
                                </div>
                                <h2 className="text-4xl font-black mb-4 leading-tight">화성 탐사선 '다누리 2호'<br/>궤도 설계 및 주기 분석</h2>
                                <p className="text-blue-100 opacity-80 text-base max-w-2xl leading-relaxed">
                                    화성 표면 정밀 관측과 전역 통신망 확보라는 두 가지 목표를 달성하기 위해 가장 효율적인 타원 궤도를 설계하고, 케플러 법칙을 적용하여 궤도의 타당성을 증명하십시오.
                                </p>
                            </div>

                            <div className="p-12 grid grid-cols-1 md:grid-cols-2 gap-12 items-start bg-white">
                                <div className="space-y-10">
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-blue-100 group-hover:scale-110 transition-transform">G</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Goal (목표)</h4>
                                            <p className="text-[14px] text-slate-500 leading-relaxed font-medium">최소 연료로 운용 가능한 안정적인 타원 궤도를 설계하고 공전 주기를 계산하여 이론적 정확성을 입증함.</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-indigo-100 group-hover:scale-110 transition-transform">R</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Role (역할)</h4>
                                            <p className="text-[14px] text-slate-500 leading-relaxed font-medium">대한민국 우주항공청(KASA) 소속 궤도역학 전문 수석 연구원</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-slate-50 text-slate-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-slate-100 group-hover:scale-110 transition-transform">S</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Standards (평가 기준)</h4>
                                            <ul className="text-[13px] text-slate-500 list-disc list-inside space-y-2 mt-2 font-bold marker:text-blue-500">
                                                <li>제3법칙을 활용한 주기 계산의 수치적 정확성</li>
                                                <li>이심률에 따른 속력 변화의 물리학적 인과관계</li>
                                                <li>설계 궤도의 효율성에 대한 논리적 타당성</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-8 bg-slate-50 p-8 rounded-[40px] border-4 border-dashed border-slate-200 relative overflow-hidden">
                                    <h4 className="font-black text-slate-700 flex items-center gap-2 text-sm uppercase tracking-widest mb-2">
                                        <Icon name="rocket" className="text-blue-600" /> Mission Briefing
                                    </h4>
                                    <div className="text-[14px] text-slate-600 font-bold space-y-6 leading-relaxed">
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">01</span>
                                            <p><strong className="text-blue-700">궤도 조작:</strong> 시뮬레이터를 활용해 최적의 이심률을 도출하고, 근일점과 원일점의 비율을 설정하십시오.</p>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">02</span>
                                            <p><strong className="text-emerald-700">물리 검증:</strong> 화성의 관측 목적(고해상도 촬영 vs 광범위 통신)에 따른 궤도의 장단점을 서술하십시오.</p>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">03</span>
                                            <p><strong className="text-amber-700">수식 도출:</strong> 뉴턴의 중력 법칙에서 케플러 제3법칙이 유도되는 과정을 보고서에 포함하십시오.</p>
                                        </div>
                                    </div>
                                    <div className="pt-6">
                                        <p className="text-center text-[10px] text-slate-400 mt-4 font-bold tracking-tight">
                                            * 아래 시뮬레이터에서 궤도를 설계하고, 연구보고서 페이지에서 제출하세요.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerProject />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=750, scrolling=False)

    # ════════════════════════════════════════════════════════════════
    # 🛸 궤도 시뮬레이터 섹션
    # ════════════════════════════════════════════════════════════════
    st.markdown("---")
    st.markdown("## 🛸 궤도 설계 시뮬레이터")
    st.markdown("""
    아래 사이드바에서 **궤도 장반경**과 **이심률**을 조절하여 탐사선 궤도를 직접 설계해 보세요.
    케플러 제2법칙(면적 속도 일정)의 시각화와 제3법칙 검증 그래프를 실시간으로 확인할 수 있습니다.
    """)

    # ── 사이드바 입력 ──────────────────────────────────────
    with st.sidebar:
        st.markdown("### 🛸 궤도 설계 파라미터")
        st.markdown("---")

        planet_name = st.selectbox(
            "🌍 중심 천체 선택",
            list(PLANETS.keys()),
            index=0
        )
        planet_info = PLANETS[planet_name]
        R_km = planet_info["R_km"]

        st.markdown(f"""
        <div style="background:#1e293b;border-radius:12px;padding:12px;margin:8px 0;border:1px solid #334155">
            <div style="color:#94a3b8;font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.1em">선택된 천체</div>
            <div style="color:white;font-size:1.1rem;font-weight:800;margin-top:4px">{planet_info['emoji']} {planet_name}</div>
            <div style="color:#64748b;font-size:0.75rem">반지름: {R_km:,.1f} km | 질량: {planet_info['M']:.2e} kg</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("**① 궤도 장반경 (a)**")
        a_min = int(R_km) + 100
        a_default = max(a_min, int(R_km * 1.5) + 3000)
        a_km = st.slider(
            "장반경 a (km) — 천체 표면 기준 고도 포함",
            min_value=a_min,
            max_value=a_min + 20000,
            value=a_default,
            step=100,
            help="장반경은 천체 반지름보다 커야 합니다."
        )
        altitude_km = a_km - R_km
        st.caption(f"📡 표면으로부터 평균 고도: **{altitude_km:,.0f} km**")

        st.markdown("**② 이심률 (e)**")
        e = st.slider(
            "이심률 e",
            min_value=0.0,
            max_value=0.80,
            value=0.30,
            step=0.01,
            help="0 = 원 궤도, 0.8 = 긴 타원 궤도"
        )

        orbit = calculate_orbit(a_km, e, planet_info["M"])

        st.markdown("---")
        st.markdown("### 📊 계산 결과")

        def metric_card(label, value, unit="", color="#38bdf8"):
            st.markdown(f"""
            <div style="background:#0f172a;border:1px solid #1e293b;border-radius:12px;
                        padding:10px 14px;margin:6px 0;border-left:3px solid {color}">
                <div style="color:#64748b;font-size:0.7rem;font-weight:700;text-transform:uppercase">{label}</div>
                <div style="color:{color};font-size:1.05rem;font-weight:800;margin-top:2px">
                    {value} <span style="color:#64748b;font-size:0.75rem">{unit}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        metric_card("공전 주기 T", f"{orbit['T_h']:.2f}", "시간", "#a78bfa")
        metric_card("공전 주기 T", f"{orbit['T_d']:.4f}", "일", "#a78bfa")
        metric_card("근일점 거리", f"{orbit['rp_km']:,.0f}", "km", "#f87171")
        metric_card("원일점 거리", f"{orbit['ra_km']:,.0f}", "km", "#60a5fa")
        metric_card("근일점 속도 (최대)", f"{orbit['vp']/1000:.3f}", "km/s", "#4ade80")
        metric_card("원일점 속도 (최소)", f"{orbit['va']/1000:.3f}", "km/s", "#fbbf24")

        st.markdown(f"""
        <div style="background:#064e3b;border:1px solid #065f46;border-radius:12px;
                    padding:10px 14px;margin:10px 0;text-align:center">
            <div style="color:#6ee7b7;font-size:0.75rem;font-weight:700">속도 차이 배율</div>
            <div style="color:#34d399;font-size:1.3rem;font-weight:900">
                × {orbit['vp']/orbit['va']:.2f}
            </div>
            <div style="color:#6ee7b7;font-size:0.68rem">근일점이 원일점보다 빠름</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 메인 출력 영역 ─────────────────────────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### 🎬 실시간 궤도 애니메이션")
        st.caption("▶ Play 버튼을 눌러 애니메이션을 시작하세요. 근일점(가장 가까운 지점)에서 속도가 가장 빠릅니다.")
        fig_anim = kepler_animation(a_km, e, planet_info, orbit)
        st.plotly_chart(fig_anim, use_container_width=True, key="orbit_anim")

    with col2:
        st.markdown("### 📈 케플러 제3법칙 검증")
        st.caption("내 궤도(⭐)가 이론 직선 위에 놓여야 케플러 제3법칙을 만족합니다.")
        fig_log = loglog_plot(a_km, e, planet_info)
        st.plotly_chart(fig_log, use_container_width=True, key="loglog_plot")

        # 탐구 미션 카드
        st.markdown("---")
        st.markdown("#### 🔬 탐구 미션 체크리스트")

        rp_alt = orbit["rp_km"] - R_km
        ra_alt = orbit["ra_km"] - R_km
        mission1_ok = rp_alt < 500
        mission2_ok = ra_alt > 3000

        c1, c2 = st.columns(2)
        with c1:
            if mission1_ok:
                st.success(f"✅ **미션 1**: 근일점 고도 {rp_alt:.0f}km\n고해상도 촬영 가능!")
            else:
                st.info(f"🔵 **미션 1**: 근일점 고도 {rp_alt:.0f}km\n촬영을 위해 e를 높여보세요.")
        with c2:
            if mission2_ok:
                st.success(f"✅ **미션 2**: 원일점 고도 {ra_alt:.0f}km\n광역 통신 커버 가능!")
            else:
                st.info(f"🔵 **미션 2**: 원일점 고도 {ra_alt:.0f}km\n광역 통신을 위해 a를 높여보세요.")

    # ── 탐구 질문 섹션 ────────────────────────────────────
    st.markdown("---")
    st.markdown("## 🧠 심화 탐구 질문")

    q_col1, q_col2 = st.columns(2)
    with q_col1:
        with st.expander("📌 미션 1 — 관측 vs 통신 궤도 트레이드오프", expanded=False):
            st.markdown("""
**고해상도 촬영 미션**에서는 이심률을 높여 근일점을 낮춥니다.
그러나 근일점에서의 속도가 너무 빨라 **촬영 시간이 부족해지는** 문제가 생깁니다.

> **탐구 질문:** 이심률 $e$ 가 커질수록 근일점 통과 시간이 짧아지는 이유를
> 케플러 **제2법칙(면적 속도 일정)**으로 설명하시오.

**광범위 통신 미션**에서는 원일점 거리를 늘리지만,
주기 $T$ 가 지나치게 길어져 **통신 지연**이 발생합니다.

> **탐구 질문:** 현재 시뮬레이터 값에서 $T$ 가 통신 위성으로 적절한지
> 수치를 근거로 판단하시오.
            """)
    with q_col2:
        with st.expander("📌 미션 2 — 속도 차이의 물리적 인과관계", expanded=False):
            st.markdown(f"""
현재 설정에서:
- **근일점 속도 (최대):** {orbit['vp']/1000:.3f} km/s
- **원일점 속도 (최소):** {orbit['va']/1000:.3f} km/s
- **배율:** × {orbit['vp']/orbit['va']:.2f}

> **탐구 질문:** 이심률 $e$를 높였더니 근일점과 원일점의 속도 차이가 커졌다.
> 그 이유는 케플러 **제2법칙**인가, 아니면 **역학적 에너지 보존**인가?
> 두 관점에서 모두 설명하고, 어느 설명이 더 근본적인지 논하시오.

*힌트: $v_p = \sqrt{\\frac{GM}{a}\\cdot\\frac{1+e}{1-e}}$ 에서 $e$가 클수록 $v_p$는?*
            """)


if __name__ == "__main__":
    run_sim()
