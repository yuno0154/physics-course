import streamlit as st
import streamlit.components.v1 as components

# 페이지 설정
st.set_page_config(page_title="학습주제 5. 관성력과 중력 등가 원리 탐구", layout="wide")

def run_sim():
    # 제목 섹션
    st.title("🌓 학습주제 5. 관성력과 중력 등가 원리 탐구")
    st.markdown("가속 좌표계에서 나타나는 현상을 통해 등가 원리를 이해하고, 일반 상대성 이론의 기초를 탐구합니다.")

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
        q:'정지한 우주선과 가속 중인 우주선 안에서 공이 바닥으로 떨어진다. 두 경우를 관측만으로 구별할 수 있을까?',
        a:'구별할 수 없습니다. 정지한 우주선에서는 지구 중력(mg)이, 가속하는 우주선에서는 관성력(ma, a=g)이 공을 바닥으로 떨어뜨립니다. 내부 관찰자가 경험하는 현상은 완전히 동일합니다. 이것이 등가 원리의 핵심입니다.'
    },
    {
        q:'가속 좌표계에서 빛은 직진할까? 왜 빛의 경로가 휘는가?',
        a:'가속 좌표계에서 빛은 휘어 보입니다. 빛이 우주선을 통과하는 동안 우주선이 가속되므로, 내부 관찰자 입장에서는 빛이 포물선을 그리며 아래로 처집니다. 뉴턴 역학으로는 이를 설명할 수 없습니다.'
    },
    {
        q:'등가 원리에 의해 중력장에서도 빛이 휘어야 한다면, 뉴턴의 중력 법칙으로 이를 설명할 수 있을까?',
        a:'설명할 수 없습니다. 뉴턴의 중력은 질량이 있는 물체에만 작용하지만, 빛(광자)은 질량이 없습니다(m=0). 아인슈타인은 빛의 휨을 설명하기 위해 전혀 다른 접근이 필요하다고 판단했고, 이것이 일반 상대성 이론 탄생의 동기가 되었습니다.'
    },
    {
        q:'아인슈타인은 빛의 휨을 어떻게 설명했는가?',
        a:'아인슈타인은 중력을 힘이 아니라 시공간의 곡률로 해석했습니다. 질량이 주변 시공간을 휘게 하고, 빛은 그 휘어진 시공간을 따라 직진합니다. 빛이 직진하는데도 경로가 휘어 보이는 이유는 시공간 자체가 휘어져 있기 때문입니다.'
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
                    <div style={{maxHeight:open===i?'240px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
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
        note:'아인슈타인(1907)의 "가장 행복한 생각": 자유낙하하는 관찰자는 중력을 느끼지 못한다.'
    },
    {
        title:'Step 2. 가속 좌표계에서 빛의 경로',
        desc:'가속도 a로 위로 가속하는 우주선에서 수평으로 입사한 빛의 처짐을 계산한다.',
        formula:'\\Delta y = \\frac{1}{2}a t^2 = \\frac{1}{2}a \\left(\\frac{L}{c}\\right)^2',
        color:'#8b5cf6', bg:'#1a0d3c',
        note:'우주선 폭 L을 빛이 통과하는 시간 t = L/c 동안 우주선이 위로 ½at² 만큼 이동하므로 빛은 아래로 그만큼 처진 것처럼 보인다.'
    },
    {
        title:'Step 3. 등가 원리 적용: 중력장에서도 동일',
        desc:'등가 원리에 의해 중력장(g=a)에서도 빛이 동일하게 휘어야 한다.',
        formula:'\\Delta y_{\\text{중력}} = \\frac{1}{2}g\\left(\\frac{L}{c}\\right)^2',
        color:'#a855f7', bg:'#1e0d3c',
        note:'이 결론은 뉴턴 역학으로 설명 불가. 빛의 에너지 E=hf에서 등가 질량 m=E/c²으로 근사 계산은 가능하지만, 실제 값의 절반밖에 예측하지 못한다.'
    },
    {
        title:'Step 4. 아인슈타인의 결론: 시공간 곡률',
        desc:'빛은 직진하지만, 질량이 시공간 자체를 휘게 하므로 경로가 휘어 보인다.',
        formula:'G_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}',
        color:'#10b981', bg:'#0a1f18',
        note:'아인슈타인 장 방정식: 좌변은 시공간의 곡률(기하), 우변은 에너지-운동량(물질). 질량·에너지가 시공간을 휘고, 휘어진 시공간이 빛과 물질의 경로를 결정한다.'
    },
    {
        title:'Step 5. 실험적 검증: 1919년 일식 관측',
        desc:'에딩턴(Eddington)이 태양 근처를 지나는 별빛의 편향각을 측정했다.',
        formula:'\\delta\\theta = \\frac{4GM_{\\odot}}{c^2 R_{\\odot}} \\approx 1.75^{\\prime\\prime}',
        color:'#fbbf24', bg:'#1f1200',
        note:'뉴턴 역학 예측: 0.875초각. 일반 상대성 이론 예측: 1.75초각. 에딩턴의 측정값은 1.75초각과 일치 → 아인슈타인 이론 검증. 현대 실측값: 1.7512±0.0006초각.'
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
                <h2 style={{fontSize:18,fontWeight:800,color:'#e2e8f0'}}>개념 연결: 가속 좌표계 → 등가 원리 → 시공간 곡률</h2>
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
    // 불꽃
    if(accel > 0) {
        const fH = (20 + accel*1.5)*thrustFlicker;
        const fg = ctx.createLinearGradient(cx, cy+h/2, cx, cy+h/2+fH);
        fg.addColorStop(0,'rgba(255,200,50,0.95)');
        fg.addColorStop(0.4,'rgba(255,100,20,0.8)');
        fg.addColorStop(1,'rgba(255,40,0,0)');
        ctx.beginPath();
        ctx.moveTo(cx-10,cy+h/2-2);
        ctx.quadraticCurveTo(cx-6,cy+h/2+fH*0.6, cx, cy+h/2+fH);
        ctx.quadraticCurveTo(cx+6,cy+h/2+fH*0.6, cx+10,cy+h/2-2);
        ctx.fillStyle=fg; ctx.fill();
    }
    // 몸체
    const bg=ctx.createLinearGradient(cx-w/2,0,cx+w/2,0);
    bg.addColorStop(0,'#8aa0c0'); bg.addColorStop(0.4,'#d0dff0');
    bg.addColorStop(0.6,'#e8f0ff'); bg.addColorStop(1,'#6080a0');
    ctx.beginPath(); ctx.roundRect(cx-w/2,cy-h/2,w,h,w/4);
    ctx.fillStyle=bg; ctx.fill();
    ctx.strokeStyle='rgba(180,200,230,0.4)'; ctx.lineWidth=1; ctx.stroke();
    // 창문
    ctx.beginPath(); ctx.arc(cx, cy-h/8, w/5, 0, Math.PI*2);
    const wg=ctx.createRadialGradient(cx-2,cy-h/8-2,1,cx,cy-h/8,w/5);
    wg.addColorStop(0,'rgba(180,220,255,0.9)'); wg.addColorStop(0.5,'rgba(80,150,255,0.6)');
    wg.addColorStop(1,'rgba(20,60,120,0.8)');
    ctx.fillStyle=wg; ctx.fill();
    ctx.strokeStyle='rgba(200,220,255,0.7)'; ctx.lineWidth=1.5; ctx.stroke();
    // 인물 실루엣
    ctx.beginPath(); ctx.arc(cx,cy-h/8,w/5*0.4,0,Math.PI*2);
    ctx.fillStyle='rgba(20,40,80,0.8)'; ctx.fill();
    // 상단 캡
    ctx.beginPath(); ctx.moveTo(cx-w/2,cy-h/2);
    ctx.quadraticCurveTo(cx,cy-h/2-h*0.28,cx+w/2,cy-h/2);
    ctx.fillStyle='rgba(160,180,210,0.9)'; ctx.fill();
    // 핀
    [[-1],[1]].forEach(([d])=>{
        ctx.beginPath();
        ctx.moveTo(cx+d*w/2,cy+h/2-h*0.15);
        ctx.lineTo(cx+d*w/2+d*w*0.4,cy+h/2+h*0.1);
        ctx.lineTo(cx+d*w/2,cy+h/2);
        ctx.fillStyle='rgba(120,150,190,0.8)'; ctx.fill();
    });
}

/* ── 화살표 ── */
function arrow(ctx,x1,y1,x2,y2,color='rgba(100,200,255,0.9)',lw=2){
    const dx=x2-x1, dy=y2-y1, angle=Math.atan2(dy,dx);
    ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=lw; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    const al=10, aa=0.4;
    ctx.beginPath();
    ctx.moveTo(x2,y2);
    ctx.lineTo(x2-al*Math.cos(angle-aa),y2-al*Math.sin(angle-aa));
    ctx.moveTo(x2,y2);
    ctx.lineTo(x2-al*Math.cos(angle+aa),y2-al*Math.sin(angle+aa));
    ctx.stroke(); ctx.restore();
}

/* ── 텍스트 ── */
function txt(ctx,x,y,s,color='rgba(200,220,255,0.9)',size=12,align='center',weight='400'){
    ctx.save(); ctx.fillStyle=color; ctx.font=`${weight} ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align; ctx.fillText(s,x,y); ctx.restore();
}

/* ── 점선 사각형 ── */
function dashedRect(ctx,x,y,w,h,color,r=10){
    ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=1; ctx.setLineDash([5,5]);
    ctx.beginPath(); ctx.roundRect(x,y,w,h,r); ctx.stroke();
    ctx.setLineDash([]); ctx.restore();
}

/* ════ Phase 0: 공 낙하 비교 ════ */
function drawPhase0(ctx,W,H,accel,t,running){
    const cx1=W*0.27, cx2=W*0.73, cy=H*0.5;
    const rw=Math.min(W*0.22,130), rh=Math.min(H*0.68,320);

    // 왼쪽: 중력 우주선
    dashedRect(ctx, cx1-rw/2, cy-rh/2, rw, rh, 'rgba(255,179,71,0.25)');
    drawRocket(ctx, cx1, cy+rh*0.06, rw*0.7, rh*0.72, 0);
    // 지구 아이콘
    const earthY = cy+rh/2+28;
    const eg=ctx.createRadialGradient(cx1-4,earthY-4,3,cx1,earthY,18);
    eg.addColorStop(0,'#5090e0'); eg.addColorStop(0.6,'#2060b0'); eg.addColorStop(1,'#0a3060');
    ctx.beginPath(); ctx.arc(cx1,earthY,18,0,Math.PI*2);
    ctx.fillStyle=eg; ctx.fill();
    ctx.strokeStyle='rgba(100,180,255,0.4)'; ctx.lineWidth=1.5; ctx.stroke();
    // 중력 화살표
    arrow(ctx, cx1+rw*0.38, cy+40, cx1+rw*0.38, cy+90, 'rgba(255,179,71,0.9)');
    txt(ctx, cx1+rw*0.38+22, cy+65, 'g', 'rgba(255,179,71,0.9)', 12, 'left');
    txt(ctx, cx1, cy-rh/2-18, '중력 작용 우주선', 'rgba(255,179,71,0.8)', 13);
    txt(ctx, cx1, cy-rh/2-4, '(지구 표면)', 'rgba(255,179,71,0.5)', 11);

    // 오른쪽: 가속 우주선
    dashedRect(ctx, cx2-rw/2, cy-rh/2, rw, rh, 'rgba(74,222,128,0.25)');
    const thrust = running ? (0.88+0.24*Math.sin(t*0.02)) : 1;
    drawRocket(ctx, cx2, cy+rh*0.06, rw*0.7, rh*0.72, running?accel:0, thrust);
    // 속도 지시 별
    if(running){
        for(let i=0;i<5;i++){
            const sy=((cy-rh/2+i*(rh/4)+t*0.06)%rh)+cy-rh/2;
            const sx=cx2-rw/3+(i%3-1)*rw/6;
            ctx.beginPath(); ctx.arc(sx,sy,1.2,0,Math.PI*2);
            ctx.fillStyle='rgba(255,255,255,0.45)'; ctx.fill();
            ctx.beginPath(); ctx.moveTo(sx,sy); ctx.lineTo(sx,sy+6);
            ctx.strokeStyle='rgba(255,255,255,0.2)'; ctx.lineWidth=0.5; ctx.stroke();
        }
    }
    arrow(ctx, cx2+rw*0.38, cy+30, cx2+rw*0.38, cy-60, 'rgba(74,222,128,0.9)');
    txt(ctx, cx2+rw*0.38+22, cy-20, `a=${accel.toFixed(1)}`, 'rgba(74,222,128,0.9)', 11, 'left');
    txt(ctx, cx2, cy-rh/2-18, '가속 중인 우주선', 'rgba(74,222,128,0.8)', 13);
    txt(ctx, cx2, cy-rh/2-4, '(무중력 공간)', 'rgba(74,222,128,0.5)', 11);

    // 공 (낙하 애니메이션)
    const bStart = cy-rh*0.28;
    const bEnd   = cy+rh*0.35;
    const bY = running
        ? bStart + (bEnd-bStart)*Math.min(((t%3000)/3000)*1.4,1)
        : bStart;

    [cx1,cx2].forEach(bx=>{
        const grad=ctx.createRadialGradient(bx-3,bY-3,2,bx,bY,10);
        grad.addColorStop(0,'#fff8dc'); grad.addColorStop(0.4,'#ffcc44'); grad.addColorStop(1,'#cc8800');
        ctx.beginPath(); ctx.arc(bx,bY,10,0,Math.PI*2);
        ctx.fillStyle=grad; ctx.fill();
        ctx.strokeStyle='rgba(255,200,80,0.4)'; ctx.lineWidth=1; ctx.stroke();
        if(running && bY > bStart+10){
            arrow(ctx,bx,bY-14,bx,bY+14,'rgba(255,230,100,0.7)',1.5);
        }
    });

    // 구별 가능? 레이블
    if(running){
        const pulse=0.7+0.3*Math.sin(t*0.006);
        ctx.save();
        ctx.globalAlpha=pulse;
        txt(ctx, W/2, H-22, '→ 두 경우를 관측만으로 구별할 수 있는가?', 'rgba(167,139,250,0.95)', 14, 'center', '700');
        ctx.restore();
    }
}

/* ════ Phase 1: 빛의 경로 비교 ════ */
function drawPhase1(ctx,W,H,accel,t,running){
    const cx1=W*0.27, cx2=W*0.73, cy=H*0.5;
    const rw=Math.min(W*0.22,130), rh=Math.min(H*0.68,320);

    // 왼쪽: 정지 좌표계 (빛 직진)
    dashedRect(ctx, cx1-rw/2, cy-rh/2, rw, rh, 'rgba(255,255,100,0.15)');
    drawRocket(ctx, cx1, cy+rh*0.06, rw*0.7, rh*0.72, 0);
    txt(ctx, cx1, cy-rh/2-18, '정지 좌표계', 'rgba(255,255,100,0.8)', 13);
    txt(ctx, cx1, cy-rh/2-4, '빛은 직진', 'rgba(255,255,100,0.5)', 11);

    // 빛 진행 (직선)
    const lProg = running ? Math.min((t%2800)/2800, 1) : 0;
    const lyIn  = cy-rh*0.08;
    const lx1s  = cx1-rw*0.38, lx1e = cx1+rw*0.38;
    if(lProg > 0){
        ctx.save();
        ctx.beginPath(); ctx.rect(cx1-rw/2, cy-rh/2, rw, rh); ctx.clip();
        ctx.shadowColor='rgba(255,255,100,0.7)'; ctx.shadowBlur=8;
        ctx.strokeStyle='rgba(255,255,100,0.95)'; ctx.lineWidth=2.5;
        ctx.beginPath();
        ctx.moveTo(lx1s, lyIn);
        ctx.lineTo(lx1s+(lx1e-lx1s)*lProg, lyIn);
        ctx.stroke();
        ctx.restore();
    }
    // 빛 입자
    if(running && lProg < 0.98){
        ctx.beginPath(); ctx.arc(lx1s+(lx1e-lx1s)*lProg, lyIn, 5, 0, Math.PI*2);
        ctx.fillStyle='rgba(255,255,150,1)';
        ctx.shadowColor='rgba(255,255,100,0.9)'; ctx.shadowBlur=12; ctx.fill(); ctx.shadowBlur=0;
    }

    // 오른쪽: 가속 좌표계 (빛 휨)
    dashedRect(ctx, cx2-rw/2, cy-rh/2, rw, rh, 'rgba(248,113,113,0.2)');
    const thrust=running?(0.88+0.24*Math.sin(t*0.02)):1;
    drawRocket(ctx, cx2, cy+rh*0.06, rw*0.7, rh*0.72, running?accel:0, thrust);
    txt(ctx, cx2, cy-rh/2-18, '가속 좌표계', 'rgba(248,113,113,0.8)', 13);
    txt(ctx, cx2, cy-rh/2-4, '빛이 휜다!', 'rgba(248,113,113,0.5)', 11);

    // 빛 경로 (포물선 휨)
    const lx2s = cx2-rw*0.38, lx2e = cx2+rw*0.38;
    const bendAmt = (accel/9.8)*22;
    if(lProg > 0){
        ctx.save();
        ctx.beginPath(); ctx.rect(cx2-rw/2, cy-rh/2, rw, rh); ctx.clip();
        ctx.shadowColor='rgba(255,255,100,0.7)'; ctx.shadowBlur=8;
        ctx.strokeStyle='rgba(255,255,100,0.95)'; ctx.lineWidth=2.5;
        ctx.beginPath();
        const steps=60;
        for(let i=0;i<=steps*lProg;i++){
            const frac=i/steps;
            const px=lx2s+(lx2e-lx2s)*frac;
            const py=lyIn+frac*frac*bendAmt;
            if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
        }
        ctx.stroke();
        // 기준선 (직선)
        ctx.shadowBlur=0;
        ctx.strokeStyle='rgba(255,255,100,0.2)'; ctx.lineWidth=1;
        ctx.setLineDash([4,4]);
        ctx.beginPath(); ctx.moveTo(lx2s,lyIn); ctx.lineTo(lx2s+(lx2e-lx2s)*lProg,lyIn);
        ctx.stroke(); ctx.setLineDash([]);
        // 처짐 표시
        if(lProg>0.8){
            const endX=lx2e, endY=lyIn+bendAmt;
            ctx.shadowBlur=0; ctx.strokeStyle='rgba(248,113,113,0.6)'; ctx.lineWidth=1;
            ctx.setLineDash([2,3]);
            ctx.beginPath(); ctx.moveTo(endX,lyIn); ctx.lineTo(endX,endY); ctx.stroke();
            ctx.setLineDash([]);
            txt(ctx, endX+12, (lyIn+endY)/2, `Δy=${bendAmt.toFixed(0)}`, 'rgba(248,113,113,0.8)', 10, 'left');
        }
        ctx.restore();
    }
    if(running && lProg < 0.98){
        const frac=lProg;
        const px=lx2s+(lx2e-lx2s)*frac, py=lyIn+frac*frac*bendAmt;
        ctx.beginPath(); ctx.arc(px,py,5,0,Math.PI*2);
        ctx.fillStyle='rgba(255,255,150,1)';
        ctx.shadowColor='rgba(255,255,100,0.9)'; ctx.shadowBlur=14; ctx.fill(); ctx.shadowBlur=0;
    }

    if(lProg>0.6){
        txt(ctx, W/2, H-22, '→ 뉴턴 역학으로 빛의 휨을 설명할 수 없다! 새로운 이론이 필요하다.', 'rgba(248,113,113,0.9)', 13, 'center', '700');
    }
}

/* ════ Phase 2: 등가 원리 다이어그램 ════ */
function drawPhase2(ctx,W,H,accel,t,running){
    const cx=W/2, cy=H*0.47;
    const bw=W*0.72, bh=H*0.72;

    // 외곽 박스
    ctx.save();
    ctx.strokeStyle='rgba(167,139,250,0.35)'; ctx.lineWidth=1.5;
    ctx.setLineDash([7,5]);
    ctx.beginPath(); ctx.roundRect(cx-bw/2,cy-bh/2,bw,bh,14); ctx.stroke();
    ctx.setLineDash([]); ctx.restore();
    txt(ctx, cx, cy-bh/2-20, '등가 원리 (Equivalence Principle)', 'rgba(167,139,250,0.9)', 15, 'center', '800');

    const lx=cx-bw*0.26, rx=cx+bw*0.26;
    const iw=bw*0.36, ih=bh*0.76;

    // 왼쪽 박스: 중력
    ctx.save();
    ctx.fillStyle='rgba(255,179,71,0.06)'; ctx.strokeStyle='rgba(255,179,71,0.3)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.roundRect(lx-iw/2,cy-ih/2,iw,ih,10);
    ctx.fill(); ctx.stroke(); ctx.restore();
    txt(ctx,lx,cy-ih*0.35,'중력장 (g)','rgba(255,179,71,0.9)',14,'center','700');
    txt(ctx,lx,cy-ih*0.18,'공이 바닥으로 낙하','rgba(200,180,120,0.8)',12);
    txt(ctx,lx,cy-ih*0.06,'빛이 아래로 휜다','rgba(200,180,120,0.8)',12);
    // 작은 공+화살
    const bY2=cy+ih*0.1;
    ctx.beginPath(); ctx.arc(lx,bY2,8,0,Math.PI*2);
    const g1=ctx.createRadialGradient(lx-2,bY2-2,1,lx,bY2,8);
    g1.addColorStop(0,'#fff8dc'); g1.addColorStop(1,'#cc8800');
    ctx.fillStyle=g1; ctx.fill();
    arrow(ctx,lx,bY2+10,lx,bY2+26,'rgba(255,179,71,0.8)',1.5);
    txt(ctx,lx,cy+ih*0.35,'F = mg','rgba(255,179,71,0.6)',13,'center','700');

    // 오른쪽 박스: 관성력
    ctx.save();
    ctx.fillStyle='rgba(74,222,128,0.06)'; ctx.strokeStyle='rgba(74,222,128,0.3)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.roundRect(rx-iw/2,cy-ih/2,iw,ih,10);
    ctx.fill(); ctx.stroke(); ctx.restore();
    txt(ctx,rx,cy-ih*0.35,`가속 좌표계 (a=g)`,'rgba(74,222,128,0.9)',14,'center','700');
    txt(ctx,rx,cy-ih*0.18,'공이 바닥으로 낙하','rgba(140,200,160,0.8)',12);
    txt(ctx,rx,cy-ih*0.06,'빛이 아래로 휜다','rgba(140,200,160,0.8)',12);
    ctx.beginPath(); ctx.arc(rx,bY2,8,0,Math.PI*2);
    const g2=ctx.createRadialGradient(rx-2,bY2-2,1,rx,bY2,8);
    g2.addColorStop(0,'#f0fff4'); g2.addColorStop(1,'#16a34a');
    ctx.fillStyle=g2; ctx.fill();
    arrow(ctx,rx,bY2+10,rx,bY2+26,'rgba(74,222,128,0.8)',1.5);
    txt(ctx,rx,cy+ih*0.35,'F = ma','rgba(74,222,128,0.6)',13,'center','700');

    // 가운데 ≡ 기호
    const pulse=0.7+0.3*Math.sin(t*0.005);
    ctx.save(); ctx.globalAlpha=pulse;
    txt(ctx,cx,cy+ih*0.08,'≡','rgba(167,139,250,0.9)',38,'center','800');
    txt(ctx,cx,cy+ih*0.24,'물리적으로 동등','rgba(167,139,250,0.75)',12);
    ctx.restore();

    // 하단 결론
    ctx.save();
    ctx.fillStyle='rgba(167,139,250,0.08)'; ctx.strokeStyle='rgba(167,139,250,0.25)'; ctx.lineWidth=0.5;
    ctx.beginPath(); ctx.roundRect(cx-bw*0.44,cy+bh/2-44,bw*0.88,38,7);
    ctx.fill(); ctx.stroke(); ctx.restore();
    txt(ctx,cx,cy+bh/2-21,'관측만으로는 두 상황을 구별할 방법이 없다 → 중력의 새로운 해석이 필요하다','rgba(200,190,255,0.9)',12,'center','600');
}

/* ════ Phase 3: 시공간 곡률 ════ */
function drawPhase3(ctx,W,H,accel,t,running){
    const cx=W/2, cy=H*0.46;
    const massR=34+(accel/9.8)*8;
    const massStrength=160*(accel/9.8);

    // 격자 (시공간 휨)
    const step=46, cols=Math.ceil(W/step)+2, rows=Math.ceil(H*0.82/step)+2;
    ctx.save(); ctx.strokeStyle='rgba(100,160,255,0.14)'; ctx.lineWidth=0.8;
    const gridOffY=H*0.07;
    for(let r=0;r<rows;r++){
        ctx.beginPath();
        for(let c=0;c<=cols;c++){
            const gx=c*step-step, gy=r*step+gridOffY;
            const dx=gx-cx, dy=gy-cy;
            const dist=Math.sqrt(dx*dx+dy*dy);
            const warp=massStrength/(dist+55);
            const wx=gx-dx*warp/(dist+55);
            const wy=gy-dy*warp/(dist+55);
            if(c===0) ctx.moveTo(wx,wy); else ctx.lineTo(wx,wy);
        }
        ctx.stroke();
    }
    for(let c=0;c<cols;c++){
        ctx.beginPath();
        for(let r=0;r<=rows;r++){
            const gx=c*step-step, gy=r*step+gridOffY;
            const dx=gx-cx, dy=gy-cy;
            const dist=Math.sqrt(dx*dx+dy*dy);
            const warp=massStrength/(dist+55);
            const wx=gx-dx*warp/(dist+55);
            const wy=gy-dy*warp/(dist+55);
            if(r===0) ctx.moveTo(wx,wy); else ctx.lineTo(wx,wy);
        }
        ctx.stroke();
    }
    ctx.restore();

    // 질량 천체
    const mg=ctx.createRadialGradient(cx-8,cy-8,4,cx,cy,massR);
    mg.addColorStop(0,'rgba(200,180,80,0.95)'); mg.addColorStop(0.5,'rgba(140,100,40,0.85)');
    mg.addColorStop(1,'rgba(60,40,10,0.7)');
    ctx.beginPath(); ctx.arc(cx,cy,massR,0,Math.PI*2);
    ctx.fillStyle=mg; ctx.fill();
    ctx.strokeStyle='rgba(255,200,80,0.35)'; ctx.lineWidth=1.5; ctx.stroke();
    txt(ctx,cx,cy+6,'M','rgba(255,220,100,0.9)',18,'center','700');
    txt(ctx,cx,cy+massR+17,`질량 M (중력: ${accel.toFixed(1)}×)`, 'rgba(200,180,100,0.65)',11);

    // 빛 경로 (시간에 따라 진행)
    const lProg = running ? ((t%5000)/5000) : 0.85;
    const lx1=W*0.04, lx2=W*0.96, ly0=cy-H*0.27;
    ctx.save();
    ctx.strokeStyle='rgba(255,255,100,0.92)'; ctx.lineWidth=2.5;
    ctx.shadowColor='rgba(255,255,100,0.55)'; ctx.shadowBlur=6;
    ctx.beginPath();
    const steps=200;
    for(let i=0;i<=steps*lProg;i++){
        const frac=i/steps;
        const lx=lx1+(lx2-lx1)*frac;
        const dx=lx-cx, dy=ly0-cy;
        const dist=Math.sqrt(dx*dx+dy*dy);
        const deflect=(massStrength*0.65)/(dist+48);
        const loco=1-Math.abs(lx-cx)/(lx2-lx1)*0.75;
        const ly=ly0+deflect*loco;
        if(i===0) ctx.moveTo(lx,ly); else ctx.lineTo(lx,ly);
    }
    ctx.stroke(); ctx.restore();

    // 기준 직선
    ctx.save(); ctx.strokeStyle='rgba(255,255,100,0.17)'; ctx.lineWidth=1;
    ctx.setLineDash([5,5]);
    ctx.beginPath(); ctx.moveTo(lx1,ly0); ctx.lineTo(lx2,ly0);
    ctx.stroke(); ctx.setLineDash([]); ctx.restore();

    // 빛 입자
    if(running && lProg<0.98){
        const frac=lProg;
        const lx=lx1+(lx2-lx1)*frac;
        const dx=lx-cx, dy=ly0-cy;
        const dist=Math.sqrt(dx*dx+dy*dy);
        const deflect=(massStrength*0.65)/(dist+48);
        const ly=ly0+deflect*(1-Math.abs(lx-cx)/(lx2-lx1)*0.75);
        ctx.beginPath(); ctx.arc(lx,ly,5,0,Math.PI*2);
        ctx.fillStyle='rgba(255,255,150,1)';
        ctx.shadowColor='rgba(255,255,100,0.9)'; ctx.shadowBlur=14; ctx.fill(); ctx.shadowBlur=0;
    }

    // 레이블
    txt(ctx,lx1+40,ly0-14,'빛 (기준 직선)','rgba(255,255,100,0.3)',11,'left');
    txt(ctx,lx1+40,ly0+32,'실제 빛 경로 (시공간이 휘어짐)','rgba(255,255,100,0.9)',11,'left');

    // 아인슈타인 결론 박스
    ctx.save();
    ctx.fillStyle='rgba(10,15,35,0.88)'; ctx.strokeStyle='rgba(167,139,250,0.4)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.roundRect(W*0.63,H*0.7,W*0.33,70,9); ctx.fill(); ctx.stroke();
    txt(ctx,W*0.63+13,H*0.7+22,'아인슈타인의 결론:','rgba(167,139,250,0.9)',12,'left','700');
    txt(ctx,W*0.63+13,H*0.7+40,'빛은 직진하지만 시공간이','rgba(200,190,255,0.8)',11,'left');
    txt(ctx,W*0.63+13,H*0.7+56,'질량에 의해 휘어져 있다.','rgba(200,190,255,0.8)',11,'left');
    ctx.restore();

    // 1919 관측 박스
    ctx.save();
    ctx.fillStyle='rgba(10,15,35,0.82)'; ctx.strokeStyle='rgba(255,200,80,0.3)'; ctx.lineWidth=0.8;
    ctx.beginPath(); ctx.roundRect(W*0.03,H*0.7,W*0.33,70,9); ctx.fill(); ctx.stroke();
    txt(ctx,W*0.03+12,H*0.7+22,'1919년 일식 관측 (에딩턴)','rgba(255,200,80,0.88)',11,'left','700');
    txt(ctx,W*0.03+12,H*0.7+40,'태양 근처 별빛 편향: 1.75″','rgba(220,200,160,0.75)',11,'left');
    txt(ctx,W*0.03+12,H*0.7+56,'→ 일반 상대성 이론 최초 검증','rgba(220,200,160,0.75)',11,'left');
    ctx.restore();
}

/* ════════════════════════════════════════════
   메인 앱
════════════════════════════════════════════ */
const PHASES = [
    { label:'① 공 낙하 비교',    desc:'중력 vs 가속 좌표계' },
    { label:'② 빛의 경로',       desc:'가속 좌표계에서 빛 휨' },
    { label:'③ 등가 원리',       desc:'물리적 동등성' },
    { label:'④ 시공간 곡률',     desc:'중력의 기하학적 본질' },
];

const App = () => {
    const [phase,   setPhase]   = useState(0);
    const [accel,   setAccel]   = useState(9.8);
    const [running, setRunning] = useState(false);
    const [t, setT]             = useState(0);
    const rafRef = useRef(null);
    const startRef = useRef(null);

    useEffect(()=>{
        if(running){
            startRef.current = performance.now() - t;
            const loop=(now)=>{
                setT(now - startRef.current);
                rafRef.current=requestAnimationFrame(loop);
            };
            rafRef.current=requestAnimationFrame(loop);
        } else {
            if(rafRef.current) cancelAnimationFrame(rafRef.current);
        }
        return ()=>{ if(rafRef.current) cancelAnimationFrame(rafRef.current); };
    },[running]);

    const handlePhase=(i)=>{ setPhase(i); setRunning(false); setT(0); };

    return (
        <div style={{maxWidth:1160,margin:'0 auto',display:'flex',flexDirection:'column',gap:22}}>

            {/* ── ① 탐구 질문 ── */}
            <div className="card">
                <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:16}}>
                    <div style={{width:4,height:22,background:'#fbbf24',borderRadius:2}}/>
                    <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0'}}>🔍 탐구 질문</h2>
                </div>
                <QnA items={QNA_ITEMS}/>
            </div>

            {/* ── ② 시뮬레이션 ── */}
            <div style={{display:'grid',gridTemplateColumns:'260px 1fr',gap:16}}>

                {/* 왼쪽 컨트롤 패널 */}
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:16}}>
                    <div>
                        <h2 style={{fontSize:18,fontWeight:800,color:'#e2e8f0',marginBottom:4}}>탐구 시뮬레이션</h2>
                        <p style={{color:'#475569',fontSize:12,fontStyle:'italic'}}>단계별로 탐구 순서를 따라가 보세요.</p>
                    </div>

                    {/* 단계 선택 */}
                    <div>
                        <label>탐구 단계 선택</label>
                        <div style={{display:'flex',flexDirection:'column',gap:6,marginTop:4}}>
                            {PHASES.map((p,i)=>(
                                <button key={i} className={`phase-btn${phase===i?' active':''}`} onClick={()=>handlePhase(i)}>
                                    <div style={{fontWeight:phase===i?700:400}}>{p.label}</div>
                                    <div style={{fontSize:11,color:phase===i?'#93c5fd':'#475569',marginTop:1}}>{p.desc}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* 가속도 조절 */}
                    <div>
                        <label>가속도 / 중력 크기</label>
                        <input type="range" min="2" max="20" step="0.2" value={accel}
                            onChange={e=>setAccel(parseFloat(e.target.value))}/>
                        <p style={{textAlign:'center',fontSize:12,color:'#64748b',marginTop:4,fontFamily:'Space Mono,monospace'}}>
                            {accel.toFixed(1)} m/s²
                        </p>
                    </div>

                    {/* 실행 / 정지 */}
                    <button onClick={()=>setRunning(r=>!r)} style={{
                        padding:'11px',borderRadius:10,border:'none',cursor:'pointer',fontFamily:'inherit',
                        fontSize:14,fontWeight:700,
                        background: running ? 'rgba(239,68,68,0.15)' : 'rgba(59,130,246,0.15)',
                        color: running ? '#f87171' : '#60a5fa',
                        border: `1px solid ${running?'rgba(239,68,68,0.4)':'rgba(59,130,246,0.4)'}`,
                        transition:'all 0.2s'
                    }}>
                        {running ? '⏸ 일시 정지' : '▶ 시뮬레이션 실행'}
                    </button>
                    <button onClick={()=>{ setRunning(false); setT(0); }} style={{
                        padding:'8px',borderRadius:10,border:'1px solid #1e293b',background:'transparent',
                        color:'#64748b',cursor:'pointer',fontFamily:'inherit',fontSize:13
                    }}>
                        ↺ 초기화
                    </button>

                    {/* 현재 단계 요약 */}
                    <div style={{background:'#070b14',borderRadius:10,padding:'12px 14px',border:'1px solid #1e293b'}}>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>현재 단계</span>
                            <span className="result-val" style={{fontSize:12}}>{PHASES[phase].label}</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>설정 가속도</span>
                            <span className="result-val">{accel.toFixed(1)} m/s²</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>빛의 처짐(Δy)</span>
                            <span className="result-val" style={{color:'#f87171'}}>
                                {(accel/9.8*22).toFixed(1)} px
                            </span>
                        </div>
                    </div>

                    <div style={{fontSize:11,color:'#334155',lineHeight:1.8,borderTop:'1px solid #1e293b',paddingTop:10}}>
                        <p>* 가속도를 크게 하면 빛의 처짐과 시공간 곡률이 강해집니다.</p>
                        <p>* 시공간 격자가 휘는 정도는 질량(중력)에 비례합니다.</p>
                    </div>
                </div>

                {/* 캔버스 */}
                <div style={{background:'#070b14',borderRadius:14,border:'1px solid #1e293b',overflow:'hidden',minHeight:620}}>
                    <SimCanvas phase={phase} accel={accel} running={running} t={t}/>
                </div>
            </div>

            {/* ── ③ 개념 연결 유도 ── */}
            <div className="card">
                <DerivationSection/>
            </div>

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
