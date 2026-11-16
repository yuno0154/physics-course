import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 정상파와 악기 형성평가(8문항) — 문제 상황 시뮬레이션 + 펼침식 해설/정답
# =========================================================================

PRE = r"""
const cv=document.getElementById('cv'),c=cv.getContext('2d'),W=cv.width,H=cv.height;
let t=0,run=true,last=performance.now(),SP=1,MUL=1;
const f=(v,d)=>(v<-0.5*Math.pow(10,-d)?'−':'+')+Math.abs(v).toFixed(d);
function line(x0,y0,x1,y1,col,w,d){c.beginPath();c.setLineDash(d||[]);c.strokeStyle=col;c.lineWidth=w||1;c.moveTo(x0,y0);c.lineTo(x1,y1);c.stroke();c.setLineDash([])}
function arrow(x0,y0,x1,y1,col,w){const L=Math.hypot(x1-x0,y1-y0);if(L<4)return;line(x0,y0,x1,y1,col,w||3);const a=Math.atan2(y1-y0,x1-x0);c.beginPath();c.fillStyle=col;c.moveTo(x1,y1);c.lineTo(x1-10*Math.cos(a-.4),y1-10*Math.sin(a-.4));c.lineTo(x1-10*Math.cos(a+.4),y1-10*Math.sin(a+.4));c.fill()}
function dbl(x0,y0,x1,y1,col){arrow(x0,y0,x1,y1,col,2);arrow(x1,y1,x0,y0,col,2)}
function txt(s,x,y,col,sz,al){c.font='bold '+(sz||13)+'px "Malgun Gothic",sans-serif';c.fillStyle=col||'#0f172a';c.textAlign=al||'center';c.textBaseline='middle';c.fillText(s,x,y)}
function dot(x,y,r,col){c.beginPath();c.fillStyle=col;c.arc(x,y,r,0,7);c.fill()}
function axes(ox,oy,w,h,xl,yl){line(ox,oy,ox+w,oy,'#0f172a',1.5);line(ox,oy-h,ox,oy+h,'#0f172a',1.5);txt(xl,ox+w-2,oy+14,'#475569',12,'right');txt(yl,ox+6,oy-h-8,'#475569',12,'left')}
function box(x,y,w,h,lab,col){c.fillStyle=col||'#e2e8f0';c.fillRect(x,y,w,h);c.strokeStyle='#1e293b';c.lineWidth=2;c.strokeRect(x,y,w,h);if(lab)txt(lab,x+w/2,y+h/2,'#0f172a',13)}
const pp=document.getElementById('pp');
pp.onclick=()=>{run=!run;pp.textContent=run?'⏸ 일시정지':'▶ 재생'};
document.getElementById('spd').onchange=e=>{MUL=+e.target.value};
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{t=+b.dataset.t;run=false;pp.textContent='▶ 재생'});
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(run)t+=dt*SP*MUL;c.clearRect(0,0,W,H);draw();requestAnimationFrame(loop)}
"""

STYLE = ('<style>.b{padding:4px 9px;font-size:12px;border:1px solid #94a3b8;border-radius:5px;background:#f8fafc;cursor:pointer;margin-left:3px}'
         '.b.on{background:#dbeafe;border-color:#2563eb;color:#1e3a8a;font-weight:700}</style>')
CTRL = ('<button class="b" id="pp">⏸ 일시정지</button>'
        '<select id="spd" class="b"><option value="0.5">0.5배속</option><option value="1" selected>1배속</option><option value="2">2배속</option></select>')


def sim(title, js, extra=""):
    return (STYLE + '<div style="font-family:sans-serif;border:1px solid #cbd5e1;border-radius:10px;padding:10px;max-width:680px;margin:0 auto;background:#fff">'
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:6px">'
            '<b style="font-size:13px">🎬 ' + title + '</b><span>' + extra + CTRL + '</span></div>'
            '<canvas id="cv" width="640" height="270" style="width:100%;border:1px solid #e2e8f0;border-radius:6px;background:#fafafa"></canvas></div>'
            '<script>(function(){' + PRE + js + '\nrequestAnimationFrame(loop);})();</script>')


# ---------------- 1. 3 m 줄의 정상파 (n=3 vs n=1, v=40 m/s) ----------------
JS1 = r"""
SP=1.2;let n=3;
function draw(){
 const x0=80,x1=560,L=x1-x0,cy=120,A=52;
 line(x0,cy-68,x0,cy+68,'#0f172a',5);line(x1,cy-68,x1,cy+68,'#0f172a',5);
 line(x0,cy,x1,cy,'#e2e8f0',1.5);
 // 진동 포락선 (연한 파랑)
 for(const sg of [1,-1]){
  c.beginPath();c.setLineDash([5,4]);c.strokeStyle='#93c5fd';c.lineWidth=1.8;
  for(let x=0;x<=L;x+=3){const y=cy-sg*A*Math.sin(n*Math.PI*x/L);x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}
  c.stroke();
 }
 c.setLineDash([]);
 // 현재 순간의 줄 모습
 const osc=Math.cos(2*Math.PI*(n===3?1.2:0.4)*t);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=3.2;
 for(let x=0;x<=L;x+=3){const y=cy-A*Math.sin(n*Math.PI*x/L)*osc;x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}
 c.stroke();
 // 마디(빨강) & 배(파랑) 표시
 for(let k=0;k<=n;k++){const xn=x0+k*L/n;dot(xn,cy,5.5,'#e11d48');txt('마디',xn,cy+20,'#e11d48',11)}
 for(let k=0;k<n;k++){const xa=x0+(k+0.5)*L/n;txt('배',xa,cy-A-12,'#2563eb',11.5)}
 dbl(x0,cy+80,x1,cy+80,'#475569');txt('줄의 길이 l = 3 m (속력 v = 40 m/s)',(x0+x1)/2,cy+96,'#0f172a',12.5);
 if(n===3){
  txt('문제 조건 (3배 진동): 마디 4개(양 끝 포함), 배 3개 | 반 파장 λ/2 = 1 m → 파장 λ = 2 m',320,20,'#0f172a',12.5);
  txt('진동수 f = v / λ = 40 / 2 = 20 Hz',320,248,'#1d4ed8',14);
 }else{
  txt('(4) 기본 진동 (n = 1): 마디 2개, 배 1개 | 반 파장 λ₁/2 = 3 m → 파장 λ₁ = 6 m',320,20,'#0f172a',12.5);
  txt('기본 진동수 f₁ = v / λ₁ = 40 / 6 ≈ 6.7 Hz (= 20/3 Hz)',320,248,'#059669',14);
 }
}
document.getElementById('n_3').onclick=()=>{n=3};
document.getElementById('n_1').onclick=()=>{n=1};
"""
EX1 = '<button class="b" id="n_3">문제 그림 (3배 진동)</button><button class="b" id="n_1">(4) 기본 진동 보기</button>'

