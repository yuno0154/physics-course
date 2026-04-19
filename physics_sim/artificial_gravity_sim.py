import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import os

st.set_page_config(page_title="인공중력 프리미엄 시뮬레이션", layout="wide")

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
        canvas {{ display: block; background: #010409; }}
        #hud {{
            position: absolute; top: 20px; right: 20px;
            color: #38bdf8; background: rgba(15, 23, 42, 0.8);
            padding: 15px; border-radius: 10px; border: 1px solid rgba(56, 189, 248, 0.3);
            font-size: 13px; pointer-events: none; backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        }}
    </style>
</head>
<body>
    <div id="hud">
        <div style="font-weight:700; margin-bottom:8px; border-bottom:1px solid rgba(56,189,248,0.3); padding-bottom:4px; color:#f8fafc;">STATION STATUS</div>
        <span style="color:#94a3b8">Mode:</span> {obs_mode}<br>
        <span style="color:#94a3b8">Radius:</span> {radius_val} m<br>
        <span style="color:#94a3b8">Omega:</span> {omega_val} rad/s<br>
        <div style="margin-top:8px; color:#facc15; font-weight:700;">Gravity: {accel:.2f} m/s² ({g_force:.2f} G)</div>
    </div>
    <div id="coord" style="position:absolute; bottom:10px; left:10px; color:rgba(148,163,184,0.4); font-size:10px;"></div>
    <canvas id="simCanvas"></canvas>

