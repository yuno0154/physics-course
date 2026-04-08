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
                    }
                ];

                const getScore = () => {
                    let s = 0;
                    questions.forEach(q => {
                        if (q.type === 'ox') {
                            const isCorrect = q.correct.every((ans, idx) => answers[q.id][idx] === ans);
                            if (isCorrect) s += 1;
                        } else if (q.type === 'sim_problem') {
                            let correctCount = 0;
                            q.items.forEach((item, idx) => {
                                if (answers[q.id][idx].trim() === item.correct) correctCount++;
                            });
                            // All sub-items must be correct for 1 point, or give partial? 
                            // Let's give 1 point if at least 3 correct for now, or 1 total.
                            // Better: 1 point only if all correct.
                            if (correctCount === q.items.length) s += 1;
                        }
                    });
                    return s;
                };

                const handleOXChange = (qId, idx, val) => {
                    const newArr = [...answers[qId]];
                    newArr[idx] = val;
                    setAnswers({ ...answers, [qId]: newArr });
                };

                const handleSimInputChange = (qId, idx, val) => {
                    const newArr = [...answers[qId]];
                    newArr[idx] = val;
                    setAnswers({ ...answers, [qId]: newArr });
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
                                    <p className="text-6xl font-black">{getScore()} / 2</p>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl space-y-4 border border-white/10">
                                    <p className="text-amber-400 font-bold flex items-center gap-2"><Icon name="info" /> 주요 해설</p>
                                    <p className="text-sm text-slate-300 leading-relaxed font-medium">
                                        (1) ω = 2π/2 = 3.14 rad/s<br/>
                                        (2) T = 2π/π = 2s<br/>
                                        (3) f = 1/2 = 0.5Hz<br/>
                                        (4) ac = v²/r = (2π)²/2 = 2π² ≈ 19.7 m/s²<br/>
                                        (5) Fc = mac = 2 * 19.7 = 39.4 N
                                    </p>
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
                                                                onChange={e => handleSimInputChange(q.id, idx, e.target.value)}
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
