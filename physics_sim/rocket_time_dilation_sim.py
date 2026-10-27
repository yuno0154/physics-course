import streamlit as st
import streamlit.components.v1 as components

st.title("🚀 로켓 빛 신호와 중력 시간 지연")
st.caption("위로 가속하는 로켓의 위쪽 관찰자 A가 아래쪽 관찰자 B에게 1초 간격으로 빛 신호를 보낸다. B는 두 신호를 몇 초 간격으로 받을까? (교과서 42~43쪽, 활동지 E)")

html_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Noto Sans KR',sans-serif;background:#f8fafc;color:#1e293b;padding:10px}
.wrap{display:grid;grid-template-columns:250px 1fr 260px;gap:12px}
.card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:14px}
.lbl{font-size:11px;color:#64748b;font-weight:700;margin:10px 0 6px}
.seg{display:flex;flex-direction:column;gap:6px}
.btn{padding:8px 10px;border-radius:9px;border:1px solid #cbd5e1;background:#fff;color:#334155;font-size:12px;font-weight:700;cursor:pointer;text-align:left;font-family:inherit}
.btn.on{background:#1e3a5f;color:#fff;border-color:#1e3a5f}
.play{width:100%;padding:11px;border-radius:10px;border:none;background:#0ea5e9;color:#fff;font-size:14px;font-weight:800;cursor:pointer;margin-top:12px;font-family:inherit}
.reset{width:100%;padding:8px;border-radius:10px;border:1px solid #cbd5e1;background:#f1f5f9;color:#475569;font-size:12px;font-weight:700;cursor:pointer;margin-top:6px;font-family:inherit}
input[type=range]{width:100%}
.row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid #f1f5f9;font-size:12px}
.row b{font-size:15px}
.big{font-size:26px;font-weight:800}
.note{font-size:11px;color:#64748b;line-height:1.6}
.warn{font-size:11px;color:#b45309;background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:8px;line-height:1.55;margin-top:10px}
.concl{margin-top:10px;padding:10px;border-radius:10px;background:#eff6ff;border:1px solid #bfdbfe;font-size:13px;font-weight:700;color:#1e3a5f;line-height:1.6;min-height:64px}
canvas{width:100%;border-radius:14px;background:#0b1224;display:block}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <div class="lbl" style="margin-top:0">상황</div>
    <div class="seg">
      <button class="btn on" id="mAcc">① 우주 공간에서 위로 가속하는 로켓</button>
      <button class="btn" id="mGrav">② 지표면에 정지해 있는 로켓 (g = a)</button>
    </div>
    <div class="lbl">신호를 보내는 방향</div>
    <div class="seg">
      <button class="btn on" id="dDown">A(위) → B(아래)</button>
      <button class="btn" id="dUp">B(아래) → A(위)  · 거꾸로 생각하기</button>
    </div>
    <div class="lbl">보는 위치 (상황 ①)</div>
    <div class="seg">
      <button class="btn on" id="vIn">로켓 안에서 보기</button>
      <button class="btn" id="vOut">로켓 밖에서 보기</button>
    </div>
    <div class="lbl">가속도 a (과장된 단위) <span id="aVal" style="float:right;color:#0ea5e9">20</span></div>
    <input type="range" id="aSl" min="0" max="30" step="1" value="20">
    <button class="play" id="play">▶ 신호 보내기</button>
    <button class="reset" id="reset">↺ 처음으로</button>
  </div>

  <div class="card" style="padding:8px"><canvas id="cv" width="760" height="560"></canvas></div>

  <div class="card">
    <div class="lbl" style="margin-top:0">측정 결과</div>
    <div class="row"><span id="sendLbl">A가 보낸 간격</span><b>1.00 s</b></div>
    <div class="row"><span id="recvLbl">B가 받은 간격</span><b id="recv" class="big">-</b></div>
    <div class="row"><span id="vRedLbl">빨간 신호를 만날 때 B의 속력</span><b id="vRed">-</b></div>
    <div class="row"><span id="vBlueLbl">파란 신호를 만날 때 B의 속력</span><b id="vBlue">-</b></div>
    <div class="concl" id="concl">▶ 신호 보내기를 눌러 보자.</div>
    <div class="warn">⚠ 효과를 눈으로 보기 위해 <b>빛의 속력을 아주 느리게</b> 과장했다. 실제 지표면에서 높이 1 m 차이의 시간 지연은 약 10<sup>-16</sup> 정도로 매우 작다.</div>
  </div>
</div>

<script>
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
const W=cv.width,H=cv.height;
// 과장된 물리 단위: 빛의 속력 c, 로켓 길이 h, 가속도 a
const c=160, h=180, TE=[0.5,1.5];   // 신호를 보내는 시각(1초 간격)
let a=20, mode='acc', dir='down', view='in', t=0, running=false, last=null, stars=[];
for(let i=0;i<90;i++)stars.push([Math.random()*W,Math.random()*2000,Math.random()*1.4+0.3]);

const yB=t=> mode==='acc'?0.5*a*t*t:0;            // 바닥(B)의 위치(밖에서 본 좌표)
const vB=t=> mode==='acc'?a*t:0;
function recvTime(te){
  if(dir==='down'){ // A(위)→B(아래): h + ½a te² − c(t−te) = ½ a t²
    if(a===0) return te+h/c;
    const k=h+0.5*a*te*te+c*te; return (-c+Math.sqrt(c*c+2*a*k))/a;
  } else {          // B(아래)→A(위): ½a te² + c(t−te) = h + ½ a t²
    if(a===0) return te+h/c;
    const k=h+c*te-0.5*a*te*te; const D=c*c-2*a*k; if(D<0) return Infinity;
    return (c-Math.sqrt(D))/a;
  }
}
// 등가 원리: 지표면(g=a)에 정지한 로켓 안에서의 신호 위치 = 가속하는 로켓 안에서 본 위치
function pulseRel(te,t){ // 바닥에서 잰 신호의 높이 (로켓 안 기준)
  if(t<te) return null;
  const tr=recvTime(te); if(t>tr) return null;
  if(dir==='down') return h+0.5*a*te*te-c*(t-te)-0.5*a*t*t;
  return 0.5*a*te*te+c*(t-te)-0.5*a*t*t;
}
function absPos(te,t){ // 밖에서 본 신호의 높이
  if(dir==='down') return h+0.5*a*te*te-c*(t-te);
  return 0.5*a*te*te+c*(t-te);
}

function drawRocket(x,baseY,S,flame){
  const top=baseY-h*S-40, w=120;
  ctx.fillStyle='#cbd5e1';ctx.strokeStyle='#94a3b8';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(x-w/2,baseY);ctx.lineTo(x-w/2,top+40);ctx.quadraticCurveTo(x,top-30,x+w/2,top+40);ctx.lineTo(x+w/2,baseY);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle='#e2e8f0';ctx.fillRect(x-w/2+12,baseY-h*S-8,w-24,h*S+8);
  ctx.fillStyle='#64748b';ctx.beginPath();ctx.moveTo(x-w/2,baseY-30);ctx.lineTo(x-w/2-26,baseY+8);ctx.lineTo(x-w/2,baseY+8);ctx.fill();
  ctx.beginPath();ctx.moveTo(x+w/2,baseY-30);ctx.lineTo(x+w/2+26,baseY+8);ctx.lineTo(x+w/2,baseY+8);ctx.fill();
  if(flame){const f=18+Math.random()*10;ctx.fillStyle='rgba(251,146,60,0.9)';ctx.beginPath();ctx.moveTo(x-22,baseY+8);ctx.lineTo(x,baseY+8+f*2.2);ctx.lineTo(x+22,baseY+8);ctx.fill();
    ctx.fillStyle='rgba(253,224,71,0.95)';ctx.beginPath();ctx.moveTo(x-11,baseY+8);ctx.lineTo(x,baseY+8+f*1.2);ctx.lineTo(x+11,baseY+8);ctx.fill();}
  // 관찰자 A(위), B(아래)
  person(x,baseY-h*S-2,'A'); person(x,baseY,'B');
}
function person(x,y,l){
  ctx.fillStyle='#1e3a5f';ctx.beginPath();ctx.arc(x-30,y-34,7,0,7);ctx.fill();ctx.fillRect(x-35,y-27,10,22);
  ctx.fillStyle='#fff';ctx.font='bold 14px Noto Sans KR';ctx.fillText(l,x-58,y-18);
  ctx.strokeStyle='#475569';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x-56,y);ctx.lineTo(x+56,y);ctx.stroke();
}
function pulse(x,y,col){
  ctx.save();ctx.shadowColor=col;ctx.shadowBlur=14;ctx.fillStyle=col;ctx.fillRect(x-34,y-4,68,8);ctx.restore();
}
function arrow(x,y1,y2,col,label){
  ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x,y1);ctx.lineTo(x,y2);ctx.stroke();
  const d=Math.sign(y2-y1);ctx.beginPath();ctx.moveTo(x-7,y2-d*10);ctx.lineTo(x,y2);ctx.lineTo(x+7,y2-d*10);ctx.fill();
  ctx.font='bold 13px Noto Sans KR';ctx.fillText(label,x+10,(y1+y2)/2);
}

function draw(){
  ctx.clearRect(0,0,W,H);
  const S=(mode==='acc'&&view==='out')?1.15:1.45;   // 화면 배율
  const tr=[recvTime(TE[0]),recvTime(TE[1])];
  // 배경
  if(mode==='grav'){
    ctx.fillStyle='#0b1224';ctx.fillRect(0,0,W,H);
    ctx.fillStyle='#14532d';ctx.fillRect(0,H-60,W,60);
    ctx.fillStyle='#86efac';ctx.font='bold 13px Noto Sans KR';ctx.fillText('지표면',16,H-24);
  } else {
    ctx.fillStyle='#0b1224';ctx.fillRect(0,0,W,H);
    const shift=(view==='in')?yB(t)*S:0;
    ctx.fillStyle='rgba(255,255,255,0.7)';
    for(const s of stars){const yy=((s[1]+shift)%H+H)%H;ctx.fillRect(s[0],yy,s[2],s[2]);}
  }
  const x=W*0.42;
  let base;
  if(mode==='grav' || view==='in'){ base=H-80; }
  else { base=H-80-yB(t)*S; } // 밖에서 보기: 로켓이 위로 올라감
  drawRocket(x,base,S,mode==='acc' && a>0);
  // 가속도 또는 중력 화살표
  if(mode==='acc' && a>0) arrow(W*0.83,170,100,'#38bdf8','a');
  if(mode==='grav' && a>0) arrow(W*0.83,100,170,'#4ade80','g');
  // 신호
  const cols=['#f87171','#60a5fa'];
  TE.forEach((te,i)=>{
    let yy=null;
    if(mode==='acc' && view==='out'){
      if(t>=te && t<=tr[i]){ yy=(H-80)-absPos(te,t)*S; }
    } else {
      const r=pulseRel(te,t); if(r!==null) yy=base-r*S;
    }
    if(yy!==null) pulse(x,yy,cols[i]);
  });
  // 시간 막대
  const tl=24, tw=W-48, tmax=Math.max(3.2,(isFinite(tr[1])?tr[1]:3)+0.4), ty=36;
  ctx.fillStyle='rgba(255,255,255,0.08)';ctx.fillRect(tl,ty-16,tw,58);
  ctx.font='bold 12px Noto Sans KR';ctx.fillStyle='#e2e8f0';
  ctx.fillText(dir==='down'?'A가 보냄':'B가 보냄',tl+6,ty);ctx.fillText(dir==='down'?'B가 받음':'A가 받음',tl+6,ty+28);
  const X=tt=>tl+90+(tw-100)*tt/tmax;
  ctx.strokeStyle='rgba(255,255,255,0.3)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(X(0),ty-4);ctx.lineTo(X(tmax),ty-4);ctx.moveTo(X(0),ty+24);ctx.lineTo(X(tmax),ty+24);ctx.stroke();
  TE.forEach((te,i)=>{ if(t>=te){ctx.fillStyle=cols[i];ctx.fillRect(X(te)-3,ty-12,6,16);} if(t>=tr[i]&&isFinite(tr[i])){ctx.fillStyle=cols[i];ctx.fillRect(X(tr[i])-3,ty+16,6,16);} });
  ctx.fillStyle='#facc15';ctx.fillRect(X(Math.min(t,tmax))-1,ty-16,2,58);
  // 라벨
  ctx.fillStyle='#94a3b8';ctx.font='12px Noto Sans KR';
  const vlabel = mode==='grav' ? '지표면에 정지한 로켓 안' : (view==='in'?'로켓 안에서 본 모습':'로켓 밖(정지한 관찰자)에서 본 모습');
  ctx.fillText(vlabel,W-16-ctx.measureText(vlabel).width,H-16);
  updatePanel(tr);
}

function updatePanel(tr){
  const done=t>=tr[1];
  const dB=tr[1]-tr[0];
  document.getElementById('sendLbl').textContent=dir==='down'?'A가 보낸 간격':'B가 보낸 간격';
  document.getElementById('recvLbl').textContent=dir==='down'?'B가 받은 간격':'A가 받은 간격';
  const who=dir==='down'?'B':'A';
  document.getElementById('vRedLbl').textContent=`빨간 신호를 받을 때 ${who}의 속력`;
  document.getElementById('vBlueLbl').textContent=`파란 신호를 받을 때 ${who}의 속력`;
  const vr=t>=tr[0]?vB(tr[0]):null, vb=t>=tr[1]?vB(tr[1]):null;
  const fmt=v=> v===null?'-':(mode==='grav'?'0 (정지)':v.toFixed(0));
  document.getElementById('vRed').textContent=fmt(vr);
  document.getElementById('vBlue').textContent=fmt(vb);
  document.getElementById('recv').textContent=done&&isFinite(dB)?dB.toFixed(2)+' s':'-';
  let msg='▶ 신호 보내기를 눌러 보자.';
  if(done&&isFinite(dB)){
    if(a===0) msg='가속도가 0이면 받은 간격도 1.00 s — 두 시계의 빠르기가 같다.';
    else if(dir==='down') msg=(mode==='acc'?'B는 신호를 마중 나가므로 ':'등가 원리: 지표에서도 똑같이 ')+'1초보다 짧은 간격으로 받는다 → B가 보기에 A(위)의 시계가 빠르다. 아래쪽 시계가 느리다.';
    else msg=(mode==='acc'?'A는 신호로부터 달아나므로 ':'등가 원리: 지표에서도 똑같이 ')+'1초보다 긴 간격으로 받는다 → A가 보기에 B(아래)의 시계가 느리다.';
  } else if(t>0) msg='신호가 이동 중…';
  document.getElementById('concl').textContent=msg;
}

function loop(ts){
  if(running){ if(last===null) last=ts; t+=(ts-last)/1000*0.8; last=ts;
    const tr=recvTime(TE[1]); if(t>tr+0.6 || t>8){running=false;} }
  draw(); requestAnimationFrame(loop);
}
function reset(){t=0;running=false;last=null;}
function setOn(ids,on){ids.forEach(i=>document.getElementById(i).classList.toggle('on',i===on));}
document.getElementById('mAcc').onclick=()=>{mode='acc';setOn(['mAcc','mGrav'],'mAcc');reset();};
document.getElementById('mGrav').onclick=()=>{mode='grav';setOn(['mAcc','mGrav'],'mGrav');reset();};
document.getElementById('dDown').onclick=()=>{dir='down';setOn(['dDown','dUp'],'dDown');reset();};
document.getElementById('dUp').onclick=()=>{dir='up';setOn(['dDown','dUp'],'dUp');reset();};
document.getElementById('vIn').onclick=()=>{view='in';setOn(['vIn','vOut'],'vIn');reset();};
document.getElementById('vOut').onclick=()=>{view='out';setOn(['vIn','vOut'],'vOut');reset();};
document.getElementById('aSl').oninput=e=>{a=parseInt(e.target.value);document.getElementById('aVal').textContent=a;reset();};
document.getElementById('play').onclick=()=>{reset();running=true;};
document.getElementById('reset').onclick=reset;
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(html_code, height=600, scrolling=False)

st.markdown("### 📋 활동지 E와 함께 보기")
st.markdown("""
<style>
.q-table{width:100%;border-collapse:collapse;font-size:14px}
.q-table td{border:1px solid #e2e8f0;padding:10px;vertical-align:middle}
.q-table td:first-child{width:72%}
summary{cursor:pointer;list-style:none;background:#0ea5e9;color:#fff;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:800;display:inline-block}
details[open] summary{display:none}
</style>
<table class="q-table">
<tr><td>1. 빛 신호가 내려오는 동안 B는 위쪽으로 점점 빨라지며 신호를 마중 나간다. 파란색 신호를 만날 때 B의 속력은 빨간색 신호를 만날 때보다 (크다, 작다).</td><td><details><summary>확인</summary><b>크다</b></details></td></tr>
<tr><td>2. 그래서 B는 파란색 신호를 더 (빨리, 늦게) 만나고, B가 받은 두 신호의 시간 간격은 1초보다 (길다, 짧다).</td><td><details><summary>확인</summary><b>빨리, 짧다</b></details></td></tr>
<tr><td>3. B가 보기에 A의 시계는 자신의 시계보다 (빠르게, 느리게) 간다. 즉, 로켓의 아래쪽 시계가 (빠르게, 느리게) 간다.</td><td><details><summary>확인</summary><b>빠르게, 느리게</b></details></td></tr>
<tr><td>4. 등가 원리를 적용하면, 로켓이 지표면에 정지해 있을 때에도 지표면에 가까운 B의 시계가 A의 시계보다 (빠르게, 느리게) 간다.</td><td><details><summary>확인</summary><b>느리게</b></details></td></tr>
</table>
""", unsafe_allow_html=True)

with st.expander("👀 사용 방법과 정리"):
    st.markdown("""
- **상황 ①**에서 ‘로켓 안에서 보기’와 ‘로켓 밖에서 보기’를 번갈아 본다. 밖에서 보면 빛은 일정한 속력으로 내려오고, B가 위로 점점 빨라지며 신호를 마중 나간다.
- **가속도를 0**으로 두면 받은 간격도 1.00 s가 된다(비교 사례).
- **상황 ②**(지표면에 정지한 로켓)로 바꾸면 로켓 안에서 본 모습과 받은 간격이 상황 ①과 똑같다. 이것이 **등가 원리**를 적용한 결과이다.
- **거꾸로 생각하기**(B → A): A는 1초보다 긴 간격으로 받는다 → A가 보기에 B의 시계가 느리다. 두 방향의 결론은 같은 사실을 가리킨다.

**정리** 천체에 가까운 곳(중력이 강한 곳)일수록 시간이 **느리게** 흐른다(중력 시간 지연).
""")
