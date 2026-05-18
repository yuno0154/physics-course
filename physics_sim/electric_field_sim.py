"""
전기장 세기 탐구 실험
Activity 1: 전기장 센서 시뮬레이션 (거리 r에 따른 E 측정)
Activity 2: 그래프 모델링 (r vs E, 1/r² vs E 선형화)
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

K_E    = 8.99e9
Q_UNIT = 1e-9

def compute_E(Q_nC, r_m):
    return K_E * Q_nC * Q_UNIT / (r_m ** 2)

# ── 공통 스타일 ──────────────────────────────────────────────
st.markdown("""
<style>
.info-box {
    background: linear-gradient(135deg,#1e2a3a,#0f1a2a);
    border-left: 4px solid #3b82f6;
    border-radius: 8px; padding:14px 18px; margin:10px 0;
}
.step-header {
    background: linear-gradient(90deg,#1e3a5f,#0f2a4a);
    border-radius: 8px; padding:10px 16px; margin:12px 0 6px 0;
    font-weight:700; color:#93c5fd; font-size:1.05rem;
}
.result-box {
    background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.4);
    border-radius:8px; padding:12px 16px; margin:8px 0;
}
.warn-box {
    background:rgba(251,191,36,0.1); border:1px solid rgba(251,191,36,0.4);
    border-radius:8px; padding:12px 16px; margin:8px 0;
}
</style>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──────────────────────────────────────
if 'ef_measurements' not in st.session_state:
    st.session_state.ef_measurements = []
if 'ef_Q_nC' not in st.session_state:
    st.session_state.ef_Q_nC = 1.0
if 'ef_r' not in st.session_state:
    st.session_state.ef_r = 1.0

# ══════════════════════════════════════════════════════════════
st.title("🔬 전기장 세기 탐구 실험")
st.markdown("""
<div class='info-box'>
<b style='color:#93c5fd; font-size:1rem;'>🎯 학습 목표</b><br>
<span style='color:#e2e8f0; font-size:0.92rem;'>
점전하로부터의 거리 <b>r</b>에 따른 전기장 세기 <b>E</b>를 측정하고,<br>
그래프 분석과 <b>선형화(Linearization)</b>를 통해 <b>E = kQ/r²</b> 관계를 탐구합니다.
</span>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚡ 활동 1: 전기장 측정", "📊 활동 2: 그래프 모델링"])

# ══════════════════════════════════════════════════════════════
# 활동 1
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='step-header'>① 전하량(Q) 설정</div>", unsafe_allow_html=True)
    st.markdown("측정할 점전하의 크기를 선택하세요. (실험 중 변경하지 않는 것을 권장)")

    Q_options = [1.0, 2.0, 5.0, 10.0]
    q_cols = st.columns(4)
    for i, q in enumerate(Q_options):
        with q_cols[i]:
            selected = st.session_state.ef_Q_nC == q
            if st.button(
                f"{'✅ ' if selected else ''}{int(q)} nC",
                key=f'ef_q{i}',
                use_container_width=True,
                type='primary' if selected else 'secondary'
            ):
                st.session_state.ef_Q_nC = q
                st.session_state.ef_measurements = []
                st.rerun()

    Q_nC = st.session_state.ef_Q_nC
    st.markdown(f"**현재 전하량: Q = {Q_nC:.0f} nC**")

    st.markdown("---")
    st.markdown("<div class='step-header'>② 센서 위치(거리 r) 설정</div>", unsafe_allow_html=True)
    st.markdown("전기장 센서를 전하로부터 원하는 거리에 위치시키세요.")

    # 빠른 선택 버튼
    st.markdown("**빠른 선택:**")
    r_presets = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    r_cols = st.columns(6)
    for i, rp in enumerate(r_presets):
        with r_cols[i]:
            if st.button(f"{rp}m", key=f'ef_rp{i}', use_container_width=True):
                st.session_state.ef_r = rp
                st.rerun()

    # 직접 입력
    r_input = st.number_input(
        "거리 r 직접 입력 (m)",
        min_value=0.1, max_value=5.0,
        value=st.session_state.ef_r,
        step=0.1, format="%.1f",
        key='ef_r_input'
    )
    st.session_state.ef_r = r_input
    r = st.session_state.ef_r
    E_now = compute_E(Q_nC, r)

    st.markdown("---")
    st.markdown("<div class='step-header'>③ 캔버스에서 센서 위치 확인</div>", unsafe_allow_html=True)

    # ── 캔버스 그리기 ──
    fig1 = go.Figure()
    theta = np.linspace(0, 2 * np.pi, 300)

    # 동심원 (r = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
    for ring_r in r_presets:
        alpha = 0.5 if abs(ring_r - r) < 0.05 else 0.2
        fig1.add_trace(go.Scatter(
            x=ring_r * np.cos(theta), y=ring_r * np.sin(theta),
            mode='lines',
            line=dict(color=f'rgba(100,150,255,{alpha})', width=1.5 if abs(ring_r - r) < 0.05 else 0.8, dash='dot'),
            showlegend=False, hoverinfo='skip'
        ))
        fig1.add_annotation(x=ring_r + 0.05, y=0.12, text=f'{ring_r}m',
                            font=dict(size=9, color='#6688bb'), showarrow=False)

    # 전기장 방사형 화살표
    n_arr = 12
    for i in range(n_arr):
        angle = 2 * np.pi * i / n_arr
        for frac in r_presets:
            r0 = max(frac - 0.18, 0.15)
            r1 = frac + 0.18
            E_here = compute_E(Q_nC, frac)
            log_e = np.log10(max(E_here, 1))
            op = min(0.65, max(0.15, log_e / 10))
            fig1.add_annotation(
                x=r1 * np.cos(angle), y=r1 * np.sin(angle),
                ax=r0 * np.cos(angle), ay=r0 * np.sin(angle),
                xref='x', yref='y', axref='x', ayref='y',
                arrowhead=2, arrowsize=0.9, arrowwidth=1.5,
                arrowcolor=f'rgba(255,180,60,{op:.2f})'
            )

    # 이미 측정된 점들
    for m in st.session_state.ef_measurements:
        fig1.add_trace(go.Scatter(
            x=[m['r']], y=[0],
            mode='markers',
            marker=dict(size=10, color='rgba(100,255,150,0.6)',
                        symbol='circle', line=dict(color='#00ff88', width=1.5)),
            showlegend=False,
            hovertemplate=f"r={m['r']}m, E={m['E']:.2f} N/C<extra></extra>"
        ))

    # 현재 센서 위치
    fig1.add_trace(go.Scatter(
        x=[r], y=[0],
        mode='markers+text',
        marker=dict(size=22, color='#facc15',
                    symbol='circle', line=dict(color='white', width=2)),
        text=['📡'],
        textposition='top center',
        textfont=dict(size=14),
        showlegend=False,
        hovertemplate=f'센서 위치: r = {r:.1f} m<extra></extra>'
    ))

    # E값 말풍선
    fig1.add_annotation(
        x=r, y=0.45,
        text=f'<b>E = {E_now:.2f} N/C</b>',
        font=dict(size=13, color='#facc15'),
        bgcolor='rgba(30,30,60,0.85)',
        bordercolor='#facc15', borderwidth=1.5,
        showarrow=True, arrowhead=2, arrowcolor='#facc15',
        ax=0, ay=-35
    )

    # 중심 전하
    fig1.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        marker=dict(size=30, color='#ef4444', line=dict(color='#fca5a5', width=2.5)),
        text=['+'], textposition='middle center',
        textfont=dict(size=16, color='white', family='Arial Black'),
        showlegend=False,
        hovertemplate=f'점전하 Q = +{Q_nC:.0f} nC<extra></extra>'
    ))

    fig1.update_layout(
        xaxis=dict(range=[-3.8, 3.8], showgrid=False, zeroline=True,
                   zerolinecolor='#334455', tickfont=dict(color='#778899'), title='거리 (m)'),
        yaxis=dict(range=[-2.2, 2.2], showgrid=False, zeroline=True,
                   zerolinecolor='#334455', scaleanchor='x', scaleratio=1,
                   tickfont=dict(color='#778899')),
        plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
        height=380, margin=dict(l=40, r=20, t=20, b=40),
        showlegend=False
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 현재 측정값 표시
    col_info1, col_info2, col_info3 = st.columns(3)
    with col_info1:
        st.metric("전하량 Q", f"{Q_nC:.0f} nC")
    with col_info2:
        st.metric("거리 r", f"{r:.2f} m")
    with col_info3:
        st.metric("전기장 E", f"{E_now:.2f} N/C")

    st.markdown("---")
    st.markdown("<div class='step-header'>④ 측정값 기록</div>", unsafe_allow_html=True)
    st.markdown("센서 위치를 바꿔가며 **최소 6개 이상** 측정하여 데이터를 수집하세요.")

    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        if st.button("📥 이 값 기록하기", type='primary', use_container_width=True):
            already = any(abs(m['r'] - r) < 0.01 for m in st.session_state.ef_measurements)
            if already:
                st.warning(f"r = {r:.2f} m 는 이미 기록되어 있습니다.")
            else:
                st.session_state.ef_measurements.append({
                    'r': round(r, 2),
                    'E': round(E_now, 4),
                    '1/r²': round(1 / r**2, 4)
                })
                st.success(f"✅ 기록 완료: r = {r:.2f} m, E = {E_now:.2f} N/C")
                st.rerun()
    with col_btn2:
        if st.button("🗑️ 전체 초기화", use_container_width=True):
            st.session_state.ef_measurements = []
            st.rerun()

    if st.session_state.ef_measurements:
        df = pd.DataFrame(st.session_state.ef_measurements).sort_values('r').reset_index(drop=True)
        df.index += 1
        st.dataframe(
            df.rename(columns={'r': '거리 r (m)', 'E': '전기장 E (N/C)', '1/r²': '1/r² (m⁻²)'}),
            use_container_width=True
        )
        n = len(df)
        if n < 5:
            st.markdown(f"<div class='warn-box'>📌 현재 {n}개 측정 완료. 활동 2 그래프를 위해 <b>최소 5개 이상</b> 측정하세요.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-box'>✅ {n}개 측정 완료! <b>활동 2 탭</b>으로 이동하여 그래프를 분석하세요.</div>", unsafe_allow_html=True)
    else:
        st.info("아직 기록된 데이터가 없습니다. 위 버튼으로 측정값을 기록하세요.")

# ══════════════════════════════════════════════════════════════
# 활동 2
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
<div class='info-box'>
<b style='color:#93c5fd;'>📊 그래프 모델링 순서</b><br>
<span style='color:#e2e8f0; font-size:0.92rem;'>
<b>1차:</b> r vs E 그래프 → 반비례 곡선 확인<br>
<b>2차:</b> 1/r² vs E 그래프 → 선형화 확인 (원점 통과 직선)
</span>
</div>
""", unsafe_allow_html=True)

    if not st.session_state.ef_measurements or len(st.session_state.ef_measurements) < 3:
        st.warning("⚠️ 활동 1에서 최소 3개 이상 측정 후 이 탭을 이용하세요.")
        st.stop()

    df = pd.DataFrame(st.session_state.ef_measurements).sort_values('r').reset_index(drop=True)
    Q_nC = st.session_state.ef_Q_nC

    # ── 데이터 테이블 ──
    st.markdown("<div class='step-header'>① 측정 데이터 확인 (1/r² 포함)</div>", unsafe_allow_html=True)
    df_show = df.copy()
    df_show.index += 1
    st.dataframe(
        df_show.rename(columns={'r': '거리 r (m)', 'E': '전기장 E (N/C)', '1/r²': '1/r² (m⁻²)'}),
        use_container_width=True
    )

    st.markdown("""
<div class='warn-box'>
💡 <b>1/r² 열이란?</b><br>
E = kQ/r² 이므로, 만약 E가 1/r²에 비례한다면 (1/r²)를 X축으로 했을 때 <b>직선</b>이 나와야 합니다.
이 열은 그 관계를 확인하기 위한 것입니다.
</div>
""", unsafe_allow_html=True)

    # ── 그래프 선택 ──
    st.markdown("---")
    st.markdown("<div class='step-header'>② 그래프 선택</div>", unsafe_allow_html=True)

    graph_mode = st.radio(
        "X축을 선택하세요:",
        ["📈 r vs E  (반비례 곡선 확인)", "📉 1/r² vs E  (선형화 확인)"],
        key='ef_graph_mode'
    )

    r_arr  = df['r'].values
    E_arr  = df['E'].values
    ir2_arr = df['1/r²'].values

    fig2 = go.Figure()

    if "r vs E" in graph_mode:
        # ── 1차: r vs E ──
        st.markdown("""
<div class='step-header'>③ 1차 그래프: r vs E — 반비례 곡선 확인</div>
""", unsafe_allow_html=True)
        st.markdown("""
**관찰 포인트:**
- r이 커질수록 E는 어떻게 변하나요?
- 곡선의 모양은 직선인가요, 반비례 곡선인가요?
- 이론 곡선(점선)과 측정 데이터가 잘 일치하나요?
""")

        # 측정 데이터
        fig2.add_trace(go.Scatter(
            x=r_arr, y=E_arr,
            mode='markers',
            marker=dict(size=11, color='#facc15',
                        line=dict(color='white', width=1.5)),
            name='측정 데이터',
            hovertemplate='r = %{x:.2f} m<br>E = %{y:.2f} N/C<extra></extra>'
        ))

        # 이론 곡선
        r_fit = np.linspace(min(r_arr) * 0.8, max(r_arr) * 1.1, 200)
        E_fit = compute_E(Q_nC, r_fit)
        fig2.add_trace(go.Scatter(
            x=r_fit, y=E_fit,
            mode='lines',
            line=dict(color='rgba(100,200,255,0.7)', width=2, dash='dash'),
            name=f'이론값 E = kQ/r²'
        ))

        fig2.update_layout(
            xaxis=dict(title='거리 r (m)', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(title='전기장 E (N/C)', showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#e2e8f0'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1),
            height=430, margin=dict(l=60, r=20, t=40, b=60)
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
<div class='result-box'>
🔍 <b>분석 결론</b><br>
r vs E 그래프는 <b>반비례 곡선(쌍곡선)</b> 형태를 보입니다.<br>
이 그래프만으로는 정확한 수식 관계를 파악하기 어렵습니다.<br>
👉 <b>X축을 1/r²로 바꿔</b> 그래프를 선형화해 봅시다!
</div>
""", unsafe_allow_html=True)

    else:
        # ── 2차: 1/r² vs E 선형화 ──
        st.markdown("""
<div class='step-header'>③ 2차 그래프: 1/r² vs E — 선형화(Linearization)</div>
""", unsafe_allow_html=True)
        st.markdown("""
**선형화 원리:**

$$E = kQ \\cdot \\frac{1}{r^2}$$

X축을 $\\frac{1}{r^2}$으로 놓으면: $E = kQ \\cdot X$ → **원점을 지나는 직선!**

**관찰 포인트:**
- 그래프가 직선이 되나요?
- 직선이 원점(0, 0)을 통과하나요?
- 기울기는 얼마인가요? kQ 값과 비교해 보세요.
""")

        # 선형 회귀
        coeffs = np.polyfit(ir2_arr, E_arr, 1)
        slope, intercept = coeffs[0], coeffs[1]
        kQ_theory = K_E * Q_nC * Q_UNIT

        # 측정 데이터
        fig2.add_trace(go.Scatter(
            x=ir2_arr, y=E_arr,
            mode='markers',
            marker=dict(size=11, color='#facc15',
                        line=dict(color='white', width=1.5)),
            name='측정 데이터',
            hovertemplate='1/r² = %{x:.4f}<br>E = %{y:.2f} N/C<extra></extra>'
        ))

        # 선형 회귀선
        x_line = np.linspace(0, max(ir2_arr) * 1.1, 100)
        y_line = slope * x_line + intercept
        fig2.add_trace(go.Scatter(
            x=x_line, y=y_line,
            mode='lines',
            line=dict(color='#f87171', width=2.5),
            name=f'회귀직선: 기울기 = {slope:.4f}'
        ))

        # 원점 통과 이론선
        y_theory = kQ_theory * x_line
        fig2.add_trace(go.Scatter(
            x=x_line, y=y_theory,
            mode='lines',
            line=dict(color='rgba(100,200,100,0.6)', width=2, dash='dash'),
            name=f'이론선: 기울기 = kQ = {kQ_theory:.4f}'
        ))

        # 원점 강조
        fig2.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            marker=dict(size=12, color='white', symbol='x', line=dict(color='white', width=2)),
            name='원점 (0, 0)', showlegend=True
        ))

        fig2.update_layout(
            xaxis=dict(title='1/r² (m⁻²)', showgrid=True, gridcolor='rgba(255,255,255,0.1)',
                       rangemode='tozero'),
            yaxis=dict(title='전기장 E (N/C)', showgrid=True, gridcolor='rgba(255,255,255,0.1)',
                       rangemode='tozero'),
            plot_bgcolor='#0d1117', paper_bgcolor='#0d1117',
            font=dict(color='#e2e8f0'),
            legend=dict(bgcolor='rgba(0,0,0,0.5)', bordercolor='rgba(255,255,255,0.2)', borderwidth=1),
            height=430, margin=dict(l=60, r=20, t=40, b=60)
        )
        st.plotly_chart(fig2, use_container_width=True)

        # 분석 결과
        error_pct = abs(slope - kQ_theory) / kQ_theory * 100
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("회귀 직선 기울기", f"{slope:.4f}")
        with col_r2:
            st.metric("이론값 kQ", f"{kQ_theory:.4f}",
                      delta=f"{slope - kQ_theory:+.4f}")
        with col_r3:
            st.metric("오차율", f"{error_pct:.2f} %")

        st.markdown(f"""
<div class='result-box'>
✅ <b>선형화 결론</b><br>
X축을 <b>1/r²</b>로 바꾸면 그래프가 <b>원점을 지나는 직선</b>이 됩니다.<br>
직선의 기울기 = <b>{slope:.4f}</b> ≈ kQ = k × {Q_nC:.0f} nC = <b>{kQ_theory:.4f}</b><br>
→ 따라서 전기장 세기는 <b>E = kQ · (1/r²)</b> 임을 실험적으로 확인했습니다!
</div>
""", unsafe_allow_html=True)

        st.latex(r"E = k \frac{Q}{r^2} \quad \Leftrightarrow \quad E = kQ \cdot \frac{1}{r^2}")
        st.markdown("이 식에서 $X = \\frac{1}{r^2}$으로 놓으면 $E = kQ \\cdot X$ 로 **직선 관계**가 됩니다.")

    # ── 탐구 정리 ──
    st.markdown("---")
    with st.expander("📝 탐구 정리 및 토론", expanded=False):
        st.markdown("""
### 탐구 결론

| 그래프 | X축 | Y축 | 모양 | 의미 |
|--------|-----|-----|------|------|
| 1차 | r | E | 반비례 곡선 | E ∝ 1/r² 임을 암시 |
| 2차 | 1/r² | E | **원점 통과 직선** | E = kQ·(1/r²) 확인 |

### 토론 주제
1. **기울기의 물리적 의미**: 직선의 기울기가 kQ인 이유는?
2. **전하량 Q가 달라지면**: 기울기는 어떻게 변할까? 활동 1에서 Q를 바꿔 비교해 보세요.
3. **실제 응용**: 이 관계를 이용하면 측정된 전기장으로부터 전하량 Q를 역으로 구할 수 있을까요?

### 핵심 정리
$$E = k \\frac{Q}{r^2}, \\quad k = 8.99 \\times 10^9 \\text{ N·m}^2/\\text{C}^2$$
        """)
