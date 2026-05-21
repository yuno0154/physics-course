"""
3D 전기장 시각화 Streamlit 앱

실행 방법:
    streamlit run electric_field_3d.py

필요 패키지:
    pip install streamlit plotly numpy
"""

import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ══════════════════════════════════════════════════════════════
# 페이지 설정
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="3D 전기장 시각화",
    page_icon="⚡",
    layout="wide",
)
st.title("⚡ 3D 전기장 시각화")
st.caption("마우스: 회전  |  스크롤: 확대/축소  |  더블클릭: 초기화")

# ══════════════════════════════════════════════════════════════
# 상수
# ══════════════════════════════════════════════════════════════
DOMAIN = 3.5    # 시각화 영역 반경
CUTOFF = 0.35   # 특이점(singularity) 방지 최솟값

# ══════════════════════════════════════════════════════════════
# 사이드바
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ 설정")

    CONFIGS = [
        "① 양전하 + 양전하",
        "② 음전하 + 음전하",
        "③ 양전하 + 음전하  (쌍극자)",
        "④ 전하량이 다른 양전하 + 음전하",
        "⑤ 두 평행판 도체  (커패시터)",
        "⑥ 균일한 전기장 속 도체구",
    ]
    cfg = st.selectbox("전하 배치 선택", CONFIGS)

    st.divider()
    st.subheader("📊 파라미터")

    if cfg in (CONFIGS[0], CONFIGS[1]):
        q_val = st.slider("전하량 크기 |q|",    0.5, 3.0, 1.0, 0.1)
        sep   = st.slider("두 전하 간격 (d)",   1.0, 5.0, 2.0, 0.1)

    elif cfg == CONFIGS[2]:   # 쌍극자
        q_val = st.slider("전하량 크기 |q|",    0.5, 3.0, 1.0, 0.1)
        sep   = st.slider("두 전하 간격 (d)",   1.0, 5.0, 2.0, 0.1)

    elif cfg == CONFIGS[3]:   # 전하량이 다른 +/-
        q1  = st.slider("양전하 크기  q₁",      0.5, 3.0, 2.0, 0.1)
        q2  = st.slider("음전하 크기 |q₂|",     0.5, 3.0, 1.0, 0.1)
        sep = st.slider("두 전하 간격 (d)",      1.0, 5.0, 2.0, 0.1)

    elif cfg == CONFIGS[4]:   # 평행판
        plate_d = st.slider("판 간격 (d)",       0.5, 3.0, 1.5, 0.1)
        plate_L = st.slider("판 크기 (L)",       1.0, 5.0, 3.0, 0.1)

    elif cfg == CONFIGS[5]:   # 도체구
        E0 = st.slider("외부 전기장 세기 E₀",   0.5, 3.0, 1.0, 0.1)
        Rs = st.slider("도체구 반지름 R",        0.2, 1.5, 0.8, 0.05)

    st.divider()
    st.subheader("🎨 시각화 옵션")
    show_geo = st.checkbox("전하/도체 표시", value=True)
    colormap = st.selectbox("색상표", ["Plasma", "Viridis", "Hot", "Jet"])
    n_grid   = st.select_slider("격자 해상도 N (N³개 점)", [6, 7, 8, 9, 10], value=8)


# ══════════════════════════════════════════════════════════════
# 3차원 격자
# ══════════════════════════════════════════════════════════════
g = np.linspace(-DOMAIN, DOMAIN, n_grid)
X, Y, Z = np.meshgrid(g, g, g)


# ══════════════════════════════════════════════════════════════
# 전기장 계산 함수
# ══════════════════════════════════════════════════════════════
def E_point(q, r0, X, Y, Z):
    """
    점전하 q (위치 r0)에 의한 전기장.
    특이점 근처는 CUTOFF로 클램핑하여 발산 방지.
    """
    dx, dy, dz = X - r0[0], Y - r0[1], Z - r0[2]
    r = np.maximum(np.sqrt(dx**2 + dy**2 + dz**2), CUTOFF)
    c = q / r**3
    return c * dx, c * dy, c * dz


def E_sum(charge_list, X, Y, Z):
    """중첩 원리: 여러 점전하의 전기장 합산."""
    Ex = np.zeros_like(X, dtype=float)
    Ey = np.zeros_like(X, dtype=float)
    Ez = np.zeros_like(X, dtype=float)
    for q, r0 in charge_list:
        ex, ey, ez = E_point(q, r0, X, Y, Z)
        Ex += ex;  Ey += ey;  Ez += ez
    return Ex, Ey, Ez


