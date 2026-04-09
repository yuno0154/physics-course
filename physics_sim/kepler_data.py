import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙", layout="wide")

    react_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/prop-types@15.8.1/prop-types.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://unpkg.com/recharts@2.12.7/umd/Recharts.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0d1117;color:#e2e8f0;padding:20px 24px;}
canvas{display:block;cursor:crosshair;}
input[type=range]{-webkit-appearance:none;width:100%;height:7px;border-radius:4px;background:#1e293b;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;border-radius:50%;background:#6366f1;cursor:pointer;box-shadow:0 0 12px rgba(99,102,241,0.7);}
.card{background:#0f172a;border-radius:16px;border:1px solid #1e293b;padding:24px;}
.planet-btn{padding:8px 18px;background:#1e293b;border:1px solid #334155;border-radius:9px;color:#94a3b8;cursor:pointer;font-size:13px;font-family:inherit;transition:all 0.2s;}
.planet-btn:hover{border-color:#6366f1;color:#e2e8f0;}
.planet-row:hover{background:#0d1525;cursor:pointer;}
.selected-row{background:#131e35 !important;border-left:3px solid #6366f1;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const STARS = Array.from({length:180},()=>({
    x:Math.random(), y:Math.random(),
    r:Math.random()*1.4+0.3,
    b:Math.random()*0.55+0.2
}));

const getPeriod = r => Math.pow(r, 1.5);

/* ─── Canvas 시뮬레이션 ─── */
const SimCanvas = ({ orbitalRadius, scaleRef }) => {
    const canvasRef = useRef(null);
    const animRef   = useRef(null);
    const angleRef  = useRef(0);
    const rRef      = useRef(orbitalRadius);
    rRef.current    = orbitalRadius;

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const resize = () => { canvas.width = canvas.offsetWidth; canvas.height = canvas.offsetHeight; };
        resize();
        const ro = new ResizeObserver(resize);
        ro.observe(canvas);
        return () => ro.disconnect();
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const onWheel = e => {
            e.preventDefault();
            // deltaY < 0 = 위로 스크롤(확대), > 0 = 아래 스크롤(축소)
            const dir = e.deltaY < 0 ? 1 : -1;   // 위: +1, 아래: -1
            const f   = dir > 0 ? 1.15 : 0.87;   // 확대 or 축소
            scaleRef.current = Math.max(0.25, Math.min(5, scaleRef.current * f));
        };
        canvas.addEventListener('wheel', onWheel, {passive:false});
        return () => canvas.removeEventListener('wheel', onWheel);
    }, []);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        let last = 0;
        const draw = ts => {
            const dt = Math.min((ts - last) / 1000, 0.05);
            last = ts;
            const r = rRef.current;
            const T = getPeriod(r);
            angleRef.current += (2 * Math.PI / (T * 25)) * dt * 60;

            const w = canvas.width, h = canvas.height;
            if (!w || !h) { animRef.current = requestAnimationFrame(draw); return; }
            const cx = w/2, cy = h/2;
            const sc = scaleRef.current;
            const pxAU = Math.min(w, h) * 0.20 * sc;
            const orbitR = r * pxAU;

            /* 배경 */
            ctx.fillStyle = '#070b14';
            ctx.fillRect(0, 0, w, h);

            /* 별 */
            STARS.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x*w, s.y*h, s.r, 0, Math.PI*2);
                ctx.fillStyle = `rgba(200,220,255,${s.b})`;
                ctx.fill();
            });

            /* 궤도 */
            ctx.beginPath();
            ctx.arc(cx, cy, orbitR, 0, Math.PI*2);
            ctx.strokeStyle = 'rgba(99,102,241,0.35)';
            ctx.lineWidth = 1.6; ctx.setLineDash([6,4]); ctx.stroke(); ctx.setLineDash([]);

            /* 태양 글로우 */
            const gs = Math.min(65 * sc, 100);
            const sg = ctx.createRadialGradient(cx,cy,0,cx,cy,gs);
            sg.addColorStop(0,'rgba(251,191,36,0.5)');
            sg.addColorStop(0.5,'rgba(251,191,36,0.12)');
            sg.addColorStop(1,'rgba(251,191,36,0)');
            ctx.beginPath(); ctx.arc(cx,cy,gs,0,Math.PI*2);
            ctx.fillStyle = sg; ctx.fill();

            /* 태양 */
            const sun = ctx.createRadialGradient(cx-6,cy-6,0,cx,cy,20);
            sun.addColorStop(0,'#fffde7'); sun.addColorStop(0.4,'#fbbf24'); sun.addColorStop(1,'#d97706');
            ctx.beginPath(); ctx.arc(cx,cy,20,0,Math.PI*2); ctx.fillStyle=sun; ctx.fill();

            /* 행성 위치 */
            const px = cx + orbitR * Math.cos(angleRef.current);
            const py = cy + orbitR * Math.sin(angleRef.current);

            /* 반지름 선  */
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(px,py);
            ctx.strokeStyle='rgba(99,102,241,0.2)'; ctx.lineWidth=1; ctx.stroke();

            /* 행성 글로우 */
            const pg = ctx.createRadialGradient(px,py,0,px,py,24);
            pg.addColorStop(0,'rgba(59,130,246,0.4)'); pg.addColorStop(1,'rgba(59,130,246,0)');
            ctx.beginPath(); ctx.arc(px,py,24,0,Math.PI*2); ctx.fillStyle=pg; ctx.fill();

            /* 행성 */
            const pl = ctx.createRadialGradient(px-3,py-3,0,px,py,11);
            pl.addColorStop(0,'#bfdbfe'); pl.addColorStop(1,'#2563eb');
            ctx.beginPath(); ctx.arc(px,py,11,0,Math.PI*2); ctx.fillStyle=pl; ctx.fill();

            /* HUD */
            ctx.fillStyle='rgba(148,163,184,0.85)';
            ctx.font='14px "Space Mono",monospace';
            ctx.fillText(`a = ${r.toFixed(2)} AU`, 18, 30);
            ctx.fillText(`T = ${T.toFixed(3)} yr`, 18, 52);
            ctx.fillStyle='rgba(99,102,241,0.6)';
            ctx.font='12px sans-serif';
            ctx.fillText('🖱 휠: 확대/축소', w-120, h-14);

            animRef.current = requestAnimationFrame(draw);
        };
        animRef.current = requestAnimationFrame(draw);
        return () => cancelAnimationFrame(animRef.current);
    }, []);

    return <canvas ref={canvasRef} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ─── 태양계 분석 (ScatterChart + 표) ─── */
