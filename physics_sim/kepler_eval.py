import streamlit as st
import streamlit.components.v1 as components
import os
import base64
from pathlib import Path

try:
    from streamlit_pdf_viewer import pdf_viewer
    HAS_PDF_VIEWER = True
except ImportError:
    HAS_PDF_VIEWER = False

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
            margin-bottom: 14px !important; 
            box-shadow: none !important;
        }
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
        margin-bottom: 12px; 
    }
    .badge-primary { background-color: #eff6ff; color: #1d4ed8; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-success { background-color: #ecfdf5; color: #047857; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-purple { background-color: #faf5ff; color: #7e22ce; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    .badge-amber { background-color: #fffbeb; color: #b45309; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
    </style>
""", unsafe_allow_html=True)

# --- 상단 타이틀 및 원문 PDF 다운로드 ---
pdf_file_name = "케플러 과제.pdf"
pdf_path = Path(__file__).parent.parent / pdf_file_name

col_title, col_pdf = st.columns([2.5, 1.2])
with col_title:
    st.title("📝 케플러 법칙 과제 문제 풀이")
    st.caption("2022 개정 교육과정 역학과 에너지 [12역학01-04] · 케플러 법칙과 만유인력에 의한 행성 및 인공위성 운동 분석")
with col_pdf:
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        st.download_button(
            label="📥 원문 과제 PDF 다운로드",
            data=pdf_data,
            file_name="케플러_법칙_과제_학습지.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# 원문 PDF 펼쳐보기 expander
if os.path.exists(pdf_path):
    with st.expander("📖 원문 과제 PDF 원본 펼쳐보기", expanded=False):
        if HAS_PDF_VIEWER:
            pdf_viewer(str(pdf_path), width=750)
        else:
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

# --- 출력 모드 선택 ---
col_mode1, col_mode2 = st.columns([1.8, 1])
with col_mode1:
    is_print_mode = st.toggle("🖨️ 학습지 출력 모드 전환 (인쇄 및 PDF 저장용)", value=False)
with col_mode2:
    if is_print_mode:
        if st.button("🖨️ 브라우저 바로 인쇄 / PDF 저장", use_container_width=True):
            st.components.v1.html("<script>parent.window.print()</script>", height=0)

if is_print_mode:
    st.markdown('<div class="print-header">📝 케플러 법칙 과제 학습지 &nbsp; [ 학년: 2 &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="meta-table">
        <tr>
            <th>단원정보</th><td>Ⅰ. 시공간과 운동 &nbsp; 04 케플러 법칙과 중력</td>
            <th>성취기준</th><td>[12역학01-04] 케플러 법칙으로부터 중력의 존재가 밝혀지는 과학사적 배경을 이해하고, 중력을 이용하여 인공위성과 행성의 운동을 분석하고 설명할 수 있다.</td>
        </tr>
        <tr>
            <th>학습목표</th><td colspan="3">• 케플러 법칙으로부터 중력의 존재가 밝혀지는 과학사적 배경을 이해할 수 있다.<br>• 중력을 이용해 인공위성과 행성의 운동을 분석하고 설명할 수 있다.</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["📄 1페이지: 타원 궤도와 면적 속도 일정 법칙 (3문항)", "📄 2페이지: 뉴턴 중력과 인공위성 궤도 운동 (4문항)", "📖 전체 7문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    **2022 개정 교육과정 역학과 에너지** [12역학01-04] 성취기준에 따른 **케플러 법칙 과제 문항**입니다.
    각 문항마다 **인터랙티브 시뮬레이션 및 다이어그램**이 탑재되어 있어, 타원 궤도의 면적 속도, 근일점/원일점 물리량 변화, 만유인력과 구심력의 역학적 관계를 직접 관찰하며 학습할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["📄 1페이지: 타원 궤도와 면적 속도 일정 법칙 (3문항)", "📄 2페이지: 뉴턴 중력과 인공위성 궤도 운동 (4문항)", "📖 전체 7문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 각 문항별 인터랙티브 시뮬레이션 컴포넌트 HTML 생성 함수군
# =========================================================================

def render_sim_prob1():
    """문제 1: 타원 궤도 근일점(a)과 원일점(c) 면적 속도 일정 실시간 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 타원 궤도 면적 속도 일정 법칙 및 근일점·원일점 물리량</div>
            <div>
                <button id="btnPlay1" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
                <button id="btnNear1" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#eff6ff; color:#1d4ed8; cursor:pointer; font-weight:bold;">근일점 a</button>
                <button id="btnFar1" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#fef2f2; color:#b91c1c; cursor:pointer; font-weight:bold;">원일점 c</button>
            </div>
        </div>
        <canvas id="cv1" width="580" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div id="stat1" style="display:flex; justify-content:space-around; font-size:11.5px; color:#475569; margin-top:8px; font-weight:600; background:#f1f5f9; padding:6px; border-radius:6px;">
            <span>거리 r: <b>-</b></span>
            <span>속력 v: <b>-</b></span>
            <span>중력 F: <b>-</b></span>
            <span>가속도 a: <b>-</b></span>
            <span>운동E: <b>-</b></span>
            <span>퍼텐셜E: <b>-</b></span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv1');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay1');
        const btnNear = document.getElementById('btnNear1');
        const btnFar = document.getElementById('btnFar1');
        const stat = document.getElementById('stat1');

        const cx = 300, cy = 115, a = 180, b = 105;
        const e = 0.55; // 이심률
        const c_focal = a * e; // 초점 거리 = 99px
        const sunX = cx - c_focal; // 태양 위치 (좌측 초점) = 201px
        const sunY = cy;

        let E_ano = 0; // 이심 근점각 (Eccentric anomaly)
        let isRunning = true;
        let lastTime = performance.now();

        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;

            if (isRunning) {
                // 케플러 방정식 수치 적분: dE/dt = n / (1 - e * cos(E))
                const n = 0.85; // 평균 운동
                const r_norm = 1 - e * Math.cos(E_ano);
                E_ano += (n / r_norm) * dt;
                if (E_ano > Math.PI * 2) E_ano -= Math.PI * 2;
            }

            ctx.clearRect(0, 0, cv.width, cv.height);

            // 1. 타원 궤도 그리기
            ctx.strokeStyle = '#3b82f6';
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.ellipse(cx, cy, a, b, 0, 0, Math.PI * 2);
            ctx.stroke();

            // 2. 장축 점선
            ctx.strokeStyle = '#cbd5e1';
            ctx.lineWidth = 1;
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.moveTo(cx - a, cy);
            ctx.lineTo(cx + a, cy);
            ctx.stroke();
            ctx.setLineDash([]);

            // 3. 부채꼴 면적 S (근일점 a 근처: theta from 0 to 0.5 rad)
            ctx.fillStyle = 'rgba(34, 197, 94, 0.25)';
            ctx.strokeStyle = '#16a34a';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(sunX, sunY);
            for(let ang = Math.PI; ang >= Math.PI - 0.75; ang -= 0.05) {
                const px = cx + a * Math.cos(ang);
                const py = cy + b * Math.sin(ang);
                ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#15803d';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText('S', sunX - 45, cy + 20);

            // 부채꼴 면적 S (원일점 c 근처: theta from 0 to 0.28 rad)
            ctx.fillStyle = 'rgba(34, 197, 94, 0.25)';
            ctx.beginPath();
            ctx.moveTo(sunX, sunY);
            for(let ang = 0; ang <= 0.35; ang += 0.03) {
                const px = cx + a * Math.cos(ang);
                const py = cy + b * Math.sin(ang);
                ctx.lineTo(px, py);
            }
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            ctx.fillStyle = '#15803d';
            ctx.fillText('S', sunX + 90, cy + 18);

            // 4. 태양 (Sun)
            ctx.fillStyle = '#f59e0b';
            ctx.beginPath();
            ctx.arc(sunX, sunY, 11, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#b45309';
            ctx.font = 'bold 11px sans-serif';
            ctx.fillText('태양', sunX - 11, sunY - 14);

            // 5. 주요 지점 라벨: a(근일점), b, c(원일점), d
            ctx.fillStyle = '#1e293b';
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText('a (근일점)', cx - a - 45, cy + 4);
            ctx.fillText('c (원일점)', cx + a + 6, cy + 4);

            // b 지점
            const bx = cx + a * Math.cos(Math.PI - 0.75);
            const by = cy + b * Math.sin(Math.PI - 0.75);
            ctx.fillText('b', bx - 14, by + 12);

            // d 지점
            const dx = cx + a * Math.cos(0.35);
            const dy = cy + b * Math.sin(0.35);
            ctx.fillText('d', dx + 6, dy + 12);

            // 6. 행성 현재 위치 계산
            const curX = cx + a * Math.cos(E_ano);
            const curY = cy + b * Math.sin(E_ano);

            // 태양과 행성 연결선 (동경 벡터)
            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(sunX, sunY);
            ctx.lineTo(curX, curY);
            ctx.stroke();

            // 행성 그리기
            ctx.fillStyle = '#2563eb';
            ctx.beginPath();
            ctx.arc(curX, curY, 7, 0, Math.PI * 2);
            ctx.fill();

            // 물리량 계산 및 실시간 상태 표시
            const dist = Math.sqrt((curX - sunX)**2 + (curY - sunY)**2);
            const rMin = a * (1 - e); // 근일점 거리 ~ 81px
            const rMax = a * (1 + e); // 원일점 거리 ~ 279px
            const speedRel = Math.sqrt(2/dist - 1/a) * 15; // 활력 방정식 기반 상대 속력

            const isNearA = Math.abs(curX - (cx - a)) < 12;
            const isNearC = Math.abs(curX - (cx + a)) < 12;

            if (isNearA) {
                stat.innerHTML = '<span style="color:#1d4ed8;">📍 <b>근일점 a</b>: 속력 <b>최대</b> · 중력 <b>최대</b> · 가속도 <b>최대</b> · 운동E <b>최대</b> · 위치E <b>최소</b></span>';
            } else if (isNearC) {
                stat.innerHTML = '<span style="color:#b91c1c;">📍 <b>원일점 c</b>: 속력 <b>최소</b> · 중력 <b>최소</b> · 가속도 <b>최소</b> · 운동E <b>최소</b> · 위치E <b>최대</b></span>';
            } else {
                stat.innerHTML = `<span>거리 r: <b>${(dist/rMin).toFixed(2)} r₀</b></span>
                                  <span>속력 v: <b>${speedRel.toFixed(1)}</b></span>
                                  <span>중력: <b>${(1/(dist/rMin)**2).toFixed(2)} F₀</b></span>
                                  <span style="color:#0284c7;">역학적 에너지 보존 (E = Ek + Ep)</span>`;
            }

            requestAnimationFrame(animate);
        }

        btnPlay.onclick = () => {
            isRunning = !isRunning;
            btnPlay.textContent = isRunning ? '일시정지' : '재생';
        };
        btnNear.onclick = () => {
            isRunning = false;
            E_ano = Math.PI; // 근일점 (x = cx - a)
            btnPlay.textContent = '재생';
        };
        btnFar.onclick = () => {
            isRunning = false;
            E_ano = 0; // 원일점 (x = cx + a)
            btnPlay.textContent = '재생';
        };

        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=310)

