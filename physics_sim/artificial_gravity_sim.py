import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="인공중력 시뮬레이션: 관성계 vs 비관성계", layout="wide")

# ── 사이드바 제어판 ──
st.sidebar.title("🧬 물리 탐구 설정")
st.sidebar.markdown("---")

obs_mode = st.sidebar.radio(
    "🔭 시점(Frame) 선택",
    ["관성계 (Inertial Frame)", "비관성계 (Rotating Frame)"]
)

st.sidebar.markdown("---")
# 슬라이더 - 물리량 제어
radius_val = st.sidebar.slider("정거장 반지름 (r) [m]", 100, 1000, 500, step=50)
omega_val = st.sidebar.slider("회전 각속도 (ω) [rad/s]", 0.05, 0.40, 0.15, step=0.01)

# 물리 계산 (a = r * omega^2)
accel = radius_val * (omega_val ** 2)
g_force = accel / 9.8

st.sidebar.info(f"""
- **반지름(r):** {radius_val} m
- **각속도(ω):** {omega_val:.2f} rad/s
- **모사중력(a):** {accel:.2f} m/s² ({g_force:.2f} G)
""")

# ── 메인 화면 ──
st.title("🛡️ 인공중력 우주 정거장 시뮬레이션")
st.markdown(f"모드: **{obs_mode}** | 인공중력 가속도: **{accel:.2f} m/s²**")

# 이미지 경로 설정
base_path = "physics_sim/" if os.path.exists("physics_sim/cooper_exterior.png") else ""

# ── 시뮬레이션 캔버스 (두 번째 이미지의 스타일 복제) ──
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;700;900&display=swap');
        body {{ margin: 0; background: #000; overflow: hidden; font-family: 'Pretendard', sans-serif; }}
        canvas {{ display: block; }}
        
        #data-window {{
            position: absolute; top: 15px; left: 15px;
            background: rgba(255, 255, 255, 0.1);
            color: white; padding: 15px; border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            pointer-events: none; font-size: 13px;
        }}
    </style>
</head>
<body>
    <div id="data-window">
        📡 DATA WINDOW<br/>
        ----------------<br/>
        a = rω² = {accel:.2f} m/s²<br/>
        r = {radius_val}m / ω = {omega_val}rad/s
    </div>
    <canvas id="simCanvas"></canvas>

