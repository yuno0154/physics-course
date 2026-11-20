import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """도플러 효과와 속도 측정(3차시) — 소리의 3요소 기초 + 학습지 B~D 순서의 탭형 시뮬레이션.
    ⓪ 소리의 3요소(진폭·진동수·파형/악기 음색) → ① 파면으로 보는 파장 변화(단계별, A/B/원래 소리 분리)
    → ② 관찰자가 움직일 때(두 줄 비교) → ③ 4가지 경우 비교·관계식
    → ④ 구급차의 속력 측정(f′–t 그래프·실제 사이렌·스테레오 패닝) → ⑤ 스피드건·청색/적색 편이
    기본 재생 속도 0.5배. 외부 라이브러리 없이 HTML/JS + Web Audio API로 동작.
    """
    st.title("🚑 도플러 효과와 속도 측정")
    components.html(HTML, height=940, scrolling=True)


HTML = r"""<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">
<style>
:root{--ink:#0f172a;--sub:#64748b;--line:#e2e8f0;--key:#1d4ed8}
*{box-sizing:border-box}body{margin:0;font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:var(--ink)}
#app{max-width:1120px;margin:0 auto;padding:4px 4px 16px}
h1{font-size:20px;margin:4px 0 2px}.lead{font-size:13px;color:var(--sub);margin:0 0 8px}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}
.tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:7px 12px;font-size:13px;font-weight:700;color:var(--sub);cursor:pointer;font-family:inherit;transition:.15s}
.tab:hover{border-color:#93c5fd;color:var(--key)}
.tab.on{background:var(--key);border-color:var(--key);color:#fff}
.ctrl{display:flex;flex-wrap:wrap;gap:7px 12px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:8px 13px;margin-bottom:8px}
.speed{background:#fffbeb;border-color:#fde68a}
.grp{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600}
input[type=range]{width:125px}.val{min-width:66px;color:var(--key);font-weight:800;font-variant-numeric:tabular-nums}
.btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:6px 10px;font-size:12.5px;font-weight:700;cursor:pointer;font-family:inherit;color:var(--ink);transition:.12s}
.btn:hover{border-color:#93c5fd;background:#f8fafc}
.btn.on{background:#eff6ff;border-color:#3b82f6;color:#1e3a8a}
.btn.on-gn{background:#ecfdf5;border-color:#059669;color:#065f46}
.btn.on-or{background:#fff7ed;border-color:#ea580c;color:#9a3412}
.btn.primary{background:#0f172a;color:#fff;border-color:#0f172a}
.btn.go{background:#1d4ed8;color:#fff;border-color:#1d4ed8;font-size:13.5px;padding:7px 13px}
.sel{border:1px solid var(--line);background:#fff;border-radius:9px;padding:5px 8px;font-size:12.5px;font-weight:700;color:var(--ink);font-family:inherit}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:8px}
canvas{display:block;width:100%;height:auto}
.view{display:none}.show{display:flex}
.step{margin-top:8px;background:#eff6ff;border:1px solid #bfdbfe;border-radius:14px;padding:10px 14px;font-size:14px;line-height:1.65;min-height:62px}
.step b{color:#1d4ed8}.note{margin-top:8px;background:#f1f5f9;border-radius:14px;padding:9px 14px;font-size:13.5px;line-height:1.6}
.ws{display:inline-block;background:#dbeafe;color:#1e3a8a;border-radius:6px;padding:0 6px;font-size:12px;font-weight:800;margin-right:6px}
.sep{width:1px;height:22px;background:#e2e8f0;margin:0 2px}
.pill-lbl{font-size:12px;font-weight:800;color:#475569;background:#f1f5f9;padding:3px 8px;border-radius:99px}
</style></head><body><div id="app">
<h1>🚑 도플러 효과와 속도 측정</h1>
<p class="lead">소리의 3요소 기초부터 3차시 학습지 B~D 순서까지 연결한 시뮬레이션입니다. 화면 속 파면 속력은 관찰을 위해 느리게 나타냈으며, 진동수·속력은 실제 음속(340 m/s)으로 계산합니다.</p>
<div class="ctrl speed"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button>
<button class="btn primary" id="pp">⏸ 일시정지</button><button class="btn" id="rs">↺ 처음부터</button></div>
<div class="tabs" id="tabs"></div>

<!-- TAB 0: 소리의 3요소 (기초) -->
<div id="c0" class="ctrl view">
 <span class="pill-lbl">🎵 음원(파형·음색)</span>
 <button class="btn on" data-inst="sine">〰️ 순음(함수발생기)</button>
 <button class="btn" data-inst="violin">🎻 바이올린</button>
 <button class="btn" data-inst="piano">🎹 피아노</button>
 <button class="btn" data-inst="square">🔲 사각파</button>
 <div class="sep"></div>
 <div class="grp">진동수(높이) <i>f</i><input type="range" id="sfreq" min="130" max="880" step="1" value="440"><span class="val" id="vsfreq">440 Hz</span></div>
 <div class="grp">진폭(세기) <i>A</i><input type="range" id="samp" min="0.1" max="1.0" step="0.05" value="0.6"><span class="val" id="vsamp">60%</span></div>
 <div class="sep"></div>
 <button class="btn go" id="splay">🔊 소리 재생</button>
 <button class="btn" id="spianoHit" style="display:none">🎹 건반 다시 치기</button>
 <span class="grp" style="gap:4px">
  <button class="btn" data-note="262">도(262)</button>
  <button class="btn" data-note="330">미(330)</button>
  <button class="btn" data-note="392">솔(392)</button>
  <button class="btn on" data-note="440">라(440)</button>
  <button class="btn" data-note="523">높은도(523)</button>
 </span>
</div>

<!-- TAB 1: 파면으로 보는 파장 변화 (A/B/원래 소리 완전 분리 + 실제 사이렌) -->
<div id="c1" class="ctrl view">
 <button class="btn go" id="nx">다음 단계 ▶</button><button class="btn" id="auto">연속 재생</button>
 <div class="grp">파원 속력 <i>v</i><sub>s</sub><input type="range" id="r0" min="0" max="0.7" step="0.05" value="0.3"><span class="val" id="v0"></span></div>
 <label class="grp"><input type="checkbox" id="ghost" checked> 정지 파면(회색)</label>
 <div class="sep"></div>
 <select id="siren0" class="sel">
  <option value="ambulance">🚑 구급차 사이렌 (삐-뽀)</option>
  <option value="firetruck">🚒 소방차 사이렌 (윙~)</option>
  <option value="pure">🎵 순음 (480 Hz 기준)</option>
 </select>
 <button class="btn" id="snd0_ref">🔊 원래 소리(도플러 없음)</button>
 <button class="btn" id="snd0_a">🔊 A 듣는 소리(다가옴·높음)</button>
 <button class="btn" id="snd0_b">🔊 B 듣는 소리(멀어짐·낮음)</button>
 <button class="btn" id="snd0_off">🔇 끄기</button>
</div>

<!-- TAB 2: 관찰자가 움직일 때 -->
<div id="c2" class="ctrl view">
 <div class="grp">관찰자 2의 속력 <i>v</i><sub>o</sub><input type="range" id="r1" min="0" max="0.8" step="0.05" value="0.5"><span class="val" id="v1"></span></div>
 <button class="btn" id="cnt1">↺ 파면 세기 다시 시작</button>
 <div class="sep"></div>
 <button class="btn" id="snd1_ref">🔊 관찰자 1 (정지 · 원래 소리)</button>
 <button class="btn" id="snd1_mov">🔊 관찰자 2 (다가감 · 높은 소리)</button>
 <button class="btn" id="snd1_off">🔇 끄기</button>
</div>

<!-- TAB 3: 4가지 경우 비교·관계식 -->
<div id="c3" class="ctrl view">
 <div class="grp">파원 <i>v</i><sub>s</sub><input type="range" id="rs2" min="-0.6" max="0.6" step="0.05" value="0.3"><span class="val" id="vs2"></span></div>
 <div class="grp">관찰자 <i>v</i><sub>o</sub><input type="range" id="ro2" min="-0.6" max="0.6" step="0.05" value="0"><span class="val" id="vo2"></span></div>
 <button class="btn" data-case="0">파원이 다가옴</button><button class="btn" data-case="1">파원이 멀어짐</button><button class="btn" data-case="2">관찰자가 다가감</button><button class="btn" data-case="3">관찰자가 멀어짐</button><button class="btn" data-case="4">같은 속도로 함께</button>
 <div class="sep"></div>
 <button class="btn" id="snd2_ref">🔊 원래 소리</button>
 <button class="btn" id="snd2_obs">🔊 관찰자 듣는 소리</button>
 <button class="btn" id="snd2_off">🔇 끄기</button>
</div>

<!-- TAB 4: 구급차의 속력 측정 (실제 사이렌 + 거리 음량 + 좌우 스테레오) -->
<div id="c4" class="ctrl view">
 <div class="grp">구급차 속력<input type="range" id="r3" min="5" max="60" step="1" value="20"><span class="val" id="v3"></span></div>
 <div class="grp">기준 진동수<input type="range" id="f3" min="300" max="900" step="10" value="480"><span class="val" id="vf3"></span></div>
 <select id="siren3" class="sel">
  <option value="ambulance">🚑 구급차 사이렌 (삐-뽀)</option>
  <option value="firetruck">🚒 소방차 사이렌 (윙~)</option>
  <option value="pure">🎵 일정 기준음 (순음)</option>
 </select>
 <button class="btn go" id="go3">▶ 구급차 출발</button>
 <button class="btn" id="snd3">🔊 통과 소리 켜기</button>
 <button class="btn" id="snd3_ref">🔊 정지(원래) 소리 듣기</button>
</div>

<!-- TAB 5: 스피드건·청색/적색 편이 -->
<div id="c5" class="ctrl view">
 <button class="btn on" id="m4a">스피드건</button><button class="btn" id="m4b">별빛의 편이</button>
 <span id="g4" style="display:flex;gap:8px;align-items:center;flex-wrap:wrap"><button class="btn on" data-st="1">1단계: 스피드건 → 자동차</button><button class="btn" data-st="2">2단계: 자동차 → 스피드건</button><button class="btn" data-st="3">3단계: 합쳐 보기</button><span class="grp">자동차 속력<input type="range" id="r4" min="0" max="60" step="5" value="30"><span class="val" id="v4"></span></span></span>
 <span id="g4star" style="display:none;gap:6px;align-items:center;flex-wrap:wrap">
  <button class="btn" data-sth="0">위치 A (적색 편이)</button>
  <button class="btn" data-sth="1.5708">위치 B (편이 없음)</button>
  <button class="btn" data-sth="3.1416">위치 C (청색 편이)</button>
  <button class="btn" data-sth="4.7124">위치 D (편이 없음)</button>
  <button class="btn on" id="starPlay">▶ 연속 공전</button>
 </span>
</div>

<div class="card"><canvas id="cv" width="1000" height="460"></canvas></div>
<div class="step" id="step"></div>
<div class="note" id="note"></div>
</div>
<script>
const $=id=>document.getElementById(id), cv=$('cv'), ctx=cv.getContext('2d'), W=1000, H=460;
const BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',INK='#0f172a',SUB='#64748b',OR='#ea580c';
const VS=340;
const TABS=[
 ['⓪ 소리의 3요소 (기초)','기초 개념','소리의 3요소는 <b>세기(진폭)</b>, <b>높낮이(진동수)</b>, <b>음색(파형)</b>입니다. 도플러 효과에서 변하는 것은 소리의 <b>진동수(높낮이)</b>입니다!'],
 ['① 파면으로 보는 파장 변화','B','파원이 한 주기 T 동안 v<sub>s</sub>T만큼 움직이는 사이 앞의 파면은 vT만큼 진행합니다. 그래서 앞쪽 파장은 (v−v<sub>s</sub>)T로 짧아지고 뒤쪽은 (v+v<sub>s</sub>)T로 길어집니다.'],
 ['② 관찰자가 움직일 때','C①~⑤','파면 사이의 거리(파장)는 그대로입니다. 다가가는 관찰자에게는 소리가 v+v<sub>o</sub>의 속력으로 다가와 1초 동안 만나는 파면의 수가 많아집니다.'],
 ['③ 4가지 경우 비교·관계식','C⑥·알아두기','파원이 움직이면 파장이, 관찰자가 움직이면 관찰자가 측정하는 소리의 속력이 달라집니다. 같은 속도로 함께 움직이면 진동수는 변하지 않습니다.'],
 ['④ 구급차의 속력 측정','D①②','다가올 때와 멀어질 때 측정한 진동수로 구급차의 속력을 거꾸로 구할 수 있습니다. (실제 구급차·소방차 사이렌으로 도플러 효과를 들어 보세요!)'],
 ['⑤ 스피드건·청색/적색 편이','D③④','반사파의 진동수 변화로 속력을 재고(스피드건), 별빛의 파장 변화로 별의 운동을 압니다(청색·적색 편이).']
];
let tab=0,paused=false,speed=0.5,last=performance.now();
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};
$('rs').onclick=()=>reset();

// ---------- draw helpers
function txt(s,x,y,o){o=o||{};ctx.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Pretendard","Malgun Gothic",sans-serif';ctx.fillStyle=o.c||INK;ctx.textAlign=o.a||'center';ctx.textBaseline='middle';ctx.fillText(s,x,y)}
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function head(x,y,dx,dy,c,s){s=s||9;const a=Math.atan2(dy,dx);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x,y);ctx.lineTo(x-s*Math.cos(a-0.4),y-s*Math.sin(a-0.4));ctx.lineTo(x-s*Math.cos(a+0.4),y-s*Math.sin(a+0.4));ctx.fill()}
function arr(x0,y0,x1,y1,c,w){ln(x0,y0,x1,y1,c,w||2.5);head(x1,y1,x1-x0,y1-y0,c)}
function dbl(x0,y0,x1,y1,c){if(Math.hypot(x1-x0,y1-y0)<2)return;ln(x0,y0,x1,y1,c,2);head(x1,y1,x1-x0,y1-y0,c,7);head(x0,y0,x0-x1,y0-y1,c,7)}
function dot(x,y,r,c){ctx.beginPath();ctx.fillStyle=c;ctx.arc(x,y,r,0,7);ctx.fill()}
function person(x,y,c){c=c||INK;ctx.strokeStyle=c;ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y-34,7,0,7);ctx.stroke();ln(x,y-27,x,y-10,c,2);ln(x-9,y,x,y-10,c,2);ln(x+9,y,x,y-10,c,2);ln(x-10,y-21,x+10,y-21,c,2)}
function clear(){ctx.clearRect(0,0,W,H)}
function f1(x,d){return x.toFixed(d==null?0:d)}

// =========================================================================
// 고품질 Web Audio 사운드 엔진
// 1) 악기·함수발생기 합성기 (순음 / 바이올린 / 피아노 / 사각파)
// 2) 실제 구급차(Hi-Lo 삐뽀) · 소방차(Wail 윙~) 사이렌 합성기 (도플러 배율·거리음량·스테레오 패닝)
// =========================================================================
let AC=null;
function ensureAC(){
 if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();
 if(AC.state==='suspended')AC.resume();
 return AC;
}

// --- (A) 사이렌 / 도플러 음원 엔진 ---
const Siren={
 active:false, mode:'ambulance', ratio:1.0, baseF:480, vol:0.14, pan:0,
 osc1:null, osc2:null, osc3:null, flt:null, gNode:null, pNode:null, timer:null, startT:0,
 start(mode, baseF, ratio, vol, pan){
  this.stop();
  const ac=ensureAC();
  this.active=true; this.mode=mode||'ambulance'; this.baseF=baseF||480;
  this.ratio=ratio||1.0; this.vol=vol!=null?vol:0.14; this.pan=pan||0; this.startT=ac.currentTime;

  this.gNode=ac.createGain();
  this.gNode.gain.setValueAtTime(0.001, ac.currentTime);
  this.gNode.gain.linearRampToValueAtTime(this.vol, ac.currentTime+0.04);

  this.flt=ac.createBiquadFilter();
  this.flt.type='bandpass';
  this.flt.frequency.value=1100;
  this.flt.Q.value=1.1;

  if(ac.createStereoPanner){
   this.pNode=ac.createStereoPanner();
   this.pNode.pan.value=this.pan;
   this.flt.connect(this.gNode).connect(this.pNode).connect(ac.destination);
  }else{
   this.flt.connect(this.gNode).connect(ac.destination);
  }

  this.osc1=ac.createOscillator();
  this.osc2=ac.createOscillator();
  this.osc3=ac.createOscillator();
  const g1=ac.createGain(), g2=ac.createGain(), g3=ac.createGain();

  if(this.mode==='pure'){
   this.osc1.type='sine'; g1.gain.value=1.0;
   this.osc2.type='sine'; g2.gain.value=0.0;
   this.osc3.type='sine'; g3.gain.value=0.0;
   this.flt.type='allpass';
  }else{
   // 실제 구급차/소방차 혼 스피커 배음 구성 (풍부한 톱니/사각 혼합 + 대역통과 공명)
   this.osc1.type='sawtooth'; g1.gain.value=0.55;
   this.osc2.type='triangle'; g2.gain.value=0.45;
   this.osc3.type='square';   g3.gain.value=0.14;
   this.flt.type='bandpass';
   this.flt.frequency.value=Math.max(600, this.baseF*2.1);
   this.flt.Q.value=0.9;
  }
  this.osc1.connect(g1).connect(this.flt);
  this.osc2.connect(g2).connect(this.flt);
  this.osc3.connect(g3).connect(this.flt);
  this.osc1.start(); this.osc2.start(); this.osc3.start();
  this.applyFreq();
  this.timer=setInterval(()=>this.applyFreq(), 40);
 },
 applyFreq(){
  if(!this.active||!AC)return;
  const t=AC.currentTime-this.startT;
  let fBase=this.baseF;
  if(this.mode==='ambulance'){
   // 한국 구급차 특유의 2음 Hi-Lo 사이렌 (삐-뽀: 660Hz ↔ 880Hz 비율 = 1 : 1.333, 0.55초 교대)
   const hi=(Math.floor(t/0.55)%2===0);
   fBase=hi ? this.baseF*1.333 : this.baseF;
  }else if(this.mode==='firetruck'){
   // 소방차 Wail 사이렌 (부드럽게 윙~ 올라갔다 내려옴: 0.78f ↔ 1.45f, 2.2초 주기)
   const cyc=(Math.sin(2*Math.PI*t/2.2 - Math.PI/2)+1)/2;
   fBase=this.baseF*(0.78 + 0.67*cyc);
  }
  const fObs=Math.max(80, Math.min(3500, fBase*this.ratio));
  const now=AC.currentTime;
  this.osc1.frequency.setTargetAtTime(fObs, now, 0.025);
  this.osc2.frequency.setTargetAtTime(fObs*2.0, now, 0.025);
  this.osc3.frequency.setTargetAtTime(fObs*3.0, now, 0.025);
  if(this.gNode)this.gNode.gain.setTargetAtTime(this.vol, now, 0.04);
  if(this.pNode)this.pNode.pan.setTargetAtTime(Math.max(-1,Math.min(1,this.pan)), now, 0.04);
 },
 update(ratio, vol, pan, baseF){
  this.ratio=ratio;
  if(vol!=null)this.vol=vol;
  if(pan!=null)this.pan=pan;
  if(baseF!=null)this.baseF=baseF;
  this.applyFreq();
 },
 stop(){
  this.active=false;
  if(this.timer){clearInterval(this.timer);this.timer=null}
  [this.osc1,this.osc2,this.osc3].forEach(o=>{if(o){try{o.stop()}catch(e){}}});
  this.osc1=this.osc2=this.osc3=null;
  if(this.gNode){try{this.gNode.disconnect()}catch(e){};this.gNode=null}
  if(this.pNode){try{this.pNode.disconnect()}catch(e){};this.pNode=null}
 }
};

// --- (B) 소리의 3요소: 함수발생기 & 실제 악기(바이올린·피아노) 합성기 ---
const HARMONICS={
 sine:   [1.0, 0,    0,    0,    0,    0,    0,    0],
 violin: [1.0, 0.74, 0.52, 0.36, 0.25, 0.16, 0.10, 0.06], // 활로 긋는 현악기(풍부한 고차 배음)
 piano:  [1.0, 0.56, 0.26, 0.16, 0.08, 0.04, 0.02, 0.01], // 해머 타격 피아노(기본음+2~4배음 중심)
 square: [1.0, 0,    0.33, 0,    0.20, 0,    0.14, 0]     // 홀수 배음만 존재
};

const InstAudio={
 playing:false, inst:'sine', freq:440, amp:0.6,
 oscs:[], master:null, vibOsc:null, vibGain:null, pianoTimer:null,
 start(){
  this.stop();
  const ac=ensureAC();
  this.playing=true;
  if(this.inst==='piano'){
   this.triggerPiano();
   this.pianoTimer=setInterval(()=>{if(this.playing)this.triggerPiano()}, 1350);
   return;
  }
  this.master=ac.createGain();
  this.master.gain.setValueAtTime(0.001, ac.currentTime);
  this.master.gain.linearRampToValueAtTime(this.amp*0.20, ac.currentTime+(this.inst==='violin'?0.18:0.04));

  // 바이올린 공명통(Body Formant) 필터
  let dest=ac.destination;
  if(this.inst==='violin'){
   const f1=ac.createBiquadFilter(); f1.type='peaking'; f1.frequency.value=480; f1.gain.value=5; f1.Q.value=2.0;
   const f2=ac.createBiquadFilter(); f2.type='peaking'; f2.frequency.value=2500; f2.gain.value=4; f2.Q.value=2.5;
   const lp=ac.createBiquadFilter(); lp.type='lowpass'; lp.frequency.value=4600;
   this.master.connect(f1).connect(f2).connect(lp).connect(ac.destination);
   // 바이올린 자연스러운 비브라토 (5.5 Hz)
   this.vibOsc=ac.createOscillator();
   this.vibGain=ac.createGain();
   this.vibOsc.frequency.value=5.5;
   this.vibGain.gain.value=this.freq*0.008;
   this.vibOsc.connect(this.vibGain);
   this.vibOsc.start();
  }else{
   this.master.connect(dest);
  }

  const hArr=HARMONICS[this.inst]||HARMONICS.sine;
  const norm=hArr.reduce((a,b)=>a+b,0)||1;
  this.oscs=[];
  hArr.forEach((w,idx)=>{
   if(w<=0.001)return;
   const o=ac.createOscillator();
   const g=ac.createGain();
   o.type='sine';
   o.frequency.value=this.freq*(idx+1);
   g.gain.value=w/norm;
   if(this.vibGain)this.vibGain.connect(o.frequency);
   o.connect(g).connect(this.master);
   o.start();
   this.oscs.push({o, mul:idx+1});
  });
 },
 triggerPiano(){
  const ac=ensureAC();
  const now=ac.currentTime;
  const env=ac.createGain();
  // 피아노 특유의 즉각적 해머 어택 + 자연스러운 지수 감쇠
  env.gain.setValueAtTime(0.001, now);
  env.gain.linearRampToValueAtTime(this.amp*0.28, now+0.012);
  env.gain.exponentialRampToValueAtTime(this.amp*0.08, now+0.28);
  env.gain.exponentialRampToValueAtTime(0.0008, now+1.25);

  const lp=ac.createBiquadFilter();
  lp.type='lowpass';
  lp.frequency.setValueAtTime(Math.min(7500, this.freq*9), now);
  lp.frequency.exponentialRampToValueAtTime(Math.max(600, this.freq*2.4), now+0.9);
  env.connect(lp).connect(ac.destination);

  const hArr=HARMONICS.piano;
  const norm=hArr.reduce((a,b)=>a+b,0);
  hArr.forEach((w,idx)=>{
   if(w<=0.001)return;
   const o=ac.createOscillator();
   const g=ac.createGain();
   o.type='sine';
   // 피아노 현의 미세한 인하모니시티(inharmonicity) 반영
   const inharm=1+0.00025*idx*idx;
   o.frequency.setValueAtTime(this.freq*(idx+1)*inharm, now);
   g.gain.value=w/norm;
   o.connect(g).connect(env);
   o.start(now); o.stop(now+1.3);
  });
 },
 update(){
  if(!this.playing||!AC)return;
  if(this.inst==='piano')return; // 피아노는 다음 타건에 반영
  const now=AC.currentTime;
  if(this.master)this.master.gain.setTargetAtTime(this.amp*0.20, now, 0.03);
  if(this.vibGain)this.vibGain.gain.setTargetAtTime(this.freq*0.008, now, 0.03);
  this.oscs.forEach(item=>item.o.frequency.setTargetAtTime(this.freq*item.mul, now, 0.025));
 },
 stop(){
  this.playing=false;
  if(this.pianoTimer){clearInterval(this.pianoTimer);this.pianoTimer=null}
  if(this.vibOsc){try{this.vibOsc.stop()}catch(e){};this.vibOsc=null;this.vibGain=null}
  this.oscs.forEach(item=>{try{item.o.stop()}catch(e){}});
  this.oscs=[];
  if(this.master){try{this.master.disconnect()}catch(e){};this.master=null}
 }
};

function stopAllAudio(){
 Siren.stop(); InstAudio.stop();
 snd0mode='off'; snd1mode='off'; snd2mode='off'; T3.snd=false; T3.sndRef=false;
 syncSndButtons();
}

// =========================================================================
// TAB 0 : 소리의 3요소 (진폭·진동수·파형/악기 음색)
// =========================================================================
const TS={t:0, inst:'sine', freq:440, amp:0.6};
const INST_INFO={
 sine:   {name:'순음 (함수 발생기 · 사인파)', col:BL, desc:'기본 진동수(1f) 하나만 있는 가장 단순한 사인파입니다. 도플러 효과의 진동수 변화 기준음으로 사용합니다.'},
 violin: {name:'🎻 바이올린 (활로 긋는 현악기)', col:RD, desc:'활이 현을 계속 문지르며 2배음·3배음·4배음 이상 고차 배음이 강하게 섞여, 뾰족한 톱니 모양에 가까운 복합 파형을 만듭니다.'},
 piano:  {name:'🎹 피아노 (해머로 치는 건반악기)', col:PU, desc:'해머가 현을 때리는 순간 맑고 단단한 어택과 함께 1~4배음이 조화롭게 섞인 둥근 복합 파형이 만들어지며 서서히 감쇠합니다.'},
 square: {name:'🔲 사각파 (디지털 부저음)', col:OR, desc:'홀수 배음(1f, 3f, 5f, 7f)만 섞여 계단처럼 각진 파형을 이루며, 전자 시계·게임기 같은 톡 쏘는 기계 음색이 납니다.'}
};

function evalWave(inst, phase){
 const h=HARMONICS[inst]||HARMONICS.sine;
 let y=0, sum=0;
 for(let k=0;k<h.length;k++){
  if(h[k]>0){
   // 바이올린/피아노의 위상 조합으로 실제 오실로스코프 파형 재현
   const ph=(inst==='violin') ? (k+1)*phase : (k+1)*phase + (k%2?0.35:0);
   y += h[k]*Math.sin(ph);
   sum += h[k];
  }
 }
 return y/(sum*0.72);
}

function sceneSound(dt){
 if(!paused)TS.t+=dt*1.2;
 clear();
 const info=INST_INFO[TS.inst];

 // 좌측: 실시간 오실로스코프 (시간-변위 파형)
 const ox=45, oy=52, ow=610, oh=315, midY=oy+oh/2;
 ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.roundRect(ox,oy,ow,oh,14); ctx.fill();
 // 격자
 for(let i=1;i<10;i++)ln(ox+i*ow/10,oy,ox+i*ow/10,oy+oh,'rgba(148,163,184,0.16)',1);
 for(let j=1;j<6;j++)ln(ox,oy+j*oh/6,ox+ow,oy+j*oh/6,'rgba(148,163,184,0.16)',1);
 ln(ox,midY,ox+ow,midY,'rgba(148,163,184,0.45)',1.5);

 txt('📺 실시간 오실로스코프 (시간 – 공기 압력 변위 파형)', ox+14, oy-16, {a:'left',b:1,s:14,c:INK});
 txt('표시 시간 창: 0 ~ 10 ms (0.01초)', ox+ow-8, oy-16, {a:'right',s:12,c:SUB});

 // 파형 그리기 (시간 창 = 0.010초 동안 freq * 0.010 사이클 표시)
 const winSec=0.010;
 const maxAmpPx=(oh/2 - 26);
 const curAmpPx=TS.amp*maxAmpPx;
 ctx.beginPath();
 ctx.strokeStyle=info.col==='#e11d48'?'#fb7185':(info.col==='#7c3aed'?'#c084fc':(info.col==='#ea580c'?'#fb923c':'#38bdf8'));
 ctx.lineWidth=3.2;
 for(let px=0;px<=ow;px+=2){
  const tSec=(px/ow)*winSec;
  const phase=2*Math.PI*TS.freq*tSec - TS.t*6.0;
  const val=Math.max(-1.08, Math.min(1.08, evalWave(TS.inst, phase)));
  const py=midY - val*curAmpPx;
  if(px===0)ctx.moveTo(ox+px,py); else ctx.lineTo(ox+px,py);
 }
 ctx.stroke();

 // 진폭 A 화살표 표시
 const ax=ox+ow-44;
 dbl(ax, midY-curAmpPx, ax, midY, '#fde047');
 txt('진폭 A', ax-30, midY-curAmpPx/2, {c:'#fde047',b:1,s:12});

 // 주기 T 표시
 const periodPx=(1/TS.freq)/winSec*ow;
 if(periodPx>=26 && periodPx<=ow*0.8){
  const px0=ox+55, px1=px0+periodPx, pyT=oy+26;
  dbl(px0, pyT, px1, pyT, '#34d399');
  txt('1주기 T = '+(1000/TS.freq).toFixed(2)+' ms', (px0+px1)/2, pyT-12, {c:'#34d399',b:1,s:12});
 }

 // 하단 요약 배지 (진폭 / 진동수 / 파형)
 const bx=ox, by=oy+oh+24;
 const cards=[
  ['① 세기 (진폭 A)', Math.round(TS.amp*100)+'%', '파동의 위아래 높이', '#ea580c'],
  ['② 높낮이 (진동수 f)', TS.freq+' Hz', '1초당 진동 횟수 (도플러 변화!)', '#2563eb'],
  ['③ 음색 (파형)', info.name.split(' ')[0], '배음 구성에 따른 파형 모양', '#7c3aed']
 ];
 cards.forEach((c,i)=>{
  const cx=bx+i*208;
  ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2;
  ctx.beginPath(); ctx.roundRect(cx,by,196,62,10); ctx.fill(); ctx.stroke();
  txt(c[0], cx+98, by+15, {s:11.5,c:SUB,b:1});
  txt(c[1], cx+98, by+34, {s:15.5,c:c[3],b:1});
  txt(c[2], cx+98, by+51, {s:10.5,c:SUB});
 });

 // 우측: 배음(주파수) 스펙트럼 막대 그래프
 const sx=685, sy=52, sw=285, sh=315;
 ctx.fillStyle='#f8fafc'; ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1.2;
 ctx.beginPath(); ctx.roundRect(sx,sy,sw,sh,14); ctx.fill(); ctx.stroke();
 txt('📊 배음 스펙트럼 (음색의 비밀)', sx+sw/2, sy-16, {b:1,s:14,c:INK});
 txt('기본음(1f)과 정수배 배음(2f, 3f…)의 비율', sx+sw/2, sy+22, {s:11.5,c:SUB});

 const hArr=HARMONICS[TS.inst]||HARMONICS.sine;
 const baseY=sy+sh-42, maxBarH=sh-96;
 ln(sx+22, baseY, sx+sw-18, baseY, '#64748b', 1.5);
 hArr.forEach((val,idx)=>{
  const barX=sx+34+idx*30;
  const bh=val*TS.amp*maxBarH;
  ctx.fillStyle=idx===0?BL:info.col;
  ctx.beginPath(); ctx.roundRect(barX-9, baseY-bh, 18, Math.max(2,bh), [4,4,0,0]); ctx.fill();
  txt((idx+1)+'f', barX, baseY+14, {s:11,b:1,c:idx===0?BL:INK});
  if(val>0)txt(Math.round(val*100)+'%', barX, baseY-bh-10, {s:9.5,c:SUB,b:1});
 });

 // 우측 하단 안내 박스
 ctx.fillStyle='#eff6ff'; ctx.strokeStyle='#bfdbfe';
 ctx.beginPath(); ctx.roundRect(sx, sy+sh+24, sw, 62, 10); ctx.fill(); ctx.stroke();
 txt('💡 같은 440 Hz라도', sx+sw/2, sy+sh+44, {s:12.5,b:1,c:BL});
 txt('바이올린·피아노의 배음 비율이 달라', sx+sw/2, sy+sh+61, {s:11.5,c:INK});
 txt('파형 모양과 음색이 다르게 들립니다!', sx+sw/2, sy+sh+76, {s:11.5,c:INK});

 $('step').innerHTML='<b>'+info.name+'</b> · '+info.desc+'<br>👉 <b>진동수</b>를 바꾸면 음의 높낮이와 화면 속 마루 개수가, <b>진폭</b>을 바꾸면 소리의 세기와 파형 높이가, <b>악기(바이올린·피아노)</b>를 바꾸면 파형 모양(음색)이 바뀝니다.';
}

document.querySelectorAll('[data-inst]').forEach(b=>b.onclick=()=>{
 TS.inst=b.dataset.inst; InstAudio.inst=TS.inst;
 document.querySelectorAll('[data-inst]').forEach(x=>x.classList.toggle('on',x===b));
 $('spianoHit').style.display=(TS.inst==='piano')?'inline-block':'none';
 if(InstAudio.playing)InstAudio.start();
});
$('sfreq').oninput=e=>{TS.freq=+e.target.value; InstAudio.freq=TS.freq; $('vsfreq').textContent=TS.freq+' Hz'; InstAudio.update();};
$('samp').oninput=e=>{TS.amp=+e.target.value; InstAudio.amp=TS.amp; $('vsamp').textContent=Math.round(TS.amp*100)+'%'; InstAudio.update();};
$('splay').onclick=()=>{
 if(InstAudio.playing){InstAudio.stop(); $('splay').textContent='🔊 소리 재생'; $('splay').classList.remove('on')}
 else{InstAudio.inst=TS.inst; InstAudio.freq=TS.freq; InstAudio.amp=TS.amp; InstAudio.start(); $('splay').textContent='🔇 소리 끄기'; $('splay').classList.add('on')}
};
$('spianoHit').onclick=()=>{InstAudio.inst='piano'; InstAudio.freq=TS.freq; InstAudio.amp=TS.amp; InstAudio.triggerPiano();};
document.querySelectorAll('[data-note]').forEach(b=>b.onclick=()=>{
 TS.freq=+b.dataset.note; InstAudio.freq=TS.freq; $('sfreq').value=TS.freq; $('vsfreq').textContent=TS.freq+' Hz';
 document.querySelectorAll('[data-note]').forEach(x=>x.classList.toggle('on',x===b));
 if(TS.inst==='piano')InstAudio.triggerPiano(); else if(InstAudio.playing)InstAudio.update();
});

// =========================================================================
// TAB 1 : 파면으로 보는 파장 변화 (A · B · 원래 소리 완전 분리!)
// =========================================================================
const T0={t:0,target:0,auto:false,r:0.3,ghost:true};
const V0=78;
let snd0mode='off'; // 'off' | 'ref' | 'a' | 'b'

function step0Text(k,r){
 if(k<0.01) return '<b>0단계</b> · 파원(●)이 S<sub>0</sub>에 있습니다. <b>다음 단계 ▶</b>를 누르면 한 주기 <i>T</i>씩 시간이 흐릅니다. 위 버튼으로 <b>원래 소리 / A 소리 / B 소리</b>를 따로 눌러 비교해 보세요.';
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
 if(N>=1){const a=N-1,b=N; const xa=x0+vs*a,xb=x0+vs*b,Ra=V0*(t-a),Rb=V0*(t-b);
  const fa=xa+Ra,fb=xb+Rb,ba=xa-Ra,bb=xb-Rb;
  const yA=cy+95; ln(fa,cy,fa,yA+8,GN,1,[3,3]);ln(fb,cy,fb,yA+8,GN,1,[3,3]);dbl(fb,yA,fa,yA,GN);txt('A 쪽 파장',(fa+fb)/2,yA+17,{c:GN,b:1,s:13});
  ln(ba,cy,ba,yA+8,OR,1,[3,3]);ln(bb,cy,bb,yA+8,OR,1,[3,3]);dbl(ba,yA,bb,yA,OR);txt('B 쪽 파장',(ba+bb)/2,yA+17,{c:OR,b:1,s:13});
  if(t-N<0.05||!T0.auto){
   const yv=Math.max(16,cy-Ra-12); ln(xa,cy,xa,yv,BL,1,[2,3]);dbl(xa,yv,xa+V0,yv,BL);txt('vT (파면이 진행한 거리)',xa+V0/2,yv-12,{c:BL,b:1,s:13});
   if(vs>2){dbl(xa,cy+38,xb,cy+38,RD);txt('vₛT (파원이 이동한 거리)',(xa+xb)/2,cy+54,{c:RD,b:1,s:13})}}
 }

 // 현재 듣는 관찰자 강조 표시
 if(snd0mode==='a'){ctx.fillStyle='rgba(5,150,105,0.14)';ctx.beginPath();ctx.arc(W-40,cy+22,34,0,7);ctx.fill();txt('🔊 듣는 중',W-40,cy-22,{c:GN,b:1,s:12})}
 if(snd0mode==='b'){ctx.fillStyle='rgba(234,88,12,0.14)';ctx.beginPath();ctx.arc(40,cy+22,34,0,7);ctx.fill();txt('🔊 듣는 중',40,cy-22,{c:OR,b:1,s:12})}
 if(snd0mode==='ref'){txt('🔊 정지 파원 원래 소리(도플러 없음) 재생 중',W/2,24,{c:BL,b:1,s:13})}

 person(W-40,cy+40,GN);txt('A',W-40,cy+56,{b:1,c:GN});person(40,cy+40,OR);txt('B',40,cy+56,{b:1,c:OR});
 const by=405,sc=1.6,lam=V0,la=(V0-vs),lb=(V0+vs),f=480,vsr=r*VS;
 txt('파장 비교',60,by-28,{b:1,s:13,a:'left'});
 [['B 쪽 파장',lb,OR],['정지했을 때',lam,'#94a3b8'],['A 쪽 파장',la,GN]].forEach((q,i)=>{const y=by-10+i*20;txt(q[0],60,y,{s:12,a:'left',c:q[2],b:1});ctx.fillStyle=q[2];ctx.fillRect(150,y-6,q[1]*sc,12)});
 txt('f = 480 Hz일 때  A: '+f1(f*VS/(VS-vsr))+' Hz (높음),   원래: 480 Hz,   B: '+f1(f*VS/(VS+vsr))+' Hz (낮음)',W-20,by+10,{a:'right',s:13.5,b:1});
 txt('vₛ = '+f1(vsr)+' m/s  ( vₛ/v = '+r.toFixed(2)+' )',W-20,by-18,{a:'right',s:13,c:SUB});
 $('step').innerHTML=step0Text(Math.min(t,T0.target+0.0001),r);

 if(snd0mode!=='off'&&Siren.active){
  const ratio=snd0mode==='ref'?1.0:(snd0mode==='a'?VS/(VS-vsr):VS/(VS+vsr));
  Siren.update(ratio, 0.14, snd0mode==='a'?0.35:(snd0mode==='b'?-0.35:0), 480);
 }
}
function setSnd0(mode){
 snd0mode=(snd0mode===mode)?'off':mode;
 if(snd0mode==='off'){Siren.stop();}
 else{
  const vsr=T0.r*VS;
  const ratio=snd0mode==='ref'?1.0:(snd0mode==='a'?VS/(VS-vsr):VS/(VS+vsr));
  Siren.start($('siren0').value, 480, ratio, 0.14, snd0mode==='a'?0.35:(snd0mode==='b'?-0.35:0));
 }
 syncSndButtons();
}
function unpause(){if(paused){paused=false;$('pp').textContent='⏸ 일시정지'}}
$('nx').onclick=()=>{unpause();T0.auto=false;$('auto').classList.remove('on');if(T0.target>=5){T0.t=0;T0.target=1}else T0.target=Math.floor(T0.target+1e-6)+1};
$('auto').onclick=()=>{unpause();T0.auto=!T0.auto;$('auto').classList.toggle('on',T0.auto)};
$('r0').oninput=e=>{T0.r=+e.target.value;$('v0').textContent=f1(T0.r*VS)+' m/s'};
$('ghost').onchange=e=>T0.ghost=e.target.checked;
$('siren0').onchange=()=>{if(snd0mode!=='off'){const cur=snd0mode;snd0mode='off';setSnd0(cur);}};
$('snd0_ref').onclick=()=>setSnd0('ref');
$('snd0_a').onclick=()=>setSnd0('a');
$('snd0_b').onclick=()=>setSnd0('b');
$('snd0_off').onclick=()=>{snd0mode='off';Siren.stop();syncSndButtons()};

// =========================================================================
// TAB 2 : 관찰자가 움직일 때
// =========================================================================
const T1={t:0,r:0.5,c1:0,c2:0,t0:0,x2:0,prev1:null,prev2:null};
const LV=90,LT=1.0;
let snd1mode='off';
function scene1(dt){
 if(!paused){T1.t+=dt*0.9}
 const t=T1.t; clear();
 const sx=60,lanes=[150,320];
 const lam=LV*LT, vo=T1.r*LV;
 if(T1.x2===0)T1.x2=930; if(!paused)T1.x2-=vo*dt*0.9; if(T1.x2<380){T1.x2=930;T1.c1=0;T1.c2=0;T1.prev1=null;T1.prev2=null;T1.t0=t}
 const x1=930,x2=T1.x2;
 lanes.forEach((y,k)=>{ctx.fillStyle=k?'#faf5ff':'#f8fafc';ctx.fillRect(20,y-55,W-40,110);
  const nmax=Math.floor(t/LT);for(let n=nmax;n>=0;n--){const x=sx+LV*(t-n*LT);if(x>W-20)break;ln(x,y-48,x,y+48,BL,2.2)}
  dot(sx,y,10,RD);txt('파원(정지)',sx,y+66,{s:12,c:SUB});
 });
 const crossCount=(x,tt)=>Math.floor((tt-(x-sx)/LV)/LT);
 const c1=crossCount(x1,t);
 if(T1.prev1===null)T1.prev1=c1; if(c1>T1.prev1){T1.c1+=c1-T1.prev1;T1.prev1=c1}
 const c2=Math.floor((t-(x2-sx)/LV)/LT); if(T1.prev2===null)T1.prev2=c2; if(c2>T1.prev2){T1.c2+=c2-T1.prev2;T1.prev2=c2}
 person(x1,lanes[0]+38,INK);txt('관찰자 1 (정지)',x1,lanes[0]+56,{s:12,b:1});
 person(x2,lanes[1]+38,PU);arr(x2-14,lanes[1]-40,x2-14-Math.max(14,vo*0.6),lanes[1]-40,PU,2);txt('관찰자 2 (v_o로 다가감)',x2,lanes[1]+56,{s:12,b:1,c:PU});
 lanes.forEach(y=>{const k=Math.floor(t/LT);const xL=sx+LV*(t-(k-1)*LT),xR=sx+LV*(t-(k-2)*LT);if(xR<W-40){dbl(xL,y-54,xR,y-54,GN);txt('λ (같음)',(xL+xR)/2,y-66,{c:GN,b:1,s:12})}});
 txt('만난 파면 수:  관찰자 1 = '+T1.c1+'개,   관찰자 2 = '+T1.c2+'개   (같은 시간 동안)',W/2,415,{b:1,s:16});
 txt('관찰자 2가 측정하는 소리의 속력 = v + v_o = '+f1(VS)+' + '+f1(T1.r*VS)+' = '+f1(VS*(1+T1.r))+' m/s  →  f′ = f(v+v_o)/v = '+(1+T1.r).toFixed(2)+'f',W/2,442,{s:14,c:PU,b:1});
 $('step').innerHTML='두 줄의 <b>파면 간격(파장)은 똑같습니다.</b> 그런데 파원 쪽으로 다가가는 관찰자 2는 파면을 마중 나가므로 같은 시간 동안 <b>더 많은 파면</b>을 만납니다. → 진동수가 커집니다. (위 버튼으로 두 관찰자의 소리를 비교해 보세요.)';
 if(snd1mode!=='off'&&Siren.active){
  Siren.update(snd1mode==='ref'?1.0:(1+T1.r), 0.13, 0, 480);
 }
}
function setSnd1(mode){
 snd1mode=(snd1mode===mode)?'off':mode;
 if(snd1mode==='off')Siren.stop();
 else Siren.start('ambulance', 480, snd1mode==='ref'?1.0:(1+T1.r), 0.13, 0);
 syncSndButtons();
}
$('r1').oninput=e=>{T1.r=+e.target.value;$('v1').textContent=f1(T1.r*VS)+' m/s';T1.c1=0;T1.c2=0;T1.x2=930;T1.prev1=null;T1.prev2=null;T1.t0=T1.t};
$('cnt1').onclick=()=>{T1.c1=0;T1.c2=0;T1.x2=930;T1.prev1=null;T1.prev2=null;T1.t0=T1.t};
$('snd1_ref').onclick=()=>setSnd1('ref');
$('snd1_mov').onclick=()=>setSnd1('mov');
$('snd1_off').onclick=()=>{snd1mode='off';Siren.stop();syncSndButtons()};

// =========================================================================
// TAB 3 : 4가지 경우 비교·관계식
// =========================================================================
const T2={t:0,s:0.3,o:0,xs:0,xo:0,em:[],last:0,hits:[],c:0};
let snd2mode='off';
function reset2(){T2.t=0;T2.xs=200;T2.xo=820;T2.em=[];T2.last=-1;T2.hits=[]}
function scene2(dt){
 const vs=T2.s*LV,vo=T2.o*LV;
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
 const xs_=T2.em.map(e=>e.x+LV*(T2.t-e.t)).filter(x=>x<=T2.xo).sort((a,b)=>a-b);
 if(xs_.length>=2){const a=xs_[xs_.length-2],b=xs_[xs_.length-1];dbl(a,y-84,b,y-84,GN);txt('파장',(a+b)/2,y-96,{c:GN,b:1,s:12})}
 const v=VS,vsr=T2.s*VS,vor=T2.o*VS,lamR=(1-T2.s),vrel=(1+T2.o),fr=vrel/lamR;
 const sg=x=>x>0?'커짐':(x<0?'작아짐':'그대로');
 const rows=[['관찰자가 측정하는 소리의 속력',f1(v+vor)+' m/s',sg(T2.o)],['파장 (정지일 때 1.00λ)',lamR.toFixed(2)+'λ',T2.s>0?'짧아짐':(T2.s<0?'길어짐':'그대로')],['진동수 (f = 480 Hz)',f1(480*fr)+' Hz',sg(fr-1>1e-9?1:(fr-1<-1e-9?-1:0))]];
 rows.forEach((r,i)=>{const yy=318+i*30;ctx.fillStyle=i%2?'#f8fafc':'#fff';ctx.fillRect(60,yy-14,880,28);txt(r[0],80,yy,{a:'left',s:14,b:1});txt(r[1],620,yy,{s:15,b:1,c:BL});txt(r[2],820,yy,{s:15,b:1,c:r[2]==='그대로'?SUB:(r[2]==='커짐'?GN:OR)})});
 txt("f′ = f (v ± v_o) / (v ∓ v_s) = 480 × ("+f1(v)+(vor>=0?' + ':' − ')+f1(Math.abs(vor))+") / ("+f1(v)+(vsr>=0?' − ':' + ')+f1(Math.abs(vsr))+") = "+f1(480*fr)+' Hz',W/2,420,{b:1,s:15});
 let msg='슬라이더는 <b>다가가는 쪽이 +</b>입니다. ';
 if(Math.abs(T2.s-(-T2.o))<1e-9&&T2.s!==0)msg+='<b>파원과 관찰자가 같은 속도로 함께 움직입니다.</b> 파장은 달라지지만 관찰자가 측정하는 속력도 같은 비율로 달라져 <b>진동수는 그대로</b>입니다(상대적인 운동이 없음).';
 else if(T2.s!==0&&T2.o!==0)msg+='파원과 관찰자가 <b>모두 움직이므로</b> 분모(파원)와 분자(관찰자)를 함께 넣어 계산합니다.';
 else if(T2.s!==0)msg+='파원이 움직이면 <b>파장</b>이 달라지고, 관찰자가 측정하는 소리의 속력은 그대로입니다.';
 else if(T2.o!==0)msg+='관찰자가 움직이면 파장은 그대로이고 <b>관찰자가 측정하는 소리의 속력</b>이 달라집니다.';
 else msg+='둘 다 정지하면 도플러 효과가 없습니다.';
 $('step').innerHTML=msg;
 if(snd2mode!=='off'&&Siren.active){
  Siren.update(snd2mode==='ref'?1.0:fr, 0.13, 0, 480);
 }
}
function setSnd2(mode){
 snd2mode=(snd2mode===mode)?'off':mode;
 if(snd2mode==='off')Siren.stop();
 else{const fr=(1+T2.o)/(1-T2.s); Siren.start('ambulance', 480, snd2mode==='ref'?1.0:fr, 0.13, 0);}
 syncSndButtons();
}
function set2(s,o){T2.s=s;T2.o=o;$('rs2').value=s;$('ro2').value=o;sync2();reset2()}
function sync2(){$('vs2').textContent=(T2.s>0?'다가감 ':T2.s<0?'멀어짐 ':'')+f1(Math.abs(T2.s*VS))+' m/s';$('vo2').textContent=(T2.o>0?'다가감 ':T2.o<0?'멀어짐 ':'')+f1(Math.abs(T2.o*VS))+' m/s'}
$('rs2').oninput=e=>{T2.s=+e.target.value;sync2();reset2()};$('ro2').oninput=e=>{T2.o=+e.target.value;sync2();reset2()};
document.querySelectorAll('[data-case]').forEach(b=>b.onclick=()=>{const c=+b.dataset.case;[[0.3,0],[-0.3,0],[0,0.3],[0,-0.3],[0.3,-0.3]].forEach((q,i)=>{if(i===c)set2(q[0],q[1])});document.querySelectorAll('[data-case]').forEach(x=>x.classList.toggle('on',x===b))});
$('snd2_ref').onclick=()=>setSnd2('ref');
$('snd2_obs').onclick=()=>setSnd2('obs');
$('snd2_off').onclick=()=>{snd2mode='off';Siren.stop();syncSndButtons()};

// =========================================================================
// TAB 4 : 구급차의 속력 측정 (실제 사이렌 + 거리 음량 + 좌우 스테레오 패닝)
// =========================================================================
const T3={t:0,run:false,hist:[],snd:false,sndRef:false};
function scene3(dt){
 const vsr=+$('r3').value,f=+$('f3').value;const road=145,obsX=500,obsY=road+72;
 const pxm=6;
 if(T3.run&&!paused){T3.t+=dt*1.0;if(T3.t*vsr*pxm>W+120){T3.run=false}}
 clear();
 // 도로 & 구급차
 ctx.fillStyle='#e5e7eb';ctx.fillRect(0,road-28,W,56);ln(0,road,W,road,'#fff',2,[18,14]);
 const xa=-80+T3.t*vsr*pxm;
 ctx.fillStyle='#fff';ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.beginPath();ctx.roundRect(xa-44,road-24,88,36,6);ctx.fill();ctx.stroke();
 ctx.fillStyle='#dbeafe';ctx.fillRect(xa+22,road-20,18,15);
 ctx.fillStyle=RD;ctx.fillRect(xa-10,road-20,10,24);ctx.fillRect(xa-17,road-13,24,10);
 dot(xa-25,road+14,8,INK);dot(xa+25,road+14,8,INK);
 ctx.fillStyle=Math.floor(performance.now()/180)%2?RD:BL;ctx.fillRect(xa-10,road-32,20,8);
 person(obsX,obsY,INK);txt('관찰자',obsX,obsY+16,{s:12,b:1});

 // 도플러 계산 + 거리 감쇠 + 스테레오 패닝
 const dx=(obsX-xa)/pxm, dy=11.0;
 const dist=Math.hypot(dx,dy);
 const cos=dx/dist;
 const ratio=T3.t>0||T3.run ? VS/(VS-vsr*cos) : 1.0;
 const fo=f*ratio;
 if(T3.run&&!paused)T3.hist.push([T3.t,fo]);

 if(T3.snd&&Siren.active){
  const vol=Math.max(0.025, Math.min(0.24, 0.24*(12/Math.max(12,dist*0.55))));
  const pan=Math.max(-0.9, Math.min(0.9, (xa-obsX)/420));
  Siren.update(ratio, T3.run?vol:0.06, pan, f);
 }else if(T3.sndRef&&Siren.active){
  Siren.update(1.0, 0.14, 0, f);
 }

 // 실시간 상태 배지
 const phaseTxt=xa<obsX-20?'◀ 다가오는 중 (높은 소리)':(xa>obsX+20?'멀어지는 중 (낮은 소리) ▶':'★ 관찰자 정면 통과 순간 (원래 진동수)');
 const phaseCol=xa<obsX-20?GN:(xa>obsX+20?OR:BL);
 txt(phaseTxt+'  ·  현재 측정 f′ = '+f1(fo)+' Hz', W/2, 56, {s:15,b:1,c:phaseCol});

 // f'-t 그래프
 const gx0=90,gx1=940,gy0=260,gy1=430,tmax=(W+200)/(vsr*pxm),fmin=f*VS/(VS+65)-10,fmax=f*VS/(VS-65)+10;
 ln(gx0,gy1,gx1,gy1,INK,1.5);ln(gx0,gy0,gx0,gy1,INK,1.5);txt('시간 (s)',gx1,gy1+15,{s:12,a:'right'});txt('측정 진동수 f′ (Hz)',gx0+6,gy0-10,{s:12,a:'left',b:1});
 const Y=v=>gy1-(v-fmin)/(fmax-fmin)*(gy1-gy0);
 ln(gx0,Y(f),gx1,Y(f),'#94a3b8',1.2,[4,4]);txt(f+' Hz (원래)',gx0-6,Y(f),{s:11,a:'right',c:SUB,b:1});
 ctx.beginPath();ctx.strokeStyle=PU;ctx.lineWidth=2.8;
 T3.hist.forEach((p,i)=>{const x=gx0+p[0]/tmax*(gx1-gx0),y=Y(p[1]);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});
 ctx.stroke();
 if(T3.hist.length>0){
  const lp=T3.hist[T3.hist.length-1];
  dot(gx0+lp[0]/tmax*(gx1-gx0), Y(lp[1]), 5.5, RD);
 }
 const fa=f*VS/(VS-vsr),fb=f*VS/(VS+vsr);
 txt('다가올 때 '+f1(fa)+' Hz',gx0+160,Y(fa)-13,{s:13,b:1,c:GN});
 txt('멀어질 때 '+f1(fb)+' Hz',gx1-150,Y(fb)+16,{s:13,b:1,c:OR});
 $('step').innerHTML='<b>측정값으로 속력 구하기</b> · 다가올 때 측정한 진동수 '+f1(fa)+' Hz를 식에 넣으면  '+f1(fa)+' = '+f+' × 340 / (340 − v<sub>s</sub>)  →  <b>v<sub>s</sub> = '+f1(VS-f*VS/fa,1)+' m/s</b> (약 '+f1((VS-f*VS/fa)*3.6)+' km/h). <br>🎧 <b>통과 소리 켜기</b>를 누르고 구급차를 출발시키면 왼쪽→오른쪽 스테레오 음량 변화와 함께 지나가는 순간 음높이가 뚝 떨어지는 실제 도플러 효과를 들을 수 있습니다.';
}
$('go3').onclick=()=>{unpause();T3.t=0;T3.hist=[];T3.run=true; if(T3.sndRef){T3.sndRef=false;T3.snd=true;Siren.start($('siren3').value, +$('f3').value, 1.0, 0.14, -0.8);syncSndButtons()}};
$('snd3').onclick=()=>{
 T3.snd=!T3.snd; T3.sndRef=false;
 if(T3.snd)Siren.start($('siren3').value, +$('f3').value, 1.0, 0.14, 0);
 else Siren.stop();
 syncSndButtons();
};
$('snd3_ref').onclick=()=>{
 T3.sndRef=!T3.sndRef; T3.snd=false;
 if(T3.sndRef)Siren.start($('siren3').value, +$('f3').value, 1.0, 0.14, 0);
 else Siren.stop();
 syncSndButtons();
};
$('siren3').onchange=()=>{
 if(T3.snd)Siren.start($('siren3').value, +$('f3').value, 1.0, 0.14, 0);
 else if(T3.sndRef)Siren.start($('siren3').value, +$('f3').value, 1.0, 0.14, 0);
};
$('r3').oninput=()=>{$('v3').textContent=$('r3').value+' m/s'};$('f3').oninput=()=>{$('vf3').textContent=$('f3').value+' Hz'};

// =========================================================================
// TAB 5 : 스피드건 & 별빛의 청색/적색 편이
// =========================================================================
const T4={t:0,mode:0,r:30,em:[],ref:[],last:-1,cx:820,step:1};
const G4={c:230,P:0.45,gx:110};
function step4(d){const c=G4.c,P=G4.P,gx=G4.gx,vc=(0.06+T4.r/60*0.24)*c;
 T4.t+=d;T4.cx-=vc*d;if(T4.cx<470){T4.cx=820;T4.em=[];T4.ref=[];T4.last=Math.floor(T4.t/P);warm4(false)}
 const n=Math.floor(T4.t/P);if(n>T4.last){T4.last=n;T4.em.push({t:T4.t})}
 const carF=T4.cx-45;
 T4.em.forEach(e=>{const x=gx+c*(T4.t-e.t);if(!e.r&&x>=carF){e.r=1;e.hitT=T4.t;T4.ref.push({t:T4.t,x:carF})}});
 T4.em=T4.em.filter(e=>!e.r||T4.t-e.hitT<0.25);T4.ref=T4.ref.filter(e=>e.x-c*(T4.t-e.t)>gx)}
function warm4(full){for(let i=0;i<140;i++)step4(0.025);T4.cx=Math.max(T4.cx,560)}
function scene4(dt){
 if(!paused&&T4.mode===1)T4.t+=dt*0.9;clear();
 if(T4.mode===0){
  const y=190,gx=110,c=G4.c,P=G4.P,st=T4.step;
  if(!paused)step4(dt*0.9);
  const carF=T4.cx-45;
  const showE=(st!==2),showR=(st!==1);
  T4.em.forEach(e=>{if(e.r){if(st===1)dot(carF,y-45,8,'rgba(37,99,235,'+(1-(T4.t-e.hitT)/0.25)+')');return}const x=gx+c*(T4.t-e.t);ln(x,y-75,x,y-15,showE?BL:'#dbeafe',showE?2.4:1.2)});
  T4.ref.forEach(e=>{const x=e.x-c*(T4.t-e.t);ln(x,y+15,x,y+75,showR?PU:'#ede9fe',showR?2.4:1.2)});
  if(showE){const xs=T4.em.filter(e=>!e.r).map(e=>gx+c*(T4.t-e.t)).sort((p,q)=>p-q);if(xs.length>=3){dbl(xs[0],y-88,xs[1],y-88,BL);txt('파장 λ (그대로)',(xs[0]+xs[1])/2,y-100,{c:BL,b:1,s:12})}}
  if(showR){const xs=T4.ref.map(e=>e.x-c*(T4.t-e.t)).sort((p,q)=>p-q);if(xs.length>=3){dbl(xs[0],y+88,xs[1],y+88,PU);txt('파장 λ′ (짧아짐)',(xs[0]+xs[1])/2,y+101,{c:PU,b:1,s:12})}}
  person(gx-50,y+40);ctx.fillStyle='#334155';ctx.fillRect(gx-44,y-8,34,12);txt('스피드건',gx-45,y+62,{s:12,b:1});
  ctx.fillStyle='#93c5fd';ctx.strokeStyle=INK;ctx.lineWidth=2;ctx.fillRect(carF,y-20,110,36);ctx.strokeRect(carF,y-20,110,36);dot(carF+25,y+18,9,INK);dot(carF+85,y+18,9,INK);
  arr(carF+55,y-30,carF+55-28,y-30,RD,2);txt('v',carF+64,y-30,{c:RD,b:1,s:13,a:'left'});
  function badge(x,yy,t1,col){ctx.font='700 13px "Malgun Gothic",sans-serif';const w=ctx.measureText(t1).width+18;ctx.fillStyle=col;ctx.beginPath();ctx.roundRect(x-w/2,yy-13,w,26,13);ctx.fill();txt(t1,x,yy,{c:'#fff',b:1,s:13})}
  if(st===1){badge(gx-45,y-62,'파원 (정지)',BL);badge(carF+55,y-62,'관찰자 (다가감)',OR)}
  else if(st===2){badge(gx-45,y-62,'관찰자 (정지)',OR);badge(carF+55,y-62,'파원 (다가옴)',PU)}
  else{badge(gx-45,y-62,'파원 → 관찰자',INK);badge(carF+55,y-62,'관찰자 → 파원',INK)}
  const vr=T4.r, f=24.15e9, C=3e8, df=2*vr*f/C;
  const lines={1:['1단계 · 자동차가 "관찰자"입니다.','스피드건(파원)은 가만히 있고 자동차(관찰자)가 다가가므로, 파장은 그대로인데 자동차가 1초 동안 만나는 파면 수가 늘어납니다.','자동차가 받는 진동수   f₁ = f · (c + v) / c          ← 학습지 C: 관찰자가 다가갈 때'],
              2:['2단계 · 이번에는 자동차가 "파원"입니다.','자동차는 받은 진동수 f₁ 그대로 전자기파를 되돌려 보냅니다. 다가오는 파원이므로 앞쪽(스피드건 쪽) 파장이 짧아집니다.','스피드건이 받는 진동수   f′ = f₁ · c / (c − v)          ← 학습지 B: 파원이 다가올 때'],
              3:['3단계 · 두 번의 도플러 효과를 합칩니다.','f′ = f · (c + v)/c × c/(c − v) = f · (c + v)/(c − v)   ≈  f (1 + 2v/c)     →   Δf = f′ − f ≈ 2vf/c ,   v ≈ cΔf / (2f)','실제 값: f = 24.15 GHz, v = '+vr+' m/s → Δf ≈ '+f1(df)+' Hz   (Δf / f ≈ '+(df/f*1e7).toFixed(1)+' × 10⁻⁷)']}[st];
  txt(lines[0],60,330,{a:'left',b:1,s:16,c:st===1?OR:(st===2?PU:INK)});
  txt(lines[1],60,362,{a:'left',s:13.5});
  txt(lines[2],60,394,{a:'left',b:1,s:14.5,c:BL});
  txt('※ 그림은 차이가 보이도록 자동차 속력을 매우 크게 과장했습니다. 실제 자동차 속력은 빛의 속력의 약 1000만분의 1입니다.',60,432,{a:'left',s:12,c:SUB});
  $('step').innerHTML={1:'<b>1단계</b> · 스피드건이 쏜 전자기파를 <b>받는 쪽은 자동차</b>입니다. 그래서 이 단계에서 움직이는 <b>관찰자는 자동차</b>이고, 분자가 c + v가 됩니다.',
   2:'<b>2단계</b> · 반사파를 <b>내보내는 쪽은 자동차</b>입니다. 이 단계에서는 자동차가 <b>움직이는 파원</b>이 되어 분모가 c − v가 됩니다.',
   3:'<b>3단계</b> · 스피드건을 든 사람은 두 단계 모두 <b>정지</b>해 있습니다. 자동차가 1단계에서는 관찰자, 2단계에서는 파원 역할을 하므로 도플러 효과가 <b>두 번</b> 일어납니다.'}[st];
 }else{
  const cx=240,cy=185,R=110,w=0.5,th=T4.t*w;const sx=cx+R*Math.cos(th),sy=cy-R*Math.sin(th);
  ctx.beginPath();ctx.setLineDash([5,5]);ctx.strokeStyle='#94a3b8';ctx.arc(cx,cy,R,0,7);ctx.stroke();ctx.setLineDash([]);dot(cx,cy,3,INK);txt('O',cx+12,cy,{s:12,b:1,c:SUB});
  [['A',cx+R+18,cy],['B',cx,cy-R-16],['C',cx-R-18,cy],['D',cx,cy+R+16]].forEach(p=>txt(p[0],p[1],p[2],{s:13,b:1,c:INK}));
  const vx=-Math.sin(th),vy=-Math.cos(th);
  arr(sx,sy,sx+vx*34,sy+vy*34,RD,2.2);
  const vrad=Math.cos(th)*-1;
  const col=vrad>0.15?'#60a5fa':(vrad<-0.15?'#f87171':'#fde047');dot(sx,sy,14,col);
  dot(cx,405,18,'#93c5fd');txt('지구 (관측)',cx+34,405,{s:13,b:1,a:'left'});ln(cx,387,cx,cy+R+24,'#cbd5e1',1,[3,4]);

  const x0=450,x1=950,sw=x1-x0,yRef=105,yObs=235,bh=48;
  const grd=ctx.createLinearGradient(x0,0,x1,0);
  ['#7c3aed','#2563eb','#06b6d4','#22c55e','#eab308','#f97316','#dc2626'].forEach((c,i)=>grd.addColorStop(i/6,c));

  txt('① 기준 스펙트럼 (실험실 정지 광원의 고유 흡수선 무늬)',x0,yRef-18,{s:13.5,b:1,a:'left',c:INK});
  ctx.fillStyle=grd;ctx.fillRect(x0,yRef,sw,bh);ctx.strokeStyle='#334155';ctx.lineWidth=1.5;ctx.strokeRect(x0,yRef,sw,bh);
  txt('② 지구에서 관측한 별빛 스펙트럼 (선 스펙트럼 전체가 함께 이동!)',x0,yObs-18,{s:13.5,b:1,a:'left',c:vrad>0.15?BL:(vrad<-0.15?RD:INK)});
  ctx.fillStyle=grd;ctx.fillRect(x0,yObs,sw,bh);ctx.strokeStyle='#334155';ctx.lineWidth=1.5;ctx.strokeRect(x0,yObs,sw,bh);

  const lines=[{p:0.16,w:2.5,lab:'Hδ'},{p:0.27,w:3.2,lab:'Hγ'},{p:0.44,w:4.0,lab:'Hβ'},{p:0.64,w:2.8,lab:'Na'},{p:0.81,w:4.5,lab:'Hα'}];
  const shift=-vrad*42, aCol=vrad>0.15?BL:(vrad<-0.15?RD:'#64748b');
  lines.forEach(L=>{
   const xr=x0+L.p*sw, xo=xr+shift;
   ctx.fillStyle='#0f172a';ctx.fillRect(xr-L.w/2,yRef,L.w,bh);txt(L.lab,xr,yRef+bh+13,{s:11,c:SUB,b:1});
   ctx.fillStyle='#0f172a';ctx.fillRect(xo-L.w/2,yObs,L.w,bh);
   ln(xr,yRef+bh+24,xo,yObs-28,aCol,1.8,[3,3]);head(xo,yObs-28,xo-xr,(yObs-28)-(yRef+bh+24),aCol,7);
  });
  txt('◀ 짧은 파장 (청색·보라)',x0,yObs+bh+20,{s:12.5,b:1,a:'left',c:BL});
  txt('긴 파장 (적색) ▶',x1,yObs+bh+20,{s:12.5,b:1,a:'right',c:RD});
  const lab=vrad>0.15?'◀ 청색 편이: 별이 다가올 때 모든 흡수선이 일제히 짧은 파장(청색) 쪽으로 이동'
           :(vrad<-0.15?'적색 편이 ▶: 별이 멀어질 때 모든 흡수선이 일제히 긴 파장(적색) 쪽으로 이동'
                       :'편이 없음: 시선 방향과 수직으로 운동할 때는 기준 스펙트럼 위치와 일치');
  txt(lab,(x0+x1)/2,yObs+bh+56,{s:15,b:1,c:vrad>0.15?BL:(vrad<-0.15?RD:SUB)});
  $('step').innerHTML='별빛 스펙트럼의 검은 선들은 별의 대기가 흡수한 원소 고유의 <b>흡수선 묶음</b>입니다. 별이 지구로 다가올 때(C)는 <b>모든 흡수선이 함께 짧은 파장 쪽(청색 편이)</b>으로, 멀어질 때(A)는 <b>모든 흡수선이 함께 긴 파장 쪽(적색 편이)</b>으로 이동합니다.';
 }
}
$('m4a').onclick=()=>{T4.mode=0;$('m4a').classList.add('on');$('m4b').classList.remove('on');$('g4').style.display='flex';$('g4star').style.display='none'};
document.querySelectorAll('[data-st]').forEach(b=>b.onclick=()=>{T4.step=+b.dataset.st;document.querySelectorAll('[data-st]').forEach(x=>x.classList.toggle('on',x===b));T4.cx=820;T4.em=[];T4.ref=[];T4.last=Math.floor(T4.t/G4.P);warm4(true)});
$('m4b').onclick=()=>{T4.mode=1;$('m4b').classList.add('on');$('m4a').classList.remove('on');$('g4').style.display='none';$('g4star').style.display='flex'};
document.querySelectorAll('[data-sth]').forEach(b=>b.onclick=()=>{T4.t=(+b.dataset.sth)/0.5;paused=true;$('pp').textContent='▶ 재생';document.querySelectorAll('[data-sth]').forEach(x=>x.classList.toggle('on',x===b));$('starPlay').classList.remove('on')});
$('starPlay').onclick=()=>{paused=false;$('pp').textContent='⏸ 일시정지';document.querySelectorAll('[data-sth]').forEach(x=>x.classList.remove('on'));$('starPlay').classList.add('on')};
$('r4').oninput=e=>{T4.r=+e.target.value;$('v4').textContent=T4.r+' m/s'};

// ---------- button state sync / tabs / loop
function syncSndButtons(){
 $('snd0_ref').classList.toggle('on', snd0mode==='ref');
 $('snd0_a').classList.toggle('on-gn', snd0mode==='a');
 $('snd0_b').classList.toggle('on-or', snd0mode==='b');
 $('snd1_ref').classList.toggle('on', snd1mode==='ref');
 $('snd1_mov').classList.toggle('on', snd1mode==='mov');
 $('snd2_ref').classList.toggle('on', snd2mode==='ref');
 $('snd2_obs').classList.toggle('on', snd2mode==='obs');
 $('snd3').classList.toggle('on', T3.snd);
 $('snd3').textContent=T3.snd?'🔇 통과 소리 끄기':'🔊 통과 소리 켜기';
 $('snd3_ref').classList.toggle('on', T3.sndRef);
 $('splay').textContent=InstAudio.playing?'🔇 소리 끄기':'🔊 소리 재생';
 $('splay').classList.toggle('on', InstAudio.playing);
}
function reset(){
 T0.t=0;T0.target=0;T0.auto=false;$('auto').classList.remove('on');
 T1.t=0;T1.x2=0;T1.c1=0;T1.c2=0;T1.prev1=null;T1.prev2=null;T1.t0=0;
 reset2();T3.t=0;T3.hist=[];T3.run=(tab===4);T4.t=0;T4.cx=820;T4.em=[];T4.ref=[];T4.last=-1;warm4(true);
}
function go(i){
 stopAllAudio();
 unpause();
 tab=i;
 [...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));
 for(let k=0;k<TABS.length;k++)$('c'+k).classList.toggle('show',k===i);
 $('note').innerHTML='<span class="ws">학습지 '+TABS[i][1]+'</span>'+TABS[i][2];
 reset();
}
function frame(now){
 requestAnimationFrame(frame);
 const dt=Math.max(0,Math.min(0.05,(now-last)/1000))*speed; last=now;
 try{[sceneSound,scene0,scene1,scene2,scene3,scene4][tab](paused?0:dt);}catch(e){console.error(e);}
}
$('v0').textContent=f1(0.3*VS)+' m/s';$('v1').textContent=f1(0.5*VS)+' m/s';sync2();$('v3').textContent='20 m/s';$('vf3').textContent='480 Hz';$('v4').textContent='30 m/s';
go(0);requestAnimationFrame(frame);
</script></body></html>
"""


if __name__ == "__main__":
    run_sim()
