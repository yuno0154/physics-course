import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="아인슈타인의 중력: 시공간의 마술", layout="wide")

# 에셋 경로 설정 (상대 경로 및 환경 호환성 확보)
current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

img_blackhole = os.path.join(assets_dir, "blackhole.png")
img_reunion = os.path.join(assets_dir, "reunion.png")
img_logic = os.path.join(assets_dir, "disk_logic.png")

# HTML/JavaScript 공통 템플릿
HTML_TEMPLATE = """
<div id="root" style="width: 100%; height: 500px; overflow: hidden; background: #05070a; border-radius: 12px;"></div>
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

/* ── 별 배경 ── */
const STARS = Array.from({length:100},(_,i)=>{
    const s=(n)=>{let x=Math.sin(n)*43758.54;return x-Math.floor(x);};
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.2)*1.2+0.2, ph:s(i*5)*Math.PI*2 };
});

const drawStars = (ctx, W, H, t) => {
    STARS.forEach(st=>{
        const op = 0.15 + 0.35*Math.sin(st.ph+t*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
};

/* ── 시공간 격자 (Grid) ── */
function drawGrid(ctx, W, H, mode, sunX, sunY) {
    ctx.save();
    ctx.strokeStyle = mode === 'newton' ? 'rgba(100, 116, 139, 0.4)' : 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 1.0;
    const step = 45;
    const cols = Math.ceil(W/step) + 2;
    const rows = Math.ceil(H/step) + 2;

    for (let i = -1; i <= cols; i++) {
        ctx.beginPath();
        for (let j = -1; j <= rows; j++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const distDist = Math.sqrt(dx*dx + dy*dy);
                const force = 3000 / (distDist + 50); 
                px -= (dx / (distDist + 1)) * force;
                py -= (dy / (distDist + 1)) * force;
            }
            if (j === -1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    for (let j = -1; j <= rows; j++) {
        ctx.beginPath();
        for (let i = -1; i <= cols; i++) {
            let px = i * step, py = j * step;
            if (mode === 'einstein') {
                const dx = px - sunX, dy = py - sunY;
                const distDist = Math.sqrt(dx*dx + dy*dy);
                const force = 3000 / (distDist + 50);
                px -= (dx / (distDist + 1)) * force;
                py -= (dy / (distDist + 1)) * force;
            }
            if (i === -1) ctx.moveTo(px, py); else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

/* ── 에딩턴의 일식 ── */
function drawEddington(ctx, W, H, mode, t) {
    const sunX = W * 0.5, sunY = H * 0.3, sunR = 50; 
    const earthX = W * 0.5, earthY = H * 0.75; // 잘림 방지를 위해 대폭 상향
    drawGrid(ctx, W, H, mode, sunX, sunY);
    drawStars(ctx, W, H, t);
    
    const starRealX = sunX + 5, starRealY = H * 0.08;
    const prog = (t * 0.0006) % 1;

    if(mode === 'newton') {
        ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1.5; ctx.setLineDash([5,5]);
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.lineTo(earthX, earthY); ctx.stroke(); ctx.setLineDash([]);
        const hitSunY = sunY - sunR * 0.92;
        const currentT = Math.min(prog / 0.4, 1); 
        const beamY = starRealY + (hitSunY - starRealY) * currentT;
        ctx.save(); ctx.shadowBlur = 10; ctx.shadowColor = '#fff';
        ctx.beginPath(); ctx.arc(starRealX, beamY, 3.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
    } else {
        ctx.strokeStyle = '#6366f1'; ctx.lineWidth = 3; 
        const cpX = sunX + 130, cpY = sunY;
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.quadraticCurveTo(cpX, cpY, earthX, earthY); ctx.stroke();
        const appStarX = sunX + 220, appStarY = 35; 
        ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.setLineDash([6,4]);
        ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(appStarX, appStarY); ctx.stroke(); ctx.setLineDash([]);
        const px = (1-prog)*(1-prog)*starRealX + 2*(1-prog)*prog*cpX + prog*prog*earthX;
        const py = (1-prog)*(1-prog)*starRealY + 2*(1-prog)*prog*cpY + prog*prog*earthY;
        ctx.save(); ctx.shadowBlur = 15; ctx.shadowColor = '#6366f1';
        ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.save(); ctx.shadowBlur=20; ctx.shadowColor='#818cf8';
        ctx.beginPath(); ctx.arc(appStarX, appStarY, 7, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
    }
    
    // Sun
    const sg = ctx.createRadialGradient(sunX, sunY, sunR*0.7, sunX, sunY, sunR*1.7);
    sg.addColorStop(0, 'rgba(253, 224, 71, 0.5)'); sg.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR*1.7, 0, Math.PI*2); ctx.fillStyle=sg; ctx.fill();
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR, 0, Math.PI*2); ctx.fillStyle='#000'; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.4)'; ctx.lineWidth=1.5; ctx.stroke();

    // Earth (고가용성 위치)
    const eg = ctx.createRadialGradient(earthX-5, earthY-5, 3, earthX, earthY, 25);
    eg.addColorStop(0,'#3b82f6'); eg.addColorStop(1,'#1e3a8a');
    ctx.beginPath(); ctx.arc(earthX, earthY, 25, 0, Math.PI*2); ctx.fillStyle=eg; ctx.fill();
    ctx.fillStyle='#fff'; ctx.font='bold 14px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('지구 (관측자)', earthX, earthY + 45);
}

/* ── 시간 대시보드 ── */
function drawDashboard(ctx, clocks) {
    const sX = 15, sY = 15, bW = 180, bH = 160;
    ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
    ctx.strokeStyle = 'rgba(99, 102, 241, 0.6)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.rect(sX, sY, bW, bH); ctx.fill(); ctx.stroke();
    
    ctx.fillStyle = '#fff'; ctx.font = 'bold 14px Noto Sans KR'; ctx.textAlign = 'center';
    ctx.fillText('🕒 시간 지연 비교', sX + bW/2, sY + 25);
    
    const renderClock = (y, label, time, color) => {
        ctx.save(); ctx.translate(sX + 30, y);
        ctx.beginPath(); ctx.arc(0, 0, 14, 0, Math.PI*2); ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, 0); ctx.rotate(time * 0.002); ctx.lineTo(0, -11); ctx.stroke();
        ctx.restore();
        ctx.fillStyle = color; ctx.font = 'bold 12px Noto Sans KR'; ctx.textAlign = 'left';
        ctx.fillText(label, sX + 55, y - 5);
        ctx.font = '12px monospace'; ctx.fillText(time.toFixed(1), sX + 55, y + 10);
    };

    renderClock(sY + 60, 'A (지면/정지)', clocks.A, '#3b82f6');
    renderClock(sY + 100, 'B (중심/회전)', clocks.B, '#10b981');
    renderClock(sY + 140, 'C (가장자리)', clocks.C, '#f59e0b');
}

/* ── 회전 원판 ── */
function drawRotatingDisk(ctx, W, H, vel, t, clocks, pov) {
    const cx = W*0.5, cy = H*0.45, r = 160; 
    const ang = t * 0.001 * vel;

    drawStars(ctx, W, H, t);

    ctx.save();
    if (pov === 'B') { ctx.translate(cx, cy); }
    else if (pov === 'C') {
        ctx.translate(cx, cy); ctx.rotate(-ang);
        ctx.translate(-r * 0.85, 0); ctx.translate(cx, cy);
    } else { ctx.translate(cx, cy); ctx.rotate(ang); }
    
    const grad = ctx.createRadialGradient(0,0, r*0.8, 0,0, r);
    grad.addColorStop(0, 'rgba(30, 41, 59, 0.9)'); grad.addColorStop(1, 'rgba(71, 85, 105, 0.4)');
    ctx.beginPath(); ctx.arc(0,0, r, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth = 2; ctx.stroke();
    
    for(let i=0; i<360; i+=30) {
        const rad = i*Math.PI/180;
        ctx.beginPath(); ctx.moveTo(r*0.85*Math.cos(rad), r*0.85*Math.sin(rad));
        ctx.lineTo(r*Math.cos(rad), r*Math.sin(rad)); ctx.stroke();
    }
    ctx.beginPath(); ctx.arc(0,0, 10, 0, Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    const cx_off = r * 0.85, cy_off = 0;
    ctx.beginPath(); ctx.arc(cx_off, cy_off, 10, 0, Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    
    if (pov === 'C') {
        ctx.strokeStyle='#ef4444'; ctx.lineWidth=4;
        ctx.beginPath(); ctx.moveTo(cx_off, cy_off); ctx.lineTo(cx_off + 40, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx_off+40, 0); ctx.lineTo(cx_off+32, -6); ctx.lineTo(cx_off+32, 6); ctx.closePath(); ctx.fillStyle='#ef4444'; ctx.fill();
    }
    ctx.restore();

    if (pov === 'A') {
        const ax = cx - r - 60, ay = cy;
        ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
    } else {
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang);
        const ax = -r - 60, ay = 0;
        ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
        ctx.restore();
    }

    drawDashboard(ctx, clocks);
}

const Main = () => {
    const canvasRef = React.useRef(null);
    const [t, setT] = React.useState(0);
    const [clocks, setClocks] = React.useState({ A: 0, B: 0, C: 0 });

    React.useEffect(() => {
        let frame;
        const loop = (t_val) => {
            setT(t_val);
            setClocks(prev => {
                const speed = (window.stParams?.speed || 1);
                const discVel = (window.stParams?.discVel || 1);
                const factorC = Math.max(0.1, 1 - (discVel * 0.08)); 
                return { A: prev.A + 0.1 * speed, B: prev.B + 0.1 * speed, C: prev.C + 0.1 * speed * factorC };
            });
            frame = requestAnimationFrame(loop);
        };
        frame = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(frame);
    }, []);

    React.useEffect(() => {
        const ctx = canvasRef.current.getContext('2d');
        const W = 800, H = 500;
        const mode = window.stParams?.mode || 'eddington';
        const pov = window.stParams?.pov || 'A';
        ctx.clearRect(0, 0, W, H);
        if (mode === 'eddington') {
            const theory = window.stParams?.theory || 'newton';
            drawEddington(ctx, W, H, theory, t);
        } else {
            const discVel = window.stParams?.discVel || 1;
            drawRotatingDisk(ctx, W, H, discVel, t, clocks, pov);
        }
    }, [t, clocks]);

    return <canvas ref={canvasRef} width={800} height={500} style={{ width: '100%', height: '500px', borderRadius: '12px' }} />;
};

ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
body { font-family: 'Noto Sans KR', sans-serif; background: transparent; margin: 0; padding: 0; overflow: hidden; }
</style>
"""

