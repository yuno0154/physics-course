"""
저항의 연결 공식 및 소비전력 계산 학습 시뮬레이터 (활동지 통합형)
- [1단계] 탐구 질문과 물리 직관 (전자 운동, 에너지 전환 원리)
- [2단계] 전기에너지(W) 및 전력(P) 공식의 연동 유도
- [3단계] 직렬 vs 병렬 가상 실험실 (3컬럼 실시간 SVG 및 소비전력 밸런스 게이지)
- [4단계] 디지털 활동지 작성 및 개념 자가 진단 평가
"""

import streamlit as st

# 소수점 2자리 반올림 포맷팅 Helper
def fmt(val):
    return round(val, 2)

# ── SVG 회로 다이어그램 생성 함수 (직렬) ──────────────────────────────────
def series_circuit_svg(v, r1, r2, i, v1, v2, req, p1, p2):
    p_max = max(p1, p2, 0.01)
    a1 = min(0.85, p1 / p_max * 0.85)
    a2 = min(0.85, p2 / p_max * 0.85)
    wc = "#60a5fa"
    return f"""
<svg viewBox="0 0 400 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#090d16;border-radius:10px;border: 1px solid #1e293b;">
  <text x="200" y="22" text-anchor="middle" fill="#64748b" font-size="11" font-family="monospace">⚡ 직렬 회로 실시간 시뮬레이션</text>
  <!-- 상단 전선 -->
  <line x1="55" y1="75" x2="120" y2="75" stroke="{wc}" stroke-width="2.5"/>
  <line x1="205" y1="75" x2="235" y2="75" stroke="{wc}" stroke-width="2.5"/>
  <line x1="320" y1="75" x2="370" y2="75" stroke="{wc}" stroke-width="2.5"/>
  <line x1="370" y1="75" x2="370" y2="165" stroke="{wc}" stroke-width="2.5"/>
  <!-- 하단 전선 -->
  <line x1="55" y1="165" x2="370" y2="165" stroke="{wc}" stroke-width="2.5"/>
  <!-- 배터리 왼쪽 세로선 -->
  <line x1="40" y1="75" x2="40" y2="103" stroke="{wc}" stroke-width="2.5"/>
  <line x1="23" y1="103" x2="57" y2="103" stroke="#38bdf8" stroke-width="4"/>
  <line x1="29" y1="117" x2="51" y2="117" stroke="#38bdf8" stroke-width="2"/>
  <line x1="40" y1="117" x2="40" y2="165" stroke="{wc}" stroke-width="2.5"/>
  <line x1="40" y1="75" x2="55" y2="75" stroke="{wc}" stroke-width="2.5"/>
  <text x="62" y="108" fill="#34d399" font-size="12" font-family="monospace">+</text>
  <text x="62" y="122" fill="#f87171" font-size="12" font-family="monospace">−</text>
  <text x="40" y="148" text-anchor="middle" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace">{v}V</text>
  <!-- 전류 화살표 -->
  <text x="88" y="67" text-anchor="middle" fill="#34d399" font-size="14" font-family="monospace">→</text>
  <text x="220" y="67" text-anchor="middle" fill="#34d399" font-size="14" font-family="monospace">→</text>
  <text x="345" y="67" text-anchor="middle" fill="#34d399" font-size="14" font-family="monospace">→</text>
  <!-- R1 저항 -->
  <rect x="120" y="59" width="85" height="32" fill="rgba(245,158,11,{a1:.2f})" stroke="#f59e0b" stroke-width="2.5" rx="5"/>
  <text x="162" y="79" text-anchor="middle" fill="#fef3c7" font-size="12" font-weight="bold" font-family="monospace">R₁={r1}Ω</text>
  <text x="162" y="104" text-anchor="middle" fill="#f59e0b" font-size="10" font-family="monospace">V₁={fmt(v1)}V</text>
  <text x="162" y="117" text-anchor="middle" fill="#fbbf24" font-size="10" font-family="monospace">P₁={fmt(p1)}W 🔥</text>
  <!-- R2 저항 -->
  <rect x="235" y="59" width="85" height="32" fill="rgba(234,88,12,{a2:.2f})" stroke="#ea580c" stroke-width="2.5" rx="5"/>
  <text x="277" y="79" text-anchor="middle" fill="#fed7aa" font-size="12" font-weight="bold" font-family="monospace">R₂={r2}Ω</text>
  <text x="277" y="104" text-anchor="middle" fill="#ea580c" font-size="10" font-family="monospace">V₂={fmt(v2)}V</text>
  <text x="277" y="117" text-anchor="middle" fill="#f97316" font-size="10" font-family="monospace">P₂={fmt(p2)}W 🔥</text>
  <!-- 하단 전류 표시 -->
  <text x="213" y="183" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">← I={fmt(i)}A (공통 전류)</text>
  <!-- 요약 박스 -->
  <rect x="80" y="200" width="240" height="28" fill="#1e293b" rx="8"/>
  <text x="200" y="218" text-anchor="middle" fill="#a5b4fc" font-size="11" font-family="monospace">R_eq={fmt(req)}Ω  |  I_total={fmt(i)}A</text>
</svg>"""

