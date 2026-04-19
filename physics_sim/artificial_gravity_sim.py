import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import os

st.set_page_config(page_title="인공중력 시뮬레이션", layout="wide")

# ── 사이드바 설정 ──
st.sidebar.title("🚀 인공중력 시뮬레이터")
st.sidebar.markdown("---")

obs_mode = st.sidebar.radio(
    "🔭 관찰 모드 선택",
    ["외부 원경 (Cinematic)", "관성계 (Inertial Frame)", "비관성계 (Rotating Frame)"]
)

st.sidebar.markdown("---")
radius_val = st.sidebar.slider("반지름 (r) [m]", 100, 1000, 500, step=50)
omega_val = st.sidebar.slider("각속도 (ω) [rad/s]", 0.05, 0.40, 0.15, step=0.01)

# 물리 값 계산
accel = radius_val * (omega_val ** 2)
g_force = accel / 9.8

st.sidebar.info(f"""
- **가속도 (a):** {accel:.2f} m/s²
- **중력 대비 (G):** {g_force:.2f} G
""")

st.sidebar.markdown("---")
st.sidebar.caption("본 시뮬레이션은 인터스텔라 쿠퍼 스테이션의 설계를 참고하여 고화질 2D 캔버스로 구현되었습니다.")

# ── 메인 화면 ──
st.title("🛡️ 인공중력 우주 정거장 시뮬레이터")
st.markdown(f"현재 선택된 모드: **{obs_mode}**")

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        body {{ margin: 0; background: #010409; overflow: hidden; font-family: 'JetBrains+Mono', monospace; }}
        canvas {{ display: block; background: radial-gradient(circle at 30% 30%, #0d1117 0%, #010409 100%); }}
        #hud {{
            position: absolute; top: 20px; right: 20px;
            color: #38bdf8; background: rgba(15, 23, 42, 0.7);
            padding: 15px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.3);
            font-size: 13px; pointer-events: none; backdrop-filter: blur(5px);
        }}
    </style>
</head>
<body>
    <div id="hud">
        <div style="font-weight:700; margin-bottom:8px; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:4px;">STATION TELEMETRY</div>
        Radius: {radius_val}m<br>
        Omega: {omega_val} rad/s<br>
        Gravity: {accel:.2f} m/s² ({g_force:.2f} G)
    </div>
    <div id="coord" style="position:absolute; bottom:10px; left:10px; color:rgba(148,163,184,0.4); font-size:10px;"></div>
    <canvas id="simCanvas"></canvas>

<script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    const coordDisp = document.getElementById('coord');

    const r = {radius_val};
    const omega = {omega_val};
    let angle = 0;
    let earthAngle = 0;

    function resize() {{
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }}
    window.onresize = resize;
    resize();

    // ── 우주 배경 자산 ──
    const stars = [];
    for (let i = 0; i < 400; i++) {{
        stars.push({{
            x: (Math.random() - 0.5) * canvas.width * 2,
            y: (Math.random() - 0.5) * canvas.height * 2,
            size: Math.random() * 1.5,
            opacity: Math.random() * 0.8 + 0.2,
            phase: Math.random() * Math.PI * 2
        }});
    }}

    function drawSpace(cx, cy, rot) {{
        const now = Date.now() * 0.001;
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);
        ctx.fillStyle = '#010409';
        ctx.fillRect(-canvas.width * 2, -canvas.height * 2, canvas.width * 4, canvas.height * 4);
        stars.forEach(s => {{
            const glow = 0.5 + 0.5 * Math.sin(now + s.phase);
            ctx.fillStyle = `rgba(255, 255, 255, ${{s.opacity * (0.7 + 0.3 * glow)}})`;
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
            ctx.fill();
        }});
        ctx.restore();
    }}

    function drawEarth(cx, cy, scale, rot) {{
        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);
        const er = 220 * scale;
        const ex = -canvas.width * 0.35;
        const ey = -canvas.height * 0.38;
        
        ctx.save();
        ctx.translate(ex, ey);
        const glow = ctx.createRadialGradient(0, 0, er, 0, 0, er * 1.4);
        glow.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
        glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow;
        ctx.beginPath(); ctx.arc(0, 0, er * 1.4, 0, Math.PI * 2); ctx.fill();
        
        const grad = ctx.createRadialGradient(-er*0.3, -er*0.3, er*0.1, 0, 0, er);
        grad.addColorStop(0, '#3b82f6');
        grad.addColorStop(0.6, '#1d4ed8');
        grad.addColorStop(1, '#1e3a8a');
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(0, 0, er, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
        ctx.restore();
    }}

    // ── 공통 고화질 자산: 우주정거장 ──
    function drawRealisticStation(cx, cy, rot, scale, isInternal) {{
        const visualR = 210 * scale;
        const tubeW = 40 * scale;

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);

        // 1. 지주 (Spokes)
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 14 * scale;
        for (let i = 0; i < 4; i++) {{
            const a = (i / 4) * Math.PI * 2;
            ctx.beginPath(); ctx.moveTo(0, 0);
            ctx.lineTo(Math.cos(a) * visualR, Math.sin(a) * visualR);
            ctx.stroke();
        }}

        // 2. 허브 (Hub)
        const hr = 45 * scale;
        const hGrad = ctx.createRadialGradient(-hr*0.3, -hr*0.3, 0, 0, 0, hr);
        hGrad.addColorStop(0, '#94a3b8'); hGrad.addColorStop(1, '#0f172a');
        ctx.fillStyle = hGrad;
        ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.fill();

        // 3. 토러스 링 (Ring)
        ctx.shadowBlur = 25; ctx.shadowColor = 'rgba(0,0,0,0.8)';
        ctx.strokeStyle = '#1e293b'; ctx.lineWidth = tubeW * 1.2;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        ctx.shadowBlur = 0;

        ctx.strokeStyle = '#475569'; ctx.lineWidth = tubeW * 0.7;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

        // 창문
        ctx.strokeStyle = 'rgba(56,189,248,0.4)'; ctx.lineWidth = 3 * scale;
        for (let i = 0; i < 24; i++) {{
            const a = (i / 24) * Math.PI * 2;
            ctx.beginPath(); ctx.arc(0, 0, visualR, a, a + 0.08); ctx.stroke();
        }}
        ctx.restore();
    }}

    function drawAstronaut(x, y, rot, scale, isInternal) {{
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        const s = scale * 1.4;
        ctx.fillStyle = '#f8fafc'; // Suit
        ctx.beginPath(); ctx.roundRect(-6*s, -12*s, 12*s, 18*s, 4*s); ctx.fill();
        ctx.fillStyle = '#1e293b'; // Visor
        ctx.beginPath(); ctx.roundRect(-4*s, -10*s, 8*s, 5*s, 2*s); ctx.fill();
        ctx.restore();
    }}

    function drawArrow(x, y, len, ang, color, label) {{
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(ang);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-10, -5); ctx.lineTo(len-10, 5); ctx.closePath(); ctx.fill();
        ctx.rotate(-ang);
        ctx.font = 'bold 12px Arial';
        ctx.fillText(label, 15, -10);
        ctx.restore();
    }}

    function renderExternal(cx, cy) {{
        const scale = Math.min(canvas.width, canvas.height) / 560;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 16px Arial';
        ctx.fillText('EXTERNAL VIEW', 20, 40);
    }}

    function renderInertial(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 560;
        const visualR = 210 * scale;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        const ax = cx + Math.cos(angle) * visualR;
        const ay = cy + Math.sin(angle) * visualR;
        drawAstronaut(ax, ay, angle - Math.PI/2, scale, true);
        drawArrow(ax, ay, 60, angle + Math.PI, '#ef4444', 'N (Normal Force)');
        ctx.fillStyle = '#ef4444'; ctx.font = 'bold 16px Arial';
        ctx.fillText('INERTIAL FRAME', 20, 40);
    }}

    function renderRotating(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 560;
        const visualR = 210 * scale;
        drawSpace(cx, cy, -angle);
        drawEarth(cx, cy, scale, -angle + earthAngle);
        drawRealisticStation(cx, cy, 0, scale, true);
        const ax = cx + visualR;
        const ay = cy;
        drawAstronaut(ax, ay, -Math.PI/2, scale, true);
        drawArrow(ax, ay, 60, 0, '#10b981', 'Inertial Force');
        drawArrow(ax, ay, 50, Math.PI, '#ef4444', 'N');
        ctx.fillStyle = '#10b981'; ctx.font = 'bold 16px Arial';
        ctx.fillText('NON-INERTIAL FRAME', 20, 40);
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        earthAngle += 0.0005;
        angle += omega * 0.016;

        const mode = "{obs_mode}";
        if (mode === "외부 원경 (Cinematic)") renderExternal(cx, cy);
        else if (mode === "관성계 (Inertial Frame)") renderInertial(cx, cy, accel);
        else renderRotating(cx, cy, accel);

        requestAnimationFrame(render);
    }}

    canvas.addEventListener('mousemove', e => {{
        const r = canvas.getBoundingClientRect();
        coordDisp.textContent = `X: ${{(e.clientX - r.left).toFixed(0)}}  Y: ${{(e.clientY - r.top).toFixed(0)}}`;
    }});

    render();
</script>
</body>
</html>
"""

components.html(html_content, height=680, scrolling=False)

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("**외부 원경:** 정거장이 회전하고 배경은 고정된 관찰자 시점입니다.")
with col2:
    st.error("**관성계:** 물체가 원운동을 하기 위해 안쪽으로 힘(N)을 받는 실제 물리 현상입니다.")
with col3:
    st.success("**비관성계:** 회전하는 내부에서 바깥으로 쏠리는 가상의 힘(원심력)을 관찰합니다.")

def show():
    pass

show()
