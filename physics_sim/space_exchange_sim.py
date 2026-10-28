import streamlit as st
import streamlit.components.v1 as components
import os

# ── 헤더 섹션 ──────────────────────────────────────────────────
st.title("💹 [융합] 우주 거래소의 시계")
st.markdown(
    "2045년 지구·우주 정거장·달 기지의 주민이 같은 주식을 주문할 때, "
    "**거리에 따른 시간 차**(신호 지연)와 **상대성에 따른 시간 차**(중력 효과·속도 효과)를 구별하고, "
    "시각을 환산해 공정한 체결 순서를 판단하는 가상 실험실"
)
st.caption("① 시계 맞추기 → ② 주문하기 → ③ 하루가 지나면 → ④ 체결 비교 · 활동지 연계")

# ── HTML 파일 로드 ──────────────────────────────────────────────
html_path = os.path.join(os.path.dirname(__file__), "space-exchange.html")

# 기본 HTML 코드 (space-exchange.html과 동일한 최신 버전 내장 fallback)
DEFAULT_HTML = r"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>우주 거래소의 시계</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=IBM+Plex+Mono:wght@500;600&display=swap">
<style>
/* Layout: 교실 프로젝션용. 상단 단계 탭(①~④) + 탭마다 '예측 → 관찰 → 설명' 흐름. 밝은 한 가지 테마(의도). */
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#1e3a5f; --text:#2b2f36; --muted:#6a7280; --line:#dfe3ea;
  --gold:#c9a96e; --earth:#2e8b7a; --station:#4e6bd6; --moon:#c97b2a;
  --ok:#2f8f5b; --ok-soft:#e3f3ea; --bad:#c0392b; --bad-soft:#fbeaea; --soft:#eef1f6;
  --f:"Noto Sans KR","Malgun Gothic","Apple SD Gothic Neo",sans-serif;
  --num:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  color-scheme:light;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:var(--f);font-size:16px;line-height:1.6}