def render_sim_prob2():
    """문제 2: 타원 궤도 p(근일점) -> q -> r(원일점) 면적 S1, S2와 공전 주기 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:6px;">🎬 [가상실험] 타원 궤도 절반 구간(p→q→r)과 면적 S₁ = S₂ 분석</div>
        <canvas id="cv2" width="580" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600; background:#f8fafc; padding:6px; border-radius:6px;">
            <span>p → q: 시간 T 동안 휩쓴 면적 <b>S₁</b></span>
            <span>q → r: 시간 T 동안 휩쓴 면적 <b>S₂</b></span>
            <span style="color:#1d4ed8;">케플러 제2법칙: <b>S₁ = S₂</b></span>
            <span style="color:#b91c1c;">반 바퀴 걸린 시간 = <b>2T</b> → 전체 주기 = <b>4T</b></span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv2');
        const ctx = cv.getContext('2d');
        const cx = 300, cy = 105, a = 180, b = 85;
        const e = 0.55;
        const sunX = cx - a * e;
        const sunY = cy;

        // 면적 분할 점 q: p에서 q까지 면적이 반타원의 절반이 되는 지점
        // 반타원의 총면적 = (1/2)*pi*a*b. 절반 = (1/4)*pi*a*b.
        const q_ang = Math.PI - 1.25;
        const qx = cx + a * Math.cos(q_ang);
        const qy = cy + b * Math.sin(q_ang);

        // 1. 타원 궤도
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 1.8;
        ctx.beginPath();
        ctx.ellipse(cx, cy, a, b, 0, 0, Math.PI * 2);
        ctx.stroke();

        // 2. 장축 (p ~ r)
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 1.2;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(cx - a, cy);
        ctx.lineTo(cx + a, cy);
        ctx.stroke();
        ctx.setLineDash([]);

        // 3. 면적 S1 채우기 (p에서 q까지 아래쪽)
        ctx.fillStyle = 'rgba(59, 130, 246, 0.2)';
        ctx.beginPath();
        ctx.moveTo(sunX, sunY);
        for(let ang = Math.PI; ang >= q_ang; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath();
        ctx.fill();

        // 4. 면적 S2 채우기 (q에서 r까지 아래쪽)
        ctx.fillStyle = 'rgba(239, 68, 68, 0.2)';
        ctx.beginPath();
        ctx.moveTo(sunX, sunY);
        for(let ang = q_ang; ang >= 0; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath();
        ctx.fill();

        // 태양에서 q까지 경계선
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(sunX, sunY);
        ctx.lineTo(qx, qy);
        ctx.stroke();

        // 라벨 S1, S2
        ctx.fillStyle = '#1d4ed8'; ctx.font = 'bold 13px sans-serif';
        ctx.fillText('S₁ (시간 T)', sunX - 60, cy + 35);
        ctx.fillStyle = '#b91c1c';
        ctx.fillText('S₂ (시간 T)', sunX + 50, cy + 35);

        // 태양
        ctx.fillStyle = '#f59e0b'; ctx.beginPath();
        ctx.arc(sunX, sunY, 10, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#b45309'; ctx.font = 'bold 11px sans-serif';
        ctx.fillText('태양', sunX - 11, sunY - 14);

        // 점 라벨 p, q, r
        ctx.fillStyle = '#1e293b'; ctx.font = 'bold 13px sans-serif';
        ctx.fillText('p (근일점)', cx - a - 45, cy + 4);
        ctx.fillText('r (원일점)', cx + a + 6, cy + 4);
        ctx.fillText('q', qx - 4, qy + 16);

        // 점 표시
        ctx.fillStyle = '#0f172a';
        ctx.beginPath(); ctx.arc(cx - a, cy, 4, 0, Math.PI*2); ctx.fill();
        ctx.beginPath(); ctx.arc(cx + a, cy, 4, 0, Math.PI*2); ctx.fill();
        ctx.beginPath(); ctx.arc(qx, qy, 4, 0, Math.PI*2); ctx.fill();
    })();
    </script>
    """
    components.html(html, height=270)

