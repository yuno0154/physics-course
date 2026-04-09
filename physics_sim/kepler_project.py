import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="화성 탐사선 '다누리 2호' 궤도 설계 프로젝트", layout="wide")
    
    st.title("🚀 프로젝트: 화성 탐사선 '다누리 2호' 궤도 설계")
    st.markdown("""
    대한민국 우주항공청(KASA) 연구원이 되어 화성 관측을 위한 최적의 타원 궤도를 설계하고 물리학적으로 입증하는 수행평가 프로젝트입니다.
    **GRASPS 전략**에 따라 미션을 수행하고 탐구 보고서를 작성해 보세요.
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
            const { useEffect } = React;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerProject = () => {
                return (
                    <div className="max-w-5xl mx-auto p-4">
                        <div className="bg-white rounded-[40px] overflow-hidden border border-slate-200 shadow-2xl">
                            <div className="bg-gradient-to-br from-indigo-700 via-blue-800 to-slate-900 p-12 text-white relative">
                                <div className="absolute top-0 right-0 w-64 h-64 bg-blue-400/10 rounded-full blur-3xl"></div>
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="p-2 bg-white/10 rounded-xl backdrop-blur-md">
                                        <Icon name="lightbulb" size={24} className="text-amber-400" />
                                    </div>
                                    <span className="text-blue-200 font-black uppercase tracking-[0.3em] text-xs">Performance Assessment (GRASPS)</span>
                                </div>
                                <h2 className="text-4xl font-black mb-4 leading-tight">화성 탐사선 '다누리 2호'<br/>궤도 설계 및 주기 분석</h2>
                                <p className="text-blue-100 opacity-80 text-base max-w-2xl leading-relaxed">
                                    화성 표면 정밀 관측과 전역 통신망 확보라는 두 가지 목표를 달성하기 위해 가장 효율적인 타원 궤도를 설계하고, 케플러 법칙을 적용하여 궤도의 타당성을 증명하십시오.
                                </p>
                            </div>
                            
                            <div className="p-12 grid grid-cols-1 md:grid-cols-2 gap-12 items-start bg-white">
                                <div className="space-y-10">
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-blue-100 group-hover:scale-110 transition-transform">G</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Goal (목표)</h4>
                                            <p className="text-[14px] text-slate-500 leading-relaxed font-medium">최소 연료로 운용 가능한 안정적인 타원 궤도를 설계하고 공전 주기를 계산하여 이론적 정확성을 입증함.</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-indigo-100 group-hover:scale-110 transition-transform">R</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Role (역할)</h4>
                                            <p className="text-[14px] text-slate-500 leading-relaxed font-medium">대한민국 우주항공청(KASA) 소속 궤도역학 전문 수석 연구원</p>
                                        </div>
                                    </div>
                                    <div className="flex gap-6 group">
                                        <div className="flex-shrink-0 w-16 h-16 bg-slate-50 text-slate-600 rounded-2xl flex items-center justify-center font-black text-2xl shadow-sm border border-slate-100 group-hover:scale-110 transition-transform">S</div>
                                        <div>
                                            <h4 className="font-black text-slate-800 text-lg mb-1">Standards (평가 기준)</h4>
                                            <ul className="text-[13px] text-slate-500 list-disc list-inside space-y-2 mt-2 font-bold marker:text-blue-500">
                                                <li>제3법칙을 활용한 주기 계산의 수치적 정확성</li>
                                                <li>이심률에 따른 속력 변화의 물리학적 인과관계</li>
                                                <li>설계 궤도의 효율성에 대한 논리적 타당성</li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <div className="space-y-8 bg-slate-50 p-8 rounded-[40px] border-4 border-dashed border-slate-200 relative overflow-hidden">
                                    <h4 className="font-black text-slate-700 flex items-center gap-2 text-sm uppercase tracking-widest mb-2">
                                        <Icon name="rocket" className="text-blue-600" /> Mission Briefing
                                    </h4>
                                    <div className="text-[14px] text-slate-600 font-bold space-y-6 leading-relaxed">
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">01</span>
                                            <p><strong className="text-blue-700">궤도 조작:</strong> 시뮬레이터를 활용해 최적의 이심률을 도출하고, 근일점과 원일점의 비율을 설정하십시오.</p>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">02</span>
                                            <p><strong className="text-emerald-700">물리 검증:</strong> 화성의 관측 목적(고해상도 촬영 vs 광범위 통신)에 따른 궤도의 장단점을 서술하십시오.</p>
                                        </div>
                                        <div className="flex gap-4">
                                            <span className="w-6 h-6 bg-slate-200 rounded text-[10px] flex items-center justify-center shrink-0">03</span>
                                            <p><strong className="text-amber-700">수식 도출:</strong> 뉴턴의 중력 법칙에서 케플러 제3법칙이 유도되는 과정을 보고서에 포함하십시오.</p>
                                        </div>
                                    </div>
                                    <div className="pt-6">
                                        <button className="w-full py-5 bg-blue-600 text-white rounded-2xl text-base font-black hover:bg-blue-700 shadow-xl shadow-blue-200 transition-all active:scale-95 flex items-center justify-center gap-3 group">
                                            <Icon name="file-text" className="group-hover:translate-y-[-2px] transition-transform" />
                                            연구 보고서 양식 다운로드
                                        </button>
                                        <p className="text-center text-[10px] text-slate-400 mt-4 font-bold tracking-tight">
                                            * 제출 기한: 2026학년도 1학기 지필고시 전까지
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerProject />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=850, scrolling=False)

if __name__ == "__main__":
    run_sim()