# ---------------- 2. 한쪽 막힌 관 0.5 m (기본 진동 170 Hz vs 3배 진동 510 Hz) ----------------
JS2 = r"""
SP=1.2;let m=1;
function draw(){
 const x0=110,x1=530,L=x1-x0,cy=115,hh=54;
 // 관 외곽 (왼쪽 A 막힘, 오른쪽 B 열림)
 line(x0,cy-hh,x1,cy-hh,'#0f172a',3.5);line(x0,cy+hh,x1,cy+hh,'#0f172a',3.5);
 line(x0,cy-hh,x0,cy+hh,'#0f172a',7);
 txt('A (막힌 끝 · 마디)',x0,cy-hh-15,'#e11d48',12.5);
 txt('B (열린 끝 · 배)',x1,cy-hh-15,'#2563eb',12.5);
 const osc=Math.cos(2*Math.PI*(m===1?0.8:2.4)*t);
 // 공기 입자 종파 진동
 for(let r=0;r<5;r++)for(let i=0;i<=36;i++){
  const xe=x0+i*L/36,env=Math.sin(m*Math.PI*(xe-x0)/(2*L));
  const dx=(i===0?0:12*env*osc),yy=cy-hh+12+r*(2*hh-24)/4;
  dot(xe+dx,yy,2.2,'#94a3b8');
 }
 // 변위 포락선 & 실시간 정상파 곡선
 for(const sg of [1,-1]){
  c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#93c5fd';c.lineWidth=1.5;
  for(let x=0;x<=L;x+=3){const y=cy-sg*(hh-6)*Math.sin(m*Math.PI*x/(2*L));x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}
  c.stroke();
 }
 c.setLineDash([]);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=3;
 for(let x=0;x<=L;x+=3){const y=cy-(hh-6)*Math.sin(m*Math.PI*x/(2*L))*osc;x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}
 c.stroke();
 dbl(x0,cy+hh+22,x1,cy+hh+22,'#475569');txt('관의 길이 l = 0.5 m (소리 속력 340 m/s)',(x0+x1)/2,cy+hh+38,'#0f172a',12.5);
 if(m===1){
  txt('기본 진동 (n=1): 관 길이 0.5 m = λ/4 → 파장 λ = 2.0 m',320,20,'#0f172a',13);
  txt('기본 진동수 f₁ = v / λ = 340 / 2.0 = 170 Hz',320,250,'#1d4ed8',14);
 }else{
  txt('(4) 두 번째로 작은 공명 진동수 (홀수 배 n=3): 관 길이 0.5 m = 3λ/4 → λ₃ = 2/3 m',320,20,'#0f172a',12.5);
  txt('진동수 f₃ = 3 × f₁ = 3 × 170 = 510 Hz (막힌 관은 홀수 배만 공명!)',320,250,'#059669',13.5);
 }
}
document.getElementById('m_1').onclick=()=>{m=1};
document.getElementById('m_3').onclick=()=>{m=3};
"""
EX2 = '<button class="b" id="m_1">기본 진동 (170 Hz)</button><button class="b" id="m_3">(4) 두 번째 공명 (510 Hz)</button>'

