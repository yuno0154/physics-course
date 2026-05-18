"""
중력장과 전기장 비교 시뮬레이션
================================
중력장(g)과 전기장(E)의 개념적 유사성을 단계적으로 시각화하는 수업 도입 자료
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🌌 서로 떨어진 두 물체 사이에 힘은 어떻게 작용하는 것일까?")
st.subheader("[수업 자료] 중력장과 전기장의 비교")
st.markdown("""
<div style='background:linear-gradient(135deg,#1e2a3a,#0f1a2a);border-left:4px solid #3b82f6;
border-radius:8px;padding:14px 18px;margin-bottom:18px;'>
<b style='color:#93c5fd;'>🎯 학습 목표</b><br>
<span style='color:#e2e8f0;font-size:0.93rem;'>
만유인력 법칙과 쿨롱 법칙으로부터 <b>장(Field)</b>의 개념이 어떻게 도출되는지 이해하고,<br>
중력장(<i>g</i>)과 전기장(<i>E</i>)의 유사성을 비교합니다.
</span><br><br>
<b style='color:#93c5fd;'>🔍 탐구 목표</b><br>
<span style='color:#e2e8f0;font-size:0.93rem;'>
장(field) 즉 힘이 작용하는 공간의 의미는 무엇일까?
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

    # 지구와 사과 다이어그램 (Plotly)
    fig_dia = go.Figure()
    # 지구 (큰 원)
    fig_dia.add_trace(go.Scatter(
        x=[2], y=[5], mode="markers+text",
        marker=dict(size=80, color="#3498db"),
        text=["<b>지구 (M)</b>"], textposition="middle center",
        textfont=dict(color="white", size=14),
        showlegend=False
    ))
    # 사과 (작은 원)
    fig_dia.add_trace(go.Scatter(
        x=[8], y=[5], mode="markers+text",
        marker=dict(size=25, color="#e74c3c"),
        text=["사과 (m)"], textposition="top center",
        textfont=dict(color="#e2e8f0", size=12),
        showlegend=False
    ))
    # 거리 r 표시선
    fig_dia.add_trace(go.Scatter(
        x=[2, 8], y=[3.5, 3.5], mode="lines+markers",
        marker=dict(symbol="line-ns-open", size=10),
        line=dict(color="#95a5a6", width=2, dash="dash"),
        showlegend=False
    ))
    # r 레이블
    fig_dia.add_annotation(
        x=5, y=2.8, text="거리 (r)",
        showarrow=False, font=dict(color="#95a5a6", size=13)
    )
    fig_dia.update_layout(
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[1, 7], showgrid=False, zeroline=False, showticklabels=False),
        height=150, template="plotly_white",
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_dia, use_container_width=True)

    # ── [추가] 장(Field)의 인과관계 시각화 시뮬레이션 ─────────────────
    st.markdown("#### 🔄 힘이 작용하는 2단계 과정 (장의 개념)")
    
    process_step = st.radio(
        "과정을 순서대로 확인해보세요:",
        ["1단계: 질량(지구)이 공간의 성질을 변화시킴 (장 형성)", 
         "2단계: 변화된 공간이 물체(사과)에 힘을 가함"],
        horizontal=True,
        key="grav_proc_step"
    )
    
    fig_proc = go.Figure()
    
    # 기본 요소: 지구 (모든 단계 공통)
    fig_proc.add_trace(go.Scatter(
        x=[2], y=[5], mode="markers+text",
        marker=dict(size=60, color="#3498db"),
        text=["<b>지구</b>"], textposition="middle center",
        textfont=dict(color="white", size=12),
        showlegend=False
    ))
    
    if "1단계" in process_step:
        # 중력장 화살표들 (지구를 향하는 방향)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r_val = 2.0
            dx = r_val * np.cos(angle)
            dy = r_val * np.sin(angle)
            fig_proc.add_trace(go.Scatter(
                x=[2 + dx, 2 + dx*0.3], y=[5 + dy, 5 + dy*0.3],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(52,152,219,0.5)", width=2),
                showlegend=False
            ))
        fig_proc.add_annotation(x=5, y=5, text="지구가 주변 공간의 성질을 변화시킴<br>(중력장 형성)", showarrow=False, font=dict(color="#93c5fd", size=12))
        
    elif "2단계" in process_step:
        # 중력장 화살표들 (배경에 흐릿하게)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r_val = 2.0
            dx = r_val * np.cos(angle)
            dy = r_val * np.sin(angle)
            fig_proc.add_trace(go.Scatter(
                x=[2 + dx, 2 + dx*0.3], y=[5 + dy, 5 + dy*0.3],
                mode="lines",
                line=dict(color="rgba(52,152,219,0.15)", width=1),
                showlegend=False
            ))
            
        # 사과 등장
        fig_proc.add_trace(go.Scatter(
            x=[8], y=[5], mode="markers+text",
            marker=dict(size=20, color="#e74c3c"),
            text=["사과"], textposition="top center",
            textfont=dict(color="#e2e8f0", size=12),
            showlegend=False
        ))
        
        # 사과가 받는 힘 화살표 (지구 방향)
        fig_proc.add_trace(go.Scatter(
            x=[8, 5.5], y=[5, 5], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#e74c3c", width=4),
            showlegend=False
        ))
        fig_proc.add_annotation(x=6.5, y=5.8, text="변화된 공간이<br>사과에 힘(중력)을 가함", showarrow=False, font=dict(color="#fca5a5", size=12))

    fig_proc.update_layout(
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[2, 8], showgrid=False, zeroline=False, showticklabels=False),
        height=180, template="plotly_white",
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_proc, use_container_width=True)
    st.markdown("---")

    col_eq1, col_eq2, col_eq3 = st.columns(3)
    with col_eq1:
        st.markdown("<div style='text-align:center; color:#93c5fd; font-weight:700;'>① 뉴턴의 만유인력 법칙 (지구와 물체 사이)</div>", unsafe_allow_html=True)
        st.latex(r"F = G\frac{Mm}{r^2}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'>G: 만유인력 상수<br>M: 지구 질량, m: 물체 질량<br>r: 지구 중심까지 거리</div>", unsafe_allow_html=True)
    with col_eq2:
        st.markdown("<div style='text-align:center; color:#93c5fd; font-weight:700;'>② 식 정리 → g 정의</div>", unsafe_allow_html=True)
        st.latex(r"F = m \cdot \underbrace{\frac{GM}{r^2}}_{g}")
        st.latex(r"g \equiv \frac{GM}{r^2}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'>g는 <b>지구(M)</b>가 공간에 만드는 성질<br>물체의 질량 m과 무관</div>", unsafe_allow_html=True)
    with col_eq3:
        st.markdown("<div style='text-align:center; color:#86efac; font-weight:700;'>③ 최종 결과</div>", unsafe_allow_html=True)
        st.latex(r"\boxed{F = mg}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'><b>공간의 성질</b>(g) × <b>물체의 특성</b>(m)<br>= 물체가 받는 힘(F)</div>", unsafe_allow_html=True)

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
        st.warning("🔍 질문: g값이 같은 이유는 무엇일까요?")

