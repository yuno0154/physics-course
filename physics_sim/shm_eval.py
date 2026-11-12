import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 단진동 형성평가(8문항) — 문제 상황 시뮬레이션 + 펼침식 해설/정답
# =========================================================================

PRE = r"""
const cv=document.getElementById('cv'),c=cv.getContext('2d'),W=cv.width,H=cv.height;
let t=0,run=true,last=performance.now(),SP=1,MUL=1;
const f=(v,d)=>(v<-0.5*Math.pow(10,-d)?'−':'+')+Math.abs(v).toFixed(d);
function line(x0,y0,x1,y1,col,w,d){c.beginPath();c.setLineDash(d||[]);c.strokeStyle=col;c.lineWidth=w||1;c.moveTo(x0,y0);c.lineTo(x1,y1);c.stroke();c.setLineDash([])}
function arrow(x0,y0,x1,y1,col,w){const L=Math.hypot(x1-x0,y1-y0);if(L<4)return;line(x0,y0,x1,y1,col,w||3);const a=Math.atan2(y1-y0,x1-x0);c.beginPath();c.fillStyle=col;c.moveTo(x1,y1);c.lineTo(x1-10*Math.cos(a-.4),y1-10*Math.sin(a-.4));c.lineTo(x1-10*Math.cos(a+.4),y1-10*Math.sin(a+.4));c.fill()}
function txt(s,x,y,col,sz,al){c.font='bold '+(sz||13)+'px "Malgun Gothic",sans-serif';c.fillStyle=col||'#0f172a';c.textAlign=al||'center';c.textBaseline='middle';c.fillText(s,x,y)}
function dot(x,y,r,col){c.beginPath();c.fillStyle=col;c.arc(x,y,r,0,7);c.fill()}
function spring(x0,x1,y,n,a){c.beginPath();c.strokeStyle='#334155';c.lineWidth=2;const p=8,L=x1-x0-2*p;c.moveTo(x0,y);c.lineTo(x0+p,y);for(let i=1;i<=n;i++)c.lineTo(x0+p+L*(i-.5)/n,y+(i%2?-a:a));c.lineTo(x1-p,y);c.lineTo(x1,y);c.stroke()}
function vspring(y0,y1,x,n,a){c.beginPath();c.strokeStyle='#334155';c.lineWidth=2;const p=8,L=y1-y0-2*p;c.moveTo(x,y0);c.lineTo(x,y0+p);for(let i=1;i<=n;i++)c.lineTo(x+(i%2?-a:a),y0+p+L*(i-.5)/n);c.lineTo(x,y1-p);c.lineTo(x,y1);c.stroke()}
function box(x,y,w,h,lab){c.fillStyle='#e2e8f0';c.fillRect(x,y,w,h);c.strokeStyle='#1e293b';c.lineWidth=2;c.strokeRect(x,y,w,h);txt(lab,x+w/2,y+h/2,'#0f172a',14)}
function axes(ox,oy,w,h,xl,yl){line(ox,oy,ox+w,oy,'#0f172a',1.5);line(ox,oy-h,ox,oy+h,'#0f172a',1.5);txt(xl,ox+w-4,oy+14,'#475569',12,'right');txt(yl,ox+6,oy-h-8,'#475569',12,'left')}
const pp=document.getElementById('pp');
pp.onclick=()=>{run=!run;pp.textContent=run?'⏸ 일시정지':'▶ 재생'};
document.getElementById('spd').onchange=e=>{MUL=+e.target.value};
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{t=+b.dataset.t;run=false;pp.textContent='▶ 재생'});
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(run)t+=dt*SP*MUL;c.clearRect(0,0,W,H);draw();requestAnimationFrame(loop)}
"""

STYLE = ('<style>.b{padding:4px 9px;font-size:12px;border:1px solid #94a3b8;border-radius:5px;background:#f8fafc;cursor:pointer;margin-left:3px}'
         '.b.on{background:#dbeafe;border-color:#2563eb}</style>')
CTRL = ('<button class="b" id="pp">⏸ 일시정지</button>'
        '<select id="spd" class="b"><option value="0.5">0.5배속</option><option value="1" selected>1배속</option><option value="2">2배속</option></select>')


def sim(title, js, extra=""):
    return (STYLE + '<div style="font-family:sans-serif;border:1px solid #cbd5e1;border-radius:10px;padding:10px;max-width:680px;margin:0 auto;background:#fff">'
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:6px">'
            '<b style="font-size:13px">🎬 ' + title + '</b><span>' + extra + CTRL + '</span></div>'
            '<canvas id="cv" width="640" height="270" style="width:100%;border:1px solid #e2e8f0;border-radius:6px;background:#fafafa"></canvas></div>'
            '<script>(function(){' + PRE + js + '\nrequestAnimationFrame(loop);})();</script>')


