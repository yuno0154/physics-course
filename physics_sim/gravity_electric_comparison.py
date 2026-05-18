"""
중력장과 전기장 비교 시뮬레이션
================================
중력장(g)과 전기장(E)의 개념적 유사성을 단계적으로 시각화하는 수업 도입 자료
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🌌 [수업 자료] 중력장과 전기장의 비교")
st.markdown("""
<div style='background:linear-gradient(135deg,#1e2a3a,#0f1a2a);border-left:4px solid #3b82f6;
border-radius:8px;padding:14px 18px;margin-bottom:18px;'>
<b style='color:#93c5fd;'>🎯 학습 목표</b><br>
<span style='color:#e2e8f0;font-size:0.93rem;'>
만유인력 법칙과 쿨롱 법칙으로부터 <b>장(Field)</b>의 개념이 어떻게 도출되는지 이해하고,<br>
중력장(<i>g</i>)과 전기장(<i>E</i>)의 유사성을 비교합니다.
</span></div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["⚖️ 1단계: 균일한 중력장 (g)", "⚡ 2단계: 균일한 전기장 (E)", "📊 3단계: 비교 정리"])

# ═══════════════════════════════════════════════════════════
# 1단계: 중력장
# ═══════════════════════════════════════════════════════════
with tab1:
    st.subheader("STAGE 1: 균일한 중력장 속에서의 힘")

    # ── 식 단계별 유도 ──────────────────────────────────────
    st.markdown("### 📐 중력장 g의 근원: 만유인력 법칙으로부터")

    col_eq1, col_eq2, col_eq3 = st.columns(3)
    with col_eq1:
        st.markdown("""
<div style='background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.4);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#93c5fd;font-weight:700;margin-bottom:8px;'>① 뉴턴의 만유인력 법칙 (지구와 물체 사이)</div>
<div style='font-size:1.1rem;color:#e2e8f0;'>
$$F = G\\frac{Mm}{r^2}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:8px;'>
G: 만유인력 상수<br>M: 지구 질량, m: 물체 질량<br>r: 지구 중심까지 거리
</div></div>
""", unsafe_allow_html=True)
    with col_eq2:
        st.markdown("""
<div style='background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.5);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#93c5fd;font-weight:700;margin-bottom:8px;'>② 식 정리 → g 정의</div>
<div style='font-size:1.1rem;color:#e2e8f0;'>
$$F = m \\cdot \\underbrace{\\frac{GM}{r^2}}_{g}$$
</div>
<div style='color:#fbbf24;font-size:0.9rem;margin-top:8px;font-weight:600;'>
$$g \\equiv \\frac{GM}{r^2}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:4px;'>
g는 <b>지구(M)</b>가 공간에 만드는 성질<br>물체의 질량 m과 무관
</div></div>
""", unsafe_allow_html=True)
    with col_eq3:
        st.markdown("""
<div style='background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.4);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#86efac;font-weight:700;margin-bottom:8px;'>③ 최종 결과</div>
<div style='font-size:1.2rem;color:#e2e8f0;font-weight:700;'>
$$\\boxed{F = mg}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:8px;'>
<b>공간의 성질</b>(g) × <b>물체의 특성</b>(m)<br>
= 물체가 받는 힘(F)
</div></div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖼️ 균일한 중력장 시각화")
    col_fig, col_info = st.columns([3, 1])

    with col_fig:
        fig1 = go.Figure()

        # 배경 중력장 화살표 (아래 방향)
        for x in np.linspace(1, 9, 5):
            fig1.add_trace(go.Scatter(
                x=[x, x], y=[8.5, 2],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(52,152,219,0.25)", width=2, dash="dash"),
                showlegend=False
            ))
        # g 레이블
        fig1.add_annotation(x=9.3, y=5.2, text="<b>g</b>↓", font=dict(size=14, color="#3498db"), showarrow=False)

        # 물체 A (질량 m)
        fig1.add_trace(go.Scatter(
            x=[3], y=[5.5], mode="markers+text",
            marker=dict(size=32, color="#7f8c8d"),
            text=["m"], textposition="middle center",
            textfont=dict(color="white", size=13),
            name="물체 A (질량 m)"
        ))
        # 중력 F=mg
        fig1.add_trace(go.Scatter(
            x=[3, 3], y=[5.5, 3.8], mode="lines+markers",
            marker=dict(symbol="arrow", size=13, angleref="previous"),
            line=dict(color="#2c3e50", width=4),
            name="F = mg"
        ))
        fig1.add_annotation(x=2.4, y=4.6, text="F=mg", font=dict(size=11, color="#2c3e50"), showarrow=False)

        # 물체 B (질량 2m)
        fig1.add_trace(go.Scatter(
            x=[7], y=[5.5], mode="markers+text",
            marker=dict(size=48, color="#34495e"),
            text=["2m"], textposition="middle center",
            textfont=dict(color="white", size=13),
            name="물체 B (질량 2m)"
        ))
        # 중력 F=2mg
        fig1.add_trace(go.Scatter(
            x=[7, 7], y=[5.5, 2.3], mode="lines+markers",
            marker=dict(symbol="arrow", size=16, angleref="previous"),
            line=dict(color="#2c3e50", width=6),
            name="F = 2mg"
        ))
        fig1.add_annotation(x=6.3, y=3.9, text="F=2mg", font=dict(size=11, color="#2c3e50"), showarrow=False)

        fig1.update_layout(
            xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            height=430, template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=20, r=30, t=20, b=20)
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col_info:
        st.info("""
**💡 핵심 개념**

$g = \\dfrac{GM}{r^2}$

은 **지구(M)**가 주변 공간에 만들어 놓은 **중력장**입니다.

물체 m이 크든 작든 g값은 **동일**하지만, 힘 F=mg는 질량에 **비례**합니다.
        """)
        st.warning("🔍 질문: 두 물체의 질량은 다르지만 g 값은 같을까요?")

# ═══════════════════════════════════════════════════════════
# 2단계: 전기장
# ═══════════════════════════════════════════════════════════
with tab2:
    st.subheader("STAGE 2: 균일한 전기장 속에서의 힘")

    # ── 식 단계별 유도 ──────────────────────────────────────
    st.markdown("### 📐 전기장 E의 근원: 쿨롱 법칙으로부터")

    col_eq1, col_eq2, col_eq3 = st.columns(3)
    with col_eq1:
        st.markdown("""
<div style='background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.4);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#fca5a5;font-weight:700;margin-bottom:8px;'>① 쿨롱의 법칙 (전하와 전하 사이)</div>
<div style='font-size:1.1rem;color:#e2e8f0;'>
$$F = k\\frac{Qq}{r^2}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:8px;'>
k: 쿨롱 상수 (8.99×10⁹)<br>Q: 원천 전하, q: 시험 전하<br>r: 전하 간 거리
</div></div>
""", unsafe_allow_html=True)
    with col_eq2:
        st.markdown("""
<div style='background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.5);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#fca5a5;font-weight:700;margin-bottom:8px;'>② 식 정리 → E 정의</div>
<div style='font-size:1.1rem;color:#e2e8f0;'>
$$F = q \\cdot \\underbrace{\\frac{kQ}{r^2}}_{E}$$
</div>
<div style='color:#fbbf24;font-size:0.9rem;margin-top:8px;font-weight:600;'>
$$E \\equiv \\frac{kQ}{r^2}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:4px;'>
E는 <b>원천 전하(Q)</b>가 공간에 만드는 성질<br>시험 전하 q의 크기와 무관
</div></div>
""", unsafe_allow_html=True)
    with col_eq3:
        st.markdown("""
<div style='background:rgba(34,197,94,0.1);border:1px solid rgba(34,197,94,0.4);
border-radius:8px;padding:16px;text-align:center;'>
<div style='color:#86efac;font-weight:700;margin-bottom:8px;'>③ 최종 결과</div>
<div style='font-size:1.2rem;color:#e2e8f0;font-weight:700;'>
$$\\boxed{F = qE}$$
</div>
<div style='color:#94a3b8;font-size:0.82rem;margin-top:8px;'>
<b>공간의 성질</b>(E) × <b>물체의 특성</b>(q)<br>
= 물체가 받는 힘(F)<br>
<span style='color:#fca5a5;'>단, q &lt; 0이면 반대 방향!</span>
</div></div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🖼️ 균일한 전기장 시각화")
    col_fig2, col_info2 = st.columns([3, 1])

    with col_fig2:
        fig2 = go.Figure()

        # 배경 전기장 화살표 (오른쪽)
        for y in np.linspace(1, 9, 5):
            fig2.add_trace(go.Scatter(
                x=[0.5, 9.5], y=[y, y],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(231,76,60,0.25)", width=2, dash="dash"),
                showlegend=False
            ))
        fig2.add_annotation(x=5, y=9.6, text="→ <b>E</b> →", font=dict(size=14, color="#e74c3c"), showarrow=False)

        # 양전하 +2q
        fig2.add_trace(go.Scatter(
            x=[4], y=[7], mode="markers+text",
            marker=dict(size=42, color="#e74c3c"),
            text=["+2q"], textposition="middle center",
            textfont=dict(color="white", size=12),
            name="양전하 (+2q)"
        ))
        fig2.add_trace(go.Scatter(
            x=[4, 6.8], y=[7, 7], mode="lines+markers",
            marker=dict(symbol="arrow", size=13, angleref="previous"),
            line=dict(color="#d35400", width=5),
            name="F = 2qE (→ E 방향)"
        ))
        fig2.add_annotation(x=5.4, y=7.5, text="F=2qE →", font=dict(size=11, color="#d35400"), showarrow=False)

        # 음전하 -q
        fig2.add_trace(go.Scatter(
            x=[6], y=[3], mode="markers+text",
            marker=dict(size=32, color="#9b59b6"),
            text=["-q"], textposition="middle center",
            textfont=dict(color="white", size=12),
            name="음전하 (-q)"
        ))
        fig2.add_trace(go.Scatter(
            x=[6, 4.6], y=[3, 3], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#8e44ad", width=4),
            name="F = -qE (← E 반대)"
        ))
        fig2.add_annotation(x=5.3, y=3.5, text="← F=-qE", font=dict(size=11, color="#8e44ad"), showarrow=False)

        fig2.update_layout(
            xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            height=430, template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig2, use_container_width=True)

    with col_info2:
        st.error("""
**💡 핵심 개념**

$E = \\dfrac{kQ}{r^2}$

은 **원천 전하(Q)**가 주변 공간에 만들어 놓은 **전기장**입니다.

**⚠️ 중력과의 차이:**
질량은 항상 (+)이지만, 전하 q는 (−)가 될 수 있어 **반대 방향**으로 힘을 받습니다.
        """)
        st.success("✍️ F = qE 에서 q < 0이면 힘의 방향이 E와 반대!")

# ═══════════════════════════════════════════════════════════
# 3단계: 비교 정리
# ═══════════════════════════════════════════════════════════
with tab3:
    st.subheader("📊 중력장과 전기장 비교 정리")

    st.markdown("""
| 구분 | 중력 (Gravity) | 전기력 (Electric Force) |
|------|---------------|------------------------|
| 기본 법칙 | 만유인력: $F = G\\dfrac{Mm}{r^2}$ | 쿨롱 법칙: $F = k\\dfrac{Qq}{r^2}$ |
| **장(Field) 정의** | $g \\equiv \\dfrac{GM}{r^2}$ | $E \\equiv \\dfrac{kQ}{r^2}$ |
| 장을 만드는 것 | 지구(질량 M) | 원천 전하(Q) |
| 힘 공식 | $F = mg$ | $F = qE$ |
| 물체의 특성 | 질량 m (항상 양수) | 전하량 q (양수 or 음수) |
| 방향 | 항상 장과 같은 방향 | q > 0: 장과 같은 방향<br>q < 0: 장과 반대 방향 |
""")

    st.markdown("---")
    st.markdown("""
<div style='background:rgba(124,58,237,0.1);border:1px solid rgba(124,58,237,0.4);
border-radius:10px;padding:18px 22px;'>
<b style='color:#c4b5fd;font-size:1.05rem;'>🔑 핵심 통찰: "장(Field)"의 의미</b><br><br>
<span style='color:#e2e8f0;'>
두 법칙 모두 <b>공간의 성질(장)</b>과 <b>물체의 특성</b>이 곱해져 힘이 결정됩니다.<br><br>
</span>
<div style='display:flex;gap:20px;'>
<div style='flex:1;background:rgba(59,130,246,0.1);border-radius:8px;padding:12px;text-align:center;'>
<div style='color:#93c5fd;font-weight:700;'>중력</div>
<div style='color:#e2e8f0;margin-top:6px;'>F = <span style='color:#fbbf24;'>g</span> × <span style='color:#86efac;'>m</span></div>
<div style='color:#94a3b8;font-size:0.8rem;'>공간의 성질 × 물체 특성</div>
</div>
<div style='flex:1;background:rgba(239,68,68,0.1);border-radius:8px;padding:12px;text-align:center;'>
<div style='color:#fca5a5;font-weight:700;'>전기력</div>
<div style='color:#e2e8f0;margin-top:6px;'>F = <span style='color:#fbbf24;'>E</span> × <span style='color:#86efac;'>q</span></div>
<div style='color:#94a3b8;font-size:0.8rem;'>공간의 성질 × 물체 특성</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 **다음 활동**: 점전하 주위의 전기장 세기 E가 거리 r에 따라 어떻게 변하는지 직접 측정해 봅시다! → **[실험] 전기장 세기 탐구** 페이지로 이동")
