import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── 물리 상수 및 설정 (화성 중심) ──────────────────────────────────
G = 6.674e-11
MARS_M = 6.39e23  # 화성 질량 (kg)
MARS_R = 3389.5   # 화성 반지름 (km)

def calculate_orbit(a_km, e):
    a = a_km * 1000
    T = 2 * np.pi * np.sqrt(a**3 / (G * MARS_M))
    rp = a * (1 - e)
    ra = a * (1 + e)
    vp = np.sqrt(G * MARS_M * (2/rp - 1/a))
    va = np.sqrt(G * MARS_M * (2/ra - 1/a))
    return {
        "T_h": T/3600, 
        "rp_km": rp/1000, 
        "ra_km": ra/1000, 
        "vp": vp, 
        "va": va
    }

def kepler_animation(a_km, e):
    a = a_km * 1000
    c = a * e
    N = 40 
    M_mean = np.linspace(0, 2*np.pi, N, endpoint=False)
    E_arr = M_mean.copy()
    for _ in range(15):
        E_arr -= (E_arr - e * np.sin(E_arr) - M_mean) / (1 - e * np.cos(E_arr))
    
    true_theta = 2 * np.arctan2(np.sqrt(1+e)*np.sin(E_arr/2), np.sqrt(1-e)*np.cos(E_arr/2))
    r_arr = a * (1 - e**2) / (1 + e * np.cos(true_theta))
    px = r_arr * np.cos(true_theta) / 1000 - c/1000
    py = r_arr * np.sin(true_theta) / 1000

    frames = []
    for i in range(N):
        altitude = r_arr[i]/1000 - MARS_R
        beam_color = "rgba(255, 255, 255, 0.3)" if altitude < 500 else "rgba(0,0,0,0)"
        frames.append(go.Frame(
            data=[
                go.Scatter(x=[px[i]], y=[py[i]], mode="markers", marker=dict(size=12, color="#38bdf8")),
                go.Scatter(x=[px[i], 0], y=[py[i], 0], mode="lines", 
                           line=dict(color=beam_color, width=1, dash="dot"))
            ],
            name=str(i)
        ))

    fig = go.Figure(
        data=[
            go.Scatter(x=[0], y=[0], mode="markers", 
                       marker=dict(size=40, color="#c1440e", line=dict(color="white", width=1))),
            frames[0].data[0],
            frames[0].data[1]
        ],
        layout=go.Layout(
            template="plotly_dark", paper_bgcolor="#0f172a", plot_bgcolor="#0f172a",
            xaxis=dict(range=[-a_km*2.5, a_km*2.5], visible=False),
            yaxis=dict(range=[-a_km*2.5, a_km*2.5], scaleanchor="x", visible=False),
            margin=dict(l=0, r=0, t=0, b=0),
            updatemenus=[dict(type="buttons", buttons=[
                dict(label="▶ 탐사 시작", method="animate", args=[None, {"frame": {"duration": 50}, "fromcurrent": True}])
            ])]
        ),
        frames=frames
    )
    return fig

def run_sim():
    st.set_page_config(page_title="KASA 화성 궤도 설계", layout="wide")
    st.markdown("<style>.stMetric { background: #1e293b; border-radius: 10px; padding: 10px; border: 1px solid #334155; } .stSlider > label { color: #38bdf8 !important; font-weight: bold; }</style>", unsafe_allow_html=True)
    st.title("🚀 KASA 화성 탐사선 궤도 설계 시스템")
    st.caption("대한민국 우주항공청(KASA) 수석연구원 미션 전용 시뮬레이터")

    with st.sidebar:
        st.header("🛰️ 설계 파라미터")
        a_km = st.slider("궤도 장반경 (a) [km]", 4000, 25000, 10000)
        e = st.slider("이심률 (e)", 0.0, 0.9, 0.4)
        orbit = calculate_orbit(a_km, e)
        rp_alt = orbit["rp_km"] - MARS_R
        photo_score = max(0, 100 - abs(rp_alt - 350) / 3) if rp_alt > 100 else 0
        comm_score = min(100, (orbit["ra_km"] / 20000) * 100)
        st.markdown("---")
        st.subheader("🎯 미션 적합도 평가")
        st.write(f"📷 촬영 정밀도: {photo_score:.1f}%")
        st.progress(int(photo_score)/100)
        st.write(f"📡 통신 커버리지: {comm_score:.1f}%")
        st.progress(int(comm_score)/100)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.plotly_chart(kepler_animation(a_km, e), use_container_width=True)
    with col2:
        st.markdown("### 📊 실시간 궤도 제원")
        st.metric("근일점 고도", f"{rp_alt:.1f} km")
        st.metric("원일점 고도", f"{orbit['ra_km'] - MARS_R:.1f} km")
        st.metric("공전 주기", f"{orbit['T_h']:.2f} 시간")
        st.metric("근일점 속도", f"{orbit['vp']:.0f} m/s")
        if rp_alt < 200: st.error("⚠️ 경고: 고도 낮음")
        elif photo_score > 90: st.success("✅ 최적 궤도")

if __name__ == "__main__":
    run_sim()