<script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');
    const isRotatingFrame = "{obs_mode}" === "비관성계 (Rotating Frame)";
    
    const radiusParam = {radius_val};
    const omega = {omega_val};
    const accelVal = {accel};
    let angle = 0;

    function resize() {{ canvas.width = window.innerWidth; canvas.height = window.innerHeight; }}
    window.onresize = resize; resize();

    // 별 생성 (심플한 배경)
    const stars = [];
    for(let i=0; i<300; i++) {{
        stars.push({{ x: Math.random()*2-1, y: Math.random()*2-1, size: Math.random()*1.5 }});
    }}

    function drawStars(cx, cy, rot) {{
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot);
        ctx.fillStyle = "white";
        stars.forEach(s => {{
            ctx.beginPath();
            ctx.arc(s.x * canvas.width, s.y * canvas.height, s.size, 0, Math.PI*2);
            ctx.fill();
        }});
        ctx.restore();
    }}

    function drawRing(cx, cy, ringR) {{
        ctx.save(); ctx.translate(cx, cy);
        // 외벽
        ctx.strokeStyle = "#253145"; ctx.lineWidth = 40;
        ctx.beginPath(); ctx.arc(0, 0, ringR, 0, Math.PI*2); ctx.stroke();
        // 안쪽 라인
        ctx.strokeStyle = "#1a1f2e"; ctx.lineWidth = 15;
        ctx.beginPath(); ctx.arc(0, 0, ringR-20, 0, Math.PI*2); ctx.stroke();
        ctx.restore();
    }}

    function drawAstronaut(x, y, rot) {{
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot);
        ctx.fillStyle = "white";
        // 본체 (이미지의 심플한 스타일)
        ctx.beginPath(); ctx.roundRect(-8, -14, 16, 22, 4); ctx.fill();
        // 헬멧
        ctx.fillStyle = "#333"; ctx.beginPath(); ctx.roundRect(-6, -12, 12, 6, 2); ctx.fill();
        ctx.restore();
    }}

    function drawArrow(x, y, len, ang, color, label) {{
        ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
        ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(len, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(len, 0); ctx.lineTo(len-12, -6); ctx.lineTo(len-12, 6); ctx.closePath(); ctx.fill();
        // 텍스트Label
        ctx.rotate(-ang); ctx.font = "bold 15px Pretendard"; ctx.shadowBlur=2; ctx.shadowColor="black";
        ctx.fillText(label, 20, -15);
        ctx.restore();
    }}

    function render() {{
        ctx.fillStyle = "black"; ctx.fillRect(0, 0, canvas.width, canvas.height);
        const cx = canvas.width / 2;
        const cy = canvas.height / 2;
        const baseR = 200; // 시뮬레이션용 반지름 스케일
        
        angle += omega * 0.016; 

        if(!isRotatingFrame) {{
            // ── 관성계 ──
            drawStars(cx, cy, 0); // 배경 고정
            drawRing(cx, cy, baseR); // 정거장 회전은 우주인 위치로 표현
            
            const ax = cx + Math.cos(angle) * (baseR - 10);
            const ay = cy + Math.sin(angle) * (baseR - 10);
            drawAstronaut(ax, ay, angle - Math.PI/2);
            
            // 수직항력 (이미지처럼 빨간색, 중심 방향)
            const arrowLen = Math.max(40, accelVal * 1.5);
            drawArrow(ax, ay, arrowLen, angle + Math.PI, "#ef4444", "수직항력 (N)");
            
        }} else {{
            // ── 비관성계 ──
            drawStars(cx, cy, -angle); // 배경 역회전 (핵심!)
            drawRing(cx, cy, baseR); // 정거장 고정 (핵심!)
            
            const ax = cx + (baseR - 10); // 3시 방향 고정
            const ay = cy;
            drawAstronaut(ax, ay, -Math.PI/2);
            
            const arrowLen = Math.max(40, accelVal * 1.5);
            // 원심력 (비관성계에만 존재, 바깥 방향)
            drawArrow(ax, ay, arrowLen, 0, "#10b981", "원심력 (Centrifugal Force)");
            // 수직항력 (안쪽 방향)
            drawArrow(ax, ay, arrowLen, Math.PI, "#ef4444", "수직항력 (N)");
        }}

        requestAnimationFrame(render);
    }}
    render();
</script>
</body>
</html>
"""

components.html(html_content, height=600, scrolling=False)

# ── 하단 탐구 섹션 복원 ──
st.markdown("---")
st.markdown("### 🔍 회전하는 우주 정거장 속의 물리 탐구")

# 비교 분석 테이블 (사용자가 제공한 첫 번째 이미지 내용 기준)
st.markdown("""
<style>
    .physics-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
    .physics-table th { background: #f4f6f9; color: #333; padding: 12px; font-weight: 800; border: 1px solid #ddd; }
    .physics-table td { background: white; padding: 12px; border: 1px solid #ddd; text-align: center; }
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
            <td style="background:#f9f9f9; font-weight:700;">우주인의 운동</td>
            <td style="color:#3b82f6;">등속 원운동 진행</td>
            <td>관찰자와 함께 <b>정지</b>한 상태</td>
        </tr>
        <tr>
            <td style="background:#f9f9f9; font-weight:700;">작용하는 힘</td>
            <td style="color:#ef4444;">수직항력 (N)</td>
            <td><span style="color:#ef4444;">수직항력(N)</span> + <span style="color:#10b981;">원심력 (Inertial Force)</span></td>
        </tr>
        <tr>
            <td style="background:#f9f9f9; font-weight:700;">운동의 해석</td>
            <td>수직항력이 <b>구심력</b>이 되어 원운동 유발</td>
            <td>수직항력과 원심력이 <b>평형</b>을 이룸</td>
        </tr>
    </tbody>
</table>
""", unsafe_allow_html=True)

# 쿠퍼 스테이션 이미지 섹션 (학습용)
st.markdown("#### 🪐 쿠퍼 스테이션 물리 모델")
col1, col2 = st.columns(2)
with col1:
    img_ext = base_path + "cooper_exterior.png"
    if os.path.exists(img_ext): st.image(img_ext, caption="Cooper Station Exterior", use_container_width=True)
with col2:
    img_int = base_path + "cooper_interior.png"
    if os.path.exists(img_int): st.image(img_int, caption="Cooper Station Interior", use_container_width=True)

st.markdown("""
> **참고**: 영화 '인터스텔라'의 쿠퍼 스테이션 시나리오에서는 반지름 $r=1,000m$인 거대 원통형 구조물이 회전합니다. 
> 위 시뮬레이션에서 반지름을 늘리고 각속도를 조절하여 $9.8m/s^2$ (지구 중력)에 도달하는 조건을 직접 찾아보세요.
""")

def show():
    pass

if __name__ == "__main__":
    show()
