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
pdf_file_name = "힘의합성과운동예측 과제.pdf"
pdf_path = Path(__file__).parent.parent / pdf_file_name

col_title, col_pdf = st.columns([2.5, 1.2])
with col_title:
    st.title("📝 힘의 합성과 운동 예측 과제 문제 풀이")
    st.caption("2022 개정 교육과정 역학과 에너지 [12역학01-01] · 힘의 벡터 합성 및 운동 상태 정량 예측")

with col_pdf:
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        st.download_button(
            label="📥 원문 과제 PDF 다운로드",
            data=pdf_data,
            file_name="힘의합성과운동예측_과제_학습지.pdf",
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
    st.markdown('<div class="print-header">📝 힘의 합성과 운동 예측 과제 학습지 &nbsp; [ 학년: 2 &nbsp; 반: ____ &nbsp; 번호: ____ &nbsp; 이름: __________ &nbsp; 점수: ______ ]</div>', unsafe_allow_html=True)
    st.markdown("""
    <table class="meta-table">
        <tr>
            <th>단원정보</th><td>Ⅰ. 시공간과 운동 &nbsp; 01 힘의 합성과 예측</td>
            <th>성취기준</th><td>[12역학01-01] 물체에 작용하는 여러 가지 힘의 합력을 구하여 물체의 운동을 정량적으로 예측할 수 있다.</td>
        </tr>
        <tr>
            <th>학습목표</th><td colspan="3">• 힘을 벡터로 나타내고 여러 힘의 합력을 구할 수 있다.<br>• 힘을 적절한 방향의 성분으로 분해하여 합력을 정량적으로 구할 수 있다.<br>• 합력의 크기와 방향을 이용하여 물체의 운동 변화를 예측할 수 있다.</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    view_category = st.radio("인쇄 범위 선택", ["📄 1페이지: 힘의 기본 개념과 합성 (4문항)", "📄 2페이지: 힘의 성분 분해와 빗면 운동 (6문항)", "📄 3페이지: 심화 연결계와 도르래 운동 (4문항)", "📖 전체 14문항 모두 인쇄"], horizontal=True)
else:
    st.markdown("""
    **2022 개정 교육과정 역학과 에너지** [12역학01-01] 성취기준에 따른 **힘의 합성과 운동 예측 과제 문항**입니다.
    문제마다 **살아 움직이는 인터랙티브 시뮬레이션**과 **정밀 물리 다이어그램**을 통해 힘의 합성, 분해, 빗면 마찰, 도르래 연결계의 운동 원리를 직접 체감하며 학습할 수 있습니다.
    """)
    view_category = st.radio(
        "문항 분류 선택", 
        ["📄 1페이지: 힘의 기본 개념과 합성 (4문항)", "📄 2페이지: 힘의 성분 분해와 빗면 운동 (6문항)", "📄 3페이지: 심화 연결계와 도르래 운동 (4문항)", "📖 전체 14문항 모두 보기"], 
        horizontal=True
    )

st.markdown("---")

# =========================================================================
# 인터랙티브 시뮬레이션 및 다이어그램 컴포넌트군
# =========================================================================

def render_sim_prob1():
    """문제 1: 1차원 반대 방향 두 힘의 합성 시뮬레이터 (오른쪽 12N, 왼쪽 7N)"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 1차원 두 힘의 벡터 합성과 알짜힘 시뮬레이터</div>
        <canvas id="cv_f1" width="560" height="150" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#2563eb;">F₁ = 12 N (오른쪽)</span>
            <span style="color:#dc2626;">F₂ = 7 N (왼쪽)</span>
            <span style="color:#16a34a; font-weight:bold;">알짜힘 F_net = 12 - 7 = 5 N (오른쪽)</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f1');
        const ctx = cv.getContext('2d');
        const cx = 280, cy = 75, bw = 60, bh = 40;
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color, text) {
            const headlen = 8;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 2.8;
            ctx.beginPath(); ctx.moveTo(fromx, fromy); ctx.lineTo(tox, toy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
            if (text) {
                ctx.font = 'bold 12px sans-serif';
                ctx.fillText(text, (fromx + tox)/2, fromy - 8);
            }
        }
        
        // 지면
        ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(40, cy + bh/2); ctx.lineTo(520, cy + bh/2); ctx.stroke();
        
        // 물체 상자
        ctx.fillStyle = '#f1f5f9'; ctx.strokeStyle = '#334155'; ctx.lineWidth = 2;
        ctx.fillRect(cx - bw/2, cy - bh/2, bw, bh);
        ctx.strokeRect(cx - bw/2, cy - bh/2, bw, bh);
        
        // 왼쪽 7N (길이 70px)
        drawArrow(ctx, cx - bw/2, cy, cx - bw/2 - 70, cy, '#dc2626', '7 N');
        // 오른쪽 12N (길이 120px)
        drawArrow(ctx, cx + bw/2, cy, cx + bw/2 + 120, cy, '#2563eb', '12 N');
        
        // 알짜힘 (초록, 상자 위)
        drawArrow(ctx, cx, cy - bh/2 - 15, cx + 50, cy - bh/2 - 15, '#16a34a', '알짜힘 5 N');
    })();
    </script>
    """
    components.html(html, height=220)

def render_sim_prob4():
    """문제 4: 동쪽 6N과 북쪽 8N의 2D 평행사변형법 벡터 합성 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 직교하는 두 힘의 평행사변형법 합성 (피타고라스 정리)</div>
        <canvas id="cv_f4" width="560" height="210" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#2563eb;">동쪽 Fx = 6 N</span>
            <span style="color:#dc2626;">북쪽 Fy = 8 N</span>
            <span style="color:#16a34a; font-weight:bold;">알짜힘 F = √(6²+8²) = 10 N (북동쪽 53°)</span>
            <span style="color:#7c3aed;">가속도 a = 5 m/s²</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f4');
        const ctx = cv.getContext('2d');
        const ox = 180, oy = 160;
        const scale = 14; // 1N당 14px
        const fx = 6 * scale; // 84
        const fy = 8 * scale; // 112
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color, text, width=2.5) {
            const headlen = 8;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width;
            ctx.beginPath(); ctx.moveTo(fromx, fromy); ctx.lineTo(tox, toy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
            if (text) {
                ctx.font = 'bold 11.5px sans-serif';
                ctx.fillText(text, (fromx + tox)/2 + (tox > fromx ? 6 : -14), (fromy + toy)/2 - 6);
            }
        }
        
        // 동쪽 6N
        drawArrow(ctx, ox, oy, ox + fx, oy, '#2563eb', '6 N (동쪽)');
        // 북쪽 8N
        drawArrow(ctx, ox, oy, ox, oy - fy, '#dc2626', '8 N (북쪽)');
        
        // 평행사변형 점선
        ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.5; ctx.setLineDash([3,3]);
        ctx.beginPath();
        ctx.moveTo(ox + fx, oy); ctx.lineTo(ox + fx, oy - fy);
        ctx.lineTo(ox, oy - fy);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // 알짜힘 대각선 10N
        drawArrow(ctx, ox, oy, ox + fx, oy - fy, '#16a34a', '합력 10 N', 3.2);
        
        // 각도 호
        ctx.strokeStyle = '#d97706'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(ox, oy, 30, -Math.atan2(8, 6), 0); ctx.stroke();
        ctx.fillStyle = '#b45309'; ctx.font = 'bold 11px sans-serif';
        ctx.fillText('θ ≈ 53°', ox + 36, oy - 14);
        
        // 원점 물체 (2kg)
        ctx.fillStyle = '#1e293b';
        ctx.beginPath(); ctx.arc(ox, oy, 7, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#475569'; ctx.font = '11px sans-serif';
        ctx.fillText('물체(2kg)', ox - 55, oy + 16);
    })();
    </script>
    """
    components.html(html, height=270)

def render_sim_prob5():
    """문제 5: 30도 비스듬한 10N 힘의 직교 성분 분해 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 비스듬한 힘(10N, 30°)의 수평·수직 성분 분해</div>
        <canvas id="cv_f5" width="560" height="190" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#2563eb;">수평 성분 Fx = 10 cos 30° = 5√3 N (8.66 N)</span>
            <span style="color:#dc2626;">수직 성분 Fy = 10 sin 30° = 5 N</span>
            <span style="color:#1e293b;">원래 힘 F = 10 N</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f5');
        const ctx = cv.getContext('2d');
        const ox = 120, oy = 140;
        const len = 160;
        const theta = Math.PI / 6; // 30도
        const fx = len * Math.cos(theta); // ~138.6
        const fy = len * Math.sin(theta); // 80
        
        function drawArrow(ctx, fromx, fromy, tox, toy, color, text, width=2.5) {
            const headlen = 8;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width;
            ctx.beginPath(); ctx.moveTo(fromx, fromy); ctx.lineTo(tox, toy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
            if (text) {
                ctx.font = 'bold 11.5px sans-serif';
                ctx.fillText(text, (fromx + tox)/2 + (tox > fromx ? 6 : -14), (fromy + toy)/2 - 6);
            }
        }
        
        // 수평 지면 기준선
        ctx.strokeStyle = '#94a3b8'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(ox, oy); ctx.lineTo(ox + fx + 50, oy); ctx.stroke();
        
        // 분해 직각 점선
        ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.5; ctx.setLineDash([3,3]);
        ctx.beginPath();
        ctx.moveTo(ox + fx, oy); ctx.lineTo(ox + fx, oy - fy);
        ctx.lineTo(ox, oy - fy);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // 수평 성분 Fx (파랑)
        drawArrow(ctx, ox, oy, ox + fx, oy, '#2563eb', 'Fx = 5√3 N (8.66 N)', 2.8);
        // 수직 성분 Fy (빨강)
        drawArrow(ctx, ox, oy, ox, oy - fy, '#dc2626', 'Fy = 5 N', 2.8);
        
        // 원래 힘 10N (검정 대각선)
        drawArrow(ctx, ox, oy, ox + fx, oy - fy, '#0f172a', 'F = 10 N', 3.2);
        
        // 각도 30도 호
        ctx.strokeStyle = '#d97706'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(ox, oy, 40, -theta, 0); ctx.stroke();
        ctx.fillStyle = '#b45309'; ctx.font = 'bold 11.5px sans-serif';
        ctx.fillText('30°', ox + 48, oy - 12);
        
        // 원점
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(ox, oy, 5, 0, Math.PI*2); ctx.fill();
    })();
    </script>
    """
    components.html(html, height=250)

def render_sim_prob6_8():
    """문제 6~8: 30도 빗면에서의 중력 분해(mg sinθ, mg cosθ) 및 마찰력 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 30° 빗면 위의 힘 분해 (중력, 수직항력, 마찰력)</div>
        <canvas id="cv_f6" width="560" height="230" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#0f172a;">중력 mg = 20 N</span>
            <span style="color:#2563eb;">빗면 나란한 성분 mg sin 30° = 10 N</span>
            <span style="color:#64748b;">수직항력 N = 10√3 N</span>
            <span style="color:#dc2626;">마찰력 f</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f6');
        const ctx = cv.getContext('2d');
        
        const ox = 80, oy = 180, L = 400, theta = Math.PI / 6; // 30도
        const bx = ox + L * Math.cos(theta);
        const by = oy - L * Math.sin(theta);
        
        // 빗면 바닥삼각형
        ctx.fillStyle = '#f8fafc'; ctx.strokeStyle = '#334155'; ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(ox, oy); ctx.lineTo(bx, by); ctx.lineTo(bx, oy); ctx.closePath();
        ctx.fill(); ctx.stroke();
        
        // 빗면 각도 호
        ctx.strokeStyle = '#d97706'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.arc(ox, oy, 35, -theta, 0); ctx.stroke();
        ctx.fillStyle = '#b45309'; ctx.font = 'bold 11px sans-serif';
        ctx.fillText('30°', ox + 42, oy - 10);
        
        // 상자 위치 (빗면 중간)
        const dBox = 200;
        const boxX = ox + dBox * Math.cos(theta);
        const boxY = oy - dBox * Math.sin(theta);
        
        ctx.save();
        ctx.translate(boxX, boxY);
        ctx.rotate(-theta);
        
        // 상자 본체 (회전계)
        ctx.fillStyle = '#e2e8f0'; ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 1.8;
        ctx.fillRect(-25, -35, 50, 35);
        ctx.strokeRect(-25, -35, 50, 35);
        ctx.fillStyle = '#1e293b'; ctx.font = 'bold 11px sans-serif';
        ctx.fillText('2 kg', -12, -18);
        
        // 상자 중심
        const cx = 0, cy = -17.5;
        ctx.restore();
        
        // 힘 벡터 그리기 (글로벌 좌표계)
        function drawArrow(ctx, fromx, fromy, tox, toy, color, text, width=2.2) {
            const headlen = 7;
            const angle = Math.atan2(toy - fromy, tox - fromx);
            ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = width;
            ctx.beginPath(); ctx.moveTo(fromx, fromy); ctx.lineTo(tox, toy); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(tox, toy);
            ctx.lineTo(tox - headlen * Math.cos(angle - Math.PI / 6), toy - headlen * Math.sin(angle - Math.PI / 6));
            ctx.lineTo(tox - headlen * Math.cos(angle + Math.PI / 6), toy - headlen * Math.sin(angle + Math.PI / 6));
            ctx.fill();
            if (text) {
                ctx.font = 'bold 10.5px sans-serif';
                ctx.fillText(text, (fromx + tox)/2 + 8, (fromy + toy)/2);
            }
        }
        
        const centerGx = boxX - 17.5 * Math.sin(theta);
        const centerGy = boxY - 17.5 * Math.cos(theta);
        
        // 1. 중력 연직 아래 (20N)
        drawArrow(ctx, centerGx, centerGy, centerGx, centerGy + 75, '#0f172a', '중력 mg = 20 N');
        
        // 2. 빗면 나란 성분 (아래쪽 10N)
        const parX = -Math.cos(theta) * 45;
        const parY = Math.sin(theta) * 45;
        drawArrow(ctx, centerGx, centerGy, centerGx + parX, centerGy + parY, '#2563eb', '10 N (mg sin 30°)');
        
        // 3. 수직항력 N (빗면 수직 위쪽)
        const perpX = -Math.sin(theta) * 55;
        const perpY = -Math.cos(theta) * 55;
        drawArrow(ctx, centerGx, centerGy, centerGx + perpX, centerGy + perpY, '#64748b', 'N = 10√3 N');
    })();
    </script>
    """
    components.html(html, height=290)

def render_sim_prob11():
    """문제 11: 빗면-연직 연결계 A, B 위치 교환 가속도 시뮬레이터 (가: 정지 -> 나: 가속도 2/3 g)"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 빗면 물체 A(3m), B(m) 위치 교환과 가속도 유도</div>
        <canvas id="cv_f11" width="560" height="190" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#2563eb;">(가) 정지 상태: 3mg sin θ = mg ⟹ sin θ = 1/3</span>
            <span style="color:#dc2626;">(나) 위치 교환: 알짜힘 F = 3mg - mg(1/3) = 8/3 mg</span>
            <span style="color:#16a34a; font-weight:bold;">가속도 a = (8/3 mg) / 4m = 2/3 g</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f11');
        const ctx = cv.getContext('2d');
        
        // (가) 정지 영역
        const ox1 = 40, oy1 = 150, L = 160;
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8;
        ctx.beginPath(); ctx.moveTo(ox1, oy1); ctx.lineTo(ox1 + L, oy1 - 65); ctx.lineTo(ox1 + L, oy1); ctx.closePath();
        ctx.stroke();
        ctx.font = 'bold 12px sans-serif'; ctx.fillStyle = '#1e293b';
        ctx.fillText('(가) 정지 (A: 3m 빗면, B: m 연직)', ox1 + 10, oy1 + 22);
        
        // (가) A 상자 (3m)
        ctx.fillStyle = '#bfdbfe'; ctx.strokeStyle = '#1d4ed8'; ctx.lineWidth = 1.5;
        ctx.fillRect(ox1 + 60, oy1 - 50, 32, 22); ctx.strokeRect(ox1 + 60, oy1 - 50, 32, 22);
        ctx.fillStyle = '#1e3a8a'; ctx.fillText('A(3m)', ox1 + 62, oy1 - 35);
        
        // (가) B 추 (m)
        ctx.fillStyle = '#fecdd3'; ctx.strokeStyle = '#e11d48';
        ctx.fillRect(ox1 + L + 6, oy1 - 25, 20, 20); ctx.strokeRect(ox1 + L + 6, oy1 - 25, 20, 20);
        ctx.fillStyle = '#881337'; ctx.fillText('B(m)', ox1 + L + 4, oy1 - 10);
        
        // (나) 가속 영역
        const ox2 = 320, oy2 = 150;
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 1.8;
        ctx.beginPath(); ctx.moveTo(ox2, oy2); ctx.lineTo(ox2 + L, oy2 - 65); ctx.lineTo(ox2 + L, oy2); ctx.closePath();
        ctx.stroke();
        ctx.fillStyle = '#1e293b';
        ctx.fillText('(나) 가속 (B: m 빗면, A: 3m 연직)', ox2 + 10, oy2 + 22);
        
        // (나) B 상자 (m)
        ctx.fillStyle = '#fecdd3'; ctx.strokeStyle = '#e11d48';
        ctx.fillRect(ox2 + 65, oy2 - 48, 24, 18); ctx.strokeRect(ox2 + 65, oy2 - 48, 24, 18);
        ctx.fillStyle = '#881337'; ctx.fillText('B(m)', ox2 + 66, oy2 - 35);
        
        // (나) A 추 (3m)
        ctx.fillStyle = '#bfdbfe'; ctx.strokeStyle = '#1d4ed8';
        ctx.fillRect(ox2 + L + 4, oy2 - 30, 26, 26); ctx.strokeRect(ox2 + L + 4, oy2 - 30, 26, 26);
        ctx.fillStyle = '#1e3a8a'; ctx.fillText('A(3m)', ox2 + L + 2, oy2 - 13);
    })();
    </script>
    """
    components.html(html, height=250)

def render_sim_prob12():
    """문제 12: 두 줄 p(30°), q(60°)로 매달린 물체의 힘의 평형 시뮬레이터"""
    html = """
    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:12px; max-width:600px; margin:0 auto; font-family:sans-serif;">
        <div style="font-size:13px; font-weight:bold; color:#1e293b; margin-bottom:8px;">🎬 [가상실험] 두 실(30°, 60°)의 장력 평형과 삼각비 분석</div>
        <canvas id="cv_f12" width="560" height="190" style="width:100%; border:1px solid #e2e8f0; border-radius:6px; background:#fafafa;"></canvas>
        <div style="display:flex; justify-content:space-around; font-size:11.5px; color:#334155; margin-top:6px; font-weight:600;">
            <span style="color:#2563eb;">수평 평형: Tp sin 30° = Tq sin 60°</span>
            <span style="color:#dc2626;">Tp (1/2) = Tq (√3/2)</span>
            <span style="color:#16a34a; font-weight:bold;">Tp / Tq = √3</span>
        </div>
    </div>
    <script>
    (function(){
        const cv = document.getElementById('cv_f12');
        const ctx = cv.getContext('2d');
        const ceilY = 30;
        const px = 280, py = 135;
        
        // 천장
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(120, ceilY); ctx.lineTo(440, ceilY); ctx.stroke();
        
        // 실 p: 연직각 30도 (좌측 상단으로 연결)
        const lenP = 120;
        const c1x = px - lenP * Math.sin(Math.PI/6); // px - 60 = 220
        const c1y = ceilY;
        
        // 실 q: 연직각 60도 (우측 상단으로 연결)
        const lenQ = 120 / Math.sqrt(3); // 약 69.3
        const c2x = px + lenQ * Math.sin(Math.PI/3); // px + 60 = 340
        const c2y = ceilY;
        
        // 연직 점선
        ctx.strokeStyle = '#cbd5e1'; ctx.lineWidth = 1.2; ctx.setLineDash([3,3]);
        ctx.beginPath(); ctx.moveTo(px, ceilY); ctx.lineTo(px, py + 35); ctx.stroke();
        ctx.setLineDash([]);
        
        // 실 p (파랑)
        ctx.strokeStyle = '#2563eb'; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(c1x, c1y); ctx.stroke();
        ctx.fillStyle = '#1d4ed8'; ctx.font = 'bold 12px sans-serif';
        ctx.fillText('실 p (Tp)', c1x - 45, (ceilY + py)/2);
        
        // 실 q (빨강)
        ctx.strokeStyle = '#dc2626'; ctx.lineWidth = 2.0;
        ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(c2x, c2y); ctx.stroke();
        ctx.fillStyle = '#b91c1c';
        ctx.fillText('실 q (Tq)', c2x + 10, (ceilY + py)/2);
        
        // 각도 표시
        ctx.strokeStyle = '#d97706'; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.arc(c1x, c1y, 25, Math.PI/2 - Math.PI/6, Math.PI/2); ctx.stroke();
        ctx.fillStyle = '#b45309'; ctx.font = '10.5px sans-serif'; ctx.fillText('30°', c1x + 8, c1y + 24);
        
        ctx.beginPath(); ctx.arc(c2x, c2y, 25, Math.PI/2, Math.PI/2 + Math.PI/3); ctx.stroke();
        ctx.fillText('60°', c2x - 28, c2y + 24);
        
        // 물체 m
        ctx.fillStyle = '#1e293b';
        ctx.beginPath(); ctx.arc(px, py, 10, 0, Math.PI*2); ctx.fill();
        ctx.fillStyle = '#ffffff'; ctx.font = 'bold 10px sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText('m', px, py);
    })();
    </script>
    """
    components.html(html, height=250)

# =========================================================================
# 문항 렌더링 루틴 (1~14번 문항)
# =========================================================================

show_p1 = (view_category in ["📄 1페이지: 힘의 기본 개념과 합성 (4문항)", "📖 전체 14문항 모두 보기", "📖 전체 14문항 모두 인쇄"])
show_p2 = (view_category in ["📄 2페이지: 힘의 성분 분해와 빗면 운동 (6문항)", "📖 전체 14문항 모두 보기", "📖 전체 14문항 모두 인쇄"])
show_p3 = (view_category in ["📄 3페이지: 심화 연결계와 도르래 운동 (4문항)", "📖 전체 14문항 모두 보기", "📖 전체 14문항 모두 인쇄"])

# ==================== [PAGE 1] ====================
if show_p1:
    st.markdown("### 📄 [과제 1페이지] 힘의 기본 개념과 합성")

    # ---------- [문제 1] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">[기초] 문제 1</span> &nbsp; <b>마찰 없는 수평면 위의 반대 방향 두 힘의 합성</b>
        <p style="margin-top:6px;">마찰이 없는 수평면 위의 물체에 오른쪽으로 12 N, 왼쪽으로 7 N의 힘이 동시에 작용한다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob1()

    if is_print_mode:
        st.markdown("**（1） 알짜힘의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 12 + 7 = 19 N으로 계산하면 안 되는 이유를 힘의 방향을 이용하여 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 1 정답 및 개념 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 알짜힘의 크기와 방향**:
              * 오른쪽 방향을 (+)로 두면:
                $$F_{net} = +12\\,\\text{N} + (-7\\,\\text{N}) = \\mathbf{+5\\,\\text{N}}$$
              * 따라서 알짜힘의 크기는 **$5\\,\\text{N}$**, 방향은 **오른쪽**입니다.
            * **(2) 12 + 7 = 19 N으로 계산하면 안 되는 이유**:
              * 힘은 크기뿐만 아니라 **방향을 갖는 벡터(Vector) 물리량**이기 때문입니다.
              * 작용하는 두 힘의 방향이 서로 정반대(180°)이므로 크기만을 더하는 스칼라 합이 아니라, 방향 부호를 고려한 **벡터 합($12 - 7 = 5\\,\\text{N}$)**으로 계산해야 합니다.
            """)

    st.divider()

    # ---------- [문제 2] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">[기초] 문제 2</span> &nbsp; <b>알짜힘이 0일 때의 운동 상태 (관성의 법칙)</b>
        <p style="margin-top:6px;">마찰이 없는 수평면에서 물체가 처음에 오른쪽으로 4 m/s의 속력으로 운동하고 있다. 이 물체에 작용하는 알짜힘의 크기가 0 N으로 유지된다.</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 5초 후 물체의 운동 상태를 판단하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 그 이유를 알짜힘, 가속도, 속도의 관계를 이용하여 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 2 정답 및 뉴턴 운동 법칙 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 5초 후 물체의 운동 상태**:
              * **오른쪽으로 $4\\,\\text{m/s}$의 일정한 속력으로 등속 직선 운동을 한다.**
            * **(2) 관계를 이용한 설명**:
              * 뉴턴 제2법칙($F_{net} = ma$)에 따라 물체에 작용하는 알짜힘 $F_{net} = 0\\,\\text{N}$이면 가속도 $a = 0\\,\\text{m/s}^2$입니다.
              * 가속도는 단위 시간당 속도의 변화량이므로, $a = 0$이면 속도의 크기와 방향이 전혀 변하지 않습니다.
              * 따라서 5초 후에도 처음 운동 상태 그대로 오른쪽 $4\\,\\text{m/s}$의 등속도 운동을 유지합니다.
            """)

    st.divider()

    # ---------- [문제 3] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">[기초] 문제 3</span> &nbsp; <b>마찰이 있는 면에서의 등속도 운동과 알짜힘</b>
        <p style="margin-top:6px;">마찰이 있는 수평면에서 물체가 처음에 오른쪽으로 4 m/s의 속력으로 운동하고 있다. 물체에는 오른쪽으로 2 N의 힘이 작용한다. 운동을 시작한 후 1초가 지났을 때 물체의 속력이 여전히 4 m/s이었다.</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 이 물체에 작용한 알짜힘의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 그렇게 판단한 이유를 알짜힘과 가속도의 관계를 이용하여 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 3 정답 및 마찰력 평형 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 알짜힘의 크기**: **$0\\,\\text{N}$**
            * **(2) 판단 근거**:
              * 1초 동안 물체의 속력이 $4\\,\\text{m/s}$로 일정하게 유지되었으므로 속도의 변화량 $\\Delta v = 0$이며, 가속도 $a = \\frac{\\Delta v}{\\Delta t} = 0\\,\\text{m/s}^2$입니다.
              * $F_{net} = ma$에 의해 가속도가 0이므로 물체에 작용하는 **알짜힘은 반드시 $0\\,\\text{N}$**이어야 합니다.
              * *(참고: 오른쪽 외력 $2\\,\\text{N}$과 운동을 방해하는 마찰력 $2\\,\\text{N}$이 힘의 평형을 이루고 있습니다.)*
            """)

    st.divider()

    # ---------- [문제 4] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">[보통] 문제 4</span> &nbsp; <b>직교하는 두 힘의 합성 (동쪽 6N, 북쪽 8N)</b>
        <p style="margin-top:6px;">질량이 2kg인 물체에 동쪽으로 6 N, 북쪽으로 8 N의 힘이 동시에 작용한다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob4()

    if is_print_mode:
        st.markdown("**（1） 물체에 작용하는 알짜힘의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체의 가속도의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 물체의 가속도 방향을 동쪽과 북쪽을 기준으로 말로 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 4 정답 및 피타고라스 벡터 합성 확인하기", expanded=False):
            st.markdown("""
            * **(1) 알짜힘의 크기**:
              * 두 힘이 $90^\\circ$를 이루므로 피타고라스 정리에 의해:
                $$F_{net} = \\sqrt{6^2 + 8^2} = \\sqrt{36 + 64} = \\sqrt{100} = \\mathbf{10\\,\\text{N}}$$
            * **(2) 가속도의 크기**:
              $$a = \\frac{F_{net}}{m} = \\frac{10\\,\\text{N}}{2\\,\\text{kg}} = \\mathbf{5\\,\\text{m/s}^2}$$
            * **(3) 가속도의 방향**:
              * 가속도의 방향은 알짜힘의 방향과 같습니다.
              * $\\tan\\theta = \\frac{F_y}{F_x} = \\frac{8}{6} = \\frac{4}{3} \\approx 1.33$
              * 따라서 **동쪽을 기준으로 북쪽으로 약 $53^\\circ$ 기울어진 방향** (북동쪽)입니다.
            """)

