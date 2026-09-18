import streamlit as st
import streamlit.components.v1 as components
import os
import base64

def get_base64_image(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    return ""

def run_sim():
    st.title("📜 [도입] 행성 운동의 과학사적 변천: 천동설, 지동설, 그리고 타원 궤도")
    st.markdown("""
    고대 그리스의 **프톨레마이오스 천동설**부터 16세기 **코페르니쿠스 지동설**, 그리고 17세기 **케플러의 타원 궤도 법칙**까지,
    인류가 행성의 운동을 이해해 온 2천 년간의 과학사적 인식의 변화를 실제 역사적 도판 및 인터랙티브 시뮬레이션으로 탐구해 보세요.
    """)

    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    textbook_img = get_base64_image(os.path.join(assets_dir, "planetary_history_textbook.png"))
    geocentric_img = get_base64_image(os.path.join(assets_dir, "geocentric_model.png"))
    heliocentric_img = get_base64_image(os.path.join(assets_dir, "heliocentric_copernicus.png"))

    react_template = r"""
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
                background: #6366f1;
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

            const IMAGES = {
                textbook: "___TEXTBOOK_IMG___",
                geocentric: "___GEOCENTRIC_IMG___",
                heliocentric: "___HELIOCENTRIC_IMG___"
            };

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const PlanetaryHistorySim = () => {
                // 탭 상태: sim(시뮬레이션), gallery(실제 도판 갤러리), compare(비교 질문 및 정리)
                const [mainTab, setMainTab] = useState('sim');

                // 시뮬레이션 모델 선택: 'ptolemy' (천동설), 'copernicus' (원형 지동설), 'kepler' (타원 지동설)
                const [model, setModel] = useState('copernicus');

                // 시뮬레이션 제어
                const [isPlaying, setIsPlaying] = useState(true);
                const [speed, setSpeed] = useState(1.0); // 0.5, 1.0, 2.0
                const [time, setTime] = useState(0);

                // 시각화 옵션
                const [showTrails, setShowTrails] = useState(true);
                const [showSightLine, setShowSightLine] = useState(true); // 지구-행성 시선
                const [showEpicycleCircle, setShowEpicycleCircle] = useState(true); // 프톨레마이오스 주전원 원형 궤적
                const [keplerEccentricity, setKeplerEccentricity] = useState(0.35); // 케플러 타원 이심률 조절

                // 이미지 모달
                const [activeModalImg, setActiveModalImg] = useState(null);

                // 퀴즈 정답/해설 상태
                const [quizAnswers, setQuizAnswers] = useState({ q1: null, q2: null, q3: null, q4: null });
                const [revealed, setRevealed] = useState({ q1: false, q2: false, q3: false, q4: false });

                const animRef = useRef(null);
                const lastTimeRef = useRef(null);
                const trailsRef = useRef([]);

                // 궤적 초기화
                useEffect(() => {
                    trailsRef.current = [];
                }, [model, keplerEccentricity]);

                // 시뮬레이션 애니메이션 루프
                useEffect(() => {
                    if (!isPlaying) {
                        if (animRef.current) cancelAnimationFrame(animRef.current);
                        lastTimeRef.current = null;
                        return;
                    }

                    const loop = (t) => {
                        if (lastTimeRef.current != null) {
                            const dt = Math.min((t - lastTimeRef.current) / 1000, 0.05) * speed;
                            setTime(prev => prev + dt);
                        }
                        lastTimeRef.current = t;
                        animRef.current = requestAnimationFrame(loop);
                    };

                    animRef.current = requestAnimationFrame(loop);
                    return () => {
                        if (animRef.current) cancelAnimationFrame(animRef.current);
                    };
                }, [isPlaying, speed]);

                // 기하 계산 (캔버스 크기 580 x 480)
                const W = 580;
                const H = 480;
                const cX = W / 2;
                const cY = H / 2;

                // 1) 프톨레마이오스 천동설 기하
                const ptolemyState = useMemo(() => {
                    const wSun = 0.85;
                    const sunTheta = time * wSun;
                    const sunX = cX + 130 * Math.cos(sunTheta);
                    const sunY = cY + 130 * Math.sin(sunTheta);

                    // 수성 & 금성: 주전원 중심이 지구-태양 선상에 정렬 (실제 역사적 도판 고증)
                    const mercCenter = { x: cX + 60 * Math.cos(sunTheta), y: cY + 60 * Math.sin(sunTheta) };
                    const mercX = mercCenter.x + 18 * Math.cos(time * 3.2);
                    const mercY = mercCenter.y + 18 * Math.sin(time * 3.2);

                    const venusCenter = { x: cX + 95 * Math.cos(sunTheta), y: cY + 95 * Math.sin(sunTheta) };
                    const venusX = venusCenter.x + 28 * Math.cos(time * 2.1);
                    const venusY = venusCenter.y + 28 * Math.sin(time * 2.1);

                    // 화성: 이심원(R=180) 위를 중심이 돌고, 그 위에서 주전원(r=45) 회전
                    const wDef = 0.45;
                    const defTheta = time * wDef;
                    const defX = cX + 180 * Math.cos(defTheta);
                    const defY = cY + 180 * Math.sin(defTheta);

                    const wEpi = 1.4;
                    const epiTheta = time * wEpi;
                    const marsX = defX + 45 * Math.cos(epiTheta);
                    const marsY = defY + 45 * Math.sin(epiTheta);

                    return {
                        sun: { x: sunX, y: sunY },
                        mercury: { x: mercX, y: mercY, center: mercCenter, r: 18 },
                        venus: { x: venusX, y: venusY, center: venusCenter, r: 28 },
                        marsDeferent: { x: defX, y: defY, r: 180 },
                        mars: { x: marsX, y: marsY, r: 45 }
                    };
                }, [time]);

                // 2) 코페르니쿠스 지동설 기하
                const copernicusState = useMemo(() => {
                    const wEarth = 1.2;
                    const earthTheta = time * wEarth;
                    const earthX = cX + 115 * Math.cos(earthTheta);
                    const earthY = cY + 115 * Math.sin(earthTheta);

                    const wMars = 0.63;
                    const marsTheta = time * wMars;
                    const marsX = cX + 185 * Math.cos(marsTheta);
                    const marsY = cY + 185 * Math.sin(marsTheta);

                    // 내행성
                    const mercX = cX + 50 * Math.cos(time * 3.5);
                    const mercY = cY + 50 * Math.sin(time * 3.5);

                    const venusX = cX + 80 * Math.cos(time * 2.0);
                    const venusY = cY + 80 * Math.sin(time * 2.0);

                    // 지구-화성 시선 연장선
                    const dx = marsX - earthX;
                    const dy = marsY - earthY;
                    const angleSight = Math.atan2(dy, dx);
                    const projX = earthX + 235 * Math.cos(angleSight);
                    const projY = earthY + 235 * Math.sin(angleSight);

                    return {
                        sun: { x: cX, y: cY },
                        mercury: { x: mercX, y: mercY },
                        venus: { x: venusX, y: venusY },
                        earth: { x: earthX, y: earthY, r: 115 },
                        mars: { x: marsX, y: marsY, r: 185 },
                        sightProj: { x: projX, y: projY }
                    };
                }, [time]);

                // 3) 케플러 타원 궤도 기하
                const keplerState = useMemo(() => {
                    const a = 175;
                    const e = keplerEccentricity;
                    const b = a * Math.sqrt(Math.max(0.1, 1 - e * e));
                    const c = a * e;

                    const sunPos = { x: cX - c, y: cY };

                    // 케플러 방정식 풀이 E - e*sin(E) = M
                    const n = 0.8;
                    const M = (time * n) % (2 * Math.PI);
                    let E = M;
                    for (let i = 0; i < 5; i++) {
                        E = E - (E - e * Math.sin(E) - M) / (1 - e * Math.cos(E));
                    }

                    const x_center = a * Math.cos(E);
                    const y_center = b * Math.sin(E);

                    const marsX = cX + x_center;
                    const marsY = cY + y_center;

                    const perihelion = { x: cX - a, y: cY };
                    const aphelion = { x: cX + a, y: cY };

                    const distToSun = Math.sqrt((marsX - sunPos.x)**2 + (marsY - sunPos.y)**2);
                    const speedRel = Math.sqrt(Math.max(0.1, (2 / (distToSun / a)) - 1));

                    return {
                        a, b, e, c,
                        sun: sunPos,
                        mars: { x: marsX, y: marsY },
                        distToSun,
                        speedRel,
                        perihelion,
                        aphelion
                    };
                }, [time, keplerEccentricity]);

                // 궤적 업데이트
                useEffect(() => {
                    if (!showTrails) return;
                    let pt = null;
                    if (model === 'ptolemy') {
                        pt = { x: ptolemyState.mars.x, y: ptolemyState.mars.y };
                    } else if (model === 'copernicus') {
                        pt = { x: copernicusState.sightProj.x, y: copernicusState.sightProj.y };
                    } else if (model === 'kepler') {
                        pt = { x: keplerState.mars.x, y: keplerState.mars.y };
                    }

                    if (pt) {
                        trailsRef.current.push(pt);
                        if (trailsRef.current.length > 280) {
                            trailsRef.current.shift();
                        }
                    }
                }, [time, model, showTrails]);

                return (
                    <div className="w-full max-w-6xl mx-auto flex flex-col gap-6 text-slate-800 pb-16">
                        
                        {/* 상단 브랜딩 배너 */}
                        <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 text-white shadow-xl border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-4">
                            <div className="flex items-center gap-4">
                                <div className="w-14 h-14 rounded-2xl bg-indigo-600/30 border border-indigo-400/40 flex items-center justify-center text-indigo-300 shadow-inner">
                                    <Icon name="orbit" size={28} />
                                </div>
                                <div>
                                    <div className="flex items-center gap-2">
                                        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-indigo-500/30 text-indigo-300 border border-indigo-500/40">교과서 과학사 연계</span>
                                        <span className="text-xs text-slate-400">물리학Ⅱ: 단원 1. 행성의 운동</span>
                                    </div>
                                    <h2 className="text-xl md:text-2xl font-black tracking-tight mt-1 text-white">
                                        행성의 운동에 대한 인식의 변화 (천동설 → 지동설 → 타원 궤도)
                                    </h2>
                                </div>
                            </div>

                            {/* 메인 네비게이션 탭 */}
                            <div className="flex bg-slate-800/80 p-1.5 rounded-2xl border border-slate-700">
                                {[
                                    { id: 'sim', label: '🪐 시뮬레이션', icon: 'play' },
                                    { id: 'gallery', label: '🖼️ 실제 도판 갤러리', icon: 'image' },
                                    { id: 'compare', label: '📋 특징 비교 & 질문', icon: 'help-circle' }
                                ].map(tab => (
                                    <button
                                        key={tab.id}
                                        onClick={() => setMainTab(tab.id)}
                                        className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                                            mainTab === tab.id 
                                                ? 'bg-indigo-600 text-white shadow-md' 
                                                : 'text-slate-400 hover:text-white'
                                        }`}
                                    >
                                        <Icon name={tab.icon} size={14} />
                                        {tab.label}
                                    </button>
                                ))}
                            </div>
                        </div>

                        {/* [탭 1: 시뮬레이션 화면] */}
                        {mainTab === 'sim' && (
                            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                                
                                {/* 좌측 캔버스 & 3대 모델 선택 컨트롤 (7 cols) */}
                                <div className="lg:col-span-7 flex flex-col gap-4">
                                    <div className="bg-white rounded-3xl p-5 shadow-lg border border-slate-200 flex flex-col items-center">
                                        
                                        {/* 모델 선택 라디오 버튼 바 */}
                                        <div className="w-full grid grid-cols-3 gap-2 p-1.5 bg-slate-100 rounded-2xl mb-3">
                                            {[
                                                { id: 'ptolemy', label: '1. 프톨레마이오스 (천동설)', sub: '지구 중심 + 주전원' },
                                                { id: 'copernicus', label: '2. 코페르니쿠스 (지동설)', sub: '태양 중심 + 원 궤도' },
                                                { id: 'kepler', label: '3. 케플러 (타원 궤도)', sub: '태양 초점 + 속력 변화' }
                                            ].map(m => (
                                                <button
                                                    key={m.id}
                                                    onClick={() => setModel(m.id)}
                                                    className={`py-2.5 px-2 rounded-xl text-center transition-all ${
                                                        model === m.id 
                                                            ? 'bg-indigo-600 text-white shadow-md' 
                                                            : 'text-slate-600 hover:bg-white/80'
                                                    }`}
                                                >
                                                    <p className="text-xs font-black leading-tight">{m.label}</p>
                                                    <p className={`text-[10px] mt-0.5 ${model === m.id ? 'text-indigo-200' : 'text-slate-400'}`}>
                                                        {m.sub}
                                                    </p>
                                                </button>
                                            ))}
                                        </div>

                                        {/* SVG 시뮬레이션 캔버스 */}
                                        <svg
                                            width="100%"
                                            height="430"
                                            viewBox={`0 0 ${W} ${H}`}
                                            className="bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 rounded-2xl border border-slate-800 select-none shadow-inner"
                                        >
                                            <defs>
                                                <radialGradient id="sunGlow" cx="50%" cy="50%" r="50%">
                                                    <stop offset="0%" stopColor="#fde047" />
                                                    <stop offset="40%" stopColor="#f59e0b" stopOpacity="0.9" />
                                                    <stop offset="100%" stopColor="#ea580c" stopOpacity="0" />
                                                </radialGradient>
                                                <radialGradient id="earthGlow" cx="50%" cy="50%" r="50%">
                                                    <stop offset="0%" stopColor="#67e8f9" />
                                                    <stop offset="80%" stopColor="#0284c7" />
                                                    <stop offset="100%" stopColor="#0369a1" />
                                                </radialGradient>
                                            </defs>

                                            {/* 배경 좌표 십자선 */}
                                            <line x1={cX} y1={20} x2={cX} y2={H - 20} stroke="#334155" strokeWidth="1" strokeDasharray="2 4" />
                                            <line x1={20} y1={cY} x2={W - 20} y2={cY} stroke="#334155" strokeWidth="1" strokeDasharray="2 4" />

                                            {/* 외곽 천구 원형 경계 */}
                                            <circle cx={cX} cy={cY} r="230" fill="none" stroke="#475569" strokeWidth="1" strokeDasharray="4 6" opacity="0.6" />
                                            <text x={cX} y={32} fill="#94a3b8" fontSize="10" fontWeight="bold" textAnchor="middle" letterSpacing="1">
                                                항성 천구 (STELLARUM FIXARUM SPHAERA)
                                            </text>

                                            {/* 1) 프톨레마이오스 천동설 렌더링 */}
                                            {model === 'ptolemy' && (
                                                <g>
                                                    <circle cx={cX} cy={cY} r="12" fill="url(#earthGlow)" />
                                                    <text x={cX} y={cY + 24} fill="#38bdf8" fontSize="11" fontWeight="bold" textAnchor="middle">지구 (Earth)</text>

                                                    <circle cx={cX} cy={cY} r="130" fill="none" stroke="#f59e0b" strokeWidth="1" strokeDasharray="3 3" opacity="0.4" />
                                                    <circle cx={ptolemyState.sun.x} cy={ptolemyState.sun.y} r="10" fill="#f59e0b" />
                                                    <text x={ptolemyState.sun.x + 14} y={ptolemyState.sun.y + 4} fill="#fcd34d" fontSize="11" fontWeight="bold">태양 (Sun)</text>

                                                    <line x1={cX} y1={cY} x2={ptolemyState.sun.x} y2={ptolemyState.sun.y} stroke="#f59e0b" strokeWidth="1" strokeDasharray="2 2" opacity="0.5" />
                                                    
                                                    {/* 수성 주전원 */}
                                                    <circle cx={ptolemyState.mercury.center.x} cy={ptolemyState.mercury.center.y} r={ptolemyState.mercury.r} fill="none" stroke="#cbd5e1" strokeWidth="1" opacity="0.5" />
                                                    <circle cx={ptolemyState.mercury.x} cy={ptolemyState.mercury.y} r="4" fill="#94a3b8" />

                                                    {/* 금성 주전원 */}
                                                    <circle cx={ptolemyState.venus.center.x} cy={ptolemyState.venus.center.y} r={ptolemyState.venus.r} fill="none" stroke="#fde047" strokeWidth="1" opacity="0.5" />
                                                    <circle cx={ptolemyState.venus.x} cy={ptolemyState.venus.y} r="6" fill="#fef08a" />

                                                    {/* 화성 이심원 */}
                                                    <circle cx={cX} cy={cY} r={ptolemyState.marsDeferent.r} fill="none" stroke="#f43f5e" strokeWidth="1.5" strokeDasharray="4 4" opacity="0.6" />
                                                    <circle cx={ptolemyState.marsDeferent.x} cy={ptolemyState.marsDeferent.y} r="4" fill="#fb7185" />
                                                    <line x1={cX} y1={cY} x2={ptolemyState.marsDeferent.x} y2={ptolemyState.marsDeferent.y} stroke="#e11d48" strokeWidth="1" opacity="0.4" />

                                                    {/* 화성 주전원 */}
                                                    {showEpicycleCircle && (
                                                        <circle
                                                            cx={ptolemyState.marsDeferent.x}
                                                            cy={ptolemyState.marsDeferent.y}
                                                            r={ptolemyState.mars.r}
                                                            fill="none"
                                                            stroke="#f43f5e"
                                                            strokeWidth="1.5"
                                                        />
                                                    )}

                                                    <line
                                                        x1={ptolemyState.marsDeferent.x}
                                                        y1={ptolemyState.marsDeferent.y}
                                                        x2={ptolemyState.mars.x}
                                                        y2={ptolemyState.mars.y}
                                                        stroke="#fb7185"
                                                        strokeWidth="2"
                                                    />

                                                    <circle cx={ptolemyState.mars.x} cy={ptolemyState.mars.y} r="8" fill="#e11d48" stroke="#ffffff" strokeWidth="1.5" />
                                                    <text x={ptolemyState.mars.x + 12} y={ptolemyState.mars.y + 4} fill="#fda4af" fontSize="12" fontWeight="bold">화성 (Mars)</text>

                                                    {/* 화성 궤적 */}
                                                    {showTrails && trailsRef.current.length > 1 && (
                                                        <path
                                                            d={trailsRef.current.reduce((acc, p, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`, '')}
                                                            fill="none"
                                                            stroke="#f43f5e"
                                                            strokeWidth="2"
                                                            opacity="0.8"
                                                        />
                                                    )}
                                                </g>
                                            )}

                                            {/* 2) 코페르니쿠스 지동설 렌더링 */}
                                            {model === 'copernicus' && (
                                                <g>
                                                    <circle cx={cX} cy={cY} r="24" fill="url(#sunGlow)" />
                                                    <circle cx={cX} cy={cY} r="12" fill="#ea580c" />
                                                    <text x={cX} y={cY + 28} fill="#fcd34d" fontSize="11" fontWeight="bold" textAnchor="middle">태양 (Sol.)</text>

                                                    <circle cx={cX} cy={cY} r="50" fill="none" stroke="#64748b" strokeWidth="1" strokeDasharray="2 4" />
                                                    <circle cx={copernicusState.mercury.x} cy={copernicusState.mercury.y} r="4" fill="#94a3b8" />

                                                    <circle cx={cX} cy={cY} r="80" fill="none" stroke="#64748b" strokeWidth="1" strokeDasharray="2 4" />
                                                    <circle cx={copernicusState.venus.x} cy={copernicusState.venus.y} r="6" fill="#fef08a" />

                                                    <circle cx={cX} cy={cY} r={copernicusState.earth.r} fill="none" stroke="#38bdf8" strokeWidth="1.5" strokeDasharray="3 3" opacity="0.6" />
                                                    <circle cx={copernicusState.earth.x} cy={copernicusState.earth.y} r="9" fill="url(#earthGlow)" stroke="#ffffff" strokeWidth="1" />
                                                    <text x={copernicusState.earth.x + 12} y={copernicusState.earth.y + 4} fill="#7dd3fc" fontSize="11" fontWeight="bold">지구</text>

                                                    <circle cx={cX} cy={cY} r={copernicusState.mars.r} fill="none" stroke="#f43f5e" strokeWidth="1.5" strokeDasharray="4 4" opacity="0.6" />
                                                    <circle cx={copernicusState.mars.x} cy={copernicusState.mars.y} r="8" fill="#e11d48" stroke="#ffffff" strokeWidth="1" />
                                                    <text x={copernicusState.mars.x + 12} y={copernicusState.mars.y + 4} fill="#fda4af" fontSize="11" fontWeight="bold">화성</text>

                                                    {showSightLine && (
                                                        <g>
                                                            <line
                                                                x1={copernicusState.earth.x} y1={copernicusState.earth.y}
                                                                x2={copernicusState.sightProj.x} y2={copernicusState.sightProj.y}
                                                                stroke="#a855f7" strokeWidth="1.5" strokeDasharray="3 3"
                                                            />
                                                            <circle cx={copernicusState.sightProj.x} cy={copernicusState.sightProj.y} r="6" fill="#c084fc" stroke="#ffffff" strokeWidth="1.5" />
                                                            <text x={copernicusState.sightProj.x + 8} y={copernicusState.sightProj.y + 4} fill="#d8b4fe" fontSize="10" fontWeight="bold">
                                                                겉보기 위치
                                                            </text>
                                                        </g>
                                                    )}

                                                    {showTrails && trailsRef.current.length > 1 && (
                                                        <path
                                                            d={trailsRef.current.reduce((acc, p, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`, '')}
                                                            fill="none"
                                                            stroke="#c084fc"
                                                            strokeWidth="3"
                                                            opacity="0.85"
                                                        />
                                                    )}
                                                </g>
                                            )}

                                            {/* 3) 케플러 타원 궤도 렌더링 */}
                                            {model === 'kepler' && (
                                                <g>
                                                    <ellipse
                                                        cx={cX} cy={cY}
                                                        rx={keplerState.a} ry={keplerState.b}
                                                        fill="none"
                                                        stroke="#6366f1"
                                                        strokeWidth="2"
                                                        strokeDasharray="4 4"
                                                    />

                                                    <circle cx={keplerState.sun.x} cy={keplerState.sun.y} r="20" fill="url(#sunGlow)" />
                                                    <circle cx={keplerState.sun.x} cy={keplerState.sun.y} r="10" fill="#ea580c" />
                                                    <text x={keplerState.sun.x} y={keplerState.sun.y + 24} fill="#fcd34d" fontSize="11" fontWeight="bold" textAnchor="middle">
                                                        태양 (초점 F1)
                                                    </text>

                                                    <circle cx={cX + keplerState.c} cy={cY} r="3" fill="#64748b" />
                                                    <text x={cX + keplerState.c} y={cY + 16} fill="#94a3b8" fontSize="9" textAnchor="middle">초점 F2</text>

                                                    <line
                                                        x1={keplerState.sun.x} y1={keplerState.sun.y}
                                                        x2={keplerState.mars.x} y2={keplerState.mars.y}
                                                        stroke="#f59e0b" strokeWidth="2"
                                                    />

                                                    <circle cx={keplerState.perihelion.x} cy={keplerState.perihelion.y} r="4" fill="#10b981" />
                                                    <text x={keplerState.perihelion.x - 8} y={keplerState.perihelion.y - 10} fill="#34d399" fontSize="10" fontWeight="bold">
                                                        근일점 (가장 빠름)
                                                    </text>

                                                    <circle cx={keplerState.aphelion.x} cy={keplerState.aphelion.y} r="4" fill="#38bdf8" />
                                                    <text x={keplerState.aphelion.x + 8} y={keplerState.aphelion.y - 10} fill="#38bdf8" fontSize="10" fontWeight="bold">
                                                        원일점 (가장 느림)
                                                    </text>

                                                    <circle cx={keplerState.mars.x} cy={keplerState.mars.y} r="9" fill="#ef4444" stroke="#ffffff" strokeWidth="2" />
                                                    <text x={keplerState.mars.x + 12} y={keplerState.mars.y + 4} fill="#fca5a5" fontSize="12" fontWeight="bold">
                                                        행성 (속력: {keplerState.speedRel.toFixed(2)}x)
                                                    </text>

                                                    {showTrails && trailsRef.current.length > 1 && (
                                                        <path
                                                            d={trailsRef.current.reduce((acc, p, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`, '')}
                                                            fill="none"
                                                            stroke="#ef4444"
                                                            strokeWidth="2"
                                                            opacity="0.8"
                                                        />
                                                    )}
                                                </g>
                                            )}
                                        </svg>

                                        {/* 캔버스 하단 컨트롤 바 */}
                                        <div className="w-full mt-3 flex flex-wrap items-center justify-between gap-2 px-2">
                                            <div className="flex items-center gap-2">
                                                <button
                                                    onClick={() => setIsPlaying(!isPlaying)}
                                                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                                                        isPlaying ? 'bg-amber-500 text-white' : 'bg-indigo-600 text-white'
                                                    }`}
                                                >
                                                    <Icon name={isPlaying ? "pause" : "play"} size={14} />
                                                    <span>{isPlaying ? '일시정지' : '재생'}</span>
                                                </button>
                                                <button
                                                    onClick={() => { setTime(0); trailsRef.current = []; }}
                                                    className="p-1.5 rounded-xl text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-600 transition-all"
                                                    title="처음으로 리셋"
                                                >
                                                    <Icon name="rotate-ccw" size={14} />
                                                </button>
                                            </div>

                                            <div className="flex items-center gap-2">
                                                <button
                                                    onClick={() => setShowTrails(!showTrails)}
                                                    className={`px-2.5 py-1 rounded-lg text-xs font-bold border transition-all ${
                                                        showTrails ? 'bg-purple-50 text-purple-700 border-purple-200' : 'bg-slate-100 text-slate-400 border-slate-200'
                                                    }`}
                                                >
                                                    궤적(Trail) {showTrails ? 'ON' : 'OFF'}
                                                </button>

                                                {model === 'copernicus' && (
                                                    <button
                                                        onClick={() => setShowSightLine(!showSightLine)}
                                                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border transition-all ${
                                                            showSightLine ? 'bg-indigo-50 text-indigo-700 border-indigo-200' : 'bg-slate-100 text-slate-400 border-slate-200'
                                                        }`}
                                                    >
                                                        시선 광선(Ray) {showSightLine ? 'ON' : 'OFF'}
                                                    </button>
                                                )}

                                                {model === 'ptolemy' && (
                                                    <button
                                                        onClick={() => setShowEpicycleCircle(!showEpicycleCircle)}
                                                        className={`px-2.5 py-1 rounded-lg text-xs font-bold border transition-all ${
                                                            showEpicycleCircle ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-slate-100 text-slate-400 border-slate-200'
                                                        }`}
                                                    >
                                                        주전원(Epicycle) 원 {showEpicycleCircle ? 'ON' : 'OFF'}
                                                    </button>
                                                )}
                                            </div>
                                        </div>

                                        {model === 'kepler' && (
                                            <div className="w-full mt-3 p-3 bg-indigo-50/60 rounded-2xl border border-indigo-100 flex items-center justify-between gap-4">
                                                <div className="flex items-center gap-2">
                                                    <span className="text-xs font-black text-indigo-900">타원 이심률 (e):</span>
                                                    <span className="text-xs font-mono font-black text-indigo-600">{keplerEccentricity.toFixed(2)}</span>
                                                </div>
                                                <input
                                                    type="range" min="0.0" max="0.6" step="0.05"
                                                    value={keplerEccentricity}
                                                    onChange={(e) => setKeplerEccentricity(parseFloat(e.target.value))}
                                                    className="flex-1 h-2 bg-indigo-200 rounded-lg appearance-none cursor-pointer"
                                                />
                                                <span className="text-[11px] text-slate-500 font-bold whitespace-nowrap">
                                                    {keplerEccentricity === 0 ? '원(e=0)' : '타원(e>0)'}
                                                </span>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* 우측 설명 카드 & 실제 이미지 썸네일 (5 cols) */}
                                <div className="lg:col-span-5 flex flex-col gap-4">
                                    
                                    <div className="bg-white rounded-3xl p-5 shadow-lg border border-slate-200 flex flex-col gap-3">
                                        {model === 'ptolemy' && (
                                            <div className="space-y-3">
                                                <div className="flex items-center gap-2 border-b border-slate-100 pb-2">
                                                    <span className="p-2 rounded-xl bg-rose-100 text-rose-600 font-bold text-xs">모델 1</span>
                                                    <h3 className="font-black text-slate-900 text-base">프톨레마이오스의 천동설 (AD 150년경)</h3>
                                                </div>
                                                <ul className="text-xs text-slate-600 space-y-2 leading-relaxed list-disc list-inside">
                                                    <li><strong>우주의 중심:</strong> <strong>지구</strong>가 우주의 중심에 고정되어 있음.</li>
                                                    <li><strong>완벽한 원운동:</strong> 하늘의 천체는 오직 '완벽한 등속 원운동'만 해야 한다는 고대 철학적 신념.</li>
                                                    <li><strong>주전원(Epicycle)의 도입:</strong> 행성이 뒤로 후진하는 <strong>'역행 운동'</strong>을 설명하기 위해, 대원(이심원) 위를 도는 작은 원(주전원)을 도입함.</li>
                                                    <li><strong>수성과 금성:</strong> 내행성의 주전원 중심은 항상 지구-태양 연결선상에 고정되어 태양 곁을 크게 벗어나지 못함(최대 이각 설명).</li>
                                                </ul>
                                            </div>
                                        )}

                                        {model === 'copernicus' && (
                                            <div className="space-y-3">
                                                <div className="flex items-center gap-2 border-b border-slate-100 pb-2">
                                                    <span className="p-2 rounded-xl bg-indigo-100 text-indigo-600 font-bold text-xs">모델 2</span>
                                                    <h3 className="font-black text-slate-900 text-base">코페르니쿠스의 지동설 (1543년)</h3>
                                                </div>
                                                <ul className="text-xs text-slate-600 space-y-2 leading-relaxed list-disc list-inside">
                                                    <li><strong>우주의 중심:</strong> <strong>태양</strong>이 우주의 중심이며, 지구도 태양을 도는 행성 중 하나임.</li>
                                                    <li><strong>역행 운동의 자연스러운 설명:</strong> 주전원이라는 복잡한 장치 없이, 안쪽을 빠르게 도는 지구가 바깥쪽 화성을 <strong>추월(Overtake)</strong>하면서 배경 별자리에 대해 뒤로 밀려나는 현상으로 명쾌하게 설명함!</li>
                                                    <li><strong>미완의 혁명:</strong> 여전히 '완벽한 원 궤도'와 '등속'의 신념을 벗어나지 못해, 관측 오차를 보정하기 위해 소형 주전원을 여전히 사용함.</li>
                                                </ul>
                                            </div>
                                        )}

                                        {model === 'kepler' && (
                                            <div className="space-y-3">
                                                <div className="flex items-center gap-2 border-b border-slate-100 pb-2">
                                                    <span className="p-2 rounded-xl bg-emerald-100 text-emerald-600 font-bold text-xs">모델 3</span>
                                                    <h3 className="font-black text-slate-900 text-base">케플러의 타원 궤도 법칙 (1609년)</h3>
                                                </div>
                                                <ul className="text-xs text-slate-600 space-y-2 leading-relaxed list-disc list-inside">
                                                    <li><strong>2천 년 편견의 타파:</strong> 티코 브라헤의 정밀 화성 관측 자료에서 나타난 <strong>단 8분의 오차</strong>를 놓치지 않고 분석하여 '완벽한 원'의 굴레를 깸.</li>
                                                    <li><strong>제1법칙 (타원 궤도):</strong> 행성은 태양을 한 초점으로 하는 <strong>타원 궤도</strong>를 돎.</li>
                                                    <li><strong>제2법칙 (면적 속도 일정):</strong> 등속이 아닌 <strong>가변 속력</strong>! 태양에 가까운 근일점에서 가장 빠르고, 먼 원일점에서 가장 느림.</li>
                                                </ul>
                                            </div>
                                        )}
                                    </div>

                                    {/* 실제 도판 미리보기 썸네일 카드 */}
                                    <div className="bg-slate-900 text-white rounded-3xl p-5 shadow-lg border border-slate-800 flex flex-col gap-3">
                                        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                                            <span className="text-xs font-black text-amber-300 flex items-center gap-1.5">
                                                <Icon name="book-open" size={14} />
                                                실제 역사적 원전 도판 미리보기
                                            </span>
                                            <button
                                                onClick={() => setMainTab('gallery')}
                                                className="text-[11px] font-bold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                                            >
                                                전체보기 <Icon name="arrow-right" size={12} />
                                            </button>
                                        </div>

                                        <div className="grid grid-cols-2 gap-3">
                                            <div
                                                onClick={() => setMainTab('gallery')}
                                                className="bg-slate-800/80 p-2.5 rounded-2xl border border-slate-700 cursor-pointer hover:border-indigo-500 transition-all group"
                                            >
                                                <div className="w-full h-24 bg-white/5 rounded-xl overflow-hidden mb-2 flex items-center justify-center p-1">
                                                    <img src={IMAGES.geocentric} alt="천동설 도판" className="max-h-full object-contain group-hover:scale-105 transition-transform" />
                                                </div>
                                                <p className="text-[11px] font-black text-slate-200">천동설 실제 도판</p>
                                                <p className="text-[9px] text-slate-400">이심원과 주전원 구조</p>
                                            </div>

                                            <div
                                                onClick={() => setMainTab('gallery')}
                                                className="bg-slate-800/80 p-2.5 rounded-2xl border border-slate-700 cursor-pointer hover:border-indigo-500 transition-all group"
                                            >
                                                <div className="w-full h-24 bg-white/5 rounded-xl overflow-hidden mb-2 flex items-center justify-center p-1">
                                                    <img src={IMAGES.heliocentric} alt="지동설 도판" className="max-h-full object-contain group-hover:scale-105 transition-transform" />
                                                </div>
                                                <p className="text-[11px] font-black text-slate-200">코페르니쿠스 원전</p>
                                                <p className="text-[9px] text-slate-400">1543년 『천구의 회전』</p>
                                            </div>
                                        </div>
                                    </div>

                                </div>
                            </div>
                        )}

                        {/* [탭 2: 실제 문헌 도판 & 교과서 갤러리] */}
                        {mainTab === 'gallery' && (
                            <div className="flex flex-col gap-6">
                                
                                <div className="bg-white rounded-3xl p-6 shadow-lg border border-slate-200">
                                    <div className="flex items-center gap-2 border-b border-slate-100 pb-3 mb-4">
                                        <div className="w-8 h-8 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center">
                                            <Icon name="book" size={18} />
                                        </div>
                                        <div>
                                            <h3 className="font-black text-slate-900 text-base">교과서 핵심 삽화: 행성의 운동에 대한 인식의 변화</h3>
                                            <p className="text-xs text-slate-500">과거에는 행성이 원 궤도를 따라 운동한다고 믿었으나 케플러의 연구에 의해 타원 궤도를 따라 운동함을 알게 됨</p>
                                        </div>
                                    </div>
                                    <div className="w-full bg-slate-50 rounded-2xl p-4 border border-slate-100 flex items-center justify-center">
                                        <img
                                            src={IMAGES.textbook}
                                            alt="행성의 운동에 대한 인식의 변화 (프톨레마이오스-코페르니쿠스-케플러)"
                                            className="max-h-[440px] w-full object-contain rounded-xl shadow-sm cursor-zoom-in hover:brightness-105 transition-all"
                                            onClick={() => setActiveModalImg(IMAGES.textbook)}
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    
                                    {/* 1. 천동설 실제 도판 상세 카드 */}
                                    <div className="bg-white rounded-3xl p-6 shadow-lg border border-slate-200 flex flex-col gap-4">
                                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                                            <div>
                                                <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-rose-100 text-rose-700">실제 도판 1</span>
                                                <h4 className="font-black text-slate-900 text-base mt-1">프톨레마이오스의 천동설 체계도</h4>
                                            </div>
                                            <span className="text-xs text-slate-400 font-mono">AD 2세기</span>
                                        </div>

                                        <div className="w-full h-72 bg-slate-50 rounded-2xl p-3 border border-slate-100 flex items-center justify-center overflow-hidden">
                                            <img
                                                src={IMAGES.geocentric}
                                                alt="천동설 실제 도판"
                                                className="max-h-full max-w-full object-contain cursor-zoom-in hover:scale-105 transition-transform"
                                                onClick={() => setActiveModalImg(IMAGES.geocentric)}
                                            />
                                        </div>

                                        <div className="p-4 bg-rose-50/50 rounded-2xl border border-rose-100 text-xs text-slate-700 space-y-2">
                                            <p className="font-black text-rose-900">🔍 도판의 핵심 관찰 포인트:</p>
                                            <ul className="space-y-1.5 list-disc list-inside leading-relaxed text-slate-600">
                                                <li><strong>지구(Earth) 중심:</strong> 지구는 중심에 정지해 있고 달(Moon), 수성(Mercury), 금성(Venus), 태양(Sun), 화성(Mars), 목성(Jupiter), 토성(Saturn) 순으로 공전함.</li>
                                                <li><strong>수성과 금성의 정렬:</strong> 수성과 금성의 주전원 중심은 항상 <strong>지구-태양 직선상</strong>에 고정되어 있음 (실제 도판에서 태양과 일직선으로 그려진 이유).</li>
                                                <li><strong>외행성 주전원:</strong> 화성, 목성, 토성의 주전원 반경 막대는 모두 <strong>지구-태양 방향과 항상 평행</strong>하게 움직임.</li>
                                            </ul>
                                        </div>
                                    </div>

                                    {/* 2. 코페르니쿠스 지동설 실제 도판 상세 카드 */}
                                    <div className="bg-white rounded-3xl p-6 shadow-lg border border-slate-200 flex flex-col gap-4">
                                        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                                            <div>
                                                <span className="px-2.5 py-0.5 rounded-full text-xs font-black bg-indigo-100 text-indigo-700">실제 도판 2</span>
                                                <h4 className="font-black text-slate-900 text-base mt-1">코페르니쿠스 『천구의 회전에 관하여』 (1543)</h4>
                                            </div>
                                            <span className="text-xs text-slate-400 font-mono">1543년 출간</span>
                                        </div>

                                        <div className="w-full h-72 bg-slate-50 rounded-2xl p-3 border border-slate-100 flex items-center justify-center overflow-hidden">
                                            <img
                                                src={IMAGES.heliocentric}
                                                alt="코페르니쿠스 지동설 목판화"
                                                className="max-h-full max-w-full object-contain cursor-zoom-in hover:scale-105 transition-transform"
                                                onClick={() => setActiveModalImg(IMAGES.heliocentric)}
                                            />
                                        </div>

                                        <div className="p-4 bg-indigo-50/50 rounded-2xl border border-indigo-100 text-xs text-slate-700 space-y-2">
                                            <p className="font-black text-indigo-900">🔍 도판의 라틴어 원문 해석:</p>
                                            <ul className="space-y-1.5 list-disc list-inside leading-relaxed text-slate-600">
                                                <li><strong>Sol. (중심):</strong> 우주의 한가운데에 태양(Sol)이 움직이지 않고 당당히 자리 잡고 있음.</li>
                                                <li><strong>V. Telluris cum orbe lunari:</strong> 5번째 원은 <strong>지구(Terra)</strong>와 달의 궤도로, 달이 지구 주위를 돌며 함께 태양을 공전함.</li>
                                                <li><strong>I. Stellarum fixarum sphaera immobilis:</strong> 가장 바깥의 제1천구는 '움직이지 않는 고정된 별들의 천구'를 뜻함.</li>
                                            </ul>
                                        </div>
                                    </div>

                                </div>
                            </div>
                        )}

                        {/* [탭 3: 특징 비교 & 탐구 질문] */}
                        {mainTab === 'compare' && (
                            <div className="flex flex-col gap-6">
                                
                                <div className="bg-white rounded-3xl p-6 shadow-lg border border-slate-200 overflow-x-auto">
                                    <h3 className="font-black text-slate-900 text-base mb-4 flex items-center gap-2">
                                        <Icon name="table" size={20} className="text-indigo-600" />
                                        행성 운동 3대 모델 특징 비교 매트릭스
                                    </h3>

                                    <table className="w-full text-xs text-left border-collapse min-w-[620px]">
                                        <thead>
                                            <tr className="bg-slate-900 text-white text-center">
                                                <th className="py-3 px-4 rounded-tl-xl">비교 항목</th>
                                                <th className="py-3 px-4 bg-rose-950/80">1. 프톨레마이오스 천동설</th>
                                                <th className="py-3 px-4 bg-indigo-950/80">2. 코페르니쿠스 지동설</th>
                                                <th className="py-3 px-4 bg-emerald-950/80 rounded-tr-xl">3. 케플러 타원 운동</th>
                                            </tr>
                                        </thead>
                                        <tbody className="divide-y divide-slate-100">
                                            <tr className="hover:bg-slate-50">
                                                <td className="py-3 px-4 font-black bg-slate-50 text-slate-700">우주의 중심</td>
                                                <td className="py-3 px-4 font-bold text-rose-700">지구 (Earth)</td>
                                                <td className="py-3 px-4 font-bold text-indigo-700">태양 (Sun)</td>
                                                <td className="py-3 px-4 font-bold text-emerald-700">태양 (타원의 한 초점)</td>
                                            </tr>
                                            <tr className="hover:bg-slate-50">
                                                <td className="py-3 px-4 font-black bg-slate-50 text-slate-700">궤도의 형태</td>
                                                <td className="py-3 px-4">이심원 + <strong>주전원(Epicycle)</strong></td>
                                                <td className="py-3 px-4"><strong>완벽한 동심원</strong></td>
                                                <td className="py-3 px-4 font-bold text-emerald-700"><strong>타원 (Ellipse)</strong></td>
                                            </tr>
                                            <tr className="hover:bg-slate-50">
                                                <td className="py-3 px-4 font-black bg-slate-50 text-slate-700">행성의 공전 속력</td>
                                                <td className="py-3 px-4">등속 원운동</td>
                                                <td className="py-3 px-4">등속 원운동</td>
                                                <td className="py-3 px-4 font-bold text-emerald-700"><strong>가변 속력</strong> (근일점 빠름, 원일점 느림)</td>
                                            </tr>
                                            <tr className="hover:bg-slate-50">
                                                <td className="py-3 px-4 font-black bg-slate-50 text-slate-700">역행 운동 설명</td>
                                                <td className="py-3 px-4">행성이 주전원을 돌기 때문</td>
                                                <td className="py-3 px-4 font-bold text-indigo-700">안쪽 지구가 외행성을 <strong>추월</strong>하기 때문</td>
                                                <td className="py-3 px-4">행성 추월 + 타원에 의한 속력 변화 반영</td>
                                            </tr>
                                            <tr className="hover:bg-slate-50">
                                                <td className="py-3 px-4 font-black bg-slate-50 text-slate-700">역사적 의의 및 한계</td>
                                                <td className="py-3 px-4 text-slate-600">1400여 년간 천문학 지배 / 복잡한 인위적 주전원들</td>
                                                <td className="py-3 px-4 text-slate-600">지동설 패러다임 전환 / 원운동 신념 때문에 오차 잔존</td>
                                                <td className="py-3 px-4 text-slate-600 font-bold">2천 년간의 원 신념 타파 / <strong>뉴턴 만유인력의 기초 완성</strong></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                                <div className="space-y-4">
                                    {[
                                        {
                                            id: 'q1',
                                            num: '질문 1',
                                            title: '우주의 중심과 좌표계의 전환',
                                            question: '프톨레마이오스와 코페르니쿠스 모델에서 행성의 "겉보기 역행 운동"을 설명하는 방식의 가장 본질적인 차이는 무엇인가요?',
                                            options: [
                                                '천동설은 주전원이라는 기하학적 장치를 도입했고, 지동설은 지구의 공전 속도가 더 빨라 외행성을 추월하기 때문으로 설명했다.',
                                                '천동설은 행성이 멈추기 때문이고, 지동설은 행성이 충돌하기 때문이다.',
                                                '천동설은 태양이 중심이라 설명했고, 지동설은 지구가 중심이라 설명했다.'
                                            ],
                                            ans: 0,
                                            exp: '정답: 1번! 프톨레마이오스는 지구가 정지해 있으므로 행성 자체가 작은 원(주전원)을 돌며 후진해야 한다고 보았으나, 코페르니쿠스는 지구와 행성이 모두 태양을 돌며 안쪽 지구가 외행성을 추월하는 상대적 시선 차이로 명쾌하게 설명했습니다.'
                                        },
                                        {
                                            id: 'q2',
                                            num: '질문 2',
                                            title: '코페르니쿠스 지동설의 한계점',
                                            question: '코페르니쿠스는 우주의 중심을 태양으로 바꾼 위대한 혁신을 이루었지만, 여전히 버리지 못했던 고대 그리스 철학의 전통적 신념은 무엇이었나요?',
                                            options: [
                                                '행성은 반드시 완벽한 등속 원운동을 해야 한다는 신념',
                                                '지구에는 중력이 없다는 신념',
                                                '태양도 다른 블랙홀 주위를 돈다는 신념'
                                            ],
                                            ans: 0,
                                            exp: '정답: 1번! 코페르니쿠스는 태양 중심설을 주장했음에도 불구하고 "천체는 신성하므로 오직 완벽한 원을 등속으로 돌아야 한다"는 아리스토텔레스와 플라톤의 신념을 버리지 못해 실제 관측 데이터와 오차가 생겼고, 소형 주전원을 완전히 없애지 못했습니다.'
                                        },
                                        {
                                            id: 'q3',
                                            num: '질문 3',
                                            title: '케플러의 8분 오차와 타원 궤도',
                                            question: '케플러가 스승 티코 브라헤의 화성 관측 자료를 분석하며 발견한 단 8분의 오차(8/60도)가 과학사에서 가지는 의미는?',
                                            options: [
                                                '작은 오차라도 무시하지 않고 끝까지 원인을 탐구하여 2천 년간 지배해 온 원 궤도의 편견을 깨고 타원 궤도 법칙을 발견함',
                                                '티코 브라헤의 망원경이 고장 났음을 증명함',
                                                '행성의 공전 속도가 완전히 일정함을 밝혀냄'
                                            ],
                                            ans: 0,
                                            exp: '정답: 1번! 케플러는 "만약 내가 이 8분의 오차를 무시할 수 있었다면 나의 가설을 기워 맞출 수 있었을 것이다. 그러나 이 8분이야말로 천문학 전체를 개혁하는 길을 열어주었다"라고 고백했습니다.'
                                        },
                                        {
                                            id: 'q4',
                                            num: '질문 4',
                                            title: '면적 속도 일정 법칙과 행성의 속력',
                                            question: '케플러 시뮬레이션에서 행성이 태양에 가장 가까운 근일점(Perihelion)과 가장 먼 원일점(Aphelion)을 지날 때의 속력 비교는?',
                                            options: [
                                                '근일점에서 가장 빠르고, 원일점에서 가장 느리다.',
                                                '원일점에서 가장 빠르고, 근일점에서 가장 느리다.',
                                                '모든 지점에서 속력이 완벽히 동일하다.'
                                            ],
                                            ans: 0,
                                            exp: '정답: 1번! 케플러 제2법칙(면적 속도 일정 법칙)에 의해 같은 시간 동안 쓸고 지나가는 부채꼴의 면적이 같아야 하므로, 태양에 가까워 거리가 짧아질수록 호의 길이가 길어져 속력이 가장 빨라집니다.'
                                        }
                                    ].map(q => (
                                        <div key={q.id} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col gap-3">
                                            <div className="flex items-center justify-between">
                                                <span className="text-xs font-black text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg">{q.num}</span>
                                                <span className="text-xs text-slate-400">{q.title}</span>
                                            </div>
                                            <p className="text-sm font-bold text-slate-800">{q.question}</p>
                                            
                                            <div className="space-y-2 mt-1">
                                                {q.options.map((opt, idx) => (
                                                    <button
                                                        key={idx}
                                                        onClick={() => setQuizAnswers({ ...quizAnswers, [q.id]: idx })}
                                                        className={`w-full p-3 rounded-xl text-xs font-semibold text-left transition-all border ${
                                                            quizAnswers[q.id] === idx
                                                                ? (revealed[q.id] ? (idx === q.ans ? 'bg-emerald-50 border-emerald-500 text-emerald-800' : 'bg-rose-50 border-rose-500 text-rose-800') : 'bg-indigo-50 border-indigo-500 text-indigo-800')
                                                                : 'bg-slate-50 border-slate-200 hover:bg-slate-100 text-slate-700'
                                                        }`}
                                                    >
                                                        {idx + 1}. {opt}
                                                    </button>
                                                ))}
                                            </div>

                                            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-100">
                                                <button
                                                    onClick={() => setRevealed({ ...revealed, [q.id]: !revealed[q.id] })}
                                                    className="text-xs font-bold text-indigo-600 hover:underline"
                                                >
                                                    {revealed[q.id] ? '해설 숨기기' : '정답 및 해설 확인'}
                                                </button>
                                                {revealed[q.id] && (
                                                    <p className="text-xs text-emerald-700 font-bold bg-emerald-50 px-3 py-1.5 rounded-lg max-w-xl">
                                                        💡 {q.exp}
                                                    </p>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>

                            </div>
                        )}

                        {/* 이미지 확대 모달 */}
                        {activeModalImg && (
                            <div
                                onClick={() => setActiveModalImg(null)}
                                className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 cursor-zoom-out animate-in fade-in duration-200"
                            >
                                <div className="max-w-4xl max-h-[90vh] bg-white p-3 rounded-3xl shadow-2xl overflow-hidden flex flex-col items-center">
                                    <img src={activeModalImg} alt="확대 도판" className="max-h-[82vh] object-contain rounded-2xl" />
                                    <p className="text-xs text-slate-500 font-bold mt-2">바깥을 클릭하면 닫힙니다.</p>
                                </div>
                            </div>
                        )}

                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<PlanetaryHistorySim />);
        </script>
    </body>
    </html>
    """

    react_code = react_template.replace("___TEXTBOOK_IMG___", textbook_img)\
                               .replace("___GEOCENTRIC_IMG___", geocentric_img)\
                               .replace("___HELIOCENTRIC_IMG___", heliocentric_img)

    components.html(react_code, height=980, scrolling=True)

if __name__ == "__main__":
    run_sim()
