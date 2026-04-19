import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="학습주제 5. 관성력과 중력 등가 원리 탐구", layout="wide")

def run_sim():
    # 제목 섹션
    st.title("🌓 학습주제 5. 관성력과 중력 등가 원리 탐구")
    st.markdown("가속 좌표계에서의 현상을 내부와 외부 시점으로 분석하며 등가 원리의 본질과 시공간 곡률을 탐구합니다.")

    # React 기반 통합 시뮬레이션 코드 (내부/외부 시점 추가 버전)
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
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.result-val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;font-size:14px;}
.phase-btn{padding:7px 16px;border-radius:8px;border:1px solid #1e293b;background:#0d1526;color:#94a3b8;cursor:pointer;font-size:13px;font-family:inherit;transition:all 0.2s;text-align:left;}
.phase-btn.active{border-color:#3b82f6;background:#1e3a5f;color:#e2e8f0;font-weight:700;}
.phase-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
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
        a:'네, 보기는 다르지만 물리적 인과관계는 일치합니다. 내부 관찰자는 공이 하강 가속도를 받는다고 느끼고, 외부 관찰자는 공은 멈춰 있는데 우주선 바닥이 올라와 충돌한다고 봅니다. 두 시점 모두 공과 바닥이 만난다는 결론은 동일합니다.'
    },
    {
        q:'정지한 우주선과 가속 중인 우주선 안에서 공이 바닥으로 떨어진다. 두 경우를 관측만으로 구별할 수 있을까?',
        a:'구별할 수 없습니다. 정지한 우주선에서는 지구 중력(mg)이, 가속하는 우주선에서는 관성력(ma, a=g)이 공을 바닥으로 떨어뜨립니다. 내부 관찰자가 경험하는 현상은 완전히 동일합니다. 이것이 등가 원리의 핵심입니다.'
    },
    {
        q:'가속 좌표계에서 빛은 직진할까? 왜 빛의 경로가 휘는가?',
        a:'가속 좌표계에서 빛은 휘어 보입니다. 빛이 우주선을 통과하는 동안 우주선이 가속되므로, 내부 관찰자 입장에서는 빛이 포물선을 그리며 아래로 처집니다. 외부 관찰자가 보면 빛은 직진하지만 우주선이 위로 가속하여 빗나가는 것뿐입니다.'
    },
    {
        q:'아인슈타인은 중력에 의한 빛의 휨을 어떻게 증명했는가?',
        a:'등가 원리를 통해 가속계에서의 빛의 휨을 중력장으로 확장한 후, 이를 시공간의 곡률로 해석했습니다. 1919년 개기일식 당시 태양 주변을 지나는 별빛의 위치 변화를 실측함으로써 중력이 시공간을 휘게 한다는 것을 증명했습니다.'
    },
];

