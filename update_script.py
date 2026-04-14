import re

# 1. Circular Motion Practice Update
path_cm = r'd:\OneDrive - 사곡고등학교\2026학년도\프로그램 개발\물리학 가상실험\physics_sim\circular_motion_practice.py'
with open(path_cm, 'r', encoding='utf-8') as f:
    code = f.read()

if '<script src="https://unpkg.com/docx@8.5.0/build/index.umd.js"></script>' not in code:
    code = code.replace('<script src="https://cdn.tailwindcss.com"></script>\n        <script src="https://unpkg.com/lucide@latest"></script>', '<script src="https://cdn.tailwindcss.com"></script>\n        <script src="https://unpkg.com/docx@8.5.0/build/index.umd.js"></script>\n        <script src="https://unpkg.com/lucide@latest"></script>')

state_replacement = """                const [currentStep, setCurrentStep] = useState(0);
                const [submitted, setSubmitted] = useState(false);
                const [studentInfo, setStudentInfo] = useState({ grade: '3', classNum: '', stNo: '', name: '' });

                const analyzeResults = () => {
                    let totalItems = 0;
                    let correctItems = 0;
                    const itemAnalytics = questions.map(q => {
                        let subResults = [];
                        if (q.type === 'ox') {
                            subResults = q.items.map((item, idx) => answers[q.id] && answers[q.id][idx] === q.correct[idx]);
                        } else if (q.type === 'sim_problem') {
                            subResults = q.items.map((item, idx) => answers[q.id] && answers[q.id][idx] && answers[q.id][idx].toString().trim() === item.correct);
                        } else if (q.type === 'graph_problem') {
                            subResults = q.items.map((item, idx) => {
                                const ans = answers[q.id] ? answers[q.id][idx] : null;
                                if (item.type === 'choice') {
                                    return parseInt(ans) === item.correct;
                                } else {
                                    return ans && ans.toString().trim() === item.correct;
                                }
                            });
                        } else if (q.type === 'concept_choice' || q.type === 'multi_choice') {
                            const ans = answers[q.id];
                            subResults = [ans !== null && parseInt(ans) === q.correct];
                        }
                        
                        subResults.forEach(r => {
                            totalItems++;
                            if(r) correctItems++;
                        });

                        const isAllCorrect = subResults.every(v => v);
                        return { id: q.id, title: q.title, subResults, isAllCorrect };
                    });
                    return { totalItems, correctItems, itemAnalytics };
                };

                const getExplanationText = (id) => {
                    const explanations = {
                        q1: "등속 원운동은 속도(방향 포함)가 매순간 변하므로 등가속도가 아닌 가속도 운동입니다. 구심력 크기는 일정하나 중심을 향하므로 방향이 변합니다.",
                        q2: "ω = 2π/2 = 3.14 rad/s, T=2s, f=0.5Hz, a = v²/r = (2π)²/2 ≈ 19.7, F = 39.5N.",
                        q3: "1회전에 2t₀가 소요되므로 주기는 2t₀입니다. ω=2π/2t₀ = π/t₀. 가속도는 중심으로 향합니다.",
                        q4: "B가 정지해 있으므로 실의 장력 T=2mg입니다. 구심력 mv²/r = 2mg, v=√(2rg). (ㄱ, ㄷ)",
                        q5: "영희의 거리가 2배이므로 속력과 가속도가 2배입니다. 구심력은 질량이 절반이라 철수와 같습니다. (ㄱ, ㄴ)",
                        q6: "접선 가속도가 일정하므로 속력이 비례 증가하며, 추진력이 사라진 이후 일정한 속력을 유지합니다. (ㄱ, ㄷ)"
                    };
                    return explanations[id] || "";
                };

                const exportToDocx = () => {
                    if(!window.docx) return alert("라이브러리 로드 실패");
                    const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = window.docx;
                    const results = analyzeResults();
                    
                    const doc = new Document({
                        sections: [{
                            properties: {},
                            children: [
                                new Paragraph({ text: "원운동 연습문제 평가 리포트", heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, spacing: { after: 400 } }),
                                new Paragraph({ children: [new TextRun({ text: "학생 정보: ", bold: true, size: 28 }), new TextRun({ text: `${studentInfo.grade}학년 ${studentInfo.classNum}반 ${studentInfo.stNo}번 ${studentInfo.name}`, size: 28 })], spacing: { after: 200 } }),
                                new Paragraph({ children: [new TextRun({ text: "최종 평가: ", bold: true, size: 36, color: "0052cc" }), new TextRun({ text: `${results.correctItems} / ${results.totalItems} 문항 정답`, size: 36, bold: true, color: "ff0000" })], spacing: { after: 600 } }),
                                new Paragraph({ text: "[오답 해설 요약]", heading: HeadingLevel.HEADING_2, spacing: { after: 300 } }),
                                ...results.itemAnalytics.filter(r => !r.isAllCorrect).map(r => new Paragraph({ text: `[${r.id.replace('q','')}번. ${r.title}] ${getExplanationText(r.id)}`, spacing: { after: 240 } }))
                            ]
                        }]
                    });

                    Packer.toBlob(doc).then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        const safeName = studentInfo.name.trim() ? studentInfo.name.trim() : '이름없음';
                        a.download = `원운동리포트_${studentInfo.grade}학년_${studentInfo.classNum}반_${studentInfo.stNo}번_${safeName}.docx`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    });
                };"""

