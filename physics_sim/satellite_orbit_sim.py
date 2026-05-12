import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# ============================================================
#  인공위성 궤도 반지름과 공전 속도 시뮬레이션
#  - 물리학습 지원 포털 (physics-course)
# ============================================================

st.title("🛰️ 수행평가 : 포물선 운동과 인공위성 궤도의 역학적 연결 탐구")
st.markdown("""
**[수행평가 안내]**
- **평가 요소**: 궤도 반지름과 속도 해석
- **평가 방식**: 시뮬레이션 실험, 서술형, 개별

지구 주위를 공전하는 인공위성의 **궤도 반지름(r)** 을 변화시키며 
**공전 속도(v)** 가 어떻게 변화하는지 정밀 분석합니다.  
시뮬레이션 결과를 바탕으로 **공전 속도 식 v = √(GM/r)** 을 스스로 유도해 보세요!
""")

# --- 물리 상수 ---
G = 6.674e-11          # 만유인력 상수 (N·m²/kg²)
M_EARTH = 5.972e24     # 지구 질량 (kg)
R_EARTH = 6.371e6      # 지구 반지름 (m)
GEO_R = 4.2164e7       # 정지궤도 반지름 (m)

# ------------------------------------------------------------
# ⚙️ 실험 조건 설정
# ------------------------------------------------------------
with st.container(border=True):
    st.markdown("### ⚙️ 실험 조건 설정")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        r_mult = st.number_input(
            "궤도 반지름 r (×Rₑ) [1.0 ~ 8.0]",
            min_value=1.0, max_value=8.0, value=1.0, step=0.1,
            help="지구 반지름(Rₑ ≈ 6,371 km)의 배수로 입력합니다.")
    with c2:
        preset = st.selectbox(
            "🎯 대표 궤도 프리셋",
            ["사용자 지정", "지표면(r=Rₑ)", "저궤도 LEO(r≈1.1Rₑ)",
             "중궤도 MEO(r≈3.1Rₑ)", "정지궤도 GEO(r≈6.6Rₑ)"],
            index=0)
    with c3:
        speed_mode = st.radio(
            "🎮 애니메이션 속도",
            options=["느림", "보통", "빠름"], index=1, horizontal=True)
    with c4:
        show_force = st.checkbox("🧲 만유인력 벡터 표시", value=True)

# 프리셋 적용
if preset == "지표면(r=Rₑ)":
    r_mult = 1.0
elif preset == "저궤도 LEO(r≈1.1Rₑ)":
    r_mult = 1.1
elif preset == "중궤도 MEO(r≈3.1Rₑ)":
    r_mult = 3.1
elif preset == "정지궤도 GEO(r≈6.6Rₑ)":
    r_mult = GEO_R / R_EARTH

r = r_mult * R_EARTH                  # 실제 궤도 반지름 (m)
v = np.sqrt(G * M_EARTH / r)          # 공전 속도 (m/s)
T = 2 * np.pi * r / v                 # 공전 주기 (s)
a_c = v ** 2 / r                      # 구심 가속도 (m/s²)
F_grav = G * M_EARTH / (r ** 2)       # 단위 질량당 만유인력 (N/kg)

# ------------------------------------------------------------
# 📊 주요 시뮬레이션 결과 요약
# ------------------------------------------------------------
st.divider()
st.markdown("### 📊 주요 시뮬레이션 결과 요약")
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("궤도 반지름 r", f"{r/1e6:.2f} ×10⁶ m")
with m2:
    st.metric("공전 속도 v", f"{v:.1f} m/s", f"{v/1000:.3f} km/s")
with m3:
    st.metric("공전 주기 T", f"{T/60:.2f} 분",
              f"{T/3600:.3f} 시간")
with m4:
    st.metric("구심 가속도 aₙ", f"{a_c:.3f} m/s²")

# 제1 우주 속도와의 비교
v1 = np.sqrt(G * M_EARTH / R_EARTH)
ratio = v / v1
st.info(
    f"💡 **제1 우주 속도(v₁ = √(GM/Rₑ)) ≈ {v1:.1f} m/s** "
    f"대비 현재 위성 속도의 비율: **{ratio:.3f}** "
    f"(거리비 r/Rₑ = {r_mult:.2f})")

# ------------------------------------------------------------
# 🌍 궤도 운동 시각화 (애니메이션)
# ------------------------------------------------------------
st.divider()
st.markdown("### 🌍 궤도 운동 시각화")

