import streamlit as st
import streamlit.components.v1 as components

# ── 공통 스타일 시트 ──────────────────────────────────────────────
st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
}
.info-card {
    background: linear-gradient(135deg, #1e1b4b, #0f172a);
    border-left: 5px solid #818cf8;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.1);
}
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("<h1 class='main-title'>🔌 [탐구] PNP BJT 트랜지스터의 동작 원리와 포화</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-size: 0.95rem; margin-top: -5px;'>베이스 전압 및 컬렉터-이미터 전압 스윕을 통한 포화(Saturation) 영역과 활성(Active) 영역의 전류 거동을 실시간으로 시뮬레이션합니다.</p>", unsafe_allow_html=True)

st.markdown("""
<div class='info-card'>
    <b style='color:#c7d2fe; font-size:1.05rem;'>🎯 탐구 목표</b><br>
    <span style='color:#e2e8f0; font-size:0.92rem; line-height: 1.6;'>
    1. PNP 양극성 접합 트랜지스터(BJT)의 3가지 단자(Emitter, Base, Collector) 전류 관계를 이해합니다.<br>
    2. 컬렉터-이미터 전압($V_{CE}$)이 매우 낮을 때($V_{CE} < V_{CE,sat}$) 발생하는 <b>포화 영역</b>의 물리적 상태와 증폭률 $\beta$가 1 부근으로 하락하는 이유를 확인합니다.<br>
    3. 충분한 $V_{CE}$가 인가되었을 때 <b>활성 영역</b>에 진입하여 $I_C = \beta \cdot I_B$의 관계식에 따라 전류가 정상적으로 증폭되는 메커니즘을 탐구합니다.
    </span>
</div>
""", unsafe_allow_html=True)

# 시뮬레이터 HTML 코드 정의
html_content = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PNP BJT 트랜지스터 가상 실험실</title>
  
  <!-- Tailwind CSS & Web Fonts & FontAwesome -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

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
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #6366f1;
      cursor: pointer;
      transition: transform 0.1s ease;
    }
    input[type="range"]::-webkit-slider-thumb:hover {
      transform: scale(1.25);
    }
    .vbb-slider::-webkit-slider-thumb {
      background: #d946ef !important;
    }
    .rb-slider::-webkit-slider-thumb {
      background: #f59e0b !important;
    }
    .beta-slider::-webkit-slider-thumb {
      background: #10b981 !important;
    }
    .vcesat-slider::-webkit-slider-thumb {
      background: #ef4444 !important;
    }
    .vce-slider::-webkit-slider-thumb {
      background: #3b82f6 !important;
    }
  </style>