match = re.search(r'                const \[currentStep, setCurrentStep\] = useState\(\d+\);\n                const \[submitted, setSubmitted\] = useState\(false\);', code)
if match and 'const getExplanationText' not in code:
    code = code[:match.start()] + state_replacement + code[match.end():]

submitted_replacement = """                if (submitted) {
                    const results = analyzeResults();
                    const wrongItems = results.itemAnalytics.filter(r => !r.isAllCorrect);
                    
                    return (
                        <div className="max-w-4xl mx-auto p-6 bg-slate-900 rounded-[3rem] text-white shadow-2xl animate-in zoom-in duration-500">
                            <h3 className="text-3xl font-black mb-6 italic">평가 결과 리포트</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="space-y-4 flex flex-col justify-between">
                                    <div className="bg-white/10 p-8 rounded-3xl text-center border border-white/10">
                                        <p className="text-sm text-sky-400 font-bold mb-2 uppercase">최종 점수</p>
                                        <p className="text-6xl font-black">{results.correctItems} / {results.totalItems}</p>
                                    </div>
                                    <div className="bg-white/10 p-6 rounded-3xl flex-1 border border-white/10">
                                        <p className="text-sm text-sky-400 font-bold mb-3 uppercase">문항별 정답 확인</p>
                                        <div className="grid grid-cols-2 gap-2">
                                            {results.itemAnalytics.map((res, i) => (
                                                <div key={res.id} className={`p-3 rounded-xl border flex items-center justify-between ${res.isAllCorrect ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30'}`}>
                                                    <span className="text-sm font-bold text-slate-300">{i+1}번</span>
                                                    <span className="text-xs flex gap-1 flex-wrap justify-end">
                                                        {res.subResults.map((r, ri) => (
                                                            <span key={ri} className={`flex items-center justify-center w-5 h-5 rounded-md ${r ? 'bg-emerald-500/80 text-white' : 'bg-rose-500/80 text-white'}`}>
                                                                {r ? 'O' : 'X'}
                                                            </span>
                                                        ))}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl space-y-4 border border-white/10 overflow-y-auto max-h-[400px] no-scrollbar">
                                    <p className="text-rose-400 font-bold flex items-center gap-2"><Icon name="info" /> 오답 해설</p>
                                    <div className="text-[13px] text-slate-300 leading-relaxed space-y-5">
                                        {wrongItems.length === 0 ? (
                                            <div className="p-4 bg-emerald-500/20 text-emerald-400 rounded-xl font-bold text-center">
                                                모든 문제를 맞추셨습니다! 완벽합니다. 🎉
                                            </div>
                                        ) : (
                                            wrongItems.map(r => (
                                                <div key={r.id} className="p-4 bg-black/20 rounded-xl border border-white/5 disabled whitespace-pre-wrap">
                                                    <strong className="text-rose-300 block mb-2">[{r.id.replace('q','')}번. {r.title}]</strong>
                                                    {getExplanationText(r.id)}
                                                </div>
                                            ))
                                        )}
                                    </div>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setSubmitted(false)} className="flex-1 py-4 bg-slate-700 rounded-2xl font-bold hover:bg-slate-600 transition-all">오답 확인하기</button>
                                <button onClick={exportToDocx} className="flex-1 py-4 bg-blue-600 rounded-2xl font-black hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/30">리포트 다운로드 (DOCX)</button>
                            </div>
                        </div>
                    );
                }"""

