import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 법칙: 인출 학습 및 오개념 교정", layout="wide")
    
    st.title("📝 케플러 법칙: 인출 학습 및 오개념 교정")
    st.markdown("""
    학습한 내용을 바탕으로 퀴즈를 풀며 자신의 이해도를 점검해 보세요. 
    특히 **행성의 속도와 거리, 중력의 관계**에 대한 대표적인 오개념을 바로잡는 것이 목표입니다.
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
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerPractice = () => {
                const [quizAnswer, setQuizAnswer] = useState(null);
                const [showFeedback, setShowFeedback] = useState(false);

                const checkAnswer = (ans) => {
                    setQuizAnswer(ans);
                    setShowFeedback(true);
                };

                return (
                    <div className="max-w-3xl mx-auto p-4 space-y-8">
                        <div className="bg-white p-10 rounded-3xl border border-slate-200 shadow-2xl relative overflow-hidden">
                            <div className="absolute top-0 left-0 w-2 h-full bg-blue-600"></div>
                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 bg-blue-50 rounded-2xl text-blue-600">
                                    <Icon name="list-checks" size={28} />
                                </div>
                                <h2 className="text-2xl font-black text-slate-800">개념 정교화 퀴즈</h2>
                            </div>
                            
                            <div className="p-8 bg-slate-50 rounded-[32px] border border-slate-100 relative group">
                                <div className="absolute -top-4 -right-4 bg-amber-400 text-white p-3 rounded-2xl rotate-12 shadow-lg group-hover:rotate-0 transition-all">
                                    <Icon name="help-circle" size={24} />
                                </div>
                                <h3 className="font-bold text-xl mb-8 leading-relaxed text-slate-800 pr-8">
                                    Q. 타원 궤도를 따라 태양 주위를 도는 행성의 운동에 대한 설명 중 <span className="text-red-600 underline decoration-4 underline-offset-4 font-black">옳지 않은</span> 것은?
                                </h3>
                                
                                <div className="space-y-4">
                                    {[
                                        "행성이 태양과 가장 가까운 지점(근일점)에서 속력이 가장 빠르다.",
                                        "행성의 공전 궤도 장반경의 세제곱은 공전 주기의 제곱에 비례한다.",
                                        "태양과 행성을 잇는 선분이 같은 시간 동안 훑고 지나가는 면적은 항상 일정하다.",
                                        "행성이 타원 궤도를 도는 동안 태양으로부터 받는 중력의 크기는 어디서나 같다."
                                    ].map((option, idx) => (
                                        <button
                                            key={idx}
                                            onClick={() => checkAnswer(idx)}
                                            disabled={showFeedback}
                                            className={`w-full p-5 text-left rounded-2xl border-2 transition-all font-bold flex items-center justify-between text-[15px] ${
                                                quizAnswer === idx 
                                                    ? (idx === 3 ? 'border-emerald-500 bg-emerald-50 text-emerald-700' : 'border-red-500 bg-red-50 text-red-700 shadow-inner')
                                                    : 'border-white bg-white hover:border-blue-300 shadow-sm hover:translate-x-1'
                                            }`}
                                        >
                                            <span className="flex gap-4">
                                                <span className={`w-6 h-6 rounded-lg flex items-center justify-center text-xs shrink-0 ${quizAnswer === idx ? 'bg-white/20' : 'bg-slate-100 text-slate-400'}`}>{idx + 1}</span>
                                                {option}
                                            </span>
                                            {showFeedback && idx === 3 && <Icon name="check-circle" className="text-emerald-500 shrink-0" size={20} />}
                                            {showFeedback && idx !== 3 && quizAnswer === idx && <Icon name="x-circle" className="text-red-500 shrink-0" size={20} />}
                                        </button>
                                    ))}
                                </div>

                                {showFeedback && (
                                    <div className={`mt-10 p-8 rounded-3xl animate-in slide-in-from-top-4 duration-500 border-2 ${
                                        quizAnswer === 3 ? 'bg-emerald-600 text-white border-emerald-400 shadow-xl shadow-emerald-100 text-center' : 'bg-slate-900 text-white border-slate-700'
                                    }`}>
                                        <div className="flex flex-col items-center gap-3 mb-4">
                                            <div className={`w-12 h-12 rounded-full flex items-center justify-center ${quizAnswer === 3 ? 'bg-emerald-500' : 'bg-rose-500'}`}>
                                                <Icon name={quizAnswer === 3 ? "thumbs-up" : "alert-triangle"} size={28} />
                                            </div>
                                            <p className="font-black text-2xl">
                                                {quizAnswer === 3 ? '정확한 개념입니다! 🎉' : '다시 한번 관찰해 보세요! 🧐'}
                                            </p>
                                        </div>
                                        <p className="text-[15px] opacity-95 leading-relaxed text-left p-6 bg-black/10 rounded-2xl">
                                            <strong>[해설]</strong> 만유인력(중력)의 크기 $F = G \cdot \frac{Mm}{r^2}$ 입니다. 타원 궤도에서는 행성과 태양 사이의 거리($r$)가 위치에 따라 계속 변하기 때문에, 행성이 받는 중계의 크기 역시 위치에 따라 항상 달라집니다. 이 변화무쌍한 중력이 행성의 속력을 변화시키는 근본 원인입니다.
                                        </p>
                                        <button 
                                            onClick={() => {setShowFeedback(false); setQuizAnswer(null);}}
                                            className="mt-6 px-10 py-3 bg-white/20 rounded-xl text-sm font-black hover:bg-white/30 transition-all active:scale-95"
                                        >
                                            다시 도전하기
                                        </button>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pb-12">
                            {[
                                { title: '제1법칙', desc: '타원 궤도 법칙' },
                                { title: '제2법칙', desc: '면적 속도 일정 법칙' },
                                { title: '제3법칙', desc: '조화의 법칙' }
                            ].map((item, i) => (
                                <div key={i} className="bg-white p-4 rounded-2xl border border-slate-100 text-center shadow-sm">
                                    <p className="text-xs font-black text-blue-600 mb-1">{item.title}</p>
                                    <p className="text-[13px] font-bold text-slate-500">{item.desc}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerPractice />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=900, scrolling=False)

if __name__ == "__main__":
    run_sim()
