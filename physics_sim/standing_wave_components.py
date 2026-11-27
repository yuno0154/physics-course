import base64
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """정상파와 악기(5차시) — 학습지 A~D 순서의 탭형 시뮬레이션.
    ① 정상파 만들기(두 파동이 만나는 과정 → T/4 간격 그림 → 계속 관찰, 위치별 탐침으로 배·마디 확인) → ② 현악기의 정상파(n, 길이, 장력, 소리) → ③ 관악기의 정상파(열린/막힌 관, 공기 입자)
    → ④ 공명으로 소리의 속력 측정(유리관 물 높이, 위치 기록) → ⑤ 물병 악기 → ⑥ 3D 공명 실험실
    (⑥은 standing_wave_3d_lab.html을 그대로 iframe으로 띄우며 Three.js·Tailwind CDN을 사용)
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS로 동작(소리는 브라우저 Web Audio).
    """
    st.title("🎸 정상파와 악기")
    lab = (Path(__file__).parent / "standing_wave_3d_lab.html").read_bytes()
    components.html(HTML.replace("__LAB3D_B64__", base64.b64encode(lab).decode("ascii")), height=1080, scrolling=True)


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
<h1>🎸 정상파와 악기</h1>
<p class="lead">5차시 학습지 A~D 순서의 시뮬레이션입니다. 화면의 진동은 실제보다 매우 느리게 나타냈고, 진동수는 실제 값으로 계산합니다. 🔊 버튼을 누르면 그 진동수의 소리가 납니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="st">T/4씩 넘기기 ▶|</button></div>
<div class="tabs" id="tabs"></div>
<div id="c0" class="ctrl view" style="flex-direction:column;align-items:stretch;gap:6px">
 <div style="display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center">
  <span class="grp">보기</span>
  <button class="btn on" data-m0="0">🎬 두 파동이 만나는 과정</button><button class="btn" data-m0="1">📸 T/4 간격으로 보기</button><button class="btn" data-m0="2">🔁 정상파 계속 관찰</button>
  <button class="btn go" id="rst0">⟲ 처음부터</button>
  <label class="grp"><input type="checkbox" id="trav" checked> 두 진행파 따로</label><label class="grp"><input type="checkbox" id="ovl" checked> 합성파에 겹쳐</label><label class="grp"><input type="checkbox" id="env" checked> 배·마디 표시</label>
 </div>
 <div style="display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;border-top:1px dashed var(--line);padding-top:6px">
  <span class="grp" style="color:#7c3aed">📍 탐침 위치 <i>x</i></span><input type="range" id="px0" min="0" max="72" step="1" value="12" style="width:260px"><span class="val" id="vpx0" style="min-width:90px"></span>
  <button class="btn" id="toN">◆ 가까운 마디로</button><button class="btn" id="toA">◇ 가까운 배로</button>
  <span class="grp" style="color:var(--sub);font-weight:500">그림 위를 클릭·드래그해도 탐침이 움직입니다.</span>
 </div></div>
<div id="c1" class="ctrl view">
 <div class="grp">진동 <i>n</i><input type="range" id="n1" min="1" max="6" step="1" value="1"><span class="val" id="vn1"></span></div>
 <div class="grp">줄의 길이<input type="range" id="l1" min="0.3" max="0.8" step="0.01" value="0.65"><span class="val" id="vl1"></span></div>
 <div class="grp">줄의 장력(→ 속력)<input type="range" id="v1" min="250" max="600" step="1" value="429"><span class="val" id="vv1"></span></div>
 <button class="btn" id="s1">🔊 소리</button></div>
<div id="c2" class="ctrl view">
 <button class="btn on" id="op">양쪽 끝이 열린 관</button><button class="btn" id="cl">한쪽 끝이 막힌 관</button>
 <div class="grp">진동<input type="range" id="n2" min="1" max="5" step="1" value="1"><span class="val" id="vn2"></span></div>
 <div class="grp">관의 길이<input type="range" id="l2" min="0.17" max="0.68" step="0.01" value="0.34"><span class="val" id="vl2"></span></div>
 <button class="btn" id="s2">🔊 소리</button></div>
<div id="c3" class="ctrl view">
 <div class="grp">스마트 기기 진동수<input type="range" id="f3" min="400" max="900" step="1" value="647"><span class="val" id="vf3"></span></div>
 <button class="btn" id="f3_500">500 Hz로 설정</button>
 <div class="grp">수면까지 거리 <i>y</i><input type="range" id="y3" min="0.02" max="0.9" step="0.002" value="0.05"><span class="val" id="vy3"></span></div>
 <button class="btn" id="rec">📌 이 위치 기록</button><button class="btn" id="clr">기록 지우기</button><button class="btn" id="s3">🔊 소리</button></div>
<div id="c4" class="ctrl view"><span class="grp">병을 클릭하면 소리가 납니다. 슬라이더로 물 높이를 바꾸세요.</span>
 <span id="bw"></span></div>
