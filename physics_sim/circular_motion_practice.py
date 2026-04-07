import streamlit as st
import streamlit.components.v1 as components

def run_practice():
    st.title("📝 [마무리] 원운동 실전 연습 문제")
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
                const [answers, setAnswers] = useState({ q1: '', q2: '', q3: '', q4: '', q5: '' });
                const [submitted, setSubmitted] = useState(false);

                const questions = [
                    { id: 'q1', title: '구심 가속도의 크기', text: '반지름 10m인 원 궤도를 20m/s의 속력으로 도는 물체의 구심 가속도는?', unit: 'm/s²', correct: '40' },
                    { id: 'q2', title: '각속도 계산', text: '반지름 2m인 원을 10m/s의 속력으로 도는 물체의 각속도(ω)는?', unit: 'rad/s', correct: '5' },
                    { id: 'q3', title: '주기와 진동수', text: '각속도가 2π rad/s인 물체의 회전 주기(T)는?', unit: 's', correct: '1' },
                    { id: 'q4', title: '구심력 추론', text: '질량 2kg인 물체가 반지름 1m, 각속도 3rad/s로 회전할 때 필요한 구심력은?', unit: 'N', correct: '18' },
                    { id: 'q5', title: '성분 분해', text: '반지름 r, 각속도 ω로 운동하는 물체의 x축 가속도 성분 ax의 최대 크기는?', unit: 'rω²', correct: '1' }
                ];

                const getScore = () => {
                    let s = 0;
                    questions.forEach(q => { if(answers[q.id].trim() === q.correct) s++; });
                    return s;
                };

                if (submitted) {
                    return (
                        <div className="max-w-4xl mx-auto p-6 bg-slate-900 rounded-[3rem] text-white shadow-2xl animate-in zoom-in duration-500">
                            <h3 className="text-3xl font-black mb-6 italic">평가 결과 리포트</h3>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                                <div className="bg-white/10 p-8 rounded-3xl text-center border border-white/10">
                                    <p className="text-sm text-sky-400 font-bold mb-2 uppercase">최종 점수</p>
                                    <p className="text-6xl font-black">{getScore()} / 5</p>
                                </div>
                                <div className="bg-white/10 p-8 rounded-3xl space-y-4 border border-white/10">
                                    <p className="text-amber-400 font-bold flex items-center gap-2"><Icon name="info" /> 주요 해설</p>
                                    <p className="text-sm text-slate-300 leading-relaxed">구심 가속도 a = v²/r = rω² 공식을 활용합니다. 각속도 ω = v/r 이며, 주기는 T = 2π/ω 입니다.</p>
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <button onClick={() => setSubmitted(false)} className="flex-1 py-4 bg-slate-700 rounded-2xl font-bold hover:bg-slate-600 transition-all">다시 풀기</button>
                                <button className="flex-1 py-4 bg-blue-600 rounded-2xl font-black hover:bg-blue-500 transition-all shadow-lg shadow-blue-500/30">DOCX 리포트 다운로드</button>
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
                                    <div className="bg-slate-50 p-6 rounded-2xl mb-6 text-slate-600 font-medium leading-relaxed italic border border-slate-100 uppercase text-sm tracking-tight">{q.text}</div>
                                    <div className="relative">
                                        <input type="text" value={answers[q.id]} onChange={e => setAnswers({...answers, [q.id]: e.target.value})} className="w-full bg-slate-50 border-2 border-slate-100 rounded-2xl px-6 py-4 text-xl font-black text-blue-600 outline-none focus:border-blue-400 focus:bg-white transition-all" placeholder="정답 입력..." />
                                        <span className="absolute right-6 top-1/2 -translate-y-1/2 font-black text-slate-300 italic">{q.unit}</span>
                                    </div>
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