match_sub = re.search(r'                if \(submitted\) \{.*?(?=\s+return \(\n\s+<div className="max-w-4xl)', code, flags=re.DOTALL)
if match_sub and 'const wrongItems =' not in code:
    code = code[:match_sub.start()] + submitted_replacement + code[match_sub.end():]

form_html = """                        <div className="bg-slate-900 p-8 rounded-[2.5rem] mt-4 shadow-2xl animate-in fade-in slide-in-from-top-4 duration-500">
                            <h3 className="text-white text-2xl font-black mb-6">📝 학생 정보 입력</h3>
                            <div className="grid grid-cols-4 gap-4">
                                <div><label className="text-slate-400 text-sm font-bold ml-2 mb-2 block">학년</label><input type="text" className="w-full bg-slate-800 text-white p-4 rounded-2xl outline-none font-bold" placeholder="예: 3" value={studentInfo.grade} onChange={e=>setStudentInfo({...studentInfo, grade: e.target.value})} /></div>
                                <div><label className="text-slate-400 text-sm font-bold ml-2 mb-2 block">반</label><input type="text" className="w-full bg-slate-800 text-white p-4 rounded-2xl outline-none font-bold" placeholder="반" value={studentInfo.classNum} onChange={e=>setStudentInfo({...studentInfo, classNum: e.target.value})} /></div>
                                <div><label className="text-slate-400 text-sm font-bold ml-2 mb-2 block">번호</label><input type="text" className="w-full bg-slate-800 text-white p-4 rounded-2xl outline-none font-bold" placeholder="번호" value={studentInfo.stNo} onChange={e=>setStudentInfo({...studentInfo, stNo: e.target.value})} /></div>
                                <div><label className="text-slate-400 text-sm font-bold ml-2 mb-2 block">이름</label><input type="text" className="w-full bg-slate-800 text-white p-4 rounded-2xl outline-none font-bold flex-1" placeholder="이름" value={studentInfo.name} onChange={e=>setStudentInfo({...studentInfo, name: e.target.value})} /></div>
                            </div>
                        </div>
                        {questions.slice"""

if '📝 학생 정보 입력' not in code:
    code = code.replace('                        {questions.slice', form_html)

with open(path_cm, 'w', encoding='utf-8') as f:
    f.write(code)


# 2. Kepler Practice Update
path_kep = r'd:\OneDrive - 사곡고등학교\2026학년도\프로그램 개발\물리학 가상실험\physics_sim\kepler_practice.py'
with open(path_kep, 'r', encoding='utf-8') as f:
    code2 = f.read()

