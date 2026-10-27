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
#    v = √(GM/r) 같은 이론식으로 역산하지 않는다.
#  - 단위 변환 과정과 케플러 제3법칙 상수 T²/r³ 데이터를 명확하게 제시하여
#    조화의 법칙 성립을 직접 정량적으로 검증할 수 있도록 한다.
#    (※ v²r 항목은 생략하고 T²/r³ 열을 데이터 표에 직접 제공)
# ============================================================

try:
    st.set_page_config(page_title="인공위성 궤도 데이터", page_icon="🛰️", layout="wide")
except Exception:
    pass

R_EARTH_KM = 6371  # 지구 반지름 (km) — 문항과 같은 값

# ---------- 위성 자료 (공개 자료 기준 근사값) ----------
# period: (시, 분, 초)
# speed_kms: 평균 공전 속력 (km/s)
# 시인성을 위해 어두운 배경에서도 뚜렷하게 식별 가능한 고대비 색상 적용
SATELLITES = {
    "ISS": {
        "name": "국제우주정거장 (ISS)",
        "orbit": "저궤도 (LEO)",
        "altitude_km": 420,
        "period": (0, 92, 54),     # 약 92.9분
        "speed_kms": 7.66,
        "color": "#FF6B4A",        # 고시인성 코랄 오렌지
        "info": "우주인이 머무르며 실험을 수행하는 다국적 우주정거장. 하루에 지구를 약 15.5바퀴 돈다.",
        "source": "NASA ISS Facts and Figures",
    },
    "GPS": {
        "name": "GPS 위성",
        "orbit": "중궤도 (MEO)",
        "altitude_km": 20200,
        "period": (11, 58, 0),
        "speed_kms": 3.88,
        "color": "#818CF8",        # 지구의 파란색과 명확히 구분되는 밝은 라벤더/인디고
        "info": "위치 정보를 알려 주는 항법 위성. 하루에 지구를 약 2바퀴 돈다.",
        "source": "GPS.gov Space Segment",
    },
    "천리안 2A호": {
        "name": "천리안 2A호 (GK-2A)",
        "orbit": "정지궤도 (GEO)",
        "altitude_km": 35786,
        "period": (23, 56, 4),
        "speed_kms": 3.07,
        "color": "#F43F5E",        # 고시인성 로즈 핑크
        "info": "한국의 기상 관측 위성. 적도 상공에서 지구 자전과 같은 주기로 돌아 늘 한반도 쪽을 바라본다.",
        "source": "국가기상위성센터 / 한국항공우주연구원",
    },
}

SUP = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def sci(x, sig=3):
    """6791000 -> '6.79 × 10⁶', 9.91e-14 -> '9.91 × 10⁻¹⁴'"""
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
    r_m = r_km * 1000
    v_ms = sat["speed_kms"] * 1000
    t2_r3 = (T_s ** 2) / (r_m ** 3)
    return dict(r_km=r_km, r_m=r_m, T_s=T_s, v_ms=v_ms, t2_r3=t2_r3)


