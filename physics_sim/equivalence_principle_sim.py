import streamlit as st
import streamlit.components.v1 as components

def run_sim():

    react_code = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&family=Space+Mono&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Noto Sans KR',sans-serif;background:#0a0f1e;color:#e2e8f0;padding:18px;}
.panel{background:#0d1526;border:1px solid #1e293b;border-radius:14px;padding:20px;}
.card{background:#0f172a;border:1px solid #1e293b;border-radius:14px;padding:20px;}
input[type=range]{-webkit-appearance:none;width:100%;height:5px;background:#1e293b;border-radius:3px;outline:none;}
input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:18px;height:18px;border-radius:50%;background:#3b82f6;cursor:pointer;box-shadow:0 0 8px rgba(59,130,246,0.6);}
label{font-size:11px;color:#64748b;font-weight:700;display:block;margin-bottom:5px;text-transform:uppercase;letter-spacing:0.04em;}
.result-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.result-val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;font-size:13px;}
.scene-btn{padding:9px 14px;border-radius:9px;border:1px solid #1e293b;background:#0d1526;color:#94a3b8;cursor:pointer;font-size:13px;font-family:inherit;transition:all 0.2s;text-align:left;width:100%;}
.scene-btn.active{border-color:#6366f1;background:rgba(99,102,241,0.12);color:#e2e8f0;font-weight:700;}
.scene-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.view-badge{display:inline-block;padding:2px 8px;border-radius:4px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef, useCallback } = React;

/* ── KaTeX ── */
const Eq = ({ f, display=false }) => {
    const ref = useRef(null);
    useEffect(()=>{
        if(ref.current && window.katex)
            window.katex.render(f, ref.current, {throwOnError:false, displayMode:display});
    },[f,display]);
    return <span ref={ref}/>;
};

/* ══════════════════════════════════════════
   물리 공식: s = ½at²  (pixel/sec² 스케일)
   두 시나리오에 동일한 scale/maxDist 적용
══════════════════════════════════════════ */
const SCALE  = 55;   // pixel / (m/s²) — 시각적 이동량 비율
const MAX_MS = 2200; // 애니메이션 최대 시간(ms)

const physDist = (tMs, a) => {
    const tSec = Math.min(tMs, MAX_MS) / 1000;
    return 0.5 * a * tSec * tSec * SCALE;
};

/* ── 별 배경 ── */
const STARS = Array.from({length:80},(_,i)=>{
    const s = (n)=>{ let x=Math.sin(n)*43758.5453; return x-Math.floor(x); };
    return { x:s(i*1.1), y:s(i*2.3), r:s(i*3.7)*1.2+0.3, ph:s(i*5.1)*Math.PI*2, spd:0.5+s(i*7.3) };
});

function drawStars(ctx, W, H, t){
    STARS.forEach(st=>{
        const op=0.2+0.45*Math.sin(st.ph+t*st.spd*0.001);
        ctx.beginPath(); ctx.arc(st.x*W, st.y*H, st.r, 0, Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`; ctx.fill();
    });
}

/* ── 공 ── */
function drawBall(ctx, x, y, r=11){
    const g=ctx.createRadialGradient(x-r*0.3, y-r*0.3, r*0.1, x, y, r);
    g.addColorStop(0,'#fff8dc'); g.addColorStop(0.4,'#ffcc44'); g.addColorStop(1,'#b45309');
    ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2);
    ctx.fillStyle=g; ctx.fill();
    ctx.strokeStyle='rgba(255,200,80,0.4)'; ctx.lineWidth=1; ctx.stroke();
}

/* ── 우주선 (전체, 외부 시점용) ── */
function drawRocketFull(ctx, cx, cy, w, h, thrust=0, flicker=1){
    // 불꽃
    if(thrust>0){
        const fH=(18+thrust*1.8)*flicker;
        const fg=ctx.createLinearGradient(cx,cy+h/2,cx,cy+h/2+fH);
        fg.addColorStop(0,'rgba(255,210,60,0.95)'); fg.addColorStop(0.4,'rgba(255,100,20,0.8)'); fg.addColorStop(1,'rgba(255,40,0,0)');
        ctx.beginPath();
        ctx.moveTo(cx-11,cy+h/2-2);
        ctx.quadraticCurveTo(cx-6,cy+h/2+fH*0.6,cx,cy+h/2+fH);
        ctx.quadraticCurveTo(cx+6,cy+h/2+fH*0.6,cx+11,cy+h/2-2);
        ctx.fillStyle=fg; ctx.fill();
    }
    // 몸체
    const bg=ctx.createLinearGradient(cx-w/2,0,cx+w/2,0);
    bg.addColorStop(0,'#8aa0c0'); bg.addColorStop(0.4,'#d0dff0'); bg.addColorStop(0.6,'#e8f0ff'); bg.addColorStop(1,'#6080a0');
    ctx.beginPath(); ctx.roundRect(cx-w/2,cy-h/2,w,h,w/4);
    ctx.fillStyle=bg; ctx.fill();
    ctx.strokeStyle='rgba(180,200,230,0.4)'; ctx.lineWidth=1; ctx.stroke();
    // 창문
    ctx.beginPath(); ctx.arc(cx,cy-h/8,w/5,0,Math.PI*2);
    const wg=ctx.createRadialGradient(cx-2,cy-h/8-2,1,cx,cy-h/8,w/5);
    wg.addColorStop(0,'rgba(180,220,255,0.9)'); wg.addColorStop(0.7,'rgba(50,120,240,0.6)'); wg.addColorStop(1,'rgba(20,60,120,0.8)');
    ctx.fillStyle=wg; ctx.fill();
    ctx.strokeStyle='rgba(200,220,255,0.7)'; ctx.lineWidth=1.5; ctx.stroke();
    // 인물
    ctx.beginPath(); ctx.arc(cx,cy-h/8,w/5*0.42,0,Math.PI*2);
    ctx.fillStyle='rgba(15,30,70,0.85)'; ctx.fill();
    // 상단 캡
    ctx.beginPath(); ctx.moveTo(cx-w/2,cy-h/2);
    ctx.quadraticCurveTo(cx,cy-h/2-h*0.25,cx+w/2,cy-h/2);
    ctx.fillStyle='rgba(160,180,210,0.9)'; ctx.fill();
    // 핀
    [[-1],[1]].forEach(([d])=>{
        ctx.beginPath();
        ctx.moveTo(cx+d*w/2, cy+h/2-h*0.15);
        ctx.lineTo(cx+d*w/2+d*w*0.38, cy+h/2+h*0.08);
        ctx.lineTo(cx+d*w/2, cy+h/2);
        ctx.fillStyle='rgba(120,150,190,0.8)'; ctx.fill();
    });
}

/* ── 우주선 내부 단면 (내부 시점용) ── */
function drawRocketInterior(ctx, cx, cy, w, h){
    // 바닥판
    ctx.beginPath(); ctx.roundRect(cx-w/2, cy-h/2, w, h, 10);
    ctx.fillStyle='rgba(20,30,55,0.92)'; ctx.fill();
    ctx.strokeStyle='rgba(100,150,220,0.5)'; ctx.lineWidth=2; ctx.stroke();
    // 바닥
    ctx.beginPath(); ctx.rect(cx-w/2+2, cy+h/2-14, w-4, 12);
    ctx.fillStyle='rgba(60,90,140,0.7)'; ctx.fill();
    // 왼쪽 벽
    ctx.beginPath(); ctx.rect(cx-w/2+2, cy-h/2+2, 8, h-18);
    ctx.fillStyle='rgba(40,60,100,0.5)'; ctx.fill();
    // 오른쪽 벽
    ctx.beginPath(); ctx.rect(cx+w/2-10, cy-h/2+2, 8, h-18);
    ctx.fillStyle='rgba(40,60,100,0.5)'; ctx.fill();
    // 창문 (위쪽 작은 창)
    ctx.beginPath(); ctx.roundRect(cx-14,cy-h/2+10,28,18,4);
    ctx.fillStyle='rgba(100,180,255,0.15)'; ctx.fill();
    ctx.strokeStyle='rgba(100,180,255,0.4)'; ctx.lineWidth=1; ctx.stroke();
    // 바닥 눈금선 (기준)
    for(let i=1;i<4;i++){
        ctx.beginPath();
        ctx.moveTo(cx-w/2+2, cy+h/2-14-i*28);
        ctx.lineTo(cx-w/2+10, cy+h/2-14-i*28);
        ctx.strokeStyle=`rgba(100,150,220,${0.15+i*0.05})`; ctx.lineWidth=0.5; ctx.stroke();
    }
}

/* ── 화살표 ── */
function arrow(ctx,x1,y1,x2,y2,color,lw=2){
    const dx=x2-x1,dy=y2-y1,ang=Math.atan2(dy,dx);
    ctx.save(); ctx.strokeStyle=color; ctx.lineWidth=lw; ctx.lineCap='round';
    ctx.beginPath(); ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke();
    const al=11,aa=0.42;
    ctx.beginPath();
    ctx.moveTo(x2,y2);
    ctx.lineTo(x2-al*Math.cos(ang-aa),y2-al*Math.sin(ang-aa));
    ctx.moveTo(x2,y2);
    ctx.lineTo(x2-al*Math.cos(ang+aa),y2-al*Math.sin(ang+aa));
    ctx.stroke(); ctx.restore();
}

/* ── 라벨 ── */
function lbl(ctx,x,y,s,color,size=12,align='center',weight='400'){
    ctx.save(); ctx.fillStyle=color;
    ctx.font=`${weight} ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align; ctx.fillText(s,x,y); ctx.restore();
}

/* ── 라벨 배경박스 ── */
function lblBox(ctx,x,y,s,bg,textColor,size=11,align='center'){
    ctx.save();
    ctx.font=`700 ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align;
    const tw=ctx.measureText(s).width;
    const pad=8, ph=6;
    const bx = align==='center' ? x-tw/2-pad : align==='left' ? x-pad : x-tw-pad;
    ctx.fillStyle=bg; ctx.beginPath(); ctx.roundRect(bx,y-size-ph,tw+pad*2,size+ph*2,5); ctx.fill();
    ctx.fillStyle=textColor; ctx.fillText(s,x,y); ctx.restore();
}

/* ══════════════════════════════════════════
   시나리오 1 : 내부 / 외부 시점
   무중력 공간, 우주선이 a로 위쪽 가속
   내부: 우주선 단면 고정, 공이 아래로 낙하
   외부: 전체 우주선이 위로 이동, 공은 고정
══════════════════════════════════════════ */
function drawScenario1(ctx,W,H,accel,tL,tR){
    drawStars(ctx,W,H,tL+tR);
    const rw=100, rh=240;
    const baseCy = H*0.50;  // 두 시점의 기준 중심 y

    /* ── 공통 물리 거리 ── */
    const dL = physDist(tL, accel);   // 내부: 공이 내려온 거리
    const dR = physDist(tR, accel);   // 외부: 우주선이 올라간 거리
    const ballStartRelY = -rh*0.30;   // 우주선 중심에서 공의 시작 상대 y

    /* ══ 왼쪽: 내부 관찰자 시점 ══ */
    const cx1=W*0.27;
    // 배경 프레임
    ctx.save();
    ctx.strokeStyle='rgba(99,102,241,0.35)'; ctx.lineWidth=1.5; ctx.setLineDash([6,4]);
    ctx.beginPath(); ctx.roundRect(cx1-rw/2-14, baseCy-rh/2-36, rw+28, rh+90, 12);
    ctx.stroke(); ctx.setLineDash([]); ctx.restore();

    // 뱃지
    lblBox(ctx,cx1,baseCy-rh/2-44,'내부 관찰자 시점','rgba(99,102,241,0.85)','#e0e7ff',11);
    lbl(ctx,cx1,baseCy-rh/2-10,'우주선 내부 (가속 중)', 'rgba(180,185,230,0.7)',11);

    // 우주선 내부 단면 (고정)
    drawRocketInterior(ctx, cx1, baseCy+20, rw, rh);

    // 공 (아래로 이동 = 바닥에 접근)
    const ballY1 = baseCy + 20 + ballStartRelY + dL;
    const floorY1 = baseCy + 20 + rh/2 - 20;
    const hitFloor1 = ballY1 + 11 >= floorY1;

    // 클리핑
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cx1-rw/2+2, baseCy+20-rh/2+2, rw-4, rh-4, 8); ctx.clip();
    drawBall(ctx, cx1, hitFloor1 ? floorY1-11 : ballY1);

    // 관성력 화살표 (공 아래 방향)
    if(!hitFloor1 && dL > 5){
        const by=hitFloor1 ? floorY1-11 : ballY1;
        arrow(ctx, cx1, by+14, cx1, by+36, 'rgba(248,113,113,0.9)', 2);
        lblBox(ctx, cx1+22, by+29, 'F관성', 'rgba(248,113,113,0.2)', '#fca5a5', 10, 'left');
    }
    ctx.restore();

    // 속도 텍스트
    const vL = (accel * Math.min(tL, MAX_MS)/1000).toFixed(2);
    lbl(ctx,cx1,baseCy+rh/2+54,`v = ${vL} m/s  |  d = ${dL.toFixed(1)} px`,'rgba(248,113,113,0.7)',11);

    /* ══ 오른쪽: 외부 관찰자 시점 ══ */
    const cx2=W*0.73;
    ctx.save();
    ctx.strokeStyle='rgba(74,222,128,0.35)'; ctx.lineWidth=1.5; ctx.setLineDash([6,4]);
    ctx.beginPath(); ctx.roundRect(cx2-rw/2-14, baseCy-rh/2-36, rw+28, rh+90, 12);
    ctx.stroke(); ctx.setLineDash([]); ctx.restore();

    lblBox(ctx,cx2,baseCy-rh/2-44,'외부 관찰자 시점','rgba(74,222,128,0.85)','#d1fae5',11);
    lbl(ctx,cx2,baseCy-rh/2-10,'우주 공간 (관성 좌표계)', 'rgba(140,200,160,0.7)',11);

    // 우주선이 dR만큼 위로 이동
    const rocketCy2 = baseCy + 20 - dR;
    const thrust2 = 0.88 + 0.18*Math.sin(tR*0.018);
    drawRocketFull(ctx, cx2, rocketCy2, rw, rh, accel, thrust2);

    // 공은 공간에 고정 (관성)
    const ballAbsY2 = baseCy + 20 + ballStartRelY;  // 절대 위치 고정
    drawBall(ctx, cx2, ballAbsY2);

    // 가속도 화살표 (우주선 위 방향)
    if(dR > 4){
        arrow(ctx, cx2+rw*0.55, rocketCy2-30, cx2+rw*0.55, rocketCy2-70, 'rgba(74,222,128,0.9)', 2.5);
        lblBox(ctx, cx2+rw*0.55+22, rocketCy2-50, `a=${accel.toFixed(1)}`, 'rgba(74,222,128,0.2)', '#6ee7b7', 10, 'left');
    }

    // 우주선이 공에 접근하는 거리 표시
    const gap = Math.max(0, ballAbsY2 - (rocketCy2 + ballStartRelY));
    lbl(ctx,cx2,baseCy+rh/2+54,`d = ${dR.toFixed(1)} px  |  간격 = ${gap.toFixed(1)} px`,'rgba(74,222,128,0.7)',11);

    // 두 시점 연결 화살표 + 설명
    const midX = W/2;
    lbl(ctx, midX, baseCy+20, '=', 'rgba(167,139,250,0.8)', 28, 'center', '800');
    lbl(ctx, midX, baseCy+50, '두 시점에서', 'rgba(167,139,250,0.6)', 11);
    lbl(ctx, midX, baseCy+64, '공과 바닥이 만남', 'rgba(167,139,250,0.6)', 11);

    // 동기화 확인: 이동거리 같음 표시
    if(tL>50 && tR>50){
        const syncOk = Math.abs(dL-dR) < 1;
        lbl(ctx, midX, baseCy-20,
            syncOk ? '✓ 동일한 물리량' : '비동기',
            syncOk ? 'rgba(74,222,128,0.8)' : 'rgba(248,113,113,0.7)', 11);
    }
}

/* ══════════════════════════════════════════
   시나리오 2 : 중력 vs 가속 우주선 비교
   왼쪽: 지구 표면, 공이 중력으로 낙하
   오른쪽: 가속 우주선, 공에 관성력 작용
   → 핵심 질문: 내부 관찰자가 구별할 수 있는가?
══════════════════════════════════════════ */
function drawScenario2(ctx,W,H,accel,tL,tR){
    drawStars(ctx,W,H,tL+tR);
    const rw=100, rh=240;
    const baseCy = H*0.50;
    const ballStartRelY = -rh*0.30;

    const dL = physDist(tL, 9.8);       // 왼쪽: 중력 g=9.8 고정
    const dR = physDist(tR, accel);     // 오른쪽: 설정된 가속도

    /* ══ 왼쪽: 지구 중력 ══ */
    const cx1=W*0.27;

    // 지구 배경 힌트
    ctx.save();
    ctx.strokeStyle='rgba(255,179,71,0.3)'; ctx.lineWidth=1.5; ctx.setLineDash([6,4]);
    ctx.beginPath(); ctx.roundRect(cx1-rw/2-14, baseCy-rh/2-36, rw+28, rh+100, 12);
    ctx.stroke(); ctx.setLineDash([]); ctx.restore();

    lblBox(ctx,cx1,baseCy-rh/2-44,'지구 표면 (중력장)','rgba(255,179,71,0.85)','#fef3c7',11);
    lbl(ctx,cx1,baseCy-rh/2-10,'내부 관찰자 시점', 'rgba(200,170,100,0.7)',11);

    // 지구 아이콘 (하단)
    const earthY1=baseCy+rh/2+36;
    const eg=ctx.createRadialGradient(cx1-5,earthY1-5,3,cx1,earthY1,22);
    eg.addColorStop(0,'#5090e0'); eg.addColorStop(0.6,'#2060b0'); eg.addColorStop(1,'#0a3060');
    ctx.beginPath(); ctx.arc(cx1,earthY1,22,0,Math.PI*2);
    ctx.fillStyle=eg; ctx.fill(); ctx.strokeStyle='rgba(100,180,255,0.4)'; ctx.lineWidth=1.5; ctx.stroke();
    lbl(ctx,cx1,earthY1+5,'지구','rgba(180,210,255,0.8)',10);

    // 우주선 내부
    drawRocketInterior(ctx, cx1, baseCy+20, rw, rh);

    // 공 낙하
    const ballY1 = baseCy+20+ballStartRelY+dL;
    const floorY1 = baseCy+20+rh/2-20;
    const hit1 = ballY1+11 >= floorY1;
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cx1-rw/2+2,baseCy+20-rh/2+2,rw-4,rh-4,8); ctx.clip();
    drawBall(ctx, cx1, hit1 ? floorY1-11 : ballY1);
    // 중력 화살표
    if(!hit1 && dL>5){
        const by=hit1?floorY1-11:ballY1;
        arrow(ctx,cx1,by+14,cx1,by+40,'rgba(255,179,71,0.9)',2.5);
        lblBox(ctx,cx1+22,by+30,'F = mg','rgba(255,179,71,0.2)','#fcd34d',11,'left');
    }
    ctx.restore();

    const vL=(9.8*Math.min(tL,MAX_MS)/1000).toFixed(2);
    lbl(ctx,cx1,baseCy+rh/2+68,`v = ${vL} m/s`,'rgba(255,179,71,0.7)',11);

    /* ══ 오른쪽: 가속 우주선 ══ */
    const cx2=W*0.73;

    ctx.save();
    ctx.strokeStyle='rgba(74,222,128,0.3)'; ctx.lineWidth=1.5; ctx.setLineDash([6,4]);
    ctx.beginPath(); ctx.roundRect(cx2-rw/2-14, baseCy-rh/2-36, rw+28, rh+100, 12);
    ctx.stroke(); ctx.setLineDash([]); ctx.restore();

    lblBox(ctx,cx2,baseCy-rh/2-44,'가속 우주선 (무중력 공간)','rgba(74,222,128,0.85)','#d1fae5',11);
    lbl(ctx,cx2,baseCy-rh/2-10,'내부 관찰자 시점', 'rgba(140,200,160,0.7)',11);

    // 가속 화살표 (우주선 바깥 위쪽)
    const aArrX = cx2+rw/2+20;
    arrow(ctx, aArrX, baseCy+rh/2+10, aArrX, baseCy-rh/2+10, 'rgba(74,222,128,0.7)',2);
    lblBox(ctx, aArrX+10, baseCy, `a=${accel.toFixed(1)}`, 'rgba(74,222,128,0.2)', '#6ee7b7', 10, 'left');

    // 우주선 내부 (고정)
    drawRocketInterior(ctx, cx2, baseCy+20, rw, rh);

    // 공 낙하 (관성력에 의해)
    const ballY2=baseCy+20+ballStartRelY+dR;
    const floorY2=baseCy+20+rh/2-20;
    const hit2=ballY2+11>=floorY2;
    ctx.save();
    ctx.beginPath(); ctx.roundRect(cx2-rw/2+2,baseCy+20-rh/2+2,rw-4,rh-4,8); ctx.clip();
    drawBall(ctx, cx2, hit2 ? floorY2-11 : ballY2);
    // 관성력 화살표
    if(!hit2 && dR>5){
        const by=hit2?floorY2-11:ballY2;
        arrow(ctx,cx2,by+14,cx2,by+40,'rgba(248,113,113,0.9)',2.5);
        lblBox(ctx,cx2+22,by+30,'F관성 = ma','rgba(248,113,113,0.2)','#fca5a5',11,'left');
    }
    ctx.restore();

    const vR=(accel*Math.min(tR,MAX_MS)/1000).toFixed(2);
    lbl(ctx,cx2,baseCy+rh/2+68,`v = ${vR} m/s`,'rgba(74,222,128,0.7)',11);

    /* ══ 가운데: 핵심 질문 ══ */
    const mx=W/2;
    const sameA = Math.abs(accel - 9.8) < 0.15;

    if(sameA){
        // 구별 불가 강조
        const pulse=0.65+0.35*Math.sin((tL+tR)*0.004);
        ctx.save(); ctx.globalAlpha=pulse;
        lbl(ctx,mx,baseCy-30,'≡','rgba(167,139,250,0.95)',34,'center','800');
        ctx.restore();
        lbl(ctx,mx,baseCy+10,'내부에서 구별','rgba(167,139,250,0.85)',12);
        lbl(ctx,mx,baseCy+28,'불가능하다!','rgba(167,139,250,0.85)',12);

        ctx.save();
        ctx.fillStyle='rgba(167,139,250,0.07)'; ctx.strokeStyle='rgba(167,139,250,0.25)'; ctx.lineWidth=0.5;
        ctx.beginPath(); ctx.roundRect(mx-62,baseCy-52,124,100,8); ctx.fill(); ctx.stroke(); ctx.restore();
    } else {
        lbl(ctx,mx,baseCy-20,'비교 중','rgba(167,139,250,0.6)',11);
        lbl(ctx,mx,baseCy,`a = ${accel.toFixed(1)}`, 'rgba(167,139,250,0.7)',12,'center','700');
        lbl(ctx,mx,baseCy+18,'≠ g = 9.8', 'rgba(248,113,113,0.6)',11);
    }

    // 하단 탐구 질문 배너
    const qY=baseCy+rh/2+90;
    ctx.save();
    ctx.fillStyle='rgba(10,15,40,0.85)'; ctx.strokeStyle='rgba(167,139,250,0.3)'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.roundRect(W*0.08, qY, W*0.84, 46, 8); ctx.fill(); ctx.stroke(); ctx.restore();
    lbl(ctx,W/2,qY+16,'🔍 탐구 질문:','rgba(255,220,80,0.9)',12,'center','700');
    lbl(ctx,W/2,qY+34,'내부 관찰자는 두 상황(중력 vs 관성력)을 구별할 수 있는가?','rgba(200,190,255,0.9)',12,'center','600');
}

/* ══════════════════════════════════════════
   캔버스 컴포넌트
══════════════════════════════════════════ */
const SimCanvas = ({ scenario, accel, tL, tR }) => {
    const ref = useRef(null);
    const draw = useCallback(() => {
        const canvas=ref.current; if(!canvas) return;
        const ctx=canvas.getContext('2d');
        const W=canvas.width, H=canvas.height;
        ctx.clearRect(0,0,W,H);
        ctx.fillStyle='#0a0f1e'; ctx.fillRect(0,0,W,H);
        if(scenario===0) drawScenario1(ctx,W,H,accel,tL,tR);
        else              drawScenario2(ctx,W,H,accel,tL,tR);
    },[scenario,accel,tL,tR]);

    useEffect(()=>{
        const canvas=ref.current; if(!canvas) return;
        const ro=new ResizeObserver(()=>{
            canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw();
        });
        ro.observe(canvas);
        canvas.width=canvas.offsetWidth; canvas.height=canvas.offsetHeight; draw();
        return()=>ro.disconnect();
    },[]);
    useEffect(()=>{ draw(); },[draw]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ══════════════════════════════════════════
   QnA
══════════════════════════════════════════ */
const QNA = [
    {
        q:'내부 관찰자 시점에서 공이 아래로 떨어지는 것처럼 보이는 이유는?',
        a:'가속 좌표계(우주선 내부)에서는 뉴턴의 운동 법칙이 성립하지 않습니다. 이를 보정하기 위해 도입한 관성력(F = −ma)이 마치 중력처럼 공을 아래로 당기는 것처럼 느껴집니다. 실제로 공에는 아무 힘도 작용하지 않지만(무중력 공간), 좌표계 자체가 가속되므로 공이 낙하하는 것처럼 보입니다.'
    },
    {
        q:'외부 관찰자 시점에서는 공이 왜 정지해 있는가?',
        a:'외부 관찰자는 관성 좌표계에 있습니다. 무중력 공간에서 공에 아무 힘도 작용하지 않으므로, 뉴턴의 제1법칙에 의해 공은 처음 속도를 유지하며 정지해 있습니다. 대신 우주선이 가속되어 위로 올라오기 때문에, 결국 우주선 바닥이 공에 충돌하게 됩니다.'
    },
    {
        q:'두 시점(내부/외부)에서 공과 바닥이 만나는 시간이 같은 이유는?',
        a:'두 시점 모두 동일한 물리 공식 s = ½at²를 사용합니다. 내부에서는 공이 바닥 방향으로 s만큼 이동하고, 외부에서는 바닥(우주선)이 공 방향으로 s만큼 이동합니다. 상대적 위치 변화량이 동일하므로 두 시점에서 충돌 시각은 정확히 일치합니다.'
    },
    {
        q:'중력을 받는 상황과 가속 우주선 상황을 내부 관찰자가 구별할 수 없는 이유는? (등가 원리)',
        a:'중력(F = mg)과 관성력(F = ma, a = g일 때)은 크기와 방향이 완전히 동일합니다. 내부 관찰자가 어떤 실험을 해도(공 낙하, 저울 측정, 빛의 경로 등) 두 상황을 구별할 방법이 없습니다. 아인슈타인은 이를 등가 원리로 정식화하고, 이로부터 중력을 시공간의 곡률로 재해석하여 일반 상대성 이론을 발전시켰습니다.'
    },
];

const QnASection = () => {
    const [open, setOpen] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {QNA.map((item,i)=>(
                <div key={i} style={{borderRadius:12,border:`1px solid ${open===i?'#6366f1':'#1e293b'}`,overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
                    <button onClick={()=>setOpen(open===i?null:i)}
                        style={{width:'100%',display:'flex',alignItems:'flex-start',gap:12,padding:'13px 16px',background:'transparent',border:'none',cursor:'pointer',textAlign:'left',fontFamily:'inherit'}}>
                        <span style={{color:'#6366f1',fontWeight:800,fontSize:14,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
                        <span style={{color:'#cbd5e1',fontSize:13,lineHeight:1.65,flex:1}}>{item.q}</span>
                        <span style={{color:'#475569',fontSize:16,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
                    </button>
                    <div style={{maxHeight:open===i?'220px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
                        <div style={{padding:'0 16px 14px 42px',display:'flex',gap:10}}>
                            <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                            <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.75}}>{item.a}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

/* ══════════════════════════════════════════
   개념 연결 (수식 유도)
══════════════════════════════════════════ */
const STEPS = [
    { title:'Step 1. 관성력의 정의', desc:'비관성 좌표계에서 뉴턴의 법칙을 성립시키기 위해 도입한 가상의 힘.',
      formula:'\\vec{F}_{\\text{관성}} = -m\\vec{a}', color:'#3b82f6', bg:'#0d1f3c',
      note:'실제 힘이 아니라 좌표계 가속에 의한 겉보기 힘이다. 크기는 ma, 방향은 가속도의 반대.' },
    { title:'Step 2. 동일한 운동 방정식', desc:'중력과 관성력, 두 상황 모두 공의 운동방정식이 동일하다.',
      formula:'ma_{\\text{공}} = mg = ma_{\\text{우주선}} \\quad (a=g)', color:'#8b5cf6', bg:'#1a0d3c',
      note:'가속도 a = g로 설정하면 공의 가속도가 완전히 일치한다. 내부 관찰자 입장에서 두 상황은 물리적으로 동일하다.' },
    { title:'Step 3. 낙하 운동의 동일성', desc:'두 상황에서 공의 위치 변화량이 같다.',
      formula:'s = \\frac{1}{2}g t^2 = \\frac{1}{2}a t^2', color:'#ec4899', bg:'#2d0d1a',
      note:'s, v, t 모든 운동량이 완전히 일치. 어떤 역학 실험을 해도 두 상황을 구별할 수 없다.' },
    { title:'Step 4. 아인슈타인 등가 원리', desc:'중력과 관성력은 물리적으로 완전히 동등하다.',
      formula:'g_{\\mu\\nu}\\text{(중력)} \\equiv F_{\\text{관성}}/m', color:'#10b981', bg:'#0a1f18',
      note:'아인슈타인(1907): "지금까지 내가 한 생각 중 가장 행복한 생각." 이 등가 원리가 일반 상대성 이론의 출발점이다.' },
    { title:'Step 5. 시공간 곡률로의 확장', desc:'등가 원리는 중력이 힘이 아닌 시공간의 곡률임을 암시한다.',
      formula:'G_{\\mu\\nu} = \\frac{8\\pi G}{c^4}T_{\\mu\\nu}', color:'#f59e0b', bg:'#1f1200',
      note:'질량이 시공간을 휘게 하고, 휘어진 시공간이 물체의 경로를 결정한다. 중력은 힘이 아니라 기하학이다.' },
];

const DerivationSection = () => {
    const [open, setOpen] = useState(null);
    return (
        <div>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:14}}>
                <div style={{width:4,height:22,background:'#6366f1',borderRadius:2}}/>
                <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0'}}>개념 연결: 관성력 → 등가 원리 → 시공간 곡률</h2>
            </div>
            <div style={{display:'flex',flexDirection:'column',gap:9}}>
                {STEPS.map((s,i)=>(
                    <div key={i} style={{border:`1px solid ${open===i?s.color+'99':'#1e293b'}`,borderRadius:12,overflow:'hidden',transition:'border-color 0.25s'}}>
                        <button onClick={()=>setOpen(open===i?null:i)}
                            style={{width:'100%',display:'flex',alignItems:'center',gap:12,padding:'12px 16px',background:open===i?s.bg:'transparent',border:'none',cursor:'pointer',fontFamily:'inherit',transition:'background 0.25s'}}>
                            <div style={{width:26,height:26,borderRadius:'50%',background:s.color+'22',border:`1.5px solid ${s.color}66`,display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
                                <span style={{color:s.color,fontWeight:800,fontSize:12}}>{i+1}</span>
                            </div>
                            <span style={{color:'#e2e8f0',fontWeight:700,fontSize:13,flex:1,textAlign:'left'}}>{s.title}</span>
                            <span style={{color:'#475569',fontSize:16,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)'}}>▾</span>
                        </button>
                        <div style={{maxHeight:open===i?'260px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                            <div style={{padding:'0 16px 16px 54px',background:s.bg}}>
                                <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.7,marginBottom:12}}>{s.desc}</p>
                                <div style={{background:'#070b14',borderRadius:8,padding:'12px 16px',marginBottom:10,textAlign:'center',border:`1px solid ${s.color}33`}}>
                                    <Eq f={s.formula} display={true}/>
                                </div>
                                <p style={{color:'#64748b',fontSize:12,lineHeight:1.75,borderLeft:`3px solid ${s.color}55`,paddingLeft:10}}>{s.note}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

/* ══════════════════════════════════════════
   메인 App
══════════════════════════════════════════ */
const App = () => {
    const [scenario, setScenario] = useState(0);
    const [accel,    setAccel]    = useState(9.8);
    const [tL, setTL] = useState(0);
    const [tR, setTR] = useState(0);
    const [runL, setRunL] = useState(false);
    const [runR, setRunR] = useState(false);
    const rafL = useRef(null), rafR = useRef(null);
    const stL  = useRef(null), stR  = useRef(null);

    /* ── 타이머 루프 ── */
    useEffect(()=>{
        if(runL){
            stL.current = performance.now() - tL;
            const loop=(now)=>{
                const nt=now-stL.current;
                if(nt<MAX_MS){ setTL(nt); rafL.current=requestAnimationFrame(loop); }
                else{ setTL(MAX_MS); setRunL(false); }
            };
            rafL.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafL.current);
        return()=>cancelAnimationFrame(rafL.current);
    },[runL]);

    useEffect(()=>{
        if(runR){
            stR.current = performance.now() - tR;
            const loop=(now)=>{
                const nt=now-stR.current;
                if(nt<MAX_MS){ setTR(nt); rafR.current=requestAnimationFrame(loop); }
                else{ setTR(MAX_MS); setRunR(false); }
            };
            rafR.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafR.current);
        return()=>cancelAnimationFrame(rafR.current);
    },[runR]);

    const reset=()=>{ setRunL(false); setRunR(false); setTL(0); setTR(0); };

    const syncRun=()=>{ reset(); setTimeout(()=>{ setRunL(true); setRunR(true); },50); };

    const changeScenario=(i)=>{ setScenario(i); reset(); };

    /* ── 현재 물리량 계산 ── */
    const dL = physDist(tL, scenario===0 ? accel : 9.8);
    const dR = physDist(tR, accel);
    const vL = ((scenario===0?accel:9.8)*Math.min(tL,MAX_MS)/1000);
    const vR = (accel*Math.min(tR,MAX_MS)/1000);

    return (
        <div style={{maxWidth:1200,margin:'0 auto',display:'flex',flexDirection:'column',gap:20}}>

            {/* ── 시뮬레이션 영역 ── */}
            <div style={{display:'grid',gridTemplateColumns:'260px 1fr',gap:18}}>

                {/* 컨트롤 패널 */}
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:16}}>
                    <div>
                        <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0',marginBottom:4}}>관성력과 중력</h2>
                        <p style={{color:'#475569',fontSize:12}}>등가 원리 탐구 시뮬레이션</p>
                    </div>

                    {/* 시나리오 선택 */}
                    <div>
                        <label>시나리오 선택</label>
                        <div style={{display:'flex',flexDirection:'column',gap:7,marginTop:4}}>
                            <button className={`scene-btn${scenario===0?' active':''}`} onClick={()=>changeScenario(0)}>
                                <div style={{fontWeight:700,fontSize:13}}>시나리오 1</div>
                                <div style={{fontSize:11,color:scenario===0?'#93c5fd':'#475569',marginTop:2}}>내부 / 외부 관찰자 시점</div>
                            </button>
                            <button className={`scene-btn${scenario===1?' active':''}`} onClick={()=>changeScenario(1)}>
                                <div style={{fontWeight:700,fontSize:13}}>시나리오 2</div>
                                <div style={{fontSize:11,color:scenario===1?'#93c5fd':'#475569',marginTop:2}}>중력 vs 관성력 비교</div>
                            </button>
                        </div>
                    </div>

                    {/* 가속도 슬라이더 */}
                    <div>
                        <label>{scenario===0 ? '우주선 가속도 (a)' : '우주선 가속도 (a, 오른쪽)'}</label>
                        <input type="range" min="1" max="20" step="0.1" value={accel}
                            onChange={e=>{setAccel(parseFloat(e.target.value)); reset();}}/>
                        <p style={{textAlign:'center',fontSize:12,fontFamily:'Space Mono,monospace',color:'#60a5fa',marginTop:4}}>
                            {accel.toFixed(1)} m/s²
                            {scenario===1 && Math.abs(accel-9.8)<0.15 &&
                                <span style={{color:'#a78bfa',marginLeft:8}}>← g와 같음!</span>}
                        </p>
                    </div>

                    {/* 실행 버튼 */}
                    <div style={{display:'flex',flexDirection:'column',gap:8}}>
                        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:6}}>
                            <div style={{display:'flex',flexDirection:'column',gap:4}}>
                                <div style={{fontSize:10,color:scenario===0?'#a78bfa':'#fbbf24',fontWeight:700,textTransform:'uppercase',letterSpacing:'0.05em'}}>
                                    {scenario===0?'내부 시점':'중력(LEFT)'}
                                </div>
                                <button onClick={()=>setRunL(true)} disabled={runL}
                                    style={{padding:'8px 4px',borderRadius:7,background:'rgba(99,102,241,0.1)',color:runL?'#475569':'#a78bfa',border:'1px solid rgba(99,102,241,0.35)',cursor:runL?'default':'pointer',fontSize:12,fontFamily:'inherit',fontWeight:700}}>
                                    ▶ 시작
                                </button>
                                <button onClick={()=>{setRunL(false);setTL(0);}}
                                    style={{padding:'5px',borderRadius:7,background:'transparent',border:'1px solid #1e293b',color:'#475569',cursor:'pointer',fontSize:11,fontFamily:'inherit'}}>
                                    ↺
                                </button>
                            </div>
                            <div style={{display:'flex',flexDirection:'column',gap:4}}>
                                <div style={{fontSize:10,color:scenario===0?'#4ade80':'#4ade80',fontWeight:700,textTransform:'uppercase',letterSpacing:'0.05em'}}>
                                    {scenario===0?'외부 시점':'관성력(RIGHT)'}
                                </div>
                                <button onClick={()=>setRunR(true)} disabled={runR}
                                    style={{padding:'8px 4px',borderRadius:7,background:'rgba(74,222,128,0.1)',color:runR?'#475569':'#4ade80',border:'1px solid rgba(74,222,128,0.35)',cursor:runR?'default':'pointer',fontSize:12,fontFamily:'inherit',fontWeight:700}}>
                                    ▶ 시작
                                </button>
                                <button onClick={()=>{setRunR(false);setTR(0);}}
                                    style={{padding:'5px',borderRadius:7,background:'transparent',border:'1px solid #1e293b',color:'#475569',cursor:'pointer',fontSize:11,fontFamily:'inherit'}}>
                                    ↺
                                </button>
                            </div>
                        </div>
                        <button onClick={syncRun}
                            style={{padding:'9px',borderRadius:8,background:'rgba(167,139,250,0.1)',color:'#c4b5fd',border:'1px solid rgba(167,139,250,0.35)',cursor:'pointer',fontSize:13,fontFamily:'inherit',fontWeight:700}}>
                            ⚡ 동기화 동시 실행
                        </button>
                        <button onClick={reset}
                            style={{padding:'7px',borderRadius:8,background:'transparent',border:'1px solid #1e293b',color:'#64748b',cursor:'pointer',fontSize:12,fontFamily:'inherit'}}>
                            ↺ 전체 초기화
                        </button>
                    </div>

                    {/* 실시간 물리량 */}
                    <div style={{background:'#070b14',borderRadius:10,padding:'10px 14px',border:'1px solid #1e293b'}}>
                        <div className="result-row">
                            <span style={{color:'#64748b',fontSize:12}}>{scenario===0?'내부/거리':'중력/거리'}</span>
                            <span className="result-val" style={{fontSize:12}}>{dL.toFixed(1)} px</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b',fontSize:12}}>{scenario===0?'외부/거리':'관성/거리'}</span>
                            <span className="result-val" style={{color:'#4ade80',fontSize:12}}>{dR.toFixed(1)} px</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b',fontSize:12}}>속도 (LEFT)</span>
                            <span className="result-val" style={{fontSize:12}}>{vL.toFixed(2)} m/s</span>
                        </div>
                        <div className="result-row">
                            <span style={{color:'#64748b',fontSize:12}}>속도 (RIGHT)</span>
                            <span className="result-val" style={{color:'#4ade80',fontSize:12}}>{vR.toFixed(2)} m/s</span>
                        </div>
                        {scenario===0 &&
                        <div className="result-row">
                            <span style={{color:'#64748b',fontSize:12}}>동기화</span>
                            <span className="result-val" style={{color:Math.abs(dL-dR)<2?'#4ade80':'#f87171',fontSize:12}}>
                                {Math.abs(dL-dR)<2?'✓ 일치':'비동기'}
                            </span>
                        </div>}
                    </div>
                </div>

                {/* 캔버스 */}
                <div style={{height:560,borderRadius:16,overflow:'hidden',border:'1px solid #1e293b',background:'#0a0f1e'}}>
                    <SimCanvas scenario={scenario} accel={accel} tL={tL} tR={tR}/>
                </div>
            </div>

            {/* ── 탐구 질문 + 개념 연결 ── */}
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:18}}>
                <div className="card">
                    <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:14}}>
                        <div style={{width:4,height:22,background:'#fbbf24',borderRadius:2}}/>
                        <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0'}}>🔍 탐구 질문</h2>
                    </div>
                    <QnASection/>
                </div>
                <div className="card">
                    <DerivationSection/>
                </div>
            </div>

        </div>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""
    components.html(react_code, height=1800, scrolling=True)

if __name__ == "__main__":
    run_sim()