# 정지 궤도(원) 좌표
theta = np.linspace(0, 2 * np.pi, 200)
orbit_x = r_mult * np.cos(theta)
orbit_y = r_mult * np.sin(theta)

# 애니메이션 프레임
n_frames = 60
frame_step = {"느림": 80, "보통": 40, "빠름": 20}[speed_mode]
frames = []
for k in range(n_frames):
    ang = 2 * np.pi * k / n_frames
    sx, sy = r_mult * np.cos(ang), r_mult * np.sin(ang)
    # 속도 벡터(접선 방향)
    vx_dir, vy_dir = -np.sin(ang), np.cos(ang)
    # 만유인력 벡터(중심 방향)
    fx_dir, fy_dir = -np.cos(ang), -np.sin(ang)
    vec_len = 0.35 * r_mult

    data = [
        go.Scatter(x=orbit_x, y=orbit_y, mode="lines",
                   line=dict(color="lightgray", dash="dot"),
                   name="궤도", showlegend=False),
        go.Scatter(x=[0], y=[0], mode="markers",
                   marker=dict(size=28, color="royalblue",
                               line=dict(color="darkblue", width=2)),
                   name="지구", showlegend=False),
        go.Scatter(x=[sx], y=[sy], mode="markers+text",
                   marker=dict(size=14, color="crimson",
                               symbol="diamond"),
                   text=["🛰️"], textposition="top center",
                   name="위성", showlegend=False),
        # 속도 벡터 (녹색)
        go.Scatter(x=[sx, sx + vec_len * vx_dir],
                   y=[sy, sy + vec_len * vy_dir],
                   mode="lines+markers",
                   line=dict(color="green", width=3),
                   marker=dict(size=[0, 8], symbol="arrow-up",
                               angleref="previous"),
                   name="속도 v", showlegend=(k == 0)),
    ]
    if show_force:
        data.append(
            go.Scatter(x=[sx, sx + vec_len * 0.6 * fx_dir],
                       y=[sy, sy + vec_len * 0.6 * fy_dir],
                       mode="lines+markers",
                       line=dict(color="orange", width=3),
                       marker=dict(size=[0, 8], symbol="arrow-up",
                                   angleref="previous"),
                       name="만유인력 F",
                       showlegend=(k == 0)))
    frames.append(go.Frame(data=data, name=str(k)))

# 초기 프레임
init_data = frames[0].data
axis_lim = max(1.3, r_mult * 1.3)

fig = go.Figure(
    data=init_data,
    frames=frames,
    layout=go.Layout(
        xaxis=dict(range=[-axis_lim, axis_lim], zeroline=False,
                   showgrid=True, gridcolor="rgba(200,200,200,0.3)",
                   title="x (×Rₑ)"),
        yaxis=dict(range=[-axis_lim, axis_lim], zeroline=False,
                   showgrid=True, gridcolor="rgba(200,200,200,0.3)",
                   scaleanchor="x", scaleratio=1,
                   title="y (×Rₑ)"),
        height=520,
        margin=dict(l=20, r=20, t=40, b=20),
        title=f"r = {r_mult:.2f} Rₑ,  v = {v:.1f} m/s,  T = {T/60:.1f} 분",
        updatemenus=[dict(
            type="buttons", showactive=False, y=1.12, x=0.05,
            buttons=[
                dict(label="▶ Play", method="animate",
                     args=[None, {"frame": {"duration": frame_step,
                                            "redraw": True},
                                  "fromcurrent": True,
                                  "transition": {"duration": 0}}]),
                dict(label="⏸ Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0,
                                              "redraw": False},
                                    "mode": "immediate"}])])]))
st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------------------------
# 📈 r-v 관계 그래프 (이론값 vs 측정값)
# ------------------------------------------------------------
st.divider()
st.markdown("### 📈 궤도 반지름 - 공전 속도 관계")

r_arr = np.linspace(1.0, 8.0, 200) * R_EARTH
v_arr = np.sqrt(G * M_EARTH / r_arr)

# 대표 측정점(시뮬레이션 데이터)
sample_mult = np.array([1.0, 1.1, 1.25, 1.6, 3.1, 6.6])
sample_r = sample_mult * R_EARTH
sample_v = np.sqrt(G * M_EARTH / sample_r)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=r_arr / 1e6, y=v_arr,
    mode="lines", line=dict(color="royalblue", width=2),
    name="이론값 v = √(GM/r)"))
fig2.add_trace(go.Scatter(
    x=sample_r / 1e6, y=sample_v,
    mode="markers", marker=dict(size=10, color="crimson"),
    name="시뮬레이션 측정점"))
