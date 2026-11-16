import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """정상파와 악기(5차시) — 학습지 A~D 순서의 탭형 시뮬레이션.
    ① 정상파 만들기(T/4씩 넘기기) → ② 현악기의 정상파(n, 길이, 장력, 소리) → ③ 관악기의 정상파(열린/막힌 관, 공기 입자)
    → ④ 공명으로 소리의 속력 측정(유리관 물 높이, 위치 기록) → ⑤ 물병 악기
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS로 동작(소리는 브라우저 Web Audio).
    """
    st.title("🎸 정상파와 악기")
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
<h1>🎸 정상파와 악기</h1>
<p class="lead">5차시 학습지 A~D 순서의 시뮬레이션입니다. 화면의 진동은 실제보다 매우 느리게 나타냈고, 진동수는 실제 값으로 계산합니다. 🔊 버튼을 누르면 그 진동수의 소리가 납니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="st">T/4씩 넘기기 ▶|</button></div>
<div class="tabs" id="tabs"></div>
<div id="c0" class="ctrl view"><label class="grp"><input type="checkbox" id="trav" checked> 두 진행파 보기</label><label class="grp"><input type="checkbox" id="env" checked> 진동 범위(배·마디) 보기</label></div>
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
<div class="card"><canvas id="cv" width="1000" height="460"></canvas></div>
<div class="step" id="step"></div><div class="note" id="note"></div>
</div>
<script>
const $=id=>document.getElementById(id),cv=$('cv'),ctx=cv.getContext('2d'),W=1000,H=460;
const BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',INK='#0f172a',SUB='#64748b',OR='#ea580c',VS=340;
const TABS=[['① 정상파 만들기','A','반대 방향으로 진행하는 두 파동이 겹치면 제자리에서 진동하는 정상파가 생깁니다. 마디 사이 거리는 반 파장입니다.'],
['② 현악기의 정상파','B','양 끝이 마디인 정상파만 생깁니다: λₙ = 2l/n, fₙ = nv/(2l). 줄이 짧을수록, 팽팽할수록 높은 소리가 납니다.'],
['③ 관악기의 정상파','C','열린 끝은 배, 막힌 끝은 마디입니다. 열린 관은 모든 정수 배, 막힌 관은 홀수 배의 진동수만 공명합니다.'],
['④ 공명으로 소리의 속력 측정','D','이웃한 두 공명 위치의 차는 반 파장입니다: v = fλ = 2f(y₂ − y₁).'],
['⑤ 물병 악기','C②','병 속 공기 기둥(한쪽이 막힌 관)이 짧을수록 높은 소리가 납니다: f = v/(4l).']];
let tab=0,paused=false,speed=0.5,last=performance.now(),T=0;
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};
$('st').onclick=()=>{paused=true;$('pp').textContent='▶ 재생';T=(Math.round(T/0.25+1e-6)+1)*0.25};
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
function sndBtn(id,getf){$(id).onclick=()=>{sndOn=!sndOn;if(sndOn){tone(getf())}else stop();document.querySelectorAll('[id^=s][id$=""]');$(id).textContent=sndOn?'🔇 끄기':'🔊 소리'}}
// ===== tab0
function scene0(){clear();const x0=60,x1=940,lam=293.3,k=2*Math.PI/lam,w=2*Math.PI*0.25,A=34;
 const fa=x=>A*Math.sin(k*(x-x0)-w*T),fb=x=>A*Math.sin(k*(x-x0)+w*T);
 if($('trav').checked){[[90,'오른쪽으로 진행하는 파동',fa,BL],[200,'왼쪽으로 진행하는 파동',fb,RD]].forEach(r=>{ln(x0,r[0],x1,r[0],'#e2e8f0',1);txt(r[1],x0,r[0]-48,{a:'left',b:1,s:13,c:r[3]});plot(r[2],x0,x1,r[0],r[3],2.2)});arr(x1-90,52,x1-20,52,BL);arr(x0+90,162,x0+20,162,RD)}
 const ys=$('trav').checked?350:240;ln(x0,ys,x1,ys,'#e2e8f0',1);txt('합성파 = 정상파',x0,ys-88,{a:'left',b:1,s:14,c:PU});
 if($('env').checked){plot(x=>2*A*Math.abs(Math.sin(k*(x-x0))),x0,x1,ys,'#ddd6fe',1.4,[4,4]);plot(x=>-2*A*Math.abs(Math.sin(k*(x-x0))),x0,x1,ys,'#ddd6fe',1.4,[4,4]);
  for(let m=0;m<=6;m++){const xn=x0+m*lam/2;if(xn>x1+1)break;dot(xn,ys,5,RD);txt('마디',xn,ys+22,{s:11,c:RD,b:1})}
  for(let m=0;m<6;m++){const xa=x0+lam/4+m*lam/2;if(xa>x1)break;txt('배',xa,ys-80,{s:11,c:BL,b:1})}
  dbl(x0,ys+44,x0+lam/2,ys+44,GN);txt('반 파장 (λ/2)',x0+lam/4,ys+58,{s:12,c:GN,b:1})}
 plot(x=>fa(x)+fb(x),x0,x1,ys,PU,3);
 const ph=((T%4)+4)%4,lab=ph<0.05||Math.abs(ph-2)<0.05?'두 파동이 같은 위상으로 겹쳐 <b>변위가 가장 큼</b>':(Math.abs(ph-1)<0.05||Math.abs(ph-3)<0.05?'두 파동이 반대 위상으로 겹쳐 <b>줄 전체가 평평</b>(변위 0)':'');
 txt('t = '+(T%4).toFixed(2)+' T',W-30,24,{a:'right',b:1,s:14});
 $('step').innerHTML=(lab?lab+' · ':'')+'정상파는 옆으로 진행하지 않고 제자리에서 진동합니다. <b>마디</b>는 두 파동이 늘 반대 위상으로 만나 항상 정지하고, <b>배</b>는 늘 같은 위상으로 만나 원래 진폭의 2배로 진동합니다. 「T/4씩 넘기기」로 학습지 그림을 확인하세요.';}
