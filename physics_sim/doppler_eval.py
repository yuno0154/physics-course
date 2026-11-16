import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 도플러 효과 형성평가(8문항) — 문제 상황 시뮬레이션 + 펼침식 해설/정답
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


# ---------------- 1. 음원 이동 (600 Hz, 40 m/s -> A) ----------------
JS1 = r"""
SP=1;const cy=115,x0=250,V=52,vs=V*(40/340)*2.2;
function draw(){
 const s=t%4.5,N=Math.floor(s);
 line(30,cy+42,610,cy+42,'#cbd5e1',2);
 // 측정기 B (왼쪽), 측정기 A (오른쪽)
 box(42,cy-6,28,46,'','#f1f5f9');dot(56,cy+17,7,'#ea580c');txt('측정기 B',56,cy-18,'#ea580c',13);
 box(570,cy-6,28,46,'','#f1f5f9');dot(584,cy+17,7,'#059669');txt('측정기 A',584,cy-18,'#059669',13);
 for(let n=0;n<=N;n++){
  const xs=x0+vs*n,R=V*(s-n);
  if(R>1){c.beginPath();c.strokeStyle=n===N?'#1d4ed8':'#60a5fa';c.lineWidth=n===N?2.2:1.5;c.arc(xs,cy,R,0,7);c.stroke()}
 }
 const xsNow=x0+vs*s;
 box(xsNow-26,cy+8,52,32,'음원','#fee2e2');dot(xsNow,cy,7,'#e11d48');
 arrow(xsNow+30,cy+22,xsNow+72,cy+22,'#e11d48',2.5);txt('40 m/s',xsNow+51,cy+8,'#e11d48',12);
 if(N>=2){
  const xa=x0+vs*(N-2)+V*(s-(N-2)),xb=x0+vs*(N-1)+V*(s-(N-1));
  dbl(xb,cy+66,xa,cy+66,'#059669');txt('λ_A = 0.5 m',(xa+xb)/2,cy+82,'#059669',12);
  const la=x0+vs*(N-2)-V*(s-(N-2)),lb=x0+vs*(N-1)-V*(s-(N-1));
  dbl(la,cy+66,lb,cy+66,'#ea580c');txt('λ_B ≈ 0.63 m',(la+lb)/2,cy+82,'#ea580c',12);
 }
 txt('음원 진동수 f = 600 Hz  |  소리의 속력 v = 340 m/s (A, B 모두 동일)',320,18,'#0f172a',13);
 txt('측정기 B: f_B = 600×340/380 ≈ 537 Hz (낮음)',24,230,'#ea580c',13,'left');
 txt('측정기 A: λ_A = (340−40)/600 = 0.5 m → f_A = 340/0.5 = 680 Hz (높음)',24,252,'#059669',13,'left');
}
"""

# ---------------- 2. 동심원 파면 간격 (X쪽 1.2 m, Y쪽 0.8 m) ----------------
JS2 = r"""
SP=1;const cy=118,xStart=210,Rstep=28,dx=Rstep*0.2;
function draw(){
 const s=(t*1.1)%5.2;
 txt('X 쪽 (뒤쪽 · 파장 길어짐)',110,24,'#ea580c',13);txt('Y 쪽 (앞쪽 · 파장 짧아짐)',520,24,'#059669',13);
 line(30,cy,610,cy,'#e2e8f0',1);
 const N=Math.floor(s);
 for(let n=0;n<=N;n++){
  const age=s-n,R=age*Rstep,cx=xStart+n*dx;
  if(R>0.5){
   c.beginPath();c.strokeStyle=n===N?'#1d4ed8':'#2563eb';c.lineWidth=n===N?2.3:1.8;
   c.arc(cx,cy,R,0,7);c.stroke();
   dot(cx,cy,2.5,'#94a3b8');
  }
 }
 const curX=xStart+s*dx;
 dot(curX,cy,7,'#e11d48');txt('음원',curX,cy+18,'#0f172a',12);
 arrow(curX+10,cy-14,curX+52,cy-14,'#e11d48',2.5);txt('운동 방향 (Y 쪽, 68 m/s)',curX+58,cy-14,'#e11d48',12,'left');

 // 가장 바깥 두 파면(n=0, n=1) 사이의 간격 표시
 if(s>=1.2){
  const xL0=xStart-s*Rstep,xL1=(xStart+dx)-(s-1)*Rstep;
  const xR1=(xStart+dx)+(s-1)*Rstep,xR0=xStart+s*Rstep;
  const yBar=cy+Math.min(96,s*Rstep*0.75+18);
  line(xL0,cy,xL0,yBar+6,'#94a3b8',1,[3,3]);line(xL1,cy,xL1,yBar+6,'#94a3b8',1,[3,3]);
  dbl(xL0,yBar,xL1,yBar,'#ea580c');txt('1.2 m = λ + vₛT',(xL0+xL1)/2,yBar+15,'#ea580c',12);
  line(xR1,cy,xR1,yBar+6,'#94a3b8',1,[3,3]);line(xR0,cy,xR0,yBar+6,'#94a3b8',1,[3,3]);
  dbl(xR1,yBar,xR0,yBar,'#059669');txt('0.8 m = λ − vₛT',(xR1+xR0)/2,yBar+15,'#059669',12);
 }
 txt('정지 파장 λ = (1.2 + 0.8)/2 = 1.0 m  |  진동수 f = 340/1.0 = 340 Hz  |  음원 속력 vₛ = 0.2×340 = 68 m/s',320,254,'#1d4ed8',12.5);
}
"""
EX2 = '<button class="b" data-t="3.8">파면 4개 순간 보기</button>'

