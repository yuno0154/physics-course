import streamlit as st
import streamlit.components.v1 as components

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
    각 문제마다 **살아 움직이는 인터랙티브 물리 시뮬레이션**이 함께 탑재되어 있어, 실시간 벡터 변화와 물리 법칙을 직접 눈으로 관찰하며 학습할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["📄 1페이지: 원운동 기본 및 단진자 (4문항)", "📄 2페이지: 그래프 및 다체 원운동 (3문항)", "📖 전체 7문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 각 문항별 인터랙티브 시뮬레이션 컴포넌트 HTML 생성 함수군
# =========================================================================

def render_sim_prob1():
    """문제 1: 등속 원운동 시뮬레이터 (반지름 4m, 속력 π m/s, 속도 및 구심력 벡터)"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 등속 원운동 실시간 시뮬레이션</div>
            <div>
                <button id="btnPlay1" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
                <button id="btnReset1" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">처음으로</button>
            </div>
        </div>
        <canvas id="cv1" width="560" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#475569; margin-top:8px; font-weight:600;">
            <span>반지름 r = 4.0 m</span>
            <span>속력 v = π m/s (3.14 m/s)</span>
            <span style="color:#2563eb;">접선속도 (파랑)</span>
            <span style="color:#dc2626;">구심력 (빨강)</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv1');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay1');
        const btnReset = document.getElementById('btnReset1');
        
        const cx = 280, cy = 115, R = 75;
        let theta = 0;
        let isRunning = true;
        const omega = Math.PI / 4; // T = 8s
        let lastTime = performance.now();
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color) {
            const headlen = 8;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color;
            ctx.fillStyle = color;
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(fromx, fromy);
            ctx.lineTo(tox, toy);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
        }

        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                theta += omega * dt;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 궤도
            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 1.5;
            ctx.setLineDash([4, 4]);
            ctx.beginPath();
            ctx.arc(cx, cy, R, 0, Math.PI * 2);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 중심 O
            ctx.fillStyle = '#1e293b';
            ctx.beginPath();
            ctx.arc(cx, cy, 4, 0, Math.PI * 2);
            ctx.fill();
            ctx.font = 'bold 12px sans-serif';
            ctx.fillText('O', cx - 14, cy - 6);
            
            // 반지름 선
            const px = cx + R * Math.cos(theta);
            const py = cy + R * Math.sin(theta);
            ctx.strokeStyle = '#64748b';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(px, py);
            ctx.stroke();
            
            // 접선 속도 벡터 (파란색)
            const vx = -Math.sin(theta) * 45;
            const vy = Math.cos(theta) * 45;
            drawArrow(ctx, px, py, px + vx, py + vy, '#2563eb');
            
            // 구심력 벡터 (빨간색 - 중심 방향)
            const fx = -Math.cos(theta) * 40;
            const fy = -Math.sin(theta) * 40;
            drawArrow(ctx, px, py, px + fx, py + fy, '#dc2626');
            
            // 물체 (2kg)
            ctx.fillStyle = '#1d4ed8';
            ctx.beginPath();
            ctx.arc(px, py, 9, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#ffffff';
            ctx.font = 'bold 10px sans-serif';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText('2kg', px, py);
            
            requestAnimationFrame(animate);
        }
        
        btnPlay.onclick = () => {
            isRunning = !isRunning;
            btnPlay.textContent = isRunning ? '일시정지' : '재생';
        };
        btnReset.onclick = () => {
            theta = 0;
        };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=310)

def render_sim_prob2_3():
    """문제 2 & 3: 단진자의 왕복 운동 및 O점/p점 알짜힘 벡터 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 단진자의 왕복 운동과 힘 벡터 분석</div>
            <div>
                <button id="btnPlay2" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
                <button id="btnGoO" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #2563eb; background:#eff6ff; color:#1d4ed8; font-weight:bold; cursor:pointer;">최하점 O 정지</button>
                <button id="btnGoP" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #dc2626; background:#fef2f2; color:#b91c1c; font-weight:bold; cursor:pointer;">최고점 p 정지</button>
            </div>
        </div>
        <canvas id="cv2" width="560" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#475569; margin-top:8px; font-weight:600;">
            <span style="color:#2563eb;">장력 T (파랑)</span>
            <span style="color:#64748b;">중력 mg (회색)</span>
            <span style="color:#dc2626; font-weight:bold;">알짜힘 F_net (빨강 화살표)</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv2');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay2');
        const btnGoO = document.getElementById('btnGoO');
        const btnGoP = document.getElementById('btnGoP');
        
        const originX = 280, originY = 30, L = 140;
        const maxTheta = 0.6; // 약 34도
        let theta = maxTheta;
        let omega = 0;
        let isRunning = true;
        const g = 9.8;
        let lastTime = performance.now();
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color, width=2) {
            const headlen = 7;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color;
            ctx.fillStyle = color;
            ctx.lineWidth = width;
            ctx.beginPath();
            ctx.moveTo(fromx, fromy);
            ctx.lineTo(tox, toy);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
        }

        function animate(now) {
            const dt = Math.min((now - lastTime) / 1000, 0.05);
            lastTime = now;
            
            if (isRunning) {
                // 단진자 각가속도: alpha = -(g/L)*sin(theta)
                const alpha = -(180 / L) * Math.sin(theta);
                omega += alpha * dt;
                theta += omega * dt;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 천장
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(originX - 60, originY);
            ctx.lineTo(originX + 60, originY);
            ctx.stroke();
            
            // 궤적 원호
            ctx.strokeStyle = '#cbd5e1';
            ctx.setLineDash([3, 3]);
            ctx.beginPath();
            ctx.arc(originX, originY, L, Math.PI/2 - maxTheta - 0.05, Math.PI/2 + maxTheta + 0.05);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 기준 위치 A, O, B 표시
            const ax = originX + L * Math.sin(-maxTheta);
            const ay = originY + L * Math.cos(-maxTheta);
            const bx = originX + L * Math.sin(maxTheta);
            const by = originY + L * Math.cos(maxTheta);
            const ox = originX;
            const oy = originY + L;
            
            ctx.fillStyle = '#94a3b8';
            ctx.font = 'bold 12px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('A', ax - 14, ay);
            ctx.fillText('B(p)', bx + 18, by);
            ctx.fillText('O(최하점)', ox, oy + 22);
            
            // 실
            const px = originX + L * Math.sin(theta);
            const py = originY + L * Math.cos(theta);
            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 1.8;
            ctx.beginPath();
            ctx.moveTo(originX, originY);
            ctx.lineTo(px, py);
            ctx.stroke();
            
            // 힘 계산
            // 중력: 연직 아래 40px
            const fgY = 42;
            drawArrow(ctx, px, py, px, py + fgY, '#64748b', 1.8);
            
            // 장력: T = mg*cos(theta) + m*v^2/L
            const speedSq = Math.max(0, 2 * 9.8 * L * (Math.cos(theta) - Math.cos(maxTheta)) * 0.15);
            const T_len = 42 * Math.cos(theta) + speedSq * 0.5;
            const tx = -Math.sin(theta) * T_len;
            const ty = -Math.cos(theta) * T_len;
            drawArrow(ctx, px, py, px + tx, py + ty, '#2563eb', 1.8);
            
            // 알짜힘 (F_net = T + Fg)
            const netX = tx;
            const netY = ty + fgY;
            drawArrow(ctx, px, py, px + netX, py + netY, '#dc2626', 3.0);
            
            // 추
            ctx.fillStyle = '#1d4ed8';
            ctx.beginPath();
            ctx.arc(px, py, 9, 0, Math.PI * 2);
            ctx.fill();
            
            requestAnimationFrame(animate);
        }
        
        btnPlay.onclick = () => {
            isRunning = !isRunning;
            btnPlay.textContent = isRunning ? '일시정지' : '재생';
        };
        btnGoO.onclick = () => {
            isRunning = false;
            theta = 0;
            omega = 0;
            btnPlay.textContent = '재생';
        };
        btnGoP.onclick = () => {
            isRunning = false;
            theta = maxTheta;
            omega = 0;
            btnPlay.textContent = '재생';
        };
        requestAnimationFrame(animate);
    })();
    </script>
    """
    components.html(html, height=310)

def render_sim_prob4():
    """문제 4: 단진자의 높이-시간 h(t) 실시간 동기화 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 단진자 진동과 높이-시간 h(t) 그래프 실시간 연동</div>
            <div>
                <button id="btnPlay4" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv4" width="560" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv4');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay4');
        let isRunning = true;
        let t = 0;
        let lastTime = performance.now();
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) {
                t += dt * 1.5;
            }
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 좌측: 단진자 (가)
            const cx = 100, cy = 25, L = 110;
            const maxAngle = 0.55;
            const curAngle = maxAngle * Math.cos(t);
            const bx = cx + L * Math.sin(curAngle);
            const by = cy + L * Math.cos(curAngle);
            
            // 천장
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 2.5;
            ctx.beginPath();
            ctx.moveTo(cx - 40, cy);
            ctx.lineTo(cx + 40, cy);
            ctx.stroke();
            
            // 궤적
            ctx.strokeStyle = '#cbd5e1';
            ctx.setLineDash([2, 2]);
            ctx.beginPath();
            ctx.arc(cx, cy, L, Math.PI/2 - maxAngle, Math.PI/2 + maxAngle);
            ctx.stroke();
            ctx.setLineDash([]);
            
            // 실 & 추
            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 1.6;
            ctx.beginPath();
            ctx.moveTo(cx, cy);
            ctx.lineTo(bx, by);
            ctx.stroke();
            
            ctx.fillStyle = '#2563eb';
            ctx.beginPath();
            ctx.arc(bx, by, 8, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.font = 'bold 12px sans-serif';
            ctx.fillStyle = '#1e293b';
            ctx.fillText('(가) 단진자', cx - 28, 175);
            
            // 우측: h(t) 그래프 (나)
            const gx = 250, gy = 145, gw = 280, gh = 95;
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(gx, gy);
            ctx.lineTo(gx + gw, gy); // 시간축
            ctx.moveTo(gx, gy);
            ctx.lineTo(gx, gy - gh); // 높이축
            ctx.stroke();
            
            ctx.fillStyle = '#334155';
            ctx.font = '11px sans-serif';
            ctx.fillText('시간(t)', gx + gw - 35, gy + 15);
            ctx.fillText('높이(h)', gx - 20, gy - gh - 5);
            ctx.fillText('h', gx - 12, gy - gh + 10);
            ctx.fillText('0', gx - 12, gy + 4);
            
            // h(t) 파형 그리기 (h는 cos^2 형태)
            ctx.strokeStyle = '#2563eb';
            ctx.lineWidth = 2.2;
            ctx.beginPath();
            for (let x = 0; x < gw - 20; x++) {
                const simT = x * 0.05;
                // 높이 h = L * (1 - cos(theta)) 비례
                const val = Math.pow(Math.cos(simT), 2);
                const pyPlot = gy - val * (gh - 15);
                if (x === 0) ctx.moveTo(gx + x, pyPlot);
                else ctx.lineTo(gx + x, pyPlot);
            }
            ctx.stroke();
            
            // 현재 시각 점 트레이싱
            const curPlotX = (t % (Math.PI * 4)) / 0.05;
            if (curPlotX < gw - 20) {
                const curVal = Math.pow(Math.cos(t % (Math.PI * 4)), 2);
                const curPlotY = gy - curVal * (gh - 15);
                ctx.fillStyle = '#dc2626';
                ctx.beginPath();
                ctx.arc(gx + curPlotX, curPlotY, 5, 0, Math.PI*2);
                ctx.fill();
            }
            
            ctx.font = 'bold 12px sans-serif';
            ctx.fillStyle = '#1e293b';
            ctx.fillText('(나) 높이-시간 h(t)', gx + 80, 175);
            
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
    components.html(html, height=280)

def render_sim_prob5():
    """문제 5: 물체 A, B의 xy 원운동과 ay 가속도 곡선 비교 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 두 물체 A, B의 등속 원운동과 ay 가속도 비교</div>
            <div>
                <button id="btnPlay5" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv5" width="560" height="220" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; margin-top:8px; font-weight:600;">
            <span style="color:#2563eb;">물체 A (곡선 P: 주기 6π, 진폭 3)</span>
            <span style="color:#dc2626;">물체 B (곡선 Q: 주기 3π, 진폭 2)</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv5');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay5');
        let isRunning = true;
        let t = 0;
        let lastTime = performance.now();
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) t += dt * 1.8;
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 좌측: xy 평면 원운동
            const ox = 110, oy = 110;
            const rA = 65, rB = 35;
            
            // 좌표축
            ctx.strokeStyle = '#cbd5e1';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(15, oy); ctx.lineTo(205, oy);
            ctx.moveTo(ox, 15); ctx.lineTo(ox, 205);
            ctx.stroke();
            
            // 궤도 A, B
            ctx.strokeStyle = '#94a3b8';
            ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.arc(ox, oy, rA, 0, Math.PI*2); ctx.stroke();
            ctx.beginPath(); ctx.arc(ox, oy, rB, 0, Math.PI*2); ctx.stroke();
            ctx.setLineDash([]);
            
            // 각속도: omega_A = 1/3, omega_B = 2/3 (B가 2배 빠름)
            // A는 t=0에 (-rA, 0)에서 +y로 회전 -> thetaA = Math.PI - (1/3)*t
            // B는 t=0에 (+rB, 0)에서 -y로 회전 -> thetaB = -(2/3)*t
            const thetaA = Math.PI - (1/3) * t;
            const thetaB = -(2/3) * t;
            
            const ax = ox + rA * Math.cos(thetaA);
            const ay = oy + rA * Math.sin(thetaA);
            const bx = ox + rB * Math.cos(thetaB);
            const by = oy + rB * Math.sin(thetaB);
            
            // 물체 A
            ctx.fillStyle = '#2563eb';
            ctx.beginPath(); ctx.arc(ax, ay, 7, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 11px sans-serif'; ctx.fillText('A', ax - 14, ay - 6);
            
            // 물체 B
            ctx.fillStyle = '#dc2626';
            ctx.beginPath(); ctx.arc(bx, by, 7, 0, Math.PI*2); ctx.fill();
            ctx.fillText('B', bx + 8, by - 6);
            
            // 우측: ay(t) 가속도 그래프
            const gx = 250, gy = 110, gw = 280, gh = 80;
            ctx.strokeStyle = '#1e293b';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(gx, gy); ctx.lineTo(gx + gw, gy);
            ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy + gh);
            ctx.stroke();
            
            ctx.fillStyle = '#475569';
            ctx.font = '10px sans-serif';
            ctx.fillText('t(s)', gx + gw - 25, gy + 15);
            ctx.fillText('a_y', gx - 20, gy - gh + 10);
            
            // 곡선 P (A: 파랑, 진폭 35, 주기 60px)
            ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 2.0;
            ctx.beginPath();
            for(let x=0; x<gw-20; x++){
                const val = -Math.sin(x * 0.04);
                const py = gy + val * 45;
                if(x===0) ctx.moveTo(gx+x, py); else ctx.lineTo(gx+x, py);
            }
            ctx.stroke();
            
            // 곡선 Q (B: 빨강, 진폭 25, 주기 30px)
            ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 1.8; ctx.setLineDash([4, 2]);
            ctx.beginPath();
            for(let x=0; x<gw-20; x++){
                const val = Math.sin(x * 0.08);
                const py = gy + val * 30;
                if(x===0) ctx.moveTo(gx+x, py); else ctx.lineTo(gx+x, py);
            }
            ctx.stroke();
            ctx.setLineDash([]);
            
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
    components.html(html, height=290)

def render_sim_prob6():
    """문제 6: 시계 방향 등속 원운동과 vx(t) 코사인 속도 성분 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 시계 방향 등속 원운동과 속도 x성분(vx) 실시간 연동</div>
            <div>
                <button id="btnPlay6" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv6" width="560" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv6');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay6');
        let isRunning = true;
        let t = 0;
        let lastTime = performance.now();
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) t += dt * (Math.PI / 2); // 주기 T = 4s
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 좌측: 시계 방향 원운동 (최상단 (0, r)에서 시작, +x 속도)
            const ox = 110, oy = 110, R = 60;
            const theta = t - Math.PI / 2; // t=0일 때 theta = -pi/2 (최상단)
            const px = ox + R * Math.cos(theta);
            const py = oy + R * Math.sin(theta);
            
            // 궤도
            ctx.strokeStyle = '#94a3b8'; ctx.setLineDash([3,3]);
            ctx.beginPath(); ctx.arc(ox, oy, R, 0, Math.PI*2); ctx.stroke();
            ctx.setLineDash([]);
            
            // 속도 벡터 (시계 방향 접선)
            const vx = -Math.sin(theta) * 35;
            const vy = Math.cos(theta) * 35;
            
            // 접선 속도 (파랑)
            ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 2.5;
            ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + vx, py + vy); ctx.stroke();
            
            // 수평 vx 성분 (초록)
            ctx.strokeStyle = '#16a34a'; ctx.lineWidth = 2.5;
            ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + vx, py); ctx.stroke();
            
            // 물체
            ctx.fillStyle = '#1e293b';
            ctx.beginPath(); ctx.arc(px, py, 7, 0, Math.PI*2); ctx.fill();
            
            // 우측: vx(t) 그래프
            const gx = 250, gy = 110, gw = 280, gh = 65;
            ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(gx, gy); ctx.lineTo(gx + gw, gy);
            ctx.moveTo(gx, gy - gh); ctx.lineTo(gx, gy + gh);
            ctx.stroke();
            
            ctx.fillStyle = '#475569'; ctx.font = '10px sans-serif';
            ctx.fillText('시간(s)', gx + gw - 30, gy + 15);
            ctx.fillText('v_x (5 m/s)', gx - 35, gy - gh + 5);
            ctx.fillText('-5', gx - 20, gy + gh);
            
            // vx 코사인 곡선
            ctx.strokeStyle = '#16a34a'; ctx.lineWidth = 2.2;
            ctx.beginPath();
            for(let x=0; x<gw-20; x++){
                const val = Math.cos(x * 0.05);
                const cyPlot = gy - val * (gh - 10);
                if(x===0) ctx.moveTo(gx+x, cyPlot); else ctx.lineTo(gx+x, cyPlot);
            }
            ctx.stroke();
            
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
    components.html(html, height=280)

