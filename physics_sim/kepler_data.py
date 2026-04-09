import streamlit as st
import streamlit.components.v1 as components

def run_sim():
    st.set_page_config(page_title="케플러 제3법칙: 조화의 법칙 데이터 분석", layout="wide")
    
    st.title("📊 케플러 제3법칙: 공전 주기와 궤도 반지름의 관계")
    st.markdown("""
    실제 태양계 행성들의 데이터를 통해 **조화의 법칙($T^2 \propto a^3$)**이 성립함을 수학적으로 확인합니다. 
    행성의 공전 궤도 장반경($a$)의 세제곱과 공전 주기($T$)의 제곱이 그리는 비례 관계를 그래프로 탐구해 보세요.
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
        <script src="https://unpkg.com/recharts/umd/Recharts.js"></script>
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
            const { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } = Recharts;

            const Icon = ({ name, size = 18, className = "" }) => {
                useEffect(() => {
                    if (window.lucide) {
                        window.lucide.createIcons();
                    }
                }, [name]);
                return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
            };

            const KeplerData = () => {
                const planetData = [
                    { name: '수성', r: 0.39, t: 0.24, r3: 0.059, t2: 0.058 },
                    { name: '금성', r: 0.72, t: 0.62, r3: 0.373, t2: 0.384 },
                    { name: '지구', r: 1.00, t: 1.00, r3: 1.000, t2: 1.000 },
                    { name: '화성', r: 1.52, t: 1.88, r3: 3.512, t2: 3.534 },
                    { name: '목성', r: 5.20, t: 11.86, r3: 140.6, t2: 140.7 }
                ];

                return (
                    <div className="max-w-6xl mx-auto p-4 flex flex-col gap-8">
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                            <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-xl space-y-6">
                                <h3 className="text-xl font-black text-slate-800 flex items-center gap-2">
                                    <Icon name="bar-chart-3" className="text-blue-600" /> 데이터 시각화 (T² vs r³)
                                </h3>
                                <div className="h-80 w-full bg-slate-50 p-4 rounded-2xl border border-slate-100">
                                    <ResponsiveContainer width="100%" height="100%">
                                        <ScatterChart margin={{ top: 20, right: 30, bottom: 40, left: 40 }}>
                                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                            <XAxis 
                                                type="number" 
                                                dataKey="r3" 
                                                name="r³" 
                                                label={{ value: 'r³ (AU³)', position: 'insideBottom', offset: -25, fontSize: 12, fontWeight: 'bold' }} 
                                            />
                                            <YAxis 
                                                type="number" 
                                                dataKey="t2" 
                                                name="T²" 
                                                label={{ value: 'T² (yr²)', angle: -90, position: 'insideLeft', offset: -15, fontSize: 12, fontWeight: 'bold' }} 
                                            />
                                            <Tooltip cursor={{ strokeDasharray: '3 3' }} content={({ payload }) => {
                                                if (payload && payload[0]) {
                                                    const data = payload[0].payload;
                                                    return (
                                                        <div className="bg-slate-900 text-white p-4 border border-slate-700 shadow-2xl rounded-2xl animate-in fade-in zoom-in-95">
                                                            <p className="font-black text-blue-400 text-base mb-1">{data.name}</p>
                                                            <div className="text-[11px] text-slate-400 space-y-0.5">
                                                                <p>r³ = {data.r3.toFixed(3)} AU³</p>
                                                                <p>T² = {data.t2.toFixed(3)} yr²</p>
                                                            </div>
                                                        </div>
                                                    );
                                                }
                                                return null;
                                            }} />
                                            <Scatter name="Planets" data={planetData}>
                                                {planetData.map((entry, index) => (
                                                    <Cell key={`cell-${index}`} fill={index === 2 ? '#ef4444' : '#3b82f6'} />
                                                ))}
                                            </Scatter>
                                        </ScatterChart>
                                    </ResponsiveContainer>
                                </div>
                                <div className="p-5 bg-blue-50 rounded-2xl border-l-4 border-blue-500">
                                    <h4 className="font-bold text-slate-800 mb-2 underline underline-offset-4 flex items-center gap-2">
                                        <Icon name="lightbulb" size={16} /> 탐구 포인트
                                    </h4>
                                    <p className="text-[13px] text-slate-600 leading-relaxed">
                                        기울기가 정확히 <strong>1</strong>인 직선이 나타나는 것을 통해, 거리의 세제곱과 주기의 제곱이 비례함을 알 수 있습니다.
                                    </p>
                                </div>
                            </div>

                            <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-xl">
                                <h3 className="text-xl font-black text-slate-800 mb-6 flex items-center gap-2">
                                    <Icon name="table" className="text-amber-600" /> 수치 데이터 테이블
                                </h3>
                                <div className="overflow-x-auto rounded-2xl border border-slate-100 mb-6">
                                    <table className="w-full text-xs text-left border-collapse">
                                        <thead>
                                            <tr className="bg-slate-50 text-slate-500 border-b border-slate-100 uppercase tracking-tighter">
                                                <th className="p-4 font-black">행성</th>
                                                <th className="p-4 font-black">r (AU)</th>
                                                <th className="p-4 font-black">T (yr)</th>
                                                <th className="p-4 font-black">r³ (AU³)</th>
                                                <th className="p-4 font-black">T² (yr²)</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {planetData.map((p) => (
                                                <tr key={p.name} className="hover:bg-slate-50 border-b border-slate-50 transition-colors">
                                                    <td className="p-4 font-bold text-slate-800">{p.name}</td>
                                                    <td className="p-4 font-mono">{p.r}</td>
                                                    <td className="p-4 font-mono">{p.t}</td>
                                                    <td className="p-4 font-mono bg-blue-50/50 font-bold text-blue-700">{p.r3.toFixed(3)}</td>
                                                    <td className="p-4 font-mono bg-amber-50/50 font-bold text-amber-700">{p.t2.toFixed(3)}</td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                                <div className="bg-slate-900 p-6 rounded-2xl text-white">
                                    <div className="flex items-center gap-2 text-amber-400 mb-3 text-xs font-black">
                                        <Icon name="calculator" size={16} /> 이론적 배경
                                    </div>
                                    <div className="font-mono text-[14px] p-4 bg-white/5 rounded-xl border border-white/10 text-center mb-4">
                                        T² / r³ = K (일정)
                                    </div>
                                    <p className="text-[11px] text-slate-400 leading-relaxed italic">
                                        여기서 K 값은 중심 천체의 질량에 의존하며, 태양계 행성들에 대해서는 이 비가 모두 소수점 셋째 자리까지 일치합니다.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                );
            };

            const root = ReactDOM.createRoot(document.getElementById('root'));
            root.render(<KeplerData />);
        </script>
    </body>
    </html>
    """
    components.html(react_code, height=750, scrolling=False)

if __name__ == "__main__":
    run_sim()
