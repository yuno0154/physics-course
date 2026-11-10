import streamlit as st
import streamlit.components.v1 as components


def run_sim():
    """단진동 수업용 시뮬레이션 (명시적 지도 1차시용, 탭형).
    A. 복원력(가로 용수철) → ① 복원력 F-x(세로) → ② 위치 x-t → ③ 속도 v-t → ④ 가속도 a-t → ⑤ 위상 · a-x → ⑥ 주기 T
    - 원운동 물체 P의 위치·속도·가속도 벡터의 세로 성분이 스크린의 그림자가 되고, 그 값이 그래프로 그려집니다.
    - 외부 CDN(React/Babel/Tailwind)을 쓰지 않는 순수 HTML/JS 이므로 학교 네트워크에서도 동작합니다.
    """
    st.title("〰️ 단진동: 복원력 · 그림자 사영 · 주기")
    components.html(HTML, height=1600, scrolling=True)


HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  :root{--ink:#0f172a;--sub:#64748b;--line:#e2e8f0;--bg:#f8fafc;--x:#2563eb;--v:#059669;--a:#e11d48;--f:#9333ea;--key:#1d4ed8}
  *{box-sizing:border-box}
  body{margin:0;font-family:"Pretendard","Malgun Gothic","Apple SD Gothic Neo",sans-serif;color:var(--ink);background:transparent}
  #app{max-width:1120px;margin:0 auto;padding:6px 4px 20px}
  h1{font-size:20px;margin:4px 0 2px}
  .lead{font-size:13px;color:var(--sub);margin:0 0 8px}
  .tabs{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0 10px}
  .tab{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font-size:14px;font-weight:700;color:var(--sub);cursor:pointer;font-family:inherit}
  .tab:hover{border-color:#94a3b8}
  .tab.on{background:var(--key);border-color:var(--key);color:#fff}
  .card{background:#fff;border:1px solid var(--line);border-radius:18px;padding:10px 14px}

  .ctrl{display:flex;flex-wrap:wrap;gap:10px 20px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:9px 16px;margin-bottom:10px}
  .grp{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600}
  .ctrl input[type=range]{width:110px}
  .val{min-width:58px;font-variant-numeric:tabular-nums;color:var(--key);font-weight:800}
  .btn{border:1px solid var(--line);background:#fff;border-radius:10px;padding:6px 12px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;color:var(--ink)}
  .btn:hover{background:var(--bg)}
  .btn.primary{background:#0f172a;color:#fff;border-color:#0f172a}
  .btn.on{background:#eff6ff;border-color:#93c5fd;color:#1e3a8a}
  .derived{margin-left:auto;font-size:13px;font-weight:700}
  .derived b{color:var(--key);font-variant-numeric:tabular-nums}

  .view{display:none}
  #app.vH #viewH,#app.vA #viewA,#app.vB #viewB,#app.vC #viewC{display:block}
  #app.vH #viewH,#app.vA #viewA{display:grid}
  svg{display:block}
  #svB{width:100%;height:auto}
  .keys{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px;align-items:center;font-size:12px;color:var(--sub)}
  .keys .btn{font-size:12px;padding:5px 10px}

  #viewH{grid-template-columns:minmax(0,1.42fr) minmax(0,1fr);gap:14px;align-items:start}
  @media(max-width:860px){#viewH{grid-template-columns:1fr}}
  .hcol{display:grid;gap:12px}
  .ws-list{margin:6px 0 0;padding:0;list-style:none;font-size:13.5px;line-height:1.85;color:#1e293b}
  .ws-list li{margin-bottom:8px;padding:8px 10px;background:#f8fafc;border:1px solid var(--line);border-radius:10px}
  .blank-pill{display:inline-block;min-width:64px;padding:1px 10px;margin:0 2px;border:1.5px dashed #9333ea;border-radius:6px;background:#faf5ff;color:#9333ea;font-weight:800;font-size:13px;text-align:center;cursor:pointer;user-select:none;transition:all .15s}
  .blank-pill:hover{background:#f3e8ff}
  .blank-pill.on{border-style:solid;background:#9333ea;color:#fff}
  .ans-box{cursor:pointer}
  .ans-box rect{transition:fill .15s,stroke .15s}
  .ans-box:hover rect{fill:#f3e8ff}

  #viewA{grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:14px;align-items:start}
  @media(max-width:760px){#viewA{grid-template-columns:1fr}}
  #viewC{display:none}
  .cgrid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:14px;align-items:start}
  @media(max-width:860px){.cgrid{grid-template-columns:1fr}}
  .gt{display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:var(--sub);margin-bottom:2px;flex-wrap:wrap;gap:6px}
  .ovt label{margin-right:12px;font-size:12px;font-weight:700;cursor:pointer}

  .info{margin-top:10px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px}
  @media(max-width:860px){.info{grid-template-columns:1fr}}
  .info h2{font-size:16px;margin:0 0 6px}
  .keysent{background:#eff6ff;border-radius:12px;padding:9px 12px;font-size:14px;font-weight:700;color:#1e3a8a;line-height:1.6;margin:4px 0 8px}
  .given{background:#fefce8;border:1px solid #fde68a;border-radius:12px;padding:8px 12px;font-size:13px;line-height:1.7;color:#713f12;margin:0 0 8px}
  .lab{font-size:12px;font-weight:800;color:var(--sub);margin:8px 0 3px}
  ul.rd{margin:0;padding-left:18px;font-size:13px;line-height:1.7}
  .formula{font-family:"Times New Roman","Batang",serif;font-size:20px;line-height:1.9}
  .formula div{white-space:nowrap;overflow-x:auto}
  .formula .blue{color:var(--key);font-weight:700}
  .formula sub{font-size:13px}
  .sqrt .rad{border-top:1.5px solid currentColor;padding:0 2px}
  .fbox{border:1px dashed #cbd5e1;border-radius:12px;padding:8px 12px;margin-top:4px}
  .fhide{color:var(--sub);font-size:13px;padding:10px 0}
  ul.sy{margin:4px 0 0;padding-left:18px;font-size:13px;line-height:1.7;color:#334155}
  .note{font-size:12px;color:var(--sub);margin:8px 0 0;line-height:1.6}
  .obs details{border-bottom:1px dashed var(--line)}
  .obs summary{cursor:pointer;font-size:13px;font-weight:600;padding:3px 0}
  .obs .ans{color:var(--key);font-weight:700;font-size:13px;padding:2px 0 6px 14px}
  .split{font-size:13px;font-variant-numeric:tabular-nums;color:#334155;margin-top:6px}

  .read{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-top:10px}
  @media(max-width:700px){.read{grid-template-columns:repeat(3,1fr)}}
  .read div{background:#fff;border:1px solid var(--line);border-radius:12px;padding:6px 10px;font-size:12px;color:var(--sub)}
  .read b{display:block;font-size:17px;font-variant-numeric:tabular-nums;margin-top:1px}
</style>
</head>
<body>
<div id="app" class="vH">
  <h1>단진동 : 복원력 · 그림자 사영 · 주기</h1>
  <p class="lead">맨 앞의 [A. 복원력(가로 용수철)]부터 ① → ⑥ 순서로 누르며 수업합니다. ②~④는 원운동 물체 P의 벡터를 스크린에 비춘 그림자가 그래프로 그려집니다.</p>

  <div class="tabs" id="tabs">
    <button class="tab on" data-step="0">A. 복원력 (가로 용수철)</button>
    <button class="tab" data-step="1">① 복원력 F–x (세로)</button>
    <button class="tab" data-step="2">② 위치 x–t</button>
    <button class="tab" data-step="3">③ 속도 v–t</button>
    <button class="tab" data-step="4">④ 가속도 a–t</button>
    <button class="tab" data-step="5">⑤ 위상 · a–x</button>
    <button class="tab" data-step="6">⑥ 주기 T</button>
  </div>

  <div class="ctrl">
    <div class="grp">
      <button class="btn primary" id="play">⏸ 정지</button>
      <button class="btn" id="reset">↺ 처음으로</button>
      <select class="btn" id="speed"><option value="1">속도 ×1</option><option value="0.5">속도 ×0.5</option><option value="0.25">속도 ×0.25</option></select>
    </div>
    <div class="grp">진폭 A <input type="range" id="rA" min="0.3" max="1" step="0.05" value="0.8"><span class="val" id="vA"></span></div>
    <div class="grp cw">각속도 ω <input type="range" id="rw" min="0.6" max="3.4" step="0.1" value="2"><span class="val" id="vw"></span></div>
    <div class="grp cmk">질량 m <input type="range" id="rm" min="0.5" max="4" step="0.5" value="1"><span class="val" id="vm"></span></div>
    <div class="grp cmk">용수철 상수 k <input type="range" id="rk" min="2" max="12" step="0.5" value="4"><span class="val" id="vk"></span></div>
    <div class="grp cghost"><label style="cursor:pointer"><input type="checkbox" id="ghost"> 전체 곡선 미리 보기</label></div>
    <div class="derived" id="derived"></div>
  </div>

  <!-- ===== 뷰 H : 가로 용수철 복원력 + 학습지 A. ①~③ 비교 + F–x 그래프 (0) ===== -->
  <div class="view" id="viewH">
    <div class="hcol">
      <div class="card">
        <div class="gt">
          <span style="color:var(--ink);font-size:13px">실시간 수평 용수철 진자 (평형점 O 기준, 오른쪽 +)</span>
          <span id="hStateTag" style="color:var(--f)"></span>
        </div>
        <svg id="svH" viewBox="0 0 580 186" style="width:100%;height:auto">
          <defs>
            <marker id="hMF" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#9333ea"/></marker>
            <marker id="hMX" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2563eb"/></marker>
          </defs>
          <!-- 바닥면 및 왼쪽 벽 -->
          <line x1="24" y1="132" x2="556" y2="132" stroke="#94a3b8" stroke-width="2"/>
          <rect x="18" y="28" width="8" height="106" rx="2" fill="#334155"/>
          <!-- -A, 평형점 O, +A 기준선 -->
          <line id="hLineMinA" x1="162" y1="30" x2="162" y2="144" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
          <text id="hTxtMinA" x="162" y="23" text-anchor="middle" font-size="11.5" font-weight="700" fill="#64748b">x = −A</text>
          <line x1="290" y1="26" x2="290" y2="168" stroke="#2563eb" stroke-width="1.8" stroke-dasharray="5 4"/>
          <text x="290" y="19" text-anchor="middle" font-size="12.5" font-weight="800" fill="#2563eb">평형점 O (x = 0)</text>
          <line id="hLinePlusA" x1="418" y1="30" x2="418" y2="144" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4"/>
          <text id="hTxtPlusA" x="418" y="23" text-anchor="middle" font-size="11.5" font-weight="700" fill="#64748b">x = +A</text>
          <!-- 수평 용수철 및 물체 m -->
          <polyline id="hSpring" points="" fill="none" stroke="#334155" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"/>
          <rect id="hMass" x="264" y="80" width="52" height="52" rx="4" fill="#e2e8f0" stroke="#334155" stroke-width="2.5"/>
          <text id="hMassT" x="290" y="111" text-anchor="middle" font-size="16" font-weight="800" fill="#0f172a">m</text>
          <!-- 복원력 F 화살표 (보라색) -->
          <line id="haF" x1="290" y1="54" x2="290" y2="54" stroke="#9333ea" stroke-width="5" stroke-linecap="round" marker-end="url(#hMF)"/>
          <text id="htF" x="290" y="42" text-anchor="middle" font-size="12.5" font-weight="800" fill="#9333ea" stroke="#fff" stroke-width="4" paint-order="stroke"></text>
          <!-- 변위 x 화살표 (파란색) -->
          <line id="haX" x1="290" y1="154" x2="290" y2="154" stroke="#2563eb" stroke-width="3.5" stroke-linecap="round" marker-end="url(#hMX)"/>
          <circle cx="290" cy="154" r="3.5" fill="#2563eb"/>
          <text id="htX" x="290" y="176" text-anchor="middle" font-size="12" font-weight="800" fill="#2563eb"></text>
        </svg>
        <div class="keys" style="justify-content:space-between">
          <div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center">
            <span>위치 바로가기:</span>
            <button class="btn" data-ph="0.75">① x = −A (압축)</button>
            <button class="btn" data-ph="0">② x = 0 (평형점 O)</button>
            <button class="btn" data-ph="0.25">③ x = +A (늘어남)</button>
          </div>
          <div style="display:flex;align-items:center;gap:6px">
            <span>직접 끌기(x):</span>
            <input type="range" id="rxH" min="-1" max="1" step="0.01" value="0" style="width:120px">
          </div>
        </div>
      </div>

      <!-- 학습지 A 그림 ①~③ 비교 카드 -->
      <div class="card">
        <div class="gt" style="align-items:center;margin-bottom:6px">
          <span style="color:var(--ink);font-size:13px">학습지 [A] 그림 ①~③ — 위치별 복원력 F의 방향과 크기 (빈칸을 클릭해 보세요)</span>
          <button class="btn" id="hShowAll" style="padding:4px 10px;font-size:12px">빈칸 정답 모두 보기</button>
        </div>
        <svg id="svH3" viewBox="0 0 580 282" style="width:100%;height:auto">
          <defs>
            <marker id="h3F" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#9333ea"/></marker>
            <marker id="h3X1" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M10 0L0 5L10 10Z" fill="#2563eb"/></marker>
            <marker id="h3X2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2563eb"/></marker>
          </defs>
          <!-- 왼쪽 벽 -->
          <rect x="18" y="18" width="6" height="232" fill="#334155"/>
          <!-- 바닥선 3개 -->
          <line x1="24" y1="82" x2="430" y2="82" stroke="#94a3b8" stroke-width="1.4"/>
          <line x1="24" y1="164" x2="430" y2="164" stroke="#94a3b8" stroke-width="1.4"/>
          <line x1="24" y1="246" x2="430" y2="246" stroke="#94a3b8" stroke-width="1.4"/>
          <!-- 평형점 O 점선 -->
          <line x1="225" y1="18" x2="225" y2="254" stroke="#2563eb" stroke-width="1.6" stroke-dasharray="4 4"/>
          <text x="225" y="13" text-anchor="middle" font-size="11.5" font-weight="800" fill="#2563eb">평형점 O</text>

          <!-- ① x = -A -->
          <text x="32" y="34" font-size="12" font-weight="800" fill="#0f172a">① x = −A</text>
          <polyline id="h3Sp1" points="" fill="none" stroke="#334155" stroke-width="2" stroke-linejoin="round"/>
          <rect id="h3M1" x="123" y="40" width="42" height="42" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
          <text id="h3T1" x="144" y="66" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0f172a">m</text>
          <line id="h3F1" x1="170" y1="61" x2="218" y2="61" stroke="#9333ea" stroke-width="4" stroke-linecap="round" marker-end="url(#h3F)"/>
          <text x="380" y="47" font-size="11.5" font-weight="700" fill="#9333ea">F의 방향</text>
          <text x="380" y="73" font-size="11.5" font-weight="700" fill="#9333ea">F의 크기</text>
          <g class="ans-box" data-b="0"><rect x="434" y="31" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb0" x="503" y="47" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>
          <g class="ans-box" data-b="1"><rect x="434" y="57" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb1" x="503" y="73" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>

          <!-- ② x = 0 (평형점 O) -->
          <text x="32" y="116" font-size="12" font-weight="800" fill="#0f172a">② x = 0 (평형점 O)</text>
          <polyline id="h3Sp2" points="" fill="none" stroke="#334155" stroke-width="2" stroke-linejoin="round"/>
          <rect id="h3M2" x="204" y="122" width="42" height="42" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
          <text id="h3T2" x="225" y="148" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0f172a">m</text>
          <text x="380" y="129" font-size="11.5" font-weight="700" fill="#9333ea">F의 방향</text>
          <text x="380" y="155" font-size="11.5" font-weight="700" fill="#9333ea">F의 크기</text>
          <g class="ans-box" data-b="2"><rect x="434" y="113" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb2" x="503" y="129" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>
          <g class="ans-box" data-b="3"><rect x="434" y="139" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb3" x="503" y="155" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>

          <!-- ③ x = +A -->
          <text x="32" y="198" font-size="12" font-weight="800" fill="#0f172a">③ x = +A</text>
          <polyline id="h3Sp3" points="" fill="none" stroke="#334155" stroke-width="2" stroke-linejoin="round"/>
          <rect id="h3M3" x="285" y="204" width="42" height="42" fill="#e2e8f0" stroke="#334155" stroke-width="2"/>
          <text id="h3T3" x="306" y="230" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0f172a">m</text>
          <line id="h3F3" x1="280" y1="225" x2="232" y2="225" stroke="#9333ea" stroke-width="4" stroke-linecap="round" marker-end="url(#h3F)"/>
          <text x="380" y="211" font-size="11.5" font-weight="700" fill="#9333ea">F의 방향</text>
          <text x="380" y="237" font-size="11.5" font-weight="700" fill="#9333ea">F의 크기</text>
          <g class="ans-box" data-b="4"><rect x="434" y="195" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb4" x="503" y="211" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>
          <g class="ans-box" data-b="5"><rect x="434" y="221" width="138" height="23" rx="3" fill="#fff" stroke="#475569" stroke-width="1.5"/><text id="hb5" x="503" y="237" text-anchor="middle" font-size="12" font-weight="800" fill="#9333ea"></text></g>

          <!-- 하단 변위 x (오른쪽 +) 화살표 -->
          <line x1="228" y1="260" x2="302" y2="260" stroke="#2563eb" stroke-width="2" marker-start="url(#h3X1)" marker-end="url(#h3X2)"/>
          <text x="265" y="276" text-anchor="middle" font-size="11.5" font-weight="800" fill="#2563eb">변위 x (오른쪽 +)</text>
        </svg>
      </div>
    </div>

    <div class="hcol">
      <div class="card">
        <div class="gt"><span style="color:var(--f)">복원력–변위 그래프 (F–x, 오른쪽 +)</span><span id="fxhs"></span></div>
        <svg id="gFxH" viewBox="0 0 320 250" style="width:100%;height:auto;max-width:380px;margin:0 auto"></svg>
      </div>
      <div class="card">
        <div class="gt" style="align-items:center">
          <span style="color:var(--ink);font-size:13px">A. 용수철 진자에 작용하는 힘에는 어떤 특징이 있을까?</span>
          <span style="font-size:11.5px;color:var(--f)">빈칸 클릭</span>
        </div>
        <ul class="ws-list">
          <li><b>① 용수철 진자:</b> 용수철에 매단 물체가 <b>평형점 O</b>를 중심으로 왕복하는 장치. 평형점에서 물체까지의 위치를 변위 <i>x</i>라 하고 <b>오른쪽을 (+)</b>로 한다.</li>
          <li><b>② 복원력의 특징:</b> 그림 ①~③에서 용수철이 물체에 작용하는 복원력 <i>F</i>의 방향은 항상 <span class="blank-pill" data-ws="0" data-ans="평형점 O">? (클릭)</span>을(를) 향하고, 크기는 변위의 크기 |<i>x</i>|에 <span class="blank-pill" data-ws="1" data-ans="비례">? (클릭)</span>한다.</li>
          <li><b>③ 복원력의 식:</b> 복원력을 식으로 쓰면 <i>F</i> = −(<span class="blank-pill" data-ws="2" data-ans="k (용수철 상수)">?</span>)<i>x</i> 이다. 식의 (−) 부호는 <span class="blank-pill" data-ws="3" data-ans="복원력의 방향이 변위 x와 반대 방향임">? (클릭)</span>을(를) 뜻한다.</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- ===== 뷰 A : 용수철 + 그래프 (① ⑥) ===== -->
  <div class="view" id="viewA">
    <div class="card">
      <svg id="svA" viewBox="0 0 330 520" style="width:100%;height:auto;max-width:300px;margin:0 auto">
        <defs>
          <marker id="aF" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#9333ea"/></marker>
          <marker id="aA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#e11d48"/></marker>
          <marker id="aS" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#ea580c"/></marker>
          <marker id="aG" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#475569"/></marker>
        </defs>
        <line x1="16" y1="250" x2="316" y2="250" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6 5"/>
        <text x="318" y="268" text-anchor="end" font-size="13" font-weight="700" fill="#475569">평형점 O</text>
        <rect x="140" y="24" width="60" height="9" rx="3" fill="#94a3b8"/>
        <polyline id="aSpring" points="" fill="none" stroke="#475569" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
        <rect id="aMass" x="148" y="0" width="44" height="34" rx="9" fill="#334155"/>
        <text id="aMassT" x="170" y="0" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">m</text>
        <line id="aDl" x1="250" y1="250" x2="250" y2="250" stroke="#2563eb" stroke-width="3"/>
        <line x1="242" y1="250" x2="258" y2="250" stroke="#2563eb" stroke-width="2"/>
        <line id="aDt" x1="242" y1="0" x2="258" y2="0" stroke="#2563eb" stroke-width="2"/>
        <text id="aDx" x="262" y="0" font-size="12" font-weight="800" fill="#2563eb"></text>
        <line id="aaS" stroke="#ea580c" stroke-width="5" stroke-linecap="round" marker-end="url(#aS)"/>
        <line id="aaG" stroke="#475569" stroke-width="5" stroke-linecap="round" marker-end="url(#aG)"/>
        <line id="aaF" stroke="#9333ea" stroke-width="5" stroke-linecap="round" marker-end="url(#aF)"/>
        <line id="aaA" stroke="#e11d48" stroke-width="5" stroke-linecap="round" marker-end="url(#aA)"/>
        <text id="atS" stroke="#fff" stroke-width="4" paint-order="stroke" font-size="12" font-weight="800" fill="#ea580c" text-anchor="middle">탄성력</text>
        <text id="atG" stroke="#fff" stroke-width="4" paint-order="stroke" font-size="12" font-weight="800" fill="#475569" text-anchor="middle">중력</text>
        <text id="atF" stroke="#fff" stroke-width="4" paint-order="stroke" font-size="12" font-weight="800" fill="#9333ea" text-anchor="middle">F</text>
        <text id="atA" stroke="#fff" stroke-width="4" paint-order="stroke" font-size="12" font-weight="800" fill="#e11d48" text-anchor="middle">a</text>
      </svg>
      <div class="keys">
        <button class="btn" data-ph="0">평형점</button><button class="btn" data-ph="0.25">+A</button><button class="btn" data-ph="0.5">평형점</button><button class="btn" data-ph="0.75">−A</button>
      </div>
      <div class="keys" id="splitRow"><button class="btn" id="splitBtn">힘 나누어 보기 (중력 + 탄성력)</button></div>
    </div>
    <div>
      <div class="card" id="boxFx"><div class="gt"><span style="color:var(--f)">복원력–변위 그래프 (F–x)</span><span id="fxs"></span></div><svg id="gFx" viewBox="0 0 320 250" style="width:100%;height:auto;max-width:380px;margin:0 auto"></svg></div>
      <div class="card" id="boxXt"><div class="gt"><span style="color:var(--x)">변위–시간 그래프 (x–t)</span><span id="xts"></span></div><svg id="gXt" viewBox="0 0 440 150" style="width:100%;height:auto"></svg></div>
    </div>
  </div>

  <!-- ===== 뷰 B : 원운동 + 스크린 + 그래프 (② ③ ④) ===== -->
  <div class="view card" id="viewB">
    <svg id="svB" viewBox="0 0 900 440">
      <defs>
        <marker id="bBl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#2563eb"/></marker>
        <marker id="bGr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#059669"/></marker>
        <marker id="bRd" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#e11d48"/></marker>
      </defs>
    </svg>
    <div class="keys">
      <span>P 위치 바로가기:</span>
      <button class="btn" data-ph="0">θ=0 (평형점 높이)</button><button class="btn" data-ph="0.25">θ=90° (맨 위)</button><button class="btn" data-ph="0.5">θ=180°</button><button class="btn" data-ph="0.75">θ=270° (맨 아래)</button>
    </div>
  </div>

  <!-- ===== 뷰 C : 비교 + a–x (⑤) ===== -->
  <div class="view" id="viewC">
    <div class="cgrid">
      <div class="card">
        <div class="gt"><span>x–t · v–t · a–t 겹쳐 보기 (각각 최댓값으로 나눈 모양)</span>
          <span class="ovt"><label style="color:var(--x)"><input type="checkbox" id="ox" checked> x</label><label style="color:var(--v)"><input type="checkbox" id="ov"> v</label><label style="color:var(--a)"><input type="checkbox" id="oa" checked> a</label></span></div>
        <svg id="gOv" viewBox="0 0 520 260" style="width:100%;height:auto"></svg>
      </div>
      <div class="card">
        <div class="gt"><span style="color:var(--a)">가속도–변위 그래프 (a–x)</span><span id="axs"></span></div>
        <svg id="gAx" viewBox="0 0 320 250" style="width:100%;height:auto;max-width:380px;margin:0 auto"></svg>
      </div>
    </div>
  </div>

  <!-- ===== 설명 ===== -->
  <div class="info">
    <div class="card">
      <h2 id="iTitle"></h2>
      <div class="keysent" id="iKey"></div>
      <div class="given" id="iGiven"></div>
      <div class="lab">그래프(그림) 읽기</div>
      <ul class="rd" id="iRead"></ul>
      <p class="note" id="iNote"></p>
      <div class="split" id="splitInfo"></div>
    </div>
    <div class="card">
      <div style="display:flex;align-items:center;justify-content:space-between"><div class="lab" style="margin:0">식과 기호의 뜻</div><button class="btn" id="fbtn">식 확인하기</button></div>
      <div id="iFormula"></div>
      <div class="lab">확인 질문 (클릭하면 답이 보입니다)</div>
      <div class="obs" id="iObs"></div>
    </div>
  </div>

  <div class="read">
    <div>시간 t<b id="rt"></b></div>
    <div>위상 θ = ωt<b id="rth"></b></div>
    <div style="color:var(--x)">변위 x<b id="rx"></b></div>
    <div style="color:var(--v)">속도 v<b id="rv"></b></div>
    <div style="color:var(--a)">가속도 a<b id="ra"></b></div>
    <div style="color:var(--f)">복원력 F = −kx<b id="rf"></b></div>
  </div>
</div>

<script>
(function(){
  const NS='http://www.w3.org/2000/svg';
  const $=id=>document.getElementById(id);
  function el(tag,attrs,parent){const e=document.createElementNS(NS,tag);for(const k in attrs)e.setAttribute(k,attrs[k]);if(parent)parent.appendChild(e);return e;}
  function clear(g){while(g.firstChild)g.removeChild(g.firstChild);}
  const TMAX=10, G=9.8;
  const S={t:0,playing:true,A:0.8,w:2,m:1,k:4,step:0,speed:1,ghost:false,split:false,fshow:false,ov:{x:true,v:false,a:true},hbox:[false,false,false,false,false,false],ws:[false,false,false,false]};
  const X=t=>S.A*Math.sin(S.w*t), V=t=>S.A*S.w*Math.cos(S.w*t), AC=t=>-S.A*S.w*S.w*Math.sin(S.w*t);
  const T=()=>2*Math.PI/S.w;
  const sg=v=>(v<-0.005?'−':'+')+Math.abs(v).toFixed(2);
  const SQ=i=>'<span class="sqrt">√<span class="rad">'+i+'</span></span>';

  /* ================= 단계 내용 ================= */
  const ST={
   0:{view:'H',title:'A. 용수철 진자에 작용하는 힘의 특징 (가로 용수철)',
      key:'용수철에 매단 물체가 평형점 O를 중심으로 왕복할 때, 용수철이 물체에 작용하는 복원력 F의 방향은 항상 평형점 O를 향하고 크기는 변위의 크기 |x|에 비례한다 (F = −kx).',
      given:'<b>부호 약속</b> 평형점 O에서 물체까지의 위치를 변위 <i>x</i>라 하고, <b>오른쪽을 (+)</b>, <b>왼쪽을 (−)</b>로 정한다.',
      read:[
        '① x = −A (압축): 변위는 왼쪽(−)이고, 복원력 F는 오른쪽(+, 평형점 O 방향), 크기는 kA로 최대',
        '② x = 0 (평형점 O): 용수철이 늘어나지도 압축되지도 않아 복원력 F = 0',
        '③ x = +A (늘어남): 변위는 오른쪽(+)이고, 복원력 F는 왼쪽(−, 평형점 O 방향), 크기는 kA로 최대',
        'F–x 그래프는 원점을 지나는 직선(기울기 −k)이며, 복원력의 크기는 |x|에 비례한다'
      ],
      formula:'<div class="blue">F = −kx</div>',
      sym:[
        'F : 복원력(N) — 물체를 항상 평형점 O로 되돌리려는 힘',
        'k : 용수철 상수(N/m) — 용수철의 뻣뻣한 정도 (F–x 그래프 기울기의 크기)',
        'x : 평형점 O에서의 변위(m), 오른쪽을 (+)로 약속',
        '(−) 부호 : 복원력 F의 방향이 변위 x의 방향과 항상 반대임을 뜻함'
      ],
      note:'학습지 [A]의 그림 ①~③ 빈칸과 오른쪽 정리 문장의 빈칸을 직접 클릭하여 정답을 확인할 수 있습니다. 「직접 끌기(x)」 슬라이더를 움직여 위치별 복원력 화살표를 관찰해 보세요.',
      obs:[
        ['그림 ①(x = −A)에서 복원력 F의 방향과 크기는?','방향: 오른쪽(+, 평형점 O 방향), 크기: kA (최대)'],
        ['그림 ②(x = 0, 평형점 O)에서 복원력 F의 방향과 크기는?','방향: 없음, 크기: 0'],
        ['그림 ③(x = +A)에서 복원력 F의 방향과 크기는?','방향: 왼쪽(−, 평형점 O 방향), 크기: kA (최대)'],
        ['복원력 식 F = −kx에서 (−) 부호가 뜻하는 것은?','힘 F의 방향이 변위 x의 방향과 반대(항상 평형점 O를 향함)']
      ]},
   1:{view:'A',title:'① 복원력과 단진동 — F–x 그래프 (세로 용수철)',
      key:'복원력은 변위와 반대 방향으로 작용하고 크기는 변위에 비례한다. 복원력을 받아 평형점을 중심으로 주기적으로 왕복하는 운동이 단진동이다.',
      read:['F–x 그래프는 원점을 지나는 직선 → 복원력의 크기는 변위에 비례','기울기는 −k : 용수철이 뻣뻣할수록(k↑) 같은 변위에서 복원력이 크다','(+) 변위에서는 (−)힘, (−) 변위에서는 (+)힘 → 항상 평형점 쪽','점이 원점(평형점)에 있을 때 복원력은 0'],
      formula:'<div class="blue">F = −kx</div>',
      sym:['F : 복원력(N) — 물체를 평형점으로 되돌리려는 알짜힘','k : 용수철 상수(N/m) — F–x 그래프 기울기의 크기','x : 평형점에서의 변위(m), 위쪽을 (+)로 약속','(−) : 힘의 방향이 변위와 반대임'],
      note:'수직으로 매단 용수철에서 x는 평형점 기준 변위이고, F는 중력과 탄성력의 합(알짜힘)이다. 「힘 나누어 보기」로 확인한다. 교과서는 아래쪽을 +로 쓰므로 두 가지 표기를 함께 보여 준다.',
      obs:[['x가 +(위쪽)일 때 복원력의 방향은?','−(아래쪽), 평형점을 향한다'],['평형점을 지날 때 복원력의 크기는?','0'],['k가 2배가 되면 F–x 그래프는?','기울기의 크기가 2배, 더 가팔라진다']]},
   2:{view:'B',title:'② 위치의 그림자 — x–t 그래프',
      key:'단진동하는 물체(용수철 진자의 추)의 위치는 등속 원운동하는 물체 P를 옆에서 비춘 그림자의 위치와 같은 꼴이다. 용수철 진자가 실제로 이 식을 따르는지는 ⑥에서 확인한다.',
      given:'<b>알아두기 · 성분</b> 벡터를 세로 방향과 가로 방향으로 나눈 각각을 성분이라 한다. 스크린(세로)에는 세로 성분만 비치며, 그림의 굵은 선이 세로 성분이다.',
      read:['그림자 Q가 오르내린 높이를 시간 순서대로 이으면 x–t 그래프(사인 곡선)','그래프의 최댓값 = 진폭 A (원의 반지름)','곡선이 한 번 반복되는 시간 = 주기 T (P가 한 바퀴 도는 시간)','P가 θ = ωt 만큼 돌았을 때 그림자의 높이 = A sinθ'],
      formula:'<div>x = A sin<i>θ</i> = A sin<i>ωt</i></div><div><i>ω</i> = 2π/T = 2π<i>f</i></div>',
      sym:['A : 진폭 = 원의 반지름(m)','ω : 각속도 — P가 도는 빠르기(rad/s)','θ = ωt : t초 동안 P가 회전한 각(위상)','T : 주기(s), f = 1/T : 진동수(Hz)'],
      note:'ω를 바꾸면 그래프가 촘촘해지거나 늘어나지만 최댓값은 그대로이고, A를 바꾸면 최댓값만 변한다.',
      obs:[['P가 맨 위(θ=90°)에 있을 때 그림자의 변위는?','x = +A (위쪽 끝점)'],['ω를 키우면 그래프는 어떻게 변하나?','주기 T가 짧아져 촘촘해진다. 최댓값 A는 그대로'],['A를 키우면?','최댓값만 커지고 주기 T는 그대로']]},
   3:{view:'B',title:'③ 속도의 그림자 — v–t 그래프',
      key:'P의 속도는 원의 접선 방향이고 크기가 Aω로 일정하다. 이 속도의 세로 성분이 그림자 Q의 속도이다.',
      given:'<b>알아두기</b> 등속 원운동하는 P의 속력은 v = Aω, 방향은 접선이다. (원 둘레 2πA를 주기 T = 2π/ω 동안 가므로 v = 2πA/T) 이 값은 교과서에서 제시한 대로 사용한다.',
      read:['v–t의 최댓값 = Aω (원운동 속력)','P가 평형점 높이(θ=0°, 180°)일 때 접선이 수직 → 세로 성분 최대 → Q의 속력 최대','P가 맨 위·맨 아래(θ=90°, 270°)일 때 접선이 수평 → 세로 성분 0 → Q의 속도 0','x–t 그래프보다 1/4주기(위상 90°) 앞선다'],
      formula:'<div>v<sub>P</sub> = A<i>ω</i> (원운동의 속력)</div><div class="blue">v = A<i>ω</i> cos<i>ωt</i></div>',
      sym:['Aω : 원운동 속력 = 단진동 속력의 최댓값(m/s)','cos ωt : P의 속도 방향에 따른 세로 성분의 비율','v > 0 : 위쪽으로 운동, v < 0 : 아래쪽으로 운동'],
      note:'ω가 클수록(주기가 짧을수록) 같은 진폭에서 최대 속력 Aω가 커진다.',
      obs:[['Q의 속력이 최대인 위치는?','평형점 (v = Aω)'],['Q의 속도가 0인 위치는?','양쪽 끝점 (방향이 바뀌는 순간)'],['v가 (−)인 구간에서 Q는 어느 쪽으로 움직이나?','아래쪽']]},
   4:{view:'B',title:'④ 가속도의 그림자 — a–t 그래프',
      key:'P의 가속도는 중심을 향하는 구심 가속도이고 크기가 Aω²로 일정하다. 이 가속도의 세로 성분이 그림자 Q의 가속도이다.',
      given:'<b>알아두기</b> 등속 원운동하는 P의 가속도(구심 가속도)는 항상 원의 중심을 향하고 크기는 a = Aω²이다. 이 값은 교과서에서 제시한 대로 사용한다.',
      read:['a–t의 최댓값 = Aω² (구심가속도의 크기)','P가 맨 위·맨 아래에 있을 때 구심가속도가 수직 → Q의 가속도 크기 최대(끝점)','P가 평형점 높이에 있을 때 구심가속도가 수평 → 세로 성분 0','x–t와 모양은 같고 부호가 반대(위상 180°) → 위로 변위일 때 가속도는 아래'],
      formula:'<div>a<sub>P</sub> = A<i>ω</i>² (구심가속도)</div><div class="blue">a = −A<i>ω</i>² sin<i>ωt</i></div>',
      sym:['Aω² : 구심가속도 = 단진동 가속도 크기의 최댓값(m/s²)','(−) : 가속도가 항상 변위와 반대 방향(평형점 쪽)','sin ωt : 변위의 모양과 같다 → x와 비례'],
      note:'x = A sinωt 이므로 a = −ω²(A sinωt) = −ω²x 로 정리된다. 다음 탭에서 확인한다.',
      obs:[['Q의 가속도 크기가 최대인 위치는? 그때 속도는?','양쪽 끝점, 속도는 0'],['평형점을 지날 때 가속도는?','0'],['x가 (+)일 때 a의 부호는?','(−): 아래쪽, 평형점 쪽']]},
   5:{view:'C',title:'⑤ 한눈에 정리 — 위상과 a–x 관계',
      key:'단진동하는 물체의 가속도는 변위에 비례하고 방향은 반대이다.',
      read:['x–t와 a–t를 겹치면 위아래가 뒤집힌 모양 → 위상 180° 차이','v–t는 x–t보다 1/4주기 앞선다(위상 90°)','a–x 그래프는 원점을 지나는 직선, 기울기 = −ω²','점이 직선 위를 왕복 → 진폭을 바꾸면 움직이는 범위만 달라지고 기울기는 그대로'],
      formula:'<div>a = −A<i>ω</i>² sin<i>ωt</i> = −<i>ω</i>²(A sin<i>ωt</i>)</div><div class="blue">a = −<i>ω</i>² x</div>',
      sym:['a = −ω²x : 단진동의 조건(가속도 ∝ −변위)','−ω² : a–x 그래프의 기울기','이 식을 만족하는 운동 = 단진동'],
      note:'다음 탭에서 용수철 진자가 이 식을 만족하는지(뉴턴 제2법칙) 확인한다.',
      obs:[['a–x 그래프의 모양과 기울기는?','원점을 지나는 직선, 기울기 −ω²'],['ω를 키우면 기울기는?','더 가팔라진다'],['진폭 A를 바꾸면 기울기는?','변하지 않는다. 점이 움직이는 범위만 달라진다']]},
   6:{view:'A',title:'⑥ 용수철 진자의 주기',
      key:'용수철 진자의 a = −(k/m)x는 ②~④의 그림자와 같은 a = −ω²x 꼴이므로 용수철 진자는 단진동이며 ω² = k/m이다. 주기는 질량이 클수록 크고 용수철 상수가 클수록 작으며, 진폭과는 관계없다.',
      read:['뉴턴 제2법칙에서 F와 a는 같은 방향(화살표 비교) : F = ma','m을 키우면 x–t 그래프가 늘어난다(주기 증가), k를 키우면 촘촘해진다(주기 감소)','A를 바꿔도 그래프의 가로 길이(주기)는 그대로'],
      formula:'<div>F = −kx = ma ⇒ a = −(k/m)x</div><div>a = −<i>ω</i>²x 와 같은 꼴 ⇒ 단진동, <i>ω</i>² = k/m</div><div class="blue">T = 2π/<i>ω</i> = 2π'+SQ('m/k')+'</div>',
      sym:['m : 매단 물체의 질량(kg)','k : 용수철 상수(N/m)','T : 용수철 진자의 주기(s) — A와 g는 식에 없다'],
      note:'수직으로 매단 경우 중력은 평형점의 위치만 아래로 옮길 뿐 주기에는 영향이 없다(①의 「힘 나누어 보기」). 그래서 달에서도 주기가 같다.',
      obs:[['m을 2배로 하면 T는?','√2배 (약 1.41배)'],['k를 4배로 하면 T는?','1/2배'],['진폭 A를 바꾸면 T는?','변하지 않는다 (식에 A가 없다)']]}
  };

  function renderInfo(){
    const d=ST[S.step];
    $('iTitle').textContent=d.title; $('iKey').textContent=d.key;
    $('iGiven').innerHTML=d.given||'';$('iGiven').style.display=d.given?'':'none';
    $('iRead').innerHTML=d.read.map(r=>'<li>'+r+'</li>').join('');
    $('iNote').textContent=d.note;
    S.fshow=false; renderFormula();
    $('iObs').innerHTML=d.obs.map((o,i)=>'<details><summary>'+(i+1)+'. '+o[0]+'</summary><div class="ans">→ '+o[1]+'</div></details>').join('');
  }
  function renderFormula(){
    const d=ST[S.step];
    $('fbtn').textContent=S.fshow?'식 숨기기':'식 확인하기';
    $('iFormula').innerHTML=S.fshow?
      '<div class="fbox formula">'+d.formula+'</div><ul class="sy">'+d.sym.map(s=>'<li>'+s+'</li>').join('')+'</ul>':
      '<div class="fhide">그래프를 보고 먼저 식을 써 본 뒤 「식 확인하기」를 누르세요.</div>';
  }

  /* ================= 그래프 도구 ================= */
  const PL=48,PR=14,PT=10,PB=24,GW=440,GH=150;
  function Graph(svgId,color,withT){
    this.svg=$(svgId);this.color=color;this.withT=withT;
    this.w=GW-PL-PR;this.h=GH-PT-PB;this.mid=PT+this.h/2;
    this.grid=el('g',{},this.svg);
    this.curve=el('polyline',{fill:'none',stroke:color,'stroke-width':3,'stroke-linejoin':'round',opacity:.9},this.svg);
    this.cur=el('line',{y1:PT,y2:GH-PB,stroke:'#94a3b8','stroke-width':1.5,'stroke-dasharray':'4 3'},this.svg);
    this.dot=el('circle',{r:6,fill:color,stroke:'#fff','stroke-width':2.5},this.svg);
  }
  Graph.prototype.redraw=function(fn,maxVal){
    const g=this.grid;clear(g);const mid=this.mid,h=this.h,w=this.w;
    [-1,0,1].forEach(s=>{const y=mid-s*h/2*0.9;el('line',{x1:PL,x2:PL+w,y1:y,y2:y,stroke:s===0?'#94a3b8':'#eef2f7','stroke-width':s===0?1.5:1},g);});
    const lab=(txt,y)=>{const t=el('text',{x:PL-6,y:y+4,'text-anchor':'end','font-size':11,fill:'#64748b'},g);t.textContent=txt;};
    lab('+'+maxVal.toFixed(2),mid-h/2*0.9);lab('0',mid);lab('−'+maxVal.toFixed(2),mid+h/2*0.9);
    for(let s=0;s<=TMAX;s++){const x=PL+s/TMAX*w;el('line',{x1:x,x2:x,y1:GH-PB,y2:GH-PB+4,stroke:'#94a3b8'},g);
      if(s%2===0&&s<10){const t=el('text',{x,y:GH-PB+16,'text-anchor':'middle','font-size':11,fill:'#64748b'},g);t.textContent=s;}}
    const ut=el('text',{x:PL+w,y:GH-PB+16,'text-anchor':'end','font-size':11,fill:'#64748b'},g);ut.textContent='t (s)';
    const Tp=T();
    for(let n=1;n*Tp<=TMAX+1e-9;n++){const x=PL+n*Tp/TMAX*w;
      el('line',{x1:x,x2:x,y1:PT,y2:GH-PB,stroke:'#cbd5e1','stroke-width':1,'stroke-dasharray':'2 3'},g);
      if(this.withT&&n<=3){const t=el('text',{x,y:PT+9,'text-anchor':'middle','font-size':11,fill:'#1d4ed8','font-weight':700},g);t.textContent=(n===1?'T':n+'T');}}
    if(this.withT&&Tp<=TMAX){ // 첫 주기 괄호
      const x1=PL+Tp/TMAX*w;el('line',{x1:PL,x2:x1,y1:GH-PB-6,y2:GH-PB-6,stroke:'#1d4ed8','stroke-width':2},g);
      el('line',{x1:PL,x2:PL,y1:GH-PB-10,y2:GH-PB-2,stroke:'#1d4ed8','stroke-width':2},g);el('line',{x1:x1,x2:x1,y1:GH-PB-10,y2:GH-PB-2,stroke:'#1d4ed8','stroke-width':2},g);
      const t=el('text',{x:(PL+x1)/2,y:GH-PB-11,'text-anchor':'middle','font-size':11,fill:'#1d4ed8','font-weight':800,stroke:'#fff','stroke-width':4,'paint-order':'stroke'},g);t.textContent='T = '+Tp.toFixed(2)+' s';}
    const pts=[];const N=400;
    for(let i=0;i<=N;i++){const t=i/N*TMAX;pts.push((PL+t/TMAX*w).toFixed(1)+','+(mid-fn(t)/maxVal*h/2*0.9).toFixed(1));}
    this.curve.setAttribute('points',pts.join(' '));this.fn=fn;this.maxVal=maxVal;
  };
  Graph.prototype.update=function(t){
    if(!this.fn)return;
    const x=PL+t/TMAX*this.w,y=this.mid-this.fn(t)/this.maxVal*this.h/2*0.9;
    this.cur.setAttribute('x1',x);this.cur.setAttribute('x2',x);this.dot.setAttribute('cx',x);this.dot.setAttribute('cy',y);
  };
  const gXt=new Graph('gXt','#2563eb',true);

  /* XY 그래프 (F–x, a–x) */
  function XY(svgId,o){
    this.o=o;this.svg=$(svgId);const s=this.svg,g=el('g',{},s);
    const cid='clip_'+svgId;const cp=el('clipPath',{id:cid},s);el('rect',{x:o.L,y:o.T,width:o.W-o.L-o.R,height:o.H-o.T-o.B},cp);
    this.px=x=>o.L+(x+o.xm)/(2*o.xm)*(o.W-o.L-o.R);this.py=y=>o.T+(o.ym-y)/(2*o.ym)*(o.H-o.T-o.B);
    el('rect',{x:o.L,y:o.T,width:o.W-o.L-o.R,height:o.H-o.T-o.B,fill:'#fff',stroke:'#e2e8f0'},g);
    el('line',{x1:this.px(0),x2:this.px(0),y1:o.T,y2:o.H-o.B,stroke:'#94a3b8','stroke-width':1.5},g);
    el('line',{x1:o.L,x2:o.W-o.R,y1:this.py(0),y2:this.py(0),stroke:'#94a3b8','stroke-width':1.5},g);
    o.xt.forEach(v=>{const t=el('text',{x:this.px(v),y:o.H-o.B+14,'text-anchor':'middle','font-size':11,fill:'#64748b'},g);t.textContent=v;});
    o.yt.forEach(v=>{const t=el('text',{x:o.L-5,y:this.py(v)+4,'text-anchor':'end','font-size':11,fill:'#64748b'},g);t.textContent=v;});
    const tx=el('text',{x:o.W-o.R,y:o.H-3,'text-anchor':'end','font-size':11,fill:'#2563eb','font-weight':700},g);tx.textContent=o.xlab;
    const ty=el('text',{x:o.L+4,y:o.T+11,'font-size':11,fill:o.color,'font-weight':700},g);ty.textContent=o.ylab;
    this.full=el('line',{stroke:o.light,'stroke-width':2,'clip-path':'url(#'+cid+')'},s);
    this.seg=el('line',{stroke:o.color,'stroke-width':4,'stroke-linecap':'round','clip-path':'url(#'+cid+')'},s);
    this.dot=el('circle',{r:7,fill:o.color,stroke:'#fff','stroke-width':2.5},s);
  }
  XY.prototype.setLine=function(slope,A){
    const o=this.o;
    this.full.setAttribute('x1',this.px(-o.xm));this.full.setAttribute('y1',this.py(-slope*o.xm));this.full.setAttribute('x2',this.px(o.xm));this.full.setAttribute('y2',this.py(slope*o.xm));
    this.seg.setAttribute('x1',this.px(-A));this.seg.setAttribute('y1',this.py(-slope*A));this.seg.setAttribute('x2',this.px(A));this.seg.setAttribute('y2',this.py(slope*A));
  };
  XY.prototype.move=function(x,y){this.dot.setAttribute('cx',this.px(x));this.dot.setAttribute('cy',this.py(y));};
  const xyFH=new XY('gFxH',{W:320,H:250,L:44,R:14,T:12,B:30,xm:1,ym:12.5,xt:[-1,-0.5,0.5,1],yt:[-10,-5,5,10],xlab:'x (m, 오른쪽 +)',ylab:'F (N)',color:'#9333ea',light:'#e9d5ff'});
  const xyF=new XY('gFx',{W:320,H:250,L:44,R:14,T:12,B:30,xm:1,ym:12.5,xt:[-1,-0.5,0.5,1],yt:[-10,-5,5,10],xlab:'x (m)',ylab:'F (N)',color:'#9333ea',light:'#e9d5ff'});
  const xyA=new XY('gAx',{W:320,H:250,L:44,R:14,T:12,B:30,xm:1,ym:12.5,xt:[-1,-0.5,0.5,1],yt:[-10,-5,5,10],xlab:'x (m)',ylab:'a (m/s²)',color:'#e11d48',light:'#fecdd3'});

  /* ================= 뷰 H : 가로 용수철 복원력 (0) ================= */
  const CXH=290, PXH=160;
  function springPtsH(x0,x1,y0,n,amp){
    const p=[];
    const len=x1-x0;
    const pad=Math.min(12,Math.max(4,len*0.08));
    p.push(x0.toFixed(1)+','+y0.toFixed(1));
    p.push((x0+pad).toFixed(1)+','+y0.toFixed(1));
    const inner=len-2*pad;
    for(let j=1;j<=n;j++){
      const x=x0+pad+inner*(j-0.5)/n;
      const y=y0+(j%2?-amp:amp);
      p.push(x.toFixed(1)+','+y.toFixed(1));
    }
    p.push((x1-pad).toFixed(1)+','+y0.toFixed(1));
    p.push(x1.toFixed(1)+','+y0.toFixed(1));
    return p.join(' ');
  }
  function updateH3(){
    const dpx=S.A*102;
    const x1=225-dpx, x2=225, x3=225+dpx;
    $('h3M1').setAttribute('x',x1-21); $('h3T1').setAttribute('x',x1);
    $('h3Sp1').setAttribute('points',springPtsH(24,x1-21,61,14,11));
    $('h3F1').setAttribute('x1',x1+25); $('h3F1').setAttribute('x2',Math.min(222,x1+25+Math.max(24,dpx*0.55)));

    $('h3M2').setAttribute('x',x2-21); $('h3T2').setAttribute('x',x2);
    $('h3Sp2').setAttribute('points',springPtsH(24,x2-21,143,14,11));

    $('h3M3').setAttribute('x',x3-21); $('h3T3').setAttribute('x',x3);
    $('h3Sp3').setAttribute('points',springPtsH(24,x3-21,225,14,11));
    $('h3F3').setAttribute('x1',x3-25); $('h3F3').setAttribute('x2',Math.max(228,x3-25-Math.max(24,dpx*0.55)));

    const fMax=(S.k*S.A).toFixed(1);
    const ans=[
      '오른쪽 (+, O 방향)',
      'kA (최대, '+fMax+' N)',
      '없음',
      '0 (0 N)',
      '왼쪽 (−, O 방향)',
      'kA (최대, '+fMax+' N)'
    ];
    for(let i=0;i<6;i++){
      const on=S.hbox[i];
      const g=document.querySelector('.ans-box[data-b="'+i+'"] rect');
      if(g){
        g.setAttribute('fill',on?'#faf5ff':'#ffffff');
        g.setAttribute('stroke',on?'#9333ea':'#475569');
      }
      $('hb'+i).textContent=on?ans[i]:'? (클릭)';
      $('hb'+i).setAttribute('fill',on?'#7e22ce':'#94a3b8');
    }
    document.querySelectorAll('.blank-pill').forEach(el=>{
      const idx=+el.dataset.ws;
      const on=S.ws[idx];
      el.classList.toggle('on',on);
      el.textContent=on?el.dataset.ans:'? (클릭)';
    });
    const allOn=S.hbox.every(Boolean)&&S.ws.every(Boolean);
    $('hShowAll').textContent=allOn?'빈칸 정답 모두 숨기기':'빈칸 정답 모두 보기';
  }
  function drawH(){
    const x=X(S.t), xm=CXH+x*PXH, F=-S.k*x;
    const minAx=CXH-S.A*PXH, plusAx=CXH+S.A*PXH;
    $('hLineMinA').setAttribute('x1',minAx); $('hLineMinA').setAttribute('x2',minAx); $('hTxtMinA').setAttribute('x',minAx);
    $('hLinePlusA').setAttribute('x1',plusAx); $('hLinePlusA').setAttribute('x2',plusAx); $('hTxtPlusA').setAttribute('x',plusAx);
    $('hSpring').setAttribute('points',springPtsH(26,xm-26,106,14,13));
    $('hMass').setAttribute('x',xm-26);
    $('hMassT').setAttribute('x',xm);
    $('rxH').value=(x/S.A).toFixed(2);

    // 복원력 F 화살표 (수평)
    const LM=115, fLen=(F/(S.k*S.A))*LM;
    if(Math.abs(fLen)<4){
      $('haF').style.display='none';
      $('htF').textContent='F = 0 N (평형점)';
      $('htF').setAttribute('x',CXH);
    }else{
      $('haF').style.display='';
      $('haF').setAttribute('x1',xm);
      $('haF').setAttribute('x2',xm+fLen);
      $('htF').setAttribute('x',xm+fLen*0.5);
      $('htF').textContent='복원력 F = '+sg(F)+' N ('+(F>0?'오른쪽 +':'왼쪽 −')+')';
    }

    // 변위 x 화살표 (수평)
    const xLen=xm-CXH;
    if(Math.abs(xLen)<4){
      $('haX').style.display='none';
      $('htX').setAttribute('x',CXH);
      $('htX').textContent='변위 x = 0.00 m (평형점 O)';
    }else{
      $('haX').style.display='';
      $('haX').setAttribute('x1',CXH);
      $('haX').setAttribute('x2',xm);
      $('htX').setAttribute('x',CXH+xLen*0.5);
      $('htX').textContent='변위 x = '+sg(x)+' m ('+(x>0?'오른쪽 +':'왼쪽 −')+')';
    }

    if(x<-0.35*S.A) $('hStateTag').textContent='용수철 압축 (x < 0) → 복원력 F는 오른쪽(+)';
    else if(x>0.35*S.A) $('hStateTag').textContent='용수철 늘어남 (x > 0) → 복원력 F는 왼쪽(−)';
    else $('hStateTag').textContent='평형점 부근 (x ≈ 0) → 복원력 F ≈ 0';

    xyFH.move(x,F);
  }

  /* ================= 뷰 A : 용수철 ================= */
  const CYA=250,PXA=150;
  function springPts(x0,y0,y1,n,amp){const p=[];for(let j=0;j<=n+1;j++){const y=y0+(y1-y0)*j/(n+1);const x=(j===0||j===n+1)?x0:x0+(j%2?amp:-amp);p.push(x.toFixed(1)+','+y.toFixed(1));}return p.join(' ');}
  function arrow(id,x,y0,lenUp,tid,tx,ty){const e=$(id);if(Math.abs(lenUp)<3){e.style.display='none';if(tid)$(tid).style.display='none';return;}
    e.style.display='';e.setAttribute('x1',x);e.setAttribute('x2',x);e.setAttribute('y1',y0);e.setAttribute('y2',y0-lenUp);
    if(tid){const t=$(tid);t.style.display='';t.setAttribute('x',tx);t.setAttribute('y',lenUp>=0?(y0-lenUp-9):(y0-lenUp+19));}}
  function drawA(){
    const x=X(S.t),ym=CYA-x*PXA;
    $('aSpring').setAttribute('points',springPts(170,33,ym-17,10,14));
    $('aMass').setAttribute('y',ym-17);$('aMassT').setAttribute('y',ym+5);
    $('aDl').setAttribute('y1',CYA);$('aDl').setAttribute('y2',ym);$('aDt').setAttribute('y1',ym);$('aDt').setAttribute('y2',ym);
    $('aDx').setAttribute('y',(CYA+ym)/2+4);$('aDx').textContent='x = '+sg(x)+' m';
    const F=-S.k*x,LM=110;
    const fF=F/(S.k*S.A)*LM;
    arrow('aaF',118,ym,fF,'atF',118,ym-fF-8*Math.sign(fF||1));
    if(S.step===6){const aa=AC(S.t)/(S.A*S.w*S.w)*LM;arrow('aaA',94,ym,aa,'atA',94,ym-aa-8*Math.sign(aa||1));}
    else{$('aaA').style.display='none';$('atA').style.display='none';}
    const split=(S.step===1&&S.split);
    if(split){
      const mg=S.m*G,x0=mg/S.k,Fs=S.k*(x0-x),s=100/(mg+S.k*S.A);
      arrow('aaS',92,ym,Fs*s,'atS',92,ym-Fs*s-8);
      arrow('aaG',66,ym,-mg*s,'atG',66,ym+mg*s+16);
      $('splitInfo').innerHTML='x₀ = mg/k = '+x0.toFixed(2)+' m (평형점에서 늘어난 길이)<br>탄성력 k(x₀−x) = <b style="color:#ea580c">'+Fs.toFixed(2)+' N</b>, 중력 mg = <b style="color:#475569">'+mg.toFixed(2)+' N</b><br>알짜힘 = '+Fs.toFixed(2)+' − '+mg.toFixed(2)+' = <b style="color:#9333ea">'+sg(Fs-mg)+' N</b> = −kx'+
        '<div style="margin-top:6px;padding-top:6px;border-top:1px dashed #e2e8f0"><b>교과서 표기</b> (아래쪽 +, x′ = −x = '+sg(-x)+' m)<br>F = mg − k(x₀+x′) = '+mg.toFixed(2)+' − '+(S.k*(x0-x)).toFixed(2)+' = <b style="color:#9333ea">'+sg(mg-S.k*(x0-x))+' N</b> = −kx′</div>';
    }else{['aaS','aaG','atS','atG'].forEach(i=>$(i).style.display='none');$('splitInfo').innerHTML='';}
    xyF.move(x,F); gXt.update(S.t);
  }

  /* ================= 뷰 B : 원운동 사영 ================= */
  const OX=170,OY=220,SXB=380,GX0=380,GX1=860,PXT=(GX1-GX0)/TMAX,PXM=140;
  const svB=$('svB');
  const bBand=el('rect',{x:366,y:34,width:28,height:372,rx:10,fill:'#fef9c3',opacity:.85},svB);
  const bIcCeil=el('rect',{x:326,y:36,width:28,height:6,rx:3,fill:'#94a3b8'},svB);
  const bIcSpring=el('polyline',{fill:'none',stroke:'#475569','stroke-width':2.5,'stroke-linejoin':'round'},svB);
  const bIcMass=el('rect',{x:326,y:0,width:28,height:26,rx:7,fill:'#334155'},svB);
  const bIcT=el('text',{x:340,y:0,'text-anchor':'middle','font-size':12,'font-weight':800,fill:'#fff'},svB);bIcT.textContent='m';
  const bIcL=el('text',{x:340,y:30,'text-anchor':'middle','font-size':10,fill:'#64748b'},svB);bIcL.textContent='용수철 진자';
  const bGrid=el('g',{},svB);
  el('line',{x1:16,y1:OY,x2:884,y2:OY,stroke:'#94a3b8','stroke-width':1.5},svB);
  const bRing=el('circle',{cx:OX,cy:OY,r:100,fill:'#f8fafc',stroke:'#cbd5e1','stroke-width':2},svB);
  el('line',{x1:OX,y1:OY-155,x2:OX,y2:OY+155,stroke:'#e2e8f0','stroke-width':1.5},svB);
  const bGhost=el('polyline',{fill:'none','stroke-width':2.5,'stroke-dasharray':'5 5',opacity:.35},svB);
  const bTrace=el('polyline',{fill:'none','stroke-width':3.5,'stroke-linejoin':'round','stroke-linecap':'round'},svB);
  const bLink=el('line',{'stroke-width':1.8,'stroke-dasharray':'5 4'},svB);
  const bCompH=el('line',{'stroke-width':2,'stroke-dasharray':'3 4'},svB);
  const bCompV=el('line',{'stroke-width':6,'stroke-linecap':'round',opacity:.55},svB);
  const bVec=el('line',{'stroke-width':3.5,'stroke-linecap':'round'},svB);
  const bBar=el('line',{x1:SXB,x2:SXB,'stroke-width':8,'stroke-linecap':'round',opacity:.6},svB);
  const bQ=el('circle',{r:8,stroke:'#fff','stroke-width':2.5},svB);
  const bHead=el('circle',{r:6,stroke:'#fff','stroke-width':2.5},svB);
  const bP=el('circle',{r:10,fill:'#0f172a',stroke:'#fff','stroke-width':3},svB);
  const bPt=el('text',{'font-size':14,'font-weight':800,fill:'#0f172a'},svB);bPt.textContent='P';
  const bQt=el('text',{'font-size':13,'font-weight':800,'text-anchor':'start',stroke:'#fff','stroke-width':4,'paint-order':'stroke'},svB);
  const bArc=el('path',{fill:'none',stroke:'#f59e0b','stroke-width':2.5},svB);
  const bTh=el('text',{'font-size':13,fill:'#b45309','font-weight':700,stroke:'#fff','stroke-width':4,'paint-order':'stroke'},svB);
  const bCap=el('text',{x:OX,y:430,'text-anchor':'middle','font-size':12,fill:'#64748b'},svB);bCap.textContent='등속 원운동하는 물체 P (반지름 = 진폭 A)';
  const bScr=el('text',{x:SXB,y:430,'text-anchor':'middle','font-size':12,fill:'#a16207'},svB);bScr.textContent='스크린';
  const bTitle=el('text',{x:GX0+30,y:24,'font-size':14,'font-weight':800},svB);
  const COL={2:'#2563eb',3:'#059669',4:'#e11d48'}, MK={2:'url(#bBl)',3:'url(#bGr)',4:'url(#bRd)'};
  const UNIT={2:'x (m)',3:'v (m/s)',4:'a (m/s²)'}, TIT={2:'x–t 그래프 : 그림자 Q의 위치',3:'v–t 그래프 : 그림자 Q의 속도',4:'a–t 그래프 : 그림자 Q의 가속도'};
  const maxOf=()=>S.step===2?S.A:S.step===3?S.A*S.w:S.A*S.w*S.w;
  const valOf=()=>S.step===2?X:S.step===3?V:AC;
  const ampPx=()=>S.step===2?S.A*PXM:0.8*S.A*PXM;
  function rebuildGridB(){
    clear(bGrid);if(S.step<2||S.step>4)return;
    const R=S.A*PXM,AMP=ampPx(),mx=maxOf(),col=COL[S.step],g=bGrid;
    // 시간 격자
    for(let s=0;s<=TMAX;s++){const x=GX0+s*PXT;el('line',{x1:x,x2:x,y1:OY-155,y2:OY+155,stroke:'#f1f5f9','stroke-width':1},g);
      if(s%2===0&&s<10){const t=el('text',{x,y:412,'text-anchor':'middle','font-size':11,fill:'#64748b'},g);t.textContent=s;}}
    const ut=el('text',{x:GX1+8,y:412,'text-anchor':'start','font-size':11,fill:'#64748b'},g);ut.textContent='t (s)';
    [-1,1].forEach(s=>el('line',{x1:GX0,x2:GX1,y1:OY-s*AMP,y2:OY-s*AMP,stroke:'#e2e8f0','stroke-width':1,'stroke-dasharray':'3 3'},g));
    [[AMP,'+'+mx.toFixed(2)],[0,'0'],[-AMP,'−'+mx.toFixed(2)]].forEach(p=>{const t=el('text',{x:402,y:OY-p[0]+4,'text-anchor':'start','font-size':11,fill:'#64748b',stroke:'#fff','stroke-width':3,'paint-order':'stroke'},g);t.textContent=p[1];});
    const un=el('text',{x:402,y:OY-155-8,'text-anchor':'start','font-size':12,'font-weight':700,fill:col},g);un.textContent=UNIT[S.step];
    // 주기선
    const Tp=T();
    for(let n=1;n*Tp<=TMAX+1e-9;n++){const x=GX0+n*Tp*PXT;el('line',{x1:x,x2:x,y1:OY-155,y2:OY+155,stroke:'#cbd5e1','stroke-width':1,'stroke-dasharray':'2 3'},g);
      if(n<=3){const t=el('text',{x,y:OY-160,'text-anchor':'middle','font-size':11,fill:'#1d4ed8','font-weight':700},g);t.textContent=(n===1?'T':n+'T');}}
    bTitle.textContent=TIT[S.step];bTitle.setAttribute('fill',col);
    // 색
    [bTrace,bGhost].forEach(e=>e.setAttribute('stroke',col));
    bLink.setAttribute('stroke',col);bCompH.setAttribute('stroke',col);bCompV.setAttribute('stroke',col);bVec.setAttribute('stroke',col);
    bBar.setAttribute('stroke',col);bQ.setAttribute('fill',col);bHead.setAttribute('fill',col);bQt.setAttribute('fill',col);
    // 미리보기 곡선
    const fn=valOf(),pts=[];for(let i=0;i<=400;i++){const t=i/400*TMAX;pts.push((GX0+t*PXT).toFixed(1)+','+(OY-fn(t)/mx*AMP).toFixed(1));}
    bGhost.setAttribute('points',pts.join(' '));
  }
  function drawB(){
    const th=S.w*S.t,R=S.A*PXM,c=Math.cos(th),s=Math.sin(th),px=OX+R*c,py=OY-R*s,L=0.8*R,AMP=ampPx(),mx=maxOf(),fn=valOf();
    bRing.setAttribute('r',R);
    bIcSpring.setAttribute('points',springPts(340,42,py-13,8,6));bIcMass.setAttribute('y',py-13);bIcT.setAttribute('y',py+4);
    bP.setAttribute('cx',px);bP.setAttribute('cy',py);bPt.setAttribute('x',px+13);bPt.setAttribute('y',py-12);
    let comp,tipx,tipy,vx1,vy1,vx2,vy2;
    if(S.step===2){comp=R*s;vx1=OX;vy1=OY;tipx=px;tipy=py;
      bVec.setAttribute('x1',OX);bVec.setAttribute('y1',OY);bVec.setAttribute('x2',px);bVec.setAttribute('y2',py);
      bCompV.setAttribute('x1',px);bCompV.setAttribute('y1',OY);bCompV.setAttribute('x2',px);bCompV.setAttribute('y2',py);
      bCompH.setAttribute('x1',OX);bCompH.setAttribute('y1',OY);bCompH.setAttribute('x2',px);bCompH.setAttribute('y2',OY);
      bQt.textContent='그림자 Q';
    }else{
      if(S.step===3){comp=L*c;tipx=px-L*s;tipy=py-L*c;bQt.textContent='Q의 속도 v';}
      else{comp=-L*s;tipx=px-L*c;tipy=py+L*s;bQt.textContent='Q의 가속도 a';}
      bVec.setAttribute('x1',px);bVec.setAttribute('y1',py);bVec.setAttribute('x2',tipx);bVec.setAttribute('y2',tipy);
      bCompV.setAttribute('x1',px);bCompV.setAttribute('y1',py);bCompV.setAttribute('x2',px);bCompV.setAttribute('y2',py-comp);
      bCompH.setAttribute('x1',px);bCompH.setAttribute('y1',py-comp);bCompH.setAttribute('x2',tipx);bCompH.setAttribute('y2',tipy);
    }
    bVec.setAttribute('marker-end',MK[S.step]);
    // 스크린 막대, Q, 연결선, 머리
    const qy=OY-comp,hx=GX0+S.t*PXT;
    bBar.setAttribute('y1',OY);bBar.setAttribute('y2',qy);
    bQ.setAttribute('cx',SXB);bQ.setAttribute('cy',qy);
    bQt.setAttribute('x',SXB+14);bQt.setAttribute('y',qy-12);
    bHead.setAttribute('cx',hx);bHead.setAttribute('cy',qy);
    bLink.setAttribute('x1',S.step===2?px:SXB);bLink.setAttribute('y1',qy);bLink.setAttribute('x2',hx);bLink.setAttribute('y2',qy);
    // 궤적
    const n=Math.max(2,Math.floor(S.t/TMAX*400)),pts=[];
    for(let i=0;i<=n;i++){const t=Math.min(S.t,i/n*S.t);pts.push((GX0+t*PXT).toFixed(1)+','+(OY-fn(t)/mx*AMP).toFixed(1));}
    bTrace.setAttribute('points',pts.join(' '));
    bGhost.style.display=S.ghost?'':'none';
    // 각
    const thm=((th%(2*Math.PI))+2*Math.PI)%(2*Math.PI),r0=Math.min(34,R*0.4);
    bArc.setAttribute('d','M '+(OX+r0)+' '+OY+' A '+r0+' '+r0+' 0 '+(thm>Math.PI?1:0)+' 0 '+(OX+r0*Math.cos(thm)).toFixed(1)+' '+(OY-r0*Math.sin(thm)).toFixed(1));
    bTh.setAttribute('x',OX+r0+8);bTh.setAttribute('y',OY+(Math.sin(thm)>0.3?18:-8));bTh.textContent='θ = '+thm.toFixed(2)+' rad';
  }

  /* ================= 뷰 C : 겹쳐 보기 ================= */
  const OW=520,OH=260,OPL=40,OPR=14,OPT=14,OPB=26,OWW=OW-OPL-OPR,OHH=OH-OPT-OPB,OMID=OPT+OHH/2;
  const gOv=$('gOv'),ovGrid=el('g',{},gOv),ovC={x:el('polyline',{fill:'none',stroke:'#2563eb','stroke-width':3,opacity:.9},gOv),v:el('polyline',{fill:'none',stroke:'#059669','stroke-width':3,opacity:.9},gOv),a:el('polyline',{fill:'none',stroke:'#e11d48','stroke-width':3,opacity:.9},gOv)};
  const ovCur=el('line',{y1:OPT,y2:OH-OPB,stroke:'#94a3b8','stroke-width':1.5,'stroke-dasharray':'4 3'},gOv);
  const ovD={x:el('circle',{r:6,fill:'#2563eb',stroke:'#fff','stroke-width':2.5},gOv),v:el('circle',{r:6,fill:'#059669',stroke:'#fff','stroke-width':2.5},gOv),a:el('circle',{r:6,fill:'#e11d48',stroke:'#fff','stroke-width':2.5},gOv)};
  const nrm={x:t=>Math.sin(S.w*t),v:t=>Math.cos(S.w*t),a:t=>-Math.sin(S.w*t)};
  function ovRedraw(){
    const g=ovGrid;clear(g);
    [-1,0,1].forEach(s=>{const y=OMID-s*OHH/2*0.9;el('line',{x1:OPL,x2:OPL+OWW,y1:y,y2:y,stroke:s===0?'#94a3b8':'#eef2f7','stroke-width':s===0?1.5:1},g);
      const t=el('text',{x:OPL-6,y:y+4,'text-anchor':'end','font-size':11,fill:'#64748b'},g);t.textContent=s===0?'0':(s>0?'+최대':'−최대');});
    for(let s=0;s<=TMAX;s++){const x=OPL+s/TMAX*OWW;el('line',{x1:x,x2:x,y1:OH-OPB,y2:OH-OPB+4,stroke:'#94a3b8'},g);
      if(s%2===0&&s<10){const t=el('text',{x,y:OH-OPB+16,'text-anchor':'middle','font-size':11,fill:'#64748b'},g);t.textContent=s;}}
    const ut=el('text',{x:OPL+OWW,y:OH-OPB+16,'text-anchor':'end','font-size':11,fill:'#64748b'},g);ut.textContent='t (s)';
    const Tp=T();
    for(let n=1;n*Tp<=TMAX+1e-9;n++){const x=OPL+n*Tp/TMAX*OWW;el('line',{x1:x,x2:x,y1:OPT,y2:OH-OPB,stroke:'#cbd5e1','stroke-width':1,'stroke-dasharray':'2 3'},g);
      if(n<=3){const t=el('text',{x,y:OPT+8,'text-anchor':'middle','font-size':11,fill:'#1d4ed8','font-weight':700},g);t.textContent=(n===1?'T':n+'T');}}
    ['x','v','a'].forEach(k=>{const pts=[];for(let i=0;i<=400;i++){const t=i/400*TMAX;pts.push((OPL+t/TMAX*OWW).toFixed(1)+','+(OMID-nrm[k](t)*OHH/2*0.9).toFixed(1));}
      ovC[k].setAttribute('points',pts.join(' '));});
    ovVis();
  }
  function ovVis(){['x','v','a'].forEach(k=>{ovC[k].style.display=S.ov[k]?'':'none';ovD[k].style.display=S.ov[k]?'':'none';});}
  function drawC(){
    const x=OPL+S.t/TMAX*OWW;ovCur.setAttribute('x1',x);ovCur.setAttribute('x2',x);
    ['x','v','a'].forEach(k=>{ovD[k].setAttribute('cx',x);ovD[k].setAttribute('cy',OMID-nrm[k](S.t)*OHH/2*0.9);});
    xyA.move(X(S.t),AC(S.t));
  }

  /* ================= 공통 ================= */
  function draw(){
    const t=S.t,x=X(t),v=V(t),a=AC(t),th=S.w*t,thm=((th%(2*Math.PI))+2*Math.PI)%(2*Math.PI);
    const vw=ST[S.step].view;
    if(vw==='H')drawH();else if(vw==='A')drawA();else if(vw==='B')drawB();else drawC();
    $('rt').textContent=t.toFixed(2)+' s';$('rth').textContent=thm.toFixed(2)+' rad';
    $('rx').textContent=sg(x)+' m';$('rv').textContent=sg(v)+' m/s';$('ra').textContent=sg(a)+' m/s²';$('rf').textContent=sg(-S.k*x)+' N';
  }
  function syncText(){
    $('vA').textContent=S.A.toFixed(2)+' m';$('vw').textContent=S.w.toFixed(1)+' rad/s';
    $('vm').textContent=S.m.toFixed(1)+' kg';$('vk').textContent=S.k.toFixed(1)+' N/m';
    const sv=S.step;
    $('derived').innerHTML=(sv===0||sv===1)?'최대 복원력 kA = <b>'+(S.k*S.A).toFixed(2)+'</b> N':(sv===6?'ω = √(k/m) = <b>'+S.w.toFixed(2)+'</b> rad/s &nbsp; T = 2π/ω = <b>'+T().toFixed(2)+'</b> s':
      'ω = <b>'+S.w.toFixed(1)+'</b> rad/s &nbsp; T = 2π/ω = <b>'+T().toFixed(2)+'</b> s &nbsp; f = 1/T = <b>'+(1/T()).toFixed(2)+'</b> Hz');
    $('fxhs').textContent='기울기 = −k = −'+S.k.toFixed(1)+' N/m';
    $('fxs').textContent='기울기 = −k = −'+S.k.toFixed(1)+' N/m';
    $('axs').textContent='기울기 = −ω² = −'+(S.w*S.w).toFixed(1)+' s⁻²';
    $('xts').textContent='최댓값 A = '+S.A.toFixed(2)+' m';
  }
  function setSliders(){$('rA').value=S.A;$('rw').value=S.w;$('rm').value=S.m;$('rk').value=S.k;}
  function redrawStatic(){
    syncText();
    gXt.redraw(X,S.A);
    xyFH.setLine(-S.k,S.A);xyF.setLine(-S.k,S.A);xyA.setLine(-S.w*S.w,S.A);
    updateH3();ovRedraw();rebuildGridB();draw();
  }
  function setStep(n){
    S.step=n;const d=ST[n];
    $('app').className='v'+d.view;
    document.querySelectorAll('.tab').forEach(b=>b.classList.toggle('on',+b.dataset.step===n));
    const circ=(n>=2&&n<=5),mk=(n===0||n===1||n===6);
    if(circ){S.w=Math.min(3.4,Math.max(0.6,S.w));S.k=S.m*S.w*S.w;}
    if(mk){S.k=Math.min(12,Math.max(2,S.k));S.w=Math.sqrt(S.k/S.m);}
    setSliders();
    document.querySelectorAll('.cw').forEach(e=>e.style.display=circ?'':'none');
    document.querySelectorAll('.cmk').forEach(e=>e.style.display=mk?'':'none');
    document.querySelectorAll('.cghost').forEach(e=>e.style.display=(n>=2&&n<=4)?'':'none');
    $('boxFx').style.display=(n===1)?'':'none';$('boxXt').style.display=(n===6)?'':'none';
    $('splitRow').style.display=(n===1)?'':'none';
    $('splitInfo').innerHTML='';renderInfo();redrawStatic();
  }

  /* ---------- 입력 ---------- */
  document.querySelectorAll('.tab').forEach(b=>b.addEventListener('click',()=>setStep(+b.dataset.step)));
  $('rA').addEventListener('input',e=>{S.A=+e.target.value;redrawStatic();});
  $('rw').addEventListener('input',e=>{S.w=+e.target.value;S.k=S.m*S.w*S.w;redrawStatic();});
  $('rm').addEventListener('input',e=>{S.m=+e.target.value;S.w=Math.sqrt(S.k/S.m);redrawStatic();});
  $('rk').addEventListener('input',e=>{S.k=+e.target.value;S.w=Math.sqrt(S.k/S.m);redrawStatic();});
  $('speed').addEventListener('change',e=>{S.speed=+e.target.value;});
  $('ghost').addEventListener('change',e=>{S.ghost=e.target.checked;draw();});
  $('fbtn').addEventListener('click',()=>{S.fshow=!S.fshow;renderFormula();});
  $('splitBtn').addEventListener('click',()=>{S.split=!S.split;$('splitBtn').classList.toggle('on',S.split);draw();});
  ['ox','ov','oa'].forEach(id=>$(id).addEventListener('change',e=>{S.ov[id[1]]=e.target.checked;ovVis();}));
  $('play').addEventListener('click',()=>{S.playing=!S.playing;S.last=null;$('play').textContent=S.playing?'⏸ 정지':'▶ 재생';});
  $('reset').addEventListener('click',()=>{S.t=0;draw();});
  document.querySelectorAll('.keys .btn[data-ph]').forEach(b=>b.addEventListener('click',()=>{
    S.playing=false;$('play').textContent='▶ 재생';S.t=(+b.dataset.ph)*T();draw();}));
  $('rxH').addEventListener('input',e=>{
    S.playing=false;$('play').textContent='▶ 재생';
    const ratio=Math.max(-1,Math.min(1,+e.target.value));
    const ang=Math.asin(ratio);
    S.t=(ang>=0?ang:(ang+2*Math.PI))/S.w;
    draw();
  });
  document.querySelectorAll('.ans-box').forEach(g=>g.addEventListener('click',()=>{
    const idx=+g.dataset.b;S.hbox[idx]=!S.hbox[idx];updateH3();
  }));
  document.querySelectorAll('.blank-pill').forEach(el=>el.addEventListener('click',()=>{
    const idx=+el.dataset.ws;S.ws[idx]=!S.ws[idx];updateH3();
  }));
  $('hShowAll').addEventListener('click',()=>{
    const next=!(S.hbox.every(Boolean)&&S.ws.every(Boolean));
    S.hbox=S.hbox.map(()=>next);
    S.ws=S.ws.map(()=>next);
    updateH3();
  });
  function tick(ts){
    if(S.playing){if(S.last!=null){S.t+=Math.min(0.05,(ts-S.last)/1000)*S.speed;if(S.t>=TMAX)S.t-=TMAX;}S.last=ts;draw();}
    requestAnimationFrame(tick);
  }
  setStep(0);requestAnimationFrame(tick);
  window.__S=S;window.__setStep=setStep;window.__draw=draw;window.__redraw=redrawStatic;
})();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    run_sim()