# ---------------- 1. 수평 용수철 ----------------
JS1 = r"""
SP=0.3;const A=.2,k=100,w=10,O=250,S=500;
function draw(){const x=A*Math.cos(w*t),bx=O+x*S,F=-k*x;
 c.fillStyle='#1e293b';c.fillRect(20,110,10,70);line(20,180,620,180,'#94a3b8',2);
 spring(30,bx-30,145,12,14);box(bx-30,115,60,60,'1 kg');
 line(O,70,O,190,'#2563eb',2,[5,4]);txt('평형점 O',O,58,'#2563eb',14);
 arrow(bx,100,bx+F*2.5,100,'#dc2626',3);if(Math.abs(F)>2)txt('복원력 F',bx+F*1.25,86,'#dc2626',13);
 txt('x = '+f(x,2)+' m (오른쪽 +)',20,24,'#0f172a',14,'left');
 txt('F = −kx = '+f(F,1)+' N',20,46,'#dc2626',14,'left');
 txt('a = F/m = '+f(F/1,1)+' m/s²',250,24,'#7c3aed',14,'left');
 txt('속력 = '+(A*w*Math.abs(Math.sin(w*t))).toFixed(2)+' m/s',250,46,'#059669',14,'left');}
"""
EX1 = '<button class="b" data-t="0">놓는 순간</button><button class="b" data-t="0.157">O 통과</button>'

# ---------------- 2. 원운동 그림자 ----------------
JS2 = r"""
SP=0.5;const A=.2,w=Math.PI,cx=150,cy=135,R=90,sx=400;
function draw(){const th=w*t,px=cx+R*Math.cos(th),py=cy-R*Math.sin(th),y=A*Math.sin(th);
 for(let i=-3;i<=3;i++)arrow(15,cy+i*30,55,cy+i*30,'#f59e0b',2);txt('평행 광선',40,20,'#b45309',12);
 line(cx-R-5,cy,sx-8,cy,'#94a3b8',1,[4,4]);line(cx,cy-R-8,cx,cy+R+8,'#cbd5e1',1);
 c.beginPath();c.strokeStyle='#1e293b';c.lineWidth=2.5;c.arc(cx,cy,R,0,7);c.stroke();
 line(sx,25,sx,250,'#1e293b',5);txt('스크린',sx,12,'#0f172a',13);txt('O′',sx+22,cy,'#0f172a',14);
 line(cx,cy,px,py,'#1e293b',2);txt('A=0.2 m',cx+R/2,cy+14,'#475569',12);
 line(px,py,sx,py,'#64748b',1.5,[5,4]);dot(px,py,9,'#0f172a');txt('P',px+2,py-16,'#0f172a',14);
 c.fillStyle='#1d4ed8';c.fillRect(sx-8,py-8,16,16);txt('Q',sx+20,py-12,'#1d4ed8',14);
 txt('t = '+(t%2).toFixed(2)+' s',445,70,'#0f172a',14,'left');
 txt('변위 y = '+f(y,2)+' m',445,100,'#1d4ed8',14,'left');
 txt('속도 v = '+f(A*w*Math.cos(th),2)+' m/s',445,130,'#059669',14,'left');
 txt('가속도 a = '+f(-A*w*w*Math.sin(th),2)+' m/s²',445,160,'#dc2626',14,'left');
 txt('(위쪽 +)',445,190,'#64748b',12,'left');}
"""
EX2 = '<button class="b" data-t="0.5">t=0.5 s</button><button class="b" data-t="1">t=1 s</button>'

# ---------------- 3. x-t 그래프 ----------------
JS3 = r"""
SP=0.5;const A=.1,k=10,w=Math.PI,O=140,S=800,ox=330,oy=135,ps=65;
function draw(){const tt=t%4,x=A*Math.sin(w*tt),bx=O+x*S,F=-k*x;
 c.fillStyle='#1e293b';c.fillRect(15,100,10,70);line(15,170,300,170,'#94a3b8',2);
 spring(25,bx-25,135,10,12);box(bx-25,110,50,50,'1 kg');line(O,80,O,180,'#2563eb',2,[5,4]);txt('O',O,68,'#2563eb',14);
 arrow(bx,95,bx+F*10,95,'#dc2626',3);
 axes(ox,oy,280,100,'t (s)','x (m)');
 for(let s=.5;s<=4;s+=.5){line(ox+s*ps,oy-3,ox+s*ps,oy+3,'#0f172a',1);txt(String(s),ox+s*ps,oy+16,'#475569',10)}
 txt('0.1',ox-18,oy-80,'#475569',11);txt('−0.1',ox-22,oy+80,'#475569',11);
 line(ox,oy-80,ox+260,oy-80,'#e2e8f0',1,[3,3]);line(ox,oy+80,ox+260,oy+80,'#e2e8f0',1,[3,3]);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2.5;for(let s=0;s<=4;s+=.02){const X=ox+s*ps,Y=oy-A*Math.sin(w*s)*800;s?c.lineTo(X,Y):c.moveTo(X,Y)}c.stroke();
 dot(ox+tt*ps,oy-x*800,6,'#dc2626');
 txt('t = '+tt.toFixed(2)+' s',15,24,'#0f172a',14,'left');txt('x = '+f(x,3)+' m',15,46,'#1d4ed8',14,'left');
 txt('F = −kx = '+f(F,2)+' N',150,24,'#dc2626',14,'left');txt('a = '+f(F,2)+' m/s²',150,46,'#7c3aed',14,'left');}
"""
EX3 = '<button class="b" data-t="0.5">t=0.5 s</button><button class="b" data-t="1">t=1 s</button>'

