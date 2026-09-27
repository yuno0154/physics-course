import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.title("🪐 케플러 제2법칙: 면적 속도 일정 법칙")
    st.markdown("""
    태양과 행성을 잇는 선분이 같은 시간 동안 쓸고 지나가는 **면적은 항상 일정(케플러 제2법칙: 면적 속도 일정 법칙)**합니다.
    
    부채꼴의 면적을 비교하며 **"태양과 가까울수록 빠르고, 멀수록 느리다"**는 핵심 원리를 관찰하고, 
    고등학교 시험에 반드시 출제되는 **근일점과 원일점에서의 5대 물리량(중력, 가속도, 운동 에너지, 퍼텐셜 에너지, 역학적 에너지)**의 대소 관계를 인터랙티브하게 정리해 보세요.
    """)

    react_code = r"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
        <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                height: 20px;
                width: 20px;
                border-radius: 50%;
                background: #ef4444;
                cursor: pointer;
                border: 2px solid white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            }
            .katex-display { margin: 0.3em 0 !important; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) window.lucide.createIcons();
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }} className={className}></i>;
            };

            const MathBox = ({ formula, inline = false, className = "" }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (ref.current && window.katex) {
                        try {
                            window.katex.render(formula, ref.current, {
                                throwOnError: false,
                                displayMode: !inline
                            });
                        } catch (e) {
                            ref.current.innerText = formula;
                        }
                    }
                }, [formula, inline]);
                return <span ref={ref} className={className} />;
            };

            // 대표 천체 프리셋 (고교 수준에 맞게 간결화)
            const CELESTIAL_PRESETS = [
                { name: '지구', e: 0.0167, a: 140, desc: '거의 원형', color: '#3b82f6', symbol: '⊕' },
                { name: '화성', e: 0.0934, a: 140, desc: '케플러 2법칙 발견의 열쇠', color: '#ef4444', symbol: '♂' },
                { name: '수성', e: 0.2056, a: 140, desc: '행성 중 최대 타원', color: '#94a3b8', symbol: '☿' },
                { name: '가상 타원', e: 0.5000, a: 140, desc: '속도 변화 뚜렷한 연습 궤도', color: '#a855f7', symbol: '🚀' }
            ];

            // 고등학교 수준 5가지 물리량 비교 데이터 (핵심 중심)
            const PHYSICAL_QUANTITIES = [
                {
                    id: 'gravity',
                    name: '중력 (만유인력)',
                    symbol: 'F',
                    formula: 'F = G \\frac{Mm}{r^2}',
                    perihelion: '최대',
                    aphelion: '최소',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    badgeColor: 'bg-red-500 text-white',
                    coreReason: '중력은 태양과의 거리 제곱에 반비례(F ∝ 1/r²)합니다. 따라서 거리가 가장 가까운 근일점에서 중력이 가장 큽니다.'
                },
                {
                    id: 'accel',
                    name: '가속도 (중력 가속도)',
                    symbol: 'a',
                    formula: 'a = \\frac{F}{m} = G \\frac{M}{r^2}',
                    perihelion: '최대',
                    aphelion: '최소',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    badgeColor: 'bg-orange-500 text-white',
                    coreReason: '뉴턴 운동 제2법칙(F = ma)에 의해 가속도는 중력에 비례합니다. 거리가 가까워 중력이 가장 큰 근일점에서 가속도가 최대입니다.'
                },
                {
                    id: 'kinetic',
                    name: '운동 에너지',
                    symbol: 'E_k',
                    formula: 'E_k = \\frac{1}{2} m v^2',
                    perihelion: '최대',
                    aphelion: '최소',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    badgeColor: 'bg-rose-500 text-white',
                    coreReason: '케플러 제2법칙에 의해 근일점에서 공전 속력(v)이 가장 빠릅니다. 운동 에너지는 속력의 제곱에 비례(E_k ∝ v²)하므로 근일점에서 최대입니다.'
                },
                {
                    id: 'potential',
                    name: '만유인력 퍼텐셜 에너지 (위치 에너지)',
                    symbol: 'E_p',
                    formula: 'E_p = -G \\frac{Mm}{r}',
                    perihelion: '최소',
                    aphelion: '최대',
                    comparison: '근일점 < 원일점',
                    sign: '<',
                    badgeColor: 'bg-blue-600 text-white',
                    coreReason: '★ [시험 단골 주의!] 태양에 가까울수록 위치 에너지는 작아지고, 멀어질수록 커집니다 (인력이 작용하는 공간에서는 무한대 거리 r=∞를 기준 0으로 두므로, 가까울수록 음수(-) 값이 더 커져 에너지는 최소가 됩니다).'
                },
                {
                    id: 'mechanical',
                    name: '역학적 에너지',
                    symbol: 'E',
                    formula: 'E = E_k + E_p',
                    perihelion: '일정 (보존)',
                    aphelion: '일정 (보존)',
                    comparison: '근일점 = 원일점',
                    sign: '=',
                    badgeColor: 'bg-emerald-600 text-white',
                    coreReason: '★ [역학적 에너지 보존] 행성에는 보존력인 만유인력만 작용하므로, 궤도 상의 모든 지점에서 총 역학적 에너지는 항상 일정하게 보존됩니다.'
                }
            ];

            const KeplerAreaSim = () => {
                const [eccentricity, setEccentricity] = useState(0.50);
                const [semiMajorAxis, setSemiMajorAxis] = useState(140);
                const [isPlaying, setIsPlaying] = useState(false);
                const [timeFraction, setTimeFraction] = useState(8); // 관측 시간 간격 T/N
                const [planetPos, setPlanetPos] = useState({ x: 0, y: 0, angle: 0 });
                const [selectedPresetName, setSelectedPresetName] = useState('가상 타원');
                const [isCounterClockwise, setIsCounterClockwise] = useState(true); // 천문학 표준: 반시계 방향
                const [showVectors, setShowVectors] = useState(true); // 속도 벡터 표시

                // 물리량 정답 열람 상태 관리
                const [revealedItems, setRevealedItems] = useState({});

                // 퀴즈 답안 관리
                const [quizAnswers, setQuizAnswers] = useState({});

                const canvasRef = useRef(null);

                // 물리 파라미터
                const a = semiMajorAxis;
                const e = eccentricity;
                const b = a * Math.sqrt(Math.max(0.0001, 1 - e * e));
                const focusOffset = a * e;
                const rp = a * (1 - e); // 근일점 거리
                const ra = a * (1 + e); // 원일점 거리
                const speedRatio = (1 + e) / Math.max(0.01, 1 - e); // 속도 비 (근일점/원일점)
                const baseSpeed = 100;
                const dirSign = isCounterClockwise ? 1 : -1;

                // 정답 전체 토글
                const toggleAllRevealed = () => {
                    const allOpen = PHYSICAL_QUANTITIES.every(q => revealedItems[q.id]);
                    const next = {};
                    PHYSICAL_QUANTITIES.forEach(q => { next[q.id] = !allOpen; });
                    setRevealedItems(next);
                };

                const toggleItem = (id) => {
                    setRevealedItems(prev => ({ ...prev, [id]: !prev[id] }));
                };

                const handleSelectPreset = (preset) => {
                    setEccentricity(preset.e);
                    setSelectedPresetName(preset.name);
                };

                // 케플러 방정식 풀이 (면적 비례 계산용)
                const solveKepler = (M, eVal) => {
                    let E = M;
                    for (let i = 0; i < 15; i++) {
                        E = E - (E - eVal * Math.sin(E) - M) / (1 - eVal * Math.cos(E));
                    }
                    return E;
                };

                const getTrueAnomaly = (M, eVal) => {
                    const E = solveKepler(M, eVal);
                    return 2 * Math.atan2(Math.sqrt(1 + eVal) * Math.sin(E / 2), Math.sqrt(Math.max(0.0001, 1 - eVal)) * Math.cos(E / 2));
                };

                // 실시간 궤도 애니메이션
                useEffect(() => {
                    let animationFrame;
                    if (isPlaying) {
                        const animate = () => {
                            setPlanetPos(prev => {
                                const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                                const deltaAngle = (baseSpeed / (r * r)) * 10;
                                const newAngle = prev.angle + deltaAngle;
                                const x = -focusOffset - r * Math.cos(newAngle);
                                const y = dirSign * r * Math.sin(newAngle);
                                return { x, y, angle: newAngle };
                            });
                            animationFrame = requestAnimationFrame(animate);
                        };
                        animate();
                    }
                    return () => cancelAnimationFrame(animationFrame);
                }, [isPlaying, e, a, isCounterClockwise]);

                useEffect(() => {
                    setPlanetPos(prev => {
                        const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                        const x = -focusOffset - r * Math.cos(prev.angle);
                        const y = dirSign * r * Math.sin(prev.angle);
                        return { ...prev, x, y };
                    });
                }, [e, a, isCounterClockwise]);

                // 캔버스 드로잉
                useEffect(() => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    const ctx = canvas.getContext('2d');
                    const width = canvas.width;
                    const height = canvas.height;
                    const centerX = width / 2;
                    const centerY = height / 2;

                    ctx.clearRect(0, 0, width, height);

                    // 1. 기준 좌표축
                    ctx.strokeStyle = '#1e293b';
                    ctx.lineWidth = 0.8;
                    ctx.beginPath();
                    ctx.moveTo(0, centerY); ctx.lineTo(width, centerY);
                    ctx.moveTo(centerX, 0); ctx.lineTo(centerX, height);
                    ctx.stroke();

                    // 2. 타원 궤도 선
                    ctx.beginPath();
                    ctx.ellipse(centerX, centerY, a, b, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = '#475569';
                    ctx.lineWidth = 1.8;
                    ctx.setLineDash([5, 5]);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 3. 부채꼴 그리기 함수
                    const drawSector = (startM, color, fillAlpha = 0.40) => {
                        ctx.beginPath();
                        ctx.fillStyle = color;
                        ctx.globalAlpha = fillAlpha;
                        ctx.moveTo(centerX - focusOffset, centerY);

                        const dM = (Math.PI * 2) / timeFraction;
                        const numSteps = 50;

                        for (let i = 0; i <= numSteps; i++) {
                            const currentM = startM + (dM * i) / numSteps;
                            const theta = getTrueAnomaly(currentM, e);
                            const r = a * (1 - e * e) / (1 + e * Math.cos(theta));
                            const x = -focusOffset - r * Math.cos(theta);
                            const y = dirSign * r * Math.sin(theta);
                            ctx.lineTo(centerX + x, centerY + y);
                        }

                        ctx.lineTo(centerX - focusOffset, centerY);
                        ctx.fill();
                        ctx.globalAlpha = 1.0;
                        ctx.strokeStyle = color;
                        ctx.lineWidth = 2;
                        ctx.stroke();
                    };

                    // 구역 A (근일점 부채꼴)
                    drawSector(-(Math.PI / timeFraction), '#ef4444');
                    // 구역 B (원일점 부채꼴)
                    drawSector(Math.PI - (Math.PI / timeFraction), '#3b82f6');

                    // 4. 태양 (초점)
                    ctx.beginPath();
                    ctx.arc(centerX - focusOffset, centerY, 15, 0, Math.PI * 2);
                    ctx.fillStyle = '#fbbf24';
                    ctx.shadowBlur = 22;
                    ctx.shadowColor = '#fbbf24';
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // 5. 근일점 & 원일점 마커
                    const periX = centerX - a;
                    const apheX = centerX + a;

                    ctx.font = 'bold 12px Pretendard, sans-serif';
                    ctx.fillStyle = '#ef4444';
                    ctx.fillText(`근일점 P (가장 가까움)`, periX - 25, centerY + 28);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fillText(`원일점 A (가장 멂)`, apheX - 35, centerY + 28);

                    // 6. 행성 연결선 및 행성 본체
                    const curX = centerX + planetPos.x;
                    const curY = centerY + planetPos.y;

                    ctx.beginPath();
                    ctx.moveTo(centerX - focusOffset, centerY);
                    ctx.lineTo(curX, curY);
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 1.4;
                    ctx.stroke();

                    // 속도 벡터 표시
                    if (showVectors) {
                        const rCur = Math.sqrt(Math.pow(planetPos.x + focusOffset, 2) + Math.pow(planetPos.y, 2));
                        const vMag = Math.sqrt(Math.max(10, 2 / rCur - 1 / a)) * 320;
                        
                        const normX = (planetPos.x) / (a * a);
                        const normY = (planetPos.y) / (b * b);
                        const tanX = dirSign * normY;
                        const tanY = -dirSign * normX;
                        const tanLen = Math.sqrt(tanX * tanX + tanY * tanY) || 1;
                        const vX = (tanX / tanLen) * vMag;
                        const vY = (tanY / tanLen) * vMag;

                        ctx.beginPath();
                        ctx.moveTo(curX, curY);
                        ctx.lineTo(curX + vX, curY + vY);
                        ctx.strokeStyle = '#f43f5e';
                        ctx.lineWidth = 3.5;
                        ctx.stroke();

                        // 화살표 머리
                        const headLen = 9;
                        const angle = Math.atan2(vY, vX);
                        ctx.beginPath();
                        ctx.moveTo(curX + vX, curY + vY);
                        ctx.lineTo(curX + vX - headLen * Math.cos(angle - Math.PI / 6), curY + vY - headLen * Math.sin(angle - Math.PI / 6));
                        ctx.lineTo(curX + vX - headLen * Math.cos(angle + Math.PI / 6), curY + vY - headLen * Math.sin(angle + Math.PI / 6));
                        ctx.fillStyle = '#f43f5e';
                        ctx.fill();

                        ctx.font = 'bold 11px Pretendard, sans-serif';
                        ctx.fillStyle = '#fda4af';
                        ctx.fillText(`속도 v`, curX + vX + 5, curY + vY);
                    }

                    // 행성
                    ctx.beginPath();
                    ctx.arc(curX, curY, 8.5, 0, Math.PI * 2);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2.5;
                    ctx.stroke();

                }, [planetPos, e, a, timeFraction, showVectors, isCounterClockwise]);

                return (
                    <div className="max-w-7xl mx-auto p-2 sm:p-4 flex flex-col gap-6 text-slate-800">

                        {/* 1. 상단 행성 프리셋 바 */}
                        <div className="bg-slate-900 text-white p-4 sm:p-5 rounded-3xl shadow-xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-2xl bg-red-600 flex items-center justify-center text-white shadow-md shadow-red-500/30">
                                    <Icon name="pie-chart" size={20} />
                                </div>
                                <div>
                                    <h4 className="font-extrabold text-sm sm:text-base flex items-center gap-2">
                                        케플러 제2법칙 (면적 속도 일정 법칙)
                                        <span className="text-xs px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 font-mono">
                                            {selectedPresetName} (e = {e.toFixed(4)})
                                        </span>
                                    </h4>
                                    <p className="text-xs text-slate-400">같은 시간(Δt) 동안 행성이 쓸고 지나가는 부채꼴의 면적을 직접 비교해 보세요.</p>
                                </div>
                            </div>
                            
                            <div className="flex flex-wrap items-center gap-2">
                                {CELESTIAL_PRESETS.map((p) => {
                                    const isSel = selectedPresetName === p.name;
                                    return (
                                        <button
                                            key={p.name}
                                            onClick={() => handleSelectPreset(p)}
                                            className={`px-3 py-1.5 rounded-xl font-bold text-xs transition-all flex items-center gap-1.5 border ${
                                                isSel 
                                                ? 'bg-red-600 text-white border-red-400 shadow-md shadow-red-600/40 scale-105' 
                                                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white'
                                            }`}
                                        >
                                            <span style={{ color: p.color }}>{p.symbol}</span>
                                            <span>{p.name}</span>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                        {/* 2. 메인 시뮬레이션 캔버스 & 컨트롤 */}
                        <div className="flex flex-col lg:flex-row gap-6">
                            
                            {/* 시뮬레이션 캔버스 뷰 */}
                            <div className="flex-1 space-y-4">
                                <div className="bg-slate-900 rounded-[2.5rem] overflow-hidden relative shadow-2xl border-[10px] border-slate-800 aspect-video flex items-center justify-center">
                                    <canvas ref={canvasRef} width={900} height={550} className="w-full h-auto" />

                                    {/* 상단 오버레이 인포 */}
                                    <div className="absolute top-5 left-5 flex flex-col gap-2">
                                        <div className="px-3.5 py-1.5 bg-black/70 backdrop-blur-md rounded-2xl border border-white/10 text-white text-[11px] font-black tracking-wider flex items-center gap-2">
                                            <div className="w-2.5 h-2.5 bg-red-500 rounded-full animate-ping"></div>
                                            <span>관측 시간: Δt = 전체 주기의 1/{timeFraction}</span>
                                        </div>
                                        <div className="px-3 py-1 bg-black/60 backdrop-blur-md rounded-xl border border-white/10 text-[11px] text-slate-300 font-medium">
                                            속력 비교: <span className="text-red-400 font-bold">근일점이 {speedRatio.toFixed(1)}배 더 빠름</span>
                                        </div>
                                    </div>

                                    {/* 하단 범례 */}
                                    <div className="absolute bottom-5 right-5 flex flex-wrap gap-2 text-white text-[11px] bg-black/75 px-3.5 py-2.5 rounded-2xl backdrop-blur-md border border-white/10 font-bold">
                                        <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-yellow-400 rounded-full"></div> 태양</div>
                                        <div className="flex items-center gap-1.5 text-red-400"><div className="w-3 h-3 bg-red-400/50 border border-red-400 rounded-sm"></div> 면적 A (근일점)</div>
                                        <div className="flex items-center gap-1.5 text-blue-400"><div className="w-3 h-3 bg-blue-400/50 border border-blue-400 rounded-sm"></div> 면적 B (원일점)</div>
                                    </div>
                                </div>

                                {/* 핵심 3대 요약 카드 (고등학교 핵심 요약) */}
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                    {/* 구역 A */}
                                    <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-3.5">
                                        <div className="w-12 h-12 bg-red-50 rounded-2xl flex items-center justify-center text-red-500 shrink-0 border border-red-100 italic font-black text-xl">A</div>
                                        <div className="space-y-0.5">
                                            <div className="flex items-center gap-1.5">
                                                <h5 className="font-extrabold text-slate-800 text-sm">근일점 구역</h5>
                                                <span className="px-2 py-0.5 bg-red-100 text-red-600 rounded-md text-[10px] font-bold">거리 최소</span>
                                            </div>
                                            <p className="text-xs text-slate-500">
                                                태양과 가까워 <strong>공전 속력이 가장 빠름 (v 최대)</strong>
                                            </p>
                                        </div>
                                    </div>

                                    {/* 구역 B */}
                                    <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-3.5">
                                        <div className="w-12 h-12 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shrink-0 border border-blue-100 italic font-black text-xl">B</div>
                                        <div className="space-y-0.5">
                                            <div className="flex items-center gap-1.5">
                                                <h5 className="font-extrabold text-slate-800 text-sm">원일점 구역</h5>
                                                <span className="px-2 py-0.5 bg-blue-100 text-blue-600 rounded-md text-[10px] font-bold">거리 최대</span>
                                            </div>
                                            <p className="text-xs text-slate-500">
                                                태양과 멀어서 <strong>공전 속력이 가장 느림 (v 최소)</strong>
                                            </p>
                                        </div>
                                    </div>

                                    {/* 결론 핵심 카드 */}
                                    <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-5 rounded-3xl shadow-md flex flex-col justify-center space-y-1">
                                        <div className="flex items-center justify-between text-xs text-emerald-400 font-bold">
                                            <span className="flex items-center gap-1"><Icon name="check-circle" size={14} /> 케플러 제2법칙 핵심</span>
                                            <span className="font-mono bg-emerald-500/20 px-2 py-0.5 rounded text-emerald-300">면적 A = 면적 B</span>
                                        </div>
                                        <p className="text-xs text-slate-300 leading-snug">
                                            같은 시간(Δt) 동안 쓸고 지나간 <strong>면적은 항상 동일</strong>합니다.
                                        </p>
                                        <div className="text-[11px] text-cyan-300 font-bold pt-0.5">
                                            💡 "가까우면 빠르고, 멀면 느리다!"
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 컨트롤 사이드바 */}
                            <div className="w-full lg:w-[340px] space-y-4">
                                <div className="bg-white p-6 rounded-[2rem] border border-slate-200 shadow-xl space-y-5">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-base font-extrabold text-slate-800 flex items-center gap-2">
                                            <div className="w-7 h-7 bg-red-600 rounded-xl flex items-center justify-center text-white shadow-md shadow-red-200">
                                                <Icon name="sliders" size={15} />
                                            </div>
                                            시뮬레이션 조절
                                        </h3>
                                        <span className="px-2.5 py-0.5 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold font-mono">
                                            {selectedPresetName}
                                        </span>
                                    </div>

                                    <div className="space-y-4">
                                        {/* 공전 제어 버튼 */}
                                        <div className="space-y-2">
                                            <button 
                                                onClick={() => setIsPlaying(!isPlaying)} 
                                                className={`w-full py-3.5 rounded-2xl font-black text-sm shadow-md transition-all flex items-center justify-center gap-2 ${
                                                    isPlaying 
                                                    ? 'bg-slate-800 text-white hover:bg-slate-900' 
                                                    : 'bg-red-600 text-white hover:bg-red-700 shadow-red-200'
                                                }`}
                                            >
                                                <Icon name={isPlaying ? "pause" : "play"} size={18} /> 
                                                {isPlaying ? '일시정지' : '공전 시뮬레이션 시작'}
                                            </button>
                                            <button 
                                                onClick={() => { setPlanetPos({ x: 0, y: 0, angle: 0 }); setIsPlaying(false); }} 
                                                className="w-full py-2 bg-slate-100 text-slate-600 rounded-xl font-bold text-xs hover:bg-slate-200 flex items-center justify-center gap-1.5 transition-colors"
                                            >
                                                <Icon name="refresh-cw" size={13} /> 처음 위치로 리셋
                                            </button>
                                        </div>

                                        {/* 이심률 슬라이더 */}
                                        <div className="space-y-1.5 pt-2 border-t border-slate-100">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-bold text-slate-600 flex items-center gap-1">
                                                    <Icon name="disc" size={13} /> 궤도 찌그러짐 (이심률 e)
                                                </label>
                                                <span className="px-2 py-0.5 bg-red-50 text-red-600 rounded font-mono font-bold text-xs">
                                                    {e.toFixed(3)}
                                                </span>
                                            </div>
                                            <input 
                                                type="range" 
                                                min="0.00" 
                                                max="0.70" 
                                                step="0.01" 
                                                value={e} 
                                                onChange={(ev) => { setEccentricity(parseFloat(ev.target.value)); setSelectedPresetName('사용자 정의'); }} 
                                                className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" 
                                            />
                                            <div className="flex justify-between text-[10px] text-slate-400">
                                                <span>0.0 (원)</span>
                                                <span>지구(0.017)</span>
                                                <span>0.7 (타원)</span>
                                            </div>
                                        </div>

                                        {/* 관측 시간 간격 (Δt) 버튼 그룹 */}
                                        <div className="space-y-1.5 pt-2 border-t border-slate-100">
                                            <label className="text-xs font-bold text-slate-600 flex items-center gap-1">
                                                <Icon name="clock" size={13} /> 부채꼴 시간 간격 (Δt)
                                            </label>
                                            <div className="grid grid-cols-4 gap-1.5">
                                                {[4, 6, 8, 12].map(n => (
                                                    <button
                                                        key={n}
                                                        onClick={() => setTimeFraction(n)}
                                                        className={`py-1.5 rounded-xl font-mono font-bold text-xs transition-all border ${
                                                            timeFraction === n
                                                            ? 'bg-red-500 text-white border-red-500 shadow-sm'
                                                            : 'bg-slate-50 text-slate-600 border-slate-200 hover:bg-slate-100'
                                                        }`}
                                                    >
                                                        T/{n}
                                                    </button>
                                                ))}
                                            </div>
                                        </div>

                                        {/* 공전 방향 및 벡터 토글 */}
                                        <div className="space-y-2 pt-2 border-t border-slate-100">
                                            <button 
                                                onClick={() => setIsCounterClockwise(!isCounterClockwise)} 
                                                className={`w-full p-2.5 rounded-xl border transition-all flex items-center justify-between font-bold text-xs ${
                                                    isCounterClockwise ? 'border-cyan-500 bg-cyan-50 text-cyan-800' : 'border-amber-500 bg-amber-50 text-amber-800'
                                                }`}
                                            >
                                                <span className="flex items-center gap-1.5">
                                                    <Icon name="rotate-ccw" size={14} /> 
                                                    방향: {isCounterClockwise ? '반시계 (표준)' : '시계 방향'}
                                                </span>
                                                <span className={`px-2 py-0.5 rounded text-[10px] font-extrabold ${isCounterClockwise ? 'bg-cyan-600 text-white' : 'bg-amber-600 text-white'}`}>
                                                    {isCounterClockwise ? 'CCW' : 'CW'}
                                                </span>
                                            </button>

                                            <button 
                                                onClick={() => setShowVectors(!showVectors)} 
                                                className={`w-full p-2.5 rounded-xl border transition-all flex items-center justify-between font-bold text-xs ${
                                                    showVectors ? 'border-rose-300 bg-rose-50 text-rose-700' : 'border-slate-200 text-slate-500'
                                                }`}
                                            >
                                                <span className="flex items-center gap-1.5">
                                                    <Icon name="arrow-up-right" size={14} /> 속도 벡터 화살표
                                                </span>
                                                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${showVectors ? 'bg-rose-500 text-white' : 'bg-slate-200 text-slate-500'}`}>
                                                    {showVectors ? 'ON' : 'OFF'}
                                                </span>
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* 3. [핵심 정리] 근일점 vs 원일점 5대 물리량 비교표 (클릭하여 정답 확인) */}
                        <div className="bg-white rounded-[2.5rem] p-5 sm:p-7 border border-slate-200 shadow-xl space-y-5">
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
                                <div>
                                    <div className="flex items-center gap-2 text-red-600 font-extrabold text-xs tracking-wider uppercase">
                                        <Icon name="check-square" size={16} /> 고등학교 핵심 필수 개념
                                    </div>
                                    <h3 className="text-lg sm:text-xl font-black text-slate-800 mt-0.5">
                                        근일점(P) vs 원일점(A) 5대 물리량 비교
                                    </h3>
                                    <p className="text-xs text-slate-500 mt-0.5">
                                        각 물리량이 어느 쪽에서 더 클지 직접 생각해 보고, 카드를 클릭하여 <strong>정답과 핵심 이유</strong>를 확인하세요.
                                    </p>
                                </div>

                                <button
                                    onClick={toggleAllRevealed}
                                    className="self-start sm:self-auto px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs flex items-center gap-1.5 transition-all shadow-sm"
                                >
                                    <Icon name={PHYSICAL_QUANTITIES.every(q => revealedItems[q.id]) ? "eye-off" : "eye"} size={14} />
                                    {PHYSICAL_QUANTITIES.every(q => revealedItems[q.id]) ? "모두 가리기" : "모든 정답 한 번에 보기"}
                                </button>
                            </div>

                            {/* 5대 물리량 카드 목록 */}
                            <div className="space-y-3">
                                {PHYSICAL_QUANTITIES.map((q, idx) => {
                                    const isOpen = !!revealedItems[q.id];
                                    return (
                                        <div 
                                            key={q.id}
                                            onClick={() => toggleItem(q.id)}
                                            className={`rounded-2xl border-2 transition-all p-4 cursor-pointer ${
                                                isOpen 
                                                ? 'border-indigo-200 bg-indigo-50/20 shadow-sm' 
                                                : 'border-slate-200 hover:border-slate-300 bg-white hover:bg-slate-50/50'
                                            }`}
                                        >
                                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                                                <div className="flex items-center gap-3">
                                                    <div className={`w-8 h-8 rounded-xl flex items-center justify-center font-black text-xs shrink-0 ${
                                                        isOpen ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'
                                                    }`}>
                                                        {idx + 1}
                                                    </div>
                                                    <div>
                                                        <div className="flex items-center gap-2 flex-wrap">
                                                            <h4 className="font-extrabold text-slate-800 text-sm sm:text-base">{q.name}</h4>
                                                            <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-mono text-xs font-bold">
                                                                <MathBox formula={q.formula} inline={true} />
                                                            </span>
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="flex items-center gap-2 self-end sm:self-auto">
                                                    {isOpen ? (
                                                        <div className="flex items-center gap-1.5 px-3 py-1 rounded-xl bg-indigo-100 text-indigo-900 font-extrabold text-xs border border-indigo-200">
                                                            <span>{q.comparison}</span>
                                                            <span className={`w-5 h-5 rounded-full ${q.badgeColor} flex items-center justify-center text-[11px] font-black`}>
                                                                {q.sign}
                                                            </span>
                                                        </div>
                                                    ) : (
                                                        <span className="px-3 py-1 rounded-xl bg-slate-100 text-indigo-600 hover:bg-indigo-50 font-bold text-xs flex items-center gap-1">
                                                            <Icon name="eye" size={13} /> 정답 확인
                                                        </span>
                                                    )}
                                                    <div className={`w-6 h-6 rounded-full flex items-center justify-center text-slate-400 transition-transform ${isOpen ? 'rotate-180' : ''}`}>
                                                        <Icon name="chevron-down" size={14} />
                                                    </div>
                                                </div>
                                            </div>

                                            {/* 클릭 시 펼쳐지는 고교 핵심 설명 */}
                                            {isOpen && (
                                                <div className="mt-3 pt-3 border-t border-indigo-100/80 text-xs sm:text-sm text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-100">
                                                    <span className="font-bold text-indigo-600 mr-1.5">💡 핵심 이유:</span>
                                                    {q.coreReason}
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* 4. 고등학교 내신/수능 대비 개념 확인 퀴즈 */}
                        <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-[2.5rem] p-5 sm:p-8 shadow-xl space-y-6">
                            <div className="border-b border-white/10 pb-4 space-y-1">
                                <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 text-xs font-bold">
                                    <Icon name="check-square" size={13} /> 자가 점검
                                </div>
                                <h3 className="text-lg sm:text-xl font-black text-white">
                                    케플러 제2법칙 핵심 확인 문제
                                </h3>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                {/* 문제 1 */}
                                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl space-y-3 flex flex-col justify-between">
                                    <div className="space-y-2">
                                        <span className="px-2 py-0.5 rounded bg-blue-500/20 text-blue-300 text-xs font-mono font-bold">Q1. 거리와 속력</span>
                                        <h4 className="font-bold text-white text-xs sm:text-sm leading-snug">
                                            어떤 행성의 근일점 거리가 1 AU, 속력이 30 km/s일 때, 원일점 거리가 2 AU라면 원일점에서의 공전 속력은?
                                        </h4>
                                    </div>
                                    <div className="space-y-1.5 pt-1">
                                        {[
                                            { text: '① 15 km/s', correct: true },
                                            { text: '② 30 km/s', correct: false },
                                            { text: '③ 60 km/s', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q1: opt.correct }))}
                                                className={`w-full p-2 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q1 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q1 !== undefined && opt.correct && <Icon name="check" size={13} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q1 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/50 p-2 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 거리와 공전 속력은 반비례하므로(r_p · v_p = r_a · v_a), 거리가 2배 멀어지면 속력은 1/2배(15 km/s)가 됩니다.
                                        </p>
                                    )}
                                </div>

                                {/* 문제 2 */}
                                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl space-y-3 flex flex-col justify-between">
                                    <div className="space-y-2">
                                        <span className="px-2 py-0.5 rounded bg-red-500/20 text-red-300 text-xs font-mono font-bold">Q2. 부채꼴 면적 비교</span>
                                        <h4 className="font-bold text-white text-xs sm:text-sm leading-snug">
                                            동일한 시간 Δt 동안 행성이 근일점 부근에서 쓸고 간 면적 A와 원일점 부근에서 쓸고 간 면적 B의 관계는?
                                        </h4>
                                    </div>
                                    <div className="space-y-1.5 pt-1">
                                        {[
                                            { text: '① A > B', correct: false },
                                            { text: '② A = B', correct: true },
                                            { text: '③ A < B', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q2: opt.correct }))}
                                                className={`w-full p-2 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q2 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q2 !== undefined && opt.correct && <Icon name="check" size={13} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q2 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/50 p-2 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 케플러 제2법칙(면적 속도 일정)에 따라 같은 시간 동안 쓸고 간 면적은 위치에 관계없이 항상 같습니다(A = B).
                                        </p>
                                    )}
                                </div>

                                {/* 문제 3 */}
                                <div className="bg-white/5 border border-white/10 p-5 rounded-2xl space-y-3 flex flex-col justify-between">
                                    <div className="space-y-2">
                                        <span className="px-2 py-0.5 rounded bg-purple-500/20 text-purple-300 text-xs font-mono font-bold">Q3. 물리량 변화</span>
                                        <h4 className="font-bold text-white text-xs sm:text-sm leading-snug">
                                            행성이 원일점에서 근일점으로 접근할 때, 크기가 증가하는 물리량은?
                                        </h4>
                                    </div>
                                    <div className="space-y-1.5 pt-1">
                                        {[
                                            { text: '① 중력, 공전 속력, 운동 에너지', correct: true },
                                            { text: '② 퍼텐셜 에너지, 역학적 에너지', correct: false },
                                            { text: '③ 역학적 에너지 전체', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q3: opt.correct }))}
                                                className={`w-full p-2 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q3 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q3 !== undefined && opt.correct && <Icon name="check" size={13} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q3 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/50 p-2 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 거리가 가까워지므로 중력·가속도·속력·운동에너지는 커지며, 퍼텐셜 에너지는 작아지고, 역학적 에너지는 일정하게 보존됩니다.
                                        </p>
                                    )}
                                </div>
                            </div>
                        </div>

                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerAreaSim />);
        </script>
    </body>
    </html>
    """

    components.html(react_code, height=1850, scrolling=True)

if __name__ == "__main__":
    run_sim()
