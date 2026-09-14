import streamlit as st
import plotly.graph_objects as go
import numpy as np

# --- 인쇄 및 스타일 CSS 설정 ---
st.markdown("""
    <style>
    @media print {
        @page { 
            size: A4 portrait; 
            margin: 12mm 12mm 15mm 12mm; 
        }
        html, body, .stApp { 
            width: 100% !important; 
            max-width: 100% !important; 
            background: white !important;
            overflow: visible !important; 
        }
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stActionButton, button, [data-testid="stRadio"], .no-print { 
            display: none !important; 
        }
        .main .block-container { 
            max-width: 100% !important; 
            padding: 0 !important; 
            margin: 0 !important; 
        }
        .stMarkdown { 
            page-break-inside: avoid !important; 
            break-inside: avoid !important; 
            margin-bottom: 4px !important; 
        }
        .exam-box { 
            page-break-inside: avoid !important; 
            break-inside: avoid !important; 
            border: 1px solid #94a3b8 !important; 
            background: white !important;
            padding: 12px 16px !important; 
            margin-bottom: 16px !important; 
            box-shadow: none !important;
        }
        svg { 
            max-width: 100% !important; 
            height: auto !important; 
            display: block !important; 
            margin: 6px auto !important; 
            page-break-inside: avoid !important; 
            break-inside: avoid !important; 
        }
        .svg-container {
            max-width: 100% !important;
            page-break-inside: avoid !important;
            break-inside: avoid !important;
        }
        h1 { font-size: 1.25rem !important; margin-bottom: 6px !important; }
        h2 { font-size: 1.05rem !important; margin-top: 8px !important; margin-bottom: 4px !important; }
        h3 { font-size: 0.95rem !important; margin-top: 4px !important; margin-bottom: 4px !important; }
        p, li { font-size: 0.85rem !important; line-height: 1.3 !important; }
        .answer-space { 
            border-bottom: 1px solid #64748b !important; 
            height: 26px !important; 
            margin-bottom: 6px !important; 
            width: 100% !important; 
        }
        .bar-chart-container { 
            page-break-inside: avoid !important; 
            break-inside: avoid !important; 
        }
        .stDivider { margin: 6px 0 !important; }
    }

    .print-header { 
        font-size: 0.95rem; 
        font-weight: bold; 
        margin-bottom: 12px; 
        border-bottom: 2px solid #1e293b; 
        padding-bottom: 6px; 
    }
    .answer-space { 
        border-bottom: 1px solid #94a3b8; 
        height: 28px; 
        margin-bottom: 6px; 
        width: 100%; 
    }
    .exam-box { 
        background-color: #f8fafc; 
        border: 1px solid #e2e8f0; 
        border-radius: 12px; 
        padding: 16px 20px; 
        margin-bottom: 16px; 
    }
    .badge-primary { background-color: #eff6ff; color: #1d4ed8; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-success { background-color: #ecfdf5; color: #047857; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-purple { background-color: #faf5ff; color: #7e22ce; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-amber { background-color: #fffbeb; color: #b45309; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    
    .svg-container {
        text-align: center;
        width: 100%;
        max-width: 520px;
        margin: 10px auto;
        overflow: visible;
    }

    /* 인쇄용 에너지 막대그래프 틀 */
    .bar-chart-container { display: flex; gap: 24px; justify-content: center; margin: 12px 0; }
    .bar-chart-card { border: 1px solid #cbd5e1; border-radius: 8px; padding: 10px 14px; background: white; text-align: center; width: 220px; }
    .bar-chart-title { font-size: 0.85rem; font-weight: bold; margin-bottom: 6px; color: #1e293b; }
    .bar-chart-frame { height: 120px; border-left: 2px solid #334155; border-bottom: 2px solid #334155; display: flex; justify-content: space-around; align-items: flex-end; padding: 0 4px; position: relative; }
    .bar-chart-bar-outline { width: 42px; border: 1.5px dashed #64748b; height: 105px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #64748b; font-weight: bold; background: #f8fafc; }
    .bar-chart-labels { display: flex; justify-content: space-around; margin-top: 4px; font-size: 0.72rem; color: #475569; font-weight: bold; }
    .tick-50 { position: absolute; top: 6px; left: -26px; font-size: 0.65rem; color: #64748b; font-weight: bold; }
    .tick-0 { position: absolute; bottom: -2px; left: -18px; font-size: 0.65rem; color: #64748b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 포물선 운동 실전 연습 문제")

# --- 출력 모드 선택 ---
col_mode1, col_mode2 = st.columns([1.8, 1])
with col_mode1:
    is_print_mode = st.toggle("🖨️ 학습지 출력 모드 전환 (인쇄 및 PDF 저장용)", value=False)
with col_mode2:
    if is_print_mode:
        if st.button("🖨️ 브라우저 바로 인쇄 / PDF 저장", use_container_width=True):
            st.components.v1.html("<script>parent.window.print()</script>", height=0)

if is_print_mode:
    st.markdown('<div class="print-header">📝 포물선 운동 실전 연습 학습지 &nbsp; [ 학년: ____ &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["🎯 실전 기출 & 활동지 연계 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    수능 및 내신 기출 핵심 문항과 [활동 6] 연계 **에너지 막대그래프 분석 문항**을 교과서급 정밀 벡터 일러스트와 함께 학습할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["🎯 실전 기출 & 활동지 연계 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 수능/EBS 교과서급 정밀 SVG 벡터 일러스트 생성 함수군
# (어떤 해상도나 인쇄 모드에서도 100% 잘림 없이 선명하게 비례 축소 렌더링됨)
# =========================================================================

def render_html(html_str):
    """HTML 및 SVG 문자열의 들여쓰기를 제거하여 Markdown 코드 블록 오작동을 방지하고 st.html로 안전하게 렌더링"""
    clean_html = "".join(line.strip() for line in html_str.splitlines())
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

COMMON_SVG_DEFS = """
    <defs>
        <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1d4ed8"/>
        </marker>
        <marker id="arr-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626"/>
        </marker>
        <marker id="arr-dark" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155"/>
        </marker>
        <pattern id="groundHatch" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
            <line x1="0" y1="0" x2="0" y2="10" stroke="#cbd5e1" stroke-width="1.5" />
        </pattern>
        <radialGradient id="sphereBlue" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stop-color="#bfdbfe"/>
            <stop offset="45%" stop-color="#2563eb"/>
            <stop offset="100%" stop-color="#1e3a8a"/>
        </radialGradient>
        <radialGradient id="sphereRose" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stop-color="#fecdd3"/>
            <stop offset="45%" stop-color="#e11d48"/>
            <stop offset="100%" stop-color="#881337"/>
        </radialGradient>
        <radialGradient id="sphereGreen" cx="35%" cy="35%" r="65%">
            <stop offset="0%" stop-color="#bbf7d0"/>
            <stop offset="45%" stop-color="#16a34a"/>
            <stop offset="100%" stop-color="#14532d"/>
        </radialGradient>
    </defs>
"""

def get_svg_prob1():
    """문제 1: 30도 40 m/s 포물선 운동 SVG (최고점 H, 도달거리 R)"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 210" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 지면 및 해칭 -->
        <rect x="25" y="160" width="490" height="12" fill="url(#groundHatch)" />
        <line x1="20" y1="160" x2="520" y2="160" stroke="#1e293b" stroke-width="2.5"/>
        
        <!-- 포물선 궤적 (Q 베지어 곡선으로 물리적 포물선 완벽 일치) -->
        <path d="M 60 160 Q 250 -30 440 160" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="5,4"/>
        
        <!-- 발사 지점 공 및 초기 속도 벡터 -->
        <circle cx="60" cy="160" r="8" fill="url(#sphereBlue)"/>
        <text x="36" y="164" font-size="13" font-weight="bold" font-style="italic" fill="#334155">2 kg</text>
        <line x1="60" y1="160" x2="135" y2="117" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arr-blue)"/>
        <text x="142" y="112" font-size="13" font-weight="bold" fill="#1e40af">v₀ = 40 m/s</text>
        
        <!-- 발사 각도 호 -->
        <path d="M 95 160 A 35 35 0 0 0 90.3 142.5" fill="none" stroke="#d97706" stroke-width="2"/>
        <text x="102" y="152" font-size="12" font-weight="bold" fill="#b45309">30°</text>
        
        <!-- 최고점 및 H 치수선 -->
        <circle cx="250" cy="65" r="4.5" fill="#dc2626"/>
        <line x1="250" y1="65" x2="250" y2="160" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="242" y1="65" x2="258" y2="65" stroke="#dc2626" stroke-width="1.5"/>
        <line x1="265" y1="68" x2="265" y2="157" stroke="#dc2626" stroke-width="1.5" marker-start="url(#arr-red)" marker-end="url(#arr-red)"/>
        <text x="275" y="117" font-size="13" font-weight="bold" fill="#b91c1c">H</text>
        <text x="250" y="52" font-size="12" font-weight="bold" fill="#0f172a" text-anchor="middle">최고점</text>
        
        <!-- 수평 도달 거리 R 치수선 -->
        <line x1="60" y1="185" x2="440" y2="185" stroke="#334155" stroke-width="1.5" marker-start="url(#arr-dark)" marker-end="url(#arr-dark)"/>
        <line x1="60" y1="178" x2="60" y2="192" stroke="#334155" stroke-width="1.5"/>
        <line x1="440" y1="178" x2="440" y2="192" stroke="#334155" stroke-width="1.5"/>
        <text x="250" y="202" font-size="13" font-weight="bold" fill="#1e293b" text-anchor="middle">R (수평 도달 거리)</text>
    </svg>
    </div>
    """

def get_svg_prob2():
    """문제 2: A, B(3.2m), C(1.6m) 세 지점 궤적 좌표축 SVG"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 220" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 좌표축 -->
        <line x1="50" y1="165" x2="500" y2="165" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-dark)"/>
        <line x1="70" y1="180" x2="70" y2="25" stroke="#1e293b" stroke-width="2" marker-end="url(#arr-dark)"/>
        <text x="500" y="180" font-size="11" font-weight="bold" fill="#334155" text-anchor="end">수평 방향 (m)</text>
        <text x="65" y="20" font-size="11" font-weight="bold" fill="#334155">높이 (m)</text>
        <text x="58" y="178" font-size="12" font-weight="bold" fill="#64748b">0</text>
        
        <!-- 포물선 궤적 (A -> B -> C) -->
        <path d="M 70 165 Q 250 -35 430 165" fill="none" stroke="#334155" stroke-width="2" stroke-dasharray="5,4"/>
        
        <!-- 지점 A (0, 0) -->
        <circle cx="70" cy="165" r="7.5" fill="url(#sphereBlue)"/>
        <text x="70" y="152" font-size="14" font-weight="bold" fill="#1e3a8a" text-anchor="middle">A</text>
        <line x1="70" y1="165" x2="115" y2="120" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
        <text x="122" y="122" font-size="12" font-weight="bold" fill="#1e40af">v₀</text>
        
        <!-- 지점 B (최고점 3.2m) -->
        <circle cx="250" cy="65" r="7.5" fill="url(#sphereRose)"/>
        <text x="250" y="52" font-size="14" font-weight="bold" fill="#9f1239" text-anchor="middle">B (최고점)</text>
        <line x1="250" y1="65" x2="250" y2="165" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="70" y1="65" x2="250" y2="65" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="58" y="69" font-size="11" font-weight="bold" fill="#e11d48" text-anchor="end">3.2</text>
        <line x1="250" y1="65" x2="295" y2="65" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
        <text x="300" y="60" font-size="11" font-weight="bold" fill="#1e40af">vx=6m/s</text>
        
        <!-- 지점 C (1.6m) -->
        <circle cx="377" cy="115" r="7.5" fill="url(#sphereGreen)"/>
        <text x="390" y="110" font-size="14" font-weight="bold" fill="#166534">C</text>
        <line x1="377" y1="115" x2="377" y2="165" stroke="#16a34a" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="70" y1="115" x2="377" y2="115" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="58" y="119" font-size="11" font-weight="bold" fill="#16a34a" text-anchor="end">1.6</text>
        <line x1="377" y1="115" x2="415" y2="148" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
    </svg>
    </div>
    """

def get_svg_prob3():
    """문제 3: (가) 30°, v0 vs (나) 60°, 2v0 비교 SVG (좌우 완벽 분할)"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 205" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 좌측 패널: (가) 30°, v0 -->
        <rect x="15" y="10" width="245" height="185" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
        <text x="25" y="32" font-size="13" font-weight="bold" fill="#1e40af">그림 (가) 30°, 속력 v₀</text>
        <rect x="25" y="155" width="225" height="8" fill="url(#groundHatch)"/>
        <line x1="20" y1="155" x2="255" y2="155" stroke="#1e293b" stroke-width="2"/>
        
        <!-- (가) 궤적: H1 낮음 -->
        <path d="M 45 155 Q 135 75 225 155" fill="none" stroke="#2563eb" stroke-width="2" stroke-dasharray="4,3"/>
        <circle cx="45" cy="155" r="7" fill="url(#sphereBlue)"/>
        <line x1="45" y1="155" x2="95" y2="126" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
        <text x="98" y="124" font-size="11" font-weight="bold" fill="#1e40af">v₀</text>
        <text x="32" y="159" font-size="11" font-style="italic" fill="#64748b">m</text>
        <path d="M 70 155 A 25 25 0 0 0 66.6 142.5" fill="none" stroke="#d97706" stroke-width="1.5"/>
        <text x="73" y="150" font-size="10" font-weight="bold" fill="#b45309">30°</text>
        <circle cx="135" cy="115" r="3.5" fill="#1d4ed8"/>
        <line x1="135" y1="115" x2="135" y2="155" stroke="#2563eb" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="135" y="105" font-size="11" font-weight="bold" fill="#1e40af" text-anchor="middle">H₁</text>

        <!-- 우측 패널: (나) 60°, 2v0 -->
        <rect x="280" y="10" width="245" height="185" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
        <text x="290" y="32" font-size="13" font-weight="bold" fill="#9f1239">그림 (나) 60°, 속력 2v₀</text>
        <rect x="290" y="155" width="225" height="8" fill="url(#groundHatch)"/>
        <line x1="285" y1="155" x2="520" y2="155" stroke="#1e293b" stroke-width="2"/>
        
        <!-- (나) 궤적: H2 높음 -->
        <path d="M 310 155 Q 400 -65 490 155" fill="none" stroke="#dc2626" stroke-width="2" stroke-dasharray="4,3"/>
        <circle cx="310" cy="155" r="7" fill="url(#sphereRose)"/>
        <line x1="310" y1="155" x2="345" y2="94" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red)"/>
        <text x="350" y="94" font-size="11" font-weight="bold" fill="#991b1b">2v₀</text>
        <text x="297" y="159" font-size="11" font-style="italic" fill="#64748b">m</text>
        <path d="M 330 155 A 20 20 0 0 0 320 137.7" fill="none" stroke="#d97706" stroke-width="1.5"/>
        <text x="333" y="148" font-size="10" font-weight="bold" fill="#b45309">60°</text>
        <circle cx="400" cy="45" r="4" fill="#dc2626"/>
        <line x1="400" y1="45" x2="400" y2="155" stroke="#ef4444" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="400" y="37" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">H₂ (12배)</text>
    </svg>
    </div>
    """

def get_svg_prob4():
    """문제 4: 60°, 속력 v, 최고점, 점 p (사용자 화면에서 잘렸던 문제 - 100% 안전 마진)"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 520 190" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 지면 및 해칭 -->
        <rect x="25" y="155" width="470" height="12" fill="url(#groundHatch)"/>
        <line x1="20" y1="155" x2="500" y2="155" stroke="#1e293b" stroke-width="2.5"/>
        <text x="495" y="172" font-size="11" fill="#64748b" text-anchor="end">수평면</text>
        
        <!-- 포물선 전체 궤적 (x: 65 ~ 425 안전 범위 안착) -->
        <path d="M 65 155 Q 245 -55 425 155" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4"/>
        
        <!-- 최고점 -->
        <circle cx="245" cy="50" r="4.5" fill="#0f172a"/>
        <text x="245" y="38" font-size="13" font-weight="bold" fill="#0f172a" text-anchor="middle">최고점</text>
        
        <!-- 던진 순간 공 (질량 m, 60도, 속력 v) -->
        <circle cx="65" cy="155" r="8" fill="url(#sphereBlue)"/>
        <text x="47" y="159" font-size="13" font-style="italic" font-weight="bold" fill="#334155">m</text>
        <line x1="65" y1="155" x2="115" y2="68" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arr-blue)"/>
        <text x="122" y="75" font-size="13" font-weight="bold" fill="#1e40af">v</text>
        <path d="M 90 155 A 25 25 0 0 0 77.5 133.3" fill="none" stroke="#d97706" stroke-width="2"/>
        <text x="96" y="148" font-size="12" font-weight="bold" fill="#b45309">60°</text>
        
        <!-- 통과점 p (하강 구간, 속도 화살표 완벽 포함) -->
        <circle cx="355" cy="105" r="8" fill="url(#sphereBlue)"/>
        <text x="368" y="102" font-size="16" font-weight="bold" fill="#1e3a8a">p</text>
        <line x1="355" y1="105" x2="390" y2="142" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
    </svg>
    </div>
    """

def get_svg_prob5():
    """문제 5: 60°, 10 m/s 다중 스트로브(점묘구) 및 1/2 H 보조선 SVG"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 215" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 지면 및 해칭 -->
        <rect x="25" y="160" width="490" height="12" fill="url(#groundHatch)"/>
        <line x1="20" y1="160" x2="520" y2="160" stroke="#1e293b" stroke-width="2.5"/>
        
        <!-- 포물선 점선 경로 -->
        <path d="M 60 160 Q 250 -60 440 160" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4,4"/>
        
        <!-- 7개 다중 스트로브 구 (핑크/로즈 3D 광택) -->
        <circle cx="60" cy="160" r="8" fill="url(#sphereRose)"/>
        <circle cx="102" cy="108" r="8" fill="url(#sphereRose)"/>
        <circle cx="165" cy="69" r="8" fill="url(#sphereRose)"/>
        <circle cx="250" cy="50" r="8.5" fill="url(#sphereRose)"/>
        <circle cx="335" cy="69" r="8" fill="url(#sphereRose)"/>
        <circle cx="398" cy="108" r="8" fill="url(#sphereRose)"/>
        <circle cx="440" cy="160" r="8" fill="url(#sphereRose)"/>
        
        <!-- 초기 속도 벡터 (10 m/s, 60도) -->
        <line x1="60" y1="160" x2="105" y2="82" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arr-blue)"/>
        <text x="110" y="85" font-size="12" font-weight="bold" fill="#1e40af">10 m/s</text>
        <path d="M 85 160 A 25 25 0 0 0 72.5 138.3" fill="none" stroke="#d97706" stroke-width="2"/>
        <text x="89" y="152" font-size="11" font-weight="bold" fill="#b45309">60°</text>
        
        <!-- 최고점 H 치수선 -->
        <line x1="250" y1="50" x2="250" y2="160" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="3,3"/>
        <line x1="262" y1="52" x2="262" y2="158" stroke="#e11d48" stroke-width="1.5" marker-start="url(#arr-red)" marker-end="url(#arr-red)"/>
        <text x="272" y="108" font-size="13" font-weight="bold" fill="#9f1239">H</text>
        
        <!-- 1/2 H 수평 기준선 (y = 105) -->
        <line x1="50" y1="105" x2="450" y2="105" stroke="#2563eb" stroke-width="1.2" stroke-dasharray="3,3"/>
        <text x="456" y="109" font-size="12" font-weight="bold" fill="#1d4ed8">1/2 H</text>
        
        <!-- 수평 도달 거리 R 치수선 -->
        <line x1="60" y1="185" x2="440" y2="185" stroke="#334155" stroke-width="1.5" marker-start="url(#arr-dark)" marker-end="url(#arr-dark)"/>
        <line x1="60" y1="178" x2="60" y2="192" stroke="#334155" stroke-width="1.5"/>
        <line x1="440" y1="178" x2="440" y2="192" stroke="#334155" stroke-width="1.5"/>
        <text x="250" y="202" font-size="13" font-weight="bold" fill="#1e293b" text-anchor="middle">R</text>
    </svg>
    </div>
    """

def get_svg_independence():
    """기초 1: 운동의 독립성 (자유낙하 vs 수평투사 동시 낙하 스트로브)"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 520 200" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 발사대 타워 -->
        <rect x="40" y="40" width="70" height="120" fill="#e2e8f0" stroke="#475569" stroke-width="1.5"/>
        <line x1="30" y1="160" x2="480" y2="160" stroke="#1e293b" stroke-width="2.5"/>
        <rect x="35" y="160" width="450" height="10" fill="url(#groundHatch)"/>
        
        <!-- 공 B 수평 발사 화살표 -->
        <line x1="110" y1="40" x2="160" y2="40" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arr-blue)"/>
        <text x="165" y="38" font-size="11" font-weight="bold" fill="#1e40af">v₀ (수평 발사)</text>
        
        <!-- 수평 동시 도달 보조 점선 및 스트로브 구 -->
        <!-- t=0 -->
        <line x1="110" y1="40" x2="110" y2="40" stroke="#94a3b8" stroke-dasharray="2,2"/>
        <circle cx="110" cy="40" r="6" fill="url(#sphereRose)"/>
        <circle cx="110" cy="40" r="6" fill="url(#sphereBlue)"/>
        
        <!-- t=1 -->
        <line x1="110" y1="65" x2="190" y2="65" stroke="#cbd5e1" stroke-dasharray="2,2"/>
        <circle cx="110" cy="65" r="6" fill="url(#sphereRose)"/>
        <circle cx="190" cy="65" r="6" fill="url(#sphereBlue)"/>
        
        <!-- t=2 -->
        <line x1="110" y1="105" x2="290" y2="105" stroke="#cbd5e1" stroke-dasharray="2,2"/>
        <circle cx="110" cy="105" r="6" fill="url(#sphereRose)"/>
        <circle cx="290" cy="105" r="6" fill="url(#sphereBlue)"/>
        
        <!-- t=3 (지면 도달) -->
        <line x1="110" y1="160" x2="420" y2="160" stroke="#cbd5e1" stroke-dasharray="2,2"/>
        <circle cx="110" cy="160" r="7" fill="url(#sphereRose)"/>
        <circle cx="420" cy="160" r="7" fill="url(#sphereBlue)"/>
        
        <!-- 궤적 선 -->
        <line x1="110" y1="40" x2="110" y2="160" stroke="#e11d48" stroke-width="1.5" stroke-dasharray="3,3"/>
        <path d="M 110 40 Q 265 40 420 160" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="3,3"/>
        
        <!-- 라벨 -->
        <text x="75" y="100" font-size="12" font-weight="bold" fill="#9f1239" text-anchor="middle">
            <tspan x="75" dy="0">공 A</tspan>
            <tspan x="75" dy="16">(자유낙하)</tspan>
        </text>
        <text x="360" y="85" font-size="12" font-weight="bold" fill="#1e40af">공 B (수평투사)</text>
        <text x="260" y="182" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">연직 방향으로는 동일한 중력만 작용하므로 매 순간 높이가 같고 동시에 도달!</text>
    </svg>
    </div>
    """

def get_svg_q3():
    """기초 2: 10 m/s, 30도 포물선 정밀 SVG"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 520 170" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <line x1="25" y1="130" x2="495" y2="130" stroke="#1e293b" stroke-width="2"/>
        <rect x="30" y="130" width="460" height="8" fill="url(#groundHatch)"/>
        <path d="M 60 130 Q 250 10 440 130" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4"/>
        <circle cx="60" cy="130" r="7.5" fill="url(#sphereBlue)"/>
        <line x1="60" y1="130" x2="130" y2="90" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arr-blue)"/>
        <text x="135" y="88" font-size="12" font-weight="bold" fill="#1e40af">v₀=10m/s (30°)</text>
        <path d="M 90 130 A 30 30 0 0 0 86 115" fill="none" stroke="#d97706" stroke-width="1.5"/>
        <text x="96" y="125" font-size="11" font-weight="bold" fill="#b45309">30°</text>
        <circle cx="250" cy="70" r="4" fill="#dc2626"/>
        <line x1="250" y1="70" x2="250" y2="130" stroke="#ef4444" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="250" y="60" font-size="11" font-weight="bold" fill="#991b1b" text-anchor="middle">최고점</text>
    </svg>
    </div>
    """

def get_svg_q4():
    """기초 3: 4초 후 수평 39.2m 도달 정밀 SVG"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 520 170" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <line x1="25" y1="130" x2="495" y2="130" stroke="#1e293b" stroke-width="2"/>
        <rect x="30" y="130" width="460" height="8" fill="url(#groundHatch)"/>
        <path d="M 60 130 Q 250 20 440 130" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,4"/>
        <circle cx="60" cy="130" r="7.5" fill="url(#sphereBlue)"/>
        <line x1="60" y1="130" x2="135" y2="130" stroke="#1d4ed8" stroke-width="3" marker-end="url(#arr-blue)"/>
        <text x="142" y="125" font-size="12" font-weight="bold" fill="#1e40af">v_x = ? m/s</text>
        <line x1="60" y1="130" x2="110" y2="75" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#arr-dark)"/>
        <circle cx="440" cy="130" r="6" fill="#10b981"/>
        <text x="440" y="115" font-size="11" font-weight="bold" fill="#047857" text-anchor="middle">도달 (t = 4초)</text>
        <line x1="60" y1="150" x2="440" y2="150" stroke="#334155" stroke-width="1.5" marker-start="url(#arr-dark)" marker-end="url(#arr-dark)"/>
        <text x="250" y="165" font-size="12" font-weight="bold" fill="#1e293b" text-anchor="middle">39.2 m</text>
    </svg>
    </div>
    """

def get_svg_q5():
    """기초 4: 0~1초 연직 변위 25m 최고점 도달 시간 추론 SVG"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 520 180" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <line x1="25" y1="145" x2="495" y2="145" stroke="#1e293b" stroke-width="2"/>
        <rect x="30" y="145" width="460" height="8" fill="url(#groundHatch)"/>
        <path d="M 60 145 Q 260 -60 460 145" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
        <!-- 0~1초 강조 구간 -->
        <path d="M 60 145 Q 120 70 170 55" fill="none" stroke="#ea580c" stroke-width="3"/>
        <circle cx="60" cy="145" r="7" fill="url(#sphereBlue)"/>
        <circle cx="170" cy="55" r="7" fill="url(#sphereRose)"/>
        <line x1="170" y1="55" x2="170" y2="145" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="2,2"/>
        <text x="175" y="50" font-size="12" font-weight="bold" fill="#c2410c">1초 시점 (연직 변위 25 m)</text>
        <!-- 최고점 -->
        <circle cx="260" cy="42" r="4" fill="#0f172a"/>
        <text x="260" y="32" font-size="11" font-weight="bold" fill="#0f172a" text-anchor="middle">최고점 ?초</text>
    </svg>
    </div>
    """

def get_energy_barchart_prob2(show_answer=True):
    """문제 2: 지점 B와 C의 에너지 막대그래프 (Plotly - 인터랙티브용)"""
    fig = go.Figure()
    categories = ['B (최고점, 3.2m)', 'C (하강 중, 1.6m)']
    
    if show_answer:
        fig.add_trace(go.Bar(
            name='운동에너지 (Ek)',
            x=categories,
            y=[18.0, 34.0],
            marker_color='#3b82f6',
            text=['18.0 J', '34.0 J'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='퍼텐셜에너지 (Ep)',
            x=categories,
            y=[32.0, 16.0],
            marker_color='#ef4444',
            text=['32.0 J', '16.0 J'],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            name='역학적에너지 (E_total)',
            x=categories,
            y=[50.0, 50.0],
            marker_color='#10b981',
            text=['50.0 J', '50.0 J'],
            textposition='auto'
        ))
    else:
        fig.add_trace(go.Bar(name='운동에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))
        fig.add_trace(go.Bar(name='퍼텐셜에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))
        fig.add_trace(go.Bar(name='역학적에너지', x=categories, y=[0, 0], marker_color='#cbd5e1'))

    fig.update_layout(
        barmode='group',
        yaxis=dict(title='에너지 (J)', range=[0, 55], dtick=10),
        height=250,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor='#f8fafc',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    return fig

# =========================================================================
# 섹션 1: 실전 기출 및 활동지 연계 문항 (5종)
# =========================================================================

if view_category in ["🎯 실전 기출 & 활동지 연계 5문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"]:
    st.header("🎯 실전 기출 & 활동지 연계 심화 문제")
    st.caption("수능/내신 빈출 유형 및 [활동 6] 포물선 운동의 역학적 에너지 보존 탐구 문항입니다.")

    # ---------------------------------------------------------------------
    # [문제 1] 30도 방향 40m/s 포물선 운동 (질량 2kg)
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [문제 1] 비스듬히 던진 물체의 기본 포물선 운동 계산")
    st.markdown("""
    <span class="badge-primary">기출 빈출</span> &nbsp;
    지면에서 질량이 **2 kg**인 물체를 수평면과 **30°**를 이루는 방향으로 **40 m/s**의 속력으로 던진 물체의 운동 경로를 나타낸 것이다. 
    *(단, 중력 가속도는 $10\\text{ m/s}^2$이고, 공기 저항은 무시한다.)*
    """, unsafe_allow_html=True)
    
    render_html(get_svg_prob1())

    if is_print_mode:
        st.markdown("**1) 최고점에 도달할 때까지 걸린 시간(s)을 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2) 최고점의 높이(m)를 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3) 수평 도달 거리(m)를 구하고, 풀이 과정과 답을 쓰시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            ans1_1 = st.text_input("1) 최고점 도달 시간 (s)", key="p1_1", placeholder="예: 2")
        with c2:
            ans1_2 = st.text_input("2) 최고점 높이 (m)", key="p1_2", placeholder="예: 20")
        with c3:
            ans1_3 = st.text_input("3) 수평 도달 거리 (m)", key="p1_3", placeholder="예: 80루트3 또는 138.6")

        if st.button("결과 및 단계별 풀이 확인", key="btn_p1"):
            st.success("""
            **[정답 및 모범 풀이]**
            - **초기 속도 성분 분해**:
              - 수평 초기 속도: $v_{x0} = 40 \\cos 30^\\circ = 40 \\times \\frac{\\sqrt{3}}{2} = 20\\sqrt{3}\\text{ m/s} \\approx 34.64\\text{ m/s}$
              - 연직 초기 속도: $v_{y0} = 40 \\sin 30^\\circ = 40 \\times \\frac{1}{2} = 20\\text{ m/s}$
            
            1. **최고점 도달 시간**:
               - 최고점에서 연직 속도 $v_y = 0$ 이므로, $v_y = v_{y0} - gt = 20 - 10t = 0 \\implies \\mathbf{t = 2\\text{초}}$
            
            2. **최고점의 높이**:
               - $H = v_{y0}t - \\frac{1}{2}gt^2 = 20(2) - \\frac{1}{2}(10)(2^2) = 40 - 20 = \\mathbf{20\\text{ m}}$
               - *(에너지 보존: $\\frac{1}{2}m v_{y0}^2 = mgH \\implies H = \\frac{20^2}{20} = 20\\text{ m}$)*
            
            3. **수평 도달 거리**:
               - 전체 체공 시간 $T = 2t = 4\\text{초}$
               - 수평 방향은 등속도 운동이므로, $R = v_{x0} \\times T = 20\\sqrt{3} \\times 4 = \\mathbf{80\\sqrt{3}\\text{ m}} \\approx \\mathbf{138.6\\text{ m}}$
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 2] 활동 6 연계: 포물선 운동 에너지 분석 및 막대그래프
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("⚡ [문제 2 / 활동6 연계] 포물선 운동의 역학적 에너지 보존 & 막대그래프")
    st.markdown("""
    <span class="badge-success">활동지 연계</span> &nbsp;
    질량이 **1 kg**인 공이 운동하는 도중 세 지점 **A, B, C**에서의 높이 및 수평/연직 방향 속력을 나타낸 것이다. 
    *(단, 공기 저항은 무시하고 중력 가속도의 크기는 $10\\text{ m/s}^2$, 지면의 중력 퍼텐셜에너지는 0으로 한다.)*
    """, unsafe_allow_html=True)

    col_p2_diag, col_p2_table = st.columns([1.3, 1])
    with col_p2_diag:
        render_html(get_svg_prob2())
    with col_p2_table:
        st.markdown("""
        | 지점 | 높이(m) | 수평 속력(m/s) | 연직 속력(m/s) |
        | :---: | :---: | :---: | :---: |
        | **A** | **0** | **6** | **8** |
        | **B (최고점)** | **3.2** | **6** | **0** |
        | **C (하강 중)** | **1.6** | **6** | **-** |
        """)
        st.caption("💡 힌트: 수평 방향으로는 알짜힘이 없으므로 수평 속력은 항상 6 m/s로 일정하게 보존됩니다.")

    st.markdown("---")

    if is_print_mode:
        st.markdown("**1) A와 B에서 공의 운동에너지, 중력에 의한 퍼텐셜에너지, 역학적 에너지를 각각 구하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

        st.markdown("**2) (1)의 계산 결과를 바탕으로 아래 B(최고점, 3.2m), C(하강 중, 1.6m)의 에너지 막대그래프를 완성하시오.**")
        render_html("""
        <div class="bar-chart-container">
            <div class="bar-chart-card">
                <div class="bar-chart-title">B (최고점, 3.2 m)</div>
                <div class="bar-chart-frame">
                    <span class="tick-50">50J</span>
                    <span class="tick-0">0J</span>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                </div>
                <div class="bar-chart-labels">
                    <span>운동E</span>
                    <span>위치E</span>
                    <span>역학적E</span>
                </div>
            </div>
            <div class="bar-chart-card">
                <div class="bar-chart-title">C (하강 중, 1.6 m)</div>
                <div class="bar-chart-frame">
                    <span class="tick-50">50J</span>
                    <span class="tick-0">0J</span>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                    <div class="bar-chart-bar-outline">?</div>
                </div>
                <div class="bar-chart-labels">
                    <span>운동E</span>
                    <span>위치E</span>
                    <span>역학적E</span>
                </div>
            </div>
        </div>
        """)

        st.markdown("**3) 계산 결과를 근거로 하여, A에서 B까지 운동하는 동안 운동에너지와 퍼텐셜에너지가 어떻게 변하는지 서술하고, 역학적 에너지가 일정하게 유지되는 이유를 에너지 전환 관점에서 설명하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

        st.markdown("**4) C에서의 역학적 에너지를 계산 없이 예측하고, 그 근거를 서술하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

    else:
        st.markdown("**1) A와 B에서의 에너지 구하기**")
        c2_1, c2_2 = st.columns(2)
        with c2_1:
            st.text_input("A 지점: 운동E / 위치E / 역학적E (J)", key="p2_ans_A", placeholder="예: 50, 0, 50")
        with c2_2:
            st.text_input("B 지점: 운동E / 위치E / 역학적E (J)", key="p2_ans_B", placeholder="예: 18, 32, 50")

        st.markdown("**2) B와 C 지점의 에너지 막대그래프 완성하기**")
        show_bar_ans = st.checkbox("📊 정답 막대그래프 노출하기", value=False)
        st.plotly_chart(get_energy_barchart_prob2(show_answer=show_bar_ans), use_container_width=True)

        st.markdown("**3) 서술형 질문: 에너지 전환과 역학적 에너지 보존**")
        st.text_area("A에서 B까지 운동하는 동안의 에너지 변화와 역학적 에너지가 보존되는 이유", key="p2_desc1", height=70, placeholder="운동에너지 감소량과 퍼텐셜에너지 증가량의 관계를 에너지 전환 관점에서 서술하세요.")
        
        st.markdown("**4) 서술형 질문: C에서의 역학적 에너지 예측**")
        st.text_input("C에서의 역학적 에너지 및 그 이유", key="p2_desc2", placeholder="예: 50 J, 외력이 없고 보존력(중력)만 작용하므로 역학적 에너지가 보존됨")

        if st.button("결과 및 모범 해설 확인", key="btn_p2"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            1. **A와 B에서의 에너지**:
               - **A 지점 ($h=0\\text{ m}$)**:
                 - 전체 속력 $v_A = \\sqrt{6^2 + 8^2} = 10\\text{ m/s}$
                 - 운동에너지 $E_k = \\frac{1}{2}(1)(10^2) = \\mathbf{50\\text{ J}}$ (수평 18 J + 연직 32 J)
                 - 퍼텐셜에너지 $E_p = mgh = 1 \\times 10 \\times 0 = \\mathbf{0\\text{ J}}$
                 - 역학적 에너지 $E_{total} = E_k + E_p = \\mathbf{50\\text{ J}}$
               - **B 지점 ($h=3.2\\text{ m}$, 최고점)**:
                 - 전체 속력 $v_B = v_x = 6\\text{ m/s}$ ($v_y = 0$)
                 - 운동에너지 $E_k = \\frac{1}{2}(1)(6^2) = \\mathbf{18\\text{ J}}$
                 - 퍼텐셜에너지 $E_p = mgh = 1 \\times 10 \\times 3.2 = \\mathbf{32\\text{ J}}$
                 - 역학적 에너지 $E_{total} = 18 + 32 = \\mathbf{50\\text{ J}}$
            
            2. **에너지 막대그래프 (B, C)**:
               - **B 지점**: 운동E = **18 J**, 위치E = **32 J**, 역학적E = **50 J**
               - **C 지점 ($h=1.6\\text{ m}$)**:
                 - 위치에너지: $E_p = 1 \\times 10 \\times 1.6 = \\mathbf{16\\text{ J}}$
                 - 역학적 에너지가 50 J로 보존되므로, 운동에너지 $E_k = 50 - 16 = \\mathbf{34\\text{ J}}$
                 - 막대그래프: 운동E = **34 J**, 위치E = **16 J**, 역학적E = **50 J**
            
            3. **에너지 전환 서술 모범 답안**:
               - A에서 B로 상승하는 동안 높이가 증가하여 퍼텐셜에너지는 0 J에서 32 J로 **32 J 증가**하고, 연직 속력이 8 m/s에서 0으로 줄어들어 운동에너지는 50 J에서 18 J로 **32 J 감소**한다.
               - 공기 저항이 없을 때 **운동에너지 감소량(32 J)이 그대로 퍼텐셜에너지 증가량(32 J)으로 1:1 전환**되므로, 두 에너지의 합인 역학적 에너지는 **50 J로 일정하게 유지**된다.
            
            4. **C 지점 역학적 에너지 예측**:
               - **답: 50 J**
               - **근거**: 공기 저항과 같은 비보존력이 작용하지 않고 중력(보존력)만 작용하므로, 물체의 운동 경로 상 모든 지점에서 역학적 에너지는 항상 50 J로 일정하게 보존되기 때문이다.
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 3] 두 물체의 포물선 운동 비교 ((가) 30°, v0 vs (나) 60°, 2v0)
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📊 [문제 3] 두 물체의 포물선 운동 비교 ((가) 30°, v₀ vs (나) 60°, 2v₀)")
    st.markdown("""
    <span class="badge-purple">수능 빈출</span> &nbsp;
    그림 (가), (나)는 각각 수평면과 **30°, 60°**의 각을 이루는 방향으로 속력 **$v_0, 2v_0$**으로 던져진 **동일한 물체**가 포물선 운동하는 모습을 나타낸 것이다.
    """, unsafe_allow_html=True)

    render_html(get_svg_prob3())

    if is_print_mode:
        st.markdown("**1) 물체를 던진 순간부터 최고점 도달할 때까지 걸린 시간을 비교하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2) 최고점에서 중력에 의한 위치 에너지를 비교하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3) (나)에서 최고점에서 물체의 중력에 의한 위치 에너지는 운동에너지의 몇 배인지 구하시오.**")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c3_1, c3_2, c3_3 = st.columns(3)
        with c3_1:
            ans3_1 = st.text_input("1) 최고점 도달 시간 비 t(가) : t(나)", key="p3_1", placeholder="예: 1:2루트3 또는 (나)가 2루트3배")
        with c3_2:
            ans3_2 = st.text_input("2) 최고점 위치에너지 비 Ep(가) : Ep(나)", key="p3_2", placeholder="예: 1:12 또는 (나)가 12배")
        with c3_3:
            ans3_3 = st.text_input("3) (나) 최고점 Ep는 Ek의 몇 배?", key="p3_3", placeholder="예: 3배")

        if st.button("결과 및 상세 풀이 확인", key="btn_p3"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            1. **최고점 도달 시간 비교**:
               - 최고점 도달 시간은 연직 초기 속도 성분에 비례합니다 ($t_H = \\frac{v_y}{g}$):
                 - (가): $v_{y1} = v_0 \\sin 30^\\circ = \\frac{1}{2}v_0 \\implies t_1 = \\frac{v_0}{2g}$
                 - (나): $v_{y2} = 2v_0 \\sin 60^\\circ = 2v_0 \\times \\frac{\\sqrt{3}}{2} = \\sqrt{3}v_0 \\implies t_2 = \\frac{\\sqrt{3}v_0}{g}$
               - **비율: $t_{(가)} : t_{(나)} = \\frac{1}{2} : \\sqrt{3} = \\mathbf{1 : 2\\sqrt{3}}$ ((나)가 $2\\sqrt{3} \\approx 3.46$배)**
            
            2. **최고점에서의 위치 에너지 비교**:
               - 최고점 높이 $H = \\frac{v_y^2}{2g}$이므로, $E_p = mgH = \\frac{1}{2}mv_y^2$
                 - (가): $E_{p1} = \\frac{1}{2}m (\\frac{1}{2}v_0)^2 = \\frac{1}{8}mv_0^2$
                 - (나): $E_{p2} = \\frac{1}{2}m (\\sqrt{3}v_0)^2 = \\frac{3}{2}mv_0^2 = \\frac{12}{8}mv_0^2$
               - **비율: $E_{p(가)} : E_{p(나)} = \\frac{1}{8} : \\frac{3}{2} = \\mathbf{1 : 12}$ ((나)가 12배)**
            
            3. **(나)에서 최고점 위치에너지는 운동에너지의 몇 배인가?**:
               - (나) 최고점에서의 속력은 수평 방향 속도만 남으므로:
                 $v_x = 2v_0 \\cos 60^\\circ = 2v_0 \\times \\frac{1}{2} = v_0$
               - 최고점 운동에너지: $E_k = \\frac{1}{2}m v_x^2 = \\frac{1}{2}mv_0^2$
               - 최고점 위치에너지: $E_p = \\frac{3}{2}mv_0^2$
               - **배수: $\\frac{E_p}{E_k} = \\frac{\\frac{3}{2}mv_0^2}{\\frac{1}{2}mv_0^2} = \\mathbf{3\\text{배}}$**
               *(참고 공식: $\\frac{E_p}{E_k} = \\tan^2 \\theta = \\tan^2 60^\\circ = (\\sqrt{3})^2 = 3$배)*
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 4] 에너지 관계를 이용한 점 p에서의 운동에너지 추론 (잘림 없는 완벽 SVG)
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🔍 [문제 4] 최고점을 지난 임의의 점 p에서의 운동에너지 추론")
    st.markdown("""
    <span class="badge-amber">역학적 에너지 관계 추론</span> &nbsp;
    그림은 수평면과 **60°**의 각을 이루며 속력 **$v$**로 던져진 질량 **$m$**인 물체가 포물선 운동 하여 최고점을 지나 **점 p**를 통과한 모습을 나타낸 것이다. 
    **수평면에서 던져진 순간 물체의 운동 에너지는 물체가 최고점에서 p까지 운동하는 동안 물체의 중력에 의한 위치 에너지 감소량의 2배이다.**
    
    **점 p에서 물체의 운동 에너지는?** *(단, 물체의 크기 및 공기 저항은 무시한다.)*
    """, unsafe_allow_html=True)

    render_html(get_svg_prob4())

    if is_print_mode:
        st.markdown("**풀이 과정과 답을 쓰시오.**")
        for _ in range(3): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans4 = st.text_input("점 p에서의 운동에너지 입력 (던진 순간 운동에너지 E₀ 또는 mv²으로 표현)", key="p4_ans", placeholder="예: 3/4 E0 또는 3/8 mv^2")
        if st.button("정답 및 풀이 과정 확인", key="btn_p4"):
            st.success("""
            **[정답 및 모범 풀이]**
            
            - **정답**: $\\mathbf{\\frac{3}{4} E_{k0}}$ (또는 $\\mathbf{\\frac{3}{8} mv^2}$)
            
            - **단계별 풀이 과정**:
              1. **던진 순간(지면)의 초기 운동에너지**:
                 $E_{k0} = \\frac{1}{2}mv^2$
              
              2. **최고점에서의 운동에너지**:
                 - 최고점에서는 연직 속도 $v_y = 0$이고 수평 속도 $v_x = v \\cos 60^\\circ = \\frac{1}{2}v$ 만 존재합니다.
                 - $E_{k,top} = \\frac{1}{2}m v_x^2 = \\frac{1}{2}m \\left(\\frac{1}{2}v\\right)^2 = \\frac{1}{8}mv^2 = \\mathbf{\\frac{1}{4} E_{k0}}$
              
              3. **문제 조건 해석**:
                 - "던져진 순간 운동에너지($E_{k0}$)는 최고점에서 p까지의 위치에너지 감소량($\\Delta E_p$)의 2배이다."
                 - $E_{k0} = 2 \\times \\Delta E_p \\implies \\mathbf{\\Delta E_p = \\frac{1}{2} E_{k0}}$
              
              4. **역학적 에너지 보존에 의한 점 p의 운동에너지 계산**:
                 - 최고점에서 p까지 낙하하면서 감소한 위치에너지는 고스란히 운동에너지 증가량($\\Delta E_k$)이 됩니다:
                   $\\Delta E_k = \\Delta E_p = \\frac{1}{2} E_{k0}$
                 - 따라서 점 p에서의 운동에너지 $E_k(p)$는 최고점 운동에너지에 증가량을 더한 값입니다:
                   $$E_k(p) = E_{k,top} + \\Delta E_k = \\frac{1}{4} E_{k0} + \\frac{1}{2} E_{k0} = \\mathbf{\\frac{3}{4} E_{k0}} = \\mathbf{\\frac{3}{8} mv^2}$$
            """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------------------------------------------------
    # [문제 5] 60도, 10m/s 포물선 운동의 7단계 종합 분석
    # ---------------------------------------------------------------------
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🌟 [문제 5] 60°, 10 m/s 포물선 운동과 1/2 H 지점의 7단계 종합 탐구")
    st.markdown("""
    <span class="badge-primary">종합 탐구</span> &nbsp;
    그림은 수평면과 **60°**의 각으로 속력 **10 m/s**로 던져진 물체가 운동하는 모습을 나타낸 것이다. 
    *(단, 중력 가속도는 $10\\text{ m/s}^2$이고, 물체의 질량은 $m$이라 하자. 수치 계산 시 $m=1\\text{ kg}$ 기준으로 계산할 수 있다. 물체의 크기 및 공기 저항은 무시한다.)*
    """, unsafe_allow_html=True)

    render_html(get_svg_prob5())

    if is_print_mode:
        q_list_p5 = [
            "(1) 속력 10 m/s로 비스듬히 던져진 물체가 최고점에 도달할 때까지 걸린 시간은?",
            "(2) 최고점의 높이는?",
            "(3) 수평도달 거리는?",
            "(4) 물체를 던진 순간의 역학적 에너지는?",
            "(5) 최고점에서 운동에너지는?",
            "(6) 1/2 H 지점에서의 운동에너지와 위치에너지를 각각 구하시오.",
            "(7) 1/2 H 지점에서의 속도의 크기를 구하시오."
        ]
        for q in q_list_p5:
            st.markdown(f"**{q}**")
            st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        col_5a, col_5b = st.columns(2)
        with col_5a:
            ans5_1 = st.text_input("(1) 최고점 도달 시간 (s)", key="p5_1", placeholder="예: 루트3/2 또는 0.87")
            ans5_2 = st.text_input("(2) 최고점 높이 (m)", key="p5_2", placeholder="예: 3.75")
            ans5_3 = st.text_input("(3) 수평도달 거리 (m)", key="p5_3", placeholder="예: 5루트3 또는 8.66")
            ans5_4 = st.text_input("(4) 던진 순간 역학적에너지 (J, m=1kg)", key="p5_4", placeholder="예: 50")
        with col_5b:
            ans5_5 = st.text_input("(5) 최고점에서 운동에너지 (J, m=1kg)", key="p5_5", placeholder="예: 12.5")
            ans5_6 = st.text_input("(6) 1/2 H 지점의 운동E / 위치E (J, m=1kg)", key="p5_6", placeholder="예: 31.25 / 18.75")
            ans5_7 = st.text_input("(7) 1/2 H 지점에서의 속력 (m/s)", key="p5_7", placeholder="예: 루트62.5 또는 7.91")

        if st.button("전체 7문항 모범 해설 확인", key="btn_p5"):
            st.success("""
            **[7단계 상세 정답 및 해설]**
            - **초기 속도 성분**:
              - $v_{x} = 10 \\cos 60^\\circ = 5\\text{ m/s}$
              - $v_{y0} = 10 \\sin 60^\\circ = 5\\sqrt{3}\\text{ m/s} \\approx 8.66\\text{ m/s}$
            
            1. **최고점 도달 시간**:
               - $t_H = \\frac{v_{y0}}{g} = \\frac{5\\sqrt{3}}{10} = \\mathbf{\\frac{\\sqrt{3}}{2}\\text{초}} \\approx \\mathbf{0.87\\text{초}}$
            
            2. **최고점의 높이 ($H$)**:
               - $H = \\frac{v_{y0}^2}{2g} = \\frac{(5\\sqrt{3})^2}{20} = \\frac{75}{20} = \\mathbf{3.75\\text{ m}}$ (또는 $\\frac{15}{4}\\text{ m}$)
            
            3. **수평도달 거리 ($R$)**:
               - $R = v_x \\times (2t_H) = 5 \\times \\sqrt{3} = \\mathbf{5\\sqrt{3}\\text{ m}} \\approx \\mathbf{8.66\\text{ m}}$
            
            4. **던진 순간의 역학적 에너지**:
               - 지면에서 $E_p = 0$이므로, $E_{total} = \\frac{1}{2}mv_0^2 = \\frac{1}{2}m(10^2) = \\mathbf{50m\\text{ J}}$ ($m=1\\text{kg}$일 때 **50 J**)
            
            5. **최고점에서 운동에너지**:
               - 최고점에서는 수평 속도($v_x = 5\\text{ m/s}$)만 존재하므로:
                 $E_k(top) = \\frac{1}{2}mv_x^2 = \\frac{1}{2}m(5^2) = \\mathbf{12.5m\\text{ J}}$ ($m=1\\text{kg}$일 때 **12.5 J**)
            
            6. **1/2 H 지점에서의 운동에너지와 위치에너지**:
               - 높이 $h = \\frac{1}{2}H = \\frac{3.75}{2} = 1.875\\text{ m}$
               - 위치에너지: $E_p = mgh = mg(\\frac{1}{2}H) = \\frac{1}{2}E_p(top) = \\mathbf{18.75m\\text{ J}}$ ($m=1\\text{kg}$일 때 **18.75 J**)
               - 운동에너지: 역학적 에너지 보존에 의해
                 $E_k = E_{total} - E_p = 50m - 18.75m = \\mathbf{31.25m\\text{ J}}$ ($m=1\\text{kg}$일 때 **31.25 J**)
            
            7. **1/2 H 지점에서의 속도의 크기**:
               - $E_k = \\frac{1}{2}mv^2 = 31.25m \\implies v^2 = 62.5$
               - $\\mathbf{v = \\sqrt{62.5}\\text{ m/s} = \\frac{5\\sqrt{10}}{2}\\text{ m/s}} \\approx \\mathbf{7.91\\text{ m/s}}$
               - *(성분 검산: $v_x = 5$, $v_y^2 = v_{y0}^2 - 2g(H/2) = 75 - 37.5 = 37.5 \\implies v = \\sqrt{25 + 37.5} = \\sqrt{62.5}\\text{ m/s}$)*
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================================
# 섹션 2: 기초 개념 확인 문제 (4종)
# =========================================================================

if view_category in ["🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"]:
    st.header("🌱 포물선 운동 기초 개념 확인 문제")
    st.caption("운동의 독립성, 수평/연직 속도 성분 분해 및 등가속도 운동 공식의 기본 적용 문항입니다.")

    # --- [서술형 1] 운동의 독립성 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🖋️ [기초 1] 운동의 독립성 이해 (자유낙하 vs 수평투사)")
    render_html(get_svg_independence())
    st.markdown("동일한 높이에서 공 A(자유낙하)와 공 B(수평투사)를 동시에 발사했습니다. **왜 동시에 지면에 도달하는지 설명하시오.**")

    if is_print_mode:
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("🔍 모범 답안 보기"):
            st.info("수평과 연직 방향의 운동은 서로 **독립적**이며, 연직 방향으로는 공의 종류나 수평 속력과 무관하게 오직 동일한 **중력**만 작용하여 연직 가속도가 $g$로 같기 때문입니다.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 2] 10m/s, 30도 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [기초 2] 비스듬히 던진 물체의 정밀 분석 (10m/s, 30°)")
    render_html(get_svg_q3())
    st.markdown("처음 속도 **10m/s**, 각도 **30도**로 던졌습니다. ($g=10m/s^2$) 아래 질문에 답하세요.")

    if is_print_mode:
        st.markdown("1) 최고점 도달 시간(s)은? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
        st.markdown("2) 최고점의 높이(m)는? ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        c_k1, c_k2 = st.columns(2)
        with c_k1:
            ans3_t = st.text_input("1) 최고점 도달 시간(s)", key="q3_1", placeholder="예: 0.5")
        with c_k2:
            ans3_h = st.text_input("2) 최고점의 높이(m)", key="q3_2", placeholder="예: 1.25")
        if st.button("정답 확인", key="b3"):
            st.success(f"**[정답 및 풀이]**\n- 시간: $v_{{y0}}/g = (10 \\sin 30^\\circ)/10 = 0.5$초\n- 높이: $v_{{y0}}^2/2g = 5^2/20 = 1.25$m")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 3] 수평 속도의 역추적 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("📝 [기초 3] 수평 속도의 역추적")
    render_html(get_svg_q4())
    st.markdown("""
    물체를 비스듬히 던져 올렸더니 **4초 후** 수평으로 **39.2m** 떨어진 곳에 도달했습니다. 
    처음 발사 속도의 **수평 방향 성분**은 몇 m/s인가요? ($g=9.8m/s^2$)
    """)

    if is_print_mode:
        st.markdown("정답 및 풀이 과정:")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans4 = st.text_input("수평 속도(m/s) 입력", key="q4", placeholder="예: 9.8")
        if st.button("정답 확인", key="b4"):
            st.success("**[정답] 9.8 m/s** (수평 방향은 등속도 운동이므로 $v_x = x/t = 39.2/4 = 9.8$ m/s)")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- [기초 4] 최고점 시간 추론 ---
    st.markdown('<div class="exam-box">', unsafe_allow_html=True)
    st.subheader("🔥 [기초 4] 연직 변위를 통한 최고점 도달 시간 추론")
    render_html(get_svg_q5())
    st.markdown("""
    비스듬히 던진 야구공이 **0초부터 1초까지** 연직 방향으로 이동한 거리(변위)가 **25m**입니다. 
    이 공이 **최고점에 도달할 때까지** 걸리는 시간은 약 몇 초인가요? ($g=9.8m/s^2$)
    """)

    if is_print_mode:
        st.markdown("정답 및 풀이 과정:")
        for _ in range(2): st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        ans5 = st.text_input("최고점 시간(초) 입력", key="q5", placeholder="예: 3.05")
        if st.button("정답 확인", key="b5"):
            st.success("""
            **[정답 및 풀이] 약 3.05초**
            1. $y = v_{y0}t - 1/2gt^2$ 공식에 대입: $25 = v_{y0}(1) - 4.9(1)^2$
            2. 연직 초기 속도 $v_{y0} = 29.9$ m/s 도출
            3. 최고점 시간 $t_H = v_{y0}/g = 29.9 / 9.8 \\approx 3.05$초
            """)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.info("💡 모든 도표는 교과서급 정밀 벡터 SVG로 제작되어 화면 및 인쇄(A4) 시 잘림 없이 선명하게 출력됩니다.")
