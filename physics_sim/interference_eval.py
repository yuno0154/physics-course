import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 음파의 간섭과 소음 제어 형성평가(8문항) — 문제 상황 시뮬레이션 + 펼침식 해설/정답
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


# ---------------- 1. 두 펄스 A(+2 cm), B(-1 cm / +1 cm) 중첩 ----------------
JS1 = r"""
SP=1;let upB=false;const ox=50,sc=45,by=135;
const tri=(u,h)=>{const d=Math.abs(u);return d<1?h*(1-d):0};
function draw(){
 const s=t%7;
 for(let i=0;i<=12;i++)line(ox+i*sc,by-90,ox+i*sc,by+90,'#e2e8f0',1);
 for(let j=-2;j<=2;j++)line(ox,by+j*sc,ox+12*sc,by+j*sc,'#e2e8f0',1);
 line(ox,by,ox+12*sc,by,'#64748b',1.5);
 const cA=2.5+s,cB=9.5-s,hB=upB?1:-1;
 // 개별 펄스 점선
 c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#3b82f6';c.lineWidth=1.8;
 for(let X=0;X<=12;X+=.04){const px=ox+X*sc,py=by-tri(X-cA,2)*sc;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 c.beginPath();c.strokeStyle='#e11d48';
 for(let X=0;X<=12;X+=.04){const px=ox+X*sc,py=by-tri(X-cB,hB)*sc;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();c.setLineDash([]);
 // 합성파 실선
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=3.5;
 for(let X=0;X<=12;X+=.03){const y=tri(X-cA,2)+tri(X-cB,hB);const px=ox+X*sc,py=by-y*sc;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 const ym=tri(6-cA,2)+tri(6-cB,hB);
 dot(ox+6*sc,by-ym*sc,6,'#7c3aed');
 txt('t = '+s.toFixed(1)+' s (모눈 1칸 = 1 cm, 속력 1 cm/s)',ox,20,'#0f172a',13,'left');
 txt('중앙(x=6) 합성 변위 = '+(tri(6-cA,2)).toFixed(1)+' + ('+(tri(6-cB,hB)).toFixed(1)+') = '+ym.toFixed(1)+' cm',320,250,'#7c3aed',13.5);
}
document.getElementById('b_dn').onclick=()=>{upB=false};
document.getElementById('b_up').onclick=()=>{upB=true};
"""
EX1 = ('<button class="b" data-t="0">t=0</button>'
       '<button class="b" data-t="3.5">t=3.5 s (꼭짓점 겹침)</button>'
       '<button class="b" id="b_dn">B 아래로(−1 cm)</button>'
       '<button class="b" id="b_up">(3) B 위로(+1 cm)</button>')

# ---------------- 2. (가) 보강 간섭 vs (나) 상쇄 간섭 ----------------
JS2 = r"""
SP=1;const ox=65,gw=530;
function draw(){
 const y1=72,y2=185,A=22;
 // (가) 같은 위상
 axes(ox,y1,gw,48,'시간','변위');
 txt('+2A',ox-22,y1-2*A,'#7c3aed',11);txt('+A',ox-18,y1-A,'#475569',11);txt('−A',ox-20,y1+A,'#475569',11);
 txt('(가) 두 음파가 같은 위상으로 도달 → 보강 간섭 (합성 진폭 = 2A, 진동수 그대로)',ox+80,y1-50,'#059669',12.5,'left');
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2;
 for(let x=0;x<=gw-20;x+=3){const y=y1-A*Math.sin(x/32-t*2);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();
 c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#e11d48';c.lineWidth=2;
 for(let x=0;x<=gw-20;x+=3){const y=y1-A*Math.sin(x/32-t*2)+3;x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();c.setLineDash([]);
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=3;
 for(let x=0;x<=gw-20;x+=3){const y=y1-2*A*Math.sin(x/32-t*2);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();

 // (나) 반대 위상
 axes(ox,y2,gw,48,'시간','변위');
 txt('+A',ox-18,y2-A,'#475569',11);txt('0',ox-14,y2,'#7c3aed',11);txt('−A',ox-20,y2+A,'#475569',11);
 txt('(나) 두 음파가 반대 위상으로 도달 → 상쇄 간섭 (합성 진폭 = 0, 소리 사라짐)',ox+80,y2-50,'#e11d48',12.5,'left');
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2;
 for(let x=0;x<=gw-20;x+=3){const y=y2-A*Math.sin(x/32-t*2);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();
 c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#e11d48';c.lineWidth=2;
 for(let x=0;x<=gw-20;x+=3){const y=y2+A*Math.sin(x/32-t*2);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();c.setLineDash([]);
 line(ox,y2,ox+gw-20,y2,'#7c3aed',3.5);
 txt('보라색 굵은 선 = 합성파  |  (가) 진폭 2A (소리 큼),  (나) 진폭 0 (소리 작음)',320,252,'#7c3aed',13);
}
"""

