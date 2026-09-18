import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.title("🕰️ [탐구] 진자의 운동과 힘의 분석 (교과서 그림 I-15 연계)")
    st.markdown("""
    이 시뮬레이션은 교과서 **「진자의 운동」** 단원과 **[그림 I-15 진자의 운동]**을 직접 조작하며 탐구할 수 있는 가상실험실입니다.
    실에 매달려 왕복 운동하는 진자에서 **중력($mg$)**과 **장력($T$)**이 어떻게 합성되어 **알짜힘($F$)**과 **가속도($a$)**를 만들어내는지 벡터 평행사변형법을 통해 관찰해 보세요.
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
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800;900&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
            .math-font { font-family: 'Times New Roman', serif; font-style: italic; }
            input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                height: 18px;
                width: 18px;
                border-radius: 50%;
                background: #2563eb;
                cursor: pointer;
                border: 2px solid white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div id="root"></div>

        <script type="text/babel">
            const { useState, useEffect, useRef, useMemo } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                const ref = useRef(null);
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const PendulumSimulation = () => {
                // --- 물리 파라미터 상태 ---
                const [length, setLength] = useState(1.8);        // m (진자 길이)
                const [mass, setMass] = useState(1.0);            // kg (추 질량)
                const [maxAngleDeg, setMaxAngleDeg] = useState(35); // 도 (진폭 각도 θ)
                const [g, setG] = useState(9.8);                  // m/s^2 (중력가속도)
                
                // --- 시뮬레이션 제어 상태 ---
                const [isPlaying, setIsPlaying] = useState(false);
                const [simSpeed, setSimSpeed] = useState(0.5);    // 0.2x, 0.5x, 1.0x
                const [angle, setAngle] = useState(-35 * (Math.PI / 180)); // 현재 각도 (rad)
                const [omega, setOmega] = useState(0);             // 각속도 (rad/s)
                const [activeTab, setActiveTab] = useState('explore'); // explore, compare, quiz
                
                // --- 시각화 표시 옵션 ---
                const [showFigure15Mode, setShowFigure15Mode] = useState(false); // 교과서 5개 지점 동시 표시
                const [showTension, setShowTension] = useState(true);
                const [showGravity, setShowGravity] = useState(true);
                const [showParallelogram, setShowParallelogram] = useState(true);
                const [showNetForce, setShowNetForce] = useState(true);
                const [showComponents, setShowComponents] = useState(false); // 접선 복원력 & 구심력 성분 분해
                const [showVelocity, setShowVelocity] = useState(false);
                const [showEnergyBar, setShowEnergyBar] = useState(true);

                // --- 퀴즈 풀이 상태 ---
                const [quizAnswers, setQuizAnswers] = useState({
                    q1: null,
                    q2: null,
                    q3: null
                });
                const [quizRevealed, setQuizRevealed] = useState({
                    q1: false,
                    q2: false,
                    q3: false
                });

                const animFrameRef = useRef(null);
                const lastTimeRef = useRef(null);
                const angleRef = useRef(angle);
                const omegaRef = useRef(omega);
                angleRef.current = angle;
                omegaRef.current = omega;

                const maxAngleRad = (maxAngleDeg * Math.PI) / 180;

                // --- 물리 계산 함수 ---
                const calcPhysicsAtAngle = (curAngle, curOmega = null) => {
                    const theta = curAngle;
                    // 역학적 에너지 보존을 통해 속력 계산 (무마찰)
                    let v = 0;
                    if (curOmega !== null && isPlaying) {
                        v = length * curOmega;
                    } else {
                        const cosDiff = Math.cos(theta) - Math.cos(maxAngleRad);
                        const vSq = 2 * g * length * Math.max(0, cosDiff);
                        v = Math.sqrt(vSq) * (curOmega >= 0 ? 1 : -1);
                    }
                    const speed = Math.abs(v);

                    // 힘 계산
                    const F_gravity = mass * g; // 연직 아래
                    // 장력 T = mg cosθ + m v^2 / L
                    const T_mag = mass * g * Math.cos(theta) + (mass * speed * speed) / length;

                    // 벡터 성분 (캔버스 좌표계: x 오른쪽 +, y 아래 +)
                    const Fg_vec = { x: 0, y: F_gravity };

                    // 장력 방향: 추 -> 중심 ( -sin(theta), -cos(theta) )
                    const T_vec = {
                        x: -T_mag * Math.sin(theta),
                        y: -T_mag * Math.cos(theta)
                    };

                    // 알짜힘 F_net = T_vec + Fg_vec
                    const Fnet_vec = {
                        x: T_vec.x + Fg_vec.x,
                        y: T_vec.y + Fg_vec.y
                    };
                    const Fnet_mag = Math.sqrt(Fnet_vec.x * Fnet_vec.x + Fnet_vec.y * Fnet_vec.y);

                    // 성분 분해: 접선 복원력 & 구심력
                    const F_tangential = -mass * g * Math.sin(theta); // 접선 복원력
                    const F_centripetal = (mass * speed * speed) / length; // 중심 방향 구심력

                    // 가속도 a = F_net / m
                    const a_mag = Fnet_mag / mass;

                    // 에너지
                    const h = length * (1 - Math.cos(theta));
                    const h_max = length * (1 - Math.cos(maxAngleRad));
                    const Ep = mass * g * h;
                    const Ek = 0.5 * mass * speed * speed;
                    const E_total = mass * g * h_max;

                    return {
                        theta,
                        thetaDeg: (theta * 180) / Math.PI,
                        speed,
                        v,
                        F_gravity,
                        Fg_vec,
                        T_mag,
                        T_vec,
                        Fnet_mag,
                        Fnet_vec,
                        F_tangential,
                        F_centripetal,
                        a_mag,
                        h,
                        Ep,
                        Ek,
                        E_total
                    };
                };

                // 현재 상태의 물리량
                const curPhys = useMemo(() => {
                    return calcPhysicsAtAngle(angle, omega);
                }, [angle, omega, length, mass, maxAngleRad, g]);

                // 교과서 5개 기준 지점 (A, B, C, D, E) 물리량 계산
                const fivePoints = useMemo(() => {
                    const pts = [
                        { id: 'A', name: '최고점 (A)', theta: -maxAngleRad, desc: '좌측 최고점 (속력 0)' },
                        { id: 'B', name: '중간점 (B)', theta: -maxAngleRad * 0.5, desc: '하강 중간점' },
                        { id: 'C', name: '최저점 (C)', theta: 0, desc: '중심 평형점 (속력 최대)' },
                        { id: 'D', name: '중간점 (D)', theta: maxAngleRad * 0.5, desc: '상승 중간점' },
                        { id: 'E', name: '최고점 (E)', theta: maxAngleRad, desc: '우측 최고점 (속력 0)' }
                    ];

                    return pts.map(p => {
                        const phys = calcPhysicsAtAngle(p.theta, 0);
                        return { ...p, ...phys };
                    });
                }, [length, mass, maxAngleRad, g]);

                // --- 시뮬레이션 애니메이션 루프 (심플렉틱 오일러) ---
                useEffect(() => {
                    if (!isPlaying) {
                        if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
                        lastTimeRef.current = null;
                        return;
                    }

                    const updateSim = (time) => {
                        if (lastTimeRef.current != null) {
                            const realDt = (time - lastTimeRef.current) / 1000;
                            const dt = Math.min(realDt, 0.033) * simSpeed;

                            // 수치 오차를 줄이기 위해 6단계 서브스텝 적분 (Euler-Cromer)
                            const subSteps = 6;
                            const subDt = dt / subSteps;
                            let curA = angleRef.current;
                            let curW = omegaRef.current;

                            for (let i = 0; i < subSteps; i++) {
                                const alpha = -(g / length) * Math.sin(curA);
                                curW += alpha * subDt;
                                curA += curW * subDt;
                            }

                            // 에너지 드리프트 방지: 진폭 제어 보정
                            const cosDiff = Math.cos(curA) - Math.cos(maxAngleRad);
                            if (cosDiff < 0) {
                                curA = curA > 0 ? maxAngleRad : -maxAngleRad;
                                curW = 0;
                            }

                            setAngle(curA);
                            setOmega(curW);
                        }
                        lastTimeRef.current = time;
                        animFrameRef.current = requestAnimationFrame(updateSim);
                    };

                    animFrameRef.current = requestAnimationFrame(updateSim);
                    return () => {
                        if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
                    };
                }, [isPlaying, simSpeed, length, maxAngleRad, g]);

                // 컨트롤 핸들러
                const handlePlayPause = () => setIsPlaying(!isPlaying);
                const handleReset = () => {
                    setIsPlaying(false);
                    setAngle(-maxAngleRad);
                    setOmega(0);
                };
                const handleJumpTo = (targetAngle) => {
                    setIsPlaying(false);
                    setAngle(targetAngle);
                    setOmega(0);
                };

                // --- 캔버스 기하학 파라미터 ---
                const canvasW = 620;
                const canvasH = 460;
                const pivotX = canvasW / 2;
                const pivotY = 70;
                const pixelScale = 170; // 1m 당 170px
                const visualLength = length * pixelScale;

                // 벡터 화살표 스케일링: 1N 당 픽셀 길이
                const forceScale = 6.6;

                // 추 위치 계산
                const getBobCoord = (th) => ({
                    x: pivotX + visualLength * Math.sin(th),
                    y: pivotY + visualLength * Math.cos(th)
                });

                const currentBob = getBobCoord(angle);

                // 화살표 SVG 마커 헬퍼
                const renderArrow = (fromX, fromY, toX, toY, color, width = 3, isDashed = false) => {
                    const dx = toX - fromX;
                    const dy = toY - fromY;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 2) return null;

                    const angleRad = Math.atan2(dy, dx);
                    const headLen = Math.min(12, dist * 0.4);

                    const headX1 = toX - headLen * Math.cos(angleRad - Math.PI / 6);
                    const headY1 = toY - headLen * Math.sin(angleRad - Math.PI / 6);
                    const headX2 = toX - headLen * Math.cos(angleRad + Math.PI / 6);
                    const headY2 = toY - headLen * Math.sin(angleRad + Math.PI / 6);

                    return (
                        <g>
                            <line
                                x1={fromX} y1={fromY} x2={toX} y2={toY}
                                stroke={color}
                                strokeWidth={width}
                                strokeDasharray={isDashed ? "4 4" : "none"}
                                strokeLinecap="round"
                            />
                            {!isDashed && (
                                <polygon
                                    points={`${toX},${toY} ${headX1},${headY1} ${headX2},${headY2}`}
                                    fill={color}
                                />
                            )}
                        </g>
                    );
                };

                // 단일 지점의 힘 벡터 및 평행사변형 그리기 헬퍼
                const renderForceVectorsForPoint = (ptCoord, physData, labelPrefix = "") => {
                    const bx = ptCoord.x;
                    const by = ptCoord.y;

                    // 중력 벡터 끝점
                    const gx = bx + physData.Fg_vec.x * forceScale;
                    const gy = by + physData.Fg_vec.y * forceScale;

                    // 장력 벡터 끝점
                    const tx = bx + physData.T_vec.x * forceScale;
                    const ty = by + physData.T_vec.y * forceScale;

                    // 알짜힘 벡터 끝점
                    const fx = bx + physData.Fnet_vec.x * forceScale;
                    const fy = by + physData.Fnet_vec.y * forceScale;

                    return (
                        <g key={`vectors-${labelPrefix}`}>
                            {/* 평행사변형 점선 (그림 I-15와 100% 일치) */}
                            {showParallelogram && (
                                <g>
                                    <line
                                        x1={gx} y1={gy} x2={fx} y2={fy}
                                        stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="3 3"
                                    />
                                    <line
                                        x1={tx} y1={ty} x2={fx} y2={fy}
                                        stroke="#94a3b8" strokeWidth="1.5" strokeDasharray="3 3"
                                    />
                                </g>
                            )}

                            {/* 중력 벡터 mg (빨강) */}
                            {showGravity && (
                                <g>
                                    {renderArrow(bx, by, gx, gy, "#ef4444", 3)}
                                    <text x={gx + 6} y={gy + 4} fill="#dc2626" fontSize="13" fontWeight="bold" fontStyle="italic">
                                        mg
                                    </text>
                                </g>
                            )}

                            {/* 장력 벡터 T (파랑) */}
                            {showTension && (
                                <g>
                                    {renderArrow(bx, by, tx, ty, "#2563eb", 3)}
                                    <text x={tx - 18} y={ty - 6} fill="#1d4ed8" fontSize="13" fontWeight="bold" fontStyle="italic">
                                        {labelPrefix ? `T_${labelPrefix}` : 'T'}
                                    </text>
                                </g>
                            )}

                            {/* 알짜힘 벡터 F (자주/보라) */}
                            {showNetForce && (
                                <g>
                                    {renderArrow(bx, by, fx, fy, "#a855f7", 3.5)}
                                    <text x={fx + (physData.Fnet_vec.x >= 0 ? 8 : -26)} y={fy + 4} fill="#9333ea" fontSize="14" fontWeight="900" fontStyle="italic">
                                        {labelPrefix ? `F_${labelPrefix}` : 'F'}
                                    </text>
                                </g>
                            )}

                            {/* 성분 분해 모드 (접선 복원력: 핑크, 구심력: 시안) */}
                            {showComponents && (
                                <g>
                                    {/* 접선 성분 Ft = -mg sinθ */}
                                    {(() => {
                                        const ftX = bx + physData.F_tangential * Math.cos(physData.theta) * forceScale;
                                        const ftY = by - physData.F_tangential * Math.sin(physData.theta) * forceScale;
                                        return renderArrow(bx, by, ftX, ftY, "#f43f5e", 2, true);
                                    })()}
                                    {/* 구심 성분 Fc = mv^2/L */}
                                    {(() => {
                                        const fcX = bx - physData.F_centripetal * Math.sin(physData.theta) * forceScale;
                                        const fcY = by - physData.F_centripetal * Math.cos(physData.theta) * forceScale;
                                        return renderArrow(bx, by, fcX, fcY, "#06b6d4", 2, true);
                                    })()}
                                </g>
                            )}

                            {/* 속도 벡터 (초록) */}
                            {showVelocity && Math.abs(physData.v) > 0.05 && (
                                <g>
                                    {(() => {
                                        const vx = bx + physData.v * Math.cos(physData.theta) * 25;
                                        const vy = by - physData.v * Math.sin(physData.theta) * 25;
                                        return (
                                            <g>
                                                {renderArrow(bx, by, vx, vy, "#10b981", 2.5)}
                                                <text x={vx + 6} y={vy} fill="#059669" fontSize="12" fontWeight="bold" fontStyle="italic">v</text>
                                            </g>
                                        );
                                    })()}
                                </g>
                            )}
                        </g>
                    );
                };

                return (
                    <div className="w-full max-w-6xl mx-auto flex flex-col gap-6 text-slate-800 pb-16">
                        
                        {/* 상단 핵심 브리핑 배너 */}
                        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 text-white shadow-xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-4">
                                <div className="w-14 h-14 rounded-2xl bg-indigo-600/30 border border-indigo-400/40 flex items-center justify-center text-indigo-300 shadow-inner">
                                    <Icon name="clock" size={28} />
                                </div>
                                <div>
                                    <div className="flex items-center gap-2">
                                        <span className="px-2 py-0.5 rounded-full text-xs font-bold bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">교과서 그림 I-15 완벽 연계</span>
                                        <span className="text-xs text-slate-400">물리학Ⅱ: 단원 1. 힘과 운동</span>
                                    </div>
                                    <h2 className="text-xl md:text-2xl font-black tracking-tight mt-1 text-white">
                                        진자의 운동: 장력과 중력의 합성 및 알짜힘
                                    </h2>
                                </div>
                            </div>
                            <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2.5 rounded-2xl border border-slate-700">
                                <div className="text-center px-3 border-r border-slate-700">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">주기 (T = 2π√(L/g))</p>
                                    <p className="text-base font-black text-amber-300 font-mono">
                                        {(2 * Math.PI * Math.sqrt(length / g)).toFixed(2)}s
                                    </p>
                                </div>
                                <div className="text-center px-3">
                                    <p className="text-[10px] text-slate-400 font-bold uppercase">최대 속력 (C)</p>
                                    <p className="text-base font-black text-sky-300 font-mono">
                                        {(Math.sqrt(2 * g * length * (1 - Math.cos(maxAngleRad)))).toFixed(2)}m/s
                                    </p>
                                </div>
                            </div>
                        </div>

                        {/* 메인 인터랙션 영역: 좌측 시뮬레이션 캔버스 + 우측 상태 계측 패널 */}
                        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                            
                            {/* 좌측: 인터랙티브 캔버스 & 컨트롤 (7 cols) */}
                            <div className="lg:col-span-7 flex flex-col gap-4">
                                <div className="bg-white rounded-3xl p-4 shadow-lg border border-slate-200 relative overflow-hidden flex flex-col items-center">
                                    
                                    {/* 캔버스 상단 조작 툴바 */}
                                    <div className="w-full flex items-center justify-between px-3 py-2 border-b border-slate-100 mb-2">
                                        <div className="flex items-center gap-1.5">
                                            <span className="inline-block w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                                            <span className="text-xs font-black text-slate-700">가상 진자 실험실</span>
                                        </div>

                                        {/* 모드 토글: 그림 I-15 모드 (5개 위치 동시 표시) */}
                                        <button
                                            onClick={() => setShowFigure15Mode(!showFigure15Mode)}
                                            className={`px-3 py-1 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                                                showFigure15Mode 
                                                    ? 'bg-purple-600 text-white shadow-md shadow-purple-200' 
                                                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                                            }`}
                                        >
                                            <Icon name="layers" size={14} />
                                            <span>교과서 [그림 I-15] 5지점 모드</span>
                                            <span className="font-mono text-[10px]">{showFigure15Mode ? 'ON' : 'OFF'}</span>
                                        </button>
                                    </div>

                                    {/* SVG 시뮬레이션 캔버스 */}
                                    <svg
                                        width="100%"
                                        height="420"
                                        viewBox={`0 0 ${canvasW} ${canvasH}`}
                                        className="bg-gradient-to-b from-slate-50/70 to-white rounded-2xl border border-slate-100 select-none shadow-inner"
                                    >
                                        <defs>
                                            {/* 천장 그림자 패턴 */}
                                            <pattern id="ceilingHatch" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
                                                <line x1="0" y1="0" x2="0" y2="10" stroke="#94a3b8" strokeWidth="2" />
                                            </pattern>
                                        </defs>

                                        {/* 천장 지지대 */}
                                        <rect x={pivotX - 180} y={pivotY - 24} width="360" height="20" fill="#cbd5e1" rx="4" />
                                        <rect x={pivotX - 180} y={pivotY - 24} width="360" height="20" fill="url(#ceilingHatch)" opacity="0.4" rx="4" />
                                        <line x1={pivotX - 190} y1={pivotY - 4} x2={pivotX + 190} y2={pivotY - 4} stroke="#475569" strokeWidth="3" />
                                        
                                        {/* 천장 피벗 힌지 */}
                                        <circle cx={pivotX} cy={pivotY} r="7" fill="#334155" stroke="#ffffff" strokeWidth="2" />
                                        
                                        {/* 각도 기준 연직선 (점선) */}
                                        <line
                                            x1={pivotX} y1={pivotY}
                                            x2={pivotX} y2={pivotY + visualLength + 40}
                                            stroke="#cbd5e1" strokeWidth="1.5" strokeDasharray="4 4"
                                        />

                                        {/* 각도 호 (θ) 표시 */}
                                        {(() => {
                                            const arcR = 55;
                                            const arcX1 = pivotX + arcR * Math.sin(-maxAngleRad);
                                            const arcY1 = pivotY + arcR * Math.cos(-maxAngleRad);
                                            const arcX2 = pivotX + arcR * Math.sin(maxAngleRad);
                                            const arcY2 = pivotY + arcR * Math.cos(maxAngleRad);
                                            return (
                                                <g opacity="0.85">
                                                    <path
                                                        d={`M ${arcX1} ${arcY1} A ${arcR} ${arcR} 0 0 1 ${arcX2} ${arcY2}`}
                                                        fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3 3"
                                                    />
                                                    <text x={pivotX - 24} y={pivotY + 45} fill="#d97706" fontSize="13" fontWeight="bold" fontStyle="italic">θ</text>
                                                    <text x={pivotX + 14} y={pivotY + 45} fill="#d97706" fontSize="13" fontWeight="bold" fontStyle="italic">θ</text>
                                                </g>
                                            );
                                        })()}

                                        {/* 진자 운동 호 궤적 (점선) */}
                                        {(() => {
                                            const aPt = getBobCoord(-maxAngleRad);
                                            const ePt = getBobCoord(maxAngleRad);
                                            return (
                                                <path
                                                    d={`M ${aPt.x} ${aPt.y} A ${visualLength} ${visualLength} 0 0 0 ${ePt.x} ${ePt.y}`}
                                                    fill="none"
                                                    stroke="#cbd5e1"
                                                    strokeWidth="2"
                                                    strokeDasharray="4 4"
                                                />
                                            );
                                        })()}

                                        {/* 모드 1: 그림 I-15 완벽 재현 모드 (A, B, C, D, E 동시 렌더링) */}
                                        {showFigure15Mode && (
                                            <g>
                                                {fivePoints.map((pt) => {
                                                    const coord = getBobCoord(pt.theta);
                                                    return (
                                                        <g key={`pt-${pt.id}`}>
                                                            {/* 실 (황금색 점선) */}
                                                            <line
                                                                x1={pivotX} y1={pivotY} x2={coord.x} y2={coord.y}
                                                                stroke="#f59e0b" strokeWidth="2" strokeDasharray="4 3" opacity="0.75"
                                                            />
                                                            {/* 힘 벡터 및 평행사변형 */}
                                                            {renderForceVectorsForPoint(coord, pt, pt.id)}

                                                            {/* 진자 추 (구슬) */}
                                                            <circle
                                                                cx={coord.x} cy={coord.y} r="18"
                                                                fill="url(#bobGrad)"
                                                                stroke="#3b82f6" strokeWidth="2"
                                                                className="cursor-pointer hover:brightness-110"
                                                                onClick={() => handleJumpTo(pt.theta)}
                                                            />
                                                            {/* 위치 라벨 A, B, C, D, E */}
                                                            <text
                                                                x={coord.x + (pt.theta < 0 ? -28 : pt.theta > 0 ? 22 : 0)}
                                                                y={coord.y + (pt.id === 'C' ? 32 : 6)}
                                                                fill="#1e293b" fontSize="15" fontWeight="900"
                                                                textAnchor={pt.id === 'C' ? 'middle' : 'inherit'}
                                                            >
                                                                {pt.id}
                                                            </text>
                                                        </g>
                                                    );
                                                })}
                                            </g>
                                        )}

                                        {/* 모드 2: 단일 진자 실시간 운동 렌더링 */}
                                        {!showFigure15Mode && (
                                            <g>
                                                {/* 5개 위치 가이드 고스트 표시 */}
                                                {fivePoints.map(pt => {
                                                    const c = getBobCoord(pt.theta);
                                                    return (
                                                        <g key={`ghost-${pt.id}`} opacity="0.35" className="cursor-pointer" onClick={() => handleJumpTo(pt.theta)}>
                                                            <circle cx={c.x} cy={c.y} r="14" fill="#94a3b8" />
                                                            <text x={c.x} y={c.y + 4} fill="#ffffff" fontSize="10" fontWeight="bold" textAnchor="middle">{pt.id}</text>
                                                        </g>
                                                    );
                                                })}

                                                {/* 진자 실 */}
                                                <line
                                                    x1={pivotX} y1={pivotY} x2={currentBob.x} y2={currentBob.y}
                                                    stroke="#1e293b" strokeWidth="2.5"
                                                />

                                                {/* 힘 벡터 및 평행사변형 렌더링 */}
                                                {renderForceVectorsForPoint(currentBob, curPhys, '')}

                                                {/* 실시간 진자 추 구슬 */}
                                                <circle
                                                    cx={currentBob.x} cy={currentBob.y} r="19"
                                                    fill="#38bdf8"
                                                    stroke="#0284c7" strokeWidth="3"
                                                    filter="drop-shadow(0 4px 6px rgba(0,0,0,0.2))"
                                                />
                                                <circle
                                                    cx={currentBob.x - 5} cy={currentBob.y - 5} r="5"
                                                    fill="#ffffff" opacity="0.7"
                                                />
                                            </g>
                                        )}

                                        {/* 추 그라데이션 정의 */}
                                        <defs>
                                            <radialGradient id="bobGrad" cx="35%" cy="35%" r="65%">
                                                <stop offset="0%" stopColor="#bae6fd" />
                                                <stop offset="60%" stopColor="#38bdf8" />
                                                <stop offset="100%" stopColor="#0284c7" />
                                            </radialGradient>
                                        </defs>
                                    </svg>

                                    {/* 캔버스 하단 위치 프리셋 버튼 (A, B, C, D, E 점프) */}
                                    <div className="w-full mt-3 flex flex-wrap items-center justify-between gap-2 px-2">
                                        <div className="flex items-center gap-1">
                                            <span className="text-[11px] font-bold text-slate-500 mr-1">위치 점프:</span>
                                            {fivePoints.map((pt) => (
                                                <button
                                                    key={`btn-${pt.id}`}
                                                    onClick={() => handleJumpTo(pt.theta)}
                                                    className="px-2.5 py-1 rounded-lg text-xs font-black bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 text-slate-700 transition-all border border-slate-200 shadow-sm"
                                                    title={pt.desc}
                                                >
                                                    {pt.id} {pt.id === 'C' ? '(최저)' : pt.id === 'A' || pt.id === 'E' ? '(최고)' : ''}
                                                </button>
                                            ))}
                                        </div>

                                        {/* 재생 컨트롤 버튼 */}
                                        <div className="flex items-center gap-2">
                                            <button
                                                onClick={handlePlayPause}
                                                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1 shadow-sm ${
                                                    isPlaying 
                                                        ? 'bg-amber-500 hover:bg-amber-600 text-white' 
                                                        : 'bg-indigo-600 hover:bg-indigo-700 text-white'
                                                }`}
                                            >
                                                <Icon name={isPlaying ? "pause" : "play"} size={14} />
                                                <span>{isPlaying ? '일시정지' : '운동 재생'}</span>
                                            </button>
                                            <button
                                                onClick={handleReset}
                                                className="p-1.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-600 transition-all border border-slate-200"
                                                title="처음으로 리셋"
                                            >
                                                <Icon name="rotate-ccw" size={14} />
                                            </button>
                                        </div>
                                    </div>
                                </div>

                                {/* 인터랙티브 변인 슬라이더 및 벡터 토글 패널 */}
                                <div className="bg-white rounded-3xl p-5 shadow-lg border border-slate-200 flex flex-col gap-4">
                                    <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                                        <span className="text-xs font-black text-slate-800 flex items-center gap-1.5">
                                            <Icon name="sliders" size={15} className="text-indigo-600" />
                                            실험 변인 및 벡터 표시 제어
                                        </span>
                                        <div className="flex items-center gap-1">
                                            <span className="text-[11px] text-slate-400 font-bold">배속:</span>
                                            {[0.2, 0.5, 1.0].map((s) => (
                                                <button
                                                    key={s}
                                                    onClick={() => setSimSpeed(s)}
                                                    className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                                        simSpeed === s ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'
                                                    }`}
                                                >
                                                    {s}x
                                                </button>
                                            ))}
                                        </div>
                                    </div>

                                    {/* 3대 슬라이더 (최대 진폭 각도 θ, 진자 길이 L, 추 질량 m) */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        <div>
                                            <div className="flex justify-between text-xs font-bold mb-1">
                                                <span className="text-slate-600">진폭 각도 (θ)</span>
                                                <span className="text-indigo-600 font-mono">{maxAngleDeg}°</span>
                                            </div>
                                            <input
                                                type="range" min="5" max="60" step="1"
                                                value={maxAngleDeg}
                                                onChange={(e) => {
                                                    const deg = parseInt(e.target.value);
                                                    setMaxAngleDeg(deg);
                                                    if (!isPlaying) {
                                                        setAngle(-deg * Math.PI / 180);
                                                    }
                                                }}
                                                className="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer"
                                            />
                                            <p className="text-[10px] text-slate-400 mt-1">※ 5°~10°는 작은 각도 근사</p>
                                        </div>

                                        <div>
                                            <div className="flex justify-between text-xs font-bold mb-1">
                                                <span className="text-slate-600">실의 길이 (L)</span>
                                                <span className="text-indigo-600 font-mono">{length.toFixed(1)} m</span>
                                            </div>
                                            <input
                                                type="range" min="0.8" max="2.5" step="0.1"
                                                value={length}
                                                onChange={(e) => setLength(parseFloat(e.target.value))}
                                                className="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer"
                                            />
                                            <p className="text-[10px] text-slate-400 mt-1">길수록 주기 T 증가</p>
                                        </div>

                                        <div>
                                            <div className="flex justify-between text-xs font-bold mb-1">
                                                <span className="text-slate-600">추의 질량 (m)</span>
                                                <span className="text-indigo-600 font-mono">{mass.toFixed(1)} kg</span>
                                            </div>
                                            <input
                                                type="range" min="0.2" max="3.0" step="0.1"
                                                value={mass}
                                                onChange={(e) => setMass(parseFloat(e.target.value))}
                                                className="w-full h-2 bg-slate-100 rounded-lg appearance-none cursor-pointer"
                                            />
                                            <p className="text-[10px] text-slate-400 mt-1">중력 및 장력 비례</p>
                                        </div>
                                    </div>

                                    {/* 벡터 가시성 체크 토글 바 */}
                                    <div className="pt-2 border-t border-slate-100 flex flex-wrap items-center gap-2">
                                        <span className="text-[11px] font-bold text-slate-400 mr-1">시각화 토글:</span>
                                        <button
                                            onClick={() => setShowGravity(!showGravity)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showGravity ? 'bg-red-50 text-red-600 border border-red-200' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <span className="w-2 h-2 rounded-full bg-red-500"></span>
                                            중력 (mg)
                                        </button>
                                        <button
                                            onClick={() => setShowTension(!showTension)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showTension ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                                            장력 (T)
                                        </button>
                                        <button
                                            onClick={() => setShowNetForce(!showNetForce)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showNetForce ? 'bg-purple-50 text-purple-600 border border-purple-200' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                                            알짜힘 (F)
                                        </button>
                                        <button
                                            onClick={() => setShowParallelogram(!showParallelogram)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showParallelogram ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <Icon name="git-commit" size={13} />
                                            평행사변형 점선
                                        </button>
                                        <button
                                            onClick={() => setShowComponents(!showComponents)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showComponents ? 'bg-amber-100 text-amber-800 border border-amber-300' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <Icon name="split" size={13} />
                                            성분 분해(접선/구심)
                                        </button>
                                        <button
                                            onClick={() => setShowVelocity(!showVelocity)}
                                            className={`px-2.5 py-1 rounded-lg text-xs font-bold transition-all flex items-center gap-1 ${
                                                showVelocity ? 'bg-emerald-50 text-emerald-600 border border-emerald-200' : 'bg-slate-100 text-slate-400'
                                            }`}
                                        >
                                            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                            속도 (v)
                                        </button>
                                    </div>
                                </div>
                            </div>

                            {/* 우측: 실시간 물리 계측 HUD & 역학적 에너지 (5 cols) */}
                            <div className="lg:col-span-5 flex flex-col gap-4">
                                
                                {/* 교과서 핵심 물리 계측 카드 */}
                                <div className="bg-white rounded-3xl p-6 shadow-lg border border-slate-200 flex flex-col gap-5">
                                    <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                                        <div className="flex items-center gap-2">
                                            <div className="w-8 h-8 rounded-xl bg-purple-100 text-purple-600 flex items-center justify-center">
                                                <Icon name="gauge" size={18} />
                                            </div>
                                            <div>
                                                <h3 className="font-black text-slate-900 text-sm">실시간 물리 계측기</h3>
                                                <p className="text-[11px] text-slate-400">현재 각도: {curPhys.thetaDeg.toFixed(1)}°</p>
                                            </div>
                                        </div>
                                        <span className={`px-2.5 py-1 rounded-full text-xs font-black ${
                                            Math.abs(curPhys.thetaDeg) < 2 
                                                ? 'bg-emerald-100 text-emerald-700' 
                                                : Math.abs(curPhys.thetaDeg) > maxAngleDeg - 1.5 
                                                    ? 'bg-amber-100 text-amber-700' 
                                                    : 'bg-indigo-100 text-indigo-700'
                                        }`}>
                                            {Math.abs(curPhys.thetaDeg) < 2 ? 'C (최저점)' : Math.abs(curPhys.thetaDeg) > maxAngleDeg - 1.5 ? (curPhys.thetaDeg < 0 ? 'A (최고점)' : 'E (최고점)') : 'B/D (중간)'}
                                        </span>
                                    </div>

                                    {/* 4대 힘 데이터 카드 그리드 */}
                                    <div className="grid grid-cols-2 gap-3">
                                        {/* 중력 mg */}
                                        <div className="p-3.5 rounded-2xl bg-red-50/60 border border-red-100 flex flex-col justify-between">
                                            <div className="flex items-center justify-between">
                                                <span className="text-[11px] font-bold text-red-600">중력 (mg)</span>
                                                <span className="text-[10px] text-red-400">항상 일정(↓)</span>
                                            </div>
                                            <p className="text-xl font-black text-red-700 font-mono mt-1">
                                                {curPhys.F_gravity.toFixed(2)} <span className="text-xs font-normal">N</span>
                                            </p>
                                        </div>

                                        {/* 실의 장력 T */}
                                        <div className="p-3.5 rounded-2xl bg-blue-50/60 border border-blue-100 flex flex-col justify-between">
                                            <div className="flex items-center justify-between">
                                                <span className="text-[11px] font-bold text-blue-600">장력 (T)</span>
                                                <span className="text-[10px] text-blue-400">실 방향</span>
                                            </div>
                                            <p className="text-xl font-black text-blue-700 font-mono mt-1">
                                                {curPhys.T_mag.toFixed(2)} <span className="text-xs font-normal">N</span>
                                            </p>
                                        </div>

                                        {/* 알짜힘 F */}
                                        <div className="p-3.5 rounded-2xl bg-purple-50/60 border border-purple-100 flex flex-col justify-between">
                                            <div className="flex items-center justify-between">
                                                <span className="text-[11px] font-bold text-purple-600">알짜힘 (F = T+mg)</span>
                                                <span className="text-[10px] text-purple-400">합력 벡터</span>
                                            </div>
                                            <p className="text-xl font-black text-purple-700 font-mono mt-1">
                                                {curPhys.Fnet_mag.toFixed(2)} <span className="text-xs font-normal">N</span>
                                            </p>
                                        </div>

                                        {/* 가속도 a */}
                                        <div className="p-3.5 rounded-2xl bg-amber-50/60 border border-amber-100 flex flex-col justify-between">
                                            <div className="flex items-center justify-between">
                                                <span className="text-[11px] font-bold text-amber-600">가속도 (a = F/m)</span>
                                                <span className="text-[10px] text-amber-400">F와 동방향</span>
                                            </div>
                                            <p className="text-xl font-black text-amber-700 font-mono mt-1">
                                                {curPhys.a_mag.toFixed(2)} <span className="text-xs font-normal">m/s²</span>
                                            </p>
                                        </div>
                                    </div>

                                    {/* 알짜힘 성분 분석 (접선 복원력 vs 구심력) */}
                                    <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                                        <p className="text-xs font-black text-slate-700 mb-2 flex items-center justify-between">
                                            <span>알짜힘 성분 분해</span>
                                            <span className="text-[10px] text-slate-400 font-mono">F = √(Ft² + Fc²)</span>
                                        </p>
                                        <div className="space-y-2 text-xs">
                                            <div className="flex items-center justify-between">
                                                <span className="text-slate-600 flex items-center gap-1">
                                                    <span className="w-2 h-2 rounded-full bg-rose-500"></span>
                                                    접선 복원력 (<span className="math-font">mg sinθ</span>):
                                                </span>
                                                <span className="font-mono font-bold text-rose-600">
                                                    {Math.abs(curPhys.F_tangential).toFixed(2)} N
                                                </span>
                                            </div>
                                            <div className="flex items-center justify-between">
                                                <span className="text-slate-600 flex items-center gap-1">
                                                    <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
                                                    구심력 성분 (<span className="math-font">mv²/L</span>):
                                                </span>
                                                <span className="font-mono font-bold text-cyan-600">
                                                    {curPhys.F_centripetal.toFixed(2)} N
                                                </span>
                                            </div>
                                        </div>
                                    </div>

                                    {/* 역학적 에너지 보존 바 (Ep vs Ek) */}
                                    {showEnergyBar && (
                                        <div className="p-4 rounded-2xl bg-indigo-50/50 border border-indigo-100 flex flex-col gap-2">
                                            <div className="flex items-center justify-between text-xs font-bold">
                                                <span className="text-slate-700">역학적 에너지 보존</span>
                                                <span className="font-mono text-indigo-700">{curPhys.E_total.toFixed(2)} J</span>
                                            </div>
                                            
                                            {/* 누적 바 */}
                                            <div className="w-full h-4 rounded-full bg-slate-200 overflow-hidden flex shadow-inner">
                                                <div
                                                    style={{ width: `${curPhys.E_total > 0 ? (curPhys.Ek / curPhys.E_total) * 100 : 0}%` }}
                                                    className="h-full bg-emerald-500 transition-all duration-75"
                                                    title={`운동에너지: ${curPhys.Ek.toFixed(2)} J`}
                                                />
                                                <div
                                                    style={{ width: `${curPhys.E_total > 0 ? (curPhys.Ep / curPhys.E_total) * 100 : 0}%` }}
                                                    className="h-full bg-amber-500 transition-all duration-75"
                                                    title={`위치에너지: ${curPhys.Ep.toFixed(2)} J`}
                                                />
                                            </div>

                                            <div className="flex items-center justify-between text-[11px] font-bold mt-1">
                                                <span className="text-emerald-700 flex items-center gap-1">
                                                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                                                    운동에너지 (Ek): {curPhys.Ek.toFixed(2)} J
                                                </span>
                                                <span className="text-amber-700 flex items-center gap-1">
                                                    <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                                                    위치에너지 (Ep): {curPhys.Ep.toFixed(2)} J
                                                </span>
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {/* 교과서 요약 카드 (그림 I-15 설명문구 발췌) */}
                                <div className="bg-gradient-to-br from-indigo-900 to-slate-900 rounded-3xl p-5 text-white shadow-lg border border-indigo-800/50">
                                    <h4 className="text-xs font-black text-indigo-300 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                                        <Icon name="book-open" size={14} />
                                        교과서 본문 핵심 원리 (그림 I-15)
                                    </h4>
                                    <ul className="space-y-2 text-xs text-slate-200 leading-relaxed list-disc list-inside">
                                        <li>
                                            <strong className="text-white">장력의 크기:</strong> 최고점 <strong>A, E에서 가장 작고</strong>, 최저점 <strong>C에서 가장 크다</strong>.
                                        </li>
                                        <li>
                                            <strong className="text-white">알짜힘의 크기:</strong> 만약 θ의 크기가 작을 경우 <strong>최고점 A, E에서 가장 크고</strong>, 최저점 <strong>C에서 가장 작다</strong>.
                                        </li>
                                        <li>
                                            <strong className="text-white">가속도:</strong> 알짜힘의 방향과 같고 크기에 비례하므로 <strong>최고점 A, E에서 가장 크고, 최저점 C에서 가장 작다</strong>.
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        {/* 하단 탭 메뉴: 1) 힘 벡터 비교표, 2) 교과서 개념 퀴즈, 3) 작은 각도 심화 탐구 */}
                        <div className="bg-white rounded-3xl shadow-lg border border-slate-200 overflow-hidden">
                            {/* 탭 헤더 */}
                            <div className="flex border-b border-slate-200 bg-slate-50/70 overflow-x-auto no-scrollbar">
                                {[
                                    { id: 'explore', label: '📊 5개 위치(A~E) 힘 벡터 정밀 비교표', icon: 'table' },
                                    { id: 'quiz', label: '💡 교과서 핵심 개념 확인 퀴즈', icon: 'help-circle' },
                                    { id: 'compare', label: '🔬 작은 각도(θ ≪ 1) vs 큰 각도 심화 분석', icon: 'activity' }
                                ].map(tab => (
                                    <button
                                        key={tab.id}
                                        onClick={() => setActiveTab(tab.id)}
                                        className={`flex items-center gap-2 px-6 py-4 text-xs md:text-sm font-black whitespace-nowrap transition-all border-b-2 ${
                                            activeTab === tab.id 
                                                ? 'border-indigo-600 text-indigo-600 bg-white' 
                                                : 'border-transparent text-slate-500 hover:text-slate-800'
                                        }`}
                                    >
                                        <Icon name={tab.icon} size={16} />
                                        {tab.label}
                                    </button>
                                ))}
                            </div>

                            {/* 탭 내용 1: 5개 위치(A~E) 비교표 */}
                            {activeTab === 'explore' && (
                                <div className="p-6 overflow-x-auto">
                                    <div className="mb-4 flex flex-col md:flex-row md:items-center justify-between gap-2">
                                        <p className="text-xs text-slate-600">
                                            현재 설정: <strong>θ = {maxAngleDeg}°, L = {length}m, m = {mass}kg</strong> 에서 계산된 교과서 5개 지점의 실제 물리량입니다.
                                        </p>
                                        <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-xl">
                                            위치 관찰 버튼을 누르면 진자가 해당 위치로 즉시 이동합니다.
                                        </span>
                                    </div>

                                    <table className="w-full text-xs text-center border-collapse">
                                        <thead>
                                            <tr className="bg-slate-900 text-white">
                                                <th className="py-3 px-3 rounded-tl-xl">구분</th>
                                                <th className="py-3 px-3">각도 (θ)</th>
                                                <th className="py-3 px-3">속력 (v)</th>
                                                <th className="py-3 px-3 text-red-300">중력 (mg)</th>
                                                <th className="py-3 px-3 text-blue-300">장력 (T)</th>
                                                <th className="py-3 px-3 text-purple-300">알짜힘 (F)</th>
                                                <th className="py-3 px-3 text-amber-300">가속도 (a)</th>
                                                <th className="py-3 px-3 rounded-tr-xl">작동</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-slate-100">
                                            {fivePoints.map(pt => (
                                                <tr key={pt.id} className="hover:bg-slate-50 transition-colors">
                                                    <td className="py-3 px-3 font-black text-slate-800">
                                                        <span className="w-6 h-6 rounded-full inline-flex items-center justify-center bg-slate-100 text-indigo-600 mr-1.5 font-bold">
                                                            {pt.id}
                                                        </span>
                                                        {pt.name}
                                                    </td>
                                                    <td className="py-3 px-3 font-mono">{pt.thetaDeg.toFixed(1)}°</td>
                                                    <td className="py-3 px-3 font-mono font-bold text-emerald-600">
                                                        {pt.speed.toFixed(2)} m/s
                                                    </td>
                                                    <td className="py-3 px-3 font-mono text-red-600 font-bold">
                                                        {pt.F_gravity.toFixed(2)} N (↓)
                                                    </td>
                                                    <td className="py-3 px-3 font-mono text-blue-600 font-bold">
                                                        {pt.T_mag.toFixed(2)} N
                                                    </td>
                                                    <td className="py-3 px-3 font-mono text-purple-600 font-bold">
                                                        {pt.Fnet_mag.toFixed(2)} N
                                                    </td>
                                                    <td className="py-3 px-3 font-mono text-amber-600 font-bold">
                                                        {pt.a_mag.toFixed(2)} m/s²
                                                    </td>
                                                    <td className="py-3 px-3">
                                                        <button
                                                            onClick={() => handleJumpTo(pt.theta)}
                                                            className="px-3 py-1 rounded-lg text-xs font-bold bg-indigo-50 hover:bg-indigo-600 hover:text-white text-indigo-600 transition-all"
                                                        >
                                                            위치 관찰
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>

                                    {/* 핵심 분석 노트 */}
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
                                        <div className="p-4 rounded-2xl bg-red-50/50 border border-red-100 text-xs">
                                            <p className="font-bold text-red-700 mb-1">1. 중력 (mg)의 불변성</p>
                                            <p className="text-slate-600">A, B, C, D, E 어느 위치에서도 중력의 크기와 방향은 연직 아래 방향으로 항상 일정합니다.</p>
                                        </div>
                                        <div className="p-4 rounded-2xl bg-blue-50/50 border border-blue-100 text-xs">
                                            <p className="font-bold text-blue-700 mb-1">2. 장력 (T)의 변화</p>
                                            <p className="text-slate-600">최고점 A, E에서는 속력이 0이므로 <span className="math-font">mg cosθ</span>로 가장 작고, 최저점 C에서는 속력이 최대가 되어 <span className="math-font">mg + mv²/L</span>로 가장 큽니다.</p>
                                        </div>
                                        <div className="p-4 rounded-2xl bg-purple-50/50 border border-purple-100 text-xs">
                                            <p className="font-bold text-purple-700 mb-1">3. 알짜힘 (F)과 가속도</p>
                                            <p className="text-slate-600">알짜힘은 장력과 중력의 벡터 합(평행사변형 대각선)이며, 가속도의 방향과 크기는 항상 알짜힘과 완벽히 비례합니다.</p>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* 탭 내용 2: 교과서 개념 확인 퀴즈 */}
                            {activeTab === 'quiz' && (
                                <div className="p-6 space-y-6">
                                    <div className="bg-indigo-50/50 p-4 rounded-2xl border border-indigo-100">
                                        <h4 className="font-black text-indigo-900 text-sm mb-1">교과서 본문 기반 탐구 퀴즈</h4>
                                        <p className="text-xs text-indigo-700">교과서에 서술된 원리를 깊이 있게 이해했는지 직접 점검해 보세요.</p>
                                    </div>

                                    {/* Q1 */}
                                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col gap-3">
                                        <div className="flex items-center justify-between">
                                            <span className="text-xs font-black text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg">질문 1</span>
                                            <span className="text-xs text-slate-400">최저점 C에서의 힘 분석</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-800">
                                            진자가 최저점 C를 지날 때, 물체에 작용하는 알짜힘의 방향과 크기에 대한 설명으로 옳은 것은?
                                        </p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
                                            {[
                                                { id: 1, text: '속력이 최대이므로 알짜힘은 0이다.' },
                                                { id: 2, text: '중력과 장력이 완전히 평형을 이루어 위아래 힘이 상쇄된다.' },
                                                { id: 3, text: '원운동의 구심 가속도가 필요하므로 알짜힘은 연직 위쪽을 향한다.', correct: true },
                                                { id: 4, text: '진행 방향으로 관성력이 작용하여 수평 방향을 향한다.' }
                                            ].map(opt => (
                                                <button
                                                    key={opt.id}
                                                    onClick={() => setQuizAnswers({ ...quizAnswers, q1: opt.id })}
                                                    className={`p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                                                        quizAnswers.q1 === opt.id 
                                                            ? (quizRevealed.q1 ? (opt.correct ? 'bg-emerald-50 border-emerald-500 text-emerald-800' : 'bg-rose-50 border-rose-500 text-rose-800') : 'bg-indigo-50 border-indigo-500 text-indigo-800')
                                                            : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-700'
                                                    }`}
                                                >
                                                    {opt.text}
                                                </button>
                                            ))}
                                        </div>
                                        <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                                            <button
                                                onClick={() => setQuizRevealed({ ...quizRevealed, q1: !quizRevealed.q1 })}
                                                className="text-xs font-bold text-indigo-600 hover:underline"
                                            >
                                                {quizRevealed.q1 ? '해설 숨기기' : '정답 및 해설 확인'}
                                            </button>
                                            {quizRevealed.q1 && (
                                                <p className="text-xs text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-lg">
                                                    💡 정답: 3번! 최저점 C에서 호를 그리며 회전하므로 중심을 향하는 구심력 F = mv²/L = T - mg &gt; 0 이 작용합니다.
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    {/* Q2 */}
                                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col gap-3">
                                        <div className="flex items-center justify-between">
                                            <span className="text-xs font-black text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg">질문 2</span>
                                            <span className="text-xs text-slate-400">최고점 A, E에서의 장력</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-800">
                                            최고점 A, E에서 순간 속력은 0입니다. 이때 실의 장력 T는 왜 0이 아닐까요?
                                        </p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
                                            {[
                                                { id: 1, text: '실 방향으로 중력 성분(mg cosθ)이 작용하여 실이 팽팽하게 당겨지기 때문', correct: true },
                                                { id: 2, text: '공기 저항력이 실을 당기기 때문' },
                                                { id: 3, text: '물체가 정지해 있어도 원심력이 최대로 작용하기 때문' },
                                                { id: 4, text: '실 자체의 무게 때문에 0이 될 수 없음' }
                                            ].map(opt => (
                                                <button
                                                    key={opt.id}
                                                    onClick={() => setQuizAnswers({ ...quizAnswers, q2: opt.id })}
                                                    className={`p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                                                        quizAnswers.q2 === opt.id 
                                                            ? (quizRevealed.q2 ? (opt.correct ? 'bg-emerald-50 border-emerald-500 text-emerald-800' : 'bg-rose-50 border-rose-500 text-rose-800') : 'bg-indigo-50 border-indigo-500 text-indigo-800')
                                                            : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-700'
                                                    }`}
                                                >
                                                    {opt.text}
                                                </button>
                                            ))}
                                        </div>
                                        <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                                            <button
                                                onClick={() => setQuizRevealed({ ...quizRevealed, q2: !quizRevealed.q2 })}
                                                className="text-xs font-bold text-indigo-600 hover:underline"
                                            >
                                                {quizRevealed.q2 ? '해설 숨기기' : '정답 및 해설 확인'}
                                            </button>
                                            {quizRevealed.q2 && (
                                                <p className="text-xs text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-lg">
                                                    💡 정답: 1번! 최고점에서 v=0이라 구심 가속도는 0이지만, 실 방향 중력 성분 mg cosθ를 지탱해야 하므로 T = mg cosθ &gt; 0 입니다.
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    {/* Q3 */}
                                    <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col gap-3">
                                        <div className="flex items-center justify-between">
                                            <span className="text-xs font-black text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg">질문 3</span>
                                            <span className="text-xs text-slate-400">교과서 핵심 문장 해석</span>
                                        </div>
                                        <p className="text-sm font-bold text-slate-800">
                                            교과서 본문: "만약 θ의 크기가 작을 경우 알짜힘의 크기는 최고점 A, E에서 가장 크고, 최저점 C에서 가장 작다." 이 문장의 물리적 이유는?
                                        </p>
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 mt-1">
                                            {[
                                                { id: 1, text: 'θ가 작으면 C에서의 구심력(mv²/L ∝ θ²)은 거의 0에 가깝고, A, E에서의 복원력(mg sinθ ≈ mgθ)이 지배적이기 때문', correct: true },
                                                { id: 2, text: 'θ가 작으면 중력 자체가 최고점에서 더 세지기 때문' },
                                                { id: 3, text: 'θ가 작으면 실의 장력이 C에서 0이 되기 때문' },
                                                { id: 4, text: '단순히 관측 오차 때문' }
                                            ].map(opt => (
                                                <button
                                                    key={opt.id}
                                                    onClick={() => setQuizAnswers({ ...quizAnswers, q3: opt.id })}
                                                    className={`p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                                                        quizAnswers.q3 === opt.id 
                                                            ? (quizRevealed.q3 ? (opt.correct ? 'bg-emerald-50 border-emerald-500 text-emerald-800' : 'bg-rose-50 border-rose-500 text-rose-800') : 'bg-indigo-50 border-indigo-500 text-indigo-800')
                                                            : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-700'
                                                    }`}
                                                >
                                                    {opt.text}
                                                </button>
                                            ))}
                                        </div>
                                        <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                                            <button
                                                onClick={() => setQuizRevealed({ ...quizRevealed, q3: !quizRevealed.q3 })}
                                                className="text-xs font-bold text-indigo-600 hover:underline"
                                            >
                                                {quizRevealed.q3 ? '해설 숨기기' : '정답 및 해설 확인'}
                                            </button>
                                            {quizRevealed.q3 && (
                                                <p className="text-xs text-emerald-700 font-bold bg-emerald-50 px-3 py-1 rounded-lg">
                                                    💡 정답: 1번! 각도가 작은 단진동 영역에서는 최고점 복원력이 1차항(θ)으로 크고, 중심 구심력은 2차항(θ²)으로 무시할 수 있을 만큼 작아집니다.
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* 탭 내용 3: 작은 각도 vs 큰 각도 심화 비교 */}
                            {activeTab === 'compare' && (
                                <div className="p-6 space-y-6">
                                    <div className="bg-slate-900 text-white p-5 rounded-2xl">
                                        <h4 className="text-sm font-black text-amber-300 mb-2 flex items-center gap-2">
                                            <Icon name="sparkles" size={16} />
                                            교과서 조건 검증: "만약 θ의 크기가 작을 경우" vs "θ가 클 경우"
                                        </h4>
                                        <p className="text-xs text-slate-300 leading-relaxed">
                                            교과서에서 왜 굳이 <em>"만약 θ의 크기가 작을 경우 알짜힘의 크기는 최고점 A, E에서 가장 크고, 최저점 C에서 가장 작다"</em>라는 단서를 달았을까요?
                                            슬라이더를 조작해 각도를 <strong>8°(작은 각도)</strong>와 <strong>60°(큰 각도)</strong>로 바꾸어 알짜힘의 크기를 직접 비교해 보세요!
                                        </p>
                                    </div>

                                    {/* 원클릭 비교 프리셋 버튼 */}
                                    <div className="flex flex-wrap gap-3">
                                        <button
                                            onClick={() => {
                                                setMaxAngleDeg(8);
                                                if (!isPlaying) setAngle(-8 * Math.PI / 180);
                                            }}
                                            className="px-4 py-2 rounded-xl text-xs font-black bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 shadow-sm"
                                        >
                                            📐 작은 각도 모드 설정 (θ = 8°)
                                        </button>
                                        <button
                                            onClick={() => {
                                                setMaxAngleDeg(60);
                                                if (!isPlaying) setAngle(-60 * Math.PI / 180);
                                            }}
                                            className="px-4 py-2 rounded-xl text-xs font-black bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 shadow-sm"
                                        >
                                            📐 큰 각도 모드 설정 (θ = 60°)
                                        </button>
                                    </div>

                                    {/* 이론적 수학 비교 카드 */}
                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                        <div className="p-5 rounded-2xl bg-indigo-50/60 border border-indigo-100">
                                            <h5 className="font-black text-indigo-900 text-xs mb-2">경우 1: 각도 θ가 작을 때 (θ ≤ 10° ≈ 0.17 rad)</h5>
                                            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
                                                <li>최고점 알짜힘: <span className="math-font">F_A = mg sinθ ≈ mg θ</span> (1차 근사)</li>
                                                <li>최저점 구심력: <span className="math-font">F_C = mv_C²/L = 2mg(1-cosθ) ≈ mg θ²</span> (2차 근사)</li>
                                                <li><span className="font-bold text-indigo-700">결론:</span> <span className="math-font">θ² ≪ θ</span> 이므로 <strong className="text-indigo-900">최고점 알짜힘이 최저점보다 훨씬 큽니다!</strong> (교과서 서술과 완전 일치)</li>
                                            </ul>
                                        </div>

                                        <div className="p-5 rounded-2xl bg-amber-50/60 border border-amber-100">
                                            <h5 className="font-black text-amber-900 text-xs mb-2">경우 2: 각도 θ가 클 때 (예: θ = 60°)</h5>
                                            <ul className="text-xs text-slate-700 space-y-1.5 list-disc list-inside">
                                                <li>최고점 알짜힘: <span className="math-font">F_A = mg sin 60° = 0.866 mg</span></li>
                                                <li>최저점 구심력: <span className="math-font">F_C = 2mg(1 - cos 60°) = 1.000 mg</span></li>
                                                <li><span className="font-bold text-amber-700">결론:</span> 각도가 60° 이상으로 커지면 구심력이 복원력보다 커져서 <strong className="text-amber-900">최저점 알짜힘이 최고점보다 더 커질 수도 있습니다!</strong></li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<PendulumSimulation />);
        </script>
    </body>
    </html>
    """

    components.html(react_code, height=920, scrolling=True)

if __name__ == "__main__":
    run_sim()