def render_sim_prob7():
    """문제 7: 막대 p, q 연결 이체 원운동 동축 회전계 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="font-size:13px; font-weight:bold; color:#1e293b;">🎬 [가상실험] 동축 막대 연결 이체 원운동과 장력(구심력) 분석</div>
            <div>
                <button id="btnPlay7" style="padding:4px 10px; font-size:12px; border-radius:5px; border:1px solid #94a3b8; background:#f8fafc; cursor:pointer;">일시정지</button>
            </div>
        </div>
        <canvas id="cv7" width="560" height="220" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:8px; font-weight:600;">
            <span>A: 질량 2m, 반경 2r (속도 2v₀)</span>
            <span>B: 질량 m, 반경 3r (속도 3v₀)</span>
            <span style="color:#2563eb;">막대 p 장력: 7mrω²</span>
            <span style="color:#dc2626;">막대 q 장력: 3mrω²</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv7');
        const ctx = cv.getContext('2d');
        const btnPlay = document.getElementById('btnPlay7');
        let isRunning = true;
        let theta = 0;
        let lastTime = performance.now();
        const ox = 280, oy = 110;
        const rA = 55, rB = 85;
        
        function animate(now) {
            const dt = (now - lastTime) / 1000;
            lastTime = now;
            if (isRunning) theta += dt * 1.5;
            
            ctx.clearRect(0, 0, cv.width, cv.height);
            
            // 궤도 A, B
            ctx.strokeStyle = '#cbd5e1'; ctx.setLineDash([3,3]);
            ctx.beginPath(); ctx.arc(ox, oy, rA, 0, Math.PI*2); ctx.stroke();
            ctx.beginPath(); ctx.arc(ox, oy, rB, 0, Math.PI*2); ctx.stroke();
            ctx.setLineDash([]);
            
            // 막대 p (0 ~ rA) & 막대 q (rA ~ rB)
            const ax = ox + rA * Math.cos(theta);
            const ay = oy + rA * Math.sin(theta);
            const bx = ox + rB * Math.cos(theta);
            const by = oy + rB * Math.sin(theta);
            
            // 막대 p (파랑)
            ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 4.0;
            ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(ax, ay); ctx.stroke();
            
            // 막대 q (빨강)
            ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 3.0;
            ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(bx, by); ctx.stroke();
            
            // 중심 회전축 O
            ctx.fillStyle = '#1e293b';
            ctx.beginPath(); ctx.arc(ox, oy, 5, 0, Math.PI*2); ctx.fill();
            ctx.font = 'bold 12px sans-serif'; ctx.fillText('O', ox - 15, oy - 6);
            
            // 물체 A (질량 2m)
            ctx.fillStyle = '#1d4ed8';
            ctx.beginPath(); ctx.arc(ax, ay, 11, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px sans-serif';
            ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText('2m', ax, ay);
            
            // 물체 B (질량 m)
            ctx.fillStyle = '#b91c1c';
            ctx.beginPath(); ctx.arc(bx, by, 8, 0, Math.PI*2); ctx.fill();
            ctx.fillStyle = '#ffffff'; ctx.font = 'bold 9px sans-serif';
            ctx.fillText('m', bx, by);
            
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
    components.html(html, height=290)

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
    
    render_sim_prob1()

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
    
    render_sim_prob2_3()

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
        <p style="margin-top:6px;">그림은 추가 실에 매달려 점 O를 중심으로 왕복 운동하는 모습을 나타낸 것이다. 점 p는 추의 최고점이다. O, p점에서 추에 작용하는 알짜힘의 방향을 각각 화살표로 나타내시오. (위 시뮬레이션에서 '최하점 O 정지' 및 '최고점 p 정지' 버튼을 눌러 확인해 보세요.)</p>
    </div>
    """, unsafe_allow_html=True)

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
    
    render_sim_prob4()

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
    
    render_sim_prob5()

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
    
    render_sim_prob6()

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
    
    render_sim_prob7()

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
