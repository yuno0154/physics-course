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
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0a0f1e;color:#e2e8f0;padding:18px;}
.panel{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;}
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

/* ── 행성 + 물체 Canvas ── */
const PlanetCanvas = ({ G, M, R, m, h_km }) => {
    const ref = useRef(null);
    const v   = useRef({ G, M, R, m, h_km });
    v.current = { G, M, R, m, h_km };

    const draw = () => {
        const canvas = ref.current; if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const { G, M, R, m, h_km } = v.current;
        const w = canvas.width, h = canvas.height;
        const cx = w * 0.42, cy = h / 2;

        ctx.clearRect(0,0,w,h);
        ctx.fillStyle='#070b14'; ctx.fillRect(0,0,w,h);

        /* 별 */
        for (let i=0;i<80;i++){
            const sx=(i*137.508)%w, sy=(i*97.3+i*13)%h;
            ctx.beginPath(); ctx.arc(sx,sy,0.6+(i%3)*0.4,0,Math.PI*2);
            ctx.fillStyle=`rgba(200,220,255,${0.15+(i%5)*0.07})`; ctx.fill();
        }

        const pR = Math.min(w,h)*0.31;

        /* 행성 글로우 */
        const gw = ctx.createRadialGradient(cx,cy,pR*0.3,cx,cy,pR*2);
        gw.addColorStop(0,'rgba(59,130,246,0.3)'); gw.addColorStop(1,'rgba(59,130,246,0)');
        ctx.beginPath(); ctx.arc(cx,cy,pR*2,0,Math.PI*2); ctx.fillStyle=gw; ctx.fill();

        /* 행성 */
        const pg = ctx.createRadialGradient(cx-pR*.22,cy-pR*.22,pR*.04,cx,cy,pR);
        pg.addColorStop(0,'#93c5fd'); pg.addColorStop(0.35,'#3b82f6'); pg.addColorStop(1,'#1e3a8a');
        ctx.beginPath(); ctx.arc(cx,cy,pR,0,Math.PI*2); ctx.fillStyle=pg; ctx.fill();

        /* 물체 위치 */
        const MAX_H=50000;
        const objPx = pR + (Math.min(h_km,MAX_H)/MAX_H)* pR * 1.6;
        const ox = cx + objPx, oy = cy;

        /* 화살표 (중력: 물체→행성) */
        const arLen = Math.min(objPx - pR - 14, 80);
        if (arLen > 6){
            ctx.beginPath();
            ctx.moveTo(ox - 8, oy);
            ctx.lineTo(ox - 8 - arLen, oy);
            ctx.strokeStyle='#ef4444'; ctx.lineWidth=2.5; ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(ox-8-arLen,oy); ctx.lineTo(ox-8-arLen+9,oy-5); ctx.lineTo(ox-8-arLen+9,oy+5);
            ctx.closePath(); ctx.fillStyle='#ef4444'; ctx.fill();
        }

        /* 물체 */
        const og = ctx.createRadialGradient(ox-2,oy-2,0,ox,oy,8);
        og.addColorStop(0,'#fed7aa'); og.addColorStop(1,'#ea580c');
        ctx.beginPath(); ctx.arc(ox,oy,8,0,Math.PI*2); ctx.fillStyle=og; ctx.fill();
        ctx.beginPath(); ctx.arc(ox,oy,12,0,Math.PI*2);
        ctx.strokeStyle='rgba(251,146,60,0.35)'; ctx.lineWidth=2; ctx.stroke();

        /* g 레이블 */
        const g_val = G*M/Math.pow(R+h_km*1000,2);
        ctx.fillStyle='#fbbf24'; ctx.font='bold 13px "Space Mono",monospace';
        ctx.fillText(`g = ${g_val.toFixed(3)}`, ox+14, oy-6);
        ctx.fillStyle='#64748b'; ctx.font='11px sans-serif';
        ctx.fillText(`h = ${h_km.toLocaleString()} km`, ox+14, oy+14);

        /* 스케일 힌트 */
        const pxPerKm = (pR*1.6)/MAX_H;
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
        const { G, M, R, h_km } = v.current;
        const w=canvas.width, h=canvas.height;
        const ml=44, mr=16, mt=14, mb=32;
        const gw=w-ml-mr, gh=h-mt-mb;

        ctx.clearRect(0,0,w,h);
        ctx.fillStyle='#070b14'; ctx.fillRect(0,0,w,h);

        /* 그래프 배경 */
        ctx.fillStyle='#0a0f1e'; ctx.fillRect(ml,mt,gw,gh);

        const maxR = R*10;
        const g0  = G*M/(R*R);

        /* Y 그리드 */
        for(let i=0;i<=4;i++){
            const gy=mt+gh*(i/4);
            ctx.beginPath(); ctx.moveTo(ml,gy); ctx.lineTo(ml+gw,gy);
            ctx.strokeStyle='rgba(30,41,59,0.9)'; ctx.lineWidth=1; ctx.stroke();
            const gVal=g0*(1-i/4);
            ctx.fillStyle='#475569'; ctx.font='10px monospace';
            ctx.textAlign='right';
            ctx.fillText(gVal.toFixed(1), ml-4, gy+4);
            ctx.textAlign='left';
        }

        /* 곡선 */
        ctx.beginPath();
        for(let px=0;px<=gw;px++){
            const r=R+(px/gw)*(maxR-R);
            const g=G*M/(r*r);
            const gy=mt+gh*(1-Math.min(g/g0,1));
            if(px===0) ctx.moveTo(ml+px,gy); else ctx.lineTo(ml+px,gy);
        }
        ctx.strokeStyle='#3b82f6'; ctx.lineWidth=2.5; ctx.stroke();

        /* 현재 고도 점 */
        const curR=R+h_km*1000;
        const curG=G*M/(curR*curR);
        const cpx=ml+((curR-R)/(maxR-R))*gw;
        const cpy=mt+gh*(1-Math.min(curG/g0,1));
        ctx.beginPath(); ctx.arc(cpx,cpy,5,0,Math.PI*2);
        ctx.fillStyle='#ef4444'; ctx.fill();
        ctx.beginPath(); ctx.arc(cpx,cpy,9,0,Math.PI*2);
        ctx.strokeStyle='rgba(239,68,68,0.4)'; ctx.lineWidth=2; ctx.stroke();

        /* X 축 레이블 */
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
    const [G, setG]     = useState(6.674e-11);
    const [M, setM]     = useState(5.972e24);
    const [R, setR]     = useState(6371000);
    const [m, setm]     = useState(1.0);
    const [h_km, setH]  = useState(0);

    const r   = R + h_km * 1000;
    const g   = G * M / (r * r);
    const F   = G * M * m / (r * r);

    const applyPreset = p => { setM(p.M); setR(p.R); setH(0); };

    return (
        <div style={{display:'grid',gridTemplateColumns:'290px 1fr',gap:16,minHeight:650}}>

            {/* ── 왼쪽 패널 ── */}
            <div className="panel" style={{display:'flex',flexDirection:'column',gap:14}}>
                <div>
                    <h2 style={{fontSize:20,fontWeight:800,color:'#e2e8f0',marginBottom:4}}>중력 물리 계산기</h2>
                    <p style={{color:'#475569',fontSize:12,fontStyle:'italic'}}>뉴턴의 만유인력 법칙: F = G·M·m / r²</p>
                </div>

                {/* 프리셋 */}
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

                {/* 결과 */}
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

            {/* ── 오른쪽 ── */}
            <div style={{display:'flex',flexDirection:'column',gap:14}}>
                {/* 행성 Canvas */}
                <div style={{flex:'1 1 0',minHeight:320,background:'#070b14',borderRadius:14,
                    border:'1px solid #1e293b',overflow:'hidden'}}>
                    <PlanetCanvas G={G} M={M} R={R} m={m} h_km={h_km}/>
                </div>

                {/* 그래프 */}
                <div style={{flex:'0 0 220px',background:'#0f172a',borderRadius:14,
                    border:'1px solid #1e293b',overflow:'hidden',padding:'14px 6px 2px'}}>
                    <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700,margin:'0 0 6px 40px',
                        borderLeft:'3px solid #3b82f6',paddingLeft:10}}>
                        고도에 따른 중력 가속도(g) 그래프
                    </p>
                    <div style={{height:168}}>
                        <GraphCanvas G={G} M={M} R={R} h_km={h_km}/>
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
    components.html(react_code, height=720, scrolling=False)

if __name__ == "__main__":
    run_sim()