# ── SVG 회로 다이어그램 생성 함수 (병렬) ──────────────────────────────────
def parallel_circuit_svg(v, r1, r2, i1, i2, itot, req, p1, p2):
    p_max = max(p1, p2, 0.01)
    a1 = min(0.85, p1 / p_max * 0.85)
    a2 = min(0.85, p2 / p_max * 0.85)
    wc = "#60a5fa"
    return f"""
<svg viewBox="0 0 400 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#090d16;border-radius:10px;border: 1px solid #1e293b;">
  <text x="200" y="17" text-anchor="middle" fill="#64748b" font-size="11" font-family="monospace">⚡ 병렬 회로 실시간 시뮬레이션</text>
  <!-- 배터리 (좌측 세로, y=65~195) -->
  <line x1="40" y1="65" x2="40" y2="103" stroke="{wc}" stroke-width="2.5"/>
  <line x1="22" y1="103" x2="58" y2="103" stroke="#38bdf8" stroke-width="4"/>
  <line x1="29" y1="118" x2="51" y2="118" stroke="#38bdf8" stroke-width="2"/>
  <line x1="40" y1="118" x2="40" y2="195" stroke="{wc}" stroke-width="2.5"/>
  <text x="63" y="108" fill="#34d399" font-size="12" font-family="monospace">+</text>
  <text x="63" y="123" fill="#f87171" font-size="12" font-family="monospace">-</text>
  <text x="40" y="162" text-anchor="middle" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace">{v}V</text>
  <!-- 상단 수평 버스 -->
  <line x1="40" y1="65" x2="360" y2="65" stroke="{wc}" stroke-width="2.5"/>
  <!-- 하단 수평 버스 -->
  <line x1="40" y1="195" x2="360" y2="195" stroke="{wc}" stroke-width="2.5"/>
  <!-- 우측 마감선 -->
  <line x1="360" y1="65" x2="360" y2="195" stroke="{wc}" stroke-width="2.5"/>
  <!-- R1 세로 가지 -->
  <line x1="148" y1="65" x2="148" y2="103" stroke="{wc}" stroke-width="2"/>
  <rect x="108" y="103" width="80" height="38" fill="rgba(165,180,252,{a1:.2f})" stroke="#a5b4fc" stroke-width="2.5" rx="6"/>
  <text x="148" y="126" text-anchor="middle" fill="#e0e7ff" font-size="12" font-weight="bold" font-family="monospace">R₁={r1}Ω</text>
  <line x1="148" y1="141" x2="148" y2="195" stroke="{wc}" stroke-width="2"/>
  <text x="97" y="120" text-anchor="end" fill="#a5b4fc" font-size="10" font-family="monospace">I₁={fmt(i1)}A</text>
  <text x="97" y="133" text-anchor="end" fill="#a5b4fc" font-size="10" font-family="monospace">P₁={fmt(p1)}W</text>
  <!-- R2 세로 가지 -->
  <line x1="268" y1="65" x2="268" y2="103" stroke="{wc}" stroke-width="2"/>
  <rect x="228" y="103" width="80" height="38" fill="rgba(129,140,248,{a2:.2f})" stroke="#818cf8" stroke-width="2.5" rx="6"/>
  <text x="268" y="126" text-anchor="middle" fill="#e0e7ff" font-size="12" font-weight="bold" font-family="monospace">R₂={r2}Ω</text>
  <line x1="268" y1="141" x2="268" y2="195" stroke="{wc}" stroke-width="2"/>
  <text x="319" y="120" fill="#818cf8" font-size="10" font-family="monospace">I₂={fmt(i2)}A</text>
  <text x="319" y="133" fill="#818cf8" font-size="10" font-family="monospace">P₂={fmt(p2)}W</text>
  <!-- 방향 화살표 및 라벨 -->
  <text x="131" y="90" text-anchor="middle" fill="#34d399" font-size="14" font-family="monospace">↓</text>
  <text x="251" y="90" text-anchor="middle" fill="#34d399" font-size="14" font-family="monospace">↓</text>
  <text x="90" y="57" text-anchor="middle" fill="#34d399" font-size="10" font-family="monospace">→ I={fmt(itot)}A</text>
  <text x="200" y="215" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">V₁ = V₂ = {v}V (공통 전압)</text>
  <!-- 요약 박스 -->
  <rect x="80" y="228" width="240" height="24" fill="#1e293b" rx="7"/>
  <text x="200" y="244" text-anchor="middle" fill="#a5b4fc" font-size="11" font-family="monospace">R_eq={fmt(req)}Ω  |  I_total={fmt(itot)}A</text>
</svg>"""