// ===== tab1 string
function f1(){return (+$('n1').value)*(+$('v1').value)/(2*(+$('l1').value))}
function scene1(){clear();const n=+$('n1').value,L=+$('l1').value,v=+$('v1').value,f=f1(),lamn=2*L/n;
 $('vn1').textContent=n+(n===1?' (기본)':'배');$('vl1').textContent=L.toFixed(2)+' m';$('vv1').textContent=v+' m/s';
 const x0=100,x1=100+L/0.8*800,y=170,A=60;
 ln(x0,y-90,x0,y+90,INK,6);ln(x1,y-90,x1,y+90,INK,6);
 plot(x=>A*Math.sin(n*Math.PI*(x-x0)/(x1-x0))*Math.cos(2*Math.PI*0.4*T),x0,x1,y,BL,3);
 plot(x=>A*Math.abs(Math.sin(n*Math.PI*(x-x0)/(x1-x0))),x0,x1,y,'#bfdbfe',1,[4,4]);plot(x=>-A*Math.abs(Math.sin(n*Math.PI*(x-x0)/(x1-x0))),x0,x1,y,'#bfdbfe',1,[4,4]);
 for(let m=0;m<=n;m++){const xn=x0+m*(x1-x0)/n;dot(xn,y,5,RD)}
 dbl(x0,y+105,x1,y+105,SUB);txt('l = '+L.toFixed(2)+' m',(x0+x1)/2,y+120,{s:13,b:1});
 const rows=[['파장  λₙ = 2l/n',lamn.toFixed(3)+' m'],['진동수  fₙ = nv/(2l)',f.toFixed(0)+' Hz'],['기본 진동수  f₁',(v/(2*L)).toFixed(0)+' Hz  (fₙ = '+n+' × f₁)']];
 rows.forEach((r,i)=>{const yy=345+i*32;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(100,yy-14,800,28);txt(r[0],120,yy,{a:'left',s:15,b:1});txt(r[1],880,yy,{a:'right',s:16,b:1,c:BL})});
 if(sndOn&&tab===1)tone(f);
 $('step').innerHTML='줄의 양 끝(고정)은 항상 <b style="color:#e11d48">마디</b>입니다. 그래서 줄 길이에 반 파장이 <b>정수 개</b> 들어가는 정상파만 생깁니다. 줄을 <b>짧게</b> 하거나(손가락으로 누르기) <b>팽팽하게</b> 하면(속력 증가) 진동수가 커져 높은 소리가 납니다.';}
