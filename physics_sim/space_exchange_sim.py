import streamlit as st
import streamlit.components.v1 as components
import os
import io
from datetime import datetime, date
import pandas as pd
import xml.sax.saxutils

# ── ReportLab 임포트 및 폰트 설정 ──────────────────────────────────
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
    )
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

FONT_REG = os.path.join(os.path.dirname(__file__), "fonts", "NanumGothic.ttf")
FONT_BOLD = os.path.join(os.path.dirname(__file__), "fonts", "NanumGothicBold.ttf")

if HAS_REPORTLAB and os.path.exists(FONT_REG):
    try:
        if "NG" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("NG", FONT_REG))
        if "NGB" not in pdfmetrics.getRegisteredFontNames():
            pdfmetrics.registerFont(TTFont("NGB", FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_REG))
    except Exception as e:
        print("ReportLab Font register error:", e)

# ── 패들렛 발표 게시판 URL 상수 ─────────────────────────────────
PADLET_URL = "https://padlet.com/sgh/padlet-s024y3iekcz0b0xn6dtu"

# ── 헤더 섹션 ──────────────────────────────────────────────────
st.title("💹 [융합] 우주 거래소의 시계")
st.markdown(
    "2045년 지구·우주 정거장·달 기지의 주민이 같은 주식을 주문할 때, "
    "**거리에 따른 시간 차**(신호 지연)와 **상대성에 따른 시간 차**(중력 효과·속도 효과)를 구별하고, "
    "시각을 환산해 공정한 체결 순서를 판단하는 가상 실험실 및 모둠 탐구 활동 지원 포털"
)

# 상단 빠른 액션 바
col_top1, col_top2 = st.columns([3, 2])
with col_top1:
    st.caption("2022 개정 역학과 에너지 [12역학01-08] 중력 시간 지연의 적용 × 경제·금융 융합 탐구")
with col_top2:
    st.link_button(
        "🪐 우주거래소 모둠별 발표 게시판 (패들렛) ↗",
        PADLET_URL,
        use_container_width=True,
        type="secondary"
    )

# ── HTML 시뮬레이션 파일 로드 ──────────────────────────────────────
html_path = os.path.join(os.path.dirname(__file__), "space-exchange.html")