const QnA = ({ items }) => {
    const [open, setOpen] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {items.map((item,i)=>(
                <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#3b82f6':'#1e293b'}`,overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
                    <button onClick={()=>setOpen(open===i?null:i)}
                        style={{width:'100%',display:'flex',alignItems:'flex-start',gap:12,padding:'14px 18px',background:'transparent',border:'none',cursor:'pointer',textAlign:'left',fontFamily:'inherit'}}>
                        <span style={{color:'#6366f1',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
                        <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
                        <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
                    </button>
                    <div style={{maxHeight:open===i?'240px':'0px',overflow:'hidden',transition:'max-height(0.35s) ease'}}>
                        <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                            <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                            <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.75}}>{item.a}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

/* ── 수식 유도 단계 ── */
const DERIVE_STEPS = [
    {
        title:'Step 1. 등가 원리 (Equivalence Principle)',
        desc:'가속 좌표계에서 느끼는 관성력과 중력은 물리적으로 구별할 수 없다.',
        formula:'a = g \\quad \\Rightarrow \\quad F_{\\text{관성}} = ma = mg = F_{\\text{중력}}',
        color:'#3b82f6', bg:'#0d1f3c',
        note:'아인슈타인(1907): "자유낙하하는 관찰자는 중력을 느끼지 못한다." (가장 행복한 생각)'
    },
    {
        title:'Step 2. 관측 시점에 따른 운동의 해석',
        desc:'내부 관찰자는 힘(관성력)을 도입하고, 외부 관찰자는 물체의 관성과 우주선의 가속으로 설명한다.',
        formula:'y_{\\text{rel}} = y_{\\text{ball}} - y_{\\text{floor}} = \\frac{1}{2}at^2',
        color:'#ec4899', bg:'#2d0d1a',
        note:'어떤 시점이든 공이 바닥에 닿기까지 걸리는 시간은 동일하게 계산된다.'
    },
    {
        title:'Step 3. 가속 좌표계에서 빛의 경로',
        desc:'가속도 a로 위로 가속하는 우주선에서 수평으로 입사한 빛의 처짐을 계산한다.',
        formula:'\\Delta y = \\frac{1}{2}a t^2 = \\frac{1}{2}a \\left(\\frac{L}{c}\\right)^2',
        color:'#8b5cf6', bg:'#1a0d3c',
        note:'이 현상은 중력장에서도 동일하게 관측되어야 함을 시사한다.'
    },
    {
        title:'Step 4. 아인슈타인의 결론: 시공간 곡률',
        desc:'빛은 직진하지만, 질량이 시공간 자체를 휘게 하므로 경로가 휘어 보인다.',
        formula:'G_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}',
        color:'#10b981', bg:'#0a1f18',
        note:'질량이 시공간을 휘고, 휘어진 시공간이 빛의 경로를 결정한다.'
    },
    {
        title:'Step 5. 실험적 검증: 1919년 일식 관측',
        desc:'에딩턴이 태양 근처 별빛의 편향각을 측정하여 아인슈타인의 이론을 증명했다.',
        formula:'\\delta\\theta = \\frac{4GM_{\\odot}}{c^2 R_{\\odot}} \\approx 1.75^{\\prime\\prime}',
        color:'#fbbf24', bg:'#1f1200',
        note:'뉴턴 예측(0.875")의 두 배인 1.75"가 측정되어 일반상대성이론이 승리했다.'
    },
];

const DerivationSection = () => {
    const [open, setOpen] = useState(null);
    const [kReady, setKReady] = useState(!!window.katex);
    useEffect(()=>{
        if(window.katex){setKReady(true);return;}
        const t=setInterval(()=>{if(window.katex){setKReady(true);clearInterval(t);}},200);
        return ()=>clearInterval(t);
    },[]);

    return (
        <div>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:6}}>
                <div style={{width:4,height:22,background:'#6366f1',borderRadius:2}}/>
                <h2 style={{fontSize:18,fontWeight:800,color:'#e2e8f0'}}>개념 연결: 가속 → 관성력 → 중력(시공간 곡률)</h2>
            </div>
            <p style={{color:'#475569',fontSize:13,marginBottom:18,marginLeft:14}}>
                각 단계를 클릭해 논리적 연결 과정을 확인하세요.
            </p>
            <div style={{display:'flex',flexDirection:'column',gap:10}}>
                {DERIVE_STEPS.map((step,i)=>(
                    <div key={i} style={{border:`1px solid ${open===i?step.color+'80':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
                        <button onClick={()=>setOpen(open===i?null:i)}
                            style={{width:'100%',display:'flex',alignItems:'center',gap:14,padding:'14px 18px',background:open===i?step.bg:'transparent',border:'none',cursor:'pointer',fontFamily:'inherit',transition:'background 0.25s'}}>
                            <div style={{width:28,height:28,borderRadius:'50%',background:step.color+'22',border:`1.5px solid ${step.color}66`,display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
                                <span style={{color:step.color,fontWeight:800,fontSize:13}}>{i+1}</span>
                            </div>
                            <span style={{color:'#e2e8f0',fontWeight:700,fontSize:14,flex:1,textAlign:'left'}}>{step.title}</span>
                            <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)'}}>▾</span>
                        </button>
                        <div style={{maxHeight:open===i?'280px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                            <div style={{padding:'0 18px 18px 60px',background:step.bg}}>
                                <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.7,marginBottom:14}}>{step.desc}</p>
                                {kReady && (
                                    <div style={{background:'#070b14',borderRadius:10,padding:'14px 20px',marginBottom:12,textAlign:'center',border:`1px solid ${step.color}33`}}>
                                        <Math_ f={step.formula} display={true}/>
                                    </div>
                                )}
                                <p style={{color:'#64748b',fontSize:12,lineHeight:1.75,borderLeft:`3px solid ${step.color}55`,paddingLeft:10}}>{step.note}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

/* ════════════════════════════════════════════
   메인 시뮬레이션 캔버스
════════════════════════════════════════════ */
const SimCanvas = ({ phase, accel, running, t }) => {
    const ref = useRef(null);

    const draw = useCallback(() => {
        const canvas = ref.current;
        if (!canvas) return;
        const W = canvas.width, H = canvas.height;
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, W, H);

        /* ── 별 배경 ── */
        ctx.fillStyle = '#0a0f1e';
        ctx.fillRect(0, 0, W, H);
        const rng = (seed) => { let x=Math.sin(seed)*10000; return x-Math.floor(x); };
        for(let i=0;i<80;i++){
            const sx=rng(i*3+1)*W, sy=rng(i*3+2)*H, sr=rng(i*3+3)*1.4+0.3;
            const op=0.25+0.5*Math.sin(t*0.001*rng(i+50)+i);
            ctx.beginPath(); ctx.arc(sx,sy,sr,0,Math.PI*2);
            ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
        }

        if(phase===0) drawPhase0(ctx,W,H,accel,t,running);
        else if(phase===1) drawPhase1(ctx,W,H,accel,t,running);
        else if(phase===2) drawPhase2(ctx,W,H,accel,t,running);
        else if(phase===3) drawPhase3(ctx,W,H,accel,t,running);
        else if(phase===4) drawPhase4(ctx,W,H,accel,t,running);
    }, [phase, accel, running, t]);

    useEffect(()=>{
        const canvas=ref.current; if(!canvas) return;
        const ro=new ResizeObserver(()=>{ canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw(); });
        ro.observe(canvas); canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw();
        return ()=>ro.disconnect();
    },[]);
    useEffect(()=>{ draw(); },[draw]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ── 헬퍼: 우주선 그리기 ── */
function drawRocket(ctx, cx, cy, w, h, accel, thrustFlicker=1) {
    if(accel > 0) {
        const fH = (20 + accel*1.5)*thrustFlicker;
        const fg = ctx.createLinearGradient(cx, cy+h/2, cx, cy+h/2+fH);
        fg.addColorStop(0,'#fbbf24'); fg.addColorStop(1,'transparent');
        ctx.beginPath(); ctx.moveTo(cx-8,cy+h/2); ctx.lineTo(cx,cy+h/2+fH); ctx.lineTo(cx+8,cy+h/2);
        ctx.fillStyle=fg; ctx.fill();
    }
    const bg=ctx.createLinearGradient(cx-w/2,0,cx+w/2,0);
    bg.addColorStop(0,'#475569'); bg.addColorStop(0.5,'#94a3b8'); bg.addColorStop(1,'#475569');
    ctx.beginPath(); ctx.roundRect(cx-w/2,cy-h/2,w,h,10); ctx.fillStyle=bg; ctx.fill();
    ctx.beginPath(); ctx.arc(cx,cy-h/4,w/4,0,Math.PI*2); ctx.fillStyle='#1e293b'; ctx.fill();
}

function arrow(ctx,x1,y1,x2,y2,color='rgba(100,200,255,0.9)',lw=2){
    const dx=x2-x1, dy=y2-y1, angle=Math.atan2(dy,dx);
    ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=lw; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    const al=8, aa=0.4;
    ctx.beginPath(); ctx.moveTo(x2,y2);
    ctx.lineTo(x2-al*Math.cos(angle-aa),y2-al*Math.sin(angle-aa));
    ctx.moveTo(x2,y2); ctx.lineTo(x2-al*Math.cos(angle+aa),y2-al*Math.sin(angle+aa));
    ctx.stroke(); ctx.restore();
}

function txt(ctx,x,y,s,color='#e2e8f0',size=12,align='center',weight='400'){
    ctx.save(); ctx.fillStyle=color; ctx.font=`${weight} ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align; ctx.fillText(s,x,y); ctx.restore();
}

function dashedRect(ctx,x,y,w,h,color,r=10){
    ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=1; ctx.setLineDash([5,5]);
    ctx.beginPath(); ctx.roundRect(x,y,w,h,r); ctx.stroke(); ctx.restore();
}

/* ════ Phase 0: 중력 vs 관찰자(가속) ════ */
function drawPhase0(ctx,W,H,accel,t,running){
    const cx1=W*0.27, cx2=W*0.73, cy=H*0.5, rw=120, rh=H*0.7;
    dashedRect(ctx,cx1-rw/2,cy-rh/2,rw,rh,'#fbbf2444');
    drawRocket(ctx,cx1,cy+30,80,220,0);
    arrow(ctx,cx1+rw,cy,cx1+rw,cy+60,'#fbbf24'); txt(ctx,cx1+rw+15,cy+35,'g', '#fbbf24', 12, 'left');
    txt(ctx,cx1,cy-rh/2-15,'중력장(지구)','white',13);

    dashedRect(ctx,cx2-rw/2,cy-rh/2,rw,rh,'#4ade8044');
    drawRocket(ctx,cx2,cy+30,80,220,running?accel:0,running?0.8+0.2*Math.sin(t*0.01):1);
    arrow(ctx,cx2+rw,cy+30,cx2+rw,cy-30,'#4ade80'); txt(ctx,cx2+rw+15,cy,'a', '#4ade80', 12, 'left');
    txt(ctx,cx2,cy-rh/2-15,'가속 중인 우주선','white',13);

    const bStart=cy-rh*0.3, bEnd=cy+rh*0.3;
    const bY = running? bStart+(bEnd-bStart)*Math.min(((t%2500)/2500)*1.3, 1) : bStart;
    [cx1,cx2].forEach(bx=>{
       ctx.beginPath(); ctx.arc(bx,bY,10,0,Math.PI*2); ctx.fillStyle='#facc15'; ctx.fill();
    });
    if(running) txt(ctx,W/2,H-30,'내부 관찰자는 두 상황을 구별할 수 없다!','#a78bfa',14,'center','700');
}

/* ════ Phase 1: 내부 vs 외부 시점 (New) ════ */
function drawPhase1(ctx,W,H,accel,t,running){
    const cx1=W*0.27, cx2=W*0.73, cy=H*0.5, rw=130, rh=H*0.7;
    const loopTime=3000;
    const prog=running? (t%loopTime)/loopTime : 0;

    // LEFT: 내부 시점 (비관성계)
    dashedRect(ctx,cx1-rw/2,cy-rh/2,rw,rh,'#ec489944');
    txt(ctx,cx1,cy-rh/2-15,'내부 관찰자 시점','white',13);
    drawRocket(ctx,cx1,cy+30,80,220,0); // 우주선 고정
    const bY1 = cy-rh*0.3 + (rh*0.6)*Math.min(prog*1.2, 1);
    ctx.beginPath(); ctx.arc(cx1,bY1,10,0,Math.PI*2); ctx.fillStyle='#facc15'; ctx.fill();
    arrow(ctx,cx1+40,bY1-20,cx1+40,bY1+10,'#ec4899',2); txt(ctx,cx1+65,bY1,'관성력','#ec4899',11,'left');

    // RIGHT: 외부 시점 (관성계)
    dashedRect(ctx,cx2-rw/2,cy-rh/2,rw,rh,'#3b82f644');
    txt(ctx,cx2,cy-rh/2-15,'외부 관찰자 시점','white',13);
    const rockAccDist = (accel/10)*80 * (prog**2);
    const rockY = cy+30 - rockAccDist;
    drawRocket(ctx,cx2,rockY,80,220,running?accel:0); // 우주선 가속 상승
    const bY2 = cy-rh*0.3; // 공은 제자리에 (관성)
    ctx.beginPath(); ctx.arc(cx2,bY2,10,0,Math.PI*2); ctx.fillStyle='#facc15'; ctx.fill();
    arrow(ctx,cx2+rw/2+10, rockY+100, cx2+rw/2+10, rockY+40, '#3b82f6');
    txt(ctx,cx2+rw/2+25, rockY+70, '가속(a)', '#3b82f6', 11, 'left');
    
    if(running){
        txt(ctx,W/2,H-30,'외부에서 보면 공은 멈춰있고 우주선 바닥이 올라옵니다!','#a78bfa',14,'center','700');
    }
}

/* ════ Phase 2: 빛의 경로 ════ */
function drawPhase2(ctx,W,H,accel,t,running){
    const cx1=W*0.27, cx2=W*0.73, cy=H*0.5, rw=120, rh=H*0.7;
    const lProg = running? (t%2500)/2500 : 0;
    const lyIn=cy-30, lxIn_dist=rw*0.4;

    dashedRect(ctx,cx1-rw/2,cy-rh/2,rw,rh,'#fff4');
    drawRocket(ctx,cx1,cy+30,80,220,0);
    ctx.strokeStyle='#fde047'; ctx.lineWidth=2; ctx.beginPath();
    ctx.moveTo(cx1-lxIn_dist, lyIn); ctx.lineTo(cx1-lxIn_dist+rw*0.8*Math.min(lProg*1.5,1), lyIn); ctx.stroke();
    txt(ctx,cx1,cy-rh/2-15,'정지 좌표계 (빛 직진)','white',12);

    dashedRect(ctx,cx2-rw/2,cy-rh/2,rw,rh,'#f8717144');
    drawRocket(ctx,cx2,cy+30,80,220,running?accel:0);
    ctx.strokeStyle='#fde047'; ctx.beginPath();
    const steps=40; const bend= (accel/9.8)*25;
    for(let i=0;i<steps*lProg*1.3;i++){
        let fr=i/steps; let px=cx2-lxIn_dist+rw*0.8*fr; let py=lyIn+fr*fr*bend;
        if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }
    ctx.stroke();
    txt(ctx,cx2,cy-rh/2-15,'가속 좌표계 (빛 휨)','white',12);
}

/* ════ Phase 3: 등가 원리 ════ */
function drawPhase3(ctx,W,H,accel,t,running){
    const cx=W/2, cy=H*0.5;
    txt(ctx,cx,cy-100,'등가 원리 (Equivalence Principle)', '#a78bfa', 22, 'center', '800');
    txt(ctx,cx-180, cy, '가속(a)에 의한 관성력', '#ec4899', 16);
    txt(ctx,cx+180, cy, '질량(M)에 의한 중력', '#fbbf24', 16);
    txt(ctx,cx, cy, '≡', 'white', 40);
    txt(ctx,cx, cy+60, '둘을 구별할 물리적 방법은 없다.', '#94a3b8', 14);
}

/* ════ Phase 4: 시공간 곡률 ════ */
function drawPhase4(ctx,W,H,accel,t,running){
    const cx=W/2, cy=H*0.5;
    const massR=40+(accel/9.8)*10;
    const grid=40;
    ctx.strokeStyle='#3b82f622';
    for(let r=0;r<H;r+=grid){
        ctx.beginPath();
        for(let c=0;c<W;c+=5){
            let dx=c-cx, dy=r-cy; let dist=Math.sqrt(dx*dx+dy*dy);
            let warp= (accel/9.8)*1500/(dist+50);
            ctx.lineTo(c-dx*warp/(dist+50), r-dy*warp/(dist+50));
        }
        ctx.stroke();
    }
    const grad=ctx.createRadialGradient(cx,cy,0,cx,cy,massR);
    grad.addColorStop(0,'#fbbf24'); grad.addColorStop(1,'#92400e');
    ctx.beginPath(); ctx.arc(cx,cy,massR,0,Math.PI*2); ctx.fillStyle=grad; ctx.fill();
    txt(ctx,cx,cy+massR+25,'질량에 의해 휘어진 시공간','white',14);
}

const PHASES = [
    { label:'① 관성력 vs 중력',  desc:'우주선 내부 실험' },
    { label:'② 내부 vs 외부 시점', desc:'관찰자 위치의 차이' },
    { label:'③ 빛의 경로',       desc:'가속 좌표계에서 빛 휨' },
    { label:'④ 등가 원리',       desc:'물리적 동등성' },
    { label:'⑤ 시공간 곡률',     desc:'중력의 기하학적 본질' },
];

const App = () => {
    const [phase,   setPhase]   = useState(0);
    const [accel,   setAccel]   = useState(9.8);
    const [running, setRunning] = useState(false);
    const [t, setT]             = useState(0);
    const rafRef = useRef(null);

    useEffect(()=>{
        if(running){
            let start = performance.now() - t;
            const loop=(now)=>{ setT(now - start); rafRef.current=requestAnimationFrame(loop); };
            rafRef.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafRef.current);
        return ()=>cancelAnimationFrame(rafRef.current);
    },[running]);

    return (
        <div style={{maxWidth:1160,margin:'0 auto',display:'flex',flexDirection:'column',gap:22}}>
            <div className="card">
                <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0',marginBottom:16}}>🔍 탐구 질문</h2>
                <QnA items={QNA_ITEMS}/>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'260px 1fr',gap:16}}>
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:16}}>
                    <label>탐구 단계 선택</label>
                    <div style={{display:'flex',flexDirection:'column',gap:6}}>
                        {PHASES.map((p,i)=>(
                            <button key={i} className={`phase-btn${phase===i?' active':''}`} onClick={()=>{setPhase(i);setT(0);setRunning(false);}}>
                                <div>{p.label}</div>
                                <div style={{fontSize:11,opacity:0.6}}>{p.desc}</div>
                            </button>
                        ))}
                    </div>
                    <label>가속도 크기 (a)</label>
                    <input type="range" min="2" max="20" step="0.5" value={accel} onChange={e=>setAccel(parseFloat(e.target.value))}/>
                    <div style={{textAlign:'center',fontFamily:'Space Mono'}}>{accel.toFixed(1)} m/s²</div>
                    <button onClick={()=>setRunning(!running)} style={{padding:12,borderRadius:10,background:running?'#ef444422':'#3b82f622',color:running?'#f87171':'#60a5fa',border:`1px solid ${running?'#ef444466':'#3b82f666'}`,fontWeight:700}}>
                        {running ? '⏸ 일시 정지' : '▶ 시뮬레이션 실행'}
                    </button>
                    <button onClick={()=>{setRunning(false);setT(0);}} style={{padding:8,borderRadius:10,background:'transparent',border:'1px solid #1e293b',color:'#64748b'}}>↺ 초기화</button>
                </div>
                <div style={{background:'#070b14',borderRadius:14,border:'1px solid #1e293b',overflow:'hidden',minHeight:500}}>
                    <SimCanvas phase={phase} accel={accel} running={running} t={t}/>
                </div>
            </div>
            <div className="card"><DerivationSection/></div>
        </div>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""
    components.html(react_code, height=2200, scrolling=True)

if __name__ == "__main__":
    run_sim()
