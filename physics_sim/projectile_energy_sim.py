import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="활동 6. 포물선 운동에서 역학적 에너지 보존 확인하기", page_icon="⚡", layout="wide")

st.title("⚡ [분석3 / 활동 6] 포물선 운동에서 역학적 에너지는 보존될까?")
st.markdown(r"""
**탐구 질문**: **포물선 운동을 하는 물체의 높이가 변할 때, 어떤 운동에너지가 퍼텐셜 에너지로 전환될까?**  
*(조건: 공기 저항이 없는 조건에서 물체가 지점 1 → 최고점(지점 2) → 지점 3으로 운동함)*
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

        const ProjectileEnergySim = () => {
            // [1. 예측하기] 학생 선택 상태 관리
            const [predictions, setPredictions] = useState({
                height_12: '', height_23: '',
                vx_12: '', vx_23: '',
                vy_12: '', vy_23: '',
                ek_12: '', ek_23: '',
                ep_12: '', ep_23: '',
                emech_12: '', emech_23: ''
            });
            const [showPredFeedback, setShowPredFeedback] = useState(false);
            const [showPredQuestion, setShowPredQuestion] = useState(false);
            const [showEnergyQuestion, setShowEnergyQuestion] = useState(false);
            const [showDeltaQuestion, setShowDeltaQuestion] = useState(false);
            const [showFillAnswer, setShowFillAnswer] = useState(false);

            // 발사 조건 파라미터 (기본값: 질량 1.0kg, vx0=6, vy0=8, g=10 -> v0=10, theta=53.13)
            const [mass, setMass] = useState(1.0); // kg
            const [v0, setV0] = useState(10.0); // m/s
            const [thetaDeg, setThetaDeg] = useState(53.13); // deg
            const [g, setG] = useState(10.0); // m/s^2

            // 시뮬레이션 제어
            const [currentTime, setCurrentTime] = useState(0.0);
            const [isPlaying, setIsPlaying] = useState(false);
            const [playSpeed, setPlaySpeed] = useState(1.0);
            const [showVelComponents, setShowVelComponents] = useState(true);

            // 3개 지점 선택 (지점 1: 발사직후/상승중, 지점 2: 최고점, 지점 3: 하강중)
            const [pointA, setPointA] = useState(null);
            const [pointB, setPointB] = useState(null);
            const [pointC, setPointC] = useState(null);
            const [activeSlot, setActiveSlot] = useState('1');

            // 토글 상태들
            const [showTableAnswer, setShowTableAnswer] = useState(false);
            const [showChartAnswer, setShowChartAnswer] = useState(true);
            const [openQuestions, setOpenQuestions] = useState({
                q1: false, q2: false, q3: false, q4: false, q5: false, q6: false, ext: false
            });

            const canvasRef = useRef(null);
            const animRef = useRef(null);
            const lastTimeRef = useRef(null);

            // 물리 상수
            const theta = (thetaDeg * Math.PI) / 180.0;
            const vx0 = v0 * Math.cos(theta);
            const vy0 = v0 * Math.sin(theta);
            const t_H = vy0 / g;
            const H = (vy0 * vy0) / (2 * g);
            const t_R = 2 * t_H;
            const R = vx0 * t_R;

            // 시각 t에서의 물리 상태 계산
            const getStateAtTime = useCallback((t) => {
                const clampedT = Math.max(0, Math.min(t, t_R));
                const x = vx0 * clampedT;
                const y = Math.max(0, vy0 * clampedT - 0.5 * g * clampedT * clampedT);
                const vx = vx0;
                const vy = vy0 - g * clampedT;
                const v = Math.sqrt(vx * vx + vy * vy);

                const Ek_x = 0.5 * mass * vx * vx;
                const Ek_y = 0.5 * mass * vy * vy;
                const Ek = 0.5 * mass * v * v;
                const Ep = mass * g * y;
                const E_total = Ek + Ep;

                return { t: clampedT, x, y, vx, vy, v, Ek_x, Ek_y, Ek, Ep, E_total };
            }, [vx0, vy0, g, t_R, mass]);

            // 문제 조건 프리셋 적용
            const applyProblemPreset = () => {
                setMass(1.0);
                setV0(10.0);
                setThetaDeg(53.13);
                setG(10.0);

                const tC = (8.0 + Math.sqrt(32.0)) / 10.0; // 약 1.3657초
                const st1 = {
                    t: 0.0, x: 0.0, y: 0.0,
                    vx: 6.0, vy: 8.0, v: 10.0,
                    Ek_x: 18.0, Ek_y: 32.0, Ek: 50.0, Ep: 0.0, E_total: 50.0
                };
                const st2 = {
                    t: 0.8, x: 4.8, y: 3.2,
                    vx: 6.0, vy: 0.0, v: 6.0,
                    Ek_x: 18.0, Ek_y: 0.0, Ek: 18.0, Ep: 32.0, E_total: 50.0
                };
                const vyC = -Math.sqrt(32.0);
                const st3 = {
                    t: tC, x: 6.0 * tC, y: 1.6,
                    vx: 6.0, vy: vyC, v: Math.sqrt(36.0 + 32.0),
                    Ek_x: 18.0, Ek_y: 16.0, Ek: 34.0, Ep: 16.0, E_total: 50.0
                };

                setPointA(st1);
                setPointB(st2);
                setPointC(st3);
                setCurrentTime(0.0);
                setIsPlaying(false);
            };

            useEffect(() => {
                applyProblemPreset();
            }, []);

            // 애니메이션 루프
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

            const currentState = useMemo(() => getStateAtTime(currentTime), [currentTime, getStateAtTime]);

            // 지점 1 기록 (상승 구간 체크)
            const captureAsPoint1 = () => {
                if (currentTime > t_H * 0.98) {
                    alert("지점 1은 최고점에 도달하기 전인 '상승 구간'이어야 합니다. 슬라이더를 최고점(왼쪽) 이전으로 옮겨주세요.");
                    return;
                }
                setPointA(currentState);
            };

            // 지점 2 기록 (최고점 정확한 상태로 고정)
            const captureAsPoint2 = () => {
                const bSt = getStateAtTime(t_H);
                setPointB(bSt);
                setCurrentTime(t_H);
                setIsPlaying(false);
            };

            // 지점 3 기록 (하강 구간 체크)
            const captureAsPoint3 = () => {
                if (currentTime < t_H * 1.02) {
                    alert("지점 3은 최고점을 지난 '하강 구간'이어야 합니다. 슬라이더를 최고점(오른쪽) 이후로 옮겨주세요.");
                    return;
                }
                setPointC(currentState);
            };

            // 캔버스 클릭 핸들러 (지능형 구간 자동 매핑: 궤적 왼쪽=지점 1, 꼭대기=지점 2, 궤적 오른쪽=지점 3)
            const handleCanvasClick = (e) => {
                const canvas = canvasRef.current;
                if (!canvas) return;
                const rect = canvas.getBoundingClientRect();
                const clickX = e.clientX - rect.left;

                const margin = { left: 65, right: 35, top: 40, bottom: 50 };
                const plotW = canvas.width - margin.left - margin.right;
                const maxX = Math.max(R * 1.15, 12);
                const scaleX = plotW / maxX;

                const worldClickX = (clickX - margin.left) / scaleX;
                if (worldClickX >= 0 && worldClickX <= R) {
                    const clickT = Math.max(0, Math.min(worldClickX / vx0, t_R));
                    const st = getStateAtTime(clickT);
                    setCurrentTime(clickT);

                    // [명확한 물리적 규칙 자동 매핑]
                    // 1. 최고점 이전 (상승 구간): 무조건 [지점 1]로 저장
                    if (clickT < t_H * 0.92) {
                        setPointA(st);
                    }
                    // 2. 최고점 이후 (하강 구간): 무조건 [지점 3]으로 저장
                    else if (clickT > t_H * 1.08) {
                        setPointC(st);
                    }
                    // 3. 최고점 근처: [지점 2(최고점)]로 정확히 저장
                    else {
                        setPointB(getStateAtTime(t_H));
                    }
                }
            };

            // 화살표 그리기
            const drawArrow = (ctx, fromX, fromY, toX, toY, color, width = 2.5, headLength = 9) => {
                const dx = toX - fromX;
                const dy = toY - fromY;
                const angle = Math.atan2(dy, dx);
                const length = Math.sqrt(dx * dx + dy * dy);
                if (length < 2) return;

                ctx.save();
                ctx.strokeStyle = color;
                ctx.fillStyle = color;
                ctx.lineWidth = width;
                ctx.beginPath();
                ctx.moveTo(fromX, fromY);
                ctx.lineTo(toX, toY);
                ctx.stroke();

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

                const maxX = Math.max(R * 1.15, 12);
                const maxY = Math.max(H * 1.35, 5);
                const scaleX = plotW / maxX;
                const scaleY = plotH / maxY;
                const scale = Math.min(scaleX, scaleY);

                const toCanvasX = (wx) => margin.left + wx * scale;
                const toCanvasY = (wy) => height - margin.bottom - wy * scale;

                // 1. 그리드
                ctx.strokeStyle = '#e2e8f0';
                ctx.lineWidth = 1;
                const gridStepX = maxX > 40 ? 5 : (maxX > 15 ? 2 : 1);
                for (let gx = 0; gx <= maxX; gx += gridStepX) {
                    const cx = toCanvasX(gx);
                    ctx.beginPath();
                    ctx.moveTo(cx, margin.top);
                    ctx.lineTo(cx, height - margin.bottom);
                    ctx.stroke();

                    ctx.fillStyle = '#64748b';
                    ctx.font = '11px Pretendard';
                    ctx.textAlign = 'center';
                    ctx.fillText(`${gx}`, cx, height - margin.bottom + 18);
                }

                const gridStepY = maxY > 20 ? 5 : (maxY > 8 ? 2 : 1);
                for (let gy = 0; gy <= maxY; gy += gridStepY) {
                    const cy = toCanvasY(gy);
                    ctx.beginPath();
                    ctx.moveTo(margin.left, cy);
                    ctx.lineTo(margin.left + plotW, cy);
                    ctx.stroke();

                    ctx.fillStyle = '#64748b';
                    ctx.font = '11px Pretendard';
                    ctx.textAlign = 'right';
                    ctx.fillText(`${gy}`, margin.left - 10, cy + 4);
                }

                ctx.fillStyle = '#1e293b';
                ctx.font = 'bold 12px Pretendard';
                ctx.textAlign = 'center';
                ctx.fillText('수평 거리 x (m)', margin.left + plotW / 2, height - 12);

                ctx.save();
                ctx.translate(18, margin.top + plotH / 2);
                ctx.rotate(-Math.PI / 2);
                ctx.textAlign = 'center';
                ctx.fillText('높이 y (m)', 0, 0);
                ctx.restore();

                // 2. 바닥선
                ctx.strokeStyle = '#94a3b8';
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                ctx.moveTo(margin.left, height - margin.bottom);
                ctx.lineTo(margin.left + plotW, height - margin.bottom);
                ctx.stroke();

                // 2-1. 발사 각도 θ 호(Arc) 및 시각적 각도 표시
                const originX = toCanvasX(0);
                const originY = toCanvasY(0);
                const arcR = 46;
                ctx.save();
                ctx.beginPath();
                ctx.moveTo(originX, originY);
                ctx.arc(originX, originY, arcR, 0, -theta, true);
                ctx.closePath();
                ctx.fillStyle = 'rgba(245, 158, 11, 0.2)';
                ctx.fill();

                ctx.beginPath();
                ctx.arc(originX, originY, arcR, 0, -theta, true);
                ctx.strokeStyle = '#f59e0b';
                ctx.lineWidth = 2;
                ctx.stroke();

                // 발사 방향 가이드 점선
                const guideLen = arcR + 24;
                ctx.beginPath();
                ctx.setLineDash([3, 3]);
                ctx.moveTo(originX, originY);
                ctx.lineTo(originX + guideLen * Math.cos(theta), originY - guideLen * Math.sin(theta));
                ctx.strokeStyle = '#d97706';
                ctx.lineWidth = 1.5;
                ctx.stroke();
                ctx.setLineDash([]);

                // 각도 라벨 (θ = 53.1°)
                const midA = theta / 2;
                const textR = arcR + 18;
                const textX = originX + textR * Math.cos(midA);
                const textY = originY - textR * Math.sin(midA);
                ctx.fillStyle = '#b45309';
                ctx.font = 'bold 11px Pretendard';
                ctx.textAlign = 'left';
                ctx.textBaseline = 'middle';
                ctx.fillText(`θ = ${thetaDeg.toFixed(1)}°`, textX, textY);
                ctx.restore();

                // 3. 궤적
                ctx.strokeStyle = '#93c5fd';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                for (let s = 0; s <= 80; s++) {
                    const st_t = (t_R * s) / 80;
                    const px = vx0 * st_t;
                    const py = Math.max(0, vy0 * st_t - 0.5 * g * st_t * st_t);
                    if (s === 0) ctx.moveTo(toCanvasX(px), toCanvasY(py));
                    else ctx.lineTo(toCanvasX(px), toCanvasY(py));
                }
                ctx.stroke();
                ctx.setLineDash([]);

                // 4. 진행선
                ctx.strokeStyle = '#2563eb';
                ctx.lineWidth = 3;
                ctx.beginPath();
                const curSteps = Math.max(2, Math.floor((currentTime / t_R) * 80));
                for (let s = 0; s <= curSteps; s++) {
                    const st_t = Math.min(currentTime, (t_R * s) / 80);
                    const px = vx0 * st_t;
                    const py = Math.max(0, vy0 * st_t - 0.5 * g * st_t * st_t);
                    if (s === 0) ctx.moveTo(toCanvasX(px), toCanvasY(py));
                    else ctx.lineTo(toCanvasX(px), toCanvasY(py));
                }
                ctx.stroke();

                // 5. 최고점 표시
                const apexCanvasX = toCanvasX(vx0 * t_H);
                const apexCanvasY = toCanvasY(H);
                ctx.fillStyle = '#dc2626';
                ctx.font = 'bold 11px Pretendard';
                ctx.textAlign = 'center';
                ctx.fillText(`★ 최고점 H=${H.toFixed(2)}m`, apexCanvasX, apexCanvasY - 14);

                // 6. 관찰 지점(1, 2, 3) 뱃지 (지점별 Y오프셋 차별화로 겹침 방지)
                const renderBadge = (pt, label, tagColor, offsetY = 32) => {
                    if (!pt) return;
                    const px = toCanvasX(pt.x);
                    const py = toCanvasY(pt.y);

                    ctx.fillStyle = tagColor;
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 2.5;
                    ctx.beginPath();
                    ctx.arc(px, py, 7, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.stroke();

                    const tagW = 84;
                    const tagH = 22;
                    const tagX = px - tagW / 2;
                    const tagY = py - offsetY;

                    ctx.fillStyle = tagColor;
                    ctx.beginPath();
                    ctx.roundRect ? ctx.roundRect(tagX, tagY, tagW, tagH, 6) : ctx.rect(tagX, tagY, tagW, tagH);
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.stroke();

                    ctx.fillStyle = '#ffffff';
                    ctx.font = 'bold 10.5px Pretendard';
                    ctx.textAlign = 'center';
                    ctx.fillText(`${label} (h=${pt.y.toFixed(1)}m)`, px, tagY + 15);
                };

                renderBadge(pointA, '지점 1', '#2563eb', 32);
                renderBadge(pointB, '지점 2 (최고점)', '#dc2626', 48);
                renderBadge(pointC, '지점 3', '#16a34a', 32);

                // 7. 실시간 물체 및 속도 벡터
                const curCanvasX = toCanvasX(currentState.x);
                const curCanvasY = toCanvasY(currentState.y);

                if (showVelComponents) {
                    const vScale = 2.2;
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX + currentState.vx * vScale, curCanvasY, '#16a34a', 2.5, 8);
                    drawArrow(ctx, curCanvasX, curCanvasY, curCanvasX, curCanvasY - currentState.vy * vScale, '#dc2626', 2.5, 8);
                }

                ctx.fillStyle = '#f97316';
                ctx.strokeStyle = '#1e293b';
                ctx.lineWidth = 2.5;
                ctx.beginPath();
                ctx.arc(curCanvasX, curCanvasY, 9, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = '#ffffff';
                ctx.beginPath();
                ctx.arc(curCanvasX - 2, curCanvasY - 2, 3, 0, Math.PI * 2);
                ctx.fill();

            }, [currentState, pointA, pointB, pointC, showVelComponents, R, H, t_H, t_R, vx0, vy0, g]);

            // 변화량 계산 (구간 1: 1->2, 구간 2: 2->3)
            const delta12 = useMemo(() => {
                if (!pointA || !pointB) return null;
                return {
                    dEky: pointB.Ek_y - pointA.Ek_y,
                    dEp: pointB.Ep - pointA.Ep,
                    sum: (pointB.Ek_y - pointA.Ek_y) + (pointB.Ep - pointA.Ep),
                    dEkx: pointB.Ek_x - pointA.Ek_x
                };
            }, [pointA, pointB]);

            const delta23 = useMemo(() => {
                if (!pointB || !pointC) return null;
                return {
                    dEky: pointC.Ek_y - pointB.Ek_y,
                    dEp: pointC.Ep - pointB.Ep,
                    sum: (pointC.Ek_y - pointB.Ek_y) + (pointC.Ep - pointB.Ep),
                    dEkx: pointC.Ek_x - pointB.Ek_x
                };
            }, [pointB, pointC]);

            // 최대 역학적 에너지 (막대그래프 스케일)
            const maxEnergy = useMemo(() => {
                const eA = pointA ? pointA.E_total : 50;
                const eB = pointB ? pointB.E_total : 50;
                const eC = pointC ? pointC.E_total : 50;
                return Math.max(eA, eB, eC, 50);
            }, [pointA, pointB, pointC]);

            // 질문 열고 닫기 헬퍼
            const toggleQuestion = (qKey) => {
                setOpenQuestions(prev => ({ ...prev, [qKey]: !prev[qKey] }));
            };

            return (
                <div className="max-w-5xl mx-auto space-y-6 pb-16">
                    {/* [단계 1] 예측하기 카드 */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2.5">
                                <span className="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl">
                                    <Icon name="help-circle" size={22} />
                                </span>
                                <div>
                                    <h3 className="font-bold text-slate-800 text-base">🤔 1. 예측하기 (시뮬레이션 전 가설 세우기)</h3>
                                    <p className="text-xs text-slate-500">물체가 <b>지점 1 → 지점 2(최고점) → 지점 3</b>으로 이동할 때 각 물리량이 어떻게 변할지 먼저 예상해 보세요.</p>
                                </div>
                            </div>

                            <button
                                onClick={() => setShowPredFeedback(prev => !prev)}
                                className="px-3.5 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-xl text-xs font-bold transition-all flex items-center gap-1 cursor-pointer"
                            >
                                <Icon name={showPredFeedback ? "eye-off" : "check"} size={14} />
                                {showPredFeedback ? "예측 해설 접기" : "나의 예측 검증 & 모범 가설 보기"}
                            </button>
                        </div>

                        {/* 예측 인터랙티브 표 */}
                        <div className="overflow-x-auto rounded-xl border border-slate-200">
                            <table className="w-full text-xs text-center border-collapse">
                                <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                                    <tr>
                                        <th className="p-2.5 text-left pl-4">물리량</th>
                                        <th className="p-2.5">지점 1 → 지점 2 (상승 구간)</th>
                                        <th className="p-2.5">지점 2 → 지점 3 (하강 구간)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 font-sans">
                                    {[
                                        { id: 'height', label: '높이 (m)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '증가', ans2: '감소' },
                                        { id: 'vx', label: '수평 속도의 크기 (m/s)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '일정', ans2: '일정' },
                                        { id: 'vy', label: '연직 속도의 크기 (m/s)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '감소', ans2: '증가' },
                                        { id: 'ek', label: '운동에너지 (Ek)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '감소', ans2: '증가' },
                                        { id: 'ep', label: '위치에너지 (Ep)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '증가', ans2: '감소' },
                                        { id: 'emech', label: '역학적 에너지 (=운동E + 위치E)', opt1: ['증가', '감소', '일정'], opt2: ['증가', '감소', '일정'], ans1: '일정', ans2: '일정' }
                                    ].map(row => (
                                        <tr key={row.id} className="hover:bg-slate-50/60">
                                            <td className="p-2.5 text-left pl-4 font-bold text-slate-700">{row.label}</td>
                                            {/* 구간 1->2 */}
                                            <td className="p-2.5">
                                                <div className="flex justify-center gap-1.5">
                                                    {row.opt1.map(val => (
                                                        <button
                                                            key={val}
                                                            onClick={() => setPredictions(p => ({ ...p, [`${row.id}_12`]: val }))}
                                                            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                                                                predictions[`${row.id}_12`] === val
                                                                    ? 'bg-blue-600 text-white shadow-xs'
                                                                    : 'bg-slate-100 hover:bg-slate-200 text-slate-600'
                                                            }`}
                                                        >
                                                            {val}
                                                        </button>
                                                    ))}
                                                    {showPredFeedback && (
                                                        <span className="ml-2 font-bold text-emerald-600 self-center">
                                                            (정답: {row.ans1})
                                                        </span>
                                                    )}
                                                </div>
                                            </td>
                                            {/* 구간 2->3 */}
                                            <td className="p-2.5">
                                                <div className="flex justify-center gap-1.5">
                                                    {row.opt2.map(val => (
                                                        <button
                                                            key={val}
                                                            onClick={() => setPredictions(p => ({ ...p, [`${row.id}_23`]: val }))}
                                                            className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                                                                predictions[`${row.id}_23`] === val
                                                                    ? 'bg-blue-600 text-white shadow-xs'
                                                                    : 'bg-slate-100 hover:bg-slate-200 text-slate-600'
                                                            }`}
                                                        >
                                                            {val}
                                                        </button>
                                                    ))}
                                                    {showPredFeedback && (
                                                        <span className="ml-2 font-bold text-emerald-600 self-center">
                                                            (정답: {row.ans2})
                                                        </span>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {/* 1단계 발문 카드: 퍼텐셜 에너지는 어디에서 얻은 것일까? */}
                        <div className="bg-indigo-50/70 border border-indigo-200 rounded-xl p-3.5 text-xs space-y-2">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                                <span className="font-bold text-indigo-950 flex items-center gap-1.5">
                                    <Icon name="help-circle" size={15} className="text-indigo-600 shrink-0" />
                                    [질문] 물체가 상승하면서 증가하는 퍼텐셜 에너지는 어디에서 얻은 것일까? 예상해 보자.
                                </span>
                                <button
                                    onClick={() => setShowPredQuestion(prev => !prev)}
                                    className="px-2.5 py-1 bg-white hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-lg text-xs font-bold transition-all cursor-pointer shadow-xs"
                                >
                                    {showPredQuestion ? "생각 닫기" : "💡 나의 생각 정리 & 모범 생각 보기"}
                                </button>
                            </div>
                            {showPredQuestion && (
                                <div className="bg-white p-3 rounded-lg border border-indigo-100 text-slate-700 leading-relaxed space-y-1">
                                    <p className="font-bold text-indigo-900">
                                        👉 모범 예상: <b>"물체가 위로 올라갈 때 연직 방향 속력이 줄어들며 감소한 ‘연직 운동에너지’가 퍼텐셜 에너지로 전환되어 얻어진 것이다."</b>
                                    </p>
                                    <p className="text-slate-500 text-[11px]">
                                        (수평 방향 속도는 항상 일정하므로 수평 운동에너지는 퍼텐셜 에너지로 전환되지 않고 그대로 유지됩니다.)
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* [시뮬레이션 조작 및 3개 지점 캡처] */}
                    <div className="bg-white rounded-2xl p-4 md:p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <span className="p-2 bg-blue-50 text-blue-600 rounded-xl">
                                    <Icon name="play-circle" size={20} />
                                </span>
                                <div>
                                    <h3 className="font-bold text-slate-800 text-base">🏀 포물선 운동 시뮬레이션 & 세 지점 선택</h3>
                                    <p className="text-xs text-slate-500">
                                        <b>지점 1:</b> 발사 직후/상승 중 &nbsp;|&nbsp; <b>지점 2:</b> 최고점(vy=0) &nbsp;|&nbsp; <b>지점 3:</b> 내려오는 중 낮은 위치
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-center gap-2">
                                <button 
                                    onClick={applyProblemPreset}
                                    className="px-3.5 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-xs font-bold transition-all shadow-sm flex items-center gap-1.5 cursor-pointer"
                                >
                                    <Icon name="bookmark-check" size={15} />
                                    [문제 조건 적용] (v₀=10m/s, θ=53.1°, vx=6, vy=8, g=10)
                                </button>
                                <button 
                                    onClick={() => setShowVelComponents(prev => !prev)}
                                    className={`px-3 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 border cursor-pointer ${
                                        showVelComponents ? 'bg-emerald-50 text-emerald-700 border-emerald-300' : 'bg-slate-100 text-slate-600 border-slate-200'
                                    }`}
                                >
                                    <Icon name="arrow-up-right" size={14} />
                                    속도 성분 (vx, vy)
                                </button>
                            </div>
                        </div>

                        {/* 🚀 발사 조건 요약 바 (각도 θ 포함) */}
                        <div className="flex flex-wrap items-center gap-2 text-xs bg-amber-50/70 border border-amber-200 px-3.5 py-2 rounded-xl text-slate-800">
                            <span className="font-bold text-amber-900 flex items-center gap-1 shrink-0">
                                <Icon name="compass" size={15} className="text-amber-600" />
                                발사 조건:
                            </span>
                            <span className="bg-white px-2.5 py-0.5 rounded-lg border border-amber-200 font-medium text-slate-800">초기 속력 <b>v₀ = {v0.toFixed(1)} m/s</b></span>
                            <span className="bg-amber-500 text-white px-2.5 py-0.5 rounded-lg font-bold shadow-xs">발사 각도 θ = {thetaDeg.toFixed(1)}° (약 53.13°)</span>
                            <span className="bg-white px-2.5 py-0.5 rounded-lg border border-amber-200 text-emerald-700 font-medium">수평 속도 vx₀ = {vx0.toFixed(1)} m/s (cosθ = 0.6)</span>
                            <span className="bg-white px-2.5 py-0.5 rounded-lg border border-amber-200 text-rose-700 font-medium">연직 속도 vy₀ = {vy0.toFixed(1)} m/s (sinθ = 0.8)</span>
                            <span className="bg-white px-2.5 py-0.5 rounded-lg border border-amber-200 text-slate-600">중력 가속도 g = {g.toFixed(1)} m/s²</span>
                            <span className="bg-white px-2.5 py-0.5 rounded-lg border border-amber-200 text-slate-600">질량 m = {mass.toFixed(1)} kg</span>
                        </div>

                        {/* 💡 지점 선택 명확한 규칙 안내 배너 */}
                        <div className="p-3 bg-blue-50/80 border border-blue-200 rounded-xl text-xs text-blue-950 flex items-start gap-2.5">
                            <Icon name="info" size={17} className="text-blue-600 mt-0.5 shrink-0" />
                            <div className="space-y-0.5">
                                <div className="font-bold text-blue-900">💡 세 지점(1, 2, 3) 선택 규칙 및 방법 안내</div>
                                <div className="text-slate-700 leading-relaxed">
                                    • <b>방법 1 (포물선 궤적 직접 클릭)</b>: 궤적의 <b>왼쪽(상승부)</b>을 누르면 [지점 1], <b>꼭대기</b>를 누르면 [지점 2(최고점)], <b>오른쪽(하강부)</b>을 누르면 [지점 3]으로 즉시 자동 지정됩니다.<br/>
                                    • <b>방법 2 (슬라이더 조작)</b>: 슬라이더로 원하는 순간으로 이동한 후, 아래 해당 지점 카드의 <b>[현재 위치로 확정]</b> 버튼을 누르세요.
                                </div>
                            </div>
                        </div>

                        {/* 캔버스 및 실시간 HUD */}
                        <div className="relative">
                            <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-sm p-3 rounded-xl border border-slate-200 shadow-md pointer-events-none z-10 text-xs font-mono space-y-1 min-w-[210px]">
                                <div className="font-bold text-slate-800 font-sans flex items-center justify-between pb-1 border-b border-slate-200">
                                    <span className="flex items-center gap-1.5">
                                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                                        현재 물리 상태
                                    </span>
                                    <span className="text-[10px] text-slate-400 font-normal">t = {currentState.t.toFixed(2)}s</span>
                                </div>
                                <div className="text-amber-700 font-sans font-semibold pb-0.5 border-b border-slate-100 flex items-center justify-between">
                                    <span>발사 각도 (θ):</span>
                                    <b>{thetaDeg.toFixed(1)}° <span className="text-[10px] font-normal text-slate-500">(53.13°)</span></b>
                                </div>
                                <div className="text-slate-600">높이 (h): <b className="text-slate-900">{currentState.y.toFixed(2)} m</b></div>
                                <div className="text-emerald-700">수평 속도 (vx): <b>+{currentState.vx.toFixed(2)} m/s</b></div>
                                <div className={currentState.vy >= 0 ? "text-rose-600" : "text-blue-600"}>
                                    연직 속도 (vy): <b>{currentState.vy >= 0 ? `+${currentState.vy.toFixed(2)}` : currentState.vy.toFixed(2)} m/s</b>
                                </div>
                                <div className="text-purple-700 pt-1 border-t border-slate-100">
                                    전체 속력 (v): <b>{currentState.v.toFixed(2)} m/s</b>
                                </div>
                            </div>

                            <canvas 
                                ref={canvasRef} 
                                width={920} 
                                height={420}
                                onClick={handleCanvasClick}
                                className="w-full h-auto bg-slate-50/50 rounded-xl cursor-crosshair border border-slate-100"
                            />
                        </div>

                        {/* 타임라인 컨트롤 바 */}
                        <div className="flex flex-wrap items-center gap-3 pt-2">
                            <button 
                                onClick={() => {
                                    if (currentTime >= t_R) setCurrentTime(0);
                                    setIsPlaying(!isPlaying);
                                }}
                                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 shadow-sm cursor-pointer ${
                                    isPlaying ? 'bg-amber-500 text-white' : 'bg-blue-600 text-white'
                                }`}
                            >
                                <Icon name={isPlaying ? "pause" : "play"} size={16} />
                                {isPlaying ? "일시정지" : "재생 (Play)"}
                            </button>

                            <button 
                                onClick={() => {
                                    setIsPlaying(false);
                                    setCurrentTime(0);
                                }}
                                className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-bold transition-all flex items-center gap-1 cursor-pointer"
                            >
                                <Icon name="rotate-ccw" size={14} />
                                처음으로
                            </button>

                            <div className="flex-1 flex items-center gap-2 min-w-[200px]">
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
                        </div>

                        {/* 🌟 3개 지점(지점 1, 2, 3) 전용 확정 카드 (직관적인 상태 및 버튼) */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-3 border-t border-slate-100">
                            {/* 지점 1 카드 (상승 구간) */}
                            <div className={`p-3.5 rounded-xl border transition-all ${
                                currentTime <= t_H * 0.98 ? 'bg-blue-50/70 border-blue-300 shadow-xs' : 'bg-slate-50 border-slate-200'
                            }`}>
                                <div className="flex items-center justify-between mb-1.5">
                                    <span className="font-bold text-xs text-blue-700 flex items-center gap-1.5">
                                        <span className="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                                        지점 1 (상승 중)
                                    </span>
                                    <span className="text-[10px] text-slate-500 font-mono">0.00s ~ {t_H.toFixed(2)}s</span>
                                </div>
                                <div className="text-xs font-mono text-slate-700 mb-2.5">
                                    {pointA ? `t=${pointA.t.toFixed(2)}s | h=${pointA.y.toFixed(2)}m | v=${pointA.v.toFixed(1)}m/s` : '미지정'}
                                </div>
                                <button
                                    onClick={captureAsPoint1}
                                    disabled={currentTime > t_H * 0.98}
                                    className={`w-full py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
                                        currentTime <= t_H * 0.98
                                            ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-xs'
                                            : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                                    }`}
                                >
                                    <Icon name="pin" size={13} />
                                    {currentTime <= t_H * 0.98 ? `현재 위치(t=${currentTime.toFixed(2)}s)를 [지점 1]로 확정` : '⚠️ 슬라이더를 상승 구간으로 이동'}
                                </button>
                            </div>

                            {/* 지점 2 카드 (최고점) */}
                            <div className="p-3.5 rounded-xl border bg-rose-50/70 border-rose-300 shadow-xs">
                                <div className="flex items-center justify-between mb-1.5">
                                    <span className="font-bold text-xs text-rose-700 flex items-center gap-1.5">
                                        <span className="w-2.5 h-2.5 rounded-full bg-rose-600"></span>
                                        지점 2 (최고점 ★)
                                    </span>
                                    <span className="text-[10px] text-rose-600 font-bold font-mono">vy = 0 m/s</span>
                                </div>
                                <div className="text-xs font-mono text-slate-700 mb-2.5">
                                    {pointB ? `t=${pointB.t.toFixed(2)}s | h=${pointB.y.toFixed(2)}m | v=${pointB.v.toFixed(1)}m/s` : '미지정'}
                                </div>
                                <button
                                    onClick={captureAsPoint2}
                                    className="w-full py-2 rounded-lg text-xs font-bold bg-rose-600 hover:bg-rose-700 text-white shadow-xs transition-all flex items-center justify-center gap-1 cursor-pointer"
                                >
                                    <Icon name="star" size={13} />
                                    ★ 최고점으로 자동 이동 & 확정
                                </button>
                            </div>

                            {/* 지점 3 카드 (하강 구간) */}
                            <div className={`p-3.5 rounded-xl border transition-all ${
                                currentTime >= t_H * 1.02 ? 'bg-emerald-50/70 border-emerald-300 shadow-xs' : 'bg-slate-50 border-slate-200'
                            }`}>
                                <div className="flex items-center justify-between mb-1.5">
                                    <span className="font-bold text-xs text-emerald-700 flex items-center gap-1.5">
                                        <span className="w-2.5 h-2.5 rounded-full bg-emerald-600"></span>
                                        지점 3 (하강 중)
                                    </span>
                                    <span className="text-[10px] text-slate-500 font-mono">{t_H.toFixed(2)}s ~ {t_R.toFixed(2)}s</span>
                                </div>
                                <div className="text-xs font-mono text-slate-700 mb-2.5">
                                    {pointC ? `t=${pointC.t.toFixed(2)}s | h=${pointC.y.toFixed(2)}m | v=${pointC.v.toFixed(1)}m/s` : '미지정'}
                                </div>
                                <button
                                    onClick={captureAsPoint3}
                                    disabled={currentTime < t_H * 1.02}
                                    className={`w-full py-2 rounded-lg text-xs font-bold transition-all flex items-center justify-center gap-1 cursor-pointer ${
                                        currentTime >= t_H * 1.02
                                            ? 'bg-emerald-600 hover:bg-emerald-700 text-white shadow-xs'
                                            : 'bg-slate-200 text-slate-400 cursor-not-allowed'
                                    }`}
                                >
                                    <Icon name="pin" size={13} />
                                    {currentTime >= t_H * 1.02 ? `현재 위치(t=${currentTime.toFixed(2)}s)를 [지점 3]으로 확정` : '⚠️ 슬라이더를 하강 구간으로 이동'}
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* [단계 2] 시뮬레이션으로 확인하기 (운동 상태 관찰 표) */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <span className="p-2 bg-emerald-50 text-emerald-600 rounded-xl">
                                    <Icon name="eye" size={20} />
                                </span>
                                <div>
                                    <h3 className="font-bold text-slate-800 text-base">🔭 2. 시뮬레이션으로 확인하기 (운동 상태 관찰)</h3>
                                    <p className="text-xs text-slate-500">
                                        시뮬레이션에서 선택한 <b>세 지점(1: 상승, 2: 최고점, 3: 하강)</b>의 높이와 속도 성분을 확인하고 표에 기록하세요.
                                    </p>
                                </div>
                            </div>

                            <button 
                                onClick={applyProblemPreset}
                                className="px-3.5 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 border border-emerald-300 rounded-xl text-xs font-bold transition-all shadow-xs flex items-center gap-1.5 cursor-pointer"
                            >
                                <Icon name="sparkles" size={14} className="text-amber-500" />
                                ✨ 암산하기 쉬운 예쁜 정수 데이터 스냅 (h=0m, 3.2m, 1.6m)
                            </button>
                        </div>

                        <div className="overflow-x-auto rounded-xl border border-slate-200">
                            <table className="w-full text-xs text-center border-collapse">
                                <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                                    <tr>
                                        <th className="p-3 text-left pl-4">물리량</th>
                                        <th className="p-3 text-blue-700 font-bold">지점 1 (상승 중)</th>
                                        <th className="p-3 text-rose-700 font-bold">지점 2 (최고점 ★)</th>
                                        <th className="p-3 text-emerald-700 font-bold">지점 3 (하강 중)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 font-mono">
                                    <tr className="hover:bg-slate-50">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-slate-700">높이 (m)</td>
                                        <td className="p-3 font-semibold text-slate-800">{pointA ? `${pointA.y.toFixed(2)} m` : '-'}</td>
                                        <td className="p-3 font-semibold text-rose-700 bg-rose-50/40">{pointB ? `${pointB.y.toFixed(2)} m (최고)` : '-'}</td>
                                        <td className="p-3 font-semibold text-slate-800">{pointC ? `${pointC.y.toFixed(2)} m` : '-'}</td>
                                    </tr>
                                    <tr className="hover:bg-emerald-50/30">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-emerald-800">
                                            수평 속도의 크기 (m/s)
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700">{pointA ? `${pointA.vx.toFixed(2)} m/s` : '-'}</td>
                                        <td className="p-3 font-bold text-emerald-700 bg-emerald-50/40">{pointB ? `${pointB.vx.toFixed(2)} m/s (일정!)` : '-'}</td>
                                        <td className="p-3 font-bold text-emerald-700">{pointC ? `${pointC.vx.toFixed(2)} m/s` : '-'}</td>
                                    </tr>
                                    <tr className="hover:bg-rose-50/30">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-rose-800">
                                            연직 속도의 크기 (m/s)
                                        </td>
                                        <td className="p-3 font-bold text-rose-600">{pointA ? `${Math.abs(pointA.vy).toFixed(2)} m/s` : '-'}</td>
                                        <td className="p-3 font-bold text-rose-600 bg-rose-50/60">0.00 m/s (순간 정지)</td>
                                        <td className="p-3 font-bold text-blue-600">{pointC ? `${Math.abs(pointC.vy).toFixed(2)} m/s` : '-'}</td>
                                    </tr>
                                    <tr className="hover:bg-slate-50">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-slate-700">전체 속력 (m/s)</td>
                                        <td className="p-3 font-semibold text-slate-800">{pointA ? `${pointA.v.toFixed(2)} m/s` : '-'}</td>
                                        <td className="p-3 font-semibold text-rose-700 bg-rose-50/30">{pointB ? `${pointB.v.toFixed(2)} m/s (=vx)` : '-'}</td>
                                        <td className="p-3 font-semibold text-slate-800">{pointC ? `${pointC.v.toFixed(2)} m/s` : '-'}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    {/* [단계 3] 에너지로 확인하기 (에너지 계산 및 분석 표) */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
                            <div className="flex items-center gap-2">
                                <span className="p-2 bg-amber-50 text-amber-600 rounded-xl">
                                    <Icon name="zap" size={20} />
                                </span>
                                <div>
                                    <h3 className="font-bold text-slate-800 text-base">⚡ 3. 에너지로 확인하기 (에너지 계산 및 분석)</h3>
                                    <p className="text-xs text-slate-500">
                                        물체의 질량 <b>m = {mass.toFixed(1)} kg</b>, 중력가속도 <b>g = {g.toFixed(1)} m/s²</b> 조건에서 각 지점의 에너지를 계산해 보세요.
                                    </p>
                                </div>
                            </div>

                            <button 
                                onClick={() => setShowTableAnswer(prev => !prev)}
                                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 border shadow-sm cursor-pointer ${
                                    showTableAnswer 
                                        ? 'bg-amber-50 text-amber-800 border-amber-300' 
                                        : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white border-blue-600'
                                }`}
                            >
                                <Icon name={showTableAnswer ? "eye-off" : "calculator"} size={15} />
                                {showTableAnswer ? "계산값 숨기기 (학생 풀이 모드)" : "⚡ 1초 에너지 자동 계산 & 공식 채우기"}
                            </button>
                        </div>

                        {/* 수평 운동에너지 불변 팁 배너 */}
                        <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-950 flex items-center gap-2.5">
                            <span className="px-2 py-0.5 bg-emerald-600 text-white rounded-md font-bold text-[11px] shrink-0">시간 단축 팁</span>
                            <span className="leading-relaxed">
                                수평 속도 <b>vx = 6.0 m/s</b>로 항상 일정하므로, <b>수평 운동에너지(½m·vx²)는 세 지점 모두 18.0 J로 동일</b>합니다! (매번 계산할 필요 없이 바로 기입)
                            </span>
                        </div>

                        <div className="overflow-x-auto rounded-xl border border-slate-200">
                            <table className="w-full text-xs text-center border-collapse">
                                <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                                    <tr>
                                        <th className="p-3 text-left pl-4">물리량</th>
                                        <th className="p-3 text-blue-700 font-bold">지점 1 (상승 중)</th>
                                        <th className="p-3 text-rose-700 font-bold">지점 2 (최고점 ★)</th>
                                        <th className="p-3 text-emerald-700 font-bold">지점 3 (하강 중)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 font-mono">
                                    {/* 수평방향 운동에너지 */}
                                    <tr className="hover:bg-emerald-50/40 bg-emerald-50/10">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-emerald-900">
                                            수평방향 운동에너지 <span className="font-normal font-mono text-[11px] text-emerald-600">(½m·vx²)</span>
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700">
                                            {showTableAnswer ? (pointA ? `${pointA.Ek_x.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointA && <div className="text-[10px] text-emerald-600 font-normal">½×1×6²</div>}
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700 bg-emerald-50/40">
                                            {showTableAnswer ? (pointB ? `${pointB.Ek_x.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointB && <div className="text-[10px] text-emerald-600 font-normal">½×1×6²</div>}
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700">
                                            {showTableAnswer ? (pointC ? `${pointC.Ek_x.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointC && <div className="text-[10px] text-emerald-600 font-normal">½×1×6²</div>}
                                        </td>
                                    </tr>

                                    {/* 연직방향 운동에너지 */}
                                    <tr className="hover:bg-rose-50/40 bg-rose-50/10">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-rose-900">
                                            연직방향 운동에너지 <span className="font-normal font-mono text-[11px] text-rose-600">(½m·vy²)</span>
                                        </td>
                                        <td className="p-3 font-bold text-rose-600">
                                            {showTableAnswer ? (pointA ? `${pointA.Ek_y.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointA && <div className="text-[10px] text-rose-500 font-normal">½×1×8²</div>}
                                        </td>
                                        <td className="p-3 font-bold text-rose-600 bg-rose-50/40">
                                            {showTableAnswer ? '0.0 J' : '0 (J)'}
                                            {showTableAnswer && <div className="text-[10px] text-rose-500 font-normal">½×1×0² (0)</div>}
                                        </td>
                                        <td className="p-3 font-bold text-rose-600">
                                            {showTableAnswer ? (pointC ? `${pointC.Ek_y.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointC && <div className="text-[10px] text-rose-500 font-normal">½×1×(√32)²</div>}
                                        </td>
                                    </tr>

                                    {/* 위치에너지 */}
                                    <tr className="hover:bg-amber-50/40 bg-amber-50/10">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-amber-900">
                                            위치에너지 <span className="font-normal font-mono text-[11px] text-amber-600">(mgh)</span>
                                        </td>
                                        <td className="p-3 font-bold text-amber-700">
                                            {showTableAnswer ? (pointA ? `${pointA.Ep.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointA && <div className="text-[10px] text-amber-600 font-normal">1×10×0</div>}
                                        </td>
                                        <td className="p-3 font-bold text-amber-700 bg-amber-50/40">
                                            {showTableAnswer ? (pointB ? `${pointB.Ep.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointB && <div className="text-[10px] text-amber-600 font-normal">1×10×3.2</div>}
                                        </td>
                                        <td className="p-3 font-bold text-amber-700">
                                            {showTableAnswer ? (pointC ? `${pointC.Ep.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && pointC && <div className="text-[10px] text-amber-600 font-normal">1×10×1.6</div>}
                                        </td>
                                    </tr>

                                    {/* 역학적 에너지 */}
                                    <tr className="hover:bg-purple-50/50 bg-purple-50/20 border-t-2 border-purple-200">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-purple-900">
                                            역학적 에너지 <span className="font-normal font-mono text-[11px] text-purple-600">(Ek + Ep)</span>
                                        </td>
                                        <td className="p-3 font-bold text-purple-700 text-sm">
                                            {showTableAnswer ? (pointA ? `${pointA.E_total.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && <div className="text-[10px] text-purple-500 font-normal">18+32+0</div>}
                                        </td>
                                        <td className="p-3 font-bold text-purple-700 text-sm bg-purple-50/60">
                                            {showTableAnswer ? (pointB ? `${pointB.E_total.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && <div className="text-[10px] text-purple-500 font-normal">18+0+32</div>}
                                        </td>
                                        <td className="p-3 font-bold text-purple-700 text-sm">
                                            {showTableAnswer ? (pointC ? `${pointC.E_total.toFixed(1)} J` : '-') : '? (J)'}
                                            {showTableAnswer && <div className="text-[10px] text-purple-500 font-normal">18+16+16</div>}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        {/* 3단계 발문 카드: 함께 변하는 에너지 vs 변하지 않는 에너지는? */}
                        <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-3.5 text-xs space-y-2">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                                <span className="font-bold text-amber-950 flex items-center gap-1.5">
                                    <Icon name="help-circle" size={15} className="text-amber-600 shrink-0" />
                                    [질문] 높이가 변할 때 함께 변하는 에너지는 무엇인가? 반대로 변하지 않는 에너지는 무엇인가?
                                </span>
                                <button
                                    onClick={() => setShowEnergyQuestion(prev => !prev)}
                                    className="px-2.5 py-1 bg-white hover:bg-amber-100 text-amber-800 border border-amber-300 rounded-lg text-xs font-bold transition-all cursor-pointer shadow-xs"
                                >
                                    {showEnergyQuestion ? "해설 닫기" : "💡 모범 분석 확인하기"}
                                </button>
                            </div>
                            {showEnergyQuestion && (
                                <div className="bg-white p-3 rounded-lg border border-amber-100 text-slate-700 leading-relaxed space-y-1.5">
                                    <p>
                                        • <b>함께 변하는 에너지:</b> <span className="text-rose-700 font-bold">연직방향 운동에너지(Ek,y)</span>와 <span className="text-amber-700 font-bold">위치에너지(Ep)</span> (높이가 증가하면 연직 운동E는 감소하고 위치E는 증가함)
                                    </p>
                                    <p>
                                        • <b>변하지 않는 에너지:</b> <span className="text-emerald-700 font-bold">수평방향 운동에너지(Ek,x = 18.0 J)</span>와 <span className="text-purple-700 font-bold">전체 역학적 에너지(E = 50.0 J)</span>
                                    </p>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* [단계 4] 변화량을 비교하여 예상 검증하기 */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
                            <span className="p-2 bg-rose-50 text-rose-600 rounded-xl">
                                <Icon name="git-commit" size={20} />
                            </span>
                            <div>
                                <h3 className="font-bold text-slate-800 text-base">🔍 4. 변화량을 비교하여 예상 검증하기</h3>
                                <p className="text-xs text-slate-500">
                                    세 에너지의 구간별 변화량(Δ)을 계산하고 비교하여 어떤 에너지가 서로 전환되는지 검증해 보세요.
                                </p>
                            </div>
                        </div>

                        {/* 핵심 비교 테이블 */}
                        <div className="overflow-x-auto rounded-xl border border-slate-200">
                            <table className="w-full text-xs text-center border-collapse">
                                <thead className="bg-slate-100 text-slate-700 font-bold border-b border-slate-200">
                                    <tr>
                                        <th className="p-3 text-left pl-4">구간</th>
                                        <th className="p-3 text-emerald-700 font-bold">수평 운동E 변화량 (ΔEk,x)</th>
                                        <th className="p-3 text-rose-700 font-bold">연직 운동E 변화량 (ΔEk,y)</th>
                                        <th className="p-3 text-amber-700 font-bold">퍼텐셜E 변화량 (ΔEp)</th>
                                        <th className="p-3 text-purple-700 font-bold bg-purple-50">두 변화량의 합 (ΔEk,y + ΔEp)</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 font-mono text-xs">
                                    {/* 지점 1 -> 지점 2 */}
                                    <tr className="hover:bg-slate-50">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-blue-800 flex items-center gap-1.5">
                                            <span className="w-2 h-2 rounded-full bg-blue-600"></span>
                                            지점 1 → 지점 2 (상승 구간)
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700 bg-emerald-50/20">
                                            0.0 J (일정)
                                        </td>
                                        <td className="p-3 font-bold text-rose-600">
                                            {delta12 ? `${delta12.dEky >= 0 ? `+${delta12.dEky.toFixed(1)}` : delta12.dEky.toFixed(1)} J (감소)` : '-'}
                                        </td>
                                        <td className="p-3 font-bold text-amber-700">
                                            {delta12 ? `${delta12.dEp >= 0 ? `+${delta12.dEp.toFixed(1)}` : delta12.dEp.toFixed(1)} J (증가)` : '-'}
                                        </td>
                                        <td className="p-3 font-bold text-purple-700 bg-purple-50/50 text-sm">
                                            {delta12 ? `${delta12.sum.toFixed(1)} J (완전 보존)` : '-'}
                                        </td>
                                    </tr>

                                    {/* 지점 2 -> 지점 3 */}
                                    <tr className="hover:bg-slate-50">
                                        <td className="p-3 text-left pl-4 font-sans font-bold text-emerald-800 flex items-center gap-1.5">
                                            <span className="w-2 h-2 rounded-full bg-emerald-600"></span>
                                            지점 2 → 지점 3 (하강 구간)
                                        </td>
                                        <td className="p-3 font-bold text-emerald-700 bg-emerald-50/20">
                                            0.0 J (일정)
                                        </td>
                                        <td className="p-3 font-bold text-rose-600">
                                            {delta23 ? `${delta23.dEky >= 0 ? `+${delta23.dEky.toFixed(1)}` : delta23.dEky.toFixed(1)} J (증가)` : '-'}
                                        </td>
                                        <td className="p-3 font-bold text-amber-700">
                                            {delta23 ? `${delta23.dEp >= 0 ? `+${delta23.dEp.toFixed(1)}` : delta23.dEp.toFixed(1)} J (감소)` : '-'}
                                        </td>
                                        <td className="p-3 font-bold text-purple-700 bg-purple-50/50 text-sm">
                                            {delta23 ? `${delta23.sum.toFixed(1)} J (완전 보존)` : '-'}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        {/* 4단계 질문 1: 어떤 두 에너지의 변화량이 크기는 같고 방향은 반대인가? */}
                        <div className="bg-rose-50/70 border border-rose-200 rounded-xl p-3.5 text-xs space-y-2">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                                <span className="font-bold text-rose-950 flex items-center gap-1.5">
                                    <Icon name="help-circle" size={15} className="text-rose-600 shrink-0" />
                                    [질문 1] 세 에너지의 변화량을 비교해 보자. 어떤 두 에너지의 변화량이 크기는 같고 방향은 반대인가?
                                </span>
                                <button
                                    onClick={() => setShowDeltaQuestion(prev => !prev)}
                                    className="px-2.5 py-1 bg-white hover:bg-rose-100 text-rose-800 border border-rose-300 rounded-lg text-xs font-bold transition-all cursor-pointer shadow-xs"
                                >
                                    {showDeltaQuestion ? "닫기" : "💡 답변 확인하기"}
                                </button>
                            </div>
                            {showDeltaQuestion && (
                                <div className="bg-white p-3 rounded-lg border border-rose-100 text-slate-700 leading-relaxed space-y-1">
                                    <p className="font-bold text-rose-900">
                                        → <b>연직 방향 운동에너지 변화량(ΔEk,y)</b>과 <b>퍼텐셜 에너지 변화량(ΔEp)</b>의 크기는 같고 방향(부호)은 반대이다.
                                    </p>
                                    <p className="text-slate-500 font-mono text-[11px]">
                                        수식 관계: ΔEk,y + ΔEp = 0  ⇔  |ΔEk,y| = |ΔEp| (단, ΔEk,x = 0)
                                    </p>
                                </div>
                            )}
                        </div>

                        {/* 4단계 질문 2: 활동지 총괄 빈칸 완성하기 인터랙티브 */}
                        <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-4 text-xs text-blue-950 space-y-3 font-sans">
                            <div className="flex flex-wrap items-center justify-between gap-2">
                                <div className="font-bold text-sm text-blue-900 flex items-center gap-1.5">
                                    <Icon name="edit-3" size={16} className="text-blue-600 shrink-0" />
                                    [활동지 총괄 결론] 빈칸을 채워 탐구 결론을 완성해 보자!
                                </div>
                                <button
                                    onClick={() => setShowFillAnswer(prev => !prev)}
                                    className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-xs font-bold transition-all shadow-xs cursor-pointer"
                                >
                                    {showFillAnswer ? "정답 가리기" : "👁️ 정답 확인하기"}
                                </button>
                            </div>

                            <div className="bg-white p-3.5 rounded-xl border border-blue-100 text-slate-800 leading-loose text-sm">
                                "공기 저항이 없는 포물선 운동에서 수평 방향 운동에너지는{' '}
                                <span className={`px-2.5 py-0.5 rounded font-bold border transition-all ${showFillAnswer ? 'bg-emerald-100 text-emerald-800 border-emerald-300' : 'bg-slate-100 text-slate-400 border-slate-300'}`}>
                                    {showFillAnswer ? '일정 (보존)' : '____________'}
                                </span>
                                하고, 연직 방향 운동에너지의 감소량은 퍼텐셜 에너지의{' '}
                                <span className={`px-2.5 py-0.5 rounded font-bold border transition-all ${showFillAnswer ? 'bg-amber-100 text-amber-800 border-amber-300' : 'bg-slate-100 text-slate-400 border-slate-300'}`}>
                                    {showFillAnswer ? '증가' : '__________'}
                                </span>
                                량과 같다."
                            </div>
                        </div>
                    </div>

                    {/* [단계 5] 결과 비교하기 및 해석하기 (활동지 심화 문항 & 모범 답안) */}
                    <div className="bg-white rounded-2xl p-5 shadow-sm border border-slate-200 space-y-4">
                        <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
                            <span className="p-2 bg-amber-50 text-amber-600 rounded-xl">
                                <Icon name="file-text" size={20} />
                            </span>
                            <div>
                                <h3 className="font-bold text-slate-800 text-base">✍️ 5. 결과 비교하기 및 심화 해석</h3>
                                <p className="text-xs text-slate-500">측정 및 계산한 데이터를 바탕으로 다음 탐구 질문에 답해 보세요. (클릭하여 모범 답안 확인)</p>
                            </div>
                        </div>

                        <div className="space-y-3">
                            {/* 질문 1 */}
                            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                                <button 
                                    onClick={() => toggleQuestion('q1')}
                                    className="w-full bg-slate-50 hover:bg-slate-100 p-3.5 text-left font-bold text-slate-800 flex items-center justify-between cursor-pointer"
                                >
                                    <span>① 세 지점 중 높이가 가장 높은 곳은 어디인가?</span>
                                    <Icon name={openQuestions.q1 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q1 && (
                                    <div className="bg-white p-4 border-t border-slate-200 text-slate-700 leading-relaxed space-y-1">
                                        <p className="font-bold text-blue-900">→ 지점 2 (최고점, h = {pointB ? pointB.y.toFixed(2) : '3.20'} m)</p>
                                        <p className="text-slate-500">연직 방향 속도 vy가 0이 되는 순간 물체는 궤적에서 가장 높은 위치에 도달합니다.</p>
                                    </div>
                                )}
                            </div>

                            {/* 질문 2 */}
                            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                                <button 
                                    onClick={() => toggleQuestion('q2')}
                                    className="w-full bg-slate-50 hover:bg-slate-100 p-3.5 text-left font-bold text-slate-800 flex items-center justify-between cursor-pointer"
                                >
                                    <span>② 그 지점(최고점)에서 속력과 운동에너지는 다른 지점과 비교하여 어떠한가?</span>
                                    <Icon name={openQuestions.q2 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q2 && (
                                    <div className="bg-white p-4 border-t border-slate-200 text-slate-700 leading-relaxed space-y-1">
                                        <p className="font-bold text-blue-900">→ 다른 지점과 비교하여 속력과 운동에너지가 가장 작다 (최솟값).</p>
                                        <p className="text-slate-500">
                                            연직 속력 vy가 0이 되므로 연직 운동에너지는 0이 되고, 오직 수평 속도 vx에 의한 운동에너지({pointB ? pointB.Ek_x.toFixed(1) : '18.0'} J)만 남아 전체 운동에너지가 가장 작아집니다.
                                        </p>
                                    </div>
                                )}
                            </div>

                            {/* 질문 3 */}
                            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                                <button 
                                    onClick={() => toggleQuestion('q3')}
                                    className="w-full bg-slate-50 hover:bg-slate-100 p-3.5 text-left font-bold text-slate-800 flex items-center justify-between cursor-pointer"
                                >
                                    <span>③ 높이가 증가하는 동안 운동에너지와 위치에너지는 각각 어떻게 변하는가?</span>
                                    <Icon name={openQuestions.q3 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q3 && (
                                    <div className="bg-white p-4 border-t border-slate-200 text-slate-700 leading-relaxed space-y-1">
                                        <p className="font-bold text-blue-900">→ 운동에너지: 감소 / 위치에너지(퍼텐셜에너지): 증가</p>
                                        <p className="text-slate-500">
                                            물체가 위로 올라갈수록 중력에 대항하여 높이가 높아져 퍼텐셜 에너지는 증가하고, 연직 방향 속력이 줄어들어 운동에너지는 감소합니다.
                                        </p>
                                    </div>
                                )}
                            </div>

                            {/* 질문 4 - 핵심 발문! */}
                            <div className="border border-indigo-200 rounded-xl overflow-hidden text-xs bg-indigo-50/20">
                                <button 
                                    onClick={() => toggleQuestion('q4')}
                                    className="w-full bg-indigo-50 hover:bg-indigo-100/80 p-3.5 text-left font-bold text-indigo-950 flex items-center justify-between cursor-pointer"
                                >
                                    <span>④ [핵심] 물체가 상승할 때 퍼텐셜 에너지가 증가한다. 이 에너지는 물체의 수평 운동에너지와 연직 운동에너지 중 어느 것에서 온 것인지 설명하자.</span>
                                    <Icon name={openQuestions.q4 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q4 && (
                                    <div className="bg-white p-4 border-t border-indigo-200 text-slate-700 leading-relaxed space-y-2">
                                        <p className="font-bold text-blue-900">[모범 답안]</p>
                                        <p>
                                            공기 저항이 없으므로 수평 방향 속도 vx는 일정하게 유지되어 <b>수평 운동에너지(½m·vx²)는 전혀 변하지 않습니다.</b>
                                        </p>
                                        <p>
                                            반면 연직 속도 vy는 중력에 의해 점차 감소하여 <b>연직 운동에너지(½m·vy²)가 줄어듭니다.</b> 
                                            측정 결과에서 연직 운동에너지가 감소한 양(32 J)과 퍼텐셜 에너지가 증가한 양(32 J)이 정확히 일치하므로, 
                                            <b>증가한 퍼텐셜 에너지는 물체의 '연직 운동에너지'에서 전환되어 온 것</b>입니다.
                                        </p>
                                    </div>
                                )}
                            </div>

                            {/* 질문 5 */}
                            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                                <button 
                                    onClick={() => toggleQuestion('q5')}
                                    className="w-full bg-slate-50 hover:bg-slate-100 p-3.5 text-left font-bold text-slate-800 flex items-center justify-between cursor-pointer"
                                >
                                    <span>⑤ 세 지점의 역학적 에너지를 비교하면 어떠한가?</span>
                                    <Icon name={openQuestions.q5 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q5 && (
                                    <div className="bg-white p-4 border-t border-slate-200 text-slate-700 leading-relaxed space-y-1">
                                        <p className="font-bold text-blue-900">→ 세 지점의 역학적 에너지는 모두 50.0 J로 서로 같다 (일정하게 보존됨).</p>
                                    </div>
                                )}
                            </div>

                            {/* 질문 6 */}
                            <div className="border border-slate-200 rounded-xl overflow-hidden text-xs">
                                <button 
                                    onClick={() => toggleQuestion('q6')}
                                    className="w-full bg-slate-50 hover:bg-slate-100 p-3.5 text-left font-bold text-slate-800 flex items-center justify-between cursor-pointer"
                                >
                                    <span>⑥ 포물선 운동을 하는 물체의 높이와 속력은 계속 변한다. 그럼에도 세 지점의 역학적 에너지가 거의 같은 이유를 설명해 보자.</span>
                                    <Icon name={openQuestions.q6 ? "chevron-up" : "chevron-down"} size={16} />
                                </button>
                                {openQuestions.q6 && (
                                    <div className="bg-white p-4 border-t border-slate-200 text-slate-700 leading-relaxed space-y-2">
                                        <p className="font-bold text-blue-900">[모범 답안]</p>
                                        <p>
                                            물체가 올라갈 때는 연직 운동에너지가 위치에너지로 전환되고, 내려올 때는 위치에너지가 연직 운동에너지로 다시 전환됩니다.
                                            공기 저항과 같은 비보존력이 작용하지 않고 오직 중력(보존력)만이 일하므로, 
                                            <b>운동에너지의 감소량과 위치에너지의 증가량(또는 그 반대)이 항상 같아 두 에너지의 합인 역학적 에너지는 일정하게 보존</b>됩니다.
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* [단계 6] 생각 확장하기 (오개념 교정) */}
                    <div className="bg-gradient-to-r from-amber-50 to-orange-50 rounded-2xl p-5 shadow-sm border border-amber-200 space-y-3">
                        <div className="flex items-center gap-2 border-b border-amber-200 pb-2.5">
                            <span className="p-2 bg-amber-100 text-amber-800 rounded-xl">
                                <Icon name="lightbulb" size={20} />
                            </span>
                            <div>
                                <h3 className="font-bold text-amber-950 text-base">💡 6. 생각 확장하기 (오개념 타파)</h3>
                                <p className="text-xs text-amber-800">최고점에서는 연직 방향 속도가 0이 됩니다. 그렇다면 최고점에서 물체의 운동에너지도 0이라고 할 수 있을까요?</p>
                            </div>
                        </div>

                        <div className="bg-white/90 p-4 rounded-xl border border-amber-200 text-xs space-y-2.5 text-slate-800 leading-relaxed">
                            <div className="font-bold text-rose-600 text-sm flex items-center gap-1.5">
                                <Icon name="alert-triangle" size={16} />
                                ❌ 아닙니다! 최고점에서도 운동에너지는 0이 아닙니다.
                            </div>
                            <p>
                                연직으로 던져 올린 물체는 최고점에서 속도가 0이 되므로 운동에너지도 0이 맞습니다.
                            </p>
                            <p>
                                하지만 <b>비스듬히 던진 포물선 운동</b>에서는 최고점에 도달했을 때 <b>연직 방향 속도 vy만 0이 될 뿐, 수평 방향 속도 vx는 그대로 유지</b>됩니다!
                            </p>
                            <div className="p-2.5 bg-amber-50 rounded-lg border border-amber-200 font-mono text-amber-950">
                                최고점 속력: v = √(vx² + 0²) = vx = <b>{pointB ? pointB.vx.toFixed(1) : '6.0'} m/s</b><br/>
                                최고점 운동에너지: Ek = ½m·vx² = <b>{pointB ? pointB.Ek_x.toFixed(1) : '18.0'} J ≠ 0</b>
                            </div>
                            <p className="text-slate-600 text-[11px]">
                                👉 따라서 포물선 운동의 최고점에서는 모든 에너지가 위치에너지로 바뀌는 것이 아니라, <b>수평 운동에너지를 제외한 '연직 운동에너지'만 위치에너지로 전환</b>됩니다.
                            </p>
                        </div>
                    </div>

                    {/* [단계 7] 물리 개념 및 공식 정리 카드 */}
                    <div className="bg-slate-900 text-white rounded-2xl p-5 shadow-sm space-y-3">
                        <div className="flex items-center gap-2 border-b border-slate-800 pb-2.5">
                            <span className="p-2 bg-slate-800 text-blue-400 rounded-xl">
                                <Icon name="book-open" size={20} />
                            </span>
                            <div>
                                <h3 className="font-bold text-white text-base">📚 7. 물리 개념 총정리 (수식 도출)</h3>
                                <p className="text-xs text-slate-400">포물선 운동에서 역학적 에너지 보존의 성분 분해 원리</p>
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono pt-1">
                            <div className="bg-slate-800/80 p-3.5 rounded-xl border border-slate-700 space-y-1.5">
                                <div className="text-blue-400 font-bold font-sans">1. 운동에너지의 수평/연직 성분 분해</div>
                                <div>Ek = ½m·v² = ½m·(vx² + vy²)</div>
                                <div className="text-emerald-400">Ek = ½m·vx² (수평, 일정) + ½m·vy² (연직, 변화)</div>
                            </div>

                            <div className="bg-slate-800/80 p-3.5 rounded-xl border border-slate-700 space-y-1.5">
                                <div className="text-purple-400 font-bold font-sans">2. 연직 운동에너지와 퍼텐셜 에너지 보존</div>
                                <div>E = (½m·vx²) + (½m·vy² + mgh) = 일정</div>
                                <div className="text-amber-400 font-bold">👉 Δ(½m·vy²) = -Δ(mgh)  ⇔  |ΔEk,y| = |ΔEp|</div>
                            </div>
                        </div>
                    </div>
                </div>
            );
        };

        ReactDOM.render(<ProjectileEnergySim />, document.getElementById('root'));
    </script>
</body>
</html>
"""

components.html(react_code, height=2350, scrolling=True)

with st.expander("📚 활동 6 지도서 및 이론 공식 상세", expanded=False):
    st.latex(r"E_k = \frac{1}{2}m(v_x^2 + v_y^2) = \underbrace{\frac{1}{2}mv_x^2}_{\text{일정 (등속)}} + \underbrace{\frac{1}{2}mv_y^2}_{\text{변화 (등가속도)}}")
    st.latex(r"E_{\text{mech}} = \frac{1}{2}mv_x^2 + \left( \frac{1}{2}mv_y^2 + mgh \right) = \text{일정}")
    st.latex(r"\Delta E_{k,y} + \Delta E_p = 0 \iff \left| \Delta E_{k,y} \right| = \left| \Delta E_p \right|")