# ---------------- 3. 동심원 마루·골과 A, B, C, D 경로차 ----------------
JS3 = r"""
SP=0.8;let invS1=false;
function draw(){
 const s1x=250,s2x=390,sy=225,lam=44;
 // 동심원 파면 (k = 1..4.5)
 for(let m=1;m<=8;m++){
  const R=m*(lam/2),isCrest=(m%2===0);
  // S1
  const c1=invS1?!isCrest:isCrest;
  c.beginPath();c.setLineDash(c1?[]:[5,4]);c.strokeStyle='#2563eb';c.lineWidth=1.5;
  c.arc(s1x,sy,R,Math.PI,2*Math.PI);c.stroke();
  // S2
  c.beginPath();c.setLineDash(isCrest?[]:[5,4]);c.strokeStyle='#e11d48';c.lineWidth=1.5;
  c.arc(s2x,sy,R,Math.PI,2*Math.PI);c.stroke();
 }
 c.setLineDash([]);
 dot(s1x,sy,6,'#2563eb');txt('S₁'+(invS1?'(위상반대)':''),s1x,sy+15,'#2563eb',12);
 dot(s2x,sy,6,'#e11d48');txt('S₂',s2x,sy+15,'#e11d48',12);

 // 교점 계산 함수 (r1, r2 거리인 위쪽 교점)
 function pt(r1,r2){
  const d=s2x-s1x,x=(r1*r1-r2*r2+d*d)/(2*d),y=Math.sqrt(Math.max(0,r1*r1-x*x));
  return [s1x+x,sy-y];
 }
 const pA=pt(3*lam,3*lam),pB=pt(3*lam,2.5*lam),pC=pt(3.5*lam,2.5*lam),pD=pt(3.5*lam,2*lam);
 [[pA,'A (Δr=0)',!invS1],[pB,'B (Δr=λ/2)',invS1],[pC,'C (Δr=λ)',!invS1],[pD,'D (Δr=3λ/2)',invS1]].forEach(q=>{
  dot(q[0][0],q[0][1],6,q[2]?'#059669':'#ea580c');
  txt(q[1],q[0][0]+6,q[0][1]-13,q[2]?'#059669':'#ea580c',12,'left');
 });
 txt('실선 = 마루, 점선 = 골  |  초록 점 = 보강 간섭, 주황 점 = 상쇄 간섭',320,18,'#0f172a',12.5);
 const cyC=Math.cos(2*Math.PI*t)*2;
 txt('C 지점(골+골 보강)의 현재 변위 = '+f(cyC,1)+' A (+2A와 −2A 사이를 크게 진동!)',320,256,'#7c3aed',12.5);
}
document.getElementById('s1_0').onclick=()=>{invS1=false};
document.getElementById('s1_1').onclick=()=>{invS1=true};
"""
EX3 = '<button class="b" id="s1_0">같은 위상 (기본)</button><button class="b" id="s1_1">(4) S₁ 위상 반대로</button>'

# ---------------- 4. 스피커 S1, S2와 측정 경로 O -> Q (L1=3.17 m, L2=3.00 m) ----------------
JS4 = r"""
SP=1;let hiF=false;
function draw(){
 const cx=320,s1x=250,s2x=390,sy=215,py=85;
 const qx=hiF?cx+52:cx+78;
 // 측정 경로 및 세기 곡선
 line(80,py,560,py,'#64748b',1.5,[5,4]);txt('측정 경로',560,py+15,'#475569',11,'right');
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=2.2;
 const wSp=hiF?Math.PI/(52):Math.PI/(78);
 for(let x=90;x<=550;x+=2){const I=Math.pow(Math.cos((x-cx)*wSp/2),2);const y=py-I*42;x===90?c.moveTo(x,y):c.lineTo(x,y)}c.stroke();
 txt('소리 세기 분포',135,py-48,'#7c3aed',11.5);

 // 스피커 S1, S2
 box(s1x-18,sy-12,36,24,'S₁','#dbeafe');
 box(s2x-18,sy-12,36,24,'S₂','#fee2e2');
 // 점 O, 점 Q
 dot(cx,py,6,'#059669');txt('O (중심 보강)',cx,py+16,'#059669',12);
 dot(qx,py,6,'#e11d48');txt('Q (첫 상쇄)',qx+8,py+16,'#e11d48',12,'left');
 line(s1x,sy-12,qx,py,'#2563eb',2);line(s2x,sy-12,qx,py,'#e11d48',2);
 if(!hiF){
  txt('L₁ = 3.17 m',(s1x+qx)/2-28,(sy+py)/2,'#2563eb',12);
  txt('L₂ = 3.00 m',(s2x+qx)/2+28,(sy+py)/2,'#e11d48',12);
  txt('Q 경로차 ΔL = 3.17 − 3.00 = 0.17 m = λ/2 (반 파장의 1배) → λ = 0.34 m, f = 340/0.34 = 1000 Hz',320,252,'#0f172a',12);
 }else{
  dbl(cx,py-16,qx,py-16,'#e11d48');txt('거리 가까워짐!',(cx+qx)/2,py-28,'#e11d48',12);
  txt('(4) 진동수를 높이면 파장 λ가 짧아져 경로차가 λ/2가 되는 첫 상쇄 지점 Q가 O에 더 가까워진다!',320,252,'#1d4ed8',12);
 }
}
document.getElementById('f_1000').onclick=()=>{hiF=false};
document.getElementById('f_1500').onclick=()=>{hiF=true};
"""
EX4 = '<button class="b" id="f_1000">f = 1000 Hz (문제 조건)</button><button class="b" id="f_1500">(4) 진동수 높였을 때</button>'

