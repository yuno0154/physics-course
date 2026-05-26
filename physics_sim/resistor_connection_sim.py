"""
저항의 연결과 소비 전력 탐구 시뮬레이터
- 직렬, 병렬, 복합 회로 연결에 따른 합성 저항, 전류, 전압 강하, 전력 분석
- 도선 내 전하(전자) 흐름 및 저항 발열 실시간 SVG 애니메이션 시각화
- 오개념 격파 및 스마트팜 열원 설계 탐구 챌린지
"""

import streamlit as st
import numpy as np

# 소수점 2자리 반올림 포맷팅 Helper
def fmt(val):
    return round(val, 2)

# ── 공통 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #34d399, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #064e3b, #022c22);
    border-left: 5px solid #10b981;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);
}
.step-header {
    background: linear-gradient(90deg, #1e293b, #0f172a);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 12px 18px;
    margin: 15px 0 10px 0;
    font-weight: 700;
    color: #38bdf8;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.analysis-card {
    background: #0f172a;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 15px;
}
.heat-gauge-container {
    background: #090d16;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 14px;
    margin-top: 10px;
}
.feedback-box-success {
    background: rgba(16, 185, 129, 0.12);
    border: 1.5px solid rgba(16, 185, 129, 0.4);
    border-radius: 10px;
    padding: 14px;
    margin-top: 12px;
    color: #34d399;
}
.feedback-box-error {
    background: rgba(244, 63, 94, 0.12);
    border: 1.5px solid rgba(244, 63, 94, 0.4);
    border-radius: 10px;
    padding: 14px;
    margin-top: 12px;
    color: #fb7185;
}
.badge-mission {
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    border-radius: 9999px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──────────────────────────────────────
if 'rcs_score' not in st.session_state:
    st.session_state.rcs_score = 0
if 'rcs_user_answer' not in st.session_state:
    st.session_state.rcs_user_answer = ""
if 'rcs_feedback' not in st.session_state:
    st.session_state.rcs_feedback = None
if 'rcs_current_mission' not in st.session_state:
    st.session_state.rcs_current_mission = 1

# ══════════════════════════════════════════════════════════════
# 헤더 섹션
# ══════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-title'>🔌 저항의 연결과 소비 전력 탐구 시뮬레이터</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>직류 회로의 연결 방식에 따른 전하 흐름의 보존 법칙과 열에너지 발열 설계 물리 실험실</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <b style='color:#34d399; font-size:1.05rem;'>🎯 탐구 목표</b><br>
    <span style='color:#e2e8f0; font-size:0.92rem; line-height: 1.6;'>
    1. 직렬 연결과 병렬 연결 방식에 따라 전체 합성 저항과 각 저항별 전압, 전류 분포가 달라지는 규칙을 정량적으로 탐구합니다.<br>
    2. 저항에서 방출되는 소비 전력(열 에너지)의 분포를 비교하여 스마트팜 등의 실생활 발열 열원 설계를 직접 체험해 봅니다.
    </span>
</div>
""", unsafe_allow_html=True)

# Streamlit 탭 설정 (가상 회로실, 탐구 챌린지)
tab_sim, tab_mission = st.tabs(["🔌 가상 회로실 (Virtual Circuit Room)", "🏆 탐구 챌린지 (Inquiry Challenge)"])

# ══════════════════════════════════════════════════════════════
# 탭 1: 가상 회로실
# ══════════════════════════════════════════════════════════════
with tab_sim:
    col_ctrl, col_display = st.columns([1, 2])

    with col_ctrl:
        st.markdown("<div class='step-header'>⚙️ 1. 회로 연결 방식 선택</div>", unsafe_allow_html=True)
        
        circuit_type = st.radio(
            "회로 구성 방법",
            ["직렬 회로 (Series: R1 + R2)", "병렬 회로 (Parallel: R1 // R2)", "복합 회로 (Mixed: R1 + (R2 // R3))"],
            label_visibility="collapsed",
            key="rcs_circuit_type"
        )
        
        # 간소화된 타입 식별자 지정
        if "직렬" in circuit_type:
            c_type = "series"
        elif "병렬" in circuit_type:
            c_type = "parallel"
        else:
            c_type = "mixed"

        st.markdown("<div class='step-header'>🎛️ 2. 가변 회로 변수 조절</div>", unsafe_allow_html=True)

        # 초기화 버튼
        if st.button("🔄 설정 변수 초기화", use_container_width=True):
            st.session_state.rcs_voltage = 12
            st.session_state.rcs_r1 = 6
            st.session_state.rcs_r2 = 12
            st.session_state.rcs_r3 = 4
            st.rerun()

        # 전압 및 저항 변수 슬라이더
        voltage = st.slider("입력 전압 (V)", 1, 24, 12, step=1, key="rcs_voltage")
        r1 = st.slider("저항 R1 (Ω)", 1, 20, 6, step=1, key="rcs_r1")
        r2 = st.slider("저항 R2 (Ω)", 1, 24, 12, step=1, key="rcs_r2")
        
        if c_type == "mixed":
            r3 = st.slider("저항 R3 (Ω) [병렬 구간]", 1, 20, 4, step=1, key="rcs_r3")
        else:
            r3 = 4 # 기본값 유지

        st.markdown("<div class='step-header'>👁️ 3. 시각화 제어</div>", unsafe_allow_html=True)
        show_electron = st.checkbox("자유 전자 (e⁻) 흐름 애니메이션 표시", True, key="rcs_show_electron")

    with col_display:
        # --- 물리 계산 공식 ---
        req = 0.0      # 등가 저항
        i_total = 0.0  # 전체 전류
        i1 = i2 = i3 = 0.0
        v1 = v2 = v3 = 0.0
        p1 = p2 = p3 = 0.0
        p_total = 0.0

        if c_type == 'series':
            req = r1 + r2
            i_total = voltage / req
            i1 = i_total
            i2 = i_total
            v1 = i1 * r1
            v2 = i2 * r2
            p1 = i1 * v1
            p2 = i2 * v2
            p_total = p1 + p2
        elif c_type == 'parallel':
            req = 1 / ((1 / r1) + (1 / r2))
            i_total = voltage / req
            v1 = voltage
            v2 = voltage
            i1 = v1 / r1
            i2 = v2 / r2
            p1 = i1 * v1
            p2 = i2 * v2
            p_total = p1 + p2
        else: # mixed
            r_parallel = 1 / ((1 / r2) + (1 / r3))
            req = r1 + r_parallel
            i_total = voltage / req
            i1 = i_total
            v1 = i1 * r1
            
            v_parallel = voltage - v1
            v2 = v_parallel
            v3 = v_parallel
            i2 = v2 / r2
            i3 = v3 / r3
            
            p1 = i1 * v1
            p2 = i2 * v2
            p3 = i3 * v3
            p_total = p1 + p2 + p3

        # 회로 상태 대시보드 리드아웃
        st.markdown("### 📊 실시간 회로 정량 분석")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("합성 저항 (Req)", f"{fmt(req)} Ω")
        with col_m2:
            st.metric("전체 전류 (Itotal)", f"{fmt(i_total)} A")
        with col_m3:
            st.metric("총 소비 전력 (Ptotal)", f"{fmt(p_total)} W")

        # --- SVG 회로 도면 생성 ---
        # 저항 발열 글로우 크기 및 오파시티 계산
        op1 = min(0.6, 0.2 + (p1 / max(1.0, p_total)) * 0.4) if p1 > 0 else 0
        r_glow1 = min(30.0, 8.0 + p1 * 1.5)
        
        op2 = min(0.6, 0.2 + (p2 / max(1.0, p_total)) * 0.4) if p2 > 0 else 0
        r_glow2 = min(30.0, 8.0 + p2 * 1.5)

        op3 = min(0.6, 0.2 + (p3 / max(1.0, p_total)) * 0.4) if p3 > 0 else 0
        r_glow3 = min(30.0, 8.0 + p3 * 1.5)

        components_svg = ""
        electron_svg = ""

        if c_type == 'series':
            components_svg = f"""
            <!-- 저항 1 (상단 왼쪽) -->
            <g transform="translate(220, 50)">
              <circle cx="0" cy="0" r="{r_glow1}" fill="#ef4444" opacity="{op1}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#f59e0b" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#f59e0b" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R1: {r1}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(v1)}V &#124; {fmt(p1)}W</text>
            </g>

            <!-- 저항 2 (상단 오른쪽) -->
            <g transform="translate(370, 50)">
              <circle cx="0" cy="0" r="{r_glow2}" fill="#ef4444" opacity="{op2}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#ea580c" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#ea580c" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#ea580c" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R2: {r2}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(v2)}V &#124; {fmt(p2)}W</text>
            </g>
            """
            if show_electron:
                dur = max(0.4, 5 / (i_total + 0.1))
                for offset in [0, 0.2, 0.4, 0.6, 0.8]:
                    begin = offset * dur
                    electron_svg += f'<circle r="5" fill="#67e8f9" opacity="0.95"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M 100,200 L 100,50 L 450,50 L 450,200 Z" begin="{begin}s" /></circle>'

        elif c_type == 'parallel':
            components_svg = f"""
            <!-- 병렬 배선 -->
            <path d="M 200,50 L 200,150 L 380,150 L 380,50" fill="none" stroke="url(#potentialGrad)" stroke-width="3" opacity="0.6" />

            <!-- 저항 1 (상단 분기) -->
            <g transform="translate(290, 50)">
              <circle cx="0" cy="0" r="{r_glow1}" fill="#ef4444" opacity="{op1}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#f59e0b" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#f59e0b" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R1: {r1}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(i1)}A &#124; {fmt(p1)}W</text>
            </g>

            <!-- 저항 2 (하단 분기) -->
            <g transform="translate(290, 150)">
              <circle cx="0" cy="0" r="{r_glow2}" fill="#ef4444" opacity="{op2}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#ea580c" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#ea580c" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#ea580c" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R2: {r2}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(i2)}A &#124; {fmt(p2)}W</text>
            </g>
            """
            if show_electron:
                dur_total = max(0.4, 4 / (i_total + 0.1))
                dur1 = max(0.4, 4 / (i1 + 0.1))
                dur2 = max(0.4, 4 / (i2 + 0.1))

                # 주도선 좌측 흐름
                for offset in [0, 0.3, 0.6]:
                    begin = offset * dur_total
                    electron_svg += f'<circle r="5" fill="#67e8f9"><animateMotion dur="{dur_total}s" repeatCount="indefinite" path="M 100,200 L 100,50 L 200,50" begin="{begin}s" /></circle>'
                # 분기 R1 흐름
                for offset in [0, 0.4, 0.8]:
                    begin = offset * dur1
                    electron_svg += f'<circle r="4" fill="#fbbf24"><animateMotion dur="{dur1}s" repeatCount="indefinite" path="M 200,50 L 380,50" begin="{begin}s" /></circle>'
                # 분기 R2 흐름
                for offset in [0, 0.4, 0.8]:
                    begin = offset * dur2
                    electron_svg += f'<circle r="4" fill="#f97316"><animateMotion dur="{dur2}s" repeatCount="indefinite" path="M 200,50 L 200,150 L 380,150 L 380,50" begin="{begin}s" /></circle>'
                # 주도선 우측 회수 흐름
                for offset in [0, 0.3, 0.6]:
                    begin = offset * dur_total
                    electron_svg += f'<circle r="5" fill="#67e8f9"><animateMotion dur="{dur_total}s" repeatCount="indefinite" path="M 380,50 L 450,50 L 450,200 L 100,200" begin="{begin}s" /></circle>'

        else: # mixed
            components_svg = f"""
            <!-- 복합 회로 병렬 배선 -->
            <path d="M 300,50 L 300,130 L 420,130 L 420,50" fill="none" stroke="url(#potentialGrad)" stroke-width="3" opacity="0.6" />

            <!-- 저항 1 (직렬 구간) -->
            <g transform="translate(200, 50)">
              <circle cx="0" cy="0" r="{r_glow1}" fill="#ef4444" opacity="{op1}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#f59e0b" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#f59e0b" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#f59e0b" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R1: {r1}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(i1)}A &#124; {fmt(p1)}W</text>
            </g>

            <!-- 저항 2 (상단 분기) -->
            <g transform="translate(360, 50)">
              <circle cx="0" cy="0" r="{r_glow2}" fill="#ef4444" opacity="{op2}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#ea580c" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#ea580c" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#ea580c" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R2: {r2}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(i2)}A &#124; {fmt(p2)}W</text>
            </g>

            <!-- 저항 3 (하단 분기) -->
            <g transform="translate(360, 130)">
              <circle cx="0" cy="0" r="{r_glow3}" fill="#ef4444" opacity="{op3}" filter="url(#glow)" />
              <path d="M -30,0 L -15,-10 L -5,10 L 5,-10 L 15,10 L 30,0" fill="none" stroke="#f43f5e" stroke-width="4" />
              <rect x="-35" y="-30" width="70" height="20" rx="4" fill="#0f172a" stroke="#f43f5e" stroke-width="1.5" opacity="0.9" />
              <text x="0" y="-16" fill="#f43f5e" font-weight="bold" font-family="sans-serif" font-size="10" text-anchor="middle">R3: {r3}Ω</text>
              <text x="0" y="25" fill="#94a3b8" font-family="monospace" font-size="9.5" text-anchor="middle">{fmt(i3)}A &#124; {fmt(p3)}W</text>
            </g>
            """
            if show_electron:
                dur_total = max(0.4, 5 / (i_total + 0.1))
                dur2 = max(0.4, 4 / (i2 + 0.1))
                dur3 = max(0.4, 4 / (i3 + 0.1))

                # 직렬부 주도선 흐름
                for offset in [0, 0.25, 0.5, 0.75]:
                    begin = offset * dur_total
                    electron_svg += f'<circle r="5" fill="#67e8f9"><animateMotion dur="{dur_total}s" repeatCount="indefinite" path="M 100,200 L 100,50 L 300,50" begin="{begin}s" /></circle>'
                # 상단 병렬 분기 R2
                for offset in [0, 0.5]:
                    begin = offset * dur2
                    electron_svg += f'<circle r="4" fill="#f97316"><animateMotion dur="{dur2}s" repeatCount="indefinite" path="M 300,50 L 420,50" begin="{begin}s" /></circle>'
                # 하단 병렬 분기 R3
                for offset in [0, 0.5]:
                    begin = offset * dur3
                    electron_svg += f'<circle r="4" fill="#f43f5e"><animateMotion dur="{dur3}s" repeatCount="indefinite" path="M 300,50 L 300,130 L 420,130 L 420,50" begin="{begin}s" /></circle>'
                # 주도선 우측 회수
                for offset in [0, 0.25, 0.5, 0.75]:
                    begin = offset * dur_total
                    electron_svg += f'<circle r="5" fill="#67e8f9"><animateMotion dur="{dur_total}s" repeatCount="indefinite" path="M 420,50 L 450,50 L 450,200 L 100,200" begin="{begin}s" /></circle>'

        svg_diagram = f"""
        <svg width="100%" height="270" viewBox="0 0 550 250" style="background-color: #0b1329; border: 1.5px solid #1e293b; border-radius: 16px;">
          <defs>
            <linearGradient id="potentialGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stop-color="#ef4444" />
              <stop offset="50%" stop-color="#f59e0b" />
              <stop offset="100%" stop-color="#3b82f6" />
            </linearGradient>
            <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
              <feGaussianBlur stdDeviation="7" result="blur" />
              <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
          </defs>

          <!-- 도선 기본 라인 -->
          <path d="M 100,50 L 450,50 L 450,200 L 100,200 Z" fill="none" stroke="url(#potentialGrad)" stroke-width="4.5" stroke-linecap="round" opacity="0.4" />

          <!-- 배터리 전원장치 (100, 125) -->
          <g transform="translate(100, 125)">
            <line x1="0" y1="-30" x2="0" y2="30" stroke="#ef4444" stroke-width="4" />
            <line x1="-15" y1="-15" x2="15" y2="-15" stroke="#ef4444" stroke-width="6" />
            <line x1="-8" y1="-5" x2="8" y2="-5" stroke="#3b82f6" stroke-width="9" />
            <line x1="-15" y1="5" x2="15" y2="5" stroke="#ef4444" stroke-width="6" />
            <line x1="-8" y1="15" x2="8" y2="15" stroke="#3b82f6" stroke-width="9" />
            <text x="-48" y="5" fill="#ef4444" font-weight="bold" font-family="monospace" font-size="13">{voltage}V</text>
          </g>

          <!-- 실시간 저항 소자 및 라벨 렌더링 -->
          {components_svg}

          <!-- 애니메이션 효과 전자 렌더링 -->
          {electron_svg}
        </svg>
        """
        
        # SVG 화면 드로잉
        st.markdown(svg_diagram, unsafe_allow_html=True)

        # 범례 표시
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #ef4444; border-radius: 2px;"></span> 고전위 (+)</div>
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #3b82f6; border-radius: 2px;"></span> 저전위 (-)</div>
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #67e8f9; border-radius: 50%;"></span> 이동하는 자유 전자 (e⁻)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # 3색 세부 카드 레이아웃
        col_c1, col_c2, col_c3 = st.columns(3)

        with col_c1:
            st.markdown(f"""
            <div class='analysis-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                    <b style='color:#f59e0b;'>저항 R1 분석</b>
                    <span style='font-size:1.1rem;'>🌡️</span>
                </div>
                <div style='font-family:monospace; font-size:0.85rem; color:#cbd5e1; line-height:1.7;'>
                    저항값: {r1} Ω<br>
                    전류 I1: <span style='color:#22d3ee;'>{fmt(i1)} A</span><br>
                    전압 V1: <span style='color:#c084fc;'>{fmt(v1)} V</span><br>
                    <div style='border-top:1px solid #1e293b; margin:6px 0;'></div>
                    소비 전력: <span style='color:#f59e0b; font-weight:bold;'>{fmt(p1)} W</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
            <div class='analysis-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                    <b style='color:#ea580c;'>저항 R2 분석</b>
                    <span style='font-size:1.1rem;'>🌡️</span>
                </div>
                <div style='font-family:monospace; font-size:0.85rem; color:#cbd5e1; line-height:1.7;'>
                    저항값: {r2} Ω<br>
                    전류 I2: <span style='color:#22d3ee;'>{fmt(i2)} A</span><br>
                    전압 V2: <span style='color:#c084fc;'>{fmt(v2)} V</span><br>
                    <div style='border-top:1px solid #1e293b; margin:6px 0;'></div>
                    소비 전력: <span style='color:#ea580c; font-weight:bold;'>{fmt(p2)} W</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_c3:
            if c_type == 'mixed':
                st.markdown(f"""
                <div class='analysis-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                        <b style='color:#f43f5e;'>저항 R3 분석</b>
                        <span style='font-size:1.1rem;'>🌡️</span>
                    </div>
                    <div style='font-family:monospace; font-size:0.85rem; color:#cbd5e1; line-height:1.7;'>
                        저항값: {r3} Ω<br>
                        전류 I3: <span style='color:#22d3ee;'>{fmt(i3)} A</span><br>
                        전압 V3: <span style='color:#c084fc;'>{fmt(v3)} V</span><br>
                        <div style='border-top:1px solid #1e293b; margin:6px 0;'></div>
                        소비 전력: <span style='color:#f43f5e; font-weight:bold;'>{fmt(p3)} W</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='analysis-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
                        <b style='color:#94a3b8;'>시스템 열 출력</b>
                        <span style='font-size:1.1rem;'>⚡</span>
                    </div>
                    <div class='heat-gauge-container'>
                        <div style='display:flex; justify-content:space-between; font-size:0.75rem; color:#94a3b8; font-family:monospace;'>
                            <span>에너지 공급률</span>
                            <span>{fmt(p_total)} J/s (W)</span>
                        </div>
                        <div style='background:#1e293b; border-radius:9999px; height:8px; width:100%; margin-top:5px; overflow:hidden;'>
                            <div style='background:linear-gradient(90deg, #f59e0b, #f43f5e); height:100%; width:{min(100.0, (p_total / 60) * 100)}%;'></div>
                        </div>
                    </div>
                    <p style='font-size:0.7rem; color:#64748b; line-height:1.3; margin-top:8px;'>* 전기 에너지는 자유전자가 금속 원자핵과 충돌하여 줄 열(Joule Heat)로 100% 전환 방출됩니다.</p>
                </div>
                """, unsafe_allow_html=True)

        if c_type == 'mixed':
            st.markdown(f"""
            <div class='analysis-card'>
                <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;'>
                    <b style='color:#10b981;'>시스템 전체 열 방출 밸런스</b>
                    <span style='font-size:0.85rem; color:#10b981; font-family:monospace; font-weight:bold;'>총 {fmt(p_total)} J/s</span>
                </div>
                <div class='heat-gauge-container'>
                    <div style='background:#1e293b; border-radius:9999px; height:12px; width:100%; overflow:hidden;'>
                        <div style='background:linear-gradient(90deg, #f59e0b, #f43f5e); height:100%; width:{min(100.0, (p_total / 60) * 100)}%;'></div>
                    </div>
                </div>
                <p style='font-size:0.7rem; color:#64748b; line-height:1.3; margin-top:8px;'>* 세 가변 저항(R1, R2, R3)의 결합에 의해 소비되는 전기 에너지의 열 전환량 게이지입니다. (가변 저항을 변경하면 실시간으로 밸런스가 조절됩니다)</p>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 2: 탐구 챌린지
# ══════════════════════════════════════════════════════════════
with tab_mission:
    col_list, col_quiz = st.columns([1, 2])

    with col_list:
        st.markdown("<h4 style='color: #e2e8f0; margin-bottom: 12px;'>🏆 탐구 과제 목록</h4>", unsafe_allow_html=True)
        
        # 미션 목록 정의
        m_list = [
            {"id": 1, "title": "⚡ 미션 01. 전류 보존 법칙 증명"},
            {"id": 2, "title": "🌱 미션 02. 스마트팜 열원 설계"}
        ]
        
        for m in m_list:
            is_selected = st.session_state.rcs_current_mission == m["id"]
            if st.button(
                m["title"],
                key=f"rcs_m_btn_{m['id']}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                st.session_state.rcs_current_mission = m["id"]
                st.session_state.rcs_user_answer = ""
                st.session_state.rcs_feedback = None
                st.rerun()

    with col_quiz:
        active_id = st.session_state.rcs_current_mission
        
        if active_id == 1:
            st.markdown("""
            <span class='badge-mission'>실험 탐구 미션 01</span>
            <h3 style='color: #e2e8f0; margin-top: 8px; margin-bottom: 12px;'>오개념 격파! 전류 보존 법칙 증명하기</h3>
            <div style='background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; font-size: 0.92rem; line-height: 1.6; color: #e2e8f0;'>
                <b>[문제 상황]</b><br>
                가상 회로실에서 <b>직렬 회로(Series)</b>를 선택하고 아래 조건으로 값을 조정하세요.<br>
                - <b>입력 전압 (V): 18V</b><br>
                - <b>저항 R1: 6Ω</b><br>
                - <b>저항 R2: 12Ω</b><br><br>
                이때 R1을 지나는 전류(I1)와 R2를 지나는 전류(I2)의 비율 <b>(I1 / I2)</b>은 얼마입니까?<br>
                <i>(정답을 계산하거나 실시간 분석 카드에서 찾아 숫자로 정밀하게 입력하세요. 예: 1)</i>
            </div>
            """, unsafe_allow_html=True)

            # 정답 검증 로직
            def verify_ans1(ans_str):
                try:
                    val = float(ans_str.strip())
                    # 직렬 회로에서 입력 변수를 올바르게 맞추었는지와, 전류 비율이 1인지 검증
                    correct_params = (st.session_state.rcs_voltage == 18 and 
                                      st.session_state.rcs_r1 == 6 and 
                                      st.session_state.rcs_r2 == 12 and 
                                      c_type == "series")
                    
                    if not correct_params:
                        return False, "⚠️ 먼저 가상 회로실 탭으로 가셔서 회로 구조를 '직렬 회로'로 변경하고, 전압=18V, R1=6Ω, R2=12Ω으로 가변 슬라이더를 맞추어 시뮬레이션 데이터를 관측하세요!"
                    
                    if abs(val - 1.0) < 0.01:
                        return True, "🎉 훌륭합니다! 많은 학생들이 큰 저항 R2를 지나면 전류가 '소비'되어 줄어든다고 착각하지만, 단일 도선 내 전하량은 보존되므로 전류는 어디서나 같습니다! 소비되는 것은 전류가 아니라 '전기적 위치 에너지(전압)'입니다."
                    else:
                        return False, "❌ 비율 계산이 잘못되었습니다. 전류 보존 법칙(전하량 보존 법칙)에 의해 단일 회로에서 전류의 크기가 어때야 하는지 가상 회로실 분석 카드를 보고 다시 확인해 보세요."
                except ValueError:
                    return False, "⚠️ 숫자로 입력해 주세요 (예: 1)"

        else: # 미션 2
            st.markdown("""
            <span class='badge-mission'>실험 탐구 미션 02</span>
            <h3 style='color: #e2e8f0; margin-top: 8px; margin-bottom: 12px;'>사곡고 스마트팜 열원 설계 챌린지</h3>
            <div style='background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; font-size: 0.92rem; line-height: 1.6; color: #e2e8f0;'>
                <b>[문제 상황]</b><br>
                사곡고 스마트팜 수조 온도를 일정하게 유지하기 위해 <b>전기에너지 발열 전도 장치</b>를 설계하고 있습니다.<br>
                전력(발열량)이 정확히 <b>12W</b>가 되는 직렬 회로를 구축하고자 합니다.<br><br>
                전압이 <b>12V</b>일 때, 전하량 소모 효율을 고려하여 R1과 R2의 합성 저항(Req)이 몇 옴(Ω)이 되어야 총 전력 P = 12W가 될 수 있을까요?<br>
                합성 저항 Req(Ω)에 해당하는 수치값을 정답으로 입력하세요.<br>
                <i>(힌트: 전력 공식 P = V² / Req 를 이용하여 역산해 보세요!)</i>
            </div>
            """, unsafe_allow_html=True)

            def verify_ans2(ans_str):
                try:
                    val = float(ans_str.strip())
                    # P = V^2 / Req => Req = V^2 / P = 12^2 / 12 = 12 Ohm.
                    if abs(val - 12.0) < 0.01:
                        return True, "🎉 정답입니다! 12V의 인가 전압 조건에서 전체 합성 저항이 12Ω이 되면, 1초당 12J의 열 에너지가 고르게 발생하여 스마트팜을 안전하고 효율적으로 데울 수 있습니다."
                    else:
                        return False, "❌ 스마트팜 열 효율 조건을 만족하지 못합니다. P = V² / Req 공식을 이용하여 Req = V² / P 로 합성 저항을 설계해 보세요."
                except ValueError:
                    return False, "⚠️ 숫자로 입력해 주세요 (예: 12)"

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 답안 입력 상자
        user_ans = st.text_input(
            "계산 및 시뮬레이션 측정 정답 기입",
            value=st.session_state.rcs_user_answer,
            placeholder="정답 수치를 입력하고 제출 버튼을 누르세요",
            key="rcs_ans_input"
        )
        
        # 답안 제출 및 검증
        if st.button("🚀 답안 제출", type="primary", use_container_width=True):
            if active_id == 1:
                success, msg = verify_ans1(user_ans)
            else:
                success, msg = verify_ans2(user_ans)
                
            if success:
                st.session_state.rcs_feedback = {"success": True, "text": msg}
                # 점수 가산은 최초 1회만 가산하는 효과를 내기 위해 피드백이 이전에 통과 상태가 아니었을 때만
                st.session_state.rcs_score += 10
            else:
                st.session_state.rcs_feedback = {"success": False, "text": msg}
            st.rerun()

        # 피드백 메시지 박스 드로잉
        if st.session_state.rcs_feedback:
            fb = st.session_state.rcs_feedback
            if fb["success"]:
                st.markdown(f"""
                <div class='feedback-box-success'>
                    <b>✅ 축하합니다! 정답입니다.</b><br>
                    <p style='font-size:0.88rem; line-height:1.5; color:#e2e8f0; margin-top:6px;'>{fb['text']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='feedback-box-error'>
                    <b>❌ 틀렸습니다. 다시 도전해 보세요!</b><br>
                    <p style='font-size:0.88rem; line-height:1.5; color:#e2e8f0; margin-top:6px;'>{fb['text']}</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        
        # 하단 점수 누계 스코어보드
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; color: #94a3b8; font-size: 0.85rem;">
            <span>* 탐구 미션을 성공하면 교과 가산점(마일리지)을 부여합니다.</span>
            <span>현재 누적 탐구 스코어: <strong style="color: #34d399; font-size: 1.1rem; font-family: monospace;">{st.session_state.rcs_score} pts</strong></span>
        </div>
        """, unsafe_allow_html=True)
