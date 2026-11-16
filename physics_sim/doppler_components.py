import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """도플러 효과와 속도 측정(3차시) — 학습지 B~D 순서의 탭형 시뮬레이션.
    ① 파면으로 보는 파장 변화(단계별) → ② 관찰자가 움직일 때(두 줄 비교) → ③ 4가지 경우 비교·관계식
    → ④ 구급차의 속력 측정(f′–t 그래프·소리) → ⑤ 스피드건·청색/적색 편이
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS로 동작(소리는 브라우저 Web Audio).
    """
    st.title("🚑 도플러 효과와 속도 측정")
    components.html(HTML, height=900, scrolling=True)


HTML = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<style>
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
<h1>🚑 도플러 효과와 속도 측정</h1>
<p class="lead">3차시 학습지 B~D 순서의 시뮬레이션입니다. 화면 속 소리의 속력은 실제보다 매우 느리게 나타냈고, 숫자는 실제 값(소리의 속력 340 m/s)으로 계산합니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="rs">↺ 처음부터</button></div>
<div class="tabs" id="tabs"></div>

<div id="c0" class="ctrl view">
 <button class="btn go" id="nx">다음 단계 ▶</button><button class="btn" id="auto">연속 재생</button>
 <div class="grp">파원의 속력 <i>v</i><sub>s</sub><input type="range" id="r0" min="0" max="0.7" step="0.05" value="0.3"><span class="val" id="v0"></span></div>
 <label class="grp"><input type="checkbox" id="ghost" checked> 정지한 파원의 파면(회색)</label>
 <button class="btn" id="snd0">🔊 A·B가 듣는 소리</button>
</div>
<div id="c1" class="ctrl view">
 <div class="grp">관찰자 2의 속력 <i>v</i><sub>o</sub><input type="range" id="r1" min="0" max="0.8" step="0.05" value="0.5"><span class="val" id="v1"></span></div>
 <button class="btn" id="cnt1">↺ 파면 세기 다시 시작</button>
</div>
<div id="c2" class="ctrl view">
 <div class="grp">파원 <i>v</i><sub>s</sub><input type="range" id="rs2" min="-0.6" max="0.6" step="0.05" value="0.3"><span class="val" id="vs2"></span></div>
 <div class="grp">관찰자 <i>v</i><sub>o</sub><input type="range" id="ro2" min="-0.6" max="0.6" step="0.05" value="0"><span class="val" id="vo2"></span></div>
 <button class="btn" data-case="0">파원이 다가옴</button><button class="btn" data-case="1">파원이 멀어짐</button><button class="btn" data-case="2">관찰자가 다가감</button><button class="btn" data-case="3">관찰자가 멀어짐</button><button class="btn" data-case="4">같은 속도로 함께</button>
</div>
<div id="c3" class="ctrl view">
 <div class="grp">구급차 속력<input type="range" id="r3" min="5" max="60" step="1" value="20"><span class="val" id="v3"></span></div>
 <div class="grp">사이렌 진동수<input type="range" id="f3" min="300" max="900" step="10" value="480"><span class="val" id="vf3"></span></div>
 <button class="btn go" id="go3">▶ 구급차 출발</button><button class="btn" id="snd3">🔊 소리 켜기</button>
</div>
<div id="c4" class="ctrl view">
 <button class="btn on" id="m4a">스피드건</button><button class="btn" id="m4b">별빛의 편이</button>
 <span id="g4" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><button class="btn on" data-st="1">1단계: 스피드건 → 자동차</button><button class="btn" data-st="2">2단계: 자동차 → 스피드건</button><button class="btn" data-st="3">3단계: 합쳐 보기</button><span class="grp">자동차 속력<input type="range" id="r4" min="0" max="60" step="5" value="30"><span class="val" id="v4"></span></span></span>
</div>

<div class="card"><canvas id="cv" width="1000" height="460"></canvas></div>
<div class="step" id="step"></div>
<div class="note" id="note"></div>
</div>
<script>
const $=id=>document.getElementById(id), cv=$('cv'), ctx=cv.getContext('2d'), W=1000, H=460;
const BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',INK='#0f172a',SUB='#64748b',OR='#ea580c';
const VS=340;
const TABS=[['① 파면으로 보는 파장 변화','B','파원이 한 주기 T 동안 v<sub>s</sub>T만큼 움직이는 사이 앞의 파면은 vT만큼 진행합니다. 그래서 앞쪽 파장은 (v−v<sub>s</sub>)T로 짧아지고 뒤쪽은 (v+v<sub>s</sub>)T로 길어집니다.'],
 ['② 관찰자가 움직일 때','C①~⑤','파면 사이의 거리(파장)는 그대로입니다. 다가가는 관찰자에게는 소리가 v+v<sub>o</sub>의 속력으로 다가와 1초 동안 만나는 파면의 수가 많아집니다.'],
 ['③ 4가지 경우 비교·관계식','C⑥·알아두기','파원이 움직이면 파장이, 관찰자가 움직이면 관찰자가 측정하는 소리의 속력이 달라집니다. 같은 속도로 함께 움직이면 진동수는 변하지 않습니다.'],
 ['④ 구급차의 속력 측정','D①②','다가올 때와 멀어질 때 측정한 진동수로 구급차의 속력을 거꾸로 구할 수 있습니다.'],
 ['⑤ 스피드건·청색/적색 편이','D③④','반사파의 진동수 변화로 속력을 재고(스피드건), 별빛의 파장 변화로 별의 운동을 압니다(청색·적색 편이).']];