# ---------------- 5. 두 스피커 680 Hz와 점 A(4.0, 5.0 m), B(3.75, 3.00 m) ----------------
JS5 = r"""
SP=1;let mode=1;
function draw(){
 const s1x=65,s1y=75,s2x=65,s2y=185,ax=510,ay=55,bx=430,by=175;
 box(s1x-18,s1y-14,36,28,'S₁','#dbeafe');
 box(s2x-18,s2y-14,36,28,'S₂'+(mode===3?'(반전)':''),'#fee2e2');
 line(s1x+18,s1y,ax,ay,'#2563eb',1.8);line(s2x+18,s2y,ax,ay,'#e11d48',1.8,[5,4]);
 line(s1x+18,s1y,bx,by,'#2563eb',1.8);line(s2x+18,s2y,bx,by,'#e11d48',1.8,[5,4]);
 txt('4.0 m',280,52,'#2563eb',11.5);txt('5.0 m',310,112,'#e11d48',11.5);
 txt('3.75 m',230,138,'#2563eb',11.5);txt('3.00 m',250,192,'#e11d48',11.5);

 let aCon=true,bCon=false,msg1='',msg2='';
 if(mode===1){
  aCon=true;bCon=false;
  msg1='f = 680 Hz → 파장 λ = 340/680 = 0.5 m (반 파장 = 0.25 m)';
  msg2='A: Δr = 1.0 m = 4×(λ/2) [짝수배 → 보강]  |  B: Δr = 0.75 m = 3×(λ/2) [홀수배 → 상쇄]';
 }else if(mode===2){
  aCon=false;bCon=true;
  msg1='(3) 진동수를 낮춰 B(Δr = 0.75 m)에서 보강 간섭이 되는 최대 진동수: λ = 0.75 m';
  msg2='f = v / λ = 340 / 0.75 ≈ 453 Hz → B에서 경로차가 1λ(반 파장의 2배)가 되어 보강 간섭!';
 }else{
  aCon=false;bCon=true;
  msg1='(4) f = 680 Hz에서 S₂의 위상만 반대로 바꾼 경우 (보강 ↔ 상쇄 반전)';
  msg2='A: 보강 → 상쇄 (소리 작아짐)  |  B: 상쇄 → 보강 (소리 커짐)';
 }
 dot(ax,ay,8,aCon?'#059669':'#ea580c');txt('A ('+(aCon?'보강·소리 큼':'상쇄·소리 작음')+')',ax+14,ay,aCon?'#059669':'#ea580c',13,'left');
 dot(bx,by,8,bCon?'#059669':'#ea580c');txt('B ('+(bCon?'보강·소리 큼':'상쇄·소리 작음')+')',bx+14,by,bCon?'#059669':'#ea580c',13,'left');
 txt(msg1,320,22,'#0f172a',13);
 txt(msg2,320,248,'#1d4ed8',12.5);
}
document.getElementById('q5_1').onclick=()=>{mode=1};
document.getElementById('q5_2').onclick=()=>{mode=2};
document.getElementById('q5_3').onclick=()=>{mode=3};
"""
EX5 = ('<button class="b" id="q5_1">(1)(2) 680 Hz 기본</button>'
       '<button class="b" id="q5_2">(3) 453 Hz (B 보강)</button>'
       '<button class="b" id="q5_3">(4) S₂ 위상 반대</button>')

