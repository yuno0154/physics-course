import streamlit as st
import streamlit.components.v1 as components

def run_practice():
    st.title("📝 원운동 복습 및 연습 문제")
    st.markdown("""
    등속 원운동의 성분 분석과 관련된 핵심 개념을 파악하고 실전 문제를 해결해 보세요.
    모든 문제를 풀고 '제출' 버튼을 누르면 정답 확인과 리포트 출력이 가능합니다.
    """)

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
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
        </style>
    </head>
    <body>
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect } = React;
            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const PracticeSection = () => {
                const [answers, setAnswers] = useState({ 
                    q1: Array(7).fill(''), 
                    q2: Array(5).fill(''),
                    q3: Array(5).fill(''),
                    q4: null,
                    q5: null,
                    q6: null
                });
                const [currentStep, setCurrentStep] = useState(0);
                const [submitted, setSubmitted] = useState(false);

                const questions = [
                    { 
                        id: 'q1', 
                        type: 'ox',
                        title: '원운동의 성질 이해', 
                        text: '등속 원운동에 대한 다음 설명이 맞으면 O, 틀리면 X를 선택하세요.',
                        items: [
                            '속도가 일정하다.',
                            '가속도가 일정하다.',
                            '등가속도 운동이다.',
                            '가속도의 크기는 일정하다.',
                            '가속도의 방향은 원중심 방향이며 매순간 방향이 변한다.',
                            '구심력의 크기는 일정하다.',
                            '구심력의 방향은 일정하다.'
                        ],
                        correct: ['X', 'X', 'X', 'O', 'O', 'O', 'X']
                    },
                    { 
                        id: 'q2', 
                        type: 'sim_problem',
                        title: '원운동 물리량 계산 실습', 
                        text: '아래 시뮬레이션의 조건을 읽고 물음의 값을 계산하시오. (단, π = 3.14로 계산하며 소수점 둘째 자리에서 반올림하세요.)',
                        condition: { r: 2, v: '2π', m: 2 },
                        items: [
                            { label: '각속도', unit: 'rad/s', correct: '3.1' },
                            { label: '주기', unit: 's', correct: '2' },
                            { label: '진동수', unit: 'Hz', correct: '0.5' },
                            { label: '구심 가속도의 크기', unit: 'm/s²', correct: '19.7' },
                            { label: '구심력의 크기', unit: 'N', correct: '39.5' }
                        ]
                    },
                    {
                        id: 'q3',
                        type: 'graph_problem',
                        title: '속도 성분 그래프 분석 [심화]',
                        text: '그림 (가), (나)는 xy 평면에서 원점을 중심으로 등속 원운동하는 물체의 속도 성분 vx, vy를 시간에 따라 나타낸 것입니다.',
                        items: [
                            { label: '물체의 주기를 구하시오', unit: 't₀', correct: '2', type: 'input' },
                            { 
                                label: '물체의 각속도는?', 
                                type: 'choice',
                                options: ['π / 2t₀', 'π / t₀', '2π / t₀', 't₀ / π', '2t₀ / π'],
                                correct: 1
                            },
                            { label: 't = t₀일 때 가속도의 방향은?', type: 'choice', options: ['+x 방향', '-x 방향', '+y 방향', '-y 방향'], correct: 1 },
                            { label: 't = 2t₀일 때 가속도의 방향은?', type: 'choice', options: ['+x 방향', '-x 방향', '+y 방향', '-y 방향'], correct: 0 },
                            { label: 't = t₀일 때 가속도의 크기는?', unit: 'πv₀ / t₀', correct: '1', type: 'input' }
                        ]
                    },
                    {
                        id: 'q4',
                        type: 'concept_choice',
                        title: '등속 원운동과 장력의 평형',
                        text: '질량이 각각 m, 2m인 두 물체 A, B를 마찰이 없는 실험대의 구멍을 통과하는 실로 연결하였습니다. A는 반지름 r인 원운동을 하고, B는 정지해 있습니다.',
                        view: 'table',
                        bogis: [
                            'A에 작용하는 구심력의 크기는 2mg이다.',
                            '구심 가속도의 크기는 g이다.',
                            'A의 속력은 √(2rg)이다.'
                        ],
                        options: ['ㄱ', 'ㄴ', 'ㄷ', 'ㄱ, ㄴ', 'ㄱ, ㄷ'],
                        correct: 4
                    },
                    {
                        id: 'q5',
                        type: 'concept_choice',
                        title: '회전 장치에서의 물리량 비교',
                        text: '철수(2m)와 영희(m)가 회전축으로부터 각각 r, 2r 거리에 앉아 등속 원운동하고 있습니다.',
                        view: 'carousel',
                        bogis: [
                            '속력은 영희가 철수의 2배이다.',
                            '가속도의 크기는 영희가 철수의 2배이다.',
                            '구심력의 크기는 철수가 영희의 2배이다.'
                        ],
                        options: ['ㄱ', 'ㄴ', 'ㄷ', 'ㄱ, ㄴ', 'ㄱ, ㄴ, ㄷ'],
                        correct: 3
                    },
                    {
                        id: 'q6',
                        type: 'concept_choice',
                        title: '가변 속력 원운동의 분석',
                        text: '반지름 100m인 원 궤도를 도는 로켓의 속력이 시간 t까지 일정하게 증가하다가 그 이후 일정(10m/s)하게 유지됩니다.',
                        view: 'rocket',
                        bogis: [
                            '0초에서 t까지 로켓의 추진력은 일정하고, t 이후는 0이다.',
                            '0초에서 t까지 실의 장력은 시간에 비례하여 증가한다.',
                            't 이후 로켓의 구심 가속도의 크기는 1m/s²이다.'
                        ],
                        options: ['ㄱ', 'ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ'],
                        correct: 2
                    }
                ];

                const isStepCompleted = (idx) => {
                    const q = questions[idx];
                    if (!q) return false;
                    const ans = answers[q.id];
                    if (q.type === 'ox') return ans.every(v => v !== '');
                    if (q.type === 'sim_problem' || q.type === 'graph_problem') return ans.every(v => v !== '');
                    if (q.type === 'concept_choice') return ans !== null;
                    return false;
                };

                const getScore = () => {
                    let s = 0;
                    questions.forEach(q => {
                        if (q.type === 'ox') {
                            const isCorrect = q.correct.every((ans, idx) => answers[q.id][idx] === ans);
                            if (isCorrect) s += 1;
                        } else if (q.type === 'sim_problem' || q.type === 'graph_problem') {
                            let correctCount = 0;
                            q.items.forEach((item, idx) => {
                                const ans = answers[q.id][idx];
                                if (item.type === 'choice') {
                                    if (parseInt(ans) === item.correct) correctCount++;
                                } else {
                                    if (ans && ans.trim() === item.correct) correctCount++;
                                }
                            });
                            if (correctCount === q.items.length) s += 1;
                        } else if (q.type === 'concept_choice') {
                            if (answers[q.id] === q.correct) s += 1;
                        }
                    });
                    return s;
                };

                const handleOXChange = (qId, idx, val) => {
                    const newArr = [...answers[qId]];
                    newArr[idx] = val;
                    setAnswers({ ...answers, [qId]: newArr });
                };

                const handleSubInputChange = (qId, idx, val) => {
                    const newArr = [...answers[qId]];
                    newArr[idx] = val;
                    setAnswers({ ...answers, [qId]: newArr });
                };

                const handleChoiceSelect = (qId, val) => {
                    setAnswers({ ...answers, [qId]: val });
                };

                // Problem Visualizations
                const ProblemView = ({ type }) => {
                    if (type === 'table') return (
                        <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100 overflow-hidden">
                            <svg viewBox="0 0 240 160" className="w-full max-w-[320px]">
                                {/* Table Legs (Behind) */}
                                <rect x="65" y="70" width="4" height="25" fill="#94a3b8" />
                                <rect x="175" y="70" width="4" height="25" fill="#94a3b8" />
                                
                                {/* Table Top (Perspective) */}
                                <polygon points="40,70 200,70 230,110 70,110" fill="#e2e8f0" stroke="#94a3b8" strokeWidth="2" />
                                
                                {/* Hole */}
                                <circle cx="135" cy="90" r="4" fill="#1e293b" />
                                
                                {/* Orbit Ellipse */}
                                <ellipse cx="135" cy="90" rx="70" ry="25" fill="none" stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="4,4" />
                                
                                {/* Object A and Connecting String */}
                                <line x1="135" y1="90" x2="195" y2="78" stroke="#64748b" strokeWidth="2" />
                                <circle cx="195" cy="78" r="8" fill="#10b981" />
                                <text x="195" y="81" fontSize="8" fill="white" textAnchor="middle" fontWeight="bold">m</text>
                                <text x="210" y="75" fontSize="12" fill="#10b981" fontWeight="extrabold">A</text>

                                {/* Hanging String and Weight B */}
                                <line x1="135" y1="90" x2="135" y2="140" stroke="#475569" strokeWidth="2" />
                                <rect x="123" y="140" width="24" height="15" rx="4" fill="#a855f7" />
                                <text x="135" y="151" fontSize="8" fill="white" textAnchor="middle" fontWeight="bold">2m</text>
                                <text x="155" y="152" fontSize="12" fill="#a855f7" fontWeight="extrabold">B</text>

                                {/* Front Legs */}
                                <rect x="70" y="110" width="6" height="40" fill="#475569" />
                                <rect x="224" y="110" width="6" height="40" fill="#475569" />
                            </svg>
                        </div>
                    );
                    if (type === 'carousel') return (
                        <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100 overflow-hidden">
                            <svg viewBox="0 0 300 200" className="w-full max-w-[400px]">
                                {/* Central Axis */}
                                <rect x="146" y="40" width="8" height="100" fill="#64748b" rx="2" />
                                <ellipse cx="150" cy="40" rx="6" ry="2" fill="#94a3b8" />
                                
                                {/* Rotating Disk (Perspective) */}
                                <ellipse cx="150" cy="130" rx="140" ry="40" fill="#cbd5e1" stroke="#94a3b8" strokeWidth="2" />
                                <ellipse cx="150" cy="125" rx="140" ry="40" fill="#e2e8f0" stroke="#94a3b8" strokeWidth="1" />
                                
                                {/* Grid/Radius Lines for reference (Subtle) */}
                                <line x1="150" y1="125" x2="285" y2="125" stroke="#94a3b8" strokeWidth="1" strokeDasharray="4,2" />
                                
                                {/* Chul-soo (Distance r) */}
                                <g transform="translate(195, 118)">
                                    <path d="M-8,0 L8,0 L8,-4 L4,-4 L4,-18 L-4,-18 L-4,-4 L-8,-4 Z" fill="#3b82f6" />
                                    <circle cx="0" cy="-22" r="4.5" fill="#3b82f6" />
                                    <rect x="-10" y="2" width="20" height="10" rx="3" fill="rgba(59,130,246,0.15)" stroke="#3b82f6" strokeWidth="0.5" />
                                    <text x="0" y="10" fontSize="8" fill="#1d4ed8" textAnchor="middle" fontWeight="black">2m</text>
                                    <text x="0" y="-32" fontSize="10" fill="#1d4ed8" textAnchor="middle" fontWeight="black">철수</text>
                                </g>

                                {/* Young-hee (Distance 2r) */}
                                <g transform="translate(265, 118)">
                                    <path d="M-8,0 L8,0 L8,-4 L4,-4 L4,-18 L-4,-18 L-4,-4 L-8,-4 Z" fill="#f43f5e" />
                                    <circle cx="0" cy="-22" r="4.5" fill="#f43f5e" />
                                    <rect x="-10" y="2" width="20" height="10" rx="3" fill="rgba(244,63,94,0.15)" stroke="#f43f5e" strokeWidth="0.5" />
                                    <text x="0" y="10" fontSize="8" fill="#be123c" textAnchor="middle" fontWeight="black">m</text>
                                    <text x="0" y="-32" fontSize="10" fill="#be123c" textAnchor="middle" fontWeight="black">영희</text>
                                </g>

                                {/* Distance Markers */}
                                <line x1="150" y1="145" x2="195" y2="145" stroke="#64748b" strokeWidth="1.5" />
                                <line x1="150" y1="142" x2="150" y2="148" stroke="#64748b" strokeWidth="1.5" />
                                <line x1="195" y1="142" x2="195" y2="148" stroke="#64748b" strokeWidth="1.5" />
                                <text x="172" y="158" fontSize="10" fill="#64748b" textAnchor="middle" fontWeight="bold">r</text>

                                <line x1="150" y1="170" x2="265" y2="170" stroke="#64748b" strokeWidth="1.5" />
                                <line x1="150" y1="167" x2="150" y2="173" stroke="#64748b" strokeWidth="1.5" />
                                <line x1="265" y1="167" x2="265" y2="173" stroke="#64748b" strokeWidth="1.5" />
                                <text x="207" y="183" fontSize="10" fill="#64748b" textAnchor="middle" fontWeight="bold">2r</text>

                                {/* Rotation Arrow */}
                                <path d="M100,115 Q110,100 130,105" fill="none" stroke="#94a3b8" strokeWidth="2" markerEnd="url(#arrow_carousel)" />
                                <defs>
                                    <marker id="arrow_carousel" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                                        <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8" />
                                    </marker>
                                </defs>
                            </svg>
                        </div>
                    );
                    if (type === 'rocket') return (
                        <div className="bg-slate-50 p-6 rounded-3xl flex flex-col md:flex-row items-center justify-center gap-12 border border-slate-100 overflow-hidden">
                            <div className="flex flex-col items-center gap-2">
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">(가) 로켓의 궤도</p>
                                <svg viewBox="0 0 120 120" className="w-40 h-40">
                                    <circle cx="60" cy="60" r="50" fill="none" stroke="#e2e8f0" strokeWidth="1" strokeDasharray="4,4" />
                                    <circle cx="60" cy="60" r="3" fill="#64748b" />
                                    <text x="85" y="58" fontSize="8" fill="#94a3b8" fontWeight="bold">100m</text>
                                    {/* Rocket Icon */}
                                    <g transform="translate(110, 60) rotate(90)">
                                        <path d="M0,-12 L4,0 L4,10 L-4,10 L-4,0 Z" fill="#f59e0b" />
                                        <path d="M-4,10 L-6,14 L4,14 L4,10 Z" fill="#f43f5e" />
                                        <path d="M-4,14 Q0,20 4,14" fill="#fbbf24" opacity="0.8" />
                                        <circle cx="0" cy="0" r="2" fill="white" opacity="0.5" />
                                    </g>
                                </svg>
                            </div>
                            <div className="flex flex-col items-center gap-2">
                                <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">(나) 시간-속력 그래프</p>
                                <svg viewBox="0 0 120 80" className="w-48 h-32">
                                    <defs>
                                        <linearGradient id="rocket_grad" x1="0%" y1="0%" x2="0%" y2="100%">
                                            <stop offset="0%" stopColor="#f43f5e" stopOpacity="0.2" />
                                            <stop offset="100%" stopColor="#f43f5e" stopOpacity="0" />
                                        </linearGradient>
                                    </defs>
                                    <path d="M15,65 L60,25 L105,25 L105,65 Z" fill="url(#rocket_grad)" />
                                    <line x1="10" y1="65" x2="110" y2="65" stroke="#94a3b8" strokeWidth="1.5" />
                                    <line x1="15" y1="10" x2="15" y2="70" stroke="#94a3b8" strokeWidth="1.5" />
                                    <polyline points="15,65 60,25 105,25" fill="none" stroke="#f43f5e" strokeWidth="2.5" strokeLinecap="round" />
                                    <text x="60" y="75" fontSize="8" fill="#64748b" textAnchor="middle">t</text>
                                    <text x="110" y="75" fontSize="8" fill="#94a3b8">시간(s)</text>
                                    <text x="12" y="25" fontSize="8" fill="#f43f5e" textAnchor="end" fontWeight="bold">10m/s</text>
                                    <text x="12" y="10" fontSize="8" fill="#94a3b8" textAnchor="end">속력(v)</text>
                                </svg>
                            </div>
                        </div>
                    );
                    return null;
                };

                // Velocity Graph Component
                const VelocityGraph = ({ label, isSine }) => {
                    const pts = [];
                    for(let i=0; i<=100; i++) {
                        const t = i/100 * 3;
                        const v = isSine ? Math.sin(Math.PI * t) : Math.cos(Math.PI * t);
                        pts.push(`${i*1.5},${40 - v*30}`);
                    }
                    return (
                        <div className="bg-white p-4 rounded-xl border border-slate-100 flex-1">
                            <p className="text-[10px] font-black text-slate-400 mb-2">{label}</p>
                            <svg viewBox="0 0 150 80" className="w-full">
                                <line x1="10" y1="40" x2="140" y2="40" stroke="#cbd5e1" strokeWidth="1" />
                                <line x1="10" y1="5" x2="10" y2="75" stroke="#cbd5e1" strokeWidth="1" />
                                <polyline points={pts.join(' ')} fill="none" stroke="#f43f5e" strokeWidth="2" />
                                <text x="142" y="45" fontSize="8" fill="#94a3b8">t</text>
                                <text x="5" y="10" fontSize="8" fill="#94a3b8">v₀</text>
                                <text x="5" y="75" fontSize="8" fill="#94a3b8">-v₀</text>
                                <text x="55" y="55" fontSize="8" fill="#94a3b8">t₀</text>
                                <text x="105" y="55" fontSize="8" fill="#94a3b8">2t₀</text>
                            </svg>
                        </div>
                    );
                };

                // Small Sim Component for Question 2
                const ProblemSim = ({ radius, speedText, mass }) => {
                    const [angle, setAngle] = useState(0);
                    useEffect(() => {
                        const id = setInterval(() => setAngle(a => (a + 0.05) % (Math.PI * 2)), 30);
                        return () => clearInterval(id);
                    }, []);

                    const x = 100 + Math.cos(angle) * 60;
                    const y = 100 - Math.sin(angle) * 60;

                    return (
                        <div className="flex flex-col md:flex-row items-center gap-8 bg-slate-900 p-8 rounded-[2rem] text-white">
                            <div className="w-48 h-48 bg-white/5 rounded-2xl border border-white/10 flex items-center justify-center relative">
                                <svg viewBox="0 0 200 200" className="w-full h-full">
                                    <circle cx="100" cy="100" r="60" fill="none" stroke="rgba(255,255,255,0.1)" strokeWidth="2" strokeDasharray="4,4" />
                                    <line x1="40" y1="100" x2="160" y2="100" stroke="rgba(255,255,255,0.05)" />
                                    <line x1="100" y1="40" x2="100" y2="160" stroke="rgba(255,255,255,0.05)" />
                                    <line x1="100" y1="100" x2={x} y2={y} stroke="#3b82f6" strokeWidth="2" opacity="0.5" />
                                    <circle cx={x} cy={y} r="8" fill="#10b981" />
                                    <text x="105" y="115" fontSize="10" fill="#94a3b8" className="italic">O</text>
                                </svg>
                            </div>
                            <div className="flex-1 space-y-4">
                                <div className="flex items-center gap-3">
                                    <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-lg text-xs font-bold">조건</span>
                                    <p className="text-sm font-medium text-slate-300">반지름(r) = {radius}m, 속력(v) = {speedText}m/s, 질량(m) = {mass}kg</p>
                                </div>
                                <div className="p-4 bg-white/5 rounded-xl border border-white/10 space-y-1">
                                    <p className="text-[10px] text-slate-500 font-bold uppercase">준비할 공식</p>
                                    <p className="text-xs text-slate-400 leading-relaxed italic">ω = v/r, T = 2π/ω, f = 1/T, a = v²/r, F = ma</p>
                                </div>
                            </div>
                        </div>
                    );
                };

                if (submitted) {
                    return (
                        <div className="max-w-4xl mx-auto p-6 bg-slate-900 rounded-[3rem] text-white shadow-2xl animate-in zoom-in duration-500">
                            <h3 className="text-3xl font-black mb-6 italic">평가 결과 리포트</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="bg-white/10 p-8 rounded-3xl text-center border border-white/10">
                                    <p className="text-sm text-sky-400 font-bold mb-2 uppercase">최종 점수</p>
                                    <p className="text-6xl font-black">{getScore()} / 6</p>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl space-y-4 border border-white/10 overflow-y-auto max-h-[400px] no-scrollbar">
                                    <p className="text-amber-400 font-bold flex items-center gap-2"><Icon name="info" /> 주요 해설</p>
                                    <div className="text-[13px] text-slate-300 leading-relaxed space-y-5">
                                        <p><strong>[2~3번]</strong> 성분 분석과 계산 공식을 정확히 적용했습니다.</p>
                                        <p><strong>[4번]</strong> B가 정지해 있으므로 실의 장력 T=2mg입니다. 이 장력이 A의 구심력으로 작용하므로 mv²/r = 2mg, v=√(2rg)입니다. (ㄱ, ㄷ)</p>
                                        <p><strong>[5번]</strong> 같은 회전판 위에 있으므로 각속도 ω는 같습니다. v=rω, a=rω²이므로 반지름이 2배인 영희가 철수의 속력과 가속도의 2배입니다. 구심력 F=mrω²은 철수(2m*r)와 영희(m*2r)가 같습니다. (ㄱ, ㄴ)</p>
                                        <p><strong>[6번]</strong> v가 t까지 비례하므로 접선 가속도는 일정하고 추진력도 일정합니다. t 이후 v가 일정하므로 추진력은 0입니다. t 이후 a_c = v²/r = 100/100 = 1m/s²입니다. (ㄱ, ㄷ)</p>
                                    </div>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setSubmitted(false)} className="flex-1 py-4 bg-slate-700 rounded-2xl font-bold hover:bg-slate-600 transition-all">다시 풀기</button>
                                <button className="flex-1 py-4 bg-blue-600 rounded-2xl font-black hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/30">PDF 리포트 저장</button>
                            </div>
                        </div>
                    );
                }

                return (
                    <div className="max-w-4xl mx-auto p-4 space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-1000 pb-20">
                        {questions.slice(0, currentStep + 1).map((q, i) => (
                            <div key={q.id} className="bg-white p-8 rounded-[2.5rem] shadow-xl border-2 border-slate-50 relative overflow-hidden group animate-in slide-in-from-right duration-500">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-slate-50 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform"></div>
                                <div className="relative">
                                    <div className="flex items-center justify-between mb-6">
                                        <div className="flex items-center gap-4">
                                            <span className="w-10 h-10 bg-slate-900 text-white flex items-center justify-center rounded-xl font-black italic">{String(i+1).padStart(2, '0')}</span>
                                            <h4 className="text-xl font-black text-slate-800 tracking-tighter">{q.title}</h4>
                                        </div>
                                        {i < currentStep && <span className="text-emerald-500 font-black flex items-center gap-1"><Icon name="check-circle" /> 완료됨</span>}
                                    </div>
                                    <div className="bg-slate-50 p-6 rounded-2xl mb-6 text-slate-600 font-bold leading-relaxed italic border border-slate-100 text-sm tracking-tight">{q.text}</div>
                                    
                                    <div className={i < currentStep ? 'opacity-50 pointer-events-none grayscale-[0.5]' : ''}>
                                        {q.type === 'ox' && (
                                            <div className="space-y-3">
                                                {q.items.map((item, idx) => (
                                                    <div key={idx} className="flex items-center justify-between p-4 bg-slate-100/50 rounded-xl">
                                                        <span className="text-sm font-bold text-slate-600">{idx+1}. {item}</span>
                                                        <div className="flex gap-2">
                                                            {['O', 'X'].map(val => (
                                                                <button 
                                                                    key={val}
                                                                    onClick={() => handleOXChange(q.id, idx, val)}
                                                                    className={`w-12 h-10 rounded-lg font-black transition-all ${answers[q.id][idx] === val ? (val === 'O' ? 'bg-emerald-500 text-white shadow-lg' : 'bg-rose-500 text-white shadow-lg') : 'bg-white text-slate-300 border border-slate-200'}`}
                                                                >
                                                                    {val}
                                                                </button>
                                                            ))}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        )}

                                        {q.type === 'sim_problem' && (
                                            <div className="space-y-8">
                                                <ProblemSim radius={2} speedText="2π" mass={2} />
                                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                                    {q.items.map((sub, idx) => (
                                                        <div key={idx} className="relative">
                                                            <p className="text-[10px] text-slate-400 font-black uppercase mb-2 ml-2">({idx+1}) {sub.label}</p>
                                                            <div className="relative">
                                                                <input 
                                                                    type="text" 
                                                                    value={answers[q.id][idx]} 
                                                                    onChange={e => handleSubInputChange(q.id, idx, e.target.value)}
                                                                    className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 text-xl font-black text-blue-600 outline-none focus:border-blue-400 focus:bg-white transition-all" 
                                                                    placeholder="..." 
                                                                />
                                                                <span className="absolute right-6 top-1/2 -translate-y-1/2 font-black text-slate-300 italic">{sub.unit}</span>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        {q.type === 'graph_problem' && (
                                            <div className="space-y-8">
                                                <div className="flex flex-col md:flex-row gap-4 bg-slate-50 p-6 rounded-3xl border border-slate-100 shadow-inner">
                                                    <VelocityGraph label="(가) t에 따른 vx" isSine={true} />
                                                    <VelocityGraph label="(나) t에 따른 vy" isSine={false} />
                                                </div>
                                                <div className="space-y-6">
                                                    {q.items.map((sub, idx) => (
                                                        <div key={idx} className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100 group/item">
                                                            <p className="text-sm font-black text-slate-700 mb-4 flex items-center gap-2">
                                                                <span className="w-6 h-6 bg-slate-200 text-slate-500 rounded-lg flex items-center justify-center text-[10px] group-hover/item:bg-slate-900 group-hover/item:text-white transition-colors">{idx+1}</span>
                                                                {sub.label}
                                                            </p>
                                                            {sub.type === 'choice' ? (
                                                                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                                                                    {sub.options.map((opt, oIdx) => (
                                                                        <button 
                                                                            key={oIdx}
                                                                            onClick={() => handleSubInputChange(q.id, idx, oIdx)}
                                                                            className={`py-3 px-2 rounded-xl text-[11px] font-bold border-2 transition-all ${parseInt(answers[q.id][idx]) === oIdx ? 'bg-slate-900 border-slate-900 text-white shadow-lg' : 'bg-white border-slate-200 text-slate-400 hover:border-slate-300'}`}
                                                                        >
                                                                            {opt}
                                                                        </button>
                                                                    ))}
                                                                </div>
                                                            ) : (
                                                                <div className="relative max-w-xs">
                                                                    <input 
                                                                        type="text" 
                                                                        value={answers[q.id][idx]} 
                                                                        onChange={e => handleSubInputChange(q.id, idx, e.target.value)}
                                                                        className="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-lg font-black text-rose-500 outline-none focus:border-rose-400 transition-all" 
                                                                        placeholder="..." 
                                                                    />
                                                                    <span className="absolute right-4 top-1/2 -translate-y-1/2 font-black text-slate-300 italic text-xs">{sub.unit}</span>
                                                                </div>
                                                            )}
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        )}

                                        {q.type === 'concept_choice' && (
                                            <div className="space-y-6">
                                                <ProblemView type={q.view} />
                                                <div className="bg-slate-50 p-6 rounded-2xl border border-slate-100">
                                                    <p className="text-xs font-black text-slate-400 mb-3 uppercase tracking-tighter">[ 보 기 ]</p>
                                                    <div className="space-y-2 text-sm font-bold text-slate-600">
                                                        {q.bogis.map((b, bIdx) => <p key={bIdx}>{['ㄱ', 'ㄴ', 'ㄷ'][bIdx]}. {b}</p>)}
                                                    </div>
                                                </div>
                                                <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
                                                    {q.options.map((opt, oIdx) => (
                                                        <button 
                                                            key={oIdx}
                                                            onClick={() => handleChoiceSelect(q.id, oIdx)}
                                                            className={`py-4 rounded-xl text-sm font-black border-2 transition-all ${answers[q.id] === oIdx ? 'bg-slate-900 border-slate-900 text-white shadow-xl scale-105' : 'bg-white border-slate-200 text-slate-400 hover:border-slate-300'}`}
                                                        >
                                                            {oIdx+1}. {opt}
                                                        </button>
                                                    ))}
                                                </div>
                                            </div>
                                        )}
                                    </div>

                                    {i === currentStep && isStepCompleted(i) && (
                                        <div className="mt-8 pt-8 border-t border-slate-100 flex justify-end">
                                            {i < questions.length - 1 ? (
                                                <button 
                                                    onClick={() => {
                                                        setCurrentStep(i + 1);
                                                        setTimeout(() => {
                                                            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
                                                        }, 100);
                                                    }}
                                                    className="px-10 py-4 bg-emerald-500 text-white rounded-2xl font-black shadow-lg hover:bg-emerald-400 transition-all flex items-center gap-2 animate-bounce"
                                                >
                                                    다음 문제 도전하기 <Icon name="arrow-right" />
                                                </button>
                                            ) : (
                                                <button 
                                                    onClick={() => setSubmitted(true)}
                                                    className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-black shadow-lg hover:bg-slate-800 transition-all flex items-center gap-2"
                                                >
                                                    최종 결과 제출하기 <Icon name="send" />
                                                </button>
                                            )}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                );
            };
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<PracticeSection />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=1800, scrolling=True)

if __name__ == "__main__":
    run_practice()