def render_sim_prob3():
    """문제 3: 타원 궤도 a->b(S), b->c(2.5S), c->d(2.5S), d->a(S) 4분할 면적 및 공전주기 7T"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:6px;">🎬 [가상실험] 타원 대칭성 및 4구간 면적 분할 (전체 면적 = 7S, 주기 = 7T)</div>
        <canvas id="cv3" width="580" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#1e293b; margin-top:6px; font-weight:600; background:#f1f5f9; padding:6px; border-radius:6px;">
            <span style="color:#0284c7;">a → b: <b>S (T)</b></span>
            <span style="color:#d97706;">b → c: <b>2.5S (2.5T)</b></span>
            <span style="color:#ea580c;">c → d: <b>2.5S (2.5T)</b></span>
            <span style="color:#16a34a;">d → a: <b>S (T)</b></span>
            <span style="color:#7e22ce; font-weight:bold;">총 면적 7S ⟹ 주기 = 7T</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv3');
        const ctx = cv.getContext('2d');
        const cx = 300, cy = 115, a = 180, b = 95;
        // 문제 조건: 태양에서 근일점 a까지 r, 원일점 c까지 3r. 장축 = 4r => a = 2r.
        // 초점거리 c_focal = a - r = 2r - r = r = a / 2 = 90px.
        const c_focal = 90;
        const sunX = cx - c_focal; // 210px
        const sunY = cy;

        // 점 b, d는 중심 O를 지나는 수직선(단축)과 타원의 교점: x = cx, y = cy + b (b), cy - b (d)
        const bx = cx, by = cy + b;
        const dx = cx, dy = cy - b;

        // 1. 타원 궤도
        ctx.strokeStyle = '#64748b';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.ellipse(cx, cy, a, b, 0, 0, Math.PI * 2);
        ctx.stroke();

        // 2. 단축 bd (수직 점선)
        ctx.strokeStyle = '#cbd5e1'; ctx.setLineDash([3, 3]);
        ctx.beginPath(); ctx.moveTo(cx, cy - b - 10); ctx.lineTo(cx, cy + b + 10); ctx.stroke();
        // 장축 ac (수평 점선)
        ctx.beginPath(); ctx.moveTo(cx - a - 10, cy); ctx.lineTo(cx + a + 10, cy); ctx.stroke();
        ctx.setLineDash([]);

        // 3. 면적 채색 (a -> b: 하늘색 S)
        ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
        ctx.beginPath(); ctx.moveTo(sunX, sunY);
        for(let ang = Math.PI; ang >= Math.PI/2; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath(); ctx.fill();

        // (b -> c: 주황색 2.5S)
        ctx.fillStyle = 'rgba(251, 146, 60, 0.25)';
        ctx.beginPath(); ctx.moveTo(sunX, sunY);
        for(let ang = Math.PI/2; ang >= 0; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath(); ctx.fill();

        // (c -> d: 빨간색 2.5S)
        ctx.fillStyle = 'rgba(239, 68, 68, 0.25)';
        ctx.beginPath(); ctx.moveTo(sunX, sunY);
        for(let ang = 0; ang >= -Math.PI/2; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath(); ctx.fill();

        // (d -> a: 초록색 S)
        ctx.fillStyle = 'rgba(34, 197, 94, 0.25)';
        ctx.beginPath(); ctx.moveTo(sunX, sunY);
        for(let ang = -Math.PI/2; ang >= -Math.PI; ang -= 0.02) {
            ctx.lineTo(cx + a * Math.cos(ang), cy + b * Math.sin(ang));
        }
        ctx.closePath(); ctx.fill();

        // 태양에서 b, d로 잇는 선
        ctx.strokeStyle = '#475569'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(sunX, sunY); ctx.lineTo(bx, by); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(sunX, sunY); ctx.lineTo(dx, dy); ctx.stroke();

        // 라벨 표기
        ctx.fillStyle = '#0284c7'; ctx.font = 'bold 12px sans-serif'; ctx.fillText('S (T)', sunX - 55, cy + 45);
        ctx.fillStyle = '#ea580c'; ctx.fillText('2.5 S (2.5 T)', sunX + 65, cy - 45);
        ctx.fillStyle = '#b45309'; ctx.fillText('2.5 S', sunX + 65, cy + 45);
        ctx.fillStyle = '#15803d'; ctx.fillText('S (대칭)', sunX - 60, cy - 45);

        // 태양
        ctx.fillStyle = '#f59e0b'; ctx.beginPath(); ctx.arc(sunX, sunY, 9, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#b45309'; ctx.font = 'bold 10px sans-serif'; ctx.fillText('태양', sunX - 9, sunY - 12);

        // 중심 O
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(cx, cy, 3, 0, Math.PI*2); ctx.fill();
        ctx.font = 'bold 11px sans-serif'; ctx.fillText('O', cx - 12, cy - 6);

        // 거리 표시 (r, 3r)
        ctx.fillStyle = '#64748b'; ctx.font = 'bold 11px sans-serif';
        ctx.fillText('r', sunX - 45, cy - 6);
        ctx.fillText('3r', sunX + 75, cy - 6);

        // 점 라벨 a, b, c, d
        ctx.fillStyle = '#1e293b'; ctx.font = 'bold 12px sans-serif';
        ctx.fillText('a (근일점)', cx - a - 45, cy + 4);
        ctx.fillText('c (원일점)', cx + a + 6, cy + 4);
        ctx.fillText('b', bx - 3, by + 16);
        ctx.fillText('d', dx - 3, dy - 6);
    })();
    </script>
    """
    components.html(html, height=290)