# ---------- 헤더 ----------
st.title("🛰️ 실제 인공위성 궤도 데이터")
st.markdown(
    "**[수행평가 자료]** 실제 인공위성 궤도 데이터 분석 및 정량적 검증 · 서술형 · 개별  \n"
    "저궤도·중궤도·정지궤도를 대표하는 실제 인공위성 3개의 궤도 자료입니다. "
    "**③ 단위 변환** 탭에서 SI 단위 변환 및 케플러 비율 계산 과정을 확인하고, "
    "**④ 데이터 옮기기** 탭의 값($r, T, v, T^2/r^3$)을 평가지의 데이터 정리표에 옮겨 적으세요."
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
                       line=dict(color="#38BDF8", width=2.5), fill="toself",
                       fillcolor="rgba(56, 189, 248, 0.35)", hoverinfo="skip"),
            go.Scatter(x=r_norm * np.cos(th_o), y=r_norm * np.sin(th_o), mode="lines",
                       name="궤도", line=dict(color="rgba(241, 245, 249, 0.75)", width=2, dash="dash"),
                       hoverinfo="skip"),
            go.Scatter(x=[sx], y=[sy], mode="markers", name=sat["name"],
                       marker=dict(size=18, color=sat["color"], line=dict(color="#ffffff", width=2.5))),
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
                bgcolor="rgba(15, 23, 42, 0.9)", bordercolor=sat["color"], borderwidth=2,
                font=dict(family="sans-serif", size=13, color="#ffffff"))]),
        ))
        steps.append(dict(args=[[f"f{i}"], dict(frame=dict(duration=frame_dur, redraw=True),
                                                mode="immediate")],
                          label=f"{int(i/n_frames*100)}%", method="animate"))

    lim = r_norm * 1.35
    fig = go.Figure(data=traces(0), frames=frames)
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0c1021",
        paper_bgcolor="#0c1021",
        font=dict(color="#ffffff", family="sans-serif"),
        height=620,
        legend=dict(
            font=dict(color="#ffffff", size=14, family="sans-serif"),
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.3)",
            borderwidth=1,
            x=0.98,
            xanchor="right",
            y=0.98,
            yanchor="top",
        ),
        xaxis=dict(
            range=[-lim, lim],
            title=dict(text="X (지구 반지름 단위)", font=dict(color="#ffffff", size=13)),
            tickfont=dict(color="#cbd5e1", size=11),
            gridcolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
        ),
        yaxis=dict(
            range=[-lim, lim],
            title=dict(text="Y (지구 반지름 단위)", font=dict(color="#ffffff", size=13)),
            tickfont=dict(color="#cbd5e1", size=11),
            scaleanchor="x",
            scaleratio=1,
            gridcolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
        ),
        updatemenus=[dict(
            type="buttons",
            direction="left",
            x=0.05,
            y=-0.08,
            showactive=False,
            bgcolor="#1e293b",
            font=dict(color="#ffffff"),
            bordercolor="rgba(255, 255, 255, 0.25)",
            borderwidth=1,
            buttons=[
                dict(label="▶ 재생", method="animate",
                     args=[None, dict(frame=dict(duration=frame_dur, redraw=True),
                                      fromcurrent=True, mode="immediate")]),
                dict(label="⏸ 정지", method="animate",
                     args=[[None], dict(frame=dict(duration=0, redraw=False),
                                        mode="immediate")])]
        )],
        sliders=[dict(
            active=0,
            currentvalue=dict(prefix="진행: ", font=dict(color="#ffffff", size=13)),
            font=dict(color="#cbd5e1"),
            pad=dict(b=10, t=40),
            len=0.85,
            x=0.1,
            y=-0.08,
            steps=steps
        )],
    )
    st.plotly_chart(fig, width="stretch")

    st.markdown("#### 🌍 3개 위성의 궤도 크기 비교 (실제 비율)")
    fig_sc = go.Figure()
    fig_sc.add_trace(go.Scatter(x=R_EARTH_KM / 1000 * np.cos(th_e), y=R_EARTH_KM / 1000 * np.sin(th_e),
                                fill="toself", fillcolor="rgba(56, 189, 248, 0.35)",
                                line=dict(color="#38BDF8", width=2.5), name="지구"))
    for s in SATELLITES.values():
        rk = (R_EARTH_KM + s["altitude_km"]) / 1000
        fig_sc.add_trace(go.Scatter(x=rk * np.cos(th_e), y=rk * np.sin(th_e), mode="lines",
                                    line=dict(color=s["color"], width=2.5, dash="dash"), name=s["name"]))
    mr = (R_EARTH_KM + 35786) / 1000 * 1.15
    fig_sc.update_layout(
        template="plotly_dark",
        plot_bgcolor="#0c1021",
        paper_bgcolor="#0c1021",
        font=dict(color="#ffffff", family="sans-serif"),
        height=520,
        legend=dict(
            font=dict(color="#ffffff", size=13, family="sans-serif"),
            bgcolor="rgba(15, 23, 42, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.3)",
            borderwidth=1,
            x=0.98,
            xanchor="right",
            y=0.98,
            yanchor="top",
        ),
        xaxis=dict(
            range=[-mr, mr],
            title=dict(text="X (× 1000 km)", font=dict(color="#ffffff", size=13)),
            tickfont=dict(color="#cbd5e1", size=11),
            gridcolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
        ),
        yaxis=dict(
            range=[-mr, mr],
            title=dict(text="Y (× 1000 km)", font=dict(color="#ffffff", size=13)),
            tickfont=dict(color="#cbd5e1", size=11),
            scaleanchor="x",
            scaleratio=1,
            gridcolor="rgba(255, 255, 255, 0.12)",
            zerolinecolor="rgba(255, 255, 255, 0.2)",
        ),
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
    st.markdown(f"### 🔁 단위 변환 및 케플러 비율 계산 — {sat['name']}")
    st.caption("상단에서 위성을 바꾸면 해당 위성의 변환 및 계산 과정이 실시간으로 갱신됩니다. (유효숫자 3자리)")

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

    st.markdown("**④ 케플러 제3법칙 비율 ($T^2/r^3$) 계산** — 공전 주기 제곱($T^2$)을 궤도 반지름 세제곱($r^3$)으로 나눕니다.")
    st.latex(
        rf"\frac{{T^2}}{{r^3}} = \frac{{({n(d['T_s'])}\,\text{{s}})^2}}{{({n(d['r_m'])}\,\text{{m}})^3}}"
        rf" = \frac{{{sci_tex(d['T_s']**2)}\,\text{{s}}^2}}{{{sci_tex(d['r_m']**3)}\,\text{{m}}^3}}"
        rf" \approx {sci_tex(d['t2_r3'])}\,\text{{s}}^2/\text{{m}}^3"
    )

    st.success(
        f"**SI 단위 및 계산 결과:**  "
        f"r = {sci(d['r_m'])} m  |  T = {sci(d['T_s'])} s  |  "
        f"v = {sci(d['v_ms'])} m/s  |  T²/r³ = {sci(d['t2_r3'])} s²/m³"
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
            "T²/r³ (s²/m³)": sci(q["t2_r3"]),
        })
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    st.info(
        "💡 **평가지 데이터 정리표 작성 안내:**  \n"
        "위 표의 값($r, T, v, T^2/r^3$)을 평가지의 데이터 정리표 칸에 옮겨 적으세요.  \n"
        "• 세 위성 모두 **$T^2/r^3 \\approx 9.9 \\times 10^{-14}\\,\\text{s}^2/\\text{m}^3$**으로 거의 일정한 값을 가집니다.  \n"
        "• 이를 통해 지구 주위를 공전하는 인공위성의 운동에서도 **케플러 제3법칙(조화의 법칙, $T^2 \\propto r^3$)**이 정확하게 성립함을 확인할 수 있습니다."
    )

st.markdown("---")
st.caption(f"지구 반지름 R = {R_EARTH_KM:,} km  |  만유인력 상수 G = 6.67 × 10⁻¹¹ N·m²/kg²")