# ---------------- 6. 소음 제거 이어폰 (주기 2 ms, 500 Hz) ----------------
JS6 = r"""
SP=1;let mode=1;
function draw(){
 const ox=60,gw=530,ps=115,y1=68,y2=175,A=26;
 // (가) 소음
 axes(ox,y1,gw,38,'시간(ms)','압력');
 txt('(가) 감지된 소음: 주기 T = 2 ms → 진동수 f = 1 / 0.002 s = 500 Hz',ox+70,y1-42,'#0f172a',12.5,'left');
 for(let m=1;m<=4;m++){line(ox+m*ps,y1-3,ox+m*ps,y1+3,'#0f172a',1);txt(String(m),ox+m*ps,y1+13,'#475569',10)}
 c.beginPath();c.strokeStyle='#0f172a';c.lineWidth=2.5;
 for(let ms=0;ms<=4.3;ms+=0.02){
  const n=mode===3?(0.65*Math.sin(Math.PI*ms)+0.35*Math.sin(2.7*Math.PI*ms+1)):Math.sin(Math.PI*ms);
  const x=ox+ms*ps,y=y1-A*n;ms?c.lineTo(x,y):c.moveTo(x,y);
 }c.stroke();

 // (나) 이어폰이 만들 소리 + 남은 합성 소음(점선)
 axes(ox,y2,gw,38,'시간(ms)','압력');
 for(let m=1;m<=4;m++){line(ox+m*ps,y2-3,ox+m*ps,y2+3,'#0f172a',1);txt(String(m),ox+m*ps,y2+13,'#475569',10)}
 const amp=mode===2?0.55:1.0;
 c.beginPath();c.strokeStyle='#e11d48';c.lineWidth=2.5;
 for(let ms=0;ms<=4.3;ms+=0.02){
  const anti=mode===3?(-0.8*(0.65*Math.sin(Math.PI*(ms-0.25))+0.35*Math.sin(2.7*Math.PI*(ms-0.25)+1))):(-amp*Math.sin(Math.PI*ms));
  const x=ox+ms*ps,y=y2-A*anti;ms?c.lineTo(x,y):c.moveTo(x,y);
 }c.stroke();
 // 합성파 (보라색 점선)
 c.beginPath();c.setLineDash([5,3]);c.strokeStyle='#7c3aed';c.lineWidth=2.5;
 for(let ms=0;ms<=4.3;ms+=0.02){
  const n=mode===3?(0.65*Math.sin(Math.PI*ms)+0.35*Math.sin(2.7*Math.PI*ms+1)):Math.sin(Math.PI*ms);
  const anti=mode===3?(-0.8*(0.65*Math.sin(Math.PI*(ms-0.25))+0.35*Math.sin(2.7*Math.PI*(ms-0.25)+1))):(-amp*Math.sin(Math.PI*ms));
  const x=ox+ms*ps,y=y2-A*(n+anti);ms?c.lineTo(x,y):c.moveTo(x,y);
 }c.stroke();c.setLineDash([]);

 const lab=mode===1?'(나) 이어폰 소리(빨강): 500 Hz, 같은 진폭, 반대 위상(위아래 뒤집음) → 합성파(보라) = 0!'
          :(mode===2?'(3) 이어폰 소리 진폭이 작을 때: 완전히 상쇄되지 않고 진폭 차이만큼 소음이 남음(보라 점선)'
                   :'(4) 불규칙 소음: 파형이 계속 변해 반대 위상을 정확히 맞추기 어려워 잔여 소음이 남음');
 txt(lab,ox+70,y2-42,'#e11d48',12,'left');
 txt('빨간 실선 = (나) 이어폰이 만든 소리  |  보라 점선 = 귀에 들리는 남은 소리(합성파)',320,252,'#7c3aed',12.5);
}
document.getElementById('a_ok').onclick=()=>{mode=1};
document.getElementById('a_sm').onclick=()=>{mode=2};
document.getElementById('a_ir').onclick=()=>{mode=3};
"""
EX6 = ('<button class="b" id="a_ok">(2) 반대 위상·같은 진폭</button>'
       '<button class="b" id="a_sm">(3) 진폭 작을 때</button>'
       '<button class="b" id="a_ir">(4) 불규칙 소음</button>')

# ---------------- 7. 자동차 배기 소음기 (길이 차 1 m: 170 Hz, 510 Hz, 340 Hz) ----------------
JS7 = r"""
SP=1;let fr=170;
function draw(){
 const lam=340/fr,dl=1.0,ph=2*Math.PI*dl/lam;
 // 배기 소음기 관 모식도
 c.strokeStyle='#1e293b';c.lineWidth=2;
 c.strokeRect(30,68,70,26);c.strokeRect(540,68,70,26);
 c.beginPath();c.moveTo(100,68);c.lineTo(150,32);c.lineTo(490,32);c.lineTo(540,68);c.stroke();
 c.beginPath();c.moveTo(100,94);c.lineTo(150,130);c.lineTo(490,130);c.lineTo(540,94);c.stroke();
 txt('엔진 소음',65,110,'#475569',11.5);txt('배출',575,110,'#475569',11.5);
 txt('통로 1 (길이 l₁)',320,20,'#2563eb',12);
 txt('통로 2 (길이 l₂ = l₁ + 1.0 m)',320,145,'#e11d48',12);

 // 통로 1, 통로 2, 합쳐진 파형
 const ox=140,gw=360,y0=202;
 line(ox,y0,ox+gw,y0,'#cbd5e1',1.5);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2;
 for(let x=0;x<=gw;x+=3){const y=y0-18*Math.sin(x/22-t*3);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();
 c.beginPath();c.setLineDash([4,3]);c.strokeStyle='#e11d48';c.lineWidth=2;
 for(let x=0;x<=gw;x+=3){const y=y0-18*Math.sin(x/22-t*3-ph);x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();c.setLineDash([]);
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=3.2;
 for(let x=0;x<=gw;x+=3){const y=y0-18*(Math.sin(x/22-t*3)+Math.sin(x/22-t*3-ph));x?c.lineTo(ox+x,y):c.moveTo(ox+x,y)}c.stroke();

 const nHalf=dl/(lam/2),isCancel=Math.abs(nHalf-Math.round(nHalf))<0.05&&(Math.round(nHalf)%2===1);
 txt('진동수 f = '+fr+' Hz → 파장 λ = '+lam.toFixed(2)+' m  |  길이 차 1 m = 반 파장('+(lam/2).toFixed(2)+' m)의 '+nHalf.toFixed(0)+'배 ('+(isCancel?'홀수 → 상쇄 간섭!':'짝수 → 보강 간섭!')+')',320,252,isCancel?'#059669':'#e11d48',12.5);
}
document.getElementById('mf170').onclick=()=>{fr=170};
document.getElementById('mf510').onclick=()=>{fr=510};
document.getElementById('mf340').onclick=()=>{fr=340};
"""
EX7 = ('<button class="b" id="mf170">(1) 170 Hz (상쇄)</button>'
       '<button class="b" id="mf510">(2) 510 Hz (상쇄)</button>'
       '<button class="b" id="mf340">(3) 340 Hz (보강)</button>')