# ---------------- 3. (가) 음원 10 m/s 이동 vs (나) 관찰자 10 m/s 이동 ----------------
JS3 = r"""
SP=1;const V=80,T0=0.7;
function draw(){
 const s=t%4.2;
 // (가) 상단: A가 10 m/s로 B를 향해 이동
 txt('(가) 음원 A가 10 m/s로 이동 (B 정지) → 파장 λ = 0.33 m로 짧아짐, 측정 속력 = 340 m/s',20,16,'#0f172a',12.5,'left');
 const y1=72,vs=18,xA0=90,xB1=560;
 c.fillStyle='#f8fafc';c.fillRect(20,y1-36,600,72);
 const N=Math.floor(s/T0);
 for(let n=0;n<=N;n++){
  const te=n*T0,xwf=(xA0+vs*te)+V*(s-te);
  if(xwf<=xB1)line(xwf,y1-28,xwf,y1+28,'#2563eb',2);
 }
 const xA=xA0+vs*s;
 box(xA-18,y1-16,36,32,'A','#fee2e2');arrow(xA+22,y1,xA+56,y1,'#e11d48',2.5);txt('10 m/s',xA+39,y1-14,'#e11d48',11);
 box(xB1-16,y1-18,32,36,'B','#e2e8f0');txt('f′ ≈ 1030.3 Hz',xB1-30,y1+26,'#059669',12,'right');

 // (나) 하단: B가 10 m/s로 A를 향해 이동
 txt('(나) 측정기 B가 10 m/s로 이동 (A 정지) → 파장 λ = 0.34 m 그대로, 측정 속력 = 350 m/s',20,138,'#0f172a',12.5,'left');
 const y2=194,vo=18,xA2=90,xB2=560-vo*s;
 c.fillStyle='#faf5ff';c.fillRect(20,y2-36,600,72);
 for(let n=0;n<=N;n++){
  const te=n*T0,xwf=xA2+V*(s-te);
  if(xwf<=xB2+20)line(xwf,y2-28,xwf,y2+28,'#2563eb',2);
 }
 box(xA2-18,y2-16,36,32,'A','#e2e8f0');
 box(xB2-16,y2-18,32,36,'B','#ede9fe');arrow(xB2-20,y2,xB2-54,y2,'#7c3aed',2.5);txt('10 m/s',xB2-37,y2-14,'#7c3aed',11);
 txt('f′ ≈ 1029.4 Hz',xB2+24,y2+26,'#7c3aed',12,'left');
 txt('비교: (가) 1000×340/330 ≈ 1030 Hz  >  (나) 1000×350/340 ≈ 1029 Hz',320,254,'#1d4ed8',13);
}
"""

# ---------------- 4. 자동차 A(640 Hz, 20 m/s)와 자전거 B(20 m/s) ----------------
JS4 = r"""
SP=1;let mode=1;
function draw(){
 const s=t%3.8,y=115,V=85,T0=0.65;
 line(20,y+28,620,y+28,'#94a3b8',2);
 let xA0=120,vA=22,xB0=520,vB=-22,fStr='f′ = 640 × (340 + 20)/(340 − 20) = 720 Hz',sub='(1) 서로 20 m/s로 다가갈 때: 파장은 짧아지고(분모 320), B가 측정하는 소리 속력은 커짐(분자 360)';
 if(mode===2){xA0=220;vA=-22;xB0=420;vB=22;fStr='f′ = 640 × (340 − 20)/(340 + 20) ≈ 569 Hz';sub='(3) 서로 20 m/s로 멀어질 때: 파장은 길어지고(분모 360), B가 측정하는 소리 속력은 작아짐(분자 320)'}
 if(mode===3){xA0=110;vA=22;xB0=450;vB=22;fStr='f′ = 640 × (340 − 20)/(340 − 20) = 640 Hz (변화 없음)';sub='(4) 같은 방향으로 20 m/s로 달릴 때: 두 물체 사이의 상대적인 운동이 없으므로 도플러 효과가 나타나지 않음'}
 const xA=xA0+vA*s,xB=xB0+vB*s;
 const N=Math.floor(s/T0);
 for(let n=0;n<=N;n++){
  const te=n*T0,xwf=(xA0+vA*te)+V*(s-te);
  if(xwf<=xB+15&&xwf<620)line(xwf,y-36,xwf,y+24,'#60a5fa',2);
 }
 box(xA-32,y-8,64,32,'자동차 A','#dbeafe');dot(xA-18,y+26,6,'#0f172a');dot(xA+18,y+26,6,'#0f172a');
 arrow(xA,y-22,xA+(vA>0?40:-40),y-22,'#2563eb',2.5);txt('20 m/s',xA+(vA>0?20:-20),y-35,'#2563eb',11);
 dot(xB-12,y+18,9,'#0f172a');dot(xB+12,y+18,9,'#0f172a');line(xB-12,y+18,xB,y-2,'#7c3aed',2);line(xB+12,y+18,xB,y-2,'#7c3aed',2);dot(xB,y-14,6,'#7c3aed');
 txt('관찰자 B',xB,y+44,'#7c3aed',12);
 arrow(xB,y-28,xB+(vB>0?40:-40),y-28,'#7c3aed',2.5);txt('20 m/s',xB+(vB>0?20:-20),y-40,'#7c3aed',11);
 txt(sub,320,24,'#0f172a',12.5);
 txt(fStr,320,225,'#1d4ed8',14.5);
 txt('참고: A의 운동만 고려하면 640×340/320 = 680 Hz (B의 운동까지 고려한 720 Hz와 다름!)',320,252,'#64748b',12);
}
document.getElementById('m1').onclick=()=>{mode=1;t=0};
document.getElementById('m2').onclick=()=>{mode=2;t=0};
document.getElementById('m3').onclick=()=>{mode=3;t=0};
"""
EX4 = '<button class="b" id="m1">(1) 서로 다가감</button><button class="b" id="m2">(3) 서로 멀어짐</button><button class="b" id="m3">(4) 같은 방향</button>'