# 기본 HTML 코드 (space-exchange.html fallback)
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
        <div class="callout" style="border-left-color:var(--station);background:#eef4fd;margin-top:10px">
          <b style="color:var(--station)">📢 모둠 과제 보고서 제출 안내</b><br>
          시뮬레이션 탐구를 마쳤다면, 활동지 보고서를 작성하여 <b>우주거래소 모둠별 발표 게시판</b>에 제출하세요.<br>
          <div style="margin-top:8px">
            <a href="https://padlet.com/sgh/padlet-s024y3iekcz0b0xn6dtu" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:7px 14px;background:#1e3a5f;color:#fff;border-radius:6px;text-decoration:none;font-weight:700;font-size:0.9rem">
              🪐 우주거래소 모둠별 발표 게시판 (패들렛) ↗
            </a>
          </div>
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
  const ANIM1=3.2;
  function clockText(diffSec){
    if(Math.abs(diffSec)<1e-9) return '09:00:00.000000';
    const t=9*3600+diffSec; const h=Math.floor(t/3600), m=Math.floor((t%3600)/60), s=t%60;
    return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${s.toFixed(6).padStart(9,'0')}`;
  }
  function render1(p){
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
    const tau=s1.sent?Math.min(1,p)*1.28:0;
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
  const arrive=o=>o.t*1e-6+DELAY[o.w];
  const arrOrder=[...ORD].sort((a,b)=>arrive(a)-arrive(b));
  const tsOrder=[...ORD].sort((a,b)=>a.t-b.t);
  const ARRTXT={E:'바로',S:'0.0013 s 뒤',M:'1.28 s 뒤'};
  function table2(){
    $('t2').innerHTML=`<thead><tr><th>신청자</th><th>사는 곳</th><th class="r">낸 시각</th><th>거래소 도착</th></tr></thead><tbody>`+
      tsOrder.map(o=>`<tr><td>${dot(o.w)}${o.id}</span></td><td>${PLACE[o.w]}</td><td class="r num">${o.t} μs</td><td>${ARRTXT[o.w]}</td></tr>`).join('')+'</tbody>';
  }
  function nl2(done){
    const L=150,R=930, X1=t=>L+t/100*(R-L);
    const XB=v=>v<1000?L+v/100*300:v<1e6?L+350+(v-1300)/100*190:L+590+(v-1.28e6)/100*190;
    const y1=62,y2=182;
    let g=`<text x="12" y="${y1+5}" font-size="14" font-weight="700" fill="${COL.ink}">낸 순간</text>
      <text x="12" y="${y2+5}" font-size="14" font-weight="700" fill="${COL.ink}">거래소 도착</text>
      <line x1="${L}" x2="${R}" y1="${y1}" y2="${y1}" stroke="${COL.muted}" stroke-width="2"/>`;
    for(let v=0;v<=100;v+=20)g+=`<line x1="${X1(v)}" x2="${X1(v)}" y1="${y1}" y2="${y1+6}" stroke="${COL.muted}"/><text x="${X1(v)}" y="${y1+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${v}${v===100?' μs':''}</text>`;
    [[L,L+300,'0','100 μs'],[L+350,L+540,'1.30 ms','1.40 ms'],[L+590,L+780,'1.28 s','']].forEach(([x1,x2,a,b2])=>{
      g+=`<line x1="${x1}" x2="${x2}" y1="${y2}" y2="${y2}" stroke="${COL.muted}" stroke-width="2"/>
        <text x="${x1}" y="${y2+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${a}</text>${b2?`<text x="${x2}" y="${y2+34}" font-size="12" fill="${COL.muted}" text-anchor="middle">${b2}</text>`:''}`});
    [L+325,L+565].forEach(x=>g+=`<text x="${x}" y="${y2+6}" font-size="18" fill="${COL.muted}" text-anchor="middle">≈</text>`);
    g+=`<text x="${(L+350+L+540)/2}" y="${y2+54}" font-size="12" fill="${COL.muted}" text-anchor="middle">정거장: 0.0013 s 뒤</text>
        <text x="${L+685}" y="${y2+54}" font-size="12" fill="${COL.muted}" text-anchor="middle">달: 1.28 s 뒤 (약 1000배 더 늦음)</text>`;
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
    if(alt===400){g=3.5;sv=-28.3;n=-24.8}
    $('altV').textContent=alt.toLocaleString()+' km';
    $('barsS').innerHTML=barRow('중력 효과',g,60,COL.gold,sgn(g)+' μs')+barRow('속도 효과',sv,60,'#8b9bf0',sgn(sv)+' μs')+barRow('<b>합계</b>',n,60,n<0?COL.S:COL.ok,'<b>'+sgn(n)+' μs</b>');
    $('barsM').innerHTML=barRow('지구 중력에서 멀어짐',59.1,60,COL.gold,'크게 +')+barRow('달 자체의 중력',-2.7,60,'#b9a07a','조금 −')+barRow('느린 공전 속도',-0.5,60,'#8b9bf0','조금 −')+barRow('<b>합계</b>',58.7,60,COL.M,'<b>+58.7 μs</b>');
    document.querySelectorAll('[data-alt]').forEach(b=>b.classList.toggle('sel',+b.dataset.alt===alt));
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
  const off=w=>RATE[w]*days;
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
    const d=days<0.05?1:days;
    if(days<0.05){$('days4').textContent='1.0'}
    const rec=ORD.map(o=>{const of=RATE[o.w]*d;return {...o,of,rec:o.t+of}});
    const key=corr4?'t':'rec';
    const byKey=[...rec].sort((a,b)=>a[key]-b[key]);
    const win=new Set(byKey.slice(0,SLOTS).map(o=>o.id));
    const fair=new Set([...rec].sort((a,b)=>a.t-b.t).slice(0,SLOTS).map(o=>o.id));
    const L=170,R=930,hi=110, X=v=>L+v/hi*(R-L), y1=70,y2=200;
    const recWin=new Set([...rec].sort((a,b)=>a.rec-b.rec).slice(0,SLOTS).map(o=>o.id));
    let s=`<text x="10" y="${y1-4}" font-size="14" font-weight="700" fill="#555c68">낸 시각</text><text x="10" y="${y1+14}" font-size="12" fill="${COL.muted}">(그곳 시계)</text>
      <text x="10" y="${y2-4}" font-size="14" font-weight="700" fill="${COL.ok}">낸 시각</text><text x="10" y="${y2+14}" font-size="12" fill="${COL.muted}">(지구 시계로 환산)</text>`;
    [y1,y2].forEach(y=>{s+=`<line x1="${L}" x2="${R}" y1="${y}" y2="${y}" stroke="${COL.muted}" stroke-width="2"/>`;
      for(let v=0;v<=hi;v+=10)s+=`<line x1="${X(v)}" x2="${X(v)}" y1="${y}" y2="${y+6}" stroke="${COL.muted}"/>${v%20===0?`<text x="${X(v)}" y="${y+40}" font-size="12" fill="${COL.muted}" text-anchor="middle">${v}${v===100?' μs':''}</text>`:''}`});
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

if os.path.exists(html_path):
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception:
        html_content = DEFAULT_HTML
else:
    html_content = DEFAULT_HTML


# ── PDF 생성 함수 (ReportLab 기반) ──────────────────────────────────
def build_space_exchange_pdf(data: dict) -> bytes:
    if not HAS_REPORTLAB:
        return b""

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        topMargin=13 * mm,
        bottomMargin=13 * mm
    )

    W = 182 * mm
    NAVY = colors.HexColor("#1A365D")
    BLUE_HEAD = colors.HexColor("#EBF3FA")
    YELLOW_SOFT = colors.HexColor("#FFFBEB")
    GREEN_SOFT = colors.HexColor("#ECFDF5")
    RED_SOFT = colors.HexColor("#FEF2F2")
    GRAY_LINE = colors.HexColor("#CBD5E1")

    # 글꼴 매핑 (NG가 없으면 기본 헬베티카 사용)
    font_body = "NG" if "NG" in pdfmetrics.getRegisteredFontNames() else "Helvetica"
    font_bold = "NGB" if "NGB" in pdfmetrics.getRegisteredFontNames() else font_body

    P = lambda size=9, bold=False, color="#1E293B", align=0, lead=None: ParagraphStyle(
        name="style_" + str(size) + "_" + str(bold) + "_" + str(align),
        fontName=font_bold if bold else font_body,
        fontSize=size,
        leading=lead or size * 1.38,
        textColor=colors.HexColor(color) if isinstance(color, str) else color,
        alignment=align,
        wordWrap="CJK"
    )

    esc = lambda s: xml.sax.saxutils.escape(str(s)).replace("\n", "<br/>")

    elements = []

    # 1. 문서 헤더
    header_data = [
        [
            Paragraph("💹 2026 사곡고 2학년 역학과 에너지 융합 탐구 활동지", P(8.5, False, "#64748B")),
            Paragraph("성취기준 [12역학01-08] 중력 시간 지연의 적용", P(8.5, False, "#64748B", 2))
        ]
    ]
    t_header = Table(header_data, colWidths=[W * 0.55, W * 0.45])
    t_header.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(t_header)

    elements.append(Spacer(1, 1.5 * mm))
    elements.append(Paragraph("우주 거래소의 시계: 모둠 탐구 활동 보고서", P(16, True, "#0F2942", 1, 20)))
    elements.append(Paragraph("거리에 따른 신호 지연과 상대론적 중력·속도 시간 지연을 고려한 공정한 금융 시장 규칙 탐구", P(8.5, False, "#475569", 1)))
    elements.append(Spacer(1, 2.5 * mm))

    # 모둠 메타 정보 표
    meta = data.get("meta", {})
    cls_txt = meta.get("cls", "2학년 O반")
    grp_txt = meta.get("group", "1모둠")
    mem_txt = meta.get("members", "모둠원 명단")
    dt_txt = meta.get("date", "2026-10-29")

    meta_table_data = [
        [
            Paragraph("<b>학급</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(cls_txt), P(8.5, False, align=1)),
            Paragraph("<b>모둠명</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(grp_txt), P(8.5, False, align=1)),
            Paragraph("<b>모둠원</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(mem_txt), P(8.5, False)),
            Paragraph("<b>작성일</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(dt_txt), P(8.5, False, align=1))
        ]
    ]
    t_meta = Table(meta_table_data, colWidths=[14*mm, 20*mm, 15*mm, 20*mm, 15*mm, 58*mm, 16*mm, 24*mm])
    t_meta.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, GRAY_LINE),
        ('BACKGROUND', (0,0), (0,-1), BLUE_HEAD),
        ('BACKGROUND', (2,0), (2,-1), BLUE_HEAD),
        ('BACKGROUND', (4,0), (4,-1), BLUE_HEAD),
        ('BACKGROUND', (6,0), (6,-1), BLUE_HEAD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t_meta)
    elements.append(Spacer(1, 4 * mm))

    def section_title(num_str, title_str):
        p = Paragraph(f"<b>{esc(num_str)} {esc(title_str)}</b>", P(10.5, True, "#1A365D"))
        t = Table([[p]], colWidths=[W])
        t.setStyle(TableStyle([
            ('LINEBELOW', (0,0), (-1,-1), 1.2, NAVY),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        return t

    # ── [문항 1] 낸 시각 환산 표
    elements.append(section_title("1.", "낸 시각 환산 및 체결 순위 계산 (1~3위 구매)"))
    elements.append(Paragraph(
        "공식: <b>낸 시각(지구 시계로 환산) = 낸 시각(그곳 시계) − (그곳 시계가 앞선 시간)</b><br/>"
        "<font color='#64748B'>※ 1일 경과 후: 달 기지 시계는 +58.7 μs 앞서고, 우주 정거장 시계는 −24.8 μs 뒤처집니다. (사곡전자 300주, 1인당 100주)</font>",
        P(8, False, "#334155")
    ))
    elements.append(Spacer(1, 1.5 * mm))

    q1_rows = data.get("q1_table", [])
    q1_headers = ["신청자", "사는 곳", "낸 시각 (그곳 시계)", "환산 계산 과정", "지구 환산 시각", "환산 순위", "체결 여부"]
    t1_data = [[Paragraph(f"<b>{esc(h)}</b>", P(8, True, "#1A365D", 1)) for h in q1_headers]]

    for r in q1_rows:
        is_buy = "구매" in str(r[6]) or "성공" in str(r[6]) or str(r[5]).strip() in ["1", "2", "3", "1위", "2위", "3위"]
        row_cells = [
            Paragraph(f"<b>{esc(r[0])}</b>", P(8.5, True, align=1)),
            Paragraph(esc(r[1]), P(8, False, align=1)),
            Paragraph(esc(r[2]), P(8, False, align=1)),
            Paragraph(esc(r[3]), P(8, False, align=1)),
            Paragraph(f"<b>{esc(r[4])}</b>", P(8.5, True, "#1A365D" if is_buy else "#334155", 1)),
            Paragraph(f"<b>{esc(r[5])}</b>", P(8.5, True, "#059669" if is_buy else "#64748B", 1)),
            Paragraph(f"<b>{esc(r[6])}</b>", P(8.5, True, "#059669" if is_buy else "#DC2626", 1)),
        ]
        t1_data.append(row_cells)

    t1 = Table(t1_data, colWidths=[18*mm, 28*mm, 31*mm, 43*mm, 25*mm, 18*mm, 19*mm])
    t1_style = [
        ('GRID', (0,0), (-1,-1), 0.4, GRAY_LINE),
        ('BACKGROUND', (0,0), (-1,0), BLUE_HEAD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 2),
        ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]
    for i, r in enumerate(q1_rows):
        rank_str = str(r[5]).replace("위","").strip()
        if rank_str in ["1", "2", "3"]:
            t1_style.append(('BACKGROUND', (0, i+1), (-1, i+1), GREEN_SOFT))
    t1.setStyle(TableStyle(t1_style))
    elements.append(t1)
    elements.append(Spacer(1, 3.5 * mm))

    # ── [문항 2] 체결 결과 비교 표
    elements.append(section_title("2.", "지구 시계로 환산 후 다시 체결하고, 환산 전과 비교"))
    elements.append(Paragraph("그곳 시계에 찍힌 시각 그대로 체결했을 때와, 지구 시계로 환산해 체결했을 때의 결과를 비교합니다.", P(8, False, "#64748B")))
    elements.append(Spacer(1, 1.5 * mm))

    q2 = data.get("q2_table", {})
    t2_headers = ["구분", "사는 사람 (1~3위)", "손해 본 사람 (먼저 냈는데 못 삼)", "이득 본 사람 (늦게 냈는데 삼)"]
    t2_data = [
        [Paragraph(f"<b>{esc(h)}</b>", P(8, True, "#1A365D", 1)) for h in t2_headers],
        [
            Paragraph("<b>환산 전<br/>(그곳 시계 그대로)</b>", P(8, True, align=1)),
            Paragraph(esc(q2.get("before_buyers", "나, 다, 마")), P(8.5, True, "#059669", 1)),
            Paragraph(esc(q2.get("before_losers", "가, 라 (실제 1위·3위)")), P(8.5, True, "#DC2626", 1)),
            Paragraph(esc(q2.get("before_gainers", "다, 마 (실제 5위·4위)")), P(8.5, True, "#D97706", 1)),
        ],
        [
            Paragraph("<b>환산 후<br/>(지구 시계 환산)</b>", P(8, True, align=1)),
            Paragraph(esc(q2.get("after_buyers", "가, 나, 라")), P(8.5, True, "#059669", 1)),
            Paragraph(esc(q2.get("after_losers", "없음 (공정 체결)")), P(8.5, False, "#475569", 1)),
            Paragraph(esc(q2.get("after_gainers", "없음 (부당 이득 없음)")), P(8.5, False, "#475569", 1)),
        ]
    ]
    t2 = Table(t2_data, colWidths=[36*mm, 48*mm, 49*mm, 49*mm])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, GRAY_LINE),
        ('BACKGROUND', (0,0), (-1,0), BLUE_HEAD),
        ('BACKGROUND', (0,1), (0,-1), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (1,1), (1,1), YELLOW_SOFT),
        ('BACKGROUND', (2,1), (2,1), RED_SOFT),
        ('BACKGROUND', (3,1), (3,1), YELLOW_SOFT),
        ('BACKGROUND', (1,2), (-1,2), GREEN_SOFT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 3.5 * mm))

    # ── [문항 3] 주가 상승 시 손실액 계산
    elements.append(section_title("3.", "주가 상승 시 손해 본 사람이 놓친 이익 계산"))
    q3 = data.get("q3", {})
    calc_formula = q3.get("formula", "100주 × ( 1,000 )원 = ( 100,000 )원 (10만 원)")
    calc_note = q3.get("note", "공정하게 배정받았다면 주당 1,000원씩 총 10만 원의 수익을 실현할 수 있었으나, 시계 불일치로 손실 발생")

    t3_box_data = [
        [
            Paragraph("<b>상황</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph("사곡전자 주문가: <b>50,000원</b> → 체결 직후 시장 가격: <b>51,000원</b>으로 상승 (+1,000원/주, 100주)", P(8.5, False))
        ],
        [
            Paragraph("<b>계산식</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(f"<b>{esc(calc_formula)}</b>", P(9.5, True, "#B45309"))
        ],
        [
            Paragraph("<b>결과 분석</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(calc_note), P(8.5, False, "#334155"))
        ]
    ]
    t3_box = Table(t3_box_data, colWidths=[24*mm, W - 24*mm])
    t3_box.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, GRAY_LINE),
        ('BACKGROUND', (0,0), (0,-1), BLUE_HEAD),
        ('BACKGROUND', (1,1), (1,1), YELLOW_SOFT),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t3_box)
    elements.append(Spacer(1, 4 * mm))

    # ── [문항 4] 경제금융 통합질문 (토의 및 평가)
    elements.append(section_title("4.", "[경제·금융 통합] 체결 방식의 공정성 비교 및 모둠 토의"))
    elements.append(Paragraph("세 가지 체결 방법의 특징과 문제점을 분석하고, 가장 공정하다고 생각하는 방식을 선택하여 근거를 서술하시오.", P(8, False, "#64748B")))
    elements.append(Spacer(1, 1.5 * mm))

    q4 = data.get("q4", {})
    choice_val = q4.get("choice", "③ 공통 시간 기준(지구 시계)으로 환산")

    t4_headers = ["체결 방법", "이 방법이면 사는 사람", "문제점 (한계점)", "우리 모둠 선택 (○)"]
    m1_sel = "● 선택" if "①" in choice_val or "도착" in choice_val else "○"
    m2_sel = "● 선택" if "②" in choice_val or "각자" in choice_val else "○"
    m3_sel = "● 선택" if "③" in choice_val or "공통" in choice_val else "○"

    t4_data = [
        [Paragraph(f"<b>{esc(h)}</b>", P(8, True, "#1A365D", 1)) for h in t4_headers],
        [
            Paragraph("<b>① 거래소에<br/>도착한 순서</b>", P(8, True, align=1)),
            Paragraph(esc(q4.get("m1_buyers", "나, 마, 다 (지구·정거장)")), P(8, False, align=1)),
            Paragraph(esc(q4.get("m1_problem", "달 → 지구: 빛으로 약 1.3 s 늦게 도착하여 물리적 통신 지연에 따른 지리적 불평등 발생 (달 거주자는 항상 실패)")), P(7.8, False)),
            Paragraph(f"<b>{m1_sel}</b>", P(9, True, "#1A365D" if "●" in m1_sel else "#94A3B8", 1)),
        ],
        [
            Paragraph("<b>② 각자 시계에<br/>찍힌 시각</b>", P(8, True, align=1)),
            Paragraph(esc(q4.get("m2_buyers", "나, 다, 마")), P(8, False, align=1)),
            Paragraph(esc(q4.get("m2_problem", "중력과 속도에 따른 시간 지연으로 시계 빠르기가 다름. 시계가 느리게 흐르는 곳(정거장)이 부당 이득을 얻고 달이 피해를 봄")), P(7.8, False)),
            Paragraph(f"<b>{m2_sel}</b>", P(9, True, "#1A365D" if "●" in m2_sel else "#94A3B8", 1)),
        ],
        [
            Paragraph("<b>③ 공통 시간 기준<br/>(지구 시계) 환산</b>", P(8, True, align=1)),
            Paragraph(esc(q4.get("m3_buyers", "가, 나, 라 (실제 순서)")), P(8, False, align=1)),
            Paragraph(esc(q4.get("m3_problem", "각 관측지별 상대론적 시차를 실시간으로 환산·검증할 표준시 제정 및 신뢰성 있는 인프라/합의 기구 구축이 요구됨")), P(7.8, False)),
            Paragraph(f"<b>{m3_sel}</b>", P(9, True, "#059669" if "●" in m3_sel else "#94A3B8", 1)),
        ]
    ]
    t4 = Table(t4_data, colWidths=[33*mm, 35*mm, 90*mm, 24*mm])
    t4_style = [
        ('GRID', (0,0), (-1,-1), 0.4, GRAY_LINE),
        ('BACKGROUND', (0,0), (-1,0), BLUE_HEAD),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]
    if "●" in m3_sel:
        t4_style.append(('BACKGROUND', (0, 3), (-1, 3), GREEN_SOFT))
    elif "●" in m2_sel:
        t4_style.append(('BACKGROUND', (0, 2), (-1, 2), YELLOW_SOFT))
    elif "●" in m1_sel:
        t4_style.append(('BACKGROUND', (0, 1), (-1, 1), YELLOW_SOFT))
    t4.setStyle(TableStyle(t4_style))
    elements.append(t4)
    elements.append(Spacer(1, 3 * mm))

    # 서술형 답안 박스
    reason_txt = q4.get("reason", "").strip() or "(모둠 서술 내용)"
    authority_txt = q4.get("authority", "").strip() or "(모둠 서술 내용)"

    disc_box_data = [
        [
            Paragraph("<b>선택 근거<br/>(모둠 토의)</b>", P(8.5, True, "#1A365D", 1)),
            Paragraph(esc(reason_txt), P(8.5, False, lead=12))
        ],
        [
            Paragraph("<b>공통 시간 기준은<br/>누가 만들어야 할까?</b>", P(8, True, "#1A365D", 1)),
            Paragraph(esc(authority_txt), P(8.5, False, lead=12))
        ]
    ]
    t_disc = Table(disc_box_data, colWidths=[33*mm, W - 33*mm])
    t_disc.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.4, GRAY_LINE),
        ('BACKGROUND', (0,0), (0,-1), BLUE_HEAD),
        ('BACKGROUND', (1,0), (1,-1), YELLOW_SOFT),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_disc)

    # 풋터
    elements.append(Spacer(1, 3.5 * mm))
    footer_text = Paragraph(
        "사곡고등학교 물리학 학습 포털 | 2026학년도 역학과 에너지 | "
        "우주거래소 모둠별 발표 게시판(패들렛): https://padlet.com/sgh/padlet-s024y3iekcz0b0xn6dtu",
        P(7.5, False, "#64748B", 1)
    )
    elements.append(footer_text)

    doc.build(elements)
    return buffer.getvalue()


# ── 메인 탭 구성 ────────────────────────────────────────────────
tab_sim, tab_report, tab_theory = st.tabs([
    "🎮 1. 가상 실험실 (인터랙티브 시뮬레이션)",
    "📝 2. 모둠 탐구 활동 보고서 (작성 및 PDF 출력)",
    "💡 3. 핵심 물리학 & 경제학 원리 정리"
])

# ══════════════════════════════════════════════════════════════════
# [TAB 1] 가상 실험실 시뮬레이션
# ══════════════════════════════════════════════════════════════════
with tab_sim:
    components.html(html_content, height=1650, scrolling=True)

    st.markdown("---")
    sim_nav_col1, sim_nav_col2 = st.columns([3, 1])
    with sim_nav_col1:
        st.info("👉 **실험과 관찰을 마쳤다면!** 상단의 **'📝 2. 모둠 탐구 활동 보고서 (작성 및 PDF 출력)'** 탭을 클릭하여 보고서를 작성하고 PDF로 출력하여 패들렛에 제출하세요.")
    with sim_nav_col2:
        st.link_button("🪐 패들렛 제출방 바로가기 ↗", PADLET_URL, use_container_width=True, type="primary")


# ══════════════════════════════════════════════════════════════════
# [TAB 2] 모둠 탐구 활동 보고서 (작성 및 PDF 출력)
# ══════════════════════════════════════════════════════════════════
with tab_report:
    st.subheader("📝 우주 거래소 모둠 탐구 활동 보고서")
    st.markdown(
        "가상 실험실의 관찰 데이터를 바탕으로 모둠원들과 토의하여 아래 질문에 답하고, "
        "작성 완료 후 **PDF 보고서로 다운로드**받아 **모둠별 발표 게시판(패들렛)**에 제출하세요."
    )

    # 기본 모범/예시 데이터
    DEFAULT_Q1_DATA = [
        {"신청자": "가", "사는 곳": "달 기지", "낸 시각 (그곳 시계)": "78.7 μs", "환산 계산 과정": "78.7 − 58.7", "지구 환산 시각": "20.0 μs", "환산 순위": "1위", "체결 여부": "구매 성공 (1위)"},
        {"신청자": "나", "사는 곳": "지구", "낸 시각 (그곳 시계)": "35.0 μs", "환산 계산 과정": "35.0 − 0 (기준)", "지구 환산 시각": "35.0 μs", "환산 순위": "2위", "체결 여부": "구매 성공 (2위)"},
        {"신청자": "라", "사는 곳": "달 기지", "낸 시각 (그곳 시계)": "98.7 μs", "환산 계산 과정": "98.7 − 58.7", "지구 환산 시각": "40.0 μs", "환산 순위": "3위", "체결 여부": "구매 성공 (3위)"},
        {"신청자": "마", "사는 곳": "지구", "낸 시각 (그곳 시계)": "45.0 μs", "환산 계산 과정": "45.0 − 0 (기준)", "지구 환산 시각": "45.0 μs", "환산 순위": "4위", "체결 여부": "체결 실패 (4위)"},
        {"신청자": "다", "사는 곳": "우주 정거장", "낸 시각 (그곳 시계)": "35.2 μs", "환산 계산 과정": "35.2 − (−24.8) = 35.2 + 24.8", "지구 환산 시각": "60.0 μs", "환산 순위": "5위", "체결 여부": "체결 실패 (5위)"},
        {"신청자": "바", "사는 곳": "우주 정거장", "낸 시각 (그곳 시계)": "45.2 μs", "환산 계산 과정": "45.2 − (−24.8) = 45.2 + 24.8", "지구 환산 시각": "70.0 μs", "환산 순위": "6위", "체결 여부": "체결 실패 (6위)"},
    ]

    # 세션 상태 초기화
    if "q1_df" not in st.session_state:
        st.session_state["q1_df"] = pd.DataFrame(DEFAULT_Q1_DATA)

    # 상단 도구 버튼
    tbar1, tbar2, tbar3 = st.columns([1.5, 1.5, 3])
    with tbar1:
        if st.button("💡 모범 답안 채우기", use_container_width=True):
            st.session_state["q1_df"] = pd.DataFrame(DEFAULT_Q1_DATA)
            st.session_state["q2_b_buy"] = "나, 다, 마"
            st.session_state["q2_b_lose"] = "가, 라 (실제 1위·3위)"
            st.session_state["q2_b_gain"] = "다, 마 (실제 5위·4위)"
            st.session_state["q2_a_buy"] = "가, 나, 라"
            st.session_state["q2_a_lose"] = "없음 (실제 빠른 순서대로 공정 체결)"
            st.session_state["q2_a_gain"] = "없음 (부당 이득 발생하지 않음)"
            st.session_state["q3_diff"] = "1,000"
            st.session_state["q3_total"] = "100,000"
            st.session_state["q4_choice_idx"] = 2
            st.session_state["q4_reason_txt"] = "금융 시장의 '시간 우선 원칙'이 공정하게 성립하려면, 주문 신호가 거래소에 먼저 닿았거나 각자 시계에 찍힌 숫자가 작은 것이 아니라 '동일한 물리적 기준계에서 실제로 먼저 발생한 사건'에 우선권이 주어져야 합니다. 거리 지연만 보정하고 상대론적 중력·속도 시간 지연을 보정하지 않으면 우주정거장은 부당한 이득을 보고 달은 항상 불리해지는 구조적 왜곡이 발생하므로, 단일한 공통 시간 기준으로 환산하여 체결하는 방법 ③이 가장 공정합니다."
            st.session_state["q4_auth_txt"] = "공통 시간 기준은 특정 행성이나 민간 거래소, 개별 국가가 사익을 추구하기 위해 왜곡하지 못하도록 해야 합니다. 시간 표준은 인류 모두가 평등하게 누려야 할 '순수 공공재(Public Good)'이므로, 국제연합(UN) 산하 국제도량형국(BIPM)이나 전 행성 우주 표준 연합, 각국 우주청(NASA, KARI, ESA 등)의 중립적인 다자간 공공 기구가 제정하고 유지·관리해야 합니다."
            st.rerun()

    with tbar2:
        if st.button("🧹 빈칸으로 초기화", use_container_width=True):
            blank_q1 = [
                {"신청자": "가", "사는 곳": "달 기지", "낸 시각 (그곳 시계)": "78.7 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
                {"신청자": "나", "사는 곳": "지구", "낸 시각 (그곳 시계)": "35.0 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
                {"신청자": "라", "사는 곳": "달 기지", "낸 시각 (그곳 시계)": "98.7 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
                {"신청자": "마", "사는 곳": "지구", "낸 시각 (그곳 시계)": "45.0 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
                {"신청자": "다", "사는 곳": "우주 정거장", "낸 시각 (그곳 시계)": "35.2 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
                {"신청자": "바", "사는 곳": "우주 정거장", "낸 시각 (그곳 시계)": "45.2 μs", "환산 계산 과정": "", "지구 환산 시각": "", "환산 순위": "", "체결 여부": ""},
            ]
            st.session_state["q1_df"] = pd.DataFrame(blank_q1)
            st.session_state["q2_b_buy"] = ""
            st.session_state["q2_b_lose"] = ""
            st.session_state["q2_b_gain"] = ""
            st.session_state["q2_a_buy"] = ""
            st.session_state["q2_a_lose"] = ""
            st.session_state["q2_a_gain"] = ""
            st.session_state["q3_diff"] = ""
            st.session_state["q3_total"] = ""
            st.session_state["q4_reason_txt"] = ""
            st.session_state["q4_auth_txt"] = ""
            st.rerun()

    st.markdown("---")

    # 1. 모둠 및 학생 메타 정보
    st.markdown("#### 👥 0. 모둠 정보 입력")
    m_col1, m_col2, m_col3, m_col4 = st.columns([1.5, 1.5, 3.5, 1.5])
    with m_col1:
        rep_cls = st.text_input("학급 (예: 2학년 3반)", value="2학년 O반", key="meta_cls_in")
    with m_col2:
        rep_grp = st.text_input("모둠명 (예: 1모둠)", value="1모둠", key="meta_grp_in")
    with m_col3:
        rep_mems = st.text_input("모둠원 이름 (쉼표 구분)", value="홍길동, 김철수, 이영희, 박민수", key="meta_mems_in")
    with m_col4:
        rep_date = st.date_input("작성일자", value=date.today(), key="meta_date_in")

    st.markdown("---")

    # 2. [1번 문항] 표 완성하기
    st.markdown("#### 📊 1. 낸 시각 환산 표 완성하기")
    st.markdown(
        "> **공식**: **낸 시각(지구 시계로 환산) = 낸 시각(그곳 시계) − (그곳 시계가 앞선 시간)**  \n"
        "> *위 표를 완성하시오. (사곡전자 300주 · 50,000원 · 1인당 100주씩 · 1~3위가 산다)*"
    )
    st.caption("💡 팁: 달 시계는 하루에 +58.7 μs 앞서므로 앞선 시간을 빼주고, 우주정거장 시계는 하루에 −24.8 μs 뒤처졌으므로 24.8 μs를 더해줍니다.")

    edited_df = st.data_editor(
        st.session_state["q1_df"],
        use_container_width=True,
        num_rows="fixed",
        key="q1_editor"
    )
    st.session_state["q1_df"] = edited_df

    # 1번 문항 실시간 체결 요약 칩
    st.markdown("**🔍 환산 순위 및 구매 판정 미리보기**")
    p_cols = st.columns(6)
    for idx, row in edited_df.iterrows():
        with p_cols[idx]:
            who = row["신청자"]
            place = row["사는 곳"]
            rank = str(row["환산 순위"]).strip()
            is_winner = rank in ["1", "1위", "2", "2위", "3", "3위"]
            st.markdown(
                f"""
                <div style="background:{'#e3f3ea' if is_winner else '#f1f5f9'};
                            border:1.5px solid {'#2f8f5b' if is_winner else '#cbd5e1'};
                            border-radius:10px;padding:8px 6px;text-align:center;">
                    <b style="font-size:1.1rem;color:#1e3a5f;">{who}</b><br/>
                    <span style="font-size:0.78rem;color:#64748b;">{place}</span><br/>
                    <span style="font-size:0.85rem;font-weight:700;color:{'#2f8f5b' if is_winner else '#64748b'};">{rank or '-'}</span><br/>
                    <span style="display:inline-block;margin-top:4px;padding:1px 6px;border-radius:999px;font-size:0.75rem;font-weight:700;background:{'#2f8f5b' if is_winner else '#94a3b8'};color:#fff;">
                        {'구매' if is_winner else '실패'}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # 3. [2번 문항] 환산 전과 환산 후 비교 표
    st.markdown("#### ⚖️ 2. 지구 시계로 환산해 다시 체결하고, 환산 전과 비교하시오")
    st.markdown("그곳 시계에 찍힌 시각 그대로 체결했을 때와, 지구 시계로 환산하여 공정하게 체결했을 때의 구매자 및 손익자를 비교하여 작성하세요.")

    col2_1, col2_2 = st.columns(2)
    with col2_1:
        st.markdown(
            """
            <div style="background:#fef2f2;border-left:4px solid #c0392b;padding:8px 12px;border-radius:0 8px 8px 0;margin-bottom:8px;">
                <b style="color:#c0392b;">환산 전 (그곳 시계 그대로 체결 시)</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        q2_b_buy = st.text_input(
            "사는 사람 (1~3위)",
            value=st.session_state.get("q2_b_buy", "나, 다, 마"),
            key="q2_b_buy_in"
        )
        q2_b_lose = st.text_input(
            "손해 본 사람 (먼저 냈는데 못 삼)",
            value=st.session_state.get("q2_b_lose", "가, 라 (실제 1위·3위)"),
            key="q2_b_lose_in"
        )
        q2_b_gain = st.text_input(
            "이득 본 사람 (늦게 냈는데 삼)",
            value=st.session_state.get("q2_b_gain", "다, 마 (실제 5위·4위)"),
            key="q2_b_gain_in"
        )

    with col2_2:
        st.markdown(
            """
            <div style="background:#e3f3ea;border-left:4px solid #2f8f5b;padding:8px 12px;border-radius:0 8px 8px 0;margin-bottom:8px;">
                <b style="color:#2f8f5b;">환산 후 (지구 시계로 환산하여 체결 시)</b>
            </div>
            """,
            unsafe_allow_html=True
        )
        q2_a_buy = st.text_input(
            "사는 사람 (1~3위)",
            value=st.session_state.get("q2_a_buy", "가, 나, 라"),
            key="q2_a_buy_in"
        )
        q2_a_lose = st.text_input(
            "손해 본 사람",
            value=st.session_state.get("q2_a_lose", "없음 (실제 주문 순서대로 공정 체결)"),
            key="q2_a_lose_in"
        )
        q2_a_gain = st.text_input(
            "이득 본 사람",
            value=st.session_state.get("q2_a_gain", "없음 (부당 이득 발생하지 않음)"),
            key="q2_a_gain_in"
        )

    st.markdown("---")

    # 4. [3번 문항] 손실 이익 계산
    st.markdown("#### 💰 3. 주가 상승 시 손해 본 사람의 놓친 이익 계산")
    st.markdown(
        "> **주문 직후 주가가 51,000원으로 오르면, 손해 본 사람은 1인당 얼마의 이익을 놓쳤을까?**  \n"
        "> `100주 × (        )원 = (            )원`"
    )

    q3_col1, q3_col2, q3_col3 = st.columns([1.5, 2, 2.5])
    with q3_col1:
        st.text_input("주문 수량", value="100주", disabled=True)
    with q3_col2:
        q3_diff = st.text_input("1주당 시세 차익 (원)", value=st.session_state.get("q3_diff", "1,000"), key="q3_diff_in")
    with q3_col3:
        q3_total = st.text_input("1인당 놓친 총 이익 (원)", value=st.session_state.get("q3_total", "100,000"), key="q3_total_in")

    q3_note = st.text_area(
        "📝 손실 이익에 대한 모둠 분석 및 의견 서술",
        value=st.session_state.get("q3_note_txt", "가와 라 주민은 실제로 20 μs, 40 μs로 가장 먼저 주문했음에도 달 기지의 중력이 약해 시계가 빠르게 흐른 탓에 기록 시각이 커져 주식을 배정받지 못했습니다. 주가가 1,000원 상승하면서 1인당 100주 × 1,000원 = 10만 원의 정당한 시세 차익을 부당하게 놓치게 되었습니다. 시계의 물리적 오차가 실질적인 경제적 손실로 직결됨을 알 수 있습니다."),
        height=70,
        key="q3_note_in"
    )

    st.markdown("---")

    # 5. [4번 문항] 경제금융 통합질문 (토의 및 평가)
    st.markdown("#### 🏛️ 4. [경제금융 통합질문] 세 가지 체결 방법 중 어느 것이 공정할까?")
    st.markdown("모둠별로 세 가지 체결 방법 중 하나를 고르고, 그 근거와 공통 시간 기준 제정 주체를 토의하여 작성하세요.")

    # 방법 비교 안내 카드
    st.markdown("""
| 체결 방법 | 이 방법이면 사는 사람 | 문제점 및 한계 |
| :--- | :--- | :--- |
| **① 거래소에 도착한 순서** | **나, 마, 다** (지구·정거장) | **달 → 지구: 빛으로 약 1.3 s 늦게 도착**하여 물리적 통신 지연에 따른 지리적 불평등 발생 (달 거주자는 영원히 실패) |
| **② 각자 시계에 찍힌 시각** | **나, 다, 마** | 중력과 속도에 따른 시간 지연으로 시계 빠르기가 다름. 시계가 느리게 흐르는 우주정거장이 부당 이득을 보고, 달 기지가 피해를 봄 |
| **③ 공통 시간 기준(지구 시계)으로 환산** | **가, 나, 라** (실제 빠른 순서) | 각 관측지별 상대론적 시차를 실시간 환산·검증할 표준시 제정 및 신뢰성 있는 인프라/합의 기구 구축이 요구됨 |
""")

    q4_methods = [
        "① 거래소에 도착한 순서",
        "② 각자 시계에 찍힌 시각",
        "③ 공통 시간 기준(지구 시계)으로 환산"
    ]
    cur_idx = st.session_state.get("q4_choice_idx", 2)
    q4_choice = st.radio("우리 모둠의 선택 (○)", q4_methods, index=cur_idx, key="q4_choice_in")

    q4_reason = st.text_area(
        "📌 선택 근거 (모둠 발표 내용):",
        value=st.session_state.get("q4_reason_txt", "시장 경제의 '시간 우선 원칙'은 단순히 신호가 거래소에 일찍 닿았거나 각자 시계에 찍힌 숫자가 작은 것이 아니라, '동일한 물리적 기준계에서 실제로 먼저 발생한 사건'에 우선권이 주어져야 진정한 공정성이 실현됩니다. 거리 지연만 보정하고 상대론적 중력·속도 시간 지연을 보정하지 않으면 우주정거장은 항상 유리하고 달은 항상 불리해지는 구조적 왜곡이 발생하므로, 단일한 공통 시간 기준으로 환산하여 체결하는 방법 ③이 가장 공정합니다."),
        height=100,
        key="q4_reason_in"
    )

    q4_auth = st.text_area(
        "🏛️ 공통 시간 기준은 누가 만들어야 할까?:",
        value=st.session_state.get("q4_auth_txt", "공통 시간 기준은 특정 행성이나 민간 거래소, 개별 국가가 사익을 추구하기 위해 왜곡하지 못하도록 해야 합니다. 시간 표준은 인류 모두가 평등하게 누려야 할 '순수 공공재(Public Good)'이므로, 국제연합(UN) 산하 국제도량형국(BIPM)이나 전 행성 우주 표준 연합, 각국 우주청(NASA, KARI, ESA 등)의 중립적인 다자간 공공 기구가 제정하고 유지·관리해야 합니다."),
        height=90,
        key="q4_auth_in"
    )

    st.markdown("---")

    # 6. 보고서 PDF 출력 및 제출 섹션
    st.subheader("📤 보고서 출력 및 제출")

    # PDF 데이터 취합
    pdf_payload = {
        "meta": {
            "cls": rep_cls,
            "group": rep_grp,
            "members": rep_mems,
            "date": str(rep_date)
        },
        "q1_table": [
            [
                row["신청자"],
                row["사는 곳"],
                row["낸 시각 (그곳 시계)"],
                row["환산 계산 과정"],
                row["지구 환산 시각"],
                row["환산 순위"],
                row["체결 여부"]
            ]
            for _, row in edited_df.iterrows()
        ],
        "q2_table": {
            "before_buyers": q2_b_buy,
            "before_losers": q2_b_lose,
            "before_gainers": q2_b_gain,
            "after_buyers": q2_a_buy,
            "after_losers": q2_a_lose,
            "after_gainers": q2_a_gain
        },
        "q3": {
            "formula": f"100주 × ( {q3_diff} )원 = ( {q3_total} )원",
            "note": q3_note
        },
        "q4": {
            "choice": q4_choice,
            "m1_buyers": "나, 마, 다 (지구·정거장)",
            "m1_problem": "달 → 지구: 빛으로 약 1.3 s 늦게 도착하여 거리 지연에 따른 지리적 불평등 발생",
            "m2_buyers": "나, 다, 마",
            "m2_problem": "중력과 속도에 따른 시간 지연으로 시계 빠르기가 달라 정거장이 부당 이득을 보고 달이 피해를 봄",
            "m3_buyers": "가, 나, 라 (실제 순서)",
            "m3_problem": "각 관측지별 상대론적 시차를 실시간 환산·검증할 표준시 제정 및 신뢰성 있는 인프라 구축 필요",
            "reason": q4_reason,
            "authority": q4_auth
        }
    }

    # 다운로드 및 인쇄 버튼 영역
    btn_col1, btn_col2 = st.columns([1.5, 1])

    with btn_col1:
        if HAS_REPORTLAB:
            try:
                pdf_bytes = build_space_exchange_pdf(pdf_payload)
                safe_cls = rep_cls.replace(" ", "_")
                safe_grp = rep_grp.replace(" ", "_")
                file_name = f"우주거래소_탐구보고서_{safe_cls}_{safe_grp}.pdf"

                st.download_button(
                    label="⬇️ 📄 모둠 탐구 활동 보고서 PDF 다운로드",
                    data=pdf_bytes,
                    file_name=file_name,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"PDF 생성 중 오류가 발생했습니다: {e}")
        else:
            st.warning("⚠️ ReportLab 라이브러리가 없어 PDF 직접 다운로드가 비활성화되었습니다. 우측 브라우저 인쇄 기능을 이용해 PDF로 저장하세요.")

    with btn_col2:
        is_print_mode = st.toggle("🖨️ 브라우저 직접 인쇄 / PDF 저장 모드", value=False)

    if is_print_mode:
        st.markdown(
            """
            <div style="background:#ffffff;border:2px solid #1e3a5f;border-radius:12px;padding:24px;margin-top:16px;box-shadow:0 4px 12px rgba(0,0,0,0.08);">
                <div style="text-align:center;border-bottom:2px solid #1e3a5f;padding-bottom:12px;margin-bottom:16px;">
                    <h2 style="margin:0;color:#1e3a5f;">💹 우주 거래소의 시계: 모둠 탐구 활동 보고서</h2>
                    <p style="margin:4px 0 0 0;font-size:0.9rem;color:#64748b;">거리에 따른 신호 지연과 상대론적 중력·속도 시간 지연을 고려한 공정한 금융 시장 규칙 탐구</p>
                </div>
                <table style="width:100%;border-collapse:collapse;margin-bottom:16px;font-size:0.9rem;">
                    <tr style="background:#f1f5f9;">
                        <th style="border:1px solid #cbd5e1;padding:6px;width:12%;">학급</th>
                        <td style="border:1px solid #cbd5e1;padding:6px;width:18%;">""" + rep_cls + """</td>
                        <th style="border:1px solid #cbd5e1;padding:6px;width:12%;">모둠명</th>
                        <td style="border:1px solid #cbd5e1;padding:6px;width:18%;">""" + rep_grp + """</td>
                        <th style="border:1px solid #cbd5e1;padding:6px;width:14%;">작성일자</th>
                        <td style="border:1px solid #cbd5e1;padding:6px;width:26%;">""" + str(rep_date) + """</td>
                    </tr>
                    <tr>
                        <th style="border:1px solid #cbd5e1;padding:6px;background:#f1f5f9;">모둠원</th>
                        <td colspan="5" style="border:1px solid #cbd5e1;padding:6px;">""" + rep_mems + """</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🖨️ 인쇄 대화상자 실행 (PDF로 저장하기)", use_container_width=True):
            components.html("<script>parent.window.print()</script>", height=0)

    # ── 패들렛 제출 연결 배너 카드 ─────────────────────────────────
    st.markdown(
        f"""
        <div style="background:linear-gradient(135deg, #0f2b48 0%, #1a365d 100%);
                    border-radius:14px;padding:22px 24px;margin-top:24px;color:#ffffff;
                    box-shadow:0 6px 18px rgba(15,43,72,0.25);border:1px solid #2e4d75;">
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
                <span style="font-size:1.8rem;">🪐</span>
                <div>
                    <h3 style="margin:0;color:#ffffff;font-size:1.25rem;font-weight:800;">
                        우주거래소 모둠별 발표 게시판 (패들렛)
                    </h3>
                    <p style="margin:2px 0 0 0;font-size:0.88rem;color:#cbd5e1;">
                        작성 완료한 보고서 PDF를 아래 패들렛 게시판에 등록해 모둠별 탐구 결과를 공유하세요.
                    </p>
                </div>
            </div>
            <div style="background:rgba(255,255,255,0.08);border-radius:8px;padding:12px 16px;margin:12px 0;font-size:0.9rem;line-height:1.6;">
                <b>📌 보고서 제출 방법 (3단계)</b><br/>
                1. 상단의 <b>[⬇️ 모둠 탐구 활동 보고서 PDF 다운로드]</b> 버튼을 눌러 PDF 파일을 저장합니다.<br/>
                2. 아래 <b>[패들렛 게시판 바로가기]</b> 버튼을 눌러 새 탭에서 패들렛을 엽니다.<br/>
                3. 자신의 <b>모둠 카드(+)</b>를 클릭하고, 제목에 <code>[학급] 모둠명 - 모둠원</code>을 적은 뒤 다운로드한 <b>PDF 파일</b>을 첨부합니다.
            </div>
            <div style="margin-top:14px;text-align:right;">
                <a href="{PADLET_URL}" target="_blank" rel="noopener noreferrer"
                   style="display:inline-block;background:#c9a96e;color:#0f2942;font-weight:800;
                          font-size:1rem;padding:10px 22px;border-radius:8px;text-decoration:none;
                          box-shadow:0 3px 8px rgba(0,0,0,0.2);transition:all 0.2s;">
                    🚀 우주거래소 모둠별 발표 게시판 열기 ↗
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ══════════════════════════════════════════════════════════════════
# [TAB 3] 핵심 물리학 & 경제학 원리 정리
# ══════════════════════════════════════════════════════════════════
with tab_theory:
    st.subheader("💡 우주 거래소의 시계 핵심 원리 및 배경 지식")

    st.markdown("""
### 1. 거리에 따른 시간 차 (신호 지연)
- **빛의 속력 한계**: 신호는 진공에서 약 $c = 300,000\\text{ km/s}$로 이동합니다.
  - 지구-우주정거장(고도 약 400 km): 신호 지연 $\\Delta t = 400 / 300,000 \\approx 0.0013\\text{ s}$
  - 지구-달 기지(거리 약 384,000 km): 신호 지연 $\\Delta t = 384,000 / 300,000 \\approx 1.28\\text{ s}$
- **거리 보정**: 신호가 도달하는 데 걸린 시간($\\Delta t = d / c$)을 미리 알고 있다면, 신호를 받는 순간 그 시간을 더해 거래소와 시계를 한 번에 맞출 수 있습니다.

---

### 2. 상대성에 따른 시간 차 (중력 효과와 속도 효과)
시계를 한 번 맞춰도, 위치한 곳의 중력과 운동 상태에 따라 **시간이 흐르는 빠르기** 자체가 달라집니다.

1. **우주 정거장 (ISS, 고도 400 km)**
   - **중력 효과** (약한 중력): 지구 표면보다 중력이 약해 시계가 빨라짐 ($+3.5\\ \\mu\\text{s}/\\text{일}$)
   - **속도 효과** (빠른 공전 $v \\approx 7.7\\text{ km/s}$): 특수 상대성 이론에 의해 시계가 느려짐 ($-28.3\\ \\mu\\text{s}/\\text{일}$)
   - **합계**: 속도 효과가 더 커서 하루에 **약 $-24.8\\ \\mu\\text{s}$ 느려짐**

2. **달 기지 (Moon Base)**
   - **지구 중력 탈출 효과**: 지구의 깊은 중력 퍼텐셜 우물에서 멀리 벗어남 ($+59.1\\ \\mu\\text{s}/\\text{일}$)
   - **달 자체 중력 및 공전**: 달의 질량과 느린 공전 속도 ($-3.2\\ \\mu\\text{s}/\\text{일}$)
   - **합계**: 하루에 **약 $+58.7\\ \\mu\\text{s}$ 빨라짐** (NASA 달 표준시 공식 발표값)

---

### 3. 경제·사회적 의미와 공공재로서의 시간 기준
- **희소성과 가격·시간 우선의 원칙**:
  - 주문 수량(600주)이 매도 수량(300주)보다 많을 때, 동일한 가격에서는 먼저 주문한 사람에게 우선 배정하는 것이 자본시장의 공정한 규칙입니다.
- **상대성 보정이 없으면 생기는 금융 왜곡**:
  - 각자의 시계에 찍힌 시각을 그대로 사용하면, 시간이 느리게 가는 우주정거장은 부당하게 이득을 보고, 시간이 빠르게 흐르는 달 기지는 먼저 주문하고도 손해를 보게 됩니다.
- **공공재(Public Good)로서의 우주 표준시**:
  - GPS 위성이 하루 약 $38\\ \\mu\\text{s}$의 상대론적 오차를 보정하지 않으면 하루 11 km 이상의 위치 오차가 누적되는 것처럼, 우주 시대의 통신과 금융에서도 단일한 기준계로 환산하는 **공통 표준시(공공재)**가 필수적입니다.
""")

st.caption("사곡고등학교 물리학 학습 포털 | 2026학년도 역학과 에너지 가상실험실")
