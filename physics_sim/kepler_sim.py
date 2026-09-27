import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    
    st.title("🪐 케플러 제1, 2법칙: 타원 궤도와 면적 속도 일정 법칙")
    st.markdown("""
    행성은 태양을 한 초점으로 하는 **타원 궤도(케플러 제1법칙)**를 따라 공전하며, 태양과 행성을 잇는 선분이 같은 시간 동안 훑고 지나가는 **면적은 항상 일정(케플러 제2법칙)**합니다.
    
    실제 태양계 행성들의 공전 궤도 이심률($e$) 데이터를 직접 시뮬레이터에 적용해 보고, **"태양계 행성의 이심률은 매우 작아서 근사적으로 원운동으로 볼 수 있다"**는 물리학적 명제의 수학적 구조와 과학사적·물리학적 의미를 심층 탐구해 보세요.
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
            .glow-cyan {
                box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
            }
            .katex-display {
                margin: 0.5em 0 !important;
            }
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

            // 8개 행성 공전 궤도 데이터베이스 (제공된 표 기반)
            const PLANET_DATA = [
                {
                    name: '수성',
                    en: 'Mercury',
                    symbol: '☿',
                    e: 0.2056,
                    desc: '8개 행성 중 가장 큼 (최대 이각 편차가 큰 이유)',
                    color: '#94a3b8',
                    tag: '최대 이심률',
                    tagBg: 'bg-amber-100 text-amber-800 border-amber-300'
                },
                {
                    name: '금성',
                    en: 'Venus',
                    symbol: '♀',
                    e: 0.0068,
                    desc: '8개 행성 중 가장 작음 (가장 원형에 가까움)',
                    color: '#f59e0b',
                    tag: '가장 원형',
                    tagBg: 'bg-emerald-100 text-emerald-800 border-emerald-300'
                },
                {
                    name: '지구',
                    en: 'Earth',
                    symbol: '⊕',
                    e: 0.0167,
                    desc: '매우 원형에 가까움',
                    color: '#3b82f6',
                    tag: '인류의 거주지',
                    tagBg: 'bg-blue-100 text-blue-800 border-blue-300'
                },
                {
                    name: '화성',
                    en: 'Mars',
                    symbol: '♂',
                    e: 0.0934,
                    desc: '케플러가 타원 궤도 법칙을 발견하는 결정적 계기가 됨',
                    color: '#ef4444',
                    tag: '케플러의 단서',
                    tagBg: 'bg-red-100 text-red-800 border-red-300'
                },
                {
                    name: '목성',
                    en: 'Jupiter',
                    symbol: '♃',
                    e: 0.0484,
                    desc: '완만한 타원',
                    color: '#d97706',
                    tag: '완만한 타원',
                    tagBg: 'bg-orange-100 text-orange-800 border-orange-300'
                },
                {
                    name: '토성',
                    en: 'Saturn',
                    symbol: '♄',
                    e: 0.0542,
                    desc: '완만한 타원',
                    color: '#ca8a04',
                    tag: '완만한 타원',
                    tagBg: 'bg-yellow-100 text-yellow-800 border-yellow-300'
                },
                {
                    name: '천왕성',
                    en: 'Uranus',
                    symbol: '♅',
                    e: 0.0472,
                    desc: '완만한 타원',
                    color: '#06b6d4',
                    tag: '완만한 타원',
                    tagBg: 'bg-cyan-100 text-cyan-800 border-cyan-300'
                },
                {
                    name: '해왕성',
                    en: 'Neptune',
                    symbol: '♆',
                    e: 0.0086,
                    desc: '금성 다음으로 원형에 가까움',
                    color: '#6366f1',
                    tag: '원형에 매우 가까움',
                    tagBg: 'bg-indigo-100 text-indigo-800 border-indigo-300'
                }
            ];

            const KeplerSim = () => {
                const [eccentricity, setEccentricity] = useState(0.50);
                const [semiMajorAxis, setSemiMajorAxis] = useState(140);
                const [isPlaying, setIsPlaying] = useState(false);
                const [showAxes, setShowAxes] = useState(true);
                const [showAreas, setShowAreas] = useState(false);
                const [showCircleComp, setShowCircleComp] = useState(false);
                const [timeFraction, setTimeFraction] = useState(8);
                const [planetPos, setPlanetPos] = useState({ x: 0, y: 0, angle: 0 });
                const [selectedPlanetName, setSelectedPlanetName] = useState('가상 타원');
                const canvasRef = useRef(null);

                // 시뮬레이션 물리 파라미터 계산
                const a = semiMajorAxis;
                const e = eccentricity;
                const b = a * Math.sqrt(Math.max(0.0001, 1 - e * e));
                const focusOffset = a * e;
                const bOverA = Math.sqrt(Math.max(0.0001, 1 - e * e));
                const distanceRatio = (1 + e) / Math.max(0.01, (1 - e));
                const shapeSimilarity = (bOverA * 100).toFixed(2);
                const baseSpeed = 100;

                // 행성 프리셋 선택 함수
                const handleSelectPlanet = (planet) => {
                    setEccentricity(planet.e);
                    setSelectedPlanetName(planet.name);
                };

                // 슬라이더 수동 변경 핸들러
                const handleManualEccentricity = (val) => {
                    setEccentricity(val);
                    const matched = PLANET_DATA.find(p => Math.abs(p.e - val) < 0.0005);
                    if (matched) {
                        setSelectedPlanetName(matched.name);
                    } else {
                        setSelectedPlanetName('사용자 정의');
                    }
                };

                useEffect(() => {
                    let animationFrame;
                    if (isPlaying) {
                        const animate = () => {
                            setPlanetPos(prev => {
                                const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                                const deltaAngle = (baseSpeed / (r * r)) * 10; 
                                const newAngle = prev.angle + deltaAngle;
                                const x = -focusOffset + r * Math.cos(newAngle + Math.PI);
                                const y = r * Math.sin(newAngle + Math.PI);
                                return { x, y, angle: newAngle };
                            });
                            animationFrame = requestAnimationFrame(animate);
                        };
                        animate();
                    }
                    return () => cancelAnimationFrame(animationFrame);
                }, [isPlaying, e, a]);

                useEffect(() => {
                    setPlanetPos(prev => {
                        const r = a * (1 - e * e) / (1 + e * Math.cos(prev.angle));
                        const x = -focusOffset + r * Math.cos(prev.angle + Math.PI);
                        const y = r * Math.sin(prev.angle + Math.PI);
                        return { ...prev, x, y };
                    });
                }, [e, a]);

                useEffect(() => {
                    const canvas = canvasRef.current;
                    if (!canvas) return;
                    const ctx = canvas.getContext('2d');
                    const width = canvas.width;
                    const height = canvas.height;
                    const centerX = width / 2;
                    const centerY = height / 2;

                    ctx.clearRect(0, 0, width, height);

                    // 1. 그리드 축
                    ctx.strokeStyle = '#1e293b';
                    ctx.lineWidth = 0.8;
                    ctx.beginPath();
                    ctx.moveTo(0, centerY); ctx.lineTo(width, centerY);
                    ctx.moveTo(centerX, 0); ctx.lineTo(centerX, height);
                    ctx.stroke();

                    // 2. 이상적인 원 궤도 비교 가이드 (showCircleComp)
                    if (showCircleComp) {
                        // 타원 중심 기준 동일 반경 (r = a) 완벽한 원
                        ctx.beginPath();
                        ctx.ellipse(centerX, centerY, a, a, 0, 0, Math.PI * 2);
                        ctx.strokeStyle = '#06b6d4';
                        ctx.setLineDash([4, 4]);
                        ctx.lineWidth = 1.8;
                        ctx.stroke();
                        ctx.setLineDash([]);

                        // 기하학적 중심점 표시
                        ctx.beginPath();
                        ctx.arc(centerX, centerY, 3.5, 0, Math.PI * 2);
                        ctx.fillStyle = '#06b6d4';
                        ctx.fill();

                        // 초점 편위 (c = ae) 선분 표시
                        if (focusOffset > 3) {
                            ctx.beginPath();
                            ctx.moveTo(centerX, centerY);
                            ctx.lineTo(centerX - focusOffset, centerY);
                            ctx.strokeStyle = '#fbbf24';
                            ctx.lineWidth = 2.2;
                            ctx.stroke();

                            ctx.font = 'bold 11px Pretendard, sans-serif';
                            ctx.fillStyle = '#fbbf24';
                            ctx.fillText(`초점 편위 c = ae (${focusOffset.toFixed(1)}px)`, centerX - focusOffset / 2 - 40, centerY + 22);
                        }

                        // 원 라벨
                        ctx.font = 'bold 11px Pretendard, sans-serif';
                        ctx.fillStyle = '#06b6d4';
                        ctx.fillText(`기준 원 궤도 (반지름 r = a = ${a})`, centerX + a - 80, centerY - 12);
                    }

                    // 3. 실제 타원 궤도
                    ctx.beginPath();
                    ctx.ellipse(centerX, centerY, a, b, 0, 0, Math.PI * 2);
                    ctx.strokeStyle = '#94a3b8';
                    ctx.setLineDash([5, 5]);
                    ctx.lineWidth = 1.6;
                    ctx.stroke();
                    ctx.setLineDash([]);

                    // 4. 장반경, 단반경 표시 (옵션)
                    if (showAxes) {
                        ctx.lineWidth = 2;
                        // 장반경 (a) - 센터에서 근일점 축
                        ctx.strokeStyle = '#ef4444';
                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(centerX - a, centerY);
                        ctx.stroke();
                        // 단반경 (b) - 센터에서 위쪽 축
                        ctx.strokeStyle = '#10b981';
                        ctx.beginPath();
                        ctx.moveTo(centerX, centerY);
                        ctx.lineTo(centerX, centerY - b);
                        ctx.stroke();

                        ctx.font = 'bold 12px Pretendard, sans-serif';
                        ctx.fillStyle = '#ef4444'; ctx.fillText(`장반경 a: ${a}`, centerX - a/2 - 25, centerY - 10);
                        ctx.fillStyle = '#10b981'; ctx.fillText(`단반경 b: ${b.toFixed(1)} (${(bOverA * 100).toFixed(1)}%)`, centerX + 10, centerY - b/2);
                    }

                    // 5. 면적 속도 일정 법칙 시각화 (동일 시간 구간 2개 표시)
                    if (showAreas) {
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

                        const drawSector = (startM, color, label) => {
                            ctx.beginPath();
                            ctx.fillStyle = color;
                            ctx.globalAlpha = 0.45;
                            ctx.moveTo(centerX - focusOffset, centerY);
                            
                            const dM = (Math.PI * 2) / timeFraction; 
                            const numSteps = 60;
                            
                            for(let i = 0; i <= numSteps; i++) {
                                const currentM = startM + (dM * i) / numSteps;
                                const theta = getTrueAnomaly(currentM, e);
                                const r = a * (1 - e * e) / (1 + e * Math.cos(theta));
                                const x = -focusOffset + r * Math.cos(theta + Math.PI);
                                const y = r * Math.sin(theta + Math.PI);
                                ctx.lineTo(centerX + x, centerY + y);
                            }
                            
                            ctx.lineTo(centerX - focusOffset, centerY);
                            ctx.fill();
                            ctx.globalAlpha = 1.0;
                            ctx.strokeStyle = color;
                            ctx.lineWidth = 1.6;
                            ctx.stroke();
                        };

                        drawSector(-(Math.PI / timeFraction), '#ef4444', '근일점 구역'); 
                        drawSector(Math.PI - (Math.PI / timeFraction), '#3b82f6', '원일점 구역');
                    }

                    // 6. 태양 (한 초점에 위치)
                    ctx.beginPath();
                    ctx.arc(centerX - focusOffset, centerY, 15, 0, Math.PI * 2);
                    ctx.fillStyle = '#fbbf24';
                    ctx.shadowBlur = 25;
                    ctx.shadowColor = '#fbbf24';
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // 7. 행성 연결선 및 행성 본체
                    ctx.beginPath();
                    ctx.moveTo(centerX - focusOffset, centerY);
                    ctx.lineTo(centerX + planetPos.x, centerY + planetPos.y);
                    ctx.strokeStyle = '#38bdf8';
                    ctx.lineWidth = 1.2;
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.arc(centerX + planetPos.x, centerY + planetPos.y, 8.5, 0, Math.PI * 2);
                    ctx.fillStyle = '#3b82f6';
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff'; 
                    ctx.lineWidth = 2.5; 
                    ctx.stroke();

                }, [planetPos, e, a, showAxes, showAreas, showCircleComp]);

                return (
                    <div className="max-w-7xl mx-auto p-2 sm:p-4 flex flex-col gap-6 text-slate-800">
                        
                        {/* 1. 상단 행성 빠른 선택 배너 바 */}
                        <div className="bg-slate-900 text-white p-5 rounded-3xl shadow-xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/30">
                                    <Icon name="orbit" size={20} />
                                </div>
                                <div>
                                    <h4 className="font-extrabold text-sm sm:text-base flex items-center gap-2">
                                        태양계 8개 행성 궤도 프리셋
                                        <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-500/20 text-blue-300 font-mono">
                                            {selectedPlanetName} (e = {e.toFixed(4)})
                                        </span>
                                    </h4>
                                    <p className="text-xs text-slate-400">행성을 클릭하면 실제 공전 궤도 이심률이 즉시 시뮬레이터에 적용됩니다.</p>
                                </div>
                            </div>
                            
                            <div className="flex flex-wrap items-center gap-1.5 sm:gap-2">
                                {PLANET_DATA.map((p) => {
                                    const isSel = selectedPlanetName === p.name;
                                    return (
                                        <button
                                            key={p.name}
                                            onClick={() => handleSelectPlanet(p)}
                                            className={`px-3 py-1.5 rounded-xl font-bold text-xs transition-all flex items-center gap-1.5 border ${
                                                isSel 
                                                ? 'bg-blue-600 text-white border-blue-400 shadow-md shadow-blue-600/40 scale-105' 
                                                : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700 hover:text-white'
                                            }`}
                                        >
                                            <span style={{ color: p.color }}>{p.symbol}</span>
                                            <span>{p.name}</span>
                                            <span className="text-[10px] opacity-75 font-mono">({p.e})</span>
                                        </button>
                                    );
                                })}
                                <button
                                    onClick={() => { setEccentricity(0.50); setSelectedPlanetName('가상 타원'); }}
                                    className={`px-3 py-1.5 rounded-xl font-bold text-xs transition-all border ${
                                        selectedPlanetName === '가상 타원' 
                                        ? 'bg-purple-600 text-white border-purple-400 shadow-md shadow-purple-600/40 scale-105' 
                                        : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                                    }`}
                                >
                                    🚀 가상 타원 (0.50)
                                </button>
                            </div>
                        </div>

                        {/* 2. 메인 시뮬레이션 뷰 & 사이드바 */}
                        <div className="flex flex-col lg:flex-row gap-6">
                            {/* 메인 캔버스 뷰 */}
                            <div className="flex-1 space-y-4">
                                <div className="bg-slate-900 rounded-[2.5rem] overflow-hidden relative shadow-2xl border-[10px] border-slate-800 aspect-video flex items-center justify-center">
                                    <canvas ref={canvasRef} width={900} height={550} className="w-full h-auto" />
                                    
                                    {/* 상단 오버레이 인포 */}
                                    <div className="absolute top-6 left-6 flex flex-col gap-2">
                                        <div className="px-4 py-2 bg-black/70 backdrop-blur-md rounded-2xl border border-white/10 text-white text-[11px] font-black uppercase tracking-widest flex items-center gap-2">
                                            <div className="w-2.5 h-2.5 bg-blue-500 rounded-full animate-ping"></div>
                                            <span>{selectedPlanetName} 시뮬레이션 중 (e: {e.toFixed(4)})</span>
                                        </div>
                                        <div className="px-3 py-1.5 bg-black/60 backdrop-blur-md rounded-xl border border-white/10 text-[11px] text-slate-300 font-medium">
                                            단반경 비율 <span className="text-emerald-400 font-bold font-mono">b/a = {shapeSimilarity}%</span> (원운동 일치율)
                                        </div>
                                    </div>

                                    {/* 하단 범례 오버레이 */}
                                    <div className="absolute bottom-6 right-6 flex flex-wrap gap-3 text-white text-[11px] bg-black/75 p-4 rounded-2xl backdrop-blur-md border border-white/10 font-bold">
                                        <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-yellow-400 rounded-full shadow-[0_0_8px_#fbbf24]"></div> 태양 (초점)</div>
                                        <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-blue-500 rounded-full shadow-[0_0_8px_#3b82f6]"></div> 행성</div>
                                        {showCircleComp && (
                                            <div className="flex items-center gap-1.5 text-cyan-400"><div className="w-3 h-3 border-2 border-dashed border-cyan-400 rounded-full"></div> 원 궤도 (r=a)</div>
                                        )}
                                        {showAreas && (
                                            <>
                                                <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-red-400/50 border border-red-400 rounded-sm"></div> 근일점 구역</div>
                                                <div className="flex items-center gap-1.5"><div className="w-3 h-3 bg-blue-400/50 border border-blue-400 rounded-sm"></div> 원일점 구역</div>
                                            </>
                                        )}
                                    </div>
                                </div>

                                {/* 면적 속도 일정 비교 대시보드 */}
                                {showAreas && (
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-in slide-in-from-bottom-3 duration-300">
                                        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-4">
                                            <div className="w-14 h-14 bg-red-50 rounded-2xl flex items-center justify-center text-red-500 shrink-0 border border-red-100 italic font-black text-lg">A</div>
                                            <div>
                                                <h5 className="font-extrabold text-slate-800 text-sm mb-0.5">근일점 구역 (Perihelion)</h5>
                                                <p className="text-xs text-slate-500 leading-relaxed">거리는 가깝지만 공전 속력이 빨라 <span className="text-red-600 font-bold">넓고 얇은 부채꼴</span>을 형성합니다.</p>
                                            </div>
                                            <div className="ml-auto text-right">
                                                <span className="text-[10px] text-slate-400 uppercase font-black block">훑고 간 면적</span>
                                                <span className="text-base font-black text-slate-800 font-mono">100.0%</span>
                                            </div>
                                        </div>
                                        <div className="bg-white p-5 rounded-3xl border border-slate-200 shadow-md flex items-center gap-4">
                                            <div className="w-14 h-14 bg-blue-50 rounded-2xl flex items-center justify-center text-blue-500 shrink-0 border border-blue-100 italic font-black text-lg">B</div>
                                            <div>
                                                <h5 className="font-extrabold text-slate-800 text-sm mb-0.5">원일점 구역 (Aphelion)</h5>
                                                <p className="text-xs text-slate-500 leading-relaxed">거리는 멀지만 공전 속력이 느려 <span className="text-blue-600 font-bold">좁고 긴 부채꼴</span>을 형성합니다.</p>
                                            </div>
                                            <div className="ml-auto text-right">
                                                <span className="text-[10px] text-slate-400 uppercase font-black block">훑고 간 면적</span>
                                                <span className="text-base font-black text-slate-800 font-mono">100.0%</span>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* 컨트롤 사이드바 */}
                            <div className="w-full lg:w-[360px] space-y-5">
                                <div className="bg-white p-6 sm:p-7 rounded-[2rem] border border-slate-200 shadow-xl space-y-6">
                                    <div className="flex items-center justify-between">
                                        <h3 className="text-base font-extrabold text-slate-800 flex items-center gap-2.5">
                                            <div className="w-8 h-8 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-md shadow-blue-200">
                                                <Icon name="sliders" size={16} />
                                            </div>
                                            궤도 물리 파라미터
                                        </h3>
                                        <span className="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold font-mono">
                                            {selectedPlanetName}
                                        </span>
                                    </div>

                                    <div className="space-y-5">
                                        {/* 이심률 슬라이더 */}
                                        <div className="space-y-2">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-black text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                                                    <Icon name="disc" size={14} /> 이심률 (Eccentricity e)
                                                </label>
                                                <span className="px-3 py-0.5 bg-blue-50 text-blue-600 border border-blue-200 rounded-full font-mono font-black text-sm">
                                                    {e.toFixed(4)}
                                                </span>
                                            </div>
                                            <input 
                                                type="range" 
                                                min="0" 
                                                max="0.80" 
                                                step="0.001" 
                                                value={e} 
                                                onChange={(ev) => handleManualEccentricity(parseFloat(ev.target.value))} 
                                                className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" 
                                            />
                                            <div className="flex justify-between text-[10px] text-slate-400 font-mono">
                                                <span>0.00 (완전한 원)</span>
                                                <span>지구(0.0167)</span>
                                                <span>0.80 (극단적 타원)</span>
                                            </div>
                                        </div>

                                        {/* 장반경 슬라이더 */}
                                        <div className="space-y-2">
                                            <div className="flex justify-between items-center">
                                                <label className="text-xs font-black text-slate-500 uppercase tracking-wider flex items-center gap-1.5">
                                                    <Icon name="move-horizontal" size={14} /> 장반경 (Semi-major a)
                                                </label>
                                                <span className="px-3 py-0.5 bg-slate-100 text-slate-700 rounded-full font-mono font-black text-sm">
                                                    {a} px
                                                </span>
                                            </div>
                                            <input 
                                                type="range" 
                                                min="100" 
                                                max="180" 
                                                step="5" 
                                                value={a} 
                                                onChange={(ev) => setSemiMajorAxis(parseInt(ev.target.value))} 
                                                className="w-full h-2 bg-slate-100 rounded-xl appearance-none cursor-pointer" 
                                            />
                                        </div>

                                        {/* 원 궤도 비교 & 토글 버튼 그룹 */}
                                        <div className="space-y-2.5 pt-1">
                                            <button 
                                                onClick={() => setShowCircleComp(!showCircleComp)} 
                                                className={`w-full p-3.5 rounded-2xl border-2 transition-all flex items-center justify-between font-bold text-xs ${
                                                    showCircleComp 
                                                    ? 'border-cyan-500 bg-cyan-50 text-cyan-700 shadow-md shadow-cyan-100' 
                                                    : 'border-slate-100 text-slate-500 hover:border-slate-200'
                                                }`}
                                            >
                                                <span className="flex items-center gap-2">
                                                    <Icon name="circle" size={16} /> 원 궤도 비교 가이드 (r=a)
                                                </span>
                                                <span className={`px-2 py-0.5 rounded-md text-[10px] font-extrabold ${showCircleComp ? 'bg-cyan-600 text-white' : 'bg-slate-200 text-slate-500'}`}>
                                                    {showCircleComp ? 'ON' : 'OFF'}
                                                </span>
                                            </button>

                                            <div className="grid grid-cols-2 gap-2.5">
                                                <button 
                                                    onClick={() => setShowAxes(!showAxes)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex flex-col items-center gap-1 font-bold text-[11px] ${
                                                        showAxes ? 'border-blue-600 bg-blue-50 text-blue-600' : 'border-slate-100 text-slate-400 hover:border-slate-200'
                                                    }`}
                                                >
                                                    <Icon name="maximize" size={16} /> 장/단반경 {showAxes ? 'ON' : 'OFF'}
                                                </button>
                                                <button 
                                                    onClick={() => setShowAreas(!showAreas)} 
                                                    className={`p-3 rounded-2xl border-2 transition-all flex flex-col items-center gap-1 font-bold text-[11px] ${
                                                        showAreas ? 'border-red-600 bg-red-50 text-red-600' : 'border-slate-100 text-slate-400 hover:border-slate-200'
                                                    }`}
                                                >
                                                    <Icon name="pie-chart" size={16} /> 면적 속도 {showAreas ? 'ON' : 'OFF'}
                                                </button>
                                            </div>
                                        </div>

                                        {/* 관측 시간 조절 */}
                                        {showAreas && (
                                            <div className="space-y-2 p-3 bg-red-50/60 rounded-2xl border border-red-100 animate-in fade-in duration-200">
                                                <div className="flex justify-between items-center">
                                                    <label className="text-[11px] font-black text-red-700 uppercase tracking-wider flex items-center gap-1">
                                                        <Icon name="clock" size={13} /> 관측 시간 (주기 T 기준)
                                                    </label>
                                                    <span className="px-2 py-0.5 bg-red-100 text-red-600 rounded-md font-mono font-black text-xs">T / {timeFraction}</span>
                                                </div>
                                                <input 
                                                    type="range" 
                                                    min="4" 
                                                    max="24" 
                                                    step="1" 
                                                    value={timeFraction} 
                                                    onChange={(ev) => setTimeFraction(parseInt(ev.target.value))} 
                                                    className="w-full h-1.5 bg-red-200 rounded-xl appearance-none cursor-pointer" 
                                                />
                                            </div>
                                        )}

                                        {/* 실시간 기하 지표 요약 카드 */}
                                        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 space-y-2 text-xs">
                                            <div className="font-extrabold text-slate-700 flex items-center justify-between pb-1 border-b border-slate-200/60">
                                                <span>실시간 기하 수치 분석</span>
                                                <span className="text-[10px] text-blue-600 font-mono">단반경 비율 b/a</span>
                                            </div>
                                            <div className="grid grid-cols-2 gap-2 text-slate-600 font-mono">
                                                <div>장반경 (a): <span className="font-bold text-slate-800">{a}</span></div>
                                                <div>단반경 (b): <span className="font-bold text-slate-800">{b.toFixed(1)}</span></div>
                                                <div>초점 편위 (c): <span className="font-bold text-amber-600">{focusOffset.toFixed(1)}</span></div>
                                                <div>원형 일치도: <span className="font-bold text-emerald-600">{shapeSimilarity}%</span></div>
                                            </div>
                                            <div className="pt-1 text-[11px] text-slate-500">
                                                원일점/근일점 거리비: <span className="font-bold text-slate-800 font-mono">{distanceRatio.toFixed(3)} 배</span>
                                            </div>
                                        </div>

                                        {/* 시뮬레이션 동작 제어 버튼 */}
                                        <div className="space-y-2 pt-2 border-t border-slate-100">
                                            <button 
                                                onClick={() => setIsPlaying(!isPlaying)} 
                                                className={`w-full py-4 rounded-2xl font-black text-base shadow-lg transition-all flex items-center justify-center gap-2.5 ${
                                                    isPlaying 
                                                    ? 'bg-slate-800 text-white hover:bg-slate-900' 
                                                    : 'bg-blue-600 text-white hover:bg-blue-700 shadow-blue-200'
                                                }`}
                                            >
                                                <Icon name={isPlaying ? "pause" : "play"} size={20} /> 
                                                {isPlaying ? '공전 일시정지' : '공전 시작하기'}
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

                        {/* 3. 태양계 8개 행성 공전 궤도 이심률 데이터베이스 표 */}
                        <div className="bg-white rounded-[2.5rem] p-6 sm:p-8 border border-slate-200 shadow-xl space-y-6">
                            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
                                <div>
                                    <div className="flex items-center gap-2 text-blue-600 font-extrabold text-xs tracking-wider uppercase">
                                        <Icon name="table" size={16} /> 태양계 정밀 관측 데이터
                                    </div>
                                    <h3 className="text-xl font-black text-slate-800 mt-1">
                                        태양계 8개 행성의 공전 궤도 이심률($e$)과 궤도 특성
                                    </h3>
                                    <p className="text-xs sm:text-sm text-slate-500 mt-1">
                                        행성별 이심률과 장단반경 비율($b/a = \sqrt{1-e^2}$)을 확인하고, 
                                        <span className="text-blue-600 font-bold"> [시뮬레이션 적용] </span> 
                                        버튼을 눌러 실제 궤도를 관찰해 보세요.
                                    </p>
                                </div>
                                <div className="flex items-center gap-2 self-start sm:self-auto bg-slate-50 px-3.5 py-2 rounded-2xl border border-slate-200 text-xs font-bold text-slate-600">
                                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
                                    <span>원형 유사도: 8개 행성 모두 97.8% ~ 99.99%</span>
                                </div>
                            </div>

                            <div className="overflow-x-auto">
                                <table className="w-full text-left text-sm border-collapse">
                                    <thead>
                                        <tr className="border-b-2 border-slate-200 text-slate-500 text-xs uppercase font-extrabold bg-slate-50/80">
                                            <th className="py-3 px-4">행성</th>
                                            <th className="py-3 px-4">공전 궤도 이심률 ($e$)</th>
                                            <th className="py-3 px-4">단반경 비율 ($b/a = \sqrt{1-e^2}$)</th>
                                            <th className="py-3 px-4">원형 일치도</th>
                                            <th className="py-3 px-4">특징</th>
                                            <th className="py-3 px-4 text-center">시뮬레이션</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100 font-medium">
                                        {PLANET_DATA.map((planet) => {
                                            const bRatio = Math.sqrt(1 - planet.e * planet.e);
                                            const pct = (bRatio * 100).toFixed(2);
                                            const isSelected = selectedPlanetName === planet.name;
                                            return (
                                                <tr 
                                                    key={planet.name} 
                                                    className={`transition-colors cursor-pointer hover:bg-blue-50/50 ${
                                                        isSelected ? 'bg-blue-50/80 border-l-4 border-l-blue-600 font-semibold' : ''
                                                    }`}
                                                    onClick={() => handleSelectPlanet(planet)}
                                                >
                                                    <td className="py-3.5 px-4 flex items-center gap-2 font-bold text-slate-800">
                                                        <span className="text-base" style={{ color: planet.color }}>{planet.symbol}</span>
                                                        <span>{planet.name}</span>
                                                        <span className="text-xs text-slate-400 font-normal">({planet.en})</span>
                                                    </td>
                                                    <td className="py-3.5 px-4 font-mono font-extrabold text-slate-900">
                                                        {planet.e.toFixed(4)}
                                                    </td>
                                                    <td className="py-3.5 px-4 font-mono text-slate-700">
                                                        {(bRatio).toFixed(4)} <span className="text-xs text-slate-400">({pct}%)</span>
                                                    </td>
                                                    <td className="py-3.5 px-4 min-w-[140px]">
                                                        <div className="flex items-center gap-2">
                                                            <div className="flex-1 bg-slate-100 h-2.5 rounded-full overflow-hidden">
                                                                <div 
                                                                    className="bg-emerald-500 h-full rounded-full transition-all duration-500" 
                                                                    style={{ width: `${pct}%` }}
                                                                ></div>
                                                            </div>
                                                            <span className="text-[11px] font-mono font-bold text-emerald-700">{pct}%</span>
                                                        </div>
                                                    </td>
                                                    <td className="py-3.5 px-4 text-slate-700">
                                                        <span className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-bold border mr-2 ${planet.tagBg}`}>
                                                            {planet.tag}
                                                        </span>
                                                        <span className="text-xs text-slate-600">{planet.desc}</span>
                                                    </td>
                                                    <td className="py-3.5 px-4 text-center">
                                                        <button 
                                                            onClick={(e) => { e.stopPropagation(); handleSelectPlanet(planet); }}
                                                            className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                                                                isSelected 
                                                                ? 'bg-blue-600 text-white shadow-sm shadow-blue-400' 
                                                                : 'bg-slate-100 text-slate-600 hover:bg-blue-600 hover:text-white'
                                                            }`}
                                                        >
                                                            {isSelected ? '관측 중' : '적용'}
                                                        </button>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* 4. 심층 문장 분석 및 물리학적 고찰 섹션 */}
                        <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-indigo-950 text-white rounded-[2.5rem] p-6 sm:p-10 shadow-2xl space-y-8 relative overflow-hidden">
                            <div className="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-[100px] pointer-events-none"></div>
                            <div className="absolute bottom-0 left-0 w-80 h-80 bg-indigo-500/10 rounded-full blur-[90px] pointer-events-none"></div>

                            {/* 핵심 명제 배너 */}
                            <div className="relative border-b border-white/10 pb-6 space-y-3">
                                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-extrabold uppercase tracking-widest border border-blue-400/30">
                                    <Icon name="lightbulb" size={14} /> 물리학적 문장 심층 분석
                                </div>
                                <h2 className="text-xl sm:text-2xl font-black text-white leading-tight">
                                    "태양계 행성의 이심률은 매우 작아서 근사적으로 원운동으로 볼 수 있다"
                                </h2>
                                <p className="text-sm text-slate-300 leading-relaxed max-w-4xl">
                                    이 명제는 케플러 제1법칙(타원 궤도)의 엄밀한 천체역학적 진실과, 물리적 현상을 단순화하여 핵심 인과관계를 파악하는 
                                    <strong className="text-blue-300 font-extrabold"> '과학적 모델링(근사, Approximation)'</strong>의 방법론적 유용성을 동시에 담고 있습니다. 
                                    수학적 구조와 과학사적·물리학적 의미를 4개 관점으로 심층 분석합니다.
                                </p>
                            </div>

                            {/* 4대 심층 분석 카드 그리드 */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 relative">
                                
                                {/* 카드 1: 형태의 원형 유사도 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 hover:border-blue-400/40 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-2xl bg-blue-500/20 text-blue-400 border border-blue-400/30 flex items-center justify-center font-black">
                                            1
                                        </div>
                                        <div>
                                            <h4 className="font-extrabold text-white text-base">수학적 형태 분석: 왜 눈으로는 원과 구별할 수 없는가?</h4>
                                            <p className="text-xs text-slate-400 font-mono">단반경과 장반경의 비율 (b/a)</p>
                                        </div>
                                    </div>
                                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                                        타원의 장반경 <MathBox formula="a" inline={true} />와 단반경 <MathBox formula="b" inline={true} />는 
                                        이심률 <MathBox formula="e" inline={true} />에 대해 다음 관계를 갖습니다.
                                    </p>
                                    <div className="p-3 bg-black/40 rounded-2xl border border-white/10 text-center font-mono text-sm text-blue-300">
                                        <MathBox formula="b = a \sqrt{1 - e^2} \implies \frac{b}{a} \approx 1 - \frac{1}{2}e^2 \quad (e \ll 1)" />
                                    </div>
                                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside leading-relaxed">
                                        <li><strong className="text-white">지구 (e = 0.0167):</strong> <MathBox formula="b/a \approx 0.99986" inline={true} /> (99.986%). 장축과 단축의 차이가 겨우 <strong>0.014%</strong>에 불과하여 정밀 컴퍼스로 그린 원과 육안으로 절대 구별할 수 없습니다.</li>
                                        <li><strong className="text-white">수성 (e = 0.2056):</strong> 8개 행성 중 가장 큰 이심률을 가졌음에도 <MathBox formula="b/a \approx 0.9786" inline={true} /> (97.86%)로, 장축과 단축의 편차가 약 2.1%에 불과합니다.</li>
                                        <li><strong className="text-emerald-400 font-bold">결론:</strong> 기하학적 '외형(모양)' 관점에서 태양계 행성의 궤도는 사실상 완벽한 원과 다름없습니다.</li>
                                    </ul>
                                </div>

                                {/* 카드 2: 초점의 치우침과 케플러의 발견 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 hover:border-amber-400/40 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-400 border border-amber-400/30 flex items-center justify-center font-black">
                                            2
                                        </div>
                                        <div>
                                            <h4 className="font-extrabold text-white text-base">기하학적 반전: 중심이 아닌 '초점의 치우침(c = ae)'</h4>
                                            <p className="text-xs text-slate-400 font-mono">형태가 아니라 태양의 위치가 핵심</p>
                                        </div>
                                    </div>
                                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                                        모양 자체는 거의 원이지만, 태양은 원의 중심이 아니라 <strong>한 초점(중심에서 <MathBox formula="c = ae" inline={true} /> 만큼 떨어진 지점)</strong>에 위치합니다.
                                    </p>
                                    <div className="p-3 bg-black/40 rounded-2xl border border-white/10 text-center font-mono text-sm text-amber-300 flex items-center justify-center gap-2 flex-wrap">
                                        <span className="text-xs text-amber-200/80 font-sans font-bold">원일점 / 근일점 거리비:</span>
                                        <MathBox formula="\frac{r_a}{r_p} = \frac{a(1+e)}{a(1-e)} = \frac{1+e}{1-e}" inline={true} />
                                    </div>
                                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside leading-relaxed">
                                        <li><strong className="text-white">화성 (e = 0.0934):</strong> 단반경 비율은 99.56%로 거의 원이지만, 태양이 중심에서 <strong>9.34%</strong> 벗어나 있어 원일점과 근일점 거리비가 <strong>1.206배(약 20.6% 거리 차이)</strong>에 달합니다.</li>
                                        <li><strong className="text-amber-400 font-bold">케플러의 위대한 발견:</strong> 면적 속도 일정 법칙에 의해 공전 속력도 20.6% 차이가 났고, 티코 브라헤의 정밀 관측 데이터에서 나타난 단 <strong>8분(8 arcmin ≈ 0.133°)</strong>의 각도 오차를 타협하지 않고 파고든 끝에 타원 궤도를 규명해 냈습니다.</li>
                                    </ul>
                                </div>

                                {/* 카드 3: 물리학적 모델링의 본질 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 hover:border-emerald-400/40 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-2xl bg-emerald-500/20 text-emerald-400 border border-emerald-400/30 flex items-center justify-center font-black">
                                            3
                                        </div>
                                        <div>
                                            <h4 className="font-extrabold text-white text-base">물리학적 모델링: 왜 교과서에서는 '원운동'으로 근사할까?</h4>
                                            <p className="text-xs text-slate-400 font-mono">만유인력 = 구심력의 강력한 유용성</p>
                                        </div>
                                    </div>
                                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                                        <MathBox formula="e \ll 1" inline={true} />이므로 복잡한 타원 미분적분을 쓰지 않고 행성의 궤도를 <strong>등속 원운동</strong>으로 가정해도 오차가 수 % 이내로 매우 정밀합니다.
                                    </p>
                                    <div className="p-3 bg-black/40 rounded-2xl border border-white/10 text-center font-mono text-sm text-emerald-300">
                                        <MathBox formula="F = G\frac{Mm}{r^2} = m\frac{v^2}{r} = mr\left(\frac{2\pi}{T}\right)^2 \implies \frac{r^3}{T^2} = \frac{GM}{4\pi^2} = \text{constant (일정)}" />
                                    </div>
                                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside leading-relaxed">
                                        <li>원운동 근사를 적용하면 고등학교 물리학 수준에서도 <strong>케플러 제3법칙(조화의 법칙 <MathBox formula="T^2 \propto r^3" inline={true} />)</strong>을 명쾌하고 직관적으로 유도할 수 있습니다.</li>
                                        <li>인공위성 궤도 속도 계산, 탈출 속도 유도, 우주선 전이 궤도 설계 등 기초 천체물리학 문제의 90% 이상을 이 강력한 원운동 모델로 해결합니다.</li>
                                    </ul>
                                </div>

                                {/* 카드 4: 과학 탐구 방법론과 지혜 */}
                                <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md space-y-4 hover:border-purple-400/40 transition-colors">
                                    <div className="flex items-center gap-3">
                                        <div className="w-10 h-10 rounded-2xl bg-purple-500/20 text-purple-400 border border-purple-400/30 flex items-center justify-center font-black">
                                            4
                                        </div>
                                        <div>
                                            <h4 className="font-extrabold text-white text-base">과학 탐구의 지혜: '근사(Approximation)'의 진짜 가치</h4>
                                            <p className="text-xs text-slate-400 font-mono">단순한 타협이 아닌 과학적 사고의 정수</p>
                                        </div>
                                    </div>
                                    <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                                        자연의 실제 현상은 무수한 변수(이심률, 타 행성의 중력 섭동, 상대론적 세차 등)로 복잡합니다. 물리학자는 
                                        <strong>'현상의 지배적 본질'</strong>을 규명하기 위해 적절한 이상화(Idealization)를 적용합니다.
                                    </p>
                                    <div className="p-3 bg-purple-900/30 border border-purple-500/30 rounded-2xl text-xs text-purple-200 leading-relaxed">
                                        "자연의 엄밀한 법칙이 타원 궤도임을 잊지 않으면서도, 오차가 극히 작은 영역에서는 계산의 단순성과 물리적 직관을 위해 원운동 모델을 도구로 채택한다."
                                    </div>
                                    <ul className="text-xs text-slate-300 space-y-1.5 list-disc list-inside leading-relaxed">
                                        <li>오차 한계를 인식하고 적절한 모델을 선택하는 것이 물리학적 소양의 핵심입니다.</li>
                                        <li>엄밀한 진실(타원)과 실용적 유용성(원운동)의 조화야말로 물리학이 자연을 이해하는 가장 지혜로운 방식입니다.</li>
                                    </ul>
                                </div>

                            </div>

                            {/* 하단 요약 인용 배너 */}
                            <div className="p-5 bg-white/5 rounded-3xl border border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-400">
                                        <Icon name="check-circle" size={18} />
                                    </div>
                                    <span className="text-xs sm:text-sm font-bold text-slate-200">
                                        핵심 요약: 형태는 98%~99.9% 원형에 수렴하지만, 태양은 초점(<MathBox formula="c=ae" inline={true} />)에 위치하여 거리·속력 편차가 발생함!
                                    </span>
                                </div>
                                <div className="text-xs font-mono font-bold text-blue-300 bg-blue-900/40 px-3.5 py-1.5 rounded-xl border border-blue-500/30 whitespace-nowrap">
                                    Elliptical Truth + Circular Utility
                                </div>
                            </div>

                        </div>

                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerSim />);
        </script>
    </body>
    </html>
    """

    components.html(react_code, height=2100, scrolling=True)

if __name__ == "__main__":
    run_sim()
