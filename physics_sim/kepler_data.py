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
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script src="https://unpkg.com/recharts@2.12.7/umd/Recharts.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0d1117;color:#e2e8f0;padding:20px 24px;}
canvas{display:block;cursor:crosshair;}
input[type=range]{-webkit-appearance:none;width:100%;height:6px;border-radius:3px;background:#1e293b;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:20px;height:20px;border-radius:50%;background:#6366f1;cursor:pointer;box-shadow:0 0 10px rgba(99,102,241,0.6);}
.acc-btn{width:100%;padding:18px 24px;background:#161d2b;border:1px solid #1e293b;border-radius:14px;color:#e2e8f0;font-size:15px;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;font-family:inherit;transition:border-color 0.2s;}
.acc-btn:hover{border-color:#6366f1;}
.planet-btn{padding:7px 16px;background:#1e293b;border:1px solid #334155;border-radius:8px;color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;}
.planet-btn:hover{border-color:#6366f1;color:#e2e8f0;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef } = React;

const STARS = Array.from({length:150},()=>({
    x:Math.random(), y:Math.random(),
    r:Math.random()*1.4+0.3,
    b:Math.random()*0.55+0.2
}));

const getPeriod = r => Math.pow(r, 1.5);

/* ── 시뮬레이션 캔버스 ── */
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
            const f = e.deltaY > 0 ? 0.87 : 1.15;
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
            angleRef.current += (2 * Math.PI / (T * 9)) * dt * 60;
            const w = canvas.width, h = canvas.height;
            if (!w || !h) { animRef.current = requestAnimationFrame(draw); return; }
            const cx = w/2, cy = h/2;
            const sc = scaleRef.current;
            const pxAU = Math.min(w,h) * 0.16 * sc;
            const orbitR = r * pxAU;

            ctx.fillStyle = '#070b14';
            ctx.fillRect(0,0,w,h);

            STARS.forEach(s => {
                ctx.beginPath();
                ctx.arc(s.x*w, s.y*h, s.r, 0, Math.PI*2);
                ctx.fillStyle = `rgba(200,220,255,${s.b})`;
                ctx.fill();
            });

            /* 궤도 */
            ctx.beginPath();
            ctx.arc(cx,cy,orbitR,0,Math.PI*2);
            ctx.strokeStyle='rgba(99,102,241,0.35)';
            ctx.lineWidth=1.5; ctx.setLineDash([6,4]); ctx.stroke(); ctx.setLineDash([]);

            /* 태양 글로우 */
            const glowSz = 52*sc;
            const sg = ctx.createRadialGradient(cx,cy,0,cx,cy,glowSz);
            sg.addColorStop(0,'rgba(251,191,36,0.45)');
            sg.addColorStop(0.5,'rgba(251,191,36,0.12)');
            sg.addColorStop(1,'rgba(251,191,36,0)');
            ctx.beginPath(); ctx.arc(cx,cy,glowSz,0,Math.PI*2);
            ctx.fillStyle=sg; ctx.fill();

            /* 태양 */
            const sun = ctx.createRadialGradient(cx-5,cy-5,0,cx,cy,18);
            sun.addColorStop(0,'#fffde7'); sun.addColorStop(0.4,'#fbbf24'); sun.addColorStop(1,'#d97706');
            ctx.beginPath(); ctx.arc(cx,cy,18,0,Math.PI*2); ctx.fillStyle=sun; ctx.fill();

            /* 반지름 선 */
            const px = cx + orbitR*Math.cos(angleRef.current);
            const py = cy + orbitR*Math.sin(angleRef.current);
            ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(px,py);
            ctx.strokeStyle='rgba(99,102,241,0.18)'; ctx.lineWidth=1; ctx.stroke();

            /* 행성 글로우 */
            const pg = ctx.createRadialGradient(px,py,0,px,py,22);
            pg.addColorStop(0,'rgba(59,130,246,0.35)'); pg.addColorStop(1,'rgba(59,130,246,0)');
            ctx.beginPath(); ctx.arc(px,py,22,0,Math.PI*2); ctx.fillStyle=pg; ctx.fill();

            /* 행성 */
            const pl = ctx.createRadialGradient(px-3,py-3,0,px,py,10);
            pl.addColorStop(0,'#bfdbfe'); pl.addColorStop(1,'#2563eb');
            ctx.beginPath(); ctx.arc(px,py,10,0,Math.PI*2); ctx.fillStyle=pl; ctx.fill();

            /* HUD */
            ctx.fillStyle='rgba(148,163,184,0.85)';
            ctx.font='13px "Space Mono",monospace';
            ctx.fillText(`a = ${r.toFixed(2)} AU`, 16, 26);
            ctx.fillText(`T = ${T.toFixed(3)} yr`,  16, 46);
            ctx.fillStyle='rgba(99,102,241,0.6)';
            ctx.font='11px sans-serif';
            ctx.fillText('🖱 휠: 확대/축소', w-115, h-12);

            animRef.current = requestAnimationFrame(draw);
        };
        animRef.current = requestAnimationFrame(draw);
        return () => cancelAnimationFrame(animRef.current);
    }, []);

    return <canvas ref={canvasRef} style={{width:'100%',height:420,display:'block'}} />;
};

/* ── ScatterChart 분석 ── */
const ScatterAnalysis = () => {
    const [ready, setReady] = useState(false);
    const [dMin, setDMin] = useState(0);
    const [dMax, setDMax] = useState(1000);
    const chartRef = useRef(null);
    const domRef   = useRef({min:0,max:1000});

    useEffect(()=>{
        const t=setInterval(()=>{ if(window.Recharts){setReady(true);clearInterval(t);} },100);
        return ()=>clearInterval(t);
    },[]);

    useEffect(()=>{ domRef.current={min:dMin,max:dMax}; },[dMin,dMax]);

    useEffect(()=>{
        const el=chartRef.current; if(!el) return;
        const onW=e=>{
            e.preventDefault();
            const {min,max}=domRef.current;
            const f=e.deltaY>0?1.25:0.8;
            const c=(min+max)/2, rng=(max-min)*f;
            setDMin(Math.max(0,c-rng/2));
            setDMax(c+rng/2);
        };
        el.addEventListener('wheel',onW,{passive:false});
        return ()=>el.removeEventListener('wheel',onW);
    },[]);

    const data=[
        {name:'수성',r3:0.059,t2:0.058,c:'#94a3b8'},
        {name:'금성',r3:0.373,t2:0.384,c:'#fcd34d'},
        {name:'지구',r3:1.000,t2:1.000,c:'#3b82f6'},
        {name:'화성',r3:3.512,t2:3.534,c:'#ef4444'},
        {name:'목성',r3:140.6,t2:140.7,c:'#f59e0b'},
        {name:'토성',r3:868.3,t2:867.9,c:'#a855f7'},
    ];

    if(!ready) return <div style={{padding:40,textAlign:'center',color:'#475569'}}>분석 엔진 로딩 중...</div>;

    const {ScatterChart,Scatter,XAxis,YAxis,CartesianGrid,Tooltip,ResponsiveContainer,Cell,Label}=window.Recharts;

    return (
        <div>
            <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:16,flexWrap:'wrap',gap:8}}>
                <h3 style={{color:'#e2e8f0',fontSize:15,fontWeight:700}}>태양계 행성: r³ vs T² 산점도</h3>
                <div style={{display:'flex',gap:8,alignItems:'center'}}>
                    <span style={{fontSize:12,color:'#475569'}}>범위: 0 ~ {Math.round(dMax).toLocaleString()}</span>
                    <button className="planet-btn" onClick={()=>{setDMin(0);setDMax(1000);}}>전체</button>
                    <button className="planet-btn" onClick={()=>{setDMin(0);setDMax(10);}}>내행성</button>
                    <button className="planet-btn" onClick={()=>{setDMin(0);setDMax(200);}}>목성까지</button>
                </div>
            </div>
            <p style={{color:'#475569',fontSize:12,marginBottom:12}}>🖱 마우스 휠로 자유롭게 확대/축소</p>
            <div ref={chartRef} style={{height:460,background:'#070b14',borderRadius:12,padding:'16px 8px'}}>
                <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{top:20,right:40,bottom:60,left:60}}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis type="number" dataKey="r3" domain={[dMin,dMax]} stroke="#334155" tick={{fontSize:11,fill:'#475569'}} allowDataOverflow>
                            <Label value="r³ (AU³)" position="bottom" offset={35} style={{fontSize:12,fill:'#64748b'}}/>
                        </XAxis>
                        <YAxis type="number" dataKey="t2" domain={[dMin,dMax]} stroke="#334155" tick={{fontSize:11,fill:'#475569'}} allowDataOverflow>
                            <Label value="T² (yr²)" angle={-90} position="left" offset={35} style={{fontSize:12,fill:'#64748b'}}/>
                        </YAxis>
                        <Tooltip content={({active,payload})=>{
                            if(active&&payload&&payload.length){
                                const d=payload[0].payload;
                                return <div style={{background:'#0f172a',border:'1px solid #334155',borderRadius:10,padding:'10px 14px',fontSize:13}}>
                                    <p style={{fontWeight:700,color:'#6366f1',marginBottom:4}}>{d.name}</p>
                                    <p style={{color:'#94a3b8'}}>r³: {d.r3.toLocaleString()}</p>
                                    <p style={{color:'#94a3b8'}}>T²: {d.t2.toLocaleString()}</p>
                                </div>;
                            }
                            return null;
                        }}/>
                        <Scatter data={data}>
                            {data.map((e,i)=><Cell key={i} fill={e.c} stroke={e.c} r={11}/>)}
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
            </div>
            <div style={{display:'flex',flexWrap:'wrap',gap:14,marginTop:16}}>
                {data.map((p,i)=>(
                    <div key={i} style={{display:'flex',alignItems:'center',gap:7,fontSize:13}}>
                        <div style={{width:10,height:10,borderRadius:'50%',background:p.c}}></div>
                        <span style={{color:'#64748b'}}>{p.name}</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

/* ── 메인 앱 ── */
const App = () => {
    const [radius, setRadius]       = useState(1.0);
    const [dataLog, setDataLog]     = useState([{no:1,r:1.00,t:1.00,k:1.000}]);
    const [accOpen, setAccOpen]     = useState(false);
    const scaleRef                  = useRef(1.0);
    const rRef                      = useRef(1.0);

    const period = getPeriod(radius);

    const handleRadius = e => {
        const v = parseFloat(e.target.value);
        setRadius(v); rRef.current = v;
    };

    const record = () => {
        const r=radius, t=getPeriod(r), k=Math.pow(t,2)/Math.pow(r,3);
        setDataLog(prev=>[...prev,{no:prev.length+1,r:+r.toFixed(2),t:+t.toFixed(3),k:+k.toFixed(4)}]);
    };

    const reset = () => {
        setDataLog([{no:1,r:1.00,t:1.00,k:1.000}]);
        setRadius(1.0); rRef.current=1.0; scaleRef.current=1.0;
    };

    return (
        <div style={{maxWidth:1160,margin:'0 auto'}}>
            {/* 헤더 */}
            <div style={{marginBottom:20,borderBottom:'1px solid #1e293b',paddingBottom:16}}>
                <h1 style={{fontSize:24,fontWeight:800,color:'#e2e8f0',marginBottom:6}}>
                    조화의 법칙(Harmonic Law) 탐구 시뮬레이터
                </h1>
                <p style={{color:'#475569',fontSize:14}}>
                    궤도 반지름을 조절하며 행성의 주기(T)와 반지름(a) 사이의 관계를 데이터로 찾아보세요.
                </p>
            </div>

            {/* 시뮬레이션 + 사이드패널 */}
            <div style={{display:'grid',gridTemplateColumns:'1fr 310px',gap:18,marginBottom:16}}>
                {/* 캔버스 */}
                <div style={{background:'#070b14',borderRadius:18,overflow:'hidden',border:'1px solid #1e293b',position:'relative'}}>
                    <div style={{position:'absolute',top:14,left:14,zIndex:10,background:'rgba(7,11,20,0.7)',padding:'10px 14px',borderRadius:10}}>
                        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:6,fontSize:13}}>
                            <div style={{width:13,height:13,borderRadius:'50%',background:'#fbbf24'}}></div>
                            <span style={{color:'#94a3b8'}}>태양 (M)</span>
                        </div>
                        <div style={{display:'flex',alignItems:'center',gap:8,fontSize:13}}>
                            <div style={{width:13,height:13,borderRadius:'50%',background:'#3b82f6'}}></div>
                            <span style={{color:'#94a3b8'}}>행성 (m)</span>
                        </div>
                    </div>
                    <SimCanvas orbitalRadius={radius} scaleRef={scaleRef}/>
                </div>

                {/* 우측 패널 */}
                <div style={{display:'flex',flexDirection:'column',gap:14}}>
                    {/* 데이터 로그 */}
                    <div style={{background:'#0f172a',borderRadius:14,padding:18,border:'1px solid #1e293b',flex:'1',overflow:'auto',maxHeight:290}}>
                        <div style={{display:'flex',alignItems:'center',gap:8,marginBottom:14}}>
                            <span style={{fontSize:16}}>📊</span>
                            <span style={{fontSize:14,fontWeight:700,color:'#e2e8f0'}}>탐구 데이터 로그</span>
                        </div>
                        <table style={{width:'100%',borderCollapse:'collapse',fontSize:12}}>
                            <thead>
                                <tr style={{borderBottom:'1px solid #1e293b'}}>
                                    <th style={{padding:'5px 4px',color:'#475569',textAlign:'center',fontWeight:700}}>NO.</th>
                                    <th style={{padding:'5px 4px',color:'#475569',textAlign:'center',fontWeight:700}}>반지름(A)</th>
                                    <th style={{padding:'5px 4px',color:'#475569',textAlign:'center',fontWeight:700}}>주기(T)</th>
                                    <th style={{padding:'5px 4px',color:'#6366f1',textAlign:'center',fontWeight:700}}>K (T²/A³)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {dataLog.map((row,i)=>(
                                    <tr key={i} style={{borderBottom:'1px solid #0d1117'}}>
                                        <td style={{padding:'9px 4px',textAlign:'center',color:'#475569'}}>{row.no}</td>
                                        <td style={{padding:'9px 4px',textAlign:'center',color:'#e2e8f0',fontFamily:'monospace',fontWeight:700}}>{row.r.toFixed(2)}</td>
                                        <td style={{padding:'9px 4px',textAlign:'center',color:'#e2e8f0',fontFamily:'monospace',fontWeight:700}}>{row.t.toFixed(2)}</td>
                                        <td style={{padding:'9px 4px',textAlign:'center',color:'#6366f1',fontFamily:'monospace',fontWeight:700}}>{row.k.toFixed(3)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>

                    {/* 학습 질문 */}
                    <div style={{background:'#0f172a',borderRadius:14,padding:18,border:'1px solid #1e293b'}}>
                        <h3 style={{fontSize:13,fontWeight:700,color:'#fbbf24',marginBottom:12}}>학습 질문 (인출 전략)</h3>
                        {[
                            '반지름이 2배가 될 때, 주기는 몇 배가 되나요? (비례 관계 인출)',
                            'T²/a³ 값이 모든 행성에서 일정한 이유는 무엇일까요?',
                            '만약 태양의 질량이 2배가 된다면 K값은 어떻게 변할까요?'
                        ].map((q,i)=>(
                            <div key={i} style={{display:'flex',gap:8,fontSize:12,marginBottom:10}}>
                                <span style={{color:'#6366f1',fontWeight:700,minWidth:22}}>Q{i+1}.</span>
                                <span style={{color:'#94a3b8',lineHeight:1.65}}>{q}</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* 컨트롤 바 */}
            <div style={{background:'#0f172a',borderRadius:14,padding:18,border:'1px solid #1e293b',marginBottom:20}}>
                <div style={{display:'flex',alignItems:'center',gap:20,flexWrap:'wrap'}}>
                    <div style={{flex:1,minWidth:200}}>
                        <p style={{fontSize:13,color:'#64748b',marginBottom:10}}>
                            궤도 반지름 (a) 조정: <strong style={{color:'#e2e8f0'}}>{radius.toFixed(2)} AU</strong>
                            <span style={{marginLeft:14,color:'#6366f1'}}>→ T = {period.toFixed(3)} yr</span>
                        </p>
                        <input type="range" min="0.5" max="6.0" step="0.05"
                            value={radius} onChange={handleRadius}/>
                    </div>
                    <button onClick={record}
                        style={{padding:'11px 22px',background:'#6366f1',color:'white',border:'none',borderRadius:10,fontWeight:700,cursor:'pointer',fontSize:13,fontFamily:'inherit',whiteSpace:'nowrap',boxShadow:'0 4px 14px rgba(99,102,241,0.4)'}}>
                        현재 데이터 기록하기
                    </button>
                    <button onClick={reset}
                        style={{padding:'11px 18px',background:'#1e293b',color:'#94a3b8',border:'1px solid #334155',borderRadius:10,fontWeight:700,cursor:'pointer',fontSize:13,fontFamily:'inherit'}}>
                        초기화
                    </button>
                </div>
            </div>

            {/* 아코디언: 기존 분석 */}
            <div style={{marginBottom:30}}>
                <button className="acc-btn" onClick={()=>setAccOpen(v=>!v)}>
                    <span>📈 태양계 실제 데이터 검증 — 케플러 제3법칙 산점도 분석</span>
                    <span style={{fontSize:18,transition:'transform 0.3s',transform:accOpen?'rotate(180deg)':'rotate(0deg)'}}>▾</span>
                </button>
                <div style={{maxHeight:accOpen?'900px':'0px',overflow:'hidden',transition:'max-height 0.5s ease'}}>
                    <div style={{background:'#0f172a',border:'1px solid #1e293b',borderTop:'none',borderRadius:'0 0 14px 14px',padding:24}}>
                        <ScatterAnalysis/>
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