def render_sim_prob4():
    """문제 4: 만유인력 = 구심력 유도 및 케플러 제3법칙 T^2 = (4pi^2/GM)r^3 수학적 관계 인터랙티브 뷰어"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:14px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [개념 시뮬레이터] 만유인력 = 구심력으로부터 케플러 제3법칙(조화 법칙) 유도</div>
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; justify-content:space-around; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px;">
                <svg width="240" height="150" viewBox="0 0 240 150">
                    <circle cx="120" cy="75" r="55" fill="none" stroke="#94a3b8" stroke-dasharray="4,4" stroke-width="1.5"/>
                    <circle cx="120" cy="75" r="14" fill="#f59e0b"/>
                    <text x="120" y="79" font-size="11" font-weight="bold" fill="#ffffff" text-anchor="middle">M</text>
                    <text x="120" y="52" font-size="11" font-weight="bold" fill="#d97706" text-anchor="middle">태양</text>
                    <line x1="120" y1="75" x2="175" y2="75" stroke="#64748b" stroke-dasharray="2,2"/>
                    <text x="145" y="71" font-size="11" font-weight="bold" fill="#64748b" text-anchor="middle">r</text>
                    <circle cx="175" cy="75" r="8" fill="#3b82f6"/>
                    <text x="175" y="78" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">m</text>
                    <path d="M 175 75 L 140 75" fill="none" stroke="#ef4444" stroke-width="2.5" marker-end="url(#arrow_red)"/>
                    <text x="155" y="90" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle">F (중력=구심력)</text>
                    <path d="M 175 75 L 175 45" fill="none" stroke="#10b981" stroke-width="2.5" marker-end="url(#arrow_green)"/>
                    <text x="188" y="55" font-size="11" font-weight="bold" fill="#10b981">v</text>
                    <defs>
                        <marker id="arrow_red" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444"/>
                        </marker>
                        <marker id="arrow_green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                            <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981"/>
                        </marker>
                    </defs>
                </svg>
                <div style="font-size:12px; line-height:1.7; color:#334155;">
                    <div style="background:#eff6ff; padding:6px 10px; border-radius:6px; border:1px solid #bfdbfe; margin-bottom:6px;">
                        <b>[1단계] 중력 = 구심력</b><br>
                        <code>G·(M·m)/r² = m·v²/r</code><br>
                        ⟹ <b>v = √(GM/r)</b> <span style="color:#2563eb; font-weight:bold;">[㉠ 정답]</span>
                    </div>
                    <div style="background:#fef2f2; padding:6px 10px; border-radius:6px; border:1px solid #fecaca;">
                        <b>[2단계] 주기와 속력 관계 대입</b><br>
                        <code>v = 2πr / T  ⟹  T = 2πr / v</code><br>
                        <code>T² = 4π²r² / (GM/r) = (4π²/GM)·r³</code><br>
                        ⟹ <b>T² = ( 4π²/GM ) · r³</b> <span style="color:#dc2626; font-weight:bold;">[㉡ 정답]</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    components.html(html, height=220)

def render_sim_prob5():
    """문제 5: 인공위성 A(m, r), B(2m, 4r) 등속 원운동 동시 회전 및 속력 비 2:1 비교 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 인공위성 A(m, r)와 B(2m, 4r)의 궤도 운동 및 속력 비교</div>
            <button id="btnPlay5" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
        </div>
        <canvas id="cv5" width="580" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600; background:#eff6ff; padding:6px; border-radius:6px;">
            <span style="color:#1d4ed8;">위성 A: 질량 m, 반경 r, 속력 v_A = √(GM/r)</span>
            <span style="color:#ea580c;">위성 B: 질량 2m, 반경 4r, 속력 v_B = √(GM/4r) = 0.5 v_A</span>
            <span style="color:#16a34a; font-weight:bold;">속력의 비 (v_A : v_B) = 2 : 1</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv5');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay5');
        const ox = 290, oy = 105;
        const rA = 38, rB = 88; // 궤도 반지름 시각화

        let thA = 0, thB = 0;
        let isRunning = true;
        let lastTime = performance.now();

        // 주기 비 T_A : T_B = 1 : 8 (케플러 제3법칙 r^(3/2))
        // 따라서 각속도 비 w_A : w_B = 8 : 1
        const wA = 2.0;
        const wB = 2.0 / 8;

        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                thA += wA * dt;
                thB += wB * dt;
            }

            ctx.clearRect(0, 0, cv.width, cv.height);

            // 궤도 A, B
            ctx.strokeStyle = '#93c5fd'; ctx.lineWidth = 1.5; ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.arc(ox, oy, rA, 0, Math.PI * 2); ctx.stroke();
            ctx.strokeStyle = '#fed7aa'; ctx.lineWidth = 1.5;
            ctx.beginPath(); ctx.arc(ox, oy, rB, 0, Math.PI * 2); ctx.stroke();
            ctx.setLineDash([]);

            // 중심 지구
            ctx.fillStyle = '#38bdf8'; ctx.beginPath(); ctx.arc(ox, oy, 14, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#0369a1'; ctx.font = 'bold 11px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('지구', ox, oy);

            // 위성 A (질량 m, 반경 r)
            const ax = ox + rA * Math.cos(thA);
            const ay = oy + rA * Math.sin(thA);
            ctx.fillStyle = '#2563eb'; ctx.beginPath(); ctx.arc(ax, ay, 6, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#1e3a8a'; ctx.font = 'bold 11px sans-serif';
            ctx.fillText('A(m)', ax + 14, ay - 6);

            // 위성 B (질량 2m, 반경 4r)
            const bx = ox + rB * Math.cos(thB);
            const by = oy + rB * Math.sin(thB);
            ctx.fillStyle = '#ea580c'; ctx.beginPath(); ctx.arc(bx, by, 8.5, 0, Math.PI * 2); ctx.fill();
            ctx.fillStyle = '#7c2d12'; ctx.font = 'bold 11px sans-serif';
            ctx.fillText('B(2m)', bx + 16, by - 6);

            requestAnimationFrame(animate);
        }

        btnPlay.onclick = () => {
            isRunning = !isRunning;
            btnPlay.textContent = isRunning ? '일시정지' : '재생';
        };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=270)

def render_sim_prob6():
    """문제 6: 인공위성 A(3m, r)와 B(m, 2r)의 구심력(12:1), 속력(루트2:1), 주기(1:2루트2) 정량 비교 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:6px;">🎬 [가상실험] 인공위성 A(3m, r) vs B(m, 2r) 물리량 정밀 비교</div>
        <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px;">
            <svg width="260" height="170" viewBox="0 0 260 170">
                <circle cx="130" cy="85" r="42" fill="none" stroke="#60a5fa" stroke-width="1.5" stroke-dasharray="3,3"/>
                <circle cx="130" cy="85" r="75" fill="none" stroke="#f97316" stroke-width="1.5" stroke-dasharray="3,3"/>
                <circle cx="130" cy="85" r="14" fill="#38bdf8"/>
                <text x="130" y="89" font-size="10" font-weight="bold" fill="#0369a1" text-anchor="middle">지구(M)</text>
                <line x1="130" y1="85" x2="172" y2="85" stroke="#94a3b8" stroke-dasharray="2,2"/>
                <text x="151" y="80" font-size="10" font-weight="bold" fill="#64748b" text-anchor="middle">r</text>
                <circle cx="172" cy="85" r="8" fill="#2563eb"/>
                <text x="188" y="82" font-size="11" font-weight="bold" fill="#1d4ed8">A (3m)</text>
                <line x1="130" y1="85" x2="130" y2="10" stroke="#94a3b8" stroke-dasharray="2,2"/>
                <text x="140" y="48" font-size="10" font-weight="bold" fill="#64748b">2r</text>
                <circle cx="130" cy="10" r="5.5" fill="#ea580c"/>
                <text x="148" y="14" font-size="11" font-weight="bold" fill="#c2410c">B (m)</text>
            </svg>
            <div style="font-size:12px; line-height:1.8; color:#1e293b;">
                <div style="background:#eff6ff; padding:5px 8px; border-radius:5px; margin-bottom:4px; border:1px solid #bfdbfe;">
                    <b>(1) 구심력 크기 비교:</b><br>
                    F_A = G·M(3m)/r² = 3·F₀<br>
                    F_B = G·Mm/(2r)² = 0.25·F₀<br>
                    ⟹ <b>F_A : F_B = 12 : 1 (F_A가 12배)</b>
                </div>
                <div style="background:#f0fdf4; padding:5px 8px; border-radius:5px; margin-bottom:4px; border:1px solid #bbf7d0;">
                    <b>(2) 속력 비교 (v ∝ 1/√R):</b><br>
                    v_A : v_B = 1/√r : 1/√(2r) = <b>√2 : 1 (v_A가 √2배)</b>
                </div>
                <div style="background:#fef3c7; padding:5px 8px; border-radius:5px; border:1px solid #fde68a;">
                    <b>(3) 공전 주기 비교 (T ∝ R^(3/2)):</b><br>
                    T_A : T_B = r^(3/2) : (2r)^(3/2) = <b>1 : 2√2 (T_B가 2√2배)</b>
                </div>
            </div>
        </div>
    </div>
    """
    components.html(html, height=230)

