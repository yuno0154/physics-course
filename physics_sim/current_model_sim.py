"""
도선 내 전하 흐름 모델 개념 학습 시뮬레이터 (Current Model Sim)
- Pygame 기반 데스크톱 시뮬레이터를 고성능 브라우저 SVG 애니메이션 기반 Streamlit 웹 앱으로 완벽 이식
- 전압 0V(무질서한 열운동) vs 전압 인가 시(드리프트 유동 및 전류 유도) 미시 모델 시각화
- 전기장 방향, 전자 이동 방향, 전류 방향의 물리적 모순과 정의 완전 비교 분석
- 빗면 전위차 비유 모델 및 금속 양이온 충돌(저항의 미시적 원인) 스파크 애니메이션
- 자가 개념 진단 퀴즈 및 학습 스코어보드 연동
"""

import streamlit as st
import random

# 소수점 2자리 반올림 포맷팅 Helper
def fmt(val):
    return round(val, 2)

# ── 공통 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border-left: 5px solid #fbbf24;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.1);
}
.step-header {
    background: linear-gradient(90deg, #1e293b, #0f172a);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 12px 18px;
    margin: 15px 0 10px 0;
    font-weight: 700;
    color: #fbbf24;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.stats-container {
    background: #0f172a;
    border: 1.5px solid #1e293b;
    border-radius: 12px;
    padding: 18px;
    margin-top: 15px;
}
.concept-table {
    width: 100%;
    border-collapse: collapse;
    margin: 15px 0;
    font-size: 0.88rem;
}
.concept-table th {
    background: #1e293b;
    color: #fbbf24;
    padding: 10px;
    text-align: center;
    border: 1px solid #334155;
}
.concept-table td {
    padding: 10px;
    border: 1px solid #334155;
    text-align: center;
    color: #cbd5e1;
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
</style>
""", unsafe_allow_html=True)

# ── session_state 초기화 ──────────────────────────────────────
if 'cms_score' not in st.session_state:
    st.session_state.cms_score = 0
if 'cms_q1_feedback' not in st.session_state:
    st.session_state.cms_q1_feedback = None
if 'cms_q2_feedback' not in st.session_state:
    st.session_state.cms_q2_feedback = None

# ══════════════════════════════════════════════════════════════
# 헤더 섹션
# ══════════════════════════════════════════════════════════════
st.markdown("<h1 class='main-title'>🔌 도선 내 전하 흐름 모델 개념 학습실</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>도선 내부를 미시적으로 들여다보며 자유 전하, 전위, 전류, 저항의 물리적 상호작용 모델을 분석합니다.</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <b style='color:#fbbf24; font-size:1.05rem;'>💡 미시적 모델의 핵심 물리 상식</b><br>
    <span style='color:#e2e8f0; font-size:0.92rem; line-height: 1.6;'>
    1. <b>전압이 없을 때 (0V)</b>: 도선 내부의 자유 전자들은 무질서하게 사방으로 끊임없이 <b>열운동(Random thermal motion)</b>을 하지만 알짜 이동량은 0이므로 전류가 흐르지 않습니다.<br>
    2. <b>전압이 있을 때 (>0V)</b>: 도선 내부에 <b>전기장(Electric Field, $\vec{E}$)</b>이 형성되어 전자가 전기력을 받아 <b>(+)극(고전위) 방향으로 유동(Drift)</b>하기 시작하고, 이에 따라 알짜 전하 흐름인 <b>전류</b>가 유도됩니다.
    </span>
</div>
""", unsafe_allow_html=True)

# 탭 배치 (미시적 전하 유동 모델, 경사면 비유 모델, 미시 개념 진단)
tab_micro, tab_analogy, tab_quiz = st.tabs([
    "🔬 미시적 전하 유동 모델 (Microscopic Model)",
    "📐 전위차 경사면 비유 모델 (Slope Analogy)",
    "🏆 미시 개념 진단 평가 (Concept Test)"
])

# ══════════════════════════════════════════════════════════════
# 탭 1: 미시적 전하 유동 모델
# ══════════════════════════════════════════════════════════════
with tab_micro:
    col_ctrl, col_sim = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown("<div class='step-header'>🎛️ 1. 전압 조절 컨트롤</div>", unsafe_allow_html=True)
        voltage = st.slider("인가 전압 (V)", 0.0, 10.0, 0.0, step=0.5, key="cms_voltage")
        
        st.markdown("<div class='step-header'>👁️ 2. 시각 설정</div>", unsafe_allow_html=True)
        show_electric_field = st.checkbox("전기장 벡터 (E) 방향 표시", True, key="cms_show_ef")
        show_current_dir = st.checkbox("가상의 전류 (I) 방향 표시", True, key="cms_show_cur")
        show_spark = st.checkbox("원자핵 충돌(저항 발생) 스파크 표시", True, key="cms_show_spark")
        
    with col_sim:
        st.markdown("### 🔬 도선 내 자유 전자 및 격자 충돌 실시간 시뮬레이션")
        
        # --- 동적 SVG 애니메이션 생성 ---
        # 전압에 비례한 전자의 평균 유동 속도(Drift speed) 계산
        drift_speed = voltage * 0.4
        
        # 자유 전하(전자)들의 실시간 SVG 렌더링 루프
        electrons_svg = ""
        sparks_svg = ""
        
        # 도선 내부에 32개의 전자를 배치하여 전압 조건에 따른 운동 정의
        random.seed(42)  # 재현성을 위한 시드 고정
        for i in range(32):
            # 기본 고정 시작점
            base_x = random.randint(30, 520)
            base_y = random.randint(30, 150)
            
            if voltage == 0.0:
                # 0V 일 때는 각기 다른 방향으로 부들부들 떠는 열운동(Random thermal loop) 묘사
                angle = random.uniform(0, 3.14 * 2)
                r_amp = random.randint(4, 10)
                dx1 = r_amp * 0.7 * (1 if i%2==0 else -1)
                dy1 = r_amp * 0.7 * (1 if i%3==0 else -1)
                
                electrons_svg += f"""
                <circle cx="{base_x}" cy="{base_y}" r="6.5" fill="#f59e0b" stroke="#fff" stroke-width="1" opacity="0.9">
                  <animate attributeName="cx" values="{base_x}; {base_x + dx1}; {base_x - dx1}; {base_x}" dur="{random.uniform(0.3, 0.7)}s" repeatCount="indefinite" />
                  <animate attributeName="cy" values="{base_y}; {base_y + dy1}; {base_y - dy1}; {base_y}" dur="{random.uniform(0.3, 0.7)}s" repeatCount="indefinite" />
                </circle>
                """
            else:
                # 전압이 있을 때는 오른쪽(-)에서 왼쪽(+)으로 일정한 방향성을 가지고 드리프트(Drift)하는 애니메이션
                # 슬라이더 값에 비례하여 애니메이션 속도 조절 (dur는 속도의 반비례)
                dur = max(0.3, 8.0 - voltage * 0.7)
                begin_offset = random.uniform(0, dur)
                
                # 도선 경계: x=25 ~ x=525 사이를 좌측으로 드리프트하고 우측에서 재유입
                electrons_svg += f"""
                <circle cx="0" cy="{base_y}" r="6.5" fill="#f59e0b" stroke="#fff" stroke-width="1" opacity="0.95">
                  <animateMotion dur="{dur}s" repeatCount="indefinite" path="M {base_x},0 L {base_x - 550},0" begin="-{begin_offset}s" />
                </circle>
                """
                
                # 충돌 격자(저항 원자핵) 근처를 지날 때 스파크 시각화
                if show_spark and voltage > 2.0:
                    # 양이온 원자핵 격자의 X 좌표들과 매칭될 때 스파크(노란원 깜빡임) 생성
                    for ion_x in [100, 180, 260, 340, 420, 500]:
                        if abs(base_x - ion_x) < 40 and base_y % 3 == 0:
                            sparks_svg += f"""
                            <circle cx="{ion_x}" cy="{base_y}" r="15" fill="#fef08a" opacity="0.4" filter="url(#blur-spark)">
                              <animate attributeName="opacity" values="0.4; 0.0; 0.4" dur="0.2s" repeatCount="indefinite" />
                            </circle>
                            """

        # 고정된 금속 양이온(Copper Lattice, (+) 원자핵) 격자선 배치 (저항 소자 근원)
        ions_svg = ""
        # 6개의 열과 3개의 행으로 구성된 (+) 격자 배치
        for ix in [100, 180, 260, 340, 420, 500]:
            for iy in [45, 90, 135]:
                ions_svg += f"""
                <!-- 양이온 원자핵 -->
                <circle cx="{ix}" cy="{iy}" r="10" fill="#3b82f6" stroke="#60a5fa" stroke-width="1.5" />
                <text x="{ix}" y="{iy + 4}" fill="#fff" font-weight="bold" font-family="sans-serif" font-size="12" text-anchor="middle">+</text>
                """

        # 전기장 벡터 방향 지시 화살표
        ef_arrow = ""
        if show_electric_field and voltage > 0.0:
            ef_arrow = """
            <g transform="translate(150, 10)">
              <path d="M 0,5 L 250,5" fill="none" stroke="#ea580c" stroke-width="2.5" marker-end="url(#arrow-red)" />
              <text x="125" y="-3" fill="#ea580c" font-size="10.5" font-weight="bold" font-family="sans-serif" text-anchor="middle">전기장 E 방향 (높은 전위 → 낮은 전위)</text>
            </g>
            """

        # 가상 전류 방향 지시 화살표
        cur_arrow = ""
        if show_current_dir and voltage > 0.0:
            cur_arrow = """
            <g transform="translate(150, 172)">
              <path d="M 0,5 L 250,5" fill="none" stroke="#38bdf8" stroke-width="2.5" marker-end="url(#arrow-blue)" />
              <text x="125" y="16" fill="#38bdf8" font-size="10.5" font-weight="bold" font-family="sans-serif" text-anchor="middle">전류 I 방향 (전자의 반대 방향 / (+)극 → (-)극)</text>
            </g>
            """

        # 전위차 그라데이션 및 등전위선 정보
        al = min(voltage / 10.0, 1.0)
        grad_color_stop = f"""
        <linearGradient id="potentialGradBar" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#ef4444" stop-opacity="{al * 0.4}" />
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="{al * 0.4}" />
        </linearGradient>
        """

        svg_markup = f"""
        <svg width="100%" height="255" viewBox="0 0 550 215" style="background-color: #0b1329; border: 1.5px solid #1e293b; border-radius: 16px;">
          <defs>
            {grad_color_stop}
            <marker id="arrow-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#ea580c" />
            </marker>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
              <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#38bdf8" />
            </marker>
            <filter id="blur-spark">
              <feGaussianBlur stdDeviation="3" />
            </filter>
          </defs>

          <!-- 도선 배경 (전위 경사에 따른 동적 색상 채우기) -->
          <rect x="25" y="20" width="500" height="140" fill="url(#potentialGradBar)" rx="10" stroke="#334155" stroke-width="2" />
          <rect x="25" y="20" width="500" height="140" fill="none" rx="10" stroke="#1e293b" stroke-width="1.5" />

          <!-- 좌우 전극 단자 블록 -->
          <g transform="translate(1, 20)">
            <rect x="0" y="0" width="24" height="140" fill="#ef4444" rx="4" opacity="0.9" />
            <text x="12" y="76" fill="#fff" font-weight="bold" font-family="sans-serif" font-size="11" text-anchor="middle" transform="rotate(-90 12 76)">+ 극 (고전위)</text>
          </g>
          <g transform="translate(525, 20)">
            <rect x="0" y="0" width="24" height="140" fill="#3b82f6" rx="4" opacity="0.9" />
            <text x="12" y="76" fill="#fff" font-weight="bold" font-family="sans-serif" font-size="11" text-anchor="middle" transform="rotate(90 12 76)">- 극 (저전위)</text>
          </g>

          <!-- 스파크(충돌) 효과 렌더링 -->
          {sparks_svg}

          <!-- 금속 양이온 격자 드로잉 -->
          {ions_svg}

          <!-- 자유 전하(전자)들의 실시간 운동 -->
          {electrons_svg}

          <!-- 방향 지시 벡터선 -->
          {ef_arrow}
          {cur_arrow}
        </svg>
        """

        # SVG 렌더링 (마크다운 들여쓰기 버그 예방용 strip 헬퍼 적용)
        clean_svg = "\n".join([line.strip() for line in svg_markup.split("\n")])
        st.markdown(clean_svg, unsafe_allow_html=True)

        # 범례 표시
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #3b82f6; border-radius: 50%;"></span> 고정된 구리 양이온 (+)</div>
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #f59e0b; border-radius: 50%;"></span> 이동하는 자유 전자 (e⁻)</div>
            <div><span style="display: inline-block; width: 10px; height: 10px; background-color: #fef08a; border-radius: 2px;"></span> 원자핵 격자 충돌 (저항의 원인)</div>
        </div>
        """, unsafe_allow_html=True)

    # 미시적 분석 대시보드
    st.markdown("<div class='stats-container'>", unsafe_allow_html=True)
    st.markdown("### 📊 실시간 미시적 상태 대시보드")
    col_d1, col_d2, col_d3 = st.columns(3)
    
    with col_d1:
        st.metric("전하 평균 유동 속도 (Drift velocity)", f"{fmt(drift_speed * 0.1)} mm/s" if voltage > 0 else "0.0 mm/s")
    with col_d2:
        st.metric("단면 통과 전하 흐름률 (Current I)", f"{fmt(voltage * 1.5)} A")
    with col_d3:
        st.metric("도선 내 평균 충돌 빈도", f"약 {int(voltage * 8)} 회/sec" if voltage > 0 else "0 회/sec")
    
    st.markdown("""
        <p style='font-size:0.75rem; color:#64748b; line-height:1.45; margin-top:10px;'>
            * <b>실제 물리 고증</b>: 전도성이 우수한 도선에서 전자의 실제 평균 유동 속도(Drift velocity)는 약 0.1 mm/s ~ 1 mm/s 정도로 매우 느립니다. 그럼에도 스위치를 켜는 순간 불이 즉시 켜지는 이유는, 전압 인가 시 도선 내 전체에 광속에 가까운 전자기파(전기장)가 순식간에 형성되어 모든 자유전자가 일제히 움직이기 시작하기 때문입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 전위차, 전기장, 전류 방향의 정의와 모순 비교표
    st.markdown("### ⚖️ 물리적 방향 정의 및 관계 대조표")
    st.markdown("""
    <table class='concept-table'>
        <thead>
            <tr>
                <th>구분</th>
                <th>전기장 ($\vec{E}$)</th>
                <th>자유 전자 ($e^-$)</th>
                <th>전류 ($I$)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td style='font-weight:bold; color:#fbbf24;'>물리적 방향</td>
                <td style='color:#ea580c; font-weight:bold;'>(+)극 → (-)극 (고전위 → 저전위)</td>
                <td style='color:#fbbf24; font-weight:bold;'>(-)극 → (+)극 (저전위 → 고전위)</td>
                <td style='color:#38bdf8; font-weight:bold;'>(+)극 → (-)극 (고전위 → 저전위)</td>
            </tr>
            <tr>
                <td style='font-weight:bold;'>방향 설정의 원인</td>
                <td>양전하가 전기력을 받는 방향으로 약속</td>
                <td>(-) 음전하를 띠어 전기장 반대 방향으로 힘을 받음</td>
                <td>전자의 실체가 밝혀지기 전 (+)전하의 흐름으로 임의 규정</td>
            </tr>
            <tr>
                <td style='font-weight:bold;'>역학적 비유</td>
                <td>빗면의 경사 하강 방향</td>
                <td>빗면 위로 스스로 기어올라가는 구슬</td>
                <td>빗면을 따라 아래로 흐르는 물줄기</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 2: 전위차 경사면 비유 모델
# ══════════════════════════════════════════════════════════════
with tab_analogy:
    st.markdown("### 📐 전위(Potential)와 중력 경사면 비유 모델")
    
    col_ctrl_a, col_sim_a = st.columns([1, 2])
    
    with col_ctrl_a:
        st.markdown("<div class='step-header'>🎛️ 경사도 및 마찰 제어</div>", unsafe_allow_html=True)
        slope_angle = st.slider("빗면 경사각 (전위차 비유)", 0, 45, 15, step=5, key="cms_slope_angle")
        pin_density = st.slider("충돌 못 개수 (전기 저항 비유)", 1, 10, 4, step=1, key="cms_pin_density")
        
        st.markdown("""
        <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; font-size:0.85rem; color:#cbd5e1; line-height:1.5; margin-top:15px;'>
            <b>💡 경사면 비유 분석 가이드</b><br>
            - <b>빗면의 높은 곳</b>: 고전위 (+)극<br>
            - <b>빗면의 낮은 곳</b>: 저전위 (-)극<br>
            - <b>굴러가는 쇠구슬</b>: 자유 전자 (e⁻)<br>
            - <b>빗면에 박힌 못</b>: 금속 양이온 (저항)<br><br>
            경사도(전압)가 높을수록 쇠구슬의 속도(전류)가 빨라지며, 못(저항)이 촘촘할수록 쇠구슬이 튕기며 하강을 방해받고 열(소비 전력)이 발생합니다.
        </div>
        """, unsafe_allow_html=True)
        
    with col_sim_a:
        # --- 경사면 비유 SVG 드로잉 ---
        # 경사도에 따라 빗면의 기울기 좌표 계산
        import math
        rad = math.radians(slope_angle)
        slope_y = 60 + math.sin(rad) * 200
        
        # 박힌 못(저항 격자) 렌더링
        pins_markup = ""
        for i in range(pin_density):
            px = 120 + i * (320 / max(1, pin_density))
            py = 60 + (px - 100) * math.sin(rad) * 0.4
            pins_markup += f"""
            <line x1="{px}" y1="{py}" x2="{px}" y2="{py + 25}" stroke="#94a3b8" stroke-width="4.5" stroke-linecap="round" />
            <circle cx="{px}" cy="{py}" r="6.5" fill="#e2e8f0" stroke="#475569" stroke-width="1.5" />
            """
            
        # 굴러떨어지는 쇠구슬(자유 전자) 애니메이션
        marbles_markup = ""
        if slope_angle > 0:
            dur_marb = max(0.4, 5.0 - slope_angle * 0.1)
            for j in range(3):
                offset_j = j * (dur_marb / 3)
                marbles_markup += f"""
                <circle r="7.5" fill="#f59e0b" stroke="#fff" stroke-width="1.5">
                  <animateMotion dur="{dur_marb}s" repeatCount="indefinite" path="M 100,50 L 450,{slope_y}" begin="-{offset_j}s" />
                </circle>
                """
        else:
            # 경사가 없을 때는 쇠구슬이 굴러가지 않고 멈춰있음
            marbles_markup = """
            <circle cx="100" cy="50" r="7.5" fill="#f59e0b" stroke="#fff" stroke-width="1.5" />
            <circle cx="200" cy="50" r="7.5" fill="#f59e0b" stroke="#fff" stroke-width="1.5" />
            """
            
        svg_analogy = f"""
        <svg width="100%" height="255" viewBox="0 0 550 215" style="background-color: #0b1329; border: 1.5px solid #1e293b; border-radius: 16px;">
          <!-- 빗면 베이스 라인 -->
          <path d="M 80,60 L 460,{slope_y} L 460,180 L 80,180 Z" fill="#1e293b" opacity="0.4" stroke="#475569" stroke-width="2" />
          <path d="M 80,60 L 460,{slope_y}" fill="none" stroke="#fbbf24" stroke-width="5" stroke-linecap="round" />

          <!-- 고전위 및 저전위 표시단 -->
          <circle cx="80" cy="60" r="14" fill="#ef4444" />
          <text x="80" y="64" fill="#fff" font-weight="bold" font-size="12" font-family="sans-serif" text-anchor="middle">+</text>
          <text x="80" y="38" fill="#ef4444" font-size="10" font-family="sans-serif" text-anchor="middle">고전위 (+) 높음</text>

          <circle cx="460" cy="{slope_y}" r="14" fill="#3b82f6" />
          <text x="460" y="{slope_y + 4}" fill="#fff" font-weight="bold" font-size="12" font-family="sans-serif" text-anchor="middle">-</text>
          <text x="460" y="{slope_y - 20}" fill="#3b82f6" font-size="10" font-family="sans-serif" text-anchor="middle">저전위 (-) 낮음</text>

          <!-- 저항 못 렌더링 -->
          {pins_markup}

          <!-- 굴러 떨어지는 전하(구슬) -->
          {marbles_markup}
        </svg>
        """
        
        clean_svg_a = "\n".join([line.strip() for line in svg_analogy.split("\n")])
        st.markdown(clean_svg_a, unsafe_allow_html=True)
        
        # 빗면 렌더링 범례
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; font-size: 0.8rem; color: #94a3b8; margin-top: 8px;">
            <div><span style="display: inline-block; width: 12px; height: 12px; background-color: #f59e0b; border-radius: 50%;"></span> 자유 전자 (쇠구슬)</div>
            <div><span style="display: inline-block; width: 6px; height: 12px; background-color: #94a3b8; border-radius: 1px;"></span> 전기 저항 (박힌 못)</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# 탭 3: 미시 개념 진단 평가
# ══════════════════════════════════════════════════════════════
with tab_quiz:
    st.markdown("<h3 style='color: #e2e8f0;'>🏆 도선 내 전하 유동 모델 자가 진단 평가</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94a3b8; font-size: 0.9rem;'>학습한 미시 전하 모델 지식을 바탕으로 자가 진단 평가를 풀며 오개념을 극복해 봅니다.</p>", unsafe_allow_html=True)
    
    # ── 문항 1 ────────────────────────────────────────────────
    st.markdown("""
    <div class='step-header'>❓ [문항 1] 전극 단자와 입자의 운동 방향</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; font-size:0.92rem; line-height:1.6;'>
        금속 도선 양단에 전압(전위차)을 걸어줄 때, 형성되는 <b>전기장의 방향</b>과 도선 내 <b>자유 전자의 실제 알짜 이동 방향</b>으로 올바르게 짝지어진 것은 무엇입니까?<br><br>
        ① 전기장: (+)극 → (-)극  |  자유 전자: (+)극 → (-)극<br>
        ② 전기장: (+)극 → (-)극  |  자유 전자: (-)극 → (+)극<br>
        ③ 전기장: (-)극 → (+)극  |  자유 전자: (+)극 → (-)극<br>
        ④ 전기장: (-)극 → (+)극  |  자유 전자: (-)극 → (+)극
    </div>
    """, unsafe_allow_html=True)
    
    q1_choice = st.radio(
        "문항 1 정답 선택",
        ["선택지를 골라주세요", "① 전기장: (+)극 → (-)극  |  자유 전자: (+)극 → (-)극", "② 전기장: (+)극 → (-)극  |  자유 전자: (-)극 → (+)극", "③ 전기장: (-)극 → (+)극  |  자유 전자: (+)극 → (-)극", "④ 전기장: (-)극 → (+)극  |  자유 전자: (-)극 → (+)극"],
        key="cms_q1_ans",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 문항 1 제출", key="cms_q1_btn"):
        if q1_choice == "② 전기장: (+)극 → (-)극  |  자유 전자: (-)극 → (+)극":
            st.session_state.cms_q1_feedback = {
                "success": True, 
                "text": "🎉 정답입니다! 전기장은 높은 전위((+)극)에서 낮은 전위((-)극) 방향으로 형성됩니다. 하지만 음(-)전하를 띤 자유 전자는 전기장과 반대 방향인 (-)극에서 (+)극 방향으로 힘을 받아 드리프트 운동하게 됩니다."
            }
            st.session_state.cms_score += 10
        elif q1_choice == "선택지를 골라주세요":
            st.session_state.cms_q1_feedback = {"success": False, "text": "⚠️ 정답을 골라주세요."}
        else:
            st.session_state.cms_q1_feedback = {
                "success": False, 
                "text": "❌ 오답입니다. 전기장은 양(+)전하가 힘을 받는 방향이므로 (+)극 → (-)극으로 설정되나, 전자는 음(-)전하를 띠고 있으므로 인력에 의해 (+)극 방향(즉, (-)극 → (+)극)으로 이끌려 가게 됩니다. 시뮬레이션의 화살표 방향을 다시 비교해 보세요."
            }
        st.rerun()

    # 문항 1 피드백 출력
    if st.session_state.cms_q1_feedback:
        fb1 = st.session_state.cms_q1_feedback
        if fb1["success"]:
            st.markdown(f"<div class='feedback-box-success'><b>✅ 정답입니다!</b><br>{fb1['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-box-error'><b>❌ 오답 또는 미선택!</b><br>{fb1['text']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── 문항 2 ────────────────────────────────────────────────
    st.markdown("""
    <div class='step-header'>❓ [문항 2] 전기 저항이 발생하는 미시적 근원</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #1e293b; font-size:0.92rem; line-height:1.6;'>
        금속 도선에 전류가 흐를 때 <b>전기 저항이 발생하는 근본적인 미시적 원인</b>은 무엇입니까?<br><br>
        ① 자유 전자의 질량이 너무 무거워 움직이기 힘들기 때문<br>
        ② 이동하는 자유 전자들끼리 서로 강하게 인력이 작용하기 때문<br>
        ③ 이동하는 자유 전자가 금속 도선 내부의 고정된 양이온(원자핵 격자)과 충돌하기 때문<br>
        ④ 도선 외부로 자유 전자들이 증발하여 빠져나가기 때문
    </div>
    """, unsafe_allow_html=True)
    
    q2_choice = st.radio(
        "문항 2 정답 선택",
        ["선택지를 골라주세요", "① 자유 전자의 질량이 너무 무거워 움직이기 힘들기 때문", "② 이동하는 자유 전자들끼리 서로 강하게 인력이 작용하기 때문", "③ 이동하는 자유 전자가 금속 도선 내부의 고정된 양이온(원자핵 격자)과 충돌하기 때문", "④ 도선 외부로 자유 전자들이 증발하여 빠져나가기 때문"],
        key="cms_q2_ans",
        label_visibility="collapsed"
    )
    
    if st.button("🚀 문항 2 제출", key="cms_q2_btn"):
        if q2_choice == "③ 이동하는 자유 전자가 금속 도선 내부의 고정된 양이온(원자핵 격자)과 충돌하기 때문":
            st.session_state.cms_q2_feedback = {
                "success": True, 
                "text": "🎉 정답입니다! 전기 저항의 본질적인 원인은 도선 내부에서 드리프트하는 자유 전자가 금속 양이온(원자핵 격자)과 부딪치며 전진을 방해받는 충돌 과정입니다. 이때 자유 전자의 운동 에너지가 열에너지(소비 전력)로 전환 방출됩니다."
            }
            st.session_state.cms_score += 10
        elif q2_choice == "선택지를 골라주세요":
            st.session_state.cms_q2_feedback = {"success": False, "text": "⚠️ 정답을 골라주세요."}
        else:
            st.session_state.cms_q2_feedback = {
                "success": False, 
                "text": "❌ 오답입니다. 도선 내에서 전자가 전진할 때 가장 지대한 방해를 받는 요인은 도선 내부의 구리 원자핵(양이온 격자)과의 물리적인 충돌 때문입니다. 비유 모델의 못(Pin)이나 충돌 섬광 묘사를 참고하여 다시 확인해 보세요."
            }
        st.rerun()

    # 문항 2 피드백 출력
    if st.session_state.cms_q2_feedback:
        fb2 = st.session_state.cms_q2_feedback
        if fb2["success"]:
            st.markdown(f"<div class='feedback-box-success'><b>✅ 정답입니다!</b><br>{fb2['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='feedback-box-error'><b>❌ 오답 또는 미선택!</b><br>{fb2['text']}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # 종합 스코어 표시
    st.markdown(f"""
    <div style="text-align: right; font-size: 0.9rem; color: #94a3b8; font-weight: bold;">
        현재 미시 개념 점수: <strong style="color: #fbbf24; font-size: 1.15rem; font-family: monospace;">{st.session_state.cms_score} pts</strong>
    </div>
    """, unsafe_allow_html=True)
