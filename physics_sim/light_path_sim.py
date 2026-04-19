import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="빛의 경로와 등가원리", layout="wide")
st.title("💡 빛의 경로 시뮬레이션: 정지 vs 등속 vs 가속")

react_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background-color: #0a0a1a; overflow-x: hidden; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        const App = () => {
            const [motionState, setMotionState] = useState('rest'); // 'rest' | 'constant' | 'accelerating'
            const [velocity, setVelocity] = useState(5);  // 속도 (m/s)
            const [accel, setAccel] = useState(5);  // 가속도 (m/s²)
            const [time, setTime] = useState(0);
            const [isAnimating, setIsAnimating] = useState(true);

            const canvasRefs = [useRef(null), useRef(null), useRef(null)];

            // 애니메이션
            useEffect(() => {
                if (!isAnimating) return;
                const interval = setInterval(() => setTime(t => t + 0.016), 16);
                return () => clearInterval(interval);
            }, [isAnimating]);

            // Case 1: 정지 (v=0, a=0)
            useEffect(() => {
                const canvas = canvasRefs[0].current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드
                ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
                ctx.lineWidth = 1;
                for (let x = 0; x < w; x += 30) {
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
                }
                for (let y = 0; y < h; y += 30) {
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
                }

                const cx = w / 2;
                const cy = h / 2;

                // 우주선 (고정)
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#64748b';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(cx - 120, cy - 30, 240, 60, 10);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(100, 116, 139, 0.3)';
                [-60, 0, 60].forEach(offset => {
                    ctx.beginPath();
                    ctx.arc(cx + offset, cy, 12, 0, Math.PI * 2);
                    ctx.fill();
                });

                // 빛 (수평 직선)
                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 8;
                ctx.setLineDash([]);
                ctx.beginPath();
                ctx.moveTo(cx - 140, cy - 5);
                ctx.lineTo(cx + 140, cy - 5);
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 빛 방향 화살표
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                ctx.moveTo(cx + 145, cy - 5);
                ctx.lineTo(cx + 135, cy - 12);
                ctx.lineTo(cx + 135, cy + 2);
                ctx.closePath();
                ctx.fill();

                // 상태 레이블
                ctx.font = 'bold 14px Inter';
                ctx.fillStyle = '#94a3b8';
                ctx.textAlign = 'center';
                ctx.fillText('우주선: 정지 (v = 0, a = 0)', cx, cy - 60);

                ctx.font = '12px Inter';
                ctx.fillStyle = '#f59e0b';
                ctx.fillText('빛: 직선 전파', cx, cy + 55);

                ctx.font = 'bold 11px JetBrains Mono';
                ctx.fillStyle = '#10b981';
                ctx.fillText('F = 0 (관성계)', cx, cy + 75);

            }, [time, motionState]);

            // Case 2: 등속 (v≠0, a=0)
            useEffect(() => {
                const canvas = canvasRefs[1].current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드
                ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
                ctx.lineWidth = 1;
                for (let x = 0; x < w; x += 30) {
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
                }
                for (let y = 0; y < h; y += 30) {
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
                }

                const cx = w / 2;
                const cy = h / 2;
                const offset = Math.sin(time * 0.3) * 20;  // 미세한 좌우 이동

                // 우주선 (등속 - 미세한 움직임)
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#38bdf8';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(cx - 120 + offset, cy - 30, 240, 60, 10);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(56, 189, 248, 0.3)';
                [-60, 0, 60].forEach(dx => {
                    ctx.beginPath();
                    ctx.arc(cx + dx + offset, cy, 12, 0, Math.PI * 2);
                    ctx.fill();
                });

                // 빛 (수평 직선 - 도플러 효과示意)
                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 8;
                ctx.setLineDash([5, 5]);  // 파선으로 도플러 효과示意
                ctx.beginPath();
                ctx.moveTo(cx - 140 + offset, cy - 5);
                ctx.lineTo(cx + 140 + offset, cy - 5);
                ctx.stroke();
                ctx.setLineDash([]);
                ctx.shadowBlur = 0;

                // 빛 방향 화살표
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                ctx.moveTo(cx + 145 + offset, cy - 5);
                ctx.lineTo(cx + 135 + offset, cy - 12);
                ctx.lineTo(cx + 135 + offset, cy + 2);
                ctx.closePath();
                ctx.fill();

                // 상태 레이블
                ctx.font = 'bold 14px Inter';
                ctx.fillStyle = '#38bdf8';
                ctx.textAlign = 'center';
                ctx.fillText('우주선: 등속 이동 (v = ' + velocity.toFixed(1) + ' m/s, a = 0)', cx, cy - 60);

                ctx.font = '12px Inter';
                ctx.fillStyle = '#f59e0b';
                ctx.fillText('빛: 여전히 직선 전파', cx, cy + 55);

                ctx.font = 'bold 11px JetBrains Mono';
                ctx.fillStyle = '#10b981';
                ctx.fillText('F = 0 (관성계)', cx, cy + 75);

            }, [time, velocity, motionState]);

            // Case 3: 가속 (a≠0)
            useEffect(() => {
                const canvas = canvasRefs[2].current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드 (왼쪽 하단 기준점)
                ctx.strokeStyle = 'rgba(139, 92, 246, 0.08)';
                ctx.lineWidth = 1;
                for (let x = 0; x < w; x += 30) {
                    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
                }
                for (let y = 0; y < h; y += 30) {
                    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
                }

                const cx = w / 2;
                const cy = h / 2;
                const bend = (accel / 10) * 40;  // 곡률

                // 우주선 (상단 고정)
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#a78bfa';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(cx - 120, cy - 60, 240, 60, 10);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(167, 139, 250, 0.3)';
                [-60, 0, 60].forEach(offset => {
                    ctx.beginPath();
                    ctx.arc(cx + offset, cy - 30, 12, 0, Math.PI * 2);
                    ctx.fill();
                });

                // 바닥 (隆起 효과)
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(cx - 150, cy + 20);
                ctx.quadraticCurveTo(cx, cy + 20 + bend, cx + 150, cy + 20);
                ctx.stroke();
                ctx.setLineDash([]);

                // 빛 (곡선 - 아래로 휘어짐)
                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 8;
                ctx.beginPath();
                ctx.moveTo(cx - 140, cy - 30);
                const segs = 30;
                for (let i = 1; i <= segs; i++) {
                    const t = i / segs;
                    const x = cx - 140 + t * 280;
                    const y = cy - 30 + bend * t * t * 1.5;
                    ctx.lineTo(x, y);
                }
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 빛 방향 화살표
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                const arrowX = cx - 140 + 280;
                const arrowY = cy - 30 + bend * 1.5;
                ctx.moveTo(arrowX + 10, arrowY);
                ctx.lineTo(arrowX, arrowY - 8);
                ctx.lineTo(arrowX, arrowY + 8);
                ctx.closePath();
                ctx.fill();

                // 관성력 화살표 (우주선 안에서)
                const arrowLen = accel * 4;
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy - 10);
                ctx.lineTo(cx, cy - 10 + arrowLen);
                ctx.lineTo(cx - 6, cy - 10 + arrowLen - 8);
                ctx.moveTo(cx, cy - 10 + arrowLen);
                ctx.lineTo(cx + 6, cy - 10 + arrowLen - 8);
                ctx.stroke();

                // 상태 레이블
                ctx.font = 'bold 14px Inter';
                ctx.fillStyle = '#a78bfa';
                ctx.textAlign = 'center';
                ctx.fillText('우주선: 가속 중 (a = ' + accel.toFixed(1) + ' m/s²)', cx, cy - 90);

                ctx.font = '12px Inter';
                ctx.fillStyle = '#f59e0b';
                ctx.fillText('빛: 아래로 휘어짐 (겉보기)', cx, cy + 65);

                ctx.font = 'bold 11px JetBrains Mono';
                ctx.fillStyle = '#ef4444';
                ctx.fillText('f = -ma (관성력)', cx, cy + 82);

            }, [time, accel, motionState]);

            return (
                <div className="p-6 max-w-full mx-auto">
                    {/* 설명 헤더 */}
                    <div className="mb-6 bg-gradient-to-r from-slate-800/80 to-slate-900/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                        <h2 className="text-lg font-bold text-slate-200 mb-2">등가원리: 가속좌표계에서 빛의 경로</h2>
                        <p className="text-sm text-slate-400 leading-relaxed">
                            <span className="text-emerald-400 font-bold">관성계</span>에서 빛은 항상 직선으로 전파됩니다.
                            그러나 <span className="text-purple-400 font-bold">가속 좌표계</span>에서는 빛이 곡선으로 휘어보입니다.
                            이것이 아인슈타인의 등가원리: 가속도 = 중력장 (a = g)
                        </p>
                    </div>

                    {/* 컨트롤 패널 */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-6">
                        <div className="lg:col-span-3 bg-slate-800/80 backdrop-blur rounded-2xl p-4 border border-slate-700/50">
                            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">운동 상태 선택</div>
                            <div className="space-y-2">
                                <button onClick={() => setMotionState('rest')}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        motionState === 'rest' ? 'bg-slate-500 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    1. 우주선: 정지
                                </button>
                                <button onClick={() => setMotionState('constant')}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        motionState === 'constant' ? 'bg-sky-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    2. 우주선: 등속 이동
                                </button>
                                <button onClick={() => setMotionState('accelerating')}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        motionState === 'accelerating' ? 'bg-purple-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    3. 우주선: 가속 중
                                </button>
                            </div>
                        </div>

                        <div className="lg:col-span-3 bg-slate-800/80 backdrop-blur rounded-2xl p-4 border border-slate-700/50">
                            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">파라미터 조절</div>
                            <div className="space-y-4">
                                {motionState === 'constant' && (
                                    <div>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-slate-300">속도 (v)</span>
                                            <span className="text-sky-400 font-mono">{velocity.toFixed(1)} m/s</span>
                                        </div>
                                        <input type="range" min="0" max="20" step="0.5" value={velocity}
                                            onChange={e => setVelocity(parseFloat(e.target.value))}
                                            className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-sky-500" />
                                    </div>
                                )}
                                {motionState === 'accelerating' && (
                                    <div>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-slate-300">가속도 (a)</span>
                                            <span className="text-purple-400 font-mono">{accel.toFixed(1)} m/s²</span>
                                        </div>
                                        <input type="range" min="0" max="15" step="0.5" value={accel}
                                            onChange={e => setAccel(parseFloat(e.target.value))}
                                            className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-purple-500" />
                                    </div>
                                )}
                                <button onClick={() => setIsAnimating(!isAnimating)}
                                    className="w-full py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-xs font-bold text-slate-300 transition">
                                    {isAnimating ? '⏸ 정지' : '▶ 재생'}
                                </button>
                            </div>
                        </div>

                        <div className="lg:col-span-6 bg-slate-800/80 backdrop-blur rounded-2xl p-4 border border-slate-700/50">
                            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">핵심 결론</div>
                            <div className="grid grid-cols-3 gap-3 text-center">
                                <div className="bg-slate-900/50 rounded-xl p-3">
                                    <div className="text-lg font-bold text-slate-400 mb-1">정지</div>
                                    <div className="text-xs text-slate-500">a = 0</div>
                                    <div className="text-xs text-emerald-400 mt-1">빛: 직선</div>
                                </div>
                                <div className="bg-slate-900/50 rounded-xl p-3">
                                    <div className="text-lg font-bold text-sky-400 mb-1">등속</div>
                                    <div className="text-xs text-slate-500">a = 0</div>
                                    <div className="text-xs text-emerald-400 mt-1">빛: 직선</div>
                                </div>
                                <div className="bg-slate-900/50 rounded-xl p-3">
                                    <div className="text-lg font-bold text-purple-400 mb-1">가속</div>
                                    <div className="text-xs text-slate-500">a ≠ 0</div>
                                    <div className="text-xs text-amber-400 mt-1">빛: 곡선!</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 시각화 */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Case 1: 정지 */}
                        <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-slate-700/50 overflow-hidden">
                            <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50">
                                <span className="w-2 h-2 rounded-full bg-slate-500"></span>
                                <span className="text-sm font-bold text-slate-300">Case 1: 정지</span>
                                <span className="text-xs text-slate-500 ml-auto">v=0, a=0</span>
                            </div>
                            <div className="p-4">
                                <canvas ref={canvasRefs[0]} width={380} height={220} className="w-full rounded-lg"></canvas>
                            </div>
                        </div>

                        {/* Case 2: 등속 */}
                        <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-slate-700/50 overflow-hidden">
                            <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50">
                                <span className="w-2 h-2 rounded-full bg-sky-500"></span>
                                <span className="text-sm font-bold text-sky-400">Case 2: 등속</span>
                                <span className="text-xs text-slate-500 ml-auto">v≠0, a=0</span>
                            </div>
                            <div className="p-4">
                                <canvas ref={canvasRefs[1]} width={380} height={220} className="w-full rounded-lg"></canvas>
                            </div>
                        </div>

                        {/* Case 3: 가속 */}
                        <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-purple-500/30 overflow-hidden">
                            <div className="flex items-center gap-2 px-4 py-3 border-b border-purple-500/30">
                                <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                                <span className="text-sm font-bold text-purple-400">Case 3: 가속</span>
                                <span className="text-xs text-slate-500 ml-auto">a≠0</span>
                            </div>
                            <div className="p-4">
                                <canvas ref={canvasRefs[2]} width={380} height={220} className="w-full rounded-lg"></canvas>
                            </div>
                        </div>
                    </div>

                    {/* 공식 표시 */}
                    <div className="mt-6 bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
                            <div>
                                <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">관성계 (정지/등속)</div>
                                <div className="text-xl font-bold text-emerald-400 font-mono">F = 0</div>
                                <div className="text-xs text-slate-500 mt-1">빛은 직선으로 전파</div>
                            </div>
                            <div>
                                <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">가속좌표계</div>
                                <div className="text-xl font-bold text-purple-400 font-mono">f = -ma</div>
                                <div className="text-xs text-slate-500 mt-1">빛은 곡선으로 휘어보임</div>
                            </div>
                            <div>
                                <div className="text-xs text-slate-500 uppercase tracking-widest mb-1">등가원리</div>
                                <div className="text-xl font-bold text-amber-400 font-mono">a = g</div>
                                <div className="text-xs text-slate-500 mt-1">가속 ≡ 중력장</div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

components.html(react_code, height=850, scrolling=False)
