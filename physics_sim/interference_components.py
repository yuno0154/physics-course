import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """음파의 간섭과 소음 제어(4차시) — 종파의 밀·소(압력·변위) + 학습지 A~C 순서의 탭형 시뮬레이션.
    ⓪ 종파의 밀·소(압력·변위) → ① 중첩의 원리 → ② 보강·상쇄 간섭(위상차) → ③ 두 스피커의 간섭(경로차, 측정점 클릭)
    → ④ 소음 제거 이어폰(진폭·위상 조절, 불규칙 소음) → ⑤ 자동차 배기 소음기(길이 차·진동수)
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS로 동작.
    """
    st.title("🔊 음파의 간섭과 소음 제어")
    components.html(HTML, height=920, scrolling=True)


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
<div id="c0" class="ctrl view">
 <div class="grp">진폭 <i>A</i><input type="range" id="la0" min="6" max="24" step="1" value="15"><span class="val" id="vla0">15</span></div>
 <div class="grp">파장 <i>λ</i><input type="range" id="lw0" min="160" max="360" step="20" value="240"><span class="val" id="vlw0">240 px</span></div>
 <label class="grp"><input type="checkbox" id="lov0" checked> 변위 그래프에 압력 점선 겹쳐 보기 (90° 위상차)</label>
 <label class="grp"><input type="checkbox" id="ltrk0" checked> 추적 입자 강조</label>
 <button class="btn" id="lpk0">📍 밀·소 순간 정지</button>
</div>
<div id="c1" class="ctrl view"><button class="btn on" id="p0a">파동 B 아래로 볼록(반대, −1칸)</button><button class="btn" id="p0b">파동 B 위로 볼록(같은 쪽, +1칸)</button><button class="btn" id="p0w">파형: 단일 곡선파</button><button class="btn" id="p0pk">📍 꼭짓점 겹침 순간 보기</button><button class="btn go" id="p0go">▶ 다시 보내기</button></div>
<div id="c2" class="ctrl view"><div class="grp">두 파동의 위상차<input type="range" id="ph1" min="0" max="360" step="15" value="0"><span class="val" id="vph1"></span></div><button class="btn" id="ph1a">같은 위상(0°)</button><button class="btn" id="ph1b">반대 위상(180°)</button></div>
<div id="c3" class="ctrl view">
 <button class="btn on" id="m2a">순간 모습(마루·골)</button><button class="btn" id="m2b">소리의 세기 분포</button>
 <button class="btn on" id="sp2both">🔊 S₁+S₂ 모두</button><button class="btn" id="sp2one">🔈 S₁ 1개만</button>
 <div class="grp">진동수<input type="range" id="f2" min="300" max="1500" step="50" value="700"><span class="val" id="vf2"></span></div>
 <div class="grp">스피커 간격<input type="range" id="d2" min="0.5" max="2.5" step="0.1" value="1.5"><span class="val" id="vd2"></span></div>
 <label class="grp"><input type="checkbox" id="inv2"> S₂ 위상 반대로</label>
 <select id="snd2type" class="btn" style="padding:5px 8px">
  <option value="tone">🎵 일정 진동수 (현재 f)</option>
  <option value="music">🎶 멜로디 음악</option>
 </select>
 <button class="btn" id="snd2">🔊 P 지점 소리 듣기</button>
 <span style="font-size:12px;color:#64748b">화면을 클릭·드래그해 P를 옮기세요</span>
</div>
<div id="c4" class="ctrl view">
 <div class="grp">경로차 Δr = |r₂−r₁|<input type="range" id="drp" min="0" max="3" step="0.1" value="0.5"><span class="val" id="vdrp">0.5 λ</span></div>
 <button class="btn" data-dr="0">0 (보강)</button>
 <button class="btn on" data-dr="0.5">0.5λ (상쇄)</button>
 <button class="btn" data-dr="1">1.0λ (보강)</button>
 <button class="btn" data-dr="1.5">1.5λ (상쇄)</button>
 <button class="btn" data-dr="2">2.0λ (보강)</button>
 <button class="btn" data-dr="2.5">2.5λ (상쇄)</button>
 <label class="grp"><input type="checkbox" id="invp"> S₂ 위상 반대로</label>
 <button class="btn" id="sndp">🔊 P 지점 소리 듣기</button>
</div>
<div id="c5" class="ctrl view">
 <button class="btn on" data-m3="0">🎧 그림 Ⅲ-24 소음 제거 이어폰</button>
 <button class="btn" data-m3="1">🚗 그림 Ⅲ-25 자동차 능동 소음 제어</button>
 <button class="btn" data-m3="2">📈 파형 상세 실험</button>
 <label class="grp"><input type="checkbox" id="anc" checked> 소음 제어(ANC) 켜기</label>
 <div class="grp">반대 파동 진폭<input type="range" id="a3" min="0" max="1.2" step="0.05" value="1"><span class="val" id="va3"></span></div>
 <div class="grp">위상차<input type="range" id="p3" min="0" max="360" step="10" value="180"><span class="val" id="vp3"></span></div>
 <button class="btn" id="noise3">소음: 규칙적</button><button class="btn" id="snd3">🔊 귀에 들리는 소리</button>