kepler_state_replacement = """                const [studentInfo, setStudentInfo] = useState({ grade: '3', classNum: '', stNo: '', name: '' });

                const analyzeResults = () => {
                    let totalItems = 0;
                    let correctItems = 0;
                    const itemAnalytics = questions.map(q => {
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

                const getExplanationText = (id) => {
                    const explanations = {
                        q1: "제2법칙(면적 속도 일정)에 의해 태양과 가장 가까운 근일점(A)에서 속력이 가장 빠르고, 원일점(B)에서 가장 느립니다. 제3법칙(조화 법칙)에 의해 주기의 제곱은 장반경(긴반지름) a의 세제곱에 비례합니다.",
                        q2: "T² ∝ a³ 이므로, 주기가 8배(8T)가 되면 주기의 제곱은 64배가 됩니다. 어떠한 수의 세제곱이 64가 되려면 해당 값은 4가 되어야 합니다. 따라서 장반경은 4a입니다.",
                        q3: "훑고 지나간 면적이 S로 같다면 어느 지점이든 걸린 시간은 T로 항상 같습니다. 만약 지나간 면적이 2S가 되었다면 걸린 시간도 정확히 2배(2T)가 됩니다.",
                        q4: "인공위성의 속력은 v = √(GM/r)이므로 중심 행성의 질량(M)과 궤도 반지름(r)에만 영향을 받습니다. 거리가 가까운 A가 중력이 크고(1/r²), 가속도가 크고(1/r²), 속력이 빠르고(1/√r), 주기가 짧습니다.",
                        q5: "반지름 비가 r:4r=1:4 입니다. v는 1/√r에 비례하므로 속력비는 √4 : √1 = 2:1 입니다. 주기는 r^(3/2)에 비례하므로 1:8 입니다.",
                        q6: "ㄱ. 중력의 크기 F = G(Mm/R²)입니다. 지구에 작용하는 힘은 m/r²에 비례하고 목성은 300m/25r² = 12m/r²에 비례하므로 목성이 더 큽니다. (O)\\n ㄴ. 구심 가속도 a = GM/R² 로 행성의 질량(m)과 무관하며 거리가 짧은 지구가 더 큽니다. (O)\\n ㄷ. 제3법칙(T² ∝ R³)에 의해 주기의 제곱은 125배입니다. 주기는 25배가 아니라 √125 ≈ 11.18배입니다. (X)",
                        q7: "T² ∝ r³ 입니다. 궤도 반지름이 2배가 되면 주기의 제곱은 8배가 됩니다. 따라서 주기는 √8 배(혹은 2√2 배)가 됩니다."
                    };
                    return explanations[id] || "";
                };

                const exportToDocx = () => {
                    if(!window.docx) {
                        alert("문서 생성 라이브러리를 불러오지 못했습니다.");
                        return;
                    }
                    const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = window.docx;
                    const results = analyzeResults();

                    const doc = new Document({
                        sections: [{
                            properties: {},
                            children: [
                                new Paragraph({
                                    text: "케플러 법칙 연습문제 평가 리포트",
                                    heading: HeadingLevel.HEADING_1,
                                    alignment: AlignmentType.CENTER,
                                    spacing: { after: 400 }
                                }),
                                new Paragraph({
                                    children: [
                                        new TextRun({ text: "학생 정보: ", bold: true, size: 28 }),
                                        new TextRun({ text: `${studentInfo.grade}학년 ${studentInfo.classNum}반 ${studentInfo.stNo}번 ${studentInfo.name}`, size: 28 })
                                    ],
                                    spacing: { after: 200 }
                                }),
                                new Paragraph({
                                    children: [
                                        new TextRun({ text: "최종 평가 점수: ", bold: true, size: 36, color: "0052cc" }),
                                        new TextRun({ text: `${results.correctItems} / ${results.totalItems} 문항 정답`, size: 36, bold: true, color: "ff0000" })
                                    ],
                                    spacing: { after: 600 }
                                }),
                                new Paragraph({
                                    text: "[오답 상세 해설 및 정답 요약]",
                                    heading: HeadingLevel.HEADING_2,
                                    spacing: { after: 300 }
                                }),
                                ...results.itemAnalytics.filter(r => !r.isAllCorrect).map(r => new Paragraph({ text: `[${r.id.replace('q','')}번. ${r.title}] ${getExplanationText(r.id)}`, spacing: { after: 240 } }))
                            ]
                        }]
                    });

                    Packer.toBlob(doc).then(blob => {
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement("a");
                        a.href = url;
                        const safeName = studentInfo.name.trim() ? studentInfo.name.trim() : '이름없음';
                        a.download = `케플러리포트_${studentInfo.grade}학년_${studentInfo.classNum}반_${studentInfo.stNo}번_${safeName}.docx`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                    });
                };"""

