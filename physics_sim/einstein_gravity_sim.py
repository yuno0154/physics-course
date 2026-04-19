import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="학습주제 5. 아인슈타인의 중력과 시간 지연", layout="wide")

def run_sim():
    st.title("🌌 학습주제 5. 아인슈타인의 중력과 시간 탐구")
    st.markdown("질량이 어떻게 시공간을 휘게 만드는지(에딩턴 실험), 그리고 그 결과 시간이 어떻게 다르게 흐르는지(시간 지연) 탐구합니다.")

    # React 기반 통합 시뮬레이션 코드
    react_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;800;900&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#05070a;color:#e2e8f0;padding:20px;overflow-x:hidden;}
.panel{background:rgba(13,21,38,0.7);border:1px solid rgba(100,120,255,0.22);border-radius:18px;padding:24px;backdrop-filter:blur(10px);}
.card{background:rgba(15,23,42,0.6);border:1px solid rgba(255,255,255,0.08);border-radius:18px;padding:24px;}
.tab-btn{padding:10px 18px;border-radius:10px;border:1px solid rgba(255,255,255,0.1);background:transparent;color:#94a3b8;cursor:pointer;font-size:14px;transition:all 0.3s;}
.tab-btn.active{background:rgba(99,102,241,0.15);border-color:#6366f1;color:#fff;font-weight:700;box-shadow:0 4px 12px rgba(99,102,241,0.25);}
label{font-size:12px;color:#818cf8;font-weight:800;letter-spacing:0.05em;display:block;margin-bottom:8px;text-transform:uppercase;}
.control-box{background:rgba(255,255,255,0.03);border-radius:12px;padding:15px;margin-bottom:15px;border:1px solid rgba(255,255,255,0.05);}
input[type=range]{-webkit-appearance:none;width:100%;height:4px;background:#1e293b;border-radius:2px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#6366f1;cursor:pointer;box-shadow:0 0 10px rgba(99,102,241,0.6);}
.theory-box{border-left:4px solid #6366f1;padding-left:15px;margin-top:15px;font-size:14px;line-height:1.7;color:#94a3b8;}
.clock-display{font-family:'Space Mono',monospace;font-size:22px;color:#38bdf8;text-shadow:0 0 10px rgba(56,189,248,0.4);}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef, useCallback } = React;

/* ── KaTeX ── */
const Eq = ({ f, display=false }) => {
    const ref = useRef(null);
    useEffect(()=>{
        if(ref.current && window.katex)
            window.katex.render(f, ref.current, {throwOnError:false, displayMode:display});
    },[f,display]);
    return <span ref={ref}/>;
};

/* ══════════════════════════════════════════
   시뮬레이션 전역 상수
══════════════════════════════════════════ */
const STARS = Array.from({length:120},(_,i)=>{
    const s=(n)=>{let x=Math.sin(n)*43758.54;return x-Math.floor(x);};
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.2)*1.3+0.3, ph:s(i*5)*Math.PI*2 };
});

const drawStars = (ctx, W, H, t) => {
    STARS.forEach(st=>{
        const op = 0.2 + 0.4*Math.sin(st.ph+t*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
};

/* ══════════════════════════════════════════
   Scenario 1: 에딩턴의 일식 (시공간 휨 증거)
══════════════════════════════════════════ */
function drawEddington(ctx, W, H, mode, t) {
    drawStars(ctx, W, H, t);
    const sunX = W * 0.5, sunY = H * 0.4, sunR = 60;
    
    // 타겟 별 위치 (태양 뒤편 옆쪽)
    const starRealX = sunX + 180, starRealY = sunY - 220;
    const earthX = W * 0.5, earthY = H * 0.95;

    // 태양/달 (일식 연출)
    const moonX = sunX + Math.sin(t*0.0002)*2, moonY = sunY;
    
    // 빛의 경로
    ctx.lineWidth = 1.5; ctx.setLineDash([5,5]);
    if(mode === 'newton') {
        // 직선 경로
        ctx.strokeStyle = 'rgba(255,255,255,0.4)';
        ctx.beginPath(); ctx.moveTo(starRealX, starRealY); ctx.lineTo(earthX, earthY); ctx.stroke();
    } else {
        // 휘어진 경로 (베지어 곡선으로 과장 연출)
        ctx.strokeStyle = '#60a5fa'; ctx.setLineDash([]);
        ctx.beginPath();
        ctx.moveTo(starRealX, starRealY);
        // 태양 근처를 지날 때 급격히 휨
        ctx.quadraticCurveTo(sunX + 60, sunY - 60, earthX, earthY);
        ctx.stroke();

        // 겉보기 위치 (지구에서 연장한 직선)
        const apparentX = sunX + 235, apparentY = sunY - 260; // 밖으로 더 밀려남
        ctx.strokeStyle = 'rgba(99,102,241,0.5)'; ctx.setLineDash([4,4]);
        ctx.beginPath(); ctx.moveTo(earthX, earthY); ctx.lineTo(apparentX, apparentY); ctx.stroke();
        
        // 겉보기 별 그리기
        ctx.save(); ctx.shadowBlur=15; ctx.shadowColor='#818cf8';
        ctx.beginPath(); ctx.arc(apparentX, apparentY, 5, 0, Math.PI*2); ctx.fillStyle='#fff'; ctx.fill();
        ctx.restore();
        ctx.fillStyle='#818cf8'; ctx.font='12px Noto Sans KR'; ctx.fillText('겉보기 위치 ( Einstein )', apparentX+10, apparentY-10);
    }
    ctx.setLineDash([]);

    // 실제 별
    ctx.beginPath(); ctx.arc(starRealX, starRealY, 4, 0, Math.PI*2); ctx.fillStyle='#facc15'; ctx.fill();
    ctx.fillStyle='#facc15'; ctx.font='12px Noto Sans KR'; ctx.fillText('실제 위치', starRealX+10, starRealY+5);

    // 태양 글로우
    const sunGrad = ctx.createRadialGradient(sunX, sunY, 0, sunX, sunY, sunR*1.5);
    sunGrad.addColorStop(0, '#fde047'); sunGrad.addColorStop(0.3, '#f59e0b'); sunGrad.addColorStop(1, 'transparent');
    ctx.beginPath(); ctx.arc(sunX, sunY, sunR*1.5, 0, Math.PI*2); ctx.fillStyle=sunGrad; ctx.fill();
    
    // 달 (태양 가림)
    ctx.beginPath(); ctx.arc(moonX, moonY, sunR+1, 0, Math.PI*2); ctx.fillStyle='#05070a'; ctx.fill();
    
    // 지구
    ctx.beginPath(); ctx.arc(earthX, earthY, 30, 0, Math.PI*2);
    const eg = ctx.createRadialGradient(earthX-5, earthY-5, 2, earthX, earthY, 30);
    eg.addColorStop(0,'#3b82f6'); eg.addColorStop(1,'#1e3a8a'); ctx.fillStyle=eg; ctx.fill();
}

/* ══════════════════════════════════════════
   Scenario 2: 회전 원판 (가속과 시간 지연)
══════════════════════════════════════════ */
function drawRotatingDisk(ctx, W, H, vel, t, clocks) {
    const cx = W*0.5, cy = H*0.5, r = 200;
    const ang = t * 0.001 * vel;

    // 고정 관찰자 A (지면)
    const ax = cx - 350, ay = cy;
    ctx.fillStyle='#94a3b8'; ctx.font='bold 14px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('A (정지 관찰자)', ax, ay-40);
    ctx.font='20px Space Mono'; ctx.fillStyle='#38bdf8';
    ctx.fillText(clocks.A.toFixed(2), ax, ay);

    // 원판 그리기
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI*2);
    ctx.fillStyle='rgba(30,41,59,0.5)'; ctx.fill();
    ctx.strokeStyle='#334155'; ctx.lineWidth=3; ctx.stroke();
    
    // 회전 눈금
    for(let i=0;i<12;i++){
        let a = ang + (i*Math.PI*2/12);
        ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(cx+r*Math.cos(a), cy+r*Math.sin(a));
        ctx.strokeStyle='rgba(148,163,184,0.1)'; ctx.stroke();
    }

    // 중심 관찰자 B
    ctx.fillStyle='#fff'; ctx.font='bold 14px Noto Sans KR';
    ctx.fillText('B (중심)', cx, cy-20);
    ctx.font='18px Space Mono'; ctx.fillStyle='#38bdf8';
    ctx.fillText(clocks.B.toFixed(2), cx, cy+10);

    // 가장자리 관찰자 C
    const cx_ = cx + (r-30)*Math.cos(ang), cy_ = cy + (r-30)*Math.sin(ang);
    ctx.beginPath(); ctx.arc(cx_, cy_, 25, 0, Math.PI*2);
    ctx.fillStyle='#1e293b'; ctx.fill(); ctx.strokeStyle='#6366f1'; ctx.lineWidth=2; ctx.stroke();
    ctx.fillStyle='#fff'; ctx.font='bold 13px Noto Sans KR';
    ctx.fillText('C (가장자리)', cx_, cy_-35);
    ctx.font='16px Space Mono'; ctx.fillStyle='#818cf8';
    ctx.fillText(clocks.C.toFixed(2), cx_, cy_-10);

    // 원심력 화살표 (등가 원리 힌트)
    const fx = cx_ + 40*Math.cos(ang), fy = cy_ + 40*Math.sin(ang);
    const dx=fx-cx_, dy=fy-cy_, angle=Math.atan2(dy,dx);
    ctx.beginPath(); ctx.moveTo(cx_, cy_); ctx.lineTo(fx, fy); ctx.strokeStyle='#f43f5e'; ctx.lineWidth=3; ctx.stroke();
    ctx.beginPath(); ctx.moveTo(fx, fy); 
    ctx.lineTo(fx-8*Math.cos(angle-0.5), fy-8*Math.sin(angle-0.5));
    ctx.moveTo(fx, fy);
    ctx.lineTo(fx-8*Math.cos(angle+0.5), fy-8*Math.sin(angle+0.5));
    ctx.stroke();
    ctx.fillStyle='#f43f5e'; ctx.font='11px Noto Sans KR';
    ctx.fillText('원심력(중력)', fx+15*Math.cos(ang), fy+15*Math.sin(ang));
}

/* ══════════════════════════════════════════
   Scenario 3: 블랙홀과 인터스텔라
══════════════════════════════════════════ */
function drawBlackHole(ctx, W, H, mass, t, clocks) {
    const cx = W*0.5, cy = H*0.45;
    const bhR = (mass * 0.4) + 30; // 질량에 비례하는 사건의 지평선

    // 인터스텔라 연출: 빛의 휨 (왜곡 효과)
    ctx.strokeStyle = 'rgba(99,102,241,0.15)'; ctx.lineWidth=1;
    for(let i=0;i<10;i++) {
        const ringR = bhR * (1.5 + i*0.4);
        ctx.beginPath(); ctx.ellipse(cx, cy, ringR, ringR*0.3, Math.sin(t*0.0001+i)*0.1, 0, Math.PI*2);
        ctx.stroke();
    }

    // 사건의 지평선 (Black Hole)
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, bhR);
    grad.addColorStop(0, '#000'); grad.addColorStop(0.8, '#000'); grad.addColorStop(0.9, '#1e1b4b'); grad.addColorStop(1, '#6366f144');
    ctx.beginPath(); ctx.arc(cx, cy, bhR, 0, Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    
    // 강착 원반 (가로 지르는 빛)
    const acR = bhR * 3;
    const acG = ctx.createLinearGradient(cx-acR, cy, cx+acR, cy);
    acG.addColorStop(0, 'rgba(251,191,36,0)'); acG.addColorStop(0.5, 'rgba(251,191,36,0.8)'); acG.addColorStop(1, 'rgba(251,191,36,0)');
    ctx.fillStyle=acG; ctx.beginPath(); ctx.ellipse(cx, cy, acR, bhR*0.2, 0.05*Math.sin(t*0.001), 0, Math.PI*2); ctx.fill();

    // 두 시계 비교
    const cardY = H * 0.82;
    // 지구 시계
    ctx.fillStyle='rgba(59,130,246,0.15)'; ctx.beginPath(); ctx.roundRect(W*0.15, cardY, 280, 80, 10); ctx.fill();
    ctx.fillStyle='#93c5fd'; ctx.font='bold 15px Noto Sans KR'; ctx.fillText('Murphy (Earth)', W*0.15+140, cardY+30);
    ctx.fillStyle='#38bdf8'; ctx.font='28px Space Mono'; ctx.fillText(clocks.Earth.toFixed(2), W*0.15+140, cardY+65);
    
    // 쿠퍼 시계
    ctx.fillStyle='rgba(244,63,94,0.15)'; ctx.beginPath(); ctx.roundRect(W*0.62, cardY, 280, 80, 10); ctx.fill();
    ctx.fillStyle='#fb7185'; ctx.font='bold 15px Noto Sans KR'; ctx.fillText('Cooper (Gargantua Orbit)', W*0.62+140, cardY+30);
    ctx.fillStyle='#f43f5e'; ctx.font='28px Space Mono'; ctx.fillText(clocks.Cooper.toFixed(2), W*0.62+140, cardY+65);
    
    ctx.fillStyle='#94a3b8'; ctx.font='12px Noto Sans KR'; ctx.textAlign='center';
    ctx.fillText('블랙홀의 질량이 클수록 사건의 지평선 주위의 시공간이 더 급격히 휩니다.', W*0.5, H*0.75);
}

/* ══════════════════════════════════════════
   메인 컴포넌트
══════════════════════════════════════════ */
const SimCanvas = ({ phase, mode, value, t, clocks }) => {
    const ref = useRef(null);
    useEffect(()=>{
        const canvas=ref.current; if(!canvas) return;
        canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight;
        const ctx=canvas.getContext('2d');
        if(phase===0) drawEddington(ctx, canvas.width, canvas.height, mode, t);
        else if(phase===1) drawRotatingDisk(ctx, canvas.width, canvas.height, value, t, clocks);
        else if(phase===2) drawBlackHole(ctx, canvas.width, canvas.height, value, t, clocks);
    },[phase, mode, value, t, clocks]);

    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block',borderRadius:12}}/>;
};

const App = () => {
    const [phase, setPhase] = useState(0);
    const [mode, setMode]   = useState('einstein');
    const [value, setValue] = useState(1); // Scenario 2: velocity, Scenario 3: Mass
    const [t, setT] = useState(0);
    const [clocks, setClocks] = useState({A:0, B:0, C:0, Earth:0, Cooper:0});
    const lastTime = useRef(performance.now());

    useEffect(()=>{
        const loop = (now) => {
            const dt = now - lastTime.current;
            lastTime.current = now;
            setT(now);
            
            setClocks(prev => {
                if(phase === 1) { // Rotating Disk
                    const deltaA = dt * 0.001;
                    const v_ratio = (value*0.03); 
                    // 로런츠 인자(특상) 혹은 등가원리(일반)를 추상화한 시계 속도 차이
                    const factorC = Math.sqrt(Math.max(0, 1 - v_ratio*v_ratio)); 
                    return { ...prev, A: prev.A + deltaA, B: prev.B + deltaA, C: prev.C + deltaA * factorC };
                } else if(phase === 2) { // Black Hole
                    const deltaE = dt * 0.001;
                    // 질량 M에 따른 중력 시간 지연 (추상화)
                    const m_ratio = (value / 100);
                    const factorCooper = Math.sqrt(Math.max(0.1, 1 - 0.9 * m_ratio));
                    return { ...prev, Earth: prev.Earth + deltaE, Cooper: prev.Cooper + deltaE * factorCooper };
                }
                return prev;
            });
            requestAnimationFrame(loop);
        };
        const raf = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(raf);
    },[phase, value]);

    const infoText = [
        { title: "에딩턴의 개기일식 실험", desc: "1919년 에딩턴은 일식 중에 태양 주변의 별빛이 휘는 현상을 최초로 관측했습니다. 이는 질량이 보이지 않는 시공간을 휘게 한다는 아인슈타인의 예견을 증명한 결정적 단서였습니다." },
        { title: "회전 원판과 시간의 흐름", desc: "외부 관찰자 A가 볼 때 움직이는 C의 시간은 느려집니다. 반면 함께 회전하는 B가 볼 때 C는 가속(원심력)을 받습니다. 등가 원리에 의해 가속은 중력과 같으므로, 결국 중력이 강한 곳의 시간은 천천히 흐르게 됩니다." },
        { title: "인터스텔라: 중력 시간 지연", desc: "거대 블랙홀 Gargantua 근처의 강한 중력장은 시공간을 극단적으로 휘게 만듭니다. 이 때문에 '시간의 흐름'이라는 지도상의 거리 자체가 늘어나, 쿠퍼의 1시간이 지구 Murphy의 수년이 되는 현상이 발생합니다." }
    ];

    return (
        <div style={{display:'grid',gridTemplateColumns:'320px 1fr',gap:20,maxWidth:1250,margin:'0 auto'}}>
            <div className="panel" style={{display:'flex',flexDirection:'column',gap:20}}>
                <div>
                    <label>탐구 테마</label>
                    <div style={{display:'flex',flexDirection:'column',gap:8}}>
                        {["빛의 휨 (실험 증명)","회전 좌표계 (시간 지연)","블랙홀 (인터스텔라)"].map((l,i)=>(
                            <button key={i} className={`tab-btn${phase===i?' active':''}`} onClick={()=>setPhase(i)}>{l}</button>
                        ))}
                    </div>
                </div>

                <div className="control-box">
                    {phase === 0 ? (
                        <>
                            <label>물리 이론 선택</label>
                            <div style={{display:'flex',gap:8}}>
                                <button className={`tab-btn${mode==='newton'?' active':''}`} style={{fontSize:12,flex:1}} onClick={()=>setMode('newton')}>Newton (직진)</button>
                                <button className={`tab-btn${mode==='einstein'?' active':''}`} style={{fontSize:12,flex:1}} onClick={()=>setMode('einstein')}>Einstein (휨)</button>
                            </div>
                        </>
                    ) : (
                        <>
                            <label>{phase===1 ? '원판 회전 속도 (v)' : '블랙홀 질량 (M)'}</label>
                            <input type="range" min="1" max="100" value={value} onChange={e=>setValue(parseInt(e.target.value))}/>
                            <div style={{textAlign:'center',fontFamily:'Space Mono',color:'#6366f1',fontSize:18,marginTop:10}}>{value} units</div>
                        </>
                    )}
                </div>

                <div className="card" style={{padding:15}}>
                    <h3 style={{fontSize:15,color:'#fff',marginBottom:10}}>{infoText[phase].title}</h3>
                    <p style={{fontSize:13,lineHeight:1.6,color:'#94a3b8'}}>{infoText[phase].desc}</p>
                </div>

                {phase !== 0 && (
                    <div className="card" style={{textAlign:'center'}}>
                        <label>시간 흐름 비교 (Normalized)</label>
                        <div className="clock-display">
                            {phase===1 ? clocks.A.toFixed(2) : clocks.Earth.toFixed(2)}s
                        </div>
                        <div style={{fontSize:11,color:'#475569',marginTop:10}}>상대적 시간 왜곡을 시뮬레이션 중입니다.</div>
                    </div>
                )}
            </div>

            <div style={{background:'#000',borderRadius:20,border:'1px solid rgba(255,255,255,0.1)',position:'relative',height:650,overflow:'hidden'}}>
                <SimCanvas phase={phase} mode={mode} value={value} t={t} clocks={clocks}/>
                
                {/* 오버레이 설명 (에딩턴 모드인 경우) */}
                {phase===0 && mode==='einstein' && (
                    <div style={{position:'absolute',top:20,right:20,background:'rgba(13,21,38,0.85)',padding:12,borderRadius:10,fontSize:12,border:'1px solid #6366f166',maxWidth:220}}>
                        <div style={{color:'#6366f1',fontWeight:800,marginBottom:5}}>🔍 관측 핵심:</div>
                        빛이 태양 쪽으로 휘어 들어오기 때문에, 지구의 관찰자는 별이 태양에서 더 **멀리 떨어진 위치**에 있는 것으로 착각하게 됩니다.
                    </div>
                )}
            </div>
            
            <div style={{gridColumn:'span 2'}} className="card">
                <div style={{display:'grid',gridTemplateColumns:'1.5fr 1fr',gap:30}}>
                    <div>
                        <h2 style={{fontSize:20,fontWeight:800,marginBottom:15,color:'#fff'}}>🤔 탐구 질문: 우리 주변의 일반 상대성 이론</h2>
                        <div className="theory-box">
                            <strong>Q: 쿠퍼 대장이 늙은 딸을 만난 이유는?</strong><br/>
                            블랙홀 근처의 시간은 지구보다 훨씬 천천히 흐릅니다. 쿠퍼에게는 짧은 여행이었지만, 시공간이 극심하게 휘어지지 않은 지구에서는 수십 년의 세월이 흐른 것이지요. 
                            이는 실제 GPS 위성에서도 발생하며, 매일 지구 시계와 0.00004초 정도의 차이를 보정해주어야 합니다.
                        </div>
                        <div className="theory-box" style={{borderColor:'#10b981'}}>
                            <strong>Q: 이미지 1 - 회전 원판 위의 시계는?</strong><br/>
                            원판 가장자리의 C는 고속 운동을 하거나 강한 원심력을 받습니다. 등가 원리에 의해 가속도는 중력과 같으므로, C의 시계는 정지한 A나 중심의 B보다 느리게 가게 됩니다. (특상과 일반 상대성 이론의 만남)
                        </div>
                    </div>
                    <div style={{background:'rgba(255,180,0,0.05)',padding:20,borderRadius:15,border:'1px dotted rgba(255,180,0,0.3)'}}>
                        <label style={{color:'#f59e0b'}}>Physical Formula</label>
                        <Eq f="dt = d\tau / \sqrt{1 - \frac{2GM}{rc^2}}" display={true}/>
                        <p style={{fontSize:12,color:'#94a3b8',marginTop:10,lineHeight:1.6}}>
                            위 공식은 슈바르츠실트 해의 시간 지연 공식입니다. 질량 M이 클수록, 거리 r이 작을수록 고유 시간(τ) 대비 관측 시간(t)이 늘어남을 알 수 있습니다.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""
    components.html(react_code, height=1200, scrolling=True)

if __name__ == "__main__":
    run_sim()
