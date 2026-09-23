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
pdf_file_name = "포물선운동 과제.pdf"
pdf_path = Path(__file__).parent.parent / pdf_file_name

col_title, col_pdf = st.columns([2.5, 1.2])
with col_title:
    st.title("📝 포물선운동 과제 문제풀이")
    st.caption("2022 개정 교육과정 역학과 에너지 [12역학01-02] · 비스듬히 던진 물체의 포물선 운동 및 역학적 에너지 보존")

with col_pdf:
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        st.download_button(
            label="📥 원문 과제 PDF 다운로드",
            data=pdf_data,
            file_name="포물선운동_과제_학습지.pdf",
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
    st.markdown('<div class="print-header">📝 포물선운동 과제 학습지 &nbsp; [ 학년: 2 &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="meta-table">
        <tr>
            <th>단원정보</th><td>Ⅰ. 시공간과 운동 &nbsp; 01 힘의 합성과 예측</td>
            <th>성취기준</th><td>[12역학01-02] 뉴턴 운동 법칙을 이용하여 물체의 포물선 운동을 정량적으로 설명하고, 포물선 운동에서의 역학적 에너지를 구할 수 있다.</td>
        </tr>
        <tr>
            <th>학습목표</th><td colspan="3">• 물체에 작용하는 힘을 바탕으로 포물선 운동의 수평·연직 방향 운동을 설명할 수 있다.<br>• 초기속도의 수평·연직 성분을 이용하여 포물선 운동의 속도와 위치를 정량적으로 예측할 수 있다.</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["🎯 과제 실전 핵심 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    **2022 개정 교육과정 역학과 에너지** [12역학01-02] 성취기준에 따른 **포물선운동 과제 문항**입니다.
    문제에 들어가는 정적 이미지 대신 **살아 움직이는 인터랙티브 시뮬레이션**을 통해 실시간 궤적, 속도 벡터 분해, 에너지 막대그래프의 변화를 직접 조작하며 학습할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["🎯 과제 실전 핵심 5문항", "🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 인터랙티브 물리 시뮬레이션 렌더링 함수군 (문제 1 ~ 5)
# =========================================================================

def render_sim_prob1():
    """문제 1: 30도 40 m/s 포물선 궤도 및 1초 시점, 최고점, 수평도달거리 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:650px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 30° 40m/s 포물선 운동 실시간 궤적 시뮬레이터</div>
            <div>
                <button id="btnPlay1" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
                <button id="btnT1" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #2563eb; background:#eff6ff; color:#1d4ed8; font-weight:bold; cursor:pointer;">1초 후(정지)</button>
                <button id="btnTop1" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #dc2626; background:#fef2f2; color:#b91c1c; font-weight:bold; cursor:pointer;">최고점(2초)</button>
                <button id="btnReset1" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">처음</button>
            </div>
        </div>
        <canvas id="cv1" width="600" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:8px; font-weight:600;">
            <span>v₀ = 40 m/s (30°)</span>
            <span>최고점 H = 20 m (t=2s)</span>
            <span>1초 후 속력 v = √1300 ≈ 36.1 m/s</span>
            <span>도달거리 R = 80√3 ≈ 138.6 m</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv1');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay1');
        const btnT1 = document.getElementById('btnT1');
        const btnTop1 = document.getElementById('btnTop1');
        const btnReset = document.getElementById('btnReset1');
        
        const g = 10, v0 = 40, theta = Math.PI / 6; // 30도
        const v0x = v0 * Math.cos(theta); // 34.64
        const v0y = v0 * Math.sin(theta); // 20.0
        const tFlight = 2 * v0y / g; // 4s
        
        let simTime = 0;
        let isRunning = true;
        let lastTime = performance.now();
        
        const ox = 50, oy = 180;
        const scaleX = 3.6; // 138.6m -> ~500px
        const scaleY = 5.5; // 20m -> 110px
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color) {
            const headlen = 7;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.0;
            ctx.beginPath(); ctx.moveTo(fromx, fromy); ctx.lineTo(tox, toy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
        }

        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                simTime += dt * 0.8;
                if (simTime > tFlight + 0.5) simTime = 0;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 지면
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(20, oy); ctx.lineTo(580, oy); ctx.stroke();
            ctx.fillStyle = '#64748b'; ctx.font = '11px sans-serif';
            ctx.fillText('수평면', 540, oy + 16);
            
            // 포물선 점선 전체 궤적
            ctx.strokeStyle = '#94a3b8'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let x=0; x<=140; x+=2) {
                const tCur = x / v0x;
                const yCur = v0y * tCur - 0.5 * g * tCur * tCur;
                if (yCur < 0) break;
                const px = ox + x * scaleX;
                const py = oy - yCur * scaleY;
                if (x === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 최고점 (t=2s, x=v0x*2, y=20)
            const topPx = ox + (v0x * 2) * scaleX;
            const topPy = oy - 20 * scaleY;
            ctx.fillStyle = '#dc2626';
            ctx.beginPath(); ctx.arc(topPx, topPy, 4.5, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('최고점(H=20m, 2s)', topPx - 45, topPy - 8);
            
            // 1초 시점 표시 (t=1s, x=v0x, y=15)
            const t1Px = ox + v0x * scaleX;
            const t1Py = oy - 15 * scaleY;
            ctx.strokeStyle = '#cbd5e1'; ctx.setLineDash([2,2]);
            ctx.beginPath(); ctx.moveTo(t1Px, oy); ctx.lineTo(t1Px, t1Py); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = '#2563eb';
            ctx.beginPath(); ctx.arc(t1Px, t1Py, 4, 0, Math.PI*2); ctx.fill();
            ctx.fillText('1초 후(y=15m)', t1Px - 30, t1Py - 8);
            
            // 현재 움직이는 공
            const curT = Math.min(simTime, tFlight);
            const curX = v0x * curT;
            const curY = Math.max(0, v0y * curT - 0.5 * g * curT * curT);
            const cx = ox + curX * scaleX;
            const cy = oy - curY * scaleY;
            
            // 현재 속도 벡터
            const vx = v0x;
            const vy = v0y - g * curT;
            drawArrow(ctx, cx, cy, cx + vx * 0.8, cy - vy * 0.8, '#1d4ed8');
            
            ctx.fillStyle = '#2563eb';
            ctx.beginPath(); ctx.arc(cx, cy, 8, 0, Math.PI*2); ctx.fill();
            
            // 시각 정보 텍스트
            ctx.fillStyle = '#1e293b'; ctx.font = 'bold 12px sans-serif';
            ctx.fillText(`현재 시간 t = ${curT.toFixed(2)} s`, ox + 10, 30);
            
            requestAnimationFrame(animate);
        }
        
        btnPlay.onclick = () => { isRunning = !isRunning; btnPlay.textContent = isRunning ? '일시정지' : '재생'; };
        btnT1.onclick = () => { isRunning = false; simTime = 1.0; btnPlay.textContent = '재생'; };
        btnTop1.onclick = () => { isRunning = false; simTime = 2.0; btnPlay.textContent = '재생'; };
        btnReset.onclick = () => { simTime = 0; isRunning = true; btnPlay.textContent = '일시정지'; };
        
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=310)

def render_sim_prob2():
    """문제 2: A, B(최고점), C 지점 비행 및 실시간 에너지 막대그래프 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:650px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 포물선 운동과 역학적 에너지 막대그래프 실시간 연동</div>
            <div>
                <button id="btnPlay2" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
                <button id="btnGoA" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #2563eb; background:#eff6ff; color:#1d4ed8; font-weight:bold; cursor:pointer;">A점(지면)</button>
                <button id="btnGoB" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #dc2626; background:#fef2f2; color:#b91c1c; font-weight:bold; cursor:pointer;">B점(최고점)</button>
                <button id="btnGoC" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #16a34a; background:#f0fdf4; color:#15803d; font-weight:bold; cursor:pointer;">C점(1.6m)</button>
            </div>
        </div>
        <canvas id="cv2" width="600" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv2');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay2');
        const btnGoA = document.getElementById('btnGoA');
        const btnGoB = document.getElementById('btnGoB');
        const btnGoC = document.getElementById('btnGoC');
        
        // 질량 m = 1kg, v0x = 6 m/s, v0y = 8 m/s, g = 10 m/s^2
        // H_max = 8^2 / 20 = 3.2m
        // E_total = 0.5 * 1 * (6^2 + 8^2) = 50 J
        const m = 1.0, g = 10, v0x = 6, v0y = 8;
        const tB = 0.8; // 최고점
        const tFlight = 1.6; // 낙하 지면
        // C점: h = 1.6m -> 1.6 = 8t - 5t^2 -> 5t^2 - 8t + 1.6 = 0 -> t = 1.365s (하강)
        const tC = 1.365;
        
        let simT = 0;
        let isRunning = true;
        let lastTime = performance.now();
        
        const ox = 40, oy = 180;
        const scaleX = 26; // 0~9.6m -> ~250px
        const scaleY = 35; // 3.2m -> ~112px
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                simT += dt * 0.7;
                if (simT > tFlight + 0.4) simT = 0;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 좌측: 포물선 운동 경로 (A -> B -> C)
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(20, oy); ctx.lineTo(310, oy); ctx.stroke();
            
            // 궤적
            ctx.strokeStyle = '#94a3b8'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let x=0; x<=9.6; x+=0.2) {
                const tc = x / v0x;
                const yc = v0y * tc - 0.5 * g * tc * tc;
                if (yc < 0) break;
                const px = ox + x * scaleX;
                const py = oy - yc * scaleY;
                if (x === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 고정 지점 A, B, C
            // A (0, 0)
            ctx.fillStyle = '#2563eb'; ctx.beginPath(); ctx.arc(ox, oy, 5, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('A(0m)', ox - 10, oy + 16);
            
            // B (4.8m, 3.2m)
            const bx = ox + 4.8 * scaleX, by = oy - 3.2 * scaleY;
            ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(bx, by, 5, 0, Math.PI*2); ctx.fill();
            ctx.fillText('B(3.2m)', bx - 18, by - 8);
            
            // C (6 * 1.365 = 8.19m, 1.6m)
            const cx = ox + (v0x * tC) * scaleX, cy = oy - 1.6 * scaleY;
            ctx.fillStyle = '#16a34a'; ctx.beginPath(); ctx.arc(cx, cy, 5, 0, Math.PI*2); ctx.fill();
            ctx.fillText('C(1.6m)', cx - 8, cy - 8);
            
            // 현재 공 위치
            const curT = Math.min(simT, tFlight);
            const curX = v0x * curT;
            const curY = Math.max(0, v0y * curT - 0.5 * g * curT * curT);
            const curPx = ox + curX * scaleX;
            const curPy = oy - curY * scaleY;
            
            ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.arc(curPx, curPy, 7, 0, Math.PI*2); ctx.fill();
            
            // 에너지 계산
            const curVy = v0y - g * curT;
            const curSpeedSq = v0x * v0x + curVy * curVy;
            const Ek = 0.5 * m * curSpeedSq;
            const Ep = m * g * curY;
            const Etotal = 50.0;
            
            // 우측: 실시간 에너지 막대그래프 (320px ~ 580px)
            const gx = 350, gy = 180, barW = 35, maxH = 120;
            ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8;
            ctx.beginPath(); ctx.moveTo(gx, gy); ctx.lineTo(gx + 220, gy); ctx.moveTo(gx, gy); ctx.lineTo(gx, gy - maxH - 10); ctx.stroke();
            
            ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif';
            ctx.fillText('에너지(J)', gx - 10, gy - maxH - 14);
            ctx.fillText('50', gx - 20, gy - maxH + 4);
            ctx.fillText('0', gx - 14, gy + 4);
            
            // 막대 1: 운동에너지 Ek (초록)
            const hEk = (Ek / 50) * maxH;
            ctx.fillStyle = '#16a34a';
            ctx.fillRect(gx + 30, gy - hEk, barW, hEk);
            ctx.fillStyle = '#1e293b'; ctx.font = 'bold 10px sans-serif';
            ctx.fillText('운동(Ek)', gx + 25, gy + 15);
            ctx.fillText(`${Ek.toFixed(1)}J`, gx + 28, gy - hEk - 4);
            
            // 막대 2: 퍼텐셜에너지 Ep (파랑)
            const hEp = (Ep / 50) * maxH;
            ctx.fillStyle = '#2563eb';
            ctx.fillRect(gx + 95, gy - hEp, barW, hEp);
            ctx.fillStyle = '#1e293b';
            ctx.fillText('위치(Ep)', gx + 90, gy + 15);
            ctx.fillText(`${Ep.toFixed(1)}J`, gx + 93, gy - hEp - 4);
            
            // 막대 3: 역학적 에너지 E (주황)
            const hTotal = maxH;
            ctx.fillStyle = '#ea580c';
            ctx.fillRect(gx + 160, gy - hTotal, barW, hTotal);
            ctx.fillStyle = '#1e293b';
            ctx.fillText('역학적(E)', gx + 155, gy + 15);
            ctx.fillText('50J', gx + 168, gy - hTotal - 4);
            
            requestAnimationFrame(animate);
        }
        
        btnPlay.onclick = () => { isRunning = !isRunning; btnPlay.textContent = isRunning ? '일시정지' : '재생'; };
        btnGoA.onclick = () => { isRunning = false; simT = 0; btnPlay.textContent = '재생'; };
        btnGoB.onclick = () => { isRunning = false; simT = tB; btnPlay.textContent = '재생'; };
        btnGoC.onclick = () => { isRunning = false; simT = tC; btnPlay.textContent = '재생'; };
        
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=310)

def render_sim_prob3():
    """문제 3: (가) 30도 v0 vs (나) 60도 2v0 궤적 및 최고점 도달 시간/높이 비교 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:650px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] (가) 30°, v₀ 와 (나) 60°, 2v₀ 최고점 도달 실시간 비교</div>
            <div>
                <button id="btnPlay3" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv3" width="600" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; font-weight:600; margin-top:8px;">
            <span style="color:#2563eb;">(가) 30°, v₀: 최고점 H₁ = 1, t₁ = 0.5</span>
            <span style="color:#dc2626;">(나) 60°, 2v₀: 최고점 H₂ = 12 (12배!), t₂ = √3 (2√3배)</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv3');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay3');
        let isRunning = true;
        let simT = 0;
        let lastTime = performance.now();
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                simT += dt * 0.9;
                if (simT > 4.0) simT = 0;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            const oy = 175;
            // 지면
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(20, oy); ctx.lineTo(580, oy); ctx.stroke();
            
            // (가) 영역: ox1 = 50
            const ox1 = 50;
            // v0y = 10, v0x = 17.32 (30도)
            ctx.strokeStyle = '#2563eb'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let t=0; t<=2.0; t+=0.1) {
                const x = ox1 + (t * 45);
                const y = oy - (t * 50 - 5 * t * t * 2.5);
                if (y > oy) break;
                if (t === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
            // (가) 현재 공
            const t1 = Math.min(simT, 2.0);
            const p1x = ox1 + (t1 * 45);
            const p1y = Math.min(oy, oy - (t1 * 50 - 5 * t1 * t1 * 2.5));
            ctx.fillStyle = '#2563eb'; ctx.beginPath(); ctx.arc(p1x, p1y, 6.5, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('(가) 30°, v₀', ox1 + 10, oy - 35);
            
            // (나) 영역: ox2 = 300
            const ox2 = 300;
            // 2v0, 60도: v0y = 34.64, v0x = 20
            ctx.strokeStyle = '#dc2626'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let t=0; t<=3.5; t+=0.1) {
                const x = ox2 + (t * 30);
                const y = oy - (t * 100 - 5 * t * t * 4.2);
                if (y > oy) break;
                if (t === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
            // (나) 현재 공
            const t2 = Math.min(simT, 3.46);
            const p2x = ox2 + (t2 * 30);
            const p2y = Math.min(oy, oy - (t2 * 100 - 5 * t2 * t2 * 4.2));
            ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(p2x, p2y, 6.5, 0, Math.PI*2); ctx.fill();
            ctx.fillText('(나) 60°, 2v₀ (H₂ = 12배)', ox2 + 10, 25);
            
            requestAnimationFrame(animate);
        }
        btnPlay.onclick = () => { isRunning = !isRunning; btnPlay.textContent = isRunning ? '일시정지' : '재생'; };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=280)

def render_sim_prob4():
    """문제 4: 60도 v 포물선과 점 p에서의 위치에너지 감소량 & 운동에너지 전환 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:650px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 60° 발사 물체의 최고점과 점 p에서의 에너지 전환 분석</div>
            <div>
                <button id="btnPlay4" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv4" width="600" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv4');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay4');
        let isRunning = true;
        let simT = 0;
        let lastTime = performance.now();
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                simT += dt * 0.8;
                if (simT > 3.0) simT = 0;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            const ox = 70, oy = 175;
            
            // 지면
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(30, oy); ctx.lineTo(550, oy); ctx.stroke();
            
            // 궤적
            ctx.strokeStyle = '#94a3b8'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.moveTo(ox, oy);
            ctx.quadraticCurveTo(ox + 200, -20, ox + 400, oy);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 최고점 (ox + 200, 77)
            const topX = ox + 200, topY = 77;
            ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(topX, topY, 4, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('최고점 (Ek = 1/4 E₀, Ep = 3/4 E₀)', topX - 85, topY - 10);
            
            // 점 p (하강 구간, ox + 320, 115)
            const px = ox + 320, py = 115;
            ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(px, py, 6, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 12px sans-serif'; ctx.fillText('p', px + 10, py - 4);
            ctx.font = '10.5px sans-serif'; ctx.fillStyle = '#b91c1c';
            ctx.fillText('Ek(p) = 3/4 E₀', px + 10, py + 14);
            
            // 현재 공
            const progress = Math.min(simT / 2.5, 1.0);
            const curX = ox + progress * 400;
            const curY = oy - (4 * (progress - progress * progress) * 98);
            ctx.fillStyle = '#2563eb'; ctx.beginPath(); ctx.arc(curX, curY, 7, 0, Math.PI*2); ctx.fill();
            
            requestAnimationFrame(animate);
        }
        btnPlay.onclick = () => { isRunning = !isRunning; btnPlay.textContent = isRunning ? '일시정지' : '재생'; };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=280)

def render_sim_prob5():
    """문제 5: 60도 10m/s 포물선 다중 점묘 잔상 궤적 및 1/2 H 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:650px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 60° 10m/s 다중 스트로브(점묘)와 1/2 H 속력 분석</div>
            <div>
                <button id="btnPlay5" style="padding:4px 9px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv5" width="600" height="220" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:8px; font-weight:600;">
            <span>최고점 도달 시간: √3/2 ≈ 0.87 s</span>
            <span>최고점 높이 H = 3.75 m</span>
            <span style="color:#2563eb;">1/2 H 지점 속력 v = √62.5 ≈ 7.91 m/s</span>
            <span>수평 도달 거리 R = 5√3 ≈ 8.66 m</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv5');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay5');
        let isRunning = true;
        let simT = 0;
        let lastTime = performance.now();
        
        const ox = 70, oy = 180;
        const totalT = Math.sqrt(3); // 약 1.732s
        const scaleX = 52; // 8.66m -> ~450px
        const scaleY = 32; // 3.75m -> ~120px
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                simT += dt * 0.9;
                if (simT > totalT + 0.5) simT = 0;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 지면
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
            ctx.beginPath(); ctx.moveTo(30, oy); ctx.lineTo(570, oy); ctx.stroke();
            
            // 궤적
            ctx.strokeStyle = '#64748b'; ctx.setLineDash([3,3]); ctx.lineWidth = 1.5;
            ctx.beginPath();
            for(let x=0; x<=8.66; x+=0.2) {
                const t = x / 5.0; // v0x = 10 * cos(60) = 5
                const y = 10 * Math.sin(Math.PI/3) * t - 0.5 * 10 * t * t;
                if (y < 0) break;
                const px = ox + x * scaleX;
                const py = oy - y * scaleY;
                if (x === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 최고점 H = 3.75m (x = 4.33m)
            const topPx = ox + 4.33 * scaleX;
            const topPy = oy - 3.75 * scaleY;
            ctx.strokeStyle = '#dc2626'; ctx.setLineDash([2,2]);
            ctx.beginPath(); ctx.moveTo(topPx, oy); ctx.lineTo(topPx, topPy); ctx.stroke();
            ctx.fillStyle = '#dc2626'; ctx.beginPath(); ctx.arc(topPx, topPy, 4.5, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('H = 3.75m', topPx - 25, topPy - 6);
            
            // 1/2 H 수평선 (y = 1.875m)
            const halfPy = oy - 1.875 * scaleY;
            ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 1.2;
            ctx.beginPath(); ctx.moveTo(ox, halfPy); ctx.lineTo(ox + 8.66 * scaleX, halfPy); ctx.stroke();
            ctx.setLineDash([]);
            ctx.fillStyle = '#2563eb'; ctx.fillText('1/2 H (속력 √62.5 m/s)', ox + 8.66 * scaleX + 6, halfPy + 4);
            
            // 다중 점묘 잔상 (스트로브 7개)
            const strobeTimes = [0, 0.28, 0.57, 0.866, 1.15, 1.44, 1.732];
            strobeTimes.forEach(st => {
                const sx = ox + (5.0 * st) * scaleX;
                const sy = oy - (10 * Math.sin(Math.PI/3) * st - 5 * st * st) * scaleY;
                ctx.fillStyle = '#f43f5e'; ctx.beginPath(); ctx.arc(sx, sy, 5.5, 0, Math.PI*2); ctx.fill();
            });
            
            // 현재 이동 공
            const curT = Math.min(simT, totalT);
            const cx = ox + (5.0 * curT) * scaleX;
            const cy = oy - Math.max(0, (10 * Math.sin(Math.PI/3) * curT - 5 * curT * curT)) * scaleY;
            ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(cx, cy, 8, 0, Math.PI*2); ctx.fill();
            
            requestAnimationFrame(animate);
        }
        btnPlay.onclick = () => { isRunning = !isRunning; btnPlay.textContent = isRunning ? '일시정지' : '재생'; };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=300)

# =========================================================================
# 문항 렌더링 루틴 (실전 5문항 + 기초 4문항)
# =========================================================================

show_real = (view_category in ["🎯 과제 실전 핵심 5문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"])
show_basic = (view_category in ["🌱 기초 개념 4문항", "📖 전체 9문항 모두 보기", "📖 전체 9문항 모두 인쇄"])

if show_real:
    st.markdown("### 🎯 과제 실전 핵심 심화 문제 (5문항)")

    # ---------- [문제 1] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 1</span> &nbsp; <b>비스듬히 던진 물체의 기본 포물선 운동 계산</b>
        <p style="margin-top:6px;">지면에서 질량이 2kg인 물체를 수평면과 30°를 이루는 방향으로 40m/s의 속력으로 던진 물체의 운동 경로를 나타낸 것이다. (단, 중력 가속도는 10m/s²이고, 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob1()

    if is_print_mode:
        st.markdown("**（1） 1초 후의 속도의 크기를 구하고, 풀이 과정과 함께 답을 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 최고점의 높이를 구하고, 풀이 과정과 답을 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 수평 도달 거리를 구하고, 풀이 과정과 답을 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 1 정답 및 단계별 풀이 확인하기", expanded=False):
            st.markdown("""
            * **초기 속도 분해**:
              * 수평 방향 속도: $v_{0x} = 40\\cos 30^\\circ = 40 \\times \\frac{\\sqrt{3}}{2} = 20\\sqrt{3}\\,\\text{m/s}$
              * 연직 방향 속도: $v_{0y} = 40\\sin 30^\\circ = 40 \\times \\frac{1}{2} = 20\\,\\text{m/s}$
            * **(1) 1초 후의 속도의 크기**:
              * $t=1\\,\\text{s}$일 때:
                * $v_x = 20\\sqrt{3}\\,\\text{m/s}$ (수평 등속 운동)
                * $v_y = v_{0y} - gt = 20 - 10(1) = 10\\,\\text{m/s}$ (연직 등가속도 운동)
              * 속도의 크기 $v$:
                $$v = \\sqrt{v_x^2 + v_y^2} = \\sqrt{(20\\sqrt{3})^2 + 10^2} = \\sqrt{1200 + 100} = \\sqrt{1300} = \\mathbf{10\\sqrt{13}\\,\\text{m/s}} \\approx 36.06\\,\\text{m/s}$$
            * **(2) 최고점의 높이 $H$**:
              * 최고점 도달 시간: $v_y = 0 \\implies t_{top} = \\frac{v_{0y}}{g} = \\frac{20}{10} = 2\\,\\text{s}$
              * 최고점 높이:
                $$H = v_{0y}t_{top} - \\frac{1}{2}gt_{top}^2 = 20(2) - \\frac{1}{2}(10)(2)^2 = 40 - 20 = \\mathbf{20\\,\\text{m}}$$
            * **(3) 수평 도달 거리 $R$**:
              * 총 비행 시간 $T = 2 t_{top} = 4\\,\\text{s}$
              * 수평 도달 거리:
                $$R = v_x \\times T = 20\\sqrt{3} \\times 4 = \\mathbf{80\\sqrt{3}\\,\\text{m}} \\approx 138.56\\,\\text{m}$$
            """)

    st.divider()

    # ---------- [문제 2] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">문제 2</span> &nbsp; <b>포물선 운동의 역학적 에너지 보존과 막대그래프</b>
        <p style="margin-top:6px;">질량 1.0 kg인 공을 지면에서 비스듬히 던졌다. 그림은 공이 지점 A에서 출발하여 최고점 B를 지나 하강하는 도중 지점 C를 통과하는 포물선 운동의 궤적을 나타낸 것이고, 표는 각 지점에서의 높이와 수평 및 연직 방향 속력을 나타낸 것이다. (단, 공기 저항은 무시하고 g = 10 m/s², 지면의 중력 퍼텐셜에너지는 0으로 한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob2()

    st.markdown("""
    | 지점 | 높이(m) | 수평 방향 속력(m/s) | 연직 방향 속력(m/s) |
    | :---: | :---: | :---: | :---: |
    | **A (출발점)** | 0 | 6 | 8 |
    | **B (최고점)** | 3.2 | 6 | 0 |
    | **C (하강점)** | 1.6 | 6 | - |
    """)

    if is_print_mode:
        st.markdown("**（1） A와 B에서 공의 운동에너지, 중력에 의한 퍼텐셜에너지, 역학적 에너지를 각각 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） (1)의 계산 결과를 바탕으로 에너지 막대그래프(B, C 지점)를 완성하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） A에서 B까지 운동하는 동안 운동에너지와 퍼텐셜에너지가 어떻게 변하는지 서술하고, 역학적 에너지가 일정하게 유지되는 이유를 에너지 전환 관점에서 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） C에서의 역학적 에너지를 계산 없이 예측하고, 그 근거를 서술하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 2 정답 및 에너지 분석 확인하기", expanded=False):
            st.markdown("""
            * **(1) A와 B에서의 에너지**:
              * **A 지점 (지면)**:
                * $E_k = \\frac{1}{2}m v_A^2 = \\frac{1}{2}(1.0)(6^2 + 8^2) = \\frac{1}{2}(100) = \\mathbf{50\\,\\text{J}}$
                * $E_p = mgh = 1.0 \\times 10 \\times 0 = \\mathbf{0\\,\\text{J}}$
                * 역학적 에너지 $E = E_k + E_p = \\mathbf{50\\,\\text{J}}$
              * **B 지점 (최고점)**:
                * $E_k = \\frac{1}{2}m v_{Bx}^2 = \\frac{1}{2}(1.0)(6^2) = \\mathbf{18\\,\\text{J}}$
                * $E_p = mgh = 1.0 \\times 10 \\times 3.2 = \\mathbf{32\\,\\text{J}}$
                * 역학적 에너지 $E = 18 + 32 = \\mathbf{50\\,\\text{J}}$
            * **(2) 에너지 막대그래프**:
              * **B 지점**: 운동에너지 18J, 위치에너지 32J, 역학적 에너지 50J
              * **C 지점**: 위치에너지 $E_p = 1.0 \\times 10 \\times 1.6 = 16\\,\\text{J}$, 운동에너지 $E_k = 50 - 16 = 34\\,\\text{J}$, 역학적 에너지 50J
            * **(3) 에너지 전환 관점 서술**:
              * A에서 B로 올라가는 동안 공의 속력이 감소하여 **운동에너지는 50J에서 18J로 32J 감소**하고, 높이가 높아져 **퍼텐셜에너지는 0J에서 32J로 32J 증가**합니다.
              * 공기 저항이 없을 때 운동에너지의 감소량이 그대로 퍼텐셜에너지 증가량으로 100% 전환되므로, 둘의 합인 **역학적 에너지는 50J로 보존**됩니다.
            * **(4) C에서의 역학적 에너지 예측**:
              * **정답**: **50 J**
              * **근거**: 외력(공기 저항 등)이 작용하지 않고 중력(보존력)만 작용하는 계이므로, 궤적 상의 모든 지점(A, B, C 등)에서 역학적 에너지는 항상 일정하게 보존되기 때문입니다.
            """)

    st.divider()

    # ---------- [문제 3] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">문제 3</span> &nbsp; <b>발사각 30°와 60°의 최고점 도달 시간 및 위치에너지 비교</b>
        <p style="margin-top:6px;">그림 (가), (나)는 각각 수평면과 30°, 60°의 각을 이루는 방향으로 속력 v₀, 2v₀으로 던져진 동일한 물체가 포물선 운동하는 모습을 나타낸 것이다. (단, 수평면에서 중력에 의한 위치에너지는 0이고, 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob3()

    if is_print_mode:
        st.markdown("**（1） 물체를 던진 순간부터 최고점에 도달할 때까지 걸린 시간을 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 최고점에서 중력에 의한 위치 에너지를 비교하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） (나)에서 최고점에서 물체의 중력에 의한 위치 에너지는 운동에너지의 몇 배인지 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 3 정답 및 비교 유도 확인하기", expanded=False):
            st.markdown("""
            * **(1) 최고점 도달 시간 비교 ($t_1 : t_2$)**:
              * $t_{top} = \\frac{v_{0y}}{g}$
              * (가): $v_{1y} = v_0 \\sin 30^\\circ = 0.5 v_0 \\implies t_1 = \\frac{0.5 v_0}{g}$
              * (나): $v_{2y} = 2v_0 \\sin 60^\\circ = 2v_0 \\times \\frac{\\sqrt{3}}{2} = \\sqrt{3}v_0 \\implies t_2 = \\frac{\\sqrt{3}v_0}{g}$
              * 따라서 **$t_1 : t_2 = 1 : 2\\sqrt{3}$** (즉, (나)가 (가)의 **$2\\sqrt{3}$배** 걸림).
            * **(2) 최고점에서의 위치 에너지 비교 ($E_{p1} : E_{p2}$)**:
              * 최고점 높이 $H = \\frac{v_y^2}{2g}$이므로 위치 에너지 $E_p = mgH = \\frac{1}{2}m v_y^2$
              * $E_{p1} \\propto (v_{1y})^2 = (0.5 v_0)^2 = 0.25 v_0^2$
              * $E_{p2} \\propto (v_{2y})^2 = (\\sqrt{3} v_0)^2 = 3 v_0^2$
              * 비례식: $E_{p1} : E_{p2} = 0.25 : 3 = \\mathbf{1 : 12}$ (즉, (나)가 (가)의 **12배**).
            * **(3) (나)의 최고점에서 위치에너지는 운동에너지의 몇 배인가**:
              * (나)의 초기 역학적 에너지: $E_0 = \\frac{1}{2}m (2v_0)^2 = 2mv_0^2$
              * 최고점에서의 속력: 수평 성분만 남으므로 $v_x = 2v_0 \\cos 60^\\circ = v_0$
              * 최고점 운동에너지: $E_k = \\frac{1}{2}m v_x^2 = \\frac{1}{2}mv_0^2$
              * 최고점 위치에너지: $E_p = E_0 - E_k = 2mv_0^2 - \\frac{1}{2}mv_0^2 = \\frac{3}{2}mv_0^2$
              * 비율: $\\frac{E_p}{E_k} = \\frac{1.5 mv_0^2}{0.5 mv_0^2} = \\mathbf{3\\,\\text{배}}$
            """)

    st.divider()

    # ---------- [문제 4] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">문제 4</span> &nbsp; <b>위치 에너지 감소량과 임의의 점 p에서의 운동 에너지</b>
        <p style="margin-top:6px;">그림은 수평면과 60°의 각을 이루며 속력 v로 던져진 질량 m인 물체가 포물선 운동 하여 최고점을 지나 점 p를 통과한 모습을 나타낸 것이다. 수평면에서 던져진 순간 물체의 운동 에너지는 물체가 최고점에서 p까지 운동하는 동안 물체의 중력에 의한 위치 에너지 감소량의 2배이다. p에서 물체의 운동 에너지는? (단, 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob4()

    if is_print_mode:
        st.markdown("**p에서 물체의 운동 에너지를 v와 m으로 나타내시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 4 정답 및 역학적 에너지 유도 확인하기", expanded=False):
            st.markdown("""
            * **던져진 순간의 역학적 에너지 ($E_0$)**:
              * $E_0 = E_{k0} = \\frac{1}{2}mv^2$ (지면 위치에너지 0)
            * **최고점에서의 운동 에너지 및 위치 에너지**:
              * 최고점 수평 속도: $v_x = v\\cos 60^\\circ = \\frac{1}{2}v$
              * 최고점 운동 에너지: $E_{k,top} = \\frac{1}{2}m\\left(\\frac{1}{2}v\\right)^2 = \\frac{1}{8}mv^2 = \\frac{1}{4}E_0$
            * **조건 해석**:
              * "던져진 순간 운동 에너지($E_0$)는 최고점에서 p까지 위치 에너지 감소량($\\Delta E_p$)의 2배이다."
              * $E_0 = 2\\Delta E_p \\implies \\Delta E_p = \\frac{1}{2}E_0$
            * **p점에서의 운동 에너지 ($E_{k,p}$)**:
              * 최고점에서 p까지 내려오는 동안 위치 에너지 감소량 $\\Delta E_p$가 그대로 운동 에너지 증가량으로 전환됩니다.
              $$E_{k,p} = E_{k,top} + \\Delta E_p = \\frac{1}{4}E_0 + \\frac{1}{2}E_0 = \\frac{3}{4}E_0$$
              * $E_0 = \\frac{1}{2}mv^2$ 대입:
                $$E_{k,p} = \\frac{3}{4}\\left(\\frac{1}{2}mv^2\\right) = \\mathbf{\\frac{3}{8}mv^2}$$
            """)

    st.divider()

    # ---------- [문제 5] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">문제 5</span> &nbsp; <b>60° 10m/s 다중 스트로브 궤적과 1/2 H 지점 속력</b>
        <p style="margin-top:6px;">그림은 수평면과 60°의 각으로 속력 10 m/s로 던져진 물체가 운동하는 모습을 나타낸 것이다. (단, 중력 가속도는 10 m/s²이고, 물체의 크기 및 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob5()

    if is_print_mode:
        st.markdown("**（1） 속력 10 m/s로 비스듬히 던져진 물체가 최고점에 도달할 때까지 걸린 시간은?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 최고점의 높이는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 수평 도달 거리는?**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（4） 물체를 던진 순간의 역학적 에너지는? (m을 포함하여 표현)**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（5） 최고점에서 운동에너지는? (m을 포함하여 표현)**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（6） 1/2 H 지점에서의 운동에너지와 위치에너지를 각각 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（7） 1/2 H 지점에서의 속도의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 5 정답 및 종합 풀이 확인하기", expanded=False):
            st.markdown("""
            * **초기 속도 성분**:
              * $v_{0x} = 10\\cos 60^\\circ = 5\\,\\text{m/s}$
              * $v_{0y} = 10\\sin 60^\\circ = 5\\sqrt{3}\\,\\text{m/s}$
            * **(1) 최고점 도달 시간**:
              $$t_{top} = \\frac{v_{0y}}{g} = \\frac{5\\sqrt{3}}{10} = \\mathbf{\\frac{\\sqrt{3}}{2}\\,\\text{s}} \\approx 0.866\\,\\text{s}$$
            * **(2) 최고점의 높이 $H$**:
              $$H = \\frac{v_{0y}^2}{2g} = \\frac{(5\\sqrt{3})^2}{20} = \\frac{75}{20} = \\mathbf{3.75\\,\\text{m}}$$
            * **(3) 수평 도달 거리 $R$**:
              $$R = v_x \\times (2t_{top}) = 5 \\times \\sqrt{3} = \\mathbf{5\\sqrt{3}\\,\\text{m}} \\approx 8.66\\,\\text{m}$$
            * **(4) 던진 순간의 역학적 에너지 $E$**:
              $$E = \\frac{1}{2}m v_0^2 = \\frac{1}{2}m (10)^2 = \\mathbf{50m\\,\\text{J}}$$
            * **(5) 최고점에서의 운동에너지 $E_{k,top}$**:
              $$E_{k,top} = \\frac{1}{2}m v_x^2 = \\frac{1}{2}m (5)^2 = \\mathbf{12.5m\\,\\text{J}} \\quad \\left(=\\frac{1}{4}E\\right)$$
            * **(6) 1/2 H 지점에서의 운동 및 위치에너지**:
              * 최고점 위치에너지: $E_{p,top} = E - E_{k,top} = 50m - 12.5m = 37.5m\\,\\text{J}$
              * $1/2 H$ 지점의 위치에너지:
                $$E_p = \\frac{1}{2} E_{p,top} = \\mathbf{18.75m\\,\\text{J}}$$
              * $1/2 H$ 지점의 운동에너지:
                $$E_k = E - E_p = 50m - 18.75m = \\mathbf{31.25m\\,\\text{J}}$$
            * **(7) 1/2 H 지점에서의 속도의 크기 $v$**:
              $$\\frac{1}{2}mv^2 = 31.25m \\implies v^2 = 62.5 \\implies v = \\sqrt{62.5} = \\mathbf{\\frac{5\\sqrt{10}}{2}\\,\\text{m/s}} \\approx 7.91\\,\\text{m/s}$$
            """)

# =========================================================================
# 기초 개념 4문항 (시뮬레이션 불필요한 개념 문제는 정밀 다이어그램 제공)
# =========================================================================
if show_basic:
    st.markdown("### 🌱 기초 개념 문제 (4문항)")

    # 기초 1
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">기초 1</span> &nbsp; <b>운동의 독립성 (자유낙하 vs 수평투사)</b>
        <p style="margin-top:6px;">같은 높이에서 물체 A는 가만히 놓고(자유 낙하), 물체 B는 수평 방향으로 v의 속력으로 던졌다. 두 물체의 운동에 대한 설명으로 옳은 것을 모두 고르시오.</p>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; padding:10px; max-width:550px; margin:0 auto;">
        <svg viewBox="0 0 450 160" style="width:100%; height:auto;" xmlns="http://www.w3.org/2000/svg">
            <line x1="20" y1="140" x2="430" y2="140" stroke="#1e293b" stroke-width="2"/>
            <rect x="30" y="30" width="40" height="110" fill="#cbd5e1" stroke="#475569"/>
            <!-- A: 자유낙하 -->
            <circle cx="90" cy="30" r="7" fill="#2563eb"/>
            <circle cx="90" cy="65" r="7" fill="#93c5fd"/>
            <circle cx="90" cy="105" r="7" fill="#93c5fd"/>
            <circle cx="90" cy="140" r="7" fill="#2563eb"/>
            <text x="85" y="20" font-size="12" font-weight="bold" fill="#2563eb">A (자유낙하)</text>
            <!-- B: 수평투사 -->
            <circle cx="120" cy="30" r="7" fill="#dc2626"/>
            <circle cx="180" cy="65" r="7" fill="#fca5a5"/>
            <circle cx="260" cy="105" r="7" fill="#fca5a5"/>
            <circle cx="360" cy="140" r="7" fill="#dc2626"/>
            <text x="120" y="20" font-size="12" font-weight="bold" fill="#dc2626">B (수평투사 v₀)</text>
            <!-- 같은 높이 점선 -->
            <line x1="90" y1="65" x2="180" y2="65" stroke="#94a3b8" stroke-dasharray="2,2"/>
            <line x1="90" y1="105" x2="260" y2="105" stroke="#94a3b8" stroke-dasharray="2,2"/>
            <line x1="90" y1="140" x2="360" y2="140" stroke="#94a3b8" stroke-dasharray="2,2"/>
        </svg>
    </div>
    """, height=190)

    if not is_print_mode:
        with st.expander("💡 기초 1 정답 및 개념 해설 확인하기"):
            st.markdown("""
            * **정답**:
              1. **지면 도달 시간은 두 물체가 서로 같다** ($t = \\sqrt{2h/g}$).
              2. **지면에 도달하는 순간의 연직 방향 속도는 서로 같다** ($v_y = gt = \\sqrt{2gh}$).
              3. **지면에 도달하는 순간의 속력은 B가 A보다 크다** ($v_B = \\sqrt{v_0^2 + v_y^2} > v_A = v_y$).
              4. **운동하는 동안 두 물체가 받는 알짜힘(중력)과 가속도(g)는 같다**.
            """)
    else:
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)

    st.divider()

    # 기초 2
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">기초 2</span> &nbsp; <b>최고점에서의 가속도와 속도</b>
        <p style="margin-top:6px;">비스듬히 위로 던져진 물체가 최고점에 도달했을 때, 물체의 속도와 가속도의 크기 및 방향에 대해 서술하시오.</p>
    </div>
    """, unsafe_allow_html=True)
    if not is_print_mode:
        with st.expander("💡 기초 2 정답 및 개념 해설 확인하기"):
            st.markdown("""
            * **속도**:
              * 크기: $v = v_0\\cos\\theta$ (연직 속도는 0이지만, 수평 방향 속도는 유지됨)
              * 방향: **수평 방향**
            * **가속도**:
              * 크기: $g = 9.8\\,\\text{m/s}^2$ (또는 $10\\,\\text{m/s}^2$) 로 일정함 (0이 아님!)
              * 방향: **연직 아래 방향 (지구 중심 방향)**
            """)
    else:
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
