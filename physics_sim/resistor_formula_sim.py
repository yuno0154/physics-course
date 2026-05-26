"""
저항의 연결 공식 및 에너지 전환 개념 학습 시뮬레이터
- 직렬 및 병렬 연결에서의 전위차, 저항, 전류, 에너지 전환(소비 전력) 공식의 정량적 유도
- 실시간 수치 연동 LaTeX 수식 계산 시뮬레이션
- 직렬(비례) vs 병렬(반비례) 에너지 방출 밸런스 비주얼 게이지
- 자가 개념 진단 퀴즈 및 스코어보드 시스템
"""

import streamlit as st

# 소수점 2자리 반올림 포맷팅 Helper
def fmt(val):
    return round(val, 2)

# ── 공통 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-left: 5px solid #3b82f6;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.1);
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
.formula-block {
    background: #0b1329;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 18px;
}
.energy-gauge-container {
    background: #090d16;
    border: 1.5px solid #1e293b;
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
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
.badge-concept {
    background: rgba(129, 140, 248, 0.15);
    border: 1px solid rgba(129, 140, 248, 0.3);
    color: #a5b4fc;
    border-radius: 9999px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──────────────────────────────────────
if 'rfs_score' not in st.session_state:
    st.session_state.rfs_score = 0
if 'rfs_q1_feedback' not in st.session_state:
    st.session_state.rfs_q1_feedback = None
if 'rfs_q2_feedback' not in st.session_state:
    st.session_state.rfs_q2_feedback = None

# ══════════════════════════════════════════════════════════════
# 헤더 섹션
# ══════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-title'>🔌 저항의 연결 공식 및 에너지 전환 학습관</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>직류 회로 속 전위차, 전류, 합성 저항, 전기에너지 전환(줄 열) 공식을 실시간으로 수학적 유도하여 완전 학습합니다.</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <b style='color:#60a5fa; font-size:1.05rem;'>📖 이론의 개요</b><br>
    <span style='color:#e2e8f0; font-size:0.92rem; line-height: 1.6;'>
    전압(전위차)이 인가된 도선에서 자유전자가 저항(원자핵)과 충돌하며 발생하는 열에너지를 <b>줄 열(Joule Heat)</b>이라고 합니다.<br>
    본 학습실에서는 저항을 <b>직렬</b>과 <b>병렬</b>로 연결할 때, 각 저항에 배분되는 물리량들과 에너지 전환(소비 전력) 공식이 유도되는 규칙을 정량적인 수치와 수식의 유기적 변화를 통해 탐구할 수 있습니다.
    </span>
</div>
""", unsafe_allow_html=True)

# 탭 구조 설계 (직렬 연결 공식, 병렬 연결 공식, 개념 진단 평가)
tab_series, tab_parallel, tab_concept_quiz = st.tabs([
    "📐 직렬 연결 공식 유도 (Series formulas)",
    "📐 병렬 연결 공식 유도 (Parallel formulas)",
    "🏆 개념 자가 진단 평가 (Diagnostic Test)"
])

# ══════════════════════════════════════════════════════════════
# 탭 1: 직렬 연결 공식 유도
# ══════════════════════════════════════════════════════════════
with tab_series:
    st.markdown("### 🔌 1. 직렬 연결(Series Connection)의 4대 핵심 물리 공식")
    
    col_th_s1, col_th_s2 = st.columns(2)
    with col_th_s1:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #38bdf8;'>1️⃣ 전류 (Current) 법칙</b><br>
            도선이 한 갈래로만 연결되어 있으므로, 단면을 지나는 단위 시간당 전하의 양은 어디서나 동일합니다.<br>
            <span style='color: #60a5fa; font-weight: bold;'>전류 보존(전하량 보존) 법칙</span>이 성립합니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col_th_s2:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #38bdf8;'>2️⃣ 전위차 (Voltage Drop) 분배</b><br>
            전체 전원장치 공급 전압은 각 저항을 지날 때 발생하는 전압 강하(전위차)의 합과 같습니다.<br>
            <span style='color: #f59e0b; font-weight: bold;'>에너지 보존 법칙</span>에 기반합니다.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    col_th_s3, col_th_s4 = st.columns(2)
    with col_th_s3:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #38bdf8;'>3️⃣ 합성 저항 (Equivalent Resistance)</b><br>
            전하가 통과해야 하는 도선의 길이가 늘어나는 효과를 가집니다. 따라서 합성 저항은 개별 저항들의 합보다 항상 커집니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col_th_s4:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #38bdf8;'>4️⃣ 에너지 전환 (Joule Heating / Power)</b><br>
            저항기에서 소비되는 전기에너지(초당 열에너지) 공식은 다음과 같습니다:<br>
            <span style='color: #f43f5e; font-weight: bold;'>P = I²R</span><br>
            전류 $I$가 일정하므로, <b>소비 전력은 저항값 $R$에 정비례</b>하여 방출됩니다.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='step-header'>🎛️ 2. 실시간 대화형 수식 유도 시뮬레이션 (직렬)</div>", unsafe_allow_html=True)
    
    col_ctrl_s, col_eq_s = st.columns([1, 2])
    with col_ctrl_s:
        s_v = st.slider("입력 전압 (V)", 1, 24, 12, key="rfs_s_v")
        s_r1 = st.slider("저항 R1 (Ω)", 1, 20, 4, key="rfs_s_r1")
        s_r2 = st.slider("저항 R2 (Ω)", 1, 20, 8, key="rfs_s_r2")
        
        # 물리값 계산
        s_req = s_r1 + s_r2
        s_i = s_v / s_req
        s_v1 = s_i * s_r1
        s_v2 = s_i * s_r2
        s_p1 = (s_i ** 2) * s_r1
        s_p2 = (s_i ** 2) * s_r2
        s_ptot = s_p1 + s_p2
        
    with col_eq_s:
        st.markdown("<div class='formula-block'>", unsafe_allow_html=True)
        st.write("#### 📐 단계별 대수 수식 유도 과정")
        
        # 1. 합성 저항 유도
        st.markdown("**① 합성 저항 ($R_{eq}$) 구하기**")
        st.latex(rf"R_{{eq}} = R_1 + R_2 = {s_r1}\,\Omega + {s_r2}\,\Omega = {s_req}\,\Omega")
        
        # 2. 전류 계산
        st.markdown("**② 옴의 법칙을 이용한 전체 전류 ($I$) 구하기**")
        st.latex(rf"I_1 = I_2 = I_{{total}} = \frac{{V}}{{R_{{eq}}}} = \frac{{{s_v}\,V}}{{{s_req}\,\Omega}} \approx {fmt(s_i)}\,A")
        
        # 3. 각 저항의 전위차
        st.markdown("**③ 각 저항의 전압 강하 (전위차 $V_n$) 구하기**")
        st.latex(rf"V_1 = I \cdot R_1 = {fmt(s_i)}\,A \times {s_r1}\,\Omega \approx {fmt(s_v1)}\,V")
        st.latex(rf"V_2 = I \cdot R_2 = {fmt(s_i)}\,A \times {s_r2}\,\Omega \approx {fmt(s_v2)}\,V")
        st.latex(rf"V_{{total}} = V_1 + V_2 = {fmt(s_v1)}\,V + {fmt(s_v2)}\,V = {s_v}\,V \quad \text{{[(에너지 보존 만족)]}}")
        
        # 4. 전기에너지 전환율(소비 전력)
        st.markdown("**④ 저항별 소비 전력($P = I^2R$) 즉, 에너지 전환율 유도**")
        st.latex(rf"P_1 = I^2 \cdot R_1 = ({fmt(s_i)}\,A)^2 \times {s_r1}\,\Omega \approx {fmt(s_p1)}\,W")
        st.latex(rf"P_2 = I^2 \cdot R_2 = ({fmt(s_i)}\,A)^2 \times {s_r2}\,\Omega \approx {fmt(s_p2)}\,W")
        st.latex(rf"P_{{1}} : P_{{2}} = R_1 : R_2 = {s_r1} : {s_r2} \quad \text{{[(저항과 소비 전력비 정비례)]}}")
        st.markdown("</div>", unsafe_allow_html=True)

    # 비주얼 에너지 전환 밸런스 게이지
    st.markdown("<div class='energy-gauge-container'>", unsafe_allow_html=True)
    st.markdown(f"#### 🔥 직렬 회로 내 소비 전력(에너지 전환율) 실시간 밸런스 (총 {fmt(s_ptot)} W)")
    
    ratio_p1 = (s_p1 / max(1.0, s_ptot)) * 100
    ratio_p2 = (s_p2 / max(1.0, s_ptot)) * 100
    
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; margin-bottom: 5px; font-size:0.85rem; font-family:monospace; color:#cbd5e1;'>
        <span style='color:#f59e0b;'>R1 발열량 ({s_r1}Ω): {fmt(s_p1)} W ({fmt(ratio_p1)}%)</span>
        <span style='color:#ea580c;'>R2 발열량 ({s_r2}Ω): {fmt(s_p2)} W ({fmt(ratio_p2)}%)</span>
    </div>
    <div style='background:#1e293b; border-radius:9999px; height:20px; width:100%; display:flex; overflow:hidden;'>
        <div style='background:#f59e0b; width:{ratio_p1}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P1</div>
        <div style='background:#ea580c; width:{ratio_p2}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P2</div>
    </div>
    <p style='font-size:0.75rem; color:#94a3b8; margin-top:8px; line-height:1.4;'>
        💡 <b>물리 직관</b>: 직렬 연결은 단일 전하 흐름 통로를 공유하므로, 전류가 공통입니다. 이에 따라 저항이 클수록 전기적 충돌 빈도가 늘어나 저항 크기에 비례하여 줄 열(소비 전력)을 방출합니다. ($P \propto R$)
    </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 2: 병렬 연결 공식 유도
# ══════════════════════════════════════════════════════════════
with tab_parallel:
    st.markdown("### 🔌 1. 병렬 연결(Parallel Connection)의 4대 핵심 물리 공식")
    
    col_th_p1, col_th_p2 = st.columns(2)
    with col_th_p1:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #a5b4fc;'>1️⃣ 전위차 (Voltage) 법칙</b><br>
            병렬로 연결된 각 갈래 도선은 배터리의 양 극단에 동일하게 직접 연결되어 있으므로, 모든 분기 저항에 인가되는 전압(전위차)은 같습니다.<br>
            <span style='color: #60a5fa; font-weight: bold;'>전위차 보존</span>이 성립합니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col_th_p2:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #a5b4fc;'>2️⃣ 전류 (Current) 분배</b><br>
            전원장치에서 출발한 전체 전류는 각 갈래 길로 나누어 흐른 뒤 다시 합쳐집니다.<br>
            <span style='color: #34d399; font-weight: bold;'>전류의 분기(KCL: 키르히호프 전류 법칙)</span>에 기반합니다.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

    col_th_p3, col_th_p4 = st.columns(2)
    with col_th_p3:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #a5b4fc;'>3️⃣ 합성 저항 (Equivalent Resistance)</b><br>
            전하가 지나갈 수 있는 유효 단면적이 넓어지는 효과를 가집니다. 따라서 합성 저항의 역수는 각 저항 역수의 합이며, 합성 저항값은 병렬 연결된 어떤 개별 저항보다도 항상 작아집니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col_th_p4:
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; height: 100%;'>
            <b style='color: #a5b4fc;'>4️⃣ 에너지 전환 (Joule Heating / Power)</b><br>
            병렬 구조에서 저항기 소비 전력(초당 열에너지) 공식은 다음과 같습니다:<br>
            <span style='color: #f43f5e; font-weight: bold;'>P = V² / R</span><br>
            각 저항의 전압 $V$가 일정하므로, <b>소비 전력은 저항값 $R$에 반비례</b>하여 방출됩니다.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='step-header'>🎛️ 2. 실시간 대화형 수식 유도 시뮬레이션 (병렬)</div>", unsafe_allow_html=True)
    
    col_ctrl_p, col_eq_p = st.columns([1, 2])
    with col_ctrl_p:
        p_v = st.slider("입력 전압 (V)", 1, 24, 12, key="rfs_p_v")
        p_r1 = st.slider("저항 R1 (Ω)", 1, 20, 6, key="rfs_p_r1")
        p_r2 = st.slider("저항 R2 (Ω)", 1, 20, 12, key="rfs_p_r2")
        
        # 물리값 계산
        p_req = 1 / ((1 / p_r1) + (1 / p_r2))
        p_i_tot = p_v / p_req
        p_i1 = p_v / p_r1
        p_i2 = p_v / p_r2
        p_p1 = (p_v ** 2) / p_r1
        p_p2 = (p_v ** 2) / p_r2
        p_ptot = p_p1 + p_p2
        
    with col_eq_p:
        st.markdown("<div class='formula-block'>", unsafe_allow_html=True)
        st.write("#### 📐 단계별 대수 수식 유도 과정")
        
        # 1. 합성 저항 유도
        st.markdown("**① 합성 저항 ($R_{eq}$) 구하기**")
        st.latex(rf"\frac{{1}}{{R_{{eq}}}} = \frac{{1}}{{R_1}} + \frac{{1}}{{R_2}} = \frac{{1}}{{{p_r1}}} + \frac{{1}}{{{p_r2}}} = \frac{{{p_r1} + {p_r2}}}{{{p_r1} \times {p_r2}}}")
        st.latex(rf"R_{{eq}} = \frac{{R_1 \cdot R_2}}{{R_1 + R_2}} = \frac{{{p_r1} \times {p_r2}}}{{{p_r1} + {p_r2}}} = \frac{{{p_r1 * p_r2}}}{{{p_r1 + p_r2}}} \approx {fmt(p_req)}\,\Omega")
        
        # 2. 전위차 보존
        st.markdown("**② 각 저항의 인가 전압 (전위차 $V_n$) 확인**")
        st.latex(rf"V_1 = V_2 = V_{{total}} = {p_v}\,V \quad \text{{[(전위차 보존 법칙 만족)]}}")
        
        # 3. 분기 전류 계산
        st.markdown("**③ 옴의 법칙을 이용한 개별 분기 전류 ($I_n$) 계산**")
        st.latex(rf"I_1 = \frac{{V}}{{R_1}} = \frac{{{p_v}\,V}}{{{p_r1}\,\Omega}} \approx {fmt(p_i1)}\,A")
        st.latex(rf"I_2 = \frac{{V}}{{R_2}} = \frac{{{p_v}\,V}}{{{p_r2}\,\Omega}} \approx {fmt(p_i2)}\,A")
        st.latex(rf"I_{{total}} = I_1 + I_2 = {fmt(p_i1)}\,A + {fmt(p_i2)}\,A = {fmt(p_i_tot)}\,A")
        
        # 4. 전기에너지 전환율(소비 전력)
        st.markdown("**④ 저항별 소비 전력($P = V^2 / R$) 즉, 에너지 전환율 유도**")
        st.latex(rf"P_1 = \frac{{V^2}}{{R_1}} = \frac{{{p_v}^2}}{{{p_r1}\,\Omega}} \approx {fmt(p_p1)}\,W")
        st.latex(rf"P_2 = \frac{{V^2}}{{R_2}} = \frac{{{p_v}^2}}{{{p_r2}\,\Omega}} \approx {fmt(p_p2)}\,W")
        st.latex(rf"P_{{1}} : P_{{2}} = \frac{{1}}{{R_1}} : \frac{{1}}{{R_2}} = {p_r2} : {p_r1} \quad \text{{[(저항과 소비 전력비 반비례)]}}")
        st.markdown("</div>", unsafe_allow_html=True)

    # 비주얼 에너지 전환 밸런스 게이지 (병렬)
    st.markdown("<div class='energy-gauge-container'>", unsafe_allow_html=True)
    st.markdown(f"#### 🔥 병렬 회로 내 소비 전력(에너지 전환율) 실시간 밸런스 (총 {fmt(p_ptot)} W)")
    
    ratio_p1 = (p_p1 / max(1.0, p_ptot)) * 100
    ratio_p2 = (p_p2 / max(1.0, p_ptot)) * 100
    
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; margin-bottom: 5px; font-size:0.85rem; font-family:monospace; color:#cbd5e1;'>
        <span style='color:#a5b4fc;'>R1 발열량 ({p_r1}Ω): {fmt(p_p1)} W ({fmt(ratio_p1)}%)</span>
        <span style='color:#818cf8;'>R2 발열량 ({p_r2}Ω): {fmt(p_p2)} W ({fmt(ratio_p2)}%)</span>
    </div>
    <div style='background:#1e293b; border-radius:9999px; height:20px; width:100%; display:flex; overflow:hidden;'>
        <div style='background:#a5b4fc; width:{ratio_p1}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P1</div>
        <div style='background:#818cf8; width:{ratio_p2}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P2</div>
    </div>
    <p style='font-size:0.75rem; color:#94a3b8; margin-top:8px; line-height:1.4;'>
        💡 <b>물리 직관</b>: 병렬 연결은 모든 저항에 공통된 전압이 분배됩니다. 따라서 저항이 작을수록 전자의 흐름이 원활하여 더 많은 전하가 흐르게 되고, 결과적으로 더 활발하게 열에너지를 방출하게 됩니다. ($P \propto \frac{{1}}{{R}}$)
    </p>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 3: 개념 자가 진단 평가
# ══════════════════════════════════════════════════════════════
with tab_concept_quiz:
    st.markdown("<h3 style='color: #e2e8f0;'>🏆 저항 연결 공식 자가 진단 평가</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>배운 공식을 바탕으로 자가 진단 문제를 해결하여 개념 오개념을 완벽하게 극복해 봅니다.</p>", unsafe_allow_html=True)
    
    # ── 문항 1 ────────────────────────────────────────────────
    st.markdown("""
    <div class='step-header'>❓ [문항 1] 직렬 연결에서의 소비 전력 비율</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; font-size:0.92rem; line-height:1.6;'>
        어떤 회로에 <b>3Ω의 저항 R1</b>과 <b>6Ω의 저항 R2</b>가 <b>직렬(Series)</b>로 연결되어 있습니다.<br>
        회로에 전원을 공급하여 전류를 흘려보낼 때, R1과 R2에서 발생하는 초당 열에너지(소비 전력)의 비율 <b>P1 : P2</b>는 어떻게 될까요?<br><br>
        ① 1 : 2 (저항값에 비례)<br>
        ② 2 : 1 (저항값에 반비례)<br>
        ③ 1 : 1 (전류가 같으므로 전력도 동일)<br>
        ④ 1 : 4 (저항의 제곱에 비례)
    </div>
    """, unsafe_allow_html=True)
    
    q1_choice = st.radio(
        "문항 1 정답 선택",
        ["선택지를 골라주세요", "① 1 : 2", "② 2 : 1", "③ 1 : 1", "④ 1 : 4"],
        key="rfs_q1_ans",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 문항 1 제출", key="rfs_q1_btn"):
        if q1_choice == "① 1 : 2":
            st.session_state.rfs_q1_feedback = {
                "success": True, 
                "text": "🎉 정답입니다! 직렬 연결에서는 각 저항에 흐르는 전류 $I$가 동일합니다. 소비 전력 공식 $P = I^2R$에 의해 전류가 동일하므로 소비 전력 비율은 저항 비율과 완벽하게 일치하게 됩니다 ($3:6 = 1:2$)."
            }
            st.session_state.rfs_score += 10
        elif q1_choice == "선택지를 골라주세요":
            st.session_state.rfs_q1_feedback = {"success": False, "text": "⚠️ 정답을 골라주세요."}
        else:
            st.session_state.rfs_q1_feedback = {
                "success": False, 
                "text": "❌ 오답입니다. 직렬 연결에서는 전류($I$)가 회로 내의 모든 위치에서 같습니다. 소비 전력 공식 $P = I^2R$을 대입하여 저항과 소비 전력의 비례 관계를 다시 검토해 보세요."
            }
        st.rerun()

    # 문항 1 피드백 출력
    if st.session_state.rfs_q1_feedback:
        fb1 = st.session_state.rfs_q1_feedback
        if fb1["success"]:
            st.markdown(f"<div class='feedback-box-success'><b>✅ 정답입니다!</b><br>{fb1['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-box-error'><b>❌ 오답 또는 미선택!</b><br>{fb1['text']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── 문항 2 ────────────────────────────────────────────────
    st.markdown("""
    <div class='step-header'>❓ [문항 2] 병렬 연결에서의 합성 저항과 에너지</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; font-size:0.92rem; line-height:1.6;'>
        어떤 가습 온도 장치에 <b>4Ω의 R1</b>과 <b>12Ω의 R2</b>가 <b>병렬(Parallel)</b>로 연결되어 있습니다.<br>
        인가된 전압이 12V일 때, 다음 설명 중 <b>옳지 않은 것</b>은 무엇입니까?<br><br>
        ① R1과 R2 양단에 걸리는 전위차는 12V로 같다.<br>
        ② R1에 흐르는 전류가 R2에 흐르는 전류의 3배이다.<br>
        ③ 이 회로의 합성 저항(Req)은 3Ω 이다.<br>
        ④ R2가 R1보다 더 많은 열에너지(소비 전력)를 방출한다.
    </div>
    """, unsafe_allow_html=True)
    
    q2_choice = st.radio(
        "문항 2 정답 선택",
        ["선택지를 골라주세요", "① R1과 R2 양단에 걸리는 전위차는 12V로 같다.", "② R1에 흐르는 전류가 R2에 흐르는 전류의 3배이다.", "③ 이 회로의 합성 저항(Req)은 3Ω 이다.", "④ R2가 R1보다 더 많은 열에너지(소비 전력)를 방출한다."],
        key="rfs_q2_ans",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 문항 2 제출", key="rfs_q2_btn"):
        if q2_choice == "④ R2가 R1보다 더 많은 열에너지(소비 전력)를 방출한다.":
            st.session_state.rfs_q2_feedback = {
                "success": True, 
                "text": "🎉 정답입니다! 병렬 회로에서는 각 저항에 걸리는 전압($V$)이 동일하므로, 소비 전력 공식 $P = V^2 / R$에 의해 저항이 더 작은 R1($4\\Omega$)이 R2($12\\Omega$)보다 전력을 3배 더 많이 방출(열에너지 전환)합니다. 따라서 ④번은 잘못된 설명입니다."
            }
            st.session_state.rfs_score += 10
        elif q2_choice == "선택지를 골라주세요":
            st.session_state.rfs_q2_feedback = {"success": False, "text": "⚠️ 정답을 골라주세요."}
        else:
            st.session_state.rfs_q2_feedback = {
                "success": False, 
                "text": "❌ 오답입니다. 선택하신 문항은 옳은 설명입니다. 병렬 회로에서의 합성 저항 공식 $R_{eq} = \\frac{R_1 R_2}{R_1+R_2} = \\frac{48}{16} = 3\\Omega$ 및 옴의 법칙 $I = V/R$을 고려하여 정답이 아닌 '옳지 않은' 설명을 골라보세요."
            }
        st.rerun()

    # 문항 2 피드백 출력
    if st.session_state.rfs_q2_feedback:
        fb2 = st.session_state.rfs_q2_feedback
        if fb2["success"]:
            st.markdown(f"<div class='feedback-box-success'><b>✅ 정답입니다!</b><br>{fb2['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-box-error'><b>❌ 오답 또는 미선택!</b><br>{fb2['text']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 종합 스코어 표시
    st.markdown(f"""
    <div style="text-align: right; font-size: 0.9rem; color: #94a3b8; font-weight: bold;">
        현재 공식 학습 점수: <strong style="color: #60a5fa; font-size: 1.15rem; font-family: monospace;">{st.session_state.rfs_score} pts</strong>
    </div>
    """, unsafe_allow_html=True)
