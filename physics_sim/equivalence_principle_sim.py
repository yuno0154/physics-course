import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="학습주제 5. 관성력과 중력 등가 원리 탐구", layout="wide")

def run_sim():
    # 제목 섹션
    st.title("🌓 학습주제 5. 관성력과 중력 등가 원리 탐구")
    st.markdown("가속 좌표계에서의 현상을 내부와 외부 시점으로 분석하며 등가 원리의 본질과 시공간 곡률을 탐구합니다.")

    # React 기반 통합 시뮬레이션 코드 (개별 제어 및 물리 동기화 버전)
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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0a0f1e;color:#e2e8f0;padding:18px;}
.panel{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;}
.card{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:20px;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#3b82f6;cursor:pointer;box-shadow:0 0 8px rgba(59,130,246,0.6);}
label{font-size:11px;color:#64748b;font-weight:700;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.04em;}
.phase-btn{padding:8px 16px;border-radius:8px;border:1px solid #1e293b;background:#0d1526;color:#94a3b8;cursor:pointer;font-size:13px;font-family:inherit;transition:all 0.2s;text-align:left;}
.phase-btn.active{border-color:#3b82f6;background:#1e3a5f;color:#e2e8f0;font-weight:700;}
.phase-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.control-group{padding:12px;border:1.5px solid #1e293b;border-radius:12px;display:flex;flex-direction:column;gap:8px;background:'rgba(255,255,255,0.02)';}
.btn-primary{padding:10px;border-radius:8px;background:rgba(59,130,246,0.1);color:#60a5fa;border:1px solid rgba(59,130,246,0.4);font-weight:700;cursor:pointer;font-size:12px;}
.btn-primary:active{background:rgba(59,130,246,0.25);}
.btn-stop{padding:10px;border-radius:8px;background:rgba(239,68,68,0.1);color:#f87171;border:1px solid rgba(239,68,68,0.4);font-weight:700;cursor:pointer;font-size:12px;}
.btn-reset{padding:6px;border-radius:8px;background:transparent;border:1px solid #1e293b;color:#475569;cursor:pointer;font-size:11px;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef, useCallback } = React;

/* ── KaTeX 수식 렌더링 ── */
const Math_ = ({ f, display=false, style={} }) => {
    const ref = useRef(null);
    useEffect(()=>{
        if(ref.current && window.katex){
            window.katex.render(f, ref.current, {throwOnError:false, displayMode:display});
        }
    },[f,display]);
    return <span ref={ref} style={style}/>;
};

/* ── 탐구 질문 QnA ── */
const QNA_ITEMS = [
    {
        q:'가속 좌표계에서 관찰자 위치(내부 vs 외부)에 따라 공의 운동은 다르게 보일까?',
        a:'네, 보기는 다르지만 물리적 인과관계는 일치합니다. 내부 관찰자는 공이 하강 가속도를 받는다고 느끼고(비관성계), 외부 관찰자는 공은 멈춰 있는데 우주선 바닥이 올라와 충돌한다고 봅니다(관성계). 두 시점 모두 공과 바닥이 만난다는 결론은 동일합니다.'
    },
    {
        q:'정지한 우주선과 가속 중인 우주선 안에서 공이 바닥으로 떨어진다. 두 경우를 관측만으로 구별할 수 있을까?',
        a:'구별할 수 없습니다. 정지한 우주선에서는 지구 중력(mg)이, 가속하는 우주선에서는 관성력(ma, a=g)이 공을 바닥으로 떨어뜨립니다. 내부 관찰자가 경험하는 현상은 완전히 동일합니다. 이것이 등가 원리의 핵심입니다.'
    },
];

const QnA = ({ items }) => {
    const [open, setOpen] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {items.map((item,i)=>(
                <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#3b82f6':'#1e293b'}`,overflow:'hidden',background:'#070b14'}}>
                    <button onClick={()=>setOpen(open===i?null:i)}
                        style={{width:'100%',display:'flex',alignItems:'flex-start',gap:12,padding:'14px 18px',background:'transparent',border:'none',cursor:'pointer',textAlign:'left',fontFamily:'inherit'}}>
                        <span style={{color:'#6366f1',fontWeight:800,fontSize:15}}>Q{i+1}.</span>
                        <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.6,flex:1}}>{item.q}</span>
                    </button>
                    {open===i && <div style={{padding:'0 18px 14px 46px',color:'#6ee7b7',fontSize:13,lineHeight:1.7}}>A. {item.a}</div>}
                </div>
            ))}
        </div>
    );
};

/* ── 수식 유도 단계 ── */
const DERIVE_STEPS = [
    { title:'Step 1. 등가 원리', desc:'가속에 의한 관성력과 중력은 구별 불가.', formula:'F_{\\text{obs}} = ma = mg', color:'#3b82f6', bg:'#0d1f3c' },
    { title:'Step 2. 운동의 상대성', desc:'외부에서 본 가속량만큼 내부에서 상대적으로 이동.', formula:'\\Delta y = \\frac{1}{2}at^2', color:'#ec4899', bg:'#2d0d1a' },
    { title:'Step 3. 빛의 경로 휨', desc:'가속계에서 빛의 경로가 포물선을 그림.', formula:'y \\approx \\frac{1}{2}a(x/c)^2', color:'#8b5cf6', bg:'#1a0d3c' },
    { title:'Step 4. 시공간 곡률', desc:'중력을 시공간의 기하학적 휨으로 해석.', formula:'G_{\\mu\\nu} \\propto T_{\\mu\\nu}', color:'#10b981', bg:'#0a1f18' },
];

const DerivationSection = () => {
    const [open, setOpen] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0',marginBottom:10}}>개념 연결: 가속 → 관성력 → 곡률</h2>
            {DERIVE_STEPS.map((step,i)=>(
                <div key={i} style={{border:`1px solid ${open===i?step.color:'#1e293b'}`,borderRadius:12,overflow:'hidden'}}>
                    <button onClick={()=>setOpen(open===i?null:i)} style={{width:'100%',padding:12,background:open===i?step.bg:'transparent',border:'none',color:'#e2e8f0',textAlign:'left',cursor:'pointer',fontWeight:700}}>
                        {i+1}. {step.title}
                    </button>
                    {open===i && <div style={{padding:'0 12px 12px 12px',background:step.bg,fontSize:13,color:'#94a3b8'}}>{step.desc}<div style={{marginTop:10,textAlign:'center'}}><Math_ f={step.formula} display={true}/></div></div>}
                </div>
            ))}
        </div>
    );
};

/* ════════════════════════════════════════════
   물리 계산 헬퍼 (동기화 용)
════════════════════════════════════════════ */
// t (ms), a (m/s2), scale (pixel/m), maxDist (pixel)
const getPhysicsDist = (tMs, accel, scale = 1.2, maxDist = 155) => {
    const tSec = tMs / 1000;
    const dist = 0.5 * accel * (tSec ** 2) * scale;
    return Math.min(dist, maxDist);
};

/* ── 우주선 디자인 ── */
function drawRocket(ctx, cx, cy, w, h, accel, thrustFlicker=1, isInside=false) {
    const thr = accel > 0 ? (20 + accel * 2) * thrustFlicker : 0;
    if(thr > 0) {
        const fg = ctx.createLinearGradient(cx, cy+h/2, cx, cy+h/2+thr);
        fg.addColorStop(0,'rgba(255,200,50,0.9)'); fg.addColorStop(1,'transparent');
        ctx.beginPath(); ctx.moveTo(cx-12, cy+h/2); ctx.quadraticCurveTo(cx, cy+h/2+thr, cx+12, cy+h/2);
        ctx.fillStyle=fg; ctx.fill();
    }
    const bg = ctx.createLinearGradient(cx-w/2, 0, cx+w/2, 0);
    bg.addColorStop(0,'#475569'); bg.addColorStop(0.5,'#94a3b8'); bg.addColorStop(1,'#475569');
    ctx.save();
    if(isInside) ctx.globalAlpha = 0.35;
    ctx.beginPath(); ctx.roundRect(cx-w/2, cy-h/2, w, h, w/4);
    ctx.fillStyle=bg; ctx.fill();
    ctx.beginPath(); ctx.arc(cx, cy-h/8, w/4.5, 0, Math.PI*2); ctx.fillStyle='rgba(15,23,42,0.85)'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx-w/2, cy-h/2); ctx.quadraticCurveTo(cx, cy-h/2-30, cx+w/2, cy-h/2); ctx.fillStyle='#334155'; ctx.fill();
    ctx.restore();
}

const SimCanvas = ({ phase, accel, tL, tR, runningL, runningR }) => {
    const ref = useRef(null);
    const draw = useCallback(() => {
        const canvas = ref.current; if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const W = canvas.width, H = canvas.height;
        ctx.fillStyle = '#0a0f1e'; ctx.fillRect(0, 0, W, H);
        
        // 별 배경
        const rng = (s) => (Math.sin(s)*10000 % 1);
        for(let i=0;i<60;i++){
            ctx.fillStyle=`rgba(255,255,255,${0.3+0.4*Math.sin(tL*0.001+i)})`;
            ctx.beginPath(); ctx.arc(rng(i*7)*W, rng(i*13)*H, 0.8, 0, Math.PI*2); ctx.fill();
        }

        const rw=90, rh=240, cy=H*0.45;
        const bStartRel = -rh*0.28; // 우주선 중심 대비 공의 시작 y

        if(phase === 0 || phase === 1) {
            const cx1 = W*0.27, cx2 = W*0.73;
            // 물리 계산 (두 시각에 동일한 공식을 적용하여 위치 일치시킴)
            const dL = getPhysicsDist(tL, phase===0? 9.8 : accel, 1.3, 155);
            const dR = getPhysicsDist(tR, accel, 1.3, 155);

            // LEFT
            const titleL = phase===0 ? "중력장(지구)" : "내부 관찰자 시점";
            ctx.fillStyle='white'; ctx.textAlign='center'; ctx.font='bold 14px Noto Sans KR'; ctx.fillText(titleL, cx1, cy-rh/2-25);
            drawRocket(ctx, cx1, cy+30, rw, rh, 0, 1, true);
            const bY1 = (cy + 30) + bStartRel + dL;
            const grad1 = ctx.createRadialGradient(cx1-3, bY1-3, 2, cx1, bY1, 10);
            grad1.addColorStop(0,'#fff8dc'); grad1.addColorStop(1,'#cc8800');
            ctx.beginPath(); ctx.arc(cx1, bY1, 10, 0, Math.PI*2); ctx.fillStyle=grad1; ctx.fill();

            // RIGHT
            const titleR = phase===0 ? "가속 중인 우주선" : "외부 관찰자 시점";
            ctx.fillText(titleR, cx2, cy-rh/2-25,);
            const rY2 = (cy + 30) - dR;
            drawRocket(ctx, cx2, rY2, rw, rh, (phase===0?9.8:accel), 0.8+0.2*Math.sin(tR*0.01), true);
            const bY2 = (cy + 30) + bStartRel; // 외부 시점에서 공은 제자리에 고정 (관성)
            const grad2 = ctx.createRadialGradient(cx2-3, bY2-3, 2, cx2, bY2, 10);
            grad2.addColorStop(0,'#fff8dc'); grad2.addColorStop(1,'#cc8800');
            ctx.beginPath(); ctx.arc(cx2, bY2, 10, 0, Math.PI*2); ctx.fillStyle=grad2; ctx.fill();
        }
        else if(phase === 2) {
            // 빛 휨 (생략 가능하나 유지를 위해 간단히)
            const cx1 = W*0.27, cx2 = W*0.73;
            drawRocket(ctx, cx1, cy+30, rw, rh, 0, 1, true);
            drawRocket(ctx, cx2, cy+30, rw, rh, accel, 1, true);
        }
        else if(phase === 4) {
            // 곡률 시각화
            ctx.fillStyle='#3b82f622';
            const cx=W/2, cyM=H*0.5;
            for(let i=0;i<W;i+=40) { ctx.beginPath(); ctx.moveTo(i,0); ctx.lineTo(i,H); ctx.strokeStyle='rgba(59,130,246,0.1)'; ctx.stroke(); }
            for(let i=0;i<H;i+=40) { ctx.beginPath(); ctx.moveTo(0,i); ctx.lineTo(W,i); ctx.stroke(); }
            ctx.beginPath(); ctx.arc(cx, cyM, 40+accel, 0, Math.PI*2); ctx.fillStyle='#fbbf24'; ctx.fill();
        }
    }, [phase, accel, tL, tR, runningL, runningR]);

    useEffect(()=>{
        const canvas=ref.current; canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw();
    },[draw]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

const App = () => {
    const [phase, setPhase] = useState(0);
    const [accel, setAccel] = useState(9.8);
    const [tL, setTL] = useState(0);
    const [tR, setTR] = useState(0);
    const [runningL, setRunningL] = useState(false);
    const [runningR, setRunningR] = useState(false);
    const rafL = useRef(null);
    const rafR = useRef(null);

    useEffect(() => {
        if(runningL) {
            let start = performance.now() - tL;
            const loop = (now) => { 
                const nt = now - start;
                if(nt < 2500) { setTL(nt); rafL.current = requestAnimationFrame(loop); }
                else { setTL(2500); setRunningL(false); }
            };
            rafL.current = requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafL.current);
        return () => cancelAnimationFrame(rafL.current);
    }, [runningL]);

    useEffect(() => {
        if(runningR) {
            let start = performance.now() - tR;
            const loop = (now) => { 
                const nt = now - start;
                if(nt < 2500) { setTR(nt); rafR.current = requestAnimationFrame(loop); }
                else { setTR(2500); setRunningR(false); }
            };
            rafR.current = requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafR.current);
        return () => cancelAnimationFrame(rafR.current);
    }, [runningR]);

    return (
        <div style={{maxWidth:1200,margin:'0 auto',display:'flex',flexDirection:'column',gap:20}}>
            <div style={{display:'grid',gridTemplateColumns:'300px 1fr',gap:20}}>
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:15}}>
                    <label>탐구 단계</label>
                    <div style={{display:'flex',flexDirection:'column',gap:5}}>
                        {["① 관성력/중력","② 내부/외부 시점","③ 빛의 휨","④ 등가 원리","⑤ 시공간 곡률"].map((l,i)=>(
                            <button key={i} className={`phase-btn${phase===i?' active':''}`} onClick={()=>{setPhase(i);setTL(0);setTR(0);setRunningL(false);setRunningR(false);}}>{l}</button>
                        ))}
                    </div>
                    
                    {(phase===0 || phase===1) && (
                        <div style={{display:'flex',flexDirection:'column',gap:12}}>
                            <div className="control-group">
                                <label style={{color:'#60a5fa'}}>LEFT SCENARIO</label>
                                <button className="btn-primary" onClick={()=>setRunningL(true)} disabled={runningL}>▶ 시작</button>
                                <button className="btn-reset" onClick={()=>{setRunningL(false);setTL(0);}}>↺ 초기화</button>
                            </div>
                            <div className="control-group">
                                <label style={{color:'#f87171'}}>RIGHT SCENARIO</label>
                                <button className="btn-primary" onClick={()=>setRunningR(true)} disabled={runningR}>▶ 시작</button>
                                <button className="btn-reset" onClick={()=>{setRunningR(false);setTR(0);}}>↺ 초기화</button>
                            </div>
                            <button className="btn-primary" style={{background:'rgba(167,139,250,0.1)', borderColor:'rgba(167,139,250,0.4)', color:'#a78bfa'}} 
                                onClick={()=>{setRunningL(true);setRunningR(true);}}>전체 동기화 실행</button>
                        </div>
                    )}

                    <label>실험 가속도 (a)</label>
                    <input type="range" min="2" max="25" step="0.5" value={accel} onChange={e=>setAccel(parseFloat(e.target.value))}/>
                    <div style={{textAlign:'center',fontFamily:'Space Mono',color:'#60a5fa'}}>{accel.toFixed(1)} m/s²</div>
                </div>
                <div style={{height:550,borderRadius:16,overflow:'hidden',border:'1px solid #1e293b'}}>
                    <SimCanvas phase={phase} accel={accel} tL={tL} tR={tR} runningL={runningL} runningR={runningR}/>
                </div>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20}}>
                <div className="card"><QnA items={QNA_ITEMS}/></div>
                <div className="card"><DerivationSection/></div>
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
