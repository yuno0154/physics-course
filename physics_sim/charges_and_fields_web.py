"""
전하와 전기장 방향 탐구 (Streamlit / Plotly 버전)
=================================================
PhET Charges and Fields 스타일의 자유 탐구 페이지
- 양전하 / 음전하 배치
- 전기장 화살표 및 등전위선 시각화
- 다음 차시 '전기장의 방향 정의'와 연결
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ── 물리 상수 ────────────────────────────────────────────────
K_E    = 8.99e9    # 쿨롱 상수 [N·m²/C²]
Q_UNIT = 1e-9      # 1 nC = 1e-9 C
DOMAIN = 5.0       # 캔버스 범위 [-5, 5]
GRID_N = 20        # 화살표 격자 해상도


def compute_field(charges, X, Y):
    """주어진 전하 배치에서 전기장(Ex, Ey)과 전위(V) 계산"""
    Ex = np.zeros_like(X, dtype=float)
    Ey = np.zeros_like(Y, dtype=float)
    V  = np.zeros_like(X, dtype=float)
    for (cx, cy, q) in charges:
        dx = X - cx
        dy = Y - cy
        r2 = dx**2 + dy**2
        r2 = np.where(r2 < 0.04, 0.04, r2)   # 특이점 방지
        r  = np.sqrt(r2)
        r3 = r2 * r
        coeff = K_E * q * Q_UNIT
        Ex += coeff * dx / r3
        Ey += coeff * dy / r3
        V  += coeff / r
    return Ex, Ey, V


def build_field_figure(charges, show_field, show_voltage,
                       direction_only, show_values, show_grid):
    """Plotly 전기장 시각화 그림 생성"""
    fig = go.Figure()

    # 격자선
    if show_grid:
        for v in np.arange(-DOMAIN, DOMAIN + 1, 1):
            fig.add_shape(type='line', x0=v, y0=-DOMAIN, x1=v, y1=DOMAIN,
                          line=dict(color='rgba(80,80,120,0.4)', width=0.8, dash='dot'))
            fig.add_shape(type='line', x0=-DOMAIN, y0=v, x1=DOMAIN, y1=v,
                          line=dict(color='rgba(80,80,120,0.4)', width=0.8, dash='dot'))

    if charges:
        xs  = np.linspace(-DOMAIN, DOMAIN, GRID_N)
        ys  = np.linspace(-DOMAIN, DOMAIN, GRID_N)
        X, Y = np.meshgrid(xs, ys)
        Ex, Ey, V = compute_field(charges, X, Y)
        E_mag = np.sqrt(Ex**2 + Ey**2)
        safe_mag = np.where(E_mag == 0, 1.0, E_mag)

        # ── 등전위선 ──
        if show_voltage:
            vmax = float(np.percentile(np.abs(V), 96))
            vmax = min(vmax, 1e5)
            lvl  = np.linspace(-vmax, vmax, 20)
            fig.add_trace(go.Contour(
                x=xs, y=ys, z=V,
                colorscale='RdBu_r',
                showscale=False,
                opacity=0.45,
                line_width=1.2,
                contours=dict(
                    showlabels=show_values,
                    start=float(lvl[0]),
                    end=float(lvl[-1]),
                    size=float((lvl[-1] - lvl[0]) / 20),
                    labelfont=dict(size=8, color='#dddddd')
                )
            ))

        # ── 전기장 화살표 (quiver 직접 구현) ──
        if show_field:
            log_mag = np.log10(np.clip(E_mag, 1e-3, None))
            lmin, lmax = log_mag.min(), log_mag.max()
            norm = (log_mag - lmin) / (lmax - lmin + 1e-10)

            if direction_only:
                Ux = Ex / safe_mag * 0.20
                Uy = Ey / safe_mag * 0.20
            else:
                Ux = Ex / safe_mag * norm * 0.22
                Uy = Ey / safe_mag * norm * 0.22

            # Plotly quiver (선분 + 화살촉)
            arrow_x, arrow_y = [], []
            for i in range(GRID_N):
                for j in range(GRID_N):
                    x0, y0 = X[i, j], Y[i, j]
                    dx_, dy_ = Ux[i, j], Uy[i, j]
                    x1, y1 = x0 + dx_, y0 + dy_
                    arrow_x += [x0, x1, None]
                    arrow_y += [y0, y1, None]

            fig.add_trace(go.Scatter(
                x=arrow_x, y=arrow_y,
                mode='lines',
                line=dict(color='rgba(255,255,255,0.6)', width=1.1),
                showlegend=False, hoverinfo='skip'
            ))

            # 화살촉 (arrowhead annotation은 비용이 크므로 marker로 대체)
            tip_x = [X[i, j] + Ux[i, j]
                     for i in range(GRID_N) for j in range(GRID_N)]
            tip_y = [Y[i, j] + Uy[i, j]
                     for i in range(GRID_N) for j in range(GRID_N)]
            fig.add_trace(go.Scatter(
                x=tip_x, y=tip_y,
                mode='markers',
                marker=dict(size=3, color='rgba(255,255,255,0.5)',
                            symbol='triangle-up'),
                showlegend=False, hoverinfo='skip'
            ))

    # ── 전하 그리기 ──
    for i, (cx, cy, sign) in enumerate(charges):
        color  = '#ff4444' if sign > 0 else '#4488ff'
        border = '#ff9999' if sign > 0 else '#88bbff'
        label  = '+1 nC' if sign > 0 else '−1 nC'
        sym    = '+' if sign > 0 else '−'

        fig.add_trace(go.Scatter(
            x=[cx], y=[cy],
            mode='markers+text',
            marker=dict(size=30, color=color,
                        line=dict(color=border, width=2.5)),
            text=[sym],
            textposition='middle center',
            textfont=dict(size=16, color='white', family='Arial Black'),
            showlegend=False,
            hovertemplate=f'전하 {i+1}: {label}<br>위치: ({cx:.1f}, {cy:.1f})<extra></extra>'
        ))

        if show_values:
            fig.add_annotation(
                x=cx, y=cy - 0.65, text=label,
                font=dict(size=10, color='#ffee88'),
                showarrow=False,
                bgcolor='rgba(0,0,0,0.55)', borderpad=3
            )

    # ── 레이아웃 ──
    fig.update_layout(
        xaxis=dict(range=[-DOMAIN, DOMAIN], showgrid=False,
                   zeroline=True, zerolinecolor='#334455', zerolinewidth=1.5,
                   tickfont=dict(color='#778899'), title='x (m)'),
        yaxis=dict(range=[-DOMAIN, DOMAIN], showgrid=False,
                   zeroline=True, zerolinecolor='#334455', zerolinewidth=1.5,
                   scaleanchor='x', scaleratio=1,
                   tickfont=dict(color='#778899'), title='y (m)'),
        plot_bgcolor='#0d1117',
        paper_bgcolor='#0d1117',
        height=580,
        margin=dict(l=50, r=20, t=20, b=50),
        showlegend=False,
        dragmode='pan'
    )
    return fig


# ══════════════════════════════════════════════════════════════
#  페이지 시작
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
  .charge-card {
      background: linear-gradient(135deg, #1e1e3a, #2a1a4a);
      border-left: 4px solid #7c3aed;
      border-radius: 10px;
      padding: 14px 18px;
      margin-bottom: 16px;
  }
  .step-box {
      background: rgba(255,255,255,0.04);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 8px;
      padding: 12px 16px;
      margin: 8px 0;
  }
</style>
""", unsafe_allow_html=True)

