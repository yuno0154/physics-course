import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import os

# 페이지 설정
st.set_page_config(page_title="인공중력 물리 탐구 프리미엄", layout="wide")

# ── 사이드바 제어판 ──
st.sidebar.title("🚀 MISSION CONTROL")
st.sidebar.markdown("---")

obs_mode = st.sidebar.radio(
    "🔭 시점(Frame) 선택",
    ["외부 원경 (Global View)", "관성계 (Inertial Frame)", "비관성계 (Rotating Frame)"]
)

st.sidebar.markdown("---")
# 슬라이더 - 물리량 제어
radius_val = st.sidebar.slider("정거장 반지름 (r) [m]", 100, 1000, 500, step=50)
omega_val = st.sidebar.slider("회전 각속도 (ω) [rad/s]", 0.05, 0.40, 0.15, step=0.01)

# 물리 계산
accel = radius_val * (omega_val ** 2)
g_force = accel / 9.8

st.sidebar.info(f"""
**[실시간 물리 데이터]**
- 가속도: {accel:.2f} m/s²
- 체감 중력: {g_force:.2f} G
""")

# ── 메인 화면 ──
st.title("🛡️ 인공중력 우주 정거장: 관성계 vs 비관성계 탐구")
st.markdown(f"현재 관찰 상태: **{obs_mode}**")

# 이미지 경로 설정
base_path = "physics_sim/" if os.path.exists("physics_sim/cooper_exterior.png") else ""

