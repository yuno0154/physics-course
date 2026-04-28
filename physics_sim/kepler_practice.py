import streamlit as st
import streamlit.components.v1 as components

def run_practice():
    st.title("📝 케플러 법칙 복습 및 연습 문제")
    st.markdown("""
    그림과 상황을 보고 케플러 제1~3법칙을 적용하여 물리량을 분석하고 비교해 보세요.
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
                    title: '타원 궤도 성질 분석',
                    text: '그림은 태양 주위를 도는 행성의 공전 궤도를 간단하게 나타낸 것입니다. A는 근일점, B는 원일점입니다.',
                    view: 'ellipse_ab',
                    items: [
                        {
                            label: '(1) A, B 지점에서 행성의 속력 크기 관계는?',
                            type: 'choice',
                            options: ['vA > vB', 'vA = vB', 'vA < vB'],
                            correct: 0
                        },
                        {
                            label: '(2) 행성의 공전 주기의 제곱은 어떤 것의 세제곱에 비례합니까?',
                            type: 'choice',
                            options: ['태양의 질량', '반단경 b', '긴반지름 a'],
                            correct: 2
                        }
                    ]
                },
                {
                    id: 'q2',
                    type: 'multiple_sub_questions',
                    title: '케플러 제3법칙 적용',
                    text: '공전 주기가 T이고, 타원 궤도의 긴반지름이 a인 행성 A가 있습니다. 공전 주기가 8T인 행성 B의 긴반지름은 얼마인지 구하시오.',
                    view: 'none',
                    items: [
                        {
                            label: '행성 B의 긴반지름을 구하시오. (a의 몇 배인지 입력)',
                            type: 'input',
                            unit: 'a',
                            correct: '4'
                        }
                    ]
                },
                {
                    id: 'q3',
                    type: 'multiple_sub_questions',
                    title: '면적 속도 일정 법칙',
                    text: '그림과 같이 행성이 태양을 한 초점으로 하는 타원 궤도를 공전합니다. 행성이 점 a에서 점 b까지, 점 c에서 점 d까지 이동하는 동안 지나간 면적은 각각 S로 같습니다. 단, a와 c는 각각 근일점과 원일점이다.',
                    view: 'areas_S',
                    items: [
                        {
                            label: '1. a에서 b까지 이동 시간이 T일 때, c에서 d까지 이동 시간은?',
                            type: 'choice',
                            options: ['0.5T', 'T', '2T', '4T'],
                            correct: 1
                        },
                        {
                            label: '2. 점 c에서 어떤 점까지 2S의 면적을 지났다면 걸린 시간은 T의 몇 배?',
                            type: 'input',
                            unit: '배',
                            correct: '2'
                        }
                    ]
                },
                {
                    id: 'q4',
                    type: 'multiple_sub_questions',
                    title: '등속 원운동하는 인공위성 분석 (1)',
                    text: '그림과 같이 질량이 같은 인공위성 A, B가 반지름이 각각 r, 2r인 원 궤도를 따라 행성 주위를 등속 원운동하고 있습니다.',
                    view: 'circular_r_2r',
                    items: [
                        {
                            label: '1. 인공위성의 속력에 영향을 주는 요인 고르기 [보기: ㄱ.행성질량 ㄴ.위성질량 ㄷ.행성부피 ㄹ.위성크기 ㅁ.거리]',
                            type: 'choice',
                            options: ['ㄱ, ㄴ', 'ㄱ, ㅁ', 'ㄴ, ㄷ, ㅁ', 'ㄱ, ㄹ, ㅁ'],
                            correct: 1
                        },
                        {
                            label: '2-(1). A와 B의 속력을 비교하시오.',
                            type: 'choice',
                            options: ['vA > vB', 'vA = vB', 'vA < vB'],
                            correct: 0
                        },
                        {
                            label: '2-(2). A와 B의 공전 주기를 비교하시오.',
                            type: 'choice',
                            options: ['TA > TB', 'TA = TB', 'TA < TB'],
                            correct: 2
                        },
                        {
                            label: '2-(3). A와 B에 작용하는 중력의 크기를 비교하시오.',
                            type: 'choice',
                            options: ['FA > FB', 'FA = FB', 'FA < FB'],
                            correct: 0
                        },
                        {
                            label: '2-(4). A와 B의 가속도 크기를 비교하시오.',
                            type: 'choice',
                            options: ['aA > aB', 'aA = aB', 'aA < aB'],
                            correct: 0
                        }
                    ]
                },
                {
                    id: 'q5',
                    type: 'multiple_sub_questions',
                    title: '등속 원운동하는 인공위성 분석 (2)',
                    text: '그림과 같이 동일한 두 인공위성 A, B가 각각 궤도 반지름 r, 4r로 지구 주위를 공전하고 있습니다.',
                    view: 'circular_r_4r',
                    items: [
                        {
                            label: '(1) A와 B의 속력의 비 (vA : vB)를 고르시오.',
                            type: 'choice',
                            options: ['1 : 2', '1 : 4', '2 : 1', '4 : 1'],
                            correct: 2
                        },
                        {
                            label: '(2) A와 B의 공전 주기의 비 (TA : TB)를 고르시오.',
                            type: 'choice',
                            options: ['1 : 2', '1 : 4', '1 : 8', '8 : 1'],
                            correct: 2
                        }
                    ]
                },
                {
                    id: 'q6',
                    type: 'multiple_sub_questions',
                    title: '행성의 궤도와 물리량 분석',
                    text: '그림은 태양 주위를 도는 지구와 목성의 질량과 공전 궤도의 반지름을 간략하게 나타낸 것입니다.',
                    view: 'sun_earth_jupiter',
                    items: [
                        {
                            label: '이에 대한 설명으로 옳은 것만을 [보기]에서 있는 대로 고른 것은? [보기: ㄱ. 태양으로부터 받는 힘은 목성이 지구보다 크다. ㄴ. 구심 가속도의 크기는 지구가 목성보다 크다. ㄷ. 목성의 공전 주기는 지구의 약 25배이다.]',
                            type: 'choice',
                            options: ['① ㄱ', '② ㄴ', '③ ㄱ, ㄴ', '④ ㄱ, ㄷ', '⑤ ㄴ, ㄷ'],
                            correct: 2
                        }
                    ]
                },
                {
                    id: 'q7',
                    type: 'multiple_sub_questions',
                    title: '인공위성의 공전 주기',
                    text: '그림과 같이 질량이 같은 인공위성 A, B가 반지름이 각각 r, 2r인 원 궤도를 따라 지구 주위를 등속 원운동하고 있습니다.',
                    view: 'circular_r_2r_earth',
                    items: [
                        {
                            label: 'B의 주기는 A의 몇 배인가?',
                            type: 'choice',
                            options: ['① 1/8 배', '② 1/4 배', '③ √2 배', '④ 4 배', '⑤ √8 배'],
                            correct: 4
                        }
                    ]
                }
            ];

            const EXPLANATIONS = {
                q1: "제2법칙(면적 속도 일정)에 의해 태양과 가장 가까운 근일점(A)에서 속력이 가장 빠르고, 원일점(B)에서 가장 느립니다. 제3법칙(조화 법칙)에 의해 주기의 제곱은 장반경(긴반지름) a의 세제곱에 비례합니다.",
                q2: "T² ∝ a³ 이므로, 주기가 8배(8T)가 되면 주기의 제곱은 64배가 됩니다. 어떠한 수의 세제곱이 64가 되려면 해당 값은 4가 되어야 합니다. 따라서 장반경은 4a입니다.",
                q3: "훑고 지나간 면적이 S로 같다면 어느 지점이든 걸린 시간은 T로 항상 같습니다. 만약 지나간 면적이 2S가 되었다면 걸린 시간도 정확히 2배(2T)가 됩니다.",
                q4: "인공위성의 속력은 v = √(GM/r)이므로 중심 행성의 질량(M)과 궤도 반지름(r)에만 영향을 받습니다. 거리가 가까운 A가 중력이 크고(1/r²), 가속도가 크고(1/r²), 속력이 빠르고(1/√r), 주기가 짧습니다.",
                q5: "반지름 비가 r:4r=1:4 입니다. v는 1/√r에 비례하므로 속력비는 √4 : √1 = 2:1 입니다. 주기는 r^(3/2)에 비례하므로 1:8 입니다.",
                q6: "ㄱ. 중력의 크기 F = G(Mm/R²)입니다. 지구에 작용하는 힘은 m/r²에 비례하고 목성은 300m/25r² = 12m/r²에 비례하므로 목성이 더 큽니다. (O)\\n ㄴ. 구심 가속도 a = GM/R² 로 행성의 질량(m)과 무관하며 거리가 짧은 지구가 더 큽니다. (O)\\n ㄷ. 제3법칙(T² ∝ R³)에 의해 주기의 제곱은 125배입니다. 주기는 25배가 아니라 √125 ≈ 11.18배입니다. (X)",
                q7: "T² ∝ r³ 입니다. 궤도 반지름이 2배가 되면 주기의 제곱은 8배가 됩니다. 따라서 주기는 √8 배(혹은 2√2 배)가 됩니다."
            };

            // --- Components ---
            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => { if (window.lucide) window.lucide.createIcons(); }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const ProblemView = ({ type }) => {
                if (type === 'none') return null;
                
                let svgInner = null;
                if (type === 'ellipse_ab') {
                    svgInner = (
                        <g>
                            <ellipse cx="150" cy="90" rx="120" ry="70" fill="none" stroke="#60a5fa" strokeWidth="2" />
                            <line x1="30" y1="90" x2="270" y2="90" stroke="#94a3b8" strokeDasharray="4,4" />
                            <line x1="150" y1="20" x2="150" y2="160" stroke="#94a3b8" strokeDasharray="4,4" />
                            <circle cx="52.5" cy="90" r="14" fill="url(#sunGrad)" />
                            <text x="52.5" y="70" fontSize="12" textAnchor="middle" fill="#f59e0b" fontWeight="bold">태양</text>
                            <circle cx="247.5" cy="90" r="3" fill="#94a3b8" />
                            <circle cx="30" cy="90" r="6" fill="#8b5cf6" />
                            <text x="15" y="94" fontSize="14" fontWeight="bold">A</text>
                            <circle cx="270" cy="90" r="6" fill="#8b5cf6" />
                            <text x="285" y="94" fontSize="14" fontWeight="bold">B</text>
                            <path d="M 150 90 Q 210 75 270 90" fill="none" stroke="#64748b" strokeDasharray="2,2" />
                            <text x="210" y="80" fontSize="12" fill="#64748b" fontStyle="italic" fontWeight="bold">a</text>
                            <path d="M 150 20 Q 135 55 150 90" fill="none" stroke="#64748b" strokeDasharray="2,2" />
                            <text x="135" y="55" fontSize="12" fill="#64748b" fontStyle="italic" fontWeight="bold">b</text>
                        </g>
                    );
                } else if (type === 'areas_S') {
                    svgInner = (
                        <g>
                            <ellipse cx="150" cy="90" rx="120" ry="70" fill="none" stroke="#3b82f6" strokeWidth="1.5" strokeDasharray="3,3" />
                            <circle cx="52.5" cy="90" r="10" fill="#f59e0b" />
                            <path d="M 52.5 90 L 30 90 A 120 70 0 0 0 45 125 Z" fill="rgba(74, 222, 128, 0.3)" stroke="#22c55e" strokeWidth="1"/>
                            <text x="45" y="105" fontSize="12" fontWeight="bold" fill="#166534">S</text>
                            <circle cx="30" cy="90" r="4" fill="#1e293b" />
                            <text x="20" y="94" fontSize="12">a</text>
                            <circle cx="45" cy="125" r="4" fill="#1e293b" />
                            <text x="35" y="135" fontSize="12">b</text>
                            <path d="M 52.5 90 L 270 90 A 120 70 0 0 0 250 45 Z" fill="rgba(74, 222, 128, 0.3)" stroke="#22c55e" strokeWidth="1"/>
                            <text x="180" y="80" fontSize="12" fontWeight="bold" fill="#166534">S</text>
                            <circle cx="270" cy="90" r="4" fill="#1e293b" />
                            <text x="280" y="94" fontSize="12">c</text>
                            <circle cx="250" cy="45" r="4" fill="#1e293b" />
                            <text x="255" y="40" fontSize="12">d</text>
                        </g>
                    );
                } else if (type === 'circular_r_2r' || type === 'circular_r_2r_earth') {
                    const isEarth = type.includes('earth');
                    svgInner = (
                        <g transform="translate(150, 120)">
                            <circle cx="0" cy="0" r="40" fill="none" stroke="#94a3b8" strokeDasharray="4,4" />
                            <circle cx="0" cy="0" r="100" fill="none" stroke="#94a3b8" strokeDasharray="4,4" />
                            <circle cx="0" cy="0" r="14" fill={isEarth ? "#93c5fd" : "#cdb4db"} />
                            <line x1="0" y1="0" x2="35" y2="-20" stroke="#64748b" strokeDasharray="2,2" />
                            <text x="15" y="-20" fontSize="12" fontWeight="bold">r</text>
                            <circle cx="35" cy="-20" r="8" fill="#facc15" />
                            <text x="45" y="-28" fontSize="14" fontWeight="bold">A</text>
                            <path d="M 35 -20 L 18 -50" fill="none" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow)" />
                            
                            <line x1="0" y1="0" x2="-80" y2="-60" stroke="#64748b" strokeDasharray="2,2" />
                            <text x="-50" y="-40" fontSize="12" fontWeight="bold">2r</text>
                            <circle cx="-80" cy="-60" r="8" fill="#facc15" />
                            <text x="-90" y="-70" fontSize="14" fontWeight="bold">B</text>
                            <path d="M -80 -60 L -95 -40" fill="none" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow)" />
                        </g>
                    );
                } else if (type === 'circular_r_4r') {
                    svgInner = (
                        <g transform="translate(50, 100)">
                            <circle cx="0" cy="0" r="40" fill="none" stroke="#60a5fa" strokeWidth="1.5" />
                            <circle cx="0" cy="0" r="160" fill="none" stroke="#60a5fa" strokeWidth="1.5" />
                            <circle cx="0" cy="0" r="16" fill="#93c5fd" />
                            <circle cx="0" cy="0" r="8" fill="#10b981" />
                            <line x1="0" y1="0" x2="28" y2="28" stroke="#475569" strokeDasharray="2,2" />
                            <text x="10" y="25" fontSize="12" fontWeight="bold">r</text>
                            <circle cx="28" cy="28" r="6" fill="#f59e0b" />
                            <text x="40" y="40" fontSize="14" fontWeight="bold">A</text>
                            <line x1="28" y1="28" x2="48" y2="8" fill="none" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow)" />
                            
                            <line x1="0" y1="0" x2="160" y2="0" stroke="#475569" strokeDasharray="2,2" />
                            <text x="80" y="-5" fontSize="12" fontWeight="bold">4r</text>
                            <circle cx="160" cy="0" r="6" fill="#f59e0b" />
                            <text x="175" y="5" fontSize="14" fontWeight="bold">B</text>
                            <line x1="160" y1="0" x2="160" y2="-30" fill="none" stroke="#ef4444" strokeWidth="2" markerEnd="url(#arrow)" />
                        </g>
                    );
                } else if (type === 'sun_earth_jupiter') {
                    svgInner = (
                        <g transform="translate(280, 80)">
                            <circle cx="0" cy="0" r="50" fill="none" stroke="#60a5fa" strokeWidth="1.5" />
                            <circle cx="0" cy="0" r="12" fill="#f59e0b" />
                            <circle cx="50" cy="0" r="6" fill="#10b981" />
                            <text x="65" y="4" fontSize="12" fontWeight="bold">지구</text>
                            <line x1="0" y1="0" x2="50" y2="0" stroke="#94a3b8" strokeDasharray="2,2" />
                            <text x="25" y="-5" fontSize="12" fontWeight="bold">r</text>
                            <path d="M -160 -60 Q -190 0 -160 60" fill="none" stroke="#22c55e" strokeWidth="1.5" markerStart="url(#arrow_green)" markerEnd="url(#arrow_green)"/>
                            <circle cx="-174" cy="0" r="10" fill="#f97316" />
                            <text x="-174" y="25" fontSize="12" textAnchor="middle" fontWeight="bold">목성</text>
                            <line x1="-174" y1="0" x2="0" y2="0" stroke="#94a3b8" strokeDasharray="2,2" />
                            <text x="-87" y="-5" fontSize="12" fontWeight="bold">5r</text>
                        </g>
                    );
                }
                
                return (
                    <div className="bg-slate-50 p-6 rounded-3xl flex items-center justify-center border border-slate-100 overflow-hidden mb-6">
                        <svg viewBox="0 0 350 200" className="w-full max-w-[450px]">
                            <defs>
                                <radialGradient id="sunGrad">
                                    <stop offset="0%" stopColor="#fde047" />
                                    <stop offset="100%" stopColor="#f59e0b" />
                                </radialGradient>
                                <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                                </marker>
                                <marker id="arrow_green" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="4" markerHeight="4" orient="auto-start-reverse">
                                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#22c55e" />
                                </marker>
                            </defs>
                            {svgInner}
                        </svg>
                    </div>
                );
            };

            const PracticeSection = () => {
                const [answers, setAnswers] = useState({ 
                    q1: ['', ''], q2: [''], q3: ['', ''], 
                    q4: ['', '', '', '', ''], q5: ['', ''], q6: [''], q7: [''] 
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
                                new Paragraph({ text: "케플러 법칙 연습문제 평가 리포트", heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, spacing: { after: 400 } }),
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
                        a.download = `케플러리포트_${studentInfo.grade}학년_${studentInfo.classNum}반_${studentInfo.stNo}번_${safeName}.docx`;
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
                                            <div key={r.id} className="mb-4 p-4 bg-black/20 rounded-xl border border-white/5 whitespace-pre-wrap text-sm">
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
                                <div className="bg-slate-50 p-6 rounded-2xl mb-6 text-slate-600 font-bold text-sm leading-relaxed">{q.text}</div>
                                <div className={i < currentStep ? 'opacity-40 pointer-events-none' : ''}>
                                    <ProblemView type={q.view} />
                                    <div className="space-y-6">
                                        {q.items.map((sub, idx) => (
                                            <div key={idx} className="bg-slate-50/50 p-6 rounded-2xl border border-slate-100">
                                                <p className="text-sm font-black text-slate-700 mb-4">{sub.label}</p>
                                                {sub.type === 'choice' ? (
                                                    <div className="grid grid-cols-1 md:grid-cols-5 gap-2">
                                                        {sub.options.map((opt, oIdx) => (
                                                            <button key={oIdx} onClick={() => handleSubInputChange(q.id, idx, oIdx)}
                                                            className={`py-3 px-2 rounded-xl text-[12px] font-bold border-2 transition-all ${parseInt(answers[q.id][idx]) === oIdx ? 'bg-slate-900 border-slate-900 text-white' : 'bg-white border-slate-200 text-slate-500'}`}>
                                                                {opt}
                                                            </button>
                                                        ))}
                                                    </div>
                                                ) : (
                                                    <div className="relative max-w-xs flex items-center gap-2">
                                                        <input type="text" value={answers[q.id][idx]} onChange={e => handleSubInputChange(q.id, idx, e.target.value)}
                                                        className="w-full bg-white border-2 border-slate-200 rounded-xl px-4 py-3 text-lg font-black text-rose-500 outline-none" />
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
                                            className="px-10 py-4 bg-emerald-500 text-white rounded-2xl font-black shadow-lg">다음 문제</button>
                                        ) : (
                                            <button onClick={() => setSubmitted(true)} className="px-10 py-4 bg-slate-900 text-white rounded-2xl font-black shadow-lg">제출하기</button>
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
    components.html(react_code, height=2000, scrolling=True)

if __name__ == "__main__":
    run_practice()