# ---------------- 3. 두 진행파 중첩 정상파 (진폭 1 cm, 속력 2 cm/s, 점 a·b) ----------------
JS3 = r"""
SP=0.6;
function draw(){
 const s=t%2.0; // 주기 T = 2.0 s
 const ox=60,cy=125,sc=64; // 1 cm = 64 px (0..8 cm -> 512 px)
 axes(ox,cy,535,75,'위치(cm)','변위(cm)');
 for(let m=2;m<=8;m+=2){line(ox+m*sc,cy-3,ox+m*sc,cy+3,'#0f172a',1);txt(String(m),ox+m*sc,cy+15,'#475569',10.5)}
 txt('+2',ox-18,cy-60,'#7c3aed',11);txt('+1',ox-18,cy-30,'#64748b',10.5);txt('−2',ox-20,cy+60,'#7c3aed',11);
 line(ox,cy-60,ox+8*sc,cy-60,'#e2e8f0',1,[3,3]);line(ox,cy+60,ox+8*sc,cy+60,'#e2e8f0',1,[3,3]);

 // 두 진행파 (진폭 1 cm = 30 px, 파장 4 cm, 주기 2 s)
 c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#60a5fa';c.lineWidth=1.6;
 for(let x=0;x<=8;x+=0.04){
  const y1=Math.sin(Math.PI*x/2)*Math.cos(Math.PI*s)+Math.cos(Math.PI*x/2)*Math.sin(Math.PI*s);
  const px=ox+x*sc,py=cy-30*y1;x===0?c.moveTo(px,py):c.lineTo(px,py);
 }c.stroke();
 c.beginPath();c.strokeStyle='#f87171';
 for(let x=0;x<=8;x+=0.04){
  const y2=Math.sin(Math.PI*x/2)*Math.cos(Math.PI*s)-Math.cos(Math.PI*x/2)*Math.sin(Math.PI*s);
  const px=ox+x*sc,py=cy-30*y2;x===0?c.moveTo(px,py):c.lineTo(px,py);
 }c.stroke();c.setLineDash([]);

 // 합성 정상파 y = 2 sin(pi*x/2) cos(pi*s)
 const osc=Math.cos(Math.PI*s);
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=3.2;
 for(let x=0;x<=8;x+=0.03){
  const y=2*Math.sin(Math.PI*x/2)*osc;
  const px=ox+x*sc,py=cy-30*y;x===0?c.moveTo(px,py):c.lineTo(px,py);
 }c.stroke();

 const ya=2*osc;
 dot(ox+1*sc,cy-30*ya,6.5,'#2563eb');txt('a (배)',ox+1*sc,cy-30*ya-14,'#2563eb',12.5);
 dot(ox+4*sc,cy,6.5,'#e11d48');txt('b (마디)',ox+4*sc+24,cy-12,'#e11d48',12.5);
 txt('파장 λ = 4 cm, 속력 v = 2 cm/s → 진동수 f = 0.5 Hz, 주기 T = 2.0 s',320,20,'#0f172a',12.5);
 txt('현재 t = '+s.toFixed(2)+' s  |  점 a(배)의 변위 = '+f(ya,2)+' cm  |  점 b(마디)의 변위 = 0.00 cm (항상 상쇄)',320,250,'#7c3aed',12.5);
}
"""
EX3 = ('<button class="b" data-t="0">t=0 (최대 +2 cm)</button>'
       '<button class="b" data-t="0.5">0.5 s 뒤 (0 cm)</button>'
       '<button class="b" data-t="1.0">1.0 s 뒤 (−2 cm)</button>')

# ---------------- 4. 소리굽쇠 A(n=1) vs B(n=3) 연결한 같은 줄 ----------------
JS4 = r"""
SP=1;let tight=false;
function draw(){
 const x0=135,x1=575,L=x1-x0,y1=82,y2=190,A=32;
 const spdMul=tight?1.4:1.0;
 // (가) 소리굽쇠 A (n=1)
 c.strokeStyle='#334155';c.lineWidth=3;
 c.beginPath();c.moveTo(x0-36,y1);c.lineTo(x0-16,y1);c.moveTo(x0-16,y1-12);c.lineTo(x0,y1-12);c.moveTo(x0-16,y1+12);c.lineTo(x0,y1+12);c.stroke();
 txt('(가) 소리굽쇠 A',x0-42,y1-26,'#0f172a',12);
 line(x1,y1-42,x1,y1+42,'#0f172a',5);line(x0,y1,x1,y1,'#e2e8f0',1);
 const osc1=Math.cos(2*Math.PI*0.7*spdMul*t);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=3;
 for(let x=0;x<=L;x+=3){const y=y1-A*Math.sin(Math.PI*x/L)*osc1;x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}c.stroke();
 txt('파장 λ_A = 2L  |  진동수 f_A = 1f₀'+(tight?' (팽팽해져 속력·진동수 증가!)':''),x0+L/2,y1-42,'#2563eb',12);

 // (나) 소리굽쇠 B (n=3)
 c.strokeStyle='#334155';c.lineWidth=3;
 c.beginPath();c.moveTo(x0-36,y2);c.lineTo(x0-16,y2);c.moveTo(x0-16,y2-12);c.lineTo(x0,y2-12);c.moveTo(x0-16,y2+12);c.lineTo(x0,y2+12);c.stroke();
 txt('(나) 소리굽쇠 B',x0-42,y2-26,'#0f172a',12);
 line(x1,y2-42,x1,y2+42,'#0f172a',5);line(x0,y2,x1,y2,'#e2e8f0',1);
 const osc3=Math.cos(2*Math.PI*2.1*spdMul*t);
 c.beginPath();c.strokeStyle='#e11d48';c.lineWidth=3;
 for(let x=0;x<=L;x+=3){const y=y2-A*Math.sin(3*Math.PI*x/L)*osc3;x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}c.stroke();
 txt('파장 λ_B = 2L/3  |  진동수 f_B = 3f₀',x0+L/2,y2-42,'#e11d48',12);

 txt('파장 비 λ_A : λ_B = 3 : 1  |  같은 줄·같은 장력(속력 동일)이므로 진동수 비 f_A : f_B = 1 : 3',320,252,'#0f172a',12.5);
}
document.getElementById('t_norm').onclick=()=>{tight=false};
document.getElementById('t_more').onclick=()=>{tight=true};
"""
EX4 = '<button class="b" id="t_norm">기본 장력</button><button class="b" id="t_more">(4) 줄을 더 팽팽하게</button>'