# ---------------- 8. 공연장 두 스피커(6.5 m, 6.0 m)와 좌석 X ----------------
JS8 = r"""
SP=1;let mode=1;
function draw(){
 const sx=85,s1y=60,s2y=185,xx=490,xy=135;
 c.fillStyle='#fef3c7';c.fillRect(25,40,36,165);c.strokeStyle='#b45309';c.strokeRect(25,40,36,165);
 txt('무대',43,122,'#92400e',13);
 box(sx-16,s1y-14,34,28,'S₁','#dbeafe');
 box(sx-16,s2y-14,34,28,'S₂'+(mode===2?'(반전)':''),'#fee2e2');
 line(sx+18,s1y,xx,xy,'#2563eb',2,[5,4]);
 line(sx+18,s2y,xx,xy,'#e11d48',2,[5,4]);
 txt('6.5 m',290,82,'#2563eb',12.5);
 txt('6.0 m',290,175,'#e11d48',12.5);

 const isLoud=(mode!==1);
 box(xx-22,xy-18,44,36,'좌석 X',isLoud?'#dcfce7':'#fee2e2');
 txt(isLoud?'🔊 소리 크게 들림 (보강)':'🔇 소리 작게 들림 (상쇄)',xx,xy-32,isLoud?'#059669':'#e11d48',13);

 let m1='',m2='';
 if(mode===1){
  m1='(1) f = 340 Hz → 파장 λ = 340/340 = 1.0 m  |  경로차 Δr = 6.5 − 6.0 = 0.5 m';
  m2='경로차 0.5 m = 반 파장(0.5 m)의 1배(홀수) → 상쇄 간섭이 일어나 소리가 작게 들린다!';
 }else if(mode===2){
  m1='(2) 해결 방법 ①: 한쪽 스피커(S₂)의 위상을 반대로 바꾼다 (또는 스피커 위치를 옮겨 경로차를 0이나 1 m로 조정)';
  m2='위상을 반대로 바꾸면 반 파장 홀수 배(0.5 m) 지점인 좌석 X에서 같은 위상으로 만나 보강 간섭이 일어난다!';
 }else{
  m1='(3) f = 680 Hz → 파장 λ = 340/680 = 0.5 m  |  경로차 Δr = 0.5 m';
  m2='경로차 0.5 m = 한 파장(λ = 0.5 m, 반 파장의 2배·짝수) → 보강 간섭이 일어나 소리가 크게 들린다!';
 }
 txt(m1,320,20,'#0f172a',12.5);
 txt(m2,320,250,isLoud?'#059669':'#e11d48',12.5);
}
document.getElementById('c8_1').onclick=()=>{mode=1};
document.getElementById('c8_2').onclick=()=>{mode=2};
document.getElementById('c8_3').onclick=()=>{mode=3};
"""
EX8 = ('<button class="b" id="c8_1">(1) 340 Hz (상쇄)</button>'
       '<button class="b" id="c8_2">(2) S₂ 위상 반전 (보강)</button>'
       '<button class="b" id="c8_3">(3) 680 Hz (보강)</button>')