match_kep_state = re.search(r'                const \[studentInfo, setStudentInfo\] = useState\(\{ grade: \'.*?\', classNum: \'\', stNo: \'\', name: \'\' \}\);\n\n                const exportToDocx = \(\) => \{.*?(?=\s+const questions = \[)', code2, re.DOTALL)
if match_kep_state and 'analyzeResults' not in code2:
    code2 = code2[:match_kep_state.start()] + kepler_state_replacement + code2[match_kep_state.end():]

# Kepler placeholder fix
code2 = code2.replace('placeholder="예: 2"', 'placeholder="예: 3"')

kepler_submitted_replacement = """                if (submitted) {
                    const results = analyzeResults();
                    const wrongItems = results.itemAnalytics.filter(r => !r.isAllCorrect);

                    return (
                        <div className="max-w-4xl mx-auto p-6 bg-slate-900 rounded-[3rem] text-white shadow-2xl animate-in zoom-in duration-500">
                            <h3 className="text-3xl font-black mb-6 italic">평가 결과 리포트</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="space-y-4 flex flex-col justify-between">
                                    <div className="bg-white/10 p-8 rounded-3xl text-center border border-white/10 flex flex-col justify-center">
                                        <p className="text-sm text-sky-400 font-bold mb-2 uppercase">최종 점수</p>
                                        <p className="text-6xl font-black">{results.correctItems} / {results.totalItems}</p>
                                    </div>
                                    <div className="bg-white/10 p-6 rounded-3xl flex-1 border border-white/10">
                                        <p className="text-sm text-sky-400 font-bold mb-3 uppercase">문항별 정답 확인</p>
                                        <div className="grid grid-cols-2 gap-2">
                                            {results.itemAnalytics.map((res, i) => (
                                                <div key={res.id} className={`p-3 rounded-xl border flex items-center justify-between ${res.isAllCorrect ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30'}`}>
                                                    <span className="text-sm font-bold text-slate-300">{i+1}번</span>
                                                    <span className="text-xs flex gap-1 flex-wrap justify-end">
                                                        {res.subResults.map((r, ri) => (
                                                            <span key={ri} className={`flex items-center justify-center w-5 h-5 rounded-md ${r ? 'bg-emerald-500/80 text-white' : 'bg-rose-500/80 text-white'}`}>
                                                                {r ? 'O' : 'X'}
                                                            </span>
                                                        ))}
                                                    </span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl space-y-4 border border-white/10 overflow-y-auto max-h-[400px] no-scrollbar">
                                    <p className="text-rose-400 font-bold flex items-center gap-2 text-lg"><Icon name="info" /> 오답 해설</p>
                                    <div className="text-[13px] text-slate-300 leading-relaxed space-y-5">
                                        {wrongItems.length === 0 ? (
                                            <div className="p-4 bg-emerald-500/20 text-emerald-400 rounded-xl font-bold text-center">
                                                모든 문제를 맞추셨습니다! 완벽합니다. 🎉
                                            </div>
                                        ) : (
                                            wrongItems.map(r => (
                                                <div key={r.id} className="p-4 bg-black/20 rounded-xl border border-white/5 disabled whitespace-pre-wrap">
                                                    <strong className="text-rose-300 block mb-2">[{r.id.replace('q','')}번. {r.title}]</strong>
                                                    {getExplanationText(r.id)}
                                                </div>
                                            ))
                                        )}
                                    </div>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setSubmitted(false)} className="flex-1 py-4 bg-slate-700 rounded-2xl font-bold hover:bg-slate-600 transition-all">오답 확인하기</button>
                                <button onClick={exportToDocx} className="flex-1 py-4 bg-blue-600 rounded-2xl font-black hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/30">리포트 다운로드 (DOCX)</button>
                            </div>
                        </div>
                    );
                }"""

match_kep_sub = re.search(r'                if \(submitted\) \{.*?(?=\s+return \(\n\s+<div className="max-w-4xl)', code2, flags=re.DOTALL)
if match_kep_sub and 'const wrongItems =' not in code2:
    code2 = code2[:match_kep_sub.start()] + kepler_submitted_replacement + code2[match_kep_sub.end():]

with open(path_kep, 'w', encoding='utf-8') as f:
    f.write(code2)

print("Updates applied completely!")
