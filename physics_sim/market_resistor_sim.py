import streamlit as st
import streamlit.components.v1 as components

# Streamlit Cloud Redeploy Tag: May 29 2026
# ── 공통 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #1e1b4b, #0f172a);
    border-left: 5px solid #6366f1;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);
}
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("<h1 class='main-title'>🔌 [융합] 직류 회로와 시장 원리의 구조적 전이 탐구</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>전기 회로의 저항 연결 방식과 미시경제학 수요·공급 곡선의 이동 간 구조적 유사성을 탐색하는 학제적 융합 가상 실험실</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <b style='color:#a5b4fc; font-size:1.05rem;'>🎯 학제적 융합 탐구 목표</b><br>
    <span style='color:#e2e8f0; font-size:0.92rem; line-height: 1.6;'>
    1. 물리학의 <b>옴의 법칙 (Ohm's Law)</b>과 경제학의 <b>수요·공급 균형 원리</b> 사이의 구조적 유사성(Isomorphism)을 이해하고 비교·대조합니다.<br>
    2. 공급 곡선의 우측 및 좌측 이동(Shift)이 전기 회로의 <b>병렬 분기(우회 통로 신설- 합성 저항 감소)</b> 및 <b>직렬 저항 추가(합성 저항 상승)</b> 현상과 어떻게 수학적·물리적 시스템 관점에서 정확히 동형 매핑되는지 직접 슬라이더를 통해 탐색해 봅니다.
    </span>
</div>
""", unsafe_allow_html=True)

# 시뮬레이터 HTML 코드 정의
html_content = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[융합] 직류 회로와 시장 원리의 구조적 전이 탐구 시뮬레이터</title>
  
  <!-- Tailwind CSS & Web Fonts & FontAwesome -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

  <style>
    body {
      font-family: 'Noto Sans KR', sans-serif;
    }
    .font-mono-jb {
      font-family: 'JetBrains Mono', monospace;
    }
    /* 슬라이더 커스텀 스타일 */
    input[type="range"] {
      -webkit-appearance: none;
      appearance: none;
      background: #cbd5e1;
      height: 6px;
      border-radius: 3px;
      outline: none;
    }
    input[type="range"]::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: #3b82f6;
      cursor: pointer;
      transition: transform 0.1s ease;
    }
    input[type="range"]::-webkit-slider-thumb:hover {
      transform: scale(1.2);
    }
    .demand-slider::-webkit-slider-thumb {
      background: #1d4ed8 !important;
    }
    .supply-slider::-webkit-slider-thumb {
      background: #dc2626 !important;
    }
    .price-slider::-webkit-slider-thumb {
      background: #d97706 !important;
    }
  </style>
</head>
<body class="bg-slate-900 min-h-screen text-slate-100">

  <!-- 헤더 영역 (다크 모드 프리미엄 스타일) -->
  <header class="bg-slate-950 text-white px-6 py-6 shadow-lg border-b border-indigo-900/60">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div class="flex items-center gap-3">
        <div class="bg-indigo-600 text-white p-3 rounded-xl shadow-inner">
          <i class="fa-solid fa-chart-line text-2xl"></i>
        </div>
        <div>
          <h1 class="font-bold text-xl md:text-2xl tracking-tight">[융합] 직류 회로와 시장 원리의 구조적 전이 탐구</h1>
          <p class="text-xs text-slate-400 mt-1">물리적 저항 연결(직렬·병렬)과 시장 수요·공급 곡선 이동 간의 구조적 동형성(Isomorphism) 분석 시뮬레이터</p>
        </div>
      </div>
      <button onclick="resetAll()" class="bg-indigo-950 hover:bg-indigo-900 text-indigo-200 border border-indigo-800/80 px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all self-stretch md:self-auto justify-center">
        <i class="fa-solid fa-rotate-left"></i>
        <span>시뮬레이터 초기화</span>
      </button>
    </div>
  </header>

  <!-- 메인 레이아웃 -->
  <main class="max-w-7xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

    <!-- 왼쪽 조절 및 실시간 상태 판넬 (4/12) -->
    <aside class="lg:col-span-4 flex flex-col gap-6">
      
      <!-- 컨트롤러 카드 -->
      <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700 shadow-md flex flex-col gap-5">
        <h3 class="text-sm font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2 border-b border-slate-700 pb-2">
          <i class="fa-solid fa-sliders text-indigo-400"></i>시장 제어 슬라이더
        </h3>

        <!-- 수요 곡선 자체 이동 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-blue-400">수요 이동 (Demand Shift)</span>
            <span id="val-d-shift" class="text-xs font-mono-jb font-bold text-blue-300">0</span>
          </div>
          <input type="range" id="slider-d-shift" min="-25" max="25" step="1" value="0" oninput="updateSimulation()" class="w-full demand-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-1">
            <span>← 선호 감소/소득 저하</span>
            <span>선호 증가/소득 상승 →</span>
          </div>
        </div>

        <!-- 공급 곡선 자체 이동 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-red-400">공급 이동 (Supply Shift)</span>
            <span id="val-s-shift" class="text-xs font-mono-jb font-bold text-red-300">0</span>
          </div>
          <input type="range" id="slider-s-shift" min="-25" max="25" step="1" value="0" oninput="updateSimulation()" class="w-full supply-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-1">
            <span>← 원가 상승/장벽 증가</span>
            <span>기술 혁신/공급 다각화 →</span>
          </div>
        </div>

        <hr class="border-slate-700">

        <!-- 인위적 가격 조절 (곡선 위에서의 운동 및 불균형 유도) -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-amber-400">실제 시장 가격 조정 (Market Price)</span>
            <span id="val-m-price" class="text-xs font-mono-jb font-bold text-amber-300">55</span>
          </div>
          <input type="range" id="slider-m-price" min="20" max="90" step="1" value="55" oninput="updateSimulation()" class="w-full price-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-1">
            <span>← 저가 형성</span>
            <span>고가 형성 →</span>
          </div>
        </div>

        <!-- 자동 균형 버튼 -->
        <button onclick="autoEquilibrium()" class="w-full bg-indigo-900/60 hover:bg-indigo-800 text-indigo-200 font-bold text-xs py-2.5 rounded-lg border border-indigo-700/80 transition-all flex items-center justify-center gap-1.5">
          <i class="fa-solid fa-scale-balanced"></i>
          <span>시장 보이지 않는 손 가동 (균형 가격으로 이동)</span>
        </button>
      </div>

      <!-- 실시간 변동 결과 패널 -->
      <div class="bg-slate-950 text-slate-100 rounded-2xl p-5 shadow-lg border border-indigo-950 flex flex-col gap-4">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2 border-b border-slate-800 pb-2">
          <i class="fa-solid fa-circle-nodes text-emerald-400"></i>실시간 시장 분석 리포트
        </h3>

        <!-- 균형 데이터 요약 -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-slate-800/80 p-3 rounded-xl border border-slate-700 text-center">
            <div class="text-[10px] text-slate-400 font-medium">이론적 균형 가격 (P*)</div>
            <div id="report-eq-price" class="text-xl font-bold text-emerald-400 font-mono-jb mt-1">55.0</div>
          </div>
          <div class="bg-slate-800/80 p-3 rounded-xl border border-slate-700 text-center">
            <div class="text-[10px] text-slate-400 font-medium">이론적 균형 거래량 (Q*)</div>
            <div id="report-eq-qty" class="text-xl font-bold text-emerald-400 font-mono-jb mt-1">56.3</div>
          </div>
        </div>

        <!-- 현재 가격 상태 피드백 -->
        <div id="feedback-card" class="p-3.5 rounded-xl border flex flex-col gap-1 text-xs">
          <!-- JS에서 동적으로 채움 -->
        </div>

        <!-- 옴의 법칙 매핑 카드 -->
        <div class="bg-indigo-950/40 border border-indigo-800/60 rounded-xl p-3.5 text-xs text-indigo-200 leading-relaxed">
          <strong class="text-indigo-300 flex items-center gap-1.5 mb-1">
            <i class="fa-solid fa-bolt-lightning"></i> ⚡ 전기 계통과의 유사구조 확인
          </strong>
          <span id="transference-feedback">
            공급 곡선이 우측으로 이동한 상태입니다. 이는 전기 회로 관점에서 <strong>'병렬 분기 우회 경로'</strong>가 신설되어 계통의 총 임피던스(공급 장벽)가 하락하고 전체 허용 전류량(시장 유통량)이 확장된 현상에 대응됩니다.
          </span>
        </div>
      </div>
    </aside>

    <!-- 오른쪽 인터랙티브 그래프 공간 (8/12) -->
    <section class="lg:col-span-8 flex flex-col gap-6">
      
      <!-- 그래프 캔버스 카드 -->
      <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700 shadow-md flex flex-col gap-4">
        <div class="flex justify-between items-center border-b border-slate-700 pb-2">
          <h3 class="font-bold text-slate-200 flex items-center gap-2">
            <i class="fa-solid fa-bezier-curve text-indigo-400"></i>수요·공급 동적 곡선 그래프
          </h3>
          <span class="text-slate-500 text-[10px] font-mono-jb">Canvas: SVG Vector Rendering (100% Crisp)</span>
        </div>

        <!-- 실제 SVG 엘리먼트 -->
        <div class="w-full aspect-[4/3] bg-slate-950 rounded-xl relative overflow-hidden shadow-inner">
          <svg viewBox="0 0 500 400" id="svg-graph" class="w-full h-full select-none">
            <!-- 그리드선 및 축 -->
            <!-- 가로 가이드라인 -->
            <line x1="60" y1="60" x2="460" y2="60" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="60" y1="130" x2="460" y2="130" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="60" y1="200" x2="460" y2="200" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="60" y1="270" x2="460" y2="270" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            
            <!-- 세로 가이드라인 -->
            <line x1="160" y1="60" x2="160" y2="340" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="260" y1="60" x2="260" y2="340" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>
            <line x1="360" y1="60" x2="360" y2="340" stroke="#1e293b" stroke-width="1" stroke-dasharray="2,2"/>

            <!-- 메인 축 -->
            <line x1="60" y1="30" x2="60" y2="340" stroke="#475569" stroke-width="2"/> <!-- Y축 -->
            <line x1="60" y1="340" x2="480" y2="340" stroke="#475569" stroke-width="2"/> <!-- X축 -->
            
            <!-- 축 화살표 -->
            <polygon points="60,25 56,35 64,35" fill="#475569"/>
            <polygon points="485,340 475,336 475,344" fill="#475569"/>

            <!-- 축 레이블 -->
            <text x="35" y="40" font-size="10" fill="#94a3b8" font-family="Noto Sans KR" font-weight="700">가격 (P)</text>
            <text x="460" y="360" font-size="10" fill="#94a3b8" font-family="Noto Sans KR" font-weight="700">수량 (Q)</text>
            <text x="45" y="350" font-size="10" fill="#64748b" font-family="JetBrains Mono">0</text>

            <!-- 실시간 동적 영역 (초과 공급/수요 표시) -->
            <polygon id="gap-area" points="100,100 200,100 200,200" fill="none" opacity="0.15"/>

            <!-- 수요 곡선 D -->
            <line id="curve-demand" x1="80" y1="102" x2="440" y2="354" stroke="#2563eb" stroke-width="3"/>
            <text id="label-demand" x="445" y="350" font-size="12" fill="#3b82f6" font-family="JetBrains Mono" font-weight="bold">D</text>

            <!-- 공급 곡선 S -->
            <line id="curve-supply" x1="80" y1="326" x2="440" y2="74" stroke="#dc2626" stroke-width="3"/>
            <text id="label-supply" x="445" y="70" font-size="12" fill="#ef4444" font-family="JetBrains Mono" font-weight="bold">S</text>

            <!-- 균형 가이드 점선 및 텍스트 -->
            <line id="eq-line-y" x1="60" y1="200" x2="220" y2="200" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,4"/>
            <line id="eq-line-x" x1="220" y1="200" x2="220" y2="340" stroke="#10b981" stroke-width="1.5" stroke-dasharray="4,4"/>
            <circle id="eq-point" cx="220" cy="200" r="6" fill="#10b981" stroke="#ffffff" stroke-width="2"/>
            <text id="eq-label" x="230" y="195" font-size="11" fill="#10b981" font-weight="bold" font-family="JetBrains Mono">E*(P*, Q*)</text>

            <!-- 실제 시장 가격 가이드선 -->
            <line id="market-line-y" x1="60" y1="180" x2="460" y2="180" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3"/>
            
            <!-- 실제 가격과 각 곡선과의 만남 점 -->
            <circle id="point-md" cx="150" cy="180" r="4" fill="#3b82f6" stroke="#fff" stroke-width="1.5"/>
            <circle id="point-ms" cx="300" cy="180" r="4" fill="#ef4444" stroke="#fff" stroke-width="1.5"/>
            <line id="gap-line" x1="150" y1="180" x2="300" y2="180" stroke="#f59e0b" stroke-width="3"/>

            <!-- 실제 가격 가이드 레이블 -->
            <text id="market-price-tag" x="65" y="175" font-size="9" fill="#f59e0b" font-weight="bold">P_market</text>
            <text id="qd-tag" x="145" y="355" font-size="9" fill="#3b82f6" font-weight="bold">Qd</text>
            <text id="qs-tag" x="295" y="355" font-size="9" fill="#ef4444" font-weight="bold">Qs</text>
            <line id="qd-line" x1="150" y1="180" x2="150" y2="340" stroke="#3b82f6" stroke-width="1" stroke-dasharray="2,2"/>
            <line id="qs-line" x1="300" y1="180" x2="300" y2="340" stroke="#ef4444" stroke-width="1" stroke-dasharray="2,2"/>
          </svg>
        </div>
      </div>
    </section>

  </main>

  <!-- 하단 교과 원리 및 개념 설명 영역 -->
  <section class="max-w-7xl mx-auto px-4 md:px-6 pb-12">
    <div class="bg-slate-800 rounded-2xl p-6 md:p-8 border border-slate-700 shadow-md flex flex-col gap-6">
      
      <div class="border-b border-slate-700 pb-4">
        <h2 class="text-xl font-bold text-slate-100 flex items-center gap-2">
          <i class="fa-solid fa-graduation-cap text-indigo-400"></i>교안 및 융합 원리: 저항의 연결 & 시장 원리의 구조적 전이
        </h2>
        <p class="text-xs text-slate-400 mt-1">인터랙티브 실험과 연계하여 학습하는 물리-경제 융합 핵심 교과 내용</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- 수요의 법칙 -->
        <div class="bg-blue-950/30 rounded-xl p-5 border border-blue-900/60">
          <h4 class="font-bold text-blue-300 flex items-center gap-1.5 mb-2.5">
            <i class="fa-solid fa-cart-shopping text-blue-400"></i>1. 수요의 법칙 (Law of Demand)
          </h4>
          <p class="text-xs text-slate-300 leading-relaxed mb-3">
            어떤 재화의 가격이 상승하면 수요량이 감소하고, 가격이 하락하면 수요량이 증가하는 역의 상관관계입니다. 그래프 상에서 우하향(Negative Slope)의 형태를 보입니다.
          </p>
          <ul class="text-xs text-slate-400 space-y-1.5">
            <li>• <strong>원인:</strong> 한계효용 체감의 법칙, 소득효과 및 대체효과</li>
            <li>• <strong>수요 이동(Demand Shift) 요인:</strong> 소비자의 기호·선호도 증가, 소득 상승, 보완재/대체재 가격 변화</li>
          </ul>
        </div>

        <!-- 공급의 법칙 -->
        <div class="bg-red-950/30 rounded-xl p-5 border border-red-900/60">
          <h4 class="font-bold text-red-300 flex items-center gap-1.5 mb-2.5">
            <i class="fa-solid fa-warehouse text-red-400"></i>2. 공급의 법칙 (Law of Supply)
          </h4>
          <p class="text-xs text-slate-300 leading-relaxed mb-3">
            어떤 재화의 가격이 상승하면 기업의 공급량이 증가하고, 가격이 하락하면 공급량이 감소하는 정의 상관관계입니다. 그래프 상에서 우상향(Positive Slope)의 형태를 보입니다.
          </p>
          <ul class="text-xs text-slate-400 space-y-1.5">
            <li>• <strong>원인:</strong> 한계비용 체증 법칙(생산 비용 상승 감내 조건)</li>
            <li>• <strong>공급 이동(Supply Shift) 요인:</strong> 생산 기술 혁신(원가 감소), 공급자 수의 증가, 규제 완화</li>
          </ul>
        </div>

      </div>

      <!-- 불균형 상태 설명 -->
      <div class="bg-amber-950/20 border border-amber-900/40 rounded-xl p-5">
        <h4 class="font-bold text-amber-300 flex items-center gap-1.5 mb-2">
          <i class="fa-solid fa-triangle-exclamation text-amber-400"></i>3. 시장 불균형과 보이지 않는 손 (Invisible Hand)
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300 leading-relaxed">
          <div>
            <strong>■ 초과 공급 (Surplus)</strong><br>
            현재 실제 시장 가격이 이론적인 균형 가격($P^*$)보다 **높을 때** 발생합니다. 팔고 싶어 하는 수량($Q_s$)이 사고 싶어 하는 수량($Q_d$)보다 많아 공급 기업들 간의 가격 인하 경쟁이 붙고, 이로 인해 가격은 서서히 균형 가격을 향해 **하락 압력**을 받게 됩니다.
          </div>
          <div>
            <strong>■ 초과 수요 (Shortage)</strong><br>
            현재 실제 시장 가격이 이론적인 균형 가격($P^*$)보다 **낮을 때** 발생합니다. 물건을 사려는 수량($Q_d$)이 팔려는 수량($Q_s$)보다 많아 구매자들 사이에 품귀 현상이 생기고, 이로 인해 가격은 서서히 균형 가격을 향해 **상승 압력**을 받게 됩니다.
          </div>
        </div>
      </div>

      <!-- 융합 섹션 (물리학 저항의 연결과 공급 충격의 동형성) -->
      <div class="bg-indigo-950/40 border border-indigo-900/60 rounded-xl p-5">
        <h4 class="font-bold text-indigo-300 flex items-center gap-1.5 mb-2.5">
          <i class="fa-solid fa-bolt-lightning text-indigo-400"></i>4. [학제적 융합] 직류 회로와 시장 구조의 구조적 전이 (Structural Analogy)
        </h4>
        <p class="text-xs text-slate-300 leading-relaxed mb-3">
          물리학의 <strong>직류 회로(Direct Current Circuit)</strong>에서의 전하 유동 법칙과 미시경제학의 <strong>시장 가격 결정 메커니즘</strong>은 시스템을 제어하는 매개변수 관점에서 완벽한 <strong>구조적 동형성(Isomorphism)</strong>을 공유하고 있습니다.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="bg-slate-900 p-3.5 rounded-lg border border-slate-700">
            <strong class="text-indigo-400 block mb-1">⚡ 물리학 직류 계통 (Circuit)</strong>
            <ul class="space-y-1 text-slate-400">
              <li>• <strong>전압 ($V$, Potential):</strong> 전류 흐름을 유도하는 기전력</li>
              <li>• <strong>전류 ($I$, Current):</strong> 초당 유동하는 전하의 흐름량</li>
              <li>• <strong>저항 ($R$, Resistance):</strong> 자유 전자의 원자 충돌 방해 요소</li>
              <li>• <strong>병렬 분로 추가:</strong> 전체 합성저항 감소 $\rightarrow$ 총 전류 $I$ 증가</li>
              <li>• <strong>직렬 저항 삽입:</strong> 전체 합성저항 증가 $\rightarrow$ 총 전류 $I$ 감소</li>
            </ul>
          </div>
          <div class="bg-slate-900 p-3.5 rounded-lg border border-slate-700">
            <strong class="text-rose-400 block mb-1">📈 미시경제학 시장 계통 (Market)</strong>
            <ul class="space-y-1 text-slate-400">
              <li>• <strong>시장 가격 ($P$, Price):</strong> 공급-수요 흐름을 조율하는 전위차</li>
              <li>• <strong>유통량 ($Q$, Quantity):</strong> 시장 내에서 순환하는 재화의 양</li>
              <li>• <strong>생산 장벽 (Impedance):</strong> 공급을 가로막는 기술/세금적 한계비용</li>
              <li>• <strong>공급 우측 이동:</strong> 원가 하락/우회 경로 개척 $\rightarrow$ 균형량 $Q$ 증가</li>
              <li>• <strong>공급 좌측 이동:</strong> 원자재 폭등/직렬 장벽 추가 $\rightarrow$ 균형량 $Q$ 감소</li>
            </ul>
          </div>
          <div class="bg-slate-900 p-3.5 rounded-lg border border-slate-700">
            <strong class="text-amber-400 block mb-1">🔗 시스템 구조적 매핑 (Mapping)</strong>
            <ul class="space-y-1 text-slate-400">
              <li>• <strong>전압 ($V$) $\Leftrightarrow$ 실제 가격 ($P_{market}$)</strong></li>
              <li>• <strong>전류 ($I$) $\Leftrightarrow$ 유통 거래량 ($Q$)</strong></li>
              <li>• <strong>전기 저항 ($R$) $\Leftrightarrow$ 생산 원가 (공급 난이도)</strong></li>
              <li>• <strong>병렬 우회 경로 신설 $\Leftrightarrow$ 공급 우측 이동 ($s\_shift > 0$)</strong></li>
              <li>• <strong>직렬 고저항 소자 추가 $\Leftrightarrow$ 공급 좌측 이동 ($s\_shift < 0$)</strong></li>
            </ul>
          </div>
        </div>
      </div>

    </div>
  </section>

  <!-- 시뮬레이터 구동 JavaScript 엔진 -->
  <script>
    // 시장 수학 모델 기초 파라미터 고정
    // 수요 함수: P_d = 100 - 0.8 * Q + shift_d
    // 공급 함수: P_s = 10 + 0.8 * Q - shift_s
    let E = 12; // 물리계 매핑 전압 비유
    
    // 실시간 상태 업데이트 함수
    function updateSimulation() {
      // 1. 슬라이더 값 확보
      const d_shift = parseInt(document.getElementById('slider-d-shift').value);
      const s_shift = parseInt(document.getElementById('slider-s-shift').value);
      const m_price = parseInt(document.getElementById('slider-m-price').value);

      // 슬라이더 옆 수치 레이블 업데이트
      document.getElementById('val-d-shift').innerText = (d_shift > 0 ? "+" : "") + d_shift;
      document.getElementById('val-s-shift').innerText = (s_shift > 0 ? "+" : "") + s_shift;
      document.getElementById('val-m-price').innerText = m_price;

      // 2. 이론적 균형점(E*) 연산 및 보고서 갱신
      // 100 - 0.8*Q + d_shift = 10 + 0.8*Q - s_shift
      // 1.6*Q = 90 + d_shift + s_shift
      const eq_qty = (90 + d_shift + s_shift) / 1.6;
      const eq_price = 10 + 0.8 * eq_qty - s_shift;

      document.getElementById('report-eq-price').innerText = eq_price.toFixed(1);
      document.getElementById('report-eq-qty').innerText = eq_qty.toFixed(1);

      // 3. 현재 시장 가격에 따른 Qd, Qs 연산
      // m_price = 100 - 0.8 * Qd + d_shift  => 0.8*Qd = 100 - m_price + d_shift
      const qd = (100 - m_price + d_shift) / 0.8;
      // m_price = 10 + 0.8 * Qs - s_shift  => 0.8*Qs = m_price - 10 + s_shift
      const qs = (m_price - 10 + s_shift) / 0.8;

      // 4. SVG 요소 실시간 그리기 변환
      // 가상 경제 좌표 (Q: 0~100, P: 0~100) -> SVG 좌표 (X: 60~460, Y: 340~60)
      // X_svg = 60 + Q * 4
      // Y_svg = 340 - P * 2.8
      
      // 수요 곡선 D 라인 좌표 연산 (Q_start=5, Q_end=95)
      const d_p1 = 100 - 0.8 * 5 + d_shift;
      const d_p2 = 100 - 0.8 * 95 + d_shift;
      const d_x1 = 60 + 5 * 4;
      const d_y1 = 340 - d_p1 * 2.8;
      const d_x2 = 60 + 95 * 4;
      const d_y2 = 340 - d_p2 * 2.8;

      const demandLine = document.getElementById('curve-demand');
      demandLine.setAttribute('x1', d_x1);
      demandLine.setAttribute('y1', d_y1);
      demandLine.setAttribute('x2', d_x2);
      demandLine.setAttribute('y2', d_y2);

      const demandLabel = document.getElementById('label-demand');
      demandLabel.setAttribute('x', d_x2 + 5);
      demandLabel.setAttribute('y', d_y2 + 4);

      // 공급 곡선 S 라인 좌표 연산
      const s_p1 = 10 + 0.8 * 5 - s_shift;
      const s_p2 = 10 + 0.8 * 95 - s_shift;
      const s_x1 = 60 + 5 * 4;
      const s_y1 = 340 - s_p1 * 2.8;
      const s_x2 = 60 + 95 * 4;
      const s_y2 = 340 - s_p2 * 2.8;

      const supplyLine = document.getElementById('curve-supply');
      supplyLine.setAttribute('x1', s_x1);
      supplyLine.setAttribute('y1', s_y1);
      supplyLine.setAttribute('x2', s_x2);
      supplyLine.setAttribute('y2', s_y2);

      const supplyLabel = document.getElementById('label-supply');
      supplyLabel.setAttribute('x', s_x2 + 5);
      supplyLabel.setAttribute('y', s_y2 + 4);

      // 이론 균형점 E* 그리기
      const eq_x = 60 + eq_qty * 4;
      const eq_y = 340 - eq_price * 2.8;
      
      document.getElementById('eq-point').setAttribute('cx', eq_x);
      document.getElementById('eq-point').setAttribute('cy', eq_y);
      document.getElementById('eq-line-y').setAttribute('y1', eq_y);
      document.getElementById('eq-line-y').setAttribute('y2', eq_y);
      document.getElementById('eq-line-y').setAttribute('x2', eq_x);
      document.getElementById('eq-line-x').setAttribute('x1', eq_x);
      document.getElementById('eq-line-x').setAttribute('x2', eq_x);
      document.getElementById('eq-line-x').setAttribute('y1', eq_y);

      const eqLabel = document.getElementById('eq-label');
      eqLabel.setAttribute('x', eq_x + 8);
      eqLabel.setAttribute('y', eq_y - 6);
      eqLabel.textContent = `E* (${eq_price.toFixed(1)}, ${eq_qty.toFixed(1)})`;

      // 5. 실제 시장 가격 및 초과 수요/공급 가이드 렌더링
      const m_y = 340 - m_price * 2.8;
      document.getElementById('market-line-y').setAttribute('y1', m_y);
      document.getElementById('market-line-y').setAttribute('y2', m_y);
      
      document.getElementById('market-price-tag').setAttribute('y', m_y - 6);
      document.getElementById('market-price-tag').textContent = `P_market (${m_price})`;

      // Qd, Qs 점 위치 및 하강 수선 렌더링
      const qd_x = 60 + qd * 4;
      const qs_x = 60 + qs * 4;

      document.getElementById('point-md').setAttribute('cx', qd_x);
      document.getElementById('point-md').setAttribute('cy', m_y);
      document.getElementById('point-ms').setAttribute('cx', qs_x);
      document.getElementById('point-ms').setAttribute('cy', m_y);

      document.getElementById('qd-line').setAttribute('x1', qd_x);
      document.getElementById('qd-line').setAttribute('x2', qd_x);
      document.getElementById('qd-line').setAttribute('y1', m_y);
      document.getElementById('qd-line').setAttribute('y2', 340);

      document.getElementById('qs-line').setAttribute('x1', qs_x);
      document.getElementById('qs-line').setAttribute('x2', qs_x);
      document.getElementById('qs-line').setAttribute('y1', m_y);
      document.getElementById('qs-line').setAttribute('y2', 340);

      document.getElementById('qd-tag').setAttribute('x', qd_x - 10);
      document.getElementById('qd-tag').textContent = `Qd(${qd.toFixed(0)})`;
      document.getElementById('qs-tag').setAttribute('x', qs_x - 10);
      document.getElementById('qs-tag').textContent = `Qs(${qs.toFixed(0)})`;

      // 초과 갭 선 렌더링
      document.getElementById('gap-line').setAttribute('x1', qd_x);
      document.getElementById('gap-line').setAttribute('x2', qs_x);
      document.getElementById('gap-line').setAttribute('y1', m_y);
      document.getElementById('gap-line').setAttribute('y2', m_y);

      // 초과 음영 면적 폴리곤 렌더링
      const gapArea = document.getElementById('gap-area');
      gapArea.setAttribute('points', `${qd_x},${m_y} ${qs_x},${m_y} ${qs_x},340 ${qd_x},340`);

      // 6. 상태 분석 리포트 카드 및 배경색 동적 갱신
      const fbCard = document.getElementById('feedback-card');
      const diff = qs - qd;

      if (Math.abs(m_price - eq_price) < 0.5) {
        // 균형 상태
        fbCard.className = "p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-950/20 text-xs text-emerald-300 flex flex-col gap-1";
        fbCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-scale-balanced text-emerald-400"></i> 현재 상태: 시장 균형 (Equilibrium)</strong>
          <span>수요량(${qd.toFixed(1)})과 공급량(${qs.toFixed(1)})이 완벽히 일치합니다. 시장 재고 누적이나 품귀 없이 자원이 가장 효율적으로 배분되는 최적 상태입니다. 가격이 안정적으로 불변을 유지합니다.</span>
        `;
        gapArea.setAttribute('fill', 'none');
      } else if (m_price > eq_price) {
        // 초과 공급 (Surplus)
        fbCard.className = "p-3.5 rounded-xl border border-red-500/30 bg-red-950/20 text-xs text-red-300 flex flex-col gap-1";
        fbCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-circle-arrow-down text-red-400"></i> 현재 상태: 초과 공급 (Surplus) +${diff.toFixed(1)}</strong>
          <span>시장 가격이 높아서 기업들이 팔려는 수량(${qs.toFixed(1)})이 사려는 수량(${qd.toFixed(1)})보다 많은 재고 누적 상태입니다. 판매 기업들 간 가격 하락 경쟁이 생겨 가격이 <strong>하락 압력</strong>을 강하게 받습니다.</span>
        `;
        gapArea.setAttribute('fill', '#ef4444');
      } else {
        // 초과 수요 (Shortage)
        fbCard.className = "p-3.5 rounded-xl border border-amber-500/30 bg-amber-950/20 text-xs text-amber-300 flex flex-col gap-1";
        fbCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-circle-arrow-up text-amber-400"></i> 현재 상태: 초과 수요 (Shortage) +${Math.abs(diff).toFixed(1)}</strong>
          <span>시장 가격이 낮아 공급되는 수량(${qs.toFixed(1)})이 물건을 사려는 수량(${qd.toFixed(1)})보다 부족한 품귀 상태입니다. 구매자들 간 웃돈 거래 경쟁으로 가격이 <strong>상승 압력</strong>을 강하게 받습니다.</span>
        `;
        gapArea.setAttribute('fill', '#fbbf24');
      }

      // 7. 학제적 전이 분석 피드백 가이드
      const transFeedback = document.getElementById('transference-feedback');
      if (s_shift > 5) {
        transFeedback.innerHTML = `공급 곡선이 우측으로 크게 이동했습니다. 이는 물리학 관점에서 주 회로에 병렬로 우회 전류를 흘릴 수 있는 <strong>'병렬 분로 통로'</strong>가 개척된 원리와 매핑되며, 마켓 저항(R)을 낮추고 결과 유통량(Q, 전류)을 크게 확장시킵니다.`;
      } else if (s_shift < -5) {
        transFeedback.innerHTML = `공급 곡선이 좌측으로 이동했습니다. 이는 물리학 관점에서 주 회로 전류망에 높은 임피던스를 가진 저항이 <strong>'직렬로 추가 결합'</strong>되어, 전체 합성저항(R)을 올려 전류 유통을 억제하고 에너지 소모량을 급감시키는 효과에 대응됩니다.`;
      } else {
        transFeedback.innerHTML = `수요와 공급의 이동 값을 조작하면, 물리학의 옴의 법칙 및 계통 저항 임피던스(직렬/병렬 추가)가 어떻게 경제의 공급망 충격과 똑같은 구조를 가졌는지 위 피드백을 통해 대조 분석됩니다.`;
      }
    }

    // 시장 보이지 않는 손 구동 (균형 가격으로 이동)
    function autoEquilibrium() {
      const d_shift = parseInt(document.getElementById('slider-d-shift').value);
      const s_shift = parseInt(document.getElementById('slider-s-shift').value);
      const eq_qty = (90 + d_shift + s_shift) / 1.6;
      const eq_price = 10 + 0.8 * eq_qty - s_shift;

      // 슬라이더 가격을 균형 가격으로 강제 보정
      document.getElementById('slider-m-price').value = Math.round(eq_price);
      updateSimulation();
    }

    // 초기 리셋
    function resetAll() {
      document.getElementById('slider-d-shift').value = 0;
      document.getElementById('slider-s-shift').value = 0;
      document.getElementById('slider-m-price').value = 55;
      updateSimulation();
    }

    // 초기화 및 실시간 구동 시작
    window.onload = function() {
      updateSimulation();
    }
  </script>
</body>
</html>
"""

# Streamlit에 컴포넌트 삽입 (충분한 높이와 스크롤 허용으로 깔끔한 레이아웃 제공)
components.html(html_content, height=1350, scrolling=True)