# ---------------- 4. a-t 그래프 + 원운동 ----------------
JS4 = r"""
SP=0.5;const R=.5,w=4,cx=105,cy=150,Rp=80,sx=225,ox=290,oy=150,ps=190.99,TT=Math.PI/2;
function draw(){const tt=t%TT,th=w*tt,px=cx+Rp*Math.cos(th),py=cy-Rp*Math.sin(th),a=-8*Math.sin(th);
 c.beginPath();c.strokeStyle='#1e293b';c.lineWidth=2.5;c.arc(cx,cy,Rp,0,7);c.stroke();line(cx-Rp-5,cy,sx,cy,'#94a3b8',1,[4,4]);
 line(sx,40,sx,260,'#1e293b',5);txt('스크린',sx,28,'#0f172a',12);txt('O′',sx+20,cy,'#0f172a',13);
 line(cx,cy,px,py,'#1e293b',2);txt('R',(cx+px)/2-8,(cy+py)/2-8,'#475569',13);
 line(px,py,sx,py,'#64748b',1.5,[5,4]);dot(px,py,8,'#0f172a');txt('P',px+2,py-14,'#0f172a',13);
 c.fillStyle='#1d4ed8';c.fillRect(sx-8,py-8,16,16);txt('Q',sx+18,py-12,'#1d4ed8',13);
 arrow(sx+14,py,sx+14,py-a*5,'#dc2626',3);
 axes(ox,oy,330,110,'t (s)','a (m/s²)');
 txt('8',ox-10,oy-100,'#475569',11);txt('−8',ox-12,oy+100,'#475569',11);
 line(ox,oy-100,ox+320,oy-100,'#e2e8f0',1,[3,3]);line(ox,oy+100,ox+320,oy+100,'#e2e8f0',1,[3,3]);
 ['π/8','π/4','3π/8','π/2'].forEach((s,i)=>{const X=ox+(i+1)*Math.PI/8*ps;line(X,oy-3,X,oy+3,'#0f172a',1);txt(s,X,oy+16,'#475569',10)});
 c.beginPath();c.strokeStyle='#be123c';c.lineWidth=2.5;for(let s=0;s<=TT+.001;s+=.01){const X=ox+s*ps,Y=oy+8*Math.sin(w*s)*12.5;s?c.lineTo(X,Y):c.moveTo(X,Y)}c.stroke();
 dot(ox+tt*ps,oy-a*12.5,6,'#dc2626');
 txt('t = '+tt.toFixed(3)+' s (π/8 = 0.393 s)',15,16,'#0f172a',13,'left');
 txt('Q 위치 y = '+f(R*Math.sin(th),2)+' m',15,36,'#1d4ed8',13,'left');
 txt('속력 = '+(R*w*Math.abs(Math.cos(th))).toFixed(2)+' m/s',270,16,'#059669',13,'left');
 txt('a = '+f(a,2)+' m/s²',270,36,'#dc2626',13,'left');}
"""
EX4 = '<button class="b" data-t="0.3927">t=π/8 s</button>'

