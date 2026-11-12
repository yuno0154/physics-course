import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# 탄성파 형성평가(8문항) — 문제 상황 시뮬레이션 + 펼침식 해설/정답
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
function box(x,y,w,h,lab){c.fillStyle='#e2e8f0';c.fillRect(x,y,w,h);c.strokeStyle='#1e293b';c.lineWidth=2;c.strokeRect(x,y,w,h);txt(lab,x+w/2,y+h/2,'#0f172a',14)}
const pp=document.getElementById('pp');
pp.onclick=()=>{run=!run;pp.textContent=run?'⏸ 일시정지':'▶ 재생'};
document.getElementById('spd').onchange=e=>{MUL=+e.target.value};
document.querySelectorAll('[data-t]').forEach(b=>b.onclick=()=>{t=+b.dataset.t;run=false;pp.textContent='▶ 재생'});
function loop(now){const dt=Math.min(.05,(now-last)/1000);last=now;if(run)t+=dt*SP*MUL;c.clearRect(0,0,W,H);draw();requestAnimationFrame(loop)}
"""

STYLE = ('<style>.b{padding:4px 9px;font-size:12px;border:1px solid #94a3b8;border-radius:5px;background:#f8fafc;cursor:pointer;margin-left:3px}</style>')
CTRL = ('<button class="b" id="pp">⏸ 일시정지</button>'
        '<select id="spd" class="b"><option value="0.5">0.5배속</option><option value="1" selected>1배속</option><option value="2">2배속</option></select>')


def sim(title, js, extra=""):
    return (STYLE + '<div style="font-family:sans-serif;border:1px solid #cbd5e1;border-radius:10px;padding:10px;max-width:680px;margin:0 auto;background:#fff">'
            '<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:6px;margin-bottom:6px">'
            '<b style="font-size:13px">🎬 ' + title + '</b><span>' + extra + CTRL + '</span></div>'
            '<canvas id="cv" width="640" height="270" style="width:100%;border:1px solid #e2e8f0;border-radius:6px;background:#fafafa"></canvas></div>'
            '<script>' + PRE + js + '\nrequestAnimationFrame(loop);</script>')


# ---------------- 1. 횡파와 종파 ----------------
JS1 = r"""
SP=1;const lam=160,k=2*Math.PI/lam,w=2*Math.PI*.4,X0=40,X1=620;
function draw(){
 txt('(가) 줄 — 횡파: 입자(●)는 위아래로 진동, 파동은 오른쪽으로 진행',X0,14,'#0f172a',13,'left');
 const by=70;line(X0,by,X1,by,'#e2e8f0',1);
 c.beginPath();c.strokeStyle='#93c5fd';c.lineWidth=2;for(let x=X0;x<=X1;x+=3){const y=by-30*Math.sin(k*(x-X0)-w*t);x==X0?c.moveTo(x,y):c.lineTo(x,y)}c.stroke();
 for(let x=X0;x<=X1;x+=20){const y=by-30*Math.sin(k*(x-X0)-w*t);dot(x,y,x==300?7:3.5,x==300?'#e11d48':'#2563eb')}
 line(300,by-42,300,by+42,'#e11d48',1,[3,3]);arrow(470,by+48,600,by+48,'#2563eb',2);txt('진행 방향',535,by+62,'#2563eb',12);
 txt('(나) 용수철 — 종파: 입자는 좌우로 진동, 밀한 곳(밀)이 오른쪽으로 이동',X0,150,'#0f172a',13,'left');
 const cy=205;
 for(let x0=X0;x0<=X1;x0+=6){const u=12*Math.sin(k*(x0-X0)-w*t),hl=(x0==304);line(x0+u,cy-(hl?32:24),x0+u,cy+(hl?32:24),hl?'#e11d48':'#334155',hl?4:1.6)}
 const cm=[];for(let n=-6;n<=6;n++){const x0=X0+(Math.PI+w*t)/k+n*lam;if(x0>X0+10&&x0<X1-10)cm.push(x0)}
 cm.forEach((x,i)=>txt(i==0?'A':(i==1?'B':'밀'),x,cy-44,'#e11d48',14));
 if(cm.length>=2){dbl(cm[0],cy+48,cm[1],cy+48,'#059669');txt('A–B 사이 거리 = 0.6 m (= 파장)',(cm[0]+cm[1])/2,cy+62,'#059669',12)}
}
"""

# ---------------- 2. 변위-위치 그래프 ----------------
JS2 = r"""
SP=.05;let fr=5;const A=.2,ox=60,oy=125,sc=120;
function draw(){const lam=10/fr,k=2*Math.PI/lam,w=2*Math.PI*fr;
 axes(ox,oy,540,75,'위치 (m)','변위 (m)');
 for(let m=1;m<=4;m++){line(ox+m*sc,oy-3,ox+m*sc,oy+3,'#0f172a',1);txt(String(m),ox+m*sc,oy+16,'#475569',11)}
 txt('0.2',ox-18,oy-50,'#475569',11);txt('−0.2',ox-22,oy+50,'#475569',11);
 line(ox,oy-50,ox+520,oy-50,'#e2e8f0',1,[3,3]);line(ox,oy+50,ox+520,oy+50,'#e2e8f0',1,[3,3]);
 c.beginPath();c.strokeStyle='#be123c';c.lineWidth=3;for(let X=0;X<=4.4;X+=.02){const px=ox+X*sc,py=oy-50*Math.sin(k*X-w*t);X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 const cr=[];for(let n=-6;n<=10;n++){const x=(Math.PI/2+w*t)/k+n*lam;if(x>=0&&x<=4.4)cr.push(x)}
 if(cr.length>=2){const a=ox+cr[0]*sc,b=ox+cr[1]*sc;dbl(a,oy-70,b,oy-70,'#059669');txt('파장 λ = '+lam+' m',(a+b)/2,oy-84,'#059669',13);line(a,oy-66,a,oy-52,'#059669',1,[2,3]);line(b,oy-66,b,oy-52,'#059669',1,[2,3])}
 arrow(430,22,570,22,'#be123c',2);txt('진행 방향',500,10,'#be123c',12);
 txt('진동수 f = '+fr+' Hz  →  주기 T = 1/f = '+(1/fr).toFixed(2)+' s',30,225,'#0f172a',14,'left');
 txt('파장 λ = '+lam+' m   속력 v = fλ = '+(fr*lam)+' m/s'+(fr==10?'  (같은 줄 → 속력 그대로)':''),30,248,'#1d4ed8',14,'left');}
document.getElementById('f5').onclick=()=>{fr=5};document.getElementById('f10').onclick=()=>{fr=10};
"""
EX2 = '<button class="b" id="f5">f = 5 Hz</button><button class="b" id="f10">f = 10 Hz</button>'

# ---------------- 3. 왼쪽 진행 파동 P, Q ----------------
JS3 = r"""
SP=.5;const ox=45,oy=75,sc=48,gx=45,gy=195,ps=450;
const Y=(x,s)=>2*Math.sin(2*Math.PI*x/8+2*Math.PI*s/.4);
function draw(){const tt=t%1;
 axes(ox,oy,520,48,'위치 (m)','변위 (cm)');
 for(let m=2;m<=10;m+=2){line(ox+m*sc,oy-3,ox+m*sc,oy+3,'#0f172a',1);txt(String(m),ox+m*sc,oy+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#be123c';c.lineWidth=3;for(let X=0;X<=10.4;X+=.05){const px=ox+X*sc,py=oy-Y(X,tt)*22;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 [[4,'P'],[8,'Q']].forEach(q=>{const px=ox+q[0]*sc,py=oy-Y(q[0],tt)*22;dot(px,py,7,'#0f172a');txt(q[1],px+14,py-12,'#0f172a',15)});
 arrow(470,18,350,18,'#be123c',2);txt('진행 방향',410,30,'#be123c',12);
 txt('(가) 파동 모습 (t = '+tt.toFixed(2)+' s)',ox+10,16,'#0f172a',12,'left');
 axes(gx,gy,520,48,'시간 (s)','(나) P, Q 중 한 점의 변위 (cm)');
 for(let s=.2;s<=1.001;s+=.2){line(gx+s*ps,gy-3,gx+s*ps,gy+3,'#0f172a',1);txt(s.toFixed(1),gx+s*ps,gy+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=2.5;for(let s=0;s<=1.001;s+=.005){const px=gx+s*ps,py=gy-(-2*Math.sin(2*Math.PI*s/.4))*22;s?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 dot(gx+tt*ps,gy+2*Math.sin(2*Math.PI*tt/.4)*22,6,'#7c3aed');
 txt('P의 변위 = '+f(Y(4,tt),2)+' cm   Q의 변위 = '+f(Y(8,tt),2)+' cm   차 = '+Math.abs(Y(4,tt)-Y(8,tt)).toFixed(2)+' cm',30,258,'#0f172a',13,'left');}
"""
EX3 = '<button class="b" data-t="0">t=0</button><button class="b" data-t="0.1">t=0.1 s</button>'

# ---------------- 4. 매질 A→B ----------------
JS4 = r"""
SP=.05;let fr=10;const ox=20,sc=46,oy=130,xb=8;
function draw(){const lA=40/fr,lB=20/fr,ph=2*Math.PI*fr*t;
 c.fillStyle='#e0f2fe';c.fillRect(ox,40,xb*sc,190);c.fillStyle='#f1f5f9';c.fillRect(ox+xb*sc,40,5*sc+20,190);
 line(ox+xb*sc,40,ox+xb*sc,230,'#0f172a',2,[6,4]);txt('경계면',ox+xb*sc,30,'#0f172a',13);txt('매질 A',ox+4*sc,246,'#0369a1',14);txt('매질 B',ox+10.5*sc,246,'#475569',14);
 line(ox,oy,ox+13*sc,oy,'#0f172a',1.5);txt('위치 (cm)',ox+13*sc,oy+16,'#475569',11,'right');
 for(let m=2;m<=12;m+=2){line(ox+m*sc,oy-3,ox+m*sc,oy+3,'#0f172a',1);txt(String(m),ox+m*sc,oy+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#be123c';c.lineWidth=3;for(let X=0;X<=13;X+=.03){const y=X<xb?Math.sin(2*Math.PI*X/lA-ph):Math.sin(2*Math.PI*(X-xb)/lB-ph);const px=ox+X*sc,py=oy-y*50;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 arrow(30,22,150,22,'#1d4ed8',2);txt('진행 방향',90,12,'#1d4ed8',12);
 txt('진동수 f = '+fr+' Hz (A, B 모두 같음)',380,12,'#0f172a',13,'left');
 txt('A: 파장 '+lA+' cm, 속력 '+(fr*lA)+' cm/s',20,262,'#0369a1',13,'left');txt('B: 파장 '+lB+' cm, 속력 '+(fr*lB)+' cm/s',360,262,'#475569',13,'left');}
document.getElementById('f10').onclick=()=>{fr=10};document.getElementById('f20').onclick=()=>{fr=20};
"""
EX4 = '<button class="b" id="f10">f = 10 Hz</button><button class="b" id="f20">f = 20 Hz</button>'

# ---------------- 5. 고정단/자유단 ----------------
JS5 = r"""
SP=1;let free=false;const ox=40,sc=45,by=125,H0=1.5;
const tri=u=>{u=Math.abs(u-8);return u<1?H0*(1-u):0};
const Y=(x,s)=>tri(x-s)+(free?1:-1)*tri(24-x-s);
function draw(){const s=t%12;
 for(let i=0;i<=12;i++)line(ox+i*sc,by-90,ox+i*sc,by+90,'#e2e8f0',1);for(let j=-2;j<=2;j++)line(ox,by+j*45,ox+12*sc,by+j*45,'#e2e8f0',1);
 line(ox,by,ox+12*sc,by,'#64748b',1.5);
 c.beginPath();c.strokeStyle='#1d4ed8';c.lineWidth=3.5;for(let X=0;X<=12.001;X+=.05){const px=ox+X*sc,py=by-Y(X,s)*sc;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 const wx=ox+12*sc;
 if(!free){line(wx,by-100,wx,by+100,'#0f172a',6);for(let y=by-100;y<by+100;y+=16)line(wx,y,wx+14,y-12,'#0f172a',1.5)}
 else{line(wx,by-100,wx,by+100,'#0f172a',2);c.beginPath();c.fillStyle='#fff';c.strokeStyle='#0f172a';c.lineWidth=2;c.arc(wx,by-Y(12,s)*sc,8,0,7);c.fill();c.stroke()}
 arrow(300,22,420,22,'#1d4ed8',2);txt('1 cm/s',360,10,'#1d4ed8',12);
 txt((free?'(나) 자유단':'(가) 고정단')+' — t = '+s.toFixed(1)+' s (모눈 한 칸 = 1 cm)',ox,16,'#0f172a',14,'left');
 const m=s<3?'① 펄스가 오른쪽 끝을 향해 진행':(s<5?'② 끝에서 반사되는 중':'③ 반사 펄스가 '+(free?'뒤집히지 않고(위상 그대로)':'뒤집혀서(위상 반대)')+' 왼쪽으로 진행');
 txt(m,320,248,'#0f172a',14);}
document.getElementById('fx').onclick=()=>{free=false;t=0};document.getElementById('fr').onclick=()=>{free=true;t=0};
"""
EX5 = '<button class="b" id="fx">고정단</button><button class="b" id="fr">자유단</button><button class="b" data-t="8">8초 후</button>'

# ---------------- 6. 줄의 경계 ----------------
JS6 = r"""
SP=1;let rev=false;const ox=30,sc=46,by=130,xb=6,x0=2,wd=.6;
const G=s=>Math.exp(-Math.pow((s-x0)/wd,2));
function draw(){const v1=rev?1:2,v2=rev?2:1,r=(v2-v1)/(v1+v2),tau=2*v2/(v1+v2),T=rev?7.5:8.5,s=t%T;
 const Y=x=>x<xb?G(x-v1*s)+r*G(2*xb-x-v1*s):tau*G(xb+(x-xb)*v1/v2-v1*s);
 c.fillStyle='#e0f2fe';c.fillRect(ox,50,xb*sc,190);c.fillStyle='#f1f5f9';c.fillRect(ox+xb*sc,50,6*sc,190);
 line(ox+xb*sc,50,ox+xb*sc,240,'#0f172a',2,[6,4]);txt('연결 지점',ox+xb*sc,40,'#0f172a',12);
 txt(rev?'무거운 줄 (속력 느림)':'가벼운 줄 (속력 빠름)',ox+3*sc,252,'#475569',13);txt(rev?'가벼운 줄 (속력 빠름)':'무거운 줄 (속력 느림)',ox+9*sc,252,'#475569',13);
 [[0,xb,rev],[xb,12,!rev]].forEach(g=>{c.beginPath();c.strokeStyle='#1d4ed8';c.lineWidth=g[2]?7:2.5;for(let X=g[0];X<=g[1]+.001;X+=.04){const px=ox+X*sc,py=by-Y(X)*75;X==g[0]?c.moveTo(px,py):c.lineTo(px,py)}c.stroke()});
 const hit=(xb-x0)/v1;
 if(s>hit+.6){const xr=2*xb-x0-v1*s;if(xr>.3&&xr<xb-.1)txt('반사파',ox+xr*sc,by-r*75-(r>0?26:-26),'#be123c',13);
  const xt=xb+(x0+v1*s-xb)*v2/v1;if(xt<11.6)txt('투과파',ox+xt*sc,by-tau*75-24,'#059669',13)}
 txt('t = '+s.toFixed(1)+' s',ox,16,'#0f172a',13,'left');
 txt('반사파 위상: '+(r<0?'반대(뒤집힘)':'그대로')+'  |  투과파 위상: 그대로  |  투과파 폭: '+(v2<v1?'좁아짐':'넓어짐'),ox+130,16,'#0f172a',13,'left');}
document.getElementById('lh').onclick=()=>{rev=false;t=0};document.getElementById('hl').onclick=()=>{rev=true;t=0};
"""
EX6 = '<button class="b" id="lh">가벼운→무거운</button><button class="b" id="hl">무거운→가벼운</button>'

# ---------------- 7. 초음파 비파괴 검사 ----------------
JS7 = r"""
SP=3;let crack=true;const v=.6,bx0=40,top=80,sc=52,ox=300,oy=232,ps=23;
const G=(s,p,h)=>h*Math.exp(-Math.pow((s-p)/.22,2));
function sig(s){return G(s,.3,150)+(crack?G(s,4,70):0)+G(s,10,crack?110:130)}
function pulse(tt,td,px,col,lab){if(tt>2*td)return;const d=tt<=td?v*tt:v*(2*td-tt);const y=top+d*sc;dot(px,y,6,col);arrow(px,y,px,y+(tt<=td?16:-16),col,2);txt(lab,px+(lab=='ㄱ'?-14:14),y,col,13)}
function draw(){const tt=t%14;
 c.fillStyle='#e2e8f0';c.fillRect(bx0,top,210,3*sc);c.strokeStyle='#1e293b';c.lineWidth=2;c.strokeRect(bx0,top,210,3*sc);
 c.fillStyle='#334155';c.fillRect(bx0+65,top-30,80,30);txt('탐촉자',bx0+105,top-15,'#fff',12);txt('강철',bx0+185,top+3*sc-14,'#0f172a',13);
 if(crack){line(bx0+30,top+1.2*sc,bx0+175,top+1.2*sc,'#be123c',5);txt('균열',bx0+198,top+1.2*sc-12,'#be123c',13)}
 dbl(bx0-14,top,bx0-14,top+3*sc,'#475569');txt('3 cm',bx0-14,top+1.5*sc,'#475569',11);
 if(crack)pulse(tt,2,bx0+90,'#2563eb','ㄱ');pulse(tt,5,bx0+125,'#7c3aed','ㄴ');
 axes(ox,oy,310,150,'시간 (μs)','신호 세기');
 for(let s=2;s<=12;s+=2){line(ox+s*ps,oy-3,ox+s*ps,oy+3,'#0f172a',1);txt(String(s),ox+s*ps,oy+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#0f172a';c.lineWidth=2.5;for(let s=0;s<=Math.min(tt,12.5);s+=.03){const px=ox+s*ps,py=oy-sig(s);s?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 txt('발신',ox+.3*ps+22,oy-142,'#475569',11);
 if(crack&&tt>4.4)txt('ㄱ',ox+4*ps,oy-sig(4)-10,'#2563eb',14);if(tt>10.4)txt('ㄴ',ox+10*ps,oy-sig(10)-10,'#7c3aed',14);
 txt('경과 시간 '+Math.min(tt,12).toFixed(1)+' μs (초음파 속력 6000 m/s)',320,16,'#0f172a',13,'left');
 txt('d = vΔt/2 : ㄱ → '+(crack?'6000×4×10⁻⁶/2 = 1.2 cm':'(균열 없음)')+' , ㄴ → 6000×10×10⁻⁶/2 = 3 cm',20,260,'#059669',12,'left');}
document.getElementById('ck1').onclick=()=>{crack=true;t=0};document.getElementById('ck0').onclick=()=>{crack=false;t=0};
"""
EX7 = '<button class="b" id="ck1">균열 있는 곳</button><button class="b" id="ck0">균열 없는 곳</button>'

# ---------------- 8. 실선/점선 파형, 점 R ----------------
JS8 = r"""
SP=.5;const ox=50,oy=85,sc=62,gx=50,gy=205,ps=340,T=1.6,v=5;
const Y=(x,s)=>Math.sin(Math.PI*(x-v*s)/2);
function curve(s,col,w,dash){c.beginPath();c.strokeStyle=col;c.lineWidth=w;c.setLineDash(dash||[]);for(let X=0;X<=8.8;X+=.04){const px=ox+X*sc,py=oy-Y(X,s)*40;X?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();c.setLineDash([])}
function draw(){const s=t%T;
 axes(ox,oy,570,48,'위치 (m)','변위 (cm)');
 for(let m=1;m<=8;m++){line(ox+m*sc,oy-3,ox+m*sc,oy+3,'#0f172a',1);txt(String(m),ox+m*sc,oy+14,'#475569',10)}
 curve(0,'#fca5a5',2);curve(.2,'#93c5fd',2,[6,4]);curve(s,'#be123c',3);
 dot(ox+2*sc,oy-Y(2,s)*40,7,'#0f172a');txt('R',ox+2*sc-14,oy+22,'#0f172a',15);
 arrow(430,16,560,16,'#be123c',2);txt('진행 방향',495,28,'#be123c',12);
 txt('(가) 연한 실선: t = 0 · 점선: 0.2 s 뒤 · 진한 선: 현재 (t = '+s.toFixed(2)+' s)',ox+6,14,'#0f172a',12,'left');
 axes(gx,gy,570,48,'시간 (s)','(나) 점 R의 변위 (cm) — 진행하며 그려집니다');
 for(const q of [.4,.8,1.2,1.6]){line(gx+q*ps,gy-3,gx+q*ps,gy+3,'#0f172a',1);txt(String(q),gx+q*ps,gy+14,'#475569',10)}
 c.beginPath();c.strokeStyle='#7c3aed';c.lineWidth=2.5;for(let q=0;q<=s;q+=.005){const px=gx+q*ps,py=gy-Y(2,q)*40;q?c.lineTo(px,py):c.moveTo(px,py)}c.stroke();
 dot(gx+s*ps,gy-Y(2,s)*40,6,'#7c3aed');
 txt('R의 변위 = '+f(Y(2,s),2)+' cm',30,258,'#7c3aed',13,'left');}
"""

SIMS = {
    1: ("줄의 횡파와 용수철의 종파", JS1, ""),
    2: ("변위–위치 그래프: 진폭·파장·주기·속력", JS2, EX2),
    3: ("왼쪽으로 진행하는 파동과 P, Q의 운동", JS3, EX3),
    4: ("매질 A → B: 진동수는 같고 파장·속력이 변함", JS4, EX4),
    5: ("펄스의 반사: 고정단과 자유단", JS5, EX5),
    6: ("가벼운 줄과 무거운 줄의 경계: 반사파와 투과파", JS6, EX6),
    7: ("초음파 비파괴 검사: 왕복 시간과 거리", JS7, EX7),
    8: ("실선·점선 파형과 점 R의 변위–시간 그래프", JS8, ""),
}

# ===== RENDER =====


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
    st.title("📝 탄성파 형성평가 문제 풀이")
    st.caption("Ⅲ. 탄성파와 소리 · 02 탄성파의 진행·투과·반사")
    st.markdown("각 문항의 문제 상황을 시뮬레이션으로 확인하고, 직접 풀어 본 뒤 **해설 및 정답을 펼쳐** 확인하세요.")
    st.markdown("---")

    B1, B2, B3 = "#eff6ff", "#ecfdf5", "#faf5ff"

    problem(1, B1, "기본",
            "(가)는 줄의 한쪽 끝을 위아래로 흔들 때, (나)는 용수철의 한쪽 끝을 앞뒤로 흔들 때 생긴 파동의 한 순간의 모습이다. (나)에서 A, B는 이웃한 촘촘한 부분이다.",
            ["(1) (가), (나)의 파동을 각각 횡파와 종파로 구분하고, 구분한 기준을 서술하시오.",
             "(2) (나)에서 파동의 파장을 쓰고, 그렇게 판단한 까닭을 쓰시오. (A, B 사이 거리 0.6 m)",
             "(3) 파동이 오른쪽으로 진행할 때 용수철의 각 부분도 파동과 함께 오른쪽으로 이동하는지 쓰고, 파동이 전달하는 것은 무엇인지 서술하시오.",
             "(4) 소리(음파), 지진파의 P파, 지진파의 S파를 횡파와 종파로 분류하시오."],
            r"""
- **(1)** (가) **횡파**, (나) **종파**. 파동의 진행 방향과 매질의 진동 방향이 **수직**이면 횡파, **나란하면** 종파이다.
- **(2)** **0.6 m**. 이웃한 밀(A)과 밀(B) 사이의 거리가 파장이다.
- **(3)** **이동하지 않는다.** 각 부분은 제자리에서 진동만 하고, 파동은 **에너지**를 전달한다.
- **(4)** 종파: **소리, P파** / 횡파: **S파**

*채점 포인트: (1) 진행 방향과 진동 방향의 관계, (3) '제자리 진동'과 '에너지'를 모두 언급.*
""")

    problem(2, B1, "기본",
            "진동수 5 Hz로 진동하는 파원에 의해 줄을 따라 오른쪽으로 진행하는 파동의 한 순간의 모습을 변위–위치 그래프로 나타낸 것이다. (진폭 0.2 m, 마루에서 마루까지 2 m)",
            ["(1) 이 파동의 진폭과 파장을 쓰시오.",
             "(2) 이 파동의 주기를 구하시오.",
             "(3) 파동의 진행 속력을 풀이 과정과 함께 구하시오.",
             "(4) 같은 줄에서 파원의 진동수만 10 Hz로 바꾸었을 때 파동의 속력과 파장을 각각 구하고, 속력을 그렇게 판단한 까닭을 서술하시오."],
            r"""
- **(1)** 진폭 **0.2 m**, 파장 **2 m**
- **(2)** $T=\dfrac1f=\dfrac15=$ **0.2 s**
- **(3)** $v=f\lambda=5\times2=$ **10 m/s**
- **(4)** 속력 **10 m/s**, 파장 $\lambda=\dfrac vf=\dfrac{10}{10}=$ **1 m**. 파동의 속력은 **매질(같은 줄)이 정하므로** 변하지 않는다.

*시뮬레이션의 「f = 10 Hz」 버튼으로 파장이 줄어드는 것을 확인해 보세요.*
""")

    problem(3, B2, "중간",
            "(가)는 왼쪽으로 진행하는 파동의 t = 0일 때 변위를 위치에 따라 나타낸 것이고, P, Q는 매질 위의 점이다. (나)는 P, Q 중 한 점의 변위를 시간에 따라 나타낸 것이다.",
            ["(1) 이 파동의 진폭, 파장, 주기를 각각 쓰시오.",
             "(2) 파동의 진행 속력을 풀이 과정과 함께 구하시오.",
             "(3) (나)는 P, Q 중 어느 점의 변위인지 쓰고, t = 0 직후 P와 Q의 운동 방향을 근거로 그 까닭을 서술하시오.",
             "(4) t = 0.1 s일 때 P와 Q의 변위를 각각 구하고, 두 점의 변위 차의 크기를 쓰시오."],
            r"""
- **(1)** 진폭 **2 cm**, 파장 **8 m**, 주기 **0.4 s**
- **(2)** $v=\lambda/T=8/0.4=$ **20 m/s**
- **(3)** **P**. 파형을 진행 방향(왼쪽)으로 살짝 옮기면 $t=0$ 직후 P는 **−방향**, Q는 **+방향**으로 움직인다. (나)는 $t=0$ 직후 변위가 −로 변하므로 P이다.
- **(4)** $0.1\,\text{s}=T/4$ → P: **−2 cm**, Q: **+2 cm**, 변위 차 **4 cm**

*주의: 진행 방향을 오른쪽으로 잘못 가정하면 Q로 오답이 된다.*
""")

    problem(4, B2, "중간",
            "진동수 10 Hz인 파동이 매질 A에서 매질 B로 진행할 때 어느 순간의 모습을 변위–위치 그래프로 나타낸 것이다. (경계면은 8 cm 지점)",
            ["(1) 매질 A에서 파동의 파장과 속력을 구하시오.",
             "(2) 매질 B에서 파동의 진동수와 속력을 구하고, 진동수를 그렇게 판단한 까닭을 서술하시오.",
             "(3) A와 B 중 파동의 속력이 더 빠른 매질을 쓰고, 경계면에서 A 쪽으로 반사되는 파동의 위상은 어떻게 되는지 까닭과 함께 서술하시오.",
             "(4) 파원의 진동수를 20 Hz로 바꾸면 A, B에서 파장은 각각 몇 cm가 되는지 구하시오."],
            r"""
- **(1)** $\lambda_A=$ **4 cm**, $v_A=10\times4=$ **40 cm/s**
- **(2)** 진동수 **10 Hz**, $\lambda_B=2$ cm → $v_B=$ **20 cm/s**. 진동수는 **파원이 정하므로** 매질이 바뀌어도 변하지 않는다.
- **(3)** **A**. 속력이 **느린 매질(B)과의 경계**에서 반사되므로 위상이 **반대로 바뀐다.**
- **(4)** 속력은 매질이 정하므로 그대로 → $\lambda_A=40/20=$ **2 cm**, $\lambda_B=20/20=$ **1 cm**
""")

    problem(5, B3, "심화",
            "줄을 따라 1 cm/s의 속력으로 오른쪽으로 진행하는 펄스가 (가) 고정단, (나) 자유단을 향하는 모습이다. (모눈 한 칸은 1 cm이고, 펄스의 꼭짓점은 끝에서 4 cm 떨어져 있다.)",
            ["(1) 8초 후 (가)의 줄의 모습을 그리시오.",
             "(2) 8초 후 (나)의 줄의 모습을 그리시오.",
             "(3) (가), (나)에서 반사파의 위상을 각각 쓰고, 두 경우의 차이가 생기는 까닭을 줄 끝의 움직임과 관련지어 서술하시오.",
             "(4) 가벼운 줄과 무거운 줄을 이어 가벼운 줄 쪽에서 펄스를 보낼 때(무거운 줄에서 속력이 더 느리다), 연결 지점에서 반사된 펄스는 (가)와 (나) 중 어느 경우와 같은지 쓰고 까닭을 서술하시오."],
            r"""
- **(1)** 끝에서 4 cm 떨어진 위치(꼭짓점이 8번째 칸)에 **아래로 뒤집힌 펄스**, 왼쪽으로 진행
- **(2)** 같은 위치에 **위로 볼록한 펄스(뒤집히지 않음)**, 왼쪽으로 진행
- **(3)** (가) **위상 반대**, (나) **위상 변화 없음**. 고정단은 끝이 움직이지 못해 반사파가 뒤집히고, 자유단은 끝이 자유롭게 움직여 그대로 반사된다.
- **(4)** **(가)와 같다**(뒤집혀 반사). 속력이 느린 매질과의 경계이므로 위상이 반대로 바뀐다.

*채점 포인트: 8초 동안 8 cm 이동 = 끝까지 4 cm + 되돌아 4 cm → 위치와 모양을 모두 맞아야 한다. 시뮬레이션의 「8초 후」 버튼으로 확인하세요.*
""")

    problem(6, B3, "심화",
            "(가)는 가벼운 줄과 무거운 줄을 이은 후 가벼운 줄 쪽에서 펄스를 보낸 모습이고, (나)는 펄스가 연결 지점을 지난 후의 모습이다. 무거운 줄에서 파동의 속력은 가벼운 줄에서보다 느리다.",
            ["(1) (나)의 펄스 X, Y는 각각 반사파와 투과파 중 무엇인지 쓰시오.",
             "(2) X가 (가)의 펄스와 반대 방향으로 뒤집혀 있는 까닭을 서술하시오.",
             "(3) Y의 폭이 (가)의 펄스보다 좁은 까닭을 파동의 속력, 진동수, 파장의 관계로 서술하시오.",
             "(4) 반대로 무거운 줄 쪽에서 펄스를 보낸다면 반사파와 투과파는 각각 어떤 모습일지 위상과 폭을 중심으로 예상하여 서술하시오."],
            r"""
- **(1)** X: **반사파**, Y: **투과파**
- **(2)** 속력이 **느린 매질(무거운 줄)과의 경계**에서 반사되었으므로 위상이 반대로 바뀐다.
- **(3)** **진동수는 같고** 무거운 줄에서 속력이 느리므로 $\lambda=v/f$가 짧아져 펄스의 폭이 좁아진다.
- **(4)** 반사파: 속력이 빠른 매질과의 경계이므로 **뒤집히지 않고 그대로** 반사. 투과파: **뒤집히지 않고**, 속력이 빨라 **폭이 넓어진다.**

*시뮬레이션의 「무거운→가벼운」 버튼으로 (4)를 확인해 보세요.*
""")

    problem(7, B3, "심화",
            "강철 덩어리 위에 탐촉자를 대고 초음파를 보냈을 때 되돌아온 신호를 시간에 따라 나타낸 것이다. 신호 ㄱ은 내부 균열에서, ㄴ은 강철의 바닥면에서 반사된 것이다. (단, 강철 속 초음파의 속력은 6000 m/s, 1 μs = 10⁻⁶ s이다. ㄱ은 4 μs, ㄴ은 10 μs에 도착)",
            ["(1) 신호 ㄴ을 이용하여 강철 덩어리의 두께를 풀이 과정과 함께 구하시오.",
             "(2) 균열이 표면으로부터 몇 cm 깊이에 있는지 구하시오.",
             "(3) 균열이 없는 곳에 탐촉자를 대면 신호 그래프는 어떻게 달라질지 서술하시오.",
             "(4) 이와 같은 비파괴 검사의 장점을 쓰고, 탄성파의 반사를 이용하는 다른 예를 한 가지 들어 설명하시오."],
            r"""
- **(1)** 왕복 시간 10 μs → $d=\dfrac{v\Delta t}{2}=\dfrac{6000\times10\times10^{-6}}{2}=0.03\,\text{m}=$ **3 cm**
- **(2)** $\dfrac{6000\times4\times10^{-6}}{2}=0.012\,\text{m}=$ **1.2 cm**
- **(3)** 균열에서 반사된 신호 ㄱ은 나타나지 않고, 바닥면 신호 ㄴ만 10 μs에 나타난다.
- **(4)** 물체를 자르거나 부수지 않고 내부의 결함을 찾을 수 있다. 예: 초음파 영상(몸속 관찰), 어군 탐지기, 지진파로 지구 내부 구조 탐사 등

*채점 포인트: 왕복 거리이므로 2로 나누는 과정이 필수.*
""")

    problem(8, B3, "심화",
            "(가)에서 실선은 오른쪽으로 진행하는 파동의 t = 0일 때 모습이고, 점선은 그로부터 0.2 s 뒤 처음으로 나타난 모습이다. R는 매질 위의 점이다. (진폭 1 cm, 점 R는 x = 2 m)",
            ["(1) 이 파동의 파장과 진행 속력을 풀이 과정과 함께 구하시오.",
             "(2) 이 파동의 주기를 구하시오.",
             "(3) 점 R의 변위를 시간에 따라 (나)에 0 ~ 1.6 s 동안 그리시오.",
             "(4) 문제에서 \"처음으로\"라는 조건이 없다면 파동의 속력을 하나로 정할 수 없는 까닭을 서술하시오."],
            r"""
- **(1)** $\lambda=$ **4 m**. 0.2 s 동안 파형이 1 m 이동 → $v=1/0.2=$ **5 m/s**
- **(2)** $T=\lambda/v=4/5=$ **0.8 s** (1 m = λ/4 이므로 0.2 s = T/4)
- **(3)** $t=0$에서 0, 0.2 s에 **+1 cm**, 0.4 s에 0, 0.6 s에 **−1 cm**, 0.8 s에 0인 **사인 곡선을 2주기** 그린다. (시뮬레이션 아래 그래프가 그려지는 모양과 같다.)
- **(4)** 0.2 s 동안 이동한 거리가 1 m, 5 m, 9 m, …(1 m + 한 파장의 정수 배)일 수 있어 속력이 5, 25, 45 m/s … 로 여러 값이 가능하다. (같은 파형이 한 파장마다 반복되기 때문)

*채점 포인트: (3) 시작 방향(+)과 주기 0.8 s를 모두 맞아야 정답.*
""")


run_sim()
