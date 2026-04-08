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
                        <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100">
                            <svg viewBox="0 0 200 120" className="w-full max-w-[240px]">
                                <rect x="40" y="40" width="120" height="10" fill="#94a3b8" />
                                <rect x="50" y="50" width="5" height="40" fill="#64748b" />
                                <rect x="145" y="50" width="5" height="40" fill="#64748b" />
                                <circle cx="100" cy="45" r="30" fill="none" stroke="#3b82f6" strokeWidth="1" strokeDasharray="2,2" />
                                <line x1="100" y1="45" x2="100" y2="80" stroke="#475569" strokeWidth="1.5" />
                                <circle cx="125" cy="35" r="6" fill="#10b981" />
                                <circle cx="100" cy="85" r="8" fill="#a855f7" />
                                <text x="122" y="38" fontSize="6" fill="white" textAnchor="middle">m</text>
                                <text x="97" y="88" fontSize="6" fill="white" textAnchor="middle">2m</text>
                                <text x="135" y="30" fontSize="8" fill="#10b981" fontWeight="bold">A</text>
                                <text x="115" y="90" fontSize="8" fill="#a855f7" fontWeight="bold">B</text>
                            </svg>
                        </div>
                    );
                    if (type === 'carousel') return (
                        <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100">
                            <svg viewBox="0 0 200 120" className="w-full max-w-[240px]">
                                <rect x="40" y="80" width="120" height="5" fill="#94a3b8" />
                                <rect x="95" y="85" width="10" height="20" fill="#64748b" />
                                <circle cx="70" cy="70" r="10" fill="#3b82f6" opacity="0.8" />
                                <circle cx="150" cy="70" r="10" fill="#f43f5e" opacity="0.8" />
                                <text x="65" y="73" fontSize="6" fill="white">2m</text>
                                <text x="148" y="73" fontSize="6" fill="white">m</text>
                                <text x="65" y="55" fontSize="8" fill="#3b82f6" fontWeight="bold">철수</text>
                                <text x="145" y="55" fontSize="8" fill="#f43f5e" fontWeight="bold">영희</text>
                                <text x="100" y="75" fontSize="10" fill="#94a3b8">⟳</text>
                                <line x1="100" y1="90" x2="70" y2="90" stroke="#94a3b8" strokeWidth="1" markerEnd="url(#dot)" />
                                <text x="85" y="100" fontSize="7" fill="#64748b">r</text>
                                <text x="125" y="100" fontSize="7" fill="#64748b">2r</text>
                            </svg>
                        </div>
                    );
                    if (type === 'rocket') return (
                        <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center gap-4 border border-slate-100">
                            <svg viewBox="0 0 100 100" className="w-24">
                                <circle cx="50" cy="50" r="40" fill="none" stroke="#cbd5e1" strokeWidth="1" strokeDasharray="2,2" />
                                <circle cx="50" cy="50" r="2" fill="#64748b" />
                                <circle cx="90" cy="50" r="5" fill="#f59e0b" />
                                <text x="65" y="48" fontSize="8" fill="#94a3b8">100m</text>
                            </svg>
                            <svg viewBox="0 0 100 60" className="w-32">
                                <line x1="10" y1="50" x2="90" y2="50" stroke="#94a3b8" />
                                <line x1="10" y1="50" x2="10" y2="10" stroke="#94a3b8" />
                                <polyline points="10,50 50,20 90,20" fill="none" stroke="#f43f5e" strokeWidth="2" />
                                <text x="45" y="58" fontSize="6">t</text>
                                <text x="10" y="20" fontSize="6" textAnchor="end">10m/s</text>
                            </svg>
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
                        {questions.map((q, i) => (
                            <div key={q.id} className="bg-white p-8 rounded-[2.5rem] shadow-xl border-2 border-slate-50 relative overflow-hidden group">
                                <div className="absolute top-0 right-0 w-32 h-32 bg-slate-50 rounded-full -mr-16 -mt-16 group-hover:scale-110 transition-transform"></div>
                                <div className="relative">
                                    <div className="flex items-center gap-4 mb-6">
                                        <span className="w-10 h-10 bg-slate-900 text-white flex items-center justify-center rounded-xl font-black italic">{String(i+1).padStart(2, '0')}</span>
                                        <h4 className="text-xl font-black text-slate-800 tracking-tighter">{q.title}</h4>
                                    </div>
                                    <div className="bg-slate-50 p-6 rounded-2xl mb-6 text-slate-600 font-bold leading-relaxed italic border border-slate-100 text-sm tracking-tight">{q.text}</div>
                                    
                                    {q.type === 'ox' && (
                                        <div className="space-y-3">
                                            {q.items.map((item, idx) => (
                                                <div key={idx} className="flex items-center justify-between p-4 bg-slate-50 rounded-xl hover:bg-slate-100 transition-all">
                                                    <span className="text-sm font-bold text-slate-600">{idx+1}. {item}</span>
                                                    <div className="flex gap-2">
                                                        {['O', 'X'].map(val => (
                                                            <button 
                                                                key={val}
                                                                onClick={() => handleOXChange(q.id, idx, val)}
                                                                className={`w-12 h-10 rounded-lg font-black transition-all ${answers[q.id][idx] === val ? (val === 'O' ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white') : 'bg-white text-slate-300 border border-slate-200'}`}
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
                                                                placeholder="값 입력..." 
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
                            </div>
                        ))}
                        <button onClick={() => setSubmitted(true)} className="w-full py-8 bg-slate-900 text-white rounded-[2.5rem] text-2xl font-black shadow-2xl hover:bg-slate-800 active:scale-[0.98] transition-all flex items-center justify-center gap-4">
                            <Icon name="send" size={32} /> 평가 결과 제출하기
                        </button>
                    </div>
                );
            };
            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<PracticeSection />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=1600, scrolling=True)

if __name__ == "__main__":
    run_practice()
