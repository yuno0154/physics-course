import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="빛의 경로와 등가원리", layout="wide")
st.title("💡 빛의 경로 시뮬레이션: 가속좌표계 vs 관성계")

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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; margin: 0; padding: 0; background-color: #0a0a1a; overflow: hidden; }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef } = React;

        const App = () => {
            const [accel, setAccel] = useState(5);
            const [lightAngle, setLightAngle] = useState(30);
            const [viewMode, setViewMode] = useState('inertial');
            const [showGrid, setShowGrid] = useState(true);
            const [time, setTime] = useState(0);
            const [isAnimating, setIsAnimating] = useState(true);

            const canvasRef1 = useRef(null);
            const canvasRef2 = useRef(null);

            // 애니메이션
            useEffect(() => {
                if (!isAnimating) return;
                const interval = setInterval(() => setTime(t => t + 0.016), 16);
                return () => clearInterval(interval);
            }, [isAnimating]);

            // 관성계 Canvas
            useEffect(() => {
                const canvas = canvasRef1.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드
                if (showGrid) {
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.1)';
                    ctx.lineWidth = 1;
                    for (let x = 0; x < w; x += 40) {
                        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
                    }
                    for (let y = 0; y < h; y += 40) {
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
                    }
                }

                const cx = w / 2;
                const cy = h / 2;
                const shipX = cx + Math.sin(time * 0.5) * 30;
                const angleRad = (lightAngle * Math.PI) / 180;

                // spacecraft
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#38bdf8';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(shipX - 50, cy - 25, 100, 50, 8);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(56, 189, 248, 0.4)';
                [-30, 0, 30].forEach(offset => {
                    ctx.beginPath();
                    ctx.arc(shipX + offset, cy, 8, 0, Math.PI * 2);
                    ctx.fill();
                });

                // 빛 (직선)
                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#f59e0b';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.moveTo(shipX - 60, cy);
                ctx.lineTo(shipX - 60 + 280 * Math.cos(angleRad), cy - 280 * Math.sin(angleRad));
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 레이블
                ctx.font = 'bold 12px Inter';
                ctx.fillStyle = '#f59e0b';
                ctx.fillText('빛 (직선 전파)', shipX + 80, cy - 80);

                // spacecraft 레이블
                ctx.fillStyle = '#38bdf8';
                ctx.fillText(' spacecraft', shipX, cy - 45);

            }, [time, lightAngle, showGrid]);

            // 가속좌표계 Canvas
            useEffect(() => {
                const canvas = canvasRef2.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 그리드 (회전)
                if (showGrid) {
                    ctx.save();
                    ctx.translate(w / 2, h / 2);
                    ctx.rotate(-time * 0.3);
                    ctx.translate(-w / 2, -h / 2);
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.1)';
                    ctx.lineWidth = 1;
                    for (let x = 0; x < w; x += 40) {
                        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
                    }
                    for (let y = 0; y < h; y += 40) {
                        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
                    }
                    ctx.restore();
                }

                const cx = w / 2;
                const cy = h / 2;
                const angleRad = (lightAngle * Math.PI) / 180;
                const bend = (accel / 10) * 0.015;

                // spacecraft (고정)
                ctx.fillStyle = '#1e293b';
                ctx.strokeStyle = '#a78bfa';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.roundRect(cx - 50, cy - 25, 100, 50, 8);
                ctx.fill();
                ctx.stroke();

                // 창
                ctx.fillStyle = 'rgba(167, 139, 250, 0.4)';
                [-30, 0, 30].forEach(offset => {
                    ctx.beginPath();
                    ctx.arc(cx + offset, cy, 8, 0, Math.PI * 2);
                    ctx.fill();
                });

                // 빛 (곡선)
                ctx.strokeStyle = '#a78bfa';
                ctx.lineWidth = 3;
                ctx.shadowColor = '#a78bfa';
                ctx.shadowBlur = 10;
                ctx.beginPath();
                ctx.moveTo(cx - 60, cy);
                const segs = 40;
                for (let i = 1; i <= segs; i++) {
                    const t = i / segs;
                    const x = cx - 60 + t * 250 * Math.cos(angleRad);
                    const y = cy - t * 250 * Math.sin(angleRad) + bend * 250 * t * t * Math.sin(angleRad * 2);
                    ctx.lineTo(x, y);
                }
                ctx.stroke();
                ctx.shadowBlur = 0;

                // 관성력 화살표
                const arrowLen = accel * 6;
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(cx, cy + 40);
                ctx.lineTo(cx + arrowLen, cy + 40);
                ctx.lineTo(cx + arrowLen - 6, cy + 35);
                ctx.moveTo(cx + arrowLen, cy + 40);
                ctx.lineTo(cx + arrowLen - 6, cy + 45);
                ctx.stroke();

                // 레이블
                ctx.font = 'bold 12px Inter';
                ctx.fillStyle = '#a78bfa';
                ctx.fillText('빛 (곡선으로 휘어보임)', cx + 50, cy - 80);
                ctx.fillStyle = '#ef4444';
                ctx.fillText('f = -ma', cx + arrowLen + 10, cy + 45);
                ctx.fillStyle = '#a78bfa';
                ctx.fillText('가속 좌표계', cx, cy - 45);

            }, [time, accel, lightAngle, showGrid]);

            return (
                <div className="p-6 max-w-full mx-auto">
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                        {/* 사이드바 */}
                        <div className="lg:col-span-3 space-y-4">
                            <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                                <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">좌표계 선택</div>
                                <div className="flex bg-slate-700 p-1 rounded-xl text-xs font-bold">
                                    <button onClick={() => setViewMode('inertial')}
                                        className={`flex-1 py-2 rounded-lg transition-all ${viewMode === 'inertial' ? 'bg-purple-500 text-white' : 'text-slate-400'}`}>
                                        관성계
                                    </button>
                                    <button onClick={() => setViewMode('accelerating')}
                                        className={`flex-1 py-2 rounded-lg transition-all ${viewMode === 'accelerating' ? 'bg-purple-500 text-white' : 'text-slate-400'}`}>
                                        가속좌표계
                                    </button>
                                </div>
                            </div>

                            <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                                <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">파라미터</div>
                                <div className="space-y-4">
                                    <div>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-slate-300">가속도 (a)</span>
                                            <span className="text-purple-400 font-mono">{accel.toFixed(1)} m/s²</span>
                                        </div>
                                        <input type="range" min="0" max="15" step="0.5" value={accel}
                                            onChange={e => setAccel(parseFloat(e.target.value))}
                                            className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-purple-500" />
                                    </div>
                                    <div>
                                        <div className="flex justify-between text-xs mb-1">
                                            <span className="text-slate-300">빛의 각도 (θ)</span>
                                            <span className="text-purple-400 font-mono">{lightAngle}°</span>
                                        </div>
                                        <input type="range" min="0" max="60" step="5" value={lightAngle}
                                            onChange={e => setLightAngle(parseInt(e.target.value))}
                                            className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-purple-500" />
                                    </div>
                                </div>
                            </div>

                            <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                                <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">표시 옵션</div>
                                <label className="flex items-center gap-2 text-xs text-slate-300 mb-2 cursor-pointer">
                                    <input type="checkbox" checked={showGrid} onChange={e => setShowGrid(e.target.checked)}
                                        className="w-4 h-4 accent-purple-500" />
                                    그리드 표시
                                </label>
                                <button onClick={() => setIsAnimating(!isAnimating)}
                                    className="w-full mt-2 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-xs font-bold text-slate-300 transition">
                                    {isAnimating ? '⏸ 정지' : '▶ 재생'}
                                </button>
                            </div>

                            <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                                <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">물리 데이터</div>
                                <div className="space-y-2 text-xs">
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">광속</span>
                                        <span className="text-slate-200 font-mono">c = 3×10⁸ m/s</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">가속도</span>
                                        <span className="text-slate-200 font-mono">a = {accel.toFixed(1)} m/s²</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-slate-400">환산 g</span>
                                        <span className="text-emerald-400 font-mono">{(accel/9.8).toFixed(2)} g</span>
                                    </div>
                                </div>
                            </div>

                            <div className="bg-purple-900/30 backdrop-blur rounded-2xl p-5 border border-purple-500/30 text-center">
                                <div className="text-2xl font-bold text-purple-400 mb-1">a = g</div>
                                <div className="text-xs text-slate-400">등가원리</div>
                            </div>
                        </div>

                        {/* 시각화 영역 */}
                        <div className="lg:col-span-9 space-y-4">
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                {/* 관성계 */}
                                <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-slate-700/50 overflow-hidden">
                                    <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50">
                                        <span className="w-2 h-2 rounded-full bg-emerald-400"></span>
                                        <span className="text-sm font-bold text-emerald-400">관성계 (External)</span>
                                        <span className="text-xs text-slate-500 ml-auto">바깥에서 관찰</span>
                                    </div>
                                    <div className="p-4">
                                        <canvas ref={canvasRef1} width={400} height={300} className="w-full rounded-lg"></canvas>
                                    </div>
                                    <div className="px-4 py-3 bg-slate-900/50 flex items-center gap-4 text-xs">
                                        <span className="text-amber-400">● 빛: 직선 전파</span>
                                        <span className="text-slate-400">F = 0</span>
                                    </div>
                                </div>

                                {/* 가속좌표계 */}
                                <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-slate-700/50 overflow-hidden">
                                    <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50">
                                        <span className="w-2 h-2 rounded-full bg-purple-400"></span>
                                        <span className="text-sm font-bold text-purple-400">가속좌표계 (Internal)</span>
                                        <span className="text-xs text-slate-500 ml-auto">안에서 관찰</span>
                                    </div>
                                    <div className="p-4">
                                        <canvas ref={canvasRef2} width={400} height={300} className="w-full rounded-lg"></canvas>
                                    </div>
                                    <div className="px-4 py-3 bg-slate-900/50 flex items-center gap-4 text-xs">
                                        <span className="text-purple-400">● 빛: 곡선으로 휘어보임</span>
                                        <span className="text-red-400">f = -ma</span>
                                    </div>
                                </div>
                            </div>

                            {/* 설명 */}
                            <div className="bg-slate-800/60 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                                <h3 className="text-sm font-bold text-slate-200 mb-2">등가원리 (Equivalence Principle)</h3>
                                <p className="text-xs text-slate-400 leading-relaxed">
                                    가속하는 좌표계에서는 중력장과 등가적인 관성력이 발생합니다.
                                    이 좌표계 안에서는 빛이 곡선으로 휘어보이는 것처럼 관찰됩니다.
                                    그러나 외부 관성계에서 보면 빛은 여전히 직선으로 전파됩니다.
                                    이것이 아인슈타인의 등가원리: <span className="text-purple-400 font-bold">가속도 = 중력장 (a = g)</span>
                                </p>
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

components.html(react_code, height=750, scrolling=False)
