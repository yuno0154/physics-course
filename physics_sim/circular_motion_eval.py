import streamlit as st
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
        p, li { font-size: 0.85rem !important; line-height: 1.35 !important; }
        .answer-space { 
            border-bottom: 1px solid #64748b !important; 
            height: 28px !important; 
            margin-bottom: 6px !important; 
            width: 100% !important; 
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
    .meta-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.82rem;
        margin-bottom: 14px;
    }
    .meta-table th, .meta-table td {
        border: 1px solid #cbd5e1;
        padding: 5px 10px;
    }
    .meta-table th {
        background: #f1f5f9;
        font-weight: bold;
        width: 15%;
        text-align: center;
    }
    .answer-space { 
        border-bottom: 1px solid #94a3b8; 
        height: 30px; 
        margin-bottom: 8px; 
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
        max-width: 500px;
        margin: 10px auto;
        overflow: visible;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 원운동 형성평가 문제 풀이")

# --- 출력 모드 선택 ---
col_mode1, col_mode2 = st.columns([1.8, 1])
with col_mode1:
    is_print_mode = st.toggle("🖨️ 학습지 출력 모드 전환 (인쇄 및 PDF 저장용)", value=False)
with col_mode2:
    if is_print_mode:
        if st.button("🖨️ 브라우저 바로 인쇄 / PDF 저장", use_container_width=True):
            st.components.v1.html("<script>parent.window.print()</script>", height=0)

if is_print_mode:
    st.markdown('<div class="print-header">📝 원운동 형성평가 학습지 &nbsp; [ 학년: 2 &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="meta-table">
        <tr>
            <th>단원정보</th><td>Ⅰ. 시공간과 운동 &nbsp; 01 힘의 합성과 예측</td>
            <th>성취기준</th><td>[12역학01-03] 물체에 작용하는 힘의 방향에 따라 물체의 운동 방향이 변할 수 있음을 원운동 등 다양한 예를 들어 설명할 수 있다.</td>
        </tr>
        <tr>
            <th>학습목표</th><td colspan="3">• 물체에 작용하는 힘의 방향에 따라 운동 방향이 변할 수 있음을 원운동 등 다양한 예를 들어 설명할 수 있다.</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["📄 1페이지: 원운동 기본 및 단진자 (4문항)", "📄 2페이지: 그래프 및 다체 원운동 (3문항)", "📖 전체 7문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    **2022 개정 교육과정 역학과 에너지** [12역학01-03] 성취기준에 따른 **원운동 형성평가 문항**입니다.
    화면에서 인터랙티브하게 문제를 확인하고 상세 해설 및 단계별 풀이 과정을 확인할 수 있으며, 인쇄 모드를 통해 실제 시험지/학습지 형태로 출력할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["📄 1페이지: 원운동 기본 및 단진자 (4문항)", "📄 2페이지: 그래프 및 다체 원운동 (3문항)", "📖 전체 7문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 정밀 SVG 벡터 일러스트 생성 함수군
# =========================================================================

def render_html(html_str):
    clean_html = "".join(line.strip() for line in html_str.splitlines())
    if hasattr(st, "html"):
        st.html(clean_html)
    else:
        st.markdown(clean_html, unsafe_allow_html=True)

COMMON_SVG_DEFS = """
    <defs>
        <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2563eb"/>
        </marker>
        <marker id="arr-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#dc2626"/>
        </marker>
        <marker id="arr-dark" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#334155"/>
        </marker>
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
    </defs>
"""

def get_svg_prob1():
    """문제 1: 등속 원운동 질량 2kg, r=4m, v=π m/s"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 320 230" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 원 궤도 점선 -->
        <circle cx="160" cy="115" r="75" fill="none" stroke="#94a3b8" stroke-width="1.8" stroke-dasharray="4,4"/>
        
        <!-- 원 중심 O -->
        <circle cx="160" cy="115" r="3.5" fill="#1e293b"/>
        <text x="145" y="119" font-size="13" font-weight="bold" fill="#1e293b">O</text>
        
        <!-- 반지름 4m 표시선 -->
        <line x1="160" y1="115" x2="235" y2="115" stroke="#334155" stroke-width="1.5"/>
        <text x="195" y="108" font-size="12" font-weight="bold" fill="#334155" text-anchor="middle">4 m</text>
        
        <!-- 물체 (2kg) -->
        <circle cx="235" cy="115" r="9" fill="url(#sphereBlue)"/>
        <text x="250" y="120" font-size="12" font-weight="bold" fill="#1e293b">2 kg</text>
        
        <!-- 접선 속도 벡터 π m/s -->
        <line x1="235" y1="115" x2="235" y2="55" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arr-blue)"/>
        <text x="242" y="55" font-size="12" font-weight="bold" fill="#2563eb">π m/s</text>
    </svg>
    </div>
    """

def get_svg_prob2():
    """문제 2: 실에 매달린 단진자 A - O - B 왕복 운동"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 320 220" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 천장 고정점 -->
        <line x1="110" y1="20" x2="210" y2="20" stroke="#475569" stroke-width="2.5"/>
        <circle cx="160" cy="20" r="3" fill="#1e293b"/>
        
        <!-- 점선 원호 궤적 -->
        <path d="M 80 155 A 150 150 0 0 0 240 155" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
        
        <!-- 실 A, O, B -->
        <line x1="160" y1="20" x2="80" y2="155" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3"/>
        <line x1="160" y1="20" x2="240" y2="155" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3"/>
        <line x1="160" y1="20" x2="160" y2="170" stroke="#334155" stroke-width="1.8"/>
        
        <!-- 위치 A -->
        <circle cx="80" cy="155" r="7.5" fill="#94a3b8"/>
        <text x="80" y="176" font-size="13" font-weight="bold" fill="#334155" text-anchor="middle">A</text>
        
        <!-- 위치 B -->
        <circle cx="240" cy="155" r="7.5" fill="#94a3b8"/>
        <text x="240" y="176" font-size="13" font-weight="bold" fill="#334155" text-anchor="middle">B</text>
        
        <!-- 위치 O (최하점) -->
        <circle cx="160" cy="170" r="8.5" fill="url(#sphereBlue)"/>
        <text x="160" y="193" font-size="14" font-weight="bold" fill="#1d4ed8" text-anchor="middle">O</text>
    </svg>
    </div>
    """

def get_svg_prob3():
    """문제 3: 최고점 p와 최하점 O에서의 알짜힘 화살표"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 320 230" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 천장 고정점 -->
        <line x1="120" y1="20" x2="200" y2="20" stroke="#475569" stroke-width="2.5"/>
        <circle cx="160" cy="20" r="3" fill="#1e293b"/>
        
        <!-- 원호 궤적 -->
        <path d="M 100 170 A 160 160 0 0 0 220 170" fill="none" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="3,3"/>
        
        <!-- 실: 최하점 O 및 최고점 p -->
        <line x1="160" y1="20" x2="160" y2="180" stroke="#64748b" stroke-width="1.2" stroke-dasharray="3,3"/>
        <line x1="160" y1="20" x2="220" y2="170" stroke="#334155" stroke-width="1.8"/>
        
        <!-- 점 O (최하점) -->
        <circle cx="160" cy="180" r="7" fill="#94a3b8"/>
        <text x="160" y="200" font-size="13" font-weight="bold" fill="#334155" text-anchor="middle">O</text>
        <!-- 점 O 알짜힘 화살표 (연직 위쪽) -->
        <line x1="160" y1="180" x2="160" y2="135" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red)"/>
        <text x="145" y="145" font-size="11" font-weight="bold" fill="#dc2626">F_net(O)</text>
        
        <!-- 점 p (최고점) -->
        <circle cx="220" cy="170" r="8" fill="url(#sphereRose)"/>
        <text x="235" y="174" font-size="13" font-weight="bold" fill="#991b1b">p (최고점)</text>
        <!-- 점 p 알짜힘 화살표 (접선 방향) -->
        <line x1="220" y1="170" x2="185" y2="184" stroke="#dc2626" stroke-width="2.5" marker-end="url(#arr-red)"/>
        <text x="175" y="205" font-size="11" font-weight="bold" fill="#dc2626">F_net(p)</text>
    </svg>
    </div>
    """

def get_svg_prob4():
    """문제 4: (가) 단진자, (나) 물체의 높이-시간 h(t) 그래프"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 210" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- (가) 단진자 영역 -->
        <g transform="translate(10, 0)">
            <line x1="60" y1="20" x2="140" y2="20" stroke="#475569" stroke-width="2.5"/>
            <circle cx="100" cy="20" r="3" fill="#1e293b"/>
            
            <path d="M 60 140 A 130 130 0 0 0 140 140" fill="none" stroke="#cbd5e1" stroke-width="1.2" stroke-dasharray="3,3"/>
            <line x1="100" y1="20" x2="65" y2="140" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3"/>
            <line x1="100" y1="20" x2="135" y2="140" stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3,3"/>
            <line x1="100" y1="20" x2="100" y2="150" stroke="#334155" stroke-width="1.8"/>
            
            <circle cx="100" cy="150" r="8" fill="url(#sphereBlue)"/>
            <text x="100" y="154" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">m</text>
            <circle cx="65" cy="140" r="5" fill="#94a3b8"/>
            <circle cx="135" cy="140" r="5" fill="#94a3b8"/>
            
            <text x="100" y="185" font-size="12" font-weight="bold" fill="#1e293b" text-anchor="middle">(가)</text>
        </g>
        
        <!-- (나) 높이-시간 h(t) 그래프 영역 -->
        <g transform="translate(240, 0)">
            <!-- 축 -->
            <line x1="30" y1="150" x2="270" y2="150" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-dark)"/>
            <line x1="30" y1="150" x2="30" y2="20" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-dark)"/>
            <text x="270" y="166" font-size="11" font-weight="bold" fill="#334155" text-anchor="end">시간</text>
            <text x="25" y="16" font-size="11" font-weight="bold" fill="#334155">물체의 높이</text>
            
            <!-- 높이 h 눈금선 -->
            <line x1="30" y1="50" x2="250" y2="50" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="3,3"/>
            <text x="20" y="54" font-size="11" font-weight="bold" fill="#334155">h</text>
            <text x="20" y="154" font-size="11" font-weight="bold" fill="#64748b">0</text>
            
            <!-- h(t) 사이클 곡선: 0에서 시작해서 t0에서 h, 2t0에서 0, 3t0에서 h -->
            <path d="M 30 150 Q 55 50 85 50 Q 115 50 140 150 Q 165 50 195 50 Q 225 50 245 150" fill="none" stroke="#2563eb" stroke-width="2.5"/>
            
            <!-- 시간 눈금 t0, 2t0, 3t0 -->
            <line x1="85" y1="50" x2="85" y2="150" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="140" y1="146" x2="140" y2="154" stroke="#1e293b" stroke-width="1.5"/>
            <line x1="195" y1="50" x2="195" y2="150" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
            
            <text x="85" y="165" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">t₀</text>
            <text x="140" y="165" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">2t₀</text>
            <text x="195" y="165" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">3t₀</text>
            
            <text x="140" y="195" font-size="12" font-weight="bold" fill="#1e293b" text-anchor="middle">(나)</text>
        </g>
    </svg>
    </div>
    """

def get_svg_prob5():
    """문제 5: (가) A, B의 xy 평면 원운동, (나) 시간-가속도 ay 그래프"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 540 220" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- (가) xy 원운동 -->
        <g transform="translate(10, 0)">
            <line x1="10" y1="110" x2="200" y2="110" stroke="#1e293b" stroke-width="1.5" marker-end="url(#arr-dark)"/>
            <line x1="105" y1="200" x2="105" y2="20" stroke="#1e293b" stroke-width="1.5" marker-end="url(#arr-dark)"/>
            <text x="200" y="125" font-size="11" font-weight="bold" fill="#334155">x(m)</text>
            <text x="100" y="16" font-size="11" font-weight="bold" fill="#334155">y(m)</text>
            <text x="94" y="123" font-size="11" font-weight="bold" fill="#64748b">O</text>
            
            <!-- 궤도 A (큰 원) -->
            <circle cx="105" cy="110" r="70" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="35" cy="110" r="6.5" fill="url(#sphereBlue)"/>
            <text x="22" y="105" font-size="12" font-weight="bold" fill="#1d4ed8">A</text>
            <line x1="35" y1="110" x2="35" y2="80" stroke="#2563eb" stroke-width="2" marker-end="url(#arr-blue)"/>
            
            <!-- 궤도 B (작은 원) -->
            <circle cx="105" cy="110" r="40" fill="none" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="3,3"/>
            <circle cx="145" cy="110" r="6.5" fill="url(#sphereRose)"/>
            <text x="156" y="105" font-size="12" font-weight="bold" fill="#b91c1c">B</text>
            <line x1="145" y1="110" x2="145" y2="140" stroke="#dc2626" stroke-width="2" marker-end="url(#arr-red)"/>
            
            <text x="105" y="210" font-size="12" font-weight="bold" fill="#1e293b" text-anchor="middle">(가)</text>
        </g>
        
        <!-- (나) ay - t 가속도 그래프 -->
        <g transform="translate(250, 0)">
            <line x1="20" y1="110" x2="260" y2="110" stroke="#1e293b" stroke-width="1.5" marker-end="url(#arr-dark)"/>
            <line x1="35" y1="200" x2="35" y2="20" stroke="#1e293b" stroke-width="1.5" marker-end="url(#arr-dark)"/>
            <text x="260" y="125" font-size="11" font-weight="bold" fill="#334155">t(s)</text>
            <text x="30" y="16" font-size="11" font-weight="bold" fill="#334155">a_y (m/s²)</text>
            
            <text x="20" y="44" font-size="11" font-weight="bold" fill="#334155">3</text>
            <text x="20" y="65" font-size="11" font-weight="bold" fill="#334155">2</text>
            <text x="23" y="114" font-size="11" font-weight="bold" fill="#64748b">0</text>
            <text x="14" y="180" font-size="11" font-weight="bold" fill="#334155">-3</text>
            
            <!-- 곡선 P (A에 해당: 진폭 3, 주기 6π, t=0에서 아래로) -->
            <!-- 0 -> 1.5π(최저-3) -> 3π(0) -> 4.5π(최고3) -> 6π(0) -->
            <path d="M 35 110 Q 80 190 125 110 Q 170 30 215 110" fill="none" stroke="#2563eb" stroke-width="2.2"/>
            <text x="222" y="102" font-size="11" font-weight="bold" fill="#2563eb">P</text>
            
            <!-- 곡선 Q (B에 해당: 진폭 2, 주기 3π, t=0에서 위로) -->
            <path d="M 35 110 Q 57 55 80 110 Q 102 165 125 110 Q 147 55 170 110 Q 192 165 215 110" fill="none" stroke="#dc2626" stroke-width="1.8" stroke-dasharray="4,2"/>
            <text x="222" y="122" font-size="11" font-weight="bold" fill="#dc2626">Q</text>
            
            <!-- 눈금 표시 -->
            <text x="125" y="125" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">3π</text>
            <text x="215" y="125" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">6π</text>
            
            <text x="140" y="210" font-size="12" font-weight="bold" fill="#1e293b" text-anchor="middle">(나)</text>
        </g>
    </svg>
    </div>
    """

def get_svg_prob6():
    """문제 6: 시계방향 등속 원운동 vx-t 속도 성분 그래프"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 380 200" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 축 -->
        <line x1="30" y1="100" x2="350" y2="100" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-dark)"/>
        <line x1="50" y1="180" x2="50" y2="20" stroke="#1e293b" stroke-width="1.8" marker-end="url(#arr-dark)"/>
        <text x="350" y="115" font-size="11" font-weight="bold" fill="#334155">시간(s)</text>
        <text x="45" y="16" font-size="11" font-weight="bold" fill="#334155">v_x (m/s)</text>
        
        <text x="34" y="44" font-size="11" font-weight="bold" fill="#1e293b">5</text>
        <text x="38" y="104" font-size="11" font-weight="bold" fill="#64748b">0</text>
        <text x="26" y="164" font-size="11" font-weight="bold" fill="#1e293b">-5</text>
        
        <!-- 코사인 곡선: (50, 40) -> (110, 100) -> (170, 160) -> (230, 100) -> (290, 40) -->
        <path d="M 50 40 Q 80 40 110 100 Q 140 160 170 160 Q 200 160 230 100 Q 260 40 290 40 Q 320 40 335 100" fill="none" stroke="#2563eb" stroke-width="2.5"/>
        
        <!-- 눈금선 및 시간 2, 4, 6 -->
        <line x1="50" y1="40" x2="310" y2="40" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2"/>
        <line x1="50" y1="160" x2="310" y2="160" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2"/>
        
        <line x1="170" y1="96" x2="170" y2="104" stroke="#1e293b" stroke-width="1.5"/>
        <line x1="290" y1="96" x2="290" y2="104" stroke="#1e293b" stroke-width="1.5"/>
        
        <text x="170" y="116" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">2</text>
        <text x="290" y="116" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">4</text>
    </svg>
    </div>
    """

def get_svg_prob7():
    """문제 7: 막대 p, q에 연결된 물체 A(2m), B(m)"""
    return f"""
    <div class="svg-container">
    <svg viewBox="0 0 380 180" style="width:100%; height:auto; display:block; margin:0 auto;" xmlns="http://www.w3.org/2000/svg">
        {COMMON_SVG_DEFS}
        <!-- 회전 중심 O -->
        <circle cx="50" cy="90" r="4.5" fill="#1e293b"/>
        <text x="45" y="75" font-size="13" font-weight="bold" fill="#1e293b">O</text>
        
        <!-- 막대 p (길이 2r) -->
        <rect x="50" y="87" width="140" height="6" fill="#cbd5e1" stroke="#64748b" stroke-width="1"/>
        <text x="120" y="80" font-size="12" font-weight="bold" fill="#475569" text-anchor="middle">막대 p</text>
        <line x1="50" y1="115" x2="190" y2="115" stroke="#334155" stroke-width="1" marker-start="url(#arr-dark)" marker-end="url(#arr-dark)"/>
        <text x="120" y="130" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">2r</text>
        
        <!-- 물체 A (2m) -->
        <circle cx="190" cy="90" r="13" fill="url(#sphereBlue)"/>
        <text x="190" y="70" font-size="13" font-weight="bold" fill="#1d4ed8" text-anchor="middle">A</text>
        <text x="190" y="94" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">2m</text>
        
        <!-- 막대 q (길이 r) -->
        <rect x="190" y="87" width="90" height="6" fill="#cbd5e1" stroke="#64748b" stroke-width="1"/>
        <text x="235" y="80" font-size="12" font-weight="bold" fill="#475569" text-anchor="middle">막대 q</text>
        <line x1="190" y1="115" x2="280" y2="115" stroke="#334155" stroke-width="1" marker-start="url(#arr-dark)" marker-end="url(#arr-dark)"/>
        <text x="235" y="130" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">r</text>
        
        <!-- 물체 B (m) -->
        <circle cx="280" cy="90" r="10" fill="url(#sphereRose)"/>
        <text x="280" y="70" font-size="13" font-weight="bold" fill="#b91c1c" text-anchor="middle">B</text>
        <text x="280" y="94" font-size="11" font-weight="bold" fill="#fff" text-anchor="middle">m</text>
    </svg>
    </div>
    """

# =========================================================================
# 문항 렌더링 루틴
# =========================================================================

show_p1 = (view_category in ["📄 1페이지: 원운동 기본 및 단진자 (4문항)", "📖 전체 7문항 모두 보기", "📖 전체 7문항 모두 인쇄"])
show_p2 = (view_category in ["📄 2페이지: 그래프 및 다체 원운동 (3문항)", "📖 전체 7문항 모두 보기", "📖 전체 7문항 모두 인쇄"])

# ==================== [PAGE 1] ====================
if show_p1:
    st.markdown("### 📄 [형성평가 1페이지] 원운동 기본 물리량 및 단진자의 역학적 에너지")

    # ---------- [문제 1] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 1</span> &nbsp; <b>등속 원운동의 기본 물리량 계산</b>
        <p style="margin-top:6px;">그림과 같이 질량이 2kg인 물체가 점 O를 중심으로 반지름이 4m인 원 궤도를 따라 π m/s의 속력으로 등속 원운동을 한다.</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob1())

    if is_print_mode:
        st.markdown("**（1） 각속도의 크기는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 주기는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 구심 가속도의 크기는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 구심력의 크기는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 1 정답 및 단계별 풀이 확인하기", expanded=False):
            st.markdown("""
            * **(1) 각속도의 크기**:
              $$v = r\\omega \\implies \\omega = \\frac{v}{r} = \\frac{\\pi}{4}\\,\\text{rad/s} = \\mathbf{0.25\\pi\\,\\text{rad/s}}$$
            * **(2) 주기**:
              $$T = \\frac{2\\pi r}{v} = \\frac{2\\pi}{\\omega} = \\frac{2\\pi \\times 4}{\\pi} = \\mathbf{8\\,\\text{s}}$$
            * **(3) 구심 가속도의 크기**:
              $$a_c = \\frac{v^2}{r} = r\\omega^2 = \\frac{\\pi^2}{4}\\,\\text{m/s}^2 = \\mathbf{0.25\\pi^2\\,\\text{m/s}^2}$$
            * **(4) 구심력의 크기**:
              $$F_c = m a_c = 2\\,\\text{kg} \\times \\frac{\\pi^2}{4}\\,\\text{m/s}^2 = \\frac{\\pi^2}{2}\\,\\text{N} = \\mathbf{0.5\\pi^2\\,\\text{N}}$$
            """)

    st.divider()

    # ---------- [문제 2] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">문제 2</span> &nbsp; <b>실에 매달린 단진자의 왕복 운동 분석</b>
        <p style="margin-top:6px;">그림과 같이 실에 매달린 물체를 점 A에 가만히 놓았더니, 점 O를 중심으로 A와 B 사이를 왕복 운동한다.</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob2())

    if is_print_mode:
        st.markdown("**（1） 물체의 속력이 최대인 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체에 작용하는 알짜힘의 크기가 최소인 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 물체에 작용하는 알짜힘의 크기가 최대인 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 장력이 가장 큰 지점과 작은 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（5） 운동 에너지가 최대인 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（6） 퍼텐셜 에너지가 최대인 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 2 정답 및 물리적 원리 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 속력이 최대인 지점**: **O점 (최하점)**
              * 중력 퍼텐셜 에너지가 최저가 되면서 역학적 에너지 보존에 의해 운동 에너지(속력)가 최대가 됩니다.
            * **(2) 알짜힘의 크기가 최소인 지점**: **O점 (최하점)**
              * 진동 운동의 복원력(접선 방향 알짜힘 $F_t = mg\\sin\\theta$) 관점에서 최하점($\\theta = 0$)일 때 $F_t = 0$으로 최소가 됩니다.
            * **(3) 알짜힘의 크기가 최대인 지점**: **A, B점 (양 끝점 / 최고점)**
              * 진폭의 양 끝점에서 변위각 $\\theta$가 최대이므로 접선 복원력 $F_t = mg\\sin\\theta_{max}$가 최대가 됩니다.
            * **(4) 장력이 가장 큰 지점과 작은 지점**:
              * 실의 장력 공식: $$T = mg\\cos\\theta + \\frac{mv^2}{l}$$
              * **가장 큰 지점**: **O점 (최하점)** ($\\theta=0$이므로 $\\cos\\theta=1$, 속력 $v$ 최대 $\\implies T_{max} = mg + mv^2/l$)
              * **가장 작은 지점**: **A, B점 (양 끝점)** ($v=0$, $\\cos\\theta < 1 \\implies T_{min} = mg\\cos\\theta_{max}$)
            * **(5) 운동 에너지가 최대인 지점**: **O점 (최하점)** ($E_k = \\frac{1}{2}mv^2$ 최대)
            * **(6) 퍼텐셜 에너지가 최대인 지점**: **A, B점 (양 끝점)** (기준면 대비 높이 $h$가 최대)
            """)

    st.divider()

    # ---------- [문제 3] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">문제 3</span> &nbsp; <b>단진자의 최하점과 최고점에서의 알짜힘 벡터 도시</b>
        <p style="margin-top:6px;">그림은 추가 실에 매달려 점 O를 중심으로 왕복 운동하는 모습을 나타낸 것이다. 점 p는 추의 최고점이다. O, p점에서 추에 작용하는 알짜힘의 방향을 각각 화살표로 나타내시오. (단, 실의 질량, 모든 마찰과 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob3())

    if is_print_mode:
        st.markdown("**（1） 최하점 O에서 추에 작용하는 알짜힘의 방향:**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 최고점 p에서 추에 작용하는 알짜힘의 방향:**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 3 정답 및 힘 벡터 분석 확인하기", expanded=False):
            st.markdown("""
            * **O점 (최하점)에서의 알짜힘 방향**: **연직 위쪽 (원의 중심 방향, ↑)**
              * 최하점에서 물체는 $v \\neq 0$으로 원운동 궤적을 그리며 지나갑니다.
              * 따라서 실 방향으로 구심 가속도 $a_c = \\frac{v^2}{l}$가 필요하므로 실의 장력 $T$가 중력 $mg$보다 큽니다 ($T > mg$).
              * 알짜힘 $\\vec{F}_{net} = T - mg$는 **연직 위쪽(원 중심 방향)**을 향합니다.
            * **p점 (최고점)에서의 알짜힘 방향**: **궤도 원호의 접선 방향 (점 O 쪽을 향하는 접선 방향, ↙)**
              * 최고점에서는 순간 속도 $v = 0$이므로 구심력 성분($mv^2/l$)은 0입니다.
              * 실 방향으로는 장력과 중력의 지름 성분이 평형을 이룹니다 ($T = mg\\cos\\theta$).
              * 따라서 남는 힘은 중력의 접선 성분 $mg\\sin\\theta$뿐이므로, 알짜힘은 **원호의 접선 방향**을 향합니다.
            """)

    st.divider()

    # ---------- [문제 4] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">문제 4</span> &nbsp; <b>단진자의 높이-시간 그래프 정량 분석</b>
        <p style="margin-top:6px;">그림 (가)는 질량이 m인 물체가 길이가 l인 실에 매달려 왕복 운동하는 모습을 나타낸 것이다. 그림 (나)는 물체의 최하점으로부터 물체의 높이를 시간에 따라 나타낸 것이다.</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob4())

    if is_print_mode:
        st.markdown("**（1） 가속도의 크기가 가장 큰 순간을 모두 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 속력이 증가하는 구간을 시각으로 나타내시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 운동 에너지가 가장 큰 순간과 퍼텐셜 에너지가 가장 큰 순간을 각각 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 4 정답 및 그래프 해석 확인하기", expanded=False):
            st.markdown("""
            * **(1) 가속도의 크기가 가장 큰 순간**: **$t_0, 3t_0$**
              * 높이가 최고점 $h$에 도달했을 때 진폭 각도 $\\theta$가 최대이며, 중력의 접선 가속도 $a_t = g\\sin\\theta$가 최대가 됩니다.
            * **(2) 속력이 증가하는 구간**: **$t_0 \\sim 2t_0$** (또는 $3t_0 \\sim 4t_0$)
              * 최고점(높이 $h$)에서 최하점(높이 $0$)으로 내려오는 구간에서는 중력 퍼텐셜 에너지가 운동 에너지로 전환되므로 속력이 점차 증가합니다.
            * **(3) 운동 에너지 및 퍼텐셜 에너지가 가장 큰 순간**:
              * **운동 에너지가 가장 큰 순간**: **$0, 2t_0, 4t_0$** (최하점을 통과하는 순간, 높이 0, 속력 최대)
              * **퍼텐셜 에너지가 가장 큰 순간**: **$t_0, 3t_0$** (최고점에 도달하는 순간, 높이 $h$ 최대)
            """)

# ==================== [PAGE 2] ====================
if show_p2:
    st.markdown("### 📄 [형성평가 2페이지] 원운동 가속도·속도 그래프 및 다체 원운동 구심력")

    # ---------- [문제 5] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 5</span> &nbsp; <b>두 원운동 물체의 가속도 y성분 그래프 비교</b>
        <p style="margin-top:6px;">그림 (가)는 xy평면에서 원점 O를 중심으로 등속 원운동을 하는 물체 A, B가 시간 t=0일 때 각각 x축을 지나는 모습을 나타낸 것이다. 그림 (나)는 시간 t에 따른 물체 A, B의 y축 방향 가속도 a_y를 순서 없이 P, Q로 나타낸 것이다. (단, 물체의 크기는 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob5())

    if is_print_mode:
        st.markdown("**（1） (나)에서 각속도의 크기는 P가 Q의 몇 배인지 풀이과정과 함께 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） t = 0 일 때 A의 운동 방향은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） t = 3π 일 때, B의 운동 방향은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） t = 0일 때와 t = 6π일 때 A와 B의 거리를 풀이과정과 함께 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 5 정답 및 상세 유도 풀이 확인하기", expanded=False):
            st.markdown("""
            * **(1) 각속도의 크기 비교**:
              * (나) 그래프에서 주기 확인:
                * 곡선 P의 주기 $T_P = 6\\pi\\,\\text{s}$
                * 곡선 Q의 주기 $T_Q = 3\\pi\\,\\text{s}$
              * 각속도 공식 $\\omega = \\frac{2\\pi}{T}$ 적용:
                $$\\omega_P = \\frac{2\\pi}{6\\pi} = \\frac{1}{3}\\,\\text{rad/s}, \\quad \\omega_Q = \\frac{2\\pi}{3\\pi} = \\frac{2}{3}\\,\\text{rad/s}$$
              * 따라서 P의 각속도는 Q의 **$\\mathbf{\\frac{1}{2}}$배 (0.5배)**입니다.
            * **(2) $t=0$일 때 A의 운동 방향**:
              * **곡선 매칭**: 구심 가속도 $a = r\\omega^2 \\implies r = \\frac{a}{\\omega^2}$
                * 곡선 P: $a_P = 3, \\omega_P = 1/3 \\implies r_P = \\frac{3}{(1/3)^2} = 27\\,\\text{m}$
                * 곡선 Q: $a_Q = 2, \\omega_Q = 2/3 \\implies r_Q = \\frac{2}{(2/3)^2} = 4.5\\,\\text{m}$
                * 그림 (가)에서 반지름 $r_A > r_B$이므로 **P가 A**, **Q가 B**입니다.
              * **운동 방향 추론**:
                * A(P)는 $t=0$에 $(-r_A, 0)$에 위치합니다.
                * 곡선 P에서 $t=0$ 직후 $a_y < 0$ (음의 방향)이 됩니다.
                * 구심 가속도는 항상 중심(원점)을 향하므로 $a_y$가 음(-)이 되려면 물체의 $y$위치는 양($+y$)이어야 합니다.
                * 따라서 물체 A는 $(-r_A, 0)$에서 $+y$ 방향(시계 방향)으로 회전하므로, $t=0$일 때 운동 방향은 **$\\mathbf{+y}$ 방향 (연직 위쪽)**입니다.
            * **(3) $t=3\\pi$일 때 B의 운동 방향**:
              * B(Q)의 주기는 $T_Q = 3\\pi\\,\\text{s}$입니다.
              * 따라서 $t=3\\pi$는 B의 **정확히 1주기 회전 완료 시점**이므로 $t=0$일 때의 위치 및 운동 방향과 완벽히 같습니다.
              * $t=0$일 때 B는 $(r_B, 0)$에 있고 곡선 Q에서 $t=0$ 직후 $a_y > 0$이므로, $y$좌표는 음수 영역으로 이동해야 중심 방향 구심 가속도가 $+y$가 됩니다.
              * 따라서 $t=3\\pi$일 때 B의 운동 방향은 **$\\mathbf{-y}$ 방향 (연직 아래쪽)**입니다.
            * **(4) $t=0$과 $t=6\\pi$일 때 A와 B의 상대 거리**:
              * $t=0$일 때: A는 $(-r_A, 0)$, B는 $(r_B, 0)$에 있으므로 거리 $d_0 = r_A + r_B = 27 + 4.5 = \\mathbf{31.5\\,\\text{m}}$.
              * $t=6\\pi$일 때:
                * A는 주기 $6\\pi$이므로 정확히 1회전하여 다시 $(-r_A, 0)$에 도달.
                * B는 주기 $3\\pi$이므로 정확히 2회전하여 다시 $(r_B, 0)$에 도달.
              * 따라서 두 시각 모두 위치가 같으므로 거리는 **$\\mathbf{r_A + r_B = 31.5\\,\\text{m}}$로 동일**합니다.
            """)

    st.divider()

    # ---------- [문제 6] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">문제 6</span> &nbsp; <b>시계 방향 등속 원운동과 속도의 x성분 그래프</b>
        <p style="margin-top:6px;">그림은 xy평면에서 원점을 중심으로 시계 방향으로 등속 원운동을 하는 물체의 속도의 x성분 v_x를 시간에 따라 나타낸 것이다.</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob6())

    if is_print_mode:
        st.markdown("**（1） 원 궤도의 반지름을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 각속도를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 3초일 때, 물체의 운동 방향을 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 구심 가속도의 크기를 풀이 과정과 함께 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（5） 2초일 때 구심가속도의 방향은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（6） 4초일 때 구심력의 방향은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 6 정답 및 단계별 풀이 확인하기", expanded=False):
            st.markdown("""
            * **기본 물리량 파악**:
              * $v_x-t$ 그래프에서 최대 속력 $v = 5\\,\\text{m/s}$, 주기 $T = 4\\,\\text{s}$.
              * 문제 조건: **시계 방향** 등속 원운동.
            * **(1) 원 궤도의 반지름**:
              $$v = \\frac{2\\pi r}{T} \\implies r = \\frac{v T}{2\\pi} = \\frac{5 \\times 4}{2\\pi} = \\mathbf{\\frac{10}{\\pi}\\,\\text{m}} \\approx 3.18\\,\\text{m}$$
            * **(2) 각속도**:
              $$\\omega = \\frac{2\\pi}{T} = \\frac{2\\pi}{4} = \\mathbf{\\frac{\\pi}{2}\\,\\text{rad/s}} = \\mathbf{0.5\\pi\\,\\text{rad/s}}$$
            * **(3) 3초일 때 물체의 운동 방향**:
              * $t=0$에서 $v_x = +5$ (시계 방향에서 $+x$ 속도를 갖는 위치는 최상단 $(0, r)$).
              * $t=1\\,\\text{s}$ (1/4주기) $\\implies$ 위치 $(r, 0)$, 속도 방향 $-y$.
              * $t=2\\,\\text{s}$ (1/2주기) $\\implies$ 위치 $(0, -r)$, 속도 방향 $-x$ ($v_x = -5$).
              * $t=3\\,\\text{s}$ (3/4주기) $\\implies$ 위치 $(-r, 0)$, 속도 방향은 **$\\mathbf{+y}$ 방향 (연직 위쪽)**입니다.
            * **(4) 구심 가속도의 크기**:
              $$a_c = v \\omega = 5 \\times \\frac{\\pi}{2} = \\mathbf{\\frac{5\\pi}{2}\\,\\text{m/s}^2} = \\mathbf{2.5\\pi\\,\\text{m/s}^2} \\approx 7.85\\,\\text{m/s}^2$$
              *(또는 $a_c = \\frac{v^2}{r} = \\frac{25}{10/\\pi} = \\frac{2.5\\pi}\\,\\text{m/s}^2$)*
            * **(5) 2초일 때 구심가속도의 방향**:
              * $t=2\\,\\text{s}$에서 물체는 최하단 $(0, -r)$에 위치합니다.
              * 구심 가속도는 항상 중심(원점)을 향하므로 방향은 **$\\mathbf{+y}$ 방향 (연직 위쪽 / 원점 방향)**입니다.
            * **(6) 4초일 때 구심력의 방향**:
              * $t=4\\,\\text{s}$는 1주기 완료 시점으로 최상단 $(0, r)$에 위치합니다.
              * 구심력은 항상 중심(원점)을 향하므로 방향은 **$\\mathbf{-y}$ 방향 (연직 아래쪽 / 원점 방향)**입니다.
            """)

    st.divider()

    # ---------- [문제 7] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">문제 7</span> &nbsp; <b>막대 p, q에 연결된 이체 원운동의 구심력과 장력 분석</b>
        <p style="margin-top:6px;">그림은 막대 p, q에 연결된 물체 A, B가 점 O를 중심으로 각각 등속 원운동을 하는 모습을 나타낸 것이다. p, q의 길이는 각각 2r, r이고, A, B의 질량은 각각 2m, m이다. (단, p와 q는 일직선을 이루며, 막대의 질량, 물체의 크기는 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    render_html(get_svg_prob7())

    if is_print_mode:
        st.markdown("**（1） A와 B의 각속도의 크기를 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） A와 B의 속도의 크기를 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 막대 q가 B에 작용하는 구심력의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 물체 A의 구심력(알짜힘)의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（5） 막대 p가 A에 작용하는 힘의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 7 정답 및 다체 구심력/장력 유도 확인하기", expanded=False):
            st.markdown("""
            * **회전 조건 파악**:
              * 물체 A: 질량 $m_A = 2m$, 회전 반지름 $r_A = 2r$
              * 물체 B: 질량 $m_B = m$, 회전 반지름 $r_B = 2r + r = 3r$
              * 동일 회전축 O에 일직선 막대로 연결되어 함께 회전하므로 회전 각속도 $\\omega$는 동일합니다.
            * **(1) A와 B의 각속도 비교**:
              * 회전 주기와 초당 회전 각도가 같으므로 **$\\mathbf{\\omega_A = \\omega_B}$ (서로 같다, $1 : 1$)**
            * **(2) A와 B의 속도(선속력) 비교**:
              $$v = r\\omega \\implies v_A = 2r\\omega, \\quad v_B = 3r\\omega$$
              * 따라서 **$\\mathbf{v_A : v_B = 2 : 3}$ ($v_B$가 $v_A$의 $1.5$배)**
            * **(3) 막대 q가 B에 작용하는 구심력(장력 $T_q$)의 크기**:
              * 물체 B에 작용하는 유일한 수평 힘은 막대 q가 당기는 장력 $T_q$입니다.
              $$F_{c,B} = T_q = m_B r_B \\omega^2 = m(3r)\\omega^2 = \\mathbf{3mr\\omega^2}$$
            * **(4) 물체 A의 알짜 구심력의 크기**:
              $$F_{c,A} = m_A r_A \\omega^2 = (2m)(2r)\\omega^2 = \\mathbf{4mr\\omega^2}$$
            * **(5) 막대 p가 A에 작용하는 힘($T_p$)의 크기**:
              * 물체 A에는 막대 p가 안쪽(원점)으로 당기는 힘 $T_p$와, 막대 q가 바깥쪽으로 당기는 반작용력 $T_q$가 함께 작용합니다.
              * A의 원운동 알짜 구심력 방정식:
                $$F_{c,A} = T_p - T_q \\implies T_p = F_{c,A} + T_q$$
              * 앞서 구한 값 대입:
                $$T_p = 4mr\\omega^2 + 3mr\\omega^2 = \\mathbf{7mr\\omega^2}$$
              * 따라서 막대 p가 A에 작용하는 힘의 크기는 **$\\mathbf{7mr\\omega^2}$**입니다.
            """)