# ---------------- 5. 음원-측정기 거리-시간 그래프 (900 Hz) ----------------
JS5 = r"""
SP=1.2;const ox=55,oy=195,gw=230,gh=145;
function dist(s){if(s<=5)return 200-20*s;if(s<=10)return 100;return 100+30*(s-10)}
function draw(){
 const s=t%15;
 // 좌측 그래프
 line(ox,oy,ox+gw,oy,'#0f172a',1.5);line(ox,oy-gh,ox,oy,'#0f172a',1.5);
 txt('시간(s)',ox+gw,oy+16,'#475569',11,'right');txt('거리(m)',ox,oy-gh-10,'#475569',11);
 [5,10,15].forEach(k=>{const x=ox+k/15*gw;line(x,oy-3,x,oy+3,'#0f172a',1);txt(String(k),x,oy+14,'#475569',10);line(x,oy,x,oy-gh,'#e2e8f0',1,[3,3])});
 [100,200,250].forEach(d=>{const y=oy-d/260*gh;line(ox-3,y,ox+3,y,'#0f172a',1);txt(String(d),ox-8,y,'#475569',10,'right');line(ox,y,ox+gw,y,'#e2e8f0',1,[3,3])});
 c.beginPath();c.strokeStyle='#be123c';c.lineWidth=2.5;
 c.moveTo(ox,oy-200/260*gh);c.lineTo(ox+5/15*gw,oy-100/260*gh);c.lineTo(ox+10/15*gw,oy-100/260*gh);c.lineTo(ox+gw,oy-250/260*gh);c.stroke();
 const curD=dist(s),px=ox+s/15*gw,py=oy-curD/260*gh;
 dot(px,py,6,'#1d4ed8');

 // 우측 음원 & 측정기 운동
 const rx0=340,ry=115,xDet=355,xSrc=xDet+curD*0.95;
 line(rx0,ry+26,620,ry+26,'#cbd5e1',2);
 box(xDet-16,ry-12,32,36,'측정기','#e2e8f0');
 box(xSrc-20,ry-10,40,34,'음원','#fee2e2');
 dbl(xDet+20,ry+42,xSrc-20,ry+42,'#475569');txt('거리 '+curD.toFixed(0)+' m',(xDet+xSrc)/2,ry+56,'#475569',12);
 let stTxt='',fTxt='',lTxt='';
 if(s<5){
  arrow(xSrc-24,ry-22,xSrc-64,ry-22,'#059669',2.5);txt('20 m/s 다가옴',xSrc-44,ry-35,'#059669',12);
  stTxt='0~5 s 구간: 20 m/s로 다가옴';fTxt='f′ = 900 × 340/(340−20) ≈ 956 Hz';lTxt='파장 λ′ = 320/900 ≈ 0.36 m (짧아짐)';
 }else if(s<10){
  txt('정지 (vₛ = 0)',xSrc,ry-26,'#64748b',12);
  stTxt='5~10 s 구간: 거리 100 m 일정 (정지)';fTxt='f′ = 900 Hz (원래 진동수 그대로)';lTxt='파장 λ = 340/900 ≈ 0.38 m';
 }else{
  arrow(xSrc+24,ry-22,xSrc+68,ry-22,'#ea580c',2.5);txt('30 m/s 멀어짐',xSrc+46,ry-35,'#ea580c',12);
  stTxt='10~15 s 구간: 30 m/s로 멀어짐';fTxt='f′ = 900 × 340/(340+30) ≈ 827 Hz';lTxt='파장 λ′ = 370/900 ≈ 0.41 m (가장 김!)';
 }
 txt('현재 t = '+s.toFixed(1)+' s  |  '+stTxt,330,24,'#0f172a',13,'left');
 txt(fTxt,320,230,'#1d4ed8',14);
 txt(lTxt,320,252,'#059669',12.5);
}
"""
EX5 = '<button class="b" data-t="2">t=2 s</button><button class="b" data-t="7">t=7 s</button><button class="b" data-t="12">t=12 s</button>'

