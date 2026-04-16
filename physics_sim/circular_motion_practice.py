import streamlit as st
import streamlit.components.v1 as components

def run_practice():
    # Note: st.set_page_config is handled by main_app.py when using st.navigation
    st.title("📝 원운동 복습 및 연습 문제")
    st.markdown("""
    등속 원운동의 성분 분석과 관련된 핵심 개념을 파악하고 실전 문제를 해결해 보세요.
    모든 문제를 풀고 '제출하기' 버튼을 누르면 정답 확인과 해설 리포트가 출력됩니다.
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
        <script src="https://unpkg.com/docx@8.5.0/build/index.umd.js"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700;800&display=swap');
            body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; }
            .no-scrollbar::-webkit-scrollbar { display: none; }
            .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        </style>
    </head>
    <body>
        <div id="root"></div>
        <script type="text/babel">
            const { useState, useEffect, useMemo } = React;

            // --- Constants & Data ---
            const QUESTIONS_DATA = [
                {
                    id: 'q1',
                    type: 'multiple_sub_questions',
                    title: '원운동의 성질 분석',
                    text: '등속 원운동하는 물체의 물리적 성질에 대한 설명입니다. 옳은 것만 골라보세요.',
                    view: 'circular_basic',
                    items: [
                        {
                            label: '(1) 등속 원운동하는 물체의 가속도에 대한 설명으로 옳은 것은?',
                            type: 'choice',
                            options: ['가속도가 0이다', '가속도가 일정하다', '가속도의 크기만 일정하다', '방향만 일정하다'],
                            correct: 2
                        },
                        {
                            label: '(2) 물체에 작용하는 알짜힘(구심력)의 방향은?',
                            type: 'choice',
                            options: ['접선 방향', '원중심 방향', '원심력 방향', '매순간 변하지 않는다'],
                            correct: 1
                        }
                    ]
                },
                {
                    id: 'q2',
                    type: 'multiple_sub_questions',
                    title: '원운동 물리량 계산',
                    text: '반지름(r)이 2m이고질량이 2kg인 물체가 v = 2π m/s의 속력으로 등속 원운동하고 있습니다. (π = 3.14로 계산하시오)',
                    view: 'circular_calc',
                    items: [
                        { 
                            label: '1. 각속도(ω)는 얼마인가?', 
                            type: 'choice', 
                            options: ['1.57 rad/s', '3.14 rad/s', '6.28 rad/s', '9.42 rad/s'],
                            correct: 1 
                        },
                        { 
                            label: '2. 공전 주기(T)는 몇 초인가?', 
                            type: 'choice', 
                            options: ['1s', '2s', '4s', 'π s'],
                            correct: 1 
                        },
                        { 
                            label: '3. 구심 가속도의 크기는?', 
                            type: 'choice', 
                            options: ['9.86 m/s²', '19.72 m/s²', '39.44 m/s²', '4.93 m/s²'],
                            correct: 1 
                        }
                    ]
                },
                {
                    id: 'q3',
                    type: 'multiple_sub_questions',
                    title: '속도 성분 그래프 분석',
                    text: '그림은 xy 평면에서 원운동하는 물체 A의 x축, y축 방향 속 성분 vx, vy를 시간에 따라 나타낸 것입니다.',
                    view: 'velocity_graphs',
                    items: [
                        {
                            label: '(1) 물체의 공전 주기는 얼마인가?',
                            type: 'choice',
                            options: ['0.5 t₀', 't₀', '1.5 t₀', '2 t₀'],
                            correct: 3
                        },
                        {
                            label: '(2) t = t₀일 때 물체의 가속도 방향은?',
                            type: 'choice',
                            options: ['+x 방향', '-x 방향', '+y 방향', '-y 방향'],
                            correct: 1
                        }
                    ]
                },
                {
                    id: 'q4',
                    type: 'multiple_sub_questions',
                    title: '등속 원운동과 장력의 평형',
                    text: '질량이 각각 m, 2m인 두 물체 A, B를 마찰이 없는 실험대의 구멍을 통과하는 실로 연결하였습니다. A는 반지름 r인 원운동을 하고, B는 정지해 있습니다.',
                    view: 'table_balance',
                    items: [
                        {
                            label: 'A에 작용하는 구심력의 크기는 얼마인가?',
                            type: 'choice',
                            options: ['mg', '2mg', '0.5mg', 'g'],
                            correct: 1
                        },
                        {
                            label: 'A의 공전 속력 v를 구하시오.',
                            type: 'choice',
                            options: ['√(rg)', '√(2rg)', '2√(rg)', '√(0.5rg)'],
                            correct: 1
                        }
                    ]
                },
                {
                    id: 'q5',
                    type: 'multiple_sub_questions',
                    title: '회전 장치에서의 물리량 비교',
                    text: '질량이 2m, m인 철수와 영희가 회전축으로부터 각각 r, 2r 거리에 앉아 등속 원운동하고 있습니다.',
                    view: 'disk_rotation',
                    items: [
                        {
                            label: '철수와 영희의 각속도(ω) 관계는?',
                            type: 'choice',
                            options: ['철수가 더 크다', '영희가 더 크다', '서로 같다'],
                            correct: 2
                        },
                        {
                            label: '철수와 영희에게 작용하는 구심력의 크기비(철수:영희)는?',
                            type: 'choice',
                            options: ['1 : 1', '1 : 2', '2 : 1', '1 : 4'],
                            correct: 0
                        }
                    ]
                },
                {
                    id: 'q6',
                    type: 'multiple_sub_questions',
                    title: '가변 속력 원운동의 분석',
                    text: '반지름 100m인 원 궤도를 도는 로켓의 속력이 시간 t까지 일정하게 증가하다가 그 이후 일정(10m/s)하게 유지됩니다.',
                    view: 'rocket_v_t',
                    items: [
                        {
                            label: 't 이후 로켓의 구심 가속도의 크기는?',
                            type: 'choice',
                            options: ['0.1 m/s²', '1 m/s²', '10 m/s²', '100 m/s²'],
                            correct: 1
                        },
                        {
                            label: '0초에서 t까지 접선 가속도에 대한 설명으로 옳은 것은?',
                            type: 'choice',
                            options: ['0이다', '일정하다', '증가한다', '알 수 없다'],
                            correct: 1
                        }
                    ]
                }
            ];

            const EXPLANATIONS = {
                q1: "등속 원운동은 속력은 일정하지만 운동 방향이 매순간 변하므로 '가속도 운동'입니다. 가속도의 크기(v²/r)는 일정하지만 방향이 항상 원의 중심을 향하므로 방향이 변하는 가속도 운동입니다.",
                q2: "1. v=rω 에서 ω = v/r = 2π/2 = 3.14 rad/s 입니다.\\n2. T = 2π/ω = 2s 입니다.\\n3. a = v²/r = (2π)² / 2 = 2π² ≈ 19.72 m/s² 입니다.",
                q3: "속도 성분이 sin, cos 파형을 그리며 한 주기를 도는 데 걸리는 시간은 2t₀입니다. t=t₀일 때 vx=0이고 vy는 최대 음수이므로 물체는 원의 가장 윗부분에서 아래로 움직이는 중이며, 가속도(중심 방향)는 -x 방향이 됩니다.",
                q4: "B가 정지해 있으므로 실의 장력 T는 B의 무게 2mg와 같습니다. 이 장력이 A의 구심력(mv²/r)이 됩니다. 따라서 mv²/r = 2mg 식을 정리하면 v = √(2rg)가 됩니다.",
                q5: "같은 회전판 위에 있으므로 각속도 ω는 같습니다. 구심력 F = mrω² 입니다. 철수는 (2m)rω², 영희는 (m)(2r)ω² 으로 두 힘의 크기는 1:1로 같습니다.",
                q6: "구심 가속도 a = v²/r 입니다. t 이후 v=10, r=100 이므로 a = 100/100 = 1 m/s² 입니다. 0~t 구간에서 속력이 일정하게 증가(일차함수)하므로 접선 가속도(dv/dt)는 기울기로 일정합니다."
            };

            // --- Components ---
            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const ProblemView = ({ type }) => {
                if (type === 'none') return null;
                
                let svgInner = null;
                if (type === 'circular_basic') {
                    svgInner = (
                        <g transform="translate(175, 100)">
                            <circle cx="0" cy="0" r="70" fill="none" stroke="#60a5fa" strokeWidth="2" strokeDasharray="4,4" />
                            <circle cx="0" cy="0" r="4" fill="#1e293b" />
                            <line x1="0" y1="0" x2="60" y2="-35" stroke="#94a3b8" strokeDasharray="2,2" />
                            <circle cx="60" cy="-35" r="8" fill="#f59e0b" />
                            <path d="M 60 -35 L 85 -75" fill="none" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow_basic)" />
                            <text x="80" y="-80" fontSize="12" fill="#ef4444" fontWeight="bold">v</text>
                            <path d="M 60 -35 L 20 -12" fill="none" stroke="#10b981" strokeWidth="2" markerEnd="url(#arrow_green)" />
                            <text x="15" y="-5" fontSize="12" fill="#10b981" fontWeight="bold">F</text>
                        </g>
                    );
                } else if (type === 'circular_calc') {
                    svgInner = (
                        <g transform="translate(175, 100)">
                            <circle cx="0" cy="0" r="60" fill="none" stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="4,4" />
                            <circle cx="0" cy="0" r="4" fill="#475569" />
                            <line x1="0" y1="0" x2="60" y2="0" stroke="#64748b" strokeWidth="2" />
                            <text x="25" y="-5" fontSize="12" fontWeight="bold">r=2m</text>
                            <circle cx="60" cy="0" r="10" fill="#8b5cf6" />
                            <text x="60" y="3" fontSize="10" fill="white" textAnchor="middle" fontWeight="bold">2kg</text>
                            <path d="M 60 0 L 60 -40" fill="none" stroke="#f43f5e" strokeWidth="2" markerEnd="url(#arrow_basic)" />
                            <text x="70" y="-20" fontSize="12" fill="#f43f5e" fontWeight="extrabold">v</text>
                        </g>
                    );
                } else if (type === 'velocity_graphs') {
                    const vxPath = Array.from({length: 41}, (_, i) => {
                        const t = i / 20; // 0 to 2
                        const x = 10 + (t * 50);
                        const y = 30 - 25 * Math.sin(Math.PI * t);
                        return `${x},${y}`;
                    }).join(' ');
                    const vyPath = Array.from({length: 41}, (_, i) => {
                        const t = i / 20; // 0 to 2
                        const x = 10 + (t * 50);
                        const y = 30 - 25 * Math.cos(Math.PI * t);
                        return `${x},${y}`;
                    }).join(' ');

                    svgInner = (
                        <g transform="translate(50, 40)">
                            <text x="0" y="-12" fontSize="10" fontWeight="bold" fill="#64748b">vx-t 그래프</text>
                            <line x1="0" y1="30" x2="120" y2="30" stroke="#cbd5e1" strokeWidth="1" />
                            <line x1="10" y1="0" x2="10" y2="60" stroke="#cbd5e1" strokeWidth="1" />
                            <polyline points={vxPath} fill="none" stroke="#f43f5e" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                            <text x="60" y="45" fontSize="8" fontWeight="bold">t₀</text>
                            <text x="110" y="45" fontSize="8" fontWeight="bold">2t₀</text>
                            
                            <g transform="translate(150, 0)">
                                <text x="0" y="-12" fontSize="10" fontWeight="bold" fill="#64748b">vy-t 그래프</text>
                                <line x1="0" y1="30" x2="120" y2="30" stroke="#cbd5e1" strokeWidth="1" />
                                <line x1="10" y1="0" x2="10" y2="60" stroke="#cbd5e1" strokeWidth="1" />
                                <polyline points={vyPath} fill="none" stroke="#3b82f6" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                                <text x="60" y="45" fontSize="8" fontWeight="bold">t₀</text>
                                <text x="110" y="45" fontSize="8" fontWeight="bold">2t₀</text>
                            </g>
                        </g>
                    );
                } else if (type === 'table_balance') {
                    svgInner = (
                        <g transform="translate(175, 40)">
                            <polygon points="-80,60 80,60 110,100 -50,100" fill="#f1f5f9" stroke="#94a3b8" />
                            <circle cx="15" cy="80" r="4" fill="#1e293b" />
                            <ellipse cx="15" cy="80" rx="60" ry="20" fill="none" stroke="#3b82f6" strokeDasharray="4,4" />
                            <line x1="15" y1="80" x2="70" y2="72" stroke="#64748b" strokeWidth="2" />
                            <circle cx="70" cy="72" r="8" fill="#10b981" />
                            <text x="82" y="70" fontSize="10" fontWeight="bold">A(m)</text>
                            <line x1="15" y1="80" x2="15" y2="130" stroke="#64748b" strokeWidth="2" />
                            <rect x="5" y="130" width="20" height="15" rx="2" fill="#a855f7" />
                            <text x="30" y="142" fontSize="10" fontWeight="bold">B(2m)</text>
                        </g>
                    );
                } else if (type === 'disk_rotation') {
                    svgInner = (
                        <g transform="translate(175, 100)">
                            <ellipse cx="0" cy="30" rx="140" ry="40" fill="#e2e8f0" stroke="#94a3b8" />
                            <line x1="0" y1="-40" x2="0" y2="30" stroke="#64748b" strokeWidth="4" />
                            <circle cx="50" cy="20" r="8" fill="#3b82f6" />
                            <text x="50" y="40" fontSize="10" textAnchor="middle" fontWeight="bold">철수(r)</text>
                            <circle cx="110" cy="25" r="8" fill="#f43f5e" />
                            <text x="110" y="45" fontSize="10" textAnchor="middle" fontWeight="bold">영희(2r)</text>
                        </g>
                    );
                } else if (type === 'rocket_v_t') {
                    svgInner = (
                        <g transform="translate(40, 40)">
                            <line x1="20" y1="120" x2="20" y2="20" stroke="#475569" strokeWidth="2" />
                            <line x1="20" y1="120" x2="280" y2="120" stroke="#475569" strokeWidth="2" />
                            <polyline points="20,120 120,40 260,40" fill="none" stroke="#f59e0b" strokeWidth="4" />
                            <text x="120" y="135" textAnchor="middle" fontSize="12" fontWeight="bold">t</text>
                            <text x="20" y="35" textAnchor="end" fontSize="12" fontWeight="bold" fill="#f59e0b">10m/s</text>
                            <text x="280" y="135" textAnchor="end" fontSize="10" fill="#94a3b8">시간(s)</text>
                        </g>
                    );
                }
                
                return (
                    <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100 overflow-hidden mb-6">
                        <svg viewBox="0 0 350 200" className="w-full max-w-[450px]">
                            <defs>
                                <marker id="arrow_basic" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                                </marker>
                                <marker id="arrow_green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#10b981" />
                                </marker>
                            </defs>
                            {svgInner}
                        </svg>
                    </div>
                );
            };

            const PracticeSection = () => {
                const [answers, setAnswers] = useState(() => {
                    const init = {};
                    QUESTIONS_DATA.forEach(q => { init[q.id] = q.items.map(() => ''); });
                    return init;
                });
                const [currentStep, setCurrentStep] = useState(0);
                const [submitted, setSubmitted] = useState(false);
                const [studentInfo, setStudentInfo] = useState({ grade: '3', classNum: '', stNo: '', name: '' });

                const analyzeResults = () => {
                    let totalItems = 0;
                    let correctItems = 0;
                    const itemAnalytics = QUESTIONS_DATA.map(q => {
                        const subResults = q.items.map((item, idx) => {
                            const ans = answers[q.id][idx];
                            let isCorrect = false;
                            if (item.type === 'choice') {
                                if (parseInt(ans) === item.correct) isCorrect = true;
                            } else {
                                if (ans && ans.toString().trim() === item.correct) isCorrect = true;
                            }
                            totalItems++;
                            if (isCorrect) correctItems++;
                            return isCorrect;
                        });
                        const isAllCorrect = subResults.every(v => v);
                        return { id: q.id, title: q.title, subResults, isAllCorrect };
                    });
                    return { totalItems, correctItems, itemAnalytics };
                };

                const exportToDocx = () => {
                    if(!window.docx) { alert("문서 생성 라이브러리를 불러오지 못했습니다."); return; }
                    const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = window.docx;
                    const results = analyzeResults();
                    const doc = new Document({
                        sections: [{
                            properties: {},
                            children: [
                                new Paragraph({ text: "원운동 연습문제 평가 리포트", heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, spacing: { after: 400 } }),
                                new Paragraph({ children: [ new TextRun({ text: "학생 정보: ", bold: true, size: 28 }), new TextRun({ text: `${studentInfo.grade}학년 ${studentInfo.classNum}반 ${studentInfo.stNo}번 ${studentInfo.name}`, size: 28 }) ], spacing: { after: 200 } }),
                                new Paragraph({ children: [ new TextRun({ text: "최종 평가 점수: ", bold: true, size: 36, color: "0052cc" }), new TextRun({ text: `${results.correctItems} / ${results.totalItems} 문항 정답`, size: 36, bold: true, color: "ff0000" }) ], spacing: { after: 600 } }),
                                ...results.itemAnalytics.filter(r => !r.isAllCorrect).map(r => new Paragraph({ text: `[${r.id.replace('q','')}번. ${r.title}] ${EXPLANATIONS[r.id]}`, spacing: { after: 240 } }))
                            ]
                        }]
                    });
                    Packer.toBlob(doc).then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        const safeName = studentInfo.name.trim() || '이름없음';
                        a.download = `원운동리포트_${studentInfo.grade}학년_${studentInfo.classNum}반_${studentInfo.stNo}번_${safeName}.docx`;
                        document.body.appendChild(a); a.click(); document.body.removeChild(a); window.URL.revokeObjectURL(url);
                    });
                };

                const handleSubInputChange = (qId, idx, val) => {
                    const newArr = [...answers[qId]];
                    newArr[idx] = val;
                    setAnswers({ ...answers, [qId]: newArr });
                };

                const isStepCompleted = (idx) => {
                    const q = QUESTIONS_DATA[idx];
                    return q && answers[q.id].every(v => v !== '');
                };

                if (submitted) {
                    const results = analyzeResults();
                    const wrongItems = results.itemAnalytics.filter(r => !r.isAllCorrect);
                    return (
                        <div className="max-w-4xl mx-auto p-6 bg-slate-900 rounded-[3rem] text-white shadow-2xl">
                            <h3 className="text-3xl font-black mb-6 italic">평가 결과 리포트</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="space-y-4">
                                    <div className="bg-white/10 p-8 rounded-3xl text-center border border-white/10">
                                        <p className="text-sm text-sky-400 font-bold mb-2 uppercase">최종 점수</p>
                                        <p className="text-6xl font-black">{results.correctItems} / {results.totalItems}</p>
                                    </div>
                                    <div className="bg-white/10 p-6 rounded-3xl border border-white/10 overflow-y-auto max-h-[300px] no-scrollbar">
                                        <p className="text-sm text-sky-400 font-bold mb-3 uppercase">문항별 정답</p>
                                        <div className="grid grid-cols-2 gap-2">
                                            {results.itemAnalytics.map((res, i) => (
                                                <div key={res.id} className={`p-3 rounded-xl border flex items-center justify-between ${res.isAllCorrect ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30'}`}>
                                                    <span className="text-xs font-bold text-slate-300">{i+1}번</span>
                                                    <span className="flex gap-1">
                                                        {res.subResults.map((r, ri) => (
                                                            <span key={ri} className={`w-5 h-5 flex items-center justify-center rounded text-[10px] ${r ? 'bg-emerald-500' : 'bg-rose-500'}`}>{r?'O':'X'}</span>
                                                        ))}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl border border-white/10 overflow-y-auto max-h-[400px] no-scrollbar">
                                    <p className="text-rose-400 font-bold flex items-center gap-2 mb-4"><Icon name="info" /> 오답 해설</p>
                                    {wrongItems.length === 0 ? <p className="text-emerald-400 font-bold">만점입니다! 축하합니다!</p> : 
                                        wrongItems.map(r => (
                                            <div key={r.id} className="mb-4 p-4 bg-black/20 rounded-xl border border-white/5 whitespace-pre-wrap text-[13px] leading-relaxed">
                                                <strong className="text-rose-300 block mb-1">[{r.id.replace('q','')}번. {r.title}]</strong>
                                                {EXPLANATIONS[r.id]}
                                            </div>
                                        ))
                                    }
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setSubmitted(false)} className="flex-1 py-4 bg-slate-700 rounded-2xl font-bold">오답 확인</button>
                                <button onClick={exportToDocx} className="flex-1 py-4 bg-blue-600 rounded-2xl font-black">리포트 다운로드</button>
                            </div>
                        </div>
                    );
                }

                return (
                    <div className="max-w-4xl mx-auto p-4 space-y-8 pb-20">
                        <div className="bg-slate-900 p-8 rounded-[2.5rem] mt-4 shadow-2xl text-white">
                            <h3 className="text-2xl font-black mb-6">📝 학생 정보 입력</h3>
                            <div className="grid grid-cols-4 gap-4">
                                {['grade', 'classNum', 'stNo', 'name'].map(field => (
                                    <div key={field}>
                                        <label className="text-slate-400 text-xs font-bold mb-2 block">{field === 'grade' ? '학년' : field === 'classNum' ? '반' : field === 'stNo' ? '번호' : '이름'}</label>
                                        <input type="text" className="w-full bg-slate-800 p-4 rounded-2xl outline-none font-bold" value={studentInfo[field]} onChange={e => setStudentInfo({...studentInfo, [field]: e.target.value})} />
                                    </div>
                                ))}
                            </div>
                        </div>
                        {QUESTIONS_DATA.slice(0, currentStep + 1).map((q, i) => (
                            <div key={q.id} className="bg-white p-8 rounded-[2.5rem] shadow-xl border-2 border-slate-50">
                                <div className="flex items-center justify-between mb-6">
                                    <div className="flex items-center gap-4">
                                        <span className="w-10 h-10 bg-slate-900 text-white flex items-center justify-center rounded-xl font-black">{(i+1 < 10 ? '0' : '') + (i+1)}</span>
                                        <h4 className="text-xl font-black text-slate-800">{q.title}</h4>
                                    </div>
                                    {i < currentStep && <span className="text-emerald-500 font-bold flex items-center gap-1"><Icon name="check-circle" /> 완료</span>}
                                </div>
                                <div className="bg-slate-50 p-6 rounded-2xl mb-6 text-slate-600 font-bold text-sm leading-relaxed whitespace-pre-wrap">{q.text}</div>
                                <div className={i < currentStep ? 'opacity-40 pointer-events-none' : ''}>
                                    <ProblemView type={q.view} />
                                    <div className="space-y-6">
                                        {q.items.map((sub, idx) => (
                                            <div key={idx} className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100">
                                                <p className="text-sm font-black text-slate-700 mb-4">{sub.label}</p>
                                                {sub.type === 'choice' ? (
                                                    <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                                                        {sub.options.map((opt, oIdx) => (
                                                            <button key={oIdx} onClick={() => handleSubInputChange(q.id, idx, oIdx)}
                                                            className={`py-3 px-2 rounded-xl text-[12px] font-bold border-2 transition-all ${parseInt(answers[q.id][idx]) === oIdx ? 'bg-slate-900 border-slate-900 text-white' : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300'}`}>
                                                                {opt}
                                                            </button>
                                                        ))}
                                                    </div>
                                                ) : (
                                                    <div className="relative max-w-xs flex items-center gap-2">
                                                        <input type="text" value={answers[q.id][idx]} onChange={e => handleSubInputChange(q.id, idx, e.target.value)}
                                                        className="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-lg font-black text-blue-500 outline-none focus:border-blue-400" placeholder="..." />
                                                        <span className="font-black text-slate-400 text-sm whitespace-nowrap">{sub.unit}</span>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                                {i === currentStep && isStepCompleted(i) && (
                                    <div className="mt-8 pt-8 border-t border-slate-100 flex justify-end">
                                        {i < QUESTIONS_DATA.length - 1 ? (
                                            <button onClick={() => { setCurrentStep(i + 1); setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100); }}
                                            className="px-10 py-4 bg-emerald-500 text-white rounded-2xl font-black shadow-lg hover:bg-emerald-600 transition-all">다음 문제</button>
                                        ) : (
                                            <button onClick={() => setSubmitted(true)} className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-black shadow-lg hover:bg-slate-800 transition-all">제출하기</button>
                                        )}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                );
            };
            ReactDOM.createRoot(document.getElementById('root')).render(<PracticeSection />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=2200, scrolling=True)

if __name__ == "__main__":
    run_practice()