.wrap{max-width:1200px;margin:0 auto;padding-inline:18px;padding-block:18px 40px;display:grid;gap:16px}
header{display:grid;gap:4px}
.eyebrow{font-size:.8rem;color:var(--muted);letter-spacing:.04em}
h1{margin:0;font-size:clamp(1.4rem,2.6vw,2rem);font-weight:800;color:var(--ink);letter-spacing:-.01em}
.iq{font-size:1rem;color:var(--ink)}
.iq b{background:linear-gradient(transparent 60%,#f1e4c8 60%)}
nav.tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;border-bottom:2px solid var(--line)}
nav.tabs button{font:inherit;cursor:pointer;background:none;border:0;border-bottom:3px solid transparent;margin-bottom:-2px;padding:10px 6px;text-align:left;color:var(--muted);display:grid;gap:0}
nav.tabs button .n{font-family:var(--num);font-size:.8rem}
nav.tabs button .t{font-weight:700;font-size:1.02rem}
nav.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:var(--gold)}
nav.tabs button:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--gold);outline-offset:2px}
section.tab{display:grid;gap:16px}
section.tab[hidden]{display:none!important}
.grid2{display:grid;grid-template-columns:minmax(0,3fr) minmax(0,2fr);gap:16px;align-items:start}
@media (max-width:900px){.grid2{grid-template-columns:minmax(0,1fr)}nav.tabs{grid-template-columns:repeat(2,minmax(0,1fr))}}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px;min-width:0;display:grid;gap:12px}
.card h3{margin:0;font-size:1.05rem;color:var(--ink)}
.step{display:grid;gap:8px;padding-left:14px;border-left:3px solid var(--line)}
.step.on{border-left-color:var(--gold)}
.step .lab{font-size:.78rem;font-weight:700;color:var(--muted);letter-spacing:.06em}
.step p{margin:0}
.choices{display:flex;gap:6px;flex-wrap:wrap}
button.btn{font:inherit;cursor:pointer;border:1px solid var(--line);background:#fff;color:var(--text);border-radius:8px;padding:7px 14px;font-size:.95rem}
button.btn:hover{border-color:var(--ink)}
button.btn.primary{background:var(--ink);color:#fff;border-color:var(--ink)}
button.btn.sel{background:var(--soft);border-color:var(--ink);font-weight:700}
button.btn:disabled{opacity:.45;cursor:default}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg button{font:inherit;border:0;background:#fff;padding:7px 14px;cursor:pointer;color:var(--muted)}
.seg button.on{background:var(--ink);color:#fff}
.reveal{background:var(--soft);border-radius:8px;padding:10px 12px}
.reveal[hidden]{display:none!important}
.reveal.good{background:var(--ok-soft)} .reveal.bad{background:var(--bad-soft)}
.note{font-size:.85rem;color:var(--muted);margin:0}
.num{font-family:var(--num);font-variant-numeric:tabular-nums}
svg{width:100%;height:auto;display:block}
svg text{font-family:var(--f)}
.clocks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
@media (max-width:620px){.clocks{grid-template-columns:minmax(0,1fr)}}
.clk{border-radius:10px;padding:10px 12px;background:var(--soft);display:grid;gap:2px;min-width:0}
.clk .who{font-weight:700;font-size:.92rem}
.clk .t{font-family:var(--num);font-size:1.15rem;font-weight:600;color:var(--ink)}
.clk .d{font-size:.86rem}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;min-width:560px;font-size:.95rem}
th,td{padding:7px 9px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
th{font-size:.8rem;color:var(--muted);font-weight:500}
td.r,th.r{text-align:right}
.who-dot{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;color:#fff;font-weight:700;font-size:.82rem;margin-right:6px}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:.8rem;font-weight:700}
.pill.ok{background:var(--ok-soft);color:var(--ok)} .pill.no{background:var(--soft);color:var(--muted)}
.pill.bad{background:var(--bad-soft);color:var(--bad)} .pill.gain{background:#fdf1e2;color:#a8641c}
.lists{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media (max-width:620px){.lists{grid-template-columns:minmax(0,1fr)}}
.olist{display:grid;gap:4px;margin:0;padding:0;list-style:none;counter-reset:o}
.olist li{display:flex;white-space:nowrap;align-items:center;gap:6px;padding:4px 8px;border-radius:6px;background:var(--soft);font-size:.92rem}
.olist li.win{background:var(--ok-soft)}
.olist li::before{counter-increment:o;content:counter(o);font-family:var(--num);font-size:.8rem;color:var(--muted);width:14px}
label.ctl{display:grid;gap:4px;font-weight:500}
.ctl-row{display:flex;justify-content:space-between;align-items:baseline;gap:8px;flex-wrap:wrap}
input[type=range]{width:100%;accent-color:var(--ink);height:26px}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
@media (max-width:760px){.two{grid-template-columns:minmax(0,1fr)}}
.bars{display:grid;gap:8px}
.bar{display:grid;grid-template-columns:96px minmax(0,1fr) 92px;align-items:center;gap:8px;font-size:.88rem}
.bar .track{position:relative;height:16px;background:var(--soft);border-radius:4px}
.bar .track .zero{position:absolute;left:50%;top:-3px;bottom:-3px;width:1px;background:var(--muted)}
.bar .fill{position:absolute;top:0;bottom:0;border-radius:3px;transition:all .4s ease}
.callout{border-left:4px solid var(--gold);background:#fbf7ef;padding:10px 14px;border-radius:0 8px 8px 0}
.callout b{color:var(--ink)}
.thumbs{font-size:1.05rem}
.flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
@media (max-width:760px){.flow{grid-template-columns:minmax(0,1fr)}}
.flow div{background:var(--soft);border-radius:10px;padding:10px 12px;font-size:.95rem}
.flow b.n{display:inline-grid;place-items:center;width:24px;height:24px;border-radius:50%;background:var(--ink);color:#fff;font-size:.85rem;margin-right:6px}
tr.cut td{border-bottom:3px solid var(--ok)}
.tag{display:inline-block;padding:0 7px;border-radius:5px;font-size:.78rem;font-weight:700;white-space:nowrap}
.tag.loc{background:#e9ebef;color:#555c68} .tag.earth{background:var(--ok-soft);color:var(--ok)}
td.calc{color:var(--muted)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>


</head>
<body style="margin:0">
<div class="wrap">
  <header>
    <div class="eyebrow">역학과 에너지 · 중력 시간 지연의 적용 × 경제금융 · 2045년 가상 상황</div>
    
    <div class="iq">탐구질문 <b>지구, 우주 정거장, 달의 시계는 하루 동안 얼마나, 왜 다르게 갈까?</b></div>
  </header>

  <nav class="tabs" role="tablist" aria-label="탐구 단계">
    <button role="tab" id="tb1" aria-selected="true" aria-controls="p1"><span class="n">① 활동 1</span><span class="t">시계 맞추기</span></button>
    <button role="tab" id="tb2" aria-selected="false" aria-controls="p2"><span class="n">② 활동 1</span><span class="t">주문하기</span></button>
    <button role="tab" id="tb3" aria-selected="false" aria-controls="p3"><span class="n">③ 활동 1~2</span><span class="t">하루가 지나면</span></button>
    <button role="tab" id="tb4" aria-selected="false" aria-controls="p4"><span class="n">④ 활동 3</span><span class="t">체결 비교</span></button>
  </nav>

  <!-- ① 시계 맞추기 -->
  <section class="tab" id="p1" role="tabpanel" aria-labelledby="tb1">
    <div class="grid2">
      <div class="card">
        <h3>거래소가 “오전 9시 정각” 신호를 보낸다</h3>
        <svg id="map1" viewBox="0 0 960 360" role="img" aria-label="지구, 우주 정거장, 달로 시각 신호가 전달되는 그림"></svg>
        <p class="note">거리는 실제 비율이 아닙니다. 정거장은 지표에서 약 400 km, 달은 약 384,000 km 떨어져 있습니다. 신호는 빛의 속력(300,000 km/s)으로 갑니다.</p>
        <div class="clocks" id="clk1"></div>
      </div>
      <div class="card">
        <div class="step on" id="s1a">
          <div class="lab">예측</div>
          <p>신호를 <b>받은 순간</b> 그대로 9시 정각으로 맞추면, 달 시계는 거래소 시계와 비교해 어떻게 될까?</p>
          <div class="choices" data-q="q1">
            <button class="btn" data-v="fast">빠르다</button><button class="btn" data-v="slow">늦다</button><button class="btn" data-v="same">같다</button>
          </div>
        </div>
        <div class="step" id="s1b">
          <div class="lab">관찰</div>
          <div class="choices">
            <button class="btn primary" id="send1">9시 정각 신호 보내기</button>
            <span class="seg" role="group" aria-label="거리 보정"><button id="c1off" class="on">거리 보정 끄기</button><button id="c1on">켜기</button></span>
          </div>
        </div>
        <div class="step" id="s1c">
          <div class="lab">설명</div>
          <div class="reveal" id="r1" hidden></div>
        </div>
        <div class="callout"><b>거리에 따른 시간 차</b> = 거리 ÷ 빛의 속력<br>
          <span class="num">달: 384,000 km ÷ 300,000 km/s ≈ 1.28 s</span><br>
          <span class="num">정거장: 400 km ÷ 300,000 km/s ≈ 0.0013 s</span><br>
          거리를 알면 미리 계산해서 <b>한 번에 보정</b>할 수 있다.</div>
      </div>
    </div>
  </section>

  <!-- ② 주문하기 -->
  <section class="tab" id="p2" role="tabpanel" aria-labelledby="tb2" hidden>
    <div class="grid2">
      <div class="card">
        <h3>시계를 맞춘 직후, 6명이 같은 값에 주문한다</h3>
        <p class="note">사곡전자 300주 · 50,000원 · 100주씩 · 먼저 낸 3명만 산다 (가격 우선 → 시간 우선)</p>
        <svg id="map2" viewBox="0 0 960 300" role="img" aria-label="주문이 거래소로 이동하는 그림"></svg>
        <svg id="nl2" viewBox="0 0 960 250" role="img" aria-label="낸 순간과 거래소에 도착한 순간을 비교하는 수직선"></svg>
        <div class="tablewrap"><table id="t2"></table></div>
        <p class="note">시각: 오전 9시 정각 이후 지난 시간(μs, 100만분의 1초). 세 곳의 시계는 방금 맞췄으므로 모두 같다.</p>
      </div>
      <div class="card">
        <div class="step on">
          <div class="lab">예측</div>
          <p>거래소에 <b>도착한 순서</b>로 체결하면, 달 주민(가, 라)은 살 수 있을까?</p>
          <div class="choices" data-q="q2"><button class="btn" data-v="yes">살 수 있다</button><button class="btn" data-v="no">살 수 없다</button></div>
        </div>
        <div class="step">
          <div class="lab">관찰</div>
          <div class="choices"><button class="btn primary" id="send2">주문 보내기</button></div>
          <div class="lists">
            <div><b>도착 순서로 체결</b><ol class="olist" id="lArr"></ol></div>
            <div><b>낸 시각 순서로 체결</b><ol class="olist" id="lTs"></ol></div>
          </div>
        </div>
        <div class="step">
          <div class="lab">설명</div>
          <div class="reveal" id="r2" hidden></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ③ 하루가 지나면 -->
  <section class="tab" id="p3" role="tabpanel" aria-labelledby="tb3" hidden>
    <div class="grid2">
      <div class="card">
        <h3>시계를 맞춘 뒤 시간이 흐르면</h3>
        <label class="ctl" for="days"><span class="ctl-row"><span>시계를 맞춘 뒤 지난 시간</span><span class="num" id="daysV">0.0일</span></span>
          <input type="range" id="days" min="0" max="3" step="0.1" value="0"></label>
        <div class="clocks" id="clk3"></div>
        <p class="note">세 시계 모두 고장 나지 않은 정확한 시계다. 그런데도 거래소 시계와의 차이가 생긴다.</p>
      </div>
      <div class="card">
        <div class="step on">
          <div class="lab">예측</div>
          <p>거리 보정까지 해서 맞춘 시계들. <b>하루 뒤에도</b> 거래소 시계와 일치할까?</p>
          <div class="choices" data-q="q3"><button class="btn" data-v="yes">일치한다</button><button class="btn" data-v="no">어긋난다</button></div>
        </div>
        <div class="step">
          <div class="lab">관찰</div>
          <p>위 슬라이더를 <b>1일</b>로 옮겨 보자.</p>
        </div>
        <div class="step">
          <div class="lab">설명</div>
          <div class="reveal" id="r3" hidden></div>
        </div>
      </div>
    </div>

    <div class="two">
      <div class="card">
        <h3>왜 다를까? ① 우주 정거장</h3>
        <label class="ctl" for="alt"><span class="ctl-row"><span>정거장 고도</span><span class="num" id="altV">400 km</span></span>
          <input type="range" id="alt" min="300" max="40000" step="100" value="400"></label>
        <div class="choices"><button class="btn" data-alt="400">400 km (활동지)</button><button class="btn" data-alt="3200">3,200 km</button><button class="btn" data-alt="20200">20,200 km (GPS)</button></div>
        <div class="bars" id="barsS"></div>
        <svg id="curve" viewBox="0 0 460 210" role="img" aria-label="고도에 따른 하루 시간 차이 그래프"></svg>
        <p class="note">중력 효과 = (GM/c²)(1/R − 1/r) × 86,400 s, 속도 효과 = (v²/2c²) × 86,400 s, v = √(GM/r)</p>
      </div>
      <div class="card">
        <h3>왜 다를까? ② 달 기지</h3>
        <div class="bars" id="barsM"></div>
        <p class="note">달의 값은 NASA 달 표준시 발표값입니다. 고교 수준 계산으로는 약 +56 μs/일이 나옵니다.</p>
        <div class="callout thumbs"><b>엄지 신호</b> 👍 빨라짐 · 👎 느려짐<br>우주 정거장 시계는? 달 기지 시계는? 그 까닭은?</div>
        <div class="reveal" id="rWhy">
          <b>정거장</b>: 낮게, 빠르게 돈다 → 높이 효과는 작고 속도 효과가 커서 <b>느려짐</b><br>
          <b>달</b>: 멀리, 천천히 돈다 → 지구 중력에서 벗어난 효과가 커서 <b>빨라짐</b>
        </div>
        <div class="choices"><button class="btn" id="whyBtn">까닭 보기</button></div>
      </div>
    </div>

    <div class="card">
      <h3>하루 뒤, 같은 6명이 같은 순간에 주문했다 · 낸 시각은 각자 <span class="tag loc">그곳 시계</span>로 찍힌다</h3>
      <div class="tablewrap"><table id="t3"></table></div>
      <div class="reveal bad" id="r3b"></div>
    </div>
  </section>

  <!-- ④ 체결 비교 -->
  <section class="tab" id="p4" role="tabpanel" aria-labelledby="tb4" hidden>
    <div class="card">
      <div class="ctl-row">
        <h3>그곳 시계에 찍힌 낸 시각 그대로 vs 지구 시계로 환산 (<span id="days4">1.0</span>일 뒤)</h3>
        <span class="seg" role="group" aria-label="상대성 보정"><button id="c4off" class="on">상대성 보정 없음</button><button id="c4on">상대성 보정 (지구 시계로 환산)</button></span>
      </div>
      <div class="flow" aria-label="2045년 우주 거래소의 체결 과정">
        <div><b class="n">1</b>주문에는 각자 <b>그곳 시계</b>로 낸 시각이 찍혀 온다.</div>
        <div><b class="n">2</b>거래소는 도착한 주문을 모았다가, 찍힌 시각을 <b>지구 시계로 환산</b>한다.</div>
        <div><b class="n">3</b>환산한 <b>낸 순간</b>이 빠른 순서로 체결한다. 도착한 순서가 아니다.</div>
      </div>
      <p class="note">예) 가: 달 시계로 78.7 μs에 냄 → 지구 시계로는 20 μs에 냄 → 거래소 도착은 약 1.28 s. 비교하는 것은 20 μs다.</p>
      <svg id="tl4" viewBox="0 0 960 270" role="img" aria-label="주문 시각 타임라인"></svg>
      <div class="tablewrap"><table id="t4"></table></div>
      <p class="note"><span class="tag earth">낸 시각 (지구 시계로 환산)</span> = <span class="tag loc">낸 시각 (그곳 시계)</span> − (그곳 시계가 앞선 시간) · 달: 78.7 − 58.7 = 20 · 정거장: 시계가 24.8 μs 뒤처졌으므로 35.2 + 24.8 = 60</p>
    </div>
    <div class="grid2">
      <div class="card" id="verdict4"></div>
      <div class="card">
        <div class="step on">
          <div class="lab">판단 (모둠)</div>
          <p>공정한 거래를 위해 <b>각자의 시계를 그대로 쓸까, 공통 시간 기준으로 환산할까?</b> 그 공통 기준은 누가 만들어야 할까?</p>
        </div>
        <div class="choices"><button class="btn" id="conceptBtn">경제 개념 정리</button></div>
        <div class="reveal" id="concept" hidden>
          <b>희소성</b>: 사려는 사람(600주)보다 주식(300주)이 적어서, 누가 살지 정하는 규칙(가격 우선 → 시간 우선)이 필요했다.<br>
          <b>공공재</b>: 모두가 함께 쓰는 공통 시간 기준은 누구나 쓸 수 있고, 써도 줄어들지 않는다.<br>
          <b>실제 사례</b>: 미국은 NASA에 달 표준시를 2026년 말까지 만들도록 지시했다. GPS 위성 시계는 상대성 보정을 하지 않으면 하루에 약 11 km의 위치 오차가 생긴다.
        </div>
      </div>
    </div>
  </section>
</div>

<script>
(function(){
  const $=id=>document.getElementById(id);
  const COL={E:'#2e8b7a',S:'#4e6bd6',M:'#c97b2a',ink:'#1e3a5f',muted:'#6a7280',line:'#dfe3ea',ok:'#2f8f5b',bad:'#c0392b',gold:'#c9a96e'};
  const PLACE={E:'지구',S:'우주 정거장',M:'달 기지'}, SHORT={E:'지구',S:'정거장',M:'달'};
  const DELAY={E:0,S:0.0013,M:1.28};           // 신호 지연 (s)
  const RATE={E:0,S:-24.8,M:58.7};             // 하루 시계 차이 (μs/일)
  const ORD=[{id:'가',w:'M',t:20},{id:'나',w:'E',t:35},{id:'라',w:'M',t:40},{id:'마',w:'E',t:45},{id:'다',w:'S',t:60},{id:'바',w:'S',t:70}];
  const SLOTS=3;
  const fmt1=v=>(Math.round(v*10)/10).toFixed(1).replace(/\.0$/,'');
  const sgn=(v,d=1)=>(v>0?'+':v<0?'−':'')+Math.abs(v).toFixed(d);
  const dot=w=>`<span class="who-dot" style="background:${COL[w]}">`;
  const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---------- 탭 ----------
  const tabs=[1,2,3,4];
  function showTab(n){tabs.forEach(i=>{$('tb'+i).setAttribute('aria-selected',i===n);$('p'+i).hidden=i!==n});
    if(n===3||n===4)render34();}
  tabs.forEach(i=>$('tb'+i).addEventListener('click',()=>showTab(i)));

  // ---------- 예측 선택 ----------
  const pred={};
  document.querySelectorAll('.choices[data-q]').forEach(g=>g.querySelectorAll('button').forEach(b=>b.addEventListener('click',()=>{
    g.querySelectorAll('button').forEach(x=>x.classList.toggle('sel',x===b));pred[g.dataset.q]=b.dataset.v;
    if(g.dataset.q==='q3')render34();
  })));

  // ---------- 지도 ----------
  let EARTH={x:150,y:180,r:72}, STN={x:250,y:108}, MOON={x:860,y:180,r:26};
  function setCy(cy){EARTH={x:150,y:cy,r:72};STN={x:250,y:cy-72};MOON={x:860,y:cy,r:26}}
  function baseMap(h,cy){
    setCy(cy);
    return `<defs><radialGradient id="eg${cy}" cx="35%" cy="35%"><stop offset="0" stop-color="#8cc7f0"/><stop offset=".6" stop-color="#3f86c8"/><stop offset="1" stop-color="#1f4f86"/></radialGradient></defs>
    <rect x="0" y="0" width="960" height="${h}" fill="#f2f4f8" rx="10"/>
    <circle cx="${EARTH.x}" cy="${EARTH.y}" r="${EARTH.r}" fill="url(#eg${cy})"/>
    <circle cx="${EARTH.x}" cy="${EARTH.y}" r="125" fill="none" stroke="${COL.S}" stroke-dasharray="3 5" opacity=".6"/>
    <g transform="translate(${STN.x} ${STN.y})"><rect x="-16" y="-4" width="32" height="8" fill="${COL.S}"/><rect x="-4" y="-10" width="8" height="20" fill="${COL.S}"/></g>
    <text x="${STN.x+22}" y="${STN.y-8}" font-size="15" font-weight="700" fill="${COL.S}">우주 정거장</text>
    <circle cx="${MOON.x}" cy="${MOON.y}" r="${MOON.r}" fill="#d9d4c7" stroke="${COL.M}" stroke-width="2"/>
    <text x="${MOON.x}" y="${MOON.y+52}" font-size="15" font-weight="700" fill="${COL.M}" text-anchor="middle">달 기지</text>
    <text x="${EARTH.x}" y="${EARTH.y+EARTH.r+24}" font-size="15" font-weight="700" fill="${COL.E}" text-anchor="middle">지구 (거래소)</text>
    <line x1="${EARTH.x+EARTH.r+60}" y1="${h-22}" x2="${MOON.x-40}" y2="${h-22}" stroke="${COL.muted}" stroke-dasharray="2 4"/>
    <text x="${(EARTH.x+MOON.x)/2+30}" y="${h-28}" font-size="13" fill="${COL.muted}" text-anchor="middle">지구–달 약 384,000 km · 빛으로 1.28초</text>`;
  }

  // ---------- ① 시계 맞추기 ----------
  let s1={sent:false,corr:false,anim:0,start:0};
  const ANIM1=3.2; // 화면에서 달까지 걸리는 시간(초)
  function clockText(diffSec){
    if(Math.abs(diffSec)<1e-9) return '09:00:00.000000';
    const t=9*3600+diffSec; const h=Math.floor(t/3600), m=Math.floor((t%3600)/60), s=t%60;
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${s.toFixed(6).padStart(9,'0')}`;
  }
  function render1(p){ // p: 0..1 애니메이션 진행
    let svg=baseMap(360,180);
    if(s1.sent){
      const k=Math.min(1,p);
      const mx=EARTH.x+EARTH.r+(MOON.x-MOON.r-EARTH.x-EARTH.r)*k;
      svg+=`<line x1="${EARTH.x+EARTH.r}" y1="${EARTH.y}" x2="${mx}" y2="${EARTH.y}" stroke="${COL.gold}" stroke-width="3"/>
            <circle cx="${mx}" cy="${EARTH.y}" r="7" fill="${COL.gold}"/>`;
      svg+=`<line x1="${EARTH.x}" y1="${EARTH.y-EARTH.r}" x2="${STN.x}" y2="${STN.y}" stroke="${COL.gold}" stroke-width="3"/>`;
      svg+=`<text x="${(EARTH.x+MOON.x)/2}" y="${EARTH.y-16}" font-size="15" fill="${COL.ink}" text-anchor="middle" font-weight="700">“9시 정각” 신호 · 보낸 뒤 ${(k*1.28).toFixed(2)} s</text>`;
    }
    $('map1').innerHTML=svg;
    const tau=s1.sent?Math.min(1,p)*1.28:0;           // 신호를 보낸 뒤 흐른 실제 시간(s)
    const got={E:true,S:s1.sent&&tau>=DELAY.S,M:s1.sent&&tau>=DELAY.M};
    $('clk1').innerHTML=['E','S','M'].map(w=>{
      let t='--:--:--', d='신호를 기다리는 중';
      if(w==='E'){t=s1.sent?clockText(tau):'09:00:00.000000';d=s1.sent?'거래소 시계 (기준)':'거래소 시계 · 9시 정각에 신호를 보낸다';}
      else if(got[w]){const diff=s1.corr?0:-DELAY[w];t=clockText(tau+diff);
        d=Math.abs(diff)<1e-9?'<span style="color:var(--ok);font-weight:700">받은 순간 '+clockText(DELAY[w])+'로 맞춤 → 거래소와 일치</span>'
          :`<span style="color:var(--bad);font-weight:700">받은 순간 09:00:00으로 맞춤 → 거래소보다 ${DELAY[w]} s 늦음</span>`;}
      return `<div class="clk"><span class="who" style="color:${COL[w]}">${PLACE[w]} 시계</span><span class="t">${t}</span><span class="d">${d}</span></div>`;
    }).join('');
    if(s1.sent&&p>=1){
      const r=$('r1');r.hidden=false;
      r.className='reveal '+(s1.corr?'good':'bad');
      r.innerHTML=s1.corr
        ?'신호를 받은 순간 09:00:00에 걸린 시간(달 1.28 s)을 <b>더해</b> 09:00:01.28로 맞추면 세 시계가 모두 일치한다. 이것이 <b>거리 보정</b>이다.'
        :`신호가 달에 닿은 순간 거래소 시계는 이미 <b>09:00:01.28</b>이다. 그때 달 시계를 09:00:00으로 맞추면 달 시계는 거래소보다 <b>1.28 s 늦다</b>${pred.q1?(pred.q1==='slow'?' (예측 적중)':' (예측과 다름)'):''}. → ‘거리 보정 켜기’를 눌러 보자.`;
      ['s1b','s1c'].forEach(i=>$(i).classList.add('on'));
    }
  }
  function run1(){s1.sent=true;s1.start=performance.now();$('r1').hidden=true;
    const loop=()=>{const p=reduce?1:(performance.now()-s1.start)/1000/ANIM1;render1(p);if(p<1)s1.anim=requestAnimationFrame(loop)};
    cancelAnimationFrame(s1.anim);loop();}
  $('send1').onclick=run1;
  $('c1off').onclick=()=>{s1.corr=false;$('c1off').classList.add('on');$('c1on').classList.remove('on');render1(s1.sent?1:0)};
  $('c1on').onclick=()=>{s1.corr=true;$('c1on').classList.add('on');$('c1off').classList.remove('on');render1(s1.sent?1:0)};
  render1(0);

  // ---------- ② 주문하기 ----------
  let s2={sent:false,start:0,anim:0};
  const ANIM2=3.4;
  const arrive=o=>o.t*1e-6+DELAY[o.w];               // 도착 시각 (s)
  const arrOrder=[...ORD].sort((a,b)=>arrive(a)-arrive(b));
  const tsOrder=[...ORD].sort((a,b)=>a.t-b.t);
  const ARRTXT={E:'바로',S:'0.0013 s 뒤',M:'1.28 s 뒤'};
  function table2(){
    $('t2').innerHTML=`<thead><tr><th>신청자</th><th>사는 곳</th><th class="r">낸 시각</th><th>거래소 도착</th></tr></thead><tbody>`+
      tsOrder.map(o=>`<tr><td>${dot(o.w)}${o.id}</span></td><td>${PLACE[o.w]}</td><td class="r num">${o.t} μs</td><td>${ARRTXT[o.w]}</td></tr>`).join('')+'</tbody>';
  }
  function nl2(done){
    const L=150,R=930, X1=t=>L+t/100*(R-L);
    // 도착 줄: 끊어진 축 [0–100 μs] [1.30–1.40 ms] [1.28 s + 0–100 μs]
    const XB=v=>v<1000?L+v/100*300:v<1e6?L+350+(v-1300)/100*190:L+590+(v-1.28e6)/100*190;
    const y1=62,y2=182;
    let g=`<text x="12" y="${y1+5}" font-size="14" font-weight="700" fill="${COL.ink}">낸 순간</text>
      <text x="12" y="${y2+5}" font-size="14" font-weight="700" fill="${COL.ink}">거래소 도착</text>
      <line x1="${L}" x2="${R}" y1="${y1}" y2="${y1}" stroke="${COL.muted}" stroke-width="2"/>`;
    for(let v=0;v<=100;v+=20)g+=`<line x1="${X1(v)}" x2="${X1(v)}" y1="${y1}" y2="${y1+6}" stroke="${COL.muted}"/><text x="${X1(v)}" y="${y1+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${v}${v===100?' μs':''}</text>`;
    // 아래 축 세 구간
    [[L,L+300,'0','100 μs'],[L+350,L+540,'1.30 ms','1.40 ms'],[L+590,L+780,'1.28 s','']].forEach(([x1,x2,a,b2])=>{
      g+=`<line x1="${x1}" x2="${x2}" y1="${y2}" y2="${y2}" stroke="${COL.muted}" stroke-width="2"/>
        <text x="${x1}" y="${y2+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${a}</text>${b2?`<text x="${x2}" y="${y2+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${b2}</text>`:''}`});
    [L+325,L+565].forEach(x=>g+=`<text x="${x}" y="${y2+6}" font-size="18" fill="${COL.muted}" text-anchor="middle">≈</text>`);
    g+=`<text x="${(L+350+L+540)/2}" y="${y2+54}" font-size="12" fill="${COL.muted}" text-anchor="middle">정거장: 0.0013 s 뒤</text>
        <text x="${L+685}" y="${y2+54}" font-size="12" fill="${COL.muted}" text-anchor="middle">달: 1.28 s 뒤 (약 1000배 더 늦음)</text>`;
    // 낸 순서 3명
    const tsWin=new Set(tsOrder.slice(0,SLOTS).map(o=>o.id)), arWin=new Set(arrOrder.slice(0,SLOTS).map(o=>o.id));
    if(done){
      ORD.forEach(o=>{const xa=X1(o.t), xb=XB(o.t+DELAY[o.w]*1e6);
        g+=`<line x1="${xa}" y1="${y1+16}" x2="${xb}" y2="${y2-16}" stroke="${COL[o.w]}" stroke-width="1.5" opacity=".55"/>`});
    }
    const node=(x,y,o,win)=>`<g transform="translate(${x} ${y})"><circle r="15" fill="${COL[o.w]}" opacity="${win?1:.4}" ${win?`stroke="${COL.ok}" stroke-width="4"`:''}/><text y="5" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">${o.id}</text></g>`;
    ORD.forEach(o=>g+=node(X1(o.t),y1,o,done&&tsWin.has(o.id)));
    if(done) ORD.forEach(o=>g+=node(XB(o.t+DELAY[o.w]*1e6),y2,o,arWin.has(o.id)));
    else g+=`<text x="${L+20}" y="${y2-22}" font-size="13" fill="${COL.muted}">‘주문 보내기’를 누르면 도착 순간이 나타난다</text>`;
    if(done) g+=`<text x="${R}" y="20" font-size="13" fill="${COL.ok}" text-anchor="end" font-weight="700">초록 테두리 = 그 순서로 체결하면 사는 3명</text>`;
    $('nl2').innerHTML=g;
  }
  function render2(p){
    let svg=baseMap(300,150);
    // 주문 패킷
    const ex={x:EARTH.x+EARTH.r-6,y:150};
    if(s2.sent){
      ORD.forEach((o,i)=>{
        let from,dur,start;
        if(o.w==='E'){from={x:EARTH.x-40+i*6,y:150+EARTH.r-10};dur=.08;start=i*.01}
        else if(o.w==='S'){from={x:STN.x,y:STN.y};dur=.12;start=.05+i*.01}
        else {from={x:MOON.x-MOON.r,y:150};dur=.9;start=.05+i*.03}
        const k=Math.max(0,Math.min(1,(p-start)/dur));
        if(p<start)return;
        const x=from.x+(ex.x-from.x)*ease(k), y=from.y+(ex.y-from.y)*ease(k);
        svg+=`<circle cx="${x}" cy="${y}" r="12" fill="${COL[o.w]}" opacity="${k>=1?.25:1}"/><text x="${x}" y="${y+5}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">${o.id}</text>`;
      });
    }
    $('map2').innerHTML=svg; nl2(s2.sent&&p>=1);
    const nArr=s2.sent?arrOrder.filter(o=>{const st=o.w==='E'?.0:o.w==='S'?.05:.05;const dur=o.w==='E'?.08:o.w==='S'?.12:.9;return p>=st+dur+ (o.w==='M'?.06:.05)}).length:0;
    $('lArr').innerHTML=arrOrder.slice(0,nArr).map((o,i)=>`<li class="${i<SLOTS?'win':''}">${dot(o.w)}${o.id}</span>${SHORT[o.w]}${i<SLOTS?' <span class="pill ok">구매</span>':''}</li>`).join('');
    $('lTs').innerHTML=(s2.sent&&p>=1)?tsOrder.map((o,i)=>`<li class="${i<SLOTS?'win':''}">${dot(o.w)}${o.id}</span>${SHORT[o.w]} <span class="num">${o.t}μs</span>${i<SLOTS?' <span class="pill ok">구매</span>':''}</li>`).join(''):'';
    if(s2.sent&&p>=1){
      const r=$('r2');r.hidden=false;r.className='reveal';
      r.innerHTML=`도착 순서로 하면 <b>나·마·다</b>가 산다. 가장 먼저 낸 달 주민 <b>가</b>와 <b>라</b>는 신호가 1.28 s 늦게 도착해서 늘 진다${pred.q2?(pred.q2==='no'?' (예측 적중)':' (예측과 다름)'):''}.<br>
      그래서 <b>2045년 우주 거래소 규칙</b>: 도착 순서가 아니라 <b>주문을 낸 곳의 시계에 찍힌 시각</b>으로 순서를 정한다. 시계를 방금 맞췄으므로 결과는 <b>가·나·라</b>, 공정하다.`;
    }
  }
  function run2(){s2.sent=true;s2.start=performance.now();
    const loop=()=>{const p=reduce?1.2:(performance.now()-s2.start)/1000/ANIM2;render2(p);if(p<1.2)s2.anim=requestAnimationFrame(loop)};
    cancelAnimationFrame(s2.anim);loop();}
  $('send2').onclick=run2; table2(); render2(0);

  // ---------- ③ 하루가 지나면 / 상대성 ----------
  const GM=3.986004418e14, Cc=299792458, R=6.371e6, k=GM/(Cc*Cc), DAY=86400;
  const gr=h=>k*(1/R-1/(R+h*1e3))*DAY*1e6, sr=h=>-k/(2*(R+h*1e3))*DAY*1e6;
  let days=0, alt=400, corr4=false;
  function barRow(label,v,max,col,txt){
    const w=Math.min(50,Math.abs(v)/max*50);
    const left=v>=0?50:50-w;
    return `<div class="bar"><span>${label}</span><span class="track"><span class="zero"></span><span class="fill" style="left:${left}%;width:${w}%;background:${col}"></span></span><span class="num" style="text-align:right">${txt}</span></div>`;
  }
  function renderBars(){
    let g=gr(alt), sv=sr(alt), n=g+sv;
    if(alt===400){g=3.5;sv=-28.3;n=-24.8} // 활동지·지도안과 같은 반올림 값
    $('altV').textContent=alt.toLocaleString()+' km';
    $('barsS').innerHTML=barRow('중력 효과',g,60,COL.gold,sgn(g)+' μs')+barRow('속도 효과',sv,60,'#8b9bf0',sgn(sv)+' μs')+barRow('<b>합계</b>',n,60,n<0?COL.S:COL.ok,'<b>'+sgn(n)+' μs</b>');
    $('barsM').innerHTML=barRow('지구 중력에서 멀어짐',59.1,60,COL.gold,'크게 +')+barRow('달 자체의 중력',-2.7,60,'#b9a07a','조금 −')+barRow('느린 공전 속도',-0.5,60,'#8b9bf0','조금 −')+barRow('<b>합계</b>',58.7,60,COL.M,'<b>+58.7 μs</b>');
    document.querySelectorAll('[data-alt]').forEach(b=>b.classList.toggle('sel',+b.dataset.alt===alt));
    // 곡선
    const W=460,H=210,L=40,Rr=10,T=12,B=30,xMax=40000,yMin=-30,yMax=60;
    const X=h=>L+h/xMax*(W-L-Rr), Y=v=>T+(yMax-v)/(yMax-yMin)*(H-T-B);
    const path=f=>{let d='';for(let h=300;h<=xMax;h+=200)d+=(d?'L':'M')+X(h).toFixed(1)+','+Y(Math.max(yMin,Math.min(yMax,f(h)))).toFixed(1);return d};
    let s='';
    for(let v=-30;v<=60;v+=15)s+=`<line x1="${L}" x2="${W-Rr}" y1="${Y(v)}" y2="${Y(v)}" stroke="${v===0?COL.muted:COL.line}"/><text x="${L-5}" y="${Y(v)+4}" font-size="10" fill="${COL.muted}" text-anchor="end">${v}</text>`;
    for(let h=0;h<=40000;h+=10000)s+=`<text x="${X(h)}" y="${H-12}" font-size="10" fill="${COL.muted}" text-anchor="middle">${h/1000}</text>`;
    s+=`<text x="${W-Rr}" y="${H-1}" font-size="10" fill="${COL.muted}" text-anchor="end">고도 (천 km)</text><text x="${L}" y="${T-2}" font-size="10" fill="${COL.muted}">하루 시간 차이 (μs)</text>`;
    s+=`<path d="${path(gr)}" fill="none" stroke="${COL.gold}" stroke-width="2"/><path d="${path(sr)}" fill="none" stroke="#8b9bf0" stroke-width="2"/><path d="${path(h=>gr(h)+sr(h))}" fill="none" stroke="${COL.ink}" stroke-width="3"/>`;
    s+=`<circle cx="${X(alt)}" cy="${Y(Math.max(yMin,Math.min(yMax,n)))}" r="6" fill="${COL.S}" stroke="#fff" stroke-width="2"/>`;
    $('curve').innerHTML=s;
  }
  const off=w=>RATE[w]*days;                   // 시계가 앞선 시간 (μs)
  function render34(){
    $('daysV').textContent=days.toFixed(1)+'일'; $('days4').textContent=days.toFixed(1);
    $('clk3').innerHTML=['E','S','M'].map(w=>{
      const o=off(w);
      const dTxt=w==='E'?'기준 시계':(Math.abs(o)<.05?'<span style="color:var(--ok);font-weight:700">거래소와 일치</span>':`<span style="color:var(--bad);font-weight:700">거래소보다 ${Math.abs(o).toFixed(1)} μs ${o>0?'빠름':'느림'}</span>`);
      return `<div class="clk"><span class="who" style="color:${COL[w]}">${PLACE[w]} 시계</span>
        <span class="d">신호 지연(고정): ${w==='E'?'없음':DELAY[w]+' s → <b>보정 완료</b>'}</span>
        <span class="d">시계 빠르기 차이(누적): <b class="num">${w==='E'?'0':sgn(o)} μs</b></span>
        <span class="d">${dTxt}</span></div>`}).join('');
    if(days>=0.95){const r=$('r3');r.hidden=false;r.className='reveal bad';
      r.innerHTML=`하루 뒤 <b>달 시계는 +58.7 μs</b>, <b>정거장 시계는 −24.8 μs</b> 어긋난다${pred.q3?(pred.q3==='no'?' (예측 적중)':' (예측과 다름)'):''}. 시계가 고장 난 것이 아니라 <b>그곳의 시간이 다르게 흐르기</b> 때문이다(중력 효과와 속도 효과). 거리 보정은 한 번으로 끝나지만, 이 차이는 <b>날마다 쌓인다</b>.`}
    else $('r3').hidden=true;
    // 하루 뒤 주문 기록
    const rec=ORD.map(o=>({...o,rec:o.t+off(o.w)}));
    const byRec=[...rec].sort((a,b)=>a.rec-b.rec);
    const win=new Set(byRec.slice(0,SLOTS).map(o=>o.id));
    $('t3').innerHTML=`<thead><tr><th>순위</th><th>신청자</th><th>사는 곳</th><th class="r"><span class="tag loc">낸 시각 (그곳 시계)</span></th><th>이 순서로 체결하면</th></tr></thead><tbody>`+
      byRec.map((o,i)=>`<tr class="${i===SLOTS-1?'cut':''}"><td class="num">${i+1}</td><td>${dot(o.w)}${o.id}</span></td><td>${PLACE[o.w]}</td><td class="r num"><b>${fmt1(o.rec)} μs</b></td><td>${win.has(o.id)?'<span class="pill ok">구매</span>':'<span class="pill no">실패</span>'}</td></tr>`).join('')+'</tbody>';
    $('r3b').innerHTML=days<0.05?'시계를 맞춘 직후이므로 기록된 시각이 그대로 공정하다. 슬라이더를 1일로 옮겨 보자.':
      `그곳 시계에 찍힌 시각대로 체결하면 <b>${byRec.slice(0,3).map(o=>o.id).join('·')}</b>가 산다. 실제로는 누가 먼저 냈을까? → ④ 체결 비교에서 확인하자.`;
    $('r3b').className='reveal '+(days<0.05?'good':'bad');
    render4();
  }
  $('days').addEventListener('input',e=>{days=+e.target.value;render34()});
  $('alt').addEventListener('input',e=>{alt=+e.target.value;renderBars()});
  document.querySelectorAll('[data-alt]').forEach(b=>b.addEventListener('click',()=>{alt=+b.dataset.alt;$('alt').value=alt;renderBars()}));
  $('whyBtn').onclick=()=>{$('rWhy').hidden=!$('rWhy').hidden};
  $('rWhy').hidden=true;

  // ---------- ④ 체결 비교 ----------
  function render4(){
    const d=days<0.05?1:days; // ④는 최소 1일 기준으로 보여 줌
    if(days<0.05){$('days4').textContent='1.0'}
    const rec=ORD.map(o=>{const of=RATE[o.w]*d;return {...o,of,rec:o.t+of}});
    const key=corr4?'t':'rec';
    const byKey=[...rec].sort((a,b)=>a[key]-b[key]);
    const win=new Set(byKey.slice(0,SLOTS).map(o=>o.id));
    const fair=new Set([...rec].sort((a,b)=>a.t-b.t).slice(0,SLOTS).map(o=>o.id));
    // 두 줄 수직선
    const L=170,R=930,hi=110, X=v=>L+v/hi*(R-L), y1=70,y2=200;
    const recWin=new Set([...rec].sort((a,b)=>a.rec-b.rec).slice(0,SLOTS).map(o=>o.id));
    let s=`<text x="10" y="${y1-4}" font-size="14" font-weight="700" fill="#555c68">낸 시각</text><text x="10" y="${y1+14}" font-size="12" fill="${COL.muted}">(그곳 시계)</text>
      <text x="10" y="${y2-4}" font-size="14" font-weight="700" fill="${COL.ok}">낸 시각</text><text x="10" y="${y2+14}" font-size="12" fill="${COL.muted}">(지구 시계로 환산)</text>`;
    [y1,y2].forEach(y=>{s+=`<line x1="${L}" x2="${R}" y1="${y}" y2="${y}" stroke="${COL.muted}" stroke-width="2"/>`;
      for(let v=0;v<=hi;v+=10)s+=`<line x1="${X(v)}" x2="${X(v)}" y1="${y}" y2="${y+6}" stroke="${COL.muted}"/>${v%20===0?`<text x="${X(v)}" y="${y+40}" font-size="12" fill="${COL.muted}" text-anchor="middle">${v}${v===100?' μs':''}</text>`:''}`});
    // 겹치는 점은 위로 쌓기
    const lay=(arr,f,y)=>{const placed=[];return arr.map(o=>{const x=X(f(o));let lv=0;while(placed.some(p=>p.lv===lv&&Math.abs(p.x-x)<32))lv++;placed.push({x,lv});return {o,x,y:y-lv*32}})};
    const top=lay([...rec].sort((a,b)=>a.rec-b.rec),o=>o.rec,y1);
    const bot=lay([...rec].sort((a,b)=>a.t-b.t),o=>o.t,y2);
    if(corr4) rec.forEach(o=>{const a=top.find(p=>p.o.id===o.id), b=bot.find(p=>p.o.id===o.id);
      s+=`<line x1="${a.x}" y1="${y1+16}" x2="${b.x}" y2="${b.y-16}" stroke="${COL[o.w]}" stroke-width="2" opacity=".6"/>`;
      if(o.w!=='E'){const f=o.w==='M'?.68:.35, lx=a.x+(b.x-a.x)*f, ly=(y1+16)+((b.y-16)-(y1+16))*f; s+=`<text x="${lx+(o.w==='M'?-8:8)}" y="${ly+4}" font-size="12" font-weight="700" fill="${COL[o.w]}" text-anchor="${o.w==='M'?'end':'start'}">${o.w==='M'?'−58.7':'+24.8'}</text>`}});
    const node=(p,win)=>`<g transform="translate(${p.x} ${p.y})"><circle r="15" fill="${COL[p.o.w]}" opacity="${win?1:.4}" ${win?`stroke="${COL.ok}" stroke-width="4"`:''}/><text y="5" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">${p.o.id}</text></g>`;
    top.forEach(p=>s+=node(p,recWin.has(p.o.id)));
    if(corr4) bot.forEach(p=>s+=node(p,fair.has(p.o.id)));
    else s+=`<text x="${L+10}" y="${y2-24}" font-size="13" fill="${COL.muted}">‘상대성 보정’을 누르면 지구 시계로 환산한 낸 시각으로 옮겨진다</text>`;
    s+=`<text x="${R}" y="18" font-size="13" fill="${COL.ok}" text-anchor="end" font-weight="700">초록 테두리 = 그 줄의 순서로 체결하면 사는 3명</text>`;
    $('tl4').innerHTML=s;
    const calc=o=>o.w==='E'?`${fmt1(o.rec)} (그대로)`:o.w==='M'?`${fmt1(o.rec)} − 58.7`:`${fmt1(o.rec)} + 24.8`;
    const rank=[...rec].sort((a,b)=>a[key]-b[key]);
    $('t4').innerHTML=`<thead><tr><th>순위</th><th>신청자</th><th>사는 곳</th><th class="r"><span class="tag loc">낸 시각 (그곳 시계)</span></th><th>계산</th><th class="r"><span class="tag earth">낸 시각 (지구 시계로 환산)</span></th><th>보정 없이</th><th>보정 후</th><th>판정</th></tr></thead><tbody>`+
      rank.map((o,i)=>{const wNo=recWin.has(o.id), wYes=fair.has(o.id);
        const v=wYes&&!wNo?'<span class="pill bad">손해</span>':!wYes&&wNo?'<span class="pill gain">부당 이득</span>':'<span class="pill no">같음</span>';
        return `<tr class="${i===SLOTS-1?'cut':''}"><td class="num">${i+1}</td><td>${dot(o.w)}${o.id}</span></td><td>${PLACE[o.w]}</td><td class="r num">${fmt1(o.rec)} μs</td><td class="calc num">${corr4?calc(o):'?'}</td><td class="r num">${corr4?'<b>'+o.t+' μs</b>':'?'}</td><td>${wNo?'<span class="pill ok">구매</span>':'<span class="pill no">실패</span>'}</td><td>${corr4?(wYes?'<span class="pill ok">구매</span>':'<span class="pill no">실패</span>'):'?'}</td><td>${corr4?v:'?'}</td></tr>`}).join('')+'</tbody>';
    const losers=[...fair].filter(x=>!recWin.has(x));
    $('verdict4').innerHTML=corr4
      ?`<h3>지구 시계로 환산하면</h3><p>실제로 먼저 낸 <b>가·나·라</b>가 산다. 보정이 없을 때 <b>${losers.join('·')}</b>는 먼저 내고도 사지 못했고, 늦게 낸 사람이 대신 샀다.</p><p class="note">주문 직후 주가가 51,000원으로 오르면, 사지 못한 사람은 1인당 100주 × 1,000원 = 10만 원의 이익을 놓친다.</p>`
      :`<h3>상대성 보정이 없다면</h3><p>그곳 시계에 찍힌 시각 그대로 체결하면 <b>${[...win].join('·')}</b>가 산다. 거리 보정은 했지만, 그곳의 시간이 다르게 흐른 만큼 순서가 바뀌었다.</p><p class="note">‘상대성 보정’을 눌러 지구 시계로 환산해 보자.</p>`;
  }
  $('c4off').onclick=()=>{corr4=false;$('c4off').classList.add('on');$('c4on').classList.remove('on');render4()};
  $('c4on').onclick=()=>{corr4=true;$('c4on').classList.add('on');$('c4off').classList.remove('on');render4()};
  $('conceptBtn').onclick=()=>{$('concept').hidden=!$('concept').hidden};

  renderBars(); render34();
})();
</script>

</body>
</html>
"""

# 외부 HTML 파일이 존재하면 읽어서 사용하고, 없을 시 내장 DEFAULT_HTML 사용
if os.path.exists(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception:
        html_content = DEFAULT_HTML
else:
    html_content = DEFAULT_HTML

components.html(html_content, height=1650, scrolling=True)

# ── 학습 개념 및 탐구 정리 (Expander) ─────────────────────────
with st.expander("💡 [학습 정리] 우주 거래소의 시계 핵심 원리"):
    st.markdown("""
### 1. 거리에 따른 시간 차 (신호 지연)
- **빛의 속력 한계**: 신호는 진공에서 약 $c = 300,000\\text{ km/s}$로 이동합니다.
  - 지구-우주정거장(고도 약 400 km): 신호 지연 $\\approx 0.0013\\text{ s}$
  - 지구-달 기지(거리 약 384,000 km): 신호 지연 $\\approx 1.28\\text{ s}$
- **거리 보정**: 신호가 도달하는 데 걸린 시간($\\Delta t = d / c$)을 미리 알고 있다면, 신호를 받는 순간 그 시간을 더해 거래소와 시계를 한 번에 맞출 수 있습니다.

### 2. 상대성에 따른 시간 차 (중력 효과와 속도 효과)
시계를 한 번 맞춰도, 위치한 곳의 중력과 운동 상태에 따라 **시간이 흐르는 빠르기** 자체가 달라집니다.
- **우주 정거장 (ISS, 고도 400 km)**
  - 중력 효과 (높은 고도): 지구 표면보다 중력이 약간 약해 시계가 빨라짐 ($+3.5\\ \\mu\\text{s}/\\text{일}$)
  - 속도 효과 (빠른 궤도 속력 $v \\approx 7.7\\text{ km/s}$): 특수 상대성 이론에 의해 시계가 느려짐 ($-28.3\\ \\mu\\text{s}/\\text{일}$)
  - **합계**: 속도 효과가 더 커서 하루에 **약 $-24.8\\ \\mu\\text{s}$ 느려짐**
- **달 기지**
  - 지구의 강한 중력 퍼텐셜 우물에서 멀리 벗어남: 시계가 크게 빨라짐 ($+59.1\\ \\mu\\text{s}/\\text{일}$)
  - 달 자체의 약한 중력 및 공전 속도: 시계가 조금 느려짐 ($-3.2\\ \\mu\\text{s}/\\text{일}$)
  - **합계**: 하루에 **약 $+58.7\\ \\mu\\text{s}$ 빨라짐** (NASA 달 표준시 기준)

### 3. 경제·사회적 의미와 공공재로서의 시간 기준
- **시간 우선 체결 규칙**: 동일 가격 주문 시 먼저 낸 사람에게 배정되는 시장 규칙에서, 시간 측정의 기준이 왜곡되면 공정성이 무너집니다.
- **상대성 보정의 필수성**: GPS 인공위성이 하루 약 38 $\\mu\\text{s}$의 상대론적 오차를 보정하지 않으면 매일 11 km 이상의 위치 오차가 누적되는 것과 마찬가지로, 우주 시대의 금융 거래에서도 단일한 기준계로 환산하는 **우주 표준시(공공재)**가 반드시 필요합니다.
""")