# ---------------- 6. 음원 1020 Hz, 측정기 B (1050 Hz / 990 Hz / 음원 이동 비교) ----------------
JS6 = r"""
SP=1;let mode=1;
function draw(){
 const s=t%3.8,y=110,V=80,T0=0.6;
 c.fillStyle='#f8fafc';c.fillRect(25,y-42,590,84);
 let xS=100,vS=0,xB=520,vB=-20,t1='',t2='',t3='';
 if(mode===1){
  vS=0;vB=-22;
  t1='(1)·(2) 측정기 B가 음원 쪽으로 v_o = 10 m/s 다가갈 때';
  t2='측정 속력 = 340 + 10 = 350 m/s  |  파장 λ = 340/1020 ≈ 0.33 m (그대로)';
  t3='측정 진동수 f′ = 1020 × (340 + 10)/340 = 1050 Hz';
 }else if(mode===2){
  vS=0;xB=380;vB=22;
  t1='(3) 측정기 B가 반대 방향으로 v_o = 10 m/s 멀어질 때';
  t2='측정 속력 = 340 − 10 = 330 m/s  |  파장 λ = 340/1020 ≈ 0.33 m (그대로)';
  t3='측정 진동수 f′ = 1020 × (340 − 10)/340 = 990 Hz';
 }else{
  vS=21;xB=520;vB=0;
  t1='(4) B는 정지하고 음원이 B 쪽으로 v_s ≈ 9.7 m/s로 다가올 때';
  t2='측정 속력 = 340 m/s  |  파장 λ′ = (340 − 9.7)/1020 ≈ 0.324 m (짧아짐)';
  t3='1050 = 1020 × 340/(340 − v_s)  →  v_s = 340 − 330.29 ≈ 9.7 m/s (10 m/s와 다름!)';
 }
 const curS=xS+vS*s,curB=xB+vB*s;
 const N=Math.floor(s/T0);
 for(let n=0;n<=N;n++){
  const te=n*T0,xwf=(xS+vS*te)+V*(s-te);
  if(xwf<=curB+15)line(xwf,y-34,xwf,y+34,'#2563eb',2);
 }
 box(curS-22,y-18,44,36,'음원','#fee2e2');
 if(vS!==0){arrow(curS+26,y,curS+64,y,'#e11d48',2.5);txt('9.7 m/s',curS+45,y-14,'#e11d48',11)}
 box(curB-22,y-18,44,36,'측정기B','#ede9fe');
 if(vB!==0){arrow(curB+(vB<0?-26:26),y,curB+(vB<0?-64:64),y,'#7c3aed',2.5);txt('10 m/s',curB+(vB<0?-45:45),y-14,'#7c3aed',11)}
 txt(t1,320,24,'#0f172a',13.5);
 txt(t2,320,218,'#475569',13);
 txt(t3,320,246,'#1d4ed8',14);
}
document.getElementById('b1').onclick=()=>{mode=1;t=0};
document.getElementById('b2').onclick=()=>{mode=2;t=0};
document.getElementById('b3').onclick=()=>{mode=3;t=0};
"""
EX6 = '<button class="b" id="b1">(1) B 10 m/s 다가감</button><button class="b" id="b2">(3) B 10 m/s 멀어짐</button><button class="b" id="b3">(4) 음원 9.7 m/s 이동</button>'

# ---------------- 7. 압력-시간 그래프와 주기 변화 (2.0 ms / 2.2 ms / 1.8 ms) ----------------
JS7 = r"""
SP=1.8;let mode=2;
function draw(){
 const s=t%8.8;
 const ox=55,oy1=85,oy2=190,gw=540,ps=58; // 1 ms = 58 px
 // (가) 자동차 정지: T = 2.0 ms (f = 500 Hz)
 axes(ox,oy1,gw,34,'시간(ms)','압력');
 txt('(가) 자동차 정지: 주기 T = 2.0 ms, f = 500 Hz',ox+215,oy1-42,'#0f172a',12,'left');
 for(let m=2;m<=8;m+=2){line(ox+m*ps,oy1-3,ox+m*ps,oy1+3,'#0f172a',1);txt(String(m),ox+m*ps,oy1+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#bfdbfe';c.lineWidth=1.5;
 for(let ms=0;ms<=8.8;ms+=0.03){const x=ox+ms*ps,y=oy1-25*Math.sin(2*Math.PI*ms/2.0);ms?c.lineTo(x,y):c.moveTo(x,y)}c.stroke();
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2.8;
 for(let ms=0;ms<=s;ms+=0.03){const x=ox+ms*ps,y=oy1-25*Math.sin(2*Math.PI*ms/2.0);ms?c.lineTo(x,y):c.moveTo(x,y)}c.stroke();
 dot(ox+s*ps,oy1-25*Math.sin(2*Math.PI*s/2.0),5.5,'#2563eb');
 dbl(ox+0.5*ps,oy1-30,ox+2.5*ps,oy1-30,'#2563eb');txt('T = 2.0 ms',ox+1.5*ps,oy1-42,'#2563eb',11.5);

 // (나) 자동차 운동: mode=2 멀어짐 (T'=2.2 ms), mode=3 다가옴 (T'=1.8 ms)
 const T2=mode===2?2.2:1.8,col=mode===2?'#e11d48':'#059669';
 axes(ox,oy2,gw,34,'시간(ms)','압력');
 const lab=mode===2?'(나) 34 m/s 멀어짐: T′ = 2.2 ms, f′ ≈ 455 Hz':'(4) 34 m/s 다가옴: T′ = 1.8 ms, f′ ≈ 556 Hz';
 txt(lab,ox+215,oy2-42,col,12,'left');
 for(let m=2;m<=8;m+=2){line(ox+m*ps,oy2-3,ox+m*ps,oy2+3,'#0f172a',1);txt(String(m),ox+m*ps,oy2+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#e2e8f0';c.lineWidth=1.5;
 for(let ms=0;ms<=8.8;ms+=0.03){const x=ox+ms*ps,y=oy2-25*Math.sin(2*Math.PI*ms/T2);ms?c.lineTo(x,y):c.moveTo(x,y)}c.stroke();
 c.beginPath();c.strokeStyle=col;c.lineWidth=2.8;
 for(let ms=0;ms<=s;ms+=0.03){const x=ox+ms*ps,y=oy2-25*Math.sin(2*Math.PI*ms/T2);ms?c.lineTo(x,y):c.moveTo(x,y)}c.stroke();
 dot(ox+s*ps,oy2-25*Math.sin(2*Math.PI*s/T2),5.5,col);
 dbl(ox+0.25*T2*ps,oy2-30,ox+1.25*T2*ps,oy2-30,col);txt('T′ = '+T2.toFixed(1)+' ms',ox+0.75*T2*ps,oy2-42,col,11.5);

 txt('T′ = T(v ± vₛ)/v → 멀어질 때 2.2 ms (vₛ = 34 m/s), 다가올 때 1.8 ms',320,254,'#0f172a',12);
}
document.getElementById('p2').onclick=()=>{mode=2;t=0};
document.getElementById('p3').onclick=()=>{mode=3;t=0};
"""
EX7 = '<button class="b" id="p2">(나) 멀어질 때 (2.2 ms)</button><button class="b" id="p3">(4) 다가올 때 (1.8 ms)</button>'