def make_plate_charges(d, L, n=7):
    """
    평행판 커패시터를 점전하 격자로 근사.
      양극판: z = +d/2  (전하 +)
      음극판: z = -d/2  (전하 -)
      각 판의 총 전하 = ±1 (단위 전하)
    """
    q_unit = 1.0 / n**2
    pts    = np.linspace(-L / 2, L / 2, n)
    cl     = []
    for xi in pts:
        for yi in pts:
            cl.append((+q_unit, [xi, yi, +d / 2]))
            cl.append((-q_unit, [xi, yi, -d / 2]))
    return cl


def E_sphere(E0, R, X, Y, Z):
    """
    균일한 전기장 E₀ẑ 속 도체구 (원점, 반지름 R) 외부 전기장.

    외부 해석해:
      E_x = 3 E₀ R³ x z / r⁵
      E_y = 3 E₀ R³ y z / r⁵
      E_z = E₀ + E₀ R³ (3z² − r²) / r⁵

    도체 내부 (r ≤ R): E = 0  → NaN으로 마킹해 화살표 미표시
    """
    r     = np.sqrt(X**2 + Y**2 + Z**2)
    outer = r > R

    with np.errstate(invalid="ignore", divide="ignore"):
        ro = np.where(outer, r, np.nan)
        Ex = np.where(outer, 3 * E0 * R**3 * X * Z / ro**5,                  np.nan)
        Ey = np.where(outer, 3 * E0 * R**3 * Y * Z / ro**5,                  np.nan)
        Ez = np.where(outer, E0 + E0 * R**3 * (3 * Z**2 - ro**2) / ro**5,   np.nan)
    return Ex, Ey, Ez


# ══════════════════════════════════════════════════════════════
# 선택된 배치에 따라 전기장 계산
# ══════════════════════════════════════════════════════════════
geo_items = []   # 렌더링할 기하 객체 목록

if cfg == CONFIGS[0]:       # 양전하 + 양전하
    cl = [(+q_val, [-sep/2, 0, 0]), (+q_val, [+sep/2, 0, 0])]
    Ex, Ey, Ez = E_sum(cl, X, Y, Z)
    geo_items  = [("charge", +1, p) for _, p in cl]

elif cfg == CONFIGS[1]:     # 음전하 + 음전하
    cl = [(-q_val, [-sep/2, 0, 0]), (-q_val, [+sep/2, 0, 0])]
    Ex, Ey, Ez = E_sum(cl, X, Y, Z)
    geo_items  = [("charge", -1, p) for _, p in cl]

elif cfg == CONFIGS[2]:     # 쌍극자
    cl = [(+q_val, [-sep/2, 0, 0]), (-q_val, [+sep/2, 0, 0])]
    Ex, Ey, Ez = E_sum(cl, X, Y, Z)
    geo_items  = [("charge", +1, cl[0][1]), ("charge", -1, cl[1][1])]

elif cfg == CONFIGS[3]:     # 전하량이 다른 +/-
    cl = [(+q1, [-sep/2, 0, 0]), (-q2, [+sep/2, 0, 0])]
    Ex, Ey, Ez = E_sum(cl, X, Y, Z)
    geo_items  = [("charge", +1, cl[0][1]), ("charge", -1, cl[1][1])]

elif cfg == CONFIGS[4]:     # 평행판 커패시터
    cl = make_plate_charges(plate_d, plate_L)
    Ex, Ey, Ez = E_sum(cl, X, Y, Z)
    geo_items  = [("plate", plate_d, plate_L)]

elif cfg == CONFIGS[5]:     # 도체구
    Ex, Ey, Ez = E_sphere(E0, Rs, X, Y, Z)
    geo_items  = [("sphere", Rs)]


# ══════════════════════════════════════════════════════════════
# Cone 데이터 준비 (로그 압축 크기 + 방향 분리)
# ══════════════════════════════════════════════════════════════
fx = X.flatten();  fy = Y.flatten();  fz = Z.flatten()
fu = Ex.flatten(); fv = Ey.flatten(); fw = Ez.flatten()

# NaN 제거 (도체 내부 등)
ok = ~(np.isnan(fu) | np.isnan(fv) | np.isnan(fw))
fx, fy, fz = fx[ok], fy[ok], fz[ok]
fu, fv, fw = fu[ok], fv[ok], fw[ok]