# ---------------- 5. 두 용수철 A, B ----------------
JS5 = r"""
SP=1;const A=.1,O=170,S=500,ox=335,oy=135,ps=22;
function draw(){const tt=t%12,xa=A*Math.sin(2*Math.PI*tt/4),xb=A*Math.sin(2*Math.PI*tt/6);
 [[70,xa,'m',50,'#2563eb','A'],[195,xb,'2m',64,'#059669','B']].forEach(r=>{const y=r[0],bx=O+r[1]*S,wd=r[3];
  c.fillStyle='#1e293b';c.fillRect(15,y-35,10,70);line(15,y+35,300,y+35,'#94a3b8',2);
  spring(25,bx-wd/2,y,10,12);box(bx-wd/2,y-25,wd,50,r[2]);line(O,y-45,O,y+45,'#94a3b8',1,[4,4]);txt(r[5],12,y-48,r[4],16,'left')});
 axes(ox,oy,285,100,'t (s)','x (m)');
 for(let s=2;s<=12;s+=2){line(ox+s*ps,oy-3,ox+s*ps,oy+3,'#0f172a',1);txt(String(s),ox+s*ps,oy+16,'#475569',10)}
 txt('0.1',ox-18,oy-50,'#475569',11);txt('−0.1',ox-22,oy+50,'#475569',11);
 c.beginPath();c.strokeStyle='#2563eb';c.lineWidth=2.5;for(let s=0;s<=12;s+=.05){const X=ox+s*ps,Y=oy-A*Math.sin(2*Math.PI*s/4)*500;s?c.lineTo(X,Y):c.moveTo(X,Y)}c.stroke();
 c.beginPath();c.strokeStyle='#059669';c.lineWidth=2.5;c.setLineDash([6,4]);for(let s=0;s<=12;s+=.05){const X=ox+s*ps,Y=oy-A*Math.sin(2*Math.PI*s/6)*500;s?c.lineTo(X,Y):c.moveTo(X,Y)}c.stroke();c.setLineDash([]);
 dot(ox+tt*ps,oy-xa*500,6,'#2563eb');dot(ox+tt*ps,oy-xb*500,6,'#059669');
 line(ox+tt*ps,oy-70,ox+tt*ps,oy+70,'#cbd5e1',1,[3,3]);
 txt('t = '+tt.toFixed(1)+' s',15,16,'#0f172a',13,'left');txt('T_A = 4 s (실선)',ox+10,252,'#2563eb',12,'left');txt('T_B = 6 s (점선)',ox+150,252,'#059669',12,'left');}
"""

# ---------------- 6. 수직 용수철 (지구/달) ----------------
JS6 = r"""
SP=0.3;let g=10;const m=2,k=200,A=.05,w=10,nat=85,S=800,cx=85;
function draw(){const y=A*Math.cos(w*t),x0=m*g/k,ye=nat+(x0+y)*S,eq=nat+x0*S;
 c.fillStyle='#1e293b';c.fillRect(35,10,100,8);
 line(cx-45,nat,cx+60,nat,'#94a3b8',1.5,[4,3]);txt('원래 길이',cx+62,nat-8,'#64748b',11,'left');
 line(cx-45,eq,cx+60,eq,'#2563eb',1.5,[6,4]);txt('평형점 O',cx+62,eq+10,'#2563eb',12,'left');
 vspring(18,ye,cx,14,13);box(cx-30,ye,60,38,'2 kg');
 const my=ye+19,Fs=k*(x0+y),Fg=m*g,Fn=Fs-Fg;
 arrow(cx+45,my,cx+45,my-Fs*3,'#ea580c',3);arrow(cx+62,my,cx+62,my+Fg*3,'#475569',3);arrow(cx+79,my,cx+79,my-Fn*3,'#9333ea',3);
 txt('탄성력',cx+45,my-Fs*3-10,'#ea580c',11);txt('중력',cx+66,my+Fg*3+10,'#475569',11);txt('알짜힘',cx+85,my-Fn*3-10,'#9333ea',11);
 txt('중력가속도 g = '+(g>9?'10 (지구)':'10/6 (달)')+' m/s²',255,30,'#0f172a',14,'left');
 txt('평형점의 늘어난 길이 mg/k = '+x0.toFixed(3)+' m',255,58,'#2563eb',14,'left');
 txt('아래로 변위 y = '+f(y,3)+' m',255,92,'#0f172a',14,'left');
 txt('탄성력 k(x₀+y) = '+Fs.toFixed(1)+' N (위쪽)',255,122,'#ea580c',14,'left');
 txt('중력 mg = '+Fg.toFixed(1)+' N (아래쪽)',255,148,'#475569',14,'left');
 txt('알짜힘 = '+Math.abs(Fn).toFixed(1)+' N ('+(Fn>0.05?'위쪽':(Fn<-0.05?'아래쪽':'0'))+') = k|y|',255,174,'#9333ea',14,'left');
 txt('주기 T = 2π√(m/k) = 0.2π s ≈ 0.63 s (g에 무관)',255,210,'#059669',14,'left');}
document.getElementById('moon').onclick=()=>{g=10/6};document.getElementById('earth').onclick=()=>{g=10};
"""
EX6 = '<button class="b" id="earth">지구</button><button class="b" id="moon">달(g/6)</button><button class="b" data-t="0">놓는 순간</button>'

