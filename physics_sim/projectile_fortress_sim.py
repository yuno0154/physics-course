import streamlit as st
import streamlit.components.v1 as components

st.title("🎯 [게임] 물리 포트리스: 포물선 탄도 포격전")
st.caption("발사각(θ)과 초기 속력(v₀)을 조절하여 지형 장애물과 바람을 극복하고 표적·적 탱크를 명중시키는 포물선 운동 시뮬레이션 게임")

HTML_CODE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Pretendard', 'Malgun Gothic', sans-serif; }
  body { background: #0f172a; color: #f8fafc; padding: 12px; user-select: none; }

  .top-bar {
    display: flex; flex-wrap: wrap; gap: 8px; justify-content: space-between; align-items: center;
    background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 10px 14px; margin-bottom: 10px;
  }
  .mode-btns { display: flex; flex-wrap: wrap; gap: 6px; }
  .m-btn {
    background: #0f172a; color: #cbd5e1; border: 1px solid #475569; border-radius: 8px;
    padding: 7px 12px; font-size: 13px; font-weight: 700; cursor: pointer; transition: 0.15s;
  }
  .m-btn:hover { border-color: #60a5fa; color: #fff; }
  .m-btn.active { background: #2563eb; color: #fff; border-color: #60a5fa; box-shadow: 0 0 10px rgba(37,99,235,0.4); }

  .env-group { display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: #cbd5e1; }
  .env-select {
    background: #0f172a; color: #f8fafc; border: 1px solid #475569; border-radius: 6px;
    padding: 5px 8px; font-size: 12.5px; font-weight: 600;
  }

  .canvas-wrap {
    position: relative; background: #0b1120; border: 2px solid #334155; border-radius: 14px;
    overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.45);
  }
  canvas { display: block; width: 100%; height: 470px; }

  .hud-overlay {
    position: absolute; top: 10px; left: 12px; right: 12px;
    display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none;
  }
  .hud-box {
    background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 10px; padding: 8px 12px; font-size: 12.5px; line-height: 1.5; backdrop-filter: blur(4px);
  }
  .wind-badge {
    background: rgba(15, 23, 42, 0.9); border: 1px solid #38bdf8; border-radius: 99px;
    padding: 6px 16px; font-size: 13px; font-weight: 800; color: #38bdf8; text-align: center;
  }
  .banner-msg {
    position: absolute; top: 44%; left: 50%; transform: translate(-50%, -50%);
    background: rgba(15, 23, 42, 0.92); border: 2px solid #facc15; border-radius: 14px;
    padding: 14px 26px; font-size: 18px; font-weight: 800; color: #fde047;
    text-align: center; pointer-events: none; display: none; box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  }

  .ctrl-panel {
    display: grid; grid-template-columns: 1.35fr 1.15fr 1.1fr; gap: 10px; margin-top: 10px;
  }
  @media (max-width: 860px) { .ctrl-panel { grid-template-columns: 1fr; } }

  .card {
    background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 12px 14px;
  }
  .card-title { font-size: 13.5px; font-weight: 800; color: #93c5fd; margin-bottom: 8px; display: flex; justify-content: space-between; }

  .slider-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; font-size: 13px; }
  .slider-row label { width: 88px; font-weight: 700; color: #e2e8f0; }
  .slider-row input[type=range] { flex: 1; accent-color: #3b82f6; cursor: pointer; }
  .val-pill {
    min-width: 74px; text-align: right; font-weight: 800; color: #38bdf8;
    background: #0f172a; padding: 3px 8px; border-radius: 6px; border: 1px solid #334155;
  }

  .btn-row { display: flex; gap: 6px; margin-top: 6px; flex-wrap: wrap; }
  .btn {
    flex: 1; padding: 9px 12px; border-radius: 8px; border: 1px solid #475569;
    background: #0f172a; color: #f8fafc; font-weight: 700; font-size: 13px; cursor: pointer; transition: 0.15s;
  }
  .btn:hover { border-color: #94a3b8; background: #1e293b; }
  .btn-fire {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    border-color: #f87171; color: #fff; font-size: 14.5px; font-weight: 800;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
  }
  .btn-fire:hover { background: linear-gradient(135deg, #f87171 0%, #ef4444 100%); }
  .btn-fire:disabled { opacity: 0.5; cursor: not-allowed; }

  .power-bar-wrap {
    margin-top: 6px; background: #0f172a; border: 1px solid #334155; border-radius: 8px;
    height: 18px; position: relative; overflow: hidden;
  }
  .power-bar-fill {
    height: 100%; width: 0%; background: linear-gradient(90deg, #22c55e 0%, #eab308 60%, #ef4444 100%);
    transition: width 0.03s linear;
  }
  .power-bar-mark {
    position: absolute; top: 0; bottom: 0; width: 3px; background: #fff; display: none;
  }

  .phys-grid {
    display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 12.5px;
  }
  .phys-item {
    background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 6px 9px;
  }
  .phys-item .k { color: #94a3b8; font-size: 11.5px; }
  .phys-item .v { color: #f8fafc; font-weight: 800; font-size: 13.5px; margin-top: 1px; }

  .shot-log {
    max-height: 125px; overflow-y: auto; font-size: 12px; color: #cbd5e1;
    background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 7px 10px; line-height: 1.55;
  }
  .chk-row { display: flex; gap: 12px; font-size: 12.5px; color: #cbd5e1; margin-top: 6px; align-items: center; flex-wrap: wrap; }
  .chk-row label { display: flex; align-items: center; gap: 4px; cursor: pointer; }
</style>
</head>
<body>

<div class="top-bar">
  <div class="mode-btns">
    <button class="m-btn active" onclick="setMission(1)">🎯 미션 1: 평지 정밀 타격</button>
    <button class="m-btn" onclick="setMission(2)">⛰️ 미션 2: 고각 포격 (산 넘기)</button>
    <button class="m-btn" onclick="setMission(3)">🏰 미션 3: 고지대 요새 타격</button>
    <button class="m-btn" onclick="setMission(4)">🌬️ 미션 4: 강풍 속 탄도 보정</button>
    <button class="m-btn" onclick="setMission(5)">⚔️ 실전: AI 탱크 포격 대결</button>
  </div>
  <div class="env-group">
    <span>행성 중력(g):</span>
    <select id="gravSelect" class="env-select" onchange="changeGravity()">
      <option value="9.8">🌍 지구 (g = 9.8 m/s²)</option>
      <option value="3.7">🔴 화성 (g = 3.7 m/s²)</option>
      <option value="1.6">🌙 달 (g = 1.6 m/s²)</option>
    </select>
    <button class="m-btn" onclick="resetStage()">🔄 새 지형/배치</button>
  </div>
</div>

<div class="canvas-wrap">
  <canvas id="gameCanvas" width="1040" height="470"></canvas>
  <div class="hud-overlay">
    <div class="hud-box" id="hudLeft">
      <div><b style="color:#60a5fa;">🟦 내 탱크 (P1)</b> · HP: <span id="p1Hp">100</span>%</div>
      <div>표적까지 수평 거리 <b>Δx = <span id="hudDx">0.0</span> m</b> · 높이차 <b>Δy = <span id="hudDy">0.0</span> m</b></div>
      <div style="font-size:11.5px;color:#94a3b8;" id="missionDesc">미션 1: 포물선 수평 도달거리 공식을 활용해 표적을 명중시키세요!</div>
    </div>
    <div class="wind-badge" id="windBadge">🌬️ 바람 가속도: 0.0 m/s² (무풍)</div>
    <div class="hud-box" id="hudRight" style="text-align:right;">
      <div><b style="color:#f87171;">🟥 표적 / AI 탱크</b> · HP: <span id="p2Hp">100</span>%</div>
      <div>명중 횟수: <b style="color:#facc15;" id="scoreHit">0</b> / 발사: <span id="scoreShot">0</span>회</div>
      <div style="font-size:11.5px;color:#94a3b8;">이전 발사: <span id="lastShotInfo">-</span></div>
    </div>
  </div>
  <div class="banner-msg" id="bannerMsg">🎯 명중!</div>
</div>

<div class="ctrl-panel">
  <!-- 1. 발사 조작 -->
  <div class="card">
    <div class="card-title">
      <span>🎮 포신 각도 · 초기 속력 조작</span>
      <span style="font-size:11.5px;color:#94a3b8;">키보드: ←/→ 이동, ↑/↓ 각도, Space 발사</span>
    </div>
    <div class="slider-row">
      <label>발사각 θ</label>
      <input type="range" id="angleSlider" min="5" max="85" step="1" value="45" oninput="syncControls()">
      <span class="val-pill"><span id="angleVal">45</span>°</span>
    </div>
    <div class="slider-row">
      <label>초기 속력 v₀</label>
      <input type="range" id="speedSlider" min="10" max="80" step="0.5" value="42.0" oninput="syncControls()">
      <span class="val-pill"><span id="speedVal">42.0</span> m/s</span>
    </div>
    <div class="btn-row">
      <button class="btn" onclick="moveTank(-1)">◀ 탱크 좌측 이동</button>
      <button class="btn" onclick="moveTank(1)">탱크 우측 이동 ▶</button>
      <button class="btn" onclick="setComplementaryAngle()" title="같은 속력에서 수평 도달거리가 같은 보각(90°-θ)으로 전환">🔁 보각(90°−θ)</button>
    </div>
    <div class="btn-row" style="margin-top:8px;">
      <button class="btn btn-fire" id="fireBtn" onclick="fireProjectile()">🔥 포탄 발사! (FIRE)</button>
    </div>
    <div class="chk-row">
      <label><input type="checkbox" id="chkVec" checked onchange="drawScene()"> 속도 성분 벡터(vx, vy) 표시</label>
      <label><input type="checkbox" id="chkGuide" onchange="drawScene()"> 📐 초기 궤적 가이드(1초) 표시</label>
      <label><input type="checkbox" id="chkTrail" checked onchange="drawScene()"> 이전 탄도 궤적 남기기</label>
    </div>
  </div>

  <!-- 2. 실시간 물리량 분석 -->
  <div class="card">
    <div class="card-title">
      <span>📐 포물선 운동 실시간 물리량</span>
      <span style="font-size:11.5px;color:#38bdf8;" id="flightTimer">t = 0.00 s</span>
    </div>
    <div class="phys-grid">
      <div class="phys-item">
        <div class="k">초기 수평 속도 v₀x = v₀cosθ</div>
        <div class="v" style="color:#60a5fa;" id="valV0x">29.70 m/s</div>
      </div>
      <div class="phys-item">
        <div class="k">초기 연직 속도 v₀y = v₀sinθ</div>
        <div class="v" style="color:#f87171;" id="valV0y">29.70 m/s</div>
      </div>
      <div class="phys-item">
        <div class="k">이론 최고점 높이 H (평지·무풍)</div>
        <div class="v" id="valTheoH">45.00 m</div>
      </div>
      <div class="phys-item">
        <div class="k">이론 수평 도달거리 R (평지·무풍)</div>
        <div class="v" id="valTheoR">180.00 m</div>
      </div>
      <div class="phys-item">
        <div class="k">현재 포탄 속도 (vx, vy)</div>
        <div class="v" id="valCurV">대기 중</div>
      </div>
      <div class="phys-item">
        <div class="k">탄도 힌트 (현재 θ에서 명중 속력)</div>
        <div class="v" style="color:#facc15;" id="valHintV0">-</div>
      </div>
    </div>
  </div>

  <!-- 3. 탄도 기록 및 물리 해설 -->
  <div class="card">
    <div class="card-title">
      <span>📋 포격 탄도 기록 & 물리 원리</span>
      <button style="background:none;border:none;color:#94a3b8;font-size:11.5px;cursor:pointer;" onclick="clearTrails()">[궤적 지우기]</button>
    </div>
    <div class="shot-log" id="shotLog">
      💡 <b>포트리스 탄도 공식 핵심</b><br>
      • 수평 속도: <b>vx = v₀cosθ</b> (바람 없을 때 등속 운동)<br>
      • 연직 속도: <b>vy = v₀sinθ − gt</b> (등가속도 운동)<br>
      • 평지 수평 도달거리: <b>R = (v₀² sin2θ) / g</b><br>
      • 같은 속력 v₀에서는 <b>θ</b>와 <b>90°−θ</b>의 도달거리가 같습니다!
    </div>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 월드 좌표계: 가로 0 ~ 240 m, 세로 0 ~ 110 m
const WORLD_W = 240.0;
const WORLD_H = 108.0;
const SCALE_X = canvas.width / WORLD_W;
const SCALE_Y = canvas.height / WORLD_H;

function wx(x) { return x * SCALE_X; }
function wy(y) { return canvas.height - (y + 8.0) * SCALE_Y; }

let mission = 1;
let g = 9.8;
let windAx = 0.0; // 수평 바람 가속도 (m/s^2)
let terrain = new Float32Array(canvas.width);

let p1 = { x: 25.0, y: 10.0, angle: 45, speed: 42.0, hp: 100 };
let p2 = { x: 195.0, y: 10.0, angle: 135, speed: 40.0, hp: 100 };

let proj = null;
let animId = null;
let pastTrails = [];
let particles = [];
let hits = 0;
let shots = 0;
let turn = 'P1';

function buildTerrain() {
  const w = canvas.width;
  const baseH = 10.0;
  for (let px = 0; px < w; px++) {
    const x = px / SCALE_X;
    let h = baseH;
    if (mission === 1) {
      // 평지 + 완만한 굴곡
      h = baseH + 1.2 * Math.sin(x * 0.05);
    } else if (mission === 2) {
      // 중앙 높은 산 장애물
      const peak = 42.0 * Math.exp(-Math.pow((x - 115.0) / 26.0, 2));
      h = baseH + peak + 1.5 * Math.sin(x * 0.08);
    } else if (mission === 3) {
      // 우측 고지대 요새 (단차 지형)
      const cliff = 32.0 / (1.0 + Math.exp(-(x - 140.0) / 5.5));
      h = baseH + cliff + 1.0 * Math.sin(x * 0.07);
    } else if (mission === 4) {
      // 바람 + 중간 언덕
      const hill = 18.0 * Math.exp(-Math.pow((x - 118.0) / 30.0, 2));
      h = baseH + hill + 2.0 * Math.sin(x * 0.06);
    } else {
      // 실전 AI 대결: 랜덤 언덕 지형
      const c1 = 105.0 + (Math.random() - 0.5) * 25.0;
      const h1 = 18.0 + Math.random() * 18.0;
      h = baseH + h1 * Math.exp(-Math.pow((x - c1) / 28.0, 2)) + 2.5 * Math.sin(x * 0.06);
    }
    terrain[px] = Math.max(2.0, h);
  }
}

function getGroundY(x) {
  const px = Math.max(0, Math.min(canvas.width - 1, Math.round(x * SCALE_X)));
  return terrain[px];
}

function placeTanks() {
  p1.x = 22.0 + Math.random() * 18.0;
  p2.x = 175.0 + Math.random() * 38.0;
  p1.y = getGroundY(p1.x);
  p2.y = getGroundY(p2.x);
  p1.hp = 100;
  p2.hp = 100;
  turn = 'P1';

  if (mission === 1 || mission === 2 || mission === 3) {
    windAx = 0.0;
  } else {
    windAx = Math.round(((Math.random() * 6.0) - 3.0) * 10) / 10;
    if (Math.abs(windAx) < 0.5) windAx = 1.8;
  }
  updateHUD();
}

function setMission(m) {
  mission = m;
  document.querySelectorAll('.mode-btns .m-btn').forEach((b, idx) => {
    b.classList.toggle('active', idx === m - 1);
  });
  const descMap = {
    1: "미션 1 (평지 타격): 바람이 없습니다. R = (v₀² sin2θ)/g 공식과 보각(90°−θ)을 실험해 보세요!",
    2: "미션 2 (고각 포격): 중앙의 높은 산을 넘기 위해 발사각 θ를 크게 높여 최고점 높이 H를 확보하세요!",
    3: "미션 3 (고지대 요새): 표적이 높은 절벽 위(Δy > 0)에 있습니다. 고도차를 고려해 발사하세요!",
    4: "미션 4 (강풍 탄도 보정): 수평 방향으로 일정한 바람 가속도(a_wind)가 작용합니다!",
    5: "실전 대결 (1P vs AI): 매 턴 바람이 바뀝니다! AI 탱크보다 먼저 상대 HP를 0으로 만드세요!"
  };
  document.getElementById('missionDesc').textContent = descMap[m];
  resetStage();
}

function changeGravity() {
  g = parseFloat(document.getElementById('gravSelect').value);
  syncControls();
  drawScene();
}

function resetStage() {
  if (animId) cancelAnimationFrame(animId);
  proj = null;
  pastTrails = [];
  particles = [];
  buildTerrain();
  placeTanks();
  syncControls();
  drawScene();
}

function clearTrails() {
  pastTrails = [];
  drawScene();
}

function setComplementaryAngle() {
  const cur = parseInt(document.getElementById('angleSlider').value, 10);
  const comp = Math.max(5, Math.min(85, 90 - cur));
  document.getElementById('angleSlider').value = comp;
  syncControls();
}

function moveTank(dir) {
  if (proj || turn !== 'P1') return;
  p1.x = Math.max(10.0, Math.min(85.0, p1.x + dir * 2.5));
  p1.y = getGroundY(p1.x);
  syncControls();
  drawScene();
}

function computeRequiredV0(dx, dy, thetaDeg) {
  const rad = thetaDeg * Math.PI / 180.0;
  const cos = Math.cos(rad);
  const sin = Math.sin(rad);
  // 바람 없을 때: dy = dx * tan(theta) - g * dx^2 / (2 * v0^2 * cos^2(theta))
  const denom = 2.0 * cos * cos * (dx * Math.tan(rad) - dy);
  if (denom <= 0.01) return null;
  const v0 = Math.sqrt((g * dx * dx) / denom);
  if (v0 < 5 || v0 > 120) return null;
  return v0;
}

function syncControls() {
  p1.angle = parseFloat(document.getElementById('angleSlider').value);
  p1.speed = parseFloat(document.getElementById('speedSlider').value);
  document.getElementById('angleVal').textContent = p1.angle.toFixed(0);
  document.getElementById('speedVal').textContent = p1.speed.toFixed(1);

  const rad = p1.angle * Math.PI / 180.0;
  const v0x = p1.speed * Math.cos(rad);
  const v0y = p1.speed * Math.sin(rad);
  const theoH = (v0y * v0y) / (2.0 * g);
  const theoR = (p1.speed * p1.speed * Math.sin(2.0 * rad)) / g;

  document.getElementById('valV0x').textContent = v0x.toFixed(2) + " m/s";
  document.getElementById('valV0y').textContent = v0y.toFixed(2) + " m/s";
  document.getElementById('valTheoH').textContent = theoH.toFixed(2) + " m";
  document.getElementById('valTheoR').textContent = theoR.toFixed(1) + " m";

  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  const reqV0 = computeRequiredV0(dx, dy, p1.angle);
  if (reqV0 !== null) {
    document.getElementById('valHintV0').textContent =
      windAx === 0 ? `약 ${reqV0.toFixed(1)} m/s` : `무풍 기준 ${reqV0.toFixed(1)} m/s`;
  } else {
    document.getElementById('valHintV0').textContent = "각도 θ를 더 높이세요";
  }

  updateHUD();
  if (!proj) drawScene();
}

function updateHUD() {
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  document.getElementById('hudDx').textContent = dx.toFixed(1);
  document.getElementById('hudDy').textContent = (dy >= 0 ? "+" : "") + dy.toFixed(1);
  document.getElementById('p1Hp').textContent = Math.max(0, Math.round(p1.hp));
  document.getElementById('p2Hp').textContent = Math.max(0, Math.round(p2.hp));
  document.getElementById('scoreHit').textContent = hits;
  document.getElementById('scoreShot').textContent = shots;

  const wb = document.getElementById('windBadge');
  if (Math.abs(windAx) < 0.05) {
    wb.textContent = "🌬️ 바람 가속도: 0.0 m/s² (무풍)";
    wb.style.borderColor = "#94a3b8";
    wb.style.color = "#e2e8f0";
  } else if (windAx > 0) {
    wb.textContent = `🌬️ 순풍 (우측 ▶) +${windAx.toFixed(1)} m/s²`;
    wb.style.borderColor = "#38bdf8";
    wb.style.color = "#38bdf8";
  } else {
    wb.textContent = `🌬️ 역풍 (◀ 좌측) ${windAx.toFixed(1)} m/s²`;
    wb.style.borderColor = "#f472b6";
    wb.style.color = "#f472b6";
  }
}

function showBanner(msg, color = "#fde047") {
  const b = document.getElementById('bannerMsg');
  b.textContent = msg;
  b.style.borderColor = color;
  b.style.color = color;
  b.style.display = "block";
  setTimeout(() => { b.style.display = "none"; }, 1900);
}

function craterTerrain(hitX, radiusM) {
  const centerPx = Math.round(hitX * SCALE_X);
  const radPx = Math.round(radiusM * SCALE_X);
  for (let px = Math.max(0, centerPx - radPx); px <= Math.min(canvas.width - 1, centerPx + radPx); px++) {
    const dist = Math.abs(px - centerPx) / radPx;
    const depth = (1.0 - dist * dist) * (radiusM * 0.65);
    terrain[px] = Math.max(1.5, terrain[px] - depth);
  }
  p1.y = getGroundY(p1.x);
  p2.y = getGroundY(p2.x);
}

function spawnExplosion(x, y, color) {
  for (let i = 0; i < 28; i++) {
    const ang = Math.random() * Math.PI * 2;
    const spd = 4 + Math.random() * 18;
    particles.push({
      x, y,
      vx: Math.cos(ang) * spd,
      vy: Math.sin(ang) * spd,
      life: 1.0,
      color: i % 2 === 0 ? color : "#facc15"
    });
  }
}

function fireProjectile(owner = 'P1') {
  if (proj) return;
  document.getElementById('fireBtn').disabled = true;

  let shooter = owner === 'P1' ? p1 : p2;
  let angDeg = owner === 'P1' ? p1.angle : p2.angle;
  let spd = owner === 'P1' ? p1.speed : p2.speed;
  const rad = angDeg * Math.PI / 180.0;
  const vx0 = spd * Math.cos(rad);
  const vy0 = spd * Math.sin(rad);

  if (owner === 'P1') {
    shots++;
    document.getElementById('lastShotInfo').textContent = `θ=${angDeg}°, v₀=${spd.toFixed(1)}m/s`;
  }

  const startX = shooter.x + Math.cos(rad) * 2.2;
  const startY = shooter.y + 1.5 + Math.sin(rad) * 2.2;

  proj = {
    owner,
    x0: startX, y0: startY,
    x: startX, y: startY,
    vx0, vy0,
    vx: vx0, vy: vy0,
    t: 0.0,
    maxY: startY,
    trail: [{ x: startX, y: startY }]
  };

  let lastTime = performance.now();

  function step(now) {
    const dtReal = Math.min(0.04, (now - lastTime) / 1000.0);
    lastTime = now;
    const dtSim = dtReal * 2.1; // 물리 시간 배속

    if (proj) {
      proj.t += dtSim;
      proj.x = proj.x0 + proj.vx0 * proj.t + 0.5 * windAx * proj.t * proj.t;
      proj.y = proj.y0 + proj.vy0 * proj.t - 0.5 * g * proj.t * proj.t;
      proj.vx = proj.vx0 + windAx * proj.t;
      proj.vy = proj.vy0 - g * proj.t;
      if (proj.y > proj.maxY) proj.maxY = proj.y;
      proj.trail.push({ x: proj.x, y: proj.y });

      document.getElementById('flightTimer').textContent = `t = ${proj.t.toFixed(2)} s`;
      document.getElementById('valCurV').textContent = `(${proj.vx.toFixed(1)}, ${proj.vy.toFixed(1)}) m/s`;

      // 충돌 판정
      const target = proj.owner === 'P1' ? p2 : p1;
      const distTarget = Math.hypot(proj.x - target.x, proj.y - (target.y + 1.2));
      const groundY = getGroundY(proj.x);

      if (distTarget <= 4.2 || proj.y <= groundY || proj.x < 0 || proj.x > WORLD_W) {
        const hitX = proj.x;
        const hitY = Math.max(proj.y, groundY);
        const totalDx = Math.abs(hitX - proj.x0);
        const maxH = proj.maxY - proj.y0;

        if (document.getElementById('chkTrail').checked) {
          pastTrails.push({
            owner: proj.owner,
            points: proj.trail,
            label: `${proj.owner === 'P1' ? p1.angle + '°/' + p1.speed.toFixed(1) + 'm/s' : 'AI'}`
          });
          if (pastTrails.length > 5) pastTrails.shift();
        }

        // 데미지 및 명중 처리
        const dP1 = Math.hypot(hitX - p1.x, hitY - p1.y);
        const dP2 = Math.hypot(hitX - p2.x, hitY - p2.y);

        if (dP2 < 7.5 && proj.owner === 'P1') {
          const dmg = dP2 < 3.8 ? 50 : Math.round(35 * (1 - dP2 / 8.0));
          p2.hp = Math.max(0, p2.hp - dmg);
          hits++;
          spawnExplosion(hitX, hitY, "#ef4444");
          craterTerrain(hitX, 4.5);
          showBanner(dP2 < 3.8 ? `🎯 정밀 직격 명중! (-${dmg} HP)` : `💥 폭발 반경 명중! (-${dmg} HP)`, "#4ade80");
          logShot(`✅ <b>명중!</b> (θ=${p1.angle}°, v₀=${p1.speed.toFixed(1)}m/s) → 비행시간 ${proj.t.toFixed(2)}s, 수평이동 ${totalDx.toFixed(1)}m, 최고높이 ${maxH.toFixed(1)}m`);
        } else if (dP1 < 7.5 && proj.owner === 'AI') {
          const dmg = dP1 < 3.8 ? 40 : Math.round(25 * (1 - dP1 / 8.0));
          p1.hp = Math.max(0, p1.hp - dmg);
          spawnExplosion(hitX, hitY, "#f97316");
          craterTerrain(hitX, 4.5);
          showBanner(`⚠️ AI 포탄 피격! (-${dmg} HP)`, "#f87171");
        } else {
          spawnExplosion(hitX, hitY, "#94a3b8");
          craterTerrain(hitX, 3.8);
          if (proj.owner === 'P1') {
            const errX = hitX - p2.x;
            const guide = errX < 0 ? `${Math.abs(errX).toFixed(1)}m 짧음` : `${errX.toFixed(1)}m 초과`;
            showBanner(`💨 빗나감 (${guide})`, "#fbbf24");
            logShot(`⚪ 탄착 (${guide}) | θ=${p1.angle}°, v₀=${p1.speed.toFixed(1)}m/s → 이동 ${totalDx.toFixed(1)}m (t=${proj.t.toFixed(2)}s)`);
          }
        }

        const finishedOwner = proj.owner;
        proj = null;
        updateHUD();

        // 승패 또는 다음 턴 진행
        if (p2.hp <= 0) {
          setTimeout(() => {
            showBanner("🏆 표적 완전 격파! 새 표적이 배치됩니다.", "#facc15");
            placeTanks();
            syncControls();
            document.getElementById('fireBtn').disabled = false;
          }, 1200);
        } else if (p1.hp <= 0) {
          setTimeout(() => {
            showBanner("💀 내 탱크 파손! 스테이지를 재시작합니다.", "#f87171");
            resetStage();
            document.getElementById('fireBtn').disabled = false;
          }, 1400);
        } else if (mission === 5 && finishedOwner === 'P1') {
          turn = 'AI';
          setTimeout(aiFireTurn, 900);
        } else {
          turn = 'P1';
          if (mission === 4 || mission === 5) {
            windAx = Math.round(((Math.random() * 6.0) - 3.0) * 10) / 10;
          }
          syncControls();
          document.getElementById('fireBtn').disabled = false;
        }
      }
    }

    // 파티클 업데이트
    for (let i = particles.length - 1; i >= 0; i--) {
      const pt = particles[i];
      pt.x += pt.vx * dtReal;
      pt.y += pt.vy * dtReal;
      pt.vy -= g * dtReal * 0.6;
      pt.life -= dtReal * 1.8;
      if (pt.life <= 0) particles.splice(i, 1);
    }

    drawScene();
    if (proj || particles.length > 0) {
      animId = requestAnimationFrame(step);
    }
  }

  animId = requestAnimationFrame(step);
}

function aiFireTurn() {
  showBanner("🤖 AI 탱크가 탄도를 계산하여 발사합니다...", "#f87171");
  const dx = p1.x - p2.x; // 음수 (좌측 방향)
  const dy = p1.y - p2.y;
  const aiAngle = 128; // 좌상단 방향 (180 - 52도)
  const rad = aiAngle * Math.PI / 180.0;
  const absDx = Math.abs(dx);
  const reqV0 = computeRequiredV0(absDx, dy, 180 - aiAngle) || 42.0;
  // 바람 보정 + 약간의 오차
  const windComp = -windAx * 1.4;
  p2.angle = aiAngle;
  p2.speed = Math.max(15, Math.min(75, reqV0 + windComp + (Math.random() - 0.5) * 4.5));
  setTimeout(() => { fireProjectile('AI'); }, 700);
}

function logShot(html) {
  const box = document.getElementById('shotLog');
  box.innerHTML = `<div style="margin-bottom:4px;border-bottom:1px dashed #334155;padding-bottom:3px;">${html}</div>` + box.innerHTML;
}

function drawTank(x, y, angleDeg, color, label, hp) {
  const cx = wx(x);
  const cy = wy(y);

  ctx.save();
  ctx.translate(cx, cy);

  // 포신
  const rad = angleDeg * Math.PI / 180.0;
  ctx.strokeStyle = "#e2e8f0";
  ctx.lineWidth = 5;
  ctx.lineCap = "round";
  ctx.beginPath();
  ctx.moveTo(0, -8);
  ctx.lineTo(Math.cos(rad) * 24, -8 - Math.sin(rad) * 24);
  ctx.stroke();

  // 몸체 및 포탑
  ctx.fillStyle = color;
  ctx.beginPath();
  ctx.roundRect(-16, -10, 32, 11, 5);
  ctx.fill();
  ctx.beginPath();
  ctx.arc(0, -10, 9, Math.PI, 0);
  ctx.fill();

  // 무한궤도 바퀴
  ctx.fillStyle = "#1e293b";
  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.roundRect(-18, -2, 36, 6, 3);
  ctx.fill();
  ctx.stroke();

  // HP 바
  ctx.fillStyle = "rgba(15,23,42,0.85)";
  ctx.fillRect(-20, -32, 40, 6);
  ctx.fillStyle = hp > 40 ? "#22c55e" : "#ef4444";
  ctx.fillRect(-19, -31, 38 * Math.max(0, hp) / 100, 4);

  // 라벨
  ctx.fillStyle = "#f8fafc";
  ctx.font = "bold 11px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(label, 0, -36);

  ctx.restore();
}

function drawArrow(x1, y1, x2, y2, color, label) {
  const head = 7;
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
    ctx.font = "bold 11px sans-serif";
    ctx.fillText(label, x2 + 6, y2 - 4);
  }
  ctx.restore();
}

function drawScene() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 배경 하늘 그라데이션 & 격자(20m 간격)
  const sky = ctx.createLinearGradient(0, 0, 0, canvas.height);
  sky.addColorStop(0, "#090d16");
  sky.addColorStop(1, "#1e293b");
  ctx.fillStyle = sky;
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  ctx.strokeStyle = "rgba(148, 163, 184, 0.12)";
  ctx.lineWidth = 1;
  ctx.fillStyle = "rgba(148, 163, 184, 0.45)";
  ctx.font = "10px sans-serif";
  for (let xm = 0; xm <= WORLD_W; xm += 20) {
    const px = wx(xm);
    ctx.beginPath();
    ctx.moveTo(px, 0);
    ctx.lineTo(px, canvas.height);
    ctx.stroke();
    ctx.fillText(`${xm}m`, px + 3, canvas.height - 6);
  }
  for (let ym = 0; ym <= 100; ym += 20) {
    const py = wy(ym);
    ctx.beginPath();
    ctx.moveTo(0, py);
    ctx.lineTo(canvas.width, py);
    ctx.stroke();
    ctx.fillText(`${ym}m`, 4, py - 3);
  }

  // 지형 렌더링
  const terrGrad = ctx.createLinearGradient(0, wy(50), 0, canvas.height);
  terrGrad.addColorStop(0, "#334155");
  terrGrad.addColorStop(1, "#0f172a");
  ctx.fillStyle = terrGrad;
  ctx.beginPath();
  ctx.moveTo(0, canvas.height);
  for (let px = 0; px < canvas.width; px++) {
    ctx.lineTo(px, wy(terrain[px]));
  }
  ctx.lineTo(canvas.width, canvas.height);
  ctx.closePath();
  ctx.fill();

  ctx.strokeStyle = "#4ade80";
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let px = 0; px < canvas.width; px++) {
    if (px === 0) ctx.moveTo(px, wy(terrain[px]));
    else ctx.lineTo(px, wy(terrain[px]));
  }
  ctx.stroke();

  // 이전 궤적 그리기
  if (document.getElementById('chkTrail').checked) {
    pastTrails.forEach((tr) => {
      ctx.save();
      ctx.strokeStyle = tr.owner === 'P1' ? "rgba(96, 165, 250, 0.45)" : "rgba(248, 113, 113, 0.45)";
      ctx.setLineDash([4, 4]);
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      tr.points.forEach((pt, idx) => {
        if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
        else ctx.lineTo(wx(pt.x), wy(pt.y));
      });
      ctx.stroke();
      const last = tr.points[tr.points.length - 1];
      if (last) {
        ctx.fillStyle = "rgba(226, 232, 240, 0.75)";
        ctx.font = "11px sans-serif";
        ctx.fillText(tr.label, wx(last.x) - 18, wy(last.y) - 8);
      }
      ctx.restore();
    });
  }

  // 초기 1.2초 가이드 궤적
  if (document.getElementById('chkGuide').checked && !proj) {
    const rad = p1.angle * Math.PI / 180.0;
    const vx0 = p1.speed * Math.cos(rad);
    const vy0 = p1.speed * Math.sin(rad);
    const sx = p1.x + Math.cos(rad) * 2.2;
    const sy = p1.y + 1.5 + Math.sin(rad) * 2.2;
    ctx.save();
    ctx.fillStyle = "rgba(250, 204, 21, 0.75)";
    for (let t = 0.1; t <= 1.2; t += 0.12) {
      const gx = sx + vx0 * t + 0.5 * windAx * t * t;
      const gy = sy + vy0 * t - 0.5 * g * t * t;
      ctx.beginPath();
      ctx.arc(wx(gx), wy(gy), 2.5, 0, Math.PI * 2);
      ctx.fill();
    }
    ctx.restore();
  }

  // 탱크 그리기
  drawTank(p1.x, p1.y, p1.angle, "#3b82f6", `P1 (${p1.angle}°)`, p1.hp);
  drawTank(p2.x, p2.y, p2.angle, "#ef4444", mission === 5 ? "AI 탱크" : "표적 요새", p2.hp);

  // 발사 전 초기 속도 성분 벡터 표시
  if (!proj && document.getElementById('chkVec').checked) {
    const rad = p1.angle * Math.PI / 180.0;
    const vx0 = p1.speed * Math.cos(rad);
    const vy0 = p1.speed * Math.sin(rad);
    const ox = wx(p1.x);
    const oy = wy(p1.y + 2.0);
    const vScale = 1.3;
    drawArrow(ox, oy, ox + vx0 * vScale, oy, "#60a5fa", `v₀x=${vx0.toFixed(1)}`);
    drawArrow(ox, oy, ox, oy - vy0 * vScale, "#f87171", `v₀y=${vy0.toFixed(1)}`);
    drawArrow(ox, oy, ox + vx0 * vScale, oy - vy0 * vScale, "#4ade80", `v₀=${p1.speed.toFixed(1)}`);
  }

  // 비행 중인 포탄 및 실시간 속도 벡터
  if (proj) {
    ctx.save();
    ctx.strokeStyle = "#facc15";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    proj.trail.forEach((pt, idx) => {
      if (idx === 0) ctx.moveTo(wx(pt.x), wy(pt.y));
      else ctx.lineTo(wx(pt.x), wy(pt.y));
    });
    ctx.stroke();

    const px = wx(proj.x);
    const py = wy(proj.y);
    ctx.fillStyle = "#fde047";
    ctx.beginPath();
    ctx.arc(px, py, 5.5, 0, Math.PI * 2);
    ctx.fill();

    if (document.getElementById('chkVec').checked) {
      const vScale = 1.2;
      drawArrow(px, py, px + proj.vx * vScale, py, "#60a5fa", `vx=${proj.vx.toFixed(1)}`);
      drawArrow(px, py, px, py - proj.vy * vScale, "#f87171", `vy=${proj.vy.toFixed(1)}`);
    }
    ctx.restore();
  }

  // 폭발 파티클
  particles.forEach((pt) => {
    ctx.save();
    ctx.globalAlpha = Math.max(0, pt.life);
    ctx.fillStyle = pt.color;
    ctx.beginPath();
    ctx.arc(wx(pt.x), wy(pt.y), 4.0, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  });
}

// 키보드 단축키 지원
window.addEventListener('keydown', (e) => {
  if (proj || turn !== 'P1') return;
  if (e.key === 'ArrowLeft') { moveTank(-1); e.preventDefault(); }
  else if (e.key === 'ArrowRight') { moveTank(1); e.preventDefault(); }
  else if (e.key === 'ArrowUp') {
    document.getElementById('angleSlider').value = Math.min(85, p1.angle + 1);
    syncControls();
    e.preventDefault();
  } else if (e.key === 'ArrowDown') {
    document.getElementById('angleSlider').value = Math.max(5, p1.angle - 1);
    syncControls();
    e.preventDefault();
  } else if (e.key === ' ') {
    fireProjectile('P1');
    e.preventDefault();
  }
});

buildTerrain();
placeTanks();
syncControls();
drawScene();
</script>
</body>
</html>
"""

components.html(HTML_CODE, height=820, scrolling=False)

with st.expander("📘 물리 포트리스 핵심 공식 & 공략 가이드", expanded=True):
    st.markdown(
        """
- **수평·연직 운동의 독립성**: 발사된 포탄의 초기 속도 $\\vec{v}_0$는 수평 성분 $v_{0x} = v_0\\cos\\theta$와 연직 성분 $v_{0y} = v_0\\sin\\theta$로 분해됩니다.
- **미션 1 (평지 타격)**: 표적까지의 수평 거리 $\\Delta x$가 주어질 때, $R = \\dfrac{v_0^2 \\sin 2\\theta}{g}$ 이므로 필요한 초기 속력은 $v_0 = \\sqrt{\\dfrac{g \\cdot \\Delta x}{\\sin 2\\theta}}$ 입니다. 또한 같은 속력 $v_0$에서는 발사각 $\\theta$와 **보각($90^\\circ - \\theta$)**의 수평 도달거리가 같습니다.
- **미션 2 (산 넘기 고각 포격)**: 중앙의 높은 산을 넘으려면 최고점 높이 $H = \\dfrac{(v_0 \\sin\\theta)^2}{2g}$가 산 정상보다 높아야 하므로 발사각 $\\theta$를 $60^\\circ$ 이상으로 높여서 포격해 보세요.
- **미션 3 (고지대 요새)**: 높이차 $\\Delta y > 0$인 지형에서는 $\\Delta y = \\Delta x \\tan\\theta - \\dfrac{g(\\Delta x)^2}{2 v_0^2 \\cos^2\\theta}$ 관계를 만족해야 합니다.
"""
    )