mag   = np.sqrt(fu**2 + fv**2 + fw**2)
mag_s = np.maximum(mag, 1e-12)
lmag  = np.log1p(mag)          # log(1 + |E|): 큰 값의 동적 범위 압축

# 방향 단위벡터 × 로그 크기  → 시각적으로 균형 잡힌 화살표
fu_c = fu / mag_s * lmag
fv_c = fv / mag_s * lmag
fw_c = fw / mag_s * lmag


# ══════════════════════════════════════════════════════════════
# Plotly 3D 그림 생성
# ══════════════════════════════════════════════════════════════
fig = go.Figure()

# ── 전기장 화살표 (Cone) ──────────────────────────────────────
fig.add_trace(go.Cone(
    x=fx, y=fy, z=fz,
    u=fu_c, v=fv_c, w=fw_c,
    colorscale=colormap,
    sizemode="scaled",
    sizeref=0.85,
    showscale=True,
    colorbar=dict(
        title=dict(text="|E| (log)", side="right"),
        thickness=14,
        len=0.6,
    ),
    customdata=mag,
    hovertemplate=(
        "x = %{x:.2f}  y = %{y:.2f}  z = %{z:.2f}<br>"
        "|E| = %{customdata:.4f}<extra>전기장</extra>"
    ),
    name="전기장",
))

# ── 기하 객체 (전하, 판, 구) ──────────────────────────────────
if show_geo:
    for item in geo_items:
        kind = item[0]

        # 점전하
        if kind == "charge":
            _, sign, pos = item
            color = "#e74c3c" if sign > 0 else "#2471a3"
            label = "양전하 (+)" if sign > 0 else "음전하 (−)"
            fig.add_trace(go.Scatter3d(
                x=[pos[0]], y=[pos[1]], z=[pos[2]],
                mode="markers",
                marker=dict(
                    size=16, color=color,
                    line=dict(color="white", width=2),
                    symbol="circle",
                ),
                name=label,
            ))

        # 평행판
        elif kind == "plate":
            _, d, L = item
            h  = L / 2
            xs = [-h, h, h, -h, -h]
            ys = [-h, -h, h, h, -h]

            plate_specs = [
                (+d / 2, "#c0392b", "양극판 (+)"),
                (-d / 2, "#1a5276", "음극판 (−)"),
            ]
            for z0, pc, lbl in plate_specs:
                # 윤곽선
                fig.add_trace(go.Scatter3d(
                    x=xs, y=ys, z=[z0] * 5,
                    mode="lines",
                    line=dict(color=pc, width=5),
                    name=lbl,
                ))
                # 반투명 면
                px = np.array([[-h, h], [-h, h]])
                py = np.array([[-h, -h], [h, h]])
                pz = np.full((2, 2), z0, dtype=float)
                fig.add_trace(go.Surface(
                    x=px, y=py, z=pz,
                    colorscale=[[0, pc], [1, pc]],
                    opacity=0.3,
                    showscale=False,
                    name=lbl,
                    showlegend=False,
                ))

        # 도체구
        elif kind == "sphere":
            _, R = item
            u_s = np.linspace(0, 2 * np.pi, 60)
            v_s = np.linspace(0, np.pi, 30)
            xs  = R * np.outer(np.cos(u_s), np.sin(v_s))
            ys  = R * np.outer(np.sin(u_s), np.sin(v_s))
            zs  = R * np.outer(np.ones(60),  np.cos(v_s))
            fig.add_trace(go.Surface(
                x=xs, y=ys, z=zs,
                colorscale=[[0, "#bdc3c7"], [1, "#ecf0f1"]],
                opacity=0.5,
                showscale=False,
                name="도체구",
            ))