def render_sim_prob7():
    """문제 7: 행성 P(M, 2R, 고도3R => r=5R) vs 행성 Q(2M, R, 고도5R => r=6R) 심화 비교 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:620px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [심화 비교] 행성 P-위성 A 계 vs 행성 Q-위성 B 계 물리량 비교</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:8px;">
            <div style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:8px; padding:8px; text-align:center;">
                <div style="font-size:12px; font-weight:bold; color:#7e22ce; margin-bottom:4px;">(가) 행성 P와 위성 A</div>
                <svg width="180" height="110" viewBox="0 0 180 110">
                    <circle cx="90" cy="55" r="45" fill="none" stroke="#c084fc" stroke-dasharray="3,3" stroke-width="1.2"/>
                    <circle cx="90" cy="55" r="18" fill="#a855f7"/>
                    <text x="90" y="58" font-size="9" font-weight="bold" fill="#ffffff" text-anchor="middle">P(M, 2R)</text>
                    <line x1="90" y1="55" x2="135" y2="55" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="135" cy="55" r="5" fill="#2563eb"/>
                    <text x="145" y="58" font-size="10" font-weight="bold" fill="#1d4ed8">A</text>
                    <text x="105" y="70" font-size="9" fill="#6b21a8">2R+3R = <b>5R</b></text>
                </svg>
                <div style="font-size:11px; color:#581c87; font-weight:600;">궤도 반지름 r_A = <b>5R</b></div>
            </div>
            <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px; padding:8px; text-align:center;">
                <div style="font-size:12px; font-weight:bold; color:#047857; margin-bottom:4px;">(나) 행성 Q와 위성 B</div>
                <svg width="180" height="110" viewBox="0 0 180 110">
                    <circle cx="90" cy="55" r="52" fill="none" stroke="#34d399" stroke-dasharray="3,3" stroke-width="1.2"/>
                    <circle cx="90" cy="55" r="12" fill="#10b981"/>
                    <text x="90" y="58" font-size="8.5" font-weight="bold" fill="#ffffff" text-anchor="middle">Q(2M, R)</text>
                    <line x1="90" y1="55" x2="142" y2="55" stroke="#94a3b8" stroke-dasharray="2,2"/>
                    <circle cx="142" cy="55" r="5" fill="#ea580c"/>
                    <text x="152" y="58" font-size="10" font-weight="bold" fill="#c2410c">B</text>
                    <text x="105" y="70" font-size="9" fill="#065f46">R+5R = <b>6R</b></text>
                </svg>
                <div style="font-size:11px; color:#065f46; font-weight:600;">궤도 반지름 r_B = <b>6R</b></div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; background:#f8fafc; border:1px solid #e2e8f0; padding:6px; border-radius:6px; font-weight:600;">
            <span style="color:#b91c1c;">(1) 중력 비 (F_A : F_B) = <b>18 : 25</b></span>
            <span style="color:#7e22ce;">(2) 주기 비 (T_A : T_B) = <b>5√5 : 6√3</b></span>
            <span style="color:#047857;">(3) 속력 비 (v_A : v_B) = <b>√3 : √5</b></span>
        </div>
    </div>
    """
    components.html(html, height=225)

# =========================================================================
# 문항 렌더링 루틴
# =========================================================================

show_p1 = (view_category in ["📄 1페이지: 타원 궤도와 면적 속도 일정 법칙 (3문항)", "📖 전체 7문항 모두 보기", "📖 전체 7문항 모두 인쇄"])
show_p2 = (view_category in ["📄 2페이지: 뉴턴 중력과 인공위성 궤도 운동 (4문항)", "📖 전체 7문항 모두 보기", "📖 전체 7문항 모두 인쇄"])