# ---------------- 7. 원운동 사영 R/2 ----------------
JS7 = r"""
SP=0.5;const w=2,cx=170,cy=140,R=100,sx=470;
function draw(){const th=w*t,px=cx+R*Math.cos(th),py=cy-R*Math.sin(th),s=Math.sin(th),co=Math.cos(th);
 for(let i=-3;i<=3;i++)arrow(15,cy+i*34,55,cy+i*34,'#f59e0b',2);
 c.beginPath();c.strokeStyle='#1e293b';c.lineWidth=2.5;c.arc(cx,cy,R,0,7);c.stroke();
 line(cx-R-5,cy,sx-8,cy,'#94a3b8',1,[4,4]);line(cx,cy-R-8,cx,cy+R+8,'#cbd5e1',1);
 dot(cx+R,cy,6,'#94a3b8');txt('P₀',cx+R+16,cy+12,'#64748b',12);
 line(sx,20,sx,260,'#1e293b',5);txt('스크린',sx,10,'#0f172a',12);
 [[cy-R,'R'],[cy-R/2,'R/2'],[cy,'O′']].forEach(q=>{line(sx-10,q[0],sx+10,q[0],'#0f172a',2);txt(q[1],sx+26,q[0],'#0f172a',12)});
 line(cx,cy,px,py,'#1e293b',2);line(px,py,sx,py,'#64748b',1.5,[5,4]);dot(px,py,9,'#0f172a');txt("P",px+8,py-14,'#0f172a',14);
 c.fillStyle='#1d4ed8';c.fillRect(sx-8,py-8,16,16);
 arrow(px,py,px-60*s,py-60*co,'#2563eb',3);arrow(px,py,px,py-60*co,'#059669',3);
 arrow(sx-18,py,sx-18,py+50*s,'#dc2626',3);
 txt('P의 속도(접선)',20,252,'#2563eb',12,'left');txt('세로 성분 = Q의 속도',140,252,'#059669',12,'left');txt('Q의 가속도',290,252,'#dc2626',12,'left');
 txt('θ = ωt = '+((th*180/Math.PI)%360).toFixed(0)+'°',20,18,'#b45309',14,'left');
 txt('Q의 변위 = '+f(s,2)+' R',20,40,'#1d4ed8',13,'left');
 txt('Q의 속력 = '+Math.abs(co).toFixed(2)+' v최대',20,62,'#059669',13,'left');
 txt('Q의 가속도 크기 = '+Math.abs(s).toFixed(2)+' a최대',20,84,'#dc2626',13,'left');}
"""
EX7 = '<button class="b" data-t="0.2618">Q가 R/2에 도달 (θ=30°)</button>'

# ---------------- 8. a-x 그래프 ----------------
JS8 = r"""
SP=0.3;let M=0.5;const k=50,A=.1,O=165,S=500,ox=490,oy=140;
function draw(){const w=Math.sqrt(k/M),x=A*Math.cos(w*t),a=-k/M*x,bx=O+x*S;
 c.fillStyle='#1e293b';c.fillRect(15,100,10,70);line(15,170,320,170,'#94a3b8',2);
 spring(25,bx-28,135,10,13);box(bx-28,108,56,54,M+' kg');line(O,80,O,180,'#2563eb',2,[5,4]);txt('O',O,68,'#2563eb',14);
 axes(ox,oy,120,110,'x (m)','a (m/s²)');
 txt('0.1',ox+100,oy+14,'#475569',11);txt('−0.1',ox-100,oy+14,'#475569',11);txt('10',ox-12,oy-80,'#475569',11);txt('−10',ox-14,oy+80,'#475569',11);
 line(ox-100,oy,ox+100,oy,'#0f172a',1.5);
 if(M>1){line(ox-100,oy-80,ox+100,oy+80,'#cbd5e1',2,[5,4])}
 const sl=k/M;line(ox-100,oy-sl*.1*8,ox+100,oy+sl*.1*8,'#be123c',3);
 dot(ox+x*1000,oy-a*8,6,'#dc2626');
 txt('질량 m = '+M+' kg',15,18,'#0f172a',14,'left');txt('ω = √(k/m) = '+w.toFixed(1)+' rad/s',15,40,'#059669',13,'left');
 txt('기울기 = −ω² = '+(-sl).toFixed(0)+' s⁻²',15,62,'#be123c',13,'left');txt('주기 T = 2π/ω = '+(2*Math.PI/w/Math.PI).toFixed(2)+'π s',15,84,'#7c3aed',13,'left');
 txt('x = '+f(x,3)+' m',200,18,'#1d4ed8',13,'left');txt('a = '+f(a,2)+' m/s²',200,40,'#dc2626',13,'left');}
document.getElementById('m1').onclick=()=>{M=0.5;t=0};document.getElementById('m2').onclick=()=>{M=2;t=0};
"""
EX8 = '<button class="b" id="m1">0.5 kg</button><button class="b" id="m2">2 kg (비교)</button>'


SIMS = {
    1: ("수평 용수철 진자: 놓는 순간과 평형점 통과", JS1, EX1),
    2: ("등속 원운동 P와 그림자 Q의 단진동", JS2, EX2),
    3: ("용수철 진자의 변위–시간(x–t) 그래프 연동", JS3, EX3),
    4: ("그림자 Q의 가속도–시간(a–t) 그래프 연동", JS4, EX4),
    5: ("두 용수철 진자 A, B의 주기 비교", JS5, ""),
    6: ("수직 용수철 진자: 힘의 합과 지구·달 비교", JS6, EX6),
    7: ("Q가 R/2에 도달한 순간의 속도·가속도", JS7, EX7),
    8: ("a–x 그래프와 질량 변화 비교", JS8, EX8),
}

