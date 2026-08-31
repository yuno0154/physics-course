import streamlit as st
import streamlit.components.v1 as components

st.title("🏀 비스듬히 던진 물체의 운동")
st.markdown("""
포물선 운동의 수평 성분과 연직 성분을 분리하여 속도와 가속도의 변화를 실시간으로 분석합니다. 
시뮬레이션을 재생하거나 슬라이더를 움직이며 **세 위치(A: 상승 중, B: 최고점, C: 하강 중)**를 직접 찍고, 활동지 데이터 표를 완성해 보세요!
""")

react_code = r"""
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
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;500;600;700;800&display=swap');
        body { font-family: 'Pretendard', sans-serif; margin: 0; padding: 0; background: transparent; color: #1e293b; }
        .tab-active { background-color: #3b82f6; color: white; }
        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 18px;
            width: 18px;
            border-radius: 50%;
            background: #2563eb;
            cursor: pointer;
            border: 2px solid white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body class="bg-slate-50 p-2 md:p-4">
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useEffect, useRef, useMemo, useCallback } = React;

        const Icon = ({ name, size = 18, className = "" }) => {
            useEffect(() => {
                if (window.lucide) window.lucide.createIcons();
            }, [name]);
            return <i data-lucide={name} style={{ width: size, height: size }} className={className}></i>;
        };

        const ObliqueProjectileSim = () => {
            // 발사 조건 파라미터
            const [v0, setV0] = useState(20.0);
            const [thetaDeg, setThetaDeg] = useState(45);
            const [g, setG] = useState(9.8);
            
            // 시뮬레이션 제어
            const [currentTime, setCurrentTime] = useState(0.0);
            const [isPlaying, setIsPlaying] = useState(false);
            const [playSpeed, setPlaySpeed] = useState(1.0);

            // 벡터 시각화 설정 (초기값: 모두 꺼짐)
            const [showVelComponents, setShowVelComponents] = useState(false);
            const [showVelComposite, setShowVelComposite] = useState(false);
            const [showAccelVector, setShowAccelVector] = useState(false);
            const [showTrajectory, setShowTrajectory] = useState(true);

            // 3개 지점 선택 (A: 상승 중, B: 최고점, C: 하강 중)
            const [pointA, setPointA] = useState(null); // { t, x, y, vx, vy, ax, ay, v }
            const [pointB, setPointB] = useState(null);
            const [pointC, setPointC] = useState(null);
            const [activeSlot, setActiveSlot] = useState('A'); // 현재 찍을 슬롯: 'A' | 'B' | 'C'

            // 탐구 결론 숨김/펼침 상태 (기본값: 숨김)
            const [showConclusion, setShowConclusion] = useState(false);

            const canvasRef = useRef(null);
            const animRef = useRef(null);
            const lastTimeRef = useRef(null);

            // 물리 계산
            const theta = (thetaDeg * Math.PI) / 180;
            const vx0 = v0 * Math.cos(theta);
            const vy0 = v0 * Math.sin(theta);
            const t_H = vy0 / g; // 최고점 도달 시간
            const H = (vy0 * vy0) / (2 * g); // 최고점 높이
            const t_R = 2 * t_H; // 지면 도달 시간
            const R = vx0 * t_R; // 수평 도달 거리

            // 임의의 시각 t에서의 물리 상태 계산 함수
            const getStateAtTime = useCallback((t) => {
                const clampedT = Math.max(0, Math.min(t, t_R));
                const x = vx0 * clampedT;
                const y = Math.max(0, vy0 * clampedT - 0.5 * g * clampedT * clampedT);
                const vx = vx0;
                const vy = vy0 - g * clampedT;
                const v = Math.sqrt(vx * vx + vy * vy);
                const ax = 0.0;
                const ay = -g;
                return { t: clampedT, x, y, vx, vy, v, ax, ay };
            }, [vx0, vy0, g, t_R]);

            // 파라미터 변경 시 기본 최고점(B) 자동 초기화
            useEffect(() => {
                const bState = getStateAtTime(t_H);
                setPointB(bState);
                
                // 기본 A (상승 50%), C (하강 50%) 기본값 설정
                setPointA(getStateAtTime(t_H * 0.5));
                setPointC(getStateAtTime(t_H + (t_R - t_H) * 0.5));
                setCurrentTime(0.0);
                setIsPlaying(false);
            }, [v0, thetaDeg, g]);

            // 실시간 애니메이션 루프 (60 FPS)
            useEffect(() => {
                if (isPlaying) {
                    lastTimeRef.current = performance.now();
                    const loop = (now) => {
                        const dt = (now - lastTimeRef.current) / 1000.0;
                        lastTimeRef.current = now;

                        setCurrentTime((prev) => {
                            const next = prev + dt * playSpeed;
                            if (next >= t_R) {
                                setIsPlaying(false);
                                return t_R;
                            }
                            return next;
                        });

                        animRef.current = requestAnimationFrame(loop);
                    };
                    animRef.current = requestAnimationFrame(loop);
                } else {
                    if (animRef.current) cancelAnimationFrame(animRef.current);
                }
                return () => {
                    if (animRef.current) cancelAnimationFrame(animRef.current);
                };
            }, [isPlaying, playSpeed, t_R]);

            // 현재 시점의 물리량
            const currentState = useMemo(() => getStateAtTime(currentTime), [currentTime, getStateAtTime]);

            // 지점 기록 핸들러
            const captureCurrentAs = (slot) => {
                if (slot === 'A') {
                    setPointA(currentState);
                    setActiveSlot('B');
                } else if (slot === 'B') {
                    // 최고점은 정확한 t_H 상태로 기록
                    setPointB(getStateAtTime(t_H));
                    setActiveSlot('C');
                } else if (slot === 'C') {
                    setPointC(currentState);
                    setActiveSlot('A');
                }
            };

            // 캔버스 클릭 시 가장 가까운 궤적 상의 점 포착
            const handleCanvasClick = (e) => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                const rect = canvas.getBoundingClientRect();
                const clickCanvasX = e.clientX - rect.left;
                const clickCanvasY = e.clientY - rect.top;

                // 마진 및 스케일 정보 계산
                const margin = { left: 65, right: 35, top: 40, bottom: 50 };
                const plotW = canvas.width - margin.left - margin.right;
                const plotH = canvas.height - margin.top - margin.bottom;

                const maxX = Math.max(R * 1.15, 20);
                const maxY = Math.max(H * 1.35, 12);
                const scaleX = plotW / maxX;
                const scaleY = plotH / maxY;
                const scale = Math.min(scaleX, scaleY);

                const worldClickX = (clickCanvasX - margin.left) / scale;
                if (worldClickX >= 0 && worldClickX <= R) {
                    const clickT = worldClickX / vx0;
                    const st = getStateAtTime(clickT);
                    setCurrentTime(clickT);

                    if (activeSlot === 'A' || clickT < t_H * 0.8) {
                        setPointA(st);
                        setActiveSlot('B');
                    } else if (activeSlot === 'B' || (clickT >= t_H * 0.8 && clickT <= t_H * 1.2)) {
                        setPointB(getStateAtTime(t_H));
                        setActiveSlot('C');
                    } else {
                        setPointC(st);
                        setActiveSlot('A');
                    }
                }
            };

            // 화살표 그리기 헬퍼
            const drawArrow = (ctx, fromX, fromY, toX, toY, color, width = 2.5, headLength = 10) => {
                const dx = toX - fromX;
                const dy = toY - fromY;
                const angle = Math.atan2(dy, dx);
                const length = Math.sqrt(dx * dx + dy * dy);
                if (length < 2) return;

                ctx.save();
                ctx.strokeStyle = color;
                ctx.fillStyle = color;
                ctx.lineWidth = width;

                // 선분
                ctx.beginPath();
                ctx.moveTo(fromX, fromY);
                ctx.lineTo(toX, toY);
                ctx.stroke();

                // 화살표 머리
                ctx.beginPath();
                ctx.moveTo(toX, toY);
                ctx.lineTo(toX - headLength * Math.cos(angle - Math.PI / 6), toY - headLength * Math.sin(angle - Math.PI / 6));
                ctx.lineTo(toX - headLength * Math.cos(angle + Math.PI / 6), toY - headLength * Math.sin(angle + Math.PI / 6));
                ctx.closePath();
                ctx.fill();
                ctx.restore();
            };

            // 캔버스 렌더링
            useEffect(() => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                const ctx = canvas.getContext('2d');
                const width = canvas.width;
                const height = canvas.height;

                ctx.clearRect(0, 0, width, height);

                const margin = { left: 65, right: 35, top: 40, bottom: 50 };
                const plotW = width - margin.left - margin.right;
                const plotH = height - margin.top - margin.bottom;

                const maxX = Math.max(R * 1.15, 20);
                const maxY = Math.max(H * 1.35, 12);
                const scaleX = plotW / maxX;
                const scaleY = plotH / maxY;
                const scale = Math.min(scaleX, scaleY);

                const toCanvasX = (wx) => margin.left + wx * scale;
                const toCanvasY = (wy) => height - margin.bottom - wy * scale;

                // 1. 격자 및 배경
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 1;

                // X축 그리드 (5m 또는 10m 단위)
                const gridStepX = maxX > 60 ? 10 : (maxX > 30 ? 5 : 2);
                for (let gx = 0; gx <= maxX; gx += gridStepX) {
                    const cx = toCanvasX(gx);
                    ctx.beginPath();
                    ctx.moveTo(cx, margin.top);
                    ctx.lineTo(cx, height - margin.bottom);
                    ctx.stroke();

                    // 라벨
                    ctx.fillStyle = '#64748b';
                    ctx.font = '11px Pretendard';
                    ctx.textAlign = 'center';
                    ctx.fillText(`${gx}`, cx, height - margin.bottom + 18);
                }

                // Y축 그리드
                const gridStepY = maxY > 40 ? 10 : (maxY > 20 ? 5 : 2);
                for (let gy = 0; gy <= maxY; gy += gridStepY) {
                    const cy = toCanvasY(gy);
                    ctx.beginPath();
                    ctx.moveTo(margin.left, cy);
                    ctx.lineTo(margin.left + plotW, cy);
                    ctx.stroke();

                    // 라벨
                    ctx.fillStyle = '#64748b';
                    ctx.font = '11px Pretendard';
                    ctx.textAlign = 'right';
                    ctx.fillText(`${gy}`, margin.left - 10, cy + 4);
                }

                // 축 라벨
                ctx.fillStyle = '#1e293b';
                ctx.font = 'bold 12px Pretendard';
                ctx.textAlign = 'center';
                ctx.fillText('수평 거리 x (m)', margin.left + plotW / 2, height - 12);

                ctx.save();
                ctx.translate(16, margin.top + plotH / 2);
                ctx.rotate(-Math.PI / 2);
                ctx.textAlign = 'center';
                ctx.fillText('높이 y (m)', 0, 0);
                ctx.restore();

                // 2. 바닥선
                ctx.strokeStyle = '#94a3b8';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(margin.left, height - margin.bottom);
                ctx.lineTo(margin.left + plotW, height - margin.bottom);
                ctx.stroke();

                // 3. 전체 포물선 궤적
                if (showTrajectory) {
                    ctx.strokeStyle = '#93c5fd';
                    ctx.lineWidth = 2;
                    ctx.setLineDash([4, 4]);
                    ctx.beginPath();
                    for (let step = 0; step <= 80; step++) {
                        const st_t = (t_R * step) / 80;
                        const px = vx0 * st_t;
                        const py = Math.max(0, vy0 * st_t - 0.5 * g * st_t * st_t);
                        if (step === 0) ctx.moveTo(toCanvasX(px), toCanvasY(py));
                        else ctx.lineTo(toCanvasX(px), toCanvasY(py));
                    }
                    ctx.stroke();
                    ctx.setLineDash([]);
                }

                // 4. 현재까지 진행된 궤적 (진한 파란 실선)
                ctx.strokeStyle = '#2563eb';
                ctx.lineWidth = 3;
                ctx.beginPath();
                const currentSteps = Math.max(2, Math.floor((currentTime / t_R) * 80));
                for (let step = 0; step <= currentSteps; step++) {
                    const st_t = Math.min(currentTime, (t_R * step) / 80);
                    const px = vx0 * st_t;
                    const py = Math.max(0, vy0 * st_t - 0.5 * g * st_t * st_t);
                    if (step === 0) ctx.moveTo(toCanvasX(px), toCanvasY(py));
                    else ctx.lineTo(toCanvasX(px), toCanvasY(py));
                }
                ctx.stroke();

                // 5. 최고점(Apex) 랜드마크 & 도달거리 랜드마크
                const apexCanvasX = toCanvasX(vx0 * t_H);
                const apexCanvasY = toCanvasY(H);
                ctx.fillStyle = '#dc2626';
                ctx.font = 'bold 11px Pretendard';
                ctx.textAlign = 'center';
                ctx.fillText(`★ 최고점 H=${H.toFixed(2)}m`, apexCanvasX, apexCanvasY - 14);

                const landCanvasX = toCanvasX(R);
                const landCanvasY = toCanvasY(0);
                ctx.fillStyle = '#475569';
                ctx.fillText(`도달 거리 R=${R.toFixed(2)}m`, landCanvasX, landCanvasY - 10);

                // 6. 관찰 지점(A, B, C) 핀 마커 표시
                const renderPointBadge = (pt, label, bgColor, textColor, borderColor) => {
                    if (!pt) return;
                    const px = toCanvasX(pt.x);
                    const py = toCanvasY(pt.y);

                    // 핀 원형
                    ctx.fillStyle = bgColor;
                    ctx.strokeStyle = borderColor;
                    ctx.lineWidth = 2.5;
                    ctx.beginPath();
                    ctx.arc(px, py, 7, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.stroke();

                    // 라벨 박스
                    ctx.fillStyle = bgColor;
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1;
                    const tagW = 74;
                    const tagH = 20;
                    const tagX = px - tagW / 2;
                    const tagY = py - 30;

                    ctx.beginPath();
                    ctx.roundRect ? ctx.roundRect(tagX, tagY, tagW, tagH, 5) : ctx.rect(tagX, tagY, tagW, tagH);
                    ctx.fill();
                    ctx.stroke();

                    ctx.fillStyle = textColor;
                    ctx.font = 'bold 10px Pretendard';
                    ctx.textAlign = 'center';
                    ctx.fillText(`${label} (${pt.t.toFixed(2)}s)`, px, tagY + 14);

                    // A, B, C 지점 속도/가속도 벡터 표시 (옵션 켜짐 시)
                    const vScale = 1.2;
                    if (showVelComponents) {
                        drawArrow(ctx, px, py, px + pt.vx * vScale, py, '#16a34a', 2, 7);
                        drawArrow(ctx, px, py, px, py - pt.vy * vScale, '#dc2626', 2, 7);
                    }
                    if (showAccelVector) {
                        drawArrow(ctx, px, py, px, py + g * 1.5, '#ea580c', 2.5, 8);
                    }
                };

                renderPointBadge(pointA, 'A (상승)', '#2563eb', '#ffffff', '#ffffff');
                renderPointBadge(pointB, 'B (최고점)', '#dc2626', '#ffffff', '#ffffff');
                renderPointBadge(pointC, 'C (하강)', '#16a34a', '#ffffff', '#ffffff');

                // 7. 현재 이동 중인 발사체(Ball) & 실시간 벡터
                const curCanvasX = toCanvasX(currentState.x);
                const curCanvasY = toCanvasY(currentState.y);

                // 속도 벡터 (vx: 초록, vy: 빨강)
                const vScale = 1.5;
                if (showVelComponents) {
                    // vx 수평 화살표 (초록색)
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX + currentState.vx * vScale, curCanvasY, '#16a34a', 3, 10);
                    // vy 연직 화살표 (빨간색) - Y축 반전 주의 (Canvas Y는 아래로 증가)
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX, curCanvasY - currentState.vy * vScale, '#dc2626', 3, 10);
                }

                // 합성 속도 v (보라색 화살표)
                if (showVelComposite) {
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX + currentState.vx * vScale, curCanvasY - currentState.vy * vScale, '#8b5cf6', 3.5, 11);
                }

                // 가속도 벡터 (중력 가속도 아래 방향 주황색)
                if (showAccelVector) {
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX, curCanvasY + g * 2.0, '#ea580c', 4, 12);
                }

                // 발사체 본체 (공)
                ctx.fillStyle = '#f97316';
                ctx.strokeStyle = '#1e293b';
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                ctx.arc(curCanvasX, curCanvasY, 9, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // 중심 하이라이트
                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(curCanvasX - 2, curCanvasY - 2, 3, 0, Math.PI * 2);
                ctx.fill();

            }, [currentState, pointA, pointB, pointC, showVelComponents, showVelComposite, showAccelVector, showTrajectory, R, H, t_H, t_R, vx0, vy0, g]);

            return (
                <div className="max-w-5xl mx-auto space-y-4">
                    {/* 발사 조건 및 시각화 컨트롤 바 */}
                    <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3 mb-3">
                            <div className="flex items-center gap-2">
                                <span className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                                    <Icon name="sliders" size={20} />
                                </span>
                                <h3 className="font-bold text-slate-800 text-base">발사 조건 & 시각화 설정</h3>
                            </div>

                            <div className="flex items-center gap-2">
                                <button 
                                    onClick={() => setShowVelComponents(prev => !prev)}
                                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 border ${
                                        showVelComponents ? 'bg-emerald-50 text-emerald-600 border-emerald-300 shadow-sm' : 'bg-slate-100 text-slate-600 border-slate-200'
                                    }`}
                                >
                                    <Icon name="arrow-up-right" size={14} />
                                    속도 성분 (vx, vy)
                                </button>

                                <button 
                                    onClick={() => setShowVelComposite(prev => !prev)}
                                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 border ${
                                        showVelComposite ? 'bg-purple-50 text-purple-600 border-purple-300 shadow-sm' : 'bg-slate-100 text-slate-600 border-slate-200'
                                    }`}
                                >
                                    <Icon name="zap" size={14} />
                                    합성 속도 (v)
                                </button>

                                <button 
                                    onClick={() => setShowAccelVector(prev => !prev)}
                                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 border ${
                                        showAccelVector ? 'bg-orange-50 text-orange-600 border-orange-300 shadow-sm' : 'bg-slate-100 text-slate-600 border-slate-200'
                                    }`}
                                >
                                    <Icon name="arrow-down" size={14} />
                                    가속도 (ay = -g)
                                </button>
                            </div>
                        </div>

                        {/* 입력 슬라이더 */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                                    <span>초기 속도 v₀</span>
                                    <span className="text-blue-600 font-bold text-sm">{v0.toFixed(1)} m/s</span>
                                </div>
                                <input 
                                    type="range" min="5" max="50" step="1" 
                                    value={v0} onChange={(e) => setV0(parseFloat(e.target.value))}
                                    className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
                                />
                            </div>

                            <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                                    <span>발사 각도 θ</span>
                                    <span className="text-blue-600 font-bold text-sm">{thetaDeg}°</span>
                                </div>
                                <input 
                                    type="range" min="10" max="85" step="1" 
                                    value={thetaDeg} onChange={(e) => setThetaDeg(parseInt(e.target.value))}
                                    className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
                                />
                            </div>

                            <div className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                                <div className="flex justify-between text-xs font-semibold text-slate-600 mb-1">
                                    <span>중력 가속도 g</span>
                                    <span className="text-blue-600 font-bold text-sm">{g.toFixed(1)} m/s²</span>
                                </div>
                                <div className="flex gap-2 mt-1">
                                    <button 
                                        onClick={() => setG(9.8)}
                                        className={`flex-1 py-1 rounded-lg text-xs font-bold transition-all ${g === 9.8 ? 'bg-blue-600 text-white shadow-sm' : 'bg-white text-slate-600 border border-slate-200'}`}
                                    >
                                        9.8 m/s² (지구)
                                    </button>
                                    <button 
                                        onClick={() => setG(10.0)}
                                        className={`flex-1 py-1 rounded-lg text-xs font-bold transition-all ${g === 10.0 ? 'bg-blue-600 text-white shadow-sm' : 'bg-white text-slate-600 border border-slate-200'}`}
                                    >
                                        10.0 m/s² (간편 계산)
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* 메인 캔버스 뷰 & 오버레이 실시간 텔레메트리 */}
                    <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-200 relative">
                        {/* 상단 캔버스 안내 및 실시간 텔레메트리 HUD */}
                        <div className="absolute top-6 left-6 bg-white/90 backdrop-blur-sm p-3 rounded-xl border border-slate-200 shadow-md pointer-events-none z-10 text-xs font-mono space-y-1">
                            <div className="font-bold text-slate-800 font-sans flex items-center gap-1.5 text-xs pb-1 border-b border-slate-200">
                                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                실시간 운동 데이터
                            </div>
                            <div className="text-slate-600">시간 (t): <b className="text-blue-600">{currentState.t.toFixed(2)} s</b></div>
                            <div className="text-slate-600">위치 (x, y): <b className="text-slate-800">({currentState.x.toFixed(2)}, {currentState.y.toFixed(2)}) m</b></div>
                            <div className="text-emerald-700">수평속도 (vx): <b>+{currentState.vx.toFixed(2)} m/s</b></div>
                            <div className={currentState.vy >= 0 ? "text-rose-600" : "text-blue-600"}>
                                연직속도 (vy): <b>{currentState.vy >= 0 ? `+${currentState.vy.toFixed(2)}` : currentState.vy.toFixed(2)} m/s</b>
                            </div>
                            <div className="text-purple-700">합성속도 (v): <b>{currentState.v.toFixed(2)} m/s</b></div>
                            <div className="text-amber-700 font-sans border-t border-slate-100 pt-1">
                                수평 가속도 (ax): <b>0.00 m/s²</b>
                            </div>
                            <div className="text-orange-600 font-sans">
                                연직 가속도 (ay): <b>-{g.toFixed(2)} m/s² (아래)</b>
                            </div>
                        </div>

                        {/* 캔버스 */}
                        <canvas 
                            ref={canvasRef} 
                            width={920} 
                            height={480}
                            onClick={handleCanvasClick}
                            className="w-full h-auto bg-slate-50/50 rounded-xl cursor-crosshair border border-slate-100"
                        />
                        <div className="text-right text-[11px] text-slate-400 mt-1">
                            💡 궤적 위를 직접 클릭하면 해당 위치로 이동하며 선택된 슬롯(A, B, C)에 기록됩니다.
                        </div>

                        {/* 재생 컨트롤 및 타임라인 슬라이더 */}
                        <div className="mt-4 pt-3 border-t border-slate-100 space-y-3">
                            <div className="flex items-center gap-3">
                                <button 
                                    onClick={() => {
                                        if (currentTime >= t_R) setCurrentTime(0);
                                        setIsPlaying(!isPlaying);
                                    }}
                                    className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm ${
                                        isPlaying ? 'bg-amber-500 text-white' : 'bg-blue-600 text-white'
                                    }`}
                                >
                                    <Icon name={isPlaying ? "pause" : "play"} size={16} />
                                    {isPlaying ? "일시정지 (Pause)" : "재생 (Play)"}
                                </button>

                                <button 
                                    onClick={() => {
                                        setIsPlaying(false);
                                        setCurrentTime(0);
                                    }}
                                    className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-all flex items-center gap-1"
                                >
                                    <Icon name="rotate-ccw" size={14} />
                                    처음으로
                                </button>

                                <div className="flex-1 flex items-center gap-2">
                                    <span className="text-xs font-mono font-bold text-slate-500 w-10">0.00s</span>
                                    <input 
                                        type="range" min="0" max={t_R} step="0.01" 
                                        value={currentTime} 
                                        onChange={(e) => {
                                            setIsPlaying(false);
                                            setCurrentTime(parseFloat(e.target.value));
                                        }}
                                        className="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer"
                                    />
                                    <span className="text-xs font-mono font-bold text-blue-600 w-14 text-right">{t_R.toFixed(2)}s</span>
                                </div>

                                <div className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl">
                                    {[0.5, 1.0, 2.0].map((spd) => (
                                        <button 
                                            key={spd}
                                            onClick={() => setPlaySpeed(spd)}
                                            className={`px-2 py-1 rounded-lg text-[11px] font-bold ${playSpeed === spd ? 'bg-white text-blue-600 shadow-xs' : 'text-slate-500'}`}
                                        >
                                            {spd}x
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* [활동 1] 3개 지점(A 상승 중, B 최고점, C 하강 중) 찍기 & 실시간 데이터 표 */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <span className="p-2 bg-indigo-50 text-indigo-600 rounded-xl">
                                    <Icon name="clipboard-check" size={20} />
                                </span>
                                <div>
                                    <h3 className="font-bold text-slate-800 text-base">📝 1. 세 위치에서 속도와 가속도를 관찰하자.</h3>
                                    <p className="text-xs text-slate-500">아래 버튼을 눌러 현재 위치를 <b>A(상승 중), B(최고점), C(하강 중)</b>로 찍고 표를 완성해 보세요.</p>
                                </div>
                            </div>

                            {/* 3개 지점 찍기 퀵 액션 버튼 */}
                            <div className="flex items-center gap-2">
                                <button 
                                    onClick={() => captureCurrentAs('A')}
                                    className="px-3 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5"
                                >
                                    <span className="w-2 h-2 rounded-full bg-blue-600"></span>
                                    현재 위치를 [A 상승 중]으로 기록
                                </button>

                                <button 
                                    onClick={() => {
                                        setPointB(getStateAtTime(t_H));
                                        setCurrentTime(t_H);
                                    }}
                                    className="px-3 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5"
                                >
                                    <span className="w-2 h-2 rounded-full bg-rose-600"></span>
                                    [B 최고점] 자동 기록 (★)
                                </button>

                                <button 
                                    onClick={() => captureCurrentAs('C')}
                                    className="px-3 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-200 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5"
                                >
                                    <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                                    현재 위치를 [C 하강 중]으로 기록
                                </button>
                            </div>
                        </div>

                        {/* 데이터 표 1: 정밀 수치 측정값 */}
                        <div>
                            <div className="text-xs font-bold text-slate-700 mb-2 flex items-center gap-1.5">
                                <Icon name="table" size={15} className="text-blue-600" />
                                [정밀 수치 데이터 표]
                            </div>
                            <div className="overflow-x-auto rounded-xl border border-slate-200">
                                <table className="w-full text-xs text-center border-collapse">
                                    <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                                        <tr>
                                            <th className="p-2.5 text-left pl-4">위치 (구분)</th>
                                            <th className="p-2.5">시간 t (s)</th>
                                            <th className="p-2.5">위치 (x, y) (m)</th>
                                            <th className="p-2.5 text-emerald-700 font-bold">수평 속도 vx (m/s)</th>
                                            <th className="p-2.5 text-rose-600 font-bold">연직 속도 vy (m/s)</th>
                                            <th className="p-2.5 text-slate-700">수평 가속도 ax (m/s²)</th>
                                            <th className="p-2.5 text-orange-600 font-bold">연직 가속도 ay (m/s²)</th>
                                            <th className="p-2.5 text-purple-700">합성 속도 v (m/s)</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-100 font-mono">
                                        {/* A 상승 중 */}
                                        <tr className="hover:bg-blue-50/50 transition-colors">
                                            <td className="p-2.5 text-left pl-4 font-sans font-bold text-blue-700 flex items-center gap-1.5">
                                                <span className="w-2.5 h-2.5 rounded-full bg-blue-600 inline-block"></span>
                                                A 상승 중
                                            </td>
                                            <td className="p-2.5">{pointA ? `${pointA.t.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5">{pointA ? `(${pointA.x.toFixed(2)}, ${pointA.y.toFixed(2)})` : '-'}</td>
                                            <td className="p-2.5 font-bold text-emerald-700">{pointA ? `+${pointA.vx.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5 font-bold text-rose-600">{pointA ? (pointA.vy >= 0 ? `+${pointA.vy.toFixed(2)}` : pointA.vy.toFixed(2)) : '-'}</td>
                                            <td className="p-2.5">0.00</td>
                                            <td className="p-2.5 font-bold text-orange-600">-{g.toFixed(2)}</td>
                                            <td className="p-2.5 font-bold text-purple-700">{pointA ? `${pointA.v.toFixed(2)}` : '-'}</td>
                                        </tr>

                                        {/* B 최고점 */}
                                        <tr className="hover:bg-rose-50/50 transition-colors">
                                            <td className="p-2.5 text-left pl-4 font-sans font-bold text-rose-700 flex items-center gap-1.5">
                                                <span className="w-2.5 h-2.5 rounded-full bg-rose-600 inline-block"></span>
                                                B 최고점
                                            </td>
                                            <td className="p-2.5">{pointB ? `${pointB.t.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5">{pointB ? `(${pointB.x.toFixed(2)}, ${pointB.y.toFixed(2)})` : '-'}</td>
                                            <td className="p-2.5 font-bold text-emerald-700">{pointB ? `+${pointB.vx.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5 font-bold text-rose-600">0.00</td>
                                            <td className="p-2.5">0.00</td>
                                            <td className="p-2.5 font-bold text-orange-600">-{g.toFixed(2)}</td>
                                            <td className="p-2.5 font-bold text-purple-700">{pointB ? `${pointB.v.toFixed(2)}` : '-'}</td>
                                        </tr>

                                        {/* C 하강 중 */}
                                        <tr className="hover:bg-emerald-50/50 transition-colors">
                                            <td className="p-2.5 text-left pl-4 font-sans font-bold text-emerald-700 flex items-center gap-1.5">
                                                <span className="w-2.5 h-2.5 rounded-full bg-emerald-600 inline-block"></span>
                                                C 하강 중
                                            </td>
                                            <td className="p-2.5">{pointC ? `${pointC.t.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5">{pointC ? `(${pointC.x.toFixed(2)}, ${pointC.y.toFixed(2)})` : '-'}</td>
                                            <td className="p-2.5 font-bold text-emerald-700">{pointC ? `+${pointC.vx.toFixed(2)}` : '-'}</td>
                                            <td className="p-2.5 font-bold text-blue-600">{pointC ? (pointC.vy >= 0 ? `+${pointC.vy.toFixed(2)}` : pointC.vy.toFixed(2)) : '-'}</td>
                                            <td className="p-2.5">0.00</td>
                                            <td className="p-2.5 font-bold text-orange-600">-{g.toFixed(2)}</td>
                                            <td className="p-2.5 font-bold text-purple-700">{pointC ? `${pointC.v.toFixed(2)}` : '-'}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* 핵심 탐구 원리 카드 (접이식 / 기본 숨김) */}
                        <div className="border border-blue-100 rounded-xl overflow-hidden text-xs">
                            <button 
                                onClick={() => setShowConclusion(prev => !prev)}
                                className="w-full bg-blue-50/80 hover:bg-blue-100/80 p-3 text-left font-bold text-blue-900 flex items-center justify-between transition-colors cursor-pointer"
                            >
                                <span className="flex items-center gap-1.5 text-xs md:text-sm">
                                    <Icon name="lightbulb" size={16} className="text-amber-500" />
                                    💡 핵심 물리 원리 탐구 결론 {showConclusion ? "(클릭하여 접기)" : "(클릭하여 펼치기)"}
                                </span>
                                <Icon name={showConclusion ? "chevron-up" : "chevron-down"} size={16} className="text-blue-600" />
                            </button>
                            
                            {showConclusion && (
                                <div className="bg-white p-4 space-y-2 border-t border-blue-100">
                                    <ul className="list-disc list-inside text-slate-700 space-y-1.5 leading-relaxed">
                                        <li><b>수평 방향(x)</b>: 공기 저항이 없으므로 알짜힘이 0(Fx = 0)이며, 가속도는 항상 <b>ax = 0 m/s²</b>로 수평 속도는 운동 내내 <b>일정(vx = v₀cosθ)</b>합니다.</li>
                                        <li><b>연직 방향(y)</b>: 일정한 중력(Fy = -mg)이 작용하므로 가속도는 항상 <b>ay = -g m/s² (아래 방향으로 일정)</b>합니다.</li>
                                        <li><b>최고점에서의 속도</b>: 연직 속도 vy는 0이지만, 수평 속도 vx는 살아있으므로 전체 속도는 0이 아니라 <b>v = vx</b>입니다.</li>
                                    </ul>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            );
        };

        ReactDOM.render(<ObliqueProjectileSim />, document.getElementById('root'));
    </script>
</body>
</html>
"""

# Streamlit에 임베드 렌더링
components.html(react_code, height=1020, scrolling=True)

# 하단 추가 수식 및 이론 요약
with st.expander("📚 포물선 운동 이론 공식 학습", expanded=False):
    st.latex(r"t_H = \frac{v_0 \sin\theta}{g}, \quad H = \frac{(v_0 \sin\theta)^2}{2g}")
    st.latex(r"t_R = 2t_H = \frac{2v_0 \sin\theta}{g}, \quad R = v_0 \cos\theta \times t_R = \frac{v_0^2 \sin 2\theta}{g}")