<div class="card" id="cvcard"><canvas id="cv" width="1000" height="460"></canvas></div>
<div id="lab3d" style="display:none"><iframe id="if3d" title="3D 공명 실험실" style="width:100%;height:780px;border:0;border-radius:18px;background:#0f172a" allow="fullscreen"></iframe></div>
<div class="step" id="step"></div><div class="note" id="note"></div>
</div>
<script>
const $=id=>document.getElementById(id),cv=$('cv'),ctx=cv.getContext('2d'),W=1000;let H=460;
const PER=[4,2.5,2.5,2.5,1,1]; // 탭별 화면 진동 주기(초, 1× 기준)
const BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',INK='#0f172a',SUB='#64748b',OR='#ea580c',VS=340;
const TABS=[['① 정상파 만들기','A','반대 방향으로 진행하는 두 파동이 겹치면 제자리에서 진동하는 정상파가 생깁니다. 마디 사이 거리는 반 파장입니다.'],
['② 현악기의 정상파','B','양 끝이 마디인 정상파만 생깁니다: l = nλₙ/2, fₙ = v/λₙ = nv/(2l). 줄이 짧을수록, 팽팽할수록 높은 소리가 납니다.'],
['③ 관악기의 정상파','C','열린 끝은 배, 막힌 끝은 마디입니다. 양 끝이 열린 관 fₙ = (2n)v/(4l), 한쪽 끝이 막힌 관 fₙ = (2n−1)v/(4l) (n = 1, 2, 3, …).'],
['④ 공명으로 소리의 속력 측정','D','이웃한 두 공명 위치의 차는 반 파장입니다: v = fλ = 2f(y₂ − y₁).'],
['⑤ 물병 악기','C②','병 속 공기 기둥(한쪽이 막힌 관)이 짧을수록 높은 소리가 납니다: f = v/(4l).'],
['⑥ 3D 공명 실험실','D','3D 가상 실험실에서 투명 필름 관의 높이를 바꾸며 공명 위치를 찾고, 정상파로 음파의 진행 속력을 측정합니다. (인터넷 연결 필요)']];
let tab=0,paused=false,speed=0.5,last=performance.now(),T=0;
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};
$('st').onclick=()=>{paused=true;$('pp').textContent='▶ 재생';const q=PER[tab]/4;T=(Math.round(T/q+1e-6)+1)*q};
function txt(s,x,y,o){o=o||{};ctx.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Malgun Gothic",sans-serif';ctx.fillStyle=o.c||INK;ctx.textAlign=o.a||'center';ctx.textBaseline='middle';ctx.fillText(s,x,y)}
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function head(x,y,dx,dy,c){const a=Math.atan2(dy,dx);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x,y);ctx.lineTo(x-9*Math.cos(a-0.4),y-9*Math.sin(a-0.4));ctx.lineTo(x-9*Math.cos(a+0.4),y-9*Math.sin(a+0.4));ctx.fill()}
function arr(x0,y0,x1,y1,c){ln(x0,y0,x1,y1,c,2.5);head(x1,y1,x1-x0,y1-y0,c)}
function dbl(x0,y0,x1,y1,c){ln(x0,y0,x1,y1,c,2);head(x1,y1,x1-x0,y1-y0,c);head(x0,y0,x0-x1,y0-y1,c)}
function dot(x,y,r,c){ctx.beginPath();ctx.fillStyle=c;ctx.arc(x,y,r,0,7);ctx.fill()}
function plot(f,x0,x1,y0,c,w,dash){ctx.beginPath();ctx.setLineDash(dash||[]);ctx.strokeStyle=c;ctx.lineWidth=w||2;for(let x=x0;x<=x1;x+=2){const y=y0-f(x);x===x0?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke();ctx.setLineDash([])}
function clear(){ctx.clearRect(0,0,W,H)}
// audio
let AC=null,osc=null,gn=null,sndOn=false;
function tone(f){if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();if(!osc){osc=AC.createOscillator();gn=AC.createGain();osc.type='triangle';gn.gain.value=0.07;osc.connect(gn).connect(AC.destination);osc.start()}osc.frequency.setTargetAtTime(f,AC.currentTime,0.02)}
function stop(){if(osc){osc.stop();osc=null}}
function beep(f,dur){tone(f);setTimeout(()=>{if(!sndOn)stop()},dur||700)}
// ===== tab0 : 정상파 만들기 (교과서 그림 III-29 표기: 빨강 y₁ 오른쪽 진행, 파랑 y₂ 왼쪽 진행, 초록 합성파)
const X0=60,X1=940,LAM=(X1-X0)/3,K=2*Math.PI/LAM,P0=PER[0],VP=LAM/P0,NA='#b45309',ND='#334155';
let m0=0;
// m0=0(만나는 과정)에서는 t=0에 두 파동이 양 끝에서 출발: 파면을 지나지 않은 곳은 아직 변위 0
function y1f(x,t,A){if(m0===0&&(t<0||x-X0>VP*t))return 0;return A*Math.sin(K*(x-X0)-2*Math.PI*t/P0)}
function y2f(x,t,A){if(m0===0&&(t<0||X1-x>VP*t))return 0;return A*Math.sin(K*(x-X0)+2*Math.PI*t/P0)}
function pxX(){return X0+(+$('px0').value)*LAM/24}
function lamTxt(v){const q=v/24;return (Math.abs(q-Math.round(q*4)/4)<1e-9?q.toFixed(2):q.toFixed(3))+' λ'}
function kind(x){const s=Math.abs(Math.sin(K*(x-X0)));return s<0.02?['마디','진폭 0 · 두 파동이 항상 상쇄 간섭',ND,s]:s>0.98?['배','진폭 2A · 두 파동이 항상 보강 간섭',NA,s]:['배와 마디 사이','진폭 '+(2*s).toFixed(2)+'A (0과 2A 사이)',PU,s]}
const sgn=v=>Math.abs(v)<0.005?'0.00':(v>0?'+':'−')+Math.abs(v).toFixed(2);
function scene0(){
 $('vpx0').textContent='x = '+lamTxt(+$('px0').value);
 if(m0===1)return snap0();
 clear();
 const sep=$('trav').checked,ovl=$('ovl').checked,env=$('env').checked,t=T,A1=24,A=32,PX=pxX();
 let oL=X0,oR=X1;if(m0===0){oL=Math.max(X0,X1-VP*t);oR=Math.min(X1,X0+VP*t)}
 const met=oR>oL,full=oL<=X0&&oR>=X1;
 const r1=58,r2=140,rs=sep?292:170;
 if(sep){
  [[r1,'y₁ : 오른쪽으로 진행하는 파동',x=>y1f(x,t,A1),RD,1],[r2,'y₂ : 왼쪽으로 진행하는 파동',x=>y2f(x,t,A1),BL,-1]].forEach(r=>{
   ln(X0,r[0],X1,r[0],'#e2e8f0',1);txt(r[1],r[4]>0?X0:X1,r[0]-A1-12,{a:r[4]>0?'left':'right',b:1,s:13,c:r[3]});plot(r[2],X0,X1,r[0],r[3],2.4);
   if(r[4]>0)arr(X0+250,r[0]-A1-12,X0+300,r[0]-A1-12,r[3]);else arr(X1-250,r[0]-A1-12,X1-300,r[0]-A1-12,r[3]);
   if(m0===0){const xf=r[4]>0?X0+VP*t:X1-VP*t;if(xf>X0&&xf<X1){ln(xf,r[0]-A1-2,xf,r[0]+A1+2,r[3],1,[3,3]);txt('파면',xf,r[0]+A1+10,{s:11,c:r[3],b:1})}}
  });
 }
 ln(X0,rs,X1,rs,'#cbd5e1',1.5);
 txt('합성파  y = y₁ + y₂',X0,rs-2*A-36,{a:'left',b:1,s:14,c:GN});
 if(ovl)txt('빨강 점선 y₁ · 파랑 점선 y₂ · 초록 실선 y₁+y₂',X0+170,rs-2*A-36,{a:'left',s:12,c:SUB});
 if(m0===0&&met&&!full){ctx.fillStyle='rgba(5,150,105,0.08)';ctx.fillRect(oL,rs-2*A-14,oR-oL,4*A+28);txt('두 파동이 겹친 구간',(oL+oR)/2,rs+2*A+6,{s:11.5,c:GN,b:1})}
 if(env&&met){
  ctx.save();ctx.beginPath();ctx.rect(oL,0,oR-oL,H);ctx.clip();
  plot(x=>2*A*Math.abs(Math.sin(K*(x-X0))),X0,X1,rs,'#a7f3d0',1.5,[4,4]);plot(x=>-2*A*Math.abs(Math.sin(K*(x-X0))),X0,X1,rs,'#a7f3d0',1.5,[4,4]);ctx.restore();
  for(let m=0;m<=6;m++){const xn=X0+m*LAM/2;if(xn<oL-1||xn>oR+1)continue;dot(xn,rs,5,ND);txt('마디',xn,rs+18,{s:11,c:ND,b:1})}
  for(let m=0;m<6;m++){const xa=X0+LAM/4+m*LAM/2;if(xa<oL||xa>oR)continue;txt('배',xa,rs-2*A-12,{s:11.5,c:NA,b:1})}
  if(full){dbl(X0,rs+2*A+14,X0+LAM/2,rs+2*A+14,GN);txt('마디 사이 = 반 파장 (λ/2)',X0+LAM/4+40,rs+2*A+28,{s:11.5,c:GN,b:1})}
 }
 if(ovl){plot(x=>y1f(x,t,A),X0,X1,rs,'rgba(225,29,72,0.8)',2,[6,4]);plot(x=>y2f(x,t,A),X0,X1,rs,'rgba(37,99,235,0.8)',2,[6,4])}
 plot(x=>y1f(x,t,A)+y2f(x,t,A),X0,X1,rs,GN,3.6);
 // 탐침
 const a1=y1f(PX,t,1),a2=y2f(PX,t,1),K0=kind(PX);
 ln(PX,sep?r1-A1-4:rs-2*A-18,PX,rs+2*A+4,PU,1.5,[5,4]);
 if(sep){dot(PX,r1-a1*A1,4.5,RD);dot(PX,r2-a2*A1,4.5,BL)}
 if(ovl){dot(PX,rs-a1*A,3.5,RD);dot(PX,rs-a2*A,3.5,BL)}
 dot(PX,rs-(a1+a2)*A,6.5,PU);ctx.beginPath();ctx.fillStyle='#fff';ctx.arc(PX,rs-(a1+a2)*A,2.5,0,7);ctx.fill();
 // 아래: 탐침 위치의 변위-시간 그래프
 const gx0=X0,gx1=640,gy=490,gs=22,tw=2*P0;
 txt('📍 탐침 위치에서 시간에 따른 변위 (최근 2T)',gx0,418,{a:'left',b:1,s:13,c:PU});
 ctx.fillStyle='#faf5ff';ctx.fillRect(gx0,gy-2*gs-10,gx1-gx0,4*gs+20);
 [2,-2].forEach(q=>{ln(gx0,gy-q*gs,gx1,gy-q*gs,'#e9d5ff',1,[3,4]);txt((q>0?'+':'−')+'2A',gx0-6,gy-q*gs,{a:'right',s:11,c:SUB})});
 ln(gx0,gy,gx1,gy,'#cbd5e1',1);txt('0',gx0-6,gy,{a:'right',s:11,c:SUB});
 const gt=(fy,c,w)=>{ctx.beginPath();ctx.strokeStyle=c;ctx.lineWidth=w;for(let px=gx0;px<=gx1;px+=2){const tt=t-tw+(px-gx0)/(gx1-gx0)*tw,yy=gy-fy(tt)*gs;px===gx0?ctx.moveTo(px,yy):ctx.lineTo(px,yy)}ctx.stroke()};
 gt(tt=>y1f(PX,tt,1),'rgba(225,29,72,0.35)',1.2);gt(tt=>y2f(PX,tt,1),'rgba(37,99,235,0.35)',1.2);gt(tt=>y1f(PX,tt,1)+y2f(PX,tt,1),PU,2.6);
 dot(gx1,gy-(a1+a2)*gs,5,PU);txt('지금',gx1,gy+2*gs+20,{s:11,c:SUB});txt('← 과거',gx0+30,gy+2*gs+20,{s:11,c:SUB});
 // 판독
 const rx=680;let st,stc;
 const arr1=m0!==0||PX-X0<=VP*t,arr2=m0!==0||X1-PX<=VP*t;
 if(arr1&&arr2){st=K0[0];stc=K0[2]}else if(arr1||arr2){st=(arr1?'y₁':'y₂')+'만 도착';stc=arr1?RD:BL}else{st='아직 파동이 오지 않음';stc=SUB}
 txt('x = '+lamTxt(+$('px0').value),rx,428,{a:'left',b:1,s:15});
 txt(st,rx,456,{a:'left',b:1,s:19,c:stc});
 txt(arr1&&arr2?K0[1]:(arr1||arr2?'한 파동만 있어 진폭 A로 진동':'변위 0으로 정지'),rx,482,{a:'left',s:12.5,c:SUB});
 txt('y₁ = '+sgn(a1)+'A   y₂ = '+sgn(a2)+'A',rx,508,{a:'left',s:13.5});
 txt('y = y₁ + y₂ = '+sgn(a1+a2)+'A',rx,532,{a:'left',b:1,s:14.5,c:PU});
 txt('t = '+(t/P0).toFixed(2)+' T',W-24,22,{a:'right',b:1,s:14});
 let s;
 if(m0===0){
  const tm=1.5*P0;
  s=!met?'<b>1단계</b> · 두 파동이 양 끝에서 서로를 향해 진행합니다. 아직 만나지 않았으므로 각 파동은 모양을 유지하며 그대로 나아갑니다.'
   :!full?'<b>2단계</b> · 두 파동이 만나 <b style="color:#059669">겹친 구간</b>에서 중첩이 일어납니다. 겹친 구간 안에서는 파형이 옆으로 진행하지 않고 <b>제자리에서 진동</b>하며, 그 구간이 점점 넓어집니다. 탐침을 마디에 두고 그래프를 보세요. 한 파동만 왔을 때는 진동하다가 두 파동이 만나면 멈춥니다.'
   :'<b>3단계</b> · 두 파동이 줄 전체에서 겹쳐 <b>정상파가 완성</b>되었습니다. <b>마디</b>는 항상 정지(상쇄 간섭), <b>배</b>는 진폭 2A로 진동(보강 간섭)합니다. 이웃한 마디 사이는 λ/2입니다.';
 }else s='합성파는 옆으로 진행하지 않고 제자리에서 진동합니다. 탐침을 움직이며 위치에 따라 진폭이 어떻게 달라지는지 확인하세요. 진폭은 <b>2A|sin(2πx/λ)|</b>로, 마디(x = 0, λ/2, λ, …)에서 0, 배(x = λ/4, 3λ/4, …)에서 2A입니다.';
 $('step').innerHTML=s;
}
const QL=['0','¼T','½T','¾T','T'];
function snap0(){clear();
 const PX=pxX(),A=19,c0=84,gap=104;
 arr(X0,16,X0+46,16,RD);txt('진행 방향 (y₁)',X0+54,16,{a:'left',s:12,c:RD,b:1});
 arr(X1,16,X1-46,16,BL);txt('진행 방향 (y₂)',X1-54,16,{a:'right',s:12,c:BL,b:1});
 if($('env').checked){
  for(let m=0;m<=6;m++){const xn=X0+m*LAM/2;ln(xn,46,xn,c0+4*gap+2*A+6,'#cbd5e1',1,[3,4]);txt('마디',xn,38,{s:11,c:ND,b:1})}
  for(let m=0;m<6;m++){const xa=X0+LAM/4+m*LAM/2;ln(xa,46,xa,c0+4*gap+2*A+6,'#fde68a',1,[3,4]);txt('배',xa,38,{s:11.5,c:NA,b:1})}
 }
 const per=P0/4;let live=-1;
 for(let i=0;i<5;i++){const yc=c0+i*gap,ti=i*per,done=T>=ti-1e-6;if(!done&&live<0)live=i;
  ctx.strokeStyle=done?'#cbd5e1':(i===live?'#c4b5fd':'#eef2f7');ctx.lineWidth=1;ctx.strokeRect(X0,yc-2*A-8,X1-X0,4*A+16);
  ln(X0,yc,X1,yc,'#e2e8f0',1);
  if(done||i===live){const tt=done?ti:T;
   plot(x=>y2f(x,tt,A),X0,X1,yc,BL,2);plot(x=>y1f(x,tt,A),X0,X1,yc,RD,2,[6,4]);plot(x=>y1f(x,tt,A)+y2f(x,tt,A),X0,X1,yc,GN,3);
   const yp=y1f(PX,tt,1)+y2f(PX,tt,1);dot(PX,yc-yp*A,5.5,PU);
   txt('t = '+(done?QL[i]:(T/P0).toFixed(2)+'T'),X1+8,yc-8,{a:'left',b:1,s:13,c:done?INK:PU});
   txt('y='+sgn(yp)+'A',X1+8,yc+12,{a:'left',s:11,c:PU});
  }else txt('t = '+QL[i],X1+8,yc,{a:'left',s:13,c:'#cbd5e1'});
 }
 ln(PX,46,PX,c0+4*gap+2*A+6,PU,1.5,[5,4]);
 const done=T>=P0-1e-6;
 $('step').innerHTML=(done?'':'<b>T/4씩 넘기기 ▶|</b>를 누르거나 재생하면 한 칸씩 채워집니다. ')+'<b>t = 0, ½T, T</b>에는 두 파동이 같은 위상으로 겹쳐 합성파의 진폭이 <b>2A</b>가 되고, <b>t = ¼T, ¾T</b>에는 반대 위상이 되어 줄 전체의 변위가 <b>0</b>이 됩니다. 탐침(보라 점)을 배에 두면 +2A → 0 → −2A → 0 → +2A, 마디에 두면 항상 0입니다. (교과서 그림 Ⅲ-29)';
}
document.querySelectorAll('[data-m0]').forEach(b=>b.onclick=()=>{m0=+b.dataset.m0;document.querySelectorAll('[data-m0]').forEach(x=>x.classList.toggle('on',x===b));T=0;if(m0!==2&&paused){paused=false;$('pp').textContent='⏸ 일시정지'}});
$('rst0').onclick=()=>{T=0;paused=false;$('pp').textContent='⏸ 일시정지'};
$('toN').onclick=()=>{const v=+$('px0').value;$('px0').value=Math.round(v/12)*12};
$('toA').onclick=()=>{const v=+$('px0').value;$('px0').value=Math.min(66,Math.max(6,Math.round((v-6)/12)*12+6))};
let drag0=false;
function setPX(e){const r=cv.getBoundingClientRect(),x=(e.clientX-r.left)*W/r.width;$('px0').value=Math.max(0,Math.min(72,Math.round((x-X0)/(LAM/24))))}
cv.addEventListener('pointerdown',e=>{if(tab!==0)return;drag0=true;setPX(e);try{cv.setPointerCapture(e.pointerId)}catch(_){}});
cv.addEventListener('pointermove',e=>{if(drag0)setPX(e)});
['pointerup','pointercancel'].forEach(ev=>cv.addEventListener(ev,()=>drag0=false));
// ===== tab1 string (교과서 그림 Ⅲ-30 표기)
const SUBN='₀₁₂₃₄₅₆₇₈₉',sb=n=>String(n).split('').map(d=>SUBN[+d]).join(''),STR='#e4572e';
function nName(n){return n===1?'기본 진동':n+'배 진동'}
function f1(){return (+$('n1').value)*(+$('v1').value)/(2*(+$('l1').value))}
function scene1(){clear();const n=+$('n1').value,L=+$('l1').value,v=+$('v1').value,f=f1(),lamn=2*L/n;
 $('vn1').textContent='n = '+n+' ('+nName(n)+')';$('vl1').textContent=L.toFixed(2)+' m';$('vv1').textContent=v+' m/s';
 const x0=100,x1=100+L/0.8*800,y=170,A=60,ph=Math.cos(2*Math.PI*T/PER[1]),sh=x=>Math.sin(n*Math.PI*(x-x0)/(x1-x0));
 ctx.fillStyle='#9ca3af';ctx.fillRect(x0-16,y-85,16,170);ctx.fillRect(x1,y-85,16,170);
 dbl(x0,y-100,x1,y-100,SUB);txt('l = '+L.toFixed(2)+' m',(x0+x1)/2,y-114,{s:13,b:1});
 plot(x=>A*Math.abs(sh(x)),x0,x1,y,'#fdba74',1.4,[3,4]);plot(x=>-A*Math.abs(sh(x)),x0,x1,y,'#fdba74',1.4,[3,4]);
 for(let m=0;m<n;m++){const xa=x0+(m+0.5)*(x1-x0)/n;dbl(xa,y-A+6,xa,y+A-6,BL);txt('배',xa,y-A-12,{s:11,c:NA,b:1})}
 plot(x=>A*sh(x)*ph,x0,x1,y,STR,3);
 for(let m=0;m<=n;m++){const xn=x0+m*(x1-x0)/n;dot(xn,y,5,ND);txt('마디',xn,y+A+14,{s:11,c:ND,b:1})}
 txt((n===1?'l = λ₁/2':'l = '+n+' × λ'+sb(n)+'/2')+'   ('+nName(n)+')',(x0+x1)/2,y+A+42,{s:15,b:1,c:STR});
 const rows=[['파장  λₙ = 2l/n',lamn.toFixed(3)+' m'],['진동수  fₙ = v/λₙ = nv/(2l)',f.toFixed(0)+' Hz'],['기본 진동수  f₁ = v/(2l)',(v/(2*L)).toFixed(0)+' Hz  (fₙ = '+n+' × f₁)']];
 rows.forEach((r,i)=>{const yy=345+i*32;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(100,yy-14,800,28);txt(r[0],120,yy,{a:'left',s:15,b:1});txt(r[1],880,yy,{a:'right',s:16,b:1,c:BL})});
 if(sndOn&&tab===1)tone(f);
 $('step').innerHTML='줄의 양 끝(고정)은 항상 <b>마디</b>입니다. 그래서 줄 길이에 반 파장이 <b>정수 개</b> 들어가는 정상파만 생깁니다: l = n·λₙ/2. 줄을 <b>짧게</b> 하거나(손가락으로 누르기) <b>팽팽하게</b> 하면(속력 증가) 진동수가 커져 높은 소리가 납니다.';}
// ===== tab2 pipe (교과서 그림 Ⅲ-33 표기: 왼쪽이 부는 쪽, 막힌 관은 오른쪽 끝이 막힘)
let closed=false;
function f2(){const n=+$('n2').value,L=+$('l2').value;return closed?(2*n-1)*VS/(4*L):(2*n)*VS/(4*L)}
function lfrac(m){const g=m%4===0?4:(m%2===0?2:1),a=4/g,b=m/g;return b===1?(a===1?'l':a+'l'):(a===1?'l/'+b:a+'/'+b+' l')}
function scene2(){clear();const n=+$('n2').value,L=+$('l2').value,f=f2(),m=closed?2*n-1:2*n;
 $('vn2').textContent='n = '+n+' ('+nName(n)+')';$('vl2').textContent=L.toFixed(2)+' m';
 const x0=100,x1=100+L/0.68*800,y=150,hh=66,l=x1-x0;
 ln(x0,y-hh,x1,y-hh,INK,3);ln(x0,y+hh,x1,y+hh,INK,3);if(closed)ln(x1,y-hh,x1,y+hh,INK,7);
 ctx.fillStyle='#fbbf24';ctx.beginPath();ctx.moveTo(x0-34,y+hh);ctx.lineTo(x0-2,y+hh);ctx.lineTo(x0-2,y+hh-34);ctx.closePath();ctx.fill();txt('부는 쪽',x0-20,y+hh+16,{s:11,c:SUB});
 const env=x=>Math.cos(m*Math.PI*(x-x0)/(2*l));
 for(let r=0;r<7;r++)for(let i=0;i<=60;i++){const xe=x0+i*l/60;const dx=13*env(xe)*Math.cos(2*Math.PI*T/PER[2]);const yy=y-hh+12+r*(2*hh-24)/6;dot(xe+dx,yy,2.2,'#94a3b8')}
 plot(x=>(hh-8)*env(x),x0,x1,y,STR,1.8);plot(x=>-(hh-8)*env(x),x0,x1,y,STR,1.8,[5,4]);
 const node=[],anti=[];for(let i=0;i<=400;i++){const xe=x0+i*l/400,e=Math.abs(env(xe));if(e<0.012)node.push(xe);if(e>0.995)anti.push(xe)}
 const uniq=a=>a.filter((v,i)=>i===0||v-a[i-1]>8);uniq(node).forEach(xn=>{txt('마디',xn,y+hh+16,{s:11,c:ND,b:1})});uniq(anti).forEach(xa=>{txt('배',xa,y-hh-14,{s:11,c:NA,b:1})});
 dbl(x0,y-hh-34,x1,y-hh-34,SUB);txt('l = '+L.toFixed(2)+' m',(x0+x1)/2,y-hh-48,{s:13,b:1});
 txt('λ'+sb(n)+' = '+lfrac(m)+'   ('+nName(n)+(closed&&n>1?', 진동수는 '+m+'f₁':'')+')',(x0+x1)/2,y+hh+42,{s:15,b:1,c:STR});
 const lamn=4*L/m,k=closed?'(2n−1)':'(2n)';
 const rows=[['파장  λₙ = 4l/'+k,lamn.toFixed(3)+' m'],['진동수  fₙ = v/λₙ = '+k+'v/(4l)',f.toFixed(0)+' Hz  (= '+(closed?m:n)+' × f₁)'],['가능한 진동수',closed?'f₁, 3f₁, 5f₁, … (홀수 배만)':'f₁, 2f₁, 3f₁, … (모든 정수 배)']];
 rows.forEach((r,i)=>{const yy=345+i*32;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(100,yy-14,800,28);txt(r[0],120,yy,{a:'left',s:15,b:1});txt(r[1],880,yy,{a:'right',s:16,b:1,c:BL})});
 if(sndOn&&tab===2)tone(f);
 $('step').innerHTML='점(●)은 관 속 공기 입자입니다. 공기는 관을 따라 <b>앞뒤로</b> 진동하지만(종파), 진동 범위를 주황 선(횡파 모양)으로 나타냈습니다. '+(closed?'<b>막힌 끝은 공기가 움직이지 못해 마디</b>, 열린 끝은 배입니다. 그래서 l = (λₙ/4)(2n−1), 즉 관 길이가 λ/4의 <b>홀수 배</b>인 정상파만 생깁니다.':'<b>열린 양 끝은 모두 배</b>입니다. l = (λₙ/4)(2n), 즉 관 길이가 λ/4의 짝수 배(λ/2의 정수 배)인 정상파가 생깁니다.')+' <span style="color:#64748b">(여기서 배·마디는 <b>공기 입자의 변위</b> 기준입니다. 압력 변화는 반대로 변위의 마디에서 가장 크고 배에서 0입니다.)</span>';}
$('op').onclick=()=>{closed=false;$('op').classList.add('on');$('cl').classList.remove('on')};$('cl').onclick=()=>{closed=true;$('cl').classList.add('on');$('op').classList.remove('on')};
// ===== tab3 resonance tube
const REC=[];const ENDC=0.012;
function amp3(){const f=+$('f3').value,y=+$('y3').value,lam=VS/f,Le=y+ENDC;const ph=2*Math.PI*Le/lam;return Math.abs(Math.sin(ph))**8}
function scene3(){clear();const f=+$('f3').value,y=+$('y3').value,lam=VS/f;$('vf3').textContent=f+' Hz';$('vy3').textContent=y.toFixed(3)+' m';
 const tx=200,ty=40,tw=70,th=380,sc=th/0.95;
 ctx.fillStyle='#bfdbfe';ctx.fillRect(tx,ty+y*sc,tw,th-y*sc);ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.strokeRect(tx,ty,tw,th);
 ctx.fillStyle='#334155';ctx.fillRect(tx+8,ty-28,tw-16,18);txt('스마트 기기 ('+f+' Hz)',tx+tw+12,ty-19,{a:'left',s:12});
 const a=amp3();
 // 공기 기둥의 정상파는 공명 여부와 관계없이 항상 그린다(수면 = 항상 마디). 공명하지 않으면 진폭만 작다.
 {const cx=tx+tw/2,amp=(tw/2-6)*(0.2+0.8*a),ph=Math.cos(2*Math.PI*T/PER[3]),env=d=>Math.sin(2*Math.PI*(y-d)/lam),strong=a>0.85;
  for(let s of [1,-1]){ctx.beginPath();ctx.setLineDash([3,4]);ctx.strokeStyle='#cbd5e1';ctx.lineWidth=1;for(let q=0;q<=y*sc;q+=2){const xx=cx+s*amp*Math.abs(env(q/sc));q===0?ctx.moveTo(xx,ty+q):ctx.lineTo(xx,ty+q)}ctx.stroke();ctx.setLineDash([])}
  for(let s of [1,-1]){ctx.beginPath();ctx.strokeStyle=strong?(s>0?BL:'#93c5fd'):(s>0?'#60a5fa':'#bfdbfe');ctx.lineWidth=strong?2.4:1.6;for(let q=0;q<=y*sc;q+=2){const xx=cx+s*amp*env(q/sc)*ph;q===0?ctx.moveTo(xx,ty+q):ctx.lineTo(xx,ty+q)}ctx.stroke()}
  dot(cx,ty+y*sc,4,ND);}
 dbl(tx-24,ty,tx-24,ty+y*sc,RD);txt('y',tx-38,ty+y*sc/2,{s:14,b:1,c:RD});
 // meter
 const mx=360,my=60;txt('소리의 세기',mx,my-20,{a:'left',b:1,s:14});ctx.fillStyle='#e2e8f0';ctx.fillRect(mx,my,300,26);ctx.fillStyle=a>0.8?GN:(a>0.3?OR:'#94a3b8');ctx.fillRect(mx,my,300*Math.max(0.03,a),26);
 txt(a>0.85?'공명! 소리가 크게 들립니다':'',mx+310,my+13,{a:'left',b:1,s:15,c:GN});
 // records
 txt('기록한 공명 위치',mx,150,{a:'left',b:1,s:14});
 REC.forEach((r,i)=>txt('y'+(i+1)+' = '+r.toFixed(3)+' m',mx,180+i*26,{a:'left',s:14}));
 if(REC.length>=2){const d=REC[1]-REC[0];txt('λ/2 = y₂ − y₁ = '+d.toFixed(3)+' m  →  λ = '+(2*d).toFixed(3)+' m',mx,300,{a:'left',b:1,s:15,c:BL});txt('v = fλ = '+f+' × '+(2*d).toFixed(3)+' = '+(2*d*f).toFixed(0)+' m/s',mx,330,{a:'left',b:1,s:16,c:PU});
  txt('※ y₁ = '+REC[0].toFixed(3)+' m 는 λ/4 = '+(lam/4).toFixed(3)+' m 보다 조금 작습니다(입구 바깥의 배).',mx,370,{a:'left',s:12.5,c:SUB})}
 if(sndOn&&tab===3){tone(f);gn.gain.setTargetAtTime(0.02+0.12*a,AC.currentTime,0.03)}
 $('step').innerHTML='수면 거리 <b>y</b>를 천천히 늘려 소리가 크게 들리는(공명) 위치를 찾아 <b>📌 기록</b>하세요. 수면은 공기가 움직이지 못하므로 <b>마디</b>, 관 입구는 <b>배</b>입니다. 이웃한 공명 위치의 차가 반 파장입니다. 관 속 정상파는 늘 생기지만(수면은 항상 마디), 관 입구가 배 자리에 올 때만 <b>공명</b>하여 진폭이 크게 커집니다. <span style="color:#64748b">소리의 세기 막대는 관 입구에서 듣는 소리입니다. 입구가 배가 되도록 공기 기둥 전체가 공명할 때 커지고, 입구가 마디 자리에 오면(y가 λ/2의 정수 배 근처) 가장 작아집니다.</span>';}
$('rec').onclick=()=>{const y=+$('y3').value;if(REC.length<4&&!REC.some(r=>Math.abs(r-y)<0.05)){REC.push(y);REC.sort((a,b)=>a-b)}};$('clr').onclick=()=>REC.length=0;
$('f3_500').onclick=()=>{$('f3').value=500;REC.length=0};
// ===== tab4 bottles
const BW=[0.05,0.08,0.11,0.14];const BH=0.25;
function bf(i){const L=BH-BW[i];return VS/(4*L)}
function noteName(f){const n=Math.round(12*Math.log2(f/440))+57;const names=['도','도#','레','레#','미','파','파#','솔','솔#','라','라#','시'];return names[((n%12)+12)%12]+Math.floor(n/12)}
let lit=-1,litT=0;
function scene4(){clear();for(let i=0;i<4;i++){const x0=130+i*200,yb=380,hpx=260,sc=hpx/BH;
  ctx.strokeStyle=INK;ctx.lineWidth=2.2;ctx.beginPath();ctx.moveTo(x0+30,yb-hpx-40);ctx.lineTo(x0+30,yb-hpx);ctx.lineTo(x0,yb-hpx+40);ctx.lineTo(x0,yb);ctx.lineTo(x0+100,yb);ctx.lineTo(x0+100,yb-hpx+40);ctx.lineTo(x0+70,yb-hpx);ctx.lineTo(x0+70,yb-hpx-40);ctx.stroke();
  ctx.fillStyle=lit===i&&performance.now()-litT<600?'#60a5fa':'#bfdbfe';ctx.fillRect(x0+2,yb-BW[i]*sc,96,BW[i]*sc-1);
  // 공기 기둥 기본 정상파(λ/4) 시각화
  const yTop=yb-hpx-40,yWat=yb-BW[i]*sc,airH=yWat-yTop;
  for(let s of [1,-1]){
   ctx.beginPath();ctx.strokeStyle=s>0?'#2563eb':'#93c5fd';ctx.lineWidth=2;
   for(let q=0;q<=airH;q+=3){
    const env=Math.cos(Math.PI/2*(q/airH))*Math.cos(2*Math.PI*(0.5+i*0.12)*T);
    const xx=x0+50+s*18*env;
    q===0?ctx.moveTo(xx,yTop+q):ctx.lineTo(xx,yTop+q);
   }
   ctx.stroke();
  }
  const L=BH-BW[i];dbl(x0+118,yb-hpx-40,x0+118,yb-BW[i]*sc,PU);txt('공기 기둥 '+(L*100).toFixed(0)+' cm',x0+50,yb-hpx-60,{s:12,b:1,c:PU});
  txt('ABCD'[i]+' · '+bf(i).toFixed(0)+' Hz',x0+50,yb+24,{s:15,b:1,c:BL});txt('≈ '+noteName(bf(i)),x0+50,yb+46,{s:13,c:SUB})}
 $('step').innerHTML='물을 더 채우면 <b>공기 기둥(수면=마디, 입구=배)이 짧아져</b> 파장 λ = 4l이 짧아지고 진동수가 커집니다 → <b>높은 소리</b>. 병을 클릭해 소리를 비교해 보세요. (병 높이 25 cm, 입구 쪽 효과는 무시)';}
cv.addEventListener('click',e=>{if(tab!==4)return;const r=cv.getBoundingClientRect();const x=(e.clientX-r.left)*W/r.width;const i=Math.floor((x-110)/200);if(i>=0&&i<4){lit=i;litT=performance.now();beep(bf(i),600)}});
(function(){let h='';for(let i=0;i<4;i++)h+='<span class="grp">'+'ABCD'[i]+'<input type="range" data-b="'+i+'" min="0.02" max="0.2" step="0.005" value="'+BW[i]+'" style="width:90px"></span>';$('bw').innerHTML=h;document.querySelectorAll('[data-b]').forEach(s=>s.oninput=()=>{BW[+s.dataset.b]=+s.value})})();
// sound buttons
[['s1',f1],['s2',f2],['s3',()=>+$('f3').value]].forEach(([id,g])=>{$(id).onclick=()=>{sndOn=!sndOn;if(sndOn)tone(g());else stop();['s1','s2','s3'].forEach(k=>$(k).textContent=sndOn&&k===id?'🔇 끄기':'🔊 소리')}});
function go(i){tab=i;[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));for(let k=0;k<5;k++)$('c'+k).classList.toggle('show',k===i);
 const is3d=i===5;['cvcard','step'].forEach(k=>$(k).style.display=is3d?'none':'');document.querySelector('.speed').style.display=is3d?'none':'';$('lab3d').style.display=is3d?'block':'none';
 if(is3d&&!$('if3d').srcdoc){$('if3d').srcdoc=new TextDecoder().decode(Uint8Array.from(atob(LAB3D),c=>c.charCodeAt(0)))}
 if(!is3d){H=i===0?560:460;if(cv.height!==H)cv.height=H;cv.style.cursor=i===0?'ew-resize':(i===4?'pointer':'default')}
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];if(sndOn){sndOn=false;stop();['s1','s2','s3'].forEach(k=>$(k).textContent='🔊 소리')}T=0}
function frame(now){const dt=Math.min(0.05,(now-last)/1000)*speed;last=now;if(!paused)T+=dt;if(tab<5)[scene0,scene1,scene2,scene3,scene4][tab]();requestAnimationFrame(frame)}
const LAB3D='__LAB3D_B64__';
go(0);requestAnimationFrame(frame);
</script></body></html>"""


if __name__ == "__main__":
    run_sim()

