import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.title("🪐 케플러 제2법칙: 면적 속도 일정 법칙과 궤도 역학")
    st.markdown("""
    태양과 행성을 잇는 선분이 같은 시간 동안 쓸고 지나가는 **면적은 항상 일정(케플러 제2법칙: 면적 속도 일정 법칙)**합니다.
    
    부채꼴의 면적을 직접 비교해 보며 행성의 위치에 따른 공전 속도를 관찰하고, **근일점과 원일점에서의 중력, 중력가속도, 운동 에너지, 퍼텐셜 에너지, 역학적 에너지의 변화**를 인터랙티브하게 비교·탐구해 보세요.
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
                background: #3b82f6;
                cursor: pointer;
                border: 2px solid white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .katex-display { margin: 0.4em 0 !important; }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef, useMemo } = React;

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

            // 대표 천체 프리셋
            const CELESTIAL_PRESETS = [
                { name: '지구', e: 0.0167, a: 140, desc: '거의 원형 (속도 편차 3.4%)', color: '#3b82f6', symbol: '⊕' },
                { name: '화성', e: 0.0934, a: 140, desc: '케플러 타원 발견 단서 (속도 편차 20.6%)', color: '#ef4444', symbol: '♂' },
                { name: '수성', e: 0.2056, a: 140, desc: '행성 중 최대 이심률 (속도 편차 51.8%)', color: '#94a3b8', symbol: '☿' },
                { name: '가상 타원', e: 0.5000, a: 140, desc: '극적인 속도 변화 체감 (속도 편차 300%)', color: '#a855f7', symbol: '🚀' },
                { name: '핼리 혜성', e: 0.7500, a: 150, desc: '초극단 타원 궤도 (속도 편차 700%)', color: '#06b6d4', symbol: '☄️' }
            ];

            // 5가지 물리량 비교 데이터 (중력, 중력가속도, 운동에너지, 퍼텐셜에너지, 역학적에너지)
            const PHYSICAL_QUANTITIES = [
                {
                    id: 'gravity',
                    name: '중력 (만유인력)',
                    symbol: 'F',
                    formula: 'F = G \\frac{Mm}{r^2}',
                    perihelion: '최대 (F_p)',
                    aphelion: '최소 (F_a)',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    ratioFormula: '\\frac{F_p}{F_a} = \\left(\\frac{r_a}{r_p}\\right)^2 = \\left(\\frac{1+e}{1-e}\\right)^2',
                    explanation: '뉴턴의 만유인력 법칙에 의해 중력은 중심체(태양)와 행성 사이의 거리 제곱에 반비례(F ∝ 1/r²)합니다. 근일점은 거리가 가장 가깝고 원일점은 가장 멀기 때문에, 중력의 크기는 근일점에서 최대, 원일점에서 최소가 됩니다.'
                },
                {
                    id: 'accel',
                    name: '중력 가속도',
                    symbol: 'g',
                    formula: 'g = \\frac{F}{m} = G \\frac{M}{r^2}',
                    perihelion: '최대 (g_p)',
                    aphelion: '최소 (g_a)',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    ratioFormula: '\\frac{g_p}{g_a} = \\left(\\frac{r_a}{r_p}\\right)^2 = \\left(\\frac{1+e}{1-e}\\right)^2',
                    explanation: '뉴턴 제2법칙(F = ma)에 의해 행성의 중력가속도는 g = F/m = GM/r²입니다. 행성의 질량과 무관하게 거리의 제곱에 반비례하므로, 중력가속도 역시 근일점에서 최대, 원일점에서 최소입니다. 근일점에서 궤도 곡률을 꺾는 구심 가속도가 가장 강력합니다.'
                },
                {
                    id: 'kinetic',
                    name: '운동 에너지',
                    symbol: 'E_k',
                    formula: 'E_k = \\frac{1}{2} m v^2',
                    perihelion: '최대 (E_{k,p})',
                    aphelion: '최소 (E_{k,a})',
                    comparison: '근일점 > 원일점',
                    sign: '>',
                    ratioFormula: '\\frac{E_{k,p}}{E_{k,a}} = \\left(\\frac{v_p}{v_a}\\right)^2 = \\left(\\frac{1+e}{1-e}\\right)^2',
                    explanation: '케플러 제2법칙(면적 속도 일정)과 각운동량 보존(L = m r_p v_p = m r_a v_a)에 의해 거리가 가까운 근일점에서 공전 속력이 가장 빠르고(v_p > v_a), 원일점에서 가장 느립니다. 운동 에너지는 속력의 제곱에 비례(E_k ∝ v²)하므로 근일점에서 최대, 원일점에서 최소입니다.'
                },
                {
                    id: 'potential',
                    name: '만유인력 퍼텐셜 에너지',
                    symbol: 'E_p',
                    formula: 'E_p = -G \\frac{Mm}{r}',
                    perihelion: '최소 (가장 작음)',
                    aphelion: '최대 (가장 큼)',
                    comparison: '근일점 < 원일점',
                    sign: '<',
                    ratioFormula: 'E_{p,p} < E_{p,a} \\quad (\\because \\text{음수 부호})',
                    explanation: '★ [가장 주의해야 할 개념!] 만유인력 위치 에너지는 무한대(r → ∞)를 0으로 정의하므로 항상 음수(-)입니다. 거리가 가까운 근일점에서는 음수의 절댓값이 커지므로(-100 < -50) 퍼텐셜 에너지가 최소(가장 작음)가 되고, 거리가 먼 원일점에서는 0에 더 가까워지므로 퍼텐셜 에너지가 최대(가장 큼)가 됩니다.'
                },
                {
                    id: 'mechanical',
                    name: '역학적 에너지',
                    symbol: 'E',
                    formula: 'E = E_k + E_p = -G \\frac{Mm}{2a}',
                    perihelion: '일정 (보존)',
                    aphelion: '일정 (보존)',
                    comparison: '근일점 = 원일점',
                    sign: '=',
                    ratioFormula: 'E_p = E_a = -G\\frac{Mm}{2a} = \\text{constant}',
                    explanation: '행성에 작용하는 유일한 힘은 보존력인 만유인력뿐이므로, 궤도 상의 모든 지점에서 총 역학적 에너지는 항상 일정하게 보존됩니다. 총 에너지는 오직 타원의 장반경 a에 의해서만 결정됩니다. 근일점에서 원일점으로 갈 때 운동 에너지가 퍼텐셜 에너지로 전환되고, 원일점에서 근일점으로 갈 때는 퍼텐셜 에너지가 운동 에너지로 전환됩니다.'
                }
            ];

            const KeplerAreaSim = () => {
                const [eccentricity, setEccentricity] = useState(0.50);
                const [semiMajorAxis, setSemiMajorAxis] = useState(140);
                const [isPlaying, setIsPlaying] = useState(false);
                const [timeFraction, setTimeFraction] = useState(8);
                const [planetPos, setPlanetPos] = useState({ x: 0, y: 0, angle: 0 });
                const [selectedPresetName, setSelectedPresetName] = useState('가상 타원');
                const [isCounterClockwise, setIsCounterClockwise] = useState(true); // 천문학 표준: 반시계 방향 (북극 조망 서→동)
                
                // 부채꼴 표시 옵션
                const [showSectorA, setShowSectorA] = useState(true); // 근일점 부채꼴
                const [showSectorB, setShowSectorB] = useState(true); // 원일점 부채꼴
                const [showSectorC, setShowSectorC] = useState(false); // 임의 위치 부채꼴
                const [sectorCAngle, setSectorCAngle] = useState(Math.PI / 2); // C 시작 각도
                const [showVectors, setShowVectors] = useState(true); // 속도 벡터 표시 여부

                // 물리량 정답 열람 상태 관리 (아이디별 toggle)
                const [revealedItems, setRevealedItems] = useState({});

                // 퀴즈 상태 관리
                const [quizAnswers, setQuizAnswers] = useState({});
                const [quizResults, setQuizResults] = useState({});

                const canvasRef = useRef(null);

                // 파라미터 계산
                const a = semiMajorAxis;
                const e = eccentricity;
                const b = a * Math.sqrt(Math.max(0.0001, 1 - e * e));
                const focusOffset = a * e;
                const rp = a * (1 - e); // 근일점 거리
                const ra = a * (1 + e); // 원일점 거리
                const speedRatio = (1 + e) / Math.max(0.01, 1 - e); // v_p / v_a
                const forceRatio = Math.pow(speedRatio, 2); // F_p / F_a
                const baseSpeed = 100;
                const dirSign = isCounterClockwise ? 1 : -1;

                // 전체 열기 / 닫기
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
                    setSemiMajorAxis(preset.a);
                    setSelectedPresetName(preset.name);
                };

                // 케플러 방정식 풀이 (Mean Anomaly -> True Anomaly)
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

                // 실시간 궤도 애니메이션 (천문학 표준 반시계 방향 / 시계 방향 전환 지원)
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

                    // 2. 타원 궤도
                    ctx.beginPath();
                    ctx.ellipse(centerX, centerY, a, b, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = '#475569';
                    ctx.lineWidth = 1.8;
                    ctx.setLineDash([5, 5]);
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 3. 부채꼴 그리기 함수
                    const drawSector = (startM, color, label, fillAlpha = 0.45) => {
                        ctx.beginPath();
                        ctx.fillStyle = color;
                        ctx.globalAlpha = fillAlpha;
                        ctx.moveTo(centerX - focusOffset, centerY);

                        const dM = (Math.PI * 2) / timeFraction;
                        const numSteps = 60;

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

                    // 부채꼴 A (근일점)
                    if (showSectorA) {
                        drawSector(-(Math.PI / timeFraction), '#ef4444', '구역 A (근일점)');
                    }

                    // 부채꼴 B (원일점)
                    if (showSectorB) {
                        drawSector(Math.PI - (Math.PI / timeFraction), '#3b82f6', '구역 B (원일점)');
                    }

                    // 부채꼴 C (임의 위치)
                    if (showSectorC) {
                        drawSector(sectorCAngle, '#a855f7', '구역 C (임의 구간)');
                    }

                    // 4. 태양 (초점)
                    ctx.beginPath();
                    ctx.arc(centerX - focusOffset, centerY, 15, 0, Math.PI * 2);
                    ctx.fillStyle = '#fbbf24';
                    ctx.shadowBlur = 25;
                    ctx.shadowColor = '#fbbf24';
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // 5. 근일점 & 원일점 표시 마커
                    // 근일점 (가장 왼쪽 초점 기준 x축 방향)
                    const periX = centerX - a;
                    const apheX = centerX + a;

                    ctx.font = 'bold 11px Pretendard, sans-serif';
                    ctx.fillStyle = '#ef4444';
                    ctx.fillText(`근일점 P (rp=${rp.toFixed(0)}px)`, periX - 15, centerY + 30);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fillText(`원일점 A (ra=${ra.toFixed(0)}px)`, apheX - 45, centerY + 30);

                    // 6. 행성 연결선 및 행성 본체
                    const curX = centerX + planetPos.x;
                    const curY = centerY + planetPos.y;

                    ctx.beginPath();
                    ctx.moveTo(centerX - focusOffset, centerY);
                    ctx.lineTo(curX, curY);
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 1.4;
                    ctx.stroke();

                    // 속도 벡터 그리기 (옵션)
                    if (showVectors) {
                        // 현재 거리 r
                        const rCur = Math.sqrt(Math.pow(planetPos.x + focusOffset, 2) + Math.pow(planetPos.y, 2));
                        // 활력 방정식 기반 속력 크기 계산 (시각화용 스케일링)
                        const vMag = Math.sqrt(Math.max(10, 2 / rCur - 1 / a)) * 320;
                        
                        // 타원 접선 방향 벡터 (공전 방향과 완벽 동기화)
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
                    ctx.arc(curX, curY, 9, 0, Math.PI * 2);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2.5;
                    ctx.stroke();

                }, [planetPos, e, a, showSectorA, showSectorB, showSectorC, sectorCAngle, timeFraction, showVectors, isCounterClockwise]);

                return (
                    <div className="max-w-7xl mx-auto p-2 sm:p-4 flex flex-col gap-6 text-slate-800">

                        {/* 1. 상단 프리셋 바 */}
                        <div className="bg-slate-900 text-white p-5 rounded-3xl shadow-xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-2xl bg-red-600 flex items-center justify-center text-white shadow-md shadow-red-500/30">
                                    <Icon name="pie-chart" size={20} />
                                </div>
                                <div>
                                    <h4 className="font-extrabold text-sm sm:text-base flex items-center gap-2">
                                        케플러 제2법칙 (면적 속도 일정) 시뮬레이션
                                        <span className="text-xs px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-300 font-mono">
                                            {selectedPresetName} (e = {e.toFixed(4)})
                                        </span>
                                    </h4>
                                    <p className="text-xs text-slate-400">동일한 관측 시간(Δt) 동안 행성이 쓸고 지나가는 부채꼴의 면적을 직접 비교해 보세요.</p>
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
                                            <span className="text-[10px] opacity-75 font-mono">({p.e})</span>
                                        </button>
                                    );
                                })}
                            </div>
                        </div>

                        {/* 2. 메인 시뮬레이션 캔버스 & 컨트롤 사이드바 */}
                        <div className="flex flex-col lg:flex-row gap-6">
                            
                            {/* 시뮬레이션 캔버스 뷰 */}
                            <div className="flex-1 space-y-4">
                                <div className="bg-slate-900 rounded-[2.5rem] overflow-hidden relative shadow-2xl border-[10px] border-slate-800 aspect-video flex items-center justify-center">
                                    <canvas ref={canvasRef} width={900} height={550} className="w-full h-auto" />

                                    {/* 상단 오버레이 인포 */}
                                    <div className="absolute top-6 left-6 flex flex-col gap-2">
                                        <div className="px-4 py-2 bg-black/70 backdrop-blur-md rounded-2xl border border-white/10 text-white text-[11px] font-black uppercase tracking-widest flex items-center gap-2">
                                            <div className="w-2.5 h-2.5 bg-red-500 rounded-full animate-ping"></div>
                                            <span>제2법칙 검증 모드: Δt = T / {timeFraction}</span>
                                        </div>
                                        <div className="px-3 py-1.5 bg-black/60 backdrop-blur-md rounded-xl border border-white/10 text-[11px] text-slate-300 font-medium">
                                            속도비 <span className="text-red-400 font-bold font-mono">v_p / v_a = {speedRatio.toFixed(3)} 배</span> (근일점이 {((speedRatio - 1) * 100).toFixed(1)}% 빠름)
                                        </div>
                                        <div className="px-3 py-1.5 bg-black/60 backdrop-blur-md rounded-xl border border-white/10 text-[11px] text-slate-300 font-medium flex items-center gap-1.5">
                                            <Icon name="rotate-ccw" size={13} className="text-cyan-400" />
                                            <span>공전 방향:</span>
                                            <span className="text-cyan-400 font-bold font-mono">
                                                {isCounterClockwise ? '반시계 방향 (황도 북극 조망 서→동 표준)' : '시계 방향'}
                                            </span>
                                        </div>
                                    </div>

                                    {/* 하단 범례 */}
                                    <div className="absolute bottom-6 right-6 flex flex-wrap gap-3 text-white text-[11px] bg-black/75 p-4 rounded-2xl backdrop-blur-md border border-white/10 font-bold">
                                        <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-yellow-400 rounded-full shadow-[0_0_8px_#fbbf24]"></div> 태양(초점)</div>
                                        {showSectorA && <div className="flex items-center gap-1.5 text-red-400"><div className="w-3 h-3 bg-red-400/50 border border-red-400 rounded-sm"></div> 구역 A (근일점)</div>}
                                        {showSectorB && <div className="flex items-center gap-1.5 text-blue-400"><div className="w-3 h-3 bg-blue-400/50 border border-blue-400 rounded-sm"></div> 구역 B (원일점)</div>}
                                        {showSectorC && <div className="flex items-center gap-1.5 text-purple-400"><div className="w-3 h-3 bg-purple-400/50 border border-purple-400 rounded-sm"></div> 구역 C (임의)</div>}
                                        {showVectors && <div className="flex items-center gap-1.5 text-rose-400"><div className="w-4 h-1 bg-rose-500 rounded"></div> 속도 벡터(v)</div>}
                                    </div>
                                </div>

                                {/* 실시간 부채꼴 면적 비교 대시보드 */}
                                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                    {/* 구역 A */}
                                    <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-4">
                                        <div className="w-14 h-14 bg-red-50 rounded-2xl flex items-center justify-center text-red-500 shrink-0 border border-red-100 italic font-black text-xl">A</div>
                                        <div className="space-y-0.5">
                                            <div className="flex items-center gap-1.5">
                                                <h5 className="font-extrabold text-slate-800 text-sm">근일점 구역</h5>
                                                <span className="px-2 py-0.5 bg-red-100 text-red-600 rounded-md text-[10px] font-bold">거리 최소 / 속력 최대</span>
                                            </div>
                                            <p className="text-xs text-slate-500">거리는 가깝지만 각속도가 빨라 <strong>넓고 얇은 부채꼴</strong>을 형성합니다.</p>
                                        </div>
                                        <div className="ml-auto text-right">
                                            <span className="text-[10px] text-slate-400 uppercase font-black block">측정 면적</span>
                                            <span className="text-base font-black text-red-600 font-mono">100.0%</span>
                                        </div>
                                    </div>

                                    {/* 구역 B */}
                                    <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-4">
                                        <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shrink-0 border border-blue-100 italic font-black text-xl">B</div>
                                        <div className="space-y-0.5">
                                            <div className="flex items-center gap-1.5">
                                                <h5 className="font-extrabold text-slate-800 text-sm">원일점 구역</h5>
                                                <span className="px-2 py-0.5 bg-blue-100 text-blue-600 rounded-md text-[10px] font-bold">거리 최대 / 속력 최소</span>
                                            </div>
                                            <p className="text-xs text-slate-500">거리는 멀지만 각속도가 느려 <strong>좁고 긴 부채꼴</strong>을 형성합니다.</p>
                                        </div>
                                        <div className="ml-auto text-right">
                                            <span className="text-[10px] text-slate-400 uppercase font-black block">측정 면적</span>
                                            <span className="text-base font-black text-blue-600 font-mono">100.0%</span>
                                        </div>
                                    </div>

                                    {/* 결론 요약 카드 */}
                                    <div className="bg-gradient-to-br from-slate-900 to-indigo-950 text-white p-5 rounded-3xl shadow-md flex flex-col justify-center space-y-1.5 col-span-1 md:col-span-2 lg:col-span-1">
                                        <div className="flex items-center justify-between text-xs text-emerald-400 font-bold">
                                            <span className="flex items-center gap-1"><Icon name="check-circle" size={14} /> 면적 속도 일정 정리</span>
                                            <span className="font-mono">Area A = Area B</span>
                                        </div>
                                        <p className="text-xs text-slate-300 leading-relaxed">
                                            동일한 시간(Δt) 동안 태양-행성 선분이 쓸고 간 면적은 궤도 상의 위치에 관계없이 <strong>완벽하게 동일</strong>합니다.
                                        </p>
                                        <div className="pt-1 text-[11px] font-mono text-cyan-300 font-bold">
                                            <MathBox formula="\frac{dA}{dt} = \frac{1}{2} r^2 \frac{d\theta}{dt} = \frac{L}{2m} = \text{일정}" inline={true} />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* 컨트롤 사이드바 */}
                            <div className="w-full lg:w-[360px] space-y-5">
                                <div className="bg-white p-6 sm:p-7 rounded-[2rem] border border-slate-200 shadow-xl space-y-6">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-base font-extrabold text-slate-800 flex items-center gap-2.5">
                                            <div className="w-8 h-8 bg-red-600 rounded-xl flex items-center justify-center text-white shadow-md shadow-red-200">
                                                <Icon name="sliders" size={16} />
                                            </div>
                                            제2법칙 탐구 설정
                                        </h3>
                                        <span className="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold font-mono">
                                            {selectedPresetName}
                                        </span>
                                    </div>

                                    <div className="space-y-5">
                                        {/* 공전 방향 선택 토글 */}
                                        <div className="space-y-1">
                                            <button 
                                                onClick={() => setIsCounterClockwise(!isCounterClockwise)} 
                                                className={`w-full p-3 rounded-2xl border-2 transition-all flex items-center justify-between font-bold text-xs ${
                                                    isCounterClockwise ? 'border-cyan-500 bg-cyan-50 text-cyan-800 shadow-sm' : 'border-amber-500 bg-amber-50 text-amber-800 shadow-sm'
                                                }`}
                                            >
                                                <span className="flex items-center gap-2">
                                                    <Icon name="rotate-ccw" size={16} /> 
                                                    공전 방향: {isCounterClockwise ? '반시계 방향 (천문학 표준)' : '시계 방향'}
                                                </span>
                                                <span className={`px-2.5 py-0.5 rounded-md text-[10px] font-extrabold ${isCounterClockwise ? 'bg-cyan-600 text-white' : 'bg-amber-600 text-white'}`}>
                                                    {isCounterClockwise ? '표준 CCW' : 'CW'}
                                                </span>
                                            </button>
                                            <p className="text-[10px] text-slate-400 pl-1">
                                                {isCounterClockwise ? '황도 북극 상공에서 본 서→동 공전 표준입니다.' : '역방향(시계 방향)으로 관찰 중입니다.'}
                                            </p>
                                        </div>

                                        {/* 이심률 조절 */}
                                        <div className="space-y-2">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-black text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                                                    <Icon name="disc" size={14} /> 이심률 (e)
                                                </label>
                                                <span className="px-3 py-0.5 bg-red-50 text-red-600 border border-red-200 rounded-full font-mono font-black text-sm">
                                                    {e.toFixed(4)}
                                                </span>
                                            </div>
                                            <input 
                                                type="range" 
                                                min="0.00" 
                                                max="0.80" 
                                                step="0.005" 
                                                value={e} 
                                                onChange={(ev) => { setEccentricity(parseFloat(ev.target.value)); setSelectedPresetName('사용자 정의'); }} 
                                                className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" 
                                            />
                                            <p className="text-[10px] text-slate-400">이심률이 클수록 근일점과 원일점의 속도 차이가 극대화됩니다.</p>
                                        </div>

                                        {/* 관측 시간 조절 */}
                                        <div className="space-y-2 p-3 bg-red-50/70 rounded-2xl border border-red-100">
                                            <div className="flex justify-between items-center">
                                                <label className="text-[11px] font-black text-red-700 uppercase tracking-wider flex items-center gap-1">
                                                    <Icon name="clock" size={14} /> 관측 시간 구간 (Δt)
                                                </label>
                                                <span className="px-2.5 py-0.5 bg-red-100 text-red-700 rounded-lg font-mono font-black text-xs">
                                                    T / {timeFraction}
                                                </span>
                                            </div>
                                            <input 
                                                type="range" 
                                                min="4" 
                                                max="20" 
                                                step="1" 
                                                value={timeFraction} 
                                                onChange={(ev) => setTimeFraction(parseInt(ev.target.value))} 
                                                className="w-full h-2 bg-red-200 rounded-xl appearance-none cursor-pointer" 
                                            />
                                            <div className="flex justify-between text-[10px] text-red-400 font-mono">
                                                <span>T/4 (넓은 구간)</span>
                                                <span>T/20 (좁은 구간)</span>
                                            </div>
                                        </div>

                                        {/* 부채꼴 토글 버튼들 */}
                                        <div className="space-y-2 pt-1">
                                            <div className="grid grid-cols-2 gap-2">
                                                <button 
                                                    onClick={() => setShowSectorA(!showSectorA)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex items-center justify-center gap-1.5 font-bold text-xs ${
                                                        showSectorA ? 'border-red-500 bg-red-50 text-red-600' : 'border-slate-100 text-slate-400'
                                                    }`}
                                                >
                                                    <Icon name="pie-chart" size={14} /> 구역 A {showSectorA ? 'ON' : 'OFF'}
                                                </button>
                                                <button 
                                                    onClick={() => setShowSectorB(!showSectorB)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex items-center justify-center gap-1.5 font-bold text-xs ${
                                                        showSectorB ? 'border-blue-500 bg-blue-50 text-blue-600' : 'border-slate-100 text-slate-400'
                                                    }`}
                                                >
                                                    <Icon name="pie-chart" size={14} /> 구역 B {showSectorB ? 'ON' : 'OFF'}
                                                </button>
                                            </div>

                                            <div className="grid grid-cols-2 gap-2">
                                                <button 
                                                    onClick={() => setShowSectorC(!showSectorC)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex items-center justify-center gap-1.5 font-bold text-xs ${
                                                        showSectorC ? 'border-purple-500 bg-purple-50 text-purple-600' : 'border-slate-100 text-slate-400'
                                                    }`}
                                                >
                                                    <Icon name="plus-circle" size={14} /> 구역 C {showSectorC ? 'ON' : 'OFF'}
                                                </button>
                                                <button 
                                                    onClick={() => setShowVectors(!showVectors)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex items-center justify-center gap-1.5 font-bold text-xs ${
                                                        showVectors ? 'border-rose-500 bg-rose-50 text-rose-600' : 'border-slate-100 text-slate-400'
                                                    }`}
                                                >
                                                    <Icon name="arrow-up-right" size={14} /> 속도 벡터 {showVectors ? 'ON' : 'OFF'}
                                                </button>
                                            </div>
                                        </div>

                                        {/* 구역 C 각도 조절 슬라이더 */}
                                        {showSectorC && (
                                            <div className="p-3 bg-purple-50 rounded-2xl border border-purple-100 space-y-1.5 animate-in fade-in duration-200">
                                                <div className="flex justify-between items-center text-xs font-bold text-purple-700">
                                                    <span>구역 C 위치 회전</span>
                                                    <span className="font-mono">{(sectorCAngle * 180 / Math.PI).toFixed(0)}°</span>
                                                </div>
                                                <input 
                                                    type="range" 
                                                    min="0" 
                                                    max={Math.PI * 2} 
                                                    step="0.05" 
                                                    value={sectorCAngle} 
                                                    onChange={(ev) => setSectorCAngle(parseFloat(ev.target.value))} 
                                                    className="w-full h-1.5 bg-purple-200 rounded-xl appearance-none cursor-pointer" 
                                                />
                                            </div>
                                        )}

                                        {/* 속도 및 거리 수치 비교 카드 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 space-y-2 text-xs">
                                            <div className="font-extrabold text-slate-700 flex items-center justify-between pb-1 border-b border-slate-200/60">
                                                <span>근일점 vs 원일점 속도 분석</span>
                                                <span className="text-[10px] text-red-600 font-mono">r_p · v_p = r_a · v_a</span>
                                            </div>
                                            <div className="grid grid-cols-2 gap-2 text-slate-600 font-mono">
                                                <div>근일점 거리 (r_p): <span className="font-bold text-red-600">{rp.toFixed(1)} px</span></div>
                                                <div>원일점 거리 (r_a): <span className="font-bold text-blue-600">{ra.toFixed(1)} px</span></div>
                                                <div>거리 비율: <span className="font-bold text-slate-800">1 : {((1+e)/(1-e)).toFixed(2)}</span></div>
                                                <div>속도 비율: <span className="font-bold text-rose-600">{((1+e)/(1-e)).toFixed(2)} : 1</span></div>
                                            </div>
                                            <div className="pt-1 text-[11px] text-slate-500">
                                                근일점 공전 속력은 원일점보다 <strong className="text-red-600">{((speedRatio - 1) * 100).toFixed(1)}%</strong> 빠릅니다.
                                            </div>
                                        </div>

                                        {/* 시뮬레이션 동작 제어 버튼 */}
                                        <div className="space-y-2 pt-2 border-t border-slate-100">
                                            <button 
                                                onClick={() => setIsPlaying(!isPlaying)} 
                                                className={`w-full py-4 rounded-2xl font-black text-base shadow-lg transition-all flex items-center justify-center gap-2.5 ${
                                                    isPlaying 
                                                    ? 'bg-slate-800 text-white hover:bg-slate-900' 
                                                    : 'bg-red-600 text-white hover:bg-red-700 shadow-red-200'
                                                }`}
                                            >
                                                <Icon name={isPlaying ? "pause" : "play"} size={20} /> 
                                                {isPlaying ? '시뮬레이션 일시정지' : '공전 시뮬레이션 시작'}
                                            </button>
                                            <button 
                                                onClick={() => { setPlanetPos({ x: 0, y: 0, angle: 0 }); setIsPlaying(false); }} 
                                                className="w-full py-2.5 bg-slate-50 text-slate-500 rounded-xl font-bold text-xs hover:bg-slate-100 flex items-center justify-center gap-1.5 transition-colors"
                                            >
                                                <Icon name="refresh-cw" size={14} /> 궤도 위치 초기화
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* 3. [핵심] 근일점 vs 원일점 5가지 물리량 비교 표 (클릭하여 정답 및 설명 확인) */}
                        <div className="bg-white rounded-[2.5rem] p-6 sm:p-8 border border-slate-200 shadow-xl space-y-6">
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-100">
                                <div>
                                    <div className="flex items-center gap-2 text-red-600 font-extrabold text-xs tracking-wider uppercase">
                                        <Icon name="help-circle" size={16} /> 케플러 제2법칙 핵심 개념 탐구
                                    </div>
                                    <h3 className="text-xl font-black text-slate-800 mt-1">
                                        근일점(P) vs 원일점(A) 주요 물리량 비교 표
                                    </h3>
                                    <p className="text-xs sm:text-sm text-slate-500 mt-1">
                                        중력, 중력가속도, 운동 에너지, 퍼텐셜 에너지, 역학적 에너지가 
                                        <strong> 어느 지점에서 더 큰지 직접 생각해 본 뒤, [정답 및 설명 확인] </strong> 버튼을 눌러 정답과 상세 해설을 확인하세요.
                                    </p>
                                </div>

                                <button
                                    onClick={toggleAllRevealed}
                                    className="self-start sm:self-auto px-4 py-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-xs flex items-center gap-2 transition-all shadow-sm"
                                >
                                    <Icon name={PHYSICAL_QUANTITIES.every(q => revealedItems[q.id]) ? "eye-off" : "eye"} size={16} />
                                    {PHYSICAL_QUANTITIES.every(q => revealedItems[q.id]) ? "모두 가리기" : "모든 정답 및 해설 열람"}
                                </button>
                            </div>

                            {/* 물리량 비교 인터랙티브 아코디언 테이블 */}
                            <div className="space-y-4">
                                {PHYSICAL_QUANTITIES.map((q, idx) => {
                                    const isOpen = !!revealedItems[q.id];
                                    return (
                                        <div 
                                            key={q.id}
                                            className={`rounded-3xl border-2 transition-all overflow-hidden ${
                                                isOpen 
                                                ? 'border-indigo-200 bg-indigo-50/20 shadow-md' 
                                                : 'border-slate-200 hover:border-slate-300 bg-white'
                                            }`}
                                        >
                                            {/* 메인 행 요약 바 */}
                                            <div 
                                                onClick={() => toggleItem(q.id)}
                                                className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer"
                                            >
                                                <div className="flex items-center gap-4">
                                                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center font-black text-sm shrink-0 ${
                                                        isOpen ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' : 'bg-slate-100 text-slate-600'
                                                    }`}>
                                                        {idx + 1}
                                                    </div>
                                                    <div>
                                                        <div className="flex items-center gap-2.5 flex-wrap">
                                                            <h4 className="font-black text-slate-800 text-base">{q.name}</h4>
                                                            <span className="px-2.5 py-0.5 rounded-md bg-slate-100 text-slate-600 font-mono text-xs font-bold">
                                                                <MathBox formula={q.formula} inline={true} />
                                                            </span>
                                                        </div>
                                                        <p className="text-xs text-slate-400 mt-0.5">
                                                            근일점({q.perihelion}) vs 원일점({q.aphelion})의 크기 관계를 비교하세요.
                                                        </p>
                                                    </div>
                                                </div>

                                                <div className="flex items-center gap-3 self-end md:self-auto">
                                                    {isOpen ? (
                                                        <div className="flex items-center gap-2 px-4 py-2 rounded-2xl bg-indigo-100 text-indigo-900 font-black text-sm border border-indigo-200 animate-in fade-in duration-300">
                                                            <span>정답: {q.comparison}</span>
                                                            <span className="w-6 h-6 rounded-full bg-indigo-600 text-white flex items-center justify-center text-xs">
                                                                {q.sign}
                                                            </span>
                                                        </div>
                                                    ) : (
                                                        <button 
                                                            onClick={(e) => { e.stopPropagation(); toggleItem(q.id); }}
                                                            className="px-4 py-2 rounded-2xl bg-slate-100 hover:bg-indigo-600 hover:text-white text-indigo-600 font-extrabold text-xs flex items-center gap-1.5 transition-all shadow-sm"
                                                        >
                                                            <Icon name="eye" size={14} /> 정답 및 설명 확인
                                                        </button>
                                                    )}
                                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center transition-transform duration-300 ${isOpen ? 'rotate-180 bg-indigo-600 text-white' : 'bg-slate-100 text-slate-400'}`}>
                                                        <Icon name="chevron-down" size={16} />
                                                    </div>
                                                </div>
                                            </div>

                                            {/* 펼쳐지는 상세 해설 및 수식 유도 박스 */}
                                            {isOpen && (
                                                <div className="px-6 pb-6 pt-2 border-t border-indigo-100 bg-white space-y-4 animate-in slide-in-from-top-2 duration-300">
                                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                                                        <div className="p-4 rounded-2xl bg-indigo-50/70 border border-indigo-100 space-y-1">
                                                            <span className="text-[11px] font-extrabold text-indigo-600 uppercase tracking-wider block">
                                                                수학적 비율 및 관계식
                                                            </span>
                                                            <div className="font-mono text-sm text-indigo-950 font-bold">
                                                                <MathBox formula={q.ratioFormula} />
                                                            </div>
                                                        </div>

                                                        <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1">
                                                            <span className="text-[11px] font-extrabold text-slate-500 uppercase tracking-wider block">
                                                                현재 시뮬레이션 수치 ({selectedPresetName})
                                                            </span>
                                                            <div className="text-xs text-slate-700 font-mono space-y-0.5">
                                                                {q.id === 'gravity' || q.id === 'accel' ? (
                                                                    <div>근일점이 원일점보다 <strong className="text-red-600">{forceRatio.toFixed(2)}배</strong> 큽니다.</div>
                                                                ) : q.id === 'kinetic' ? (
                                                                    <div>근일점이 원일점보다 <strong className="text-rose-600">{forceRatio.toFixed(2)}배</strong> 큽니다.</div>
                                                                ) : q.id === 'potential' ? (
                                                                    <div>근일점 거리가 가까워 음수의 크기가 더 큽니다 <strong className="text-blue-600">(퍼텐셜 에너지는 최소)</strong>.</div>
                                                                ) : (
                                                                    <div>궤도 장반경 a가 변하지 않으므로 <strong className="text-emerald-600">100% 동일(보존)</strong>합니다.</div>
                                                                )}
                                                            </div>
                                                        </div>
                                                    </div>

                                                    <div className="p-4 rounded-2xl bg-slate-900 text-white space-y-2">
                                                        <div className="flex items-center gap-2 text-xs font-bold text-amber-400">
                                                            <Icon name="info" size={15} /> 물리적 이유 및 핵심 원리
                                                        </div>
                                                        <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                                                            {q.explanation}
                                                        </p>
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* 4. 케플러 제2법칙 개념 실전 연습 퀴즈 */}
                        <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 text-white rounded-[2.5rem] p-6 sm:p-10 shadow-2xl space-y-8">
                            <div className="border-b border-white/10 pb-5 space-y-2">
                                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/20 text-red-300 text-xs font-extrabold uppercase tracking-widest border border-red-400/30">
                                    <Icon name="check-square" size={14} /> 개념 확인 실전 연습
                                </div>
                                <h3 className="text-xl sm:text-2xl font-black text-white">
                                    케플러 제2법칙 및 궤도 역학 자가 점검 퀴즈
                                </h3>
                                <p className="text-xs sm:text-sm text-slate-300">
                                    문제를 풀고 선택지를 클릭하면 즉시 정답 여부와 물리적 해설을 확인할 수 있습니다.
                                </p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                {/* 문제 1 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 flex flex-col justify-between">
                                    <div className="space-y-3">
                                        <span className="px-2.5 py-0.5 rounded-md bg-blue-500/20 text-blue-300 text-xs font-mono font-bold">문제 01</span>
                                        <h4 className="font-extrabold text-white text-sm leading-snug">
                                            어떤 행성의 근일점 거리가 1 AU이고, 원일점 거리가 2 AU입니다. 근일점에서의 공전 속력이 30 km/s일 때, 원일점에서의 공전 속력은?
                                        </h4>
                                    </div>
                                    <div className="space-y-2 pt-2">
                                        {[
                                            { text: '① 15 km/s', correct: true },
                                            { text: '② 30 km/s', correct: false },
                                            { text: '③ 60 km/s', correct: false },
                                            { text: '④ 7.5 km/s', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q1: opt.correct }))}
                                                className={`w-full p-2.5 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q1 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : quizAnswers.q1 === false
                                                    ? 'bg-white/10 text-slate-300'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q1 !== undefined && opt.correct && <Icon name="check" size={14} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q1 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 각운동량 보존(r_p · v_p = r_a · v_a)에 의해 거리와 속력은 반비례합니다. 거리가 2배이므로 속력은 1/2배인 15 km/s입니다.
                                        </p>
                                    )}
                                </div>

                                {/* 문제 2 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 flex flex-col justify-between">
                                    <div className="space-y-3">
                                        <span className="px-2.5 py-0.5 rounded-md bg-red-500/20 text-red-300 text-xs font-mono font-bold">문제 02</span>
                                        <h4 className="font-extrabold text-white text-sm leading-snug">
                                            행성이 근일점 부근을 지날 때와 원일점 부근을 지날 때, 동일한 시간 Δt 동안 태양과 행성을 잇는 선분이 훑고 지나간 면적 A_p와 A_a의 대소 관계는?
                                        </h4>
                                    </div>
                                    <div className="space-y-2 pt-2">
                                        {[
                                            { text: '① A_p > A_a', correct: false },
                                            { text: '② A_p = A_a', correct: true },
                                            { text: '③ A_p < A_a', correct: false },
                                            { text: '④ 이심률에 따라 달라짐', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q2: opt.correct }))}
                                                className={`w-full p-2.5 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q2 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : quizAnswers.q2 === false
                                                    ? 'bg-white/10 text-slate-300'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q2 !== undefined && opt.correct && <Icon name="check" size={14} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q2 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 케플러 제2법칙(면적 속도 일정 법칙)에 의해 동일한 시간 동안 훑고 지나간 면적은 궤도 상의 위치에 관계없이 항상 같습니다(A_p = A_a).
                                        </p>
                                    )}
                                </div>

                                {/* 문제 3 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 flex flex-col justify-between">
                                    <div className="space-y-3">
                                        <span className="px-2.5 py-0.5 rounded-md bg-purple-500/20 text-purple-300 text-xs font-mono font-bold">문제 03</span>
                                        <h4 className="font-extrabold text-white text-sm leading-snug">
                                            행성이 원일점에서 근일점으로 이동할 때, 값이 증가하는 물리량만을 짝지은 것은?
                                        </h4>
                                    </div>
                                    <div className="space-y-2 pt-2">
                                        {[
                                            { text: '① 중력, 공전 속력, 운동 에너지', correct: true },
                                            { text: '② 퍼텐셜 에너지, 역학적 에너지', correct: false },
                                            { text: '③ 중력, 퍼텐셜 에너지, 역학적 에너지', correct: false },
                                            { text: '④ 공전 주기, 가속도, 역학적 에너지', correct: false }
                                        ].map((opt, i) => (
                                            <button
                                                key={i}
                                                onClick={() => setQuizAnswers(prev => ({ ...prev, q3: opt.correct }))}
                                                className={`w-full p-2.5 rounded-xl text-xs font-bold transition-all text-left flex items-center justify-between ${
                                                    quizAnswers.q3 !== undefined && opt.correct
                                                    ? 'bg-emerald-600 text-white'
                                                    : quizAnswers.q3 === false
                                                    ? 'bg-white/10 text-slate-300'
                                                    : 'bg-white/10 text-slate-300 hover:bg-white/20'
                                                }`}
                                            >
                                                <span>{opt.text}</span>
                                                {quizAnswers.q3 !== undefined && opt.correct && <Icon name="check" size={14} />}
                                            </button>
                                        ))}
                                    </div>
                                    {quizAnswers.q3 !== undefined && (
                                        <p className="text-[11px] text-emerald-300 bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-500/30">
                                            <strong>해설:</strong> 원일점에서 근일점으로 갈수록 거리가 가까워지므로 중력·가속도·속력·운동에너지는 증가하고, 퍼텐셜 에너지는 감소하며, 역학적 에너지는 보존(일정)됩니다.
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

    components.html(react_code, height=2300, scrolling=True)

if __name__ == "__main__":
    run_sim()
