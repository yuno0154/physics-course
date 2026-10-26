import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
#  수행평가 자료 앱
#  실제 인공위성 궤도 데이터 분석 및 정량적 검증 (서술형·개별)
#
#  설계 원칙
#  - 위성 자료(고도, 주기, 속력)는 공개된 관측·운용 자료를 상수로 저장한다.
#    v = √(GM/r) 같은 이론식으로 만들지 않는다. (학생이 검증해야 할 관계를
#    앱이 미리 써서 데이터를 만들면 검증이 순환 논리가 되기 때문)
#  - 앱은 '단위 변환'까지만 보여 준다. v²r, T²/r³, 지구 질량 등
#    평가 요소에 해당하는 계산·해석은 앱에 넣지 않는다.
# ============================================================

try:
    st.set_page_config(page_title="인공위성 궤도 데이터", page_icon="🛰️", layout="wide")
except Exception:
    pass

R_EARTH_KM = 6371  # 지구 반지름 (km) — 문항과 같은 값

# ---------- 위성 자료 (공개 자료 기준 근사값) ----------
# period: (시, 분, 초)
# speed_kms: 평균 공전 속력 (km/s)
# ※ 위성 고도는 시기에 따라 조금씩 변하므로 출제 전에 최신 자료로 확인할 것
SATELLITES = {
    "ISS": {
        "name": "국제우주정거장 (ISS)",
        "orbit": "저궤도 (LEO)",
        "altitude_km": 420,
        "period": (0, 92, 54),     # 약 92.9분
        "speed_kms": 7.66,
        "color": "#E4572E",
        "info": "우주인이 머무르며 실험을 수행하는 다국적 우주정거장. 하루에 지구를 약 15.5바퀴 돈다.",
        "source": "NASA ISS Facts and Figures",
    },
    "Hubble": {
        "name": "허블 우주 망원경",
        "orbit": "저궤도 (LEO)",
        "altitude_km": 520,
        "period": (0, 94, 53),     # 약 94.9분
        "speed_kms": 7.61,
        "color": "#F3A712",
        "info": "1990년에 발사된 우주 망원경. 대기의 방해 없이 우주를 관측한다. 고도가 조금씩 낮아지고 있다.",
        "source": "NASA Hubble Space Telescope",
    },
    "Landsat 9": {
        "name": "랜드샛 9호 (Landsat 9)",
        "orbit": "태양동기궤도 (SSO)",
        "altitude_km": 705,
        "period": (0, 98, 54),     # 약 98.9분
        "speed_kms": 7.49,
        "color": "#29BF12",
        "info": "지표면의 자원과 환경 변화를 촬영하는 지구 관측 위성. 16일마다 같은 지역 위를 다시 지난다.",
        "source": "USGS / NASA Landsat 9",
    },
    "GPS": {
        "name": "GPS 위성",
        "orbit": "중궤도 (MEO)",
        "altitude_km": 20200,
        "period": (11, 58, 0),
        "speed_kms": 3.88,
        "color": "#4B8BBE",
        "info": "위치 정보를 알려 주는 항법 위성. 하루에 지구를 약 2바퀴 돈다.",
        "source": "GPS.gov Space Segment",
    },
    "천리안 2A호": {
        "name": "천리안 2A호 (GK-2A)",
        "orbit": "정지궤도 (GEO)",
        "altitude_km": 35786,
        "period": (23, 56, 4),
        "speed_kms": 3.07,
        "color": "#A23B72",
        "info": "한국의 기상 관측 위성. 적도 상공에서 지구 자전과 같은 주기로 돌아 늘 한반도 쪽을 바라본다.",
        "source": "국가기상위성센터 / 한국항공우주연구원",
    },
}

SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(x, sig=3):
    """6791000 -> '6.79 × 10⁶'"""
    exp = int(math.floor(math.log10(abs(x))))
    man = round(x / 10**exp, sig - 1)
    if man >= 10:
        man /= 10
        exp += 1
    return f"{man:.{sig-1}f} × 10{str(exp).translate(SUP)}"


