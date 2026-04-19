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
<div id="root"></div>
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
    ctx.lineWidth = 1.2;
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
                const force = 3500 / (distDist + 60); 
                px -= (dx / (distDist + 1)) * force;
                py -= (dy / (distDist + 1)) * force;
            }
            if (j === -1) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
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
                const force = 3500 / (distDist + 60);
                px -= (dx / (distDist + 1)) * force;
                py -= (dy / (distDist + 1)) * force;
            }
            if (i === -1) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.stroke();
    }
    ctx.restore();
}

/* ── 에딩턴의 일식 ── */
function drawEddington(ctx, W, H, mode, t) {
    const sunX = W * 0.5, sunY = H * 0.4, sunR = 60;
    const earthX = W * 0.5, earthY = H * 0.82; // 지구가 잘리지 않도록 위치 상향 조정
    drawGrid(ctx, W, H, mode, sunX, sunY);
    drawStars(ctx, W, H, t);
    
    // 별의 실제 위치
    const starRealX = sunX + 5, starRealY = H * 0.08;
    const prog = (t * 0.0006) % 1;

    if(mode === 'newton') {
        ctx.strokeStyle = 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1.5; ctx.setLineDash([5,5]);
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.lineTo(earthX, earthY); ctx.stroke(); ctx.setLineDash([]);
        const hitSunY = sunY - sunR * 0.92;
        const currentT = Math.min(1, prog / 0.4); 
        const beamY = starRealY + (hitSunY - starRealY) * currentT;
        ctx.save(); ctx.shadowBlur = 10; ctx.shadowColor = '#fff';
        ctx.beginPath(); ctx.arc(starRealX, beamY, 3.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='#f87171'; ctx.font='bold 15px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText('뉴턴: 평평한 시공간 (빛의 직진)', sunX, sunY - 120);
        ctx.fillText('→ 태양에 빛이 차단됨', sunX, sunY - 98);
    } else {
        ctx.strokeStyle = '#6366f1'; ctx.lineWidth = 3; 
        const cpX = sunX + 130, cpY = sunY;
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.quadraticCurveTo(cpX, cpY, earthX, earthY); ctx.stroke();
        const appStarX = sunX + 220, appStarY = 40; 
        ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.setLineDash([6,4]);
        ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(appStarX, appStarY); ctx.stroke(); ctx.setLineDash([]);
        const qt = prog;
        const px = (1-qt)*(1-qt)*starRealX + 2*(1-qt)*qt*cpX + qt*qt*earthX;
        const py = (1-qt)*(1-qt)*starRealY + 2*(1-qt)*qt*cpY + qt*qt*earthY;
        ctx.save(); ctx.shadowBlur = 15; ctx.shadowColor = '#6366f1';
        ctx.beginPath(); ctx.arc(px, py, 4.5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.save(); ctx.shadowBlur=20; ctx.shadowColor='#818cf8';
        ctx.beginPath(); ctx.arc(appStarX, appStarY, 7, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill(); ctx.restore();
        ctx.fillStyle='#fff'; ctx.font='bold 14px Noto Sans KR'; ctx.textAlign='left';
        ctx.fillText('관측된 겉보기 위치', appStarX + 15, appStarY + 5);
        ctx.fillStyle='#818cf8'; ctx.font='bold 16px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText('아인슈타인: 휘어진 시공간 (빛의 우회)', sunX, sunY - 140);
    }
    ctx.beginPath(); ctx.arc(starRealX, starRealY, 6, 0, Math.PI*2); ctx.fillStyle='#fbbf24'; ctx.fill();
    ctx.fillStyle='#fbbf24'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='right';
    ctx.fillText('실제 위치   ', starRealX - 8, starRealY + 5);
    
    // 태양/달
    const sg = ctx.createRadialGradient(sunX, sunY, sunR*0.7, sunX, sunY, sunR*1.7);
    sg.addColorStop(0, 'rgba(253, 224, 71, 0.5)'); sg.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR*1.7, 0, Math.PI*2); ctx.fillStyle=sg; ctx.fill();
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR, 0, Math.PI*2); ctx.fillStyle='#000'; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.4)'; ctx.lineWidth=1.5; ctx.stroke();

    // 지구 (위치 및 크기 최적화)
    const eg = ctx.createRadialGradient(earthX-6, earthY-6, 3, earthX, earthY, 28);
    eg.addColorStop(0,'#3b82f6'); eg.addColorStop(1,'#1e3a8a');
    ctx.beginPath(); ctx.arc(earthX, earthY, 28, 0, Math.PI*2); ctx.fillStyle=eg; ctx.fill();
}