st.title("⚡ 전하와 전기장 방향 탐구")

st.markdown("""
<div class='charge-card'>
  <b style='color:#c4b5fd; font-size:1rem;'>🎯 학습 목표</b><br>
  <span style='color:#e2e8f0; font-size:0.92rem;'>
  전하 주위에 형성되는 전기장의 <b>모양과 방향</b>을 탐구하고,<br>
  전기장의 방향이 어떻게 정의되는지 이해합니다.
  </span>
</div>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──
if 'cfw_charges' not in st.session_state:
    st.session_state.cfw_charges = []

# ── 사이드바: 제어판 ──
with st.sidebar:
    st.markdown("## ⚙️ 전하 제어판")
    st.markdown("---")

    # 전하 종류
    st.markdown("**전하 종류 선택**")
    charge_type = st.radio(
        "", ['🔴 +1 nC (양전하)', '🔵 −1 nC (음전하)'],
        key='cfw_type', label_visibility='collapsed'
    )
    sign_val = +1 if '양전하' in charge_type else -1

    st.markdown("**위치 입력 (−5 ~ +5 m)**")
    col1, col2 = st.columns(2)
    with col1:
        new_x = st.number_input("x", -4.5, 4.5, 0.0, 0.5, key='cfw_x',
                                label_visibility='visible')
    with col2:
        new_y = st.number_input("y", -4.5, 4.5, 0.0, 0.5, key='cfw_y',
                                label_visibility='visible')

    if st.button("➕ 이 위치에 전하 추가", use_container_width=True, type='primary'):
        st.session_state.cfw_charges.append((new_x, new_y, sign_val))
        st.rerun()

    st.markdown("**📍 자주 쓰는 위치**")
    quick_cols = st.columns(2)
    quick_list = [
        ("중앙", 0.0, 0.0), ("오른쪽", 2.0, 0.0),
        ("왼쪽", -2.0, 0.0), ("위쪽", 0.0, 2.0),
        ("아래", 0.0, -2.0), ("우상", 2.0, 2.0),
    ]
    for idx, (lbl, qx, qy) in enumerate(quick_list):
        with quick_cols[idx % 2]:
            if st.button(lbl, key=f'cfw_q{idx}', use_container_width=True):
                st.session_state.cfw_charges.append((qx, qy, sign_val))
                st.rerun()

    st.markdown("---")
    st.markdown("**🖥️ 표시 옵션**")
    show_field_w     = st.checkbox("⚡ 전기장 화살표",  True,  key='cfw_field')
    direction_only_w = st.checkbox("↗ 방향만 표시",    False, key='cfw_dir')
    show_voltage_w   = st.checkbox("🌊 등전위선",       False, key='cfw_volt')
    show_values_w    = st.checkbox("🔢 수치 레이블",    False, key='cfw_vals')
    show_grid_w      = st.checkbox("📐 격자선",         True,  key='cfw_grid')

    st.markdown("---")
    if st.button("🗑️ 전체 삭제", use_container_width=True):
        st.session_state.cfw_charges = []
        st.rerun()

    # 현재 전하 목록
    if st.session_state.cfw_charges:
        st.markdown("**현재 배치된 전하**")
        for i, (cx, cy, sq) in enumerate(st.session_state.cfw_charges):
            dot   = '🔴' if sq > 0 else '🔵'
            label = '+1nC' if sq > 0 else '−1nC'
            col_i, col_d = st.columns([3, 1])
            with col_i:
                st.markdown(f"<span style='font-size:0.85rem'>{dot} {label} ({cx:.1f},{cy:.1f})</span>",
                            unsafe_allow_html=True)
            with col_d:
                if st.button("✕", key=f'cfw_del{i}'):
                    st.session_state.cfw_charges.pop(i)
                    st.rerun()

# ── 메인: 캔버스 ──
fig_web = build_field_figure(
    st.session_state.cfw_charges,
    show_field_w, show_voltage_w,
    direction_only_w, show_values_w, show_grid_w
)
st.plotly_chart(fig_web, use_container_width=True, config={'scrollZoom': True})

if not st.session_state.cfw_charges:
    st.info("👈 왼쪽 사이드바에서 전하를 추가하면 전기장이 표시됩니다.")

# ── 탐구 가이드 ──
st.markdown("---")
st.markdown("### 📚 탐구 순서 및 토론 주제")

with st.expander("1단계: 양전하 1개 배치 — 전기장의 방향", expanded=True):
    st.markdown("""
    <div class='step-box'>
    <b>① 해 보기</b>: 중앙 (0, 0)에 <span style='color:#ff7777'>+1 nC 양전하</span>를 추가하세요.<br>
    <b>② 관찰</b>: 전기장 화살표는 전하로부터 어느 방향을 가리키고 있나요?<br>
    <b>③ 토론</b>: "전기장의 방향"을 어떻게 정의할 수 있을지 이야기해 봅시다.
    </div>
    """, unsafe_allow_html=True)

with st.expander("2단계: 음전하 1개 배치 — 방향 비교"):
    st.markdown("""
    <div class='step-box'>
    <b>① 전체 삭제</b> 후 중앙에 <span style='color:#7799ff'>−1 nC 음전하</span>를 추가하세요.<br>
    <b>② 관찰</b>: 화살표 방향이 양전하일 때와 어떻게 다른가요?<br>
    <b>③ 결론</b>: 전기장의 방향 = <i>양(+)전하를 놓았을 때 받는 힘의 방향</i>
    </div>
    """, unsafe_allow_html=True)

with st.expander("3단계: 쌍극자 (양전하 + 음전하)"):
    st.markdown("""
    <div class='step-box'>
    <b>① 배치</b>: 왼쪽 (−2, 0)에 +1 nC, 오른쪽 (+2, 0)에 −1 nC 추가<br>
    <b>② 관찰</b>: 전기장선이 한 전하에서 나와 다른 전하로 들어가는 모습을 확인<br>
    <b>③ 등전위선</b>도 켜서 전위(V)의 분포를 함께 관찰해 보세요.
    </div>
    """, unsafe_allow_html=True)

with st.expander("4단계: 같은 부호 전하 2개"):
    st.markdown("""
    <div class='step-box'>
    <b>① 배치</b>: 왼쪽 (−2, 0)과 오른쪽 (+2, 0) 모두 +1 nC 배치<br>
    <b>② 관찰</b>: 두 전하 사이 중간 지점의 전기장은 어떻게 될까요?<br>
    <b>③ 예측</b>: 이 결과로부터 같은 부호 전하 사이의 힘(척력)을 설명할 수 있나요?
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background:rgba(124,58,237,0.1); border:1px solid rgba(124,58,237,0.4);
     border-radius:8px; padding:12px 16px; margin-top:12px;'>
  💡 <b style='color:#c4b5fd;'>다음 차시 연결</b><br>
  <span style='color:#e2e8f0; font-size:0.9rem;'>
  오늘 관찰한 2차원 전기장의 방향과 모양을 바탕으로,<br>
  다음 시간에는 3차원 공간에서 전하 배치에 따른 입체적인 <b>전기력선 그리기 [해보기]</b> 활동을 진행하고,<br>
  이어서 전기장의 세기가 거리에 따라 어떻게 변하는지 정량적으로 탐구합니다.
  </span>
</div>
""", unsafe_allow_html=True)