# ═══════════════════════════════════════════════════════════
# 2단계: 전기장
# ═══════════════════════════════════════════════════════════
with tab2:
    st.subheader("STAGE 2: 균일한 전기장 속에서의 힘")

    # ── 식 단계별 유도 ──────────────────────────────────────
    st.markdown("### 📐 전기장 E의 근원: 쿨롱 법칙으로부터")

    # 전하 다이어그램 (Plotly)
    fig_dia2 = go.Figure()
    # 원천 전하 Q (큰 원)
    fig_dia2.add_trace(go.Scatter(
        x=[2], y=[5], mode="markers+text",
        marker=dict(size=70, color="#e74c3c"),
        text=["<b>원천 전하 (Q)</b>"], textposition="middle center",
        textfont=dict(color="white", size=12),
        showlegend=False
    ))
    # 시험 전하 q (작은 원)
    fig_dia2.add_trace(go.Scatter(
        x=[8], y=[5], mode="markers+text",
        marker=dict(size=30, color="#e74c3c"),
        text=["시험 전하 (q)"], textposition="top center",
        textfont=dict(color="#e2e8f0", size=12),
        showlegend=False
    ))
    # 거리 r 표시선
    fig_dia2.add_trace(go.Scatter(
        x=[2, 8], y=[3.5, 3.5], mode="lines+markers",
        marker=dict(symbol="line-ns-open", size=10),
        line=dict(color="#95a5a6", width=2, dash="dash"),
        showlegend=False
    ))
    # r 레이블
    fig_dia2.add_annotation(
        x=5, y=2.8, text="거리 (r)",
        showarrow=False, font=dict(color="#95a5a6", size=13)
    )
    fig_dia2.update_layout(
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[1, 7], showgrid=False, zeroline=False, showticklabels=False),
        height=150, template="plotly_white",
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_dia2, use_container_width=True)

    # ── [추가] 장(Field)의 인과관계 시각화 시뮬레이션 (전기장) ───────
    st.markdown("#### 🔄 힘이 작용하는 2단계 과정 (장의 개념)")
    
    process_step_elec = st.radio(
        "과정을 순서대로 확인해보세요:",
        ["1단계: 원천전하(Q)가 공간의 성질을 변화시킴 (장 형성)", 
         "2단계: 변화된 공간이 시험전하(q)에 힘을 가함"],
        horizontal=True,
        key="elec_proc_step"
    )
    
    fig_proc2 = go.Figure()
    
    # 기본 요소: 원천 전하 Q (모든 단계 공통)
    fig_proc2.add_trace(go.Scatter(
        x=[2], y=[5], mode="markers+text",
        marker=dict(size=60, color="#e74c3c"),
        text=["<b>Q</b>"], textposition="middle center",
        textfont=dict(color="white", size=12),
        showlegend=False
    ))
    
    if "1단계" in process_step_elec:
        # 전기장 화살표들 (나가는 방향)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r_val = 2.0
            dx = r_val * np.cos(angle)
            dy = r_val * np.sin(angle)
            # 화살표는 밖을 향해야 하므로
            fig_proc2.add_trace(go.Scatter(
                x=[2 + dx*0.3, 2 + dx], y=[5 + dy*0.3, 5 + dy],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(231,76,60,0.5)", width=2),
                showlegend=False
            ))
        fig_proc2.add_annotation(x=5, y=5, text="원천 전하가 주변 공간의 성질을 변화시킴<br>(전기장 형성)", showarrow=False, font=dict(color="#fca5a5", size=12))
        
    elif "2단계" in process_step_elec:
        # 전기장 화살표들 (배경에 흐릿하게)
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            r_val = 2.0
            dx = r_val * np.cos(angle)
            dy = r_val * np.sin(angle)
            fig_proc2.add_trace(go.Scatter(
                x=[2 + dx*0.3, 2 + dx], y=[5 + dy*0.3, 5 + dy],
                mode="lines",
                line=dict(color="rgba(231,76,60,0.15)", width=1),
                showlegend=False
            ))
            
        # 시험 전하 q 등장
        fig_proc2.add_trace(go.Scatter(
            x=[8], y=[5], mode="markers+text",
            marker=dict(size=20, color="#e74c3c"),
            text=["q"], textposition="top center",
            textfont=dict(color="#e2e8f0", size=12),
            showlegend=False
        ))
        
        # q가 받는 힘 화살표 (오른쪽 방향, 척력 가정)
        fig_proc2.add_trace(go.Scatter(
            x=[8, 9.5], y=[5, 5], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#e74c3c", width=4),
            showlegend=False
        ))
        fig_proc2.add_annotation(x=6.5, y=5.8, text="변화된 공간이<br>시험 전하에 힘을 가함", showarrow=False, font=dict(color="#fca5a5", size=12))

    fig_proc2.update_layout(
        xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[2, 8], showgrid=False, zeroline=False, showticklabels=False),
        height=180, template="plotly_white",
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_proc2, use_container_width=True)
    st.markdown("---")

    col_eq1, col_eq2, col_eq3 = st.columns(3)
    with col_eq1:
        st.markdown("<div style='text-align:center; color:#fca5a5; font-weight:700;'>① 쿨롱의 법칙 (전하와 전하 사이)</div>", unsafe_allow_html=True)
        st.latex(r"F = k\frac{Qq}{r^2}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'>k: 쿨롱 상수 (8.99×10⁹)<br>Q: 원천 전하, q: 시험 전하<br>r: 전하 간 거리</div>", unsafe_allow_html=True)
    with col_eq2:
        st.markdown("<div style='text-align:center; color:#fca5a5; font-weight:700;'>② 식 정리 → E 정의</div>", unsafe_allow_html=True)
        st.latex(r"F = q \cdot \underbrace{\frac{kQ}{r^2}}_{E}")
        st.latex(r"E \equiv \frac{kQ}{r^2}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'>E는 <b>원천 전하(Q)</b>가 공간에 만드는 성질<br>시험 전하 q의 크기와 무관</div>", unsafe_allow_html=True)
    with col_eq3:
        st.markdown("<div style='text-align:center; color:#86efac; font-weight:700;'>③ 최종 결과</div>", unsafe_allow_html=True)
        st.latex(r"\boxed{F = qE}")
        st.markdown("<div style='text-align:center; color:#94a3b8; font-size:0.82rem;'><b>공간의 성질</b>(E) × <b>물체의 특성</b>(q)<br>= 물체가 받는 힘(F)<br><span style='color:#fca5a5;'>단, q &lt; 0이면 반대 방향!</span></div>", unsafe_allow_html=True)

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
        st.warning("🔍 질문: E값이 같은 이유는 무엇일까요?")