/* ── 회전 원판 (관찰자 POV 강화) ── */
function drawRotatingDisk(ctx, W, H, vel, t, clocks, discStep, pov) {
    const cx = W*0.5, cy = H*0.5, r = 220;
    const ang = t * 0.001 * vel;

    // 배경 처리 (B나 C의 시점에서는 우주가 회전함)
    if (pov === 'B' || pov === 'C') {
        ctx.save(); ctx.translate(cx, cy); ctx.rotate(-ang); ctx.translate(-cx, -cy);
        drawStars(ctx, W, H, t); ctx.restore();
    } else {
        drawStars(ctx, W, H, t);
    }

    ctx.save();
    // 시점(POV)에 따른 캔버스 변환
    if (pov === 'B') {
        ctx.translate(cx, cy); // 중심에 고정
    } else if (pov === 'C') {
        ctx.translate(cx, cy); ctx.rotate(-ang); // 자신(C)이 정지한 것처럼 보이기 위해 원판 회전 상쇄
        ctx.translate(-r * 0.85, 0); // 자신이 12시 혹은 3시 방향에 있다고 가정하고 중심으로 이동
        ctx.translate(cx, cy); // 다시 화면 중심으로
    } else {
        ctx.translate(cx, cy); ctx.rotate(ang); // 지면(A)에서 볼 때 원판이 회전함
    }
    
    const grad = ctx.createRadialGradient(0,0, r*0.8, 0,0, r);
    grad.addColorStop(0, 'rgba(30, 41, 59, 0.9)'); grad.addColorStop(1, 'rgba(71, 85, 105, 0.4)');
    ctx.beginPath(); ctx.arc(0,0, r, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=2; ctx.stroke();
    
    // 격자 및 눈금
    for(let i=0; i<360; i+=30) {
        const rad = i*Math.PI/180;
        ctx.beginPath(); ctx.moveTo(r*0.85*Math.cos(rad), r*0.85*Math.sin(rad));
        ctx.lineTo(r*Math.cos(rad), r*Math.sin(rad)); ctx.stroke();
    }
    
    // 관찰자 B (중심)
    ctx.beginPath(); ctx.arc(0,0, 10, 0, Math.PI*2); ctx.fillStyle='#10b981'; ctx.fill();
    drawLabel(ctx, 0, -20, 'Observer B');
    drawSmallClock(ctx, 0, 15, clocks.B, '#10b981');

    // 관찰자 C (가장자리)
    const cx_off = r * 0.85, cy_off = 0;
    ctx.beginPath(); ctx.arc(cx_off, cy_off, 10, 0, Math.PI*2); ctx.fillStyle='#f59e0b'; ctx.fill();
    drawLabel(ctx, cx_off, -20, 'Observer C');
    drawSmallClock(ctx, cx_off, 15, clocks.C, '#f59e0b');
    
    // 가속도/관성력 벡터 (C의 시점에서 특히 강조)
    if (pov === 'C' || discStep >= 3) {
        ctx.strokeStyle='#ef4444'; ctx.lineWidth=4;
        ctx.beginPath(); ctx.moveTo(cx_off, cy_off); ctx.lineTo(cx_off + 50, 0); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx_off+50, 0); ctx.lineTo(cx_off+42, -6); ctx.lineTo(cx_off+42, 6); ctx.closePath(); ctx.fillStyle='#ef4444'; ctx.fill();
        ctx.fillStyle='#ef4444'; ctx.font='bold 14px Noto Sans KR'; ctx.fillText('강력한 가속도(중력)', cx_off+10, 40);
    }
    ctx.restore();

    // 관찰자 A (지면 - POV가 A일 때만 정적 위치에 표시)
    if (pov === 'A') {
        const ax = cx - r - 80, ay = cy;
        ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
        drawLabel(ctx, ax, -20, 'Observer A (Ground)');
        drawSmallClock(ctx, ax, 15, clocks.A, '#3b82f6');
    } else {
        // B나 C의 시점에서는 지면(A)이 외부에서 회전함
        ctx.save();
        ctx.translate(cx, cy); ctx.rotate(-ang);
        const ax = -r - 80, ay = 0;
        ctx.beginPath(); ctx.arc(ax, ay, 10, 0, Math.PI*2); ctx.fillStyle='#3b82f6'; ctx.fill();
        drawLabel(ctx, ax, -20, 'A (Moving)');
        drawSmallClock(ctx, ax, 15, clocks.A, '#3b82f6');
        ctx.restore();
    }

    ctx.fillStyle = '#fff'; ctx.font = '16px Noto Sans KR'; ctx.textAlign = 'center';
    let msg = pov === 'A' ? "관찰자 A의 시점: 지면에서 원판의 회전을 바라보고 있습니다." :
              pov === 'B' ? "관찰자 B의 시점: 회전 중심에서 가속도 없이 외부를 바라봅니다." :
                            "관찰자 C의 시점: 회전하는 가속 계 내부에서 중력(원심력)을 느낍니다.";
    ctx.fillText(msg, W*0.5, H - 30);
}

