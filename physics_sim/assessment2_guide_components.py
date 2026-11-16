import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """수행평가 2 안내(탄성파와 소리) — 평가 방법 안내 + 실험 절차 연습 + 2차시 개념 준비. 평가 문항의 답은 포함하지 않는다.
    반 이름·일정은 HTML 안의 CLASSES 배열에서 수정한다.
    """
    st.title("🚗 수행평가 2 안내")
    components.html(HTML, height=950, scrolling=True)


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
</style><style>
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:8px 0}
.pc{border:1px solid #e2e8f0;border-radius:12px;padding:12px;background:#fff}
.pc h3{margin:0 0 6px;font-size:15px}.pc .pt{float:right;font-weight:800;color:#1d4ed8}
.pc ul{margin:4px 0 0 16px;padding:0;font-size:13px;line-height:1.55}
table.sch{border-collapse:collapse;width:100%;font-size:13.5px;margin:6px 0}
table.sch td,table.sch th{border:1px solid #e2e8f0;padding:6px 8px;text-align:left}
table.sch th{background:#f1f5f9}
.warn{background:#fff7ed;border:1px solid #fed7aa;border-radius:10px;padding:10px 12px;font-size:13.5px;line-height:1.6;margin:8px 0}
.chk label{display:block;padding:6px 4px;font-size:14px;border-bottom:1px dashed #e2e8f0}
.pane{display:none}.pane.show{display:block}
.q{background:#eef2ff;border-radius:10px;padding:10px 12px;font-size:14px;line-height:1.6;margin:8px 0}
</style></head><body><div id="app">
<h1>🚗 수행평가 2 안내 · 미래형 모빌리티 음향 탐구</h1>
<p class="lead">수행평가 전에 평가 방법을 확인하고, 실험 절차와 개념을 미리 연습하는 화면입니다. 이 화면에는 평가 문항의 답이 없습니다. 측정과 계산은 평가 시간에 직접 합니다.</p>
<div class="tabs" id="tabs"></div>
<div class="ctrl speed" id="spd"><div class="grp">⏱ 재생 속도</div>
<button class="btn" data-sp="0.25">0.25×</button><button class="btn on" data-sp="0.5">0.5×</button><button class="btn" data-sp="1">1×</button><button class="btn primary" id="pp">⏸ 일시정지</button></div>

<div class="pane" id="p0">
 <div class="ctrl" id="cls"></div>
 <div class="card" style="padding:14px">
 <div class="q"><b>수행 과제</b> 자율주행 모빌리티 시나리오의 환경 조건을 분석하여 정상파 공명 데이터로 차내 음속을 정량 산출하고, 파면 압축 모델을 적용해 다가오는 긴급차량의 상대 속도를 도플러 효과로 역산하며, 차내 유입 소음을 위상 반전 및 상쇄 간섭 원리로 소멸시키는 능동 소음 제어(ANC) 시스템을 논리적으로 논증한다.</div>
 <table class="sch" id="schT"></table>
 <div class="cards">
  <div class="pc"><h3>① 차내 음속 구하기 <span class="pt">40점</span></h3><div style="font-size:12.5px;color:#64748b">1차시 · 실험 · 모둠별 · 모둠 보고서</div>
   <ul><li>관의 경계 조건(막힌 끝·열린 끝)과 공기 입자의 진동으로 공명 설명</li><li>스마트 기기로 진동수 확인, 정상파로 음속 산출(계산 과정의 비약 없이)</li><li>이론 음속과의 오차 원인(개구단 보정, 실내 온도 등)과 측정값에 미친 영향을 인과적으로 서술</li></ul></div>
  <div class="pc"><h3>② 긴급차량 속도 역산 <span class="pt">30점</span></h3><div style="font-size:12.5px;color:#64748b">2차시 · 서술형 · 개별</div>
   <ul><li>파원의 운동에 따른 파면 간격 변화로 관측 진동수 관계를 도출</li><li>측정 자료에 적용하여 속도를 정량적으로 산출</li><li>결과의 타당성 검토, 속도 측정 장치의 원리와 연결</li></ul></div>
  <div class="pc"><h3>③ ANC 원리 논증 <span class="pt">30점</span></h3><div style="font-size:12.5px;color:#64748b">2차시 · 서술형 · 개별</div>
   <ul><li>중첩과 간섭으로 상쇄 간섭 조건 설명</li><li>차내 소음 상황에 적용하여 소음이 줄어드는 과정을 인과적으로 논증</li><li>소음 제어 기술의 활용 사례와 한계를 과학적 근거로 판단</li></ul></div>
 </div>
 <div style="font-size:12.5px;color:#64748b;margin:-2px 0 6px">※ 위 내용은 평가 요소의 요약입니다. 채점은 평가계획서의 채점 기준 원문에 따릅니다. 평가 당일에는 연습한 것과 다른 상황·조건·자료가 제시됩니다.</div><div class="warn"><b>채점에서 특히 보는 점</b> (평가계획서 채점 기준에서)<br>
 · 계산은 <b>식 → 값 대입 → 결과·단위</b> 순서로 씁니다. 수식·단위가 빠지거나 개념 오류가 하나라도 있으면 최고 수준을 받을 수 없습니다.<br>
 · 계산이 맞아도 <b>관의 경계 조건</b>이나 <b>파원의 운동과 진동수 변화의 관계</b>에 핵심 오개념이 있으면 낮은 수준으로 판정합니다.<br>
 · 원인을 <b>나열</b>만 하지 말고, "무엇이 → 어떻게 → 그래서 측정값(소리)이 어떻게 되었는지"까지 <b>인과적으로</b> 씁니다.</div>
 <div class="warn"><b>유의 사항</b><br>
 · 계산기 사용 가능. 교과서, AI 도구 사용 불가. 2차시는 모둠 상의 불가.<br>
 · 모둠 실험은 공동 점수입니다. 다만 실험 활동에 참여하지 않으면 0점으로 판정합니다. 역할(음원·측정·기록·계산)을 미리 정하세요.<br>
 · 결시하면 추가 평가 기회가 1회 주어지며, 정당한 사유 없이 응하지 않으면 0점입니다.<br>
 · 채점 결과는 공개되며, 이의 신청 기간에 재채점을 요청할 수 있습니다.</div>
 </div>
</div>

<div class="pane" id="p1">
 <div class="ctrl">
  <div class="grp">진동수<input type="range" id="f1" min="800" max="1200" step="10" value="1000"><span class="val" id="vf1"></span></div>
  <div class="grp">필름 위 끝 높이 <i>L</i><input type="range" id="h1" min="0.320" max="0.620" step="0.001" value="0.620"><span class="val" id="vh1"></span></div>
  <button class="btn" id="rec">📌 이 높이 기록</button><button class="btn" id="clr">기록 지우기</button><button class="btn" id="snd">🔊 소리</button></div>
 <div class="card"><canvas id="cv1" width="1000" height="440"></canvas></div>
 <div class="step">① 필름을 가장 높이 올린 상태에서 시작합니다. ② 슬라이더를 <b>천천히 줄이며</b>(필름을 밀어 넣으며) 음량 막대가 가장 커지는 곳을 찾습니다. ③ 최대 지점 앞뒤로 조금씩 움직여 확인한 뒤 기록합니다. ④ 계속 밀어 넣어 다음 지점을 찾습니다.<br>
 ※ 연습용 가상 장치입니다. 실제 실린더와 온도가 달라 실제 측정값과 다릅니다. 파장·속력 계산은 평가 시간에 실제 측정값으로 직접 합니다.</div>
 <div class="q"><b>실험 전에 생각해 두기</b> · 필름 위 끝이 실린더 입구보다 아래로 내려가면 공기 기둥의 길이는 어떻게 될까? · 소리가 크게 들리는 두 지점은 몇 개나 찾을 수 있을까? 진동수를 바꾸면 어떻게 달라질까? · 측정할 때 높이는 어디서부터 어디까지 재야 할까?</div>
</div>

<div class="pane" id="p2">
 <div class="ctrl"><div class="grp">긴급차량 속력 (소리 속력에 대한 비)<input type="range" id="vs2" min="0" max="0.5" step="0.01" value="0.25"><span class="val" id="vvs2"></span></div><button class="btn" id="rs2">처음부터</button></div>
 <div class="card"><canvas id="cv2" width="1000" height="420"></canvas></div>
 <div class="step">긴급차량이 같은 시간 간격(한 주기)마다 파면을 하나씩 만듭니다. 속력을 0으로 했을 때와 비교해 보세요.</div>
 <div class="q"><b>2차시 준비 질문</b> (답은 평가 시간에 직접 서술)<br>· 앞쪽과 뒤쪽의 파면 간격은 각각 어떻게 달라지는가? 소리의 속력도 달라지는가?<br>· 속력 비를 0, 0.25, 0.5로 바꾸며 앞쪽과 뒤쪽 파면 간격이 어떻게 변하는지 관찰해 보자.<br>· 계산한 속력이 타당한지 확인할 수 있는 방법에는 어떤 것이 있을까?</div>
</div>

<div class="pane" id="p3">
 <div class="ctrl"><div class="grp">두 소리의 위상차<input type="range" id="ph3" min="0" max="360" step="5" value="0"><span class="val" id="vph3"></span></div>
  <div class="grp">스피커 소리의 진폭<input type="range" id="a3" min="0" max="1.2" step="0.05" value="1"><span class="val" id="va3"></span></div></div>
 <div class="card"><canvas id="cv3" width="1000" height="430"></canvas></div>
 <div class="step">위쪽은 소음, 가운데는 ANC 스피커 소리, 아래쪽은 두 소리가 중첩된 결과입니다. 위상차와 진폭을 바꾸며 합성파의 진폭이 어떻게 변하는지 관찰하세요.</div>
 <div class="q"><b>2차시 준비 질문</b><br>· 합성 진폭이 가장 작아지는 조건(위상차, 진폭)은 무엇인가?<br>· 위치가 달라져 한 소리가 더 먼 거리를 진행하면 위상차는 어떻게 되는가? 경로차가 파장의 몇 배일 때 상쇄·보강이 되는가?<br>· 위상차를 180°에서 조금씩 벗어나게 하거나 스피커 진폭을 바꾸면 합성 진폭은 어떻게 되는가? ANC 스피커의 소리가 정확해야 하는 까닭은 무엇일까?</div>
</div>

<div class="pane" id="p4"><div class="card" style="padding:14px">
 <h3 style="margin:4px 0 8px">제출 전 스스로 점검하기</h3>
 <div class="chk" id="chk"></div>
 <div class="step" id="cnt"></div></div></div>

<div class="note" id="note"></div>
</div>
<script>
/* ===== 교사 설정: 반 이름과 일정을 수정하세요 ===== */
const CLASSES=[
 {name:'2학년 (  )반', d1:'11월 (  )일 (  )교시', d2:'11월 (  )일 (  )교시', room:'물리실'},
 {name:'2학년 (  )반', d1:'11월 (  )일 (  )교시', d2:'11월 (  )일 (  )교시', room:'물리실'}];
const $=id=>document.getElementById(id),INK='#0f172a',SUB='#64748b',BL='#2563eb',RD='#e11d48',GN='#059669',PU='#7c3aed',OR='#ea580c';
const TABS=[['📋 수행평가 안내','평가 방법·배점·일정·유의 사항을 확인합니다.'],['🧪 1차시 실험 미리보기','교재 실험(눈금실린더 + 투명 필름)의 측정 절차를 가상으로 연습합니다.'],['🚑 2차시 준비 ① 도플러','파면 간격이 어떻게 바뀌는지 관찰합니다.'],['🎧 2차시 준비 ② ANC','두 소리의 중첩과 위상차를 관찰합니다.'],['✅ 제출 전 점검','제출 전에 스스로 점검합니다.']];
let tab=0,speed=0.5,paused=false,last=performance.now(),T=0,cls=0;
TABS.forEach((t,i)=>{const b=document.createElement('button');b.className='tab';b.textContent=t[0];b.onclick=()=>go(i);$('tabs').appendChild(b)});
document.querySelectorAll('[data-sp]').forEach(b=>b.onclick=()=>{speed=+b.dataset.sp;document.querySelectorAll('[data-sp]').forEach(x=>x.classList.toggle('on',x===b))});
$('pp').onclick=()=>{paused=!paused;$('pp').textContent=paused?'▶ 재생':'⏸ 일시정지'};
function sched(){$('cls').innerHTML=CLASSES.map((c,i)=>'<button class="btn'+(i===cls?' on':'')+'" onclick="cls='+i+';sched()">'+c.name+'</button>').join('');const c=CLASSES[cls];
 $('schT').innerHTML='<tr><th>차시</th><th>일시</th><th>평가</th><th>준비</th></tr><tr><td>1차시</td><td>'+c.d1+'<br>'+c.room+'</td><td>① 정상파 공명 실험 (모둠, 40점) — 측정 약 20분 + 보고서 작성</td><td>모둠 역할 분담, 스마트 기기 2대(소리 발생 앱, 음향 스펙트럼·음량 측정 앱), 계산기</td></tr><tr><td>2차시</td><td>'+c.d2+'</td><td>② 도플러 효과(30점) + ③ ANC(30점) — 개별 서술 45분</td><td>계산기, 필기구</td></tr>'}
function txt(s,x,y,o){o=o||{};const c=o.cv||ctx;c.font=(o.b?'700 ':'500 ')+(o.s||14)+'px "Malgun Gothic",sans-serif';c.fillStyle=o.c||INK;c.textAlign=o.a||'center';c.textBaseline='middle';c.fillText(s,x,y)}
let ctx;
function ln(x0,y0,x1,y1,c,w,d){ctx.beginPath();ctx.setLineDash(d||[]);ctx.strokeStyle=c;ctx.lineWidth=w||1;ctx.moveTo(x0,y0);ctx.lineTo(x1,y1);ctx.stroke();ctx.setLineDash([])}
function arr(x0,y0,x1,y1,c){ln(x0,y0,x1,y1,c,2.5);const a=Math.atan2(y1-y0,x1-x0);ctx.beginPath();ctx.fillStyle=c;ctx.moveTo(x1,y1);ctx.lineTo(x1-9*Math.cos(a-0.4),y1-9*Math.sin(a-0.4));ctx.lineTo(x1-9*Math.cos(a+0.4),y1-9*Math.sin(a+0.4));ctx.fill()}
// audio
let AC=null,osc=null,gn=null,sndOn=false;
function tone(f,g){if(!AC)AC=new (window.AudioContext||window.webkitAudioContext)();if(!osc){osc=AC.createOscillator();gn=AC.createGain();osc.type='sine';osc.connect(gn).connect(AC.destination);osc.start()}osc.frequency.setTargetAtTime(f,AC.currentTime,0.02);gn.gain.setTargetAtTime(g,AC.currentTime,0.04)}
function stop(){if(osc){osc.stop();osc=null}}
$('snd').onclick=()=>{sndOn=!sndOn;if(!sndOn)stop();$('snd').textContent=sndOn?'🔇 끄기':'🔊 소리'};
// ===== tab1: cylinder + film (hidden model)
const VSIM=346.5, RIM=0.32, ENDC=0.009, REC=[];
function amp1(){const f=+$('f1').value,L=+$('h1').value,lam=VSIM/f;const ph=2*Math.PI*(L+ENDC)/lam;return Math.abs(Math.sin(ph))**10}
function s1(){ctx=$('cv1').getContext('2d');ctx.clearRect(0,0,1000,440);const f=+$('f1').value,L=+$('h1').value;$('vf1').textContent=f+' Hz';$('vh1').textContent=L.toFixed(3)+' m';
 const x0=180,yb=400,sc=560,cw=70;
 ctx.fillStyle='#e2e8f0';ctx.beginPath();ctx.moveTo(x0-40,yb+10);ctx.lineTo(x0+cw+40,yb+10);ctx.lineTo(x0+cw+30,yb);ctx.lineTo(x0-30,yb);ctx.fill();
 ln(x0,yb,x0,yb-RIM*sc,INK,3);ln(x0+cw,yb,x0+cw,yb-RIM*sc,INK,3);ln(x0,yb,x0+cw,yb,INK,5);
 for(let k=1;k<=16;k++){const y=yb-k*0.02*sc;if(y<yb-RIM*sc)break;ln(x0+cw-14,y,x0+cw,y,SUB,1)}
 ctx.fillStyle='rgba(191,219,254,0.75)';ctx.strokeStyle=BL;ctx.lineWidth=2;const fl=0.30;ctx.fillRect(x0+6,yb-L*sc,cw-12,fl*sc);ctx.strokeRect(x0+6,yb-L*sc,cw-12,fl*sc);
 ctx.fillStyle='#334155';ctx.fillRect(x0+4,yb-L*sc-26,cw-8,16);txt('스마트폰',x0+cw+12,yb-L*sc-18,{a:'left',s:12});
 // ruler
 const rx=x0+cw+70;ln(rx,yb,rx,yb-0.64*sc,INK,1.5);for(let k=0;k<=64;k++){const y=yb-k*0.01*sc;ln(rx,y,rx+(k%10?6:14),y,INK,1);if(k%10===0)txt((k)+' cm',rx+20,y,{a:'left',s:11,c:SUB})}
 ln(x0+cw+6,yb-L*sc,rx,yb-L*sc,RD,1.2,[4,3]);txt('필름 위 끝',rx-8,yb-L*sc+12,{a:'right',s:11,c:RD});
 const a=amp1(),mx=470,my=70;txt('음량 (기기 B)',mx,my-22,{a:'left',b:1,s:14});ctx.fillStyle='#e2e8f0';ctx.fillRect(mx,my,360,28);ctx.fillStyle=a>0.8?GN:(a>0.3?OR:'#94a3b8');ctx.fillRect(mx,my,360*Math.max(0.03,a),28);
 txt('기록 (바닥에서 필름 위 끝까지 높이)',mx,150,{a:'left',b:1,s:14});
 REC.forEach((r,i)=>txt((i+1)+'번째 기록: '+r.toFixed(3)+' m',mx,182+i*26,{a:'left',s:14}));
 if(L<=RIM+0.0005)txt('※ 필름 위 끝이 실린더 입구에 닿았습니다. 더 밀어 넣으면 관의 길이가 실린더 높이로 고정됩니다.',mx,330,{a:'left',s:12.5,c:OR});
 if(sndOn&&tab===1)tone(f,0.015+0.1*a);}
$('rec').onclick=()=>{const L=+$('h1').value;if(REC.length<6)REC.push(L)};$('clr').onclick=()=>REC.length=0;
// ===== tab2: doppler wavefronts
let t2=5;$('rs2').onclick=()=>t2=5;
function s2(dt){ctx=$('cv2').getContext('2d');ctx.clearRect(0,0,1000,420);const r=+$('vs2').value;$('vvs2').textContent=r.toFixed(2)+' (속력 0 = 정지)';
 const c=80,Tp=1.0,yc=200;t2+=dt;const x0=330;const xs=t=>x0+r*c*t;if(xs(t2)>800)t2=5;
 ctx.fillStyle='#e2e8f0';ctx.fillRect(0,yc+18,1000,12);
 for(let n=0;n*Tp<=t2;n++){const te=n*Tp,R=c*(t2-te);if(R>700)continue;ctx.beginPath();ctx.strokeStyle='rgba(37,99,235,'+Math.max(0.2,1-R/700)+')';ctx.lineWidth=1.8;ctx.arc(xs(te),yc,R,0,7);ctx.stroke()}
 const X=xs(t2);ctx.fillStyle='#fecaca';ctx.fillRect(X-30,yc-2,60,20);ctx.strokeStyle=INK;ctx.strokeRect(X-30,yc-2,60,20);txt('긴급차량',X,yc-14,{s:12,b:1});if(r>0)arr(X+36,yc-30,X+80,yc-30,RD);
 ctx.fillStyle='#bfdbfe';ctx.fillRect(900,yc-2,60,20);ctx.strokeRect(900,yc-2,60,20);txt('앞쪽 관측자',930,yc-14,{s:12,b:1});
 ctx.fillStyle='#d1fae5';ctx.fillRect(40,yc-2,60,20);ctx.strokeRect(40,yc-2,60,20);txt('뒤쪽 관측자',70,yc-14,{s:12,b:1});}
// ===== tab3: ANC superposition
function s3(dt){ctx=$('cv3').getContext('2d');ctx.clearRect(0,0,1000,430);const ph=+$('ph3').value*Math.PI/180,A2=+$('a3').value;$('vph3').textContent=$('ph3').value+'°';$('va3').textContent=A2.toFixed(2)+' × 소음';
 const w=2*Math.PI*0.5,k=2*Math.PI/300,A=36;
 const fNoise=x=>A*Math.sin(k*x-w*T),fAnc=x=>A2*A*Math.sin(k*x-w*T+ph);
 const rows=[[70,'소음',fNoise,'#64748b'],[195,'ANC 스피커 소리',fAnc,RD],[340,'중첩 결과 (점선: 소음·스피커 소리, 실선: 합성파)',x=>fNoise(x)+fAnc(x),PU]];
 rows.forEach(r=>{ln(60,r[0],960,r[0],'#e2e8f0',1);txt(r[1],60,r[0]-50,{a:'left',b:1,s:13,c:r[3]});ctx.beginPath();ctx.strokeStyle=r[3];ctx.lineWidth=r[3]===PU?3.2:2;for(let x=60;x<=960;x+=2){const y=r[0]-r[2](x-60);x===60?ctx.moveTo(x,y):ctx.lineTo(x,y)}ctx.stroke()});
 // 중첩 결과 축에 두 개별 파동 점선 겹쳐 표시
 [[fNoise,'rgba(100,116,139,0.6)'],[fAnc,'rgba(225,29,72,0.6)']].forEach(q=>{
  ctx.beginPath();ctx.setLineDash([5,4]);ctx.strokeStyle=q[1];ctx.lineWidth=1.8;
  for(let x=60;x<=960;x+=2){const y=340-q[0](x-60);x===60?ctx.moveTo(x,y):ctx.lineTo(x,y)}
  ctx.stroke();ctx.setLineDash([]);
 });
 const amp=Math.sqrt(1+A2*A2+2*A2*Math.cos(ph));txt('합성 진폭 = 소음 진폭의 '+amp.toFixed(2)+'배',960,400,{a:'right',b:1,s:15,c:PU});}
// checklist
const CK=['[실험] 진동수(설정값·측정값)와 실내 온도를 기록했다.','[실험] 측정 높이를 3회 기록하고 평균을 구했다.','[실험] 관 양 끝이 배인지 마디인지와 그 까닭(공기 입자가 진동할 수 있는지)을 썼다.','[실험] 파장과 속력 계산에 식 → 값 대입 → 결과·단위를 모두 썼다.','[실험] 오차 원인과, 그 원인이 측정값을 크게(작게) 만든 까닭을 함께 썼다.','[서술] 파면 간격을 근거로 진동수 변화를 설명했다.','[서술] 관계식을 그림의 이동 거리로부터 이끌어 냈다.','[서술] 계산 결과가 타당한지 다른 방법이나 상식으로 확인했다.','[서술] 위상·상쇄 간섭·경로차 같은 물리 용어로 원인과 결과를 연결했다.','[서술] 기술의 활용 사례와 한계를 과학적 근거와 함께 썼다.'];
$('chk').innerHTML=CK.map((c,i)=>'<label><input type="checkbox" data-c="'+i+'"> '+c+'</label>').join('');
function cnt(){const n=document.querySelectorAll('[data-c]:checked').length;$('cnt').innerHTML='점검 '+n+' / '+CK.length}
document.querySelectorAll('[data-c]').forEach(b=>b.onchange=cnt);cnt();
function go(i){tab=i;[...$('tabs').children].forEach((b,k)=>b.classList.toggle('on',k===i));for(let k=0;k<5;k++)$('p'+k).classList.toggle('show',k===i);$('spd').style.display=(i===2||i===3)?'flex':'none';$('note').innerHTML=TABS[i][1];if(i!==1&&sndOn){sndOn=false;stop();$('snd').textContent='🔊 소리'}}
function frame(now){const dt=Math.min(0.05,(now-last)/1000)*speed;last=now;if(!paused)T+=dt;if(tab===1)s1();if(tab===2)s2(paused?0:dt);if(tab===3)s3(paused?0:dt);requestAnimationFrame(frame)}
sched();go(0);requestAnimationFrame(frame);
</script></body></html>"""


if __name__ == "__main__":
    run_sim()