def sci_tex(x, sig=3):
    exp = int(math.floor(math.log10(abs(x))))
    man = round(x / 10**exp, sig - 1)
    if man >= 10:
        man /= 10
        exp += 1
    return rf"{man:.{sig-1}f}\times10^{{{exp}}}"


def n(x):
    """LaTeX용 천 단위 쉼표 (6{,}371)"""
    return f"{x:,}".replace(",", "{,}")


def period_text(p):
    h, m, s = p
    parts = []
    if h:
        parts.append(f"{h}시간")
    if m:
        parts.append(f"{m}분")
    if s:
        parts.append(f"{s}초")
    return " ".join(parts)


def derived(sat):
    h, m, s = sat["period"]
    r_km = R_EARTH_KM + sat["altitude_km"]
    T_s = h * 3600 + m * 60 + s
    return dict(r_km=r_km, r_m=r_km * 1000, T_s=T_s, v_ms=sat["speed_kms"] * 1000)


# ---------- 헤더 ----------
st.title("🛰️ 실제 인공위성 궤도 데이터")
st.markdown(
    "**[수행평가 자료]** 실제 인공위성 궤도 데이터 분석 및 정량적 검증 · 서술형 · 개별  \n"
    "실제로 운용 중인 인공위성 5개의 궤도 자료입니다. **③ 단위 변환** 탭에서 SI 단위로 바꾼 값을 확인하고, "
    "**④ 데이터 옮기기** 탭의 값을 평가지의 데이터 정리표에 옮겨 적으세요."
)

# ---------- 상단 제어 패널 ----------
with st.container(border=True):
    c_sel, c_speed, c_frames = st.columns([2, 1, 1])
    with c_sel:
        key = st.selectbox(
            "🛰️ 관찰 및 분석할 위성 선택",
            list(SATELLITES.keys()),
            format_func=lambda k: SATELLITES[k]["name"],
            help="원하는 위성을 선택하면 궤도 애니메이션과 단위 변환 과정이 실시간으로 갱신됩니다."
        )
        sat = SATELLITES[key]
        d = derived(sat)
    with c_speed:
        frame_dur = st.select_slider(
            "⚡ 애니메이션 속도",
            options=[30, 50, 80, 120, 200],
            value=80,
            format_func=lambda x: {30: "매우 빠름", 50: "빠름", 80: "보통", 120: "느림", 200: "매우 느림"}[x],
        )
    with c_frames:
        n_frames = st.slider("🎬 프레임 수 (부드러움)", 30, 120, 60, step=10)

    st.info(f"ℹ️ **{sat['name']} ({sat['orbit']})**: {sat['info']} *(출처: {sat['source']})*")

tab1, tab2, tab3, tab4 = st.tabs(
    ["① 궤도 애니메이션", "② 위성 자료 (원자료)", "③ 단위 변환", "④ 데이터 옮기기"]
)

