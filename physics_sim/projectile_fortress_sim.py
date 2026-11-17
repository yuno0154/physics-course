import streamlit as st
import streamlit.components.v1 as components

st.title("🎯 [게임] 물리 포트리스: 포물선 탄도 포격전")
st.caption("정통 포트리스 스타일 포격 액션과 포물선 운동 물리학(v₀, θ, 보각 90°−θ, 바람 가속도)을 결합한 인터랙티브 시뮬레이션 게임")

HTML_CODE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', 'Malgun Gothic', sans-serif; user-select: none; }
  body { background: #070b14; color: #f8fafc; padding: 8px; overflow-x: hidden; }

  /* 전체 게임 아케이드 프레임 */
  .arcade-shell {
    background: linear-gradient(180deg, #111827 0%, #090d16 100%);
    border: 2px solid #334155;
    border-radius: 16px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.75), inset 0 1px 0 rgba(255,255,255,0.1);
    overflow: hidden;
  }

  /* 상단 미션 & 환경 바 */
  .top-header {
    display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 8px;
    padding: 10px 14px;
    background: linear-gradient(90deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border-bottom: 2px solid #334155;
  }
  .stage-tabs { display: flex; flex-wrap: wrap; gap: 5px; }
  .st-btn {
    background: #0f172a; color: #94a3b8; border: 1px solid #334155; border-radius: 8px;
    padding: 6px 11px; font-size: 12.5px; font-weight: 800; cursor: pointer; transition: all 0.15s;
  }
  .st-btn:hover { color: #f8fafc; border-color: #60a5fa; transform: translateY(-1px); }
  .st-btn.active {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    color: #fff; border-color: #93c5fd;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.55);
  }

  .top-right-tools { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .tool-sel, .tool-btn {
    background: #0f172a; color: #e2e8f0; border: 1px solid #475569; border-radius: 7px;
    padding: 5px 9px; font-size: 12px; font-weight: 700; cursor: pointer;
  }
  .tool-btn:hover { border-color: #38bdf8; color: #38bdf8; }

  /* 메인 캔버스 뷰포트 */
  .viewport {
    position: relative; width: 100%; height: 490px; background: #050811; overflow: hidden;
  }
  canvas { display: block; width: 100%; height: 100%; }

  /* 상단 인게임 오버레이 HUD */
  .hud-top {
    position: absolute; top: 10px; left: 12px; right: 12px;
    display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none;
  }
  .player-card {
    background: rgba(15, 23, 42, 0.82); border: 1.5px solid rgba(96, 165, 250, 0.45);
    border-radius: 12px; padding: 8px 13px; min-width: 225px;
    backdrop-filter: blur(6px); box-shadow: 0 4px 15px rgba(0,0,0,0.4);
  }
  .player-card.enemy { border-color: rgba(248, 113, 113, 0.5); text-align: right; }
  .p-name { font-size: 13px; font-weight: 900; letter-spacing: -0.02em; display: flex; justify-content: space-between; align-items: center; }
  .p-sub { font-size: 11.5px; color: #cbd5e1; margin-top: 3px; }

  /* 중앙 풍향계 & 턴 표시 */
  .center-hud {
    display: flex; flex-direction: column; align-items: center; gap: 5px;
  }
  .turn-pill {
    background: linear-gradient(90deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95), rgba(30,41,59,0.9));
    border: 1.5px solid #facc15; border-radius: 99px; padding: 4px 18px;
    font-size: 12.5px; font-weight: 900; color: #fde047; letter-spacing: 0.03em;
    box-shadow: 0 0 14px rgba(250, 204, 21, 0.3);
  }
  .wind-box {
    background: rgba(9, 13, 22, 0.88); border: 1.5px solid #38bdf8; border-radius: 10px;
    padding: 5px 14px; display: flex; align-items: center; gap: 8px;
    font-size: 12.5px; font-weight: 800; color: #38bdf8;
  }

  /* 실시간 물리 텔레메트리 플로팅 패널 */
  .telemetry-overlay {
    position: absolute; bottom: 10px; left: 12px;
    background: rgba(9, 13, 22, 0.84); border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 10px; padding: 7px 12px; font-size: 11.5px; color: #cbd5e1;
    display: flex; gap: 14px; pointer-events: none; backdrop-filter: blur(4px);
  }
  .tele-item b { color: #38bdf8; font-weight: 800; }

  /* 중앙 배너 알림 */
  .center-banner {
    position: absolute; top: 38%; left: 50%; transform: translate(-50%, -50%) scale(0.95);
    background: rgba(9, 13, 22, 0.93); border: 2px solid #facc15; border-radius: 16px;
    padding: 14px 28px; text-align: center; pointer-events: none;
    opacity: 0; transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 15px 35px rgba(0,0,0,0.75);
  }
  .center-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  .center-banner .b-title { font-size: 21px; font-weight: 900; color: #fde047; text-shadow: 0 2px 10px rgba(250,204,21,0.4); }
  .center-banner .b-sub { font-size: 13px; color: #e2e8f0; margin-top: 4px; font-weight: 600; }

  /* ════════════════════════════════════════════════════════════════
     정통 포트리스 2 스타일 하단 대시보드 (Bottom Control Deck)
     ════════════════════════════════════════════════════════════════ */
  .fortress-deck {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    border-top: 3px solid #475569;
    padding: 12px 14px;
    display: grid;
    grid-template-columns: 210px 1fr 275px;
    gap: 12px;
    align-items: center;
  }
  @media (max-width: 900px) {
    .fortress-deck { grid-template-columns: 1fr; }
  }

  /* 1) 좌측: 각도기 레이더 다이얼 & 무기 선택 */
  .dial-panel {
    display: flex; align-items: center; gap: 10px;
    background: #090d16; border: 1.5px solid #334155; border-radius: 12px; padding: 8px 10px;
  }
  .dial-canvas-wrap { position: relative; width: 84px; height: 84px; flex-shrink: 0; }
  .dial-info { flex: 1; font-size: 12px; line-height: 1.45; }
  .dial-angle-big { font-size: 20px; font-weight: 900; color: #38bdf8; }
  .mini-btns { display: flex; gap: 4px; margin-top: 4px; }
  .mini-btn {
    background: #1e293b; color: #e2e8f0; border: 1px solid #475569; border-radius: 5px;
    padding: 3px 7px; font-size: 11px; font-weight: 800; cursor: pointer;
  }
  .mini-btn:hover { border-color: #38bdf8; color: #38bdf8; }

  /* 2) 중앙: 포트리스 파워 게이지 & 체력/연료 바 & 무기 슬롯 */
  .gauge-panel {
    background: #090d16; border: 1.5px solid #334155; border-radius: 12px; padding: 10px 14px;
  }
  .weapon-bar {
    display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; gap: 6px; flex-wrap: wrap;
  }
  .wpn-slots { display: flex; gap: 5px; flex-wrap: wrap; }
  .wpn-btn {
    background: #1e293b; color: #cbd5e1; border: 1.5px solid #334155; border-radius: 7px;
    padding: 4px 9px; font-size: 11.5px; font-weight: 800; cursor: pointer; transition: 0.15s;
  }
  .wpn-btn.active {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: #090d16; border-color: #fde047; box-shadow: 0 0 10px rgba(245, 158, 11, 0.45);
  }

  /* 파워 바 (0 ~ 80 m/s) */
  .bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; }
  .bar-label {
    width: 66px; font-size: 11.5px; font-weight: 900; color: #94a3b8;
    letter-spacing: 0.04em; text-align: right;
  }
  .power-track {
    flex: 1; height: 22px; background: #111827; border: 1.5px solid #475569;
    border-radius: 6px; position: relative; overflow: visible; cursor: pointer;
  }
  .power-fill {
    height: 100%; width: 52%; border-radius: 4px;
    background: linear-gradient(90deg, #22c55e 0%, #eab308 55%, #ef4444 90%, #dc2626 100%);
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.35);
    transition: width 0.02s linear;
  }
  .power-grid-lines {
    position: absolute; inset: 0;
    background-image: repeating-linear-gradient(90deg, transparent, transparent 12.3%, rgba(255,255,255,0.14) 12.3%, rgba(255,255,255,0.14) 12.5%);
    pointer-events: none;
  }
  /* 이전 발사 마커 (빨강 ▲) & 탄도 계산기 추천 마커 (노랑 ▼) */
  .prev-marker {
    position: absolute; bottom: -7px; width: 0; height: 0;
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-bottom: 7px solid #f87171; transform: translateX(-5px); display: none;
  }
  .hint-marker {
    position: absolute; top: -7px; width: 0; height: 0;
    border-left: 5px solid transparent; border-right: 5px solid transparent;
    border-top: 7px solid #facc15; transform: translateX(-5px);
  }
  .bar-val {
    min-width: 72px; font-size: 13px; font-weight: 900; color: #fde047; text-align: right;
  }

  .sub-bars { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .small-track {
    flex: 1; height: 11px; background: #111827; border: 1px solid #334155; border-radius: 99px; overflow: hidden;
  }
  .hp-fill { height: 100%; width: 100%; background: linear-gradient(90deg, #ef4444, #22c55e); transition: width 0.25s; }
  .fuel-fill { height: 100%; width: 100%; background: linear-gradient(90deg, #0ea5e9, #38bdf8); transition: width 0.15s; }

  /* 3) 우측: 정밀 슬라이더 & 발사 버튼 */
  .action-panel {
    background: #090d16; border: 1.5px solid #334155; border-radius: 12px; padding: 10px 12px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .sl-line { display: flex; align-items: center; gap: 6px; font-size: 12px; }
  .sl-line span { width: 58px; font-weight: 700; color: #cbd5e1; }
  .sl-line input[type=range] { flex: 1; accent-color: #38bdf8; cursor: pointer; }
  .fire-btn-row { display: flex; gap: 6px; margin-top: 2px; }
  .fire-big {
    flex: 1; padding: 10px 12px; border-radius: 9px; border: 1.5px solid #f87171;
    background: linear-gradient(180deg, #ef4444 0%, #b91c1c 100%);
    color: #fff; font-size: 14px; font-weight: 900; cursor: pointer;
    box-shadow: 0 4px 14px rgba(239, 68, 68, 0.45); transition: 0.12s;
  }
  .fire-big:hover { filter: brightness(1.12); transform: translateY(-1px); }
  .fire-big:active { transform: translateY(1px); }
  .fire-big:disabled { opacity: 0.45; cursor: not-allowed; }

  .opt-bar {
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    padding: 7px 14px; background: #090d16; border-top: 1px solid #1e293b; font-size: 12px; color: #94a3b8;
  }
  .opt-checks { display: flex; gap: 12px; flex-wrap: wrap; }
  .opt-checks label { display: flex; align-items: center; gap: 4px; cursor: pointer; color: #cbd5e1; font-weight: 600; }
</style>
</head>
<body>

<div class="arcade-shell">
  <!-- 상단 스테이지 & 환경 설정 바 -->
  <div class="top-header">
    <div class="stage-tabs">
      <button class="st-btn active" onclick="setStage(1)">🎯 STAGE 1: 평지 탄도 훈련</button>
      <button class="st-btn" onclick="setStage(2)">⛰️ STAGE 2: 험준한 산맥 (고각 포격)</button>
      <button class="st-btn" onclick="setStage(3)">🏰 STAGE 3: 천공의 요새 (고지대 타격)</button>
      <button class="st-btn" onclick="setStage(4)">🌪️ STAGE 4: 폭풍의 협곡 (강풍 보정)</button>
      <button class="st-btn" onclick="setStage(5)">⚔️ STAGE 5: AI 슈퍼탱크 데스매치</button>
    </div>
    <div class="top-right-tools">
      <select id="tankSelect" class="tool-sel" onchange="changeTankType()">
        <option value="cannon">🛡️ 캐논 (대구경 고폭형)</option>
        <option value="missile">⚡ 듀크 (다연장 미사일형)</option>
        <option value="laser">🌟 슈퍼탱크 (플라즈마 정밀형)</option>
      </select>
      <select id="gravSelect" class="tool-sel" onchange="changeGravity()">
        <option value="9.8">🌍 지구 (g=9.8m/s²)</option>
        <option value="3.7">🔴 화성 (g=3.7m/s²)</option>
        <option value="1.6">🌙 달 (g=1.6m/s²)</option>
      </select>
      <button class="tool-btn" id="soundBtn" onclick="toggleSound()">🔊 효과음 ON</button>
      <button class="tool-btn" onclick="resetStage()">🔄 새 지형</button>
    </div>
  </div>

  <!-- 메인 게임 뷰포트 -->
  <div class="viewport">
    <canvas id="gameCanvas" width="1060" height="490"></canvas>

    <!-- 상단 오버레이 -->
    <div class="hud-top">
      <div class="player-card">
        <div class="p-name">
          <span style="color:#38bdf8;">🟦 PLAYER 1 (내 탱크)</span>
          <span id="p1HpTxt" style="color:#4ade80;">HP 100%</span>
        </div>
        <div class="p-sub">
          표적 거리: <b style="color:#fde047;">Δx = <span id="hudDx">0.0</span> m</b> ·
          고도차: <b style="color:#fde047;">Δy = <span id="hudDy">0.0</span> m</b>
        </div>
        <div class="p-sub" style="color:#94a3b8;" id="stageMissionTxt">
          평지 수평 도달거리 R = (v₀² sin2θ)/g 공식을 이용해 명중시키세요!
        </div>
      </div>

      <div class="center-hud">
        <div class="turn-pill" id="turnBanner">⚡ PLAYER 1 TURN — 조준 후 발사하세요!</div>
        <div class="wind-box" id="windBox">
          <span id="windIcon">🌬️</span>
          <span id="windText">WIND: 0.0 m/s² (무풍)</span>
        </div>
      </div>

      <div class="player-card enemy">
        <div class="p-name">
          <span id="p2HpTxt" style="color:#f87171;">HP 100%</span>
          <span style="color:#f87171;" id="enemyTitle">🟥 TARGET BASTION</span>
        </div>
        <div class="p-sub">
          명중 기록: <b style="color:#facc15;" id="scoreHits">0</b> hits / <span id="scoreShots">0</span> shots
        </div>
        <div class="p-sub" style="color:#94a3b8;">
          직전 탄도: <span id="prevShotTxt">기록 없음</span>
        </div>
      </div>
    </div>

    <!-- 하단 실시간 물리 텔레메트리 -->
    <div class="telemetry-overlay">
      <div class="tele-item">수평 초기속도 <b>v₀x = <span id="tV0x">29.7</span> m/s</b></div>
      <div class="tele-item">연직 초기속도 <b>v₀y = <span id="tV0y">29.7</span> m/s</b></div>
      <div class="tele-item">이론 최고높이(평지) <b>H = <span id="tTheoH">45.0</span> m</b></div>
      <div class="tele-item">이론 도달거리(평지) <b>R = <span id="tTheoR">180.0</span> m</b></div>
      <div class="tele-item">비행 시각 <b>t = <span id="tFlight">0.00</span> s</b></div>
    </div>

    <!-- 중앙 빅 배너 -->
    <div class="center-banner" id="centerBanner">
      <div class="b-title" id="bannerTitle">🎯 DIRECT HIT!</div>
      <div class="b-sub" id="bannerSub">정확한 포물선 탄도 계산으로 표적을 강타했습니다!</div>
    </div>
  </div>

  <!-- 하단 정통 포트리스 대시보드 -->
  <div class="fortress-deck">
    <!-- 1. 좌측: 각도기 레이더 다이얼 -->
    <div class="dial-panel">
      <div class="dial-canvas-wrap">
        <canvas id="dialCanvas" width="84" height="84"></canvas>
      </div>
      <div class="dial-info">
        <div style="color:#94a3b8;font-weight:700;">발사각 (ANGLE)</div>
        <div class="dial-angle-big"><span id="angleBig">45</span>°</div>
        <div style="font-size:11px;color:#94a3b8;">차체 경사: <span id="slopeTxt">0°</span></div>
        <div class="mini-btns">
          <button class="mini-btn" onclick="stepAngle(-1)">▼ -1°</button>
          <button class="mini-btn" onclick="stepAngle(1)">▲ +1°</button>
          <button class="mini-btn" onclick="setComplementaryAngle()" title="보각(90°-θ)으로 즉시 전환">90°−θ</button>
        </div>
      </div>
    </div>

    <!-- 2. 중앙: 무기 선택 & 포트리스 파워 게이지 & 체력/연료 바 -->
    <div class="gauge-panel">
      <div class="weapon-bar">
        <div class="wpn-slots">
          <button class="wpn-btn active" id="wpn1" onclick="selectWeapon(1)">① 일반 포탄 (Standard)</button>
          <button class="wpn-btn" id="wpn2" onclick="selectWeapon(2)">② 중량 고폭탄 (Crater+)</button>
          <button class="wpn-btn" id="wpn3" onclick="selectWeapon(3)">③ 3연발 확산탄 (Triple)</button>
          <button class="wpn-btn" id="wpn4" onclick="selectWeapon(4)">④ 물리 보각탄 (θ & 90°−θ 동시발사)</button>
        </div>
        <div style="font-size:11.5px;color:#facc15;font-weight:800;" id="hintPowerTxt">
          💡 탄도 계산 추천 속력: v₀ ≈ 42.0 m/s (▼ 노란 마커)
        </div>
      </div>

      <!-- 파워 게이지 바 -->
      <div class="bar-row">
        <div class="bar-label">POWER (v₀)</div>
        <div class="power-track" id="powerTrack" onclick="clickPowerBar(event)">
          <div class="power-fill" id="powerFill"></div>
          <div class="power-grid-lines"></div>
          <div class="prev-marker" id="prevMarker" title="직전 발사 속력"></div>
          <div class="hint-marker" id="hintMarker" title="현재 각도에서 명중을 위한 이론 추천 속력"></div>
        </div>
        <div class="bar-val"><span id="speedBig">42.0</span> m/s</div>
      </div>

      <!-- HP & MOVE 연료 바 -->
      <div class="sub-bars">
        <div class="bar-row" style="margin-bottom:0;">
          <div class="bar-label" style="width:42px;">HP</div>
          <div class="small-track"><div class="hp-fill" id="hpBarFill"></div></div>
          <span style="font-size:11.5px;font-weight:800;width:38px;text-align:right;" id="hpBarNum">100</span>
        </div>
        <div class="bar-row" style="margin-bottom:0;">
          <div class="bar-label" style="width:48px;">MOVE</div>
          <div class="small-track"><div class="fuel-fill" id="fuelBarFill"></div></div>
          <div style="display:flex;gap:3px;">
            <button class="mini-btn" onclick="moveTank(-1)">◀</button>
            <button class="mini-btn" onclick="moveTank(1)">▶</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. 우측: 정밀 슬라이더 & 발사 버튼 -->
    <div class="action-panel">
      <div class="sl-line">
        <span>각도 θ</span>
        <input type="range" id="angleSlider" min="5" max="85" step="1" value="45" oninput="syncFromSliders()">
      </div>
      <div class="sl-line">
        <span>속력 v₀</span>
        <input type="range" id="speedSlider" min="10" max="80" step="0.5" value="42.0" oninput="syncFromSliders()">
      </div>
      <div class="fire-btn-row">
        <button class="fire-big" id="fireBtn" onclick="fireCurrent()">
          🔥 FIRE! (포탄 발사 / Space)
        </button>
      </div>
      <div style="font-size:11px;color:#94a3b8;text-align:center;">
        키보드: <b>←/→</b> 이동 · <b>↑/↓</b> 각도 · <b>Space</b> 길게 눌러 게이지 충전 발사!
      </div>
    </div>
  </div>

  <!-- 하단 물리 시각화 옵션 바 -->
  <div class="opt-bar">
    <div class="opt-checks">
      <label><input type="checkbox" id="chkVec" checked onchange="drawScene()"> 🏹 실시간 속도 성분 벡터 (vx, vy, v) 표시</label>
      <label><input type="checkbox" id="chkTrail" checked onchange="drawScene()"> 📈 이전 포탄 탄도 궤적 및 최고점(H) 남기기</label>
      <label><input type="checkbox" id="chkAim" checked onchange="drawScene()"> 🔭 초기 조준 가이드선 표시</label>
      <label><input type="checkbox" id="chkHint" checked onchange="syncFromSliders()"> 💡 탄도 계산기 추천 마커(▼) 표시</label>
    </div>
    <div>
      <button class="mini-btn" onclick="clearTrails()">🧹 궤적 지우기</button>
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const dialCanvas = document.getElementById('dialCanvas');
const dctx = dialCanvas.getContext('2d');

// 월드 물리 스케일: 가로 240 m, 세로 112 m
const WORLD_W = 240.0;
const WORLD_H = 112.0;
const SX = canvas.width / WORLD_W;
const SY = canvas.height / WORLD_H;

function wx(x) { return x * SX; }
function wy(y) { return canvas.height - (y + 8.0) * SY; }

// 게임 상태 변수
let stage = 1;
let g = 9.8;
let windAx = 0.0;
let weapon = 1; // 1: 일반, 2: 고폭, 3: 3연발, 4: 보각 동시발사
let tankType = 'cannon';
let soundOn = true;
let audioCtx = null;

let terrain = new Float32Array(canvas.width);
let clouds = [];
let stars = [];
let windParticles = [];

let p1 = { x: 28.0, y: 12.0, angle: 45, speed: 42.0, hp: 100, fuel: 100, slopeDeg: 0, recoil: 0 };
let p2 = { x: 196.0, y: 12.0, angle: 135, speed: 42.0, hp: 100, slopeDeg: 0, recoil: 0 };

let projectiles = [];
let pastTrails = [];
let particles = [];
let shockwaves = [];
let floatingTexts = [];
let animId = null;

let turn = 'P1';
let hits = 0;
let shots = 0;
let lastSpeed = null;
let shakeTime = 0;
let shakeMag = 0;

// 스페이스바 홀드 충전 상태
let spaceCharging = false;
let chargeSpeed = 10.0;
let chargeDir = 1;
let chargeAnimId = null;

// ── Web Audio API 사운드 합성 ──────────────────────────────
function ensureAudio() {
  if (!soundOn) return null;
  if (!audioCtx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) audioCtx = new AC();
  }
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
  return audioCtx;
}

function playSound(type) {
  const ac = ensureAudio();
  if (!ac) return;
  const now = ac.currentTime;

  if (type === 'click') {
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(520, now);
    osc.frequency.exponentialRampToValueAtTime(880, now + 0.04);
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
    osc.connect(gain); gain.connect(ac.destination);
    osc.start(now); osc.stop(now + 0.045);
  } else if (type === 'fire') {
    // 대포 발사 저음 펀치 + 노이즈
    const osc = ac.createOscillator();
    const gain = ac.createGain();
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(160, now);
    osc.frequency.exponentialRampToValueAtTime(32, now + 0.28);
    gain.gain.setValueAtTime(0.28, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
    osc.connect(gain); gain.connect(ac.destination);
    osc.start(now); osc.stop(now + 0.31);
  } else if (type === 'boom') {
    // 폭발 화이트 노이즈 + 저음
    const bufSize = ac.sampleRate * 0.45;
    const buf = ac.createBuffer(1, bufSize, ac.sampleRate);
    const data = buf.getChannelData(0);
    for (let i = 0; i < bufSize; i++) data[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ac.sampleRate * 0.14));
    const noise = ac.createBufferSource();
    noise.buffer = buf;
    const filter = ac.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(420, now);
    const gain = ac.createGain();
    gain.gain.setValueAtTime(0.35, now);
    gain.gain.exponentialRampToValueAtTime(0.01, now + 0.44);
    noise.connect(filter); filter.connect(gain); gain.connect(ac.destination);
    noise.start(now);
  } else if (type === 'hit') {
    // 명중 팡파르
    [523.25, 659.25, 783.99, 1046.5].forEach((freq, i) => {
      const osc = ac.createOscillator();
      const gain = ac.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, now + i * 0.07);
      gain.gain.setValueAtTime(0.14, now + i * 0.07);
      gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.18);
      osc.connect(gain); gain.connect(ac.destination);
      osc.start(now + i * 0.07); osc.stop(now + i * 0.07 + 0.19);
    });
  }
}

function toggleSound() {
  soundOn = !soundOn;
  document.getElementById('soundBtn').textContent = soundOn ? "🔊 효과음 ON" : "🔇 효과음 OFF";
}

// ── 배경 구름/별/바람 입자 초기화 ──────────────────────────
function initAtmosphere() {
  stars = [];
  for (let i = 0; i < 65; i++) {
    stars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * (canvas.height * 0.62),
      r: 0.7 + Math.random() * 1.5,
      twinkle: Math.random() * Math.PI * 2
    });
  }
  clouds = [];
  for (let i = 0; i < 6; i++) {
    clouds.push({
      x: Math.random() * canvas.width,
      y: 45 + Math.random() * 115,
      w: 70 + Math.random() * 65,
      h: 22 + Math.random() * 14,
      spd: 0.2 + Math.random() * 0.3
    });
  }
  windParticles = [];
  for (let i = 0; i < 32; i++) {
    windParticles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * (canvas.height - 80),
      len: 8 + Math.random() * 16,
      alpha: 0.15 + Math.random() * 0.35
    });
  }
}

// ── 스테이지별 지형 생성 ──────────────────────────────────
function buildTerrain() {
  const w = canvas.width;
  const baseH = 12.0;
  for (let px = 0; px < w; px++) {
    const x = px / SX;
    let h = baseH;
    if (stage === 1) {
      // 평지 + 미세한 언덕
      h = baseH + 1.1 * Math.sin(x * 0.045) + 0.5 * Math.cos(x * 0.11);
    } else if (stage === 2) {
      // 중앙 거대 산맥 (고각 사격 필수)
      const peak = 46.0 * Math.exp(-Math.pow((x - 118.0) / 24.0, 2));
      const subPeak = 18.0 * Math.exp(-Math.pow((x - 86.0) / 16.0, 2));
      h = baseH + peak + subPeak + 1.5 * Math.sin(x * 0.09);
    } else if (stage === 3) {
      // 천공의 요새 (우측 절벽 고지대)
      const cliff = 36.0 / (1.0 + Math.exp(-(x - 135.0) / 4.2));
      const step2 = 10.0 * Math.exp(-Math.pow((x - 95.0) / 14.0, 2));
      h = baseH + cliff + step2 + 1.0 * Math.sin(x * 0.07);
    } else if (stage === 4) {
      // 폭풍의 협곡 (중앙 협곡 + 양측 능선)
      const valley = -7.0 * Math.exp(-Math.pow((x - 115.0) / 22.0, 2));
      const ridge = 22.0 * Math.exp(-Math.pow((x - 115.0) / 42.0, 2));
      h = baseH + ridge + valley + 1.8 * Math.sin(x * 0.06);
    } else {
      // AI 데스매치 (복합 전략 지형)
      const c1 = 105.0 + (Math.random() - 0.5) * 26.0;
      const h1 = 22.0 + Math.random() * 20.0;
      h = baseH + h1 * Math.exp(-Math.pow((x - c1) / 25.0, 2)) + 2.8 * Math.sin(x * 0.065);
    }
    terrain[px] = Math.max(2.5, h);
  }
}

function getGroundY(x) {
  const px = Math.max(0, Math.min(canvas.width - 1, Math.round(x * SX)));
  return terrain[px];
}

function getSlopeDeg(x) {
  const px = Math.max(4, Math.min(canvas.width - 5, Math.round(x * SX)));
  const dy = terrain[px + 4] - terrain[px - 4];
  const dx = 8.0 / SX;
  return Math.atan2(dy, dx) * 180.0 / Math.PI;
}

function placeTanks() {
  p1.x = 24.0 + Math.random() * 18.0;
  p2.x = 178.0 + Math.random() * 36.0;
  p1.y = getGroundY(p1.x);
  p2.y = getGroundY(p2.x);
  p1.slopeDeg = getSlopeDeg(p1.x);
  p2.slopeDeg = getSlopeDeg(p2.x);
  p1.hp = 100;
  p2.hp = 100;
  p1.fuel = 100;
  turn = 'P1';

  if (stage <= 3) {
    windAx = 0.0;
  } else {
    windAx = Math.round(((Math.random() * 7.0) - 3.5) * 10) / 10;
    if (Math.abs(windAx) < 0.8) windAx = 2.2;
  }
  updateHUD();
}

function setStage(s) {
  stage = s;
  playSound('click');
  document.querySelectorAll('.stage-tabs .st-btn').forEach((b, idx) => {
    b.classList.toggle('active', idx === s - 1);
  });
  const msgMap = {
    1: "STAGE 1 (평지 훈련): 무풍 환경입니다. R = (v₀² sin2θ)/g 공식과 ④번 물리 보각탄(θ & 90°−θ)을 실험해 보세요!",
    2: "STAGE 2 (험준한 산맥): 거대한 산을 넘기 위해 발사각 θ를 60° 이상으로 높여 최고점 높이 H를 확보하세요!",
    3: "STAGE 3 (천공의 요새): 표적이 높은 절벽 위(Δy > 0)에 있습니다. 고도차를 고려해 탄도를 설계하세요!",
    4: "STAGE 4 (폭풍의 협곡): 강한 수평 바람 가속도(a_wind)가 작용합니다! 풍향과 풍속을 보고 속력을 가감하세요!",
    5: "STAGE 5 (AI 슈퍼탱크전): 매 턴 바람이 바뀌며 AI 탱크가 반격합니다! 먼저 적 탱크의 HP를 0으로 만드세요!"
  };
  document.getElementById('stageMissionTxt').textContent = msgMap[s];
  document.getElementById('enemyTitle').textContent = s === 5 ? "🟥 AI SUPER TANK" : "🟥 TARGET FORTRESS";
  resetStage();
}

function changeTankType() {
  tankType = document.getElementById('tankSelect').value;
  playSound('click');
  drawScene();
}

function changeGravity() {
  g = parseFloat(document.getElementById('gravSelect').value);
  playSound('click');
  syncFromSliders();
}

function selectWeapon(w) {
  weapon = w;
  playSound('click');
  for (let i = 1; i <= 4; i++) {
    document.getElementById('wpn' + i).classList.toggle('active', i === w);
  }
  drawScene();
}

function resetStage() {
  projectiles = [];
  pastTrails = [];
  particles = [];
  shockwaves = [];
  floatingTexts = [];
  buildTerrain();
  placeTanks();
  syncFromSliders();
}

function clearTrails() {
  pastTrails = [];
  drawScene();
}

function stepAngle(delta) {
  if (projectiles.length > 0 || turn !== 'P1') return;
  const sl = document.getElementById('angleSlider');
  sl.value = Math.max(5, Math.min(85, parseInt(sl.value, 10) + delta));
  playSound('click');
  syncFromSliders();
}

function setComplementaryAngle() {
  if (projectiles.length > 0 || turn !== 'P1') return;
  const sl = document.getElementById('angleSlider');
  const comp = Math.max(5, Math.min(85, 90 - parseInt(sl.value, 10)));
  sl.value = comp;
  playSound('click');
  syncFromSliders();
}

function moveTank(dir) {
  if (projectiles.length > 0 || turn !== 'P1' || p1.fuel <= 0) return;
  p1.x = Math.max(10.0, Math.min(92.0, p1.x + dir * 2.0));
  p1.y = getGroundY(p1.x);
  p1.slopeDeg = getSlopeDeg(p1.x);
  p1.fuel = Math.max(0, p1.fuel - 8);
  playSound('click');
  syncFromSliders();
}

function clickPowerBar(e) {
  if (projectiles.length > 0 || turn !== 'P1') return;
  const rect = document.getElementById('powerTrack').getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  const v0 = 10.0 + ratio * 70.0;
  document.getElementById('speedSlider').value = (Math.round(v0 * 2) / 2).toFixed(1);
  playSound('click');
  syncFromSliders();
}

// ── 탄도 물리 계산기: 현재 θ에서 표적(dx, dy) 명중에 필요한 v₀ 계산 ──
function computeIdealV0(dx, dy, thetaDeg) {
  const rad = thetaDeg * Math.PI / 180.0;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);
  // 바람까지 포함한 반복 근사 해법:
  // x(t) = v0*cos*t + 0.5*windAx*t^2 = dx, y(t) = v0*sin*t - 0.5*g*t^2 = dy
  // -> v0*t = (dy + 0.5*g*t^2)/sin -> ((dy + 0.5*g*t^2)/tan) + 0.5*windAx*t^2 = dx
  const tan = Math.tan(rad);
  const coeffT2 = (0.5 * g / tan) + 0.5 * windAx;
  const rhs = dx - (dy / tan);
  if (coeffT2 <= 0.0001 || rhs <= 0) return null;
  const t = Math.sqrt(rhs / coeffT2);
  if (!isFinite(t) || t <= 0.05) return null;
  const v0 = (dy + 0.5 * g * t * t) / (sin * t);
  if (!isFinite(v0) || v0 < 10 || v0 > 80) return null;
  return v0;
}

function syncFromSliders() {
  p1.angle = parseFloat(document.getElementById('angleSlider').value);
  p1.speed = parseFloat(document.getElementById('speedSlider').value);

  document.getElementById('angleBig').textContent = p1.angle.toFixed(0);
  document.getElementById('speedBig').textContent = p1.speed.toFixed(1);
  document.getElementById('slopeTxt').textContent = (p1.slopeDeg >= 0 ? "+" : "") + p1.slopeDeg.toFixed(0) + "°";

  const pct = ((p1.speed - 10.0) / 70.0) * 100.0;
  document.getElementById('powerFill').style.width = `${Math.max(0, Math.min(100, pct))}%`;

  const rad = p1.angle * Math.PI / 180.0;
  const v0x = p1.speed * Math.cos(rad);
  const v0y = p1.speed * Math.sin(rad);
  const theoH = (v0y * v0y) / (2.0 * g);
  const theoR = (p1.speed * p1.speed * Math.sin(2.0 * rad)) / g;

  document.getElementById('tV0x').textContent = v0x.toFixed(1);
  document.getElementById('tV0y').textContent = v0y.toFixed(1);
  document.getElementById('tTheoH').textContent = theoH.toFixed(1);
  document.getElementById('tTheoR').textContent = theoR.toFixed(1);

  // 탄도 계산기 추천 마커 업데이트
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  const idealV0 = computeIdealV0(dx, dy, p1.angle);
  const hm = document.getElementById('hintMarker');
  const hTxt = document.getElementById('hintPowerTxt');
  const showHint = document.getElementById('chkHint').checked;

  if (showHint && idealV0 !== null) {
    const hPct = ((idealV0 - 10.0) / 70.0) * 100.0;
    hm.style.display = 'block';
    hm.style.left = `${Math.max(0, Math.min(100, hPct))}%`;
    hTxt.textContent = `💡 탄도 계산기 추천 속력 (θ=${p1.angle}° 기준): v₀ ≈ ${idealV0.toFixed(1)} m/s (▼ 노란 마커)`;
  } else if (showHint) {
    hm.style.display = 'none';
    hTxt.textContent = `⚠️ 현재 각도(θ=${p1.angle}°)로는 표적에 닿기 어렵습니다. 각도를 높여 보세요!`;
  } else {
    hm.style.display = 'none';
    hTxt.textContent = `💡 탄도 힌트 숨김 중 (직접 공식으로 v₀를 계산해 보세요!)`;
  }

  updateHUD();
  drawDial();
  drawScene();
}

function updateHUD() {
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  document.getElementById('hudDx').textContent = dx.toFixed(1);
  document.getElementById('hudDy').textContent = (dy >= 0 ? "+" : "") + dy.toFixed(1);
  document.getElementById('p1HpTxt').textContent = `HP ${Math.max(0, Math.round(p1.hp))}%`;
  document.getElementById('p2HpTxt').textContent = `HP ${Math.max(0, Math.round(p2.hp))}%`;
  document.getElementById('hpBarFill').style.width = `${Math.max(0, p1.hp)}%`;
  document.getElementById('hpBarNum').textContent = Math.max(0, Math.round(p1.hp));
  document.getElementById('fuelBarFill').style.width = `${Math.max(0, p1.fuel)}%`;
  document.getElementById('scoreHits').textContent = hits;
  document.getElementById('scoreShots').textContent = shots;

  const wBox = document.getElementById('windBox');
  const wTxt = document.getElementById('windText');
  if (Math.abs(windAx) < 0.05) {
    wTxt.textContent = "WIND: 0.0 m/s² (무풍)";
    wBox.style.borderColor = "#64748b";
    wBox.style.color = "#cbd5e1";
  } else if (windAx > 0) {
    wTxt.textContent = `WIND: ▶ 우측 순풍 +${windAx.toFixed(1)} m/s²`;
    wBox.style.borderColor = "#38bdf8";
    wBox.style.color = "#38bdf8";
  } else {
    wTxt.textContent = `WIND: ◀ 좌측 역풍 ${windAx.toFixed(1)} m/s²`;
    wBox.style.borderColor = "#f472b6";
    wBox.style.color = "#f472b6";
  }
}

function showCenterBanner(title, sub, borderColor = "#facc15") {
  const cb = document.getElementById('centerBanner');
  const bt = document.getElementById('bannerTitle');
  const bs = document.getElementById('bannerSub');
  bt.textContent = title;
  bt.style.color = borderColor;
  bs.textContent = sub;
  cb.style.borderColor = borderColor;
  cb.classList.add('show');
  setTimeout(() => { cb.classList.remove('show'); }, 2000);
}

// ── 좌측 포트리스 각도기 다이얼 렌더링 ──────────────────────
function drawDial() {
  const w = dialCanvas.width, h = dialCanvas.height;
  const cx = w / 2, cy = h / 2 + 12;
  const r = 34;
  dctx.clearRect(0, 0, w, h);

  // 배경 반원 레이더
  dctx.save();
  dctx.fillStyle = "#0f172a";
  dctx.strokeStyle = "#334155";
  dctx.lineWidth = 1.5;
  dctx.beginPath();
  dctx.arc(cx, cy, r, Math.PI, 0);
  dctx.closePath();
  dctx.fill();
  dctx.stroke();

  // 15도 간격 눈금
  dctx.strokeStyle = "rgba(148, 163, 184, 0.25)";
  for (let deg = 0; deg <= 90; deg += 15) {
    const rad = deg * Math.PI / 180.0;
    dctx.beginPath();
    dctx.moveTo(cx, cy);
    dctx.lineTo(cx + Math.cos(rad) * r, cy - Math.sin(rad) * r);
    dctx.stroke();
  }

  // 발사각 부채꼴 채우기
  const curRad = p1.angle * Math.PI / 180.0;
  dctx.fillStyle = "rgba(56, 189, 248, 0.28)";
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.arc(cx, cy, r - 2, -curRad, 0);
  dctx.closePath();
  dctx.fill();

  // 보각(90 - theta) 점선 표시
  const compRad = (90 - p1.angle) * Math.PI / 180.0;
  dctx.strokeStyle = "rgba(250, 204, 21, 0.55)";
  dctx.setLineDash([2, 2]);
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.lineTo(cx + Math.cos(compRad) * r, cy - Math.sin(compRad) * r);
  dctx.stroke();
  dctx.setLineDash([]);

  // 현재 발사각 바늘
  dctx.strokeStyle = "#38bdf8";
  dctx.lineWidth = 2.5;
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.lineTo(cx + Math.cos(curRad) * r, cy - Math.sin(curRad) * r);
  dctx.stroke();

  dctx.fillStyle = "#f8fafc";
  dctx.beginPath();
  dctx.arc(cx, cy, 3.5, 0, Math.PI * 2);
  dctx.fill();
  dctx.restore();
}

// ── 지형 파괴 및 폭발 이펙트 ──────────────────────────────
function craterTerrain(hitX, radiusM) {
  const centerPx = Math.round(hitX * SX);
  const radPx = Math.round(radiusM * SX);
  for (let px = Math.max(0, centerPx - radPx); px <= Math.min(canvas.width - 1, centerPx + radPx); px++) {
    const dist = Math.abs(px - centerPx) / radPx;
    const depth = (1.0 - dist * dist) * (radiusM * 0.72);
    terrain[px] = Math.max(2.0, terrain[px] - depth);
  }
  p1.y = getGroundY(p1.x);
  p2.y = getGroundY(p2.x);
  p1.slopeDeg = getSlopeDeg(p1.x);
  p2.slopeDeg = getSlopeDeg(p2.x);
}

function triggerExplosion(x, y, radiusM, mainColor) {
  playSound('boom');
  shakeTime = 0.32;
  shakeMag = radiusM * 1.4;

  shockwaves.push({ x, y, r: 0.5, maxR: radiusM * 2.1, alpha: 1.0, color: mainColor });

  for (let i = 0; i < 38; i++) {
    const ang = Math.random() * Math.PI * 2;
    const spd = 5 + Math.random() * 24;
    particles.push({
      x, y,
      vx: Math.cos(ang) * spd,
      vy: Math.sin(ang) * spd + 4,
      size: 2.5 + Math.random() * 4.5,
      life: 1.0,
      color: i % 3 === 0 ? "#fde047" : (i % 3 === 1 ? mainColor : "#f97316")
    });
  }
}

function addFloatingText(x, y, text, color) {
  floatingTexts.push({ x, y: y + 4, text, color, life: 1.3 });
}

// ── 포탄 발사 로직 ────────────────────────────────────────
function createShell(owner, angleDeg, speed, color, tag) {
  const shooter = owner === 'P1' ? p1 : p2;
  const rad = angleDeg * Math.PI / 180.0;
  const startX = shooter.x + Math.cos(rad) * 2.6;
  const startY = shooter.y + 1.8 + Math.sin(rad) * 2.6;
  const vx0 = speed * Math.cos(rad);
  const vy0 = speed * Math.sin(rad);

  return {
    owner,
    tag,
    color,
    angleDeg,
    speed,
    x0: startX, y0: startY,
    x: startX, y: startY,
    vx0, vy0,
    vx: vx0, vy: vy0,
    t: 0.0,
    maxY: startY,
    maxXAtPeak: startX,
    peakStamped: false,
    trail: [{ x: startX, y: startY }]
  };
}

function fireCurrent(owner = 'P1') {
  if (projectiles.length > 0) return;
  document.getElementById('fireBtn').disabled = true;
  playSound('fire');

  if (owner === 'P1') {
    shots++;
    p1.recoil = 7.0;
    lastSpeed = p1.speed;
    const pm = document.getElementById('prevMarker');
    pm.style.display = 'block';
    pm.style.left = `${Math.max(0, Math.min(100, ((p1.speed - 10.0) / 70.0) * 100.0))}%`;
    document.getElementById('prevShotTxt').textContent = `θ=${p1.angle}°, v₀=${p1.speed.toFixed(1)} m/s`;

    // 포구 화염 파티클
    const rad = p1.angle * Math.PI / 180.0;
    const mx = p1.x + Math.cos(rad) * 2.8;
    const my = p1.y + 1.8 + Math.sin(rad) * 2.8;
    for (let i = 0; i < 14; i++) {
      const a = rad + (Math.random() - 0.5) * 0.5;
      const s = 6 + Math.random() * 12;
      particles.push({
        x: mx, y: my, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
        size: 3, life: 0.45, color: "#fde047"
      });
    }

    if (weapon === 1) {
      projectiles.push(createShell('P1', p1.angle, p1.speed, "#38bdf8", `θ=${p1.angle}°`));
    } else if (weapon === 2) {
      projectiles.push(createShell('P1', p1.angle, p1.speed, "#f97316", `고폭탄 θ=${p1.angle}°`));
    } else if (weapon === 3) {
      // 3연발 확산탄 (속력 약간씩 차이)
      projectiles.push(createShell('P1', p1.angle, p1.speed - 1.8, "#60a5fa", `확산-1`));
      projectiles.push(createShell('P1', p1.angle, p1.speed, "#38bdf8", `확산-2`));
      projectiles.push(createShell('P1', p1.angle, p1.speed + 1.8, "#93c5fd", `확산-3`));
    } else if (weapon === 4) {
      // 물리 보각탄: 현재 각도 θ와 보각 (90° - θ) 동시 발사!
      const compAng = Math.max(5, Math.min(85, 90 - p1.angle));
      projectiles.push(createShell('P1', p1.angle, p1.speed, "#38bdf8", `주탄 θ=${p1.angle}°`));
      if (compAng !== p1.angle) {
        projectiles.push(createShell('P1', compAng, p1.speed, "#facc15", `보각탄 90°−θ=${compAng}°`));
      }
    }
  } else {
    p2.recoil = 7.0;
    projectiles.push(createShell('AI', p2.angle, p2.speed, "#f87171", `AI 포탄`));
  }
}

function aiTurnFire() {
  document.getElementById('turnBanner').textContent = "🤖 AI SUPER TANK 조준 중...";
  const dx = p1.x - p2.x; // 음수
  const dy = p1.y - p2.y;
  const aiElev = 50 + Math.round((Math.random() - 0.5) * 14);
  p2.angle = 180 - aiElev;
  // AI용 역방향 바람 보정 포함 이상 속력 계산
  const rad = aiElev * Math.PI / 180.0;
  const absDx = Math.abs(dx);
  const tan = Math.tan(rad);
  const coeffT2 = (0.5 * g / tan) - 0.5 * windAx;
  const rhs = absDx - (dy / tan);
  let aiV0 = 42.0;
  if (coeffT2 > 0.01 && rhs > 0) {
    const t = Math.sqrt(rhs / coeffT2);
    aiV0 = (dy + 0.5 * g * t * t) / (Math.sin(rad) * t);
  }
  p2.speed = Math.max(15, Math.min(76, aiV0 + (Math.random() - 0.5) * 3.8));
  setTimeout(() => { fireCurrent('AI'); }, 750);
}

// ── 메인 애니메이션 루프 (60 FPS) ──────────────────────────
let lastFrameTime = performance.now();

function gameLoop(now) {
  const dtReal = Math.min(0.04, (now - lastFrameTime) / 1000.0);
  lastFrameTime = now;
  const dtSim = dtReal * 2.15;

  // 구름 및 바람 먼지 이동
  const windFactor = windAx === 0 ? 0.35 : windAx * 1.1;
  clouds.forEach((c) => {
    c.x += (c.spd + windFactor * 0.45) * dtReal * 25;
    if (c.x > canvas.width + 90) c.x = -90;
    if (c.x < -90) c.x = canvas.width + 90;
  });
  windParticles.forEach((wp) => {
    wp.x += (windAx * 38 + 12) * dtReal;
    if (wp.x > canvas.width) wp.x = 0;
    if (wp.x < 0) wp.x = canvas.width;
  });

  // 포신 반동 복원
  if (p1.recoil > 0) p1.recoil = Math.max(0, p1.recoil - dtReal * 28);
  if (p2.recoil > 0) p2.recoil = Math.max(0, p2.recoil - dtReal * 28);
  if (shakeTime > 0) shakeTime = Math.max(0, shakeTime - dtReal);

  // 포탄 물리 업데이트
  let anyFinishedOwner = null;
  for (let i = projectiles.length - 1; i >= 0; i--) {
    const pr = projectiles[i];
    const prevVy = pr.vy;
    pr.t += dtSim;
    pr.x = pr.x0 + pr.vx0 * pr.t + 0.5 * windAx * pr.t * pr.t;
    pr.y = pr.y0 + pr.vy0 * pr.t - 0.5 * g * pr.t * pr.t;
    pr.vx = pr.vx0 + windAx * pr.t;
    pr.vy = pr.vy0 - g * pr.t;

    if (pr.y > pr.maxY) {
      pr.maxY = pr.y;
      pr.maxXAtPeak = pr.x;
    }
    // 최고점 통과 순간 스탬프 (vy 부호가 +에서 -로 바뀔 때)
    if (!pr.peakStamped && prevVy > 0 && pr.vy <= 0) {
      pr.peakStamped = true;
      const netH = pr.maxY - pr.y0;
      addFloatingText(pr.x, pr.y + 2, `★ 최고점 H=${netH.toFixed(1)}m (vy=0)`, pr.color);
    }

    pr.trail.push({ x: pr.x, y: pr.y });
    document.getElementById('tFlight').textContent = pr.t.toFixed(2);

    // 연기 파티클 생성
    if (Math.random() < 0.55) {
      particles.push({
        x: pr.x, y: pr.y,
        vx: (Math.random() - 0.5) * 2, vy: (Math.random() - 0.5) * 2,
        size: 2.2, life: 0.45, color: pr.color
      });
    }

    // 충돌 검사
    const target = pr.owner === 'P1' ? p2 : p1;
    const distTarget = Math.hypot(pr.x - target.x, pr.y - (target.y + 1.5));
    const groundY = getGroundY(pr.x);

    if (distTarget <= 4.3 || pr.y <= groundY || pr.x < 0 || pr.x > WORLD_W) {
      const hitX = pr.x;
      const hitY = Math.max(pr.y, groundY);
      const craterR = (pr.owner === 'P1' && weapon === 2) ? 6.8 : 4.2;

      if (document.getElementById('chkTrail').checked) {
        pastTrails.push({
          color: pr.color,
          points: pr.trail,
          peakX: pr.maxXAtPeak,
          peakY: pr.maxY,
          netH: pr.maxY - pr.y0,
          label: `${pr.tag} (R=${Math.abs(hitX - pr.x0).toFixed(1)}m)`
        });
        if (pastTrails.length > 6) pastTrails.shift();
      }

      const dP2 = Math.hypot(hitX - p2.x, hitY - p2.y);
      const dP1 = Math.hypot(hitX - p1.x, hitY - p1.y);

      if (pr.owner === 'P1' && dP2 < 8.0) {
        const baseDmg = weapon === 2 ? 60 : (weapon === 3 ? 28 : 45);
        const dmg = dP2 < 4.0 ? baseDmg : Math.max(12, Math.round(baseDmg * (1 - dP2 / 8.5)));
        p2.hp = Math.max(0, p2.hp - dmg);
        hits++;
        playSound('hit');
        triggerExplosion(hitX, hitY, craterR, "#ef4444");
        craterTerrain(hitX, craterR);
        addFloatingText(p2.x, p2.y + 5, dP2 < 4.0 ? `CRITICAL -${dmg}!` : `HIT -${dmg}`, "#fde047");
        showCenterBanner(
          dP2 < 4.0 ? "🎯 CRITICAL DIRECT HIT!" : "💥 TARGET HIT!",
          `비행 시간 ${pr.t.toFixed(2)}s · 수평 이동거리 ${Math.abs(hitX - pr.x0).toFixed(1)}m · 최고 높이 ${(pr.maxY - pr.y0).toFixed(1)}m`,
          "#4ade80"
        );
      } else if (pr.owner === 'AI' && dP1 < 8.0) {
        const dmg = dP1 < 4.0 ? 38 : Math.max(10, Math.round(28 * (1 - dP1 / 8.5)));
        p1.hp = Math.max(0, p1.hp - dmg);
        triggerExplosion(hitX, hitY, 4.2, "#f97316");
        craterTerrain(hitX, 4.2);
        addFloatingText(p1.x, p1.y + 5, `피격 -${dmg} HP!`, "#f87171");
        showCenterBanner("⚠️ AI 포탄 피격!", `내 탱크가 ${dmg}의 데미지를 입었습니다!`, "#f87171");
      } else {
        triggerExplosion(hitX, hitY, craterR, "#38bdf8");
        craterTerrain(hitX, craterR);
        if (pr.owner === 'P1' && projectiles.length === 1) {
          const errX = hitX - p2.x;
          const diffStr = errX < 0 ? `표적보다 ${Math.abs(errX).toFixed(1)}m 앞에 탄착` : `표적을 ${errX.toFixed(1)}m 초과`;
          addFloatingText(hitX, hitY + 3, diffStr, "#cbd5e1");
        }
      }

      anyFinishedOwner = pr.owner;
      projectiles.splice(i, 1);
      updateHUD();
    }
  }

  // 모든 포탄이 착탄했을 때 턴 전환 처리
  if (anyFinishedOwner && projectiles.length === 0) {
    if (p2.hp <= 0) {
      showCenterBanner("🏆 STAGE CLEAR! 표적 격파 완료!", "새로운 위치에 다음 표적이 배치됩니다.", "#fde047");
      setTimeout(() => {
        placeTanks();
        syncFromSliders();
        document.getElementById('turnBanner').textContent = "⚡ PLAYER 1 TURN — 조준 후 발사하세요!";
        document.getElementById('fireBtn').disabled = false;
      }, 1500);
    } else if (p1.hp <= 0) {
      showCenterBanner("💀 TANK DESTROYED!", "탱크가 파괴되었습니다. 스테이지를 재시작합니다.", "#f87171");
      setTimeout(() => {
        resetStage();
        document.getElementById('turnBanner').textContent = "⚡ PLAYER 1 TURN — 조준 후 발사하세요!";
        document.getElementById('fireBtn').disabled = false;
      }, 1600);
    } else if (stage === 5 && anyFinishedOwner === 'P1') {
      turn = 'AI';
      setTimeout(aiTurnFire, 800);
    } else {
      turn = 'P1';
      p1.fuel = 100;
      if (stage >= 4) {
        windAx = Math.round(((Math.random() * 7.0) - 3.5) * 10) / 10;
      }
      document.getElementById('turnBanner').textContent = "⚡ PLAYER 1 TURN — 조준 후 발사하세요!";
      syncFromSliders();
      document.getElementById('fireBtn').disabled = false;
    }
  }

  // 충격파 & 파티클 & 플로팅 텍스트 업데이트
  for (let i = shockwaves.length - 1; i >= 0; i--) {
    const sw = shockwaves[i];
    sw.r += (sw.maxR - sw.r) * dtReal * 9;
    sw.alpha -= dtReal * 2.4;
    if (sw.alpha <= 0) shockwaves.splice(i, 1);
  }
  for (let i = particles.length - 1; i >= 0; i--) {
    const pt = particles[i];
    pt.x += pt.vx * dtReal;
    pt.y += pt.vy * dtReal;
    pt.vy -= g * dtReal * 0.7;
    pt.life -= dtReal * 1.9;
    if (pt.life <= 0) particles.splice(i, 1);
  }
  for (let i = floatingTexts.length - 1; i >= 0; i--) {
    const ft = floatingTexts[i];
    ft.y += dtReal * 4.5;
    ft.life -= dtReal * 0.85;
    if (ft.life <= 0) floatingTexts.splice(i, 1);
  }

  drawScene();
  requestAnimationFrame(gameLoop);
}

// ── 화면 렌더링 (아케이드 포트리스 그래픽) ──────────────────
function drawTankSprite(tank, isPlayer) {
  const cx = wx(tank.x);
  const cy = wy(tank.y);

  ctx.save();
  ctx.translate(cx, cy);
  // 지형 경사각 반영 (실제 포트리스처럼 경사면에서 차체가 기울어짐)
  ctx.rotate((-tank.slopeDeg * Math.PI / 180.0) * 0.65);

  // 그림자
  ctx.fillStyle = "rgba(0,0,0,0.45)";
  ctx.beginPath();
  ctx.ellipse(0, 2, 22, 5, 0, 0, Math.PI * 2);
  ctx.fill();

  // 포신 (발사각은 월드 절대각 기준이므로 차체 회전 보정)
  const worldRad = tank.angle * Math.PI / 180.0;
  const localRad = worldRad - (-tank.slopeDeg * Math.PI / 180.0) * 0.65;
  const barrelLen = 26 - tank.recoil;

  ctx.save();
  ctx.translate(0, -11);
  ctx.rotate(-localRad);
  // 포신 몸통
  const bGrad = ctx.createLinearGradient(0, -4, 0, 4);
  bGrad.addColorStop(0, "#f8fafc");
  bGrad.addColorStop(1, "#64748b");
  ctx.fillStyle = bGrad;
  ctx.beginPath();
  ctx.roundRect(0, -3.5, barrelLen, 7, 2);
  ctx.fill();
  // 포구 제퇴기 (Muzzle Brake)
  ctx.fillStyle = isPlayer ? "#38bdf8" : "#f87171";
  ctx.fillRect(barrelLen - 4, -5, 5, 10);
  ctx.restore();

  // 탱크 스킨 색상
  let cTop = "#3b82f6", cBot = "#1d4ed8", cTrim = "#93c5fd";
  if (!isPlayer) {
    cTop = "#ef4444"; cBot = "#991b1b"; cTrim = "#fca5a5";
  } else if (tankType === 'cannon') {
    cTop = "#dc2626"; cBot = "#7f1d1d"; cTrim = "#fde047";
  } else if (tankType === 'laser') {
    cTop = "#eab308"; cBot = "#a16207"; cTrim = "#38bdf8";
  }

  // 포탑 돔
  const tGrad = ctx.createLinearGradient(-12, -22, 12, -8);
  tGrad.addColorStop(0, cTop);
  tGrad.addColorStop(1, cBot);
  ctx.fillStyle = tGrad;
  ctx.strokeStyle = cTrim;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.arc(0, -10, 11, Math.PI, 0);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // 차체 장갑
  ctx.fillStyle = tGrad;
  ctx.beginPath();
  ctx.moveTo(-19, -10);
  ctx.lineTo(19, -10);
  ctx.lineTo(15, -2);
  ctx.lineTo(-15, -2);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // 무한궤도 캐터필러 & 바퀴 5개
  ctx.fillStyle = "#0f172a";
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(-20, -4, 40, 8, 4);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = "#94a3b8";
  for (let wxOff = -14; wxOff <= 14; wxOff += 7) {
    ctx.beginPath();
    ctx.arc(wxOff, 0, 2.3, 0, Math.PI * 2);
    ctx.fill();
  }

  // 머리 위 미니 HP 게이지 & 각도 태그
  ctx.restore();
  ctx.save();
  ctx.translate(cx, cy - 34);
  ctx.fillStyle = "rgba(9, 13, 22, 0.85)";
  ctx.strokeStyle = "rgba(148, 163, 184, 0.4)";
  ctx.lineWidth = 1;
  ctx.fillRect(-22, 0, 44, 6);
  ctx.strokeRect(-22, 0, 44, 6);
  ctx.fillStyle = tank.hp > 40 ? "#22c55e" : "#ef4444";
  ctx.fillRect(-21, 1, 42 * Math.max(0, tank.hp) / 100, 4);

  ctx.fillStyle = isPlayer ? "#93c5fd" : "#fca5a5";
  ctx.font = "bold 11px 'Pretendard', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(isPlayer ? `P1 (${tank.angle.toFixed(0)}°)` : (stage === 5 ? "AI BOSS" : "TARGET"), 0, -4);
  ctx.restore();
}

function drawVecArrow(x1, y1, x2, y2, color, label) {
  const len = Math.hypot(x2 - x1, y2 - y1);
  if (len < 4) return;
  const head = 7.5;
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - head * Math.cos(ang - Math.PI / 6), y2 - head * Math.sin(ang - Math.PI / 6));
  ctx.lineTo(x2 - head * Math.cos(ang + Math.PI / 6), y2 - head * Math.sin(ang + Math.PI / 6));
  ctx.closePath();
  ctx.fill();

  if (label) {
    ctx.font = "bold 11px 'Pretendard', sans-serif";
    ctx.fillStyle = color;
    ctx.fillText(label, x2 + 6, y2 - 4);
  }
  ctx.restore();
}

function drawScene() {
  ctx.save();
  if (shakeTime > 0) {
    ctx.translate((Math.random() - 0.5) * shakeMag, (Math.random() - 0.5) * shakeMag);
  }

  // 1. 행성/스테이지별 밤하늘 그라데이션
  const sky = ctx.createLinearGradient(0, 0, 0, canvas.height);
  if (g === 3.7) {
    sky.addColorStop(0, "#1c0a0a");
    sky.addColorStop(0.6, "#451a1c");
    sky.addColorStop(1, "#7c2d12");
  } else if (g === 1.6) {
    sky.addColorStop(0, "#020617");
    sky.addColorStop(0.7, "#0f172a");
    sky.addColorStop(1, "#1e293b");
  } else {
    sky.addColorStop(0, "#060b19");
    sky.addColorStop(0.55, "#0f1e3a");
    sky.addColorStop(1, "#1e3a5f");
  }
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 2. 별 반짝임
  stars.forEach((s) => {
    s.twinkle += 0.03;
    ctx.fillStyle = `rgba(255, 255, 255, ${0.35 + 0.4 * Math.sin(s.twinkle)})`;
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fill();
  });

  // 3. 원경 산맥 실루엣 (Parallax Layer)
  ctx.fillStyle = "rgba(15, 23, 42, 0.55)";
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);
  for (let x = 0; x <= canvas.width; x += 40) {
    const my = canvas.height - 130 - 45 * Math.sin(x * 0.008) - 25 * Math.cos(x * 0.019);
    ctx.lineTo(x, my);
  }
  ctx.lineTo(canvas.width, canvas.height);
  ctx.closePath();
  ctx.fill();

  // 4. 구름 & 바람 스트림 라인
  clouds.forEach((c) => {
    ctx.fillStyle = "rgba(226, 232, 240, 0.09)";
    ctx.beginPath();
    ctx.ellipse(c.x, c.y, c.w, c.h, 0, 0, Math.PI * 2);
    ctx.fill();
  });

  if (Math.abs(windAx) > 0.05) {
    ctx.strokeStyle = windAx > 0 ? "rgba(56, 189, 248, 0.22)" : "rgba(244, 114, 182, 0.22)";
    ctx.lineWidth = 1.5;
    windParticles.forEach((wp) => {
      ctx.beginPath();
      ctx.moveTo(wp.x, wp.y);
      ctx.lineTo(wp.x + wp.len * (windAx > 0 ? 1 : -1), wp.y);
      ctx.stroke();
    });
  }

  // 5. 물리 거리 격자 (20m 간격)
  ctx.strokeStyle = "rgba(148, 163, 184, 0.09)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "rgba(148, 163, 184, 0.42)";
  ctx.font = "10px 'Pretendard', sans-serif";
  for (let xm = 0; xm <= WORLD_W; xm += 20) {
    const px = wx(xm);
    ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, canvas.height); ctx.stroke();
    ctx.fillText(`${xm}m`, px + 3, canvas.height - 5);
  }
  for (let ym = 0; ym <= 100; ym += 20) {
    const py = wy(ym);
    ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(canvas.width, py); ctx.stroke();
    ctx.fillText(`${ym}m`, 4, py - 3);
  }

  // 6. 다층 지형 (암석 내부 + 상단 잔디/표면 엣지)
  const tGrad = ctx.createLinearGradient(0, wy(55), 0, canvas.height);
  if (g === 3.7) {
    tGrad.addColorStop(0, "#9a3412"); tGrad.addColorStop(1, "#431407");
  } else if (g === 1.6) {
    tGrad.addColorStop(0, "#475569"); tGrad.addColorStop(1, "#0f172a");
  } else {
    tGrad.addColorStop(0, "#1e293b"); tGrad.addColorStop(0.35, "#0f172a"); tGrad.addColorStop(1, "#020617");
  }
  ctx.fillStyle = tGrad;
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);
  for (let px = 0; px < canvas.width; px++) ctx.lineTo(px, wy(terrain[px]));
  ctx.lineTo(canvas.width, canvas.height);
  ctx.closePath();
  ctx.fill();

  // 지형 상단 네온/잔디 라인
  ctx.strokeStyle = g === 3.7 ? "#fb923c" : (g === 1.6 ? "#94a3b8" : "#22c55e");
  ctx.lineWidth = 3;
  ctx.beginPath();
  for (let px = 0; px < canvas.width; px++) {
    if (px === 0) ctx.moveTo(px, wy(terrain[px]));
    else ctx.lineTo(px, wy(terrain[px]));
  }
  ctx.stroke();

  // 7. 이전 탄도 궤적 및 최고점 마커
  if (document.getElementById('chkTrail').checked) {
    pastTrails.forEach((tr) => {
      ctx.save();
      ctx.strokeStyle = tr.color;
      ctx.globalAlpha = 0.42;
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 2;
      ctx.beginPath();
      tr.points.forEach((pt, idx) => {
        if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
        else ctx.lineTo(wx(pt.x), wy(pt.y));
      });
      ctx.stroke();
      ctx.setLineDash([]);

      // 최고점 별표
      ctx.globalAlpha = 0.75;
      ctx.fillStyle = tr.color;
      ctx.beginPath();
      ctx.arc(wx(tr.peakX), wy(tr.peakY), 3.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.font = "bold 10.5px 'Pretendard', sans-serif";
      ctx.fillText(`H=${tr.netH.toFixed(1)}m`, wx(tr.peakX) - 20, wy(tr.peakY) - 7);

      const last = tr.points[tr.points.length - 1];
      if (last) {
        ctx.fillText(tr.label, wx(last.x) - 28, wy(last.y) - 8);
      }
      ctx.restore();
    });
  }

  // 8. 조준 가이드 도트 (초기 1.0초 궤적)
  if (document.getElementById('chkAim').checked && projectiles.length === 0 && turn === 'P1') {
    const rad = p1.angle * Math.PI / 180.0;
    const vx0 = p1.speed * Math.cos(rad);
    const vy0 = p1.speed * Math.sin(rad);
    const sx = p1.x + Math.cos(rad) * 2.6;
    const sy = p1.y + 1.8 + Math.sin(rad) * 2.6;
    ctx.save();
    for (let t = 0.1; t <= 1.1; t += 0.11) {
      const gx = sx + vx0 * t + 0.5 * windAx * t * t;
      const gy = sy + vy0 * t - 0.5 * g * t * t;
      ctx.fillStyle = `rgba(250, 204, 21, ${1.0 - t * 0.7})`;
      ctx.beginPath();
      ctx.arc(wx(gx), wy(gy), 2.6, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  // 9. 탱크 그리기
  drawTankSprite(p1, true);
  drawTankSprite(p2, false);

  // 10. 발사 전 속도 분해 벡터 화살표 표시
  if (projectiles.length === 0 && document.getElementById('chkVec').checked) {
    const rad = p1.angle * Math.PI / 180.0;
    const vx0 = p1.speed * Math.cos(rad);
    const vy0 = p1.speed * Math.sin(rad);
    const ox = wx(p1.x);
    const oy = wy(p1.y + 2.2);
    const vs = 1.25;
    drawVecArrow(ox, oy, ox + vx0 * vs, oy, "#38bdf8", `v₀x=${vx0.toFixed(1)}`);
    drawVecArrow(ox, oy, ox, oy - vy0 * vs, "#f87171", `v₀y=${vy0.toFixed(1)}`);
    drawVecArrow(ox, oy, ox + vx0 * vs, oy - vy0 * vs, "#4ade80", `v₀=${p1.speed.toFixed(1)}`);
  }

  // 11. 비행 중인 포탄 & 실시간 속도 벡터
  projectiles.forEach((pr) => {
    ctx.save();
    ctx.strokeStyle = pr.color;
    ctx.lineWidth = 2.6;
    ctx.beginPath();
    pr.trail.forEach((pt, idx) => {
      if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
      else ctx.lineTo(wx(pt.x), wy(pt.y));
    });
    ctx.stroke();

    const px = wx(pr.x);
    const py = wy(pr.y);
    // 포탄 광원 글로우
    const glow = ctx.createRadialGradient(px, py, 1, px, py, 12);
    glow.addColorStop(0, "#ffffff");
    glow.addColorStop(0.4, pr.color);
    glow.addColorStop(1, "transparent");
    ctx.fillStyle = glow;
    ctx.beginPath();
    ctx.arc(px, py, 12, 0, Math.PI * 2);
    ctx.fill();

    if (document.getElementById('chkVec').checked) {
      const vs = 1.15;
      drawVecArrow(px, py, px + pr.vx * vs, py, "#38bdf8", `vx=${pr.vx.toFixed(1)}`);
      drawVecArrow(px, py, px, py - pr.vy * vs, "#f87171", `vy=${pr.vy.toFixed(1)}`);
    }
    ctx.restore();
  });

  // 12. 충격파 & 폭발 파티클 & 데미지 플로팅 텍스트
  shockwaves.forEach((sw) => {
    ctx.save();
    ctx.strokeStyle = sw.color;
    ctx.globalAlpha = Math.max(0, sw.alpha);
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.arc(wx(sw.x), wy(sw.y), sw.r * SX, 0, Math.PI * 2);
    ctx.stroke();
    ctx.restore();
  });

  particles.forEach((pt) => {
    ctx.save();
    ctx.globalAlpha = Math.max(0, pt.life);
    ctx.fillStyle = pt.color;
    ctx.beginPath();
    ctx.arc(wx(pt.x), wy(pt.y), pt.size, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });

  floatingTexts.forEach((ft) => {
    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, ft.life));
    ctx.font = "900 14px 'Pretendard', sans-serif";
    ctx.fillStyle = ft.color;
    ctx.textAlign = "center";
    ctx.shadowColor = "rgba(0,0,0,0.9)";
    ctx.shadowBlur = 6;
    ctx.fillText(ft.text, wx(ft.x), wy(ft.y));
    ctx.restore();
  });

  ctx.restore();
}

// ── 키보드 조작 (포트리스 정통 Spacebar 게이지 충전 발사 포함!) ──
window.addEventListener('keydown', (e) => {
  if (projectiles.length > 0 || turn !== 'P1') return;
  if (e.key === 'ArrowLeft') {
    moveTank(-1); e.preventDefault();
  } else if (e.key === 'ArrowRight') {
    moveTank(1); e.preventDefault();
  } else if (e.key === 'ArrowUp') {
    stepAngle(1); e.preventDefault();
  } else if (e.key === 'ArrowDown') {
    stepAngle(-1); e.preventDefault();
  } else if (e.key === ' ' && !spaceCharging) {
    spaceCharging = true;
    chargeSpeed = 10.0;
    chargeDir = 1;
    function stepCharge() {
      if (!spaceCharging) return;
      chargeSpeed += chargeDir * 1.1;
      if (chargeSpeed >= 80.0) { chargeSpeed = 80.0; chargeDir = -1; }
      if (chargeSpeed <= 10.0) { chargeSpeed = 10.0; chargeDir = 1; }
      document.getElementById('speedSlider').value = chargeSpeed.toFixed(1);
      syncFromSliders();
      chargeAnimId = requestAnimationFrame(stepCharge);
    }
    chargeAnimId = requestAnimationFrame(stepCharge);
    e.preventDefault();
  }
});

window.addEventListener('keyup', (e) => {
  if (e.key === ' ' && spaceCharging) {
    spaceCharging = false;
    if (chargeAnimId) cancelAnimationFrame(chargeAnimId);
    fireCurrent('P1');
    e.preventDefault();
  }
});

// 초기 실행
initAtmosphere();
buildTerrain();
placeTanks();
syncFromSliders();
requestAnimationFrame(gameLoop);
</script>
</body>
</html>
"""

components.html(HTML_CODE, height=760, scrolling=False)

with st.expander("🎮 물리 포트리스 조작법 & 포물선 탄도 공식 공략", expanded=False):
    st.markdown(
        """
- **정통 포트리스 조작법**:
  - **키보드 조작**: `← / →` 탱크 이동(연료 소모), `↑ / ↓` 포신 각도 조절, **`Space` 키를 길게 눌러 파워 게이지 충전 후 떼면 발사**됩니다!
  - **마우스 조작**: 하단 파워 게이지 바를 직접 클릭하거나 우측 슬라이더로 각도($\\theta$)·초기 속력($v_0$)을 맞춘 뒤 **`🔥 FIRE!`** 버튼을 누르세요.
- **특수 무기 4종**:
  - **① 일반 포탄**: 표준 포물선 궤적 포탄
  - **② 중량 고폭탄**: 넓은 폭발 반경과 큰 지형 크레이터 생성
  - **③ 3연발 확산탄**: 초기 속력이 조금씩 다른 3발을 동시에 발사하여 속력에 따른 사거리 변화를 한눈에 비교
  - **④ 물리 보각탄 ($\\theta$ & $90^\\circ-\\theta$ 동시 발사)**: 현재 각도 $\\theta$와 보각 $90^\\circ-\\theta$로 두 발을 동시에 발사합니다. 평지·무풍(STAGE 1)에서 서로 다른 최고점 높이 $H$를 지나 **동일한 수평 도달거리 $R = \\dfrac{v_0^2 \\sin 2\\theta}{g}$**에 탄착하는 모습을 직접 확인해 보세요!
"""
    )