let tab=0,paused=false,speed=0.5,last=performance.now();
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};
$('rs').onclick=()=>reset();
// ---------- draw helpers
function txt(s,x,y,o){o=o||{};ctx.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Malgun Gothic",sans-serif';ctx.fillStyle=o.c||INK;ctx.textAlign=o.a||'center';ctx.textBaseline='middle';ctx.fillText(s,x,y)}
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function head(x,y,dx,dy,c,s){s=s||9;const a=Math.atan2(dy,dx);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x,y);ctx.lineTo(x-s*Math.cos(a-0.4),y-s*Math.sin(a-0.4));ctx.lineTo(x-s*Math.cos(a+0.4),y-s*Math.sin(a+0.4));ctx.fill()}
function arr(x0,y0,x1,y1,c,w){ln(x0,y0,x1,y1,c,w||2.5);head(x1,y1,x1-x0,y1-y0,c)}
function dbl(x0,y0,x1,y1,c){if(Math.abs(x1-x0)<2)return;ln(x0,y0,x1,y1,c,2);head(x1,y1,x1-x0,y1-y0,c,7);head(x0,y0,x0-x1,y0-y1,c,7)}
function dot(x,y,r,c){ctx.beginPath();ctx.fillStyle=c;ctx.arc(x,y,r,0,7);ctx.fill()}
function person(x,y,c){c=c||INK;ctx.strokeStyle=c;ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y-34,7,0,7);ctx.stroke();ln(x,y-27,x,y-10,c,2);ln(x-9,y,x,y-10,c,2);ln(x+9,y,x,y-10,c,2);ln(x-10,y-21,x+10,y-21,c,2)}
function clear(){ctx.clearRect(0,0,W,H)}
function f1(x,d){return x.toFixed(d==null?0:d)}
// ---------- audio
let AC=null,osc=null,gain=null;
function tone(on){if(on){if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();if(!osc){osc=AC.createOscillator();gain=AC.createGain();gain.gain.value=0.06;osc.type='triangle';osc.connect(gain).connect(AC.destination);osc.start()}}else if(osc){osc.stop();osc=null}}
function setF(f){if(osc)osc.frequency.setTargetAtTime(f,AC.currentTime,0.03)}
// =============== TAB 0 : step-by-step wavefronts
const T0={t:0,target:0,auto:false,r:0.3,ghost:true};
const V0=78; // px per T (wavelength when still)
function step0Text(k,r){
 const vsT=f1(r*V0/V0,2);
 if(k<0.01) return '<b>0단계</b> · 파원(●)이 S<sub>0</sub>에 있습니다. <b>다음 단계 ▶</b>를 누르면 한 주기 <i>T</i>씩 시간이 흐릅니다.';
 if(k<1.01) return '<b>1단계 (t = T)</b> · S<sub>0</sub>에서 나온 첫 파면은 반지름 <b>vT = λ</b>만큼 퍼졌습니다. 그동안 파원은 오른쪽으로 <b style="color:#e11d48">v<sub>s</sub>T</b>만큼 움직여 S<sub>1</sub>에서 두 번째 파면을 냅니다.';
 if(k<2.01) return '<b>2단계 (t = 2T)</b> · 두 파면 사이 간격을 보세요. 앞쪽(A 쪽)은 <b style="color:#059669">vT − v<sub>s</sub>T</b>로 좁고, 뒤쪽(B 쪽)은 <b style="color:#ea580c">vT + v<sub>s</sub>T</b>로 넓습니다.';
 if(k<3.01) return '<b>3단계</b> · 매 주기 같은 일이 반복되므로 앞쪽 간격은 계속 일정하게 좁고 뒤쪽 간격은 일정하게 넓습니다. 소리의 속력 <i>v</i>는 그대로입니다.';
 return '<b>4단계 이후</b> · A에게는 짧은 파장 λ<sub>A</sub> = (v − v<sub>s</sub>)T 의 소리가 같은 속력 v로 오므로 <b>f′ = v/λ<sub>A</sub> = f·v/(v − v<sub>s</sub>)</b> → 높은 소리. B는 반대로 낮은 소리를 듣습니다.';
}
function scene0(dt){
 if(!paused){ if(T0.auto){T0.t+=dt*0.9;T0.target=T0.t;if(T0.t>9){T0.t=0;T0.target=0}} else if(T0.t<T0.target){T0.t=Math.min(T0.target,T0.t+dt*0.8)} }
 clear();const r=T0.r,t=T0.t,cy=215,x0=300,vs=r*V0;
 ln(20,cy,W-20,cy,'#e2e8f0',1);
 const N=Math.floor(t+1e-6);
 if(T0.ghost){for(let n=0;n<=N;n++){const R=V0*(t-n);if(R>0){ctx.beginPath();ctx.setLineDash([4,5]);ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.3;ctx.arc(x0,cy,R,0,7);ctx.stroke();ctx.setLineDash([])}}}
 for(let n=0;n<=N;n++){const xs=x0+vs*n,R=V0*(t-n);if(R>0.5){ctx.beginPath();ctx.strokeStyle=n===N-1?'#1d4ed8':'#60a5fa';ctx.lineWidth=n>=N-1?2.6:1.8;ctx.arc(xs,cy,R,0,7);ctx.stroke()}
  dot(xs,cy,3.5,'#94a3b8');txt('S'+n,xs,cy+16,{s:11,c:SUB})}
 const xsNow=x0+vs*t;dot(xsNow,cy,9,RD);
 if(vs>0)arr(xsNow+12,cy-16,xsNow+12+Math.max(18,vs*0.9),cy-16,RD,2);
 // annotations for latest pair
 if(N>=1){const a=N-1,b=N; const xa=x0+vs*a,xb=x0+vs*b,Ra=V0*(t-a),Rb=V0*(t-b);
  const fa=xa+Ra,fb=xb+Rb,ba=xa-Ra,bb=xb-Rb;
  const yA=cy+95; ln(fa,cy,fa,yA+8,GN,1,[3,3]);ln(fb,cy,fb,yA+8,GN,1,[3,3]);dbl(fb,yA,fa,yA,GN);txt('A 쪽 파장',(fa+fb)/2,yA+17,{c:GN,b:1,s:13});
  ln(ba,cy,ba,yA+8,OR,1,[3,3]);ln(bb,cy,bb,yA+8,OR,1,[3,3]);dbl(ba,yA,bb,yA,OR);txt('B 쪽 파장',(ba+bb)/2,yA+17,{c:OR,b:1,s:13});
  if(t-N<0.05||!T0.auto){ // show vT and vsT at the step moment
   const yv=Math.max(16,cy-Ra-12); ln(xa,cy,xa,yv,BL,1,[2,3]);dbl(xa,yv,xa+V0,yv,BL);txt('vT (파면이 진행한 거리)',xa+V0/2,yv-12,{c:BL,b:1,s:13});
   if(vs>2){dbl(xa,cy+38,xb,cy+38,RD);txt('vₛT (파원이 이동한 거리)',(xa+xb)/2,cy+54,{c:RD,b:1,s:13})}}
 }
 person(W-40,cy+40,GN);txt('A',W-40,cy+56,{b:1,c:GN});person(40,cy+40,OR);txt('B',40,cy+56,{b:1,c:OR});
 // bars
 const by=405,sc=1.6,lam=V0,la=(V0-vs),lb=(V0+vs),f=480,vsr=r*VS;
 txt('파장 비교',60,by-28,{b:1,s:13,a:'left'});
 [['B 쪽 파장',lb,OR],['정지했을 때',lam,'#94a3b8'],['A 쪽 파장',la,GN]].forEach((q,i)=>{const y=by-10+i*20;txt(q[0],60,y,{s:12,a:'left',c:q[2],b:1});ctx.fillStyle=q[2];ctx.fillRect(150,y-6,q[1]*sc,12)});
 txt('f = 480 Hz일 때  A가 듣는 진동수 f′ = '+f1(f*VS/(VS-vsr))+' Hz,   B가 듣는 진동수 = '+f1(f*VS/(VS+vsr))+' Hz',W-20,by+10,{a:'right',s:14,b:1});
 txt('vₛ = '+f1(vsr)+' m/s  ( vₛ/v = '+r.toFixed(2)+' )',W-20,by-18,{a:'right',s:13,c:SUB});
 $('step').innerHTML=step0Text(Math.min(t,T0.target+0.0001),r);
 if(snd0on){const k=Math.floor(performance.now()/900)%2;setF(k?f*VS/(VS+vsr):f*VS/(VS-vsr));$('snd0').textContent=(k?'🔊 B가 듣는 소리 (낮음)':'🔊 A가 듣는 소리 (높음)')}
}
$('nx').onclick=()=>{T0.auto=false;$('auto').classList.remove('on');if(T0.target>=5){T0.t=0;T0.target=0}else T0.target=Math.floor(T0.target+1e-6)+1};
$('auto').onclick=()=>{T0.auto=!T0.auto;$('auto').classList.toggle('on',T0.auto)};
$('r0').oninput=e=>{T0.r=+e.target.value;$('v0').textContent=f1(T0.r*VS)+' m/s'};
$('ghost').onchange=e=>T0.ghost=e.target.checked;
let snd0on=false;$('snd0').onclick=()=>{snd0on=!snd0on;tone(snd0on);if(!snd0on)$('snd0').textContent='🔊 A·B가 듣는 소리'};
// =============== TAB 1 : two lanes, observer moving
const T1={t:0,r:0.5,c1:0,c2:0,t0:0,x2:0,prev1:null,prev2:null};
const LV=90,LT=1.0; // px/s speed, period s  -> lambda 90px
function scene1(dt){
 if(!paused){T1.t+=dt*0.9}
 const t=T1.t; clear();
 const sx=60,lanes=[150,320];
 const lam=LV*LT, vo=T1.r*LV;
 // observer 2 position
 if(T1.x2===0)T1.x2=930; if(!paused)T1.x2-=vo*dt*0.9; if(T1.x2<380){T1.x2=930;T1.c1=0;T1.c2=0;T1.prev1=null;T1.prev2=null;T1.t0=t}
 const x1=930,x2=T1.x2;
 lanes.forEach((y,k)=>{ctx.fillStyle=k?'#faf5ff':'#f8fafc';ctx.fillRect(20,y-55,W-40,110);
  // wavefronts as vertical lines from source
  const nmax=Math.floor(t/LT);for(let n=nmax;n>=0;n--){const x=sx+LV*(t-n*LT);if(x>W-20)break;ln(x,y-48,x,y+48,BL,2.2)}
  dot(sx,y,10,RD);txt('파원(정지)',sx,y+66,{s:12,c:SUB});
  // ruler
  for(let i=0;i<10;i++){const x=sx+20+i*lam;}
 });
 // count crossings
 const crossCount=(x,tt)=>Math.floor((tt-(x-sx)/LV)/LT); // fronts that passed static x
 const c1=crossCount(x1,t);
 if(T1.prev1===null)T1.prev1=c1; if(c1>T1.prev1){T1.c1+=c1-T1.prev1;T1.prev1=c1}
 // moving observer: front n position xn=sx+LV(t-nT); passes when xn>=x2
 const c2=Math.floor((t-(x2-sx)/LV)/LT); if(T1.prev2===null)T1.prev2=c2; if(c2>T1.prev2){T1.c2+=c2-T1.prev2;T1.prev2=c2}
 person(x1,lanes[0]+38,INK);txt('관찰자 1 (정지)',x1,lanes[0]-44+100,{s:12,b:1});
 person(x2,lanes[1]+38,PU);arr(x2-14,lanes[1]-40,x2-14-Math.max(14,vo*0.6),lanes[1]-40,PU,2);txt('관찰자 2 (v_o로 다가감)',x2,lanes[1]+56,{s:12,b:1,c:PU});
 // spacing labels (same)
 lanes.forEach(y=>{const n=Math.floor(t/LT)-2;const xa=sx+LV*(t-n*LT),xb=xa+lam;if(xb<380){} const k=Math.floor(t/LT);const xL=sx+LV*(t-(k-1)*LT),xR=sx+LV*(t-(k-2)*LT);if(xR<W-40){dbl(xL,y-62+8,xR,y-62+8,GN);txt('λ (같음)',(xL+xR)/2,y-62-4,{c:GN,b:1,s:12})}});
 const el=Math.max(0.01,t-T1.t0);
 txt('만난 파면 수:  관찰자 1 = '+T1.c1+'개,   관찰자 2 = '+T1.c2+'개   (같은 시간 동안)',W/2,415,{b:1,s:16});
 txt('관찰자 2가 측정하는 소리의 속력 = v + v_o = '+f1(VS)+' + '+f1(T1.r*VS)+' = '+f1(VS*(1+T1.r))+' m/s  →  f′ = f(v+v_o)/v = '+(1+T1.r).toFixed(2)+'f',W/2,442,{s:14,c:PU,b:1});
 $('step').innerHTML='두 줄의 <b>파면 간격(파장)은 똑같습니다.</b> 그런데 파원 쪽으로 다가가는 관찰자 2는 파면을 마중 나가므로 같은 시간 동안 <b>더 많은 파면</b>을 만납니다. → 진동수가 커집니다. (소리가 관찰자 2에게 다가오는 속력 = v + v<sub>o</sub>)';
}
$('r1').oninput=e=>{T1.r=+e.target.value;$('v1').textContent=f1(T1.r*VS)+' m/s';T1.c1=0;T1.c2=0;T1.x2=930;T1.prev1=null;T1.prev2=null;T1.t0=T1.t};
$('cnt1').onclick=()=>{T1.c1=0;T1.c2=0;T1.x2=930;T1.prev1=null;T1.prev2=null;T1.t0=T1.t};
// =============== TAB 2 : general lane (source & observer)
const T2={t:0,s:0.3,o:0,xs:0,xo:0,em:[],last:0,hits:[],c:0};
function reset2(){T2.t=0;T2.xs=200;T2.xo=820;T2.em=[];T2.last=-1;T2.hits=[]}
function scene2(dt){
 const vs=T2.s*LV,vo=T2.o*LV; // +: source moves right (toward observer), observer + = moves left (toward source)
 if(!paused){const d=dt*0.9;T2.t+=d;T2.xs+=vs*d;T2.xo-=vo*d;
  const n=Math.floor(T2.t/LT);if(n>T2.last){T2.last=n;T2.em.push({x:T2.xs,t:T2.t})}
  T2.em.forEach(e=>{const x=e.x+LV*(T2.t-e.t);if(!e.hit&&x>=T2.xo){e.hit=1;T2.hits.push(T2.t)}});
  T2.em=T2.em.filter(e=>e.x+LV*(T2.t-e.t)<W+20);T2.hits=T2.hits.filter(h=>T2.t-h<6);
  if(T2.xs>T2.xo-60||T2.xs<40||T2.xo>W-30||T2.xo<T2.xs+60)reset2();}
 clear();const y=190;
 ctx.fillStyle='#f8fafc';ctx.fillRect(20,y-80,W-40,160);
 T2.em.forEach(e=>{const x=e.x+LV*(T2.t-e.t);if(x<=T2.xo+2)ln(x,y-70,x,y+70,BL,2.2)});
 dot(T2.xs,y,11,RD);if(Math.abs(vs)>1)arr(T2.xs,y-26,T2.xs+Math.sign(vs)*Math.max(16,Math.abs(vs)*0.6),y-26,RD,2);txt('파원',T2.xs,y+90,{s:12,b:1,c:RD});
 person(T2.xo,y+40,PU);if(Math.abs(vo)>1)arr(T2.xo,y-52,T2.xo-Math.sign(vo)*Math.max(16,Math.abs(vo)*0.6),y-52,PU,2);txt('관찰자',T2.xo,y+90,{s:12,b:1,c:PU});
 // measured spacing between last two fronts
 const xs_=T2.em.map(e=>e.x+LV*(T2.t-e.t)).filter(x=>x<=T2.xo).sort((a,b)=>a-b);
 if(xs_.length>=2){const a=xs_[xs_.length-2],b=xs_[xs_.length-1];dbl(a,y-92+8,b,y-92+8,GN);txt('파장',(a+b)/2,y-96,{c:GN,b:1,s:12})}
 const v=VS,vsr=T2.s*VS,vor=T2.o*VS,lamR=(1-T2.s),vrel=(1+T2.o),fr=vrel/lamR;
 const sg=x=>x>0?'커짐':(x<0?'작아짐':'그대로');
 // table
 const rows=[['관찰자가 측정하는 소리의 속력',f1(v+vor)+' m/s',sg(T2.o)],['파장 (정지일 때 1.00λ)',lamR.toFixed(2)+'λ',T2.s>0?'짧아짐':(T2.s<0?'길어짐':'그대로')],['진동수 (f = 480 Hz)',f1(480*fr)+' Hz',sg(fr-1>1e-9?1:(fr-1<-1e-9?-1:0))]];
 rows.forEach((r,i)=>{const yy=318+i*30;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(60,yy-14,880,28);txt(r[0],80,yy,{a:'left',s:14,b:1});txt(r[1],620,yy,{s:15,b:1,c:BL});txt(r[2],820,yy,{s:15,b:1,c:r[2]==='그대로'?SUB:(r[2]==='커짐'?GN:OR)})});
 txt("f′ = f (v ± v_o) / (v ∓ v_s) = 480 × ("+f1(v)+(vor>=0?' + ':' − ')+f1(Math.abs(vor))+") / ("+f1(v)+(vsr>=0?' − ':' + ')+f1(Math.abs(vsr))+") = "+f1(480*VS*(1+T2.o)/(VS*(1-T2.s)))+' Hz',W/2,420,{b:1,s:15});
 let msg='오른쪽 슬라이더는 <b>다가가는 쪽이 +</b>입니다. ';
 if(Math.abs(T2.s-(-T2.o))<1e-9&&T2.s!==0)msg+='<b>파원과 관찰자가 같은 속도로 함께 움직입니다.</b> 파장은 달라지지만 관찰자가 측정하는 속력도 같은 비율로 달라져 <b>진동수는 그대로</b>입니다(상대적인 운동이 없음).';
 else if(T2.s!==0&&T2.o!==0)msg+='파원과 관찰자가 <b>모두 움직이므로</b> 분모(파원)와 분자(관찰자)를 함께 넣어 계산합니다.';
 else if(T2.s!==0)msg+='파원이 움직이면 <b>파장</b>이 달라지고, 관찰자가 측정하는 소리의 속력은 그대로입니다.';
 else if(T2.o!==0)msg+='관찰자가 움직이면 파장은 그대로이고 <b>관찰자가 측정하는 소리의 속력</b>이 달라집니다.';
 else msg+='둘 다 정지하면 도플러 효과가 없습니다.';
 $('step').innerHTML=msg;
}
function set2(s,o){T2.s=s;T2.o=o;$('rs2').value=s;$('ro2').value=o;sync2();reset2()}
function sync2(){$('vs2').textContent=(T2.s>0?'다가감 ':T2.s<0?'멀어짐 ':'')+f1(Math.abs(T2.s*VS))+' m/s';$('vo2').textContent=(T2.o>0?'다가감 ':T2.o<0?'멀어짐 ':'')+f1(Math.abs(T2.o*VS))+' m/s'}
$('rs2').oninput=e=>{T2.s=+e.target.value;sync2();reset2()};$('ro2').oninput=e=>{T2.o=+e.target.value;sync2();reset2()};
document.querySelectorAll('[data-case]').forEach(b=>b.onclick=()=>{const c=+b.dataset.case;[[0.3,0],[-0.3,0],[0,0.3],[0,-0.3],[0.3,-0.3]].forEach((q,i)=>{if(i===c)set2(q[0],q[1])});document.querySelectorAll('[data-case]').forEach(x=>x.classList.toggle('on',x===b))});
// =============== TAB 3 : ambulance passing
const T3={t:0,run:false,hist:[],snd:false};
function scene3(dt){
 const vsr=+$('r3').value,f=+$('f3').value;const road=150,obsX=500,obsY=road+70;
 const pxm=6; // px per m (scene length ~ 150 m)
 if(T3.run&&!paused){T3.t+=dt*1.0;if(T3.t*vsr*pxm>W+80){T3.run=false}}
 clear();
 ctx.fillStyle='#e5e7eb';ctx.fillRect(0,road-26,W,52);ln(0,road,W,road,'#fff',2,[18,14]);
 const xa=-80+T3.t*vsr*pxm;
 // ambulance
 ctx.fillStyle='#fff';ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.fillRect(xa-40,road-22,80,32);ctx.strokeRect(xa-40,road-22,80,32);ctx.fillStyle=RD;ctx.fillRect(xa-6,road-19,12,26);ctx.fillRect(xa-13,road-12,26,12);
 dot(xa-24,road+12,7,INK);dot(xa+24,road+12,7,INK);ctx.fillStyle=Math.floor(T3.t*6)%2?RD:BL;ctx.fillRect(xa-8,road-30,16,8);
 person(obsX,obsY,INK);txt('관찰자',obsX,obsY+16,{s:12,b:1});
 // observed frequency
 const dx=(obsX-xa)/pxm,dy=(obsY-road)/pxm/6; const cos=dx/Math.hypot(dx,dy);
 const fo=T3.t>0||T3.run?f*VS/(VS-vsr*cos):f;
 if(T3.run&&!paused)T3.hist.push([T3.t,fo]);
 if(T3.snd)setF(fo);
 // graph
 const gx0=80,gx1=940,gy0=260,gy1=430,tmax=(W+160)/(vsr*pxm),fmin=f*VS/(VS+60)-10,fmax=f*VS/(VS-60)+10;
 ln(gx0,gy1,gx1,gy1,INK,1.5);ln(gx0,gy0,gx0,gy1,INK,1.5);txt('시간',gx1,gy1+14,{s:12,a:'right'});txt('측정 진동수(Hz)',gx0+6,gy0-8,{s:12,a:'left'});
 const Y=v=>gy1-(v-fmin)/(fmax-fmin)*(gy1-gy0);
 ln(gx0,Y(f),gx1,Y(f),'#cbd5e1',1,[4,4]);txt(f+' Hz (사이렌)',gx0-6,Y(f),{s:11,a:'right',c:SUB});
 ctx.beginPath();ctx.strokeStyle=PU;ctx.lineWidth=2.5;T3.hist.forEach((p,i)=>{const x=gx0+p[0]/tmax*(gx1-gx0),y=Y(p[1]);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke();
 const fa=f*VS/(VS-vsr),fb=f*VS/(VS+vsr);
 txt('다가올 때 '+f1(fa)+' Hz',gx0+150,Y(fa)-12,{s:13,b:1,c:GN});txt('멀어질 때 '+f1(fb)+' Hz',gx1-140,Y(fb)+16,{s:13,b:1,c:OR});
 $('step').innerHTML='<b>측정값으로 속력 구하기</b> · 다가올 때 측정한 진동수 '+f1(fa)+' Hz를 식에 넣으면  '+f1(fa)+' = '+f+' × 340 / (340 − v<sub>s</sub>)  →  340 − v<sub>s</sub> = '+f1(f*VS/fa,1)+'  →  <b>v<sub>s</sub> = '+f1(VS-f*VS/fa,1)+' m/s</b> (약 '+f1((VS-f*VS/fa)*3.6)+' km/h). 지나가는 순간 진동수가 뚝 떨어지는 것을 그래프와 소리로 확인하세요.';
}
$('go3').onclick=()=>{T3.t=0;T3.hist=[];T3.run=true};
$('snd3').onclick=()=>{T3.snd=!T3.snd;tone(T3.snd);$('snd3').textContent=T3.snd?'🔇 소리 끄기':'🔊 소리 켜기'};
$('r3').oninput=()=>{$('v3').textContent=$('r3').value+' m/s'};$('f3').oninput=()=>{$('vf3').textContent=$('f3').value+' Hz'};
// =============== TAB 4 : speed gun & star
const T4={t:0,mode:0,r:30,em:[],ref:[],last:-1,cx:820,step:1};
const G4={c:230,P:0.45,gx:110};
function step4(d){const c=G4.c,P=G4.P,gx=G4.gx,vc=(0.06+T4.r/60*0.24)*c;
 T4.t+=d;T4.cx-=vc*d;if(T4.cx<470){T4.cx=820;T4.em=[];T4.ref=[];T4.last=Math.floor(T4.t/P);warm4(false)}
 const n=Math.floor(T4.t/P);if(n>T4.last){T4.last=n;T4.em.push({t:T4.t})}
 const carF=T4.cx-45;
 T4.em.forEach(e=>{const x=gx+c*(T4.t-e.t);if(!e.r&&x>=carF){e.r=1;e.hitT=T4.t;T4.ref.push({t:T4.t,x:carF})}});
 T4.em=T4.em.filter(e=>!e.r||T4.t-e.hitT<0.25);T4.ref=T4.ref.filter(e=>e.x-c*(T4.t-e.t)>gx)}
function warm4(full){const cx0=T4.cx;for(let i=0;i<140;i++)step4(0.025);T4.cx=Math.max(T4.cx,560)}
function scene4(dt){
 if(!paused&&T4.mode===1)T4.t+=dt*0.9;clear();
 if(T4.mode===0){
  const y=190,gx=110,c=G4.c,P=G4.P,st=T4.step;
  if(!paused)step4(dt*0.9);
  const carF=T4.cx-45;
  const showE=(st!==2),showR=(st!==1);
  // emitted
  T4.em.forEach(e=>{if(e.r){if(st===1)dot(carF,y-45,8,'rgba(37,99,235,'+(1-(T4.t-e.hitT)/0.25)+')');return}const x=gx+c*(T4.t-e.t);ln(x,y-75,x,y-15,showE?BL:'#dbeafe',showE?2.4:1.2)});
  T4.ref.forEach(e=>{const x=e.x-c*(T4.t-e.t);ln(x,y+15,x,y+75,showR?PU:'#ede9fe',showR?2.4:1.2)});
  // spacing labels
  if(showE){const xs=T4.em.filter(e=>!e.r).map(e=>gx+c*(T4.t-e.t)).sort((p,q)=>p-q);if(xs.length>=3){dbl(xs[0],y-88,xs[1],y-88,BL);txt('파장 λ (그대로)',(xs[0]+xs[1])/2,y-100,{c:BL,b:1,s:12})}}
  if(showR){const xs=T4.ref.map(e=>e.x-c*(T4.t-e.t)).sort((p,q)=>p-q);if(xs.length>=3){dbl(xs[0],y+88,xs[1],y+88,PU);txt('파장 λ′ (짧아짐)',(xs[0]+xs[1])/2,y+101,{c:PU,b:1,s:12})}}
  // gun & car
  person(gx-50,y+40);ctx.fillStyle='#334155';ctx.fillRect(gx-44,y-8,34,12);txt('스피드건',gx-45,y+62,{s:12,b:1});
  ctx.fillStyle='#93c5fd';ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.fillRect(carF,y-20,110,36);ctx.strokeRect(carF,y-20,110,36);dot(carF+25,y+18,9,INK);dot(carF+85,y+18,9,INK);
  arr(carF+55,y-30,carF+55-28,y-30,RD,2);txt('v',carF+64,y-30,{c:RD,b:1,s:13,a:'left'});
  // role badges
  function badge(x,yy,t1,col){ctx.font='700 13px "Malgun Gothic",sans-serif';const w=ctx.measureText(t1).width+18;ctx.fillStyle=col;ctx.beginPath();ctx.roundRect(x-w/2,yy-13,w,26,13);ctx.fill();txt(t1,x,yy,{c:'#fff',b:1,s:13})}
  if(st===1){badge(gx-45,y-62,'파원 (정지)',BL);badge(carF+55,y-62,'관찰자 (다가감)',OR)}
  else if(st===2){badge(gx-45,y-62,'관찰자 (정지)',OR);badge(carF+55,y-62,'파원 (다가옴)',PU)}
  else{badge(gx-45,y-62,'파원 → 관찰자',INK);badge(carF+55,y-62,'관찰자 → 파원',INK)}
  // formula panel
  const vr=T4.r, f=24.15e9, C=3e8, df=2*vr*f/C;
  const lines={1:['1단계 · 자동차가 "관찰자"입니다.','스피드건(파원)은 가만히 있고 자동차(관찰자)가 다가가므로, 파장은 그대로인데 자동차가 1초 동안 만나는 파면 수가 늘어납니다.','자동차가 받는 진동수   f₁ = f · (c + v) / c          ← 학습지 C: 관찰자가 다가갈 때'],
              2:['2단계 · 이번에는 자동차가 "파원"입니다.','자동차는 받은 진동수 f₁ 그대로 전자기파를 되돌려 보냅니다. 다가오는 파원이므로 앞쪽(스피드건 쪽) 파장이 짧아집니다.','스피드건이 받는 진동수   f′ = f₁ · c / (c − v)          ← 학습지 B: 파원이 다가올 때'],
              3:['3단계 · 두 번의 도플러 효과를 합칩니다.','f′ = f · (c + v)/c × c/(c − v) = f · (c + v)/(c − v)   ≈  f (1 + 2v/c)     →   Δf = f′ − f ≈ 2vf/c ,   v ≈ cΔf / (2f)','실제 값: f = 24.15 GHz, v = '+vr+' m/s → Δf ≈ '+f1(df)+' Hz   (Δf / f ≈ '+(df/f*1e7).toFixed(1)+' × 10⁻⁷)']}[st];
  txt(lines[0],60,330,{a:'left',b:1,s:16,c:st===1?OR:(st===2?PU:INK)});
  txt(lines[1],60,362,{a:'left',s:13.5});
  txt(lines[2],60,394,{a:'left',b:1,s:14.5,c:BL});
  txt('※ 그림은 차이가 보이도록 자동차 속력을 매우 크게 과장했습니다. 실제 자동차 속력은 빛의 속력의 약 1000만분의 1입니다.',60,432,{a:'left',s:12,c:SUB});
  $('step').innerHTML={1:'<b>1단계</b> · 스피드건이 쏜 전자기파를 <b>받는 쪽은 자동차</b>입니다. 그래서 이 단계에서 움직이는 <b>관찰자는 자동차</b>이고, 분자가 c + v가 됩니다. (파란 점: 자동차가 파면을 만나는 순간)',
   2:'<b>2단계</b> · 반사파를 <b>내보내는 쪽은 자동차</b>입니다. 이 단계에서는 자동차가 <b>움직이는 파원</b>이 되어 분모가 c − v가 됩니다. 보라색 반사파의 간격이 좁아진 것을 보세요.',
   3:'<b>3단계</b> · 스피드건을 든 사람은 두 단계 모두 <b>정지</b>해 있습니다. 자동차가 1단계에서는 관찰자, 2단계에서는 파원 역할을 하므로 도플러 효과가 <b>두 번</b> 일어나고, 진동수 차이는 약 <b>2v/c</b>에 비례합니다.'}[st];
 }else{
  const cx=330,cy=190,R=110,w=0.5,th=T4.t*w;const sx=cx+R*Math.cos(th),sy=cy-R*Math.sin(th);
  ctx.beginPath();ctx.setLineDash([5,5]);ctx.strokeStyle='#94a3b8';ctx.arc(cx,cy,R,0,7);ctx.stroke();ctx.setLineDash([]);dot(cx,cy,3,INK);txt('O',cx+12,cy,{s:12,b:1,c:SUB});
  [['A',cx+R+18,cy],['B',cx,cy-R-16],['C',cx-R-18,cy],['D',cx,cy+R+16]].forEach(p=>txt(p[0],p[1],p[2],{s:13,b:1,c:INK}));
  const vx=-Math.sin(th),vy=-Math.cos(th);
  arr(sx,sy,sx+vx*34,sy+vy*34,RD,2.2);
  const vrad=Math.cos(th)*-1; // + = approaching earth (earth below)
  const col=vrad>0.15?'#60a5fa':(vrad<-0.15?'#f87171':'#fde047');dot(sx,sy,14,col);
  dot(cx,410,18,'#93c5fd');txt('지구 (관측)',cx+34,410,{s:13,b:1,a:'left'});ln(cx,392,cx,cy+R+24,'#cbd5e1',1,[3,4]);
  // spectrum
  const x0=560,x1=960,yb=170;const grd=ctx.createLinearGradient(x0,0,x1,0);['#7c3aed','#2563eb','#06b6d4','#22c55e','#eab308','#f97316','#dc2626'].forEach((c,i)=>grd.addColorStop(i/6,c));
  ctx.fillStyle=grd;ctx.fillRect(x0,yb,x1-x0,46);txt('짧은 파장',x0,yb+62,{s:12,a:'left'});txt('긴 파장',x1,yb+62,{s:12,a:'right'});
  const base=(x0+x1)/2,shift=-vrad*90;ln(base,yb-14,base,yb+46+6,'#fff',1,[3,3]);ctx.fillStyle=INK;ctx.fillRect(base+shift-2,yb,4,46);
  txt('원래 위치',base,yb-24,{s:12,c:SUB});
  const lab=vrad>0.15?'청색 편이 (가까워짐 → 파장 짧아짐)':(vrad<-0.15?'적색 편이 (멀어짐 → 파장 길어짐)':'편이 거의 없음 (시선 방향 운동 없음)');
  txt(lab,(x0+x1)/2,yb+100,{s:16,b:1,c:vrad>0.15?BL:(vrad<-0.15?RD:SUB)});
  $('step').innerHTML='별이 지구 쪽으로 다가올 때는 스펙트럼의 선이 <b style="color:#2563eb">짧은 파장 쪽(청색 편이)</b>으로, 멀어질 때는 <b style="color:#e11d48">긴 파장 쪽(적색 편이)</b>으로 옮겨집니다. 지구와의 거리가 변하지 않는 방향으로 움직이는 순간에는 편이가 없습니다.';
 }
}
$('m4a').onclick=()=>{T4.mode=0;$('m4a').classList.add('on');$('m4b').classList.remove('on');$('g4').style.display='flex'};
document.querySelectorAll('[data-st]').forEach(b=>b.onclick=()=>{T4.step=+b.dataset.st;document.querySelectorAll('[data-st]').forEach(x=>x.classList.toggle('on',x===b));T4.cx=820;T4.em=[];T4.ref=[];T4.last=Math.floor(T4.t/G4.P);warm4(true)});
$('m4b').onclick=()=>{T4.mode=1;$('m4b').classList.add('on');$('m4a').classList.remove('on');$('g4').style.display='none'};
$('r4').oninput=e=>{T4.r=+e.target.value;$('v4').textContent=T4.r+' m/s'};
// ---------- tabs / loop
function reset(){T0.t=0;T0.target=0;T1.t=0;T1.x2=0;T1.c1=0;T1.c2=0;T1.prev1=null;T1.prev2=null;T1.t0=0;reset2();T3.t=0;T3.hist=[];T3.run=(tab===3);T4.t=0;T4.cx=820;T4.em=[];T4.ref=[];T4.last=-1;warm4(true)}
function go(i){tab=i;[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));for(let k=0;k<5;k++)$('c'+k).classList.toggle('show',k===i);
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];
 if(snd0on&&i!==0){snd0on=false;tone(false);$('snd0').textContent='🔊 A·B가 듣는 소리'}
 if(T3.snd&&i!==3){T3.snd=false;tone(false);$('snd3').textContent='🔊 소리 켜기'}
 reset()}
function frame(now){const dt=Math.min(0.05,(now-last)/1000)*speed;last=now;
 [scene0,scene1,scene2,scene3,scene4][tab](paused?0:dt);requestAnimationFrame(frame)}
$('v0').textContent=f1(0.3*VS)+' m/s';$('v1').textContent=f1(0.5*VS)+' m/s';sync2();$('v3').textContent='20 m/s';$('vf3').textContent='480 Hz';$('v4').textContent='30 m/s';
go(0);requestAnimationFrame(frame);
</script></body></html>
"""


if __name__ == "__main__":
    run_sim()