# ============================================================
# TAB 1: 궤도 애니메이션 (관찰용)
# ============================================================
with tab1:
    st.markdown(f"### {sat['name']} 궤도 운동")
    c1, c2, c3 = st.columns(3)
    c1.metric("고도 h", f"{sat['altitude_km']:,} km", sat["orbit"])
    c2.metric("공전 주기 T", period_text(sat["period"]))
    c3.metric("공전 속력 v", f"{sat['speed_kms']} km/s")

    r_norm = d["r_km"] / R_EARTH_KM
    th_e = np.linspace(0, 2 * np.pi, 100)
    th_o = np.linspace(0, 2 * np.pi, 200)

    def traces(ang):
        sx, sy = r_norm * np.cos(ang), r_norm * np.sin(ang)
        L = r_norm * 0.25
        return [
            go.Scatter(x=np.cos(th_e), y=np.sin(th_e), mode="lines", name="지구",
                       line=dict(color="#1E90FF", width=2), fill="toself",
                       fillcolor="rgba(30,144,255,0.4)", hoverinfo="skip"),
            go.Scatter(x=r_norm * np.cos(th_o), y=r_norm * np.sin(th_o), mode="lines",
                       name="궤도", line=dict(color="rgba(200,200,200,0.4)", width=1.5, dash="dash"),
                       hoverinfo="skip"),
            go.Scatter(x=[sx], y=[sy], mode="markers", name=sat["name"],
                       marker=dict(size=16, color=sat["color"], line=dict(color="white", width=2))),
            go.Scatter(x=[sx, sx - np.sin(ang) * L], y=[sy, sy + np.cos(ang) * L],
                       mode="lines", name="속도 방향", line=dict(color="#00FF7F", width=4)),
            go.Scatter(x=[sx, sx - np.cos(ang) * L * 0.7], y=[sy, sy - np.sin(ang) * L * 0.7],
                       mode="lines", name="지구가 당기는 힘의 방향", line=dict(color="#FFA500", width=4)),
        ]

    frames, steps = [], []
    for i in range(n_frames):
        ang = 2 * np.pi * i / n_frames
        t_el = i / n_frames * d["T_s"]
        t_str = f"{t_el/60:.1f} 분" if d["T_s"] < 3600 else f"{t_el/3600:.2f} 시간"
        frames.append(go.Frame(
            data=traces(ang), name=f"f{i}",
            layout=go.Layout(annotations=[dict(
                x=0.02, y=0.98, xref="paper", yref="paper", showarrow=False, align="left",
                text=f"<b>{sat['name']}</b><br>경과: {t_str}<br>진행: {i/n_frames*100:.0f}%",
                bgcolor="rgba(20,20,30,0.85)", bordercolor=sat["color"], borderwidth=2,
                font=dict(family="monospace", size=12, color="white"))]),
        ))
        steps.append(dict(args=[[f"f{i}"], dict(frame=dict(duration=frame_dur, redraw=True),
                                                mode="immediate")],
                          label=f"{int(i/n_frames*100)}%", method="animate"))

    lim = r_norm * 1.35
    fig = go.Figure(data=traces(0), frames=frames)
    fig.update_layout(
        plot_bgcolor="#0a0a14", paper_bgcolor="#0a0a14", font=dict(color="white"), height=620,
        xaxis=dict(range=[-lim, lim], title="X (지구 반지름 단위)", gridcolor="rgba(100,100,100,0.2)"),
        yaxis=dict(range=[-lim, lim], title="Y (지구 반지름 단위)", scaleanchor="x", scaleratio=1,
                   gridcolor="rgba(100,100,100,0.2)"),
        updatemenus=[dict(type="buttons", direction="left", x=0.05, y=-0.07, showactive=False,
                          bgcolor="#1a1a2e", buttons=[
                              dict(label="▶ 재생", method="animate",
                                   args=[None, dict(frame=dict(duration=frame_dur, redraw=True),
                                                    fromcurrent=True, mode="immediate")]),
                              dict(label="⏸ 정지", method="animate",
                                   args=[[None], dict(frame=dict(duration=0, redraw=False),
                                                      mode="immediate")])])],
        sliders=[dict(active=0, currentvalue=dict(prefix="진행: "), pad=dict(b=10, t=40),
                      len=0.85, x=0.1, y=-0.07, steps=steps)],
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### 🌍 5개 위성의 궤도 크기 비교 (실제 비율)")
    fig_sc = go.Figure()
    fig_sc.add_trace(go.Scatter(x=R_EARTH_KM / 1000 * np.cos(th_e), y=R_EARTH_KM / 1000 * np.sin(th_e),
                                fill="toself", fillcolor="rgba(30,144,255,0.5)",
                                line=dict(color="#1E90FF", width=2), name="지구"))
    for s in SATELLITES.values():
        rk = (R_EARTH_KM + s["altitude_km"]) / 1000
        fig_sc.add_trace(go.Scatter(x=rk * np.cos(th_e), y=rk * np.sin(th_e), mode="lines",
                                    line=dict(color=s["color"], width=2, dash="dash"), name=s["name"]))
    mr = (R_EARTH_KM + 35786) / 1000 * 1.15
    fig_sc.update_layout(
        plot_bgcolor="#0a0a14", paper_bgcolor="#0a0a14", font=dict(color="white"), height=520,
        xaxis=dict(range=[-mr, mr], title="X (× 1000 km)", gridcolor="rgba(100,100,100,0.2)"),
        yaxis=dict(range=[-mr, mr], title="Y (× 1000 km)", scaleanchor="x", scaleratio=1,
                   gridcolor="rgba(100,100,100,0.2)"),
    )
    st.plotly_chart(fig_sc, width="stretch")

# ============================================================
# TAB 2: 원자료 (공개 자료의 단위 그대로)
# ============================================================
with tab2:
    st.markdown("### 📡 위성 궤도 원자료")
    st.caption("공개 자료에 실린 단위 그대로입니다. 궤도는 원 궤도로 가정합니다.")
    raw = pd.DataFrame([{
        "위성": s["name"],
        "궤도 종류": s["orbit"],
        "지표면으로부터의 고도 h": f"{s['altitude_km']:,} km",
        "공전 주기 T": period_text(s["period"]),
        "공전 속력 v": f"{s['speed_kms']} km/s",
        "자료 출처": s["source"],
    } for s in SATELLITES.values()])
    st.dataframe(raw, width="stretch", hide_index=True)
    st.info(f"지구 반지름 R = {R_EARTH_KM:,} km  |  "
            "위성 고도는 시기에 따라 조금씩 달라지므로 값은 근사값입니다.")

# ============================================================
# TAB 3: 단위 변환 (과정 표시)
# ============================================================
with tab3:
    st.markdown(f"### 🔁 단위 변환 과정 — {sat['name']}")
    st.caption("상단에서 위성을 바꾸면 그 위성의 변환 과정이 나타납니다. 값은 유효숫자 3자리로 반올림합니다.")

    h, m, s_ = sat["period"]

    st.markdown("**① 궤도 반지름 r** — 지구 중심에서 위성까지의 거리이므로 지구 반지름에 고도를 더합니다.")
    st.latex(
        rf"r = R + h = {n(R_EARTH_KM)}\,\text{{km}} + {n(sat['altitude_km'])}\,\text{{km}}"
        rf" = {n(d['r_km'])}\,\text{{km}} = {n(d['r_km'])}\times10^{{3}}\,\text{{m}}"
        rf" \approx {sci_tex(d['r_m'])}\,\text{{m}}"
    )

    st.markdown("**② 공전 주기 T** — 1시간 = 3600 s, 1분 = 60 s")
    terms = []
    if h:
        terms.append(rf"{h}\times3600\,\text{{s}}")
    if m:
        terms.append(rf"{m}\times60\,\text{{s}}")
    if s_:
        terms.append(rf"{s_}\,\text{{s}}")
    st.latex(
        rf"T = \text{{{period_text(sat['period'])}}} = " + " + ".join(terms)
        + rf" = {n(d['T_s'])}\,\text{{s}} \approx {sci_tex(d['T_s'])}\,\text{{s}}"
    )

    st.markdown("**③ 공전 속력 v** — 1 km = 1000 m")
    st.latex(
        rf"v = {sat['speed_kms']}\,\text{{km/s}} = {sat['speed_kms']}\times10^{{3}}\,\text{{m/s}}"
    )

    st.success(
        f"**SI 단위 결과:**  r = {sci(d['r_m'])} m  |  T = {sci(d['T_s'])} s  |  v = {sci(d['v_ms'])} m/s"
    )

# ============================================================
# TAB 4: 데이터 옮기기 (SI 단위 결과표)
# ============================================================
with tab4:
    st.markdown("### 📝 평가지에 옮겨 적을 값 (SI 단위, 유효숫자 3자리)")
    rows = []
    for s in SATELLITES.values():
        q = derived(s)
        rows.append({
            "위성": s["name"],
            "궤도 반지름 r (m)": sci(q["r_m"]),
            "공전 주기 T (s)": sci(q["T_s"]),
            "공전 속력 v (m/s)": sci(q["v_ms"]),
        })
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    st.warning(
        "이 표의 값을 평가지 데이터 정리표의 r, T, v 칸에 옮겨 적으세요.  \n"
        "**v²r, T²/r³ 칸은 직접 계산하여 채웁니다.** (공학용 계산기 사용 가능)"
    )

st.markdown("---")
st.caption(f"지구 반지름 R = {R_EARTH_KM:,} km  |  만유인력 상수 G = 6.67 × 10⁻¹¹ N·m²/kg²")