</head>
<body class="bg-slate-900 min-h-screen text-slate-100">

  <!-- 헤더 영역 -->
  <header class="bg-slate-950 text-white px-6 py-5 shadow-lg border-b border-indigo-950">
    <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div class="flex items-center gap-3">
        <div class="bg-indigo-600 text-white p-2.5 rounded-xl shadow-inner">
          <i class="fa-solid fa-microchip text-xl"></i>
        </div>
        <div>
          <h1 class="font-bold text-xl md:text-2xl tracking-tight">PNP BJT 트랜지스터 특성 실험실</h1>
          <p class="text-xs text-slate-400 mt-1">포화 영역과 활성 영역의 물리적 차이를 분석하고 실시간으로 전류 및 $\beta$를 관측하는 가상 브레드보드</p>
        </div>
      </div>
      <button onclick="resetAll()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-4 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 transition-all self-stretch md:self-auto justify-center">
        <i class="fa-solid fa-rotate-left"></i>
        <span>파라미터 초기화</span>
      </button>
    </div>
  </header>

  <!-- 메인 레이아웃 -->
  <main class="max-w-7xl mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">

    <!-- 왼쪽 조절 및 분석 패널 (4/12) -->
    <aside class="lg:col-span-4 flex flex-col gap-6">
      
      <!-- 컨트롤러 카드 -->
      <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700 shadow-md flex flex-col gap-4">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-2 border-b border-slate-700 pb-2">
          <i class="fa-solid fa-sliders text-indigo-400"></i>회로 파라미터 제어
        </h3>

        <!-- VBB 베이스 전원 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-magenta-400 text-fuchsia-400">베이스 전원 전압 (V_BB)</span>
            <span id="val-vbb" class="text-xs font-mono-jb font-bold text-fuchsia-300">5.60 V</span>
          </div>
          <input type="range" id="slider-vbb" min="0.0" max="10.0" step="0.1" value="5.6" oninput="updateSimulation()" class="w-full vbb-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
            <span>0.0V (차단)</span>
            <span>10.0V (강한 바이어스)</span>
          </div>
        </div>

        <!-- RB 베이스 저항 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-amber-400">베이스 저항 (R_B)</span>
            <span id="val-rb" class="text-xs font-mono-jb font-bold text-amber-300">100 kΩ</span>
          </div>
          <input type="range" id="slider-rb" min="10" max="250" step="5" value="100" oninput="updateSimulation()" class="w-full rb-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
            <span>10 kΩ</span>
            <span>250 kΩ</span>
          </div>
        </div>

        <!-- BETA_MAX 최대 증폭률 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-emerald-400">최대 증폭률 (β_max)</span>
            <span id="val-beta" class="text-xs font-mono-jb font-bold text-emerald-300">50</span>
          </div>
          <input type="range" id="slider-beta" min="10" max="150" step="5" value="50" oninput="updateSimulation()" class="w-full beta-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
            <span>10</span>
            <span>150</span>
          </div>
        </div>

        <!-- VCE_SAT 포화 전압 -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-rose-400">포화 임계 전압 (V_CE,sat)</span>
            <span id="val-vcesat" class="text-xs font-mono-jb font-bold text-rose-300">0.20 V</span>
          </div>
          <input type="range" id="slider-vcesat" min="0.1" max="1.0" step="0.05" value="0.2" oninput="updateSimulation()" class="w-full vcesat-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
            <span>0.1V (이상적 접합)</span>
            <span>1.0V (높은 접합 저항)</span>
          </div>
        </div>

        <hr class="border-slate-700 my-1">

        <!-- 관측 지점 VCE -->
        <div>
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-blue-400">컬렉터-이미터 전압 (V_CE 관측값)</span>
            <span id="val-vce" class="text-xs font-mono-jb font-bold text-blue-300">0.00 V</span>
          </div>
          <input type="range" id="slider-vce" min="0.0" max="10.0" step="0.05" value="0.0" oninput="updateSimulation()" class="w-full vce-slider">
          <div class="flex justify-between text-[10px] text-slate-400 mt-0.5">
            <span>0.0V (V_CE = 0 상황)</span>
            <span>10.0V (활성 영역)</span>
          </div>
        </div>
      </div>

      <!-- 실시간 결과 패널 -->
      <div class="bg-slate-950 rounded-2xl p-5 shadow-lg border border-indigo-950 flex flex-col gap-4">
        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2 border-b border-slate-800 pb-2">
          <i class="fa-solid fa-chart-pie text-indigo-400"></i>실시간 계측 보고서
        </h3>

        <!-- 측정 데이터 요약 -->
        <div class="grid grid-cols-3 gap-2">
          <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700 text-center">
            <div class="text-[9px] text-slate-400 font-medium">베이스 전류 (I_B)</div>
            <div id="report-ib" class="text-sm font-bold text-amber-400 font-mono-jb mt-1">50.0 uA</div>
          </div>
          <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700 text-center">
            <div class="text-[9px] text-slate-400 font-medium">컬렉터 전류 (I_C)</div>
            <div id="report-ic" class="text-sm font-bold text-blue-400 font-mono-jb mt-1">50.0 uA</div>
          </div>
          <div class="bg-slate-800 p-2.5 rounded-xl border border-slate-700 text-center">
            <div class="text-[9px] text-slate-400 font-medium">실제 증폭률 (β)</div>
            <div id="report-beta" class="text-sm font-bold text-emerald-400 font-mono-jb mt-1">1.00</div>
          </div>
        </div>

        <!-- 동작 상태 피드백 -->
        <div id="status-card" class="p-3.5 rounded-xl border flex flex-col gap-1 text-xs transition-all duration-300">
          <!-- JS에서 동적으로 채움 -->
        </div>

        <!-- 접합 바이어스 상태 다이어그램 (동적) -->
        <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 flex flex-col gap-2.5">
          <div class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
            <i class="fa-solid fa-circle-nodes text-indigo-400"></i>접합 바이어스 상태 (Junction Bias)
          </div>
          <div class="grid grid-cols-2 gap-2 text-[10px]">
            <div class="bg-slate-800/80 p-2 rounded-lg border border-slate-700/60">
              <span class="text-slate-400 block font-semibold">이미터-베이스 (EB) 접합</span>
              <strong id="bias-eb" class="text-xs font-bold block mt-1">순방향 바이어스</strong>
            </div>
            <div class="bg-slate-800/80 p-2 rounded-lg border border-slate-700/60">
              <span class="text-slate-400 block font-semibold">베이스-컬렉터 (BC) 접합</span>
              <strong id="bias-bc" class="text-xs font-bold block mt-1">순방향 바이어스 (포화)</strong>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 오른쪽 인터랙티브 그래프 공간 (8/12) -->
    <section class="lg:col-span-8 flex flex-col gap-6">
      
      <!-- 그래프 캔버스 카드 -->
      <div class="bg-slate-800 rounded-2xl p-5 border border-slate-700 shadow-md flex flex-col gap-5">
        <h3 class="font-bold text-slate-200 flex items-center gap-2 border-b border-slate-700 pb-2">
          <i class="fa-solid fa-chart-line text-indigo-400"></i>특성 곡선 시각화 (V_CE Sweep)
        </h3>

        <!-- 두 그래프를 1x2 그리드로 배치 또는 세로 배치 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- I_C vs V_CE -->
          <div class="bg-slate-950 p-4 rounded-xl shadow-inner border border-slate-900 flex flex-col items-center">
            <div class="text-xs font-bold text-slate-300 mb-2 self-start flex justify-between w-full">
              <span>(a) 컬렉터 전류 (I_C) vs V_CE</span>
              <span class="text-[9px] text-slate-500 font-normal">포화 영역: 적색 음영</span>
            </div>
            <div class="w-full relative" style="height: 250px;">
              <canvas id="chart-ic"></canvas>
            </div>
          </div>

          <!-- beta vs V_CE -->
          <div class="bg-slate-950 p-4 rounded-xl shadow-inner border border-slate-900 flex flex-col items-center">
            <div class="text-xs font-bold text-slate-300 mb-2 self-start flex justify-between w-full">
              <span>(b) 전류 증폭률 (β) vs V_CE</span>
              <span class="text-[9px] text-slate-500 font-normal">활성 한계선: 녹색 점선</span>
            </div>
            <div class="w-full relative" style="height: 250px;">
              <canvas id="chart-beta"></canvas>
            </div>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- BJT 원리 및 교과 개념 설명 영역 -->
  <section class="max-w-7xl mx-auto px-4 md:px-6 pb-12">
    <div class="bg-slate-800 rounded-2xl p-6 md:p-8 border border-slate-700 shadow-md flex flex-col gap-6">
      
      <div class="border-b border-slate-700 pb-4">
        <h2 class="text-xl font-bold text-slate-100 flex items-center gap-2">
          <i class="fa-solid fa-graduation-cap text-indigo-400"></i>BJT 트랜지스터 교안: 물리적 원리와 해석
        </h2>
        <p class="text-xs text-slate-400 mt-1">포화 및 활성 영역의 바이어스 메커니즘과 브레드보드에서의 측정 현상 탐구</p>
      </div>

      <!-- 시각 자료: PNP 동작 구조 단면도 (SVG) -->
      <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        <div class="md:col-span-5 flex justify-center bg-slate-950/80 p-4 rounded-xl border border-slate-850">
          <svg width="280" height="200" viewBox="0 0 280 200" class="select-none">
            <!-- Emitter block (P) -->
            <rect x="20" y="50" width="70" height="80" fill="#2563eb" rx="5" opacity="0.85"/>
            <text x="55" y="95" fill="white" font-size="16" font-weight="900" text-anchor="middle">P</text>
            <text x="55" y="115" fill="#93c5fd" font-size="10" text-anchor="middle">Emitter (이미터)</text>
            
            <!-- Base block (N) -->
            <rect x="100" y="50" width="80" height="80" fill="#f59e0b" rx="5" opacity="0.85"/>
            <text x="140" y="95" fill="white" font-size="16" font-weight="900" text-anchor="middle">N</text>
            <text x="140" y="115" fill="#fde68a" font-size="10" text-anchor="middle">Base (베이스)</text>
            
            <!-- Collector block (P) -->
            <rect x="190" y="50" width="70" height="80" fill="#2563eb" rx="5" opacity="0.85"/>
            <text x="225" y="95" fill="white" font-size="16" font-weight="900" text-anchor="middle">P</text>
            <text x="225" y="115" fill="#93c5fd" font-size="10" text-anchor="middle">Collector (컬렉터)</text>

            <!-- Junction interface dashed lines -->
            <line x1="95" y1="50" x2="95" y2="130" stroke="#f1f5f9" stroke-width="1.5" stroke-dasharray="3,3"/>
            <line x1="185" y1="50" x2="185" y2="130" stroke="#f1f5f9" stroke-width="1.5" stroke-dasharray="3,3"/>
            
            <!-- Carrier movement representations (holes) -->
            <!-- E to B injection -->
            <circle cx="70" cy="70" r="3.5" fill="#ef4444"/>
            <circle cx="85" cy="70" r="3.5" fill="#ef4444"/>
            <path d="M 70 70 Q 80 65 90 70" fill="none" stroke="#ef4444" stroke-width="1" marker-end="url(#arrow)"/>
            
            <!-- B to C collection -->
            <circle cx="120" cy="70" r="3.5" fill="#ef4444"/>
            <circle cx="160" cy="70" r="3.5" fill="#ef4444"/>
            <path d="M 120 70 C 140 65, 170 65, 200 70" fill="none" stroke="#ef4444" stroke-width="1" marker-end="url(#arrow)"/>
            
            <!-- Base recombination/leakage (I_B) -->
            <path d="M 140 70 L 140 160" fill="none" stroke="#f59e0b" stroke-width="1.5" marker-end="url(#arrow)"/>
            
            <!-- Emitter current input arrow -->
            <path d="M 5 90 L 20 90" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
            <text x="5" y="82" fill="#60a5fa" font-size="10" font-family="JetBrains Mono">I_E</text>

            <!-- Collector current output arrow -->
            <path d="M 260 90 L 275 90" fill="none" stroke="#2563eb" stroke-width="2" marker-end="url(#arrow)"/>
            <text x="260" y="82" fill="#60a5fa" font-size="10" font-family="JetBrains Mono">I_C</text>

            <!-- Base current output arrow -->
            <text x="148" y="165" fill="#fbbf24" font-size="10" font-family="JetBrains Mono">I_B</text>

            <!-- SVG definitions for arrows -->
            <defs>
              <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 2 L 8 5 L 0 8 z" fill="#e2e8f0" />
              </marker>
            </defs>
          </svg>
        </div>

        <div class="md:col-span-7 flex flex-col gap-2.5 text-xs text-slate-300 leading-relaxed">
          <h4 class="font-bold text-slate-200 text-sm">1. PNP BJT의 단자 전류와 전하 유동</h4>
          <p>
            양극성 접합 트랜지스터(BJT)는 얇은 베이스 영역을 사이에 두고 두 개의 다수 반도체 접합으로 이루어집니다. 
            PNP 트랜지스터의 경우, 주요 전하 캐리어는 **정공(Hole)**입니다.
          </p>
          <ul class="space-y-1.5 list-disc pl-4 text-slate-400">
            <li><strong>이미터 (Emitter):</strong> 캐리어(정공)를 활발하게 방출하는 영역입니다. 다수 정공이 도핑되어 있습니다.</li>
            <li><strong>베이스 (Base):</strong> 아주 얇고 가볍게 도핑되어 있어, 이미터에서 주입된 정공의 극히 일부(약 1~2%)만 베이스 단자로 재결합되어 흘러나가게 합니다 ($I_B$).</li>
            <li><strong>컬렉터 (Collector):</strong> 베이스를 무사히 통과한 나머지 대다수의 정공(98% 이상)을 전기장으로 수집하는 단자입니다 ($I_C$).</li>
            <li><strong>키르히호프의 전류 법칙 (KCL):</strong> $I_E = I_B + I_C$ 이 성립합니다.</li>
          </ul>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
        <!-- 포화 vs 활성 영역 물리 바이어스 비교 -->
        <div class="bg-indigo-950/20 border border-indigo-900/40 rounded-xl p-5">
          <h4 class="font-bold text-indigo-300 flex items-center gap-1.5 mb-2.5">
            <i class="fa-solid fa-compress text-indigo-400"></i>2. 동작 영역별 바이어스 조건 (PNP 기준)
          </h4>
          <div class="space-y-3 text-xs">
            <div>
              <strong class="text-rose-400 block">■ 포화 영역 (Saturation Region): EB 접합 순방향 & BC 접합 순방향</strong>
              <p class="text-slate-300 mt-1 leading-relaxed">
                $V_{CE}$의 절대값이 매우 낮아 컬렉터 전위가 이미터와 유사한 수준(순방향)일 때 발생합니다. 컬렉터와 베이스 사이에도 순방향 전압이 인가되어, 컬렉터 단자가 이미터에서 온 캐리어를 능동적으로 끌어당기지 못합니다. 
                이 영역에서 $I_C$는 베이스 전류인 $I_B$와 비슷한 수준으로 크게 제한되며, $\beta = I_C / I_B$는 정상 증폭률($\beta_{max}$)이 아닌 1 근방의 매우 낮은 값을 가집니다.
              </p>
            </div>
            <div>
              <strong class="text-emerald-400 block">■ 활성 영역 (Active Region): EB 접합 순방향 & BC 접합 역방향</strong>
              <p class="text-slate-300 mt-1 leading-relaxed">
                컬렉터 단자에 충분한 역방향 전압($|V_{CE}| \ge 0.2\text{V}$)이 가해지면, 베이스-컬렉터 접합에 강한 역방향 장벽이 생깁니다. 베이스로 진입한 정공들은 이 강한 전기장에 휩쓸려 신속하게 컬렉터로 끌려갑니다. 
                이 때 $I_C$는 오직 베이스 전류 $I_B$에 비례하여 결정되며($I_C = \beta_{max} \cdot I_B$), 증폭 소자로서의 역할을 수행합니다.
              </p>
            </div>
          </div>
        </div>

        <!-- 왜 V_CE = 0에서 beta가 1로 보일까? -->
        <div class="bg-amber-955/10 border border-amber-900/30 rounded-xl p-5 bg-amber-950/10">
          <h4 class="font-bold text-amber-300 flex items-center gap-1.5 mb-2.5">
            <i class="fa-solid fa-circle-question text-amber-400"></i>3. 왜 V_CE = 0V에서 β ≈ 1로 측정될까?
          </h4>
          <p class="text-xs text-slate-300 leading-relaxed space-y-2">
            실제 브레드보드 실험에서 베이스 전원을 $5.6\text{V}$에 인가하고 컬렉터 전원을 연결하지 않거나 $0\text{V}$로 인가할 경우,
            측정된 베이스 전류 $I_B \approx 50.6\,\mu\text{A}$ 와 컬렉터 전류 $I_C \approx 50.4\,\mu\text{A}$의 크기가 거의 같은 현상이 발견됩니다.
            <br><br>
            <strong>이유 분석:</strong><br>
            1. **BC 접합의 순방향화:** 컬렉터 단자의 전압이 $0\text{V}$이므로 E-B 간 순방향 전압강하($V_{EB} \approx 0.6\text{V}$)에 의해 베이스 전위는 약 $5.0\text{V}$가 됩니다. 즉, 베이스($5.0\text{V}$)가 컬렉터($0\text{V}$)보다 높은 상태입니다. (PNP 관점에서는 컬렉터가 베이스에 대해 전압이 가해지지 않아 BC 접합이 전도 상태에 이르게 됩니다.)<br>
            2. **수집 전계 상실:** E-B 순방향 바이어스에 의해 이미터에서 주입된 대다수의 정공은 베이스로 도달했으나, 컬렉터 측의 전기장 상실 및 다이오드 구조 상의 내부 전압에 막혀 컬렉터로 넘어가지 못하고 정체됩니다.<br>
            3. **결론:** 전류는 증폭 작용을 완전히 상실하여, 베이스를 통해 다이오드 순방향 전도로 흘러나가는 양과 유사하게 아주 미미한 수준만 컬렉터로 흘러나가게 됩니다 ($I_C \approx I_B$). 이 상태를 회로 이론에서는 **완전 포화(Deep Saturation)** 혹은 **차단 경계**라고 부릅니다.
          </p>
        </div>
      </div>

    </div>
  </section>

  <!-- 시뮬레이션 계산 및 차트 갱신 JS 엔진 -->
  <script>
    // 전역 차트 변수
    let chartIc = null;
    let chartBeta = null;

    // 포화 영역 배경 채우기 플러그인 정의
    const saturationZonePlugin = {
      id: 'saturationZone',
      beforeDraw(chart, args, options) {
        const {ctx, chartArea: {top, right, bottom, left}, scales: {x, y}} = chart;
        const vceSatVal = options.vceSat;
        if (vceSatVal === undefined) return;
        const xPixelLimit = x.getPixelForValue(vceSatVal);
        const xPixelStart = x.getPixelForValue(0);
        
        ctx.save();
        ctx.fillStyle = 'rgba(239, 68, 68, 0.15)'; // Tailwind rose/red 500 alpha 0.15
        ctx.fillRect(xPixelStart, top, xPixelLimit - xPixelStart, bottom - top);
        ctx.restore();
      }
    };

    // Chart.js 플러그인 등록
    Chart.register(saturationZonePlugin);

    // 시뮬레이션 계산 함수
    function runSimulationData(vbb, rb, betaMax, vceSat) {
      const veb_on = 0.60;
      let ib = 0;
      if (vbb > veb_on) {
        ib = (vbb - veb_on) / (rb * 1000); // R_B는 kOhm 단위로 받음
      }
      
      const vceRange = [];
      const icRange = [];
      const betaRange = [];
      
      const steps = 100;
      for (let i = 0; i <= steps; i++) {
        let vce = (10.0 / steps) * i;
        vceRange.push(vce);
        
        let ic = 0;
        if (ib > 0) {
          if (vce < vceSat) {
            // 포화 영역 선형 보간
            let ratio = vce / vceSat;
            ic = ib * (1 + (betaMax - 1) * ratio);
          } else {
            // 활성 영역 + 얼리 효과
            let early = 1 + 0.01 * Math.min(vce - vceSat, 10);
            ic = betaMax * ib * early;
          }
        }
        icRange.push(ic * 1e6); // uA 단위 변환
        betaRange.push(ib > 0 ? ic / ib : 0);
      }

      return {
        ib: ib * 1e6, // uA
        vceRange,
        icRange,
        betaRange
      };
    }

    function updateSimulation() {
      // 1. 슬라이더 인풋값 파싱
      const vbb = parseFloat(document.getElementById('slider-vbb').value);
      const rb = parseFloat(document.getElementById('slider-rb').value);
      const betaMax = parseInt(document.getElementById('slider-beta').value);
      const vceSat = parseFloat(document.getElementById('slider-vcesat').value);
      const vceObs = parseFloat(document.getElementById('slider-vce').value);

      // 레이블 출력 업데이트
      document.getElementById('val-vbb').innerText = vbb.toFixed(2) + " V";
      document.getElementById('val-rb').innerText = rb.toFixed(0) + " kΩ";
      document.getElementById('val-beta').innerText = betaMax;
      document.getElementById('val-vcesat').innerText = vceSat.toFixed(2) + " V";
      document.getElementById('val-vce').innerText = vceObs.toFixed(2) + " V";

      // 2. 물리 연산
      const simData = runSimulationData(vbb, rb, betaMax, vceSat);
      const ibVal = simData.ib; // uA

      // 관측 포인트의 I_C, beta 연산
      let icObs = 0;
      let betaObs = 0;
      if (ibVal > 0) {
        const ibAmp = ibVal / 1e6; // A
        if (vceObs < vceSat) {
          let ratio = vceObs / vceSat;
          icObs = ibAmp * (1 + (betaMax - 1) * ratio);
        } else {
          let early = 1 + 0.01 * Math.min(vceObs - vceSat, 10);
          icObs = betaMax * ibAmp * early;
        }
        icObs = icObs * 1e6; // uA
        betaObs = icObs / ibVal;
      }

      // 리포트 갱신
      document.getElementById('report-ib').innerText = ibVal.toFixed(1) + " uA";
      document.getElementById('report-ic').innerText = icObs.toFixed(1) + " uA";
      document.getElementById('report-beta').innerText = betaObs.toFixed(2);

      // 3. 상태 카드 및 접합 바이어스 텍스트 업데이트
      const statusCard = document.getElementById('status-card');
      const biasEB = document.getElementById('bias-eb');
      const biasBC = document.getElementById('bias-bc');

      if (vbb <= 0.60) {
        statusCard.className = "p-3.5 rounded-xl border border-slate-700 bg-slate-800 text-xs text-slate-400 flex flex-col gap-1";
        statusCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-power-off text-slate-500"></i> 현재 상태: 차단 영역 (Cut-off)</strong>
          <span>베이스 전위 차가 실리콘 접합 활성 전압인 0.6V 이하이므로 이미터-베이스 접합에 전류가 흐르지 않고 트랜지스터 스위치가 완전히 꺼져 있습니다.</span>
        `;
        biasEB.innerText = "역방향 / 차단";
        biasEB.className = "text-xs font-bold block mt-1 text-slate-500";
        biasBC.innerText = "역방향";
        biasBC.className = "text-xs font-bold block mt-1 text-slate-500";
      } else if (vceObs < vceSat) {
        statusCard.className = "p-3.5 rounded-xl border border-rose-500/30 bg-rose-950/20 text-xs text-rose-300 flex flex-col gap-1";
        statusCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-compress text-rose-400"></i> 현재 상태: 포화 영역 (Saturation)</strong>
          <span>V_CE(${vceObs.toFixed(2)}V)가 포화 전압(${vceSat.toFixed(2)}V)보다 작아 E-B 접합과 B-C 접합이 모두 순방향으로 작동하여 증폭 효율이 떨어집니다. 이 지점에서는 β ≈ ${betaObs.toFixed(1)} 로 보여 전류 증폭 효과를 보기 어렵습니다.</span>
        `;
        biasEB.innerText = "순방향 바이어스";
        biasEB.className = "text-xs font-bold block mt-1 text-emerald-400";
        biasBC.innerText = "순방향 바이어스 (포화)";
        biasBC.className = "text-xs font-bold block mt-1 text-rose-400";
      } else {
        statusCard.className = "p-3.5 rounded-xl border border-emerald-500/30 bg-emerald-950/20 text-xs text-emerald-300 flex flex-col gap-1";
        statusCard.innerHTML = `
          <strong class="flex items-center gap-1.5"><i class="fa-solid fa-bolt text-emerald-400"></i> 현재 상태: 활성 영역 (Active)</strong>
          <span>V_CE가 충분히 인가되어 B-C 접합이 역방향 바이어스로 안정되었습니다. 이미터 정공이 컬렉터로 정상 전도되며, I_C ≈ ${betaMax} * I_B 의 높은 전류 증폭이 성공적으로 일어납니다 (β ≈ ${betaObs.toFixed(1)}).</span>
        `;
        biasEB.innerText = "순방향 바이어스";
        biasEB.className = "text-xs font-bold block mt-1 text-emerald-400";
        biasBC.innerText = "역방향 바이어스 (안정)";
        biasBC.className = "text-xs font-bold block mt-1 text-indigo-400";
      }

      // 4. 차트 데이터 업데이트
      // (a) I_C 및 I_B 차트
      chartIc.data.labels = simData.vceRange;
      chartIc.data.datasets[0].data = simData.icRange;
      chartIc.data.datasets[1].data = Array(simData.vceRange.length).fill(ibVal);
      chartIc.data.datasets[2].data = [{x: vceObs, y: icObs}];
      chartIc.options.plugins.saturationZone.vceSat = vceSat;
      chartIc.update();

      // (b) beta 차트
      chartBeta.data.labels = simData.vceRange;
      chartBeta.data.datasets[0].data = simData.betaRange;
      chartBeta.data.datasets[1].data = Array(simData.vceRange.length).fill(betaMax);
      chartBeta.data.datasets[2].data = [{x: vceObs, y: betaObs}];
      chartBeta.options.plugins.saturationZone.vceSat = vceSat;
      chartBeta.update();
    }

    // 차트 인스턴스 초기화
    function initCharts() {
      const ctxIc = document.getElementById('chart-ic').getContext('2d');
      chartIc = new Chart(ctxIc, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: '컬렉터 전류 I_C (uA)',
              borderColor: '#3b82f6',
              borderWidth: 2.5,
              data: [],
              pointRadius: 0,
              fill: false
            },
            {
              label: '베이스 전류 I_B (uA)',
              borderColor: '#f59e0b',
              borderWidth: 1.5,
              borderDash: [5, 5],
              data: [],
              pointRadius: 0,
              fill: false
            },
            {
              label: '현재 측정점',
              backgroundColor: '#ec4899',
              borderColor: '#ffffff',
              borderWidth: 2,
              data: [],
              pointRadius: 6,
              pointHoverRadius: 8,
              showLine: false,
              z: 10
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: '|V_CE| [V]',
                color: '#94a3b8',
                font: { size: 10 }
              },
              grid: { color: '#1e293b' },
              ticks: { color: '#94a3b8' }
            },
            y: {
              title: {
                display: true,
                text: '전류 [uA]',
                color: '#94a3b8',
                font: { size: 10 }
              },
              grid: { color: '#1e293b' },
              ticks: { color: '#94a3b8' }
            }
          },
          plugins: {
            legend: {
              labels: { color: '#e2e8f0', boxWidth: 15, font: { size: 9 } }
            },
            saturationZone: {
              vceSat: 0.20
            }
          }
        }
      });

      const ctxBeta = document.getElementById('chart-beta').getContext('2d');
      chartBeta = new Chart(ctxBeta, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: '증폭률 beta (Ic/Ib)',
              borderColor: '#a78bfa',
              borderWidth: 2.5,
              data: [],
              pointRadius: 0,
              fill: false
            },
            {
              label: '최대 증폭률 beta_max',
              borderColor: '#10b981',
              borderWidth: 1.5,
              borderDash: [5, 5],
              data: [],
              pointRadius: 0,
              fill: false
            },
            {
              label: '현재 측정점',
              backgroundColor: '#ec4899',
              borderColor: '#ffffff',
              borderWidth: 2,
              data: [],
              pointRadius: 6,
              pointHoverRadius: 8,
              showLine: false,
              z: 10
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'linear',
              position: 'bottom',
              title: {
                display: true,
                text: '|V_CE| [V]',
                color: '#94a3b8',
                font: { size: 10 }
              },
              grid: { color: '#1e293b' },
              ticks: { color: '#94a3b8' }
            },
            y: {
              title: {
                display: true,
                text: 'beta = Ic/Ib',
                color: '#94a3b8',
                font: { size: 10 }
              },
              grid: { color: '#1e293b' },
              ticks: { color: '#94a3b8' }
            }
          },
          plugins: {
            legend: {
              labels: { color: '#e2e8f0', boxWidth: 15, font: { size: 9 } }
            },
            saturationZone: {
              vceSat: 0.20
            }
          }
        }
      });
    }

    function resetAll() {
      document.getElementById('slider-vbb').value = 5.6;
      document.getElementById('slider-rb').value = 100;
      document.getElementById('slider-beta').value = 50;
      document.getElementById('slider-vcesat').value = 0.2;
      document.getElementById('slider-vce').value = 0.0;
      updateSimulation();
    }

    // 초기 실행
    window.onload = function() {
      initCharts();
      updateSimulation();
    }
  </script>
</body>
</html>
"""

# Streamlit에 컴포넌트 삽입
components.html(html_content, height=1250, scrolling=True)