# ---------------- 5. 기주 공명 실험 (500 Hz, y1=0.16 m, y2=0.50 m, y3=0.84 m) ----------------
JS5 = r"""
SP=1.2;
function draw(){
 const osc=Math.cos(2*Math.PI*1.2*t);
 const cols=[
  {x:125,y:0.16,n:1,lab:'1차 공명 (y₁ = 0.16 m)'},
  {x:320,y:0.50,n:3,lab:'2차 공명 (y₂ = 0.50 m)'},
  {x:515,y:0.84,n:5,lab:'(4) 3차 공명 (y₃ = 0.84 m)'}
 ];
 const topY=52,botY=222,sc=(botY-topY)/0.95,tw=46,e=0.01;
 cols.forEach(q=>{
  const x0=q.x-tw/2,wTop=topY+q.y*sc;
  // 물 영역
  c.fillStyle='#bfdbfe';c.fillRect(x0,wTop,tw,botY-wTop);
  c.strokeStyle='#1e293b';c.lineWidth=2;c.strokeRect(x0,topY,tw,botY-topY);
  // 스마트 기기
  c.fillStyle='#334155';c.fillRect(x0+6,topY-20,tw-12,12);
  // 정상파 곡선 (배는 입구 위 e=0.01 m 지점)
  const Lpx=(q.y+e)*sc,yAnti=topY-e*sc;
  for(const sg of [1,-1]){
   c.beginPath();c.strokeStyle=sg>0?'#2563eb':'#93c5fd';c.lineWidth=sg>0?2.5:1.6;
   for(let dy=0;dy<=Lpx;dy+=2){
    const env=Math.cos(q.n*Math.PI/2*(dy/Lpx))*(sg>0?osc:1);
    const xx=q.x+sg*(tw/2-5)*env;
    dy===0?c.moveTo(xx,yAnti+dy):c.lineTo(xx,yAnti+dy);
   }
   c.stroke();
  }
  dbl(x0-14,topY,x0-14,wTop,'#e11d48');
  txt(q.y.toFixed(2)+' m',x0-36,(topY+wTop)/2,'#e11d48',11.5);
  txt(q.lab,q.x,botY+16,'#0f172a',12);
 });
 txt('스마트 기기 f = 500 Hz  |  개구단 보정: 실제 배는 관 입구보다 약 0.01 m 바깥에 생김 (λ/4 = 0.17 m ≠ 0.16 m)',320,16,'#0f172a',12);
 txt('λ/2 = y₂ − y₁ = 0.50 − 0.16 = 0.34 m → λ = 0.68 m, 속력 v = fλ = 500×0.68 = 340 m/s',320,256,'#1d4ed8',12.5);
}
"""

# ---------------- 6. 길이 0.34 m 관 A(양쪽 열림) vs 관 B(한쪽 막힘) ----------------
JS6 = r"""
SP=1.2;let mode=1;
function draw(){
 const x0=120,x1=520,L=x1-x0,y1=82,y2=188,hh=32;
 const osc=Math.cos(2*Math.PI*1.2*t);
 // 상단: 관 A (양쪽 열림, 기본 500 Hz)
 line(x0,y1-hh,x1,y1-hh,'#0f172a',3);line(x0,y1+hh,x1,y1+hh,'#0f172a',3);
 const mA=(mode===3)?2:1;
 for(const sg of [1,-1]){
  c.beginPath();c.strokeStyle=sg>0?'#2563eb':'#93c5fd';c.lineWidth=sg>0?2.6:1.5;
  for(let x=0;x<=L;x+=3){
   const y=y1-sg*(hh-4)*Math.cos(mA*Math.PI*x/L)*(sg>0?osc:1);
   x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y);
  }c.stroke();
 }
 txt('관 A (양쪽 열림, 0.34 m): 기본 f_A = 500 Hz'+(mode===3?' → 1000 Hz(2배) 공명 O!':''),320,y1-hh-14,'#2563eb',12.5);

 // 하단: 관 B (한쪽 막힘, 기본 250 Hz, 홀수배 250, 750, 1250 Hz)
 line(x0,y2-hh,x1,y2-hh,'#0f172a',3);line(x0,y2+hh,x1,y2+hh,'#0f172a',3);line(x0,y2-hh,x0,y2+hh,'#0f172a',6);
 if(mode!==3){
  const mB=(mode===2)?3:1;
  for(const sg of [1,-1]){
   c.beginPath();c.strokeStyle=sg>0?'#059669':'#a7f3d0';c.lineWidth=sg>0?2.6:1.5;
   for(let x=0;x<=L;x+=3){
    const y=y2-sg*(hh-4)*Math.sin(mB*Math.PI*x/(2*L))*(sg>0?osc:1);
    x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y);
   }c.stroke();
  }
  txt('관 B (한쪽 막힘, 0.34 m): '+(mode===1?'기본 f_B = 250 Hz':'3배 진동 750 Hz (홀수 배 공명: 250, 750, 1250 Hz)'),320,y2-hh-14,'#059669',12.5);
 }else{
  // 1000 Hz (4f_B, 짝수배) -> 열린 끝이 마디가 되어버려 공명 불가!
  c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#e11d48';c.lineWidth=2;
  for(let x=0;x<=L;x+=3){
   const y=y2-(hh-6)*Math.sin(4*Math.PI*x/(2*L))*osc;
   x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y);
  }c.stroke();c.setLineDash([]);
  dot(x1,y2,6,'#e11d48');txt('열린 끝이 배가 될 수 없음!',x1-10,y2+hh+14,'#e11d48',11.5,'right');
  txt('관 B (한쪽 막힘): 1000 Hz(=4×250 Hz, 짝수 배)는 열린 끝이 배가 되는 조건을 만족 못 해 공명 X!',320,y2-hh-14,'#e11d48',12);
 }
 txt('A 고유 진동수: 500, 1000, 1500 Hz … (정수 배)  |  B 고유 진동수: 250, 750, 1250 Hz … (홀수 배)',320,252,'#0f172a',12);
}
document.getElementById('q6_1').onclick=()=>{mode=1};
document.getElementById('q6_2').onclick=()=>{mode=2};
document.getElementById('q6_3').onclick=()=>{mode=3};
"""
EX6 = ('<button class="b" id="q6_1">(1) 기본 진동 (500/250 Hz)</button>'
       '<button class="b" id="q6_2">(2) B의 3배 진동 (750 Hz)</button>'
       '<button class="b" id="q6_3">(3)(4) 1000 Hz 울릴 때</button>')

