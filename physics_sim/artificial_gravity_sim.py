import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import os

# 페이지 설정
st.set_page_config(page_title="인공중력 프리미엄 탐구 시뮬레이션", layout="wide")

# ── 사이드바 제어판 ──
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

# ── 메인 화면 ──
st.title("🛡️ 인공중력 우주 정거장 탐구 시뮬레이터")
st.markdown(f"현재 선택된 모드: **{obs_mode}**")

# 이미지 경로 설정 (physics_sim 폴더 여부에 따른 처리)
base_path = "physics_sim/" if os.path.exists("physics_sim/cooper_exterior.png") else ""

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700;800&family=Pretendard:wght@400;700;900&display=swap');
        body {{ margin: 0; background: #010409; overflow: hidden; font-family: 'Pretendard', sans-serif; }}
        canvas {{ display: block; background: #010409; }}
        
        /* 실시간 데이터 대시보드 (Simulation Window) */
        #dashboard {{
            position: absolute; top: 20px; right: 20px;
            width: 280px; color: #38bdf8; background: rgba(15, 23, 42, 0.85);
            padding: 20px; border-radius: 20px; border: 1px solid rgba(56, 189, 248, 0.3);
            pointer-events: none; backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            animation: fadeIn 0.8s ease-out;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(-10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .label {{ color: #94a3b8; font-size: 11px; font-weight: 800; letter-spacing: 1px; }}
        .value {{ color: #f8fafc; font-size: 20px; font-weight: 900; font-family: 'JetBrains Mono', monospace; margin-bottom: 12px; }}
        .g-value {{ color: #facc15; font-size: 24px; font-weight: 900; }}
        
        #coord {{ position: absolute; bottom: 10px; left: 10px; color: rgba(148,163,184,0.4); font-size: 10px; font-family: monospace; }}
    </style>
</head>
<body>
    <div id="dashboard">
        <div style="font-weight:900; margin-bottom:15px; border-bottom:1px solid rgba(56,189,248,0.2); padding-bottom:8px; color:#38bdf8; font-size:12px;">🛰️ MISSION TELEMETRY</div>
        
        <div class="label">RADIUS (r)</div>
        <div class="value">{radius_val} <span style="font-size:12px; color:#64748b;">m</span></div>
        
        <div class="label">ANGULAR VELOCITY (ω)</div>
        <div class="value">{omega_val} <span style="font-size:12px; color:#64748b;">rad/s</span></div>
        
        <div class="label" style="color:#ef4444;">ARTIFICIAL GRAVITY (a = rω²)</div>
        <div class="g-value">{accel:.2f} <span style="font-size:14px; color:#64748b;">m/s²</span></div>
        <div style="font-size:14px; font-weight:900; color:#f59e0b;">({g_force:.2f} G)</div>
    </div>
    <div id="coord"></div>
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

    // 별 무리 자산
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
        const ex = -canvas.width * 0.38;
        const ey = -canvas.height * 0.4;
        ctx.translate(ex, ey);
        // Atmosphere
        const glow = ctx.createRadialGradient(0, 0, er, 0, 0, er * 1.3);
        glow.addColorStop(0, 'rgba(37, 99, 235, 0.15)'); glow.addColorStop(1, 'transparent');
        ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(0, 0, er * 1.3, 0, Math.PI * 2); ctx.fill();
        // Body
        const grad = ctx.createRadialGradient(-er*0.3, -er*0.3, er*0.1, 0, 0, er);
        grad.addColorStop(0, '#3b82f6'); grad.addColorStop(0.6, '#1d4ed8'); grad.addColorStop(1, '#0e1b3d');
        ctx.fillStyle = grad; ctx.beginPath(); ctx.arc(0, 0, er, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
    }}

    function drawRealisticStation(cx, cy, rot, scale, isInternal) {{
        const baseR = 210 * scale;
        const visualR = isInternal ? baseR * 1.5 : baseR; // 내부 시점에서는 더 가깝게
        const tubeW = 40 * scale * (isInternal ? 1.4 : 1);

        ctx.save();
        ctx.translate(cx, cy);
        ctx.rotate(rot);

        // 1. Spokes
        ctx.strokeStyle = '#334155'; ctx.lineWidth = 12 * scale;
        for (let i = 0; i < 6; i++) {{
            const a = (i / 6) * Math.PI * 2;
            ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(Math.cos(a) * visualR, Math.sin(a) * visualR); ctx.stroke();
        }}

        // 2. Hub
        const hr = 45 * scale;
        ctx.fillStyle = '#1e293b'; ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#475569'; ctx.lineWidth = 3 * scale; ctx.beginPath(); ctx.arc(0, 0, hr, 0, Math.PI * 2); ctx.stroke();

        // 3. Main Torus Ring
        ctx.strokeStyle = '#0f172a'; ctx.lineWidth = tubeW * 1.1;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();
        ctx.strokeStyle = '#475569'; ctx.lineWidth = tubeW * 0.7;
        ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

        // High-res Details: Solar Panels
        for (let i = 0; i < 2; i++) {{
            const a = (i * Math.PI) + (rot * 0.1);
            ctx.save(); ctx.rotate(a);
            ctx.fillStyle = '#0f172a'; ctx.fillRect(50*scale, -30*scale, 90*scale, 60*scale);
            ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 1;
            for(let j=0; j<4; j++) {{ ctx.beginPath(); ctx.moveTo(50*scale+(j*22*scale), -30*scale); ctx.lineTo(50*scale+(j*22*scale), 30*scale); ctx.stroke(); }}
            ctx.restore();
        }}

        // Windows
        ctx.strokeStyle = 'rgba(186,230,253,0.35)'; ctx.lineWidth = 3 * scale;
        for (let i = 0; i < 36; i++) {{
            const a = (i / 36) * Math.PI * 2;
            ctx.beginPath(); ctx.arc(0, 0, visualR, a, a + 0.08); ctx.stroke();
        }}
        ctx.restore();
    }}

    function drawAstronaut(x, y, rot, scale) {{
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
        const s = scale * 1.6;
        ctx.fillStyle = '#f8fafc'; ctx.beginPath(); ctx.roundRect(-6*s, -12*s, 12*s, 18*s, 4*s); ctx.fill();
        ctx.fillStyle = '#0f172a'; ctx.beginPath(); ctx.roundRect(-4*s, -10*s, 8*s, 5*s, 2*s); ctx.fill();
        ctx.restore();
    }}

    function drawArrow(x, y, len, ang, color, label) {{
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-12, -6); ctx.lineTo(len-12, 6); ctx.closePath(); ctx.fill();
        ctx.rotate(-ang); ctx.font = 'bold 12px Pretendard';
        ctx.shadowBlur = 4; ctx.shadowColor = 'black'; ctx.fillText(label, 20, -10);
        ctx.restore();
    }}

    function renderExternal(cx, cy) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        ctx.fillStyle = '#38bdf8'; ctx.font = '900 16px Pretendard';
        ctx.fillText('CINEMATIC EXTERNAL VIEW', 30, 45);
    }}

    function renderInertial(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        const visualR = 210 * scale;
        drawSpace(cx, cy, 0);
        drawEarth(cx, cy, scale, earthAngle);
        drawRealisticStation(cx, cy, angle, scale, false);
        const ax = cx + Math.cos(angle) * visualR;
        const ay = cy + Math.sin(angle) * visualR;
        drawAstronaut(ax, ay, angle - Math.PI/2, scale);
        const nLen = Math.min(130, accel * 8) * scale;
        drawArrow(ax, ay, nLen, angle + Math.PI, '#ef4444', 'N (Normal Force)');
        ctx.fillStyle = '#ef4444'; ctx.font = '900 16px Pretendard';
        ctx.fillText('INERTIAL FRAME (관성계)', 30, 45);
    }}

    function renderRotating(cx, cy, accel) {{
        const scale = Math.min(canvas.width, canvas.height) / 580;
        const visualR = 210 * scale * 1.5; // 내부 시점이므로 확대
        drawSpace(cx, cy, -angle);
        drawEarth(cx, cy, scale, -angle + earthAngle);
        drawRealisticStation(cx, cy, 0, scale, true);
        const ax = cx + visualR;
        const ay = cy;
        drawAstronaut(ax, ay, -Math.PI/2, scale);
        const fLen = Math.min(130, accel * 8) * scale;
        drawArrow(ax, ay, fLen, 0, '#10b981', 'Inertial Force (가성력)');
        drawArrow(ax, ay, fLen * 0.9, Math.PI, '#ef4444', 'N');
        ctx.fillStyle = '#10b981'; ctx.font = '900 16px Pretendard';
        ctx.fillText('NON-INERTIAL FRAME (비관성계)', 30, 45);
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        earthAngle += 0.0004; angle += omega * 0.016;
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

# ── 탐구 섹션 및 콘텐츠 복원 ──
st.markdown("---")
st.markdown("### 🔍 회전하는 우주 정거장 속의 물리 탐구")

# 비교 분석 테이블 복원
st.markdown("""
<style>
    .physics-table { width: 100%; border-collapse: collapse; margin-bottom: 30px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .physics-table th { background: #0f172a; color: white; padding: 15px; font-weight: 800; border: 1px solid #1e293b; }
    .physics-table td { background: white; padding: 15px; border: 1px solid #e2e8f0; text-align: center; }
    .label-cell { background: #f8fafc !important; font-weight: 700; color: #475569; width: 20%; }
    .ans-tag { background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: 700; cursor: pointer; }
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
            <td>정거장과 함께 <b>등속 원운동</b> 진행</td>
            <td>정거장 내부에 <b>정지</b>한 상태</td>
        </tr>
        <tr>
            <td class="label-cell">작용하는 힘</td>
            <td>바닥이 안으로 미는 <b>수직항력(N)</b></td>
            <td><b>수직항력(N)</b> + <b>관성력(원심력)</b></td>
        </tr>
        <tr>
            <td class="label-cell">운동의 해석</td>
            <td>수직항력이 <b>구심력</b>이 되어 원운동 유발</td>
            <td>수직항력과 관성력이 <b>평형</b>을 이룸</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# ── 인터스텔라 쿠퍼 스테이션 복원 섹션 ──
st.header("🎞️ 쿠퍼 스테이션(Cooper Station) 실전 분석")
st.markdown("""
영화 '인터스텔라'의 마지막 장면에 등장하는 쿠퍼 스테이션은 지름 약 2km의 거대 원통형 구조물입니다. 
이 스테이션은 원심력을 활용해 지구와 유사한 1G($9.8m/s^2$)의 중력을 모사하도록 설계되었습니다.
""")

col_img1, col_img2 = st.columns(2)
with col_img1:
    st.subheader("🪐 Station Exterior")
    img_ext = base_path + "cooper_exterior.png"
    if os.path.exists(img_ext):
        st.image(img_ext, caption="Scene: The Cooper Station rotating in Saturn's orbit", use_container_width=True)
    else:
        st.warning(f"외측 이미지를 찾을 수 없습니다: {img_ext}")

with col_img2:
    st.subheader("🏡 Station Interior")
    img_int = base_path + "cooper_interior.png"
    if os.path.exists(img_int):
        st.image(img_int, caption="Scene: Gravity holding the landscape onto the curved floor", use_container_width=True)
    else:
        st.warning(f"내측 이미지를 찾을 수 없습니다: {img_int}")

st.markdown("""
> [!IMPORTANT]
> **쿠퍼 스테이션의 중력 설계**: 
> 반지름($r$)이 1,000m일 때 $9.8m/s^2$을 얻기 위한 각속도($\omega$)는 약 $0.099 rad/s$입니다. 
> 시뮬레이션에서 반지름을 1000m로 설정하고 각속도를 0.10 부근으로 조절하여 1G가 되는지 확인해 보세요!
""")

st.markdown("---")
st.markdown("#### 📖 더 알고 싶다면")
st.info("💡 **생각해보기**: 우주 정거장의 회전 속도가 갑자기 빨라지면, 내부 우주인이 느끼는 몸무게는 어떻게 변할까요? 수식을 통해 예측해 봅시다.")
st.video("https://youtu.be/TzKvVb6j2Zo")

def show():
    pass

if __name__ == "__main__":
    show()