# ── 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.inquiry-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-left: 5px solid #38bdf8;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);
}
.step-header {
    background: linear-gradient(90deg, #1e293b, #0f172a);
    border: 1.5px solid rgba(56, 189, 248, 0.2);
    border-radius: 10px;
    padding: 14px 20px;
    margin: 20px 0 12px 0;
    font-weight: 700;
    color: #38bdf8;
    font-size: 1.15rem;
}
.formula-block {
    background: #0b1329;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 18px;
}
.energy-gauge-container {
    background: #090d16;
    border: 1.5px solid #1e293b;
    border-radius: 10px;
    padding: 18px;
    margin-top: 15px;
}
.interactive-qa {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──────────────────────────────────────
if 'worksheet_score' not in st.session_state:
    st.session_state.worksheet_score = 0
if 'ws_submits' not in st.session_state:
    st.session_state.ws_submits = {}

# ══════════════════════════════════════════════════════════════
# 헤더 섹션
# ══════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-title'>🔌 저항의 연결과 소비전력 탐구 시뮬레이터</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>활동지 구성을 바탕으로 탐구 질문, 시뮬레이션, 수식 유도를 유기적으로 학습하는 공간입니다.</p>", unsafe_allow_html=True)

# 탭 구조 설계 (활동지 흐름)
tab_inquiry, tab_derivation, tab_simulation, tab_worksheet = st.tabs([
    "🚀 [1단계] 탐구 질문과 물리 직관",
    "📐 [2단계] 전기에너지 & 전력 공식 유도",
    "🎛️ [3단계] 직렬 vs 병렬 가상 실험실",
    "📝 [4단계] 디지털 활동지 & 평가"
])

# ══════════════════════════════════════════════════════════════
# [1단계] 탐구 질문과 물리 직관
# ══════════════════════════════════════════════════════════════
with tab_inquiry:
    st.markdown("### 🚀 E. 전자를 흐르게 하기 위한 전기력의 일과 에너지 전환")
    
    st.markdown("""
    <div class='inquiry-card'>
        <b style='color:#38bdf8; font-size:1.1rem;'>💡 핵심 탐구 과제</b><br>
        <span style='color:#e2e8f0; font-size:0.95rem; line-height: 1.7;'>
        전자가 도선 내부를 이동할 때 배터리가 공급하는 전기력은 일(Work)을 합니다. 이 일은 도선 내부에서 어떤 현상을 일으키고 어떤 형태의 에너지로 전환될까요? 아래 질문들을 깊이 고민해 봅시다.
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        st.subheader("💡 질문 1")
        st.info("**도선에 흐르는 전류(전자)는 등속 운동을 할까요, 아니면 가속 운동을 할까요?**")
        q1_ans = st.radio("질문 1에 대한 나의 생각 선택:", [
            "선택해 주세요",
            "전기력을 계속 받으므로 속도가 점점 빨라지는 가속 운동을 한다.",
            "금속 원자들과의 충돌로 인해 평균적으로 일정한 속도를 유지하는 등속 운동을 한다."
        ], key="inquiry_q1")
        
        if q1_ans != "선택해 주세요":
            if "등속 운동" in q1_ans:
                st.success("🎯 **정답입니다!** 전자는 전기력에 의해 가속되지만, 격자 구조의 금속 원자핵들과 끊임없이 충돌하면서 저항(마찰력과 유사)을 받아 **평균적으로 일정한 속력(유동 속도)**으로 이동하는 **등속 직선 운동**을 하게 됩니다.")
            else:
                st.error("❌ **다시 생각해 봅시다.** 만약 끊임없이 가속된다면 도선의 전류가 시간에 따라 무한히 증가해야 합니다. 금속 내부의 무언가가 전자의 운동을 방해하지 않을까요?")

    with col_q2:
        st.subheader("💡 질문 2")
        st.info("**도선 속 전자에 작용하는 힘에는 무엇이 있을까요?**")
        q2_ans = st.radio("질문 2에 대한 나의 생각 선택:", [
            "선택해 주세요",
            "전압에 의한 전기력만 작용한다.",
            "전압에 의한 전기력과 원자 충돌에 의한 저항력(방해하는 힘)이 함께 작용한다."
        ], key="inquiry_q2")
        
        if q2_ans != "선택해 주세요":
            if "저항력" in q2_ans:
                st.success("🎯 **정답입니다!** 전압이 형성하는 전기장 내부에서 전자는 순방향 **전기력($F = qE$)**을 받고, 동시에 원자핵과의 충돌에 의해 반대 방향으로 작용하는 **저항력(마찰 효과)**을 받습니다. 이 두 힘이 평형을 이루어 전자가 등속으로 움직이게 됩니다.")
            else:
                st.error("❌ **다시 생각해 봅시다.** 전자가 등속으로 움직이기 위해서는 짜맞춘 듯이 알짜힘이 0이 되어야 합니다. 전기력 외에 반대 방향으로 방해하는 힘이 존재해야 합니다.")

    st.markdown("---")
    st.markdown("""
    <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b;'>
        <b style='color: #818cf8;'>🔥 줄 열(Joule Heat)의 탄생</b><br>
        전자가 전기력으로부터 얻은 운동에너지는 금속 원자핵과의 충돌을 통해 <b>원자의 열진동 에너지</b>로 전환됩니다. 
        이것이 바로 저항기에서 열이 발생하는 원리이며, 공급된 <b>전기에너지가 100% 열에너지(소비전력)로 전환</b>되는 물리적 배경입니다.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# [2단계] 전기에너지 & 전력 공식 유도
# ══════════════════════════════════════════════════════════════
with tab_derivation:
    st.markdown("### 📐 전기에너지와 전력량의 대수 수식 유도")
    
    st.markdown("""
    활동지 단계를 따라 전기에너지($W$), 전력($P$), 그리고 전력량의 유도 과정을 확인하고, 가상 변수를 조절하여 실시간으로 변화하는 수식을 확인하세요.
    """)

    # 연동형 슬라이더
    col_dv1, col_dv2 = st.columns([1, 3])
    with col_dv1:
        st.markdown("##### ⚙️ 계산 변수 설정")
        dv_v = st.slider("인가 전압 V (V)", 1, 220, 110, key="dv_v")
        dv_r = st.slider("저항 값 R (Ω)", 1, 100, 20, key="dv_r")
        dv_t = st.slider("사용 시간 t (초)", 1, 60, 10, key="dv_t")
        
        # 물리량 계산
        dv_i = dv_v / dv_r
        dv_w = dv_v * dv_i * dv_t
        dv_p = dv_v * dv_i
        dv_wh = (dv_p * (dv_t / 3600)) # Wh 단위
        
    with col_dv2:
        st.markdown("<div class='formula-block'>", unsafe_allow_html=True)
        st.subheader("📚 단계별 수식 증명 학습")
        
        # 가. 전기에너지 W
        st.markdown("##### **가. 전기에너지 ($W$)**")
        st.caption("전류가 흐를 때 회로에 공급되거나 소비되는 총 에너지량 [단위: J (줄)]")
        st.latex(rf"W = V \cdot I \cdot t = I^2 \cdot R \cdot t = \frac{{V^2}}{{R}} \cdot t")
        st.markdown(f"**실시간 대입 결과:**")
        st.latex(rf"W = {dv_v}\text{{ V}} \times {fmt(dv_i)}\text{{ A}} \times {dv_t}\text{{ s}} \approx {fmt(dv_w)}\text{{ J (Joule)}}")
        
        # 다. 전력 P
        st.markdown("##### **다. 전력 ($P$)**")
        st.caption("1초 동안 소비하거나 생산되는 전기에너지 [단위: W (와트)]")
        st.latex(rf"P = \frac{{W}}{{t}} = V \cdot I = I^2 \cdot R = \frac{{V^2}}{{R}}")
        st.markdown(f"**실시간 대입 결과:**")
        st.latex(rf"P = \frac{{{fmt(dv_w)}\text{{ J}}}}{{{dv_t}\text{{ s}}}} = {dv_v}\text{{ V}} \times {fmt(dv_i)}\text{{ A}} \approx {fmt(dv_p)}\text{{ W (Watt)}}")

        # 라. 전력량
        st.markdown("##### **라. 전력량 (Electricity Consumption)**")
        st.caption("일정 시간(보통 시간 단위, h) 동안 소비하는 전기에너지의 총량 [단위: Wh]")
        st.latex(rf"\text{{전력량}} = P \cdot t_{{hour}} = {fmt(dv_p)}\text{{ W}} \times \left(\frac{{{dv_t}}}{{3600}}\right)\text{{ h}} \approx {fmt(dv_wh)}\text{{ Wh}}")
        
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# [3단계] 직렬 vs 병렬 가상 실험실
# ══════════════════════════════════════════════════════════════
with tab_simulation:
    st.markdown("### 🎛️ 직렬 vs 병렬 연결에 따른 소비전력 실시간 가상 실험")
    st.write("변수를 조정하면 두 회로 방식의 저항 온도(발열 수준)와 소비전력이 실시간으로 시각화됩니다.")
    
    sim_mode = st.radio("🔋 회로 연결 방식 선택", ["직렬 연결 (Series)", "병렬 연결 (Parallel)"], horizontal=True)
    
    col_ctrl, col_circ, col_analysis = st.columns([1, 1.4, 1.6])
    
    with col_ctrl:
        st.markdown("##### ⚙️ 회로 변수 조절")
        v = st.slider("입력 전압 (V)", 1, 24, 12, key="sim_v")
        r1 = st.slider("저항 R1 (Ω)", 1, 20, 4, key="sim_r1")
        r2 = st.slider("저항 R2 (Ω)", 1, 20, 8, key="sim_r2")
        
    if sim_mode == "직렬 연결 (Series)":
        req = r1 + r2
        i = v / req
        v1 = i * r1
        v2 = i * r2
        p1 = (i ** 2) * r1
        p2 = (i ** 2) * r2
        ptot = p1 + p2
        
        with col_circ:
            st.markdown(series_circuit_svg(v, r1, r2, i, v1, v2, req, p1, p2), unsafe_allow_html=True)
            
        with col_analysis:
            st.markdown("<div class='formula-block'>", unsafe_allow_html=True)
            st.write("##### 📐 직렬 소비전력 수식 유도")
            st.latex(rf"I = \frac{{V}}{{R_1 + R_2}} = \frac{{{v}}}{{{r1} + {r2}}} \approx {fmt(i)}\,A")
            st.latex(rf"P_1 = I^2 \cdot R_1 = ({fmt(i)})^2 \times {r1} \approx {fmt(p1)}\,W")
            st.latex(rf"P_2 = I^2 \cdot R_2 = ({fmt(i)})^2 \times {r2} \approx {fmt(p2)}\,W")
            st.latex(rf"P_1 : P_2 = R_1 : R_2 = {r1} : {r2}")
            st.markdown("</div>", unsafe_allow_html=True)

    else: # 병렬 연결 (Parallel)
        req = 1 / ((1 / r1) + (1 / r2))
        i_tot = v / req
        i1 = v / r1
        i2 = v / r2
        p1 = (v ** 2) / r1
        p2 = (v ** 2) / r2
        ptot = p1 + p2
        
        with col_circ:
            st.markdown(parallel_circuit_svg(v, r1, r2, i1, i2, i_tot, req, p1, p2), unsafe_allow_html=True)
            
        with col_analysis:
            st.markdown("<div class='formula-block'>", unsafe_allow_html=True)
            st.write("##### 📐 병렬 소비전력 수식 유도")
            st.latex(rf"R_{{eq}} = \frac{{R_1 \cdot R_2}}{{R_1 + R_2}} \approx {fmt(req)}\,\Omega")
            st.latex(rf"P_1 = \frac{{V^2}}{{R_1}} = \frac{{{v}^2}}{{{r1}}} \approx {fmt(p1)}\,W")
            st.latex(rf"P_2 = \frac{{V^2}}{{R_2}} = \frac{{{v}^2}}{{{r2}}} \approx {fmt(p2)}\,W")
            st.latex(rf"P_1 : P_2 = \frac{{1}}{{R_1}} : \frac{{1}}{{R_2}} = {r2} : {r1}")
            st.markdown("</div>", unsafe_allow_html=True)

    # 비주얼 에너지 전환 밸런스 게이지
    st.markdown("<div class='energy-gauge-container'>", unsafe_allow_html=True)
    st.markdown(f"##### 🔥 실시간 소비 전력(열에너지 방출량) 밸런스 (총 {fmt(ptot)} W)")
    
    ratio_p1 = (p1 / max(0.01, ptot)) * 100
    ratio_p2 = (p2 / max(0.01, ptot)) * 100
    
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; margin-bottom: 5px; font-size:0.85rem; font-family:monospace; color:#cbd5e1;'>
        <span style='color:#a5b4fc;'>R1 발열량 ({r1}Ω): {fmt(p1)} W ({fmt(ratio_p1)}%)</span>
        <span style='color:#818cf8;'>R2 발열량 ({r2}Ω): {fmt(p2)} W ({fmt(ratio_p2)}%)</span>
    </div>
    <div style='background:#1e293b; border-radius:9999px; height:20px; width:100%; display:flex; overflow:hidden;'>
        <div style='background:#a5b4fc; width:{ratio_p1}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P1</div>
        <div style='background:#818cf8; width:{ratio_p2}%; height:100%; text-align:center; color:#0f172a; font-weight:bold; font-size:0.75rem; line-height:20px;'>P2</div>
    </div>
    """, unsafe_allow_html=True)
    
    if sim_mode == "직렬 연결 (Series)":
        st.markdown("""
        💡 **물리 직관 (직렬)**: 직렬 회로는 모든 구간에 동일한 전류($I$)가 공통으로 통과합니다. 따라서 **저항이 클수록 ($P = I^2R$)** 전기적 충돌이 격렬해져 **더 많은 전기에너지를 열로 전환**합니다.
        """)
    else:
        st.markdown("""
        💡 **물리 직관 (병렬)**: 병렬 회로는 모든 가지에 동일한 전압($V$)이 걸립니다. 따라서 **저항이 작을수록 ($P = V^2/R$)** 전자가 원활하고 많이 흐르게 되어 **더 많은 전기에너지를 열로 전환**합니다.
        """)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# [4단계] 디지털 활동지 & 평가
# ══════════════════════════════════════════════════════════════
with tab_worksheet:
    st.markdown("### 📝 디지털 탐구 활동지 작성 및 개념 진단")
    st.write("위 시뮬레이션 가상실험 결과를 바탕으로 아래 활동지 빈칸을 알맞게 채워 탐구를 마쳐봅시다.")
    
    st.markdown("<div class='step-header'>✍️ 탐구 활동지 채우기</div>", unsafe_allow_html=True)
    
    # 활동지 문제 1
    st.markdown("**1. 같은 시간 동안 소비되는 전기에너지는 직렬연결에서는 저항에 ( ㉠ )하고, 병렬연결에서는 저항에 ( ㉡ )한다.**")
    ws_blank1 = st.text_input("㉠에 들어갈 알맞은 단어 (예: 비례, 반비례)", key="ws_b1").strip()
    ws_blank2 = st.text_input("㉡에 들어갈 알맞은 단어 (예: 비례, 반비례)", key="ws_b2").strip()
    
    if st.button("🚀 활동지 1번 제출"):
        if ws_blank1 == "비례" and ws_blank2 == "반비례":
            st.success("🎉 **완벽한 정답입니다!** 직렬에서는 저항값에 비례하고, 병렬에서는 저항값에 반비례(역수에 비례)하여 에너지가 소비됩니다.")
            if "ws_q1" not in st.session_state.ws_submits:
                st.session_state.worksheet_score += 50
                st.session_state.ws_submits["ws_q1"] = True
        else:
            st.error("❌ **틀렸습니다.** 3단계 가상실험 탭의 '물리 직관' 설명을 다시 한 번 꼼꼼히 읽어보세요.")

    st.markdown("---")

    # 활동지 문제 2 (실무 응용)
    st.markdown("**2. 가정용 전자기기는 모두 멀티탭에 ( ㉢ )로 연결됩니다. 이때 멀티탭에 너무 많은 전자기기를 꽂아 사용하면 발생하는 화재 위험의 근본적인 물리학적 원인은 무엇일까요?**")
    ws_blank3 = st.selectbox("㉢에 들어갈 연결 방법:", ["선택해 주세요", "직렬", "병렬"], key="ws_b3")
    ws_explain = st.text_area("화재 위험이 커지는 이유를 전력(소비전력) 및 합성저항 개념을 포함하여 서술해 보세요:", key="ws_b4")
    
    if st.button("🚀 활동지 2번 제출"):
        if ws_blank3 == "병렬":
            st.success("""
            🎯 **정답 및 해설:**
            가정용 기기는 모두 **병렬**로 연결됩니다. 병렬 연결 기기가 늘어날수록 회로의 **전체 합성 저항이 감소**하여, 메인 도선에 흐르는 **전체 전류($I_{total}$)가 급격히 증가**하게 됩니다.
            이에 따라 도선 자체의 저항에 의해 발생하는 소비 전력(열에너지, $P=I^2R$)이 전류의 제곱에 비례하여 기하급수적으로 폭증하게 되어 도선이 녹거나 화재가 발생할 수 있습니다!
            """)
            if "ws_q2" not in st.session_state.ws_submits:
                st.session_state.worksheet_score += 50
                st.session_state.ws_submits["ws_q2"] = True
        else:
            st.error("❌ ㉢ 연결 방식을 다시 생각해 보세요. 집안의 불 하나를 꺼도 다른 가전이 꺼지지 않는 연결 방식입니다.")

    st.markdown(f"""
    <div style="text-align: right; margin-top: 20px; font-size: 1.1rem; color: #38bdf8; font-weight: bold;">
        현재 탐구 활동 점수: <span style="font-family: monospace; font-size: 1.3rem;">{st.session_state.worksheet_score} / 100 점</span>
    </div>
    """, unsafe_allow_html=True)
