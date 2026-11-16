import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """음파의 간섭과 소음 제어(4차시) — 학습지 A~C 순서의 탭형 시뮬레이션.
    ① 중첩의 원리 → ② 보강·상쇄 간섭(위상차) → ③ 두 스피커의 간섭(경로차, 측정점 클릭)
    → ④ 소음 제거 이어폰(진폭·위상 조절, 불규칙 소음) → ⑤ 자동차 배기 소음기(길이 차·진동수)
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS로 동작.
    """
    st.title("🔊 음파의 간섭과 소음 제어")
    components.html(HTML, height=900, scrolling=True)


HTML = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8"><style>
:root{--ink:#0f172a;--sub:#64748b;--line:#e2e8f0;--key:#1d4ed8}
*{box-sizing:border-box}body{margin:0;font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:var(--ink)}
#app{max-width:1120px;margin:0 auto;padding:4px 4px 16px}
h1{font-size:20px;margin:4px 0 2px}.lead{font-size:13px;color:var(--sub);margin:0 0 8px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}
.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 13px;font-size:13.5px;font-weight:700;color:var(--sub);cursor:pointer;font-family:inherit}
.tab.on{background:var(--key);border-color:var(--key);color:#fff}
.ctrl{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 14px;margin-bottom:8px}
.speed{background:#fffbeb;border-color:#fde68a}
.grp{display:flex;align-items:center;gap:7px;font-size:13px;font-weight:600}
input[type=range]{width:130px}.val{min-width:70px;color:var(--key);font-weight:800;font-variant-numeric:tabular-nums}
.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:6px 11px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;color:var(--ink)}
.btn.on{background:#eff6ff;border-color:#93c5fd;color:#1e3a8a}.btn.primary{background:#0f172a;color:#fff;border-color:#0f172a}
.btn.go{background:#1d4ed8;color:#fff;border-color:#1d4ed8;font-size:14px;padding:8px 14px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:8px}
canvas{display:block;width:100%;height:auto}
.view{display:none}.show{display:flex}
.step{margin-top:8px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:14px;padding:10px 14px;font-size:14.5px;line-height:1.65;min-height:64px}
.step b{color:#1d4ed8}.note{margin-top:8px;background:#f1f5f9;border-radius:14px;padding:9px 14px;font-size:13.5px;line-height:1.6}
.ws{display:inline-block;background:#dbeafe;color:#1e3a8a;border-radius:6px;padding:0 6px;font-size:12px;font-weight:800;margin-right:6px}
.read{margin-left:auto;font-size:13.5px;font-weight:700}.read b{color:var(--key)}
</style></head><body><div id="app">
<h1>🔊 음파의 간섭과 소음 제어</h1>
<p class="lead">4차시 학습지 A~C 순서의 시뮬레이션입니다. 음파는 종파이지만 공기의 변위(압력 변화)를 위아래 그래프로 나타냈습니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="rs">↺ 처음부터</button></div>
<div class="tabs" id="tabs"></div>
<div id="c0" class="ctrl view"><button class="btn on" id="p0a">B를 아래로 볼록(반대, −1칸)</button><button class="btn" id="p0b">B를 위로 볼록(같은 쪽, +1칸)</button><button class="btn" id="p0pk">📍 꼭짓점 겹침 순간 보기</button><button class="btn go" id="p0go">▶ 다시 보내기</button></div>
<div id="c1" class="ctrl view"><div class="grp">두 파동의 위상차<input type="range" id="ph1" min="0" max="360" step="15" value="0"><span class="val" id="vph1"></span></div><button class="btn" id="ph1a">같은 위상(0°)</button><button class="btn" id="ph1b">반대 위상(180°)</button></div>
<div id="c2" class="ctrl view">
 <button class="btn on" id="m2a">순간 모습(마루·골)</button><button class="btn" id="m2b">소리의 세기 분포</button>
 <div class="grp">진동수<input type="range" id="f2" min="300" max="1500" step="50" value="700"><span class="val" id="vf2"></span></div>
 <div class="grp">스피커 간격<input type="range" id="d2" min="0.5" max="2.5" step="0.1" value="1.5"><span class="val" id="vd2"></span></div>
 <label class="grp"><input type="checkbox" id="inv2"> S₂ 위상 반대로</label>
 <span style="font-size:12px;color:#64748b">화면을 클릭하면 측정점 P가 옮겨집니다</span>
</div>
<div id="c3" class="ctrl view">
 <label class="grp"><input type="checkbox" id="anc" checked> 소음 제거 켜기</label>
 <div class="grp">만든 소리의 진폭<input type="range" id="a3" min="0" max="1.2" step="0.05" value="1"><span class="val" id="va3"></span></div>
 <div class="grp">위상차<input type="range" id="p3" min="0" max="360" step="10" value="180"><span class="val" id="vp3"></span></div>
 <button class="btn" id="noise3">소음: 규칙적</button><button class="btn" id="snd3">🔊 귀에 들리는 소리</button>
</div>
<div id="c4" class="ctrl view">
 <div class="grp">두 통로의 길이 차<input type="range" id="l4" min="0" max="2" step="0.05" value="1"><span class="val" id="vl4"></span></div>
 <div class="grp">소음 진동수<input type="range" id="f4" min="50" max="700" step="10" value="170"><span class="val" id="vf4"></span></div>
 <button class="btn" data-f4="170">170 Hz (반 파장 1배·상쇄)</button>
 <button class="btn" data-f4="340">340 Hz (반 파장 2배·보강)</button>
 <button class="btn" data-f4="510">510 Hz (반 파장 3배·상쇄)</button>
</div>
<div class="card"><canvas id="cv" width="1000" height="460"></canvas></div>
<div class="step" id="step"></div><div class="note" id="note"></div>
</div>
<script>
const $=id=>document.getElementById(id),cv=$('cv'),ctx=cv.getContext('2d'),W=1000,H=460;
const BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',INK='#0f172a',SUB='#64748b',OR='#ea580c',VS=340;
const TABS=[['① 중첩의 원리','A①','두 파동이 겹치는 곳의 변위는 두 변위의 합입니다. 지나간 뒤에는 각자 원래 모양으로 진행합니다.'],
['② 보강 간섭·상쇄 간섭','A②','같은 위상으로 만나면 진폭이 커지고(보강), 반대 위상으로 만나면 진폭이 작아집니다(상쇄). 진동수는 변하지 않습니다.'],
['③ 두 스피커의 간섭','B','경로차가 반 파장의 짝수 배인 곳은 보강(소리 큼), 홀수 배인 곳은 상쇄(소리 작음)입니다.'],
['④ 소음 제거 이어폰','C①','소음과 진동수·진폭이 같고 위상이 반대인 소리를 더하면 상쇄 간섭으로 소음이 줄어듭니다.'],
['⑤ 자동차 배기 소음기','C②','두 통로의 길이 차가 반 파장의 홀수 배인 진동수의 소음이 상쇄 간섭으로 줄어듭니다.']];
let tab=0,paused=false,speed=0.5,last=performance.now(),T=0;
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};$('rs').onclick=()=>{T=0;S0.t=0};
function txt(s,x,y,o){o=o||{};ctx.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Malgun Gothic",sans-serif';ctx.fillStyle=o.c||INK;ctx.textAlign=o.a||'center';ctx.textBaseline='middle';ctx.fillText(s,x,y)}
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function head(x,y,dx,dy,c){const a=Math.atan2(dy,dx);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x,y);ctx.lineTo(x-9*Math.cos(a-0.4),y-9*Math.sin(a-0.4));ctx.lineTo(x-9*Math.cos(a+0.4),y-9*Math.sin(a+0.4));ctx.fill()}
function arr(x0,y0,x1,y1,c){ln(x0,y0,x1,y1,c,2.5);head(x1,y1,x1-x0,y1-y0,c)}
function dot(x,y,r,c){ctx.beginPath();ctx.fillStyle=c;ctx.arc(x,y,r,0,7);ctx.fill()}
function plot(f,x0,x1,y0,c,w,dash){ctx.beginPath();ctx.setLineDash(dash||[]);ctx.strokeStyle=c;ctx.lineWidth=w||2;for(let x=x0;x<=x1;x+=2){const y=y0-f(x);x===x0?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke();ctx.setLineDash([])}
function clear(){ctx.clearRect(0,0,W,H)}
// ===== tab0 pulses
const S0={t:0,inv:true};
function pulseA(x){const c=150+S0.t*95,d=Math.abs(x-c);return d<60?70*(1-d/60):0}
function pulseB(x){const c=850-S0.t*95,d=Math.abs(x-c);return (d<60?35*(1-d/60):0)*(S0.inv?-1:1)}
function scene0(dt){if(!paused){S0.t+=dt;if(S0.t>8.5)S0.t=0}clear();
 const rows=[[110,'펄스 A (+2칸)',x=>pulseA(x),BL],[230,'펄스 B ('+(S0.inv?'−1칸':'+1칸')+')',x=>pulseB(x),RD],[370,'줄의 실제 모습 (합성파 = A + B)',x=>pulseA(x)+pulseB(x),PU]];
 rows.forEach(r=>{ln(40,r[0],960,r[0],'#e2e8f0',1);txt(r[1],40,r[0]-80,{a:'left',b:1,s:13,c:r[3]});plot(r[2],40,960,r[0],r[3],r[3]===PU?3:2.2)});
 const cA=150+S0.t*95,cB=850-S0.t*95,ov=Math.abs(cA-cB)<120;
 if(ov){const xm=(cA+cB)/2;ln(xm,40,xm,440,'#cbd5e1',1,[4,4]);const ya=pulseA(xm),yb=pulseB(xm);txt('A: '+(ya/35).toFixed(1)+'  +  B: '+(yb/35).toFixed(1)+'  =  '+((ya+yb)/35).toFixed(1)+' (칸)',xm+12,300,{a:'left',b:1,s:14,c:PU})}
 $('step').innerHTML=ov?'두 펄스가 <b>겹치는 곳의 변위 = A의 변위 + B의 변위</b>입니다. '+(S0.inv?'B가 반대쪽(−1칸)이라 꼭짓점이 겹치면 <b>2 + (−1) = +1칸</b>으로 줄어듭니다(상쇄).':'같은 쪽(+1칸)이라 꼭짓점이 겹치면 <b>2 + 1 = +3칸</b>으로 더 커집니다(보강).'):(S0.t<3.68?'두 펄스가 서로를 향해 다가갑니다.':'만난 뒤에도 두 펄스는 <b>원래 모양과 크기 그대로</b> 각자 진행합니다(파동의 독립성).');}
$('p0a').onclick=()=>{S0.inv=true;S0.t=0;$('p0a').classList.add('on');$('p0b').classList.remove('on')};
$('p0b').onclick=()=>{S0.inv=false;S0.t=0;$('p0b').classList.add('on');$('p0a').classList.remove('on')};
$('p0pk').onclick=()=>{S0.t=350/95;paused=true;$('pp').textContent='▶ 재생'};
$('p0go').onclick=()=>{S0.t=0;paused=false;$('pp').textContent='⏸ 일시정지'};
// ===== tab1 phase
function scene1(dt){clear();const ph=+$('ph1').value*Math.PI/180,k=2*Math.PI/260,w=2*Math.PI*0.5,A=45;
 const f1=x=>A*Math.sin(k*x-w*T),f2=x=>A*Math.sin(k*x-w*T+ph);
 [[95,'파동 1',f1,BL],[215,'파동 2',f2,RD],[355,'합성파 (파동 1 + 파동 2)',x=>f1(x)+f2(x),PU]].forEach(r=>{ln(150,r[0],960,r[0],'#e2e8f0',1);ln(150,r[0]-90,150,r[0]+90,'#f1f5f9',1);txt(r[1],20,r[0],{a:'left',b:1,s:13,c:r[3]});plot(r[2],150,960,r[0],r[3],r[3]===PU?3:2.2)});
 const amp=2*Math.abs(Math.cos(ph/2));ln(150,355-A*2,960,355-A*2,'#e9d5ff',1,[4,4]);ln(150,355+A*2,960,355+A*2,'#e9d5ff',1,[4,4]);txt('2A',140,355-A*2,{a:'right',s:12,c:PU});
 txt('합성파의 진폭 = '+amp.toFixed(2)+' A',W-30,440,{a:'right',b:1,s:17,c:PU});
 const deg=+$('ph1').value;$('vph1').textContent=deg+'°';
 $('step').innerHTML=deg%360===0?'<b>같은 위상</b>: 마루와 마루, 골과 골이 만나 진폭이 <b>2A</b>가 됩니다 → <b>보강 간섭</b> (소리가 커짐)':(deg===180?'<b>반대 위상</b>: 마루와 골이 만나 진폭이 <b>0</b>이 됩니다 → <b>상쇄 간섭</b> (소리가 사라짐)':'위상차가 0°에 가까울수록 진폭이 커지고 180°에 가까울수록 작아집니다. 합성파의 <b>진동수(마루 사이 간격)</b>는 변하지 않습니다.');}
$('ph1a').onclick=()=>{$('ph1').value=0};$('ph1b').onclick=()=>{$('ph1').value=180};
// ===== tab2 two speakers
const S2={mode:0,px:640,py:160,img:null};
const GX=500,GY=330,sc=2; // grid units
function scene2(dt){clear();const f=+$('f2').value,lam=VS/f,d=+$('d2').value,inv=$('inv2').checked;
 $('vf2').textContent=f+' Hz (λ='+lam.toFixed(2)+' m)';$('vd2').textContent=d.toFixed(1)+' m';
 const m2px=110; // px per m
 const s1={x:120,y:330-d/2*m2px},s2={x:120,y:330+d/2*m2px}; // speakers at left, field to the right
 const fw=880,fh=320,ox=100,oy=20,res=4;
 const id=ctx.createImageData(fw/res|0,fh/res|0);const k=2*Math.PI/lam,wt=2*Math.PI*T*0.8;
 for(let j=0;j<id.height;j++)for(let i=0;i<id.width;i++){const X=ox+i*res,Y=oy+j*res;
  const r1=Math.hypot(X-s1.x,Y-(s1.y-170))/m2px,r2=Math.hypot(X-s2.x,Y-(s2.y-170))/m2px;
  let v;if(S2.mode===0){const a1=Math.sin(k*r1-wt)/Math.sqrt(r1+0.3),a2=(inv?-1:1)*Math.sin(k*r2-wt)/Math.sqrt(r2+0.3);v=(a1+a2)*0.9}
  else{const dphi=k*(r1-r2)+(inv?Math.PI:0);v=(Math.cos(dphi/2))**2*2-1}
  const p=(j*id.width+i)*4;let R,G,B;
  if(S2.mode===0){if(v>0){R=255-v*200;G=255-v*170;B=255}else{R=255;G=255+v*170;B=255+v*200}}
  else{const u=(v+1)/2;R=255-u*215;G=255-u*190;B=255-u*60}
  id.data[p]=R;id.data[p+1]=G;id.data[p+2]=B;id.data[p+3]=255}
 const off=document.createElement('canvas');off.width=id.width;off.height=id.height;off.getContext('2d').putImageData(id,0,0);
 ctx.imageSmoothingEnabled=true;ctx.drawImage(off,ox,oy,fw,fh);
 const S1y=s1.y-170,S2y=s2.y-170;
 [[s1.x,S1y,'S₁'],[s2.x,S2y,'S₂']].forEach(q=>{ctx.fillStyle='#334155';ctx.fillRect(q[0]-14,q[1]-12,18,24);txt(q[2],q[0]-26,q[1],{b:1,s:13})});
 // probe
 const r1=Math.hypot(S2.px-s1.x,S2.py-S1y)/m2px,r2=Math.hypot(S2.px-s2.x,S2.py-S2y)/m2px,dp=Math.abs(r1-r2),n=dp/(lam/2);
 ln(s1.x,S1y,S2.px,S2.py,BL,1.5,[5,4]);ln(s2.x,S2y,S2.px,S2.py,RD,1.5,[5,4]);dot(S2.px,S2.py,7,'#facc15');ctx.strokeStyle=INK;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(S2.px,S2.py,7,0,7);ctx.stroke();txt('P',S2.px+14,S2.py-12,{b:1,s:15});
 const near=Math.round(n),even=near%2===0,clean=Math.abs(n-near)<0.15;let kind=clean?((even!==inv)?'보강 간섭 (소리 큼)':'상쇄 간섭 (소리 작음)'):'보강과 상쇄의 중간';
 // walk line graph
 const gy=440,gx0=ox,gx1=ox+fw;ln(gx0,gy,gx1,gy,'#cbd5e1',1);
 ctx.beginPath();ctx.strokeStyle=PU;ctx.lineWidth=2;for(let X=gx0;X<=gx1;X+=3){const a=Math.hypot(X-s1.x,S2.py-S1y)/m2px,b=Math.hypot(X-s2.x,S2.py-S2y)/m2px;const I=(Math.cos((k*(a-b)+(inv?Math.PI:0))/2))**2;const y=gy-I*70;X===gx0?ctx.moveTo(X,y):ctx.lineTo(X,y)}ctx.stroke();
 txt('P를 지나는 가로줄을 따라 걸을 때 소리의 세기',gx0,gy-82+4,{a:'left',s:12,b:1,c:PU});ln(S2.px,gy-75,S2.px,gy,'#facc15',2);
 ctx.fillStyle='rgba(255,255,255,0.92)';ctx.fillRect(700,26,290,96);
 txt('S₁P = '+r1.toFixed(2)+' m,  S₂P = '+r2.toFixed(2)+' m',710,44,{a:'left',s:13});
 txt('경로차 = '+dp.toFixed(2)+' m = 반 파장의 '+n.toFixed(1)+'배',710,68,{a:'left',s:13,b:1});
 txt(kind,710,96,{a:'left',s:15,b:1,c:kind.startsWith('보강')?BL:(kind.startsWith('상쇄')?RD:SUB)});
 $('step').innerHTML=(S2.mode===0?'<b style="color:#2563eb">파란색 = 마루</b>, <b style="color:#e11d48">빨간색 = 골</b>입니다. 마루끼리·골끼리 만나는 줄은 진하게 출렁이고(보강), 마루와 골이 만나는 줄은 거의 흰색입니다(상쇄). ':'진한 곳일수록 소리가 큽니다. 흰 줄(소리 작음)이 상쇄 간섭 지점입니다. ')+'아래 그래프처럼 스피커 앞을 걸으면 소리가 <b>커졌다 작아졌다</b>를 반복합니다.'+(inv?' (지금은 S₂ 위상이 반대라 조건이 서로 바뀌었습니다.)':'');}
cv.addEventListener('click',e=>{if(tab!==2)return;const r=cv.getBoundingClientRect();const x=(e.clientX-r.left)*W/r.width,y=(e.clientY-r.top)*H/r.height;if(x>130&&x<980&&y>20&&y<340){S2.px=x;S2.py=y}});
$('m2a').onclick=()=>{S2.mode=0;$('m2a').classList.add('on');$('m2b').classList.remove('on')};$('m2b').onclick=()=>{S2.mode=1;$('m2b').classList.add('on');$('m2a').classList.remove('on')};
// ===== tab3 ANC
const S3={irr:false,snd:false};let AC=null,osc=null,gn=null;
function noise(t){return S3.irr?(0.6*Math.sin(2*Math.PI*1.0*t)+0.35*Math.sin(2*Math.PI*2.7*t+1)+0.25*Math.sin(2*Math.PI*4.3*t+2)):Math.sin(2*Math.PI*1.0*t)}
function scene3(dt){clear();const on=$('anc').checked,a=+$('a3').value,ph=+$('p3').value*Math.PI/180;$('va3').textContent=a.toFixed(2)+' × 소음';$('vp3').textContent=$('p3').value+'°';
 const pxs=0.004,A=60;
 const n=x=>A*noise(T-x*pxs);
 const anti=x=>on?(S3.irr?-A*a*noise(T-x*pxs-0.12):A*a*Math.sin(2*Math.PI*(T-x*pxs)+ph)):0;
 [[95,'외부 소음 (마이크가 감지)',n,SUB],[215,'이어폰이 만든 소리',anti,RD],[355,'귀에 들리는 소리 (합성파)',x=>n(x)+anti(x),BL]].forEach(r=>{ln(160,r[0],960,r[0],'#e2e8f0',1);txt(r[1],20,r[0]-60,{a:'left',b:1,s:13,c:r[3]});plot(r[2],160,960,r[0],r[3],r[3]===BL?3:2.2)});
 let s=0,s0=0;for(let x=0;x<400;x++){const v=n(x)+anti(x);s+=v*v;s0+=n(x)**2}const ratio=Math.sqrt(s/s0);
 txt('남은 소음의 크기: 원래의 '+Math.round(ratio*100)+'%',W-30,445,{a:'right',b:1,s:17,c:ratio<0.2?GN:(ratio<0.7?OR:RD)});
 if(S3.snd&&osc)gn.gain.setTargetAtTime(0.08*Math.min(1.5,ratio),AC.currentTime,0.05);
 $('step').innerHTML=S3.irr?'<b>불규칙한 소음</b>은 모양이 계속 바뀌어, 감지한 뒤 반대 소리를 만드는 사이(지연)에 이미 소음이 달라집니다. 그래서 완전히 지우기 어렵습니다.':(!on?'소음 제거를 끄면 소음이 그대로 들립니다.':(Math.abs(+$('p3').value-180)<1&&Math.abs(a-1)<0.01?'진동수가 같고 <b>진폭이 같고 위상이 반대</b>인 소리를 더해 소음이 거의 사라졌습니다 → <b>상쇄 간섭</b>':'진폭과 위상차를 바꾸어 보세요. <b>진폭 1배, 위상차 180°</b>일 때 소음이 가장 많이 줄어듭니다.'));}
$('noise3').onclick=()=>{S3.irr=!S3.irr;$('noise3').textContent=S3.irr?'소음: 불규칙':'소음: 규칙적'};
$('snd3').onclick=()=>{S3.snd=!S3.snd;if(S3.snd){if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();osc=AC.createOscillator();gn=AC.createGain();osc.frequency.value=220;osc.type='sawtooth';gn.gain.value=0.05;osc.connect(gn).connect(AC.destination);osc.start()}else if(osc){osc.stop();osc=null}$('snd3').textContent=S3.snd?'🔇 소리 끄기':'🔊 귀에 들리는 소리'};
// ===== tab4 muffler
function scene4(dt){clear();const dl=+$('l4').value,f=+$('f4').value,lam=VS/f,ph=2*Math.PI*dl/lam;$('vl4').textContent=dl.toFixed(2)+' m';$('vf4').textContent=f+' Hz (λ='+lam.toFixed(2)+' m)';
 // tube drawing
 ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.strokeRect(30,90,90,36);ctx.strokeRect(880,90,90,36);
 ctx.beginPath();ctx.moveTo(120,90);ctx.lineTo(180,40);ctx.lineTo(820,40);ctx.lineTo(880,90);ctx.stroke();
 ctx.beginPath();ctx.moveTo(120,126);ctx.lineTo(180,176);ctx.lineTo(820,176);ctx.lineTo(880,126);ctx.stroke();
 txt('통로 1',500,28,{s:12,b:1});txt('통로 2 (통로 1보다 '+dl.toFixed(2)+' m 더 김)',500,192,{s:12,b:1});
 const k=2*Math.PI/220,wt=2*Math.PI*T*0.6;plot(x=>10*Math.sin(k*x-wt),180,820,58,BL,2);plot(x=>10*Math.sin(k*x-wt-ph*(x-180)/640),180,820,158,RD,2);
 txt('엔진 소음',75,140,{s:12});txt('배출',925,140,{s:12});
 // output waves
 const y1=w=>34*Math.sin(w),y2=w=>34*Math.sin(w-ph);
 [[255,'통로 1을 지난 소리',x=>y1(x/40-wt),BL],[320,'통로 2를 지난 소리',x=>y2(x/40-wt),RD],[395,'출구에서 합쳐진 소리',x=>y1(x/40-wt)+y2(x/40-wt),PU]].forEach(r=>{ln(200,r[0],560,r[0],'#e2e8f0',1);txt(r[1],30,r[0],{a:'left',s:12,b:1,c:r[3]});plot(r[2],200,560,r[0],r[3],2)});
 const amp=Math.abs(Math.cos(ph/2));
 // comb graph
 const gx0=620,gx1=970,gy0=240,gy1=420;ln(gx0,gy1,gx1,gy1,INK,1.2);ln(gx0,gy0,gx0,gy1,INK,1.2);txt('진동수(Hz)',gx1,gy1+14,{a:'right',s:11});txt('남는 소리의 세기',gx0+4,gy0-10,{a:'left',s:11});
 ctx.beginPath();ctx.strokeStyle=PU;ctx.lineWidth=2;for(let F=50;F<=700;F+=2){const a=Math.abs(Math.cos(Math.PI*dl*F/VS));const x=gx0+(F-50)/650*(gx1-gx0),y=gy1-a*(gy1-gy0-10);F===50?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke();
 const xf=gx0+(f-50)/650*(gx1-gx0);dot(xf,gy1-amp*(gy1-gy0-10),6,OR);
 txt('길이 차 = 반 파장의 '+(dl/(lam/2)).toFixed(2)+'배 → 남는 소리 '+Math.round(amp*100)+'%',W-30,448,{a:'right',b:1,s:16,c:amp<0.15?GN:(amp>0.85?RD:OR)});
 $('step').innerHTML='길이 차가 <b>반 파장의 홀수 배</b>이면 두 소리가 반대 위상으로 만나 상쇄됩니다(170 Hz, 길이 차 1 m). 오른쪽 그래프처럼 <b>특정 진동수만</b> 크게 줄어들고, 반 파장의 짝수 배가 되는 진동수(예: 340 Hz)는 오히려 보강됩니다.';}
document.querySelectorAll('[data-f4]').forEach(b=>b.onclick=()=>{$('f4').value=b.dataset.f4});
function go(i){tab=i;[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));for(let k=0;k<5;k++)$('c'+k).classList.toggle('show',k===i);
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];if(S3.snd&&i!==3)$('snd3').click();T=0;S0.t=0}
function frame(now){const dt=Math.min(0.05,(now-last)/1000)*speed;last=now;if(!paused)T+=dt;[scene0,scene1,scene2,scene3,scene4][tab](paused?0:dt);requestAnimationFrame(frame)}
go(0);requestAnimationFrame(frame);
</script></body></html>"""


if __name__ == "__main__":
    run_sim()

