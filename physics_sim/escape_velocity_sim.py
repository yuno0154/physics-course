import streamlit as st
import streamlit.components.v1 as components

st.sidebar.title("🚀 탈출속도 탐구")
st.sidebar.markdown("천체를 탈출하기 위한 최소 속도를 탐구합니다.")

REACT_HTML = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#070c18;color:#e2e8f0;padding:16px;}
.tab-bar{display:flex;gap:6px;margin-bottom:20px;flex-wrap:wrap;}
.tab-btn{padding:9px 18px;border-radius:10px;border:1px solid #1e293b;background:#0d1526;
  color:#64748b;cursor:pointer;font-size:13px;font-weight:700;font-family:inherit;transition:all 0.2s;}
.tab-btn.active{background:#1d4ed8;border-color:#3b82f6;color:#fff;}
.tab-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.card{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;margin-bottom:16px;}
.hl-box{background:linear-gradient(135deg,#0c1a3a,#0f2050);border:1px solid #1d4ed8;border-radius:12px;padding:16px;margin-bottom:14px;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;}
.preset-btn{padding:6px 14px;background:#1e293b;border:1px solid #334155;border-radius:8px;
  color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;font-weight:600;}
.preset-btn:hover,.preset-btn.sel{border-color:#3b82f6;color:#e2e8f0;background:#1e3a5f;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;
  background:#3b82f6;cursor:pointer;box-shadow:0 0 8px rgba(59,130,246,0.6);}
.step-btn{width:100%;display:flex;align-items:center;gap:12px;padding:14px 18px;
  background:#0d1526;border:none;cursor:pointer;text-align:left;font-family:inherit;border-radius:12px;}
.step-content{padding:18px 24px;display:flex;flex-direction:column;gap:12px;}
.qa-btn{width:100%;display:flex;align-items:flex-start;gap:12px;padding:14px 18px;
  background:transparent;border:none;cursor:pointer;text-align:left;font-family:inherit;}
.launch-btn{padding:12px 32px;background:#1d4ed8;border:none;border-radius:30px;color:#fff;
  font-weight:800;font-size:15px;font-family:inherit;cursor:pointer;
  box-shadow:0 4px 18px rgba(29,78,216,0.5);transition:all 0.2s;}
.launch-btn:hover{background:#2563eb;transform:translateY(-2px);}
.launch-btn:disabled{background:#334155;cursor:not-allowed;transform:none;box-shadow:none;}
label{font-size:11px;color:#64748b;font-weight:700;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.05em;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef, useCallback } = React;

/* ── 물리 상수 (정규화) ── */
const PLANET_R = 90;       // 캔버스에서 행성 반지름 (px)
const GM_NORM  = 4050;     // G*M 정규화값 → v_esc = sqrt(2*4050/90) = sqrt(90) ≈ 9.49 px/step
const V_ESC    = Math.sqrt(2 * GM_NORM / PLANET_R); // ≈ 9.49

/* ── 천체 프리셋 ── */
const G_REAL = 6.674e-11;
const PRESETS = [
  { name:'지구', M:5.972e24, R:6.371e6, color:'#3b82f6', emoji:'🌍' },
  { name:'달',   M:7.342e22, R:1.737e6, color:'#94a3b8', emoji:'🌙' },
  { name:'화성', M:6.390e23, R:3.390e6, color:'#ef4444', emoji:'🔴' },
  { name:'목성', M:1.898e27, R:6.991e7, color:'#f59e0b', emoji:'🟠' },
  { name:'태양', M:1.989e30, R:6.960e8, color:'#fbbf24', emoji:'☀️' },
];

const calcEsc = (M, R) => Math.sqrt(2 * G_REAL * M / R) / 1000; // km/s

/* ── KaTeX 수식 렌더링 ── */
const Eq = ({ f, display=false, color='#93c5fd' }) => {
  const ref = useRef(null);
  useEffect(() => {
    if (ref.current && window.katex)
      window.katex.render(f, ref.current, { throwOnError:false, displayMode:display });
  }, [f, display]);
  return <span ref={ref} style={{ color }} />;
};

/* ──────────────────────────────────────────────
   탭 1: 탈출 시뮬레이션
────────────────────────────────────────────── */
function SimTab() {
  const canvasRef = useRef(null);
  const animRef   = useRef(null);
  const simRef    = useRef(null);
  const [vFrac, setVFrac]   = useState(0.85);   // v0 / v_esc
  const [status, setStatus] = useState('ready'); // ready | running | escaped | returned
  const [energySnap, setEnergySnap] = useState({ Ek:0, Ep:0, Et:0 });

  const DT    = 0.18;
  const STEPS = 6;

  const launch = () => {
    cancelAnimationFrame(animRef.current);
    const v0 = vFrac * V_ESC;
    simRef.current = { r: PLANET_R, v: v0, trail:[] };
    setStatus('running');
  };

  useEffect(() => {
    if (status !== 'running') return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const W = 820, H = 400;
    const CX = W * 0.26, CY = H * 0.5;

    const drawFrame = () => {
      const s = simRef.current;
      let done = false, escaped = false;

      for (let i = 0; i < STEPS; i++) {
        const a = -GM_NORM / (s.r * s.r);
        s.v += a * DT;
        s.r += s.v * DT;
        if (s.r > W * 1.3) { escaped = true; done = true; break; }
        if (s.r <= PLANET_R) { s.r = PLANET_R; done = true; break; }
      }

      const objX = CX + (s.r - PLANET_R);
      const objY = CY;
      const Ek = Math.max(0, 0.5 * s.v * s.v);
      const Ep = -GM_NORM / s.r;
      const Et = Ek + Ep;

      if (s.trail.length === 0 || Math.abs(objX - s.trail[s.trail.length-1].x) > 1.5) {
        s.trail.push({ x: Math.min(objX, W - 20), y: objY });
        if (s.trail.length > 400) s.trail.shift();
      }

      setEnergySnap({ Ek, Ep, Et });

      /* ── 배경 ── */
      ctx.fillStyle = '#05070a';
      ctx.fillRect(0, 0, W, H);
      for (let i = 0; i < 120; i++) {
        const sx = (i * 137.5) % W, sy = (i * 97 + i * 11) % H;
        ctx.beginPath(); ctx.arc(sx, sy, 0.4 + (i%3)*0.3, 0, Math.PI*2);
        ctx.fillStyle = `rgba(210,225,255,${0.08+(i%5)*0.05})`; ctx.fill();
      }

      /* ── 행성 ── */
      const pg = ctx.createRadialGradient(CX-22, CY-22, 8, CX, CY, PLANET_R);
      pg.addColorStop(0,'#93c5fd'); pg.addColorStop(0.45,'#2563eb'); pg.addColorStop(1,'#1e3a8a');
      ctx.beginPath(); ctx.arc(CX, CY, PLANET_R, 0, Math.PI*2); ctx.fillStyle=pg; ctx.fill();
      const ag = ctx.createRadialGradient(CX,CY,PLANET_R,CX,CY,PLANET_R*1.28);
      ag.addColorStop(0,'rgba(59,130,246,0.28)'); ag.addColorStop(1,'rgba(59,130,246,0)');
      ctx.beginPath(); ctx.arc(CX,CY,PLANET_R*1.28,0,Math.PI*2); ctx.fillStyle=ag; ctx.fill();
      ctx.fillStyle='#93c5fd'; ctx.font='bold 13px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText('행성', CX, CY + PLANET_R + 18);

      /* ── 탈출 속도 기준선 ── */
      ctx.save(); ctx.setLineDash([6,5]);
      ctx.strokeStyle='rgba(34,197,94,0.3)'; ctx.lineWidth=1.2;
      ctx.beginPath(); ctx.moveTo(CX+PLANET_R+5, CY-24); ctx.lineTo(W-30, CY-24); ctx.stroke();
      ctx.restore();
      ctx.fillStyle='rgba(34,197,94,0.55)'; ctx.font='11px Noto Sans KR'; ctx.textAlign='left';
      ctx.fillText('⟵ 탈출 경로', CX+PLANET_R+8, CY-10);

      /* ── 궤적 ── */
      s.trail.forEach((pt, i) => {
        const a = 0.08 + (i/s.trail.length)*0.75;
        ctx.beginPath(); ctx.arc(pt.x, pt.y, 2.4, 0, Math.PI*2);
        ctx.fillStyle = `rgba(251,191,36,${a})`; ctx.fill();
      });

      /* ── 물체 ── */
      if (!done || escaped) {
        const ox = Math.min(CX+(s.r-PLANET_R), W-20);
        const og = ctx.createRadialGradient(ox-3,objY-3,1,ox,objY,10);
        og.addColorStop(0,'#fef3c7'); og.addColorStop(1,'#f59e0b');
        ctx.beginPath(); ctx.arc(ox, objY, 10, 0, Math.PI*2); ctx.fillStyle=og; ctx.fill();
        ctx.beginPath(); ctx.arc(ox, objY, 15, 0, Math.PI*2);
        ctx.strokeStyle='rgba(251,191,36,0.4)'; ctx.lineWidth=2; ctx.stroke();
      }

      /* ── 에너지 막대 ── */
      const E0 = GM_NORM / PLANET_R;
      const bX=W*0.71, bY=H*0.08, bW=28, bH=H*0.72;
      ctx.fillStyle='rgba(15,23,42,0.92)'; ctx.strokeStyle='rgba(51,65,85,0.8)';
      ctx.lineWidth=1;
      ctx.beginPath(); ctx.roundRect(bX-18,bY-36,bW*4+36,bH+56,10); ctx.fill(); ctx.stroke();
      ctx.fillStyle='#cbd5e1'; ctx.font='bold 12px Noto Sans KR'; ctx.textAlign='center';
      ctx.fillText('에너지 변화', bX+bW*1.5+18, bY-16);

      const midY = bY + bH * 0.45;
      const scale = bH * 0.4 / E0;

      [[0,'#22c55e','Ek'],[1,'#ef4444','Ep'],[2,'#a78bfa','E합']]
        .forEach(([idx, color, lbl]) => {
          const x = bX + idx*(bW+10);
          const vals = [Ek, Ep, Et];
          const v = vals[idx];
          const barH = Math.min(Math.abs(v)*scale, bH*0.44);
          ctx.fillStyle = color + '33'; ctx.strokeStyle = color;
          ctx.lineWidth = 1;
          if (v >= 0) {
            ctx.beginPath(); ctx.roundRect(x, midY-barH, bW, barH, 4);
          } else {
            ctx.beginPath(); ctx.roundRect(x, midY, bW, barH, 4);
          }
          ctx.fill(); ctx.stroke();
          ctx.fillStyle = color; ctx.font = 'bold 11px Space Mono'; ctx.textAlign='center';
          ctx.fillText(lbl, x+bW/2, bY+bH+18);
          ctx.fillStyle='#94a3b8'; ctx.font='9px Space Mono';
          ctx.fillText(v.toFixed(0), x+bW/2, v>=0 ? midY-barH-5 : midY+barH+14);
        });

      ctx.strokeStyle='rgba(148,163,184,0.5)'; ctx.lineWidth=1;
      ctx.beginPath(); ctx.moveTo(bX-14,midY); ctx.lineTo(bX+bW*3+22,midY); ctx.stroke();
      ctx.fillStyle='#475569'; ctx.font='10px sans-serif'; ctx.textAlign='left';
      ctx.fillText('E=0', bX-14, midY-4);

      /* ── 결과 표시 ── */
      if (done) {
        const msg = escaped ? '🚀 탈출 성공!' : '↩ 탈출 실패 — 낙하';
        const col = escaped ? '#22c55e' : '#ef4444';
        ctx.fillStyle = col; ctx.font = 'bold 22px Noto Sans KR'; ctx.textAlign='center';
        ctx.fillText(msg, W*0.42, H*0.13);
        setStatus(escaped ? 'escaped' : 'returned');
        return;
      }

      ctx.textAlign='left';
      animRef.current = requestAnimationFrame(drawFrame);
    };
    animRef.current = requestAnimationFrame(drawFrame);
    return () => cancelAnimationFrame(animRef.current);
  }, [status]);

  const vKms  = (vFrac * V_ESC).toFixed(2);
  const E0 = GM_NORM / PLANET_R;
  const Ek0 = 0.5 * (vFrac * V_ESC) ** 2;
  const Ep0 = -GM_NORM / PLANET_R;

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>🎯 핵심 개념</p>
        <p style={{color:'#cbd5e1',fontSize:14,lineHeight:1.8}}>
          역학적 에너지 보존 법칙에 따라, 물체가 천체를 완전히 탈출하려면
          무한히 먼 곳에서 역학적 에너지가 <strong style={{color:'#93c5fd'}}>0 이상</strong>이어야 합니다.
          따라서 탈출 속도는 <Eq f="E_{\text{역학}} = \tfrac{1}{2}mv_0^2 - \tfrac{GMm}{R} = 0" /> 에서 구합니다.
        </p>
      </div>

      <div style={{display:'grid',gridTemplateColumns:'260px 1fr',gap:16,marginBottom:16}}>
        <div className="card" style={{display:'flex',flexDirection:'column',gap:14}}>
          <div>
            <label>발사 속도 (v₀ / v탈출)</label>
            <input type="range" min={0.3} max={1.5} step={0.01} value={vFrac}
              onChange={e=>{ cancelAnimationFrame(animRef.current); setStatus('ready'); setVFrac(parseFloat(e.target.value)); }}/>
            <div style={{display:'flex',justifyContent:'space-between',fontSize:12,color:'#64748b',marginTop:4}}>
              <span>v₀ = {(vFrac*100).toFixed(0)}% v탈출</span>
              <span style={{color: vFrac>=1?'#22c55e':'#f87171'}}>{vFrac>=1?'탈출 가능':'탈출 불가'}</span>
            </div>
          </div>

          <div style={{background:'#070b14',borderRadius:10,padding:'6px 14px',border:'1px solid #1e293b'}}>
            <div className="result-row"><span style={{color:'#64748b'}}>발사 속도</span>
              <span className="val">{vKms} (상대)</span></div>
            <div className="result-row"><span style={{color:'#64748b'}}>초기 운동 에너지 Eₖ</span>
              <span className="val" style={{color:'#22c55e'}}>{Ek0.toFixed(1)}</span></div>
            <div className="result-row"><span style={{color:'#64748b'}}>초기 퍼텐셜 에너지 Eₚ</span>
              <span className="val" style={{color:'#ef4444'}}>{Ep0.toFixed(1)}</span></div>
            <div className="result-row"><span style={{color:'#64748b'}}>총 역학적 에너지</span>
              <span className="val" style={{color: Ek0+Ep0>=0?'#22c55e':'#ef4444'}}>{(Ek0+Ep0).toFixed(1)}</span></div>
          </div>

          {status !== 'running' && (
            <button className="launch-btn" onClick={launch}>
              {status==='ready' ? '▶ 발사' : '🔄 다시 발사'}
            </button>
          )}
          {status==='running' && (
            <button className="launch-btn" disabled>🚀 비행 중...</button>
          )}

          <div style={{fontSize:12,color:'#475569',lineHeight:1.9,borderTop:'1px solid #1e293b',paddingTop:10}}>
            <p>✅ 총 에너지 ≥ 0 → 탈출 성공</p>
            <p>❌ 총 에너지 &lt; 0 → 중력에 잡혀 낙하</p>
            <p style={{marginTop:6,color:'#64748b'}}>에너지 막대: 초록=운동, 빨강=퍼텐셜, 보라=합계</p>
          </div>
        </div>

        <canvas ref={canvasRef} width={820} height={400}
          style={{width:'100%',height:'400px',borderRadius:'12px',background:'#05070a'}}/>
      </div>

      <div className="hl-box">
        <p style={{color:'#a78bfa',fontWeight:700,fontSize:14,marginBottom:8}}>📌 탐구 포인트</p>
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr 1fr',gap:12}}>
          {[
            ['슬라이더를 1.0 미만으로', '총 에너지 < 0 → 낙하. 운동 에너지가 소진되기 전에 방향이 반전됩니다.'],
            ['슬라이더를 1.0으로', '총 에너지 = 0. 무한히 먼 곳에 겨우 도달하는 경계 상태입니다.'],
            ['슬라이더를 1.0 초과로', '총 에너지 > 0. 탈출 후에도 잔여 운동 에너지가 남습니다.'],
          ].map(([t,d],i)=>(
            <div key={i} style={{background:'rgba(0,0,0,0.3)',borderRadius:10,padding:12}}>
              <p style={{color:'#fbbf24',fontSize:12,fontWeight:700,marginBottom:4}}>{t}</p>
              <p style={{color:'#94a3b8',fontSize:12,lineHeight:1.7}}>{d}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 2: 탈출속도 계산기
────────────────────────────────────────────── */
function CalcTab() {
  const [sel, setSel]    = useState(0);
  const [customM, setCM] = useState(5.972e24);
  const [customR, setCR] = useState(6.371e6);
  const [isCustom, setIsCustom] = useState(false);

  const preset = PRESETS[sel];
  const M = isCustom ? customM : preset.M;
  const R = isCustom ? customR : preset.R;
  const v = calcEsc(M, R);
  const G = G_REAL;

  return (
    <div>
      <div className="hl-box" style={{marginBottom:16}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>🧮 탈출속도 계산기</p>
        <p style={{color:'#cbd5e1',fontSize:14}}>
          탈출속도 공식: <Eq f="v_{\text{탈출}} = \sqrt{\dfrac{2GM}{R}}" />
        </p>
      </div>

      <div style={{display:'flex',gap:8,flexWrap:'wrap',marginBottom:16}}>
        {PRESETS.map((p,i)=>(
          <button key={i} className={`preset-btn ${!isCustom&&sel===i?'sel':''}`}
            onClick={()=>{ setSel(i); setIsCustom(false); }}>
            {p.emoji} {p.name}
          </button>
        ))}
        <button className={`preset-btn ${isCustom?'sel':''}`} onClick={()=>setIsCustom(true)}>
          ✏️ 사용자 입력
        </button>
      </div>

      {isCustom && (
        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:12,marginBottom:16}}>
          <div className="card">
            <label>천체 질량 (M) [kg]</label>
            <input type="number" value={customM} step="1e22"
              onChange={e=>{ const v=parseFloat(e.target.value); if(v>0) setCM(v); }}
              style={{background:'#070b14',border:'1px solid #1e293b',borderRadius:8,color:'#e2e8f0',
                padding:'8px 10px',fontSize:13,width:'100%',outline:'none',fontFamily:'inherit'}}/>
          </div>
          <div className="card">
            <label>천체 반지름 (R) [m]</label>
            <input type="number" value={customR} step="1000"
              onChange={e=>{ const v=parseFloat(e.target.value); if(v>0) setCR(v); }}
              style={{background:'#070b14',border:'1px solid #1e293b',borderRadius:8,color:'#e2e8f0',
                padding:'8px 10px',fontSize:13,width:'100%',outline:'none',fontFamily:'inherit'}}/>
          </div>
        </div>
      )}

      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:16}}>
        <div className="card">
          <p style={{color:'#64748b',fontSize:12,marginBottom:12,fontWeight:700}}>입력값</p>
          <div className="result-row"><span style={{color:'#94a3b8'}}>질량 (M)</span>
            <span className="val">{M.toExponential(3)} kg</span></div>
          <div className="result-row"><span style={{color:'#94a3b8'}}>반지름 (R)</span>
            <span className="val">{(R/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})} km</span></div>
          <div className="result-row"><span style={{color:'#94a3b8'}}>표면 중력 (g)</span>
            <span className="val">{(G*M/R/R).toFixed(2)} m/s²</span></div>
        </div>
        <div className="card" style={{background:'linear-gradient(135deg,#0c2a0c,#0a3d0a)',borderColor:'#22c55e'}}>
          <p style={{color:'#22c55e',fontSize:12,marginBottom:12,fontWeight:800}}>탈출속도</p>
          <div style={{textAlign:'center',padding:'16px 0'}}>
            <p style={{color:'#86efac',fontSize:36,fontWeight:800,fontFamily:'Space Mono'}}>
              {v.toFixed(2)}
            </p>
            <p style={{color:'#4ade80',fontSize:16}}>km/s</p>
          </div>
          <p style={{color:'#4ade80',fontSize:12,textAlign:'center'}}>
            = {(v*1000).toFixed(0)} m/s
          </p>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>태양계 천체 탈출속도 비교</p>
        <div style={{overflowX:'auto'}}>
          <table style={{width:'100%',borderCollapse:'collapse',fontSize:13}}>
            <thead>
              <tr style={{borderBottom:'1px solid #1e293b'}}>
                {['천체','질량 (kg)','반지름 (km)','탈출속도 (km/s)','표면 중력 (m/s²)'].map(h=>(
                  <th key={h} style={{padding:'10px 12px',color:'#64748b',fontWeight:700,textAlign:'left'}}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {PRESETS.map((p,i)=>{
                const ve = calcEsc(p.M, p.R);
                const g = G_REAL*p.M/p.R/p.R;
                return (
                  <tr key={i} style={{borderBottom:'1px solid #0f172a',
                    background: !isCustom&&sel===i?'rgba(29,78,216,0.15)':undefined}}>
                    <td style={{padding:'10px 12px',color:p.color,fontWeight:700}}>{p.emoji} {p.name}</td>
                    <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{p.M.toExponential(3)}</td>
                    <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{(p.R/1000).toLocaleString('ko-KR',{maximumFractionDigits:0})}</td>
                    <td style={{padding:'10px 12px',color:'#60a5fa',fontWeight:800,fontFamily:'Space Mono'}}>{ve.toFixed(2)}</td>
                    <td style={{padding:'10px 12px',color:'#94a3b8',fontFamily:'Space Mono',fontSize:12}}>{g.toFixed(2)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      <div className="hl-box" style={{marginTop:14}}>
        <p style={{color:'#a78bfa',fontWeight:700,marginBottom:8}}>📌 패턴 찾기</p>
        <p style={{color:'#cbd5e1',fontSize:13,lineHeight:1.9}}>
          탈출속도는 <strong style={{color:'#93c5fd'}}>질량이 클수록 증가</strong>하고,
          <strong style={{color:'#93c5fd'}}> 반지름이 작을수록 증가</strong>합니다.
          목성의 탈출속도가 태양보다 작은 이유는 태양의 질량이 압도적으로 크기 때문입니다.
          태양의 탈출속도 617 km/s는 빛의 속도(300,000 km/s)의 약 0.2%에 불과합니다.
          그렇다면 v탈출 = c가 되려면 반지름이 얼마나 작아야 할까요?
        </p>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 3: 수식 유도
────────────────────────────────────────────── */
const STEPS = [
  { n:1, title:'역학적 에너지 보존 법칙 적용', color:'#3b82f6', bg:'#0d1f3c',
    formula:'E_{\\text{역학}} = E_k + E_p = \\text{일정}',
    note:'외력이 없으면 운동 에너지와 퍼텐셜 에너지의 합은 보존됩니다.' },
  { n:2, title:'출발점 (천체 표면) 에너지 작성', color:'#8b5cf6', bg:'#1a0d3c',
    formula:'E = \\dfrac{1}{2}mv_0^2 - \\dfrac{GMm}{R}',
    note:'R: 천체 반지름. 중력 퍼텐셜 에너지의 기준점은 무한히 먼 곳(Ep=0)입니다.' },
  { n:3, title:'탈출 조건: 무한히 먼 곳에서의 에너지 ≥ 0', color:'#a855f7', bg:'#1e0d3c',
    formula:'\\dfrac{1}{2}mv_0^2 - \\dfrac{GMm}{R} \\geq 0',
    note:'무한히 먼 곳에서 Ep = 0이므로, 탈출하려면 총 에너지가 0 이상이어야 합니다.' },
  { n:4, title:'등호 조건 (최소 탈출속도)로 정리', color:'#10b981', bg:'#0a1f18',
    formula:'\\dfrac{1}{2}mv_0^2 = \\dfrac{GMm}{R}',
    note:'양변에서 m이 약분됩니다! 탈출속도는 발사체의 질량에 무관합니다.' },
  { n:5, title:'탈출속도 최종 공식', color:'#fbbf24', bg:'#1f1200',
    formula:'v_{\\text{탈출}} = \\sqrt{\\dfrac{2GM}{R}}',
    note:'G: 중력상수 (6.674×10⁻¹¹ N·m²/kg²), M: 천체 질량, R: 천체 반지름' },
];

function DerivTab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:6}}>📐 탈출속도 수식 유도</p>
        <p style={{color:'#cbd5e1',fontSize:13,lineHeight:1.8}}>
          역학적 에너지 보존 법칙만으로 탈출속도를 유도합니다. 각 단계를 클릭하여 내용을 확인하세요.
        </p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10,marginBottom:20}}>
        {STEPS.map((s,i)=>(
          <div key={i} style={{border:`1px solid ${open===i?s.color+'90':'#1e293b'}`,borderRadius:14,overflow:'hidden',transition:'border-color 0.25s'}}>
            <button className="step-btn" onClick={()=>setOpen(open===i?null:i)}>
              <div style={{width:34,height:34,borderRadius:'50%',background:s.color,display:'flex',
                alignItems:'center',justifyContent:'center',color:'#fff',fontWeight:800,fontSize:15,flexShrink:0}}>
                {s.n}
              </div>
              <div style={{flex:1}}>
                <p style={{color:'#e2e8f0',fontSize:14,fontWeight:700}}>{s.title}</p>
              </div>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </button>
            <div style={{maxHeight:open===i?'260px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
              <div className="step-content" style={{background:s.bg}}>
                <div style={{background:'rgba(0,0,0,0.3)',borderRadius:12,padding:'18px 24px',
                  display:'flex',justifyContent:'center',border:`1px solid ${s.color}30`}}>
                  <Eq f={s.formula} display={true} color={s.color}/>
                </div>
                <div style={{display:'flex',gap:10,alignItems:'flex-start'}}>
                  <span style={{fontSize:16,flexShrink:0}}>💡</span>
                  <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.75}}>{s.note}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{background:'linear-gradient(135deg,#064e3b,#065f46)',borderRadius:16,padding:'20px 28px',
        border:'1px solid #10b981',display:'flex',alignItems:'center',gap:20,marginBottom:16}}>
        <div style={{fontSize:34}}>✅</div>
        <div>
          <p style={{color:'#34d399',fontWeight:800,fontSize:15,marginBottom:6}}>결론</p>
          <p style={{color:'#6ee7b7',fontSize:13,lineHeight:1.8}}>
            탈출속도는 발사체의 질량 m에 무관하며, 오직 천체의 질량 M과 반지름 R에만 의존합니다.<br/>
            질량이 클수록, 반지름이 작을수록 탈출속도가 커집니다.<br/>
            만약 탈출속도가 빛의 속도(c)와 같아진다면 어떤 일이 일어날까요?
          </p>
        </div>
      </div>

      <div className="card">
        <p style={{fontWeight:800,color:'#e2e8f0',marginBottom:14}}>🖊️ 심화: 탈출속도와 빛의 속도</p>
        <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.9}}>
          탈출속도 공식에서 v = c로 놓으면:<br/>
        </p>
        <div style={{textAlign:'center',margin:'16px 0'}}>
          <Eq f="c = \\sqrt{\\dfrac{2GM}{R}} \\implies R_s = \\dfrac{2GM}{c^2}" display={true} color='#fbbf24'/>
        </div>
        <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.9}}>
          이것이 슈바르츠실트 반지름입니다. 다음 탐구(블랙홀 탐구)에서 자세히 알아봅시다.
        </p>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   탭 4: 탐구 질문
────────────────────────────────────────────── */
const QA = [
  { q:'탈출속도는 발사 방향과 관계없이 같을까?',
    a:'네, 탈출속도는 방향에 무관합니다. 수직으로 발사하든 비스듬히 발사하든 역학적 에너지 보존 법칙에서 방향 성분은 사라지므로, 탈출에 필요한 속력의 크기는 동일합니다. 단, 대기권이 있는 경우 공기 저항 때문에 실제 필요 속도는 달라집니다.' },
  { q:'발사체의 질량이 두 배가 되면 탈출속도도 두 배가 될까?',
    a:'아닙니다. v탈출 = √(2GM/R)에서 발사체의 질량(m)이 없습니다. 탈출속도는 발사체의 질량과 무관합니다. 무거운 로켓이나 가벼운 물체나 같은 속도로 발사해야 탈출합니다. 이는 역학적 에너지에서 m이 약분되기 때문입니다.' },
  { q:'지구의 질량을 그대로 두고 반지름만 절반으로 줄이면 탈출속도는?',
    a:'v ∝ 1/√R 이므로, R이 1/2배가 되면 v탈출은 √2배 ≈ 1.41배가 됩니다. 지구 탈출속도는 약 11.2 km/s이므로, 반지름이 절반이 된 지구의 탈출속도는 약 15.8 km/s가 됩니다. 지구 반지름을 약 9 mm로 압축하면 탈출속도 = 빛의 속도(블랙홀 조건)가 됩니다.' },
  { q:'탈출속도와 궤도 속도의 차이는?',
    a:'원 궤도 속도 v_궤도 = √(GM/R), 탈출속도 v_탈출 = √(2GM/R) = √2 × v_궤도 입니다. 탈출속도는 원 궤도 속도의 √2 ≈ 1.41배입니다. 원 궤도를 돌기 위해서는 탈출속도의 1/√2만 있으면 됩니다.' },
  { q:'왜 달에서 발사하는 것이 지구에서 발사하는 것보다 유리할까?',
    a:'달의 탈출속도는 약 2.4 km/s로 지구(11.2 km/s)의 약 1/5입니다. 또한 달에는 대기가 없으므로 공기 저항도 없습니다. 따라서 달 기지에서 우주로 물자를 보내는 데 훨씬 적은 에너지가 필요합니다. 이것이 달 기지 건설의 중요한 이유 중 하나입니다.' },
];

function QATab() {
  const [open, setOpen] = useState(null);
  return (
    <div>
      <div className="hl-box" style={{marginBottom:18}}>
        <p style={{color:'#fbbf24',fontWeight:800,fontSize:15,marginBottom:4}}>❓ 탐구 질문</p>
        <p style={{color:'#94a3b8',fontSize:13}}>질문을 클릭하면 답변이 펼쳐집니다. 먼저 스스로 생각해 보세요.</p>
      </div>
      <div style={{display:'flex',flexDirection:'column',gap:10}}>
        {QA.map((item,i)=>(
          <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#3b82f6':'#1e293b'}`,
            overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
            <button className="qa-btn" onClick={()=>setOpen(open===i?null:i)}>
              <span style={{color:'#6366f1',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
              <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
              <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',
                transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
            </button>
            <div style={{maxHeight:open===i?'300px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
              <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.8}}>{item.a}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────
   메인 앱
────────────────────────────────────────────── */
const TABS = [
  { id:'sim',   label:'🔬 탈출 시뮬레이션' },
  { id:'calc',  label:'🧮 탈출속도 계산기' },
  { id:'deriv', label:'📐 수식 유도' },
  { id:'qa',    label:'❓ 탐구 질문' },
];

const App = () => {
  const [tab, setTab] = useState('sim');
  return (
    <div style={{maxWidth:1100,margin:'0 auto'}}>
      <div style={{background:'linear-gradient(135deg,#0f172a,#1e293b)',borderRadius:16,padding:'20px 24px',
        marginBottom:20,border:'1px solid #334155'}}>
        <h2 style={{color:'#60a5fa',margin:0,fontSize:'1.4rem'}}>🚀 학습주제 6-1: 탈출속도 탐구</h2>
        <p style={{color:'#94a3b8',margin:'8px 0 0',fontSize:'0.95rem'}}>
          <strong style={{color:'#fbbf24'}}>핵심 질문:</strong> 천체를 완전히 탈출하기 위한 최소한의 속도는 어떻게 결정되며, 왜 발사체의 질량과 무관할까?
        </p>
      </div>
      <div className="tab-bar">
        {TABS.map(t=>(
          <button key={t.id} className={`tab-btn ${tab===t.id?'active':''}`}
            onClick={()=>setTab(t.id)}>{t.label}</button>
        ))}
      </div>
      {tab==='sim'   && <SimTab/>}
      {tab==='calc'  && <CalcTab/>}
      {tab==='deriv' && <DerivTab/>}
      {tab==='qa'    && <QATab/>}
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""

components.html(REACT_HTML, height=1100, scrolling=True)
