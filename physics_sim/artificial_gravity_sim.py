import streamlit as st
import streamlit.components.v1 as components

def show():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #010409 0%, #0d1117 100%);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 16px; padding: 24px; margin-bottom: 20px;">
        <h2 style="color: #38bdf8; font-size: 1.4rem; margin: 0 0 8px 0; font-weight: 800;">
            🚀 우주정거장과 인공중력 (Artificial Gravity)
        </h2>
        <p style="color: #94a3b8; margin: 0; font-size: 0.9rem; line-height: 1.6;">
            회전하는 우주정거장에서 발생하는 <strong style="color:#10b981">원심력(가상력)</strong>이 
            어떻게 <strong style="color:#f59e0b">인공중력</strong>을 만드는지 세 가지 관점(시점)에서 탐구합니다.<br>
            관성계(외부에서 바라볼 때)와 비관성계(내부 회전좌표계) 사이의 차이를 비교하세요.
        </p>
    </div>
    """, unsafe_allow_html=True)

    html_content = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>우주정거장 인공중력 실험실</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&family=Orbitron:wght@400;900&display=swap');

        :root {
            --space-bg: #010409;
            --accent-blue: #38bdf8;
            --accent-emerald: #10b981;
            --danger-red: #ef4444;
            --panel-bg: rgba(10, 15, 25, 0.97);
            --gold: #f59e0b;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--space-bg);
            color: #f8fafc;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .font-orb { font-family: 'Orbitron', sans-serif; }
        .font-mono { font-family: 'JetBrains Mono', monospace; }

        /* ── 스캔라인 ── */
        @keyframes scan { from { top:-2px; } to { top:100%; } }
        .scanline {
            position: fixed; left:0; width: 100%; height: 2px;
            background: rgba(56,189,248,0.06);
            z-index: 100; pointer-events: none;
            animation: scan 14s linear infinite;
        }

        /* ── 헤더 ── */
        header {
            height: 52px; flex-shrink: 0;
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 20px;
            background: var(--panel-bg);
            border-bottom: 1px solid rgba(56,189,248,0.12);
            z-index: 20;
        }
        .hdr-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 0.85rem; font-weight: 900;
            color: var(--accent-blue);
            letter-spacing: 0.18em; text-transform: uppercase;
        }
        .hdr-sub { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #475569; margin-top: 2px; }
        .status-dot {
            display: inline-block; width: 7px; height: 7px;
            border-radius: 50%; background: var(--accent-emerald);
            box-shadow: 0 0 8px var(--accent-emerald);
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse { 0%,100%{ opacity:1; } 50%{ opacity:0.3; } }

        /* ── 본문 레이아웃 ── */
        main { flex-grow: 1; display: flex; overflow: hidden; }

        /* ── 사이드바 ── */
        aside {
            width: 268px; flex-shrink: 0;
            background: var(--panel-bg);
            border-right: 1px solid rgba(255,255,255,0.05);
            padding: 16px; overflow-y: auto;
            display: flex; flex-direction: column; gap: 16px;
        }

        .section-label {
            font-size: 0.6rem; font-weight: 900; letter-spacing: 0.2em;
            text-transform: uppercase; color: #475569; margin-bottom: 8px;
        }

        /* 모드 버튼 */
        .btn-mode {
            width: 100%; padding: 11px 14px;
            text-align: left; border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.06);
            background: rgba(255,255,255,0.03);
            color: #94a3b8; font-size: 0.7rem; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 4px;
        }
        .btn-mode:hover { background: rgba(56,189,248,0.1); color: #f8fafc; }
        .btn-mode.active {
            background: var(--accent-blue); color: #000;
            box-shadow: 0 0 24px rgba(56,189,248,0.5);
            border-color: transparent;
        }

        /* 슬라이더 */
        .slider-row { margin-bottom: 14px; }
        .slider-header {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.68rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;
        }
        .slider-val { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; }

        input[type="range"] {
            -webkit-appearance: none;
            width: 100%; height: 4px;
            border-radius: 2px; background: #1e293b;
        }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 14px; height: 14px;
            background: #f8fafc; border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 0 10px var(--accent-blue);
        }

        /* G-Force 카드 */
        .gforce-card {
            background: rgba(16,185,129,0.08);
            border: 1px solid rgba(16,185,129,0.25);
            border-radius: 12px; padding: 14px;
        }
        .gforce-label {
            font-size: 0.6rem; color: var(--accent-emerald);
            font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em;
        }
        .gforce-val {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.6rem; color: var(--accent-emerald);
            font-weight: 900; line-height: 1;
        }
        .gforce-bar-track {
            height: 4px; background: rgba(255,255,255,0.06);
            border-radius: 2px; overflow: hidden; margin-top: 8px;
        }
        .gforce-bar-fill {
            height: 100%; background: var(--accent-emerald);
            transition: width 0.3s ease;
        }

        /* 물리 데이터 카드 */
        .data-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 12px; padding: 12px;
        }
        .data-row {
            display: flex; justify-content: space-between; align-items: center;
            padding: 5px 0; border-bottom: 1px solid rgba(255,255,255,0.04);
            font-size: 0.68rem;
        }
        .data-row:last-child { border-bottom: none; }
        .data-key { color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .data-val { font-family: 'JetBrains Mono', monospace; color: #e2e8f0; }

        /* 하단 범례 */
        .legend {
            position: absolute; bottom: 16px; left: 50%;
            transform: translateX(-50%);
            background: var(--panel-bg);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 999px; padding: 8px 20px;
            display: flex; align-items: center; gap: 20px;
            font-size: 0.68rem; font-weight: 700;
            white-space: nowrap; z-index: 10;
        }
        .legend-dot {
            width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }

        /* 체중계 창 */
        .scale-window {
            position: absolute; top: 16px; right: 16px;
            width: 220px;
            background: var(--panel-bg);
            border: 1px solid rgba(255,255,255,0.08);
            border-top: 3px solid var(--accent-emerald);
            border-radius: 14px; padding: 16px;
            z-index: 10;
        }
        .scale-title {
            font-size: 0.6rem; color: var(--accent-emerald);
            font-weight: 900; text-transform: uppercase; letter-spacing: 0.15em;
        }
        .scale-display {
            background: #000; border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.06);
            text-align: center; padding: 14px 8px; margin: 10px 0;
        }
        .scale-num {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.2rem; font-weight: 900; color: #fff;
            line-height: 1;
        }
        .scale-unit { font-size: 0.65rem; color: #64748b; font-weight: 700; margin-top: 4px; }

        canvas {
            display: block; width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, #060d1a 0%, #000 100%);
        }

        /* 설명 텍스트 박스 */
        .physics-tip {
            background: rgba(245,158,11,0.07);
            border: 1px solid rgba(245,158,11,0.2);
            border-left: 3px solid var(--gold);
            border-radius: 8px; padding: 10px 12px;
            font-size: 0.68rem; color: #fbbf24;
            line-height: 1.6;
        }
    </style>
</head>
<body>
<div class="scanline"></div>

<!-- 헤더 -->
<header>
    <div>
        <div class="hdr-title">우주정거장 인공중력 실험실</div>
        <div class="hdr-sub">
            <span class="status-dot" style="margin-right:5px;"></span>
            ARTIFICIAL GRAVITY LAB · NON-INERTIAL FRAME EXPLORER
        </div>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#475569;" id="coordDisp">
        COORDS: — , —
    </div>
</header>

<main>
    <!-- ── 사이드바 ── -->
    <aside>
        <!-- 관점 선택 -->
        <div>
            <div class="section-label">관측 시점 (Viewing Mode)</div>
            <button class="btn-mode active" id="modeExt">🛸 01. 외부 원경 (Cinematic)</button>
            <button class="btn-mode" id="modeTop">🔭 02. 관성계 (Inertial Frame)</button>
            <button class="btn-mode" id="modeInt">🧑‍🚀 03. 비관성계 (Rotating Frame)</button>
        </div>

        <!-- 엔지니어링 스펙 -->
        <div>
            <div class="section-label">우주정거장 설계 변수</div>
            <div class="data-card" style="gap:0;">
                <div class="slider-row" style="margin-bottom:8px;">
                    <div class="slider-header">
                        <span>반지름 (r)</span>
                        <span class="slider-val" style="color:var(--accent-blue);" id="rLabel">100 m</span>
                    </div>
                    <input type="range" id="rSlider" min="50" max="250" value="100">
                </div>
                <div class="slider-row" style="margin-bottom:0;">
                    <div class="slider-header">
                        <span>각속도 (ω)</span>
                        <span class="slider-val" style="color:var(--accent-emerald);" id="wLabel">0.31 rad/s</span>
                    </div>
                    <input type="range" id="wSlider" min="0" max="1.5" step="0.01" value="0.31">
                </div>
            </div>
        </div>

        <!-- G-Force -->
        <div class="gforce-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div class="gforce-label">G-Force</div>
                <div class="gforce-val" id="gforceVal">0.00G</div>
            </div>
            <div class="gforce-bar-track">
                <div class="gforce-bar-fill" id="gforceBar" style="width:0%"></div>
            </div>
        </div>

        <!-- 물리 데이터 -->
        <div>
            <div class="section-label">실시간 물리 데이터</div>
            <div class="data-card">
                <div class="data-row">
                    <span class="data-key">원심가속도</span>
                    <span class="data-val" id="accelVal">0.00 m/s²</span>
                </div>
                <div class="data-row">
                    <span class="data-key">선속도 (v=rω)</span>
                    <span class="data-val" id="velVal">0.00 m/s</span>
                </div>
                <div class="data-row">
                    <span class="data-key">주기 (T=2π/ω)</span>
                    <span class="data-val" id="periodVal">∞</span>
                </div>
                <div class="data-row">
                    <span class="data-key">원심력 (70kg)</span>
                    <span class="data-val" id="forceVal">0.0 N</span>
                </div>
            </div>
        </div>

        <!-- 물리 원리 팁 -->
        <div class="physics-tip" id="physTip">
            💡 외부 관성계: 우주인은 실제로 원운동하며, 바닥의 수직항력이 구심력 역할을 합니다.
        </div>
    </aside>

    <!-- ── 캔버스 영역 ── -->
    <div style="flex-grow:1; position:relative; overflow:hidden;">
        <canvas id="canvas"></canvas>

        <!-- 체중계 창 -->
        <div class="scale-window">
            <div class="scale-title">Weight Scale Readout</div>
            <div class="scale-display">
                <div class="scale-num" id="scaleNum">0.0</div>
                <div class="scale-unit">뉴턴 (N)</div>
            </div>
            <div class="data-card" style="padding:8px 10px;">
                <div class="data-row">
                    <span class="data-key">질량</span>
                    <span class="data-val">70.0 kg</span>
                </div>
                <div class="data-row">
                    <span class="data-key">환산 중력</span>
                    <span class="data-val" style="color:var(--accent-emerald);" id="effG">0.00 G</span>
                </div>
            </div>
        </div>

        <!-- 하단 범례 -->
        <div class="legend">
            <div class="legend-item">
                <div class="legend-dot" style="background:#ef4444; box-shadow:0 0 6px #ef4444;"></div>
                수직항력 / 바닥반력 (N)
            </div>
            <div class="legend-item">
                <div class="legend-dot" style="background:#10b981; box-shadow:0 0 6px #10b981;"></div>
                원심력 F<sub>cf</sub> (비관성계 가상력)
            </div>
            <span style="color:#475569; padding-left:12px; border-left:1px solid rgba(255,255,255,0.08);" id="legendNote">
                가장 바깥쪽 호(선체)가 거주 공간의 바닥입니다
            </span>
        </div>
    </div>
</main>

<script>
/***********************************************
 *  우주정거장 인공중력 시뮬레이션
 *  ✦ 내부(비관성계) 시점 핵심 로직:
 *    - 선체(우주정거장) 구조물 = 고정 (회전 없음)
 *    - 배경(별, 지구)만 -angle 로 반대 방향 회전
 *    - 비행사는 바닥 중앙(화면 하단)에 고정
 ***********************************************/

const canvas  = document.getElementById('canvas');
const ctx     = canvas.getContext('2d');

// UI 요소
const rSlider    = document.getElementById('rSlider');
const wSlider    = document.getElementById('wSlider');
const rLabel     = document.getElementById('rLabel');
const wLabel     = document.getElementById('wLabel');
const gforceVal  = document.getElementById('gforceVal');
const gforceBar  = document.getElementById('gforceBar');
const accelVal   = document.getElementById('accelVal');
const velVal     = document.getElementById('velVal');
const periodVal  = document.getElementById('periodVal');
const forceVal   = document.getElementById('forceVal');
const scaleNum   = document.getElementById('scaleNum');
const effG       = document.getElementById('effG');
const coordDisp  = document.getElementById('coordDisp');
const physTip    = document.getElementById('physTip');
const legendNote = document.getElementById('legendNote');

// 상태 변수
let r           = 100;      // 반지름 (m)
let w           = 0.31;     // 각속도 (rad/s)
let angle       = 0;        // 누적 회전각
let earthAngle  = 0;        // 지구 자전각
let mode        = 'EXTERNAL';
const mass      = 70;       // kg

// 별 배열
let stars = [];
function initStars() {
    stars = [];
    for (let i = 0; i < 500; i++) {
        stars.push({
            x: (Math.random() - 0.5) * 5000,
            y: (Math.random() - 0.5) * 5000,
            size: Math.random() * 1.8 + 0.2,
            phase: Math.random() * Math.PI * 2
        });
    }
}

// 캔버스 리사이징
function resize() {
    canvas.width  = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
}
window.addEventListener('resize', resize);
resize();
initStars();

// ── 모드 전환 ──
const modeButtons = { EXTERNAL:'modeExt', TOP:'modeTop', INTERNAL:'modeInt' };
const tipMessages = {
    EXTERNAL: '💡 외부 원경: 우주정거장이 우주 공간에서 회전하는 모습을 외부에서 바라봅니다.',
    TOP:      '💡 관성계(외부 시점): 우주인은 실제로 원운동합니다. 바닥의 수직항력(N)이 구심력 역할을 합니다.',
    INTERNAL: '💡 비관성계(내부 시점): 우주정거장 내부에서는 선체가 고정되어 있고, 우주(창문 밖)만 회전하는 것처럼 느껴집니다. 원심력(가상력)이 아래쪽으로 작용하여 중력처럼 느껴집니다.'
};
const legendMessages = {
    EXTERNAL: '실제 우주에서 회전하는 우주정거장의 모습',
    TOP:      '관성계: 우주인은 실제로 원운동 중',
    INTERNAL: '비관성계: 우주선은 고정, 창 밖 배경만 회전'
};

function setMode(m) {
    mode = m;
    Object.entries(modeButtons).forEach(([k,id]) => {
        document.getElementById(id).classList.toggle('active', k === m);
    });
    physTip.textContent    = tipMessages[m] ?? '';
    legendNote.textContent = legendMessages[m] ?? '';
}
document.getElementById('modeExt').onclick = () => setMode('EXTERNAL');
document.getElementById('modeTop').onclick = () => setMode('TOP');
document.getElementById('modeInt').onclick = () => setMode('INTERNAL');

// ── 슬라이더 ──
rSlider.oninput = e => { r = +e.target.value; rLabel.textContent = r + ' m'; };
wSlider.oninput = e => {
    w = +e.target.value;
    wLabel.textContent = w.toFixed(2) + ' rad/s';
};

// ─────────────────────────────────────────────
// 그리기 유틸리티
// ─────────────────────────────────────────────

/** 별 배경 (rotAngle 만큼 회전된 좌표계에서 그림) */
function drawSpace(cx, cy, rotAngle) {
    const now = Date.now() * 0.0008;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(rotAngle);
    stars.forEach(s => {
        const alpha = 0.4 + 0.6 * (0.5 + 0.5 * Math.sin(now + s.phase));
        ctx.globalAlpha = alpha;
        ctx.fillStyle = '#fff';
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
        ctx.fill();
    });
    ctx.globalAlpha = 1;
    ctx.restore();
}

/** 지구 (rotAngle 만큼 회전) */
function drawEarth(cx, cy, scale, rotAngle) {
    const eR  = 1400 * scale;
    const eY  = cy + 1750 * scale;
    ctx.save();
    ctx.translate(cx, eY);
    ctx.rotate(rotAngle);

    // 대기권 글로우
    const glow = ctx.createRadialGradient(0, 0, eR * 0.9, 0, 0, eR + 300 * scale);
    glow.addColorStop(0, 'rgba(56,189,248,0.35)');
    glow.addColorStop(1, 'transparent');
    ctx.fillStyle = glow;
    ctx.beginPath(); ctx.arc(0, 0, eR + 300 * scale, 0, Math.PI * 2); ctx.fill();

    // 본체
    const grad = ctx.createRadialGradient(-eR * 0.3, -eR * 0.3, 0, 0, 0, eR);
    grad.addColorStop(0,   '#1d4ed8');
    grad.addColorStop(0.7, '#1e3a8a');
    grad.addColorStop(1,   '#020617');
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(0, 0, eR, 0, Math.PI * 2); ctx.fill();

    // 구름 (단순)
    ctx.globalAlpha = 0.25; ctx.fillStyle = '#fff';
    for (let i = 0; i < 12; i++) {
        const ang = (i / 12) * Math.PI * 2;
        ctx.beginPath();
        ctx.ellipse(
            Math.cos(ang) * eR * 0.6, Math.sin(ang) * eR * 0.6,
            200 * scale, 80 * scale, ang, 0, Math.PI * 2
        );
        ctx.fill();
    }
    ctx.globalAlpha = 1;
    ctx.restore();
}

/** 비행사 (x,y 기준, rot: 위쪽이 바깥쪽) */
function drawAstronaut(x, y, rot, sc, showScale) {
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(rot);

    const ps = sc * 1.0;

    if (showScale) {
        // 체중계 패드
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(-3 * ps, -25 * ps, 6 * ps, 50 * ps);
        ctx.fillStyle = 'rgba(56,189,248,0.5)';
        ctx.fillRect(-2 * ps, -24 * ps, 4 * ps, 48 * ps);
    }

    // 몸통
    ctx.fillStyle = '#e2e8f0';
    ctx.fillRect(-30 * ps, -10 * ps, 22 * ps, 22 * ps);
    // 다리
    ctx.fillRect(-16 * ps, 12 * ps,  7 * ps, 14 * ps);
    ctx.fillRect( -7 * ps, 12 * ps,  7 * ps, 14 * ps);
    // 팔
    ctx.fillRect(-36 * ps, -10 * ps,  6 * ps, 16 * ps);
    ctx.fillRect( -8 * ps, -10 * ps,  6 * ps, 16 * ps);
    // 헬멧
    ctx.beginPath();
    ctx.arc(-19 * ps, -18 * ps, 12 * ps, 0, Math.PI * 2);
    ctx.fill();
    // 바이저
    ctx.fillStyle = '#020617';
    ctx.beginPath();
    ctx.arc(-19 * ps, -18 * ps, 8 * ps, 0, Math.PI * 2);
    ctx.fill();
    // 반짝이
    ctx.fillStyle = 'rgba(255,255,255,0.3)';
    ctx.beginPath();
    ctx.arc(-22 * ps, -21 * ps, 3 * ps, 0, Math.PI * 2);
    ctx.fill();

    ctx.restore();
}

/** 힘 화살표 */
function drawArrow(x, y, len, dir, color, label) {
    if (Math.abs(len) < 4) return;
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(dir);
    ctx.strokeStyle = color;
    ctx.fillStyle   = color;
    ctx.lineWidth   = 3.5;
    ctx.shadowColor = color;
    ctx.shadowBlur  = 8;

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(len, 0);
    ctx.stroke();

    const hs = 10;
    ctx.beginPath();
    ctx.moveTo(len, 0);
    ctx.lineTo(len - hs, -5);
    ctx.lineTo(len - hs,  5);
    ctx.closePath();
    ctx.fill();

    ctx.shadowBlur = 0;
    ctx.font = 'bold 12px JetBrains Mono, monospace';
    ctx.fillStyle = color;
    ctx.fillText(label, len > 0 ? len - hs - 60 : len + 5, -10);

    ctx.restore();
}

// ─────────────────────────────────────────────
// 메인 렌더 루프
// ─────────────────────────────────────────────
const DT = 1 / 60;

function render() {
    angle      += w * DT;
    earthAngle += 0.0002;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const W  = canvas.width;
    const H  = canvas.height;
    const cx = W / 2;
    const cy = H / 2;

    // 물리량 계산
    const accel  = r * w * w;            // 원심(구심) 가속도  m/s²
    const vel    = r * w;                // 선속도            m/s
    const period = w > 0.001 ? (2 * Math.PI / w) : Infinity;
    const force  = mass * accel;         // 합력              N
    const gVal   = accel / 9.8;         // 환산 G수

    // HUD 업데이트
    accelVal.textContent  = accel.toFixed(2)  + ' m/s²';
    velVal.textContent    = vel.toFixed(2)    + ' m/s';
    periodVal.textContent = isFinite(period) ? period.toFixed(1) + ' s' : '∞';
    forceVal.textContent  = force.toFixed(1)  + ' N';
    gforceVal.textContent = gVal.toFixed(2)   + 'G';
    gforceBar.style.width = Math.min(100, gVal * 100) + '%';
    scaleNum.textContent  = force.toFixed(1);
    effG.textContent      = gVal.toFixed(2)   + ' G';

    // ── 시점별 렌더 ──
    if (mode === 'EXTERNAL') {
        renderExternal(cx, cy);
    } else if (mode === 'TOP') {
        renderInertial(cx, cy, accel, force);
    } else {
        renderRotating(cx, cy, accel, force);
    }

    requestAnimationFrame(render);
}

// ══════════════════════════════════════════════
//  [1] 외부 원경 (Cinematic) — 정면 원형 링 뷰
// ══════════════════════════════════════════════
function renderExternal(cx, cy) {
    // 화면 크기의 약 절반을 링 반지름으로 사용 — 크게 표시
    const scale   = Math.min(canvas.width, canvas.height) / 560;
    const visualR = Math.min(canvas.width, canvas.height) * 0.36;

    drawSpace(cx, cy, 0);
    drawEarth(cx, cy, scale * 0.5, earthAngle);

    ctx.save();
    ctx.translate(cx, cy);

    // ── 허브 연결 지주 (회전) ──
    ctx.save();
    ctx.rotate(angle * 0.05);
    const spokeCount = 6;
    ctx.strokeStyle = '#334155';
    ctx.lineWidth   = 14 * scale;
    for (let i = 0; i < spokeCount; i++) {
        const a = (i / spokeCount) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(Math.cos(a) * visualR * 0.85, Math.sin(a) * visualR * 0.85);
        ctx.stroke();
    }
    ctx.restore();

    // ── 태양광 패널 (허브 위아래) ──
    ctx.save();
    ctx.rotate(angle * 0.05);
    ctx.fillStyle = '#0f172a';
    ctx.fillRect(-visualR * 0.06, -visualR * 1.18, visualR * 0.12, visualR * 0.3);
    ctx.fillRect(-visualR * 0.06,  visualR * 0.88, visualR * 0.12, visualR * 0.3);
    ctx.fillStyle = 'rgba(56,189,248,0.35)';
    for (let s of [-1, 1]) {
        for (let k = 0; k < 4; k++) {
            ctx.fillRect(
                -visualR * 0.25 + k * visualR * 0.13,
                s > 0 ? visualR * 0.9 : -visualR * 1.12,
                visualR * 0.11, visualR * 0.22
            );
        }
    }
    ctx.restore();

    // ── 허브 (중심부) ──
    const hubR = 34 * scale;
    const hubGrad = ctx.createRadialGradient(-hubR*0.3, -hubR*0.3, 0, 0, 0, hubR);
    hubGrad.addColorStop(0, '#94a3b8');
    hubGrad.addColorStop(0.6, '#334155');
    hubGrad.addColorStop(1, '#0f172a');
    ctx.fillStyle = hubGrad;
    ctx.beginPath(); ctx.arc(0, 0, hubR, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = '#64748b'; ctx.lineWidth = 2.5 * scale;
    ctx.stroke();
    // 허브 내부 작은 원
    ctx.strokeStyle = 'rgba(56,189,248,0.4)'; ctx.lineWidth = 1.5 * scale;
    ctx.beginPath(); ctx.arc(0, 0, hubR * 0.55, 0, Math.PI * 2); ctx.stroke();

    ctx.restore();

    // ── 토러스 링 본체 — 정면 완전 원형 (독립 회전) ──
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(angle);

    const tubeW    = 38 * scale;

    // 링 그림자 (외곽)
    ctx.strokeStyle = '#000';
    ctx.lineWidth   = tubeW * 2.4;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    // 링 기본 몸체
    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth   = tubeW * 2.0;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    // 링 중간 레이어
    ctx.strokeStyle = '#334155';
    ctx.lineWidth   = tubeW * 1.4;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    // 링 표면
    ctx.strokeStyle = '#475569';
    ctx.lineWidth   = tubeW * 0.7;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    // 하이라이트 (상단)
    const hlGrad = ctx.createLinearGradient(0, -visualR - tubeW, 0, -visualR + tubeW);
    hlGrad.addColorStop(0, 'rgba(148,163,184,0.6)');
    hlGrad.addColorStop(1, 'transparent');
    ctx.strokeStyle = hlGrad;
    ctx.lineWidth   = tubeW * 0.35;
    ctx.beginPath(); ctx.arc(0, 0, visualR, Math.PI * 1.15, Math.PI * 1.85); ctx.stroke();

    // 링 내벽 어두운 선
    ctx.strokeStyle = 'rgba(0,0,0,0.7)';
    ctx.lineWidth   = 1.5 * scale;
    ctx.beginPath(); ctx.arc(0, 0, visualR - tubeW * 0.6, 0, Math.PI * 2); ctx.stroke();

    // 창문 / 격벽 표시 (8개 섹션)
    ctx.strokeStyle = 'rgba(56,189,248,0.25)';
    ctx.lineWidth   = 2 * scale;
    const segCount = 16;
    for (let i = 0; i < segCount; i++) {
        const a0 = (i / segCount) * Math.PI * 2;
        const a1 = ((i + 0.05) / segCount) * Math.PI * 2;
        ctx.beginPath();
        ctx.arc(0, 0, visualR - tubeW * 0.2, a0, a1);
        ctx.stroke();
    }

    ctx.restore();

    // ── 회전 방향 화살표 ──
    ctx.save();
    ctx.translate(cx, cy);
    ctx.strokeStyle = 'rgba(56,189,248,0.6)';
    ctx.fillStyle   = 'rgba(56,189,248,0.6)';
    ctx.lineWidth   = 2.5 * scale;
    // 호 화살표 (오른쪽 위)
    const arrowAng = angle % (Math.PI * 2);
    ctx.beginPath();
    ctx.arc(0, 0, visualR + tubeW * 1.6, arrowAng + 0.1, arrowAng + 0.55);
    ctx.stroke();
    // 화살표 머리
    const aEnd = arrowAng + 0.55;
    const aHeadX = Math.cos(aEnd) * (visualR + tubeW * 1.6);
    const aHeadY = Math.sin(aEnd) * (visualR + tubeW * 1.6);
    ctx.save();
    ctx.translate(aHeadX, aHeadY);
    ctx.rotate(aEnd + Math.PI / 2);
    ctx.beginPath();
    ctx.moveTo(0, 0); ctx.lineTo(-7 * scale, -14 * scale); ctx.lineTo(7 * scale, -14 * scale);
    ctx.closePath(); ctx.fill();
    ctx.restore();
    ctx.restore();

    // ── 레이블 ──
    ctx.save();
    ctx.font = `bold ${13 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(56,189,248,0.8)';
    ctx.fillText('EXTERNAL INERTIAL FRAME', 14, 28);
    ctx.font = `${11 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(148,163,184,0.6)';
    ctx.fillText('우주정거장이 실제로 회전 중', 14, 46);
    ctx.restore();
}

// ══════════════════════════════════════════════
//  [2] 관성계 (TOP view — Inertial Frame)
//      외부 공간에서 내려다본 단면도
//      우주인이 실제로 원운동함
// ══════════════════════════════════════════════
function renderInertial(cx, cy, accel, force) {
    const scale   = Math.min(canvas.width, canvas.height) / 860;
    const visualR = r * scale;

    // ★ 관성계: 우주선 링은 고정, 배경(별·지구)만 angle 방향으로 회전
    drawSpace(cx, cy, angle);
    drawEarth(cx, cy, scale, angle + earthAngle);

    ctx.save();
    ctx.translate(cx, cy);

    const cabinH   = 52 * scale;
    const hullT    = 16 * scale;

    // 선체 (가장 바깥 원) — 고정
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth   = hullT;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    ctx.strokeStyle = '#1e293b';
    ctx.lineWidth   = hullT * 0.6;
    ctx.beginPath(); ctx.arc(0, 0, visualR, 0, Math.PI * 2); ctx.stroke();

    // 생활 공간 배경
    ctx.fillStyle = 'rgba(30,41,59,0.4)';
    ctx.beginPath();
    ctx.arc(0, 0, visualR - hullT / 2, 0, Math.PI * 2);
    ctx.arc(0, 0, Math.max(1, visualR - cabinH), 0, Math.PI * 2, true);
    ctx.fill();

    // 내벽 (천장)
    ctx.strokeStyle = 'rgba(71,85,105,0.5)';
    ctx.lineWidth   = 2 * scale;
    ctx.beginPath(); ctx.arc(0, 0, Math.max(1, visualR - cabinH), 0, Math.PI * 2); ctx.stroke();

    // 분리 격벽 (8칸) — 고정
    ctx.strokeStyle = 'rgba(71,85,105,0.3)'; ctx.lineWidth = 1.5 * scale;
    for (let i = 0; i < 8; i++) {
        const a = (i / 8) * Math.PI * 2;
        const x1 = Math.cos(a) * (visualR - cabinH);
        const y1 = Math.sin(a) * (visualR - cabinH);
        const x2 = Math.cos(a) * (visualR - hullT / 2);
        const y2 = Math.sin(a) * (visualR - hullT / 2);
        ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }

    // ── 우주인: angle 위치에서 원운동 ──
    // 비행사 기본 자세: 머리=y-(위), 발=y+(아래)
    // 발이 바깥(angle 방향) = rot: angle - π/2
    const ax = Math.cos(angle) * (visualR - hullT / 2);
    const ay = Math.sin(angle) * (visualR - hullT / 2);
    drawAstronaut(ax, ay, angle - Math.PI / 2, scale, true);

    // 수직항력 (안쪽, 중심 방향으로)
    const nLen = Math.min(120, accel * 6) * scale;
    drawArrow(ax, ay, nLen, angle + Math.PI, '#ef4444', '수직항력(N)');

    ctx.restore();
}

// ══════════════════════════════════════════════
//  [3] 비관성계 (Internal — Rotating Frame)
//  ★ 핵심: 선체와 비행사는 완전 고정
//         배경(별·지구)만 -angle 회전
//         관성력(원심력) 명확히 표시
// ══════════════════════════════════════════════
function renderRotating(cx, cy, accel, force) {
    // 확대된 스케일 — 현장감 있는 내부 시점
    const scale   = Math.min(canvas.width, canvas.height) / 260;
    const visualR = r * scale;

    // ── 배경(별·지구)만 역방향 회전 (선체 내부에서 바라보면 별이 돌아감) ──
    drawSpace(cx, cy, -angle);
    drawEarth(cx, cy, scale * 0.18, -angle + earthAngle);

    // ── 별 회전 방향 화살표 (창문 밖 별들이 돌고 있음을 시각화) ──
    ctx.save();
    ctx.translate(cx, cy);
    const starArrowR = visualR * 1.15;
    const starAngNow = (-angle) % (Math.PI * 2);
    // 곡선 화살표 (별 회전 방향)
    ctx.strokeStyle = 'rgba(148,163,184,0.5)';
    ctx.lineWidth   = 2.5 * scale;
    ctx.setLineDash([6 * scale, 4 * scale]);
    ctx.beginPath();
    ctx.arc(0, 0, starArrowR, starAngNow - 0.6, starAngNow);
    ctx.stroke();
    ctx.setLineDash([]);
    // 화살표 머리
    const sAEnd = starAngNow;
    const sAX = Math.cos(sAEnd) * starArrowR;
    const sAY = Math.sin(sAEnd) * starArrowR;
    ctx.fillStyle = 'rgba(148,163,184,0.5)';
    ctx.save();
    ctx.translate(sAX, sAY);
    ctx.rotate(sAEnd - Math.PI / 2);
    ctx.beginPath();
    ctx.moveTo(0, 0); ctx.lineTo(-6 * scale, -12 * scale); ctx.lineTo(6 * scale, -12 * scale);
    ctx.closePath(); ctx.fill();
    ctx.restore();
    // 별 회전 레이블
    ctx.font = `bold ${10 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(148,163,184,0.7)';
    const lblAng = starAngNow - 0.3;
    const lblX = Math.cos(lblAng) * (starArrowR + 18 * scale);
    const lblY = Math.sin(lblAng) * (starArrowR + 18 * scale);
    ctx.fillText('별 회전 (겉보기)', lblX - 40 * scale, lblY);
    ctx.restore();

    ctx.save();
    ctx.translate(cx, cy);

    // ── 이하 선체 구조물: 회전 변환 없음 (고정) ──

    const floorT = 46 * scale;     // 바닥 두께
    const cabinH = visualR * 0.80; // 생활공간 높이(반지름 방향)
    const viewArc = 1.1;           // 보이는 각도 (라디안, ±)

    // 1. 선체 바닥 (가장 바깥쪽 — 화면 오른쪽이 "바닥")
    ctx.strokeStyle = '#0f172a';
    ctx.lineWidth   = floorT;
    ctx.beginPath();
    ctx.arc(0, 0, visualR, -viewArc, viewArc);
    ctx.stroke();

    // 바닥 표면선 (안쪽)
    ctx.strokeStyle = '#334155';
    ctx.lineWidth   = 3 * scale;
    ctx.beginPath();
    ctx.arc(0, 0, visualR - floorT / 2, -viewArc, viewArc);
    ctx.stroke();

    // 2. 생활공간 내부 영역 채우기
    ctx.fillStyle = 'rgba(15,23,42,0.85)';
    ctx.beginPath();
    ctx.moveTo(Math.cos(-viewArc) * (visualR - floorT), Math.sin(-viewArc) * (visualR - floorT));
    ctx.arc(0, 0, visualR - floorT, -viewArc, viewArc);
    ctx.lineTo(Math.cos(viewArc) * (visualR - cabinH), Math.sin(viewArc) * (visualR - cabinH));
    ctx.arc(0, 0, Math.max(1, visualR - cabinH), viewArc, -viewArc, true);
    ctx.closePath();
    ctx.fill();

    // 3. 천장 아크
    ctx.strokeStyle = 'rgba(51,65,85,0.9)';
    ctx.lineWidth   = 5 * scale;
    ctx.beginPath();
    ctx.arc(0, 0, Math.max(1, visualR - cabinH), -viewArc, viewArc);
    ctx.stroke();

    // 4. 좌우 벽
    ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 6 * scale;
    for (const side of [-1, 1]) {
        const wallAng = side * viewArc;
        const wx0 = Math.cos(wallAng) * (visualR - floorT);
        const wy0 = Math.sin(wallAng) * (visualR - floorT);
        const wx1 = Math.cos(wallAng) * (visualR - cabinH);
        const wy1 = Math.sin(wallAng) * (visualR - cabinH);
        ctx.beginPath();
        ctx.moveTo(wx0, wy0);
        ctx.lineTo(wx1, wy1);
        ctx.stroke();
    }

    // 5. 창문 (바닥 근처 — "우주 전망대")
    for (const side of [-0.5, 0, 0.5]) {
        const wAng = side;
        const wx   = Math.cos(wAng) * (visualR - floorT * 0.3);
        const wy   = Math.sin(wAng) * (visualR - floorT * 0.3);
        ctx.save();
        ctx.translate(wx, wy);
        ctx.rotate(wAng);
        ctx.fillStyle = 'rgba(14,165,233,0.2)';
        ctx.strokeStyle = '#0ea5e9';
        ctx.lineWidth = 2 * scale;
        ctx.beginPath();
        ctx.roundRect(-10 * scale, -6 * scale, 20 * scale, 12 * scale, 3 * scale);
        ctx.fill(); ctx.stroke();
        ctx.restore();
    }

    // 6. 바닥 격자/타일
    ctx.strokeStyle = 'rgba(51,65,85,0.4)';
    ctx.lineWidth   = 1 * scale;
    for (let i = -3; i <= 3; i++) {
        const lineAng = i * viewArc / 3.5;
        const x0 = Math.cos(lineAng) * (visualR - floorT);
        const y0 = Math.sin(lineAng) * (visualR - floorT);
        const x1 = Math.cos(lineAng) * (visualR - floorT * 1.02);
        const y1 = Math.sin(lineAng) * (visualR - floorT * 1.02);
        ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1, y1); ctx.stroke();
    }

    // ── 비행사: 오른쪽(바깥)이 "바닥", 왼쪽(안쪽)이 "천장" ──
    const personX  = visualR - floorT / 2;
    const personY  = 0;
    drawAstronaut(personX, personY, -Math.PI / 2, scale, true);

    // ── 관성력(원심력) 화살표 — 바깥쪽(+x)으로, 크고 명확하게 ──
    const arrowLen = Math.max(30 * scale, Math.min(180 * scale, accel * 8 * scale));

    // 원심력(관성력) — 초록색, 두꺼운 화살표
    ctx.save();
    ctx.translate(personX, personY);
    ctx.strokeStyle = '#10b981';
    ctx.fillStyle   = '#10b981';
    ctx.lineWidth   = 5 * scale;
    ctx.shadowColor = '#10b981';
    ctx.shadowBlur  = 16;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(arrowLen, 0); ctx.stroke();
    // 화살표 머리
    ctx.beginPath();
    ctx.moveTo(arrowLen, 0);
    ctx.lineTo(arrowLen - 14 * scale, -7 * scale);
    ctx.lineTo(arrowLen - 14 * scale,  7 * scale);
    ctx.closePath(); ctx.fill();
    ctx.shadowBlur = 0;
    // 레이블 (두 줄)
    ctx.font = `bold ${12 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = '#10b981';
    ctx.fillText('관성력(원심력)', arrowLen * 0.3, -16 * scale);
    ctx.font = `${10 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(110,231,183,0.85)';
    ctx.fillText('F = mω²r = ' + force.toFixed(1) + ' N', arrowLen * 0.3, -4 * scale);
    ctx.restore();

    // 수직항력 화살표 — 안쪽(-x)으로, 빨간색
    ctx.save();
    ctx.translate(personX - 28 * scale, personY);
    ctx.strokeStyle = '#ef4444';
    ctx.fillStyle   = '#ef4444';
    ctx.lineWidth   = 4 * scale;
    ctx.shadowColor = '#ef4444';
    ctx.shadowBlur  = 12;
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(-arrowLen * 0.9, 0); ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-arrowLen * 0.9, 0);
    ctx.lineTo(-arrowLen * 0.9 + 12 * scale, -6 * scale);
    ctx.lineTo(-arrowLen * 0.9 + 12 * scale,  6 * scale);
    ctx.closePath(); ctx.fill();
    ctx.shadowBlur = 0;
    ctx.font = `bold ${11 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = '#ef4444';
    ctx.fillText('수직항력(N)', -arrowLen * 0.7, 18 * scale);
    ctx.restore();

    ctx.restore();

    // ── 내부 시점 정보 레이블 ──
    ctx.save();
    ctx.font = `bold ${12 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(16,185,129,0.85)';
    ctx.fillText('NON-INERTIAL FRAME — 비관성계', 14, 28);
    ctx.font = `${10 * scale}px JetBrains Mono, monospace`;
    ctx.fillStyle = 'rgba(148,163,184,0.7)';
    ctx.fillText('선체 고정 | 별·배경이 회전하는 것처럼 보임', 14, 46);
    ctx.restore();
}

// ─────────────────────────────────────────────
canvas.addEventListener('mousemove', e => {
    const r = canvas.getBoundingClientRect();
    coordDisp.textContent = `X: ${(e.clientX - r.left).toFixed(0)}  Y: ${(e.clientY - r.top).toFixed(0)}`;
});

render();
</script>
</body>
</html>
"""

    components.html(html_content, height=680, scrolling=False)

    # ── 학습 개념 정리 ──
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e);
                    border:1px solid rgba(56,189,248,0.25); border-radius:14px; padding:20px; height:200px;">
            <div style="color:#38bdf8; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
                🛸 외부 원경 (Cinematic View)
            </div>
            <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
                우주정거장이 실제 우주에서 회전하는 모습을 외부에서 바라봅니다.
                토러스(도넛) 형태의 거주 구역이 회전하며 내부에 원심력을 생성합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e);
                    border:1px solid rgba(239,68,68,0.25); border-radius:14px; padding:20px; height:200px;">
            <div style="color:#ef4444; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
                🔭 관성계 (Inertial Frame)
            </div>
            <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
                외부의 고정 관찰자 시점입니다. 우주인이 <strong style="color:#ef4444">실제로 원운동</strong>하며,
                바닥(선체)이 안쪽 방향으로 수직항력 N을 가합니다.
                이 N이 구심력을 담당합니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#010d1f,#0c1a2e);
                    border:1px solid rgba(16,185,129,0.25); border-radius:14px; padding:20px; height:200px;">
            <div style="color:#10b981; font-weight:800; font-size:0.85rem; margin-bottom:10px;">
                🧑‍🚀 비관성계 (Rotating Frame)
            </div>
            <p style="color:#94a3b8; font-size:0.8rem; line-height:1.7; margin:0;">
                내부 거주자 시점입니다. <strong style="color:#10b981">선체는 완전히 고정</strong>되고
                창 밖의 우주만 회전합니다.
                바깥 방향의 <strong style="color:#10b981">원심력(가상력)</strong>이 중력처럼 느껴집니다.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── 핵심 공식 ──
    st.markdown("""
    <div style="background:rgba(15,23,42,0.8); border:1px solid rgba(255,255,255,0.08);
                border-radius:14px; padding:20px; margin-top:4px;">
        <div style="color:#f8fafc; font-weight:800; font-size:0.9rem; margin-bottom:14px;">
            📐 인공중력 핵심 공식
        </div>
        <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
            <div style="background:rgba(56,189,248,0.08); border-radius:10px; padding:14px; text-align:center;">
                <div style="color:#38bdf8; font-size:1.1rem; font-weight:700; font-family:monospace;">a = rω²</div>
                <div style="color:#64748b; font-size:0.72rem; margin-top:6px;">원심(구심) 가속도</div>
            </div>
            <div style="background:rgba(16,185,129,0.08); border-radius:10px; padding:14px; text-align:center;">
                <div style="color:#10b981; font-size:1.1rem; font-weight:700; font-family:monospace;">F = mrω²</div>
                <div style="color:#64748b; font-size:0.72rem; margin-top:6px;">원심력 (= 겉보기 중력)</div>
            </div>
            <div style="background:rgba(245,158,11,0.08); border-radius:10px; padding:14px; text-align:center;">
                <div style="color:#f59e0b; font-size:1.1rem; font-weight:700; font-family:monospace;">g_eff = rω²/g</div>
                <div style="color:#64748b; font-size:0.72rem; margin-top:6px;">환산 G-Force</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── 참고 영상 섹션 ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d0a00,#1a1200);
                border:1px solid rgba(245,158,11,0.3);
                border-left:4px solid #f59e0b;
                border-radius:14px; padding:20px; margin-top:4px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
            <span style="font-size:1.3rem;">🎬</span>
            <span style="color:#f59e0b; font-weight:800; font-size:0.95rem;">탐구 참고 영상</span>
            <span style="background:rgba(245,158,11,0.15); color:#fbbf24;
                         font-size:0.65rem; font-weight:700; padding:2px 10px;
                         border-radius:999px; border:1px solid rgba(245,158,11,0.3);">
                YouTube
            </span>
        </div>
        <p style="color:#94a3b8; font-size:0.82rem; margin:0 0 14px 0; line-height:1.6;">
            영화 <strong style="color:#fbbf24">인터스텔라</strong>에 등장하는 <strong style="color:#fbbf24">쿠퍼 스테이션(Cooper Station)</strong>은
            회전하는 원통형 우주 식민지로, 원심력으로 인공중력을 구현한 대표적인 SF 사례입니다.
            아래 영상에서 실제 물리 원리와 함께 탐구해 보세요.
        </p>
        <a href="https://youtu.be/TzKvVb6j2Zo" target="_blank"
           style="display:inline-flex; align-items:center; gap:8px;
                  background:rgba(239,68,68,0.15); border:1px solid rgba(239,68,68,0.4);
                  color:#fca5a5; font-size:0.8rem; font-weight:700;
                  padding:8px 18px; border-radius:8px; text-decoration:none;
                  transition:all 0.2s;">
            ▶ 우주에 도시를 세우는 게 정말로 가능할까? — 인터스텔라의 쿠퍼스테이션
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ── 대표 장면 이미지 2장 ──
    import os
    img_dir = os.path.dirname(__file__)
    ext_img = os.path.join(img_dir, "cooper_exterior.png")
    int_img = os.path.join(img_dir, "cooper_interior.png")

    st.markdown("<br>", unsafe_allow_html=True)
    img_col1, img_col2 = st.columns(2)

    with img_col1:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px; padding:12px 14px 8px 14px; margin-bottom:4px;">
            <div style="color:#38bdf8; font-size:0.72rem; font-weight:800;
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
                🛸 장면 ① — 외부에서 본 회전 우주정거장
            </div>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists(ext_img):
            st.image(ext_img, use_container_width=True,
                     caption="거대한 링형(토러스) 우주정거장이 천천히 자전하며 내부에 인공중력을 만든다.")

    with img_col2:
        st.markdown("""
        <div style="background:rgba(15,23,42,0.6); border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px; padding:12px 14px 8px 14px; margin-bottom:4px;">
            <div style="color:#10b981; font-size:0.72rem; font-weight:800;
                        text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
                🧑‍🚀 장면 ② — 내부 거주 공간 (비관성계 시점)
            </div>
        </div>
        """, unsafe_allow_html=True)
        if os.path.exists(int_img):
            st.image(int_img, use_container_width=True,
                     caption="우주정거장 내부: 원통 안쪽 '바닥'에 서 있는 사람들. 원심력이 중력처럼 작용한다.")

    st.markdown("""
    <div style="margin-top:12px; padding:12px 16px;
                background:rgba(16,185,129,0.05);
                border:1px solid rgba(16,185,129,0.15);
                border-radius:10px; font-size:0.78rem; color:#6ee7b7; line-height:1.7;">
        💡 <strong>탐구 포인트:</strong>
        쿠퍼 스테이션의 지름은 약 <strong>2km</strong>로 추정됩니다.
        위 시뮬레이터에서 반지름을 1000m로 설정하고, 지구 중력(1G)이 되려면 각속도를 얼마로 맞춰야 하는지 계산해 보세요.
        (<em>힌트: g = rω²  →  ω = √(g/r)</em>)
    </div>
    """, unsafe_allow_html=True)

show()
