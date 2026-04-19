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
.result-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1e293b;font-size:13px;}
.result-row:last-child{border-bottom:none;}
.result-val{color:#60a5fa;font-family:'Space Mono',monospace;font-weight:700;font-size:14px;}
.phase-btn{padding:7px 12px;border-radius:8px;border:1px solid #1e293b;background:#0d1526;color:#94a3b8;cursor:pointer;font-size:12px;font-family:inherit;transition:all 0.2s;text-align:left;width:100%;}
.phase-btn.active{border-color:#3b82f6;background:#1e3a5f;color:#e2e8f0;font-weight:700;}
.phase-btn:hover:not(.active){border-color:#334155;color:#e2e8f0;}
.view-tab{flex:1;padding:7px 6px;border-radius:7px;border:1px solid #1e293b;background:transparent;color:#64748b;cursor:pointer;font-size:11px;font-family:inherit;transition:all 0.2s;font-weight:600;}
.view-tab.active{border-color:#6366f1;background:rgba(99,102,241,0.15);color:#a5b4fc;}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const { useState, useEffect, useRef, useCallback } = React;

const Math_ = ({ f, display=false }) => {
    const ref = useRef(null);
    useEffect(()=>{
        if(ref.current && window.katex)
            window.katex.render(f, ref.current, {throwOnError:false, displayMode:display});
    },[f,display]);
    return <span ref={ref}/>;
};

const SCALE  = 52;
const MAX_MS = 2400;
const physDist = (tMs, a) => {
    const s = Math.min(tMs, MAX_MS) / 1000;
    return 0.5 * a * s * s * SCALE;
};

/* ── 별 배경 ── */
const STARS = Array.from({length:80},(_,i)=>{
    const h=(n)=>{let x=Math.sin(n)*43758.5;return x-Math.floor(x);};
    return{x:h(i*1.1),y:h(i*2.3),r:h(i*3.7)*1.2+0.3,ph:h(i*5.1)*Math.PI*2,sp:0.5+h(i*7.3)};
});
function drawStars(ctx,W,H,t){
    STARS.forEach(s=>{
        const op=0.2+0.45*Math.sin(s.ph+t*s.sp*0.001);
        ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`;ctx.fill();
    });
}
function arrow(ctx,x1,y1,x2,y2,color,lw=2){
    const dx=x2-x1,dy=y2-y1,ang=Math.atan2(dy,dx);
    ctx.save();ctx.strokeStyle=color;ctx.lineWidth=lw;ctx.lineCap='round';
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
    const al=11,aa=0.42;
    ctx.beginPath();
    ctx.moveTo(x2,y2);ctx.lineTo(x2-al*Math.cos(ang-aa),y2-al*Math.sin(ang-aa));
    ctx.moveTo(x2,y2);ctx.lineTo(x2-al*Math.cos(ang+aa),y2-al*Math.sin(ang+aa));
    ctx.stroke();ctx.restore();
}
function txt(ctx,x,y,s,color,size=12,align='center',weight='400'){
    ctx.save();ctx.fillStyle=color;
    ctx.font=`${weight} ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align;ctx.fillText(s,x,y);ctx.restore();
}
function dashedRect(ctx,x,y,w,h,color,r=10){
    ctx.save();ctx.strokeStyle=color;ctx.lineWidth=1;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.stroke();
    ctx.setLineDash([]);ctx.restore();
}
function lblBox(ctx,x,y,s,bg,fc,size=11,align='center'){
    ctx.save();
    ctx.font=`700 ${size}px "Noto Sans KR",sans-serif`;
    ctx.textAlign=align;
    const tw=ctx.measureText(s).width,pad=8,ph=5;
    const bx=align==='center'?x-tw/2-pad:align==='left'?x-pad:x-tw-pad;
    ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(bx,y-size-ph,tw+pad*2,size+ph*2,5);ctx.fill();
    ctx.fillStyle=fc;ctx.fillText(s,x,y);ctx.restore();
}

/* ── 우주선 외부형 ── */
function drawRocketFull(ctx,cx,cy,w,h,thrust=0,flicker=1){
    if(thrust>0){
        const fH=(18+thrust*1.8)*flicker;
        const fg=ctx.createLinearGradient(cx,cy+h/2,cx,cy+h/2+fH);
        fg.addColorStop(0,'rgba(255,210,60,0.95)');fg.addColorStop(0.4,'rgba(255,100,20,0.8)');fg.addColorStop(1,'rgba(255,40,0,0)');
        ctx.beginPath();
        ctx.moveTo(cx-11,cy+h/2-2);
        ctx.quadraticCurveTo(cx-6,cy+h/2+fH*0.6,cx,cy+h/2+fH);
        ctx.quadraticCurveTo(cx+6,cy+h/2+fH*0.6,cx+11,cy+h/2-2);
        ctx.fillStyle=fg;ctx.fill();
    }
    const bg=ctx.createLinearGradient(cx-w/2,0,cx+w/2,0);
    bg.addColorStop(0,'#8aa0c0');bg.addColorStop(0.4,'#d0dff0');bg.addColorStop(0.6,'#e8f0ff');bg.addColorStop(1,'#6080a0');
    ctx.beginPath();ctx.roundRect(cx-w/2,cy-h/2,w,h,w/4);
    ctx.fillStyle=bg;ctx.fill();
    ctx.strokeStyle='rgba(180,200,230,0.4)';ctx.lineWidth=1;ctx.stroke();
    ctx.beginPath();ctx.arc(cx,cy-h/8,w/5,0,Math.PI*2);
    const wg=ctx.createRadialGradient(cx-2,cy-h/8-2,1,cx,cy-h/8,w/5);
    wg.addColorStop(0,'rgba(180,220,255,0.9)');wg.addColorStop(0.7,'rgba(50,120,240,0.6)');wg.addColorStop(1,'rgba(20,60,120,0.8)');
    ctx.fillStyle=wg;ctx.fill();
    ctx.strokeStyle='rgba(200,220,255,0.7)';ctx.lineWidth=1.5;ctx.stroke();
    ctx.beginPath();ctx.arc(cx,cy-h/8,w/5*0.42,0,Math.PI*2);
    ctx.fillStyle='rgba(15,30,70,0.85)';ctx.fill();
    ctx.beginPath();ctx.moveTo(cx-w/2,cy-h/2);
    ctx.quadraticCurveTo(cx,cy-h/2-h*0.25,cx+w/2,cy-h/2);
    ctx.fillStyle='rgba(160,180,210,0.9)';ctx.fill();
    [[-1],[1]].forEach(([d])=>{
        ctx.beginPath();
        ctx.moveTo(cx+d*w/2,cy+h/2-h*0.15);
        ctx.lineTo(cx+d*w/2+d*w*0.38,cy+h/2+h*0.08);
        ctx.lineTo(cx+d*w/2,cy+h/2);
        ctx.fillStyle='rgba(120,150,190,0.8)';ctx.fill();
    });
}

/* ── 우주선 내부 단면 ── */
function drawRocketInterior(ctx,cx,cy,w,h){
    ctx.beginPath();ctx.roundRect(cx-w/2,cy-h/2,w,h,10);
    ctx.fillStyle='rgba(18,28,52,0.95)';ctx.fill();
    ctx.strokeStyle='rgba(100,150,220,0.55)';ctx.lineWidth=2;ctx.stroke();
    ctx.beginPath();ctx.rect(cx-w/2+2,cy+h/2-14,w-4,12);
    ctx.fillStyle='rgba(55,85,140,0.75)';ctx.fill();
    ctx.beginPath();ctx.rect(cx-w/2+2,cy-h/2+2,8,h-18);
    ctx.fillStyle='rgba(35,55,95,0.5)';ctx.fill();
    ctx.beginPath();ctx.rect(cx+w/2-10,cy-h/2+2,8,h-18);
    ctx.fillStyle='rgba(35,55,95,0.5)';ctx.fill();
    ctx.beginPath();ctx.roundRect(cx-14,cy-h/2+10,28,18,4);
    ctx.fillStyle='rgba(100,180,255,0.12)';ctx.fill();
    ctx.strokeStyle='rgba(100,180,255,0.35)';ctx.lineWidth=1;ctx.stroke();
    for(let i=1;i<4;i++){
        ctx.beginPath();
        ctx.moveTo(cx-w/2+2,cy+h/2-14-i*26);
        ctx.lineTo(cx-w/2+10,cy+h/2-14-i*26);
        ctx.strokeStyle=`rgba(100,150,220,${0.12+i*0.04})`;ctx.lineWidth=0.5;ctx.stroke();
    }
}

function drawBall(ctx,x,y,r=11){
    const g=ctx.createRadialGradient(x-r*0.3,y-r*0.3,r*0.1,x,y,r);
    g.addColorStop(0,'#fff8dc');g.addColorStop(0.4,'#ffcc44');g.addColorStop(1,'#b45309');
    ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);
    ctx.fillStyle=g;ctx.fill();
    ctx.strokeStyle='rgba(255,200,80,0.4)';ctx.lineWidth=1;ctx.stroke();
}

/* ════ Phase 0a: 내부 / 외부 관찰자 ════ */
function drawPhase0a(ctx,W,H,accel,tL,tR){
    drawStars(ctx,W,H,tL+tR);
    const rw=100,rh=240,baseCy=H*0.50;
    const ballStartRel=-rh*0.28;
    const dL=physDist(tL,accel);
    const dR=physDist(tR,accel);

    const cx1=W*0.27;
    dashedRect(ctx,cx1-rw/2-12,baseCy-rh/2-34,rw+24,rh+82,'rgba(99,102,241,0.3)');
    lblBox(ctx,cx1,baseCy-rh/2-42,'내부 관찰자 시점','rgba(99,102,241,0.85)','#e0e7ff',11);
    txt(ctx,cx1,baseCy-rh/2-10,'우주선 내부 기준','rgba(180,185,230,0.65)',10);
    drawRocketInterior(ctx,cx1,baseCy+18,rw,rh);
    const bY1=baseCy+18+ballStartRel+dL;
    const flY1=baseCy+18+rh/2-20;
    const hit1=bY1+11>=flY1;
    ctx.save();
    ctx.beginPath();ctx.roundRect(cx1-rw/2+2,baseCy+18-rh/2+2,rw-4,rh-4,8);ctx.clip();
    drawBall(ctx,cx1,hit1?flY1-11:bY1);
    if(!hit1&&dL>6){
        arrow(ctx,cx1,bY1+14,cx1,bY1+38,'rgba(248,113,113,0.9)',2.2);
        lblBox(ctx,cx1+20,bY1+30,'관성력','rgba(248,113,113,0.2)','#fca5a5',10,'left');
    }
    ctx.restore();
    txt(ctx,cx1,baseCy+rh/2+52,`d = ${dL.toFixed(1)} px`,'rgba(248,113,113,0.65)',10);

    const cx2=W*0.73;
    dashedRect(ctx,cx2-rw/2-12,baseCy-rh/2-34,rw+24,rh+82,'rgba(74,222,128,0.3)');
    lblBox(ctx,cx2,baseCy-rh/2-42,'외부 관찰자 시점','rgba(74,222,128,0.85)','#d1fae5',11);
    txt(ctx,cx2,baseCy-rh/2-10,'관성 좌표계 기준','rgba(140,200,160,0.65)',10);
    const rCy2=baseCy+18-dR;
    drawRocketFull(ctx,cx2,rCy2,rw,rh,accel,0.88+0.18*Math.sin(tR*0.018));
    const bAbs2=baseCy+18+ballStartRel;
    drawBall(ctx,cx2,bAbs2);
    if(dR>6){
        arrow(ctx,cx2+rw*0.55,rCy2-28,cx2+rw*0.55,rCy2-64,'rgba(74,222,128,0.9)',2.2);
        lblBox(ctx,cx2+rw*0.55+16,rCy2-46,`a=${accel.toFixed(1)}`,'rgba(74,222,128,0.2)','#6ee7b7',10,'left');
    }
    txt(ctx,cx2,baseCy+rh/2+52,`d = ${dR.toFixed(1)} px`,'rgba(74,222,128,0.65)',10);

    const mx=W/2;
    txt(ctx,mx,baseCy-10,'=','rgba(167,139,250,0.7)',26,'center','800');
    txt(ctx,mx,baseCy+18,'같은 물리 결과','rgba(167,139,250,0.6)',10);
    txt(ctx,mx,baseCy+32,'(s = ½at²)','rgba(167,139,250,0.5)',10);
    if(tL>50&&tR>50){
        const ok=Math.abs(dL-dR)<1.5;
        txt(ctx,mx,baseCy+52,ok?'✓ 동기화됨':'비동기',ok?'rgba(74,222,128,0.8)':'rgba(248,113,113,0.7)',10);
    }
    const qY=baseCy+rh/2+68;
    ctx.save();
    ctx.fillStyle='rgba(10,14,38,0.88)';ctx.strokeStyle='rgba(99,102,241,0.3)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(W*0.07,qY,W*0.86,44,8);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,W/2,qY+16,'두 시점 모두 공과 바닥이 만난다. 어느 시점이 "진짜"인가?','rgba(200,190,255,0.9)',12,'center','600');
    txt(ctx,W/2,qY+32,'→ 둘 다 유효하다. 가속 좌표계와 관성 좌표계는 동등하게 성립한다.','rgba(148,163,184,0.72)',11,'center','400');
}

/* ════ Phase 0b: 중력 vs 관성력 (내부 시점) ════ */
function drawPhase0b(ctx,W,H,accel,tL,tR){
    drawStars(ctx,W,H,tL+tR);
    const rw=100,rh=240,baseCy=H*0.49;
    const ballStartRel=-rh*0.28;
    const dL=physDist(tL,9.8);
    const dR=physDist(tR,accel);

    const cx1=W*0.27;
    dashedRect(ctx,cx1-rw/2-12,baseCy-rh/2-34,rw+24,rh+100,'rgba(255,179,71,0.28)');
    lblBox(ctx,cx1,baseCy-rh/2-42,'중력장 (지구 표면)','rgba(255,179,71,0.85)','#fef3c7',11);
    txt(ctx,cx1,baseCy-rh/2-10,'내부 관찰자 시점','rgba(200,170,100,0.65)',10);
    const eY=baseCy+rh/2+36;
    const eg=ctx.createRadialGradient(cx1-5,eY-5,3,cx1,eY,22);
    eg.addColorStop(0,'#5090e0');eg.addColorStop(0.6,'#2060b0');eg.addColorStop(1,'#0a3060');
    ctx.beginPath();ctx.arc(cx1,eY,22,0,Math.PI*2);ctx.fillStyle=eg;ctx.fill();
    ctx.strokeStyle='rgba(100,180,255,0.4)';ctx.lineWidth=1.5;ctx.stroke();
    txt(ctx,cx1,eY+5,'지구','rgba(180,210,255,0.8)',10);
    drawRocketInterior(ctx,cx1,baseCy+18,rw,rh);
    const bY1=baseCy+18+ballStartRel+dL;
    const flY1=baseCy+18+rh/2-20;
    const hit1=bY1+11>=flY1;
    ctx.save();
    ctx.beginPath();ctx.roundRect(cx1-rw/2+2,baseCy+18-rh/2+2,rw-4,rh-4,8);ctx.clip();
    drawBall(ctx,cx1,hit1?flY1-11:bY1);
    if(!hit1&&dL>6){
        arrow(ctx,cx1,(hit1?flY1-11:bY1)+14,cx1,(hit1?flY1-11:bY1)+40,'rgba(255,179,71,0.9)',2.5);
        lblBox(ctx,cx1+20,(hit1?flY1-11:bY1)+30,'F = mg','rgba(255,179,71,0.2)','#fcd34d',11,'left');
    }
    ctx.restore();
    txt(ctx,cx1,baseCy+rh/2+62,`v = ${(9.8*Math.min(tL,MAX_MS)/1000).toFixed(2)} m/s`,'rgba(255,179,71,0.65)',10);

    const cx2=W*0.73;
    dashedRect(ctx,cx2-rw/2-12,baseCy-rh/2-34,rw+24,rh+100,'rgba(74,222,128,0.28)');
    lblBox(ctx,cx2,baseCy-rh/2-42,'가속 우주선 (무중력)','rgba(74,222,128,0.85)','#d1fae5',11);
    txt(ctx,cx2,baseCy-rh/2-10,'내부 관찰자 시점','rgba(140,200,160,0.65)',10);
    arrow(ctx,cx2+rw/2+18,baseCy+rh/2-10,cx2+rw/2+18,baseCy-rh/2+10,'rgba(74,222,128,0.7)',2);
    lblBox(ctx,cx2+rw/2+32,baseCy,`a=${accel.toFixed(1)}`,'rgba(74,222,128,0.18)','#6ee7b7',10,'left');
    drawRocketInterior(ctx,cx2,baseCy+18,rw,rh);
    const bY2=baseCy+18+ballStartRel+dR;
    const flY2=baseCy+18+rh/2-20;
    const hit2=bY2+11>=flY2;
    ctx.save();
    ctx.beginPath();ctx.roundRect(cx2-rw/2+2,baseCy+18-rh/2+2,rw-4,rh-4,8);ctx.clip();
    drawBall(ctx,cx2,hit2?flY2-11:bY2);
    if(!hit2&&dR>6){
        arrow(ctx,cx2,(hit2?flY2-11:bY2)+14,cx2,(hit2?flY2-11:bY2)+40,'rgba(248,113,113,0.9)',2.5);
        lblBox(ctx,cx2+20,(hit2?flY2-11:bY2)+30,'F관성 = ma','rgba(248,113,113,0.2)','#fca5a5',11,'left');
    }
    ctx.restore();
    txt(ctx,cx2,baseCy+rh/2+62,`v = ${(accel*Math.min(tR,MAX_MS)/1000).toFixed(2)} m/s`,'rgba(74,222,128,0.65)',10);

    const mx=W/2;
    const sameA=Math.abs(accel-9.8)<0.2;
    if(sameA){
        const p=0.65+0.35*Math.sin((tL+tR)*0.004);
        ctx.save();ctx.globalAlpha=p;
        txt(ctx,mx,baseCy-4,'≡','rgba(167,139,250,0.95)',32,'center','800');
        ctx.restore();
        txt(ctx,mx,baseCy+28,'내부에서','rgba(167,139,250,0.8)',11);
        txt(ctx,mx,baseCy+42,'구별 불가!','rgba(167,139,250,0.8)',11);
        ctx.save();
        ctx.fillStyle='rgba(167,139,250,0.07)';ctx.strokeStyle='rgba(167,139,250,0.22)';ctx.lineWidth=0.5;
        ctx.beginPath();ctx.roundRect(mx-55,baseCy-28,110,90,8);ctx.fill();ctx.stroke();ctx.restore();
    } else {
        txt(ctx,mx,baseCy-4,'비교 중','rgba(167,139,250,0.55)',10);
        txt(ctx,mx,baseCy+14,`a=${accel.toFixed(1)} ≠ g`,'rgba(248,113,113,0.6)',10);
    }
    const qY=baseCy+rh/2+78;
    ctx.save();
    ctx.fillStyle='rgba(10,14,38,0.88)';ctx.strokeStyle='rgba(167,139,250,0.3)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(W*0.07,qY,W*0.86,44,8);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,W/2,qY+15,'🔍 내부 관찰자는 두 상황(중력 vs 관성력)을 구별할 수 있는가?','rgba(255,220,80,0.9)',12,'center','700');
    txt(ctx,W/2,qY+32,'가속도 슬라이더를 9.8 m/s²에 맞추면 두 상황이 물리적으로 완전히 동일해진다.','rgba(148,163,184,0.72)',11,'center','400');
}

/* ════ Phase 1: 빛의 경로 — 4가지 운동 상황 × 내부/외부 시점 ════ */
const SIT_CFG=[
    {name:'정지',  color:'rgba(255,255,100,0.85)',border:'rgba(255,255,100,0.3)', thrust:0,  speedDir:0,  bendFactor:0,  extSpd:0  },
    {name:'등속',  color:'rgba(100,200,255,0.85)',border:'rgba(100,200,255,0.3)', thrust:0,  speedDir:1,  bendFactor:0,  extSpd:1  },
    {name:'가속',  color:'rgba(248,113,113,0.85)',border:'rgba(248,113,113,0.3)', thrust:1,  speedDir:1,  bendFactor:1,  extSpd:2  },
    {name:'감속',  color:'rgba(167,139,250,0.85)',border:'rgba(167,139,250,0.3)', thrust:0,  speedDir:-1, bendFactor:-1, extSpd:0.5},
];

function drawLightBeam(ctx,xs,xe,y,bendPx,lProg,clip){
    if(lProg<=0) return;
    if(clip){ctx.save();ctx.beginPath();ctx.rect(clip.x,clip.y,clip.w,clip.h);ctx.clip();}
    ctx.shadowColor='rgba(255,255,100,0.7)';ctx.shadowBlur=7;
    ctx.strokeStyle='rgba(255,255,100,0.95)';ctx.lineWidth=2.5;
    ctx.beginPath();
    const steps=60;
    for(let i=0;i<=steps*Math.min(lProg,1);i++){
        const f=i/steps,px=xs+(xe-xs)*f;
        const py=bendPx===0?y:y+f*f*bendPx;
        if(i===0)ctx.moveTo(px,py);else ctx.lineTo(px,py);
    }
    ctx.stroke();
    if(bendPx!==0){
        ctx.shadowBlur=0;ctx.strokeStyle='rgba(255,255,100,0.18)';ctx.lineWidth=1;ctx.setLineDash([4,4]);
        ctx.beginPath();ctx.moveTo(xs,y);ctx.lineTo(xs+(xe-xs)*Math.min(lProg,1),y);ctx.stroke();ctx.setLineDash([]);
    }
    ctx.shadowBlur=0;
    if(clip)ctx.restore();
}

function drawLightParticle(ctx,xs,xe,y,bendPx,lProg){
    if(lProg<=0||lProg>=0.98)return;
    const f=lProg,px=xs+(xe-xs)*f,py=bendPx===0?y:y+f*f*bendPx;
    ctx.beginPath();ctx.arc(px,py,5,0,Math.PI*2);
    ctx.fillStyle='rgba(255,255,150,1)';
    ctx.shadowColor='rgba(255,255,100,0.9)';ctx.shadowBlur=12;ctx.fill();ctx.shadowBlur=0;
}

function drawMotionTrail(ctx,cx,cy,rh,dir,t,spd){
    if(dir===0||spd===0)return;
    ctx.save();
    for(let i=0;i<6;i++){
        const off=((t*spd*0.05+i*28)%180);
        const sy=dir>0?cy+rh/2+off:cy-rh/2-off;
        const op=0.12+0.22*(i/6);
        ctx.beginPath();ctx.arc(cx+(i%3-1)*12,sy,1.2,0,Math.PI*2);
        ctx.fillStyle=`rgba(255,255,255,${op})`;ctx.fill();
        ctx.beginPath();ctx.moveTo(cx+(i%3-1)*12,sy);ctx.lineTo(cx+(i%3-1)*12,sy+dir*7);
        ctx.strokeStyle=`rgba(255,255,255,${op*0.5})`;ctx.lineWidth=0.5;ctx.stroke();
    }
    ctx.restore();
}

function drawSitPanel(ctx,cx,cy,rw,rh,cfg,viewMode,lProg,accel,t){
    const isInside=viewMode===0;
    const bendAmt=cfg.bendFactor*(accel/9.8)*22;
    dashedRect(ctx,cx-rw/2-10,cy-rh/2-36,rw+20,rh+82,cfg.border);
    lblBox(ctx,cx,cy-rh/2-44,cfg.name+' 좌표계',cfg.border.replace('0.3','0.82'),'#e2e8f0',11);
    txt(ctx,cx,cy-rh/2-10,isInside?'내부 관찰자':'외부 관찰자','rgba(160,170,200,0.7)',10);

    if(isInside){
        drawRocketInterior(ctx,cx,cy,rw,rh);
        const lxS=cx-rw*0.38,lxE=cx+rw*0.38,lyB=cy-rh*0.1;
        drawLightBeam(ctx,lxS,lxE,lyB,bendAmt,lProg,{x:cx-rw/2,y:cy-rh/2,w:rw,h:rh});
        drawLightParticle(ctx,lxS,lxE,lyB,bendAmt,lProg);
        if(lProg>0.85&&bendAmt!==0){
            const endY=lyB+bendAmt;
            ctx.save();ctx.strokeStyle=bendAmt>0?'rgba(248,113,113,0.6)':'rgba(167,139,250,0.6)';
            ctx.lineWidth=1;ctx.setLineDash([2,3]);
            ctx.beginPath();ctx.moveTo(lxE,lyB);ctx.lineTo(lxE,endY);ctx.stroke();ctx.setLineDash([]);
            txt(ctx,lxE+12,(lyB+endY)/2,`Δy=${Math.abs(bendAmt).toFixed(0)}`,bendAmt>0?'rgba(248,113,113,0.8)':'rgba(167,139,250,0.8)',9,'left');
            ctx.restore();
        }
        const ldesc=bendAmt===0?'빛: 직진':(bendAmt>0?'빛: 아래로 휨':'빛: 위로 휨');
        const lclr=bendAmt===0?'rgba(255,255,100,0.75)':(bendAmt>0?'rgba(248,113,113,0.85)':'rgba(167,139,250,0.85)');
        txt(ctx,cx,cy+rh/2+20,ldesc,lclr,11,'center','700');
    } else {
        const tSec=t/1000;
        let offY=0;
        if(cfg.name==='등속')offY=-((tSec*28)%(rh*0.5));
        else if(cfg.name==='가속')offY=-(Math.min(0.5*(accel/9.8)*tSec*tSec*16,rh*0.55));
        else if(cfg.name==='감속')offY=Math.min(tSec*18,rh*0.28);
        const rCy=cy+offY;
        if(cfg.name==='등속'||cfg.name==='가속')drawMotionTrail(ctx,cx,rCy,rh,-1,t,cfg.name==='가속'?2:1);
        else if(cfg.name==='감속')drawMotionTrail(ctx,cx,rCy,rh,1,t,0.5);
        const thr=cfg.name==='가속'?accel:(cfg.name==='등속'?accel*0.28:0);
        drawRocketFull(ctx,cx,rCy,rw*0.85,rh*0.85,thr,0.88+0.22*Math.sin(t*0.02));
        if(cfg.name==='가속'){
            arrow(ctx,cx+rw*0.5,rCy-18,cx+rw*0.5,rCy-50,'rgba(248,113,113,0.9)',2);
            lblBox(ctx,cx+rw*0.5+14,rCy-34,`a=${accel.toFixed(1)}`,'rgba(248,113,113,0.2)','#fca5a5',9,'left');
        } else if(cfg.name==='등속'){
            arrow(ctx,cx+rw*0.5,rCy-18,cx+rw*0.5,rCy-46,'rgba(100,200,255,0.9)',2);
            lblBox(ctx,cx+rw*0.5+14,rCy-32,'v=일정','rgba(100,200,255,0.2)','#93c5fd',9,'left');
        } else if(cfg.name==='감속'){
            arrow(ctx,cx+rw*0.5,rCy+18,cx+rw*0.5,rCy+46,'rgba(167,139,250,0.9)',2);
            lblBox(ctx,cx+rw*0.5+14,rCy+32,'a↓감속','rgba(167,139,250,0.2)','#c4b5fd',9,'left');
        }
        const absLY=cy-rh*0.1;
        const lxS=cx-rw*0.42,lxE=cx+rw*0.42;
        ctx.save();ctx.shadowColor='rgba(255,255,100,0.7)';ctx.shadowBlur=7;
        ctx.strokeStyle='rgba(255,255,100,0.9)';ctx.lineWidth=2.5;
        ctx.beginPath();ctx.moveTo(lxS,absLY);ctx.lineTo(lxS+(lxE-lxS)*Math.min(lProg,1),absLY);ctx.stroke();ctx.restore();
        if(lProg>0&&lProg<0.98){
            const px=lxS+(lxE-lxS)*lProg;
            ctx.beginPath();ctx.arc(px,absLY,5,0,Math.PI*2);
            ctx.fillStyle='rgba(255,255,150,1)';
            ctx.shadowColor='rgba(255,255,100,0.9)';ctx.shadowBlur=12;ctx.fill();ctx.shadowBlur=0;
        }
        txt(ctx,cx,cy+rh/2+20,'빛: 직진 (관성계)','rgba(255,255,100,0.7)',11,'center','700');
    }
    const sumTbl={
        '정지':{i:'빛 직진, 우주선 정지',o:'빛 직진, 우주선 정지'},
        '등속':{i:'빛 직진, 관찰자 등속',o:'빛 직진, 우주선 등속'},
        '가속':{i:'빛 아래로 휨 (관성력)',o:'빛 직진, 우주선 가속'},
        '감속':{i:'빛 위로 휨 (관성력↑)',o:'빛 직진, 우주선 감속'},
    };
    const sr=sumTbl[cfg.name]||{i:'',o:''};
    txt(ctx,cx,cy+rh/2+36,isInside?sr.i:sr.o,'rgba(148,163,184,0.7)',9,'center');
}

function drawPhase1(ctx,W,H,accel,t,running,p1Sit){
    drawStars(ctx,W,H,t);
    const cfg=SIT_CFG[p1Sit||0];
    const lProg=running?Math.min((t%3000)/3000,1):0;
    const rw=Math.min(W*0.32,180),rh=Math.min(H*0.62,300);
    const cy=H*0.48,cx1=W*0.27,cx2=W*0.73;

    drawSitPanel(ctx,cx1,cy,rw,rh,cfg,0,lProg,accel,t);
    drawSitPanel(ctx,cx2,cy,rw,rh,cfg,1,lProg,accel,t);

    const cx=W/2;
    txt(ctx,cx,cy-22,'내부 vs 외부','rgba(148,163,184,0.5)',10,'center','700');
    txt(ctx,cx,cy-4,'같은 빛,','rgba(167,139,250,0.7)',11,'center','700');
    txt(ctx,cx,cy+12,'다른 관찰','rgba(167,139,250,0.7)',11,'center','700');

    /* ── 하단 논리 전개 배너 ── */
    const sit=p1Sit||0;
    if(sit===0||sit===1){
        /* 정지/등속: 단순 결론 */
        if(lProg>0.5){
            const msg=sit===0
                ?'정지 좌표계: 내부/외부 모두 빛이 직진 → 관찰자 위치와 무관'
                :'등속 좌표계: 내부/외부 모두 빛이 직진 → 갈릴레이 상대성 원리 확인';
            ctx.save();
            ctx.fillStyle='rgba(10,14,38,0.9)';ctx.strokeStyle='rgba(100,200,255,0.3)';ctx.lineWidth=1;
            ctx.beginPath();ctx.roundRect(W*0.1,H-52,W*0.8,36,8);ctx.fill();ctx.stroke();ctx.restore();
            txt(ctx,W/2,H-30,msg,'rgba(100,200,255,0.85)',11,'center','600');
        }
    } else if(sit===2){
        /* 가속: 3단계 논리 전개 박스 */
        const boxH=lProg>0.85?128:lProg>0.65?86:lProg>0.45?46:0;
        if(boxH>0){
            const bY=H-boxH-8;
            ctx.save();
            ctx.fillStyle='rgba(8,12,30,0.94)';ctx.strokeStyle='rgba(248,113,113,0.45)';ctx.lineWidth=1;
            ctx.beginPath();ctx.roundRect(W*0.04,bY,W*0.92,boxH,9);ctx.fill();ctx.stroke();ctx.restore();

            /* 질문 1 (lProg > 0.45) */
            txt(ctx,W*0.04+14,bY+18,'Q1.','rgba(255,200,80,0.9)',11,'left','800');
            txt(ctx,W*0.04+40,bY+18,'가속 좌표계에서 빛이 아래로 휜다 → 그렇다면 중력장에서도 빛이 아래로 휘어야 하지 않는가?','rgba(255,220,120,0.9)',11,'left','600');

            if(lProg>0.65){
                /* 질문 2 */
                txt(ctx,W*0.04+14,bY+42,'Q2.','rgba(248,113,113,0.9)',11,'left','800');
                txt(ctx,W*0.04+40,bY+42,'뉴턴의 중력 F = GMm/r²  →  빛의 질량 m = 0 이면 F = 0 → 빛은 힘을 받지 않아야 함','rgba(248,140,130,0.85)',11,'left','600');
                txt(ctx,W*0.04+14,bY+58,'→ 뉴턴 역학은 빛의 휨을 설명할 수 없다!','rgba(248,113,113,0.9)',11,'left','700');
            }

            if(lProg>0.85){
                /* 결론 */
                ctx.save();
                ctx.fillStyle='rgba(99,102,241,0.12)';ctx.strokeStyle='rgba(167,139,250,0.4)';ctx.lineWidth=0.5;
                ctx.beginPath();ctx.roundRect(W*0.04+6,bY+72,W*0.92-12,48,6);ctx.fill();ctx.stroke();ctx.restore();
                txt(ctx,W*0.04+14,bY+88,'결론.','rgba(167,139,250,0.95)',11,'left','800');
                txt(ctx,W*0.04+50,bY+88,'중력을 "두 질량 사이의 힘"으로 보는 한, 질량 없는 빛의 휨은 설명 불가','rgba(200,190,255,0.88)',11,'left','600');
                txt(ctx,W*0.04+50,bY+106,'→ 중력 = 질량에 의한 시공간 곡률 로 재해석해야만 빛의 휨이 자연스럽게 도출된다','rgba(167,139,250,0.9)',11,'left','700');
            }
        }
    } else if(sit===3){
        /* 감속 */
        if(lProg>0.5){
            ctx.save();
            ctx.fillStyle='rgba(10,14,38,0.9)';ctx.strokeStyle='rgba(167,139,250,0.35)';ctx.lineWidth=1;
            ctx.beginPath();ctx.roundRect(W*0.1,H-52,W*0.8,36,8);ctx.fill();ctx.stroke();ctx.restore();
            txt(ctx,W/2,H-30,'감속 좌표계: 빛이 위로 휨 → 가속도 방향에 따라 휨 방향도 바뀐다 (등가 원리 적용)','rgba(167,139,250,0.85)',11,'center','600');
        }
    }
}

/* ════ Phase 2: 등가 원리 다이어그램 ════ */
function drawPhase2(ctx,W,H,accel,t,running){
    drawStars(ctx,W,H,t);
    const cx=W/2,cy=H*0.47;
    const bw=W*0.72,bh=H*0.72;
    ctx.save();
    ctx.strokeStyle='rgba(167,139,250,0.35)';ctx.lineWidth=1.5;ctx.setLineDash([7,5]);
    ctx.beginPath();ctx.roundRect(cx-bw/2,cy-bh/2,bw,bh,14);ctx.stroke();
    ctx.setLineDash([]);ctx.restore();
    txt(ctx,cx,cy-bh/2-20,'등가 원리 (Equivalence Principle)','rgba(167,139,250,0.9)',15,'center','800');
    const lx=cx-bw*0.26,rx=cx+bw*0.26,iw=bw*0.36,ih=bh*0.76;
    ctx.save();
    ctx.fillStyle='rgba(255,179,71,0.06)';ctx.strokeStyle='rgba(255,179,71,0.3)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(lx-iw/2,cy-ih/2,iw,ih,10);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,lx,cy-ih*0.35,'중력장 (g)','rgba(255,179,71,0.9)',14,'center','700');
    txt(ctx,lx,cy-ih*0.18,'공이 바닥으로 낙하','rgba(200,180,120,0.8)',12);
    txt(ctx,lx,cy-ih*0.06,'빛이 아래로 휜다','rgba(200,180,120,0.8)',12);
    const bY2l=cy+ih*0.1;
    ctx.beginPath();ctx.arc(lx,bY2l,8,0,Math.PI*2);
    const g1=ctx.createRadialGradient(lx-2,bY2l-2,1,lx,bY2l,8);
    g1.addColorStop(0,'#fff8dc');g1.addColorStop(1,'#cc8800');
    ctx.fillStyle=g1;ctx.fill();
    arrow(ctx,lx,bY2l+10,lx,bY2l+26,'rgba(255,179,71,0.8)',1.5);
    txt(ctx,lx,cy+ih*0.35,'F = mg','rgba(255,179,71,0.6)',13,'center','700');
    ctx.save();
    ctx.fillStyle='rgba(74,222,128,0.06)';ctx.strokeStyle='rgba(74,222,128,0.3)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(rx-iw/2,cy-ih/2,iw,ih,10);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,rx,cy-ih*0.35,'가속 좌표계 (a=g)','rgba(74,222,128,0.9)',14,'center','700');
    txt(ctx,rx,cy-ih*0.18,'공이 바닥으로 낙하','rgba(140,200,160,0.8)',12);
    txt(ctx,rx,cy-ih*0.06,'빛이 아래로 휜다','rgba(140,200,160,0.8)',12);
    ctx.beginPath();ctx.arc(rx,bY2l,8,0,Math.PI*2);
    const g2=ctx.createRadialGradient(rx-2,bY2l-2,1,rx,bY2l,8);
    g2.addColorStop(0,'#f0fff4');g2.addColorStop(1,'#16a34a');
    ctx.fillStyle=g2;ctx.fill();
    arrow(ctx,rx,bY2l+10,rx,bY2l+26,'rgba(74,222,128,0.8)',1.5);
    txt(ctx,rx,cy+ih*0.35,'F = ma','rgba(74,222,128,0.6)',13,'center','700');
    const pulse=0.7+0.3*Math.sin(t*0.005);
    ctx.save();ctx.globalAlpha=pulse;
    txt(ctx,cx,cy+ih*0.08,'≡','rgba(167,139,250,0.9)',38,'center','800');
    txt(ctx,cx,cy+ih*0.24,'물리적으로 동등','rgba(167,139,250,0.75)',12);
    ctx.restore();
    ctx.save();
    ctx.fillStyle='rgba(167,139,250,0.08)';ctx.strokeStyle='rgba(167,139,250,0.25)';ctx.lineWidth=0.5;
    ctx.beginPath();ctx.roundRect(cx-bw*0.44,cy+bh/2-44,bw*0.88,38,7);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,cx,cy+bh/2-21,'관측만으로 구별 불가 → 중력을 힘이 아닌 시공간의 기하학으로 재해석해야 한다','rgba(200,190,255,0.9)',12,'center','600');
}

/* ════ Phase 3: 시공간 곡률 ════ */
function drawPhase3(ctx,W,H,accel,t,running){
    const cx=W/2,cy=H*0.46;
    drawStars(ctx,W,H,t);
    const massR=34+(accel/9.8)*8;
    const massStr=160*(accel/9.8);
    const step=46,cols=Math.ceil(W/step)+2,rows=Math.ceil(H*0.82/step)+2;
    ctx.save();ctx.strokeStyle='rgba(100,160,255,0.14)';ctx.lineWidth=0.8;
    const gOY=H*0.07;
    for(let r=0;r<rows;r++){
        ctx.beginPath();
        for(let c=0;c<=cols;c++){
            const gx=c*step-step,gy=r*step+gOY,dx=gx-cx,dy=gy-cy,dist=Math.sqrt(dx*dx+dy*dy);
            const w2=massStr/(dist+55);
            if(c===0)ctx.moveTo(gx-dx*w2/(dist+55),gy-dy*w2/(dist+55));
            else ctx.lineTo(gx-dx*w2/(dist+55),gy-dy*w2/(dist+55));
        }
        ctx.stroke();
    }
    for(let c=0;c<cols;c++){
        ctx.beginPath();
        for(let r=0;r<=rows;r++){
            const gx=c*step-step,gy=r*step+gOY,dx=gx-cx,dy=gy-cy,dist=Math.sqrt(dx*dx+dy*dy);
            const w2=massStr/(dist+55);
            if(r===0)ctx.moveTo(gx-dx*w2/(dist+55),gy-dy*w2/(dist+55));
            else ctx.lineTo(gx-dx*w2/(dist+55),gy-dy*w2/(dist+55));
        }
        ctx.stroke();
    }
    ctx.restore();
    const mg=ctx.createRadialGradient(cx-8,cy-8,4,cx,cy,massR);
    mg.addColorStop(0,'rgba(200,180,80,0.95)');mg.addColorStop(0.5,'rgba(140,100,40,0.85)');mg.addColorStop(1,'rgba(60,40,10,0.7)');
    ctx.beginPath();ctx.arc(cx,cy,massR,0,Math.PI*2);ctx.fillStyle=mg;ctx.fill();
    ctx.strokeStyle='rgba(255,200,80,0.35)';ctx.lineWidth=1.5;ctx.stroke();
    txt(ctx,cx,cy+6,'M','rgba(255,220,100,0.9)',18,'center','700');
    txt(ctx,cx,cy+massR+17,`질량 M (중력: ${accel.toFixed(1)}×)`,'rgba(200,180,100,0.65)',11);
    const lProg=running?((t%5000)/5000):0.85;
    const lx1=W*0.04,lx2=W*0.96,ly0=cy-H*0.27;
    ctx.save();
    ctx.strokeStyle='rgba(255,255,100,0.92)';ctx.lineWidth=2.5;
    ctx.shadowColor='rgba(255,255,100,0.55)';ctx.shadowBlur=6;
    ctx.beginPath();
    for(let i=0;i<=200*lProg;i++){
        const frac=i/200,lx=lx1+(lx2-lx1)*frac;
        const dx=lx-cx,dy=ly0-cy,dist=Math.sqrt(dx*dx+dy*dy);
        const defl=(massStr*0.65)/(dist+48);
        const ly=ly0+defl*(1-Math.abs(lx-cx)/(lx2-lx1)*0.75);
        if(i===0)ctx.moveTo(lx,ly);else ctx.lineTo(lx,ly);
    }
    ctx.stroke();ctx.restore();
    ctx.save();ctx.strokeStyle='rgba(255,255,100,0.17)';ctx.lineWidth=1;ctx.setLineDash([5,5]);
    ctx.beginPath();ctx.moveTo(lx1,ly0);ctx.lineTo(lx2,ly0);ctx.stroke();ctx.setLineDash([]);ctx.restore();
    if(running&&lProg<0.98){
        const frac=lProg,lx=lx1+(lx2-lx1)*frac;
        const dx=lx-cx,dy=ly0-cy,dist=Math.sqrt(dx*dx+dy*dy);
        const defl=(massStr*0.65)/(dist+48);
        const ly=ly0+defl*(1-Math.abs(lx-cx)/(lx2-lx1)*0.75);
        ctx.beginPath();ctx.arc(lx,ly,5,0,Math.PI*2);
        ctx.fillStyle='rgba(255,255,150,1)';
        ctx.shadowColor='rgba(255,255,100,0.9)';ctx.shadowBlur=14;ctx.fill();ctx.shadowBlur=0;
    }
    txt(ctx,lx1+40,ly0-14,'빛 (기준 직선)','rgba(255,255,100,0.28)',11,'left');
    txt(ctx,lx1+40,ly0+32,'실제 빛 경로 (시공간이 휘어짐)','rgba(255,255,100,0.9)',11,'left');
    ctx.save();
    ctx.fillStyle='rgba(10,14,38,0.9)';ctx.strokeStyle='rgba(248,113,113,0.4)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(W*0.03,H*0.68,W*0.43,80,9);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,W*0.03+12,H*0.68+18,'뉴턴 역학의 한계:','rgba(248,113,113,0.9)',12,'left','700');
    txt(ctx,W*0.03+12,H*0.68+36,'F = GMm/r²  →  m=0 이면 F=0','rgba(248,113,113,0.75)',11,'left');
    txt(ctx,W*0.03+12,H*0.68+52,'빛은 질량이 없으므로 중력을 받지 않아야 함','rgba(248,113,113,0.7)',11,'left');
    txt(ctx,W*0.03+12,H*0.68+68,'→ 뉴턴으로 빛의 휨을 설명 불가!','rgba(248,113,113,0.55)',10,'left');
    ctx.save();
    ctx.fillStyle='rgba(10,14,38,0.9)';ctx.strokeStyle='rgba(167,139,250,0.4)';ctx.lineWidth=1;
    ctx.beginPath();ctx.roundRect(W*0.55,H*0.68,W*0.42,80,9);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,W*0.55+12,H*0.68+18,'아인슈타인의 해결:','rgba(167,139,250,0.9)',12,'left','700');
    txt(ctx,W*0.55+12,H*0.68+36,'빛은 직진 — 공간 자체가 휘어짐','rgba(200,190,255,0.8)',11,'left');
    txt(ctx,W*0.55+12,H*0.68+52,'질량이 시공간 기하를 변형시킴','rgba(200,190,255,0.8)',11,'left');
    txt(ctx,W*0.55+12,H*0.68+68,'G_μν = (8πG/c⁴) T_μν','rgba(167,139,250,0.65)',11,'left');
    ctx.save();
    ctx.fillStyle='rgba(10,14,38,0.85)';ctx.strokeStyle='rgba(255,200,80,0.3)';ctx.lineWidth=0.8;
    ctx.beginPath();ctx.roundRect(W*0.2,H*0.88,W*0.6,40,8);ctx.fill();ctx.stroke();ctx.restore();
    txt(ctx,W/2,H*0.88+14,'1919년 에딩턴 일식 관측: 태양 근처 별빛 편향 1.75″ 검증','rgba(255,200,80,0.88)',11,'center','700');
    txt(ctx,W/2,H*0.88+28,'뉴턴 예측 0.875″  vs  아인슈타인 예측 1.75″  →  실측 = 1.75″ (아인슈타인 승리)','rgba(220,200,160,0.65)',10,'center');
}

/* ════ 캔버스 컴포넌트 ════ */
const SimCanvas = ({ phase, subView, p1Sit, accel, t, running, tL, tR }) => {
    const ref = useRef(null);
    const draw = useCallback(()=>{
        const canvas=ref.current;if(!canvas)return;
        const ctx=canvas.getContext('2d');
        const W=canvas.width,H=canvas.height;
        ctx.clearRect(0,0,W,H);
        ctx.fillStyle='#0a0f1e';ctx.fillRect(0,0,W,H);
        if(phase===0){
            if(subView===0)drawPhase0a(ctx,W,H,accel,tL,tR);
            else           drawPhase0b(ctx,W,H,accel,tL,tR);
        }
        else if(phase===1)drawPhase1(ctx,W,H,accel,t,running,p1Sit);
        else if(phase===2)drawPhase2(ctx,W,H,accel,t,running);
        else if(phase===3)drawPhase3(ctx,W,H,accel,t,running);
    },[phase,subView,p1Sit,accel,t,running,tL,tR]);
    useEffect(()=>{
        const canvas=ref.current;if(!canvas)return;
        const ro=new ResizeObserver(()=>{canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;draw();});
        ro.observe(canvas);canvas.width=canvas.offsetWidth;canvas.height=canvas.offsetHeight;draw();
        return()=>ro.disconnect();
    },[]);
    useEffect(()=>{draw();},[draw]);
    return <canvas ref={ref} style={{width:'100%',height:'100%',display:'block'}}/>;
};

/* ════ QnA ════ */
const QNA_ITEMS = [
    {q:'내부 vs 외부 관찰자 — 어느 쪽이 옳은가?',a:'둘 다 옳습니다. 내부(가속 좌표계)에서는 공이 관성력에 의해 낙하하고, 외부(관성 좌표계)에서는 공이 정지한 채 우주선 바닥이 올라옵니다. 두 기술은 다르게 보이지만 동일한 물리 결과(공과 바닥의 충돌)를 예측하며, s = ½at² 공식으로 완전히 동기화됩니다.'},
    {q:'중력과 관성력을 내부 관찰자가 구별할 수 없는 이유는?',a:'중력(F = mg)과 관성력(F = ma, a=g)은 크기·방향이 완전히 동일합니다. 공 낙하, 저울, 빛의 경로 등 어떤 실험을 해도 두 상황을 구별할 방법이 없습니다. 이것이 아인슈타인의 등가 원리입니다.'},
    {q:'가속 좌표계에서 빛이 휘는 이유? 뉴턴으로 설명할 수 있는가?',a:'가속하는 동안 빛이 통과하므로 내부 관찰자에게 빛은 포물선으로 처져 보입니다. 뉴턴의 중력 F=GMm/r²에서 빛의 질량 m=0이면 F=0이 되어, 뉴턴 역학으로는 빛이 전혀 휘지 않아야 합니다. 그러나 등가 원리에 의해 중력장에서도 빛은 반드시 휘어야 합니다.'},
    {q:'아인슈타인은 빛의 휨을 어떻게 설명했는가?',a:'아인슈타인은 등가 원리를 출발점으로, 중력을 시공간 자체의 곡률로 재해석했습니다. 질량이 시공간을 휘게 하고, 빛은 그 휘어진 시공간에서 가장 짧은 경로(측지선)를 따라 "직진"합니다. 1919년 에딩턴의 일식 관측에서 태양 근처 별빛 편향이 1.75초각으로 확인되어 아인슈타인의 예측이 검증되었습니다.'},
];
const QnA = ({ items }) => {
    const [open, setOpen] = useState(null);
    return (
        <div style={{display:'flex',flexDirection:'column',gap:10}}>
            {items.map((item,i)=>(
                <div key={i} style={{borderRadius:13,border:`1px solid ${open===i?'#3b82f6':'#1e293b'}`,overflow:'hidden',background:'#070b14',transition:'border-color 0.2s'}}>
                    <button onClick={()=>setOpen(open===i?null:i)}
                        style={{width:'100%',display:'flex',alignItems:'flex-start',gap:12,padding:'14px 18px',background:'transparent',border:'none',cursor:'pointer',textAlign:'left',fontFamily:'inherit'}}>
                        <span style={{color:'#6366f1',fontWeight:800,fontSize:15,flexShrink:0,marginTop:1}}>Q{i+1}.</span>
                        <span style={{color:'#cbd5e1',fontSize:14,lineHeight:1.65,flex:1}}>{item.q}</span>
                        <span style={{color:'#475569',fontSize:18,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)',flexShrink:0}}>▾</span>
                    </button>
                    <div style={{maxHeight:open===i?'260px':'0px',overflow:'hidden',transition:'max-height 0.35s ease'}}>
                        <div style={{padding:'0 18px 14px 46px',display:'flex',gap:10}}>
                            <span style={{color:'#10b981',fontWeight:800,fontSize:13,flexShrink:0,marginTop:1}}>A.</span>
                            <span style={{color:'#6ee7b7',fontSize:13,lineHeight:1.75}}>{item.a}</span>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

/* ════ 개념 연결 수식 ════ */
const DERIVE_STEPS = [
    {title:'Step 1. 관성력과 운동의 상대성',desc:'가속 좌표계에서 공은 관성력(F=−ma)에 의해 낙하한다. 내부/외부 두 기술 모두 s=½at²로 일치한다.',
     formula:'s_{\\text{내부}} = \\tfrac{1}{2}at^2 = s_{\\text{외부}}',color:'#3b82f6',bg:'#0d1f3c',
     note:'내부: 공이 아래로 s만큼 이동. 외부: 우주선 바닥이 공 방향으로 s만큼 이동. 두 기술은 다르지만 결과는 동일하다.'},
    {title:'Step 2. 등가 원리',desc:'가속 좌표계의 관성력과 중력은 물리적으로 구별할 수 없다.',
     formula:'a = g \\;\\Rightarrow\\; F_{\\text{관성}} = ma = mg = F_{\\text{중력}}',color:'#6366f1',bg:'#0d1040',
     note:'아인슈타인(1907): "지금까지 한 생각 중 가장 행복한 생각." 어떤 역학 실험도 두 상황을 구별할 수 없다.'},
    {title:'Step 3. 가속계에서 빛의 처짐',desc:'우주선이 위로 가속하는 동안 빛이 내부를 통과하면, 내부 관찰자에게 빛은 아래로 처져 보인다.',
     formula:'\\Delta y = \\tfrac{1}{2}a\\!\\left(\\tfrac{L}{c}\\right)^{\\!2}',color:'#8b5cf6',bg:'#1a0d3c',
     note:'빛이 폭 L을 통과하는 시간 t=L/c 동안 우주선이 ½at² 위로 이동한다. 따라서 빛은 그만큼 아래로 처진 것처럼 보인다.'},
    {title:'Step 4. 등가 원리 → 중력장에서도 빛이 휜다',desc:'등가 원리에 의해 중력장(g=a)에서도 반드시 동일한 크기로 빛이 휘어야 한다.',
     formula:'\\Delta y_{\\text{중력}} = \\tfrac{1}{2}g\\!\\left(\\tfrac{L}{c}\\right)^{\\!2}',color:'#a855f7',bg:'#1e0d3c',
     note:'이 값은 뉴턴 역학으로 예측한 값(0.875″)의 2배다. 뉴턴의 F=GMm/r²에서 m=0이면 F=0이 되어 빛의 휨을 설명할 수 없다.'},
    {title:'Step 5. 시공간 곡률로 해결',desc:'빛은 직진하지만, 질량이 시공간 자체를 휘게 하므로 경로가 굽어 보인다.',
     formula:'G_{\\mu\\nu} = \\dfrac{8\\pi G}{c^4}\\,T_{\\mu\\nu}',color:'#10b981',bg:'#0a1f18',
     note:'좌변: 시공간의 곡률(기하학). 우변: 에너지-운동량(물질). 중력은 힘이 아니라 시공간의 기하학적 곡률이다.'},
    {title:'Step 6. 실험 검증: 1919년 일식',desc:'에딩턴이 태양 근처를 지나는 별빛의 편향각을 측정하여 아인슈타인 이론을 검증했다.',
     formula:'\\delta\\theta_{\\text{Newton}}=0.875^{\\prime\\prime} \\quad\\text{vs}\\quad \\delta\\theta_{\\text{Einstein}}=1.75^{\\prime\\prime}',color:'#fbbf24',bg:'#1f1200',
     note:'에딩턴의 측정값 ≈ 1.75초각 → 아인슈타인 예측과 일치. 뉴턴 예측의 정확히 2배. 현대 실측값: 1.7512±0.0006초각.'},
];
const DerivationSection = () => {
    const [open, setOpen] = useState(null);
    const [kReady, setKReady] = useState(!!window.katex);
    useEffect(()=>{
        if(window.katex){setKReady(true);return;}
        const iv=setInterval(()=>{if(window.katex){setKReady(true);clearInterval(iv);}},200);
        return()=>clearInterval(iv);
    },[]);
    return (
        <div>
            <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:6}}>
                <div style={{width:4,height:22,background:'#6366f1',borderRadius:2}}/>
                <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0'}}>논리 연결: 관성력 → 등가 원리 → 빛의 휨 → 뉴턴 한계 → 시공간 곡률</h2>
            </div>
            <p style={{color:'#475569',fontSize:13,marginBottom:14,marginLeft:14}}>각 단계를 클릭해 시뮬레이션과의 논리 흐름을 확인하세요.</p>
            <div style={{display:'flex',flexDirection:'column',gap:9}}>
                {DERIVE_STEPS.map((step,i)=>(
                    <div key={i} style={{border:`1px solid ${open===i?step.color+'99':'#1e293b'}`,borderRadius:13,overflow:'hidden',transition:'border-color 0.25s'}}>
                        <button onClick={()=>setOpen(open===i?null:i)}
                            style={{width:'100%',display:'flex',alignItems:'center',gap:14,padding:'12px 16px',background:open===i?step.bg:'transparent',border:'none',cursor:'pointer',fontFamily:'inherit',transition:'background 0.25s'}}>
                            <div style={{width:26,height:26,borderRadius:'50%',background:step.color+'22',border:`1.5px solid ${step.color}66`,display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
                                <span style={{color:step.color,fontWeight:800,fontSize:12}}>{i+1}</span>
                            </div>
                            <span style={{color:'#e2e8f0',fontWeight:700,fontSize:13,flex:1,textAlign:'left'}}>{step.title}</span>
                            <span style={{color:'#475569',fontSize:16,transition:'transform 0.25s',transform:open===i?'rotate(180deg)':'rotate(0deg)'}}>▾</span>
                        </button>
                        <div style={{maxHeight:open===i?'270px':'0px',overflow:'hidden',transition:'max-height 0.4s ease'}}>
                            <div style={{padding:'0 16px 16px 56px',background:step.bg}}>
                                <p style={{color:'#94a3b8',fontSize:13,lineHeight:1.7,marginBottom:12}}>{step.desc}</p>
                                {kReady&&(
                                    <div style={{background:'#070b14',borderRadius:8,padding:'12px 16px',marginBottom:10,textAlign:'center',border:`1px solid ${step.color}33`}}>
                                        <Math_ f={step.formula} display={true}/>
                                    </div>
                                )}
                                <p style={{color:'#64748b',fontSize:12,lineHeight:1.75,borderLeft:`3px solid ${step.color}55`,paddingLeft:10}}>{step.note}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

/* ════ 메인 App ════ */
const PHASES = [
    {label:'① 공 낙하 탐구', desc:'내부/외부 시점 & 중력 vs 관성력'},
    {label:'② 빛의 경로',    desc:'가속계에서 빛이 휜다'},
    {label:'③ 등가 원리',    desc:'물리적 동등성 확인'},
    {label:'④ 시공간 곡률',  desc:'뉴턴 한계 & 아인슈타인 해결'},
];

const App = () => {
    const [phase,   setPhase]   = useState(0);
    const [subView, setSubView] = useState(0);
    const [p1Sit,   setP1Sit]   = useState(2);
    const [accel,   setAccel]   = useState(9.8);
    const [running, setRunning] = useState(false);
    const [t,       setT]       = useState(0);
    const [tL, setTL] = useState(0);
    const [tR, setTR] = useState(0);
    const [runL, setRunL] = useState(false);
    const [runR, setRunR] = useState(false);

    const rafRef=useRef(null),startRef=useRef(null);
    const rafL=useRef(null),stL=useRef(null);
    const rafR=useRef(null),stR=useRef(null);

    useEffect(()=>{
        if(running){
            startRef.current=performance.now()-t;
            const loop=(now)=>{setT(now-startRef.current);rafRef.current=requestAnimationFrame(loop);};
            rafRef.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafRef.current);
        return()=>cancelAnimationFrame(rafRef.current);
    },[running]);

    useEffect(()=>{
        if(runL){
            stL.current=performance.now()-tL;
            const loop=(now)=>{
                const nt=now-stL.current;
                if(nt<MAX_MS){setTL(nt);rafL.current=requestAnimationFrame(loop);}
                else{setTL(MAX_MS);setRunL(false);}
            };
            rafL.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafL.current);
        return()=>cancelAnimationFrame(rafL.current);
    },[runL]);

    useEffect(()=>{
        if(runR){
            stR.current=performance.now()-tR;
            const loop=(now)=>{
                const nt=now-stR.current;
                if(nt<MAX_MS){setTR(nt);rafR.current=requestAnimationFrame(loop);}
                else{setTR(MAX_MS);setRunR(false);}
            };
            rafR.current=requestAnimationFrame(loop);
        } else cancelAnimationFrame(rafR.current);
        return()=>cancelAnimationFrame(rafR.current);
    },[runR]);

    const resetAll=()=>{setRunning(false);setT(0);setRunL(false);setRunR(false);setTL(0);setTR(0);};
    const syncRun=()=>{ resetAll(); setTimeout(()=>{setRunL(true);setRunR(true);},40); };
    const handlePhase=(i)=>{ setPhase(i); resetAll(); };

    const dL=physDist(tL, subView===0?accel:9.8);
    const dR=physDist(tR, accel);

    return (
        <div style={{maxWidth:1180,margin:'0 auto',display:'flex',flexDirection:'column',gap:22}}>

            <div className="card">
                <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:16}}>
                    <div style={{width:4,height:22,background:'#fbbf24',borderRadius:2}}/>
                    <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0'}}>🔍 탐구 질문</h2>
                </div>
                <QnA items={QNA_ITEMS}/>
            </div>

            <div style={{display:'grid',gridTemplateColumns:'270px 1fr',gap:18}}>
                <div className="panel" style={{display:'flex',flexDirection:'column',gap:16}}>
                    <div>
                        <h2 style={{fontSize:17,fontWeight:800,color:'#e2e8f0',marginBottom:4}}>탐구 시뮬레이션</h2>
                        <p style={{color:'#475569',fontSize:12,fontStyle:'italic'}}>① → ② → ③ → ④ 순서로 탐구하세요.</p>
                    </div>

                    <div>
                        <label>탐구 단계</label>
                        <div style={{display:'flex',flexDirection:'column',gap:6,marginTop:4}}>
                            {PHASES.map((p,i)=>(
                                <button key={i} className={`phase-btn${phase===i?' active':''}`} onClick={()=>handlePhase(i)}>
                                    <div style={{fontWeight:phase===i?700:400,fontSize:13}}>{p.label}</div>
                                    <div style={{fontSize:10,color:phase===i?'#93c5fd':'#475569',marginTop:2}}>{p.desc}</div>
                                </button>
                            ))}
                        </div>
                    </div>

                    {phase===0&&(
                        <div>
                            <label>시점 선택</label>
                            <div style={{display:'flex',gap:6,marginTop:4}}>
                                <button className={`view-tab${subView===0?' active':''}`} onClick={()=>{setSubView(0);resetAll();}}>내부/외부</button>
                                <button className={`view-tab${subView===1?' active':''}`} onClick={()=>{setSubView(1);resetAll();}}>중력 vs 관성력</button>
                            </div>
                        </div>
                    )}

                    {phase===1&&(
                        <div>
                            <label>운동 상황 선택</label>
                            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:5,marginTop:4}}>
                                {SIT_CFG.map((s,i)=>(
                                    <button key={i}
                                        onClick={()=>{setP1Sit(i);resetAll();}}
                                        style={{
                                            padding:'7px 6px',borderRadius:8,
                                            border:`1px solid ${p1Sit===i?s.color:'#1e293b'}`,
                                            background:p1Sit===i?s.border.replace('0.3','0.12'):'transparent',
                                            color:p1Sit===i?s.color:'#64748b',
                                            cursor:'pointer',fontSize:12,fontFamily:'inherit',fontWeight:p1Sit===i?700:400,
                                            transition:'all 0.2s'
                                        }}>
                                        {s.name}
                                    </button>
                                ))}
                            </div>
                            <div style={{fontSize:10,color:'#475569',marginTop:6,textAlign:'center'}}>
                                좌: 내부 관찰자 / 우: 외부 관찰자
                            </div>
                        </div>
                    )}

                    <div>
                        <label>{phase===0&&subView===1?'우주선 가속도 a (오른쪽)':'가속도 / 중력 크기'}</label>
                        <input type="range" min="2" max="20" step="0.2" value={accel}
                            onChange={e=>{setAccel(parseFloat(e.target.value));resetAll();}}/>
                        <p style={{textAlign:'center',fontSize:12,color:Math.abs(accel-9.8)<0.15?'#a78bfa':'#64748b',marginTop:4,fontFamily:'Space Mono,monospace'}}>
                            {accel.toFixed(1)} m/s²
                            {phase===0&&subView===1&&Math.abs(accel-9.8)<0.15&&<span style={{marginLeft:6}}>← g!</span>}
                        </p>
                    </div>

                    {phase===0?(
                        <div style={{display:'flex',flexDirection:'column',gap:8}}>
                            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:6}}>
                                <div style={{display:'flex',flexDirection:'column',gap:4}}>
                                    <div style={{fontSize:10,color:'#a78bfa',fontWeight:700,textTransform:'uppercase',letterSpacing:'0.05em'}}>
                                        {subView===0?'내부 시점':'중력(LEFT)'}
                                    </div>
                                    <button onClick={()=>setRunL(true)} disabled={runL}
                                        style={{padding:'8px',borderRadius:7,background:'rgba(99,102,241,0.1)',color:runL?'#475569':'#a78bfa',border:'1px solid rgba(99,102,241,0.35)',cursor:runL?'default':'pointer',fontSize:12,fontFamily:'inherit',fontWeight:700}}>▶ 시작</button>
                                    <button onClick={()=>{setRunL(false);setTL(0);}}
                                        style={{padding:'5px',borderRadius:7,background:'transparent',border:'1px solid #1e293b',color:'#475569',cursor:'pointer',fontSize:11,fontFamily:'inherit'}}>↺</button>
                                </div>
                                <div style={{display:'flex',flexDirection:'column',gap:4}}>
                                    <div style={{fontSize:10,color:'#4ade80',fontWeight:700,textTransform:'uppercase',letterSpacing:'0.05em'}}>
                                        {subView===0?'외부 시점':'관성력(RIGHT)'}
                                    </div>
                                    <button onClick={()=>setRunR(true)} disabled={runR}
                                        style={{padding:'8px',borderRadius:7,background:'rgba(74,222,128,0.1)',color:runR?'#475569':'#4ade80',border:'1px solid rgba(74,222,128,0.35)',cursor:runR?'default':'pointer',fontSize:12,fontFamily:'inherit',fontWeight:700}}>▶ 시작</button>
                                    <button onClick={()=>{setRunR(false);setTR(0);}}
                                        style={{padding:'5px',borderRadius:7,background:'transparent',border:'1px solid #1e293b',color:'#475569',cursor:'pointer',fontSize:11,fontFamily:'inherit'}}>↺</button>
                                </div>
                            </div>
                            <button onClick={syncRun}
                                style={{padding:'9px',borderRadius:8,background:'rgba(167,139,250,0.1)',color:'#c4b5fd',border:'1px solid rgba(167,139,250,0.35)',cursor:'pointer',fontSize:13,fontFamily:'inherit',fontWeight:700}}>
                                ⚡ 동기화 동시 실행
                            </button>
                            <button onClick={resetAll}
                                style={{padding:'7px',borderRadius:8,background:'transparent',border:'1px solid #1e293b',color:'#64748b',cursor:'pointer',fontSize:12,fontFamily:'inherit'}}>
                                ↺ 초기화
                            </button>
                        </div>
                    ):(
                        <div style={{display:'flex',flexDirection:'column',gap:8}}>
                            <button onClick={()=>setRunning(r=>!r)} style={{
                                padding:'11px',borderRadius:10,cursor:'pointer',fontFamily:'inherit',fontSize:14,fontWeight:700,
                                background:running?'rgba(239,68,68,0.15)':'rgba(59,130,246,0.15)',
                                color:running?'#f87171':'#60a5fa',
                                border:`1px solid ${running?'rgba(239,68,68,0.4)':'rgba(59,130,246,0.4)'}`,
                                transition:'all 0.2s'
                            }}>{running?'⏸ 일시 정지':'▶ 시뮬레이션 실행'}</button>
                            <button onClick={()=>{setRunning(false);setT(0);}} style={{
                                padding:'8px',borderRadius:10,border:'1px solid #1e293b',background:'transparent',
                                color:'#64748b',cursor:'pointer',fontFamily:'inherit',fontSize:13
                            }}>↺ 초기화</button>
                        </div>
                    )}

                    <div style={{background:'#070b14',borderRadius:10,padding:'10px 14px',border:'1px solid #1e293b'}}>
                        {phase===0?(<>
                            <div className="result-row">
                                <span style={{color:'#64748b',fontSize:12}}>{subView===0?'내부/이동':'중력/이동'}</span>
                                <span className="result-val" style={{fontSize:12}}>{dL.toFixed(1)} px</span>
                            </div>
                            <div className="result-row">
                                <span style={{color:'#64748b',fontSize:12}}>{subView===0?'외부/이동':'관성/이동'}</span>
                                <span className="result-val" style={{color:'#4ade80',fontSize:12}}>{dR.toFixed(1)} px</span>
                            </div>
                            <div className="result-row">
                                <span style={{color:'#64748b',fontSize:12}}>동기화</span>
                                <span className="result-val" style={{color:Math.abs(dL-dR)<2?'#4ade80':'#f87171',fontSize:12}}>
                                    {Math.abs(dL-dR)<2?'✓ 일치':'비동기'}
                                </span>
                            </div>
                        </>):(<>
                            <div className="result-row">
                                <span style={{color:'#64748b'}}>가속도</span>
                                <span className="result-val">{accel.toFixed(1)} m/s²</span>
                            </div>
                            {phase===1&&(
                            <div className="result-row">
                                <span style={{color:'#64748b'}}>선택 상황</span>
                                <span className="result-val" style={{color:SIT_CFG[p1Sit].color,fontSize:12}}>{SIT_CFG[p1Sit].name}</span>
                            </div>
                            )}
                            <div className="result-row">
                                <span style={{color:'#64748b'}}>빛 처짐(Δy)</span>
                                <span className="result-val" style={{color:'#f87171'}}>{(accel/9.8*22).toFixed(1)} px</span>
                            </div>
                        </>)}
                    </div>

                    <div style={{fontSize:11,lineHeight:1.8,borderTop:'1px solid #1e293b',paddingTop:10}}>
                        <p style={{color:'#334155'}}>* ①-중력 vs 관성력에서 a=9.8로 맞추면 구별 불가를 확인합니다.</p>
                        <p style={{color:'#334155'}}>* ② 빛의 처짐 → ③ 등가원리 → ④ 시공간 순서로 탐구하세요.</p>
                    </div>
                </div>

                <div style={{background:'#070b14',borderRadius:14,border:'1px solid #1e293b',overflow:'hidden',minHeight:520}}>
                    <SimCanvas phase={phase} subView={subView} p1Sit={p1Sit} accel={accel}
                        t={t} running={running} tL={tL} tR={tR}/>
                </div>
            </div>

            <div className="card">
                <DerivationSection/>
            </div>

        </div>
    );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
</script>
</body>
</html>
"""
    components.html(react_code, height=2400, scrolling=True)

if __name__ == "__main__":
    run_sim()
