"""
중력장과 전기장 비교 시뮬레이션
================================
중력장(g)과 전기장(E)의 개념적 유사성을 시각화하는 수업 도입 자료
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🌌 [수업 자료] 중력장과 전기장의 비교 시뮬레이션")
st.markdown("---")

# 사이드바에서 수업 단계 제어
st.sidebar.header("🏫 수업 단계 선택")
step = st.sidebar.radio(
    "진행 단계를 선택하세요:",
    ("1단계: 지표면의 균일한 중력장 (g)", "2단계: 균일한 전기장 (E)")
)

# --- 1단계: 중력장 시뮬레이션 구현 ---
if "1단계" in step:
    st.subheader("STAGE 1: 균일한 중력장 ($g$) 속에서의 힘")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        
        # 1. 배경 중력장 화살표 (아래 방향)
        for x in np.linspace(1, 9, 5):
            fig.add_trace(go.Scatter(
                x=[x, x], y=[8, 2],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(52, 152, 219, 0.2)", width=2, dash="dash"),
                showlegend=False
            ))
            
        # 2. 물체 A (질량 m)
        fig.add_trace(go.Scatter(
            x=[3], y=[5], mode="markers+text",
            marker=dict(size=30, color="#7f8c8d"),
            text=["m"], textposition="inside",
            name="물체 A (질량 m)"
        ))
        fig.add_trace(go.Scatter(
            x=[3, 3], y=[5, 3.5], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#2c3e50", width=4),
            name="중력 F = mg"
        ))
        
        # 3. 물체 B (질량 2m)
        fig.add_trace(go.Scatter(
            x=[7], y=[5], mode="markers+text",
            marker=dict(size=45, color="#34495e"),
            text=["2m"], textposition="inside",
            name="물체 B (질량 2m)"
        ))
        fig.add_trace(go.Scatter(
            x=[7, 7], y=[5, 2.0], mode="lines+markers",
            marker=dict(symbol="arrow", size=15, angleref="previous"),
            line=dict(color="#2c3e50", width=6),
            name="중력 F = 2mg"
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            title="지표면 근처의 균일한 중력장 요약",
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.info("""
        **💡 수업 지도 핵심**
        * **배경의 흐린 화살표**는 지구 때문에 생긴 **중력장($g$)** 공간을 의미합니다.
        * 공간의 성질($g$)은 어디서나 일정하지만, **질량이 큰 물체($2m$)**가 더 강한 **중력($F=mg$)**을 받습니다.
        """)
        st.warning("👉 확인 질문: 두 물체의 질량은 다르지만, 이 공간의 '중력 가속도 $g$' 값은 서로 같을까요?")

# --- 2단계: 전기장 시뮬레이션 구현 ---
else:
    st.subheader("STAGE 2: 균일한 전기장 ($E$) 속에서의 힘")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = go.Figure()
        
        # 1. 배경 전기장 화살표 (오른쪽 방향)
        for y in np.linspace(1, 9, 5):
            fig.add_trace(go.Scatter(
                x=[1, 9], y=[y, y],
                mode="lines+markers",
                marker=dict(symbol="arrow", size=10, angleref="previous"),
                line=dict(color="rgba(231, 76, 60, 0.2)", width=2, dash="dash"),
                showlegend=False
            ))
            
        # 2. 양전하 (+2q)
        fig.add_trace(go.Scatter(
            x=[4], y=[7], mode="markers+text",
            marker=dict(size=40, color="#e74c3c"),
            text=["+2q"], textposition="inside",
            name="양전하 (+2q)"
        ))
        fig.add_trace(go.Scatter(
            x=[4, 6.5], y=[7, 7], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#d35400", width=5),
            name="전기력 F = 2qE (장과 같은 방향)"
        ))
        
        # 3. 음전하 (-q)
        fig.add_trace(go.Scatter(
            x=[6], y=[3], mode="markers+text",
            marker=dict(size=30, color="#9b59b6"),
            text=["-q"], textposition="inside",
            name="음전하 (-q)"
        ))
        fig.add_trace(go.Scatter(
            x=[6, 4.75], y=[3, 3], mode="lines+markers",
            marker=dict(symbol="arrow", size=12, angleref="previous"),
            line=dict(color="#8e44ad", width=4),
            name="전기력 F = -qE (장과 반대 방향)"
        ))
        
        fig.update_layout(
            xaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[0, 10], showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            title="평행 전극판 사이의 균일한 전기장 요약",
            template="plotly_white",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.error("""
        **💡 수업 지도 핵심**
        * 배경의 붉은 화살표는 전하 때문에 성질이 변한 **전기장($E$)** 공간입니다.
        * 중력 공식 $F=mg$에서 **질량($m$) 대신 전하량($q$)**을, **중력장($g$) 대신 전기장($E$)**을 넣으면 전기력 공식 $F=qE$가 됩니다.
        * **주의할 점:** 질량은 항상 (+)이지만, 전하는 (-) 부호가 있으므로 전기장과 반대로 힘을 받기도 합니다!
        """)
        st.success("✍️ 공통점 도출: 두 현상 모두 '공간의 성질'과 '물체의 특성'이 곱해져 힘이 결정됩니다.")