# ---------------- 7. 기타 줄 (l=0.65 m, 330 Hz vs l=0.49 m, 440 Hz) ----------------
JS7 = r"""
SP=1.2;let fret=false;
function draw(){
 const osc=Math.cos(2*Math.PI*(fret?1.6:1.2)*t);
 // 기타 울림통 및 넥
 c.fillStyle='#f59e0b';c.strokeStyle='#78350f';c.lineWidth=2.5;
 c.beginPath();c.arc(135,135,56,0,7);c.fill();c.stroke();
 c.fillStyle='#78350f';c.beginPath();c.arc(145,135,20+3*Math.abs(osc),0,7);c.fill();
 txt('울림통(공명)',135,205,'#78350f',12);
 c.fillStyle='#fde68a';c.fillRect(190,123,370,24);c.strokeRect(190,123,370,24);

 const x0=120,x1=fret?450:550,L=x1-x0,cy=135,A=26;
 line(x0,cy-28,x0,cy+28,'#0f172a',4);line(x1,cy-28,x1,cy+28,'#e11d48',4);
 if(fret)txt('프렛 누름 (l ≈ 0.49 m)',x1,cy-38,'#e11d48',12);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=3;
 for(let x=0;x<=L;x+=3){const y=cy-A*Math.sin(Math.PI*x/L)*osc;x===0?c.moveTo(x0+x,y):c.lineTo(x0+x,y)}c.stroke();
 dbl(x0,cy+42,x1,cy+42,'#2563eb');
 txt(fret?'진동 줄 길이 l ≈ 0.49 m (440 Hz)':'진동 줄 길이 l = 0.65 m (330 Hz)',(x0+x1)/2,cy+58,'#2563eb',12.5);

 // 공기 중 퍼져나가는 음파 표시
 for(let r=1;r<=3;r++){
  const R=22+((r*22+(t*35)%22));
  c.beginPath();c.strokeStyle='rgba(37,99,235,0.35)';c.lineWidth=2;
  c.arc(145,75,R*0.6,-2.4,-0.7);c.stroke();
 }
 txt('공기 중 소리 (v = 340 m/s, λ_공기 ≈ 1.03 m)',290,42,'#059669',12);
 txt('(1) 줄 속력 v = 2lf = 2×0.65×330 = 429 m/s  |  (3) 줄 파장 1.3 m ≠ 공기 파장 1.03 m (진동수는 같지만 속력이 다름!)',320,252,'#0f172a',11.8);
}
document.getElementById('g_330').onclick=()=>{fret=false};
document.getElementById('g_440').onclick=()=>{fret=true};
"""
EX7 = '<button class="b" id="g_330">(1)(3) 기본 0.65 m (330 Hz)</button><button class="b" id="g_440">(2) 440 Hz (l ≈ 0.49 m)</button>'

# ---------------- 8. 물병 악기 A~D (공기 기둥 길이와 진동수) ----------------
JS8 = r"""
SP=1.2;let warm=false;
function draw(){
 const vs=warm?360:340;
 const bottles=[
  {name:'A',w:0.03,l:0.22},
  {name:'B',w:0.06,l:0.19},
  {name:'C (l=0.17 m)',w:0.08,l:0.17},
  {name:'D (가장 높음)',w:0.13,l:0.12}
 ];
 bottles.forEach((b,i)=>{
  const x0=65+i*145,yb=205,hpx=135,sc=hpx/0.25;
  c.strokeStyle='#0f172a';c.lineWidth=2;
  c.beginPath();
  c.moveTo(x0+20,yb-hpx-20);c.lineTo(x0+20,yb-hpx);c.lineTo(x0,yb-hpx+22);
  c.lineTo(x0,yb);c.lineTo(x0+76,yb);c.lineTo(x0+76,yb-hpx+22);
  c.lineTo(x0+56,yb-hpx);c.lineTo(x0+56,yb-hpx-20);c.stroke();
  const wH=b.w*sc,yTop=yb-hpx-20,yWat=yb-wH,airH=yWat-yTop;
  c.fillStyle='#93c5fd';c.fillRect(x0+2,yWat,72,wH-1);
  // 공기 기둥 속 기본 정상파 (λ = 4l)
  const fr=vs/(4*b.l),osc=Math.cos(2*Math.PI*(0.6+i*0.25)*(warm?1.15:1)*t);
  for(const sg of [1,-1]){
   c.beginPath();c.strokeStyle=i===3?'#e11d48':'#2563eb';c.lineWidth=2;
   for(let q=0;q<=airH;q+=2){
    const xx=x0+38+sg*15*Math.cos(Math.PI/2*(q/airH))*osc;
    q===0?c.moveTo(xx,yTop+q):c.lineTo(xx,yTop+q);
   }c.stroke();
  }
  txt(b.name,x0+38,yb+16,i===3?'#e11d48':'#0f172a',12.5);
  txt('f = '+fr.toFixed(0)+' Hz',x0+38,yb+33,'#1d4ed8',12);
 });
 txt('병 속 공기 기둥 = 한쪽 막힌 관 (수면=마디, 입구=배) → 파장 λ = 4l, 기본 진동수 f = v / (4l)',320,18,'#0f172a',12.5);
 txt(warm?'(3) 기온이 올라가 소리 속력 v가 커지면 모든 병의 진동수 f = v/(4l)가 커져 높은 소리가 난다!'
         :'(1) 물이 가장 많은 D가 공기 기둥(l)이 가장 짧아 가장 높은 소리가 난다! | (2) l = 0.17 m일 때 f = 340/(4×0.17) = 500 Hz',320,255,warm?'#e11d48':'#059669',12);
}
document.getElementById('w_norm').onclick=()=>{warm=false};
document.getElementById('w_hot').onclick=()=>{warm=true};
"""
EX8 = '<button class="b" id="w_norm">기본 (v = 340 m/s)</button><button class="b" id="w_hot">(3) 기온 상승 (속력 증가)</button>'