<script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    const coordDisp = document.getElementById('coord');

    const radius = {radius_val};
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
            size: Math.random() * 1.6,
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

        const er = 240 * scale;
        const ex = -canvas.width * 0.35;
        const ey = -canvas.height * 0.38;
        
        ctx.translate(ex, ey);
        
        // Atmosphere layer
        const glow = ctx.createRadialGradient(0, 0, er * 0.95, 0, 0, er * 1.3);
        glow.addColorStop(0, 'rgba(37, 99, 235, 0.2)');
        glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow;
        ctx.beginPath(); ctx.arc(0, 0, er * 1.3, 0, Math.PI * 2); ctx.fill();
        
        // Planet body
        const grad = ctx.createRadialGradient(-er*0.3, -er*0.3, er*0.2, 0, 0, er);
        grad.addColorStop(0, '#3b82f6'); // Surface
        grad.addColorStop(0.5, '#1d4ed8'); // Dark blue
        grad.addColorStop(1, '#0e1b3d'); // Deep void
        ctx.fillStyle = grad;
        ctx.beginPath(); ctx.arc(0, 0, er, 0, Math.PI * 2); ctx.fill();
        
        // Subtle clouds
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 15 * scale;
        ctx.beginPath(); ctx.arc(0, 0, er * 0.7, 0.4, 1.2); ctx.stroke();
        ctx.beginPath(); ctx.arc(0, 0, er * 0.85, 2.1, 3.5); ctx.stroke();

        ctx.restore();
    }}

    // ── 프리미엄 자산: 고화질 쿠퍼 스테이션 (6-Sectors) ──
    function drawRealisticStation(cx, cy, rot, scale, isInternal) {{
        const visualR = 210 * scale;
        const tubeW = 42 * scale;

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);

        // 1. Spokes (6개 모듈 지주)
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 14 * scale;
        for (let i = 0; i < 6; i++) {{
            const a = (i / 6) * Math.PI * 2;
            ctx.beginPath();
            ctx.moveTo(0, 0);
            ctx.lineTo(Math.cos(a) * visualR * 0.92, Math.sin(a) * visualR * 0.92);
            ctx.stroke();
            
            // 지주 세부 구조
            ctx.strokeStyle = '#1e293b'; 
            ctx.lineWidth = 4 * scale;
            ctx.beginPath();
            ctx.moveTo(Math.cos(a) * 50 * scale, Math.sin(a) * 50 * scale);
            ctx.lineTo(Math.cos(a) * visualR * 0.8, Math.sin(a) * visualR * 0.8);
            ctx.stroke();
        }}

        // 2. Solar Panels (허브 옆 태양광 패널)
        ctx.save();
        ctx.rotate(angle * -0.2); // 약간의 독립적 움직임
        ctx.fillStyle = '#0f172a';
        for (let i = 0; i < 2; i++) {{
            const a = (i * Math.PI) + Math.PI/2;
            const px = Math.cos(a) * 60 * scale;
            const py = Math.sin(a) * 60 * scale;
            ctx.save();
            ctx.translate(px, py);
            ctx.rotate(a);
            ctx.fillRect(-25*scale, 0, 50*scale, 80*scale);
            // 패널 그리드
            ctx.strokeStyle = 'rgba(56,189,248,0.3)';
            ctx.lineWidth = 1;
            for(let j=0; j<4; j++) {{
                ctx.beginPath(); ctx.moveTo(-25*scale, j*20*scale); ctx.lineTo(25*scale, j*20*scale); ctx.stroke();
            }}
            ctx.restore();
        }}
        ctx.restore();

        // 3. Hub (다층 중심부)
        const hr = 50 * scale;
        const hGrad = ctx.createRadialGradient(-hr*0.3, -hr*0.3, 5, 0, 0, hr);
        hGrad.addColorStop(0, '#94a3b8');
        hGrad.addColorStop(0.7, '#334155');
        hGrad.addColorStop(1, '#0f172a');
        ctx.fillStyle = hGrad;
        ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#64748b'; ctx.lineWidth = 2 * scale;
        ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.stroke();
        
        // 허브 창문 빛
        ctx.fillStyle = 'rgba(56,189,248,0.5)';
        for(let i=0; i<8; i++) {{
            const a = (i/8)*Math.PI*2 + angle*0.1;
            ctx.beginPath(); ctx.arc(Math.cos(a)*hr*0.7, Math.sin(a)*hr*0.7, 2*scale, 0, Math.PI*2); ctx.fill();
        }}

        // 4. Main Ring (토러스 본체)
        // 외곽 두꺼운 선체
        ctx.strokeStyle = '#1e293b';
        ctx.lineWidth = tubeW * 1.1;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        
        // 메인 생활 구역
        ctx.strokeStyle = '#475569';
        ctx.lineWidth = tubeW * 0.7;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        
        // 상단 하이라이트 (금속 질감)
        ctx.strokeStyle = 'rgba(255,255,255,0.15)';
        ctx.lineWidth = tubeW * 0.15;
        ctx.beginPath(); ctx.arc(0, 0, visualR - tubeW*0.25, 0, Math.PI * 2); ctx.stroke();

        // 5. Windows & Lights
        const segs = 36;
        for (let i = 0; i < segs; i++) {{
            const a = (i / segs) * Math.PI * 2;
            const isWindow = i % 3 !== 0; // 일부는 창문, 일부는 격벽
            
            if (isWindow) {{
                ctx.strokeStyle = 'rgba(186, 230, 253, 0.4)';
                ctx.lineWidth = 4 * scale;
            }} else {{
                ctx.strokeStyle = 'rgba(15, 23, 42, 0.8)'; // 격벽
                ctx.lineWidth = 6 * scale;
            }}
            ctx.beginPath();
            ctx.arc(0, 0, visualR, a, a + 0.12);
            ctx.stroke();

            // 빨간색 항공 장해등 (일부만)
            if (i % 9 === 0) {{
                ctx.fillStyle = `rgba(239, 68, 68, ${{0.5 + 0.5 * Math.sin(Date.now()*0.005 + i)}})`;
                ctx.beginPath(); ctx.arc(Math.cos(a)*visualR, Math.sin(a)*visualR, 2.5*scale, 0, Math.PI*2); ctx.fill();
            }}
        }}

        ctx.restore();
    }}

    function drawAstronaut(x, y, rot, scale, isInternal) {{
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(rot);
        const s = scale * 1.5;
        // Suit
        ctx.fillStyle = '#f8fafc';
        ctx.beginPath(); ctx.roundRect(-6*s, -12*s, 12*s, 18*s, 4*s); ctx.fill();
        // Helmet
        ctx.fillStyle = '#0f172a';
        ctx.beginPath(); ctx.roundRect(-4*s, -10*s, 8*s, 5*s, 2*s); ctx.fill();
        // Pack
        ctx.fillStyle = '#94a3b8';
        ctx.fillRect(-7*s, -5*s, 2*s, 8*s);
        ctx.restore();
    }}

    function drawArrow(x, y, len, ang, color, label) {{
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(ang);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-15, -6); ctx.lineTo(len-15, 6); ctx.closePath(); ctx.fill();
        ctx.rotate(-ang);
        ctx.font = 'bold 12px JetBrains Mono, monospace';
        ctx.fillStyle = color;
        ctx.shadowBlur = 4; ctx.shadowColor = 'black';
        ctx.fillText(label, 20, -10);
        ctx.restore();
    }}

    // [1] EXTERNAL
    function renderExternal(cx, cy) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        
        ctx.fillStyle = '#38bdf8'; ctx.font = 'bold 18px JetBrains Mono';
        ctx.fillText('CINEMATIC EXTERNAL VIEW', 30, 50);
        ctx.fillStyle = 'rgba(148,163,184,0.6)'; ctx.font = '13px JetBrains Mono';
        ctx.fillText('Station Rotating | Stars Fixed', 30, 75);
    }}

    // [2] INERTIAL
    function renderInertial(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        const visualR = 210 * scale;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        
        const ax = cx + Math.cos(angle) * visualR;
        const ay = cy + Math.sin(angle) * visualR;
        drawAstronaut(ax, ay, angle - Math.PI/2, scale, true);
        
        const nLen = Math.min(130, accel * 8) * scale;
        drawArrow(ax, ay, nLen, angle + Math.PI, '#ef4444', 'N (Normal Force)');
        
        ctx.fillStyle = '#ef4444'; ctx.font = 'bold 18px JetBrains Mono';
        ctx.fillText('INERTIAL FRAME', 30, 50);
        ctx.fillStyle = 'rgba(148,163,184,0.6)'; ctx.font = '13px JetBrains Mono';
        ctx.fillText('Actual Circular Motion | Centripetal Force = N', 30, 75);
    }}

    // [3] NON-INERTIAL (Rotating)
    function renderRotating(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        const visualR = 210 * scale;
        
        // 배경 역회전 (겉보기 운동)
        drawSpace(cx, cy, -angle);
        drawEarth(cx, cy, scale, -angle + earthAngle);
        
        // 정거장 고정
        drawRealisticStation(cx, cy, 0, scale, true);
        
        const ax = cx + visualR;
        const ay = cy;
        drawAstronaut(ax, ay, -Math.PI/2, scale, true);
        
        const fLen = Math.min(130, accel * 8) * scale;
        drawArrow(ax, ay, fLen, 0, '#10b981', 'Inertial Force (Centrifugal)');
        drawArrow(ax, ay, fLen * 0.85, Math.PI, '#ef4444', 'N');
        
        ctx.fillStyle = '#10b981'; ctx.font = 'bold 18px JetBrains Mono';
        ctx.fillText('NON-INERTIAL FRAME', 30, 50);
        ctx.fillStyle = 'rgba(148,163,184,0.6)'; ctx.font = '13px JetBrains Mono';
        ctx.fillText('Station Fixed | Stars Rotating | Faux Gravity', 30, 75);
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        earthAngle += 0.0004;
        angle += omega * 0.016;

        const mode = "{obs_mode}";
        if (mode === "외부 원경 (Cinematic)") renderExternal(cx, cy);
        else if (mode === "관성계 (Inertial Frame)") renderInertial(cx, cy, {accel});
        else renderRotating(cx, cy, {accel});

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

# ── 학습 개념 정리 섹션 (전면 복원) ──
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e); 
                border:1px solid rgba(56,189,248,0.25); border-radius:14px; padding:20px; height:220px;">
        <div style="color:#38bdf8; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
            🛸 외부 원경 (Cinematic View)
        </div>
        <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
            우주정거장이 실제 우주에서 회전하는 모습을 외부에서 바라봅니다. 
            토러스(도넛) 형태의 거주 구역이 회전하며 내부에 <strong>관성력</strong>을 생성하여 중력을 모사합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e); 
                border:1px solid rgba(239,68,68,0.25); border-radius:14px; padding:20px; height:220px;">
        <div style="color:#ef4444; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
            🔭 관성계 (Inertial Frame)
        </div>
        <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
            외부 고정 관찰자 시점입니다. 우주인은 <strong style="color:#ef4444">실제로 원운동</strong>하고 있습니다.
            이때 선체 바닥이 우주인을 안쪽으로 밀어내는 <strong>수직항력 (N)</strong>이 구심력 역할을 합니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e); 
                border:1px solid rgba(16,185,129,0.25); border-radius:14px; padding:20px; height:220px;">
        <div style="color:#10b981; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
            🧑‍🚀 비관성계 (Rotating Frame)
        </div>
        <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
            회전하는 내부 관찰자 시점입니다. 정거장은 고정되어 보이고 배경이 회전합니다.
            바깥으로 쏠리는 <strong>원심력(가상력)</strong>이 마치 중력처럼 느껴지는 상태입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── 인터스텔라 쿠퍼 스테이션 탐구 가이드 (복원) ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08); 
            border-radius:14px; padding:25px; margin-top:4px;">
    <div style="color:#f8fafc; font-weight:800; font-size:1rem; margin-bottom:14px; display:flex; align-items:center; gap:10px;">
        <span style="font-size:1.5rem;">📐</span> 쿠퍼 스테이션의 물리적 설계
    </div>
    <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:18px;">
        <div style="background:rgba(56,189,248,0.08); border-radius:10px; padding:18px; text-align:center; border:1px solid rgba(56,189,248,0.15);">
            <div style="color:#38bdf8; font-size:1.2rem; font-weight:700; font-family:monospace;">a = rω²</div>
            <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">원심 가속도 공식</div>
        </div>
        <div style="background:rgba(16,185,129,0.08); border-radius:10px; padding:18px; text-align:center; border:1px solid rgba(16,185,129,0.15);">
            <div style="color:#10b981; font-size:1.2rem; font-weight:700; font-family:monospace;">F = mrω²</div>
            <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">체감 중력 (원심력)</div>
        </div>
        <div style="background:rgba(245,158,11,0.08); border-radius:10px; padding:18px; text-align:center; border:1px solid rgba(245,158,11,0.15);">
            <div style="color:#f59e0b; font-size:1.2rem; font-weight:700; font-family:monospace;">g_eff ≈ 1G</div>
            <div style="color:#64748b; font-size:0.75rem; margin-top:6px;">목표 중력 가속도</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── 영상 및 이미지 섹션 (복원) ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="background:linear-gradient(135deg,#0d0a00,#1a1200); border:1px solid rgba(245,158,11,0.3); border-left:4px solid #f59e0b; border-radius:14px; padding:20px;">
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
        <span style="font-size:1.3rem;">🎬</span>
        <span style="color:#f59e0b; font-weight:800; font-size:0.95rem;">인터스텔라 탐구 참고</span>
    </div>
    <p style="color:#94a3b8; font-size:0.85rem; margin-bottom:15px;">영화 속 쿠퍼 스테이션은 지름 2km의 거대 원통형 구조물입니다. 아래 영상을 통해 원심력을 활용한 거주 공간을 확인해 보세요.</p>
    <a href="https://youtu.be/TzKvVb6j2Zo" target="_blank" style="color:#fbbf24; font-size:0.85rem; font-weight:700; text-decoration:none; border-bottom:1px solid;">▶ 인터스텔라 쿠퍼스테이션 보기 (YouTube)</a>
</div>
""", unsafe_allow_html=True)

img_col1, img_col2 = st.columns(2)
with img_col1:
    st.caption("장면 1: 외부 원경 - 거대 토러스 링의 회전")
    # 이미지 파일이 있는 경우 표시 (없으면 건너뜀)
    if os.path.exists("cooper_exterior.png"): st.image("cooper_exterior.png")

with img_col2:
    st.caption("장면 2: 내부 시점 - 원심력에 의한 중력 생성")
    if os.path.exists("cooper_interior.png"): st.image("cooper_interior.png")

def show():
    pass

show()