</div>
<div id="c6" class="ctrl view">
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
const TABS=[['⓪ 종파의 밀·소 (압력·변위)','기초 개념','음파는 공기가 진행 방향과 나란히 진동하는 종파입니다. 공기가 모인 곳은 <b>밀(고압, ΔP 최대)</b>, 성긴 곳은 <b>소(저압, ΔP 최소)</b>이며, 밀·소 지점에서 <b>매질의 변위는 0</b>입니다(압력과 변위는 λ/4, 즉 90° 위상차).'],
['① 중첩의 원리','A①','두 파동이 겹치는 곳의 변위는 두 변위의 합입니다. 지나간 뒤에는 각자 원래 모양으로 진행합니다.'],
['② 보강 간섭·상쇄 간섭','A②','같은 위상으로 만나면 진폭이 커지고(보강), 반대 위상으로 만나면 진폭이 작아집니다(상쇄). 진동수는 변하지 않습니다.'],
['③ 두 스피커의 간섭','B','경로차가 반 파장의 짝수 배인 곳은 보강(소리 큼), 홀수 배인 곳은 상쇄(소리 작음)입니다. P를 드래그하며 소리 세기 변화를 직접 들어 보세요!'],
['③-2 경로차와 간섭 조건','B 심화','두 파원 S₁, S₂에서 P까지의 거리 차(경로차 Δr = |r₂ − r₁|)가 반 파장의 짝수 배(0, λ, 2λ…)이면 같은 위상으로 만나 <b>보강 간섭</b>, 홀수 배(0.5λ, 1.5λ, 2.5λ…)이면 반대 위상으로 만나 <b>상쇄 간섭</b>이 일어납니다.'],
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
// ===== tab0 longitudinal wave: 밀·소(공기 입자) + 압력 변화(ΔP) + 변위(s)
const LP={cols:46,rows:5,pts:[]};
for(let r=0;r<LP.rows;r++){
 for(let c=0;c<LP.cols;c++){
  LP.pts.push({c,r,jx:(Math.sin(c*12.7+r*31.3)*0.28),jy:(Math.cos(c*19.1+r*7.7)*0.22)});
 }
}
function sceneLong(dt){
 clear();
 const A=+$('la0').value, lam=+$('lw0').value, ov=$('lov0').checked, trk=$('ltrk0').checked;
 $('vla0').textContent=A+' px'; $('vlw0').textContent=lam+' px';
 const x0=135, x1=965, tw=x1-x0, k=2*Math.PI/lam, w=2*Math.PI*0.45, wt=w*T;

 // 1) 상단: 종파 공기 관 (y = 26 .. 138)
 const ty=26, th=112, tmid=ty+th/2;
 txt('① 공기 입자의 실제 진동 (종파: 밀·소)', x0, ty-11, {a:'left',b:1,s:13,c:INK});
 // 밀/소 배경 압력 음영 (ΔP = -cos(k(x-x0)-wt): 밀=+1 빨강, 소=-1 파랑)
 for(let x=x0;x<x1;x+=4){
  const dp=-Math.cos(k*(x-x0)-wt);
  ctx.fillStyle=dp>0?`rgba(225,29,72,${(dp*0.18).toFixed(3)})`:`rgba(37,99,235,${(-dp*0.16).toFixed(3)})`;
  ctx.fillRect(x,ty,4,th);
 }
 ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1.8; ctx.strokeRect(x0,ty,tw,th);

 // 왼쪽 스피커 진동판(피스톤)
 const pisX=x0-16+A*Math.sin(-wt);
 ctx.fillStyle='#334155'; ctx.fillRect(x0-58,tmid-20,38,40);
 ctx.fillStyle='#0f172a'; ctx.fillRect(pisX,ty+4,12,th-8);
 ln(x0-20,tmid,pisX,tmid,'#475569',5);
 txt('스피커',x0-39,ty+th+14,{s:11.5,b:1,c:SUB});

 // 공기 입자 렌더링 (s(x0,t) = A sin(k(x-x0) - wt))
 const dxStep=tw/(LP.cols-1), dyStep=(th-24)/(LP.rows-1);
 const trackCols=[11,23,35];
 LP.pts.forEach(p=>{
  const eqX=x0+p.c*dxStep+p.jx*dxStep*0.5;
  const eqY=ty+12+p.r*dyStep+p.jy*dyStep*0.4;
  const s=A*Math.sin(k*(eqX-x0)-wt);
  const px=eqX+s;
  if(px<x0+2||px>x1-2)return;
  const isTrk=trk && p.r===2 && trackCols.includes(p.c);
  if(isTrk){
   ln(eqX,ty+6,eqX,ty+th-6,'rgba(234,88,12,0.45)',1.2,[3,3]);
   dot(px,eqY,5.5,OR);
   if(Math.abs(s)>3)arr(eqX,eqY-12,px,eqY-12,OR);
  }else{
   dot(px,eqY,2.6,'#1e293b');
  }
 });

 // 밀(고압) / 소(저압) 수직 기준선 및 라벨 표시 (x_밀: k(x-x0)-wt = π + 2πn, x_소: 2πn)
 const nMin=Math.floor((-wt)/(2*Math.PI))-1, nMax=Math.ceil((k*tw-wt)/(2*Math.PI))+1;
 for(let n=nMin;n<=nMax;n++){
  const xComp=x0+(wt+Math.PI+2*Math.PI*n)/k;
  const xRare=x0+(wt+2*Math.PI*n)/k;
  if(xComp>x0+18 && xComp<x1-18){
   ln(xComp,ty,xComp,438,'rgba(225,29,72,0.38)',1.3,[4,4]);
   ctx.fillStyle=RD; ctx.beginPath(); ctx.roundRect(xComp-24,ty+4,48,18,6); ctx.fill();
   txt('밀(고압)',xComp,ty+13,{s:10.5,b:1,c:'#fff'});
   // 좌우 입자가 몰려드는 화살표 표시 (→ ● ←)
   txt('→ ● ←',xComp,ty+th-10,{s:10.5,b:1,c:RD});
  }
  if(xRare>x0+18 && xRare<x1-18){
   ln(xRare,ty,xRare,438,'rgba(37,99,235,0.32)',1.2,[4,4]);
   ctx.fillStyle=BL; ctx.beginPath(); ctx.roundRect(xRare-24,ty+4,48,18,6); ctx.fill();
   txt('소(저압)',xRare,ty+13,{s:10.5,b:1,c:'#fff'});
   txt('← ○ →',xRare,ty+th-10,{s:10.5,b:1,c:BL});
  }
 }

 // 2) 중단: 압력 변화 그래프 ΔP(x) = -ΔPmax cos(k(x-x0) - wt)
 const py0=235, pAmp=48*(A/15);
 ln(x0,py0,x1,py0,'#cbd5e1',1.4); ln(x0,py0-62,x0,py0+62,'#94a3b8',1.2);
 txt('② 압력 변화 ΔP', 18, py0-16, {a:'left',b:1,s:13,c:RD});
 txt('(고압 + / 저압 −)', 18, py0+4, {a:'left',s:11.5,c:SUB});
 txt('+ΔP (밀)', x0-8, py0-44, {a:'right',s:11,c:RD,b:1});
 txt('0 (대기압)', x0-8, py0, {a:'right',s:10.5,c:SUB});
 txt('−ΔP (소)', x0-8, py0+44, {a:'right',s:11,c:BL,b:1});
 plot(x=>-pAmp*Math.cos(k*(x-x0)-wt), x0, x1, py0, RD, 3.0);

 // 3) 하단: 매질 변위 그래프 s(x) = A sin(k(x-x0) - wt)
 const sy0=372, sAmp=48*(A/15);
 ln(x0,sy0,x1,sy0,'#cbd5e1',1.4); ln(x0,sy0-62,x0,sy0+62,'#94a3b8',1.2);
 txt('③ 매질 변위 s', 18, sy0-16, {a:'left',b:1,s:13,c:BL});
 txt('(오른쪽 + / 왼쪽 −)', 18, sy0+4, {a:'left',s:11.5,c:SUB});
 txt('+s (→)', x0-8, sy0-44, {a:'right',s:11,c:BL,b:1});
 txt('0 (평형)', x0-8, sy0, {a:'right',s:10.5,c:SUB});
 txt('−s (←)', x0-8, sy0+44, {a:'right',s:11,c:BL,b:1});
 if(ov){
  plot(x=>-sAmp*Math.cos(k*(x-x0)-wt), x0, x1, sy0, 'rgba(225,29,72,0.55)', 1.8, [5,4]);
  txt('빨간 점선: 압력 ΔP (변위보다 λ/4, 90° 앞섬)', x1-6, sy0-56, {a:'right',s:11.5,b:1,c:RD});
 }
 plot(x=>sAmp*Math.sin(k*(x-x0)-wt), x0, x1, sy0, BL, 3.0);

 // 밀 지점에서 변위 = 0 강조 점
 for(let n=nMin;n<=nMax;n++){
  const xComp=x0+(wt+Math.PI+2*Math.PI*n)/k;
  if(xComp>x0+18 && xComp<x1-18){
   dot(xComp, py0-pAmp, 5, RD);
   dot(xComp, sy0, 5, PU);
  }
 }

 $('step').innerHTML='<b>핵심 비교</b> · <b style="color:#e11d48">밀(고압, ΔP 최대)</b> 지점은 왼쪽 공기(+변위, →)와 오른쪽 공기(−변위, ←)가 양쪽에서 몰려드는 곳이므로 <b>그 지점 자체의 변위는 0</b>입니다. 반대로 변위가 최대(±A)인 지점은 압력 변화가 0(대기압)입니다. 즉, <b>압력 파동과 변위 파동은 정확히 λ/4 (90°)의 위상차</b>를 가집니다.';
}
$('lpk0').onclick=()=>{paused=true;$('pp').textContent='▶ 재생';};
// ===== tab1 curved waves (곡선 파동)
const S0={t:0,inv:true,multi:false};
function pulseA(x){
 const c=150+S0.t*95,u=x-c;
 if(!S0.multi){return Math.abs(u)<70?70*Math.pow(Math.cos(Math.PI*u/140),2):0}
 return Math.abs(u)<110?65*Math.cos(Math.PI*u/220)*Math.sin(Math.PI*u/55):0;
}
function pulseB(x){
 const c=850-S0.t*95,u=x-c,sg=S0.inv?-1:1;
 if(!S0.multi){return (Math.abs(u)<70?35*Math.pow(Math.cos(Math.PI*u/140),2):0)*sg}
 return (Math.abs(u)<110?45*Math.cos(Math.PI*u/220)*Math.sin(Math.PI*u/55):0)*sg;
}
function scene0(dt){if(!paused){S0.t+=dt;if(S0.t>8.5)S0.t=0}clear();
 const rows=[[110,'곡선 파동 A → (+2칸)',x=>pulseA(x),BL],[230,'← 곡선 파동 B ('+(S0.inv?'−1칸':'+1칸')+')',x=>pulseB(x),RD],[370,'줄의 실제 모습 (합성파 = A + B, 점선은 각 파동)',x=>pulseA(x)+pulseB(x),PU]];
 rows.forEach(r=>{ln(40,r[0],960,r[0],'#e2e8f0',1);txt(r[1],40,r[0]-80,{a:'left',b:1,s:13,c:r[3]});plot(r[2],40,960,r[0],r[3],r[3]===PU?3.4:2.4)});
 // 합성파 축(y=370) 위에 두 개별 파동(A: 파랑 점선, B: 빨강 점선)을 함께 겹쳐 표시
 plot(x=>pulseA(x),40,960,370,'rgba(37,99,235,0.7)',1.8,[5,4]);
 plot(x=>pulseB(x),40,960,370,'rgba(225,29,72,0.7)',1.8,[5,4]);
 const cA=150+S0.t*95,cB=850-S0.t*95,ov=Math.abs(cA-cB)<(S0.multi?210:135);
 arr(Math.min(920,cA+45),55,Math.min(950,cA+85),55,BL);
 arr(Math.max(80,cB-45),175,Math.max(50,cB-85),175,RD);
 if(ov){const xm=(cA+cB)/2;ln(xm,40,xm,440,'#cbd5e1',1,[4,4]);const ya=pulseA(xm),yb=pulseB(xm);txt('A: '+(ya/35).toFixed(1)+'  +  B: '+(yb/35).toFixed(1)+'  =  '+((ya+yb)/35).toFixed(1)+' (칸)',xm+12,300,{a:'left',b:1,s:14,c:PU})}
 $('step').innerHTML=ov?'두 곡선 파동이 <b>겹치는 곳의 변위 = A의 변위 + B의 변위</b>입니다. '+(S0.inv?'파동 B가 반대 위상(−1칸)이라 꼭짓점이 겹치면 <b>2 + (−1) = +1칸</b>으로 줄어듭니다(상쇄).':'같은 위상(+1칸)이라 꼭짓점이 겹치면 <b>2 + 1 = +3칸</b>으로 더 커집니다(보강).'):(S0.t<3.68?'두 곡선 파동이 서로를 향해 부드럽게 진행합니다.':'만난 뒤에도 두 파동은 <b>원래 곡선 모양과 크기 그대로</b> 각자 진행합니다(파동의 독립성).');}
$('p0a').onclick=()=>{S0.inv=true;S0.t=0;$('p0a').classList.add('on');$('p0b').classList.remove('on')};
$('p0b').onclick=()=>{S0.inv=false;S0.t=0;$('p0b').classList.add('on');$('p0a').classList.remove('on')};
$('p0w').onclick=()=>{S0.multi=!S0.multi;S0.t=0;$('p0w').textContent=S0.multi?'파형: 연속 곡선파(사인파 묶음)':'파형: 단일 곡선파';$('p0w').classList.toggle('on',S0.multi)};
$('p0pk').onclick=()=>{S0.t=350/95;paused=true;$('pp').textContent='▶ 재생'};
$('p0go').onclick=()=>{S0.t=0;paused=false;$('pp').textContent='⏸ 일시정지'};
// ===== tab1 phase
function scene1(dt){clear();const ph=+$('ph1').value*Math.PI/180,k=2*Math.PI/260,w=2*Math.PI*0.5,A=45;
 const f1=x=>A*Math.sin(k*x-w*T),f2=x=>A*Math.sin(k*x-w*T+ph);
 [[95,'파동 1',f1,BL],[215,'파동 2',f2,RD],[355,'합성파 (파동 1 + 파동 2)',x=>f1(x)+f2(x),PU]].forEach(r=>{ln(150,r[0],960,r[0],'#e2e8f0',1);ln(150,r[0]-90,150,r[0]+90,'#f1f5f9',1);txt(r[1],20,r[0],{a:'left',b:1,s:13,c:r[3]});plot(r[2],150,960,r[0],r[3],r[3]===PU?3.4:2.2)});
 // 합성파 축(y=355) 위에 파동 1(파랑 점선)과 파동 2(빨강 점선)를 함께 겹쳐 표시
 plot(f1,150,960,355,'rgba(37,99,235,0.65)',1.8,[5,4]);
 plot(f2,150,960,355,'rgba(225,29,72,0.65)',1.8,[5,4]);
 const amp=2*Math.abs(Math.cos(ph/2));ln(150,355-A*2,960,355-A*2,'#e9d5ff',1,[4,4]);ln(150,355+A*2,960,355+A*2,'#e9d5ff',1,[4,4]);txt('2A',140,355-A*2,{a:'right',s:12,c:PU});
 txt('합성파의 진폭 = '+amp.toFixed(2)+' A',W-30,440,{a:'right',b:1,s:17,c:PU});
 const deg=+$('ph1').value;$('vph1').textContent=deg+'°';
 $('step').innerHTML=deg%360===0?'<b>같은 위상</b>: 마루와 마루, 골과 골이 만나 진폭이 <b>2A</b>가 됩니다 → <b>보강 간섭</b> (소리가 커짐)':(deg===180?'<b>반대 위상</b>: 마루와 골이 만나 진폭이 <b>0</b>이 됩니다 → <b>상쇄 간섭</b> (소리가 사라짐)':'위상차가 0°에 가까울수록 진폭이 커지고 180°에 가까울수록 작아집니다. 합성파의 <b>진동수(마루 사이 간격)</b>는 변하지 않습니다.');}
$('ph1a').onclick=()=>{$('ph1').value=0};$('ph1b').onclick=()=>{$('ph1').value=180};
// ===== tab3 two speakers + P 지점 실시간 소리 재생 (일정 진동수 / 멜로디 음악) + 1개만 켜기 비교
const S2={mode:0,single:false,px:640,py:160,drag:false,snd:false,osc:null,gn:null,tm:null,step:0};
const MELODY=[523.25,659.25,783.99,659.25,880.0,783.99,659.25,587.33]; // 도-미-솔-미-라-솔-미-레
function stopSnd2(){
 S2.snd=false;
 if(S2.tm){clearInterval(S2.tm);S2.tm=null}
 if(S2.osc){try{S2.osc.stop()}catch(e){};S2.osc=null}
 if(S2.gn){try{S2.gn.disconnect()}catch(e){};S2.gn=null}
 $('snd2').classList.remove('on');$('snd2').textContent='🔊 P 지점 소리 듣기';
}
function startSnd2(){
 stopSnd2();
 if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
 if(AC.state==='suspended')AC.resume();
 S2.snd=true;
 S2.osc=AC.createOscillator(); S2.gn=AC.createGain();
 const isMus=$('snd2type').value==='music';
 S2.osc.type=isMus?'triangle':'sine';
 S2.osc.frequency.value=isMus?MELODY[0]:+$('f2').value;
 S2.gn.gain.value=0.001;
 S2.osc.connect(S2.gn).connect(AC.destination);
 S2.osc.start();
 if(isMus){
  S2.step=0;
  S2.tm=setInterval(()=>{
   if(!S2.snd||!S2.osc)return;
   S2.step=(S2.step+1)%MELODY.length;
   S2.osc.frequency.setTargetAtTime(MELODY[S2.step],AC.currentTime,0.02);
  },360);
 }
 $('snd2').classList.add('on');$('snd2').textContent='🔇 P 지점 소리 끄기';
}
$('snd2').onclick=()=>{if(S2.snd)stopSnd2();else startSnd2()};
$('snd2type').onchange=()=>{if(S2.snd)startSnd2()};

const GX=500,GY=330,sc=2; // grid units
function scene2(dt){clear();const f=+$('f2').value,lam=VS/f,d=+$('d2').value,inv=$('inv2').checked;
 $('vf2').textContent=f+' Hz (λ='+lam.toFixed(2)+' m)';$('vd2').textContent=d.toFixed(1)+' m';
 const m2px=110; // px per m
 const s1={x:120,y:330-d/2*m2px},s2={x:120,y:330+d/2*m2px}; // speakers at left, field to the right
 const fw=880,fh=320,ox=100,oy=20,res=4;
 const id=ctx.createImageData(fw/res|0,fh/res|0);const k=2*Math.PI/lam,wt=2*Math.PI*T*0.8;
 for(let j=0;j<id.height;j++)for(let i=0;i<id.width;i++){const X=ox+i*res,Y=oy+j*res;
  const r1=Math.hypot(X-s1.x,Y-(s1.y-170))/m2px,r2=Math.hypot(X-s2.x,Y-(s2.y-170))/m2px;
  let v;
  if(S2.single){
   v=(S2.mode===0)?(Math.sin(k*r1-wt)/Math.sqrt(r1+0.3))*0.9:(0.25*2-1);
  }else if(S2.mode===0){
   const a1=Math.sin(k*r1-wt)/Math.sqrt(r1+0.3),a2=(inv?-1:1)*Math.sin(k*r2-wt)/Math.sqrt(r2+0.3);v=(a1+a2)*0.9
  }else{
   const dphi=k*(r1-r2)+(inv?Math.PI:0);v=(Math.cos(dphi/2))**2*2-1
  }
  const p=(j*id.width+i)*4;let R,G,B;
  if(S2.mode===0){if(v>0){R=255-v*200;G=255-v*170;B=255}else{R=255;G=255+v*170;B=255+v*200}}
  else{const u=(v+1)/2;R=255-u*215;G=255-u*190;B=255-u*60}
  id.data[p]=R;id.data[p+1]=G;id.data[p+2]=B;id.data[p+3]=255}
 const off=document.createElement('canvas');off.width=id.width;off.height=id.height;off.getContext('2d').putImageData(id,0,0);
 ctx.imageSmoothingEnabled=true;ctx.drawImage(off,ox,oy,fw,fh);
 const S1y=s1.y-170,S2y=s2.y-170;
 ctx.fillStyle='#334155';ctx.fillRect(s1.x-14,S1y-12,18,24);txt('S₁',s1.x-26,S1y,{b:1,s:13});
 ctx.fillStyle=S2.single?'#cbd5e1':'#334155';ctx.fillRect(s2.x-14,S2y-12,18,24);txt(S2.single?'S₂(OFF)':'S₂',s2.x-32,S2y,{b:1,s:12,c:S2.single?SUB:INK});
 // probe
 const r1=Math.hypot(S2.px-s1.x,S2.py-S1y)/m2px,r2=Math.hypot(S2.px-s2.x,S2.py-S2y)/m2px,dp=Math.abs(r1-r2),n=dp/(lam/2);
 const dphiP=k*(r1-r2)+(inv?Math.PI:0);
 const ampP=S2.single?0.5:Math.abs(Math.cos(dphiP/2)); // 1개만: 진폭 0.5 (세기 25%), 2개: 0(상쇄)~1(보강 100%)
 if(S2.snd&&S2.gn&&AC){
  if($('snd2type').value==='tone'&&S2.osc)S2.osc.frequency.setTargetAtTime(f,AC.currentTime,0.03);
  S2.gn.gain.setTargetAtTime(0.14*ampP*ampP,AC.currentTime,0.04);
 }
 ln(s1.x,S1y,S2.px,S2.py,BL,1.5,[5,4]);if(!S2.single)ln(s2.x,S2y,S2.px,S2.py,RD,1.5,[5,4]);dot(S2.px,S2.py,7,'#facc15');ctx.strokeStyle=INK;ctx.lineWidth=1.5;ctx.beginPath();ctx.arc(S2.px,S2.py,7,0,7);ctx.stroke();txt('P',S2.px+14,S2.py-12,{b:1,s:15});
 const near=Math.round(n),even=near%2===0,clean=Math.abs(n-near)<0.15;let kind=S2.single?'스피커 1개 (간섭 없음 · 기준 세기)':(clean?((even!==inv)?'보강 간섭 (소리 큼)':'상쇄 간섭 (소리 작음)'):'보강과 상쇄의 중간');
 // walk line graph (1개만 켰을 때 기준 25% 점선과 비교)
 const gy=440,gx0=ox,gx1=ox+fw;ln(gx0,gy,gx1,gy,'#cbd5e1',1);
 ln(gx0,gy-0.25*70,gx1,gy-0.25*70,'#94a3b8',1.2,[4,4]);txt('1개 기준(25%)',gx0+4,gy-0.25*70-10,{a:'left',s:10.5,c:SUB});
 ctx.beginPath();ctx.strokeStyle=S2.single?'rgba(124,58,237,0.3)':PU;ctx.lineWidth=S2.single?1.5:2.2;if(S2.single)ctx.setLineDash([4,4]);
 for(let X=gx0;X<=gx1;X+=3){const a=Math.hypot(X-s1.x,S2.py-S1y)/m2px,b=Math.hypot(X-s2.x,S2.py-S2y)/m2px;const I=(Math.cos((k*(a-b)+(inv?Math.PI:0))/2))**2;const y=gy-I*70;X===gx0?ctx.moveTo(X,y):ctx.lineTo(X,y)}ctx.stroke();ctx.setLineDash([]);
 if(S2.single){ln(gx0,gy-0.25*70,gx1,gy-0.25*70,BL,2.6);}
 txt('P를 지나는 가로줄을 따라 걸을 때 소리의 세기',gx0,gy-82+4,{a:'left',s:12,b:1,c:PU});ln(S2.px,gy-75,S2.px,gy,'#facc15',2);
 // 정보 박스 + 실시간 소리 세기 바
 ctx.fillStyle='rgba(255,255,255,0.94)';ctx.fillRect(685,24,305,118);ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1;ctx.strokeRect(685,24,305,118);
 txt(S2.single?('S₁P = '+r1.toFixed(2)+' m  (S₂ 꺼짐)'):('S₁P = '+r1.toFixed(2)+' m,  S₂P = '+r2.toFixed(2)+' m'),696,42,{a:'left',s:13});
 txt(S2.single?'간섭 없음 (단일 파원 기준 진폭 A)':'경로차 = '+dp.toFixed(2)+' m = 반 파장의 '+n.toFixed(1)+'배',696,64,{a:'left',s:13,b:1});
 txt(kind,696,88,{a:'left',s:14,b:1,c:S2.single?GN:(kind.startsWith('보강')?BL:(kind.startsWith('상쇄')?RD:SUB))});
 txt('🔊 P 지점 소리 세기: '+Math.round(ampP*ampP*100)+'%',696,112,{a:'left',s:12,b:1,c:INK});
 ctx.fillStyle='#e2e8f0';ctx.fillRect(835,105,142,13);
 ctx.fillStyle=S2.single?GN:(ampP>0.7?BL:(ampP<0.3?RD:PU));ctx.fillRect(835,105,142*ampP*ampP,13);
 $('step').innerHTML=S2.single
  ? '<b>스피커 S₁ 1개만 켜진 상태</b>입니다. 간섭 무늬가 사라지고 모든 위치에서 일정한 기준 세기(<b>25%</b>, 진폭 A)로 들립니다. 상쇄 간섭(흰 줄)에 P를 두고 <b>S₁+S₂ 모두 ↔ S₁ 1개만</b>을 번갈아 눌러 보면, <b>스피커를 1개 껐는데 오히려 소리가 커지는</b> 신기한 현상을 체험할 수 있습니다!'
  : ((S2.mode===0?'<b style="color:#2563eb">파란색 = 마루</b>, <b style="color:#e11d48">빨간색 = 골</b>입니다. 마루끼리·골끼리 만나는 줄은 진하게 출렁이고(보강), 마루와 골이 만나는 줄은 거의 흰색입니다(상쇄). ':'진한 곳일수록 소리가 큽니다. 흰 줄(소리 작음)이 상쇄 간섭 지점입니다. ')+'<b>🔈 S₁ 1개만</b> 버튼과 번갈아 눌러 단일 스피커(25%) 대비 보강(100%, 4배)과 상쇄(0%)의 차이를 비교해 보세요.'+(inv?' (지금은 S₂ 위상이 반대라 조건이 서로 바뀌었습니다.)':''));}
function moveP(e){if(tab!==3)return;const r=cv.getBoundingClientRect();const x=(e.clientX-r.left)*W/r.width,y=(e.clientY-r.top)*H/r.height;if(x>130&&x<980&&y>20&&y<340){S2.px=x;S2.py=y}}
cv.addEventListener('mousedown',e=>{if(tab===3){S2.drag=true;moveP(e)}});
cv.addEventListener('mousemove',e=>{if(tab===3&&S2.drag)moveP(e)});
window.addEventListener('mouseup',()=>{S2.drag=false});
cv.addEventListener('click',moveP);
$('m2a').onclick=()=>{S2.mode=0;$('m2a').classList.add('on');$('m2b').classList.remove('on')};$('m2b').onclick=()=>{S2.mode=1;$('m2b').classList.add('on');$('m2a').classList.remove('on')};
$('sp2both').onclick=()=>{S2.single=false;$('sp2both').classList.add('on');$('sp2one').classList.remove('on')};
$('sp2one').onclick=()=>{S2.single=true;$('sp2one').classList.add('on');$('sp2both').classList.remove('on')};

// ===== tab4 경로차와 보강·상쇄 간섭 조건 (두 경로의 파동 비교)
const SP={snd:false,osc:null,gn:null};
function stopSndP(){
 SP.snd=false;
 if(SP.osc){try{SP.osc.stop()}catch(e){};SP.osc=null}
 if(SP.gn){try{SP.gn.disconnect()}catch(e){};SP.gn=null}
 $('sndp').classList.remove('on');$('sndp').textContent='🔊 P 지점 소리 듣기';
}
$('sndp').onclick=()=>{
 if(SP.snd){stopSndP();return}
 if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
 if(AC.state==='suspended')AC.resume();
 SP.snd=true;
 SP.osc=AC.createOscillator(); SP.gn=AC.createGain();
 SP.osc.type='sine'; SP.osc.frequency.value=440; SP.gn.gain.value=0.001;
 SP.osc.connect(SP.gn).connect(AC.destination); SP.osc.start();
 $('sndp').classList.add('on');$('sndp').textContent='🔇 소리 끄기';
};
function scenePath(dt){
 clear();
 const dr=+$('drp').value; // 경로차 (λ 단위: 0 ~ 3.0)
 const inv=$('invp').checked;
 const halfN=dr*2; // 반 파장의 배수
 $('vdrp').textContent=dr.toFixed(1)+' λ (반 파장 '+halfN.toFixed(1)+'배)';

 const lamPx=130; // 1파장 = 130 px
 const xP=760;    // 관찰 지점 P의 x 좌표
 const r1Lam=2.5; // S1 -> P 기본 거리 = 2.5 λ
 const xS1=xP-r1Lam*lamPx;        // 760 - 325 = 435
 const xS2=xP-(r1Lam+dr)*lamPx;   // S2는 왼쪽으로 dr*lamPx만큼 더 멀리 위치!
 const k=2*Math.PI/lamPx, wt=2*Math.PI*0.65*T, A=36;

 // 관찰점 P 수직 기준선
 ln(xP,24,xP,436,'#f59e0b',2,[5,4]);
 dot(xP,24,6,'#f59e0b');
 txt('관찰 지점 P',xP,13,{b:1,s:13,c:'#b45309'});

 // 경로차 Δr = r2 - r1 하이라이트 영역 (xS2 .. xS1)
 if(dr>0.01){
  ctx.fillStyle='rgba(250,204,21,0.16)';
  ctx.fillRect(xS2,135,xS1-xS2,102);
  ln(xS2,45,xS2,245,'#94a3b8',1.2,[3,3]);
  ln(xS1,45,xS1,245,'#94a3b8',1.2,[3,3]);
  arr(xS2+2,148,xS1-2,148,'#b45309');
  arr(xS1-2,148,xS2+2,148,'#b45309');
  txt('경로차 Δr = '+dr.toFixed(1)+'λ (반 파장의 '+halfN.toFixed(1)+'배)',(xS2+xS1)/2,133,{b:1,s:12.5,c:'#b45309'});
 }

 // 1) 파원 S1 -> P 파동 (y = 82)
 const y1Axis=82;
 ln(35,y1Axis,xP,y1Axis,'#e2e8f0',1);
 const f1=x=>A*Math.sin(k*(x-xS1)-wt);
 plot(f1,xS1,xP,y1Axis,BL,2.8);
 dot(xS1,y1Axis,7,BL); txt('S₁',xS1-18,y1Axis,{b:1,s:14,c:BL});
 txt('경로 1 (r₁ = 2.5λ)',xS1+8,y1Axis-48,{a:'left',b:1,s:12.5,c:BL});
 dot(xP,y1Axis-f1(xP),5.5,BL);

 // 2) 파원 S2 -> P 파동 (y = 202)
 const y2Axis=202;
 ln(35,y2Axis,xP,y2Axis,'#e2e8f0',1);
 const phInv=inv?Math.PI:0;
 const f2=x=>A*Math.sin(k*(x-xS2)-wt+phInv);
 plot(f2,Math.max(35,xS2),xP,y2Axis,RD,2.8);
 dot(Math.max(35,xS2),y2Axis,7,RD); txt('S₂'+(inv?'(반대위상)':''),Math.max(35,xS2),y2Axis+22,{b:1,s:12.5,c:RD});
 txt('경로 2 (r₂ = '+(r1Lam+dr).toFixed(1)+'λ)',Math.max(42,xS2+8),y2Axis-48,{a:'left',b:1,s:12.5,c:RD});
 dot(xP,y2Axis-f2(xP),5.5,RD);

 // 3) P 지점 부근 합성파 (x = xS1 .. xP, y = 352)
 const y3Axis=352;
 ln(xS1,y3Axis,xP,y3Axis,'#e2e8f0',1);
 txt('지점 P에서의 합성파 (파동 1 + 파동 2)',xS1,y3Axis-76,{a:'left',b:1,s:13,c:PU});
 plot(f1,xS1,xP,y3Axis,'rgba(37,99,235,0.5)',1.6,[4,4]);
 plot(f2,xS1,xP,y3Axis,'rgba(225,29,72,0.5)',1.6,[4,4]);
 plot(x=>f1(x)+f2(x),xS1,xP,y3Axis,PU,3.6);
 const ySumP=f1(xP)+f2(xP);
 dot(xP,y3Axis-ySumP,6.5,PU);

 // 우측 결과 판정 패널 (x = 790 .. 980)
 const dphi=2*Math.PI*dr+phInv;
 const ampRatio=2*Math.abs(Math.cos(dphi/2)); // 0 ~ 2 (A 기준)
 if(SP.snd&&SP.gn&&AC){SP.gn.gain.setTargetAtTime(0.13*(ampRatio/2)*(ampRatio/2),AC.currentTime,0.04)}

 const nearHalf=Math.round(halfN);
 const isExact=Math.abs(halfN-nearHalf)<0.08;
 const isEven=nearHalf%2===0;
 const isConst=isExact&&(isEven!==inv);
 const isDest=isExact&&(isEven===inv);
 const statusTxt=isConst?'보강 간섭 (최대!)':(isDest?'상쇄 간섭 (소멸!)':'중간 간섭');
 const statusCol=isConst?BL:(isDest?RD:SUB);

 ctx.fillStyle='#f8fafc';ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1.5;
 ctx.beginPath();ctx.roundRect(788,40,196,385,14);ctx.fill();ctx.stroke();
 txt('지점 P 간섭 판정',886,66,{b:1,s:14,c:INK});
 ctx.fillStyle=isConst?'#eff6ff':(isDest?'#fff1f2':'#f1f5f9');
 ctx.beginPath();ctx.roundRect(802,84,168,42,10);ctx.fill();
 txt(statusTxt,886,105,{b:1,s:16,c:statusCol});

 txt('합성파 진폭',886,148,{s:12,c:SUB,b:1});
 txt(ampRatio.toFixed(2)+' A',886,172,{s:22,c:PU,b:1});

 // 진폭 막대 게이지
 ctx.fillStyle='#e2e8f0';ctx.fillRect(856,196,60,120);
 const barH=(ampRatio/2)*120;
 ctx.fillStyle=statusCol;ctx.fillRect(856,316-barH,60,barH);
 txt('2A',842,202,{s:11,c:SUB});txt('A',842,256,{s:11,c:SUB});txt('0',842,316,{s:11,c:SUB});

 // 조건 요약 공식
 txt('📌 같은 위상 파원 기준',886,346,{s:11.5,b:1,c:INK});
 txt('보강: Δr = (λ/2) × 짝수',886,368,{s:11.5,b:1,c:BL});
 txt('상쇄: Δr = (λ/2) × 홀수',886,388,{s:11.5,b:1,c:RD});
 txt('현재: (λ/2) × '+halfN.toFixed(1),886,410,{s:11.5,b:1,c:'#b45309'});

 $('step').innerHTML=isConst
  ? '<b>보강 간섭 조건 성립!</b> 경로차 Δr = '+dr.toFixed(1)+'λ (반 파장의 '+nearHalf+'배)이므로 두 파동이 지점 P에 <b>같은 위상(마루+마루, 골+골)</b>으로 도착하여 진폭이 <b>2A</b>로 커집니다.'
  : (isDest
    ? '<b>상쇄 간섭 조건 성립!</b> 경로차 Δr = '+dr.toFixed(1)+'λ (반 파장의 '+nearHalf+'배)이므로 두 파동이 지점 P에 <b>반대 위상(마루+골)</b>으로 도착하여 서로 지워져 진폭이 <b>0</b>이 됩니다.'
    : '경로차 Δr = '+dr.toFixed(1)+'λ (반 파장의 '+halfN.toFixed(1)+'배)입니다. 위 프리셋 버튼을 눌러 반 파장의 짝수 배(보강)와 홀수 배(상쇄)일 때 P 지점의 두 파동이 어떻게 만나는지 비교해 보세요.');
}
document.querySelectorAll('[data-dr]').forEach(b=>b.onclick=()=>{
 $('drp').value=b.dataset.dr;
 document.querySelectorAll('[data-dr]').forEach(x=>x.classList.toggle('on',x===b));
});
$('drp').oninput=()=>document.querySelectorAll('[data-dr]').forEach(x=>x.classList.toggle('on',Math.abs(+x.dataset.dr-+$('drp').value)<0.01));
// ===== tab3 ANC (그림 III-24 이어폰 / 그림 III-25 자동차 능동 소음 제어 / 파형 상세 실험)
const S3={mode:0,irr:false,snd:false};let AC=null,osc=null,gn=null;
function noise(t){return S3.irr?(0.6*Math.sin(2*Math.PI*1.0*t)+0.35*Math.sin(2*Math.PI*2.7*t+1)+0.25*Math.sin(2*Math.PI*4.3*t+2)):Math.sin(2*Math.PI*1.0*t)}
function callout(x,y,w,h,t1,t2,col){
 ctx.fillStyle='rgba(255,255,255,0.95)';ctx.strokeStyle=col||'#cbd5e1';ctx.lineWidth=1.5;
 ctx.beginPath();ctx.roundRect(x,y,w,h,10);ctx.fill();ctx.stroke();
 txt(t1,x+12,y+19,{a:'left',b:1,s:13,c:col||INK});
 if(t2)txt(t2,x+12,y+39,{a:'left',s:12,c:SUB});
}
function scene3(dt){
 clear();
 const on=$('anc').checked,a=+$('a3').value,ph=+$('p3').value*Math.PI/180;
 $('va3').textContent=a.toFixed(2)+' × 소음';$('vp3').textContent=$('p3').value+'°';
 const pxs=0.004,A=44;
 const nFn=x=>A*noise(T-x*pxs);
 const antiFn=x=>on?(S3.irr?-A*a*noise(T-x*pxs-0.12):A*a*Math.sin(2*Math.PI*(T-x*pxs)+ph)):0;
 let s=0,s0=0;for(let x=0;x<400;x++){const v=nFn(x)+antiFn(x);s+=v*v;s0+=nFn(x)**2}const ratio=Math.sqrt(s/s0);
 if(S3.snd&&osc)gn.gain.setTargetAtTime(0.08*Math.min(1.5,ratio),AC.currentTime,0.05);

 if(S3.mode===0){
  // [그림 III-24] 소음 제거 이어폰의 원리
  ctx.fillStyle='#fdf2ec';ctx.beginPath();ctx.roundRect(35,18,930,395,28);ctx.fill();
  const cy=210,earX=340,canalX=760;

  // 이어폰 하우징 & 이어팁
  ctx.fillStyle='#cbd5e1';ctx.strokeStyle='#64748b';ctx.lineWidth=2;
  ctx.beginPath();ctx.roundRect(310,145,115,130,18);ctx.fill();ctx.stroke();
  ctx.fillStyle='#94a3b8';ctx.beginPath();ctx.roundRect(415,155,58,110,28);ctx.fill();
  // 이어폰 기둥(줄)
  ctx.fillStyle='#e2e8f0';ctx.fillRect(338,275,26,95);ctx.strokeRect(338,275,26,95);
  // ① 외부 마이크, ② 디지털 신호 처리 칩, 스피커, ③ 내부 마이크
  ctx.fillStyle='#1e293b';ctx.fillRect(304,175,10,24); // ① 마이크
  ctx.fillStyle='#0f172a';ctx.fillRect(330,178,44,36); // ② DSP 칩
  txt('DSP',352,196,{c:'#38bdf8',b:1,s:11});
  // 내부 스피커 유닛
  ctx.fillStyle='#334155';ctx.beginPath();ctx.moveTo(392,192);ctx.lineTo(412,176);ctx.lineTo(412,244);ctx.lineTo(392,228);ctx.closePath();ctx.fill();
  // ③ 피드백 마이크
  ctx.fillStyle='#1e293b';ctx.fillRect(425,148,16,8);

  // 방사형 음파 호 (스피커 → 귀)
  for(let r=1;r<=4;r++){
   ctx.beginPath();ctx.strokeStyle='rgba(148,163,184,0.35)';ctx.lineWidth=3;
   ctx.arc(415,cy,35+r*36,-0.75,0.75);ctx.stroke();
  }

  // 오른쪽 귀(귓바퀴 & 외이도)
  ctx.fillStyle='#f5d0c5';ctx.strokeStyle='#d99b82';ctx.lineWidth=3;
  ctx.beginPath();
  ctx.moveTo(730,115);
  ctx.bezierCurveTo(755,45,865,55,875,155);
  ctx.bezierCurveTo(885,245,860,340,795,355);
  ctx.bezierCurveTo(745,365,725,315,742,275);
  ctx.lineTo(742,235);
  ctx.lineTo(665,235);
  ctx.lineTo(665,185);
  ctx.lineTo(742,185);
  ctx.closePath();ctx.fill();ctx.stroke();
  // 귓속 어두운 입구
  ctx.fillStyle='#9a5b4a';ctx.beginPath();ctx.ellipse(765,cy,18,24,0,0,7);ctx.fill();
  txt('귀 (고막)',815,325,{b:1,s:14,c:'#7c2d12'});
  if(ratio<0.25)txt('♪ ♫ 깨끗한 음악 소리',690,145,{b:1,s:14,c:PU});

  // 1) 왼쪽에서 들어오는 주변 소음 (파란 곡선파: x = 70 .. 340)
  plot(x=>nFn(x)*0.85,70,340,cy,BL,3);
  txt('주변 소음',185,cy+52,{b:1,s:13.5,c:BL});

  // 2) 이어폰 이후 구간 (x = 340 .. 765): 주변 소음(연한 파랑) + 반대 위상 신호(연한 주황) + 합성파(진한 보라)
  ctx.save();ctx.globalAlpha=0.55;
  plot(x=>nFn(x)*0.85,340,765,cy,BL,2.2);
  if(on)plot(x=>antiFn(x)*0.85,340,765,cy,OR,2.2);
  ctx.restore();
  plot(x=>(nFn(x)+antiFn(x))*0.85,340,765,cy,PU,3.6);

  // 교과서 ①~④ 단계 설명 콜아웃 및 지시선
  ln(308,175,308,75,'#475569',1.2);ln(308,75,275,75,'#475569',1.2);
  callout(65,44,215,58,'① 마이크로 주변 소음을','감지한다.',BL);

  ln(352,214,352,330,'#475569',1.2);ln(352,330,305,330,'#475569',1.2);
  callout(55,302,255,64,'② 소음을 디지털 신호로 바꾸어','반대 위상의 파동 신호를 발생시킨다.',OR);

  ln(433,148,433,75,'#475569',1.2);ln(433,75,475,75,'#475569',1.2);
  callout(475,44,225,58,'③ 사용자에게 들리는','소리를 감지한다.',INK);

  ln(585,cy,585,330,'#475569',1.2);
  callout(455,302,275,64,'④ 반대 위상 신호가 소음을 상쇄시켜','깨끗한 소리가 들리게 한다. (남은 소음 '+Math.round(ratio*100)+'%)',PU);

  txt('그림 Ⅲ-24  소음 제거 이어폰의 원리 (위 슬라이더로 진폭·위상차를 바꿔 상쇄 정도를 실험해 보세요)',500,438,{b:1,s:13.5,c:INK});
 } else if(S3.mode===1){
  // [그림 III-25] 자동차 내부의 능동 소음 제어
  ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.roundRect(35,18,930,395,28);ctx.fill();

  // 상단 파형 수식: 노면 소음 + 반대 위상 음파 = 실내 소음
  ctx.fillStyle='#ffffff';ctx.beginPath();ctx.roundRect(75,32,850,96,16);ctx.fill();
  plot(x=>nFn(x)*0.48,105,305,72,RD,2.5);
  txt('노면·엔진 소음',205,112,{b:1,s:13,c:RD});
  txt('+',345,72,{b:1,s:24,c:INK});
  plot(x=>antiFn(x)*0.48,385,585,72,BL,2.5);
  txt('반대 위상 음파 (스피커)',485,112,{b:1,s:13,c:BL});
  txt('=',625,72,{b:1,s:24,c:INK});
  plot(x=>(nFn(x)+antiFn(x))*0.48,665,885,72,'#eab308',3.5);
  txt('실내 소음 (남은 소음 '+Math.round(ratio*100)+'%)',775,112,{b:1,s:13,c:'#b45309'});

  // 도로 배경
  ctx.fillStyle='#94a3b8';ctx.fillRect(35,345,930,68);
  ln(55,380,945,380,'#f8fafc',3,[28,18]);

  // SUV 자동차 차체 실루엣
  ctx.fillStyle='#1e3a5f';ctx.strokeStyle='#0f172a';ctx.lineWidth=3;
  ctx.beginPath();
  ctx.moveTo(155,335);
  ctx.lineTo(165,265);
  ctx.lineTo(275,245);
  ctx.lineTo(380,165);
  ctx.lineTo(715,165);
  ctx.lineTo(785,235);
  ctx.lineTo(815,335);
  ctx.closePath();ctx.fill();ctx.stroke();

  // 자동차 실내 창문 (내부 파형이 보이는 영역)
  ctx.fillStyle='#0f172a';
  ctx.beginPath();
  ctx.moveTo(392,178);ctx.lineTo(702,178);ctx.lineTo(755,238);ctx.lineTo(315,238);
  ctx.closePath();ctx.fill();

  // 실내 공간 속 파동 중첩 시각화 (x = 340 .. 730, y = 208)
  ctx.save();ctx.globalAlpha=0.65;
  plot(x=>nFn(x)*0.45,340,725,208,RD,2);
  if(on)plot(x=>antiFn(x)*0.45,340,725,208,'#38bdf8',2);
  ctx.restore();
  plot(x=>(nFn(x)+antiFn(x))*0.45,340,725,208,'#facc15',3.2);

  // 바퀴 2개 (회전 애니메이션)
  [275,695].forEach(wx=>{
   dot(wx,338,42,'#0f172a');dot(wx,338,28,'#cbd5e1');dot(wx,338,8,'#334155');
   for(let k=0;k<5;k++){
    const ang=T*5+k*Math.PI*2/5;
    ln(wx,338,wx+26*Math.cos(ang),338+26*Math.sin(ang),'#475569',3);
   }
  });

  // 마이크 → 디지털 신호 처리기(DSP) → 스피커
  dot(320,282,16,'#1e293b');txt('마이크',262,282,{b:1,s:13,c:'#ffffff'});
  ctx.fillStyle='#10b981';ctx.fillRect(435,292,36,28);txt('DSP',453,306,{b:1,s:11,c:'#0f172a'});
  txt('디지털 신호 처리기',453,332,{b:1,s:12.5,c:'#a7f3d0'});
  dot(590,262,18,'#1e293b');txt('스피커',642,262,{b:1,s:13,c:'#ffffff'});

  // 신호 전달 점선
  ln(336,282,435,306,'#38bdf8',2,[4,4]);
  ln(471,306,590,280,'#38bdf8',2,[4,4]);

  txt('그림 Ⅲ-25  자동차 내부의 능동 소음 제어 (마이크가 노면·엔진 소음을 감지해 스피커로 반대 위상 음파를 내보냄)',500,438,{b:1,s:13.5,c:INK});
 } else {
  // [파형 상세 실험] 3단 파형 비교
  [[95,'외부 소음 (마이크가 감지한 곡선 파동)',nFn,SUB],[215,'이어폰·스피커가 만든 반대 위상 소리',antiFn,RD],[355,'귀에 들리는 소리 (합성파)',x=>nFn(x)+antiFn(x),BL]].forEach(r=>{
   ln(160,r[0],960,r[0],'#e2e8f0',1);txt(r[1],20,r[0]-60,{a:'left',b:1,s:13,c:r[3]});plot(r[2],160,960,r[0],r[3],r[3]===BL?3.2:2.4);
  });
  txt('남은 소음의 크기: 원래의 '+Math.round(ratio*100)+'%',W-30,442,{a:'right',b:1,s:17,c:ratio<0.2?GN:(ratio<0.7?OR:RD)});
 }

 $('step').innerHTML=S3.irr?'<b>불규칙한 소음</b>은 파형이 계속 바뀌어, 마이크가 감지한 뒤 반대 위상 소리를 만드는 사이(지연)에 이미 소음이 달라집니다. 그래서 완전히 지우기 어렵고 규칙적인 소음(엔진음·비행기 소음 등)을 더 잘 줄입니다.':(!on?'소음 제어(ANC)를 끄면 외부 소음이 상쇄되지 않고 그대로 들립니다.':(Math.abs(+$('p3').value-180)<1&&Math.abs(a-1)<0.01?'소음과 <b>진동수·진폭이 같고 위상이 반대(180°)</b>인 음파를 발생시켜 <b>상쇄 간섭</b>으로 소음을 제거합니다!':'위 슬라이더로 <b>반대 파동 진폭(1배)</b>과 <b>위상차(180°)</b>를 조절해 소음이 완전히 상쇄되는 조건을 찾아보세요.'));
}
document.querySelectorAll('[data-m3]').forEach(b=>b.onclick=()=>{
 S3.mode=+b.dataset.m3;
 document.querySelectorAll('[data-m3]').forEach(x=>x.classList.toggle('on',x===b));
});
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
function go(i){tab=i;paused=false;$('pp').textContent='⏸ 일시정지';[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));for(let k=0;k<TABS.length;k++)$('c'+k).classList.toggle('show',k===i);
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];if(S2.snd&&i!==3)stopSnd2();if(SP.snd&&i!==4)stopSndP();if(S3.snd&&i!==5)$('snd3').click();T=0;S0.t=0}
function frame(now){requestAnimationFrame(frame);const dt=Math.max(0,Math.min(0.05,(now-last)/1000))*speed;last=now;if(!paused)T+=dt;try{[sceneLong,scene0,scene1,scene2,scenePath,scene3,scene4][tab](paused?0:dt);}catch(e){console.error(e);}}
go(0);requestAnimationFrame(frame);
</script></body></html>"""


if __name__ == "__main__":
    run_sim()