// ===== tab2 pipe
let closed=false;
function f2(){const n=+$('n2').value,L=+$('l2').value;return closed?(2*n-1)*VS/(4*L):n*VS/(2*L)}
function scene2(){clear();const n=+$('n2').value,L=+$('l2').value,f=f2(),m=closed?2*n-1:n;
 $('vn2').textContent=closed?(m===1?'기본':m+'배'):(m===1?'기본':m+'배');$('vl2').textContent=L.toFixed(2)+' m';
 const x0=100,x1=100+L/0.68*800,y=160,hh=70;
 ln(x0,y-hh,x1,y-hh,INK,3);ln(x0,y+hh,x1,y+hh,INK,3);if(closed)ln(x0,y-hh,x0,y+hh,INK,7);
 const env=x=>closed?Math.sin(m*Math.PI*(x-x0)/(2*(x1-x0))):Math.cos(m*Math.PI*(x-x0)/(x1-x0));
 // air particles (longitudinal)
 for(let r=0;r<7;r++)for(let i=0;i<=60;i++){const xe=x0+i*(x1-x0)/60;const dx=14*env(xe)*Math.cos(2*Math.PI*0.4*T);const yy=y-hh+12+r*(2*hh-24)/6;dot(xe+(closed&&i===0?0:dx),yy,2.2,'#94a3b8')}
 plot(x=>(hh-8)*env(x),x0,x1,y,'#2563eb',1.6,[5,4]);plot(x=>-(hh-8)*env(x),x0,x1,y,'#93c5fd',1.6,[5,4]);
 // labels
 const node=[],anti=[];for(let i=0;i<=400;i++){const xe=x0+i*(x1-x0)/400,e=Math.abs(env(xe));if(e<0.012)node.push(xe);if(e>0.995)anti.push(xe)}
 const uniq=a=>a.filter((v,i)=>i===0||v-a[i-1]>8);uniq(node).forEach(xn=>{txt('마디',xn,y+hh+18,{s:11,c:RD,b:1})});uniq(anti).forEach(xa=>{txt('배',xa,y-hh-16,{s:11,c:BL,b:1})});
 dbl(x0,y+hh+40,x1,y+hh+40,SUB);txt('l = '+L.toFixed(2)+' m',(x0+x1)/2,y+hh+54,{s:13,b:1});
 const lamn=closed?4*L/m:2*L/m;
 const rows=[['파장  λ = '+(closed?'4l/n (n 홀수)':'2l/n'),lamn.toFixed(3)+' m'],['진동수  f = v/λ',f.toFixed(0)+' Hz'],['가능한 진동수',closed?'f₁, 3f₁, 5f₁, … (홀수 배만)':'f₁, 2f₁, 3f₁, … (모든 정수 배)']];
 rows.forEach((r,i)=>{const yy=345+i*32;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(100,yy-14,800,28);txt(r[0],120,yy,{a:'left',s:15,b:1});txt(r[1],880,yy,{a:'right',s:16,b:1,c:BL})});
 if(sndOn&&tab===2)tone(f);
 $('step').innerHTML='점(●)은 관 속 공기 입자입니다. 공기는 관을 따라 <b>앞뒤로</b> 진동하지만(종파), 진동 범위를 점선(횡파 모양)으로 나타냈습니다. '+(closed?'<b>막힌 끝은 공기가 움직이지 못해 마디</b>, 열린 끝은 배입니다. 그래서 관 길이가 λ/4의 <b>홀수 배</b>인 정상파만 생깁니다.':'<b>열린 양 끝은 모두 배</b>입니다. 관 길이가 λ/2의 정수 배인 정상파가 생깁니다.');}
$('op').onclick=()=>{closed=false;$('op').classList.add('on');$('cl').classList.remove('on')};$('cl').onclick=()=>{closed=true;$('cl').classList.add('on');$('op').classList.remove('on')};
// ===== tab3 resonance tube
const REC=[];const ENDC=0.012;
function amp3(){const f=+$('f3').value,y=+$('y3').value,lam=VS/f,Le=y+ENDC;const ph=2*Math.PI*Le/lam;return Math.abs(Math.sin(ph))**8}
function scene3(){clear();const f=+$('f3').value,y=+$('y3').value,lam=VS/f;$('vf3').textContent=f+' Hz';$('vy3').textContent=y.toFixed(3)+' m';
 const tx=200,ty=40,tw=70,th=380,sc=th/0.95;
 ctx.fillStyle='#bfdbfe';ctx.fillRect(tx,ty+y*sc,tw,th-y*sc);ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.strokeRect(tx,ty,tw,th);
 ctx.fillStyle='#334155';ctx.fillRect(tx+8,ty-28,tw-16,18);txt('스마트 기기 ('+f+' Hz)',tx+tw+12,ty-19,{a:'left',s:12});
 const a=amp3();
 if(a>0.05){const Le=y+ENDC;for(let s of [1,-1]){ctx.beginPath();ctx.strokeStyle=s>0?BL:'#93c5fd';ctx.lineWidth=2;for(let q=0;q<=y*sc;q+=2){const d=q/sc;const xx=tx+tw/2+s*(tw/2-6)*a*Math.cos(2*Math.PI*(d+ENDC)/lam*1)*Math.cos(2*Math.PI*0.4*T);q===0?ctx.moveTo(xx,ty+q):ctx.lineTo(xx,ty+q)}ctx.stroke()}}
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
 $('step').innerHTML='수면 거리 <b>y</b>를 천천히 늘려 소리가 크게 들리는(공명) 위치를 찾아 <b>📌 기록</b>하세요. 수면은 공기가 움직이지 못하므로 <b>마디</b>, 관 입구는 <b>배</b>입니다. 이웃한 공명 위치의 차가 반 파장입니다.';}
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
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];if(sndOn){sndOn=false;stop();['s1','s2','s3'].forEach(k=>$(k).textContent='🔊 소리')}T=0}
function frame(now){const dt=Math.min(0.05,(now-last)/1000)*speed;last=now;if(!paused)T+=dt;[scene0,scene1,scene2,scene3,scene4][tab]();requestAnimationFrame(frame)}
go(0);requestAnimationFrame(frame);
</script></body></html>"""


if __name__ == "__main__":
    run_sim()