# ==================== [PAGE 2] ====================
if show_p2:
    st.markdown("### 📄 [과제 2페이지] 힘의 성분 분해와 빗면 운동")

    # ---------- [문제 5] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">[보통] 문제 5</span> &nbsp; <b>비슴듬한 힘(10N, 30°)의 직교 분해</b>
        <p style="margin-top:6px;">크기 10 N인 힘이 수평면에서 오른쪽 방향을 기준으로 위쪽으로 30° 기울어진 방향으로 작용하고 있다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob5()

    if is_print_mode:
        st.markdown("**（1） 이 힘의 수평 성분 Fx 와 수직 성분 Fy를 각각 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） Fx + Fy의 값이 원래 힘의 크기인 10 N과 같지 않은 이유를 벡터의 성분과 합성의 관점에서 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 5 정답 및 삼각비 분해 확인하기", expanded=False):
            st.markdown("""
            * **(1) 수평 및 수직 성분 크기**:
              * 수평 성분: $$F_x = 10\\cos 30^\\circ = 10 \\times \\frac{\\sqrt{3}}{2} = \\mathbf{5\\sqrt{3}\\,\\text{N}} \\approx 8.66\\,\\text{N}$$
              * 수직 성분: $$F_y = 10\\sin 30^\\circ = 10 \\times \\frac{1}{2} = \\mathbf{5\\,\\text{N}}$$
            * **(2) Fx + Fy ≠ 10 N 인 이유**:
              * $F_x$와 $F_y$는 서로 수직($90^\\circ$)인 방향을 가지므로 단순 대수적 합산(스칼라 합 $5\\sqrt{3} + 5 \\approx 13.66\\,\\text{N}$)을 할 수 없습니다.
              * 직각삼각형에서 빗변의 길이는 두 변의 합보다 작으며, 벡터 합성 공식 $F = \\sqrt{F_x^2 + F_y^2} = \\sqrt{(5\\sqrt{3})^2 + 5^2} = \\sqrt{75 + 25} = 10\\,\\text{N}$으로 합성되기 때문입니다.
            """)

    st.divider()

    # ---------- [문제 6] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">[보통] 문제 6</span> &nbsp; <b>마찰 없는 30° 빗면 위의 물체 가속도</b>
        <p style="margin-top:6px;">질량이 2 kg인 물체를 마찰이 없는 30° 빗면 위에 가만히 놓았다. (중력가속도는 10 m/s²로 한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob6_8()

    if is_print_mode:
        st.markdown("**（1） 중력의 빗면에 나란한 성분의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체의 가속도의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 물체에 작용하는 중력의 크기는 20 N인데 가속도의 크기가 10 m/s²가 아닌 이유를 알짜힘의 관점에서 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 6 정답 및 빗면 수직항력 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 중력의 빗면 나란한 성분**:
              $$F_\\parallel = mg\\sin 30^\\circ = 2\\,\\text{kg} \\times 10\\,\\text{m/s}^2 \\times \\frac{1}{2} = \\mathbf{10\\,\\text{N}}$$
            * **(2) 물체의 가속도**:
              * 마찰이 없으므로 알짜힘 $F_{net} = 10\\,\\text{N}$ (빗면 아래 방향)
              * 크기: $a = \\frac{10\\,\\text{N}}{2\\,\\text{kg}} = \\mathbf{5\\,\\text{m/s}^2}$
              * 방향: **빗면 아래쪽 방향**
            * **(3) 가속도가 10 m/s²가 아닌 이유**:
              * 물체에는 중력($20\\,\\text{N}$) 외에도 빗면이 물체를 수직으로 떠받치는 **수직항력($N = mg\\cos 30^\\circ = 10\\sqrt{3}\\,\\text{N}$)**이 작용합니다.
              * 중력의 빗면 수직 성분과 수직항력이 상쇄되어 빗면 수직 방향으로는 가속되지 않고, 오직 빗면에 나란한 분력($mg\\sin 30^\\circ = 10\\,\\text{N}$)만이 알짜힘으로 작용하므로 가속도는 $g$가 아니라 $g\\sin 30^\\circ = 5\\,\\text{m/s}^2$가 됩니다.
            """)

    st.divider()

    # ---------- [문제 7] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">[심화] 문제 7</span> &nbsp; <b>마찰이 있어 정지해 있는 30° 빗면 물체 (정지 마찰력)</b>
        <p style="margin-top:6px;">질량이 2kg인 물체를 마찰이 있는 30° 빗면 위에 가만히 놓았다. 물체가 계속 정지해 있다. (중력가속도는 10 m/s²로 한다.)</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 중력의 빗면에 나란한 성분의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체에 작용하는 알짜힘의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 물체에 작용하는 중력의 크기는 20 N인데, 알짜힘이 20 N이 아닌 이유를 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 7 정답 및 정지 마찰 평형 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 중력의 빗면 나란한 성분**:
              $$F_\\parallel = mg\\sin 30^\\circ = 2 \\times 10 \\times \\frac{1}{2} = \\mathbf{10\\,\\text{N}}$$
            * **(2) 알짜힘의 크기와 방향**:
              * 물체가 계속 정지해 있으므로 가속도 $a = 0$이며, 알짜힘은 **$0\\,\\text{N}$** (방향 없음)입니다.
            * **(3) 알짜힘이 20 N이 아닌 이유**:
              * 중력($20\\,\\text{N}$) 외에 빗면이 물체에 작용하는 **수직항력($10\\sqrt{3}\\,\\text{N}$)**과 빗면 위쪽 방향의 **정지 마찰력($10\\,\\text{N}$)**이 함께 작용하여 세 힘의 벡터 합이 정확히 상쇄($F_{net} = 0$)되기 때문입니다.
            """)

    st.divider()

    # ---------- [문제 8] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">[심화] 문제 8</span> &nbsp; <b>마찰력 6N이 작용하는 30° 빗면 물체의 가속도</b>
        <p style="margin-top:6px;">질량이 2 kg인 물체를 마찰이 있는 30° 빗면 위에 놓았다. 물체에 작용하는 마찰력의 크기는 6 N이며, 방향은 빗면 위쪽이다. (중력가속도는 10 m/s²로 한다.)</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 중력의 빗면에 나란한 성분의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체에 작용하는 알짜힘의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 물체의 가속도의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 8 정답 및 운동 마찰력 계산 확인하기", expanded=False):
            st.markdown("""
            * **(1) 중력의 빗면 나란 성분**:
              $$F_\\parallel = mg\\sin 30^\\circ = 2 \\times 10 \\times \\frac{1}{2} = \\mathbf{10\\,\\text{N}}$$ (빗면 아래쪽 방향)
            * **(2) 알짜힘의 크기와 방향**:
              $$F_{net} = F_\\parallel - f = 10\\,\\text{N} - 6\\,\\text{N} = \\mathbf{4\\,\\text{N}}, \\quad \\text{방향: 빗면 아래쪽}$$
            * **(3) 물체의 가속도 크기와 방향**:
              $$a = \\frac{F_{net}}{m} = \\frac{4\\,\\text{N}}{2\\,\\text{kg}} = \\mathbf{2\\,\\text{m/s}^2}, \\quad \\text{방향: 빗면 아래쪽}$$
            """)

    st.divider()

    # ---------- [문제 9] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">[심화] 문제 9</span> &nbsp; <b>운동 방향과 반대인 알짜힘과 물체의 운동 변화</b>
        <p style="margin-top:6px;">어떤 물체가 오른쪽으로 운동하고 있는 순간, 물체에 작용하는 알짜힘의 방향은 왼쪽이다.</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 이 순간 물체의 가속도 방향을 말하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 직후 물체의 속력은 증가하는지 감소하는지 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 왼쪽 방향의 알짜힘이 계속 작용한다면 충분한 시간이 지난 후 물체의 운동 방향은 어떻게 되는지 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 9 정답 및 속도 반전 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 가속도 방향**: **왼쪽 방향** (가속도의 방향은 항상 알짜힘의 방향과 일치합니다.)
            * **(2) 속력의 변화**: **감소한다.** 운동 방향(오른쪽)과 가속도 방향(왼쪽)이 반대이므로 속력이 점점 줄어듭니다.
            * **(3) 충분한 시간이 지난 후 운동 방향**: 속력이 줄어들어 순간 정지($v=0$)한 후, 알짜힘의 방향인 **왼쪽 방향으로 운동 방향이 바뀌어 속력이 점점 증가**합니다.
            """)

    st.divider()

    # ---------- [문제 10] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">[심화] 문제 10</span> &nbsp; <b>속도 변화와 알짜힘 및 개별 힘의 판별</b>
        <p style="margin-top:6px;">질량이 4kg인 물체의 속도가 1s 간격으로 2 m/s → 4 m/s → 6 m/s로 변하였다.</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**（1） 물체의 가속도의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（2） 물체에 작용한 알짜힘의 크기와 방향을 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**（3） 위 정보만으로 물체에 작용하는 각각의 힘을 모두 알 수 있는지 판단하고, 그 이유를 설명하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 10 정답 및 알짜힘의 본질 해설 확인하기", expanded=False):
            st.markdown("""
            * **(1) 가속도의 크기와 방향**:
              $$a = \\frac{\\Delta v}{\\Delta t} = \\frac{4 - 2}{1} = \\mathbf{2\\,\\text{m/s}^2}, \\quad \\text{방향: 운동 방향}$$
            * **(2) 알짜힘의 크기와 방향**:
              $$F_{net} = ma = 4\\,\\text{kg} \\times 2\\,\\text{m/s}^2 = \\mathbf{8\\,\\text{N}}, \\quad \\text{방향: 운동 방향(가속도 방향)}$$
            * **(3) 각각의 힘을 모두 알 수 있는지 여부**:
              * **알 수 없다.** 가속도와 질량 정보를 통해 구할 수 있는 것은 물체에 작용하는 모든 외력들의 벡터 합인 **'알짜힘(8 N)'뿐**입니다. 하나의 8 N 힘이 작용하는지, 10 N과 반대 2 N이 작용하는지, 수직 방향 힘들이 상쇄되고 있는지 등 개별 힘들의 구성은 알 수 없습니다.
            """)

# ==================== [PAGE 3] ====================
if show_p3:
    st.markdown("### 📄 [과제 3페이지] 심화 연결계와 도르래 운동")

    # ---------- [문제 11] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-primary">[심화] 문제 11</span> &nbsp; <b>빗면-도르래 연결 물체 A, B의 위치 교환과 가속도</b>
        <p style="margin-top:6px;">그림 (가)는 빗면에 놓인 물체 A가 물체 B와 실로 연결되어 정지해 있는 모습을, (나)는 (가)에서 A와 B의 위치를 바꾸었더니 A와 B가 등가속도 운동을 하는 모습을 나타낸 것이다. 질량은 A가 B의 3배이다. (나)에서 A의 가속도의 크기를 구하시오. (단, 중력 가속도는 g이고, 실의 질량, 모든 마찰과 공기 저항은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob11()

    if is_print_mode:
        st.markdown("**（나）에서 A의 가속도의 크기를 풀이 과정과 함께 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 11 정답 및 단계별 유도 풀이 확인하기", expanded=False):
            st.markdown("""
            * **질량 설정**: B의 질량을 $m$이라 하면, A의 질량은 $3m$입니다.
            * **1단계: (가)의 정지 조건으로부터 빗면 각도 $\\theta$ 산출**:
              * (가)에서 물체 B(질량 $m$)는 연직으로 매달려 있으므로 실의 장력 $T = mg$입니다.
              * 물체 A(질량 $3m$)는 빗면에서 정지해 있으므로:
                $$3mg \\sin\\theta = T = mg \\implies \\sin\\theta = \\mathbf{\\frac{1}{3}}$$
            * **2단계: (나)에서 계의 알짜힘 산출**:
              * 위치를 바꾸면 A(질량 $3m$)가 연직 매달리고, B(질량 $m$)가 빗면에 놓입니다.
              * A를 아래로 당기는 중력: $3mg$
              * B의 빗면 나란 성분: $mg\\sin\\theta = mg \\left(\\frac{1}{3}\\right) = \\frac{1}{3}mg$
              * 전체 계의 알짜힘:
                $$F_{net} = 3mg - \\frac{1}{3}mg = \\mathbf{\\frac{8}{3}mg}$$
            * **3단계: 가속도 계산**:
              * 계 전체 질량 $M = 3m + m = 4m$
              $$a = \\frac{F_{net}}{M} = \\frac{\\frac{8}{3}mg}{4m} = \\mathbf{\\frac{2}{3}g}$$
            """)

    st.divider()

    # ---------- [문제 12] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-success">[심화] 문제 12</span> &nbsp; <b>두 실 p, q로 천장에 매달린 물체의 힘의 평형</b>
        <p style="margin-top:6px;">그림은 질량이 m인 물체를 실 p, q로 천장에 연결했을 때, 물체가 정지해 있는 모습을 나타낸 것이다. p, q가 연직 방향에 대해 이루는 각은 각각 30°, 60°이다. p, q가 물체를 당기는 힘의 크기를 각각 Tp, Tq라고 할 때, Tp / Tq 는?</p>
    </div>
    """, unsafe_allow_html=True)
    
    render_sim_prob12()

    if is_print_mode:
        st.markdown("**Tp / Tq 의 값을 풀이 과정과 함께 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 12 정답 및 삼각함수 평형 유도 확인하기", expanded=False):
            st.markdown("""
            * **수평 방향 힘의 평형**:
              * 물체가 정지해 있으므로 수평 방향 알짜힘은 0입니다.
              $$T_p \\sin 30^\\circ = T_q \\sin 60^\\circ$$
            * **삼각비 대입**:
              $$T_p \\times \\frac{1}{2} = T_q \\times \\frac{\\sqrt{3}}{2}$$
            * **장력 비 산출**:
              $$T_p = \\sqrt{3} T_q \\implies \\mathbf{\\frac{T_p}{T_q} = \\sqrt{3}}$$
            """)

    st.divider()

    # ---------- [문제 13] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-purple">[심화] 문제 13</span> &nbsp; <b>양쪽 빗면 연결 물체 A(3m), B(m)와 실 끊기 전후 가속도 2배</b>
        <p style="margin-top:6px;">그림은 실로 연결된 물체 A, B가 경사각이 각각 60°, 30°인 빗면 p, q에서 속력이 증가하는 등가속도 운동을 하는 모습을 나타낸 것이다. A는 p를 내려가는 동안 크기 f인 마찰력을 받는다. A, B의 질량은 각각 3m, m이다. 이 때 실을 끊으면 A의 가속도 크기는 실을 끊기 전의 2배가 된다. f는? (단, 중력 가속도는 g이고, 공기 저항과 p에서 마찰 외의 모든 마찰은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)

    if is_print_mode:
        st.markdown("**1. A와 B를 하나의 계로 보았을 때, 계에 작용하는 알짜힘을 m, g, f를 사용하여 표현하시오. (A가 내려가는 방향을 +로 가정)**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2. 1에서 구한 알짜힘과 뉴턴 제 2법칙을 이용하여, 실을 끊기 전 계의 가속도 a를 표현하는 식을 세우시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3. 실이 끊어진 직후, 물체 A에 작용하는 알짜힘과 A의 질량을 이용하여, 실을 끊은 후 A의 가속도를 표현하는 식을 세우시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**4. 2에서 구한 가속도와 3에서 구한 가속도 식을 조건에 맞게 대입하여 마찰력 f를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 13 정답 및 4단계 체계적 유도 확인하기", expanded=False):
            st.markdown("""
            * **1. 실 끊기 전 계의 알짜힘**:
              * A의 빗면 중력 성분: $3mg\\sin 60^\\circ = \\frac{3\\sqrt{3}}{2}mg$
              * B의 빗면 중력 성분: $mg\\sin 30^\\circ = \\frac{1}{2}mg$
              * A의 마찰력: 운동 반대 방향 $f$
              $$F_{net,1} = \\mathbf{\\left(\\frac{3\\sqrt{3}-1}{2}\\right)mg - f}$$
            * **2. 실 끊기 전 계의 가속도 $a_1$**:
              * 전체 질량 $3m + m = 4m$
              $$a_1 = \\mathbf{\\frac{\\left(\\frac{3\\sqrt{3}-1}{2}\\right)mg - f}{4m}}$$
            * **3. 실 끊은 후 A의 가속도 $a_2$**:
              * 실이 끊어지면 A(질량 $3m$)는 자신의 중력 성분과 마찰력만 받음:
              $$F_{net,A} = \\frac{3\\sqrt{3}}{2}mg - f \\implies a_2 = \\mathbf{\\frac{\\frac{3\\sqrt{3}}{2}mg - f}{3m}}$$
            * **4. 마찰력 $f$ 계산 ($a_2 = 2 a_1$)**:
              $$\\frac{\\frac{3\\sqrt{3}}{2}mg - f}{3m} = 2 \\times \\frac{\\left(\\frac{3\\sqrt{3}-1}{2}\\right)mg - f}{4m} = \\frac{\\left(\\frac{3\\sqrt{3}-1}{2}\\right)mg - f}{2m}$$
              * 양변에 $6m$을 곱하여 정리:
                $$2\\left(\\frac{3\\sqrt{3}}{2}mg - f\\right) = 3\\left(\\frac{3\\sqrt{3}-1}{2}mg - f\\right)$$
                $$3\\sqrt{3}mg - 2f = \\frac{9\\sqrt{3}-3}{2}mg - 3f$$
                $$f = \\frac{9\\sqrt{3}-3 - 6\\sqrt{3}}{2}mg = \\mathbf{\\frac{3(\\sqrt{3}-1)}{2}mg}$$
            """)

    st.divider()

    # ---------- [문제 14] ----------
    st.markdown("""
    <div class="exam-box">
        <span class="badge-amber">[심화] 문제 14</span> &nbsp; <b>수평면 A, 빗면 B, 연직 C 3체 연결계와 실 p, q 절단 실험</b>
        <p style="margin-top:6px;">그림은 수평면 위의 물체 A가 물체 B, C에 실 p, q로 연결되어 정지해 있는 모습을 나타낸 것이다. A, B, C의 질량은 각각 m, 3m, 2m이다. 표는 A가 수평면에 정지한 상태에서 p 또는 q만 끊었을 때, A의 가속도 크기를 나타낸 것이다. (단, 중력 가속도는 g이고, 실의 질량, 공기 저항과 모든 마찰은 무시한다.)</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    | 끊은 실 | A의 가속도 크기 |
    | :---: | :---: |
    | **p만 끊음** | $a_1$ |
    | **q만 끊음** | $a_2$ |
    """)

    if is_print_mode:
        st.markdown("**1. 빗면이 B에 작용하는 힘(수직항력)의 크기를 쓰시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**2. a₁과 a₂의 비를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
        st.markdown("**3. p만 끊었을 때 q가 C를 당기는 힘의 크기를 구하시오.**")
        st.markdown('<div class="answer-space"></div>', unsafe_allow_html=True)
    else:
        with st.expander("💡 문제 14 정답 및 3체 역학 유도 확인하기", expanded=False):
            st.markdown("""
            * **정지 상태 힘의 평형을 통한 빗면각 $\\theta$ 산출**:
              * C(질량 $2m$)가 당기는 장력: $T_q = 2mg$
              * B(질량 $3m$)가 빗면으로 당기는 장력: $T_p = 3mg\\sin\\theta$
              * A가 정지해 있으므로 $T_p = T_q \\implies 3mg\\sin\\theta = 2mg \\implies \\mathbf{\\sin\\theta = \\frac{2}{3}}$
              * 따라서 $\\cos\\theta = \\sqrt{1 - (2/3)^2} = \\frac{\\sqrt{5}}{3}$
            * **1. 빗면이 B에 작용하는 힘(수직항력 $N$)**:
              $$N = m_B g \\cos\\theta = 3m g \\times \\frac{\\sqrt{5}}{3} = \\mathbf{\\sqrt{5}mg}$$
            * **2. $a_1$과 $a_2$의 비**:
              * **p만 끊었을 때 ($a_1$)**: A($m$)와 C($2m$)가 가속:
                $$a_1 = \\frac{m_C g}{m_A + m_C} = \\frac{2mg}{m + 2m} = \\mathbf{\\frac{2}{3}g}$$
              * **q만 끊었을 때 ($a_2$)**: A($m$)와 B($3m$)가 가속:
                $$a_2 = \\frac{m_B g \\sin\\theta}{m_A + m_B} = \\frac{3mg(2/3)}{m + 3m} = \\frac{2mg}{4m} = \\mathbf{\\frac{1}{2}g}$$
              * 가속도 비:
                $$\\mathbf{a_1 : a_2 = \\frac{2}{3} : \\frac{1}{2} = 4 : 3} \\quad \\left(\\frac{a_1}{a_2} = \\frac{4}{3}\\right)$$
            * **3. p만 끊었을 때 q가 C를 당기는 힘 (장력 $T_q'$)**:
              * A의 운동방정식 적용:
                $$T_q' = m_A a_1 = m \\times \\frac{2}{3}g = \\mathbf{\\frac{2}{3}mg}$$
            """)