SIMS = {
    1: ("길이 3 m 줄의 정상파: 3배 진동(20 Hz)과 기본 진동(6.7 Hz)", JS1, EX1),
    2: ("길이 0.5 m 한쪽이 막힌 관의 정상파 (기본 170 Hz · 3배 510 Hz)", JS2, EX2),
    3: ("반대 방향 진행파의 중첩과 매질 점 a(배)·b(마디)의 운동", JS3, EX3),
    4: ("같은 줄에 연결한 소리굽쇠 A(n=1)와 B(n=3)의 정상파 비교", JS4, EX4),
    5: ("기주 공명 장치: 수면 위치 y₁·y₂·y₃와 개구단 보정", JS5, ""),
    6: ("길이 0.34 m 열린 관 A와 막힌 관 B의 고유 진동수 비교", JS6, EX6),
    7: ("기타 줄(0.65 m)의 정상파와 울림통 공명", JS7, EX7),
    8: ("물병 악기 A~D: 공기 기둥 길이에 따른 기본 진동수", JS8, EX8),
}


def problem(n, badge, level, text, subs, answer_md):
    st.markdown(
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:14px 18px;margin-bottom:8px">'
        f'<span style="background:{badge};padding:3px 9px;border-radius:6px;font-weight:bold;font-size:.8rem">문제 {n} · {level}</span>'
        f'<p style="margin:8px 0 4px">{text}</p>'
        + "".join(f'<div style="font-size:.93rem;margin-left:4px">{s}</div>' for s in subs) + '</div>',
        unsafe_allow_html=True)
    title, js, extra = SIMS[n]
    components.html(sim(title, js, extra), height=360)
    with st.expander(f"💡 문제 {n} 해설 및 정답 펼치기", expanded=False):
        st.markdown(answer_md)
    st.divider()