# ==================== [PAGE 1] ====================
if show_p1:
    st.markdown("### 📄 [과제 1페이지] 케플러 제1·2법칙 및 타원 궤도 역학 분석")

    # ---------- [문제 1] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 1</span> &nbsp; <b>타원 궤도와 면적 속도 일정 법칙 및 물리량 분석</b>
        <p style="margin-top:6px;">그림은 행성이 태양 주위를 도는 모습을 나타낸 것이다. 행성이 점 a에서 점 b까지, 점 c에서 점 d까지 이동하는 동안 행성과 태양을 연결한 선분이 지나간 면적은 각각 S로 같다. a와 c는 각각 근일점과 원일점이다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob1()

    if is_print_mode:
        st.markdown("**（1） 케플러 제2법칙(면적 속도 일정 법칙)에 따라 일정한 시간 동안 태양과 행성을 연결하는 선분이 만든 ㉠ ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )은 같다. 따라서 행성이 a에서 b까지 이동하는 데 걸린 시간이 t일 때, c에서 d까지 이동하는 데 걸린 시간은 ㉡ ( &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; )이다.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 행성이 c에서 어떤 점까지 이동하는 동안 행성과 태양을 연결한 선분이 지나간 면적이 2S가 될 때 이동하는 데 걸린 시간은 a에서 b까지 이동하는 데 걸린 시간의 몇 배가 되는지 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 행성의 공전 주기가 T이고 타원 궤도의 긴반지름이 a라고 할 때, 공전 주기가 8T인 행성의 긴반지름은 얼마인지 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 행성의 속력이 가장 빠른 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（5） 행성에 작용하는 중력의 크기가 가장 큰 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（6） 가속도가 가장 큰 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（7） 운동 에너지가 가장 큰 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（8） 중력에 의한 위치 에너지가 가장 큰 지점은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 1 정답 및 고교 눈높이 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) ㉠과 ㉡**: **㉠ 면적, ㉡ $t$**
              * 케플러 제2법칙(면적 속도 일정 법칙)에 따라 행성과 태양을 잇는 선분이 같은 시간 동안 쓸고 지나가는 **면적**은 항상 같습니다.
              * 따라서 지나간 면적이 $S$로 서로 같으므로 걸린 시간도 **$t$**로 동일합니다.
            * **(2) 면적이 2S일 때 걸린 시간의 배수**: **2배 ($2t$)**
              * 면적 속도($\\Delta S / \\Delta t$)가 일정하므로 쓸고 간 면적과 걸린 시간은 정비례합니다 ($S \\propto t$).
              * 면적이 $S$에서 $2S$로 2배가 되었으므로 이동하는 데 걸린 시간도 2배($2t$)가 됩니다.
            * **(3) 공전 주기가 8T인 행성의 긴반지름**: **$4a$**
              * 케플러 제3법칙(조화의 법칙)에 따라 주기의 제곱은 타원 궤도 긴반지름의 세제곱에 비례합니다 ($T^2 \\propto a^3$).
              * 주기가 8배가 되면 주기의 제곱은 $8^2 = 64$배가 됩니다. 어떤 값의 세제곱이 64가 되려면 해당 값은 4가 되어야 합니다 ($4^3 = 64$).
              * 따라서 긴반지름은 원래의 **$4a$**가 됩니다.
            * **(4) 속력이 가장 빠른 지점**: **a점 (근일점)**
              * 태양과 가장 가까운 근일점에서 행성의 공전 속력이 최대이고, 가장 먼 원일점에서 최소입니다.
            * **(5) 중력의 크기가 가장 큰 지점**: **a점 (근일점)**
              * 만유인력 $F = G\\frac{Mm}{r^2}$에 의해 태양과의 거리 $r$이 가장 짧은 근일점에서 중력이 가장 큽니다.
            * **(6) 가속도가 가장 큰 지점**: **a점 (근일점)**
              * 뉴턴 운동 제2법칙에 의해 가속도 $a = \\frac{F}{m} = \\frac{GM}{r^2}$이므로 중력이 가장 큰 근일점에서 가속도 역시 최대입니다.
            * **(7) 운동 에너지가 가장 큰 지점**: **a점 (근일점)**
              * 운동 에너지 $E_k = \\frac{1}{2}mv^2$이므로 속력이 가장 빠른 근일점에서 운동 에너지가 최대입니다.
            * **(8) 중력에 의한 위치 에너지가 가장 큰 지점**: **c점 (원일점)**
              * 역학적 에너지 보존 법칙($E = E_k + E_p = \\text{일정}$)에 의해 운동 에너지가 최소인 원일점에서 중력 퍼텐셜 에너지(위치 에너지)는 최대가 됩니다.
            """)

    st.divider()

    # ---------- [문제 2] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">문제 2</span> &nbsp; <b>타원 궤도 p → q → r 면적과 공전 주기</b>
        <p style="margin-top:6px;">그림과 같이 행성이 태양을 한 초점으로 하는 타원 궤도를 따라 점 p, q, r을 지나며 운동한다. 행성이 p에서 q까지와 q에서 r까지 운동하는 동안 태양과 행성을 연결한 선분이 휩쓸고 지나간 면적은 각각 S₁, S₂이고, 걸린 시간은 T로 같다. p, r은 각각 근일점, 원일점이다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob2()

    if is_print_mode:
        st.markdown("**（1） S₁과 S₂의 면적을 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 행성의 공전 주기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 속력이 가장 빠른 지점과 느린 지점을 각각 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 중력이 가장 큰 지점과 가장 작은 지점을 각각 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 2 정답 및 물리적 원리 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) S₁과 S₂의 면적 비교**: **$S_1 = S_2$ (서로 같다)**
              * 케플러 제2법칙(면적 속도 일정 법칙)에 따라 행성이 같은 시간($T$) 동안 휩쓸고 지나간 면적은 항상 같으므로 $S_1 = S_2$입니다.
            * **(2) 행성의 공전 주기**: **$4T$**
              * 근일점 p에서 원일점 r까지 선분을 연결하면 타원의 장축(대칭축)이 됩니다.
              * 따라서 p에서 r까지 이동하는 구간은 **타원 궤도의 정확히 절반(반 타원)**에 해당합니다.
              * 근일점 p에서 원일점 r까지 가는 데 걸린 시간은 $T + T = 2T$입니다.
              * 타원은 장축을 기준으로 위아래가 대칭이므로, 나머지 반 바퀴(원일점 r에서 근일점 p로 돌아오는 구간)를 도는 데 걸리는 시간도 똑같이 $2T$입니다.
              * 따라서 행성이 타원 궤도를 한 바퀴 온전히 도는 **공전 주기는 $2T + 2T = \\mathbf{4T}$**입니다.
            * **(3) 속력이 가장 빠른 지점과 느린 지점**:
              * **가장 빠른 지점**: **p점 (근일점)** (태양과 거리가 가장 가까움)
              * **가장 느린 지점**: **r점 (원일점)** (태양과 거리가 가장 멂)
            * **(4) 중력이 가장 큰 지점과 가장 작은 지점**:
              * **가장 큰 지점**: **p점 (근일점)** ($F = G\\frac{Mm}{r^2}$에서 거리가 가장 작으므로 중력 최대)
              * **가장 작은 지점**: **r점 (원일점)** (거리가 가장 크므로 중력 최소)
            """)

    st.divider()

    # ---------- [문제 3] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">문제 3</span> &nbsp; <b>타원 궤도의 대칭성과 4구간 면적 분할을 이용한 주기 계산</b>
        <p style="margin-top:6px;">그림은 행성 A가 태양을 한 초점으로 하는 타원 궤도를 공전하는 모습을 나타낸 것이다. 점 O는 타원 궤도의 중심이고, 점 a, b, c, d는 공전 궤도상에 있다. A가 a에서 b까지 운동하는 데 걸린 시간은 T이다. A가 a에서 b, c에서 d까지 이동하는 동안 태양과 A를 연결한 선분이 쓸고 지나간 면적은 각각 S, 5/2 S이다. 태양에서 근일점 a까지의 거리는 r, 원일점 c까지의 거리는 3r이다. 물음에 답하시오.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob3()

    if is_print_mode:
        st.markdown("**（1） c에서 d까지 운동하는 데 걸린 시간을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） d에서 a까지 운동하는 데 걸린 시간을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 공전 주기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 3 정답 및 단계별 풀이 확인하기", expanded=False):
            st.markdown("""
            * **(1) c에서 d까지 운동하는 데 걸린 시간**: **$\\frac{5}{2}T$ (또는 $2.5T$)**
              * 케플러 제2법칙에 의해 쓸고 지나간 면적은 걸린 시간에 정비례합니다.
              * 면적이 $S$일 때 걸린 시간이 $T$이므로, 쓸고 간 면적이 $\\frac{5}{2}S$인 c에서 d까지 걸린 시간은 **$\\frac{5}{2}T$**입니다.
            * **(2) d에서 a까지 운동하는 데 걸린 시간**: **$T$**
              * 타원은 장축 ac를 기준으로 상하 완전 대칭입니다.
              * 따라서 d에서 a까지 이동할 때 태양과 연결한 선분이 쓸고 지나간 면적은 a에서 b까지 쓸고 지나간 면적 $S$와 대칭으로 완전히 같습니다.
              * 면적이 $S$로 같으므로 걸린 시간도 **$T$**입니다.
            * **(3) 공전 주기**: **$7T$**
              * 장축 대칭성에 의해 각 4구간의 면적과 이동 시간은 다음과 같습니다:
                * $a \\to b$: 면적 $S$, 걸린 시간 $T$
                * $b \\to c$: 면적 $\\frac{5}{2}S$ ($c \\to d$와 대칭), 걸린 시간 $\\frac{5}{2}T$
                * $c \\to d$: 면적 $\\frac{5}{2}S$, 걸린 시간 $\\frac{5}{2}T$
                * $d \\to a$: 면적 $S$ ($a \\to b$와 대칭), 걸린 시간 $T$
              * 타원 궤도 전체 면적:
                $$S_{\\text{전체}} = S + \\frac{5}{2}S + \\frac{5}{2}S + S = 7S$$
              * 면적 $S$당 걸리는 시간이 $T$이므로, 행성의 공전 주기는:
                $$T_{\\text{주기}} = T + \\frac{5}{2}T + \\frac{5}{2}T + T = \\mathbf{7T}$$
            """)