SIMS = {
    1: ("두 펄스 A(+2 cm)와 B(−1 cm / +1 cm)의 중첩과 독립성", JS1, EX1),
    2: ("(가) 같은 위상(보강 간섭) vs (나) 반대 위상(상쇄 간섭)", JS2, ""),
    3: ("두 음원 S₁, S₂의 마루·골 간섭 무늬와 A, B, C, D 경로차", JS3, EX3),
    4: ("두 스피커에서 첫 상쇄 지점 Q까지의 경로차와 파장", JS4, EX4),
    5: ("680 Hz 두 스피커에서 점 A(4.0, 5.0 m)와 점 B(3.75, 3.00 m)의 간섭", JS5, EX5),
    6: ("소음 제거 이어폰(ANC): 반대 위상 파형 생성과 상쇄", JS6, EX6),
    7: ("자동차 배기 소음기: 두 통로의 길이 차와 진동수별 간섭", JS7, EX7),
    8: ("공연장 좌석 X(6.5 m, 6.0 m)에서의 음파 간섭과 개선 방법", JS8, EX8),
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
    st.title("📝 음파의 간섭과 소음 제어 형성평가 문제 풀이")
    st.caption("Ⅲ. 탄성파와 소리 · 04 음파의 간섭과 소음 제어 [12역학03-04]")
    st.markdown("각 문항의 문제 상황을 시뮬레이션으로 확인하고, 직접 풀어 본 뒤 **해설 및 정답을 펼쳐** 확인하세요.")
    st.markdown("---")

    B1, B2, B3 = "#eff6ff", "#ecfdf5", "#faf5ff"

    problem(1, B1, "기본",
            "그림은 줄을 따라 서로 반대 방향으로 1 cm/s의 속력으로 진행하는 두 펄스 A, B의 t = 0일 때 모습이다. (모눈 한 칸은 1 cm이고, A의 꼭짓점은 +2 cm, B의 꼭짓점은 −1 cm이며 두 꼭짓점 사이 거리는 7 cm이다.)",
            ["(1) 두 펄스가 만나 겹쳐질 때 합성파의 변위는 어떻게 정해지는지 쓰시오.",
             "(2) t = 3.5 s일 때 두 펄스의 꼭짓점이 겹치는 곳의 변위를 구하시오.",
             "(3) B가 위쪽으로 볼록(높이 1 cm)하다면 (2)의 변위는 얼마가 되겠는지 구하시오.",
             "(4) 두 펄스가 서로 지나간 뒤 각 펄스의 모양은 어떻게 되는지 쓰시오."],
            r"""
- **(1)** **두 펄스의 변위를 더한 값**이 합성파의 변위이다 (**중첩 원리**).
- **(2)** $t = 3.5\text{ s}$일 때 A의 꼭짓점($+2\text{ cm}$)과 B의 꼭짓점($-1\text{ cm}$)이 같은 위치에서 겹치므로 $2 + (-1) =$ **$+1\text{ cm}$**
- **(3)** $2 + 1 =$ **$3\text{ cm}$**
- **(4)** **원래 모양과 크기 그대로** 각자 진행한다 (**파동의 독립성**).

*채점 포인트: (2) 변위를 부호까지 고려해 더하는가($2 - 1 = 1\text{ cm}$).*
""")

    problem(2, B1, "기본",
            "그림 (가), (나)는 한 지점에 도달한 진폭 A, 진동수가 같은 두 음파(실선, 점선)의 변위를 시간에 따라 나타낸 것이다. ((가)는 두 파동의 위상이 같고, (나)는 위상이 반대이다.)",
            ["(1) (가), (나)에서 일어나는 간섭의 종류를 각각 쓰시오.",
             "(2) (가), (나)에서 합성파의 진폭을 각각 쓰시오.",
             "(3) (가)와 (나) 중 소리가 크게 들리는 것을 쓰고, 그 까닭을 쓰시오.",
             "(4) (가)에서 합성파의 진동수는 원래 음파의 진동수와 비교하여 어떠한지 쓰시오."],
            r"""
- **(1)** (가) **보강 간섭**, (나) **상쇄 간섭**
- **(2)** (가) **$2A$**, (나) **$0$**
- **(3)** **(가)**. 두 음파가 **같은 위상으로 만나 합성파의 진폭이 커지므로** 소리가 크게 들린다.
- **(4)** **같다.** 간섭은 진폭만 바꾸고 **진동수는 바꾸지 않는다.**
""")

    problem(3, B2, "보통",
            "그림은 두 음원 S₁, S₂에서 진폭과 진동수가 같은 음파가 같은 위상으로 발생할 때 어느 순간의 마루(실선)와 골(점선)을 나타낸 것이다. 음파의 파장은 λ이다.",
            ["(1) A, B, C, D에서 두 음원까지의 경로차를 각각 λ를 써서 나타내시오.",
             "(2) A, B, C, D 중 상쇄 간섭이 일어나는 지점을 모두 쓰고, 그 까닭을 쓰시오.",
             "(3) C에서 합성파의 변위는 시간에 따라 어떻게 되는지 서술하시오.",
             "(4) S₁에서 발생하는 음파의 위상만 반대로 바꾸면 A에서 일어나는 간섭의 종류를 쓰시오."],
            r"""
- **(1)** A: **$0$**, B: **$\dfrac{\lambda}{2}$**, C: **$\lambda$**, D: **$\dfrac{3\lambda}{2}$**
- **(2)** **B, D**. 경로차가 **반 파장($\lambda/2$)의 홀수 배**여서 두 파동이 **반대 위상(마루와 골)**으로 만나기 때문이다.
- **(3)** 골과 골이 만나는 **보강 간섭 지점**이므로, 변위가 **$+2A$와 $-2A$ 사이에서 시간에 따라 크게 진동한다** (항상 골에 머무는 것이 아님).
- **(4)** **상쇄 간섭**

*채점 포인트: (3) '보강 간섭 지점도 변위가 시간에 따라 $+2A \leftrightarrow -2A$로 진동한다'는 점을 명확히 서술하는가.*
""")

    problem(4, B2, "보통",
            "두 스피커 S₁, S₂에서 진동수가 같은 소리를 같은 위상으로 발생시키고, 두 스피커에서 같은 거리에 있는 점 O에서부터 측정 경로를 따라 이동하였더니 O에서 소리가 크게, Q에서 처음으로 가장 작게 들렸다. L₁ = 3.17 m, L₂ = 3.00 m이다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) O에서 보강 간섭이 일어나는 까닭을 쓰시오.",
             "(2) Q에서의 경로차는 반 파장의 몇 배인지 쓰고, 소리의 파장을 구하시오.",
             "(3) 소리의 진동수를 구하시오.",
             "(4) 진동수를 더 높이면 O와 Q 사이의 거리는 어떻게 달라지는지 까닭과 함께 쓰시오."],
            r"""
- **(1)** O는 두 스피커에서 같은 거리(**경로차 0**)에 있어 두 소리가 **같은 위상으로 만나기 때문**이다.
- **(2)** O에서 이동하여 **처음으로 상쇄**되는 지점이므로 경로차는 **반 파장의 1배**이다. $\dfrac{\lambda}{2} = 3.17 - 3.00 = 0.17\text{ m}$ → $\lambda =$ **0.34 m**
- **(3)** $f = \dfrac{v}{\lambda} = \dfrac{340}{0.34} =$ **1000 Hz**
- **(4)** **가까워진다.** 진동수를 높이면 **파장($\lambda$)이 짧아져** 경로차가 반 파장($\lambda/2$)이 되는 지점이 O에 더 가까워지기 때문이다.

*채점 포인트: (2) '처음으로 작게 들리는 지점'이 반 파장의 1배임을 연결하는가.*
""")

    problem(5, B3, "심화",
            "두 스피커 S₁, S₂에서 진동수 680 Hz의 소리가 같은 위상으로 발생한다. 점 A는 S₁, S₂에서 각각 4.0 m, 5.0 m, 점 B는 3.75 m, 3.00 m 떨어져 있다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) 소리의 파장을 구하시오.",
             "(2) A, B에서의 경로차를 구하고, 각각 일어나는 간섭의 종류를 근거와 함께 쓰시오.",
             "(3) 진동수를 낮추어 B에서 보강 간섭이 일어나게 하려면, 진동수를 최대 몇 Hz로 하면 되는지 구하시오.",
             "(4) 진동수는 680 Hz로 두고 S₂의 위상만 반대로 하면 A, B에서 소리의 세기는 각각 어떻게 되는지 쓰시오."],
            r"""
- **(1)** $\lambda = \dfrac{v}{f} = \dfrac{340}{680} =$ **0.5 m** (반 파장 $\dfrac{\lambda}{2} = 0.25\text{ m}$)
- **(2)**
  - **A**: 경로차 $|4.0 - 5.0| = 1.0\text{ m} = 2\lambda =$ **반 파장의 4배(짝수)** → **보강 간섭**
  - **B**: 경로차 $|3.75 - 3.00| = 0.75\text{ m} = 1.5\lambda =$ **반 파장의 3배(홀수)** → **상쇄 간섭**
- **(3)** B의 경로차 $0.75\text{ m}$가 한 파장의 정수 배($n\lambda$)가 되어야 한다. 진동수를 낮추어 처음으로 보강이 되는 최대 진동수는 $\lambda = 0.75\text{ m}$일 때이므로, $f = \dfrac{340}{0.75} \approx$ **453 Hz**
- **(4)** **A: 작아짐(상쇄 간섭)**, **B: 커짐(보강 간섭)**

*채점 포인트: (3) 진동수를 낮추면 파장이 길어지므로 $0.75\text{ m} = 1\lambda$일 때가 최대 진동수임을 확인하는가.*
""")

    problem(6, B3, "심화",
            "그림 (가)는 소음 제거 이어폰의 마이크에 감지된 소음의 압력 변화를 시간에 따라 나타낸 것이다. (소음의 한 주기는 2 ms이다.)",
            ["(1) 소음의 주기와 진동수를 구하시오.",
             "(2) 이어폰이 만들어야 할 소리의 진동수, 진폭, 위상 조건을 쓰고, (나)에 그 소리의 그래프를 그리시오.",
             "(3) 이어폰이 만든 소리의 진폭이 소음의 진폭보다 작으면 어떻게 되는지 서술하시오.",
             "(4) 소음 제거 이어폰이 불규칙한 소음보다 규칙적인 소음을 더 잘 줄이는 까닭을 서술하시오."],
            r"""
- **(1)** 주기 **2 ms ($0.002\text{ s}$)**, 진동수 $f = \dfrac{1}{0.002\text{ s}} =$ **500 Hz**
- **(2)** 진동수는 **500 Hz(소음과 같게)**, 진폭은 **소음과 같게**, 위상은 **소음과 반대($180^\circ$ 차이)**로 만들어야 한다. 그래프는 **(가)를 위아래로 뒤집은 모양**으로 그린다.
- **(3)** 완전히 상쇄되지 않고 **진폭 차이만큼 소음이 남는다** (원래보다는 소리가 작아진다).
- **(4)** 규칙적인 소음은 진동수와 파형이 일정해 반대 위상의 소리를 정확히 예측해 만들 수 있지만, **불규칙한 소음은 파형이 계속 변해 반대 위상을 실시간으로 맞추기 어렵기 때문**이다.

*채점 포인트: (2) 그래프의 시작 방향이 (가)와 반대로 뒤집혀 있는지 확인.*
""")

    problem(7, B3, "심화",
            "그림은 자동차 배기 소음기의 구조를 나타낸 것이다. 엔진 소음은 두 통로로 나뉘었다가 다시 합쳐진다. 소음기 안에서 소리의 속력은 340 m/s로 한다.",
            ["(1) 진동수 170 Hz의 소음을 줄이기 위한 두 통로의 최소 길이 차를 풀이 과정과 함께 구하시오.",
             "(2) 길이 차가 (1)과 같을 때, 상쇄 간섭으로 함께 줄어드는 다른 진동수를 한 가지 구하시오.",
             "(3) 같은 소음기에서 진동수 340 Hz의 소음은 줄어드는지 근거와 함께 쓰시오.",
             "(4) 하나의 소음기로 모든 엔진 소음을 줄이기 어려운 까닭을 서술하시오."],
            r"""
- **(1)** $\lambda = \dfrac{340}{170} = 2\text{ m}$이므로, 상쇄 간섭이 일어나는 최소 길이 차는 **반 파장의 1배**인 $\dfrac{\lambda}{2} =$ **1 m**이다.
- **(2)** 길이 차 $1\text{ m}$가 반 파장의 홀수 배($3, 5, \dots$)가 되는 진동수: $\dfrac{\lambda}{2} = \dfrac{1}{3}\text{ m} \rightarrow \lambda = \dfrac{2}{3}\text{ m} \rightarrow f = \dfrac{340}{2/3} =$ **510 Hz** (또는 **850 Hz** 등)
- **(3)** **줄어들지 않는다.** $340\text{ Hz}$의 파장은 $\lambda = \dfrac{340}{340} = 1\text{ m}$이므로, 길이 차 $1\text{ m}$는 **한 파장(반 파장의 2배·짝수)**이 되어 **보강 간섭**이 일어나기 때문이다.
- **(4)** 통로의 길이 차가 정해지면 반 파장의 홀수 배 조건을 만족하는 **특정 진동수의 소음만 상쇄**되므로, 여러 진동수가 섞인 모든 엔진 소음을 한 번에 줄일 수 없다.

*채점 포인트: (2), (3)에서 '반 파장의 홀수 배 / 짝수 배'를 판단 근거로 제시하는가.*
""")

    problem(8, B3, "심화",
            "그림과 같이 공연장 무대의 두 스피커 S₁, S₂에서 진동수 340 Hz의 소리가 같은 위상으로 나오고 있다. 좌석 X는 S₁, S₂에서 각각 6.5 m, 6.0 m 떨어져 있다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) X에서 소리가 크게 들리는지 작게 들리는지 경로차를 근거로 쓰시오.",
             "(2) X에서 소리가 크게 들리게 하는 방법을 두 가지 서술하시오.",
             "(3) 같은 스피커에서 진동수 680 Hz의 소리가 나올 때 X에서 일어나는 간섭을 쓰시오.",
             "(4) 공연장 설계와 체외 충격파 쇄석기에서 공통으로 이용하는 간섭을 쓰고, 그 원리를 서술하시오."],
            r"""
- **(1)** 파장 $\lambda = \dfrac{340}{340} = 1.0\text{ m}$이고, 경로차는 $6.5 - 6.0 = 0.5\text{ m}$로 **반 파장($0.5\text{ m}$)의 1배(홀수)**이므로 **상쇄 간섭**이 일어나 **소리가 작게 들린다.**
- **(2)** ① **한쪽 스피커의 위상을 반대로 바꾼다.** ② **스피커 하나의 위치를 옮겨 경로차를 $0\text{ m}$ 또는 $1.0\text{ m}$(반 파장의 짝수 배)로 만든다.**
- **(3)** $\lambda = \dfrac{340}{680} = 0.5\text{ m}$이므로 경로차 $0.5\text{ m}$가 **한 파장(반 파장의 2배)**이 되어 **보강 간섭**이 일어난다.
- **(4)** **보강 간섭**. 여러 곳에서 나온 음파(또는 충격파)가 목표 지점에 **같은 위상으로 도달하여 만나게 함으로써 합성파의 진폭(세기)을 크게** 만든다.

*채점 포인트: (2) 위상 반전과 경로차(위치) 조정 중 근거가 타당하면 정답 인정.*
""")


run_sim()