def run_sim():
    st.title("📝 정상파와 악기 형성평가 문제 풀이")
    st.caption("Ⅲ. 탄성파와 소리 · 05 정상파와 악기 [12역학03-05]")
    st.markdown("각 문항의 문제 상황을 시뮬레이션으로 확인하고, 직접 풀어 본 뒤 **해설 및 정답을 펼쳐** 확인하세요.")
    st.markdown("---")

    B1, B2, B3 = "#eff6ff", "#ecfdf5", "#faf5ff"

    problem(1, B1, "기본",
            "그림은 길이 3 m인 줄의 양 끝을 고정하고 진동시켰을 때 생긴 정상파의 모습이다. 줄에서 파동의 속력은 40 m/s이다. (줄 전체에 반 파장 고리가 3개 생김)",
            ["(1) 이 정상파의 파장을 구하시오.",
             "(2) 양 끝을 포함한 마디의 개수와 배의 개수를 각각 쓰시오.",
             "(3) 이 정상파의 진동수를 풀이 과정과 함께 구하시오.",
             "(4) 같은 줄에서 기본 진동이 일어날 때의 진동수를 구하시오."],
            r"""
- **(1)** 이웃한 마디 사이 거리 $1\text{ m} = \dfrac{\lambda}{2}$ → $\lambda =$ **2 m**
- **(2)** 마디 **4개**(양 끝 포함), 배 **3개**
- **(3)** $f = \dfrac{v}{\lambda} = \dfrac{40}{2} =$ **20 Hz**
- **(4)** 기본 진동($n=1$)의 파장은 $\lambda_1 = 2l = 2 \times 3 = 6\text{ m}$이므로, $f_1 = \dfrac{40}{6} \approx$ **6.7 Hz** ($= \dfrac{20}{3}\text{ Hz}$)

*채점 포인트: (2) 양 끝 고정점을 마디 개수에 포함해 세는가.*
""")

    problem(2, B1, "기본",
            "그림은 길이 0.5 m이고 한쪽 끝 A가 막힌 관에서 기본 진동의 정상파가 생긴 모습이다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) A와 B는 각각 배와 마디 중 무엇인지 쓰고, 그 까닭을 쓰시오.",
             "(2) 이 정상파의 파장을 구하시오.",
             "(3) 관에서 나는 소리의 진동수를 구하시오.",
             "(4) 이 관에서 공명이 일어나는 진동수 중 두 번째로 작은 진동수를 구하시오."],
            r"""
- **(1)** **A: 마디** (막힌 끝은 공기가 움직이지 못함), **B: 배** (열린 끝은 공기가 자유롭게 진동함)
- **(2)** 관의 길이 $0.5\text{ m} = \dfrac{\lambda}{4}$ → $\lambda =$ **2 m**
- **(3)** $f_1 = \dfrac{v}{\lambda} = \dfrac{340}{2} =$ **170 Hz**
- **(4)** 한쪽이 막힌 관은 기본 진동수의 **홀수 배($1, 3, 5, \dots$)**만 공명하므로 $3 \times 170 =$ **510 Hz**

*채점 포인트: (4) 2배인 340 Hz로 답하지 않고 막힌 관의 홀수 배 조건($3f_1$)을 적용하는가.*
""")

    problem(3, B2, "보통",
            "그림은 진폭 1 cm, 속력 2 cm/s로 서로 반대 방향으로 진행하는 두 파동이 중첩하여 생긴 정상파의 변위가 최대일 때 모습이다(실선). a(x = 1 cm, 배), b(x = 4 cm, 마디)는 매질 위의 점이다.",
            ["(1) a에서 정상파의 최대 변위를 쓰시오.",
             "(2) b가 항상 정지해 있는 까닭을 간섭과 관련지어 쓰시오.",
             "(3) 원래 파동의 파장과 진동수를 구하시오.",
             "(4) 그림의 순간부터 0.5 s 뒤와 1 s 뒤 a의 변위를 각각 쓰시오."],
            r"""
- **(1)** **2 cm** (원래 파동 진폭 $1\text{ cm}$의 2배)
- **(2)** b에서는 반대 방향으로 진행하는 두 파동이 **항상 반대 위상으로 만나 상쇄 간섭**하기 때문이다(**마디**).
- **(3)** 이웃한 마디 사이 거리 $2\text{ cm} = \dfrac{\lambda}{2}$ → 파장 $\lambda =$ **4 cm**, 진동수 $f = \dfrac{v}{\lambda} = \dfrac{2}{4} =$ **0.5 Hz**
- **(4)** 주기 $T = \dfrac{1}{f} = 2\text{ s}$이므로, $0.5\text{ s}$($T/4$) 뒤에는 **0**, $1\text{ s}$($T/2$) 뒤에는 **−2 cm**

*채점 포인트: (4) 배(a)도 시간에 따라 $+2\text{ cm} \rightarrow 0 \rightarrow -2\text{ cm}$로 변위가 변함을 이해하는가.*
""")

    problem(4, B2, "보통",
            "그림 (가), (나)는 같은 줄의 한쪽 끝을 진동수가 다른 소리굽쇠 A, B에 연결하고 진동시켰을 때 생긴 정상파이다. 두 경우 줄의 길이와 장력은 같다. ((가)는 배가 1개, (나)는 배가 3개이다.)",
            ["(1) (가)와 (나)에서 정상파의 파장의 비를 구하시오.",
             "(2) A와 B의 진동수의 비를 구하고, 그 까닭을 쓰시오.",
             "(3) 줄의 진동으로 공기 중에 생긴 소리의 파장은 (가)와 (나) 중 어느 것이 더 긴지 쓰시오.",
             "(4) (가)에서 줄을 더 팽팽하게 하면 기본 진동의 진동수는 어떻게 되는지 까닭과 함께 쓰시오."],
            r"""
- **(1)** (가) $\lambda_A = 2L$, (나) $\lambda_B = \dfrac{2L}{3}$ → **3 : 1**
- **(2)** **$f_A : f_B = 1 : 3$**. 같은 줄·같은 장력이라 **줄에서 파동의 속력이 같으므로** 진동수는 파장에 반비례한다.
- **(3)** **(가)**. 공기 중 소리의 진동수는 줄의 진동수와 같고 공기 중 소리 속력은 같으므로, 진동수가 작은 (가)의 소리 파장이 더 길다.
- **(4)** **커진다.** 줄을 더 팽팽하게 하면 **줄에서 파동의 속력($v$)이 커지고** 기본 진동 파장($2L$)은 그대로이므로 $f = \dfrac{v}{\lambda}$가 커진다.

*채점 포인트: (2) '같은 줄·같은 장력이므로 파동의 속력이 같다'는 근거를 명시하는가.*
""")

    problem(5, B3, "심화",
            "진동수 500 Hz의 소리를 내는 스마트 기기를 물이 든 유리관 위에 두고 물의 높이를 낮추었더니, 관 입구에서 수면까지 거리 y가 0.16 m, 0.50 m일 때 소리가 크게 들렸다.",
            ["(1) 소리가 크게 들리는 까닭을 쓰시오.",
             "(2) 소리의 파장과 속력을 풀이 과정과 함께 구하시오.",
             "(3) 첫 번째 공명 위치 0.16 m가 λ/4와 정확히 같지 않은 까닭을 서술하시오.",
             "(4) 물을 더 빼면 세 번째로 소리가 크게 들리는 y는 몇 m인지 구하시오."],
            r"""
- **(1)** 스마트 기기의 소리와 수면에서 반사된 소리가 중첩하여 **관 속에 정상파가 생기고 공명이 일어나기 때문**이다.
- **(2)** 이웃한 두 공명 위치의 차 $\dfrac{\lambda}{2} = 0.50 - 0.16 = 0.34\text{ m}$ → 파장 $\lambda =$ **0.68 m**, 속력 $v = f\lambda = 500 \times 0.68 =$ **340 m/s**
- **(3)** **관 입구의 배가 관 입구보다 조금 바깥쪽(약 $0.01\text{ m}$)에 생기기 때문**이다(개구단 보정). 그래서 실험에서는 두 공명 위치의 차($y_2 - y_1 = \lambda/2$)를 이용한다.
- **(4)** $y_3 = y_2 + \dfrac{\lambda}{2} = 0.50 + 0.34 =$ **0.84 m**

*채점 포인트: (3) 관 입구 바깥에 배가 위치한다는 오차 요인(개구단 보정)을 설명하는가.*
""")

    problem(6, B3, "심화",
            "그림과 같이 길이가 0.34 m로 같은 관 A(양쪽 끝이 열림), B(한쪽 끝이 막힘)가 있다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) A와 B의 기본 진동수를 각각 구하시오.",
             "(2) B에서 공명이 일어나는 진동수를 작은 것부터 세 가지 쓰시오.",
             "(3) 진동수 1000 Hz의 소리굽쇠를 각 관 입구에서 울릴 때 공명이 일어나는 관을 쓰고, 근거를 쓰시오.",
             "(4) B에서는 기본 진동수의 2배인 소리가 공명하지 않는 까닭을 관 양 끝의 조건으로 서술하시오."],
            r"""
- **(1)** **A**: $f_A = \dfrac{v}{2l} = \dfrac{340}{2 \times 0.34} =$ **500 Hz**, **B**: $f_B = \dfrac{v}{4l} = \dfrac{340}{4 \times 0.34} =$ **250 Hz**
- **(2)** **250 Hz, 750 Hz, 1250 Hz** (기본 진동수의 홀수 배)
- **(3)** **A**. $1000\text{ Hz}$는 $500\text{ Hz}$의 2배로 A의 고유 진동수이지만, B의 고유 진동수($250\text{ Hz}$의 홀수 배)가 아니기 때문이다.
- **(4)** B는 **막힌 끝이 마디, 열린 끝이 배**가 되어야 하므로 관의 길이가 $\lambda/4$의 **홀수 배**인 정상파만 생긴다. 기본 진동수의 2배 진동수는 이 양 끝 조건을 만족하지 못한다.

*채점 포인트: (3), (4) 관 양 끝의 경계 조건(막힌 끝=마디, 열린 끝=배)으로 설명하는가.*
""")

    problem(7, B3, "심화",
            "그림은 진동하는 줄의 길이가 0.65 m인 기타를 나타낸 것이다. 이 줄을 튕기면 기본 진동수 330 Hz의 소리가 난다. (단, 공기 중 소리의 속력은 340 m/s이다.)",
            ["(1) 줄에서 파동의 속력을 구하시오.",
             "(2) 같은 줄로 440 Hz의 소리를 내려면 진동하는 줄의 길이를 약 몇 m로 해야 하는지 구하시오.",
             "(3) 기본 진동일 때 줄의 정상파 파장과, 이때 공기 중에 퍼지는 소리의 파장을 각각 구하고, 두 값이 다른 까닭을 쓰시오.",
             "(4) 기타의 울림통이 하는 역할을 공명과 관련지어 서술하시오."],
            r"""
- **(1)** $v_{\text{줄}} = 2lf = 2 \times 0.65 \times 330 =$ **429 m/s**
- **(2)** $l' = \dfrac{v_{\text{줄}}}{2f'} = \dfrac{429}{2 \times 440} = \dfrac{429}{880} \approx$ **0.49 m**
- **(3)** 줄의 정상파 파장 $\lambda_{\text{줄}} = 2 \times 0.65 =$ **1.3 m**, 공기 중 소리의 파장 $\lambda_{\text{공기}} = \dfrac{340}{330} \approx$ **1.03 m**. **진동수($330\text{ Hz}$)는 같지만 줄과 공기에서 파동의 속력이 다르기 때문**이다.
- **(4)** 줄의 진동이 울림통 속 공기와 **공명**하여 소리의 **진폭(세기)을 크게** 한다(진동수·높이는 변하지 않는다).

*채점 포인트: (3) '진동수는 같지만 매질에 따라 파동의 속력이 다르다'는 논리를 명확히 쓰는가.*
""")

    problem(8, B3, "심화",
            "그림과 같이 같은 병 A~D에 물을 서로 다른 높이로 채우고 병 입구를 불어 소리를 냈다. 병 속 공기 기둥은 한쪽 끝이 막힌 관으로 생각한다. (물은 A < B < C < D 순으로 많이 들어 있고, 단 소리의 속력은 340 m/s이다.)",
            ["(1) 가장 높은 소리가 나는 병을 쓰고, 그 까닭을 쓰시오.",
             "(2) 공기 기둥의 길이가 0.17 m인 병에서 나는 소리의 기본 진동수를 구하시오.",
             "(3) 기온이 올라가 소리의 속력이 커지면 같은 병에서 나는 소리의 높이는 어떻게 되는지 쓰시오.",
             "(4) 리코더의 구멍을 열수록 높은 소리가 나는 까닭을 이 문항과 관련지어 서술하시오."],
            r"""
- **(1)** **D**. 물이 가장 많아 **진동하는 공기 기둥의 길이($l$)가 가장 짧으므로** 정상파의 파장($4l$)이 가장 짧고 진동수가 가장 크다.
- **(2)** $f = \dfrac{v}{4l} = \dfrac{340}{4 \times 0.17} =$ **500 Hz**
- **(3)** **높아진다.** $f = \dfrac{v}{4l}$에서 공기 기둥 길이 $l$은 같고 소리의 속력 $v$가 커지기 때문이다.
- **(4)** 리코더의 구멍을 열면 구멍이 열린 끝(배) 역할을 하여 **진동하는 공기 기둥의 유효 길이가 짧아지므로**, 정상파의 파장이 짧아지고 진동수가 커져 높은 소리가 난다.

*채점 포인트: 공기 기둥의 길이($l$) → 정상파 파장($4l$) → 고유 진동수($f = v/4l$)의 관계로 일관되게 설명하는가.*
""")


run_sim()