# 시뮬레이션 HUD 및 캔버스
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;800&family=Pretendard:wght@400;700;900&display=swap');
        body {{ margin: 0; background: #010409; overflow: hidden; font-family: 'Pretendard', sans-serif; }}
        canvas {{ display: block; }}
        
        #dashboard {{
            position: absolute; top: 20px; right: 20px;
            width: 260px; color: #38bdf8; background: rgba(15, 23, 42, 0.85);
            padding: 20px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);
            pointer-events: none; backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        }}
        .label {{ color: #64748b; font-size: 10px; font-weight: 800; letter-spacing: 1px; margin-bottom: 2px; }}
        .value {{ color: #f8fafc; font-size: 18px; font-weight: 900; font-family: 'JetBrains Mono'; margin-bottom: 12px; }}
        .metric {{ display: flex; align-items: baseline; gap: 5px; }}
        .unit {{ font-size: 12px; color: #475569; }}
    </style>
</head>
<body>
    <div id="dashboard">
        <div style="font-weight:900; margin-bottom:15px; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:8px; color:#38bdf8; font-size:11px;">📡 HUB TELEMETRY</div>
        <div class="label">RADIUS</div><div class="value metric">{radius_val}<span class="unit">m</span></div>
        <div class="label">ANGULAR VELOCITY</div><div class="value metric">{omega_val}<span class="unit">rad/s</span></div>
        <div style="margin-top:10px; padding:10px; background:rgba(245,158,11,0.1); border-radius:10px; border:1px solid rgba(245,158,11,0.2);">
            <div class="label" style="color:#f59e0b;">SIMULATED GRAVITY</div>
            <div style="font-size:22px; font-weight:900; color:#facc15;">{accel:.2f} <span style="font-size:12px;">m/s²</span></div>
            <div style="font-size:14px; font-weight:800; color:#f59e0b;">({g_force:.2f} G)</div>
        </div>
    </div>
    <canvas id="simCanvas"></canvas>

<script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    const radius = {radius_val};
    const omega = {omega_val};
    let angle = 0;
    let earthAngle = 0;

    function resize() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
    window.onresize = resize; resize();

    // 배경 스타 필드
    const stars = [];
    for (let i = 0; i < 400; i++) {{
        stars.push({{
            x: (Math.random() - 0.5) * canvas.width * 2.5,
            y: (Math.random() - 0.5) * canvas.height * 2.5,
            size: Math.random() * 1.8,
            opacity: Math.random() * 0.7 + 0.3,
            phase: Math.random() * Math.PI * 2
        }});
    }}

    function drawSpace(cx, cy, rot) {{
        const now = Date.now() * 0.001;
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
        ctx.fillStyle = '#010409'; ctx.fillRect(-canvas.width * 2, -canvas.height * 2, canvas.width * 4, canvas.height * 4);
        stars.forEach(s => {{
            const glow = 0.5 + 0.5 * Math.sin(now + s.phase);
            ctx.fillStyle = `rgba(255, 255, 255, ${{s.opacity * (0.7 + 0.3 * glow)}})`;
            ctx.beginPath(); ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2); ctx.fill();
        }});
        ctx.restore();
    }}

    function drawEarth(cx, cy, scale, rot) {{
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
        const er = 220 * scale;
        const ex = -canvas.width * 0.35, ey = -canvas.height * 0.38;
        ctx.translate(ex, ey);
        // Atmosphere
        const glow = ctx.createRadialGradient(0, 0, er, 0, 0, er * 1.3);
        glow.addColorStop(0, 'rgba(56, 189, 248, 0.15)'); glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(0, 0, er * 1.3, 0, Math.PI * 2); ctx.fill();
        // Body
        const grad = ctx.createRadialGradient(-er*0.3, -er*0.3, er*0.1, 0, 0, er);
        grad.addColorStop(0, '#3b82f6'); grad.addColorStop(0.6, '#1d4ed8'); grad.addColorStop(1, '#0e1b3d');
        ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(0, 0, er, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    }}

    function drawStation(cx, cy, rot, scale, isDetail) {{
        const visualR = 210 * scale;
        const tubeW = 44 * scale;
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
        
        // 1. Spokes (6 EA)
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 12 * scale;
        for (let i = 0; i < 6; i++) {{
            const a = (i / 6) * Math.PI * 2;
            ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * visualR, Math.sin(a) * visualR); ctx.stroke();
        }}
        // 2. Hub
        const hr = 50 * scale;
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#64748b'; ctx.lineWidth = 3 * scale; ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.stroke();
        
        // 3. Torus Ring
        ctx.strokeStyle = '#0f172a'; ctx.lineWidth = tubeW * 1.1; ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        ctx.strokeStyle = '#475569'; ctx.lineWidth = tubeW * 0.7; ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        
        if (isDetail) {{
            // Windows and Lights details
            ctx.strokeStyle = 'rgba(186,230,253,0.4)'; ctx.lineWidth = 4 * scale;
            for (let i = 0; i < 36; i++) {{
                const a = (i / 36) * Math.PI * 2;
                ctx.beginPath(); ctx.arc(0, 0, visualR, a, a + 0.08); ctx.stroke();
            }}
        }}
        ctx.restore();
    }}

    function drawArrow(x, y, len, ang, color, label) {{
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 4;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-15, -6); ctx.lineTo(len-15, 6); ctx.closePath(); ctx.fill();
        ctx.rotate(-ang); ctx.font = '900 13px Pretendard'; ctx.fillStyle = color;
        ctx.shadowBlur = 5; ctx.shadowColor = 'black'; ctx.fillText(label, 20, -12);
        ctx.restore();
    }}

    function renderGlobal(cx, cy) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawStation(cx, cy, angle, scale, true);
        ctx.fillStyle = '#38bdf8'; ctx.font = '900 18px JetBrains Mono';
        ctx.fillText('GLOBAL CINEMATIC VIEW', 30, 50);
        ctx.fillStyle = 'rgba(148,163,184,0.6)'; ctx.font = '500 13px JetBrains Mono';
        ctx.fillText('External Observer | Fixed Stars', 30, 75);
    }}

    function renderInertial(cx, cy, accel) {{
        const scale = (Math.min(canvas.width, canvas.height) / 580) * 1.1;
        const visualR = 210 * scale;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawStation(cx, cy, angle, scale, false);
        
        // 우주인 (회전 중)
        const ax = cx + Math.cos(angle) * visualR;
        const ay = cy + Math.sin(angle) * visualR;
        
        // 우주인 본체
        ctx.save(); ctx.translate(ax, ay); ctx.rotate(angle - Math.PI/2);
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.roundRect(-8*scale, -16*scale, 16*scale, 24*scale, 5*scale); ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(-6*scale, -14*scale, 12*scale, 7*scale, 3*scale); ctx.fill();
        ctx.restore();

        // 수직항력 (구심력)
        const arrowLen = Math.min(150, accel * 10) * scale;
        drawArrow(ax, ay, arrowLen, angle + Math.PI, '#ef4444', 'N (Normal Force)');
        
        ctx.fillStyle = '#ef4444'; ctx.font = '900 18px JetBrains Mono';
        ctx.fillText('INERTIAL VIEW', 30, 50);
        ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.font = '700 14px Pretendard';
        ctx.fillText('관성계: 바닥이 우주인을 안으로 미는 수직항력이 "구심력" 역할을 하여 원운동 발생', 30, 80);
    }}

    function renderRotating(cx, cy, accel) {{
        // 시점 확대 (내부 시뮬레이션 느낌)
        const scale = (Math.min(canvas.width, canvas.height) / 580) * 1.6;
        const visualR = 210 * scale;
        
        // 1. 외부 배경이 거꾸로 회전함 (핵심 요청)
        drawSpace(cx, cy, -angle);
        drawEarth(cx, cy, scale, -angle + earthAngle);
        
        // 2. 정거장은 멈춰있음 (핵심 요청)
        drawStation(cx, cy, 0, scale, true);
        
        // 3. 우주인도 정지 상태 (3시 방향 고정)
        const ax = cx + visualR;
        const ay = cy;
        
        ctx.save(); ctx.translate(ax, ay); ctx.rotate(-Math.PI/2);
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.roundRect(-8*scale, -16*scale, 16*scale, 24*scale, 5*scale); ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(-6*scale, -14*scale, 12*scale, 7*scale, 3*scale); ctx.fill();
        ctx.restore();

        // 4. 원심력(Inertial Force)과 수직항력 표시 (핵심 요청)
        const arrowLen = Math.min(150, accel * 10) * scale;
        drawArrow(ax, ay, arrowLen, 0, '#10b981', 'Inertial Force (가성력-원심력)');
        drawArrow(ax, ay, arrowLen * 0.9, Math.PI, '#ef4444', 'Normal Force (수직항력)');
        
        ctx.fillStyle = '#10b981'; ctx.font = '900 18px JetBrains Mono';
        ctx.fillText('NON-INERTIAL VIEW', 30, 50);
        ctx.fillStyle = 'rgba(255,255,255,0.7)'; ctx.font = '700 14px Pretendard';
        ctx.fillText('비관성계: 정거장은 정지, 배경이 역회전. 바깥으로 쏠리는 "원심력"과 수직항력이 평형', 30, 80);
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2, cy = canvas.height / 2;
        earthAngle += 0.0003; angle += omega * 0.016;
        const mode = "{obs_mode}";
        if (mode === "외부 원경 (Global View)") renderGlobal(cx, cy);
        else if (mode === "관성계 (Inertial Frame)") renderInertial(cx, cy, {accel});
        else renderRotating(cx, cy, {accel});
        requestAnimationFrame(render);
    }}
    render();
</script>
</body>
</html>
"""

components.html(html_content, height=680, scrolling=False)

# ── 탐구 섹션 및 콘텐츠 복원 ──
st.markdown("---")
st.markdown("### 🔍 회전하는 우주 정거장 속의 물리 탐구")

# 비교 분석 테이블
st.markdown("""
<style>
    .physics-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
    .physics-table th { background: #0f172a; color: white; padding: 18px; font-weight: 800; border: 1px solid #1e293b; font-size: 15px; }
    .physics-table td { background: white; padding: 18px; border: 1px solid #e2e8f0; text-align: center; font-size: 14px; }
    .label-cell { background: #f8fafc !important; font-weight: 800; color: #475569; width: 20%; }
    .highlight-blue { color: #3b82f6; font-weight: 700; }
    .highlight-red { color: #ef4444; font-weight: 700; }
    .highlight-green { color: #10b981; font-weight: 700; }
</style>
<table class="physics-table">
    <thead>
        <tr>
            <th>분석 항목</th>
            <th>🌍 외부 관찰자 (관성계)</th>
            <th>👩‍🚀 내부 우주인 (비관성계)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="label-cell">우주인의 운동</td>
            <td class="highlight-blue">등속 원운동 진행</td>
            <td>관찰자와 함께 <b>정지</b>한 상태</td>
        </tr>
        <tr>
            <td class="label-cell">작용하는 힘</td>
            <td class="highlight-red">수직항력 (N)</td>
            <td><span class="highlight-red">수직항력(N)</span> + <span class="highlight-green">원심력 (Inertial Force)</span></td>
        </tr>
        <tr>
            <td class="label-cell">운동의 해석</td>
            <td>수직항력이 <b>구심력</b>이 되어 원운동 유발</td>
            <td>수직항력과 원심력이 <b>평형</b>을 이룸</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# 쿠퍼 스테이션 이미지 복원
col_img1, col_img2 = st.columns(2)
with col_img1:
    st.subheader("🪐 Station Exterior View")
    img_ext = base_path + "cooper_exterior.png"
    if os.path.exists(img_ext):
        st.image(img_ext, caption="인터스텔라: 토성의 고리 근처에서 회전하는 쿠퍼 스테이션", use_container_width=True)
    else:
        st.warning("이미지(Exterior)를 찾을 수 없습니다.")

with col_img2:
    st.subheader("🏡 Station Interior View")
    img_int = base_path + "cooper_interior.png"
    if os.path.exists(img_int):
        st.image(img_int, caption="인터스텔라: 원심력에 의해 지표면이 굽어 보이는 내부 거주 구역", use_container_width=True)
    else:
        st.warning("이미지(Interior)를 찾을 수 없습니다.")

st.markdown("---")
st.info("💡 **실험 팁**: 관성계에서는 'N' 하나의 화살표가 원운동을 만드는 것을 확인하고, 비관성계에서는 'N'과 '원심력' 두 화살표가 팽팽하게 맞서 우주인을 정지시키는 모습을 비교해 보세요.")
st.video("https://youtu.be/TzKvVb6j2Zo")

def show():
    pass

if __name__ == "__main__":
    show()