function drawLabel(ctx, x, y, txt) {
    ctx.fillStyle='#fff'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText(txt, x, y);
}

function drawSmallClock(ctx, x, y, time, color) {
    ctx.save(); ctx.translate(x, y + 25);
    ctx.beginPath(); ctx.arc(0,0, 20, 0, Math.PI*2); ctx.strokeStyle=color; ctx.lineWidth=2; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0,0); ctx.rotate(time * 0.002); ctx.lineTo(0, -15); ctx.stroke();
    ctx.restore();
    ctx.fillStyle=color; ctx.font='12px monospace'; ctx.fillText(time.toFixed(1), x, y + 60);
}

const Main = () => {
    const canvasRef = React.useRef(null);
    const [t, setT] = React.useState(0);
    const [clocks, setClocks] = React.useState({ A: 0, B: 0, C: 0 });

    React.useEffect(() => {
        let frame;
        const loop = (time) => {
            setT(time);
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
        const { width: W, height: H } = canvasRef.current;
        const mode = window.stParams?.mode || 'eddington';
        const discStep = window.stParams?.discStep || 1;
        const pov = window.stParams?.pov || 'A';
        ctx.clearRect(0, 0, W, H);
        if (mode === 'eddington') {
            const theory = window.stParams?.theory || 'newton';
            drawEddington(ctx, W, H, theory, t);
        } else {
            const discVel = window.stParams?.discVel || 1;
            drawRotatingDisk(ctx, W, H, discVel, t, clocks, discStep, pov);
        }
    }, [t, clocks]);

    return <canvas ref={canvasRef} width={800} height={600} style={{ width: '100%', height: 'auto', borderRadius: '12px' }} />;
};

ReactDOM.render(<Main />, document.getElementById('root'));
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;700&display=swap');
body { font-family: 'Noto Sans KR', sans-serif; background: transparent; margin: 0; padding: 0; overflow: hidden; }
</style>
"""

def render_ui():
    st.markdown("### 🌌 아인슈타인의 중력: 시공간과 시간의 비밀")
    
    tab1, tab2 = st.tabs(["🔭 에딩턴의 일식", "🎡 회전 원판 심층 탐구"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info("**에딩턴의 일식 실험 (1919)**")
            theory = st.radio("물리 모델 선택", ["newton", "einstein"], 
                              format_func=lambda x: "뉴턴 (평평한 시공간)" if x=="newton" else "아인슈타인 (휘어진 시공간)")
            st.write("---")
            if theory == 'newton':
                st.markdown("빛은 질량이 없으므로 중력의 영향을 받지 않고 직진하며, 태양 뒤의 별은 보이지 않아야 합니다.")
            else:
                st.markdown("중력은 공간을 휘게 하며, 빛은 휘어진 공간을 따라 굴절되어 보이지 않아야 할 별이 관측됩니다.")
        with col2:
            components.html(f"<script>window.stParams = {{ mode: 'eddington', theory: '{theory}' }};</script>" + HTML_TEMPLATE, height=620)

    with tab2:
        col_c, col_v = st.columns([1, 2])
        with col_c:
            st.success("**회전 원판: 3대 관찰자 관점**")
            pov = st.radio("관찰 시점(POV) 선택", ["A", "B", "C"], 
                           format_func=lambda x: f"관찰자 {x} (지면)" if x=="A" else (f"관찰자 {x} (중심)" if x=="B" else f"관찰자 {x} (가장자리)"))
            
            disc_vel = st.slider("회전 속도 (ω)", 0.5, 10.0, 4.0)
            st.write("---")
            if pov == "A":
                st.markdown("**POV A (지면)**: 정지된 상태에서 회전하는 원판을 봅니다. 움직이는 C의 시계가 가장 느리게 가는 것을 확인할 수 있습니다.")
            elif pov == "B":
                st.markdown("**POV B (중심)**: 회전하는 축에 서서 봅니다. 우주 전체가 회전하는 것처럼 보이며, C와 자신의 거리는 일정합니다.")
            else:
                st.markdown("**POV C (가장자리)**: 자신이 정지해 있다고 느끼지만, 강력한 **원심력(가속도)**을 받습니다. 등가 원리에 의해 이는 중력을 받는 것과 같으며, 시간이 가장 느리게 흐릅니다.")
        
        with col_v:
            components.html(f"<script>window.stParams = {{ mode: 'disk', pov: '{pov}', discVel: {disc_vel}, speed: 1.0 }};</script>" + HTML_TEMPLATE, height=620)

    # 인터스텔라 스토리 섹션 (하단에 별도로 크게 배치)
    st.write("---")
    st.markdown("#### 🎬 영화 '인터스텔라'로 배우는 일반 상대성 이론")
    
    col_img1, col_txt1 = st.columns([1, 1.2])
    with col_img1:
        st.image(img_blackhole, use_container_width=True)
    with col_txt1:
        st.markdown("""
        ##### 1. 블랙홀 '가르강튀아'와 밀러 행성
        밀러 행성은 거대 블랙홀 Gargantua와 매우 가깝습니다. 블랙홀의 엄청난 질량은 주변 시공간을 극도로 휘게 만들며, 이 '기하학적 왜곡'은 곧 시간의 흐름을 늦춥니다.
        
        - **현상**: 밀러 행성에서의 1시간은 지구에서의 약 7년과 같습니다.
        - **이유**: 중력이 강할수록 시공간의 곡률이 커지며, 시간의 밀도가 높아지기 때문입니다.
        """)

    st.write("")
    col_txt2, col_img2 = st.columns([1.2, 1])
    with col_txt2:
        st.markdown("""
        ##### 2. 시간의 강을 건너온 재회
        쿠퍼 대장이 우주를 여행하고 돌아왔을 때, 그는 여전히 젊지만 그의 딸 머피는 임종을 앞둔 노인이 되어 있습니다.
        
        - **의미**: 시간은 우주 어디에서나 일정하게 흐르는 것이 아니라, 관찰자의 위치(중력)와 운동 상태에 따라 달라지는 **상대적인 양**입니다.
        - **교훈**: 아인슈타인은 중력을 힘이 아닌 '시공간의 기하학적 형태'로 정의함으로써 현대 우주론의 기초를 닦았습니다.
        """)
    with col_img2:
        st.image(img_reunion, use_container_width=True)

    st.info("💡 **실생활 팁**: 우리가 매일 쓰는 스마트폰의 GPS도 일반 상대성 이론(중력에 의한 시간 지연)과 특수 상대성 이론(속도에 의한 시간 지연)을 모두 계산하여 보정하고 있습니다. 만약 이를 무시한다면 하루에 약 10km의 위치 오차가 발생하게 됩니다.")

if __name__ == "__main__":
    render_ui()