const actualData = [
    { name:'수성', r:0.39, t:0.24, r3:0.059, t2:0.058, color:'#94a3b8' },
    { name:'금성', r:0.72, t:0.62, r3:0.373, t2:0.384, color:'#fcd34d' },
    { name:'지구', r:1.00, t:1.00, r3:1.000, t2:1.000, color:'#3b82f6' },
    { name:'화성', r:1.52, t:1.88, r3:3.512, t2:3.534, color:'#ef4444' },
    { name:'목성', r:5.20, t:11.86, r3:140.6, t2:140.7, color:'#f59e0b' },
    { name:'토성', r:9.54, t:29.46, r3:868.3, t2:867.9, color:'#a855f7' },
];

const ScatterAnalysis = () => {
    const [ready, setReady]           = useState(!!window.Recharts);
    const [loadErr, setLoadErr]       = useState(false);
    const [dMin, setDMin]             = useState(0);
    const [dMax, setDMax]             = useState(1000);
    const [selectedPlanet, setSP]     = useState('지구');
    const [showVirtual, setShowV]     = useState(false);
    const [virtualR, setVR]           = useState(3.0);
    const [virtualT, setVT]           = useState(Math.pow(3.0,1.5));
    const chartRef                    = useRef(null);

    useEffect(()=>{
        if(window.Recharts){ setReady(true); return; }
        let elapsed=0;
        const t=setInterval(()=>{
            elapsed+=200;
            if(window.Recharts){ setReady(true); clearInterval(t); }
            else if(elapsed>8000){ setLoadErr(true); clearInterval(t); }
        },200);
        return ()=>clearInterval(t);
    },[]);


    /* 원점(0) 기준 줌 — dMin 항상 0, dMax만 배율 조정 */
    const zoomIn  = () => { setDMin(0); setDMax(v => Math.max(0.5, v * 0.6)); };
    const zoomOut = () => { setDMin(0); setDMax(v => Math.min(50000, v * 1.6)); };

    if(loadErr) return <div style={{padding:40,textAlign:'center',color:'#ef4444',fontSize:14}}>⚠️ 그래프 라이브러리 로드 실패. 인터넷 연결을 확인 후 페이지를 새로고침하세요.</div>;
    if(!ready)  return <div style={{padding:40,textAlign:'center',color:'#475569',fontSize:14}}>⏳ 분석 엔진 로딩 중...</div>;

    const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, Label } = window.Recharts;

    const virtualPlanet = { name:'가상 행성 (X)', r:virtualR, t:virtualT, r3:Math.pow(virtualR,3), t2:Math.pow(virtualT,2), color:'#22d3ee', isVirtual:true };
    const plotData = showVirtual ? [...actualData, virtualPlanet] : actualData;
    const current  = selectedPlanet==='가상 행성 (X)' ? virtualPlanet : (actualData.find(p=>p.name===selectedPlanet)||actualData[2]);

    return (
        <div>
            {/* 그래프 */}
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:16,flexWrap:'wrap',gap:8}}>
                <div>
                    <h3 style={{color:'#e2e8f0',fontSize:16,fontWeight:700,marginBottom:4}}>태양계 행성 산점도 — r³ vs T²</h3>
                    <p style={{color:'#475569',fontSize:12}}>🔍 아래 버튼으로 확대/축소 | 행성 클릭 시 선택</p>
                </div>
                <div style={{display:'flex',gap:8,alignItems:'center',flexWrap:'wrap'}}>
                    <span style={{fontSize:12,color:'#475569'}}>범위: 0 ~ {Math.round(dMax).toLocaleString()}</span>
                    <button className="planet-btn" style={{fontWeight:800,fontSize:15,padding:'6px 14px'}} onClick={zoomIn}>＋ 확대</button>
                    <button className="planet-btn" style={{fontWeight:800,fontSize:15,padding:'6px 14px'}} onClick={zoomOut}>－ 축소</button>
                    <button className="planet-btn" onClick={()=>{setDMin(0);setDMax(1000);}}>태양계 전체</button>
                    <button className="planet-btn" onClick={()=>{setDMin(0);setDMax(10);}}>내행성 확대</button>
                </div>
            </div>

            <div ref={chartRef} style={{height:480,background:'#070b14',borderRadius:14,padding:'20px 8px',marginBottom:24}}>
                <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{top:20,right:40,bottom:60,left:60}}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false}/>
                        <XAxis type="number" dataKey="r3" domain={[dMin,dMax]} stroke="#334155" tick={{fontSize:11,fill:'#475569'}} allowDataOverflow>
                            <Label value="r³ (AU³)" position="bottom" offset={35} style={{fontSize:12,fill:'#64748b'}}/>
                        </XAxis>
                        <YAxis type="number" dataKey="t2" domain={[dMin,dMax]} stroke="#334155" tick={{fontSize:11,fill:'#475569'}} allowDataOverflow>
                            <Label value="T² (yr²)" angle={-90} position="left" offset={35} style={{fontSize:12,fill:'#64748b'}}/>
                        </YAxis>
                        <Tooltip content={({active,payload})=>{
                            if(active&&payload&&payload.length){
                                const d=payload[0].payload;
                                return <div style={{background:'#0f172a',border:'1px solid #334155',borderRadius:12,padding:'12px 16px',fontSize:13}}>
                                    <p style={{fontWeight:700,color:'#6366f1',marginBottom:6}}>{d.name}</p>
                                    <p style={{color:'#94a3b8'}}>r³: {d.r3.toLocaleString()}</p>
                                    <p style={{color:'#94a3b8'}}>T²: {d.t2.toLocaleString()}</p>
                                </div>;
                            }
                            return null;
                        }}/>
                        <Scatter data={plotData} onClick={d=>setSP(d.name)}>
                            {plotData.map((e,i)=>(
                                <Cell key={i}
                                    fill={e.name===selectedPlanet ? (e.isVirtual?'#22d3ee':'#6366f1') : (e.isVirtual?'#a5f3fc':'#cbd5e1')}
                                    stroke={e.isVirtual?'#22d3ee':(e.name===selectedPlanet?'#818cf8':'#cbd5e1')}
                                    strokeWidth={e.name===selectedPlanet?5:1}
                                    r={e.name===selectedPlanet?15:9}
                                    style={{cursor:'pointer'}}
                                />
                            ))}
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
            </div>

            {/* 행성 레전드 */}
            <div style={{display:'flex',flexWrap:'wrap',gap:14,marginBottom:28}}>
                {actualData.map((p,i)=>(
                    <div key={i} onClick={()=>setSP(p.name)}
                        style={{display:'flex',alignItems:'center',gap:7,fontSize:13,cursor:'pointer',
                            opacity:p.name===selectedPlanet?1:0.55,transition:'opacity 0.2s'}}>
                        <div style={{width:10,height:10,borderRadius:'50%',background:p.color}}></div>
                        <span style={{color:'#e2e8f0',fontWeight:p.name===selectedPlanet?700:400}}>{p.name}</span>
                    </div>
                ))}
            </div>

            {/* 표 + 가상 행성 */}
            <div style={{display:'grid',gridTemplateColumns:'1fr 280px',gap:18}}>
                {/* 데이터 표 */}
                <div className="card">
                    <h4 style={{fontSize:15,fontWeight:700,color:'#e2e8f0',marginBottom:16,display:'flex',alignItems:'center',gap:8}}>
                        <span style={{background:'#1e293b',borderRadius:8,padding:'4px 8px',fontSize:13}}>📋</span> 관측 정보 리스트
                    </h4>
                    <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
                        <thead>
                            <tr style={{borderBottom:'1px solid #1e293b'}}>
                                <th style={{padding:'8px 12px',color:'#475569',textAlign:'left',fontWeight:700,fontSize:11,textTransform:'uppercase',letterSpacing:'0.05em'}}>행성</th>
                                <th style={{padding:'8px 8px',color:'#475569',textAlign:'center',fontWeight:700,fontSize:11}}>장반경 (AU)</th>
                                <th style={{padding:'8px 8px',color:'#475569',textAlign:'center',fontWeight:700,fontSize:11}}>주기 (yr)</th>
                                <th style={{padding:'8px 8px',color:'#6366f1',textAlign:'center',fontWeight:700,fontSize:11}}>r³</th>
                                <th style={{padding:'8px 8px',color:'#f59e0b',textAlign:'center',fontWeight:700,fontSize:11}}>T²</th>
                            </tr>
                        </thead>
                        <tbody>
                            {actualData.map(p=>(
                                <tr key={p.name} className={`planet-row ${p.name===selectedPlanet?'selected-row':''}`}
                                    onClick={()=>setSP(p.name)}
                                    style={{borderBottom:'1px solid #0d1117',transition:'all 0.2s'}}>
                                    <td style={{padding:'11px 12px',fontWeight:700,display:'flex',alignItems:'center',gap:8,color:'#cbd5e1'}}>
                                        <div style={{width:10,height:10,borderRadius:'50%',background:p.color,flexShrink:0}}></div>{p.name}
                                    </td>
                                    <td style={{padding:'11px 8px',textAlign:'center',fontFamily:'monospace',color:'#64748b'}}>{p.r.toFixed(2)}</td>
                                    <td style={{padding:'11px 8px',textAlign:'center',fontFamily:'monospace',color:'#64748b'}}>{p.t.toFixed(2)}</td>
                                    <td style={{padding:'11px 8px',textAlign:'center',fontFamily:'monospace',fontWeight:700,
                                        color:p.name===selectedPlanet?'#818cf8':'#e2e8f0'}}>{p.r3.toLocaleString()}</td>
                                    <td style={{padding:'11px 8px',textAlign:'center',fontFamily:'monospace',fontWeight:700,
                                        color:p.name===selectedPlanet?'#fbbf24':'#e2e8f0'}}>{p.t2.toLocaleString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* 가상 행성 예측기 */}
                <div style={{background:'#080e1a',borderRadius:16,padding:24,border:'2px solid #1e293b',display:'flex',flexDirection:'column',justifyContent:'space-between'}}>
                    <div>
                        <p style={{color:'#6366f1',fontWeight:700,fontSize:11,textTransform:'uppercase',letterSpacing:'0.15em',marginBottom:16}}>Virtual Planet Prediction</p>
                        <div style={{background:'rgba(255,255,255,0.04)',borderRadius:12,padding:16,marginBottom:12,border:'1px solid rgba(255,255,255,0.06)'}}>
                            <label style={{fontSize:10,fontWeight:700,color:'#475569',textTransform:'uppercase',display:'block',marginBottom:8}}>입력: 궤도 반지름 r (AU)</label>
                            <input type="number" value={virtualR.toFixed(2)}
                                onChange={e=>{ const r=parseFloat(e.target.value); if(!isNaN(r)){setVR(r);setVT(Math.pow(r,1.5));setShowV(true); }}}
                                style={{width:'100%',background:'transparent',color:'white',fontSize:32,fontWeight:800,border:'none',outline:'none',fontFamily:'monospace'}} step="0.1"/>
                        </div>
                        <div style={{background:'rgba(255,255,255,0.04)',borderRadius:12,padding:16,border:'1px solid rgba(255,255,255,0.06)'}}>
                            <label style={{fontSize:10,fontWeight:700,color:'#475569',textTransform:'uppercase',display:'block',marginBottom:8}}>결과: 공전 주기 T (yr)</label>
                            <input type="number" value={virtualT.toFixed(2)}
                                onChange={e=>{ const t=parseFloat(e.target.value); if(!isNaN(t)){setVT(t);setVR(Math.pow(t*t,1/3));setShowV(true); }}}
                                style={{width:'100%',background:'transparent',color:'white',fontSize:32,fontWeight:800,border:'none',outline:'none',fontFamily:'monospace'}} step="0.1"/>
                        </div>
                    </div>
                    <div>
                        <button onClick={()=>{setShowV(true);setSP('가상 행성 (X)');}}
                            style={{width:'100%',padding:'13px',background:'#6366f1',color:'white',border:'none',borderRadius:10,fontWeight:700,fontSize:14,cursor:'pointer',fontFamily:'inherit',marginTop:16,marginBottom:12}}>
                            그래프에 행성 런칭
                        </button>
                        <div style={{borderTop:'1px solid rgba(255,255,255,0.05)',paddingTop:14,display:'flex',justifyContent:'space-between',alignItems:'center'}}>
                            <div>
                                <p style={{fontSize:10,color:'#475569',marginBottom:4,fontWeight:700,textTransform:'uppercase'}}>Current K</p>
                                <p style={{fontSize:26,fontWeight:800,color:'#34d399',fontFamily:'monospace'}}>
                                    {(Math.pow(current.t2,1)/current.r3).toFixed(4)}
                                </p>
                            </div>
                            <div style={{width:36,height:36,borderRadius:'50%',background:'rgba(52,211,153,0.1)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:18}}>✓</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

/* ─── QnA 토글 컴포넌트 ─── */
const QnA = ({ items }) => {
    const [openIdx, setOpenIdx] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {items.map((item, i) => (
                <div key={i} style={{borderRadius:12,border:'1px solid #1e293b',overflow:'hidden',background:'#070b14'}}>
                    {/* 질문 헤더 */}
                    <button
                        onClick={()=>setOpenIdx(openIdx===i?null:i)}
                        style={{width:'100%',display:'flex',alignItems:'center',gap:12,padding:'13px 16px',background:'transparent',border:'none',cursor:'pointer',textAlign:'left',fontFamily:'inherit'}}
                    >
                        <span style={{color:'#6366f1',fontWeight:800,minWidth:28,fontSize:15,flexShrink:0}}>Q{i+1}.</span>
                        <span style={{color:'#94a3b8',fontSize:14,lineHeight:1.6,flex:1}}>{item.q}</span>
                        <span style={{color:'#334155',fontSize:18,transition:'transform 0.25s',transform:openIdx===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
                    </button>
                    {/* 답 (펼침) */}
                    <div style={{
                        maxHeight: openIdx===i ? '200px' : '0px',
                        overflow:'hidden',
                        transition:'max-height 0.35s ease'
                    }}>
                        <div style={{padding:'0 16px 14px 56px',display:'flex',gap:10,alignItems:'flex-start'}}>
                            <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                            <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.7}}>{item.a}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

/* ─── 메인 앱 ─── */
const App = () => {
    const [radius, setRadius]   = useState(1.0);
    const [dataLog, setDataLog] = useState([{no:1,r:1.00,t:1.00,k:1.000}]);
    const scaleRef              = useRef(1.0);

    const period = getPeriod(radius);

    const handleRadius = e => { const v=parseFloat(e.target.value); setRadius(v); };

    const record = () => {
        const r=radius, t=getPeriod(r), k=+(Math.pow(t,2)/Math.pow(r,3)).toFixed(4);
        setDataLog(prev=>[...prev,{no:prev.length+1,r:+r.toFixed(2),t:+t.toFixed(3),k}]);
    };

    const reset = () => { setDataLog([{no:1,r:1.00,t:1.00,k:1.000}]); setRadius(1.0); scaleRef.current=1.0; };

    return (
        <div style={{maxWidth:1160,margin:'0 auto'}}>

            {/* ── 헤더 ── */}
            <div style={{marginBottom:22,borderBottom:'1px solid #1e293b',paddingBottom:16}}>
                <h1 style={{fontSize:24,fontWeight:800,color:'#e2e8f0',marginBottom:6}}>
                    조화의 법칙(Harmonic Law) 탐구 시뮬레이터
                </h1>
                <p style={{color:'#475569',fontSize:14}}>
                    궤도 반지름을 조절하며 행성의 주기(T)와 반지름(a) 사이의 관계를 데이터로 찾아보세요.
                </p>
            </div>

            {/* ── 시뮬레이션 캔버스 (전체 너비, 높이 큼) ── */}
            <div style={{background:'#070b14',borderRadius:18,overflow:'hidden',border:'1px solid #1e293b',position:'relative',height:520,marginBottom:16}}>
                <div style={{position:'absolute',top:16,left:16,zIndex:10,background:'rgba(7,11,20,0.75)',padding:'10px 14px',borderRadius:10,backdropFilter:'blur(6px)'}}>
                    <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:7,fontSize:14}}>
                        <div style={{width:14,height:14,borderRadius:'50%',background:'#fbbf24'}}></div>
                        <span style={{color:'#94a3b8'}}>태양 (M)</span>
                    </div>
                    <div style={{display:'flex',alignItems:'center',gap:8,fontSize:14}}>
                        <div style={{width:14,height:14,borderRadius:'50%',background:'#3b82f6'}}></div>
                        <span style={{color:'#94a3b8'}}>행성 (m)</span>
                    </div>
                </div>
                <SimCanvas orbitalRadius={radius} scaleRef={scaleRef}/>
            </div>

            {/* ── 컨트롤 바 ── */}
            <div className="card" style={{marginBottom:20}}>
                <div style={{display:'flex',alignItems:'center',gap:20,flexWrap:'wrap'}}>
                    <div style={{flex:1,minWidth:220}}>
                        <p style={{fontSize:14,color:'#64748b',marginBottom:10}}>
                            궤도 반지름 (a): <strong style={{color:'#e2e8f0'}}>{radius.toFixed(2)} AU</strong>
                            <span style={{marginLeft:14,color:'#6366f1'}}>→ T = {period.toFixed(3)} yr</span>
                        </p>
                        <input type="range" min="0.5" max="6.0" step="0.05"
                            value={radius} onChange={handleRadius}/>
                    </div>
                    <button onClick={record}
                        style={{padding:'12px 24px',background:'#6366f1',color:'white',border:'none',borderRadius:10,fontWeight:700,cursor:'pointer',fontSize:14,fontFamily:'inherit',boxShadow:'0 4px 14px rgba(99,102,241,0.4)',whiteSpace:'nowrap'}}>
                        현재 데이터 기록하기
                    </button>
                    <button onClick={reset}
                        style={{padding:'12px 18px',background:'#1e293b',color:'#94a3b8',border:'1px solid #334155',borderRadius:10,fontWeight:700,cursor:'pointer',fontSize:14,fontFamily:'inherit'}}>
                        초기화
                    </button>
                </div>
            </div>

            {/* ── 데이터 로그 + 학습 질문 ── */}
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:18,marginBottom:32}}>

                {/* 탐구 데이터 로그 */}
                <div className="card">
                    <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:18}}>
                        <span style={{fontSize:20}}>📊</span>
                        <h3 style={{fontSize:16,fontWeight:700,color:'#e2e8f0'}}>탐구 데이터 로그</h3>
                    </div>
                    <table style={{width:'100%',borderCollapse:'collapse',fontSize:14}}>
                        <thead>
                            <tr style={{borderBottom:'1px solid #1e293b'}}>
                                <th style={{padding:'8px 6px',color:'#475569',textAlign:'center',fontWeight:700,fontSize:12}}>NO.</th>
                                <th style={{padding:'8px 6px',color:'#475569',textAlign:'center',fontWeight:700,fontSize:12}}>반지름 A (AU)</th>
                                <th style={{padding:'8px 6px',color:'#475569',textAlign:'center',fontWeight:700,fontSize:12}}>주기 T (yr)</th>
                                <th style={{padding:'8px 6px',color:'#6366f1',textAlign:'center',fontWeight:700,fontSize:12}}>K = T²/A³</th>
                            </tr>
                        </thead>
                        <tbody>
                            {dataLog.map((row,i)=>(
                                <tr key={i} style={{borderBottom:'1px solid #0a0f1a'}}>
                                    <td style={{padding:'11px 6px',textAlign:'center',color:'#475569'}}>{row.no}</td>
                                    <td style={{padding:'11px 6px',textAlign:'center',color:'#e2e8f0',fontFamily:'monospace',fontWeight:700}}>{row.r.toFixed(2)}</td>
                                    <td style={{padding:'11px 6px',textAlign:'center',color:'#e2e8f0',fontFamily:'monospace',fontWeight:700}}>{row.t.toFixed(3)}</td>
                                    <td style={{padding:'11px 6px',textAlign:'center',color:'#6366f1',fontFamily:'monospace',fontWeight:700}}>{row.k.toFixed(3)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* 학습 질문 */}
                <div className="card" style={{display:'flex',flexDirection:'column'}}>
                    <h3 style={{fontSize:16,fontWeight:700,color:'#fbbf24',marginBottom:20}}>💡 학습 질문 (인출 전략)</h3>
                    <QnA items={[
                        {
                            q:'반지름이 2배가 될 때, 주기는 몇 배가 되나요? (비례 관계 인출)',
                            a:'T = a^(3/2) 이므로, a가 2배 → T = 2^(3/2) = 2√2 ≈ 2.83배가 됩니다.'
                        },
                        {
                            q:'T²/a³ 값(K)이 모든 행성에서 일정한 이유는 무엇일까요?',
                            a:'K = 4π²/(GM) 이며, G와 태양의 질량 M은 모든 행성에 공통이므로 K는 항상 같은 값입니다.'
                        },
                        {
                            q:'만약 태양의 질량이 2배가 된다면 K값은 어떻게 변할까요?',
                            a:'K = 4π²/(GM) 에서 M이 2배 → K는 1/2배(절반)로 작아집니다.'
                        },
                        {
                            q:'반지름과 주기의 관계를 log-log 그래프로 그리면 어떤 형태일까요?',
                            a:'log T = (3/2)log a + C 이므로, 기울기 3/2인 직선이 됩니다.'
                        }
                    ]}/>
                </div>
            </div>

            {/* ── 구분선 ── */}
            <div style={{borderTop:'2px solid #1e293b',paddingTop:28,marginBottom:24}}>
                <div style={{display:'flex',alignItems:'center',gap:12,marginBottom:6}}>
                    <div style={{width:4,height:24,background:'#6366f1',borderRadius:2}}></div>
                    <h2 style={{fontSize:20,fontWeight:800,color:'#e2e8f0'}}>태양계 실제 데이터 분석</h2>
                </div>
                <p style={{color:'#475569',fontSize:14,marginLeft:16}}>
                    태양계 행성의 실측 데이터로 케플러 제3법칙을 검증합니다. 오른쪽 상단 버튼이나 마우스 휠로 그래프를 확대해 내행성을 정밀 관찰하세요.
                </p>
            </div>

            {/* ── 분석 섹션 ── */}
            <div className="card" style={{marginBottom:40}}>
                <ScatterAnalysis/>
            </div>

        </div>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""
    components.html(react_code, height=2600, scrolling=True)

if __name__ == "__main__":
    run_sim()