# ── 레이아웃 ──────────────────────────────────────────────────
ax_style = dict(
    showbackground=True,
    backgroundcolor="rgba(235, 240, 255, 0.6)",
    gridcolor="rgba(180, 180, 220, 0.5)",
    zerolinecolor="rgba(80, 80, 140, 0.4)",
    range=[-DOMAIN, DOMAIN],
)
fig.update_layout(
    scene=dict(
        xaxis=dict(**ax_style, title="x"),
        yaxis=dict(**ax_style, title="y"),
        zaxis=dict(**ax_style, title="z"),
        aspectmode="cube",
        camera=dict(
            eye=dict(x=1.6, y=1.2, z=0.9),
            up=dict(x=0, y=0, z=1),
        ),
    ),
    height=680,
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(
        x=0.01, y=0.97,
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="rgba(0,0,0,0.15)",
        borderwidth=1,
    ),
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════
# 물리 설명 & 수식
# ══════════════════════════════════════════════════════════════
st.divider()

PHYSICS_INFO = {
    CONFIGS[0]: (
        "두 **양전하** 사이에는 **척력**이 작용합니다. "
        "전기력선은 각 전하에서 방사상으로 퍼져나가며, "
        "두 전하를 잇는 선분의 중점에 **중립점**(전기장 = 0)이 형성됩니다. "
        "이 중립점은 안장점(saddle point) 구조를 가집니다."
    ),
    CONFIGS[1]: (
        "두 **음전하** 사이에도 **척력**이 작용합니다. "
        "전기력선은 모든 방향에서 각 전하를 향해 수렴하며, "
        "두 전하의 중점에 중립점이 나타납니다."
    ),
    CONFIGS[2]: (
        "양전하(+)와 음전하(−) 사이에는 **인력**이 작용하는 **전기 쌍극자**입니다. "
        "전기력선은 양전하에서 출발하여 음전하로 들어가는 "
        "특징적인 아치형 패턴을 그립니다. "
        "쌍극자 모멘트: **p** = q·d (방향: − → +)"
    ),
    CONFIGS[3]: (
        "두 전하량이 다를 경우, 더 큰 전하에서 더 많은 전기력선이 나옵니다. "
        "**중립점은 작은 전하 쪽으로 치우치며**, "
        "큰 전하에서 나온 일부 전기력선은 무한히 멀리까지 뻗어 나갑니다."
    ),
    CONFIGS[4]: (
        "이상적인 **평행판 커패시터**입니다. "
        "판 사이 영역에서는 균일하고 강한 전기장이 형성되며, "
        "판의 가장자리에서는 **가장자리 효과**(fringe effect)로 전기장이 퍼집니다. "
        "이상적인 무한 평판에서는 판 외부 전기장이 0이 됩니다."
    ),
    CONFIGS[5]: (
        "도체구 **내부 전기장 = 0** (정전기 차폐). "
        "외부 균일 전기장은 구를 우회하며, 구 표면에 **유도 전하**가 분포합니다 "
        "(E₀ 반대쪽: 음전하, E₀ 방향쪽: 양전하). "
        "도체구에서 멀어질수록 원래의 균일 전기장 E₀로 수렴합니다."
    ),
}

FORMULA_INFO = {
    CONFIGS[0]: r"\vec{E} = k\sum_{i=1}^{2}\frac{q_i}{r_i^2}\hat{r}_i \quad (q_i > 0)",
    CONFIGS[1]: r"\vec{E} = k\sum_{i=1}^{2}\frac{q_i}{r_i^2}\hat{r}_i \quad (q_i < 0)",
    CONFIGS[2]: (
        r"\vec{E}_{쌍극자} \approx \frac{p}{4\pi\varepsilon_0 r^3}"
        r"\left(2\cos\theta\,\hat{r}+\sin\theta\,\hat{\theta}\right)"
    ),
    CONFIGS[3]: (
        r"\vec{E} = k\frac{q_1}{r_1^2}\hat{r}_1 + k\frac{q_2}{r_2^2}\hat{r}_2"
        r"\quad (q_1 \neq |q_2|)"
    ),
    CONFIGS[4]: r"E = \frac{\sigma}{\varepsilon_0} = \frac{Q}{\varepsilon_0 A} \quad (\text{판 사이, 균일장})",
    CONFIGS[5]: (
        r"\vec{E}_{외부} = E_0\hat{z}"
        r"+ \frac{E_0 R^3}{r^5}"
        r"\left[(3z^2-r^2)\hat{z}+3xz\,\hat{x}+3yz\,\hat{y}\right]"
    ),
}

c1, c2 = st.columns([3, 2])
with c1:
    st.subheader("📖 물리적 해석")
    st.markdown(PHYSICS_INFO[cfg])
with c2:
    st.subheader("📐 핵심 수식")
    st.latex(FORMULA_INFO[cfg])

st.markdown("""
---
> **화살표 색상** : 전기장 세기 log(1 + |E|) — 밝을수록 강한 전기장  
> **화살표 방향** : 전기력 방향 (양전하 → 음전하)  
> **격자 해상도** : N을 높이면 더 촘촘하지만 렌더링이 느려집니다
""")