fig2.add_trace(go.Scatter(
    x=[r / 1e6], y=[v],
    mode="markers+text", marker=dict(size=16, color="gold",
                                     symbol="star",
                                     line=dict(color="black", width=1)),
    text=[f" 현재 ({v:.0f} m/s)"], textposition="top right",
    name="현재 위성"))
fig2.update_layout(
    xaxis_title="궤도 반지름 r (×10⁶ m)",
    yaxis_title="공전 속도 v (m/s)",
    height=380,
    legend=dict(x=0.55, y=0.95),
    margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------------------------------
# 📋 성분별 상세 분석표
# ------------------------------------------------------------
with st.expander("🔬 성분별 상세 분석 데이터 보기", expanded=False):
    st.subheader("📋 인공위성 등속 원운동의 역학적 분석표")
    analysis = pd.DataFrame({
        "구분": ["알짜힘(F)", "운동의 종류", "가속도(a)",
                 "속도의 크기", "속도 방향", "에너지 보존"],
        "물리량": [
            f"만유인력 F = GMm/r² → 단위질량당 {F_grav:.3f} N/kg",
            "등속 원운동 (uniform circular motion)",
            f"구심 가속도 aₙ = v²/r = {a_c:.3f} m/s² (지구 중심 방향)",
            f"v = √(GM/r) = {v:.1f} m/s (일정)",
            "궤도의 접선 방향",
            "역학적 에너지 E = -GMm/(2r) (보존)"]
    })
    st.dataframe(analysis, use_container_width=True, hide_index=True)

    st.subheader("📊 대표 궤도별 비교표")
    compare = pd.DataFrame({
        "궤도": ["지표면(r=Rₑ)", "LEO(1.1Rₑ)", "MEO(3.1Rₑ)",
                 "GEO(6.6Rₑ)"],
        "r (×10⁶ m)": [R_EARTH/1e6, 1.1*R_EARTH/1e6,
                       3.1*R_EARTH/1e6, GEO_R/1e6],
        "v (m/s)": [
            np.sqrt(G*M_EARTH/R_EARTH),
            np.sqrt(G*M_EARTH/(1.1*R_EARTH)),
            np.sqrt(G*M_EARTH/(3.1*R_EARTH)),
            np.sqrt(G*M_EARTH/GEO_R)],
        "T (분)": [
            2*np.pi*R_EARTH/np.sqrt(G*M_EARTH/R_EARTH)/60,
            2*np.pi*1.1*R_EARTH/np.sqrt(G*M_EARTH/(1.1*R_EARTH))/60,
            2*np.pi*3.1*R_EARTH/np.sqrt(G*M_EARTH/(3.1*R_EARTH))/60,
            2*np.pi*GEO_R/np.sqrt(G*M_EARTH/GEO_R)/60]
    })
    compare = compare.round(3)
    st.dataframe(compare, use_container_width=True, hide_index=True)

# ------------------------------------------------------------
# 📝 데이터 다운로드 (보고서 작성용)
# ------------------------------------------------------------
st.divider()
st.markdown("### 📝 보고서 작성용 데이터 내보내기")
st.caption("시뮬레이션에서 측정한 데이터를 CSV로 내려받아 보고서에 첨부하세요.")

export_mult = np.array([1.0, 1.1, 1.25, 1.6, 2.0, 3.1, 4.5, 6.6])
export_r = export_mult * R_EARTH
export_v = np.sqrt(G * M_EARTH / export_r)
export_T = 2 * np.pi * export_r / export_v
export_df = pd.DataFrame({
    "회차": np.arange(1, len(export_mult) + 1),
    "r/Rₑ": export_mult,
    "r (m)": export_r,
    "v (m/s)": export_v,
    "T (s)": export_T
}).round(3)

st.dataframe(export_df, use_container_width=True, hide_index=True)
st.download_button(
    "⬇ 측정 데이터 CSV 다운로드",
    data=export_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="satellite_orbit_data.csv",
    mime="text/csv")

st.divider()
st.markdown(
    "> 🔎 **탐구 미션**  \n"
    "> 1. 위 데이터를 활용하여 **v² vs 1/r** 그래프를 그려보고, "
    "기울기가 무엇을 의미하는지 해석하시오.  \n"
    "> 2. 시뮬레이션 결과로부터 **v = √(GM/r)** 식을 스스로 유도하시오.  \n"
    "> 3. **제1 우주 속도**가 시뮬레이션 데이터의 어느 지점과 "
    "대응되는지 정량적으로 설명하시오."
)