# ---------------- 8. 원운동하는 별의 스펙트럼 편이 (A, B, C, D) ----------------
JS8 = r"""
SP=0.8;const cx=135,cy=110,R=68;
function draw(){
 const th=t%(2*Math.PI),sx=cx+R*Math.cos(th),sy=cy-R*Math.sin(th);
 c.beginPath();c.setLineDash([5,4]);c.strokeStyle='#94a3b8';c.lineWidth=1.8;c.arc(cx,cy,R,0,7);c.stroke();c.setLineDash([]);
 dot(cx,cy,3,'#0f172a');txt('O',cx+10,cy,'#475569',12);
 [['A',cx+R+14,cy],['B',cx,cy-R-13],['C',cx-R-14,cy],['D',cx,cy+R+14]].forEach(p=>{txt(p[0],p[1],p[2],'#0f172a',13)});
 // 지구
 dot(cx,238,11,'#60a5fa');txt('지구 (관측)',cx+48,238,'#0f172a',12);
 line(cx,225,cx,cy+R+22,'#cbd5e1',1,[3,3]);
 // 별의 접선 속도 화살표 (반시계 공전: vx = -sin(th), vy = -cos(th))
 const vx=-Math.sin(th),vy=-Math.cos(th);
 arrow(sx,sy,sx+vx*30,sy+vy*30,'#e11d48',2.5);
 const vrad=-Math.cos(th); // +1 at C (approaching Earth), -1 at A (receding from Earth)
 const col=vrad>0.2?'#2563eb':(vrad<-0.2?'#e11d48':'#eab308');
 dot(sx,sy,9,col);

 // 우측 2단 흡수선 스펙트럼 비교 (기준 스펙트럼 vs 별빛 스펙트럼 — 선 스펙트럼 전체 묶음이 함께 이동)
 const x0=265,x1=615,sw=x1-x0,yRef=44,yObs=132,bh=32;
 const grd=c.createLinearGradient(x0,0,x1,0);
 ['#7c3aed','#2563eb','#06b6d4','#22c55e','#eab308','#f97316','#dc2626'].forEach((cl,i)=>grd.addColorStop(i/6,cl));

 txt('① 정지 광원 기준 스펙트럼 (고유 흡수선 묶음)',x0,yRef-12,'#0f172a',12,'left');
 c.fillStyle=grd;c.fillRect(x0,yRef,sw,bh);
 c.strokeStyle='#334155';c.lineWidth=1.2;c.strokeRect(x0,yRef,sw,bh);

 txt('② 지구 관측 별빛 스펙트럼 (선 스펙트럼 전체가 함께 이동!)',x0,yObs-12,col==='#eab308'?'#0f172a':col,12,'left');
 c.fillStyle=grd;c.fillRect(x0,yObs,sw,bh);
 c.strokeStyle='#334155';c.lineWidth=1.2;c.strokeRect(x0,yObs,sw,bh);

 const lines=[0.16,0.28,0.45,0.65,0.82],ws=[2.2,3.0,3.8,2.5,4.2];
 const shift=-vrad*28,aCol=vrad>0.2?'#2563eb':(vrad<-0.2?'#e11d48':'#64748b');
 lines.forEach((p,idx)=>{
  const xr=x0+p*sw,xo=xr+shift,lw=ws[idx];
  c.fillStyle='#0f172a';c.fillRect(xr-lw/2,yRef,lw,bh);
  c.fillStyle='#0f172a';c.fillRect(xo-lw/2,yObs,lw,bh);
  arrow(xr,yRef+bh+3,xo,yObs-22,aCol,1.6);
 });

 txt('◀ 짧은 파장 (청색)',x0,yObs+bh+14,'#2563eb',11.5,'left');
 txt('긴 파장 (적색) ▶',x1,yObs+bh+14,'#e11d48',11.5,'right');
 let st='B·D 부근: 시선 방향과 수직 운동 → 흡수선 전체가 기준 위치와 일치';
 if(vrad>0.2)st='◀ C 부근: 지구로 다가옴 → 흡수선 전체가 짧은 파장 쪽으로 이동 (청색 편이)';
 else if(vrad<-0.2)st='A 부근 ▶: 지구에서 멀어짐 → 흡수선 전체가 긴 파장 쪽으로 이동 (적색 편이)';
 txt(st,440,210,col==='#eab308'?'#0f172a':col,12.5);
 txt('핵심: 특정 선 하나만 움직이는 것이 아니라 흡수선 묶음 전체가 간격을 유지한 채 함께 편이된다!',440,242,'#475569',11.5);
}
"""
EX8 = ('<button class="b" data-t="0">위치 A</button>'
       '<button class="b" data-t="1.5708">위치 B</button>'
       '<button class="b" data-t="3.1416">위치 C</button>'
       '<button class="b" data-t="4.7124">위치 D</button>')