# ==================== [PAGE 2] ====================
if show_p2:
    if show_p1:
        st.markdown("---")
    st.markdown("### 📄 [과제 2페이지] 뉴턴 중력과 인공위성 궤도 운동 분석")

    # ---------- [문제 4] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 4</span> &nbsp; <b>뉴턴 만유인력 법칙으로부터 케플러 제3법칙(조화 법칙) 유도</b>
        <p style="margin-top:6px;">다음은 뉴턴 중력 법칙과 케플러 제3법칙에 대한 설명이다. 질량 M인 태양을 중심으로 질량 m인 행성이 속력 v, 궤도 반지름 r인 등속 원운동 한다. 행성이 태양으로부터 받는 중력은 구심력과 같으므로, 중력상수를 G라고 하면 다음과 같은 관계를 얻을 수 있다.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<b>v = ( ㉠ )</b><br>
        이 식에 행성의 주기와 속력 관계를 적용하면 다음과 같은 관계를 얻을 수 있다.<br>
        &nbsp;&nbsp;&nbsp;&nbsp;<b>T² = ( ㉡ ) r³</b><br>
        즉, 뉴턴 중력 법칙으로부터 케플러 제3법칙을 이끌어낼 수 있다. ㉠과 ㉡에 들어갈 식을 쓰시오.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob4()

    if is_print_mode:
        st.markdown("**（1） ㉠에 들어갈 식:**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） ㉡에 들어갈 식:**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 4 정답 및 수식 유도 과정 확인하기", expanded=False):
            st.markdown("""
            * **㉠에 들어갈 식**: **$\\sqrt{\\frac{GM}{r}}$**
              * 행성에 작용하는 만유인력이 곧 원운동을 유지시키는 구심력 역할을 합니다:
                $$G\\frac{Mm}{r^2} = \\frac{mv^2}{r}$$
              * 양변에서 행성의 질량 $m$을 소거하고 양변에 $r$을 곱하면:
                $$v^2 = \\frac{GM}{r} \\implies \\mathbf{v = \\sqrt{\\frac{GM}{r}}}$$
            * **㉡에 들어갈 식**: **$\\frac{4\\pi^2}{GM}$**
              * 등속 원운동의 주기 $T$와 궤도 반지름 $r$, 속력 $v$의 관계는 $v = \\frac{2\\pi r}{T} \\implies T = \\frac{2\\pi r}{v}$입니다.
              * 양변을 제곱하면:
                $$T^2 = \\frac{4\\pi^2 r^2}{v^2}$$
              * 위에서 구한 $v^2 = \\frac{GM}{r}$을 분모에 대입하면:
                $$T^2 = \\frac{4\\pi^2 r^2}{\\frac{GM}{r}} = \\left(\\mathbf{\\frac{4\\pi^2}{GM}}\\right) r^3$$
              * 태양의 질량 $M$과 중력상수 $G$는 변하지 않는 상수이므로, 주기의 제곱이 반지름의 세제곱에 비례한다는 케플러 제3법칙($T^2 \\propto r^3$)이 수학적으로 유도됩니다!
            """)

    st.divider()

    # ---------- [문제 5] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">문제 5</span> &nbsp; <b>인공위성 A(m, r)와 B(2m, 4r)의 구심력과 속력 유도</b>
        <p style="margin-top:6px;">그림은 지구를 중심으로 각각 등속 원운동을 하는 인공위성 A, B를 나타낸 것이다. A, B의 질량은 각각 m, 2m이고, 원 궤도의 반지름은 각각 r, 4r이다. A, B의 속력을 각각 vA, vB라고 할 때 vA : vB를 구심력을 이용하여 풀이 과정과 함께 구하시오. (단, A, B에는 지구에 의한 중력만 작용한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob5()

    if is_print_mode:
        st.markdown("**• A 위성에 작용하는 구심력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• A 위성에 작용하는 중력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• A 위성의 속력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• B 위성에 작용하는 구심력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• B 위성에 작용하는 중력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• B 위성의 속력 :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**• 최종 속력의 비 (vA : vB) :**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 5 정답 및 단계별 풀이 확인하기", expanded=False):
            st.markdown("""
            * **지구 질량을 $M$이라 할 때 단계별 유도**:
              * **A 위성에 작용하는 구심력**:
                $$F_{c,A} = \\mathbf{\\frac{m v_A^2}{r}}$$
              * **A 위성에 작용하는 중력**:
                $$F_{g,A} = \\mathbf{G\\frac{Mm}{r^2}}$$
              * **A 위성의 속력**:
                $$\\frac{m v_A^2}{r} = G\\frac{Mm}{r^2} \\implies v_A^2 = \\frac{GM}{r} \\implies \\mathbf{v_A = \\sqrt{\\frac{GM}{r}}}$$
              * **B 위성에 작용하는 구심력**:
                $$F_{c,B} = \\frac{(2m) v_B^2}{4r} = \\mathbf{\\frac{m v_B^2}{2r}}$$
              * **B 위성에 작용하는 중력**:
                $$F_{g,B} = G\\frac{M(2m)}{(4r)^2} = G\\frac{2Mm}{16r^2} = \\mathbf{G\\frac{Mm}{8r^2}}$$
              * **B 위성의 속력**:
                $$\\frac{2m v_B^2}{4r} = G\\frac{2Mm}{16r^2} \\implies v_B^2 = \\frac{GM}{4r} \\implies \\mathbf{v_B = \\sqrt{\\frac{GM}{4r}} = \\frac{1}{2}\\sqrt{\\frac{GM}{r}}}$$
            * **최종 속력의 비 ($v_A : v_B$)**:
              $$v_A : v_B = \\sqrt{\\frac{GM}{r}} : \\frac{1}{2}\\sqrt{\\frac{GM}{r}} = 1 : \\frac{1}{2} = \\mathbf{2 : 1}$$
            * *(핵심 개념: 인공위성의 궤도 속력 $v = \\sqrt{GM/r}$은 위성 자신의 질량과는 아무런 관련이 없으며, 오직 궤도 반지름의 제곱근에 반비례합니다!)*
            """)

    st.divider()

    # ---------- [문제 6] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">문제 6</span> &nbsp; <b>인공위성 A(3m, r)와 B(m, 2r)의 구심력·속력·주기 비교</b>
        <p style="margin-top:6px;">그림은 인공위성 A, B가 각각 지구를 중심으로 등속 원운동 하는 모습을 나타낸 것이다. A, B의 원 궤도 반지름은 각각 r, 2r이고, A, B의 질량은 각각 3m, m이다. 모든 풀이는 식을 사용하여 비교함.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob6()

    if is_print_mode:
        st.markdown("**（1） A와 B의 구심력의 크기를 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） A의 속력과 B의 속력을 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） A와 B의 공전 주기를 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 6 정답 및 수식 비교 풀이 확인하기", expanded=False):
            st.markdown("""
            * **(1) A와 B의 구심력의 크기 비교**: **$F_A : F_B = 12 : 1$ (A가 B의 12배)**
              * 인공위성의 구심력은 지구가 당기는 중력과 같습니다 ($F_c = F_g = G\\frac{M m_{위성}}{R^2}$):
                $$F_A = G\\frac{M(3m)}{r^2} = 3\\frac{GMm}{r^2}$$
                $$F_B = G\\frac{Mm}{(2r)^2} = \\frac{1}{4}\\frac{GMm}{r^2}$$
              * 두 힘의 비:
                $$\\frac{F_A}{F_B} = \\frac{3}{\\frac{1}{4}} = \\mathbf{12} \\quad \\implies \\mathbf{F_A = 12 F_B}$$
            * **(2) A와 B의 속력 비교**: **$v_A : v_B = \\sqrt{2} : 1$ (A가 B의 $\\sqrt{2}$배 또는 약 1.41배)**
              * 인공위성의 속력 $v = \\sqrt{\\frac{GM}{R}}$은 위성 질량과 무관하며 궤도 반지름 $R$에만 의존합니다:
                $$v_A = \\sqrt{\\frac{GM}{r}}, \\quad v_B = \\sqrt{\\frac{GM}{2r}} = \\frac{1}{\\sqrt{2}}\\sqrt{\\frac{GM}{r}}$$
              * 두 속력의 비:
                $$\\frac{v_A}{v_B} = \\frac{1}{\\frac{1}{\\sqrt{2}}} = \\mathbf{\\sqrt{2}} \\quad \\implies \\mathbf{v_A = \\sqrt{2} v_B}$$
            * **(3) A와 B의 공전 주기 비교**: **$T_A : T_B = 1 : 2\\sqrt{2}$ (B가 A의 $2\\sqrt{2}$배 또는 약 2.83배)**
              * 케플러 제3법칙에 의해 $T^2 \\propto R^3 \\implies T \\propto R^{3/2}$입니다 (위성 질량과 무관):
                $$\\frac{T_B}{T_A} = \\left(\\frac{2r}{r}\\right)^{3/2} = 2^{3/2} = \\sqrt{2^3} = \\mathbf{2\\sqrt{2} \\approx 2.83} \\quad \\implies \\mathbf{T_B = 2\\sqrt{2} T_A}$$
            """)

    st.divider()

    # ---------- [문제 7] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">문제 7</span> &nbsp; <b>행성의 질량과 반지름 및 고도가 다른 두 인공위성 심화 분석</b>
        <p style="margin-top:6px;">그림 (가)는 인공위성 A가 질량과 반지름이 각각 M, 2R인 행성 P의 표면에서 3R만큼 떨어진 궤도를 따라 등속 원운동 하는 모습을, (나)는 인공위성 B가 질량과 반지름이 각각 2M, R인 행성 Q의 표면에서 5R만큼 떨어진 궤도를 따라 등속 원운동 하는 모습을 나타낸 것이다. A와 B의 질량은 같다. A와 B에 작용하는 중력의 크기는 각각 FA, FB이고, A와 B의 공전 주기는 각각 TA, TB이다.<br>
        (1) FA : FB 는?<br>
        (2) TA : TB 는?<br>
        (3) A 위성의 속력을 vA, B 위성의 속력을 vB라고 할 때 vA : vB 는?</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob7()

    if is_print_mode:
        st.markdown("**（1） FA : FB 는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） TA : TB 는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） vA : vB 는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 7 정답 및 상세 계산 과정 확인하기", expanded=False):
            st.markdown("""
            * **[핵심 출발점] 각 인공위성의 '중심으로부터의 궤도 반지름' 계산**:
              * 만유인력 공식의 거리 $r$은 행성 표면이 아니라 **행성의 중심으로부터의 거리**입니다:
                * 위성 A의 궤도 반지름: $r_A = (\\text{행성 P 반지름 } 2R) + (\\text{고도 } 3R) = \\mathbf{5R}$ (행성 질량 $M_P = M$)
                * 위성 B의 궤도 반지름: $r_B = (\\text{행성 Q 반지름 } R) + (\\text{고도 } 5R) = \\mathbf{6R}$ (행성 질량 $M_Q = 2M$)
              * 위성 A와 B의 질량은 $m$으로 동일합니다.
            * **(1) 중력의 크기 비 ($F_A : F_B$)**: **$18 : 25$**
              * 중력 공식 $F = G\\frac{M_{\\text{행성}} m}{r^2}$:
                $$F_A = G\\frac{M \\cdot m}{(5R)^2} = \\frac{1}{25}\\frac{GMm}{R^2}$$
                $$F_B = G\\frac{2M \\cdot m}{(6R)^2} = \\frac{2}{36}\\frac{GMm}{R^2} = \\frac{1}{18}\\frac{GMm}{R^2}$$
              * 두 힘의 비:
                $$F_A : F_B = \\frac{1}{25} : \\frac{1}{18} = \\mathbf{18 : 25}$$
            * **(2) 공전 주기의 비 ($T_A : T_B$)**: **$5\\sqrt{5} : 6\\sqrt{3}$ (또는 $\\sqrt{125} : \\sqrt{108}$)**
              * 조화의 법칙 유도식 $T = 2\\pi \\sqrt{\\frac{r^3}{GM_{\\text{행성}}}}$ 또는 $T^2 \\propto \\frac{r^3}{M_{\\text{행성}}}$:
                $$T_A^2 \\propto \\frac{(5R)^3}{M} = \\frac{125 R^3}{M}$$
                $$T_B^2 \\propto \\frac{(6R)^3}{2M} = \\frac{216 R^3}{2M} = \\frac{108 R^3}{M}$$
              * 주기의 제곱의 비:
                $$T_A^2 : T_B^2 = 125 : 108$$
              * 양변에 제곱근을 취하면:
                $$T_A : T_B = \\sqrt{125} : \\sqrt{108} = \\mathbf{5\\sqrt{5} : 6\\sqrt{3}} \\quad (\\approx 11.18 : 10.39)$$
            * **(3) 속력의 비 ($v_A : v_B$)**: **$\\sqrt{3} : \\sqrt{5}$ (또는 $3 : \\sqrt{15}$)**
              * 속력 공식 $v = \\sqrt{\\frac{GM_{\\text{행성}}}{r}}$:
                $$v_A = \\sqrt{\\frac{GM}{5R}} = \\frac{1}{\\sqrt{5}}\\sqrt{\\frac{GM}{R}}$$
                $$v_B = \\sqrt{\\frac{G(2M)}{6R}} = \\sqrt{\\frac{GM}{3R}} = \\frac{1}{\\sqrt{3}}\\sqrt{\\frac{GM}{R}}$$
              * 두 속력의 비:
                $$v_A : v_B = \\frac{1}{\\sqrt{5}} : \\frac{1}{\\sqrt{3}} = \\mathbf{\\sqrt{3} : \\sqrt{5}} \\quad (\\approx 1.732 : 2.236)$$
            """)