# ===== RENDER =====


def sim_html(n):
    title, js, extra = SIMS[n]
    return sim(title, js, extra)


def problem(n, badge, level, text, subs, answer_md):
    st.markdown(
        f'<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:14px 18px;margin-bottom:8px">'
        f'<span style="background:{badge};padding:3px 9px;border-radius:6px;font-weight:bold;font-size:.8rem">문제 {n} · {level}</span>'
        f'<p style="margin:8px 0 4px">{text}</p>'
        + "".join(f'<div style="font-size:.93rem;margin-left:4px">{s}</div>' for s in subs) + '</div>',
        unsafe_allow_html=True)
    components.html(sim_html(n), height=360)
    with st.expander(f"💡 문제 {n} 해설 및 정답 펼치기", expanded=False):
        st.markdown(answer_md)
    st.divider()


def run_sim():
    st.title("📝 단진동 형성평가 문제 풀이")
    st.caption("[12역학03-01] 용수철 진자를 통해 단진동을 이해하고, 가속도와 변위 사이의 관계를 설명할 수 있다.")
    st.markdown("각 문항의 문제 상황을 시뮬레이션으로 확인하고, 직접 풀어 본 뒤 **해설 및 정답을 펼쳐** 확인하세요. (π² = 10, 별도 언급 없으면 용수철 질량 무시)")
    st.markdown("---")

    B1, B2, B3 = "#eff6ff", "#ecfdf5", "#faf5ff"

    problem(1, B1, "기본",
            "마찰이 없는 수평면에서 용수철 상수가 100 N/m인 용수철에 연결된 질량 1 kg인 물체를 평형점 O에서 오른쪽으로 0.2 m 잡아당겼다가 가만히 놓았더니 물체가 단진동하였다.",
            ["(1) 물체를 놓는 순간 용수철이 물체에 작용하는 힘의 크기와 방향을 풀이 과정과 함께 쓰시오.",
             "(2) 이때 물체의 가속도의 크기와 방향을 쓰시오.",
             "(3) 물체가 O를 지나는 순간 물체에 작용하는 알짜힘의 크기와 물체의 속력(최대 / 최소)을 쓰시오.",
             "(4) 단진동의 주기를 풀이 과정과 함께 구하시오. (π를 포함한 식)"],
            r"""
- **(1)** $F=-kx=-100\times0.2=-20\,\text{N}$ → 크기 **20 N**, 방향 **왼쪽(평형점 O 방향)**
- **(2)** $a=F/m=20/1=$ **20 m/s², 왼쪽**
- **(3)** 알짜힘 **0**, 속력 **최대**
- **(4)** $T=2\pi\sqrt{m/k}=2\pi\sqrt{1/100}=$ **0.2π s** (≈ 0.63 s)

*채점 포인트: 힘의 방향을 변위와 반대(평형점 쪽)로 쓰는가, F = −kx와 단위를 쓰는가.*
""")

    problem(2, B2, "기본",
            "반지름 0.2 m인 원을 각속도 π rad/s로 등속 원운동하는 물체 P에 평행 광선을 비추어 스크린에 그림자 Q를 만들었다. t = 0일 때 P는 기준선 위에 있고 Q는 O′에 있다. Q는 단진동한다.",
            ["(1) Q의 진폭과 단진동의 주기를 구하시오.",
             "(2) t = 0.5 s일 때 Q의 변위를 풀이 과정과 함께 구하시오.",
             "(3) Q의 속력이 최대인 위치와 그때의 속력을 구하시오. (π를 포함한 식)",
             "(4) Q의 가속도의 크기가 최대인 위치와 그때의 가속도의 크기를 구하시오. (π를 포함한 식)"],
            r"""
- **(1)** 진폭 **0.2 m**, 주기 $T=2\pi/\omega=$ **2 s**
- **(2)** $x=A\sin\omega t=0.2\sin(\pi\times0.5)=$ **0.2 m** (O′보다 위쪽)
- **(3)** **O′($x=0$)**, $v_{max}=A\omega=$ **0.2π m/s**
- **(4)** **양 끝점($x=\pm0.2$ m)**, $a_{max}=A\omega^2=$ **0.2π² m/s²**

*핵심: 그림자의 변위·속도·가속도는 원운동의 세로 성분이다.*
""")

    problem(3, B3, "중간",
            "질량 1 kg인 물체가 용수철에 매달려 수평면에서 단진동할 때, 물체의 변위 x를 시간 t에 따라 나타낸 것이다. (단, 마찰과 용수철의 질량은 무시하고 π² = 10으로 계산한다.)",
            ["(1) 진폭, 주기, 진동수를 각각 구하시오.",
             "(2) 용수철 상수 k를 풀이 과정과 함께 구하시오.",
             "(3) t = 0.5 s일 때 물체에 작용하는 힘의 크기와 방향을 쓰고, 방향을 그렇게 판단한 까닭을 서술하시오.",
             "(4) 0 s ~ 4 s 동안 물체의 가속도가 0인 시각을 모두 쓰고, 그 까닭을 변위와 가속도의 관계로 설명하시오."],
            r"""
- **(1)** 진폭 **0.1 m**, 주기 **2 s**, 진동수 $f=1/T=$ **0.5 Hz**
- **(2)** $\omega=2\pi/T=\pi\,\text{rad/s}$, $k=m\omega^2=1\times\pi^2=$ **10 N/m**
- **(3)** 0.5 s에서 $x=+0.1$ m이므로 $F=-kx=-1$ N → 크기 **1 N**, **−x 방향**. 복원력은 항상 변위와 반대 방향(평형점 쪽)이기 때문이다.
- **(4)** $a=-\omega^2x$ 이므로 $x=0$일 때 $a=0$ → **0, 1, 2, 3, 4 s**
""")

    problem(4, B1, "중간",
            "(가)는 반지름 R인 원을 각속도 ω로 등속 원운동하는 물체 P의 그림자 Q가 스크린에서 단진동하는 모습을, (나)는 Q의 가속도 a를 시간 t에 따라 나타낸 것이다. t = 0일 때 Q는 O′를 지난다. (그래프: 가속도 최댓값 8 m/s², 한 주기가 π/2 s)",
            ["(1) Q의 단진동 주기와 ω의 크기를 구하시오.",
             "(2) 원의 반지름 R를 풀이 과정과 함께 구하시오.",
             "(3) Q의 최대 속력을 구하시오.",
             "(4) t = π/8 s일 때 Q의 위치(O′ 기준)와 속력을 쓰고, 가속도의 방향과 크기를 근거로 설명하시오."],
            r"""
- **(1)** $T=\pi/2$ s, $\omega=2\pi/T=$ **4 rad/s**
- **(2)** 최대 가속도 $8=R\omega^2=16R$ → $R=$ **0.5 m**
- **(3)** $v_{max}=R\omega=0.5\times4=$ **2 m/s**
- **(4)** $t=\pi/8$ s에서 $a=-8$ m/s² (크기 최대). $a=-\omega^2x$ 이므로 $x=+R=$ **0.5 m (O′ 위쪽 끝)**, 이때 속력은 **0**.

*핵심: 가속도 크기 최대 = 변위 크기 최대 = 속력 0.*
""")

    problem(5, B2, "상위",
            "(가)는 마찰이 없는 수평면에서 용수철 상수가 각각 k_A, k_B인 용수철에 연결된 질량 m, 2m인 물체 A, B를, (나)는 A, B의 변위를 시간에 따라 나타낸 것이다. 두 물체의 진폭은 같다.",
            ["(1) A, B의 주기 T_A, T_B를 그래프에서 읽어 쓰시오.",
             "(2) k_B / k_A를 풀이 과정과 함께 구하시오.",
             "(3) 최대 속력의 비 v_B / v_A를 구하고, 진폭이 같을 때 최대 속력이 무엇에 의해 정해지는지 서술하시오.",
             "(4) 변위가 최대일 때 가속도의 크기의 비 a_B / a_A를 풀이 과정과 함께 구하시오."],
            r"""
- **(1)** $T_A=$ **4 s**, $T_B=$ **6 s**
- **(2)** $k=4\pi^2m/T^2$ → $\dfrac{k_B}{k_A}=\dfrac{2m}{m}\times\left(\dfrac{T_A}{T_B}\right)^2=2\times\left(\dfrac46\right)^2=\dfrac{\mathbf{8}}{\mathbf{9}}$
- **(3)** $v_{max}=A\omega$, 진폭이 같으므로 $v\propto\omega\propto1/T$ → $v_B/v_A=4/6=$ **2/3**. 진폭이 같을 때 최대 속력은 **각속도 ω(= 2π/주기)** 에 의해 정해진다.
- **(4)** $a_{max}=A\omega^2\propto1/T^2$ → $a_B/a_A=(4/6)^2=$ **4/9**
  (또는 $a=kA/m$ → $\dfrac{k_B/2m}{k_A/m}=\dfrac49$)
""")

    problem(6, B3, "상위",
            "(가) 용수철에 질량 2 kg인 물체를 매달아 천천히 놓았더니 용수철이 0.1 m 늘어난 상태로 정지하였다. (나) 물체를 평형점에서 0.05 m 더 아래로 잡아당겼다가 가만히 놓는 순간이다. 놓은 뒤 물체는 단진동한다. (중력 가속도 10 m/s²)",
            ["(1) 용수철 상수 k를 풀이 과정과 함께 구하시오.",
             "(2) (나)에서 놓는 순간 물체에 작용하는 탄성력과 중력의 크기를 각각 구하고, 알짜힘의 크기와 방향을 쓰시오.",
             "(3) 단진동의 주기를 구하시오. (π를 포함한 식)",
             "(4) 같은 장치를 중력 가속도가 지구의 1/6인 달에서 같은 방법으로 진동시킨다면 주기와 평형점의 위치는 지구에서와 비교하여 어떻게 되는지, 까닭과 함께 서술하시오."],
            r"""
- **(1)** 정지: $mg=kx_0$ → $k=\dfrac{2\times10}{0.1}=$ **200 N/m**
- **(2)** 탄성력 $k(0.1+0.05)=$ **30 N**(위쪽), 중력 **20 N**(아래쪽) → 알짜힘 **10 N, 위쪽** (= $kA=200\times0.05$)
- **(3)** $T=2\pi\sqrt{m/k}=2\pi\sqrt{2/200}=$ **0.2π s**
- **(4)** **주기는 같다** ($T=2\pi\sqrt{m/k}$에 $g$가 없다). 평형점에서 늘어난 길이 $mg/k$는 **1/6로 줄어(약 0.017 m)** 평형점이 **위로 올라간다**.

*핵심: 평형점 기준 알짜힘은 −kx이고, 중력은 평형점의 위치만 옮긴다.*
""")

    problem(7, B1, "상위",
            "반지름 R인 원을 각속도 ω로 등속 원운동(반시계 방향)하는 물체 P에 평행 광선을 비추어 스크린에 생긴 그림자 Q가 O′를 중심으로 단진동한다. t = 0일 때 P는 P₀에 있고, Q가 O′에서 출발하여 처음으로 R/2 지점에 도달한 순간 P는 P′, Q는 Q′에 있다.",
            ["(1) Q가 O′에서 R/2 지점까지 처음 도달하는 데 걸리는 시간을 주기 T로 나타내시오. (풀이 과정 포함)",
             "(2) 그림에 P′의 속도를 화살표로 그리고 그 세로 성분을 표시하시오. 이를 이용하여 이 순간 Q의 속력은 최대 속력의 몇 배인지 구하시오.",
             "(3) 이 순간 Q의 가속도의 크기는 최대 가속도의 몇 배인지 구하시오.",
             "(4) 이 순간 Q의 속도와 가속도의 방향을 각각 쓰고, 속력이 증가하는지 감소하는지 까닭과 함께 서술하시오."],
            r"""
- **(1)** $x=R\sin\omega t=R/2$ → $\omega t=\pi/6$ (30°) → $t=\dfrac{T}{12}$
- **(2)** P′의 속도는 접선 방향이고 크기는 $R\omega$. 세로 성분 $=R\omega\cos30^\circ$ → $v=\dfrac{\sqrt3}{2}R\omega$ → 최대 속력의 **√3/2배**
- **(3)** $a=\omega^2x=\omega^2R/2$ → 최대 가속도의 **1/2배**
- **(4)** 속도: **위쪽(+)**, 가속도: **아래쪽(O′ 방향)**. 속도와 가속도의 방향이 반대이므로 **속력은 감소**한다.
""")

    problem(8, B3, "상위",
            "(가) 마찰이 없는 수평면에서 용수철에 연결된 질량 0.5 kg인 물체를 평형점 O에서 0.1 m 당겼다가 놓아 단진동시킨다. (나)는 이 물체의 가속도 a를 변위 x에 따라 나타낸 것이다. ((나): 점 (−0.1, 10), (0.1, −10)을 지나는 직선)",
            ["(1) (나)의 기울기를 구하고, 이를 이용하여 ω와 단진동의 주기를 구하시오. (π를 포함한 식)",
             "(2) 용수철 상수 k를 풀이 과정과 함께 구하시오.",
             "(3) x = 0.05 m일 때 물체의 가속도의 크기와 방향을 구하시오.",
             "(4) 같은 용수철에 질량 2 kg인 물체를 달아 똑같이 0.1 m 당겼다가 놓을 때의 a–x 그래프를 (나)에 그리고, 기울기의 크기와 주기가 처음의 몇 배가 되는지 근거와 함께 서술하시오."],
            r"""
- **(1)** 기울기 $=-10/0.1=-100\,\text{s}^{-2}=-\omega^2$ → $\omega=$ **10 rad/s**, $T=2\pi/\omega=$ **0.2π s**
- **(2)** $k=m\omega^2=0.5\times100=$ **50 N/m**
- **(3)** $a=-\omega^2x=-100\times0.05=-5\,\text{m/s}^2$ → 크기 **5 m/s²**, **−x(평형점) 방향**
- **(4)** 기울기 $=-k/m=-50/2=-25\,\text{s}^{-2}$ → 처음의 **1/4배** (직선은 (±0.1, ∓2.5)를 지남). $T=2\pi\sqrt{m/k}$이므로 질량이 4배 → 주기는 **2배**

*시뮬레이션의 「2 kg (비교)」 버튼으로 기울기 변화를 확인해 보세요.*
""")


run_sim()

