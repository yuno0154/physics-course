import streamlit as st
import streamlit.components.v1 as components

st.title("🎯 [게임] 물리 포트리스 V2: 포물선 탄도 포격전")
st.caption("포트리스 V2 스타일 2.5D 카툰 그래픽·포탄 추적 카메라·지형 파괴 액션과 포물선 운동 물리학(v₀, θ, 보각 90°−θ, 바람 가속도)을 결합한 시뮬레이션 게임")

HTML_CODE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', 'Malgun Gothic', sans-serif; user-select: none; }
  body { background: #070b14; color: #f8fafc; padding: 6px; overflow-x: hidden; }

  /* 포트리스 V2 아케이드 프레임 */
  .fort-frame {
    background: linear-gradient(180deg, #1e293b 0%, #090d16 100%);
    border: 3px solid #475569;
    border-radius: 18px;
    box-shadow: 0 18px 45px rgba(0,0,0,0.8), inset 0 2px 0 rgba(255,255,255,0.18);
    overflow: hidden;
  }

  /* 상단 스테이지/환경 선택 바 */
  .top-bar {
    display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px;
    padding: 8px 14px;
    background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
    border-bottom: 2px solid #0f172a;
  }
  .stage-list { display: flex; flex-wrap: wrap; gap: 5px; }
  .st-btn {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    color: #cbd5e1; border: 1.5px solid #475569; border-radius: 9px;
    padding: 6px 11px; font-size: 12px; font-weight: 800; cursor: pointer; transition: 0.15s;
  }
  .st-btn:hover { border-color: #facc15; color: #fff; transform: translateY(-1px); }
  .st-btn.active {
    background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
    color: #090d16; border-color: #fef08a;
    box-shadow: 0 0 14px rgba(245, 158, 11, 0.65);
  }

  .env-tools { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
  .env-sel, .env-btn {
    background: #0f172a; color: #f8fafc; border: 1.5px solid #475569; border-radius: 8px;
    padding: 5px 9px; font-size: 12px; font-weight: 800; cursor: pointer;
  }
  .env-btn:hover { border-color: #38bdf8; color: #38bdf8; }

  /* 메인 게임 캔버스 영역 */
  .stage-viewport {
    position: relative; width: 100%; height: 500px; background: #1e3a8a; overflow: hidden;
  }
  canvas#mainCanvas { display: block; width: 100%; height: 100%; }

  /* 상단 인게임 HUD */
  .ingame-top {
    position: absolute; top: 10px; left: 12px; right: 12px;
    display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none;
  }
  .status-card {
    background: linear-gradient(180deg, rgba(15,23,42,0.88) 0%, rgba(9,13,22,0.92) 100%);
    border: 2px solid #38bdf8; border-radius: 14px; padding: 8px 14px; min-width: 245px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.55); backdrop-filter: blur(6px);
  }
  .status-card.enemy { border-color: #f87171; text-align: right; }
  .sc-head { display: flex; justify-content: space-between; align-items: center; font-size: 13.5px; font-weight: 900; }
  .sc-body { font-size: 11.5px; color: #e2e8f0; margin-top: 3px; font-weight: 600; }

  /* 중앙 풍향계 & 턴 배지 */
  .center-widget { display: flex; flex-direction: column; align-items: center; gap: 5px; }
  .turn-badge {
    background: linear-gradient(180deg, #fef08a 0%, #f59e0b 100%);
    color: #090d16; border: 2px solid #fff; border-radius: 99px;
    padding: 4px 20px; font-size: 13px; font-weight: 900;
    box-shadow: 0 4px 16px rgba(245, 158, 11, 0.55);
  }
  .wind-gauge {
    background: rgba(9, 13, 22, 0.9); border: 2px solid #60a5fa; border-radius: 12px;
    padding: 5px 16px; font-size: 12.5px; font-weight: 900; color: #93c5fd;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }

  /* 좌하단 실시간 물리 텔레메트리 */
  .phys-hud {
    position: absolute; bottom: 10px; left: 12px;
    background: rgba(9, 13, 22, 0.86); border: 1.5px solid rgba(148, 163, 184, 0.45);
    border-radius: 11px; padding: 7px 13px; font-size: 11.5px; color: #e2e8f0;
    display: flex; gap: 13px; pointer-events: none; backdrop-filter: blur(5px);
  }
  .phys-hud b { color: #fde047; font-weight: 900; }

  /* 중앙 임팩트 배너 */
  .impact-banner {
    position: absolute; top: 36%; left: 50%; transform: translate(-50%, -50%) scale(0.8);
    background: linear-gradient(180deg, rgba(15,23,42,0.96) 0%, rgba(9,13,22,0.98) 100%);
    border: 3px solid #fde047; border-radius: 18px; padding: 15px 32px;
    text-align: center; pointer-events: none; opacity: 0;
    transition: all 0.22s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 20px 50px rgba(0,0,0,0.85);
  }
  .impact-banner.show { opacity: 1; transform: translate(-50%, -50%) scale(1); }
  .ib-title { font-size: 24px; font-weight: 900; color: #fde047; text-shadow: 0 3px 12px rgba(250,204,21,0.55); }
  .ib-sub { font-size: 13px; color: #f8fafc; margin-top: 5px; font-weight: 700; }

  /* ═══════════════════════════════════════════════════════════════
     포트리스 V2 정통 아케이드 하단 계기판 (Metallic Gold/Blue Deck)
     ═══════════════════════════════════════════════════════════════ */
  .v2-deck {
    background: linear-gradient(180deg, #334155 0%, #1e293b 35%, #0f172a 100%);
    border-top: 3px solid #94a3b8;
    padding: 10px 14px;
    display: grid;
    grid-template-columns: 225px 1fr 275px;
    gap: 12px;
    align-items: center;
  }
  @media (max-width: 900px) { .v2-deck { grid-template-columns: 1fr; } }

  /* 1) 좌측: 탱크 각도기 서클 & 이동 컨트롤 */
  .angle-module {
    background: linear-gradient(180deg, #0f172a 0%, #090d16 100%);
    border: 2px solid #64748b; border-radius: 14px; padding: 8px 10px;
    display: flex; align-items: center; gap: 10px;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.7);
  }
  .angle-num { font-size: 23px; font-weight: 900; color: #fde047; text-shadow: 0 0 10px rgba(250,204,21,0.4); }
  .deck-mini-btns { display: flex; gap: 4px; margin-top: 5px; }
  .d-btn {
    background: linear-gradient(180deg, #334155 0%, #1e293b 100%);
    color: #f8fafc; border: 1px solid #64748b; border-radius: 6px;
    padding: 4px 7px; font-size: 11px; font-weight: 900; cursor: pointer;
  }
  .d-btn:hover { border-color: #fde047; color: #fde047; }

  /* 2) 중앙: 아이템 캡슐 슬롯 & 포트리스 V2 눈금 게이지 바 */
  .center-module {
    background: linear-gradient(180deg, #0f172a 0%, #090d16 100%);
    border: 2px solid #64748b; border-radius: 14px; padding: 9px 14px;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.7);
  }
  .item-capsules {
    display: flex; justify-content: space-between; align-items: center; gap: 6px; margin-bottom: 8px; flex-wrap: wrap;
  }
  .cap-group { display: flex; gap: 5px; flex-wrap: wrap; }
  .cap-btn {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    color: #cbd5e1; border: 1.5px solid #475569; border-radius: 99px;
    padding: 4px 11px; font-size: 11.5px; font-weight: 900; cursor: pointer; transition: 0.15s;
  }
  .cap-btn:hover { border-color: #60a5fa; color: #fff; }
  .cap-btn.active {
    background: linear-gradient(180deg, #fde047 0%, #eab308 100%);
    color: #090d16; border-color: #fff; box-shadow: 0 0 12px rgba(250, 204, 21, 0.6);
  }

  .g-row { display: flex; align-items: center; gap: 8px; margin-bottom: 7px; }
  .g-tag {
    width: 62px; font-size: 11.5px; font-weight: 900; color: #fde047;
    text-align: right; letter-spacing: 0.03em;
  }
  .v2-power-bar {
    flex: 1; height: 24px; background: #050811; border: 2px solid #94a3b8;
    border-radius: 7px; position: relative; cursor: pointer;
    box-shadow: inset 0 3px 6px rgba(0,0,0,0.85);
  }
  .v2-power-fill {
    height: 100%; width: 50%; border-radius: 4px;
    background: linear-gradient(90deg, #22c55e 0%, #84cc16 35%, #eab308 65%, #f97316 85%, #ef4444 100%);
    box-shadow: 0 0 12px rgba(239, 68, 68, 0.5);
    transition: width 0.02s linear;
  }
  .v2-ticks {
    position: absolute; inset: 0;
    background-image: repeating-linear-gradient(90deg, transparent, transparent 9.8%, rgba(255,255,255,0.22) 9.8%, rgba(255,255,255,0.22) 10.0%);
    pointer-events: none;
  }
  .mark-prev {
    position: absolute; bottom: -8px; width: 0; height: 0;
    border-left: 6px solid transparent; border-right: 6px solid transparent;
    border-bottom: 8px solid #ef4444; transform: translateX(-6px); display: none;
  }
  .mark-hint {
    position: absolute; top: -8px; width: 0; height: 0;
    border-left: 6px solid transparent; border-right: 6px solid transparent;
    border-top: 8px solid #fde047; transform: translateX(-6px);
  }
  .g-val { min-width: 74px; text-align: right; font-size: 13.5px; font-weight: 900; color: #38bdf8; }

  .sub-gauges { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .mini-bar {
    flex: 1; height: 12px; background: #050811; border: 1.5px solid #475569; border-radius: 99px; overflow: hidden;
  }
  .fill-hp { height: 100%; width: 100%; background: linear-gradient(90deg, #dc2626, #22c55e); transition: width 0.25s; }
  .fill-move { height: 100%; width: 100%; background: linear-gradient(90deg, #2563eb, #38bdf8); transition: width 0.15s; }

  /* 3) 우측: 슬라이더 & 발사 버튼 */
  .fire-module {
    background: linear-gradient(180deg, #0f172a 0%, #090d16 100%);
    border: 2px solid #64748b; border-radius: 14px; padding: 9px 12px;
    display: flex; flex-direction: column; gap: 6px;
  }
  .ctrl-line { display: flex; align-items: center; gap: 6px; font-size: 12px; }
  .ctrl-line span { width: 56px; font-weight: 800; color: #e2e8f0; }
  .ctrl-line input[type=range] { flex: 1; accent-color: #f59e0b; cursor: pointer; }
  .v2-fire-btn {
    padding: 10px 12px; border-radius: 10px; border: 2px solid #fef08a;
    background: linear-gradient(180deg, #ef4444 0%, #dc2626 55%, #991b1b 100%);
    color: #fff; font-size: 14.5px; font-weight: 900; cursor: pointer;
    text-shadow: 0 2px 4px rgba(0,0,0,0.6);
    box-shadow: 0 5px 16px rgba(239, 68, 68, 0.55); transition: 0.12s;
  }
  .v2-fire-btn:hover { filter: brightness(1.15); transform: translateY(-1px); }
  .v2-fire-btn:disabled { opacity: 0.45; cursor: not-allowed; }

  .bottom-options {
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
    padding: 7px 14px; background: #090d16; border-top: 1px solid #1e293b; font-size: 12px; color: #94a3b8;
  }
  .opt-group { display: flex; gap: 13px; flex-wrap: wrap; }
  .opt-group label { display: flex; align-items: center; gap: 4px; cursor: pointer; color: #e2e8f0; font-weight: 700; }
</style>
</head>
<body>

<div class="fort-frame">
  <!-- 상단 스테이지 & 탱크/행성 선택 바 -->
  <div class="top-bar">
    <div class="stage-list">
      <button class="st-btn active" onclick="setStage(1)">🌴 STAGE 1: 밸리 오브 시티 (평지)</button>
      <button class="st-btn" onclick="setStage(2)">⛰️ STAGE 2: 드래곤 마운틴 (고각 산넘기)</button>
      <button class="st-btn" onclick="setStage(3)">🏛️ STAGE 3: 스카이 템플 (고지대 요새)</button>
      <button class="st-btn" onclick="setStage(4)">🌪️ STAGE 4: 윈드 캐년 (강풍 탄도보정)</button>
      <button class="st-btn" onclick="setStage(5)">🔥 STAGE 5: 보스 다크탱크 결전 (AI 대전)</button>
    </div>
    <div class="env-tools">
      <select id="tankSkin" class="env-sel" onchange="changeSkin()">
        <option value="cannon">🛡️ 캐논 (레드 헤비탱크)</option>
        <option value="duke">⚡ 듀크 (블루 미사일탱크)</option>
        <option value="super">🌟 슈퍼탱크 (골드 사이버탱크)</option>
      </select>
      <select id="planetGrav" class="env-sel" onchange="changeGravity()">
        <option value="9.8">🌍 지구 (g=9.8m/s²)</option>
        <option value="3.7">🔴 화성 (g=3.7m/s²)</option>
        <option value="1.6">🌙 달 (g=1.6m/s²)</option>
      </select>
      <button class="env-btn" id="sfxBtn" onclick="toggleSfx()">🔊 사운드 ON</button>
      <button class="env-btn" onclick="resetMap()">🔄 맵 재생성</button>
    </div>
  </div>

  <!-- 메인 게임 뷰포트 -->
  <div class="stage-viewport">
    <canvas id="mainCanvas" width="1080" height="500"></canvas>

    <!-- 상단 오버레이 -->
    <div class="ingame-top">
      <div class="status-card">
        <div class="sc-head">
          <span style="color:#38bdf8;">🛡️ PLAYER 1 (내 탱크)</span>
          <span id="p1HpBadge" style="color:#4ade80;">HP 100%</span>
        </div>
        <div class="sc-body">
          표적까지 수평거리 <b style="color:#fde047;">Δx = <span id="uiDx">0.0</span> m</b> ·
          높이차 <b style="color:#fde047;">Δy = <span id="uiDy">0.0</span> m</b>
        </div>
        <div class="sc-body" style="color:#93c5fd;" id="uiStageGuide">
          평지 수평 도달거리 공식 R = (v₀² sin2θ)/g 를 확인하고 발사하세요!
        </div>
      </div>

      <div class="center-widget">
        <div class="turn-badge" id="uiTurnBadge">⚡ PLAYER 1 TURN — 조준 완료!</div>
        <div class="wind-gauge" id="uiWindBox">🌬️ WIND: 0.0 m/s² (무풍)</div>
      </div>

      <div class="status-card enemy">
        <div class="sc-head">
          <span id="p2HpBadge" style="color:#f87171;">HP 100%</span>
          <span style="color:#fca5a5;" id="uiEnemyName">🎯 TARGET FORTRESS</span>
        </div>
        <div class="sc-body">
          명중 전적: <b style="color:#fde047;" id="uiHits">0</b> 명중 / <span id="uiShots">0</span> 발사
        </div>
        <div class="sc-body" style="color:#cbd5e1;">
          직전 발사: <span id="uiPrevShot">기록 없음</span>
        </div>
      </div>
    </div>

    <!-- 좌하단 실시간 물리 텔레메트리 -->
    <div class="phys-hud">
      <div>초기 수평속도 <b>v₀x = <span id="phV0x">29.7</span> m/s</b></div>
      <div>초기 연직속도 <b>v₀y = <span id="phV0y">29.7</span> m/s</b></div>
      <div>이론 최고높이(평지) <b>H = <span id="phH">45.0</span> m</b></div>
      <div>이론 수평사거리(평지) <b>R = <span id="phR">180.0</span> m</b></div>
      <div>비행 시간 <b>t = <span id="phT">0.00</span> s</b></div>
    </div>

    <!-- 중앙 임팩트 알림 배너 -->
    <div class="impact-banner" id="impactBanner">
      <div class="ib-title" id="ibTitle">💥 CRITICAL HIT!!</div>
      <div class="ib-sub" id="ibSub">정확한 포물선 궤적으로 표적을 명중시켰습니다!</div>
    </div>
  </div>

  <!-- 포트리스 V2 정통 하단 계기판 -->
  <div class="v2-deck">
    <!-- 1. 좌측: 각도기 레이더 다이얼 -->
    <div class="angle-module">
      <canvas id="angleDial" width="86" height="86"></canvas>
      <div>
        <div style="font-size:11px;color:#94a3b8;font-weight:800;">포신 발사각 (θ)</div>
        <div class="angle-num"><span id="uiAngleBig">45</span>°</div>
        <div style="font-size:11px;color:#cbd5e1;">지형 경사: <span id="uiSlope">0°</span></div>
        <div class="deck-mini-btns">
          <button class="d-btn" onclick="nudgeAngle(-1)">▼ -1°</button>
          <button class="d-btn" onclick="nudgeAngle(1)">▲ +1°</button>
          <button class="d-btn" onclick="flipComplementary()" title="보각(90°-θ) 전환">90°−θ</button>
        </div>
      </div>
    </div>

    <!-- 2. 중앙: 아이템 캡슐 & 파워 게이지 바 & 체력/이동 바 -->
    <div class="center-module">
      <div class="item-capsules">
        <div class="cap-group">
          <button class="cap-btn active" id="cap1" onclick="setWeapon(1)">💣 기본 포탄</button>
          <button class="cap-btn" id="cap2" onclick="setWeapon(2)">🔥 파워업 고폭탄 (화력 1.4배)</button>
          <button class="cap-btn" id="cap3" onclick="setWeapon(3)">⚡ 더블샷 (연속 2연발)</button>
          <button class="cap-btn" id="cap4" onclick="setWeapon(4)">📐 보각 비교탄 (θ & 90°−θ 동시발사)</button>
        </div>
        <div style="font-size:11.5px;font-weight:900;color:#fde047;" id="uiHintText">
          💡 탄도 추천: v₀ ≈ 42.0 m/s (▼ 노란 화살표)
        </div>
      </div>

      <!-- 파워 게이지 -->
      <div class="g-row">
        <div class="g-tag">POWER v₀</div>
        <div class="v2-power-bar" id="powerBarTrack" onclick="clickPowerTrack(event)">
          <div class="v2-power-fill" id="powerBarFill"></div>
          <div class="v2-ticks"></div>
          <div class="mark-prev" id="markPrev" title="직전 발사 속력"></div>
          <div class="mark-hint" id="markHint" title="현재 각도에서 명중을 위한 추천 속력"></div>
        </div>
        <div class="g-val"><span id="uiSpeedBig">42.0</span> m/s</div>
      </div>

      <!-- HP & MOVE -->
      <div class="sub-gauges">
        <div class="g-row" style="margin-bottom:0;">
          <div class="g-tag" style="width:42px;color:#4ade80;">HP</div>
          <div class="mini-bar"><div class="fill-hp" id="uiHpFill"></div></div>
          <span style="font-size:11.5px;font-weight:900;width:36px;text-align:right;" id="uiHpNum">100</span>
        </div>
        <div class="g-row" style="margin-bottom:0;">
          <div class="g-tag" style="width:48px;color:#38bdf8;">MOVE</div>
          <div class="mini-bar"><div class="fill-move" id="uiMoveFill"></div></div>
          <div style="display:flex;gap:3px;">
            <button class="d-btn" onclick="stepMove(-1)">◀ 이동</button>
            <button class="d-btn" onclick="stepMove(1)">이동 ▶</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. 우측: 정밀 슬라이더 & 발사 버튼 -->
    <div class="fire-module">
      <div class="ctrl-line">
        <span>발사각 θ</span>
        <input type="range" id="slAngle" min="5" max="85" step="1" value="45" oninput="syncUI()">
      </div>
      <div class="ctrl-line">
        <span>속력 v₀</span>
        <input type="range" id="slSpeed" min="10" max="80" step="0.5" value="42.0" oninput="syncUI()">
      </div>
      <button class="v2-fire-btn" id="btnFire" onclick="triggerFire('P1')">
        🔥 FIRE!! (포탄 발사 / Space 홀드)
      </button>
      <div style="font-size:11px;color:#cbd5e1;text-align:center;">
        <b>←/→</b> 이동 · <b>↑/↓</b> 각도 · <b>Space</b> 길게 눌러 게이지 충전 발사
      </div>
    </div>
  </div>

  <!-- 하단 카메라 & 물리 벡터 옵션 바 -->
  <div class="bottom-options">
    <div class="opt-group">
      <label><input type="checkbox" id="chkCam" checked> 🎥 포트리스 포탄 추적 카메라 (Follow Cam)</label>
      <label><input type="checkbox" id="chkVec" checked onchange="render()"> 🏹 실시간 속도 성분 벡터(vx, vy) 표시</label>
      <label><input type="checkbox" id="chkTrail" checked onchange="render()"> 📈 이전 탄도 궤적 & 최고점(H) 보존</label>
      <label><input type="checkbox" id="chkHint" checked onchange="syncUI()"> 💡 탄도 계산기 추천 마커(▼) 표시</label>
    </div>
    <button class="d-btn" onclick="clearAllTrails()">🧹 탄도 궤적 초기화</button>
  </div>
</div>

<script>
const canvas = document.getElementById('mainCanvas');
const ctx = canvas.getContext('2d');
const dial = document.getElementById('angleDial');
const dctx = dial.getContext('2d');

// 월드 물리 좌표: 가로 240 m, 세로 112 m
const WORLD_W = 240.0;
const WORLD_H = 112.0;
const SX = canvas.width / WORLD_W;
const SY = canvas.height / WORLD_H;

function wx(x) { return x * SX; }
function wy(y) { return canvas.height - (y + 8.0) * SY; }

// 게임 상태
let stage = 1;
let g = 9.8;
let windAx = 0.0;
let weapon = 1;
let skin = 'cannon';
let sfxOn = true;
let audioCtx = null;

let terrain = new Float32Array(canvas.width);
let scorchMask = new Float32Array(canvas.width); // 폭발 그을림 강도
let props = []; // 배경 나무/기둥/바위 장식
let clouds = [];
let windStreaks = [];

let p1 = { x: 28.0, y: 12.0, angle: 45, speed: 42.0, hp: 100, fuel: 100, slope: 0, recoil: 0, wheelRot: 0 };
let p2 = { x: 196.0, y: 12.0, angle: 135, speed: 42.0, hp: 100, slope: 0, recoil: 0, wheelRot: 0 };

let shells = [];
let trails = [];
let particles = [];
let rings = [];
let popups = [];

let turn = 'P1';
let hits = 0;
let shots = 0;
let shakeT = 0;
let shakeAmp = 0;
let animClock = 0;

// 다이나믹 액션 카메라 상태
let cam = { x: canvas.width / 2, y: canvas.height / 2, zoom: 1.0, targetX: canvas.width / 2, targetY: canvas.height / 2, targetZoom: 1.0 };

// 스페이스바 충전 상태
let charging = false;
let chargeVal = 10.0;
let chargeDir = 1;
let chargeRaf = null;

// ── 사운드 합성 (Web Audio API) ─────────────────────────────
function getAudio() {
  if (!sfxOn) return null;
  if (!audioCtx) {
    const AC = window.AudioContext || window.webkitAudioContext;
    if (AC) audioCtx = new AC();
  }
  if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
  return audioCtx;
}

function playSfx(kind) {
  const ac = getAudio();
  if (!ac) return;
  const now = ac.currentTime;
  if (kind === 'tick') {
    const o = ac.createOscillator();
    const gn = ac.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(620, now);
    o.frequency.exponentialRampToValueAtTime(920, now + 0.035);
    gn.gain.setValueAtTime(0.07, now);
    gn.gain.exponentialRampToValueAtTime(0.001, now + 0.035);
    o.connect(gn); gn.connect(ac.destination);
    o.start(now); o.stop(now + 0.04);
  } else if (kind === 'shoot') {
    const o = ac.createOscillator();
    const gn = ac.createGain();
    o.type = 'sawtooth';
    o.frequency.setValueAtTime(190, now);
    o.frequency.exponentialRampToValueAtTime(34, now + 0.32);
    gn.gain.setValueAtTime(0.32, now);
    gn.gain.exponentialRampToValueAtTime(0.001, now + 0.34);
    o.connect(gn); gn.connect(ac.destination);
    o.start(now); o.stop(now + 0.35);
  } else if (kind === 'explode') {
    const len = Math.floor(ac.sampleRate * 0.5);
    const buf = ac.createBuffer(1, len, ac.sampleRate);
    const d = buf.getChannelData(0);
    for (let i = 0; i < len; i++) d[i] = (Math.random() * 2 - 1) * Math.exp(-i / (ac.sampleRate * 0.15));
    const src = ac.createBufferSource();
    src.buffer = buf;
    const flt = ac.createBiquadFilter();
    flt.type = 'lowpass';
    flt.frequency.setValueAtTime(480, now);
    const gn = ac.createGain();
    gn.gain.setValueAtTime(0.38, now);
    gn.gain.exponentialRampToValueAtTime(0.01, now + 0.48);
    src.connect(flt); flt.connect(gn); gn.connect(ac.destination);
    src.start(now);
  } else if (kind === 'fanfare') {
    [523.25, 659.25, 783.99, 1046.5].forEach((f, idx) => {
      const o = ac.createOscillator();
      const gn = ac.createGain();
      o.type = 'triangle';
      o.frequency.setValueAtTime(f, now + idx * 0.065);
      gn.gain.setValueAtTime(0.15, now + idx * 0.065);
      gn.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.065 + 0.2);
      o.connect(gn); gn.connect(ac.destination);
      o.start(now + idx * 0.065); o.stop(now + idx * 0.065 + 0.21);
    });
  }
}

function toggleSfx() {
  sfxOn = !sfxOn;
  document.getElementById('sfxBtn').textContent = sfxOn ? "🔊 사운드 ON" : "🔇 사운드 OFF";
}

// ── 구름 & 바람 스트림 초기화 ──────────────────────────────
function initSkyObjects() {
  clouds = [];
  for (let i = 0; i < 7; i++) {
    clouds.push({
      x: Math.random() * canvas.width,
      y: 38 + Math.random() * 125,
      scale: 0.65 + Math.random() * 0.65,
      spd: 0.25 + Math.random() * 0.35
    });
  }
  windStreaks = [];
  for (let i = 0; i < 28; i++) {
    windStreaks.push({
      x: Math.random() * canvas.width,
      y: 40 + Math.random() * (canvas.height - 120),
      len: 14 + Math.random() * 22
    });
  }
}

// ── 맵 지형 및 오브젝트(나무·신전 기둥·바위) 생성 ──────────────
function generateMap() {
  const w = canvas.width;
  const baseH = 13.0;
  scorchMask.fill(0);

  for (let px = 0; px < w; px++) {
    const x = px / SX;
    let h = baseH;
    if (stage === 1) {
      // 밸리 오브 시티: 완만한 평원
      h = baseH + 1.3 * Math.sin(x * 0.045) + 0.6 * Math.cos(x * 0.1);
    } else if (stage === 2) {
      // 드래곤 마운틴: 중앙 거대 봉우리
      const peak = 46.0 * Math.exp(-Math.pow((x - 118.0) / 24.0, 2));
      const sub = 16.0 * Math.exp(-Math.pow((x - 84.0) / 14.0, 2));
      h = baseH + peak + sub + 1.4 * Math.sin(x * 0.09);
    } else if (stage === 3) {
      // 스카이 템플: 계단식 고지대 신전
      const cliff = 35.0 / (1.0 + Math.exp(-(x - 134.0) / 3.8));
      const midStep = 14.0 * Math.exp(-Math.pow((x - 96.0) / 15.0, 2));
      h = baseH + cliff + midStep + 0.9 * Math.sin(x * 0.08);
    } else if (stage === 4) {
      // 윈드 캐년: 협곡과 능선
      const ridge = 23.0 * Math.exp(-Math.pow((x - 116.0) / 40.0, 2));
      const canyon = -9.0 * Math.exp(-Math.pow((x - 116.0) / 18.0, 2));
      h = baseH + ridge + canyon + 1.6 * Math.sin(x * 0.06);
    } else {
      // 보스 결전: 복합 전략 지형
      const c1 = 108.0 + (Math.random() - 0.5) * 24.0;
      const p1h = 22.0 + Math.random() * 20.0;
      h = baseH + p1h * Math.exp(-Math.pow((x - c1) / 25.0, 2)) + 2.4 * Math.sin(x * 0.06);
    }
    terrain[px] = Math.max(3.0, h);
  }

  // 장식 프롭(나무, 바위, 고대 신전 기둥) 배치
  props = [];
  for (let xm = 12; xm < WORLD_W - 12; xm += 18 + Math.random() * 16) {
    if (Math.abs(xm - p1.x) < 12 || Math.abs(xm - p2.x) < 12) continue;
    const gy = groundAt(xm);
    const kind = stage === 3 ? 'pillar' : (stage === 2 || stage === 4 ? 'rock' : (Math.random() > 0.35 ? 'tree' : 'rock'));
    props.push({ x: xm, y: gy, kind, scale: 0.8 + Math.random() * 0.45 });
  }
}

function groundAt(x) {
  const px = Math.max(0, Math.min(canvas.width - 1, Math.round(x * SX)));
  return terrain[px];
}

function slopeAt(x) {
  const px = Math.max(4, Math.min(canvas.width - 5, Math.round(x * SX)));
  const dy = terrain[px + 4] - terrain[px - 4];
  const dx = 8.0 / SX;
  return Math.atan2(dy, dx) * 180.0 / Math.PI;
}

function deployTanks() {
  p1.x = 24.0 + Math.random() * 16.0;
  p2.x = 180.0 + Math.random() * 34.0;
  p1.y = groundAt(p1.x);
  p2.y = groundAt(p2.x);
  p1.slope = slopeAt(p1.x);
  p2.slope = slopeAt(p2.x);
  p1.hp = 100;
  p2.hp = 100;
  p1.fuel = 100;
  turn = 'P1';

  if (stage <= 3) {
    windAx = 0.0;
  } else {
    windAx = Math.round(((Math.random() * 7.0) - 3.5) * 10) / 10;
    if (Math.abs(windAx) < 0.8) windAx = 2.3;
  }
  refreshHUD();
}

function setStage(s) {
  stage = s;
  playSfx('tick');
  document.querySelectorAll('.stage-list .st-btn').forEach((b, i) => b.classList.toggle('active', i === s - 1));
  const guides = {
    1: "STAGE 1 (밸리 오브 시티): 바람이 없습니다. R = (v₀² sin2θ)/g 공식과 📐 보각 비교탄(θ & 90°−θ)을 실험해 보세요!",
    2: "STAGE 2 (드래곤 마운틴): 높은 산맥을 넘기 위해 발사각 θ를 60° 이상으로 높여 최고점 높이 H를 확보하세요!",
    3: "STAGE 3 (스카이 템플): 표적이 높은 신전 절벽 위(Δy > 0)에 있습니다. 고도차를 고려해 발사하세요!",
    4: "STAGE 4 (윈드 캐년): 수평 바람 가속도(a_wind)가 작용합니다! 바람 방향과 세기를 보고 속력을 보정하세요!",
    5: "STAGE 5 (보스 다크탱크 결전): 매 턴 바람이 바뀌며 보스 AI 탱크가 반격합니다! 먼저 적 HP를 0으로 만드세요!"
  };
  document.getElementById('uiStageGuide').textContent = guides[s];
  document.getElementById('uiEnemyName').textContent = s === 5 ? "😈 BOSS DARK TANK" : "🎯 TARGET FORTRESS";
  resetMap();
}

function changeSkin() {
  skin = document.getElementById('tankSkin').value;
  playSfx('tick');
}

function changeGravity() {
  g = parseFloat(document.getElementById('planetGrav').value);
  playSfx('tick');
  syncUI();
}

function setWeapon(w) {
  weapon = w;
  playSfx('tick');
  for (let i = 1; i <= 4; i++) document.getElementById('cap' + i).classList.toggle('active', i === w);
}

function resetMap() {
  shells = [];
  trails = [];
  particles = [];
  rings = [];
  popups = [];
  cam.targetX = canvas.width / 2;
  cam.targetY = canvas.height / 2;
  cam.targetZoom = 1.0;
  deployTanks();
  generateMap();
  p1.y = groundAt(p1.x); p2.y = groundAt(p2.x);
  p1.slope = slopeAt(p1.x); p2.slope = slopeAt(p2.x);
  syncUI();
}

function clearAllTrails() {
  trails = [];
}

function nudgeAngle(d) {
  if (shells.length > 0 || turn !== 'P1') return;
  const el = document.getElementById('slAngle');
  el.value = Math.max(5, Math.min(85, parseInt(el.value, 10) + d));
  playSfx('tick');
  syncUI();
}

function flipComplementary() {
  if (shells.length > 0 || turn !== 'P1') return;
  const el = document.getElementById('slAngle');
  el.value = Math.max(5, Math.min(85, 90 - parseInt(el.value, 10)));
  playSfx('tick');
  syncUI();
}

function stepMove(dir) {
  if (shells.length > 0 || turn !== 'P1' || p1.fuel <= 0) return;
  p1.x = Math.max(10.0, Math.min(92.0, p1.x + dir * 2.0));
  p1.y = groundAt(p1.x);
  p1.slope = slopeAt(p1.x);
  p1.wheelRot += dir * 0.8;
  p1.fuel = Math.max(0, p1.fuel - 8);
  playSfx('tick');
  syncUI();
}

function clickPowerTrack(e) {
  if (shells.length > 0 || turn !== 'P1') return;
  const rect = document.getElementById('powerBarTrack').getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  const v0 = 10.0 + ratio * 70.0;
  document.getElementById('slSpeed').value = (Math.round(v0 * 2) / 2).toFixed(1);
  playSfx('tick');
  syncUI();
}

function calcRecommendedV0(dx, dy, thetaDeg) {
  const rad = thetaDeg * Math.PI / 180.0;
  const sin = Math.sin(rad);
  const tan = Math.tan(rad);
  const cT2 = (0.5 * g / tan) + 0.5 * windAx;
  const rhs = dx - (dy / tan);
  if (cT2 <= 0.0001 || rhs <= 0) return null;
  const t = Math.sqrt(rhs / cT2);
  if (!isFinite(t) || t <= 0.05) return null;
  const v0 = (dy + 0.5 * g * t * t) / (sin * t);
  if (!isFinite(v0) || v0 < 10 || v0 > 80) return null;
  return v0;
}

function syncUI() {
  p1.angle = parseFloat(document.getElementById('slAngle').value);
  p1.speed = parseFloat(document.getElementById('slSpeed').value);

  document.getElementById('uiAngleBig').textContent = p1.angle.toFixed(0);
  document.getElementById('uiSpeedBig').textContent = p1.speed.toFixed(1);
  document.getElementById('uiSlope').textContent = (p1.slope >= 0 ? "+" : "") + p1.slope.toFixed(0) + "°";

  const pct = ((p1.speed - 10.0) / 70.0) * 100.0;
  document.getElementById('powerBarFill').style.width = `${Math.max(0, Math.min(100, pct))}%`;

  const rad = p1.angle * Math.PI / 180.0;
  const v0x = p1.speed * Math.cos(rad);
  const v0y = p1.speed * Math.sin(rad);
  const theoH = (v0y * v0y) / (2.0 * g);
  const theoR = (p1.speed * p1.speed * Math.sin(2.0 * rad)) / g;

  document.getElementById('phV0x').textContent = v0x.toFixed(1);
  document.getElementById('phV0y').textContent = v0y.toFixed(1);
  document.getElementById('phH').textContent = theoH.toFixed(1);
  document.getElementById('phR').textContent = theoR.toFixed(1);

  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  const recV0 = calcRecommendedV0(dx, dy, p1.angle);
  const mh = document.getElementById('markHint');
  const ht = document.getElementById('uiHintText');
  const showH = document.getElementById('chkHint').checked;

  if (showH && recV0 !== null) {
    const hpct = ((recV0 - 10.0) / 70.0) * 100.0;
    mh.style.display = 'block';
    mh.style.left = `${Math.max(0, Math.min(100, hpct))}%`;
    ht.textContent = `💡 탄도 계산기 추천 (θ=${p1.angle}°): v₀ ≈ ${recV0.toFixed(1)} m/s (▼ 노란 마커)`;
  } else if (showH) {
    mh.style.display = 'none';
    ht.textContent = `⚠️ 현재 각도(θ=${p1.angle}°)로는 도달 불가 — 각도를 더 높이세요!`;
  } else {
    mh.style.display = 'none';
    ht.textContent = `💡 탄도 추천 마커 숨김 중`;
  }

  refreshHUD();
  drawAngleDial();
}

function refreshHUD() {
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  document.getElementById('uiDx').textContent = dx.toFixed(1);
  document.getElementById('uiDy').textContent = (dy >= 0 ? "+" : "") + dy.toFixed(1);
  document.getElementById('p1HpBadge').textContent = `HP ${Math.max(0, Math.round(p1.hp))}%`;
  document.getElementById('p2HpBadge').textContent = `HP ${Math.max(0, Math.round(p2.hp))}%`;
  document.getElementById('uiHpFill').style.width = `${Math.max(0, p1.hp)}%`;
  document.getElementById('uiHpNum').textContent = Math.max(0, Math.round(p1.hp));
  document.getElementById('uiMoveFill').style.width = `${Math.max(0, p1.fuel)}%`;
  document.getElementById('uiHits').textContent = hits;
  document.getElementById('uiShots').textContent = shots;

  const wb = document.getElementById('uiWindBox');
  if (Math.abs(windAx) < 0.05) {
    wb.textContent = "🌬️ WIND: 0.0 m/s² (무풍)";
    wb.style.borderColor = "#94a3b8"; wb.style.color = "#e2e8f0";
  } else if (windAx > 0) {
    wb.textContent = `🌬️ WIND: ▶ 순풍 +${windAx.toFixed(1)} m/s²`;
    wb.style.borderColor = "#38bdf8"; wb.style.color = "#38bdf8";
  } else {
    wb.textContent = `🌬️ WIND: ◀ 역풍 ${windAx.toFixed(1)} m/s²`;
    wb.style.borderColor = "#f472b6"; wb.style.color = "#f472b6";
  }
}

function showImpactBanner(title, sub, color = "#fde047") {
  const b = document.getElementById('impactBanner');
  const t = document.getElementById('ibTitle');
  const s = document.getElementById('ibSub');
  t.textContent = title; t.style.color = color;
  s.textContent = sub;
  b.style.borderColor = color;
  b.classList.add('show');
  setTimeout(() => b.classList.remove('show'), 2100);
}

// ── 좌측 각도기 레이더 다이얼 ──────────────────────────────
function drawAngleDial() {
  const w = dial.width, h = dial.height;
  const cx = w / 2, cy = h / 2 + 14;
  const r = 35;
  dctx.clearRect(0, 0, w, h);

  dctx.save();
  dctx.fillStyle = "#050811";
  dctx.strokeStyle = "#64748b";
  dctx.lineWidth = 2;
  dctx.beginPath();
  dctx.arc(cx, cy, r, Math.PI, 0);
  dctx.closePath();
  dctx.fill();
  dctx.stroke();

  dctx.strokeStyle = "rgba(148,163,184,0.25)";
  dctx.lineWidth = 1;
  for (let a = 15; a < 90; a += 15) {
    const rad = a * Math.PI / 180;
    dctx.beginPath();
    dctx.moveTo(cx, cy);
    dctx.lineTo(cx + Math.cos(rad) * r, cy - Math.sin(rad) * r);
    dctx.stroke();
  }

  const rad = p1.angle * Math.PI / 180;
  dctx.fillStyle = "rgba(250, 204, 21, 0.28)";
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.arc(cx, cy, r - 2, -rad, 0);
  dctx.closePath();
  dctx.fill();

  // 보각 점선
  const cRad = (90 - p1.angle) * Math.PI / 180;
  dctx.strokeStyle = "rgba(56, 189, 248, 0.65)";
  dctx.setLineDash([2, 2]);
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.lineTo(cx + Math.cos(cRad) * r, cy - Math.sin(cRad) * r);
  dctx.stroke();
  dctx.setLineDash([]);

  // 포신 바늘
  dctx.strokeStyle = "#fde047";
  dctx.lineWidth = 2.8;
  dctx.beginPath();
  dctx.moveTo(cx, cy);
  dctx.lineTo(cx + Math.cos(rad) * r, cy - Math.sin(rad) * r);
  dctx.stroke();

  dctx.fillStyle = "#fff";
  dctx.beginPath();
  dctx.arc(cx, cy, 3.8, 0, Math.PI * 2);
  dctx.fill();
  dctx.restore();
}

// ── 지형 크레이터 함몰 & 그을림 ─────────────────────────────
function deformTerrain(hitX, radiusM) {
  const cPx = Math.round(hitX * SX);
  const rPx = Math.round(radiusM * SX);
  for (let px = Math.max(0, cPx - rPx); px <= Math.min(canvas.width - 1, cPx + rPx); px++) {
    const u = Math.abs(px - cPx) / rPx;
    const depth = (1.0 - u * u) * (radiusM * 0.78);
    terrain[px] = Math.max(2.2, terrain[px] - depth);
    scorchMask[px] = Math.min(1.0, scorchMask[px] + (1.0 - u) * 0.9);
  }
  p1.y = groundAt(p1.x); p2.y = groundAt(p2.x);
  p1.slope = slopeAt(p1.x); p2.slope = slopeAt(p2.x);
}

function spawnExplosionFX(x, y, radiusM, color) {
  playSfx('explode');
  shakeT = 0.36;
  shakeAmp = radiusM * 1.8;

  rings.push({ x, y, r: 0.6, maxR: radiusM * 2.4, alpha: 1.0, color });
  rings.push({ x, y, r: 0.2, maxR: radiusM * 1.5, alpha: 0.9, color: "#fde047" });

  // 화염구 & 연기 버섯구름 & 튀어오르는 바위 파편
  for (let i = 0; i < 46; i++) {
    const a = Math.random() * Math.PI * 2;
    const s = 4 + Math.random() * 28;
    const isRock = i < 12;
    particles.push({
      x, y,
      vx: Math.cos(a) * s,
      vy: Math.sin(a) * s + (isRock ? 12 : 5),
      size: isRock ? (3.5 + Math.random() * 4) : (4 + Math.random() * 8),
      life: 1.0,
      isRock,
      color: isRock ? "#475569" : (i % 3 === 0 ? "#fef08a" : (i % 3 === 1 ? "#f97316" : color))
    });
  }
}

function addPopup(x, y, txt, color) {
  popups.push({ x, y: y + 4.5, txt, color, life: 1.4 });
}

// ── 포탄 생성 및 발사 ─────────────────────────────────────
function makeShell(owner, angleDeg, speed, color, label, dmgScale = 1.0) {
  const shooter = owner === 'P1' ? p1 : p2;
  const rad = angleDeg * Math.PI / 180.0;
  const sx = shooter.x + Math.cos(rad) * 3.0;
  const sy = shooter.y + 2.1 + Math.sin(rad) * 3.0;
  const vx0 = speed * Math.cos(rad);
  const vy0 = speed * Math.sin(rad);

  return {
    owner, label, color, dmgScale,
    angleDeg, speed,
    x0: sx, y0: sy,
    x: sx, y: sy,
    vx0, vy0, vx: vx0, vy: vy0,
    t: 0.0,
    maxY: sy, peakX: sx, peakMarked: false,
    pts: [{ x: sx, y: sy }]
  };
}

function triggerFire(owner = 'P1') {
  if (shells.length > 0) return;
  document.getElementById('btnFire').disabled = true;
  playSfx('shoot');

  if (owner === 'P1') {
    shots++;
    p1.recoil = 8.5;
    const mp = document.getElementById('markPrev');
    mp.style.display = 'block';
    mp.style.left = `${Math.max(0, Math.min(100, ((p1.speed - 10.0) / 70.0) * 100.0))}%`;
    document.getElementById('uiPrevShot').textContent = `θ=${p1.angle}°, v₀=${p1.speed.toFixed(1)}m/s`;

    // 포구 화염구 연출
    const rad = p1.angle * Math.PI / 180.0;
    const mx = p1.x + Math.cos(rad) * 3.1;
    const my = p1.y + 2.1 + Math.sin(rad) * 3.1;
    for (let i = 0; i < 18; i++) {
      const a = rad + (Math.random() - 0.5) * 0.55;
      const s = 8 + Math.random() * 14;
      particles.push({
        x: mx, y: my, vx: Math.cos(a) * s, vy: Math.sin(a) * s,
        size: 4.5, life: 0.4, isRock: false, color: "#fef08a"
      });
    }

    if (weapon === 1) {
      shells.push(makeShell('P1', p1.angle, p1.speed, "#38bdf8", `θ=${p1.angle}°`, 1.0));
    } else if (weapon === 2) {
      shells.push(makeShell('P1', p1.angle, p1.speed, "#f97316", `파워고폭 θ=${p1.angle}°`, 1.4));
    } else if (weapon === 3) {
      // 더블샷: 1탄 즉시 발사 + 0.28초 뒤 2탄 자동 발사!
      shells.push(makeShell('P1', p1.angle, p1.speed, "#38bdf8", `1탄 θ=${p1.angle}°`, 0.75));
      setTimeout(() => {
        playSfx('shoot');
        p1.recoil = 8.5;
        shells.push(makeShell('P1', p1.angle, p1.speed + 0.6, "#60a5fa", `2탄 θ=${p1.angle}°`, 0.75));
      }, 280);
    } else if (weapon === 4) {
      // 보각 비교탄: θ 와 90°-θ 동시 발사
      const comp = Math.max(5, Math.min(85, 90 - p1.angle));
      shells.push(makeShell('P1', p1.angle, p1.speed, "#38bdf8", `주탄 θ=${p1.angle}°`, 0.85));
      if (comp !== p1.angle) {
        shells.push(makeShell('P1', comp, p1.speed, "#fde047", `보각탄 90°−θ=${comp}°`, 0.85));
      }
    }
  } else {
    p2.recoil = 8.5;
    shells.push(makeShell('AI', p2.angle, p2.speed, "#f87171", `AI 포탄`, 1.0));
  }
}

function startAiTurn() {
  document.getElementById('uiTurnBadge').textContent = "😈 BOSS DARK TANK 조준 중...";
  const dx = p1.x - p2.x;
  const dy = p1.y - p2.y;
  const elev = 48 + Math.round((Math.random() - 0.5) * 14);
  p2.angle = 180 - elev;
  const rad = elev * Math.PI / 180.0;
  const absDx = Math.abs(dx);
  const tan = Math.tan(rad);
  const cT2 = (0.5 * g / tan) - 0.5 * windAx;
  const rhs = absDx - (dy / tan);
  let v0 = 42.0;
  if (cT2 > 0.01 && rhs > 0) {
    const t = Math.sqrt(rhs / cT2);
    v0 = (dy + 0.5 * g * t * t) / (Math.sin(rad) * t);
  }
  p2.speed = Math.max(15, Math.min(76, v0 + (Math.random() - 0.5) * 3.5));
  setTimeout(() => triggerFire('AI'), 800);
}

// ── 메인 60FPS 루프 ───────────────────────────────────────
let prevNow = performance.now();

function loop(now) {
  const dt = Math.min(0.04, (now - prevNow) / 1000.0);
  prevNow = now;
  animClock += dt;
  const dtSim = dt * 2.15;

  // 구름 및 바람 스트림 애니메이션
  const wf = windAx === 0 ? 0.3 : windAx * 1.15;
  clouds.forEach((c) => {
    c.x += (c.spd + wf * 0.45) * dt * 26;
    if (c.x > canvas.width + 110) c.x = -110;
    if (c.x < -110) c.x = canvas.width + 110;
  });
  windStreaks.forEach((ws) => {
    ws.x += (windAx * 42 + 10) * dt;
    if (ws.x > canvas.width) ws.x = 0;
    if (ws.x < 0) ws.x = canvas.width;
  });

  if (p1.recoil > 0) p1.recoil = Math.max(0, p1.recoil - dt * 30);
  if (p2.recoil > 0) p2.recoil = Math.max(0, p2.recoil - dt * 30);
  if (shakeT > 0) shakeT = Math.max(0, shakeT - dt);

  // 포탄 업데이트
  let finishedOwner = null;
  for (let i = shells.length - 1; i >= 0; i--) {
    const sh = shells[i];
    const oldVy = sh.vy;
    sh.t += dtSim;
    sh.x = sh.x0 + sh.vx0 * sh.t + 0.5 * windAx * sh.t * sh.t;
    sh.y = sh.y0 + sh.vy0 * sh.t - 0.5 * g * sh.t * sh.t;
    sh.vx = sh.vx0 + windAx * sh.t;
    sh.vy = sh.vy0 - g * sh.t;

    if (sh.y > sh.maxY) {
      sh.maxY = sh.y;
      sh.peakX = sh.x;
    }
    if (!sh.peakMarked && oldVy > 0 && sh.vy <= 0) {
      sh.peakMarked = true;
      addPopup(sh.x, sh.y + 2, `★ 최고점 H=${(sh.maxY - sh.y0).toFixed(1)}m`, sh.color);
    }

    sh.pts.push({ x: sh.x, y: sh.y });
    document.getElementById('phT').textContent = sh.t.toFixed(2);

    // 포탄 연기 & 불꽃 트레일 파티클
    particles.push({
      x: sh.x, y: sh.y,
      vx: -sh.vx * 0.08 + (Math.random() - 0.5) * 2,
      vy: -sh.vy * 0.08 + (Math.random() - 0.5) * 2,
      size: 3.5, life: 0.45, isRock: false, color: sh.color
    });

    const target = sh.owner === 'P1' ? p2 : p1;
    const distT = Math.hypot(sh.x - target.x, sh.y - (target.y + 1.8));
    const gy = groundAt(sh.x);

    if (distT <= 4.5 || sh.y <= gy || sh.x < 0 || sh.x > WORLD_W) {
      const hx = sh.x;
      const hy = Math.max(sh.y, gy);
      const cRad = (sh.owner === 'P1' && weapon === 2) ? 6.5 : 4.3;

      if (document.getElementById('chkTrail').checked) {
        trails.push({
          color: sh.color,
          pts: sh.pts,
          peakX: sh.peakX,
          peakY: sh.maxY,
          netH: sh.maxY - sh.y0,
          label: `${sh.label} (R=${Math.abs(hx - sh.x0).toFixed(1)}m)`
        });
        if (trails.length > 6) trails.shift();
      }

      const d2 = Math.hypot(hx - p2.x, hy - p2.y);
      const d1 = Math.hypot(hx - p1.x, hy - p1.y);

      if (sh.owner === 'P1' && d2 < 8.2) {
        const rawDmg = d2 < 4.2 ? 48 : Math.max(14, Math.round(36 * (1 - d2 / 8.5)));
        const dmg = Math.round(rawDmg * sh.dmgScale);
        p2.hp = Math.max(0, p2.hp - dmg);
        hits++;
        playSfx('fanfare');
        spawnExplosionFX(hx, hy, cRad, "#ef4444");
        deformTerrain(hx, cRad);
        addPopup(p2.x, p2.y + 6, d2 < 4.2 ? `💥 CRITICAL -${dmg}!!` : `HIT -${dmg}!`, "#fde047");
        showImpactBanner(
          d2 < 4.2 ? "🎯 GREAT SHOT!! 정밀 직격!" : "💥 TARGET HIT!!",
          `비행 ${sh.t.toFixed(2)}s · 수평거리 ${Math.abs(hx - sh.x0).toFixed(1)}m · 최고높이 ${(sh.maxY - sh.y0).toFixed(1)}m`,
          "#4ade80"
        );
      } else if (sh.owner === 'AI' && d1 < 8.2) {
        const dmg = d1 < 4.2 ? 38 : Math.max(12, Math.round(28 * (1 - d1 / 8.5)));
        p1.hp = Math.max(0, p1.hp - dmg);
        spawnExplosionFX(hx, hy, 4.3, "#f97316");
        deformTerrain(hx, 4.3);
        addPopup(p1.x, p1.y + 6, `피격 -${dmg} HP!`, "#f87171");
        showImpactBanner("⚠️ 보스 포탄 피격!", `내 탱크가 -${dmg} 데미지를 입었습니다!`, "#f87171");
      } else {
        spawnExplosionFX(hx, hy, cRad, "#38bdf8");
        deformTerrain(hx, cRad);
        if (sh.owner === 'P1' && shells.length === 1) {
          const err = hx - p2.x;
          addPopup(hx, hy + 3, err < 0 ? `${Math.abs(err).toFixed(1)}m 짧음` : `${err.toFixed(1)}m 초과`, "#e2e8f0");
        }
      }

      finishedOwner = sh.owner;
      shells.splice(i, 1);
      refreshHUD();
    }
  }

  // 포탄 추적 카메라 (Dynamic Follow Cam) 업데이트
  const followOn = document.getElementById('chkCam').checked;
  if (followOn && shells.length > 0) {
    const lead = shells[0];
    cam.targetX = wx(lead.x);
    cam.targetY = wy(lead.y);
    cam.targetZoom = 1.26;
  } else {
    cam.targetX = canvas.width / 2;
    cam.targetY = canvas.height / 2;
    cam.targetZoom = 1.0;
  }
  cam.x += (cam.targetX - cam.x) * dt * 5.5;
  cam.y += (cam.targetY - cam.y) * dt * 5.5;
  cam.zoom += (cam.targetZoom - cam.zoom) * dt * 5.5;

  // 턴 종료 처리
  if (finishedOwner && shells.length === 0) {
    if (p2.hp <= 0) {
      showImpactBanner("🏆 VICTORY!! 표적 완전 격파!", "잠시 후 새로운 요새가 배치됩니다.", "#fde047");
      setTimeout(() => {
        deployTanks();
        syncUI();
        document.getElementById('uiTurnBadge').textContent = "⚡ PLAYER 1 TURN — 조준 완료!";
        document.getElementById('btnFire').disabled = false;
      }, 1500);
    } else if (p1.hp <= 0) {
      showImpactBanner("💀 DEFEAT... 내 탱크 파손", "스테이지를 다시 시작합니다.", "#f87171");
      setTimeout(() => {
        resetMap();
        document.getElementById('uiTurnBadge').textContent = "⚡ PLAYER 1 TURN — 조준 완료!";
        document.getElementById('btnFire').disabled = false;
      }, 1600);
    } else if (stage === 5 && finishedOwner === 'P1') {
      turn = 'AI';
      setTimeout(startAiTurn, 850);
    } else {
      turn = 'P1';
      p1.fuel = 100;
      if (stage >= 4) {
        windAx = Math.round(((Math.random() * 7.0) - 3.5) * 10) / 10;
      }
      document.getElementById('uiTurnBadge').textContent = "⚡ PLAYER 1 TURN — 조준 완료!";
      syncUI();
      document.getElementById('btnFire').disabled = false;
    }
  }

  // 이펙트 파티클 업데이트
  for (let i = rings.length - 1; i >= 0; i--) {
    const rg = rings[i];
    rg.r += (rg.maxR - rg.r) * dt * 9;
    rg.alpha -= dt * 2.3;
    if (rg.alpha <= 0) rings.splice(i, 1);
  }
  for (let i = particles.length - 1; i >= 0; i--) {
    const pt = particles[i];
    pt.x += pt.vx * dt;
    pt.y += pt.vy * dt;
    pt.vy -= g * dt * (pt.isRock ? 1.1 : 0.45);
    pt.life -= dt * 1.85;
    if (pt.life <= 0) particles.splice(i, 1);
  }
  for (let i = popups.length - 1; i >= 0; i--) {
    const pp = popups[i];
    pp.y += dt * 4.8;
    pp.life -= dt * 0.85;
    if (pp.life <= 0) popups.splice(i, 1);
  }

  render();
  requestAnimationFrame(loop);
}

// ── 포트리스 V2 스타일 고해상도 2.5D 카툰 탱크 렌더링 ────────
function drawCartoonTank(t, isPlayer) {
  const cx = wx(t.x);
  const cy = wy(t.y);
  const bob = Math.sin(animClock * 4.5 + (isPlayer ? 0 : 2)) * 1.2;

  ctx.save();
  ctx.translate(cx, cy);
  ctx.rotate((-t.slope * Math.PI / 180.0) * 0.65);

  // 바닥 입체 그림자
  ctx.fillStyle = "rgba(0,0,0,0.48)";
  ctx.beginPath();
  ctx.ellipse(0, 3, 25, 6, 0, 0, Math.PI * 2);
  ctx.fill();

  // 스킨 컬러 팔레트
  let cMain = "#ef4444", cDark = "#991b1b", cLight = "#fca5a5", cAccent = "#fde047";
  if (isPlayer) {
    if (skin === 'cannon') {
      cMain = "#ef4444"; cDark = "#7f1d1d"; cLight = "#fecaca"; cAccent = "#fde047";
    } else if (skin === 'duke') {
      cMain = "#2563eb"; cDark = "#1e3a8a"; cLight = "#93c5fd"; cAccent = "#38bdf8";
    } else {
      cMain = "#eab308"; cDark = "#713f12"; cLight = "#fef08a"; cAccent = "#38bdf8";
    }
  } else {
    cMain = stage === 5 ? "#7c3aed" : "#dc2626";
    cDark = stage === 5 ? "#3b0764" : "#7f1d1d";
    cLight = stage === 5 ? "#ddd6fe" : "#fca5a5";
    cAccent = "#f43f5e";
  }

  // 1) 포신 (대구경 카툰 셰이딩 대포)
  const worldRad = t.angle * Math.PI / 180.0;
  const localRad = worldRad - (-t.slope * Math.PI / 180.0) * 0.65;
  const bLen = 29 - t.recoil;

  ctx.save();
  ctx.translate(0, -13 + bob);
  ctx.rotate(-localRad);
  const bGrad = ctx.createLinearGradient(0, -6, 0, 6);
  bGrad.addColorStop(0, "#f8fafc");
  bGrad.addColorStop(0.5, "#94a3b8");
  bGrad.addColorStop(1, "#1e293b");
  ctx.fillStyle = bGrad;
  ctx.strokeStyle = "#0f172a";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.roundRect(0, -5, bLen, 10, 3);
  ctx.fill();
  ctx.stroke();

  // 대구경 포구 링
  ctx.fillStyle = cAccent;
  ctx.beginPath();
  ctx.roundRect(bLen - 5, -7, 7, 14, 2);
  ctx.fill();
  ctx.stroke();
  ctx.restore();

  // 2) SD 탱크 포탑 & 헤드 (바이저 눈 포함!)
  ctx.save();
  ctx.translate(0, bob);
  const headGrad = ctx.createRadialGradient(-5, -20, 2, 0, -14, 18);
  headGrad.addColorStop(0, cLight);
  headGrad.addColorStop(0.45, cMain);
  headGrad.addColorStop(1, cDark);
  ctx.fillStyle = headGrad;
  ctx.strokeStyle = "#090d16";
  ctx.lineWidth = 2.2;
  ctx.beginPath();
  ctx.arc(0, -12, 13.5, Math.PI, 0);
  ctx.lineTo(15, -8);
  ctx.lineTo(-15, -8);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // 상단 해치 캡
  ctx.fillStyle = cAccent;
  ctx.beginPath();
  ctx.ellipse(0, -25, 6, 2.8, 0, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // 포트리스 캐릭터 바이저(눈)
  const dir = isPlayer ? 1 : -1;
  ctx.fillStyle = "#090d16";
  ctx.beginPath();
  ctx.roundRect(dir * 2, -19, dir * 9, 6, 2);
  ctx.fill();
  ctx.fillStyle = isPlayer ? "#38bdf8" : "#f43f5e";
  ctx.beginPath();
  ctx.arc(dir * 7, -16, 2.1, 0, Math.PI * 2);
  ctx.fill();

  // 3) 중장갑 차체 (Skirt Armor & 리벳)
  const hullGrad = ctx.createLinearGradient(-22, -10, 22, -2);
  hullGrad.addColorStop(0, cMain);
  hullGrad.addColorStop(1, cDark);
  ctx.fillStyle = hullGrad;
  ctx.beginPath();
  ctx.moveTo(-21, -9);
  ctx.lineTo(21, -9);
  ctx.lineTo(18, -2);
  ctx.lineTo(-18, -2);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  // 리벳 장식
  ctx.fillStyle = cLight;
  [-12, 0, 12].forEach((rx) => {
    ctx.beginPath();
    ctx.arc(rx, -5.5, 1.4, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.restore();

  // 4) 무한궤도 트랙 & 톱니 바퀴
  ctx.fillStyle = "#111827";
  ctx.strokeStyle = "#475569";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.roundRect(-22, -4, 44, 9, 4.5);
  ctx.fill();
  ctx.stroke();

  for (let wxOff = -15; wxOff <= 15; wxOff += 7.5) {
    ctx.save();
    ctx.translate(wxOff, 0.5);
    ctx.rotate(t.wheelRot);
    ctx.fillStyle = "#cbd5e1";
    ctx.beginPath();
    ctx.arc(0, 0, 3.0, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = "#334155";
    ctx.fillRect(-2.5, -0.7, 5, 1.4);
    ctx.restore();
  }

  ctx.restore();

  // 5) 탱크 상단 포트리스 스타일 이름표 & 체력바
  ctx.save();
  ctx.translate(cx, cy - 40);
  ctx.fillStyle = "rgba(9, 13, 22, 0.88)";
  ctx.strokeStyle = "#f8fafc";
  ctx.lineWidth = 1.2;
  ctx.beginPath();
  ctx.roundRect(-24, 0, 48, 7, 3);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = t.hp > 45 ? "#22c55e" : (t.hp > 20 ? "#eab308" : "#ef4444");
  ctx.fillRect(-22.5, 1.5, 45 * Math.max(0, t.hp) / 100, 4);

  ctx.font = "900 11px 'Pretendard', sans-serif";
  ctx.textAlign = "center";
  ctx.fillStyle = isPlayer ? "#fde047" : "#fca5a5";
  ctx.shadowColor = "rgba(0,0,0,0.9)";
  ctx.shadowBlur = 4;
  ctx.fillText(isPlayer ? `P1 (${t.angle.toFixed(0)}°)` : (stage === 5 ? "BOSS" : "TARGET"), 0, -4);
  ctx.restore();
}

// ── 배경 장식 프롭(야자수/소나무, 고대 신전 기둥, 바위) 그리기 ──
function drawProp(pr) {
  const x = wx(pr.x);
  const y = wy(pr.y);
  ctx.save();
  ctx.translate(x, y);
  ctx.scale(pr.scale, pr.scale);

  if (pr.kind === 'tree') {
    // 기둥
    ctx.fillStyle = "#78350f";
    ctx.fillRect(-3.5, -22, 7, 22);
    // 풍성한 3단 카툰 수관
    ctx.fillStyle = "#15803d";
    ctx.beginPath(); ctx.arc(0, -24, 13, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = "#22c55e";
    ctx.beginPath(); ctx.arc(-5, -27, 9, 0, Math.PI * 2); ctx.fill();
    ctx.beginPath(); ctx.arc(5, -26, 8, 0, Math.PI * 2); ctx.fill();
  } else if (pr.kind === 'pillar') {
    // 스카이 템플 고대 돌기둥
    ctx.fillStyle = "#cbd5e1";
    ctx.fillRect(-6, -30, 12, 30);
    ctx.fillStyle = "#94a3b8";
    ctx.fillRect(-8, -34, 16, 4);
    ctx.fillRect(-8, -4, 16, 4);
  } else {
    // 바위
    ctx.fillStyle = "#475569";
    ctx.beginPath();
    ctx.moveTo(-10, 0); ctx.lineTo(-6, -11); ctx.lineTo(4, -9); ctx.lineTo(10, 0);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
}

function drawVectorArrow(x1, y1, x2, y2, color, text) {
  const len = Math.hypot(x2 - x1, y2 - y1);
  if (len < 4) return;
  const ang = Math.atan2(y2 - y1, x2 - x1);
  const h = 8;
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 2.4;
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - h * Math.cos(ang - Math.PI / 6), y2 - h * Math.sin(ang - Math.PI / 6));
  ctx.lineTo(x2 - h * Math.cos(ang + Math.PI / 6), y2 - h * Math.sin(ang + Math.PI / 6));
  ctx.closePath();
  ctx.fill();
  if (text) {
    ctx.font = "900 11px 'Pretendard', sans-serif";
    ctx.shadowColor = "rgba(0,0,0,0.85)";
    ctx.shadowBlur = 4;
    ctx.fillText(text, x2 + 6, y2 - 4);
  }
  ctx.restore();
}

// ── 전체 씬 렌더링 ─────────────────────────────────────────
function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. 테마별 하늘 배경 (화사한 주간/석양/우주 테마)
  const sky = ctx.createLinearGradient(0, 0, 0, canvas.height);
  if (g === 3.7) {
    sky.addColorStop(0, "#451a03"); sky.addColorStop(0.55, "#9a3412"); sky.addColorStop(1, "#fdba74");
  } else if (g === 1.6) {
    sky.addColorStop(0, "#020617"); sky.addColorStop(0.6, "#0f172a"); sky.addColorStop(1, "#1e293b");
  } else if (stage === 2 || stage === 4) {
    // 석양 노을 테마
    sky.addColorStop(0, "#1e1b4b"); sky.addColorStop(0.5, "#7e22ce"); sky.addColorStop(1, "#fb923c");
  } else if (stage === 5) {
    // 보스전 다크 네온 테마
    sky.addColorStop(0, "#090d16"); sky.addColorStop(0.6, "#1e1b4b"); sky.addColorStop(1, "#311042");
  } else {
    // 포트리스 밸리 오브 시티 청량한 푸른 하늘
    sky.addColorStop(0, "#0284c7"); sky.addColorStop(0.6, "#38bdf8"); sky.addColorStop(1, "#bae6fd");
  }
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // 카메라 변환 적용 (포탄 추적 줌 & 화면 흔들림)
  ctx.save();
  const sxOff = shakeT > 0 ? (Math.random() - 0.5) * shakeAmp : 0;
  const syOff = shakeT > 0 ? (Math.random() - 0.5) * shakeAmp : 0;
  ctx.translate(canvas.width / 2 + sxOff, canvas.height / 2 + syOff);
  ctx.scale(cam.zoom, cam.zoom);
  ctx.translate(-cam.x, -cam.y);

  // 2. 원경 산맥 & 구름
  ctx.fillStyle = stage === 1 || stage === 3 ? "rgba(30, 58, 138, 0.28)" : "rgba(15, 23, 42, 0.45)";
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);
  for (let x = 0; x <= canvas.width; x += 35) {
    const y = canvas.height - 145 - 50 * Math.sin(x * 0.007) - 25 * Math.cos(x * 0.018);
    ctx.lineTo(x, y);
  }
  ctx.lineTo(canvas.width, canvas.height);
  ctx.closePath();
  ctx.fill();

  // 입체 뭉게구름
  clouds.forEach((c) => {
    ctx.save();
    ctx.translate(c.x, c.y);
    ctx.scale(c.scale, c.scale);
    ctx.fillStyle = "rgba(255, 255, 255, 0.72)";
    ctx.beginPath();
    ctx.arc(0, 0, 22, 0, Math.PI * 2);
    ctx.arc(20, -4, 18, 0, Math.PI * 2);
    ctx.arc(-20, 2, 16, 0, Math.PI * 2);
    ctx.arc(36, 4, 14, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });

  // 바람 스트림 라인
  if (Math.abs(windAx) > 0.05) {
    ctx.strokeStyle = "rgba(255, 255, 255, 0.35)";
    ctx.lineWidth = 1.8;
    windStreaks.forEach((ws) => {
      ctx.beginPath();
      ctx.moveTo(ws.x, ws.y);
      ctx.lineTo(ws.x + ws.len * (windAx > 0 ? 1 : -1), ws.y);
      ctx.stroke();
    });
  }

  // 3. 물리 거리 눈금 격자
  ctx.strokeStyle = "rgba(255, 255, 255, 0.14)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "rgba(255, 255, 255, 0.65)";
  ctx.font = "bold 10px 'Pretendard', sans-serif";
  for (let xm = 0; xm <= WORLD_W; xm += 20) {
    const px = wx(xm);
    ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, canvas.height); ctx.stroke();
    ctx.fillText(`${xm}m`, px + 3, canvas.height - 6);
  }

  // 4. 배경 장식 프롭(나무/돌기둥)
  props.forEach((pr) => {
    pr.y = groundAt(pr.x);
    drawProp(pr);
  });

  // 5. 2.5D 다층 지형 (암석 하층 + 황토 중층 + 풍성한 잔디 상층 + 폭발 그을림)
  const rockGrad = ctx.createLinearGradient(0, wy(55), 0, canvas.height);
  if (g === 3.7) {
    rockGrad.addColorStop(0, "#9a3412"); rockGrad.addColorStop(1, "#431407");
  } else if (g === 1.6) {
    rockGrad.addColorStop(0, "#64748b"); rockGrad.addColorStop(1, "#1e293b");
  } else {
    rockGrad.addColorStop(0, "#92400e"); rockGrad.addColorStop(0.35, "#78350f"); rockGrad.addColorStop(1, "#271712");
  }
  ctx.fillStyle = rockGrad;
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);
  for (let px = 0; px < canvas.width; px++) ctx.lineTo(px, wy(terrain[px]));
  ctx.lineTo(canvas.width, canvas.height);
  ctx.closePath();
  ctx.fill();

  // 단층 줄무늬(Strata) 디테일
  ctx.strokeStyle = "rgba(0, 0, 0, 0.22)";
  ctx.lineWidth = 3;
  for (let offset = 18; offset <= 75; offset += 22) {
    ctx.beginPath();
    for (let px = 0; px < canvas.width; px += 4) {
      const y = wy(terrain[px]) + offset + 3 * Math.sin(px * 0.04);
      if (px === 0) ctx.moveTo(px, y);
      else ctx.lineTo(px, y);
    }
    ctx.stroke();
  }

  // 상단 잔디 캡 (크레이터 그을림 반영)
  for (let px = 0; px < canvas.width - 1; px++) {
    const y = wy(terrain[px]);
    const sc = scorchMask[px];
    if (sc > 0.25) {
      ctx.fillStyle = "#1e293b";
    } else if (g === 3.7) {
      ctx.fillStyle = "#ea580c";
    } else if (g === 1.6) {
      ctx.fillStyle = "#cbd5e1";
    } else {
      ctx.fillStyle = "#22c55e";
    }
    ctx.fillRect(px, y, 2, 7);
    ctx.fillStyle = sc > 0.25 ? "#0f172a" : "#15803d";
    ctx.fillRect(px, y + 6, 2, 4);
  }

  // 6. 이전 탄도 궤적 및 최고점 표시
  if (document.getElementById('chkTrail').checked) {
    trails.forEach((tr) => {
      ctx.save();
      ctx.strokeStyle = tr.color;
      ctx.globalAlpha = 0.55;
      ctx.setLineDash([5, 4]);
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      tr.pts.forEach((pt, idx) => {
        if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
        else ctx.lineTo(wx(pt.x), wy(pt.y));
      });
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.globalAlpha = 0.9;
      ctx.fillStyle = tr.color;
      ctx.beginPath();
      ctx.arc(wx(tr.peakX), wy(tr.peakY), 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.font = "900 11px 'Pretendard', sans-serif";
      ctx.shadowColor = "rgba(0,0,0,0.9)";
      ctx.shadowBlur = 4;
      ctx.fillText(`★ H=${tr.netH.toFixed(1)}m`, wx(tr.peakX) - 24, wy(tr.peakY) - 8);
      const last = tr.pts[tr.pts.length - 1];
      if (last) ctx.fillText(tr.label, wx(last.x) - 30, wy(last.y) - 9);
      ctx.restore();
    });
  }

  // 7. 탱크 캐릭터 렌더링
  drawCartoonTank(p1, true);
  drawCartoonTank(p2, false);

  // 8. 발사 전 초기 속도 벡터 화살표
  if (shells.length === 0 && document.getElementById('chkVec').checked) {
    const rad = p1.angle * Math.PI / 180.0;
    const vx0 = p1.speed * Math.cos(rad);
    const vy0 = p1.speed * Math.sin(rad);
    const ox = wx(p1.x);
    const oy = wy(p1.y + 2.5);
    const vs = 1.25;
    drawVectorArrow(ox, oy, ox + vx0 * vs, oy, "#38bdf8", `v₀x=${vx0.toFixed(1)}`);
    drawVectorArrow(ox, oy, ox, oy - vy0 * vs, "#f87171", `v₀y=${vy0.toFixed(1)}`);
    drawVectorArrow(ox, oy, ox + vx0 * vs, oy - vy0 * vs, "#fde047", `v₀=${p1.speed.toFixed(1)}`);
  }

  // 9. 비행 중인 포탄 & 실시간 속도 벡터
  shells.forEach((sh) => {
    ctx.save();
    ctx.strokeStyle = sh.color;
    ctx.lineWidth = 3;
    ctx.beginPath();
    sh.pts.forEach((pt, idx) => {
      if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
      else ctx.lineTo(wx(pt.x), wy(pt.y));
    });
    ctx.stroke();

    const px = wx(sh.x);
    const py = wy(sh.y);
    const ang = Math.atan2(-sh.vy, sh.vx);

    // 회전하는 포탄 본체 + 광원 후광
    const gRad = ctx.createRadialGradient(px, py, 1, px, py, 14);
    gRad.addColorStop(0, "#ffffff");
    gRad.addColorStop(0.45, sh.color);
    gRad.addColorStop(1, "transparent");
    ctx.fillStyle = gRad;
    ctx.beginPath(); ctx.arc(px, py, 14, 0, Math.PI * 2); ctx.fill();

    ctx.save();
    ctx.translate(px, py);
    ctx.rotate(ang);
    ctx.fillStyle = "#090d16";
    ctx.strokeStyle = "#fde047";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.ellipse(0, 0, 7, 4.2, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    ctx.restore();

    if (document.getElementById('chkVec').checked) {
      const vs = 1.15;
      drawVectorArrow(px, py, px + sh.vx * vs, py, "#38bdf8", `vx=${sh.vx.toFixed(1)}`);
      drawVectorArrow(px, py, px, py - sh.vy * vs, "#f87171", `vy=${sh.vy.toFixed(1)}`);
    }
    ctx.restore();
  });

  // 10. 충격파 링, 폭발 파티클, 만화풍 데미지 팝업
  rings.forEach((rg) => {
    ctx.save();
    ctx.strokeStyle = rg.color;
    ctx.globalAlpha = Math.max(0, rg.alpha);
    ctx.lineWidth = 3.5;
    ctx.beginPath();
    ctx.arc(wx(rg.x), wy(rg.y), rg.r * SX, 0, Math.PI * 2);
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

  popups.forEach((pp) => {
    ctx.save();
    ctx.globalAlpha = Math.max(0, Math.min(1, pp.life));
    ctx.font = "900 15px 'Pretendard', sans-serif";
    ctx.fillStyle = pp.color;
    ctx.strokeStyle = "#090d16";
    ctx.lineWidth = 3.5;
    ctx.textAlign = "center";
    ctx.strokeText(pp.txt, wx(pp.x), wy(pp.y));
    ctx.fillText(pp.txt, wx(pp.x), wy(pp.y));
    ctx.restore();
  });

  ctx.restore();
}

// ── 키보드 조작 (Space 홀드 충전 발사) ──────────────────────
window.addEventListener('keydown', (e) => {
  if (shells.length > 0 || turn !== 'P1') return;
  if (e.key === 'ArrowLeft') { stepMove(-1); e.preventDefault(); }
  else if (e.key === 'ArrowRight') { stepMove(1); e.preventDefault(); }
  else if (e.key === 'ArrowUp') { nudgeAngle(1); e.preventDefault(); }
  else if (e.key === 'ArrowDown') { nudgeAngle(-1); e.preventDefault(); }
  else if (e.key === ' ' && !charging) {
    charging = true;
    chargeVal = 10.0;
    chargeDir = 1;
    function stepCharge() {
      if (!charging) return;
      chargeVal += chargeDir * 1.15;
      if (chargeVal >= 80.0) { chargeVal = 80.0; chargeDir = -1; }
      if (chargeVal <= 10.0) { chargeVal = 10.0; chargeDir = 1; }
      document.getElementById('slSpeed').value = chargeVal.toFixed(1);
      syncUI();
      chargeRaf = requestAnimationFrame(stepCharge);
    }
    chargeRaf = requestAnimationFrame(stepCharge);
    e.preventDefault();
  }
});

window.addEventListener('keyup', (e) => {
  if (e.key === ' ' && charging) {
    charging = false;
    if (chargeRaf) cancelAnimationFrame(chargeRaf);
    triggerFire('P1');
    e.preventDefault();
  }
});

// 초기 시작
initSkyObjects();
deployTanks();
generateMap();
p1.y = groundAt(p1.x); p2.y = groundAt(p2.x);
p1.slope = slopeAt(p1.x); p2.slope = slopeAt(p2.x);
syncUI();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(HTML_CODE, height=770, scrolling=False)

with st.expander("🎮 물리 포트리스 V2 조작법 & 탄도 물리학 공략", expanded=False):
    st.markdown(
        """
- **포트리스 V2 조작법**:
  - **키보드**: `← / →` 탱크 이동, `↑ / ↓` 포신 각도 조절, **`Space` 키를 길게 눌러 파워 게이지 충전 후 떼면 발사**됩니다!
  - **마우스**: 하단 파워 게이지 바를 직접 클릭하거나 슬라이더로 각도($\\theta$)·속력($v_0$)을 조절한 뒤 **`🔥 FIRE!!`** 버튼을 클릭하세요.
- **포탄 추적 카메라 (`🎥 Follow Cam`)**: 발사 순간 카메라가 포탄을 따라 부드럽게 줌인·트래킹하며, 전체 화면을 고정해서 보고 싶다면 하단 체크박스를 해제할 수 있습니다.
"""
    )