# ═══════════════════════════════════════════════════════════
# 3단계: 비교 정리
# ═══════════════════════════════════════════════════════════
with tab3:
    st.subheader("📊 중력장과 전기장 비교 정리")

    st.markdown("""
| 구분 | 중력 (Gravity) | 전기력 (Electric Force) |
|---|---|---|
| 기본 법칙 | <details><summary>🔍 보기</summary>만유인력: $F = G\\dfrac{Mm}{r^2}$</details> | <details><summary>🔍 보기</summary>쿨롱 법칙: $F = k\\dfrac{Qq}{r^2}$</details> |
| **장(Field) 정의** | <details><summary>🔍 보기</summary>$g \\equiv \\dfrac{GM}{r^2}$</details> | <details><summary>🔍 보기</summary>$E \\equiv \\dfrac{kQ}{r^2}$</details> |
| 장을 만드는 것 | <details><summary>🔍 보기</summary>지구(질량 M)</details> | <details><summary>🔍 보기</summary>원천 전하(Q)</details> |
| 힘 공식 | <details><summary>🔍 보기</summary>$F = mg$</details> | <details><summary>🔍 보기</summary>$F = qE$</details> |
| 물체의 특성 | <details><summary>🔍 보기</summary>질량 m (항상 양수)</details> | <details><summary>🔍 보기</summary>전하량 q (양수 or 음수)</details> |
| 방향 | <details><summary>🔍 보기</summary>항상 장과 같은 방향</details> | <details><summary>🔍 보기</summary>q > 0: 장과 같은 방향<br>q < 0: 장과 반대 방향</details> |
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📝 스스로 확인해보기")
    ans = st.text_input("전기장의 정의($E$)를 식으로 작성해보세요: (예: E = kQ/r^2)", key="elec_def_input")
    if ans:
        ans_clean = ans.replace(" ", "")
        if 'k' in ans_clean and 'Q' in ans_clean and ('r^2' in ans_clean or 'r**2' in ans_clean) and 'E=' in ans_clean:
            st.success("🎉 정답입니다! 원천 전하 $Q$가 거리 $r$인 지점에 만드는 전기장의 세기는 $E = k\\dfrac{Q}{r^2}$ 입니다. 이는 쿨롱의 법칙에서 시험 전하 $q$를 나눈 값과 같습니다.")
        elif 'k' in ans_clean and 'Q' in ans_clean and ('r^2' in ans_clean or 'r**2' in ans_clean):
             st.success("🎉 거의 맞았습니다! $k\\dfrac{Q}{r^2}$ 꼴을 잘 찾아냈습니다. 좌변에 $E =$ 까지 써주면 완벽합니다!")
        else:
            st.warning("🤔 조금 더 생각해보세요! 쿨롱의 법칙 $F = k\\dfrac{Qq}{r^2}$ 에서 시험 전하 $q$를 제외한(나눈) 부분이 전기장의 정의입니다.")

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
