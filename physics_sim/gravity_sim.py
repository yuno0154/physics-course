import streamlit as st
import streamlit.components.v1 as components

def run_sim():

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
input[type=number]{background:#070b14;border:1px solid #1e293b;border-radius:8px;color:#e2e8f0;
  padding:8px 10px;font-size:13px;width:100%;outline:none;font-family:inherit;}
input[type=number]:focus{border-color:#3b82f6;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#3b82f6;cursor:pointer;box-shadow:0 0 8px rgba(59,130,246,0.6);}
label{font-size:11px;color:#64748b;font-weight:700;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.04em;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.result-val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;font-size:14px;}
.preset-btn{padding:5px 12px;background:#1e293b;border:1px solid #334155;border-radius:8px;color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;}
.preset-btn:hover{border-color:#3b82f6;color:#e2e8f0;}
.acc-step-btn{width:100%;display:flex;align-items:center;gap:12;padding:14px 18px;background:transparent;border:none;cursor:pointer;text-align:left;font-family:inherit;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const PRESETS = [
    { name:'지구', M:5.972e24, R:6371000 },
    { name:'달',   M:7.342e22, R:1737000 },
    { name:'화성', M:6.390e23, R:3390000 },
    { name:'목성', M:1.898e27, R:69911000 },
    { name:'태양', M:1.989e30, R:696000000 },
];

const fmt = (v, d=3) => {
    if (!isFinite(v)) return '—';
    if (Math.abs(v) >= 1e15 || (Math.abs(v) < 0.001 && v !== 0))
        return v.toExponential(d);
    return v.toLocaleString('ko-KR', {maximumFractionDigits: d});
};

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
        q:'지구가 물체에 작용하는 중력의 크기는 물체의 질량에 비례하지만, 중력 가속도는 물체의 질량과 무관하게 일정한 이유는 무엇일까?',
        a:'F = GMm/r² 이므로 중력은 m에 비례합니다. 그런데 뉴턴의 제2법칙에서 a = F/m = GM/r² 이 되어 m이 약분됩니다. 질량이 크면 중력도 그만큼 커지지만, 가속시키기도 더 어려워 정확히 상쇄됩니다.'
    },
    {
        q:'중력 가속도의 크기는 지구로부터 멀어지면 작아진다. 거리와 중력 가속도와의 관계는?',
        a:'g = GM/r² 이므로 g ∝ 1/r² 입니다. 역제곱 법칙에 따라 거리가 2배가 되면 중력 가속도는 1/4배로 줄어듭니다.'
    },
    {
        q:'거리와 중력의 관계는?',
        a:'F = GMm/r² 이므로 F ∝ 1/r² 입니다 (m 일정). 중력도 역제곱 법칙을 따르며, 거리가 2배가 되면 중력의 크기는 1/4배가 됩니다.'
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
                    <div style={{maxHeight:open===i?'200px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
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

/* ── 수식 유도 아코디언 단계 ── */
const DERIVE_STEPS = [
    {
        title:'Step 1. 뉴턴의 제2법칙 적용',
        desc:'물체에 알짜힘 F가 작용하면 가속도 a가 생긴다.',
        formula:'F = m \\cdot a',
        color:'#3b82f6', bg:'#0d1f3c',
        note:'여기서 m은 물체의 질량, a는 물체에 생기는 가속도입니다.'
    },
    {
        title:'Step 2. 만유인력 법칙 대입',
        desc:'지구가 물체에 작용하는 중력(만유인력)의 크기는 다음과 같습니다.',
        formula:'F = \\dfrac{G M m}{r^2}',
        color:'#8b5cf6', bg:'#1a0d3c',
        note:'G: 중력 상수, M: 지구 질량, m: 물체 질량, r: 지구 중심까지의 거리'
    },
    {
        title:'Step 3. 두 식을 같다고 놓기',
        desc:'중력이 물체를 가속시키는 힘이므로 두 식을 등치합니다.',
        formula:'m \\cdot a = \\dfrac{G M m}{r^2}',
        color:'#a855f7', bg:'#1e0d3c',
        note:'좌변은 제2법칙, 우변은 만유인력입니다.'
    },
    {
        title:'Step 4. 양변을 물체 질량 m으로 나누기',
        desc:'양변을 m으로 나누면 m이 완전히 사라집니다.',
        formula:'a = \\dfrac{G M}{r^2}',
        color:'#10b981', bg:'#0a1f18',
        note:'m이 약분되어 사라졌습니다! 가속도는 물체의 질량에 무관합니다.'
    },
    {
        title:'Step 5. 결론: 중력 가속도 g의 정의',
        desc:'이 가속도를 중력 가속도 g라 정의하면 최종 결론이 완성됩니다.',
        formula:'g = \\dfrac{G M}{r^2}',
        color:'#fbbf24', bg:'#1f1200',
        note:'g는 오직 중심 천체의 질량 M과 거리 r에만 의존합니다. 지표면에서 r = R이면 g ≈ 9.8 m/s².'
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
                <h2 style={{fontSize:18,fontWeight:800,color:'#e2e8f0'}}>수식 유도: 왜 g는 m에 무관할까?</h2>
            </div>
            <p style={{color:'#475569',fontSize:13,marginBottom:18,marginLeft:14}}>
                각 단계를 클릭해 수식 유도 과정을 확인하세요.
            </p>
            <div style={{display:'flex',flexDirection:'column',gap:10}}>
                {DERIVE_STEPS.map((step,i)=>(
                    <div key={i} style={{border:`1px solid ${open===i?step.color+'80':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
                        {/* 헤더 */}
                        <button onClick={()=>setOpen(open===i?null:i)}
                            style={{width:'100%',display:'flex',alignItems:'center',gap:14,padding:'14px 18px',background:'#0d1526',border:'none',cursor:'pointer',fontFamily:'inherit',textAlign:'left'}}>
                            <div style={{width:32,height:32,borderRadius:'50%',background:step.color,display:'flex',alignItems:'center',justifyContent:'center',
                                color:'white',fontWeight:800,fontSize:14,flexShrink:0}}>
                                {i+1}
                            </div>
                            <div style={{flex:1}}>
                                <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700}}>{step.title}</p>
                                <p style={{color:'#475569',fontSize:12,marginTop:2}}>{step.desc}</p>
                            </div>
                            <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
                        </button>
                        {/* 펼침 내용 */}
                        <div style={{maxHeight:open===i?'260px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                            <div style={{padding:'20px 24px 20px',background:step.bg,display:'flex',flexDirection:'column',gap:14}}>
                                {/* 수식 */}
                                <div style={{background:'rgba(0,0,0,0.3)',borderRadius:12,padding:'18px 24px',
                                    display:'flex',justifyContent:'center',border:`1px solid ${step.color}30`}}>
                                    {kReady
                                        ? <Math_ f={step.formula} display={true}
                                            style={{color:step.color,fontSize:'1.3em'}}/>
                                        : <span style={{color:step.color,fontFamily:'monospace',fontSize:15}}>{step.formula}</span>
                                    }
                                </div>
                                {/* 설명 */}
                                <div style={{display:'flex',gap:10,alignItems:'flex-start'}}>
                                    <span style={{fontSize:16,flexShrink:0}}>💡</span>
                                    <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{step.note}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            {/* 최종 결론 박스 */}
            <div style={{marginTop:20,background:'linear-gradient(135deg,#064e3b,#065f46)',borderRadius:16,padding:'20px 28px',border:'1px solid #10b981',display:'flex',alignItems:'center',gap:20}}>
                <div style={{fontSize:32}}>✅</div>
                <div>
                    <p style={{color:'#34d399',fontWeight:800,fontSize:15,marginBottom:4}}>결론</p>
                    <p style={{color:'#6ee7b7',fontSize:13,lineHeight:1.7}}>
                        중력의 크기 F는 m에 비례하지만, 가속도 g = F/m 을 구하면 m이 완전히 약분됩니다.<br/>
                        따라서 <strong style={{color:'#34d399'}}>중력 가속도 g = GM/r²</strong>는 물체의 질량 m과 무관하며,<br/>
                        오직 중심 천체의 질량 M과 거리 r에만 의존합니다.
                    </p>
                </div>
            </div>
        </div>
    );
};

/* ── 행성 Canvas ── */
const PlanetCanvas = ({ G, M, R, m, h_km }) => {
    const ref = useRef(null);
    const v   = useRef({ G, M, R, m, h_km });
    v.current = { G, M, R, m, h_km };

    const draw = () => {
        const canvas = ref.current; if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const { G, M, R, m, h_km } = v.current;
        const w = canvas.width, h = canvas.height;
        const cx = w*0.42, cy = h/2;
        ctx.clearRect(0,0,w,h);
        ctx.fillStyle='#070b14'; ctx.fillRect(0,0,w,h);
        for(let i=0;i<80;i++){
            const sx=(i*137.508)%w, sy=(i*97.3+i*13)%h;
            ctx.beginPath(); ctx.arc(sx,sy,0.6+(i%3)*0.4,0,Math.PI*2);
            ctx.fillStyle=`rgba(200,220,255,${0.15+(i%5)*0.07})`; ctx.fill();
        }
        const pR=Math.min(w,h)*0.31;
        const gw=ctx.createRadialGradient(cx,cy,pR*0.3,cx,cy,pR*2);
        gw.addColorStop(0,'rgba(59,130,246,0.3)'); gw.addColorStop(1,'rgba(59,130,246,0)');
        ctx.beginPath(); ctx.arc(cx,cy,pR*2,0,Math.PI*2); ctx.fillStyle=gw; ctx.fill();
        const pg=ctx.createRadialGradient(cx-pR*.22,cy-pR*.22,pR*.04,cx,cy,pR);
        pg.addColorStop(0,'#93c5fd'); pg.addColorStop(0.35,'#3b82f6'); pg.addColorStop(1,'#1e3a8a');
        ctx.beginPath(); ctx.arc(cx,cy,pR,0,Math.PI*2); ctx.fillStyle=pg; ctx.fill();
        const MAX_H=50000;
        const objPx=pR+(Math.min(h_km,MAX_H)/MAX_H)*pR*1.6;
        const ox=cx+objPx, oy=cy;
        const arLen=Math.min(objPx-pR-14,80);
        if(arLen>6){
            ctx.beginPath(); ctx.moveTo(ox-8,oy); ctx.lineTo(ox-8-arLen,oy);
            ctx.strokeStyle='#ef4444'; ctx.lineWidth=2.5; ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(ox-8-arLen,oy); ctx.lineTo(ox-8-arLen+9,oy-5); ctx.lineTo(ox-8-arLen+9,oy+5);
            ctx.closePath(); ctx.fillStyle='#ef4444'; ctx.fill();
        }
        const og=ctx.createRadialGradient(ox-2,oy-2,0,ox,oy,8);
        og.addColorStop(0,'#fed7aa'); og.addColorStop(1,'#ea580c');
        ctx.beginPath(); ctx.arc(ox,oy,8,0,Math.PI*2); ctx.fillStyle=og; ctx.fill();
        ctx.beginPath(); ctx.arc(ox,oy,12,0,Math.PI*2);
        ctx.strokeStyle='rgba(251,146,60,0.35)'; ctx.lineWidth=2; ctx.stroke();
        const g_val=G*M/Math.pow(R+h_km*1000,2);
        ctx.fillStyle='#fbbf24'; ctx.font='bold 13px "Space Mono",monospace';
        ctx.fillText(`g = ${g_val.toFixed(3)}`, ox+14, oy-6);
        ctx.fillStyle='#64748b'; ctx.font='11px sans-serif';
        ctx.fillText(`h = ${h_km.toLocaleString()} km`, ox+14, oy+14);
        const pxPerKm=(pR*1.6)/MAX_H;
        ctx.fillStyle='rgba(100,116,139,0.7)'; ctx.font='11px sans-serif';
        ctx.textAlign='right';
        ctx.fillText(`거리 스케일: 1px ≈ ${Math.round(1/pxPerKm)} km (가변)`, w-10, h-10);
        ctx.textAlign='left';
    };

    useEffect(()=>{
        const canvas=ref.current; if(!canvas) return;
        const resize=()=>{ canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw(); };
        const ro=new ResizeObserver(resize); ro.observe(canvas); resize();
        return ()=>ro.disconnect();
    },[]);
    useEffect(()=>{ draw(); },[G,M,R,m,h_km]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ── 그래프 Canvas ── */
const GraphCanvas = ({ G, M, R, h_km }) => {
    const ref = useRef(null);
    const v   = useRef({ G, M, R, h_km });
    v.current = { G, M, R, h_km };

    const draw = () => {
        const canvas=ref.current; if(!canvas) return;
        const ctx=canvas.getContext('2d');
        const { G, M, R, h_km }=v.current;
        const w=canvas.width, h=canvas.height;
        const ml=44, mr=16, mt=14, mb=32;
        const gw=w-ml-mr, gh=h-mt-mb;
        ctx.clearRect(0,0,w,h);
        ctx.fillStyle='#070b14'; ctx.fillRect(0,0,w,h);
        ctx.fillStyle='#0a0f1e'; ctx.fillRect(ml,mt,gw,gh);
        const maxR=R*10, g0=G*M/(R*R);
        for(let i=0;i<=4;i++){
            const gy=mt+gh*(i/4);
            ctx.beginPath(); ctx.moveTo(ml,gy); ctx.lineTo(ml+gw,gy);
            ctx.strokeStyle='rgba(30,41,59,0.9)'; ctx.lineWidth=1; ctx.stroke();
            ctx.fillStyle='#475569'; ctx.font='10px monospace';
            ctx.textAlign='right';
            ctx.fillText((g0*(1-i/4)).toFixed(1), ml-4, gy+4);
            ctx.textAlign='left';
        }
        ctx.beginPath();
        for(let px=0;px<=gw;px++){
            const r=R+(px/gw)*(maxR-R);
            const g=G*M/(r*r);
            const gy=mt+gh*(1-Math.min(g/g0,1));
            if(px===0) ctx.moveTo(ml+px,gy); else ctx.lineTo(ml+px,gy);
        }
        ctx.strokeStyle='#3b82f6'; ctx.lineWidth=2.5; ctx.stroke();
        const curR=R+h_km*1000;
        const curG=G*M/(curR*curR);
        const cpx=ml+((curR-R)/(maxR-R))*gw;
        const cpy=mt+gh*(1-Math.min(curG/g0,1));
        ctx.beginPath(); ctx.arc(cpx,cpy,5,0,Math.PI*2);
        ctx.fillStyle='#ef4444'; ctx.fill();
        ctx.beginPath(); ctx.arc(cpx,cpy,9,0,Math.PI*2);
        ctx.strokeStyle='rgba(239,68,68,0.4)'; ctx.lineWidth=2; ctx.stroke();
        ctx.fillStyle='#475569'; ctx.font='11px sans-serif';
        ctx.fillText('지표면 (h=0)', ml, h-8);
        ctx.textAlign='right';
        ctx.fillText('중심으로부터의 거리 (r) →', w-mr, h-8);
        ctx.textAlign='left';
    };

    useEffect(()=>{
        const canvas=ref.current; if(!canvas) return;
        const resize=()=>{ canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw(); };
        const ro=new ResizeObserver(resize); ro.observe(canvas); resize();
        return ()=>ro.disconnect();
    },[]);
    useEffect(()=>{ draw(); },[G,M,R,h_km]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ── 메인 앱 ── */
const App = () => {
    const [G, setG]    = useState(6.674e-11);
    const [M, setM]    = useState(5.972e24);
    const [R, setR]    = useState(6371000);
    const [m, setm]    = useState(1.0);
    const [h_km, setH] = useState(0);

    const r = R + h_km * 1000;
    const g = G * M / (r * r);
    const F = G * M * m / (r * r);

    const applyPreset = p => { setM(p.M); setR(p.R); setH(0); };

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

            {/* ── ② 중력 계산기 ── */}
            <div style={{display:'grid',gridTemplateColumns:'290px 1fr',gap:16}}>
                {/* 왼쪽 패널 */}
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:14}}>
                    <div>
                        <h2 style={{fontSize:20,fontWeight:800,color:'#e2e8f0',marginBottom:4}}>중력 물리 계산기</h2>
                        <p style={{color:'#475569',fontSize:12,fontStyle:'italic'}}>뉴턴의 만유인력 법칙: F = G·M·m / r²</p>
                    </div>
                    <div style={{display:'flex',gap:6,flexWrap:'wrap'}}>
                        {PRESETS.map(p=>(
                            <button key={p.name} className="preset-btn" onClick={()=>applyPreset(p)}>{p.name}</button>
                        ))}
                    </div>
                    <div>
                        <label>중력 상수 (G) [N·m²/kg²]</label>
                        <input type="number" value={G} step="1e-12"
                            onChange={e=>{ const v=parseFloat(e.target.value); if(!isNaN(v)&&v>0) setG(v); }}/>
                    </div>
                    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
                        <div>
                            <label>천체 질량 (M) [kg]</label>
                            <input type="number" value={M} step="1e22"
                                onChange={e=>{ const v=parseFloat(e.target.value); if(!isNaN(v)&&v>0) setM(v); }}/>
                        </div>
                        <div>
                            <label>천체 반지름 (R) [m]</label>
                            <input type="number" value={R} step="1000"
                                onChange={e=>{ const v=parseFloat(e.target.value); if(!isNaN(v)&&v>0) setR(v); }}/>
                        </div>
                    </div>
                    <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:8}}>
                        <div>
                            <label>물체 질량 (m) [kg]</label>
                            <input type="number" value={m} step="0.1"
                                onChange={e=>{ const v=parseFloat(e.target.value); if(!isNaN(v)&&v>0) setm(v); }}/>
                        </div>
                        <div>
                            <label>고도 (h) [km]</label>
                            <input type="number" value={h_km} step="100"
                                onChange={e=>{ const v=parseFloat(e.target.value); if(!isNaN(v)&&v>=0) setH(v); }}/>
                        </div>
                    </div>
                    <div>
                        <input type="range" min="0" max="50000" step="100" value={Math.min(h_km,50000)}
                            onChange={e=>setH(parseInt(e.target.value))}/>
                        <p style={{textAlign:'center',fontSize:12,color:'#64748b',marginTop:5}}>{h_km.toLocaleString()} km</p>
                    </div>
                    <div style={{background:'#070b14',borderRadius:10,padding:'4px 14px',border:'1px solid #1e293b'}}>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>현재 거리 (r = R + h)</span>
                            <span className="result-val">{fmt(r/1000,1)} km</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>중력 가속도 (g)</span>
                            <span className="result-val">{g.toFixed(3)} m/s²</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b'}}>중력의 크기 (F)</span>
                            <span className="result-val">{fmt(F,3)} N</span>
                        </div>
                    </div>
                    <div style={{fontSize:11,color:'#475569',lineHeight:1.8,borderTop:'1px solid #1e293b',paddingTop:10}}>
                        <p>* 지구의 질량은 약 5.97e24 kg, 반지름은 6,371,000 m입니다.</p>
                        <p>* 고도가 높아질수록 중력 가속도 g는 r의 제곱에 반비례하여 감소합니다.</p>
                    </div>
                </div>

                {/* 오른쪽 */}
                <div style={{display:'flex',flexDirection:'column',gap:14}}>
                    <div style={{flex:'1 1 0',minHeight:300,background:'#070b14',borderRadius:14,border:'1px solid #1e293b',overflow:'hidden'}}>
                        <PlanetCanvas G={G} M={M} R={R} m={m} h_km={h_km}/>
                    </div>
                    <div style={{flex:'0 0 210px',background:'#0f172a',borderRadius:14,border:'1px solid #1e293b',overflow:'hidden',padding:'14px 6px 2px'}}>
                        <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700,margin:'0 0 6px 40px',borderLeft:'3px solid #3b82f6',paddingLeft:10}}>
                            고도에 따른 중력 가속도(g) 그래프
                        </p>
                        <div style={{height:162}}>
                            <GraphCanvas G={G} M={M} R={R} h_km={h_km}/>
                        </div>
                    </div>
                </div>
            </div>

            {/* ── ③ 수식 유도 ── */}
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
    components.html(react_code, height=1900, scrolling=True)

if __name__ == "__main__":
    run_sim()
