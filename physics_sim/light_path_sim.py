import streamlit as st
import streamlit.components.v1 as components

def show():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 100%);
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 16px; padding: 24px; margin-bottom: 20px;">
        <h2 style="color: #a78bfa; font-size: 1.4rem; margin: 0 0 8px 0; font-weight: 800;">
            &#9889; 빛의 경로와 등가원리 (Light Path & Equivalence Principle)
        </h2>
        <p style="color: #94a3b8; margin: 0; font-size: 0.9rem; line-height: 1.6;">
            <strong style="color:#f59e0b">가속좌표계</strong>에서 빛은 어떻게 보일까요?<br>
            관성계(외부)와 비관성계(가속)中의 차이를 탐구하세요.<br>
            <strong style="color:#10b981">등가원리</strong>: 가속도 = 중력장 (a = g)
        </p>
    </div>
    """, unsafe_allow_html=True)

    html_content = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>빛의 경로 시뮬레이션</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');

        :root {
            --bg-dark: #0a0a1a;
            --accent-violet: #a78bfa;
            --accent-amber: #f59e0b;
            --accent-emerald: #10b981;
            --panel-bg: rgba(15, 15, 30, 0.97);
            --grid-color: rgba(139, 92, 246, 0.1);
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-dark);
            color: #f8fafc;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .font-mono { font-family: 'JetBrains Mono', monospace; }

        /* ── 헤더 ── */
        header {
            height: 48px; flex-shrink: 0;
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 20px;
            background: var(--panel-bg);
            border-bottom: 1px solid rgba(139, 92, 246, 0.2);
        }
        .hdr-title {
            font-size: 0.8rem; font-weight: 700;
            color: var(--accent-violet);
            letter-spacing: 0.1em; text-transform: uppercase;
        }
        .hdr-eq {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem; color: #64748b;
        }

        /* ── 메인 레이아웃 ── */
        main { flex-grow: 1; display: flex; overflow: hidden; }

        /* ── 사이드바 ── */
        aside {
            width: 260px; flex-shrink: 0;
            background: var(--panel-bg);
            border-right: 1px solid rgba(255,255,255,0.05);
            padding: 16px; overflow-y: auto;
            display: flex; flex-direction: column; gap: 16px;
        }

        .section-label {
            font-size: 0.6rem; font-weight: 900; letter-spacing: 0.2em;
            text-transform: uppercase; color: #475569; margin-bottom: 8px;
        }

        /* 슬라이더 */
        .slider-row { margin-bottom: 14px; }
        .slider-header {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.68rem; font-weight: 700; text-transform: uppercase; margin-bottom: 6px;
        }
        .slider-val { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--accent-violet); }

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
            box-shadow: 0 0 10px var(--accent-violet);
        }

        /* 모드 버튼 */
        .btn-mode {
            width: 100%; padding: 12px 14px;
            text-align: center; border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.03);
            color: #94a3b8; font-size: 0.72rem; font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 6px;
        }
        .btn-mode:hover { background: rgba(139, 92, 246, 0.15); color: #f8fafc; }
        .btn-mode.active {
            background: var(--accent-violet); color: #000;
            box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
            border-color: transparent;
        }

        /* 데이터 카드 */
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
        .data-key { color: #64748b; font-weight: 700; }
        .data-val { font-family: 'JetBrains Mono', monospace; color: #e2e8f0; }

        /* ── 시각화 영역 ── */
        .viz-container {
            flex-grow: 1;
            display: flex;
            gap: 16px;
            padding: 16px;
            background: var(--bg-dark);
        }

        .viz-panel {
            flex: 1;
            background: var(--panel-bg);
            border: 1px solid rgba(139, 92, 246, 0.15);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .viz-header {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .viz-header-dot {
            width: 8px; height: 8px; border-radius: 50%;
        }
        .viz-title {
            font-size: 0.72rem; font-weight: 700;
            text-transform: uppercase; letter-spacing: 0.05em;
        }
        .viz-desc {
            font-size: 0.6rem; color: #64748b; margin-left: auto;
        }

        .viz-canvas-wrap {
            flex-grow: 1;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        canvas {
            display: block;
        }

        /* ── 공식 표시 ── */
        .formula-bar {
            padding: 12px 16px;
            background: rgba(0,0,0,0.3);
            border-top: 1px solid rgba(255,255,255,0.05);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            color: #94a3b8;
            display: flex;
            gap: 24px;
            justify-content: center;
        }
        .formula-item { display: flex; gap: 8px; }
        .formula-symbol { color: var(--accent-violet); }
        .formula-value { color: var(--accent-emerald); }

        /* ── 범례 ── */
        .legend {
            position: absolute; bottom: 12px; left: 50%;
            transform: translateX(-50%);
            background: var(--panel-bg);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 999px; padding: 6px 16px;
            display: flex; align-items: center; gap: 16px;
            font-size: 0.65rem; font-weight: 700;
            white-space: nowrap;
        }
        .legend-item { display: flex; align-items: center; gap: 6px; }
        .legend-dot { width: 8px; height: 8px; border-radius: 50%; }

        /* ── 눈금자 ── */
        .ruler {
            position: absolute; bottom: 50px; left: 50%;
            transform: translateX(-50%);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.55rem; color: #475569;
            display: flex; gap: 4px;
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        // ── 상수 ──
        const C = 3e8;  // 광속 (m/s)
        const SCALE = 40;  // 픽셀당 미터

        // ── 메인 앱 ──
        const App = () => {
            const [viewMode, setViewMode] = useState('inertial'); // 'inertial' | 'accelerating'
            const [accel, setAccel] = useState(5);  // 가속도 (m/s²)
            const [lightAngle, setLightAngle] = useState(30);  // 빛의 초기 각도 (도)
            const [showGrid, setShowGrid] = useState(true);
            const [isAnimating, setIsAnimating] = useState(true);
            const [time, setTime] = useState(0);

            const canvasRef1 = useRef(null);
            const canvasRef2 = useRef(null);

            // ── 애니메이션 루프 ──
            useEffect(() => {
                if (!isAnimating) return;

                const interval = setInterval(() => {
                    setTime(t => t + 0.016);
                }, 16);

                return () => clearInterval(interval);
            }, [isAnimating]);

            // ── 관성계 시각화 ──
            useEffect(() => {
                const canvas = canvasRef1.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);

                // 배경
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드
                if (showGrid) {
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
                    ctx.lineWidth = 1;
                    for (let x = 0; x < w; x += 40) {
                        ctx.beginPath();
                        ctx.moveTo(x, 0);
                        ctx.lineTo(x, h);
                        ctx.stroke();
                    }
                    for (let y = 0; y < h; y += 40) {
                        ctx.beginPath();
                        ctx.moveTo(0, y);
                        ctx.lineTo(w, y);
                        ctx.stroke();
                    }
                }

                const cx = w / 2;
                const cy = h / 2;

                // spacecraft 이동 (관성계 - 일정한 속도로 이동)
                const shipX = cx + Math.sin(time * 0.5) * 50;

                // spacecraft 그리기
                drawSpacecraft(ctx, shipX, cy, 0, false);

                // 빛의 경로 (직선 - 관성계)
                const angleRad = (lightAngle * Math.PI) / 180;
                const rayStartX = shipX - 60;
                const rayStartY = cy - 20;
                const rayLen = 300;

                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.moveTo(rayStartX, rayStartY);
                ctx.lineTo(rayStartX + rayLen * Math.cos(angleRad), rayStartY - rayLen * Math.sin(angleRad));
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 레이저 발사점
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                ctx.arc(rayStartX, rayStartY, 5, 0, Math.PI * 2);
                ctx.fill();

                // 레이블
                ctx.font = '11px Inter';
                ctx.fillStyle = '#f59e0b';
                ctx.fillText('빛 (직선 전파)', rayStartX + rayLen * Math.cos(angleRad) - 60, rayStartY - rayLen * Math.sin(angleRad) - 10);

            }, [time, viewMode, accel, lightAngle, showGrid]);

            // ── 가속좌표계 시각화 ──
            useEffect(() => {
                const canvas = canvasRef2.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);

                // 배경
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드 (좌표계와 함께 회전)
                if (showGrid) {
                    ctx.save();
                    ctx.translate(w / 2, h / 2);
                    ctx.rotate(-time * 0.3);
                    ctx.translate(-w / 2, -h / 2);

                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
                    ctx.lineWidth = 1;
                    for (let x = 0; x < w; x += 40) {
                        ctx.beginPath();
                        ctx.moveTo(x, 0);
                        ctx.lineTo(x, h);
                        ctx.stroke();
                    }
                    for (let y = 0; y < h; y += 40) {
                        ctx.beginPath();
                        ctx.moveTo(0, y);
                        ctx.lineTo(w, y);
                        ctx.stroke();
                    }
                    ctx.restore();
                }

                const cx = w / 2;
                const cy = h / 2;

                // spacecraft 고정 (가속좌표계)
                drawSpacecraft(ctx, cx, cy, 0, true);

                // 빛의 경로 (곡선 - 가속좌표계에서 겉보기)
                const angleRad = (lightAngle * Math.PI) / 180;
                const rayStartX = cx - 60;
                const rayStartY = cy - 20;

                // 곡선 빛 경로 (좌표계 회전 효과)
                ctx.strokeStyle = '#a78bfa';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#a78bfa';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.moveTo(rayStartX, rayStartY);

                const bendFactor = (accel / 10) * 0.02;  // 곡률 계수
                const segments = 50;
                for (let i = 1; i <= segments; i++) {
                    const t = i / segments;
                    const x = rayStartX + t * 200 * Math.cos(angleRad);
                    const y = rayStartY - t * 200 * Math.sin(angleRad) + bendFactor * 200 * t * t * Math.sin(angleRad * 2);
                    ctx.lineTo(x, y);
                }
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 레이블
                ctx.font = '11px Inter';
                ctx.fillStyle = '#a78bfa';
                ctx.fillText('빛 (곡선으로 휘어보임)', cx + 80, cy - 100);

                // 관성력 화살표
                const arrowLen = accel * 8;
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy + 30);
                ctx.lineTo(cx + arrowLen, cy + 30);
                // 화살촉
                ctx.lineTo(cx + arrowLen - 8, cy + 25);
                ctx.moveTo(cx + arrowLen, cy + 30);
                ctx.lineTo(cx + arrowLen - 8, cy + 35);
                ctx.stroke();

                ctx.font = '10px Inter';
                ctx.fillStyle = '#ef4444';
                ctx.fillText('f (관성력)', cx + arrowLen + 5, cy + 35);

            }, [time, viewMode, accel, lightAngle, showGrid]);

            // ── spacecraft 그리기 함수 ──
            const drawSpacecraft = (ctx, x, y, rotation, isAccelerating) => {
                ctx.save();
                ctx.translate(x, y);
                ctx.rotate(rotation);

                // 본체
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = isAccelerating ? '#a78bfa' : '#38bdf8';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(-50, -25, 100, 50, 8);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
                ctx.beginPath();
                ctx.arc(-30, 0, 10, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(0, 0, 10, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.arc(30, 0, 10, 0, Math.PI * 2);
                ctx.fill();

                // 레이블
                ctx.font = '10px Inter';
                ctx.fillStyle = isAccelerating ? '#a78bfa' : '#38bdf8';
                ctx.textAlign = 'center';
                ctx.fillText(isAccelerating ? '가속 좌표계' : ' spacecraft', 0, -40);

                ctx.restore();
            };

            return (
                <div className="flex flex-col h-screen">
                    {/* 헤더 */}
                    <header>
                        <div className="flex items-center gap-3">
                            <span className="text-purple-400 font-bold text-sm tracking-widest uppercase">Equivalence Principle</span>
                            <span className="text-gray-500 text-xs font-mono">Light Path Simulation</span>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="text-gray-500 text-xs font-mono">t = {time.toFixed(2)} s</span>
                            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        </div>
                    </header>

                    {/* 메인 */}
                    <main className="flex flex-1 overflow-hidden">
                        {/* 사이드바 */}
                        <aside>
                            <div>
                                <div className="section-label">좌표계 선택</div>
                                <button
                                    className={`btn-mode ${viewMode === 'inertial' ? 'active' : ''}`}
                                    onClick={() => setViewMode('inertial')}
                                >
                                    관성계 (Inertial)
                                </button>
                                <button
                                    className={`btn-mode ${viewMode === 'accelerating' ? 'active' : ''}`}
                                    onClick={() => setViewMode('accelerating')}
                                >
                                    가속좌표계 (Accelerating)
                                </button>
                            </div>

                            <div>
                                <div className="section-label">파라미터</div>
                                <div className="slider-row">
                                    <div className="slider-header">
                                        <span>가속도 (a)</span>
                                        <span className="slider-val">{accel.toFixed(1)} m/s²</span>
                                    </div>
                                    <input type="range" min="0" max="15" step="0.5" value={accel}
                                        onChange={e => setAccel(parseFloat(e.target.value))} />
                                </div>
                                <div className="slider-row">
                                    <div className="slider-header">
                                        <span>빛의 각도 (θ)</span>
                                        <span className="slider-val">{lightAngle}°</span>
                                    </div>
                                    <input type="range" min="0" max="60" step="5" value={lightAngle}
                                        onChange={e => setLightAngle(parseInt(e.target.value))} />
                                </div>
                            </div>

                            <div>
                                <div className="section-label">표시 옵션</div>
                                <label className="flex items-center gap-2 text-xs text-gray-400 mb-2 cursor-pointer">
                                    <input type="checkbox" checked={showGrid} onChange={e => setShowGrid(e.target.checked)}
                                        className="w-4 h-4 accent-purple-500" />
                                    그리드 표시
                                </label>
                                <button
                                    className="btn-mode"
                                    onClick={() => setIsAnimating(!isAnimating)}
                                >
                                    {isAnimating ? '⏸ 정지' : '▶ 재생'}
                                </button>
                            </div>

                            <div>
                                <div className="section-label">물리 데이터</div>
                                <div className="data-card">
                                    <div className="data-row">
                                        <span className="data-key">광속</span>
                                        <span className="data-val">c = 3×10⁸ m/s</span>
                                    </div>
                                    <div className="data-row">
                                        <span className="data-key">가속도</span>
                                        <span className="data-val">a = {accel.toFixed(1)} m/s²</span>
                                    </div>
                                    <div className="data-row">
                                        <span className="data-key">환산 g</span>
                                        <span className="data-val">{(accel/9.8).toFixed(2)} g</span>
                                    </div>
                                    <div className="data-row">
                                        <span className="data-key">빛의 각도</span>
                                        <span className="data-val">θ = {lightAngle}°</span>
                                    </div>
                                </div>
                            </div>

                            <div>
                                <div className="section-label">등가원리</div>
                                <div className="data-card text-center">
                                    <div className="font-mono text-purple-400 text-lg mb-1">a = g</div>
                                    <div className="text-xs text-gray-500">가속도 ≡ 중력장</div>
                                </div>
                            </div>
                        </aside>

                        {/* 시각화 영역 */}
                        <div className="viz-container">
                            {/* 관성계 패널 */}
                            <div className="viz-panel">
                                <div className="viz-header">
                                    <span className="viz-header-dot bg-emerald-400"></span>
                                    <span className="viz-title text-emerald-400">관성계 (External)</span>
                                    <span className="viz-desc">바깥에서 관찰</span>
                                </div>
                                <div className="viz-canvas-wrap">
                                    <canvas ref={canvasRef1} width={450} height={350}></canvas>
                                </div>
                                <div className="formula-bar">
                                    <div className="formula-item">
                                        <span className="formula-symbol">빛:</span>
                                        <span className="text-emerald-400">직선 전파</span>
                                    </div>
                                    <div className="formula-item">
                                        <span className="formula-symbol">F =</span>
                                        <span className="formula-value">0 (외부 관성계)</span>
                                    </div>
                                </div>
                            </div>

                            {/* 가속좌표계 패널 */}
                            <div className="viz-panel">
                                <div className="viz-header">
                                    <span className="viz-header-dot bg-purple-400"></span>
                                    <span className="viz-title text-purple-400">가속좌표계 (Internal)</span>
                                    <span className="viz-desc">안에서 관찰</span>
                                </div>
                                <div className="viz-canvas-wrap">
                                    <canvas ref={canvasRef2} width={450} height={350}></canvas>
                                </div>
                                <div className="formula-bar">
                                    <div className="formula-item">
                                        <span className="formula-symbol">빛:</span>
                                        <span className="text-purple-400">곡선으로 휘어보임</span>
                                    </div>
                                    <div className="formula-item">
                                        <span className="formula-symbol">f =</span>
                                        <span className="formula-value">-ma (관성력)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </main>
                </div>
            );
        };

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

    components.html(html_content, height=700, scrolling=False)

if __name__ == "__main__":
    show()