SIMS = {
    1: ("음원이 A 쪽으로 40 m/s 이동할 때 파장과 진동수", JS1, ""),
    2: ("운동하는 음원의 동심원 파면 간격 (1.2 m vs 0.8 m)", JS2, EX2),
    3: ("(가) 음원 이동 vs (나) 관찰자 이동 (10 m/s)", JS3, ""),
    4: ("자동차 A(640 Hz)와 자전거 B의 상대 운동", JS4, EX4),
    5: ("음원–측정기 거리–시간 그래프와 구간별 진동수", JS5, EX5),
    6: ("관찰자 B의 이동(10 m/s)과 음원의 이동(9.7 m/s) 비교", JS6, EX6),
    7: ("공기 압력–시간 그래프에서 측정 주기 T′와 속력 구하기", JS7, EX7),
    8: ("원운동하는 별의 위치(A·B·C·D)에 따른 스펙트럼 편이", JS8, EX8),
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
    st.title("📝 도플러 효과 형성평가 문제 풀이")
    st.caption("Ⅲ. 탄성파와 소리 · 03 도플러 효과와 속도 측정 [12역학03-03]")
    st.markdown("각 문항의 문제 상황을 시뮬레이션으로 확인하고, 직접 풀어 본 뒤 **해설 및 정답을 펼쳐** 확인하세요.")
    st.markdown("---")

    B1, B2, B3 = "#eff6ff", "#ecfdf5", "#faf5ff"

    problem(1, B1, "기본",
            "그림과 같이 정지해 있는 음파 측정기 A, B 사이에서 진동수 600 Hz의 소리를 내는 음원이 A를 향해 40 m/s의 일정한 속력으로 운동한다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) A가 측정하는 소리의 파장을 풀이 과정과 함께 구하시오.",
             "(2) A, B가 측정하는 소리의 진동수 f_A, f_B를 각각 구하시오.",
             "(3) 600 Hz, f_A, f_B의 크기를 부등호로 비교하시오.",
             "(4) A와 B가 측정하는 소리의 속력을 비교하고, 그 까닭을 쓰시오."],
            r"""
- **(1)** $\lambda_A = \dfrac{v - v_s}{f} = \dfrac{340 - 40}{600} =$ **0.5 m**
- **(2)** $f_A = \dfrac{v}{\lambda_A} = \dfrac{340}{0.5} =$ **680 Hz**, $f_B = 600 \times \dfrac{340}{340 + 40} = 600 \times \dfrac{340}{380} \approx$ **537 Hz**
- **(3)** **$f_B < 600\text{ Hz} < f_A$**
- **(4)** **둘 다 340 m/s로 같다.** 소리의 속력은 **매질(공기)이 정하므로** 음원의 운동과 관계없다.

*채점 포인트: (1) 한 주기 동안 음원 이동만큼 파장이 짧아짐을 쓰는가, (4) '매질이 속력을 정한다'는 근거를 포함하는가.*
""")

    problem(2, B1, "기본",
            "그림은 일정한 진동수의 소리를 내며 직선 운동하는 음원에서 발생한 파면(마루)을 나타낸 것이다. X 쪽과 Y 쪽에서 이웃한 파면 사이의 거리는 각각 1.2 m, 0.8 m이다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) 음원의 운동 방향(X 쪽 / Y 쪽)을 쓰고, 판단 근거를 쓰시오.",
             "(2) 음원이 정지해 있을 때 소리의 파장을 풀이 과정과 함께 구하시오.",
             "(3) 음원이 내는 소리의 진동수를 구하시오.",
             "(4) 음원의 속력을 풀이 과정과 함께 구하시오."],
            r"""
- **(1)** **Y 쪽**. 음원이 움직이는 **앞쪽에서 파면 간격(파장)이 짧아지기** 때문이다.
- **(2)** $\lambda - v_s T = 0.8\text{ m}$, $\lambda + v_s T = 1.2\text{ m}$ → $\lambda = \dfrac{0.8 + 1.2}{2} =$ **1.0 m**
- **(3)** $f = \dfrac{v}{\lambda} = \dfrac{340}{1.0} =$ **340 Hz**
- **(4)** $v_s T = 1.0 - 0.8 = 0.2\text{ m}$이고 $T = \dfrac{1}{340}\text{ s}$이므로, $v_s = 0.2 \times 340 =$ **68 m/s**

*채점 포인트: (2) 앞뒤 파장의 평균이 정지 파장임을 식으로 보이는가.*
""")

    problem(3, B2, "보통",
            "그림 (가)는 진동수 1000 Hz의 소리를 내는 스마트폰 A가 정지한 B를 향해, (나)는 정지한 A를 향해 B가 각각 10 m/s로 운동하는 모습이다. B는 A의 소리를 측정한다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) (가), (나)에서 B가 측정하는 소리의 속력을 각각 쓰시오.",
             "(2) (가), (나)에서 B가 측정하는 소리의 파장을 각각 구하시오.",
             "(3) (가), (나)에서 B가 측정하는 진동수를 각각 구하고 크기를 비교하시오. (소수 첫째 자리에서 반올림)",
             "(4) (가)와 (나)에서 측정 진동수가 커지는 까닭이 어떻게 다른지 서술하시오."],
            r"""
- **(1)** (가) **340 m/s**, (나) $340 + 10 =$ **350 m/s**
- **(2)** (가) $\dfrac{340 - 10}{1000} =$ **0.33 m**, (나) $\dfrac{340}{1000} =$ **0.34 m**
- **(3)** (가) $1000 \times \dfrac{340}{330} \approx$ **1030 Hz**, (나) $1000 \times \dfrac{350}{340} \approx$ **1029 Hz** → **(가) > (나)**
- **(4)** **(가)는 파원이 움직여 B 쪽 파장이 짧아지기 때문**이고, **(나)는 파장은 그대로이지만 B가 측정하는 소리의 속력이 커져 1초 동안 만나는 파면의 수가 많아지기 때문**이다.

*채점 포인트: (4) '파장 변화'와 '측정 속력(만나는 파면 수) 변화'를 명확히 구분하는가.*
""")

    problem(4, B2, "보통",
            "그림과 같이 진동수 640 Hz의 경적을 울리는 자동차 A와 자전거를 탄 관찰자 B가 일직선 위에서 각각 20 m/s의 속력으로 서로를 향해 운동한다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) B가 듣는 경적의 진동수를 풀이 과정과 함께 구하시오.",
             "(2) A의 운동만 고려하여 계산한 값과 (1)을 비교하여, 한쪽의 운동만 고려하면 안 되는 까닭을 쓰시오.",
             "(3) A가 B를 지나친 뒤 같은 속력으로 서로 멀어질 때 B가 듣는 진동수를 구하시오.",
             "(4) B가 A의 앞에서 A와 같은 방향으로 20 m/s로 달릴 때 B가 듣는 진동수를 쓰고, 그 까닭을 서술하시오."],
            r"""
- **(1)** $f' = 640 \times \dfrac{340 + 20}{340 - 20} = 640 \times \dfrac{360}{320} =$ **720 Hz**
- **(2)** A의 운동만 고려하면 $640 \times \dfrac{340}{320} = 680\text{ Hz}$이다. **B도 움직여 B가 측정하는 소리의 속력이 커지므로** 두 물체의 운동을 모두 넣어야 한다.
- **(3)** $640 \times \dfrac{340 - 20}{340 + 20} = 640 \times \dfrac{320}{360} \approx$ **569 Hz**
- **(4)** **640 Hz**. 두 물체가 같은 속도로 움직여 **상대적인 운동이 없으므로** 도플러 효과가 나타나지 않는다.

*채점 포인트: (1) 분자·분모 부호를 바르게 쓰는가, (4) '상대적인 운동'을 언급하는가.*
""")

    problem(5, B3, "심화",
            "그림은 진동수 900 Hz의 소리를 내는 음원과 정지해 있는 음파 측정기 사이의 거리를 시간에 따라 나타낸 것이다. 음원은 측정기와 일직선 위에서 운동한다. (단, 소리의 속력은 340 m/s이다. 0~5 s: 200 m → 100 m, 5~10 s: 100 m 일정, 10~15 s: 100 m → 250 m)",
            ["(1) 2초일 때 측정기가 측정하는 진동수를 풀이 과정과 함께 구하시오. (소수 첫째 자리에서 반올림)",
             "(2) 7초일 때 측정하는 진동수를 쓰고, 그 까닭을 쓰시오.",
             "(3) 12초일 때 측정하는 진동수를 구하시오.",
             "(4) 측정하는 소리의 파장이 가장 긴 시간 구간을 쓰고, 그 까닭을 서술하시오."],
            r"""
- **(1)** 0~5 s 동안 거리가 100 m 줄어듦 → $v_s = \dfrac{100}{5} = 20\text{ m/s}$로 다가옴. $f' = 900 \times \dfrac{340}{340 - 20} = 900 \times \dfrac{340}{320} \approx$ **956 Hz**
- **(2)** **900 Hz**. 5~10 s 동안 거리가 일정하여 **상대적인 운동이 없기 때문**이다.
- **(3)** 10~15 s 동안 거리가 150 m 늘어남 → $v_s = \dfrac{150}{5} = 30\text{ m/s}$로 멀어짐. $f' = 900 \times \dfrac{340}{340 + 30} = 900 \times \dfrac{340}{370} \approx$ **827 Hz**
- **(4)** **10~15 s**. 음원이 측정기에서 멀어져 측정기 쪽 파장이 $\lambda' = \dfrac{v + v_s}{f}$로 길어지기 때문이다.

*채점 포인트: 거리–시간 그래프의 기울기로부터 속력과 운동 방향(가까워짐·멀어짐)을 정확히 읽는가.*
""")

    problem(6, B3, "심화",
            "정지한 음원에서 진동수 1020 Hz의 소리가 나고 있다. 음원과 일직선 위에서 일정한 속력으로 운동하는 측정기 B가 측정한 진동수는 1050 Hz였다. (단, 소리의 속력은 340 m/s이다.)",
            ["(1) B의 운동 방향(음원에 가까워짐 / 멀어짐)과 속력을 풀이 과정과 함께 구하시오.",
             "(2) B가 측정하는 소리의 속력과 파장을 각각 구하시오.",
             "(3) B가 같은 속력으로 반대 방향으로 운동할 때 측정하는 진동수를 구하시오.",
             "(4) 이번에는 B가 정지해 있고 음원이 움직여 B가 1050 Hz를 측정하게 하려면, 음원은 어느 방향으로 약 몇 m/s로 움직여야 하는지 구하고, (1)의 속력과 같은지 비교하시오."],
            r"""
- **(1)** **음원에 가까워짐**. $1050 = 1020 \times \dfrac{340 + v_o}{340}$ → $340 + v_o = 350$ → $v_o =$ **10 m/s**
- **(2)** 측정 속력 **350 m/s**, 파장 $\dfrac{340}{1020} \approx$ **0.33 m** (원래 파장 그대로)
- **(3)** $1020 \times \dfrac{340 - 10}{340} = 1020 \times \dfrac{330}{340} =$ **990 Hz**
- **(4)** **음원이 B 쪽으로** 움직여야 하며, $1050 = 1020 \times \dfrac{340}{340 - v_s}$ → $v_s \approx$ **9.7 m/s**. **(1)의 속력(10 m/s)과 다르다** (파원이 움직일 때와 관찰자가 움직일 때 관계식이 다르기 때문).

*채점 포인트: (1) 관측 진동수 증가로 가까워짐을 판단하는가, (4) 두 식의 차이를 인식하는가.*
""")

    problem(7, B3, "심화",
            "그림 (가)는 정지한 자동차가 내는 소리를, (나)는 같은 소리를 내며 일직선 위를 일정한 속력으로 운동하는 자동차의 소리를 정지한 측정기로 측정하여 공기의 압력을 시간에 따라 나타낸 것이다. (단, 소리의 속력은 340 m/s이고, (가)의 주기는 2.0 ms, (나)의 주기는 2.2 ms이다.)",
            ["(1) (가), (나)에서 측정한 소리의 주기와 진동수를 각각 구하시오.",
             "(2) (나)에서 자동차는 측정기에 가까워지는지 멀어지는지 쓰고, 판단 근거를 쓰시오.",
             "(3) 자동차의 속력을 풀이 과정과 함께 구하시오.",
             "(4) 같은 자동차가 같은 속력으로 측정기에 다가올 때 측정되는 주기를 구하시오."],
            r"""
- **(1)** (가) 주기 **2.0 ms**, 진동수 $\dfrac{1}{0.002\text{ s}} =$ **500 Hz** / (나) 주기 **2.2 ms**, 진동수 $\dfrac{1}{0.0022\text{ s}} \approx$ **455 Hz**
- **(2)** **멀어진다.** 측정된 **주기가 길어졌기(진동수가 작아졌기)** 때문이다.
- **(3)** $T' = T\dfrac{v + v_s}{v}$ → $2.2 = 2.0 \times \dfrac{340 + v_s}{340}$ → $v_s =$ **34 m/s**
- **(4)** $T' = 2.0 \times \dfrac{340 - 34}{340} =$ **1.8 ms**

*채점 포인트: 주기와 진동수가 역수($f = 1/T$) 관계임을 이용해 식을 세우는가.*
""")

    problem(8, B3, "심화",
            "그림은 점 O를 중심으로 반시계 방향으로 원운동하는 별이 A, B, C, D를 지날 때 지구에서 별빛을 관측하는 모습이다. 지구는 원 궤도에 비해 아래쪽으로 매우 멀리 있다.",
            ["(1) 별빛의 파장이 가장 짧게 관측되는 위치와 가장 길게 관측되는 위치를 쓰고, 각각의 현상 이름(청색 편이 / 적색 편이)을 쓰시오.",
             "(2) 별이 B와 D를 지날 때 관측되는 파장은 원래 파장과 비교하여 어떠한지 까닭과 함께 쓰시오.",
             "(3) 스피드건이 다가오는 야구공의 속력을 측정하는 원리를 반사된 전자기파의 진동수 변화로 서술하시오.",
             "(4) 스피드건을 야구공의 운동 방향과 수직인 방향에서 겨누면 속력을 제대로 측정하기 어려운 까닭을 (2)와 관련지어 서술하시오."],
            r"""
- **(1)** 가장 짧음: **C (청색 편이)**, 가장 김: **A (적색 편이)**
- **(2)** **원래 파장과 같다.** 별의 운동 방향이 관측(시선) 방향과 **수직**이어서 지구에 가까워지거나 멀어지지 않기 때문이다.
- **(3)** 다가오는 야구공에서 반사된 전자기파는 **진동수가 커지고**, 공이 빠를수록 **진동수 차이($\Delta f$)가 커지므로** 이 차이로 속력을 계산한다.
- **(4)** 수직 방향에서는 공이 스피드건에 가까워지거나 멀어지는 **시선 방향 운동이 거의 없어** 반사파의 진동수 변화가 생기지 않기 때문이다.

*채점 포인트: 관측자 시선 방향 성분의 상대 운동만 도플러 효과를 만든다는 점을 연결하는가.*
""")


run_sim()

