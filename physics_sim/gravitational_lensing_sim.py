import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="중력 렌즈와 시공간 곡률", layout="wide")
st.title("🔭 중력 렌즈 시뮬레이션: 시공간의 휘어짐이 빛을 bending하는 원리")

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
            const [massStrength, setMassStrength] = useState(5);  // 질량/중력 세기
            const [showCase, setShowCase] = useState(1);  // 1, 2, 3
            const [showLensType, setShowLensType] = useState('gravity');  // 'gravity' | 'convex'
            const [time, setTime] = useState(0);
            const [isAnimating, setIsAnimating] = useState(true);

            const canvasRef = useRef(null);
            const lensCanvasRef = useRef(null);

            // 애니메이션
            useEffect(() => {
                if (!isAnimating) return;
                const interval = setInterval(() => setTime(t => t + 0.02), 20);
                return () => clearInterval(interval);
            }, [isAnimating]);

            // 메인 시뮬레이션 Canvas
            useEffect(() => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);

                // 배경 (별들)
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                // 배경 별 그리기
                const stars = [
                    {x: 50, y: 80, s: 1}, {x: 120, y: 150, s: 1.5}, {x: 200, y: 60, s: 1},
                    {x: 280, y: 180, s: 2}, {x: 350, y: 100, s: 1}, {x: 400, y: 200, s: 1.5},
                    {x: 450, y: 70, s: 1}, {x: 500, y: 160, s: 2}, {x: 550, y: 90, s: 1},
                    {x: 600, y: 140, s: 1.5}, {x: 650, y: 50, s: 1}, {x: 700, y: 180, s: 1},
                    {x: 80, y: 250, s: 1}, {x: 150, y: 300, s: 1.5}, {x: 220, y: 350, s: 1},
                    {x: 450, y: 280, s: 1}, {x: 520, y: 320, s: 2}, {x: 600, y: 360, s: 1.5},
                    {x: 680, y: 300, s: 1}
                ];
                ctx.fillStyle = '#fff';
                stars.forEach(star => {
                    ctx.beginPath();
                    ctx.arc(star.x, star.y, star.s, 0, Math.PI * 2);
                    ctx.fill();
                });

                const cx = w / 2;
                const cy = h / 2;
                const bendFactor = massStrength * 0.8;

                if (showCase === 1) {
                    // Case 1: 평탄한 시공간 - 빛이 직선
                    ctx.font = 'bold 14px Inter';
                    ctx.fillStyle = '#94a3b8';
                    ctx.textAlign = 'center';
                    ctx.fillText('Case 1: 평탄한 시공간 (Space)', cx, 35);

                    // 시공간 그리드 (평평한)
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.15)';
                    ctx.lineWidth = 1;
                    for (let y = 50; y < h - 50; y += 40) {
                        ctx.beginPath();
                        ctx.moveTo(50, y);
                        ctx.lineTo(w - 50, y);
                        ctx.stroke();
                    }

                    // 광원 (오른쪽)
                    ctx.fillStyle = '#f59e0b';
                    ctx.beginPath();
                    ctx.arc(w - 80, cy, 12, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '11px Inter';
                    ctx.fillText('빛', w - 80, cy + 25);

                    // 빛의 경로 (직선)
                    ctx.strokeStyle = '#f59e0b';
                    ctx.lineWidth = 3;
                    ctx.shadowColor = '#f59e0b';
                    ctx.shadowBlur = 10;
                    ctx.setLineDash([]);
                    ctx.beginPath();
                    ctx.moveTo(w - 80, cy);
                    ctx.lineTo(80, cy);
                    ctx.stroke();
                    ctx.shadowBlur = 0;

                    // 관측자 (왼쪽)
                    ctx.fillStyle = '#10b981';
                    ctx.beginPath();
                    ctx.arc(50, cy, 8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '11px Inter';
                    ctx.fillText('관측자', 50, cy + 25);

                    // 설명
                    ctx.font = 'bold 12px Inter';
                    ctx.fillStyle = '#10b981';
                    ctx.fillText('빛: 직선으로 전파', cx, h - 40);

                } else if (showCase === 2) {
                    // Case 2: 질량 근처 - 빛이 휘어짐
                    ctx.font = 'bold 14px Inter';
                    ctx.fillStyle = '#a78bfa';
                    ctx.textAlign = 'center';
                    ctx.fillText('Case 2: 질량 근처 - 시공간 곡률', cx, 35);

                    // 시공간 그리드 (휘어진 - 질량 주위)
                    ctx.strokeStyle = 'rgba(139, 92, 246, 0.2)';
                    ctx.lineWidth = 1;
                    for (let r = 60; r < 200; r += 30) {
                        ctx.beginPath();
                        ctx.arc(cx, cy, r, 0, Math.PI * 2);
                        ctx.stroke();
                    }

                    // 질량 (중심)
                    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 40);
                    grad.addColorStop(0, '#6366f1');
                    grad.addColorStop(0.5, '#4f46e5');
                    grad.addColorStop(1, '#1e1b4b');
                    ctx.fillStyle = grad;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 40, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = 'bold 11px Inter';
                    ctx.fillStyle = '#e0e7ff';
                    ctx.fillText('질량 M', cx, cy + 5);

                    // 광원 (오른쪽 위)
                    const srcX = w - 80;
                    const srcY = 100;

                    ctx.fillStyle = '#f59e0b';
                    ctx.beginPath();
                    ctx.arc(srcX, srcY, 10, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '11px Inter';
                    ctx.fillText('빛', srcX + 15, srcY);

                    // 빛의 경로 (휘어짐 - 두 갈래)
                    ctx.strokeStyle = '#f59e0b';
                    ctx.lineWidth = 3;
                    ctx.shadowColor = '#f59e0b';
                    ctx.shadowBlur = 10;

                    // 상단의 빛 (질량 위绕过)
                    ctx.beginPath();
                    ctx.moveTo(srcX, srcY);
                    ctx.quadraticCurveTo(cx + 100, cy - 80, cx + 80, cy + 100);
                    ctx.lineTo(100, h - 80);
                    ctx.stroke();

                    // 하단의 빛 (질량 아래绕过)
                    ctx.beginPath();
                    ctx.moveTo(srcX, srcY);
                    ctx.quadraticCurveTo(cx + 80, cy + 120, cx + 60, cy - 80);
                    ctx.lineTo(100, 80);
                    ctx.stroke();

                    ctx.shadowBlur = 0;

                    // 관측자 (왼쪽)
                    ctx.fillStyle = '#10b981';
                    ctx.beginPath();
                    ctx.arc(50, cy, 8, 0, Math.PI * 2);
                    ctx.fill();

                    // 확대된 상 (질량 주변)
                    ctx.strokeStyle = 'rgba(16, 185, 129, 0.5)';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([5, 5]);
                    ctx.beginPath();
                    ctx.arc(cx, cy, 100, -Math.PI * 0.3, Math.PI * 0.3);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    ctx.font = 'bold 12px Inter';
                    ctx.fillStyle = '#a78bfa';
                    ctx.fillText('빛: 시공간 곡률을 따라 휘어짐', cx, h - 40);

                } else {
                    // Case 3: 블랙홀 근처 - 극도의 휘어짐
                    ctx.font = 'bold 14px Inter';
                    ctx.fillStyle = '#ef4444';
                    ctx.textAlign = 'center';
                    ctx.fillText('Case 3: 블랙홀 근처 - 극도의 시공간 곡률', cx, 35);

                    // 사건의 지평선 (이벤트 호라이즌)
                    ctx.strokeStyle = '#1e1b4b';
                    ctx.lineWidth = 3;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 45, 0, Math.PI * 2);
                    ctx.stroke();

                    // 블랙홀 (절대 검은)
                    ctx.fillStyle = '#000';
                    ctx.beginPath();
                    ctx.arc(cx, cy, 40, 0, Math.PI * 2);
                    ctx.fill();

                    // 블랙홀의 영향권 ( accretion disk示意)
                    ctx.strokeStyle = 'rgba(239, 68, 68, 0.3)';
                    ctx.lineWidth = 20;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 70, 0, Math.PI * 2);
                    ctx.stroke();

                    // 광원들
                    const sources = [
                        {x: w - 60, y: 80},
                        {x: w - 60, y: h - 80},
                        {x: cx + 50, y: 60},
                    ];

                    sources.forEach(src => {
                        ctx.fillStyle = '#f59e0b';
                        ctx.beginPath();
                        ctx.arc(src.x, src.y, 6, 0, Math.PI * 2);
                        ctx.fill();
                    });

                    // 빛의 경로 (블랙홀 주위를 극도로 휘어짐)
                    ctx.strokeStyle = '#f59e0b';
                    ctx.lineWidth = 2;
                    ctx.shadowColor = '#f59e0b';
                    ctx.shadowBlur = 8;

                    // 여러 빛 경로들
                    const paths = [
                        [{x: w - 60, y: 80}, {x: cx + 30, y: cy - 60}, {x: 50, y: 100}],
                        [{x: w - 60, y: h - 80}, {x: cx + 30, y: cy + 60}, {x: 50, y: h - 100}],
                        [{x: cx + 50, y: 60}, {x: cx - 20, y: cy - 30}, {x: 100, y: cy}],
                    ];

                    paths.forEach(path => {
                        ctx.beginPath();
                        ctx.moveTo(path[0].x, path[0].y);
                        for (let i = 1; i < path.length; i++) {
                            ctx.lineTo(path[i].x, path[i].y);
                        }
                        ctx.stroke();
                    });

                    ctx.shadowBlur = 0;

                    // Einstein ring 효과示意
                    ctx.strokeStyle = 'rgba(245, 158, 11, 0.5)';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.arc(cx, cy, 90, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    ctx.font = 'bold 10px Inter';
                    ctx.fillStyle = '#f59e0b';
                    ctx.textAlign = 'left';
                    ctx.fillText('Einstein Ring', cx + 95, cy - 95);

                    ctx.textAlign = 'center';
                    ctx.font = 'bold 12px Inter';
                    ctx.fillStyle = '#ef4444';
                    ctx.fillText('빛: 블랙홀 주위를 극도로 휘어짐', cx, h - 40);
                }

            }, [time, massStrength, showCase, isAnimating]);

            // 볼록렌즈 vs 중력렌즈 비교 Canvas
            useEffect(() => {
                const canvas = lensCanvasRef.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const w = canvas.width;
                const h = canvas.height;

                ctx.clearRect(0, 0, w, h);
                ctx.fillStyle = '#0a0a1a';
                ctx.fillRect(0, 0, w, h);

                const cx = w / 2;
                const cy = h / 2;

                if (showLensType === 'convex') {
                    // 볼록렌즈 (Convex Lens)
                    ctx.font = 'bold 13px Inter';
                    ctx.fillStyle = '#38bdf8';
                    ctx.textAlign = 'center';
                    ctx.fillText('볼록렌즈 (Convex Lens)', cx, 25);

                    // 렌즈 모양 (양쪽이 부풀은)
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(cx - 30, 50);
                    ctx.quadraticCurveTo(cx - 50, cy, cx - 30, h - 50);
                    ctx.stroke();
                    ctx.beginPath();
                    ctx.moveTo(cx + 30, 50);
                    ctx.quadraticCurveTo(cx + 50, cy, cx + 30, h - 50);
                    ctx.stroke();

                    // 광원 (오른쪽)
                    ctx.fillStyle = '#f59e0b';
                    ctx.beginPath();
                    ctx.arc(w - 60, cy, 8, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '10px Inter';
                    ctx.fillText('광원', w - 60, cy + 20);

                    // 빛의 경로 (굴절되어 초점으로)
                    ctx.strokeStyle = '#f59e0b';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([4, 4]);
                    ctx.beginPath();
                    ctx.moveTo(w - 60, cy);
                    ctx.lineTo(cx - 30, cy);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 초점에서 오는 빛 (집속)
                    ctx.strokeStyle = '#38bdf8';
                    ctx.setLineDash([4, 4]);
                    ctx.beginPath();
                    ctx.moveTo(cx - 30, 50);
                    ctx.lineTo(40, cy + 30);
                    ctx.moveTo(cx - 30, h - 50);
                    ctx.lineTo(40, cy - 30);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 초점
                    ctx.fillStyle = '#10b981';
                    ctx.beginPath();
                    ctx.arc(40, cy, 5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '10px Inter';
                    ctx.fillText('초점', 40, cy + 20);

                    // 렌즈 중심
                    ctx.fillStyle = '#94a3b8';
                    ctx.font = '10px Inter';
                    ctx.fillText('렌즈', cx, cy + 5);

                    // 설명
                    ctx.font = '11px Inter';
                    ctx.fillStyle = '#94a3b8';
                    ctx.textAlign = 'center';
                    ctx.fillText('빛의 굴절 → 초점 집속', cx, h - 25);

                } else {
                    // 중력 렌즈 (Gravitational Lens)
                    ctx.font = 'bold 13px Inter';
                    ctx.fillStyle = '#a78bfa';
                    ctx.textAlign = 'center';
                    ctx.fillText('중력 렌즈 (Gravitational Lens)', cx, 25);

                    // 질량/은하团 (중심)
                    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, 35);
                    grad.addColorStop(0, '#6366f1');
                    grad.addColorStop(1, '#1e1b4b');
                    ctx.fillStyle = grad;
                    ctx.beginPath();
                    ctx.arc(cx, cy, 35, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '10px Inter';
                    ctx.fillStyle = '#e0e7ff';
                    ctx.fillText('은하团', cx, cy + 4);

                    // 광원들 (질량 뒤)
                    const sources = [
                        {x: w - 60, y: cy - 60},
                        {x: w - 60, y: cy},
                        {x: w - 60, y: cy + 60},
                    ];

                    sources.forEach(src => {
                        ctx.fillStyle = '#f59e0b';
                        ctx.beginPath();
                        ctx.arc(src.x, src.y, 5, 0, Math.PI * 2);
                        ctx.fill();
                    });

                    // 빛의 경로 (휘어짐)
                    ctx.strokeStyle = '#f59e0b';
                    ctx.lineWidth = 2;

                    // 위 빛
                    ctx.beginPath();
                    ctx.moveTo(w - 60, cy - 60);
                    ctx.quadraticCurveTo(cx + 60, cy - 80, 50, cy - 40);
                    ctx.stroke();

                    // 중앙 빛
                    ctx.beginPath();
                    ctx.moveTo(w - 60, cy);
                    ctx.lineTo(50, cy);
                    ctx.stroke();

                    // 아래 빛
                    ctx.beginPath();
                    ctx.moveTo(w - 60, cy + 60);
                    ctx.quadraticCurveTo(cx + 60, cy + 80, 50, cy + 40);
                    ctx.stroke();

                    // Einstein ring示意
                    ctx.strokeStyle = 'rgba(245, 158, 11, 0.4)';
                    ctx.lineWidth = 1;
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.arc(cx, cy, 55, 0, Math.PI * 2);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 관측자 (왼쪽)
                    ctx.fillStyle = '#10b981';
                    ctx.beginPath();
                    ctx.arc(30, cy, 6, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.font = '10px Inter';
                    ctx.fillText('관측자', 30, cy + 20);

                    // 설명
                    ctx.font = '11px Inter';
                    ctx.fillStyle = '#94a3b8';
                    ctx.textAlign = 'center';
                    ctx.fillText('시공간 곡률 → 빛 경로 휘어짐', cx, h - 25);
                }

            }, [showLensType]);

            return (
                <div className="p-6 max-w-full mx-auto">
                    {/* 헤더 */}
                    <div className="mb-6 bg-gradient-to-r from-indigo-900/50 to-purple-900/50 backdrop-blur rounded-2xl p-5 border border-indigo-500/30">
                        <h2 className="text-lg font-bold text-indigo-300 mb-2">중력 렌즈 효과: 시공간의 휘어짐이 빛을 bending한다</h2>
                        <p className="text-sm text-slate-400 leading-relaxed">
                            <span className="text-amber-400">아인슈타인</span>의 일반상대성이론에 따르면, 질량은 시공간을 휘게 만듭니다.
                            이 시공간 곡률을 따라 빛이 이동하면서 마치 <span className="text-sky-400">렌즈</span>처럼 빛을 모으거나 퍼뜨립니다.
                            이것을 <span className="text-purple-400">중력 렌즈 효과</span>라고 합니다.
                        </p>
                    </div>

                    {/* 실제 중력 렌즈 관측 이미지 */}
                    <div className="mb-6 bg-slate-800/60 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                        <h3 className="text-sm font-bold text-slate-300 mb-3">🔭 실제 중력 렌즈 관측 사례</h3>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="bg-slate-900/50 rounded-xl p-3 text-center">
                                <div className="bg-slate-700 rounded-lg h-32 flex items-center justify-center mb-2 overflow-hidden">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Einstein_ring_ SDSS_J0146-0929.jpg/440px-Einstein_ring_SDSS_J0146-0929.jpg"
                                         className="w-full h-full object-cover" alt="Einstein Ring" />
                                </div>
                                <div className="text-xs font-bold text-amber-400">Einstein Ring</div>
                                <div className="text-xs text-slate-500">SDSS J0146-0929</div>
                                <div className="text-xs text-slate-600 mt-1">빛이 은하 주위를 휘어 형성된 환</div>
                            </div>
                            <div className="bg-slate-900/50 rounded-xl p-3 text-center">
                                <div className="bg-slate-700 rounded-lg h-32 flex items-center justify-center mb-2 overflow-hidden">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Abell_1689_heic_0906a.jpg/440px-Abell_1689_heic_0906a.jpg"
                                         className="w-full h-full object-cover" alt="Abell 1689" />
                                </div>
                                <div className="text-xs font-bold text-purple-400">Galaxy Cluster</div>
                                <div className="text-xs text-slate-500">Abell 1689</div>
                                <div className="text-xs text-slate-600 mt-1">은하단의 중력으로 뒤의 은하상이 왜곡</div>
                            </div>
                            <div className="bg-slate-900/50 rounded-xl p-3 text-center">
                                <div className="bg-slate-700 rounded-lg h-32 flex items-center justify-center mb-2 overflow-hidden">
                                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Hubble_ultra_deep_field.jpg/440px-Hubble_ultra_deep_field.jpg"
                                         className="w-full h-full object-cover" alt="Hubble Deep Field" />
                                </div>
                                <div className="text-xs font-bold text-emerald-400">Hubble Deep Field</div>
                                <div className="text-xs text-slate-500">Extreme Deep Field</div>
                                <div className="text-xs text-slate-600 mt-1">중력 렌즈로 보이는远古 은하들</div>
                            </div>
                        </div>
                    </div>

                    {/* 컨트롤 */}
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 mb-6">
                        <div className="lg:col-span-4 bg-slate-800/80 backdrop-blur rounded-2xl p-4 border border-slate-700/50">
                            <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-3">시뮬레이션 선택</div>
                            <div className="space-y-2">
                                <button onClick={() => setShowCase(1)}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        showCase === 1 ? 'bg-slate-500 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    Case 1: 평탄한 시공간
                                </button>
                                <button onClick={() => setShowCase(2)}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        showCase === 2 ? 'bg-purple-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    Case 2: 질량 근처
                                </button>
                                <button onClick={() => setShowCase(3)}
                                    className={`w-full py-3 px-4 rounded-xl text-sm font-bold transition-all ${
                                        showCase === 3 ? 'bg-red-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                                    Case 3: 블랙홀 근처
                                </button>
                            </div>

                            {showCase === 2 && (
                                <div className="mt-4">
                                    <div className="flex justify-between text-xs mb-1">
                                        <span className="text-slate-300">질량 세기</span>
                                        <span className="text-purple-400 font-mono">{massStrength}</span>
                                    </div>
                                    <input type="range" min="1" max="10" step="1" value={massStrength}
                                        onChange={e => setMassStrength(parseInt(e.target.value))}
                                        className="w-full h-1.5 bg-slate-600 rounded-lg appearance-none cursor-pointer accent-purple-500" />
                                </div>
                            )}

                            <button onClick={() => setIsAnimating(!isAnimating)}
                                className="w-full mt-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-xs font-bold text-slate-300 transition">
                                {isAnimating ? '⏸ 정지' : '▶ 재생'}
                            </button>
                        </div>

                        <div className="lg:col-span-8">
                            <div className="bg-slate-800/60 backdrop-blur rounded-2xl border border-slate-700/50 overflow-hidden">
                                <div className="flex items-center gap-2 px-4 py-3 border-b border-slate-700/50">
                                    <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                                    <span className="text-sm font-bold text-slate-300">시공간 곡률 시뮬레이션</span>
                                </div>
                                <div className="p-4">
                                    <canvas ref={canvasRef} width={750} height={380} className="w-full rounded-lg"></canvas>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 볼록렌즈 vs 중력렌즈 비교 */}
                    <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50 mb-6">
                        <h3 className="text-sm font-bold text-slate-300 mb-4">🔍 볼록렌즈 vs 중력렌즈 비교</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <button onClick={() => setShowLensType('convex')}
                                className={`p-4 rounded-xl border transition-all ${
                                    showLensType === 'convex' ? 'border-sky-500 bg-sky-900/20' : 'border-slate-700 bg-slate-900/30'}`}>
                                <div className="text-sm font-bold text-sky-400 mb-1">볼록렌즈 (Convex Lens)</div>
                                <div className="text-xs text-slate-400">빛의 굴절에 의한 집속</div>
                            </button>
                            <button onClick={() => setShowLensType('gravity')}
                                className={`p-4 rounded-xl border transition-all ${
                                    showLensType === 'gravity' ? 'border-purple-500 bg-purple-900/20' : 'border-slate-700 bg-slate-900/30'}`}>
                                <div className="text-sm font-bold text-purple-400 mb-1">중력렌즈 (Gravitational Lens)</div>
                                <div className="text-xs text-slate-400">시공간 곡률에 의한 빛 경로 변화</div>
                            </button>
                        </div>
                        <div className="bg-slate-900/50 rounded-xl overflow-hidden">
                            <canvas ref={lensCanvasRef} width={700} height={250} className="w-full"></canvas>
                        </div>
                    </div>

                    {/* 핵심 비교 테이블 */}
                    <div className="bg-slate-800/80 backdrop-blur rounded-2xl p-5 border border-slate-700/50">
                        <h3 className="text-sm font-bold text-slate-300 mb-4">📊 볼록렌즈와 중력렌즈의 비교</h3>
                        <div className="overflow-x-auto">
                            <table className="w-full text-xs">
                                <thead>
                                    <tr className="border-b border-slate-700">
                                        <th className="text-left py-2 px-3 text-slate-400 font-bold">구분</th>
                                        <th className="text-center py-2 px-3 text-sky-400 font-bold">볼록렌즈</th>
                                        <th className="text-center py-2 px-3 text-purple-400 font-bold">중력렌즈</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr className="border-b border-slate-800">
                                        <td className="py-2 px-3 text-slate-400">빛을 휘게 하는 원인</td>
                                        <td className="py-2 px-3 text-center text-slate-300">굴절 (Refraction)</td>
                                        <td className="py-2 px-3 text-center text-slate-300">시공간 곡률 (Spacetime Curvature)</td>
                                    </tr>
                                    <tr className="border-b border-slate-800">
                                        <td className="py-2 px-3 text-slate-400">렌즈 역할</td>
                                        <td className="py-2 px-3 text-center text-slate-300">유리 또는 플라스틱</td>
                                        <td className="py-2 px-3 text-center text-slate-300">질량/에너지 (별, 은하, 블랙홀)</td>
                                    </tr>
                                    <tr className="border-b border-slate-800">
                                        <td className="py-2 px-3 text-slate-400">초점 거리</td>
                                        <td className="py-2 px-3 text-center text-slate-300">렌즈의 초점 거리 (고정)</td>
                                        <td className="py-2 px-3 text-center text-slate-300">질량에 따라 가변 (Einstein 반지름)</td>
                                    </tr>
                                    <tr className="border-b border-slate-800">
                                        <td className="py-2 px-3 text-slate-400">관측 효과</td>
                                        <td className="py-2 px-3 text-center text-slate-300">초점에서의 상 집속</td>
                                        <td className="py-2 px-3 text-center text-slate-300">은하 왜곡, Einstein 환, 중복 상</td>
                                    </tr>
                                    <tr>
                                        <td className="py-2 px-3 text-slate-400">공식</td>
                                        <td className="py-2 px-3 text-center text-slate-300 font-mono">1/f = 1/do + 1/di</td>
                                        <td className="py-2 px-3 text-center text-slate-300 font-mono">θE = √(4GM/c²b)</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* 공식 */}
                    <div className="mt-6 bg-indigo-900/30 backdrop-blur rounded-2xl p-5 border border-indigo-500/30 text-center">
                        <div className="text-lg font-bold text-indigo-300 mb-2">아인슈타인의 중력장 방정식</div>
                        <div className="font-mono text-xl text-amber-400 mb-2">Gμν = (8πG/c⁴) Tμν</div>
                        <div className="text-xs text-slate-400">시공간의 곡률(Gμν) = 물질-에너지의 분포(Tμν)</div>
                    </div>
                </div>
            );
        };

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

components.html(react_code, height=1200, scrolling=True)