def render_ui():
    st.markdown("### 🌌 아인슈타인의 중력: 시공간과 시간의 비밀")
    
    tab1, tab2 = st.tabs(["🔭 에딩턴의 일식", "🎡 회전 원판 심층 탐구"])
    
    with tab1:
        col1, col2 = st.columns([1, 2.5])
        with col1:
            st.info("**에딩턴의 일식 실험 (1919)**")
            theory = st.radio("물리 모델 선택", ["newton", "einstein"], 
                              format_func=lambda x: "뉴턴 (평평한 시공간)" if x=="newton" else "아인슈타인 (휘어진 시공간)")
            st.write("---")
            st.markdown("빛의 굴절을 통해 질량이 시공간을 어떻게 휘게 만드는지 확인해 보세요.")
        with col2:
            components.html(f"<script>window.stParams = {{ mode: 'eddington', theory: '{theory}' }};</script>" + HTML_TEMPLATE, height=520)

    with tab2:
        col_c, col_v = st.columns([1.2, 2.5])
        with col_c:
            st.success("**회전 원판: 관찰자 논리 탐구**")
            pov = st.radio("관찰 시점(POV) 선택", ["A", "B", "C"], index=0)
            disc_vel = st.slider("원판 회전 속도 (ω)", 0.5, 10.0, 5.0)
            st.write("---")
            st.markdown("**🔍 상대적 관찰 결과**")
            inquiry_data = [
                {"관찰 시점": "A (지면/정지)", "관찰 대상(C)의 운동": "빠른 원운동", "C의 시간 지연 원인": "속도 (특수 상대성)"},
                {"관찰 시점": "B (중심/회전)", "관찰 대상(C)의 운동": "정지", "C의 시간 지연 원인": "가속계 시차 (일반 상대성)"},
                {"관찰 시점": "C (끝단/가속)", "관찰 대상(C)의 운동": "자신은 정지", "C의 시간 지연 원인": "강한 관성력 (등가 원리)"}
            ]
            st.table(inquiry_data)
        with col_v:
            components.html(f"<script>window.stParams = {{ mode: 'disk', pov: '{pov}', discVel: {disc_vel}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=520)

    st.write("---")
    st.markdown("#### 🎬 영화 '인터스텔라'로 배우는 일반 상대성 이론")
    c1, c2 = st.columns(2)
    with c1:
        st.image(img_blackhole, use_container_width=True, caption="블랙홀 가르강튀아와 시공간의 굴절")
        st.markdown("**1. 밀러 행성의 시간** : 거대 질량 주변의 극심한 시공간 왜곡으로 인해 시간이 매우 천천히 흐릅니다.")
    with c2:
        st.image(img_reunion, use_container_width=True, caption="시간의 상대성이 만든 재회")
        st.markdown("**2. 상대적인 시간** : 시간은 절대적이지 않으며, 중력과 운동 상태에 따라 다르게 흐르는 상대적인 양입니다.")
    
    st.info("💡 **GPS 위성 보정**: GPS 위성은 지상보다 시간이 매일 약 38마이크로초 빨리 흐르며, 이를 상대성 이론으로 보정하지 않으면 하루에 10km 이상의 오차가 발생합니다.")

if __name__ == "__main__":
    render_ui()
