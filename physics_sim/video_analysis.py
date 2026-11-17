# app.py — 사곡고등학교 물리학Ⅱ · 지표면 역학 분석 - 포물선 운동 영상 분석 실습
# 실행: streamlit run app.py
# 필요한 패키지: streamlit pandas numpy plotly matplotlib python-docx reportlab openpyxl

import base64
import io
import json
import os
import re
from datetime import datetime, timedelta, timezone
from xml.sax.saxutils import escape as xml_escape

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# ════════════════════════════════════════════════════════════════════
# 1. 고정 설정
# ════════════════════════════════════════════════════════════════════
COURSE = "물리학Ⅱ"
UNIT_INFO = "Ⅰ. 시공간과 운동  01 힘의 합성과 예측 · 6차시"
STD_INFO = "[12역학01-02] 뉴턴 운동 법칙을 이용하여 물체의 포물선 운동을 정량적으로 설명하고, 포물선 운동 에서의 역학적 에너지를 구할 수 있다."
GOAL_INFO = "포물선 운동의 측정 자료를 그래프로 나타내어 수평·연직 방향 운동을 설명할 수 있다."
INQUIRY_Q = "실제로 던진 공도 포물선 운동 모델대로 움직일까?"

TITLE = "지표면 역학 분석 - 포물선 운동 영상 분석 실습"
AREA = "포물선 운동 영상 분석 실습"
G = 9.8

VA_URL = "https://videoanalysis.app?key=tvabJMZYyB"
VA_KEY = "tvabJMZYyB"
SIM_URL = "https://physics-course.streamlit.app/projectile_analysis_excel"

_HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(_HERE, "fonts") if os.path.isdir(os.path.join(_HERE, "fonts")) else os.path.join(os.path.dirname(_HERE), "fonts")
FONT_REG = os.path.join(FONT_DIR, "NanumGothic.ttf")
FONT_BOLD = os.path.join(FONT_DIR, "NanumGothicBold.ttf")

Q = {
    "q3a": "가. 수평 방향 운동에서 속력은 시간에 따라 어떻게 변하는가? (측정값이나 그래프를 근거로 서술하시오.)",
    "q3b": "나. 수평 방향 운동이 가와 같이 일어나는 이유는 무엇인가? (수평 방향에 작용하는 힘과 관련지어 서술하시오.)",
    "q3c_desc": "다. 연직 방향의 운동에서 속력은 시간에 따라 어떻게 변하는가? (측정값이나 그래프를 근거로 서술하시오.)",
    "q3d_reason": "라. 연직 방향 운동에서 다와 같이 일어나는 이유는 무엇인가? (연직 방향에 작용하는 힘과 관련지어 서술하시오.)",
    "q3e_calc": "마. 연직 방향의 속도-시간 데이터로부터 연직 가속도(ay)를 구하는 식을 쓰고, 측정값을 대입하여 평균 가속도를 직접 계산하시오.",
    "q4a": "가. 데이터 표 첫 번째 행의 속도 성분(vx, vy)으로 처음 속력 v0와 발사각을 구하고, 포물선 운동 시뮬레이션에서 구한 이론값과 실험값을 비교하시오.",
    "q4b": "나. 실험값과 이론값에 차이가 나는 까닭은 무엇인가? 측정 과정에서 생긴 오차와 포물선 운동 모델이 무시한 요인(공기 저항 등)으로 나누어 서술하시오.",
    "q5": "탐구 질문 — '실제로 던진 공도 포물선 운동 모델대로 움직일까?'에 대하여, 수평 방향과 연직 방향의 측정 자료·그래프 분석 결과를 근거로 결론을 정리하시오.",
}
COMP_ITEMS = ["수평 이동거리 (m)", "최고점 높이 (m)", "비행 시간 (s)", "연직 가속도 크기 (m/s²)"]

SAVE_KEYS = [
    "stu_grade", "stu_cls", "stu_num", "stu_name", "stu_partner",
    "input_mode", "raw_data", "raw_file_text", "raw_file_name",
    "map_t", "map_x", "map_y", "map_vx", "map_vy",
    "q3a", "q3b", "q3c_desc", "q3d_reason",
    "ay_i1", "ay_i2", "ay_formula", "ay_subst", "ay_result", "ay_err",
    "calc_img_b64", "calc_img_name",
    "img_h_b64", "img_h_name", "img_v_b64", "img_v_name",
    "v0x", "v0y", "v0", "theta",
    "exp_0", "exp_1", "exp_2", "exp_3",
    "th_0", "th_1", "th_2", "th_3",
    "er_0", "er_1", "er_2", "er_3",
    "err_measure", "err_model", "q5",
]

# ════════════════════════════════════════════════════════════════════
# 2. 페이지 · 스타일 · 상태
# ════════════════════════════════════════════════════════════════════
st.set_page_config(page_title=TITLE, page_icon="📹", layout="wide")

st.markdown("""
<style>
.block-container { max-width: 1080px; padding-top: 1.4rem; padding-bottom: 4rem; }
h1, h2, h3, h4 { letter-spacing: -0.02em; }
.hero { background: linear-gradient(135deg,#1F3B5C 0%,#2E6DA4 100%); color:#fff;
        padding: 20px 26px; border-radius: 12px; margin-bottom: 12px; }
.hero .k { font-size: 13px; opacity: .88; }
.hero h1 { color:#fff; font-size: 24px; margin: 2px 0 4px 0; font-weight: 800; }
.hero .m { font-size: 13px; opacity: .92; }

.curr-tbl { width:100%; border-collapse:collapse; font-size:13.5px; margin-bottom:14px; background:#fff;
            border:1.5px solid #334155; border-radius:8px; overflow:hidden; }
.curr-tbl th { background:#E2E8F0; color:#1E293B; font-weight:700; width:110px; text-align:center;
               padding:8px 12px; border:1px solid #94A3B8; }
.curr-tbl td { padding:8px 14px; border:1px solid #94A3B8; color:#1E293B; line-height:1.55; }
.curr-tbl td.blue-txt { color:#1D4ED8; font-weight:600; }

.sec { background:#1F3B5C; color:#fff; padding: 9px 16px; border-radius: 8px;
       font-weight: 700; font-size: 16px; margin: 24px 0 10px 0;
       display:flex; justify-content:space-between; align-items:center; }
.sec span.sub { font-size: 12px; font-weight: 400; opacity: .88; }
.qbox { background:#F2F6FB; border-left: 4px solid #2E6DA4; padding: 9px 13px;
        border-radius: 0 7px 7px 0; margin: 8px 0 4px 0; font-weight: 600; color:#1A2B3C; font-size: 14.5px; }
.tip { font-size: 12.5px; color:#5A6878; background:#F7F9FC; border:1px solid #E3E9F0;
       padding: 7px 11px; border-radius: 6px; margin: 3px 0 8px 0; line-height: 1.55; }
.auto-label { display:inline-block; background:#E3ECF6; color:#1F3B5C; font-size:11.5px;
              font-weight:700; padding:2px 8px; border-radius:4px; margin-bottom:4px; }
.legend { font-size: 12.5px; color:#4A5868; padding: 6px 2px; }
.legend .sw { display:inline-block; width:12px; height:12px; border-radius:3px;
              vertical-align:-2px; margin-right:4px; }
.card-t { font-weight:700; color:#1F3B5C; font-size:15px; margin-bottom:6px; }
.steps { font-size: 13.5px; line-height: 1.68; margin:0; }
.steps ol { padding-left: 18px; margin: 2px 0; }
.steps li { margin-bottom: 6px; }
.pill { display:inline-block; background:#EEF4FA; border:1px solid #CEDBE8; color:#1F3B5C;
        padding: 1px 8px; border-radius: 99px; font-size: 12px; font-weight: 600; margin: 1px 2px; }

/* 학생 작성 칸 — 연한 노란 배경 */
div[data-testid="stTextArea"] textarea,
div[data-testid="stTextInput"] input[type="text"] {
    background-color: #FFFDF2 !important;
    border: 1px solid #E2CF8A !important;
}
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stTextInput"] input[type="text"]:focus {
    background-color: #FFFFFF !important;
    border-color: #2E6DA4 !important;
}
</style>
""", unsafe_allow_html=True)

try:
    _sig = st.dataframe.__wrapped__.__code__.co_varnames
except AttributeError:
    _sig = st.dataframe.__code__.co_varnames
FULL = {"width": "stretch"} if "width" in _sig else {"use_container_width": True}


def sel_kw(key, default=0):
    return {} if key in st.session_state else {"index": default}


if "_pending_load" in st.session_state:
    data_to_load = st.session_state.pop("_pending_load")
    if isinstance(data_to_load, dict):
        for k in SAVE_KEYS:
            if k in data_to_load and data_to_load[k] is not None:
                st.session_state[k] = data_to_load[k]
    st.session_state["_loaded_msg"] = True

defaults = {
    "stu_grade": "3", "stu_cls": "", "stu_num": "", "stu_name": "", "stu_partner": "",
    "input_mode": "붙여넣기", "raw_data": "", "raw_file_text": "", "raw_file_name": "",
    "q3a": "", "q3b": "", "q3c_desc": "", "q3d_reason": "",
    "ay_i1": 0, "ay_i2": 5, "ay_formula": "", "ay_subst": "", "ay_result": "", "ay_err": "",
    "calc_img_b64": "", "calc_img_name": "",
    "img_h_b64": "", "img_h_name": "", "img_v_b64": "", "img_v_name": "",
    "v0x": "", "v0y": "", "v0": "", "theta": "",
    "exp_0": "", "exp_1": "", "exp_2": "", "exp_3": "",
    "th_0": "", "th_1": "", "th_2": "", "th_3": "9.8",
    "er_0": "", "er_1": "", "er_2": "", "er_3": "",
    "err_measure": "", "err_model": "", "q5": "",
    "exports": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def ss(k, default=""):
    v = st.session_state.get(k, default)
    return default if v is None else v


def now_kst():
    return datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d %H:%M")


def sec(num, title, sub=""):
    sub_html = f"<span class='sub'>{sub}</span>" if sub else ""
    st.markdown(f"<div class='sec'><span>{num}. {title}</span>{sub_html}</div>", unsafe_allow_html=True)


def qtext(text):
    st.markdown(f"<div class='qbox'>{text}</div>", unsafe_allow_html=True)


def tip(text):
    st.markdown(f"<div class='tip'>💡 {text}</div>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# 3. 데이터 처리 · 오류 검증 · 엑셀
# ════════════════════════════════════════════════════════════════════
def parse_table(text):
    if not text or not text.strip():
        return None
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return None
    sep = "\t" if "\t" in lines[0] else ("," if "," in lines[0] else (";" if ";" in lines[0] else None))
    rows = [(re.split(r"\s+", ln) if sep is None else [c.strip() for c in ln.split(sep)]) for ln in lines]
    ncol = max(len(r) for r in rows)
    rows = [r + [""] * (ncol - len(r)) for r in rows]

    def is_num(s):
        try:
            float(s.replace(",", ""))
            return True
        except Exception:
            return False

    if sum(is_num(c) for c in rows[0]) >= max(1, len(rows[0]) // 2):
        headers, body = [f"열{i + 1}" for i in range(ncol)], rows
    else:
        seen, headers = {}, []
        for i, h in enumerate(rows[0]):
            h = h or f"열{i + 1}"
            seen[h] = seen.get(h, 0) + 1
            headers.append(h if seen[h] == 1 else f"{h}_{seen[h]}")
        body = rows[1:]
    df = pd.DataFrame(body, columns=headers)
    for c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")
    df = df.dropna(how="all").reset_index(drop=True)
    return df if len(df) >= 2 else None


def guess_columns(cols):
    out = {k: None for k in ("t", "x", "y", "vx", "vy")}
    for c in cols:
        s = re.sub(r"[\s_()\[\]/·:-]", "", c.lower())
        if out["t"] is None and ("time" in s or "시간" in s or s in ("t", "ts", "sec")):
            out["t"] = c
        elif out["vx"] is None and any(k in s for k in ("vx", "xvel", "velx", "x속도", "속도x", "수평속도")):
            out["vx"] = c
        elif out["vy"] is None and any(k in s for k in ("vy", "yvel", "vely", "y속도", "속도y", "연직속도")):
            out["vy"] = c
    for c in cols:
        if c in out.values():
            continue
        s = re.sub(r"[\s_()\[\]/·:-]", "", c.lower())
        if out["x"] is None and (s in ("x", "xm", "xpos", "positionx") or "x위치" in s or "수평위치" in s or s.endswith(":xm") or s.endswith("xm")):
            out["x"] = c
        elif out["y"] is None and (s in ("y", "ym", "ypos", "positiony") or "y위치" in s or "연직위치" in s or s.endswith(":ym") or s.endswith("ym")):
            out["y"] = c
    rem = [c for c in cols if c not in out.values()]
    for k in ("t", "x", "y", "vx", "vy"):
        if out[k] is None and rem:
            out[k] = rem.pop(0)
    return out


def deriv(v, t):
    v, t = np.asarray(v, float), np.asarray(t, float)
    n = len(v)
    out = np.full(n, np.nan)
    if n < 2:
        return out
    dt0 = t[1] - t[0]
    dt1 = t[-1] - t[-2]
    out[0] = (v[1] - v[0]) / dt0 if dt0 != 0 else np.nan
    out[-1] = (v[-1] - v[-2]) / dt1 if dt1 != 0 else np.nan
    if n > 2:
        dt = t[2:] - t[:-2]
        out[1:-1] = np.where(dt != 0, (v[2:] - v[:-2]) / dt, np.nan)
    return out


def build_data(raw, m):
    d = pd.DataFrame()
    d["t"] = pd.to_numeric(raw[m["t"]], errors="coerce")
    d["x"] = pd.to_numeric(raw[m["x"]], errors="coerce")
    d["y"] = pd.to_numeric(raw[m["y"]], errors="coerce")
    d["vx"] = pd.to_numeric(raw[m["vx"]], errors="coerce") if m.get("vx") else np.nan
    d["vy"] = pd.to_numeric(raw[m["vy"]], errors="coerce") if m.get("vy") else np.nan
    d = d.dropna(subset=["t", "x", "y"]).reset_index(drop=True)
    if len(d) < 3:
        return None
    if d["vx"].isna().all():
        d["vx"] = deriv(d["x"], d["t"])
    else:
        d["vx"] = d["vx"].fillna(pd.Series(deriv(d["x"], d["t"])))
    if d["vy"].isna().all():
        d["vy"] = deriv(d["y"], d["t"])
    else:
        d["vy"] = d["vy"].fillna(pd.Series(deriv(d["y"], d["t"])))
    d["v"] = np.hypot(d["vx"], d["vy"])
    d["ay"] = deriv(d["vy"], d["t"])
    return d


def validate_data(d):
    """붙여넣은 데이터의 물리적·측정적 오류 여부를 검증하여 (errors, warnings, metrics) 반환."""
    errors = []
    warnings = []
    t = d["t"].to_numpy(float)
    x = d["x"].to_numpy(float)
    y = d["y"].to_numpy(float)
    vx = d["vx"].to_numpy(float)
    vy = d["vy"].to_numpy(float)

    n = len(d)
    max_abs_x = float(np.nanmax(np.abs(x)))
    max_abs_y = float(np.nanmax(np.abs(y)))
    dt = np.diff(t)

    # 1. 데이터 개수 및 시간 간격 검증
    if n < 5:
        warnings.append(f"**데이터 개수 부족 ({n}개)**: 정확한 그래프 분석을 위해 최소 8개 이상의 질점을 찍는 것을 권장합니다.")
    if np.any(dt <= 0):
        errors.append("**시간(t) 순서 오류**: 시간이 일정하게 증가하지 않는 구간이 있습니다. 열 맞추기에서 '시간 t' 열이 올바른지 확인하세요.")

    # 2. 위치(x, y) 단위 / 교정막대자 미설정 검증 (예: 픽셀 값 1129 m, 733 m 등)
    if max_abs_x > 30.0 or max_abs_y > 30.0:
        errors.append(
            f"**위치(x, y) 값 범위 이상 (최대 |x| = {max_abs_x:.1f} m, |y| = {max_abs_y:.1f} m)**: "
            f"교실·실험실 포물선 운동 범위를 크게 벗어난 수십~수천 m 값입니다. "
            f"**교정막대자(축척, Scale)**를 설정하지 않아 픽셀(px) 좌표가 그대로 들어왔거나, 좌표축 원점(0, 0) 설정이 잘못되었을 가능성이 높습니다."
        )
    elif abs(x[0]) > 5.0 or abs(y[0]) > 5.0:
        warnings.append(
            f"**좌표축 원점(0, 0) 위치 확인 (첫 점 x₀ = {x[0]:.2f} m, y₀ = {y[0]:.2f} m)**: "
            f"공의 처음 위치가 원점(0, 0)에서 멀리 떨어져 있습니다. 좌표축 원점을 공의 출발점(또는 바닥 기준점) 근처로 설정했는지 확인하세요."
        )

    # 3. 위치 미분 속도(Δx/Δt, Δy/Δt)와 붙여넣은 속도(vx, vy)의 정합성 검증
    dxdt = deriv(x, t)
    dydt = deriv(y, t)
    err_vx = float(np.nanmedian(np.abs(dxdt - vx)))
    err_vy = float(np.nanmedian(np.abs(dydt - vy)))
    med_vx = max(float(np.nanmedian(np.abs(vx))), 0.5)
    med_vy = max(float(np.nanmedian(np.abs(vy))), 0.5)
    if err_vx > max(4.0, 0.8 * med_vx) or err_vy > max(4.0, 0.8 * med_vy):
        errors.append(
            f"**위치 변화율과 속도 값 불일치 (Δx/Δt ≈ {np.nanmedian(dxdt):.2f} m/s ↔ vx ≈ {np.nanmedian(vx):.2f} m/s)**: "
            f"위치(x, y)로부터 계산한 속도와 표의 속도(vx, vy)가 서로 맞지 않습니다. "
            f"교정막대자/원점을 나중에 바꾸었거나, '🔧 열 맞추기'에서 잘못된 열이 선택되었는지 확인하세요."
        )

    # 4. 연직 가속도(vy-t 기울기) 및 좌표축 방향 검증
    slope_ay = float(np.polyfit(t, vy, 1)[0]) if n >= 2 and not np.any(np.isnan(vy)) else float(np.nanmean(d["ay"]))
    if slope_ay > 0:
        errors.append(
            f"**연직 가속도 부호 반대 (평균 ay ≈ +{slope_ay:.2f} m/s² > 0)**: "
            f"연직 속도(vy)가 시간에 따라 증가하고 있습니다. **좌표축의 +y 방향이 아래쪽**으로 뒤집혀 있거나 x·y 열이 바뀌었는지 확인하세요."
        )
    elif slope_ay > -4.0 or slope_ay < -18.0:
        warnings.append(
            f"**연직 가속도 크기 편차 큼 (평균 ay ≈ {slope_ay:.2f} m/s², 이론 -9.8 m/s²)**: "
            f"중력가속도(-9.8 m/s²)와 차이가 큽니다. **교정막대자의 실제 기준 길이(m)**가 정확히 입력되었는지, "
            f"공이 손을 떠난 직후부터 바닥에 닿기 직전까지만 질점을 찍었는지 확인하세요."
        )

    # 5. 수평 속도(vx) 일정성 검증 (클립 설정 오류: 손에서 떠나기 전/착지 후 포함 여부)
    mean_vx = float(np.nanmean(vx))
    std_vx = float(np.nanstd(vx))
    if np.nanmin(vx) * np.nanmax(vx) < 0:
        warnings.append(
            f"**수평 속도(vx) 부호 변화 ({np.nanmin(vx):.2f} ~ {np.nanmax(vx):.2f} m/s)**: "
            f"운동 도중 수평 방향이 바뀌는 데이터가 포함되어 있습니다. 공을 던지기 전이나 부딪힌 후 프레임이 포함되었는지 확인하세요."
        )
    elif abs(mean_vx) > 0.1 and (std_vx / abs(mean_vx)) > 0.35:
        warnings.append(
            f"**수평 속도(vx) 흔들림 과다 (평균 {mean_vx:.2f} m/s, 표준편차 {std_vx:.2f} m/s)**: "
            f"수평 속도의 변동 폭이 큽니다. 공이 손을 떠난 순간부터 클립을 시작했는지, 공의 중심을 일정하게 찍었는지 점검하세요."
        )

    metrics = {
        "n": n,
        "dt_total": float(t[-1] - t[0]),
        "dx_total": float(x[-1] - x[0]),
        "dy_max": float(np.nanmax(y) - y[0]),
        "y_max": float(np.nanmax(y)),
        "mean_vx": mean_vx,
        "slope_ay": slope_ay,
    }
    return errors, warnings, metrics


def make_xlsx(d):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "포물선운동분석"
    headers = ["t (s)", "x (m)", "y (m)", "vx (m/s)", "vy (m/s)", "v (m/s)", "ay (m/s²)"]
    ws.append(headers)
    for _, r in d.iterrows():
        ws.append([round(float(r[k]), 4) if pd.notna(r[k]) else None
                   for k in ("t", "x", "y", "vx", "vy", "v", "ay")])
    hdr = PatternFill("solid", fgColor="1F3B5C")
    for col_idx in range(1, 8):
        c = ws.cell(1, col_idx)
        c.font, c.fill, c.alignment = Font(bold=True, color="FFFFFF"), hdr, Alignment(horizontal="center")
    for col, w in zip("ABCDEFG", [10, 11, 11, 12, 12, 12, 13]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2, max_col=7):
        for c in row:
            c.number_format = "0.000"
    bio = io.BytesIO()
    wb.save(bio)
    return bio.getvalue()


def fnum(v, nd=3):
    try:
        return f"{float(v):.{nd}f}"
    except Exception:
        return "-"


# ════════════════════════════════════════════════════════════════════
# 4. 그래프
# ════════════════════════════════════════════════════════════════════
C_H, C_V, C_A = "#2E6DA4", "#C0504D", "#7A5195"


def zero_range(v):
    """0과 평균의 2배 사이를 보여 주는 넓은 축 (일정한 값의 작은 흔들림이 과장되지 않게)."""
    v = np.asarray(v, float)
    c = float(np.nanmean(v))
    half = max(abs(c), 1e-6)
    lo, hi = c - half, c + half
    pad = 0.08 * (hi - lo)
    return [min(lo, float(np.nanmin(v)) - pad), max(hi, float(np.nanmax(v)) + pad)]


def ay_range(v):
    """가속도-시간(ay-t) 그래프의 급간을 넓게 잡아 등가속도 운동(ay ≈ -9.8 m/s²) 경향이 잘 보이도록 설정."""
    v = np.asarray(v, float)
    min_v = float(np.nanmin(v)) if len(v) > 0 else -10.0
    max_v = float(np.nanmax(v)) if len(v) > 0 else -10.0
    lo = min(-60.0, float(np.floor((min_v - 10.0) / 20.0) * 20.0))
    hi = max(40.0, float(np.ceil((max_v + 10.0) / 20.0) * 20.0))
    return [lo, hi]


def plotly_graphs(d):
    fig1 = make_subplots(rows=1, cols=2, horizontal_spacing=0.1,
                         subplot_titles=("위치-시간 (x-t)", "속도-시간 (vx-t)"))
    fig1.add_trace(go.Scatter(x=d.t, y=d.x, mode="lines+markers", line=dict(color=C_H)), 1, 1)
    fig1.add_trace(go.Scatter(x=d.t, y=d.vx, mode="lines+markers", line=dict(color=C_H)), 1, 2)
    fig1.update_yaxes(title_text="x (m)", row=1, col=1)
    fig1.update_yaxes(title_text="vx (m/s)", range=zero_range(d.vx), row=1, col=2)

    fig2 = make_subplots(rows=1, cols=3, horizontal_spacing=0.11,
                         subplot_titles=("위치-시간 (y-t)", "속도-시간 (vy-t)", "가속도-시간 (ay-t)"))
    fig2.add_trace(go.Scatter(x=d.t, y=d.y, mode="lines+markers", line=dict(color=C_V)), 1, 1)
    fig2.add_trace(go.Scatter(x=d.t, y=d.vy, mode="lines+markers", line=dict(color=C_V)), 1, 2)
    fig2.add_trace(go.Scatter(x=d.t, y=d.ay, mode="lines+markers", line=dict(color=C_A)), 1, 3)
    fig2.update_yaxes(title_text="y (m)", row=1, col=1)
    fig2.update_yaxes(title_text="vy (m/s)", row=1, col=2)
    fig2.update_yaxes(title_text="ay (m/s²)", range=ay_range(d.ay), dtick=20, row=1, col=3)

    for f in (fig1, fig2):
        f.update_xaxes(title_text="t (s)")
        f.update_yaxes(tickformat=".1f", title_standoff=4, zeroline=True, zerolinecolor="#9AA8B8")
        f.update_layout(height=320, showlegend=False, margin=dict(l=40, r=20, t=40, b=40),
                        plot_bgcolor="#FAFBFC")
    return fig1, fig2


def mpl_png(d):
    """보고서 파일용 그래프 이미지 (matplotlib) — 화면 그래프와 같은 축 범위 사용."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
    from matplotlib import font_manager
    ko = os.path.exists(FONT_REG)
    if ko:
        font_manager.fontManager.addfont(FONT_REG)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_REG).get_name()
    plt.rcParams["axes.unicode_minus"] = False

    def style(a, yl, title):
        a.set_title(title, fontsize=10)
        a.set_xlabel("t (s)", fontsize=8)
        a.set_ylabel(yl, fontsize=8)
        a.tick_params(labelsize=7)
        a.grid(alpha=.3)
        a.ticklabel_format(useOffset=False, axis="y")
        a.axhline(0, color="#9AA8B8", lw=0.8)

    fig, ax = plt.subplots(2, 3, figsize=(10, 5.6))
    spec = [
        (0, 0, "x", "x (m)", C_H, "x-t", None),
        (0, 1, "vx", "vx (m/s)", C_H, "vx-t", zero_range(d.vx)),
        (1, 0, "y", "y (m)", C_V, "y-t", None),
        (1, 1, "vy", "vy (m/s)", C_V, "vy-t", None),
        (1, 2, "ay", "ay (m/s²)", C_A, "ay-t", ay_range(d.ay)),
    ]
    for r, c, col, yl, color, ttl, rng in spec:
        a = ax[r][c]
        a.plot(d.t, d[col], "o-", color=color, ms=3, lw=1.2)
        style(a, yl, (("수평 " if r == 0 else "연직 ") + ttl) if ko else ttl)
        if rng:
            a.set_ylim(*rng)
            if col == "ay":
                a.yaxis.set_major_locator(ticker.MultipleLocator(20))
    ax[0][2].axis("off")
    fig.tight_layout()
    bio = io.BytesIO()
    fig.savefig(bio, format="png", dpi=160)
    plt.close(fig)
    return bio.getvalue()


# ════════════════════════════════════════════════════════════════════
# 5. 콜백
# ════════════════════════════════════════════════════════════════════
def cb_file():
    f = st.session_state.get("data_upload")
    if f is not None:
        raw = f.getvalue()
        for enc in ("utf-8-sig", "cp949", "latin-1"):
            try:
                st.session_state["raw_file_text"] = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        st.session_state["raw_file_name"] = f.name
        for k in ("map_t", "map_x", "map_y", "map_vx", "map_vy"):
            st.session_state.pop(k, None)


def cb_paste():
    for k in ("map_t", "map_x", "map_y", "map_vx", "map_vy"):
        st.session_state.pop(k, None)


def cb_calc_img():
    f = st.session_state.get("calc_upload")
    if f is not None:
        st.session_state["calc_img_b64"] = base64.b64encode(f.getvalue()).decode()
        st.session_state["calc_img_name"] = f.name


def cb_img_h():
    f = st.session_state.get("upload_img_h")
    if f is not None:
        st.session_state["img_h_b64"] = base64.b64encode(f.getvalue()).decode()
        st.session_state["img_h_name"] = f.name


def cb_img_v():
    f = st.session_state.get("upload_img_v")
    if f is not None:
        st.session_state["img_v_b64"] = base64.b64encode(f.getvalue()).decode()
        st.session_state["img_v_name"] = f.name


def update_diff():
    for j in range(4):
        try:
            ev = float(str(st.session_state.get(f"exp_{j}", "")).strip())
            tv = float(str(st.session_state.get(f"th_{j}", "")).strip())
            st.session_state[f"er_{j}"] = f"{abs(ev - tv):.3f}"
        except Exception:
            pass


# ════════════════════════════════════════════════════════════════════
# 6. 화면 — 머리 · 단원정보 표 · 학생 정보 · 탐구 과정
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='hero'>
  <div class='k'>{COURSE} · {UNIT_INFO}</div>
  <h1>📹 {TITLE}</h1>
  <div class='m'>탐구 질문: {INQUIRY_Q}</div>
</div>""", unsafe_allow_html=True)

# 상단 단원정보 / 성취기준 / 학습목표 / 탐구질문 표
st.markdown(f"""
<table class='curr-tbl'>
  <tr>
    <th>단원정보</th>
    <td><b>{UNIT_INFO}</b></td>
  </tr>
  <tr>
    <th>성취기준</th>
    <td>{STD_INFO}</td>
  </tr>
  <tr>
    <th>학습목표</th>
    <td class='blue-txt'>{GOAL_INFO}</td>
  </tr>
  <tr>
    <th>탐구질문</th>
    <td class='blue-txt'>{INQUIRY_Q}</td>
  </tr>
</table>
""", unsafe_allow_html=True)

bar1, bar2, bar3 = st.columns([4.2, 1.1, 1.3])
with bar1:
    st.markdown("<div class='legend'><span class='sw' style='background:#FFF8DC;border:1px solid #E8C766'></span>"
                "노란 칸 = 학생이 작성하는 곳 &nbsp;&nbsp; <span class='sw' style='background:#EEF4FA;border:1px solid #D5DEE8'>"
                "</span>파란 표·그래프 = 앱이 자동으로 만드는 곳</div>", unsafe_allow_html=True)
with bar2:
    save_payload = {k: st.session_state.get(k) for k in SAVE_KEYS}
    save_payload["_saved_at"] = now_kst()
    st.download_button("💾 저장", json.dumps(save_payload, ensure_ascii=False, default=str).encode("utf-8"),
                       file_name=f"{ss('stu_grade')}{ss('stu_cls').zfill(2)}{ss('stu_num').zfill(2)}_{ss('stu_name')}_포물선운동실습.json",
                       mime="application/json", **FULL,
                       help="지금까지 입력한 내용을 JSON 파일로 내려받습니다.")
with bar3:
    with st.popover("📂 불러오기", **FULL):
        up = st.file_uploader("저장한 JSON 파일", type=["json"], key="load_json")
        if up is not None and st.button("이 파일로 이어서 작성", **FULL):
            try:
                st.session_state["_pending_load"] = json.load(up)
                st.rerun()
            except Exception as e:
                st.error(f"파일을 읽을 수 없습니다: {e}")
if st.session_state.pop("_loaded_msg", False):
    st.success("저장한 내용을 불러왔습니다. 이어서 작성하세요.")

# ── 학생 정보 ──────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("<div class='card-t'>👤 학생 정보</div>", unsafe_allow_html=True)
    s0, s1, s2, s3, s4 = st.columns([0.9, 0.9, 0.9, 1.4, 2.2])
    s0.text_input("학년", key="stu_grade", placeholder="3")
    s1.text_input("반", key="stu_cls", placeholder="예: 2")
    s2.text_input("번호", key="stu_num", placeholder="예: 12")
    s3.text_input("이름", key="stu_name", placeholder="이름 입력")
    s4.text_input("모둠원 (함께 실험한 친구)", key="stu_partner", placeholder="예: 홍길동")
    tip("중간에 창을 닫아야 할 때는 위의 <b>💾 저장</b>으로 파일을 받아 두고, <b>📂 불러오기</b>로 열면 이어서 작성할 수 있습니다.")

# ── 탐구 과정 안내 ─────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("<div class='card-t'>🧪 탐구 과정</div>", unsafe_allow_html=True)
    p_col1, p_col2 = st.columns([2.2, 1.0])
    with p_col1:
        st.markdown(f"""
<div class='steps'>
<ol>
<li><b>프로그램 접속</b> — 오른쪽 버튼(또는 <a href='{VA_URL}' target='_blank'>여기 ↗</a>)을 눌러 Vernier Video Analysis를 엽니다.
    제품키 입력 창이 나타나면 <span class='pill'>제품키: {VA_KEY}</span> 를 입력합니다.</li>
<li><b>영상 열기 및 설정</b> — <b>선생님의 지시에 따라</b> 분석할 영상을 불러오고 <b>클립 설정(시작·끝 프레임) → 교정막대자(축척) 설정 → 좌표축(원점) 설정 → 질점 찍기</b>를 차례대로 수행합니다.</li>
<li><b>데이터 붙여넣기 및 오류 검증</b> — 오른쪽 데이터 표를 복사(<b>Ctrl+A → Ctrl+C</b>)하거나 CSV로 내보내어 아래 <b>1. 데이터 정리</b>에 넣습니다. 붙여 넣은 값에 축척·원점·부호 오류가 있는지 자동으로 검증합니다.</li>
<li><b>그래프 분석 및 보고서 저장</b> — <b>2~5번</b> 항목을 작성하고 맨 아래에서 <b>PDF</b> 또는 <b>Word</b> 보고서를 내려받습니다.</li>
</ol>
</div>""", unsafe_allow_html=True)
    with p_col2:
        st.markdown(f"""
<div style="background:#EEF4FA;border:1px solid #CEDBE8;border-radius:10px;padding:14px;text-align:center;margin-top:4px;">
  <div style="font-size:12px;color:#475569;font-weight:600;margin-bottom:4px;">Vernier Video Analysis 제품키</div>
  <div style="font-size:20px;font-weight:800;color:#1F3B5C;letter-spacing:0.04em;margin-bottom:10px;">{VA_KEY}</div>
  <a href="{VA_URL}" target="_blank" style="text-decoration:none;">
    <div style="background:#1F3B5C;color:#fff;border-radius:8px;padding:10px 12px;font-weight:700;font-size:14px;">
      🔗 동영상 분석 프로그램 열기 ↗
    </div>
  </a>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# 7. [1] 데이터 정리 + 붙여넣은 값 오류 검증
# ════════════════════════════════════════════════════════════════════
sec(1, "데이터 정리", "붙여넣기 또는 CSV 업로드 · 자동 오류 검증")

d = None
mode = st.radio("입력 방식", ["붙여넣기", "CSV 파일"], key="input_mode", horizontal=True)
if mode == "붙여넣기":
    st.text_area("분석 프로그램의 데이터 표를 붙여 넣으세요", key="raw_data", height=170,
                 on_change=cb_paste, placeholder="여기에 붙여넣기 (Ctrl+V)")
    tip("분석 프로그램의 데이터 표를 클릭 → <b>Ctrl+A</b>(전체 선택) → <b>Ctrl+C</b>(복사) → 위 칸에 <b>Ctrl+V</b>. "
        "제목 행(Time, X, Y, VX, VY …)이 함께 붙어도 됩니다. 붙여 넣은 뒤 칸 바깥을 클릭하면 표로 바뀝니다.")
    raw_text = ss("raw_data")
else:
    st.file_uploader("내보낸 CSV 파일", type=["csv", "txt"], key="data_upload", on_change=cb_file)
    if ss("raw_file_name"):
        st.caption(f"불러온 파일: {ss('raw_file_name')}")
    tip("분석 프로그램 오른쪽 위 메뉴에서 Export → CSV로 내보낸 파일을 올리세요.")
    raw_text = ss("raw_file_text")

raw = parse_table(raw_text) if raw_text else None
if raw_text and raw is None:
    st.error("표를 인식하지 못했습니다. 숫자 데이터가 두 줄 이상 들어 있는지 확인하세요.")

if raw is not None:
    cols = list(raw.columns)
    guess = guess_columns(cols)
    with st.expander("🔧 열 맞추기 (자동으로 맞춰졌는지 확인)", expanded=not all(guess[k] for k in ("t", "x", "y"))):
        tip("앱이 열 이름을 보고 시간·위치·속도 열을 자동으로 골랐습니다. 다르게 골라졌으면 직접 바꾸세요. "
            "속도 열이 없으면 '(자동 계산)'을 두면 위치 데이터로 계산합니다.")
        mc = st.columns(5)
        opts_req, opts_opt = cols, ["(자동 계산)"] + cols
        mapping = {}
        for i, (k, lab, req) in enumerate([("t", "시간 t", True), ("x", "위치 x", True), ("y", "위치 y", True),
                                           ("vx", "속도 vx", False), ("vy", "속도 vy", False)]):
            opts = opts_req if req else opts_opt
            g = guess[k]
            idx = opts.index(g) if g in opts else (min(i, len(opts) - 1) if req else 0)
            if st.session_state.get(f"map_{k}") not in opts:
                st.session_state.pop(f"map_{k}", None)
            val = mc[i].selectbox(lab, opts, key=f"map_{k}", **sel_kw(f"map_{k}", idx))
            mapping[k] = None if val == "(자동 계산)" else val
    try:
        d = build_data(raw, mapping)
    except Exception as e:
        st.error(f"데이터 변환 중 문제가 생겼습니다: {e}")
        d = None

val_errors, val_warnings, val_metrics = [], [], {}
if d is not None:
    val_errors, val_warnings, val_metrics = validate_data(d)

    # ── 데이터 오류 검증 결과 안내 ──
    with st.container(border=True):
        st.markdown("<div class='card-t'>🔍 붙여넣은 데이터 오류 검증 결과</div>", unsafe_allow_html=True)
        if val_errors:
            st.error(f"⚠️ **데이터에서 {len(val_errors)}건의 오류가 발견되었습니다! 아래 내용을 확인하고 영상 분석 설정을 수정한 뒤 다시 붙여넣으세요.**")
            for msg in val_errors:
                st.markdown(f"- ❌ {msg}")
        if val_warnings:
            st.warning(f"💡 **데이터 점검 주의 사항 ({len(val_warnings)}건)**")
            for msg in val_warnings:
                st.markdown(f"- ⚠️ {msg}")
        if not val_errors and not val_warnings:
            st.success(
                f"✅ **데이터 검증 통과!** 총 **{val_metrics['n']}개**의 질점 데이터가 정상 범위로 인식되었습니다. "
                f"(비행 시간 Δt = {val_metrics['dt_total']:.3f} s, 수평 이동거리 Δx = {val_metrics['dx_total']:.3f} m, "
                f"평균 수평 속도 vx ≈ {val_metrics['mean_vx']:.2f} m/s, vy-t 기울기 가속도 ay ≈ {val_metrics['slope_ay']:.2f} m/s²)"
            )
        else:
            st.caption(
                f"현재 인식된 요약값: 점 {val_metrics['n']}개 · 비행 시간 Δt = {val_metrics['dt_total']:.3f} s · "
                f"수평 위치 변화 Δx = {val_metrics['dx_total']:.3f} m · 평균 vx = {val_metrics['mean_vx']:.2f} m/s · "
                f"vy-t 기울기 ay = {val_metrics['slope_ay']:.2f} m/s²"
            )

    st.markdown("<span class='auto-label'>▣ 자동 생성 — 성분별 측정값 표</span>", unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    fmt = {"t (s)": "{:.3f}", "x (m)": "{:.3f}", "vx (m/s)": "{:.3f}", "y (m)": "{:.3f}", "vy (m/s)": "{:.3f}"}
    with tc1:
        st.markdown("**수평 방향 (x, vx)**")
        st.dataframe(d[["t", "x", "vx"]].rename(columns={"t": "t (s)", "x": "x (m)", "vx": "vx (m/s)"})
                     .style.format(fmt), hide_index=True, **FULL, height=260)
    with tc2:
        st.markdown("**연직 방향 (y, vy)**")
        st.dataframe(d[["t", "y", "vy"]].rename(columns={"t": "t (s)", "y": "y (m)", "vy": "vy (m/s)"})
                     .style.format(fmt), hide_index=True, **FULL, height=260)
    st.download_button("📊 엑셀 파일 받기 (.xlsx)", make_xlsx(d),
                       file_name=f"{ss('stu_cls')}_{ss('stu_name')}_포물선운동_분석데이터.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("데이터를 붙여 넣거나 CSV 파일을 올리면 오류 검증 결과와 성분별 표·그래프가 자동으로 만들어집니다.")

# ════════════════════════════════════════════════════════════════════
# 8. [2] 그래프
# ════════════════════════════════════════════════════════════════════
sec(2, "그래프", "자동 생성 및 그래프 캡처 이미지 첨부(선택)")
if d is not None:
    f1, f2 = plotly_graphs(d)
    st.markdown("**[수평 방향 운동 — 위치-시간(x-t), 속도-시간(vx-t)]**")
    st.plotly_chart(f1, **FULL, config={"displaylogo": False})
    st.markdown("**[연직 방향 운동 — 위치-시간(y-t), 속도-시간(vy-t), 가속도-시간(ay-t)]**")
    st.plotly_chart(f2, **FULL, config={"displaylogo": False})
    st.markdown("<span class='auto-label'>▣ 그래프 눈금: vx-t와 ay-t 그래프는 측정값의 작은 흔들림이 과장되지 않도록 "
                "0이 보이는 넓은 눈금으로 그렸습니다.</span>", unsafe_allow_html=True)
    tip("위 그래프는 1번 데이터로 자동 생성되며 보고서(PDF/Word)에 자동으로 들어갑니다. "
        "분석 프로그램에서 직접 캡처한 그래프 이미지를 추가로 첨부하고 싶다면 아래 선택 칸을 이용하세요.")
else:
    st.info("1번에 데이터를 넣으면 그래프 5개(x-t, vx-t, y-t, vy-t, ay-t)가 여기에 자동으로 나타납니다.")

with st.expander("🖼️ (선택) 분석 프로그램에서 캡처한 그래프 이미지 직접 첨부하기"):
    ig1, ig2 = st.columns(2)
    with ig1:
        st.file_uploader("수평 방향 운동 그래프 이미지", type=["png", "jpg", "jpeg"], key="upload_img_h", on_change=cb_img_h)
        if ss("img_h_b64"):
            st.image(base64.b64decode(ss("img_h_b64")), caption=ss("img_h_name") or "수평 방향 그래프", **FULL)
    with ig2:
        st.file_uploader("연직 방향 운동 그래프 이미지", type=["png", "jpg", "jpeg"], key="upload_img_v", on_change=cb_img_v)
        if ss("img_v_b64"):
            st.image(base64.b64decode(ss("img_v_b64")), caption=ss("img_v_name") or "연직 방향 그래프", **FULL)

# ════════════════════════════════════════════════════════════════════
# 9. [3] 분석 및 해석
# ════════════════════════════════════════════════════════════════════
sec(3, "분석 및 해석")

qtext(Q["q3a"])
st.text_area("3-가", key="q3a", height=95, label_visibility="collapsed",
             placeholder="수평 위치(x)-시간 그래프의 기울기와 수평 속도(vx)-시간 그래프의 값을 근거로 시간에 따른 속력 변화를 서술하세요.")

qtext(Q["q3b"])
st.text_area("3-나", key="q3b", height=95, label_visibility="collapsed",
             placeholder="공이 날아가는 동안 수평 방향으로 작용하는 힘(알짜힘)과 뉴턴 운동 법칙을 관련지어 서술하세요.")

qtext(Q["q3c_desc"])
st.text_area("3-다", key="q3c_desc", height=95, label_visibility="collapsed",
             placeholder="연직 속도(vy)-시간 그래프의 모양(기울기)과 올라갈 때·최고점·내려올 때의 속도 변화를 서술하세요.")

qtext(Q["q3d_reason"])
st.text_area("3-라", key="q3d_reason", height=95, label_visibility="collapsed",
             placeholder="공이 날아가는 동안 연직 방향으로 작용하는 힘(중력)의 방향·크기와 가속도를 관련지어 서술하세요.")

qtext(Q["q3e_calc"])
with st.container(border=True):
    if d is not None:
        idx = list(range(len(d)))
        lab = lambda i: f"{i + 1}번째 점 · t = {d.t[i]:.3f} s (vy = {d.vy[i]:.3f} m/s)"
        for kk in ("ay_i1", "ay_i2"):
            if st.session_state.get(kk) is not None and st.session_state[kk] not in idx:
                st.session_state.pop(kk)
        a1, a2 = st.columns(2)
        i1 = a1.selectbox("시각 ①", idx, format_func=lab, key="ay_i1")
        i2 = a2.selectbox("시각 ②", idx, format_func=lab, key="ay_i2", **sel_kw("ay_i2", min(len(d) - 1, 5)))
        if i1 is not None and i1 < len(d) and i2 is not None and i2 < len(d):
            dt_sel = float(d.t[i2] - d.t[i1])
            dvy_sel = float(d.vy[i2] - d.vy[i1])
            ay_sel = dvy_sel / dt_sel if dt_sel != 0 else float("nan")
            a1.markdown(f"<span class='auto-label'>▣ t₁ = {d.t[i1]:.3f} s, vy₁ = {d.vy[i1]:.3f} m/s</span>",
                        unsafe_allow_html=True)
            a2.markdown(f"<span class='auto-label'>▣ t₂ = {d.t[i2]:.3f} s, vy₂ = {d.vy[i2]:.3f} m/s</span>",
                        unsafe_allow_html=True)
            with st.expander("💡 선택한 두 시각으로 계산한 참고값 확인하기"):
                if dt_sel != 0:
                    st.markdown(
                        f"- **식**: $a_y = \\dfrac{{v_{{y2}} - v_{{y1}}}}{{t_2 - t_1}}$\n"
                        f"- **대입**: $a_y = \\dfrac{{{d.vy[i2]:.3f} - ({d.vy[i1]:.3f})}}{{{d.t[i2]:.3f} - {d.t[i1]:.3f}}} = \\mathbf{{{ay_sel:.2f}\\text{{ m/s}}^2}}$\n"
                        f"- **전체 구간 vy-t 추세선 기울기**: $\\mathbf{{{val_metrics.get('slope_ay', 0.0):.2f}\\text{{ m/s}}^2}}$ "
                        f"(중력가속도 $-9.8\\text{{ m/s}}^2$와 크기 차이: ${abs(abs(ay_sel) - G):.2f}\\text{{ m/s}}^2$)"
                    )
                else:
                    st.warning("시각 ①과 시각 ②를 서로 다른 점으로 선택하세요.")
    else:
        st.caption("1번 데이터를 먼저 넣으면 두 시각의 측정값을 선택해 확인할 수 있습니다.")

    st.text_input("① 식 (예: ay = (vy2 - vy1) / (t2 - t1))", key="ay_formula")
    st.text_input("② 값 대입", key="ay_subst")
    r1, r2 = st.columns([1, 1.5])
    r1.text_input("③ 결과 ay (단위 m/s² 포함)", key="ay_result")
    r2.text_input("④ 중력 가속도(-9.8 m/s²)와 비교", key="ay_err")
    st.file_uploader("(선택) 손으로 쓴 계산 과정 사진", type=["png", "jpg", "jpeg"], key="calc_upload",
                     on_change=cb_calc_img)
    if st.session_state.get("calc_img_b64"):
        st.image(base64.b64decode(st.session_state["calc_img_b64"]), width=380, caption="올린 계산 과정 사진")

# ════════════════════════════════════════════════════════════════════
# 10. [4] 이론값과 실험값 비교
# ════════════════════════════════════════════════════════════════════
sec(4, "이론값과 실험값 비교")
qtext(Q["q4a"])

with st.container(border=True):
    st.markdown("**① 처음 속력 $v_0$와 발사각 $\\theta$ 구하기**")
    if d is not None:
        v0x_0 = float(d.vx.iloc[0])
        v0y_0 = float(d.vy.iloc[0])
        v0_0 = float(np.hypot(v0x_0, v0y_0))
        th_0_deg = float(np.degrees(np.arctan2(v0y_0, v0x_0)))
        c_info, c_btn = st.columns([3.2, 1.2])
        c_info.markdown(
            f"<span class='auto-label'>▣ 첫 번째 행 측정값 기준: vx₀ = {v0x_0:.3f} m/s, vy₀ = {v0y_0:.3f} m/s "
            f"→ v₀ = √(vx₀² + vy₀²) = {v0_0:.3f} m/s, 발사각 θ = {th_0_deg:.2f}°</span>",
            unsafe_allow_html=True,
        )
        if c_btn.button("📥 첫 행 값으로 자동 채우기", **FULL):
            st.session_state["v0x"] = f"{v0x_0:.3f}"
            st.session_state["v0y"] = f"{v0y_0:.3f}"
            st.session_state["v0"] = f"{v0_0:.3f}"
            st.session_state["theta"] = f"{th_0_deg:.2f}"
            st.rerun()
    v1, v2, v3, v4 = st.columns(4)
    v1.text_input("처음 수평 속도 vx₀ (m/s)", key="v0x")
    v2.text_input("처음 연직 속도 vy₀ (m/s)", key="v0y")
    v3.text_input("처음 속력 v₀ (m/s)", key="v0")
    v4.text_input("발사각 (°)", key="theta")
    tip("데이터 표 첫 번째 행의 vx, vy를 넣으면 $v_0 = \\sqrt{v_{x0}^2 + v_{y0}^2}$ 와 발사각 $\\theta = \\arctan(v_{y0}/v_{x0})$ 를 구할 수 있습니다.")

st.markdown("**② 시뮬레이션으로 이론값 구하기**")
st.markdown(f"""<a href="{SIM_URL}" target="_blank" style="text-decoration:none;">
<div style="background:#1F3B5C;color:#fff;border-radius:8px;padding:11px;text-align:center;font-weight:700;margin-bottom:6px;">
🚀 [포물선 운동 시뮬레이션] 새 창에서 열기 ↗</div></a>""", unsafe_allow_html=True)
tip("위에서 구한 처음 속력 $v_0$와 발사각을 시뮬레이션에 입력하여 이론값(수평 이동거리, 최고점 높이, 비행 시간)을 확인하고 아래 표에 적어 실험값과 비교해 보세요.")

with st.container(border=True):
    st.markdown("**③ 실험값과 이론값 비교 표**")
    if d is not None:
        exp_dx = float(d.x.iloc[-1] - d.x.iloc[0])
        exp_dy = float(d.y.max() - d.y.iloc[0])
        exp_dt = float(d.t.iloc[-1] - d.t.iloc[0])
        exp_ay = abs(float(val_metrics.get("slope_ay", 0.0)))
        b_col1, b_col2 = st.columns([3.2, 1.2])
        b_col1.markdown(
            f"<span class='auto-label'>▣ 내 데이터 실험값 참고: 수평 이동거리 Δx = {exp_dx:.3f} m · "
            f"최고점 높이(출발점 기준 Δy_max) = {exp_dy:.3f} m (최대 y = { float(d.y.max()):.3f} m) · "
            f"비행 시간 Δt = {exp_dt:.3f} s · |ay| = {exp_ay:.2f} m/s²</span>",
            unsafe_allow_html=True,
        )
        if b_col2.button("📥 실험값 자동 채우기", **FULL):
            st.session_state["exp_0"] = f"{exp_dx:.3f}"
            st.session_state["exp_1"] = f"{exp_dy:.3f}"
            st.session_state["exp_2"] = f"{exp_dt:.3f}"
            st.session_state["exp_3"] = f"{exp_ay:.2f}"
            if not str(st.session_state.get("th_3", "")).strip():
                st.session_state["th_3"] = "9.8"
            update_diff()
            st.rerun()

    hc = st.columns([1.5, 1.1, 1.1, 1.1])
    hc[0].markdown("**비교 항목**")
    hc[1].markdown("**실험값 (영상분석)**")
    hc[2].markdown("**이론값 (시뮬레이션)**")
    hc[3].markdown("**차이 |실험 - 이론|**")

    for j, item_name in enumerate(COMP_ITEMS):
        rc = st.columns([1.5, 1.1, 1.1, 1.1])
        rc[0].markdown(f"<div style='padding-top:8px;font-weight:600;'>{item_name}</div>", unsafe_allow_html=True)
        rc[1].text_input(f"실험값 {item_name}", key=f"exp_{j}", on_change=update_diff, label_visibility="collapsed")
        rc[2].text_input(f"이론값 {item_name}", key=f"th_{j}", on_change=update_diff, label_visibility="collapsed")
        rc[3].text_input(f"차이 {item_name}", key=f"er_{j}", label_visibility="collapsed")
    tip("실험값과 이론값에 숫자를 입력하면 <b>차이 |실험 - 이론|</b> 칸이 자동으로 계산됩니다(직접 수정도 가능).")

qtext(Q["q4b"])
o1, o2 = st.columns(2)
o1.text_area("측정 오차 (영상 분석·측정 과정에서 생긴 오차)", key="err_measure", height=135,
             placeholder="예: 교정막대자 길이 설정 오차, 좌표축 원점·기울기 설정 오차, 프레임마다 공의 중심을 찍을 때의 위치 오차, 카메라 렌즈 왜곡 등")
o2.text_area("모델의 가정 (포물선 운동 이론·시뮬레이션이 무시한 요인)", key="err_model", height=135,
             placeholder="예: 공기 저항, 공의 회전(마그누스 효과)과 크기 등 실제 운동에서 작용하지만 이론 모델에서는 무시한 요인")

# ════════════════════════════════════════════════════════════════════
# 11. [5] 결론
# ════════════════════════════════════════════════════════════════════
sec(5, "결론")
qtext(Q["q5"])
st.text_area("5-결론", key="q5", height=140, label_visibility="collapsed",
             placeholder="수평 방향 운동(등속 직선 운동 여부)과 연직 방향 운동(중력에 의한 등가속도 직선 운동 여부)의 측정 수치·그래프 근거를 들어 탐구 질문에 대한 결론을 서술하세요.")


# ════════════════════════════════════════════════════════════════════
# 12. 제출 전 점검 · 보고서 파일 만들기
# ════════════════════════════════════════════════════════════════════
def filled(*keys, min_len=1):
    return all(len(str(ss(k)).strip()) >= min_len for k in keys)


checks = [
    ("학생 정보", filled("stu_cls", "stu_num", "stu_name")),
    ("1. 데이터 정리 (오류 없음)", d is not None and len(val_errors) == 0),
    ("3-가·나 (수평 운동 분석)", filled("q3a", "q3b", min_len=5)),
    ("3-다·라 (연직 운동 분석)", filled("q3c_desc", "q3d_reason", min_len=5)),
    ("3-마 (연직 가속도 계산)", filled("ay_result") and (filled("ay_formula", "ay_subst") or bool(ss("calc_img_b64")))),
    ("4-가 (v0·발사각·비교표)", filled("v0x", "v0y", "v0", "theta", *[f"exp_{i}" for i in range(4)], *[f"th_{i}" for i in range(4)])),
    ("4-나 (오차 원인 분석)", filled("err_measure", "err_model", min_len=5)),
    ("5. 결론", filled("q5", min_len=10)),
]

sec("✓", "작성 점검 · 보고서 파일 만들기")
done = sum(ok for _, ok in checks)
st.progress(done / len(checks), text=f"작성 완료 {done} / {len(checks)}")
ck = st.columns(4)
for i, (name, ok) in enumerate(checks):
    ck[i % 4].markdown(("✅ " if ok else "⬜ ") + name)
tip("⬜ 표시가 남아 있어도 보고서 파일은 만들 수 있지만, 빈 칸은 보고서에 '(미작성)'으로 표시됩니다.")


def report_dict():
    sel = lambda k: (None if ss(k, None) is None or d is None or ss(k, None) >= len(d) else int(ss(k)))
    return dict(
        grade=ss("stu_grade"), cls=ss("stu_cls"), num=ss("stu_num"),
        name=ss("stu_name"), partner=ss("stu_partner"),
        made=now_kst(), d=d,
        ay_pts=(sel("ay_i1"), sel("ay_i2")),
        val_errors=val_errors, val_warnings=val_warnings,
    )


# ── DOCX 생성 ──────────────────────────────────────────────────────
def build_docx(R):
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Mm, Pt, RGBColor

    doc = Document()
    sec_ = doc.sections[0]
    sec_.page_width, sec_.page_height = Mm(210), Mm(297)
    sec_.left_margin = sec_.right_margin = Mm(16)
    sec_.top_margin = sec_.bottom_margin = Mm(14)
    st_n = doc.styles["Normal"]
    st_n.font.name, st_n.font.size = "맑은 고딕", Pt(10)
    st_n.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")
    st_n.paragraph_format.space_after = Pt(2)

    def shade(cell, hexcolor):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), hexcolor)
        tcPr.append(shd)

    def borders(cell, color, sz="8"):
        tcPr = cell._tc.get_or_add_tcPr()
        b = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), sz)
            e.set(qn("w:color"), color)
            b.append(e)
        tcPr.append(b)

    def run(p, text, bold=False, size=None, color=None):
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        return r

    def heading(num, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.keep_with_next = True
        run(p, f"{num}. {text}", bold=True, size=12.5, color="1F3B5C")
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        bt = OxmlElement("w:bottom")
        bt.set(qn("w:val"), "single")
        bt.set(qn("w:sz"), "10")
        bt.set(qn("w:color"), "1F3B5C")
        bdr.append(bt)
        pPr.append(bdr)

    def question(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.keep_with_next = True
        run(p, text, bold=True, size=10)

    def student_box(text, label="학생 작성"):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        shade(c, "FFF8DC")
        borders(c, "E0B84A", "10")
        p = c.paragraphs[0]
        run(p, f"[{label}]", size=7.5, color="9A7A1E")
        body = str(text).strip()
        p2 = c.add_paragraph()
        if body:
            run(p2, body, size=10)
        else:
            run(p2, "(미작성)", size=10, color="C0392B")
        return t

    def auto_label(text="자동 생성 (앱 계산)"):
        p = doc.add_paragraph()
        p.paragraph_format.keep_with_next = True
        run(p, f"▣ {text}", size=7.5, color="2E6DA4")

    def grid(headers, rows, stu_cols=(), widths=None, font=9):
        t = doc.add_table(rows=1 + len(rows), cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.style = "Table Grid"
        for j, h in enumerate(headers):
            c = t.cell(0, j)
            c.text = ""
            run(c.paragraphs[0], h, bold=True, size=font, color="1F3B5C")
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            shade(c, "E3ECF6")
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                c = t.cell(i + 1, j)
                c.text = ""
                is_stu = j in stu_cols
                txt = str(v) if str(v).strip() else ("(미작성)" if is_stu else "")
                run(c.paragraphs[0], txt, size=font, color=("C0392B" if is_stu and not str(v).strip() else None))
                c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if is_stu:
                    shade(c, "FFF8DC")
        if widths:
            for row in t.rows:
                for j, w in enumerate(widths):
                    row.cells[j].width = Mm(w)
        return t

    # 머리
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, f"{COURSE} · {UNIT_INFO}", size=9, color="5B6B7D")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, TITLE, bold=True, size=15, color="1F3B5C")

    # 단원정보 / 성취기준 / 학습목표 / 탐구질문 표
    info_tbl = doc.add_table(rows=4, cols=2)
    info_tbl.style = "Table Grid"
    info_rows = [
        ("단원정보", UNIT_INFO),
        ("성취기준", STD_INFO),
        ("학습목표", GOAL_INFO),
        ("탐구질문", INQUIRY_Q),
    ]
    for idx_r, (k_txt, v_txt) in enumerate(info_rows):
        c0, c1 = info_tbl.cell(idx_r, 0), info_tbl.cell(idx_r, 1)
        c0.text, c1.text = "", ""
        shade(c0, "E3ECF6")
        run(c0.paragraphs[0], k_txt, bold=True, size=9, color="1F3B5C")
        c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run(c1.paragraphs[0], v_txt, bold=(idx_r >= 2), size=9, color=("1D4ED8" if idx_r >= 2 else None))
        c0.width, c1.width = Mm(28), Mm(150)

    doc.add_paragraph()
    grid(["학년", "반", "번호", "이름", "모둠원 (함께 실험한 친구)"],
         [[R["grade"], R["cls"], R["num"], R["name"], R["partner"]]],
         stu_cols=(0, 1, 2, 3, 4), widths=[22, 22, 22, 42, 70], font=9)
    p = doc.add_paragraph()
    run(p, f"보고서 생성: {R['made']}", size=8.5, color="5B6B7D")

    D = R["d"]
    heading(1, "데이터 정리 (성분별 측정값)")
    if D is not None:
        auto_label()
        rows = [[i + 1, fnum(r.t), fnum(r.x), fnum(r.vx), fnum(r.y), fnum(r.vy)] for i, r in D.iterrows()]
        grid(["#", "t (s)", "x (m)", "vx (m/s)", "y (m)", "vy (m/s)"], rows, font=8,
             widths=[12, 32, 33, 33, 33, 35])
    else:
        student_box("", "데이터 없음")

    heading(2, "그래프")
    if D is not None:
        auto_label()
        doc.add_picture(io.BytesIO(mpl_png(D)), width=Mm(176))
    for img_key, cap in [("img_h_b64", "학생 첨부: 수평 방향 운동 그래프"), ("img_v_b64", "학생 첨부: 연직 방향 운동 그래프")]:
        if ss(img_key):
            p = doc.add_paragraph()
            run(p, cap, size=8.5, color="1F3B5C", bold=True)
            try:
                doc.add_picture(io.BytesIO(base64.b64decode(ss(img_key))), width=Mm(140))
            except Exception:
                pass

    heading(3, "분석 및 해석")
    question(Q["q3a"]); student_box(ss("q3a"))
    question(Q["q3b"]); student_box(ss("q3b"))
    question(Q["q3c_desc"]); student_box(ss("q3c_desc"))
    question(Q["q3d_reason"]); student_box(ss("q3d_reason"))
    question(Q["q3e_calc"])
    if R["ay_pts"] and D is not None and None not in R["ay_pts"]:
        i1, i2 = R["ay_pts"]
        auto_label(f"선택한 시각의 측정값: t1 = {D.t[i1]:.3f} s, vy1 = {D.vy[i1]:.3f} m/s  /  "
                   f"t2 = {D.t[i2]:.3f} s, vy2 = {D.vy[i2]:.3f} m/s")
    stu_rows = [["① 식", ss("ay_formula")], ["② 값 대입", ss("ay_subst")],
                ["③ 결과 ay", ss("ay_result")], ["④ 중력 가속도와 비교", ss("ay_err")]]
    t = grid(["단계", "학생 작성"], stu_rows, stu_cols=(1,), widths=[38, 140], font=9.5)
    for row in t.rows[1:]:
        row.cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
    if ss("calc_img_b64"):
        p = doc.add_paragraph()
        run(p, "손으로 쓴 계산 과정 (학생 제출 사진)", size=8, color="9A7A1E")
        try:
            doc.add_picture(io.BytesIO(base64.b64decode(ss("calc_img_b64"))), width=Mm(110))
        except Exception:
            pass

    heading(4, "이론값과 실험값 비교")
    question(Q["q4a"])
    p = doc.add_paragraph()
    run(p, "① 처음 속력 v0와 발사각 구하기", bold=True, size=9.5)
    grid(["처음 수평 속도 vx0 (m/s)", "처음 연직 속도 vy0 (m/s)", "처음 속력 v0 (m/s)", "발사각 (°)"],
         [[ss("v0x"), ss("v0y"), ss("v0"), ss("theta")]], stu_cols=(0, 1, 2, 3), widths=[44, 44, 45, 45])
    p = doc.add_paragraph()
    run(p, "② 이론값(포물선 운동 시뮬레이션)과 실험값 비교", bold=True, size=9.5)
    comp_rows = [[COMP_ITEMS[j], ss(f"exp_{j}"), ss(f"th_{j}"), ss(f"er_{j}")] for j in range(4)]
    grid(["비교 항목", "실험값 (영상분석)", "이론값 (시뮬레이션)", "차이 |실험 - 이론|"],
         comp_rows, stu_cols=(1, 2, 3), widths=[50, 42, 43, 43], font=9)

    question(Q["q4b"])
    t = doc.add_table(rows=2, cols=2)
    t.style = "Table Grid"
    for j, (h, k) in enumerate([("측정 오차 (측정 과정에서 생긴 오차)", "err_measure"),
                                ("모델의 가정 (이론이 무시한 요인)", "err_model")]):
        hcell = t.cell(0, j)
        hcell.text = ""
        run(hcell.paragraphs[0], h, bold=True, size=9, color="1F3B5C")
        shade(hcell, "E3ECF6")
        c = t.cell(1, j)
        c.text = ""
        shade(c, "FFF8DC")
        run(c.paragraphs[0], "[학생 작성]", size=7.5, color="9A7A1E")
        body = str(ss(k)).strip()
        run(c.add_paragraph(), body or "(미작성)", size=10, color=None if body else "C0392B")

    heading(5, "결론")
    question(Q["q5"])
    student_box(ss("q5"))

    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()


# ── PDF 생성 ───────────────────────────────────────────────────────
def build_pdf(R):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table,
                                    TableStyle)

    if "NG" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("NG", FONT_REG))
        pdfmetrics.registerFont(TTFont("NGB", FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_REG))
    NAVY, STU, STU_L, HEAD = (colors.HexColor("#1F3B5C"), colors.HexColor("#FFF8DC"),
                              colors.HexColor("#E0B84A"), colors.HexColor("#E3ECF6"))
    P = lambda size=9.5, bold=False, color="#222222", align=0, lead=None: ParagraphStyle(
        "x", fontName="NGB" if bold else "NG", fontSize=size, leading=lead or size * 1.45,
        textColor=colors.HexColor(color), alignment=align, wordWrap="CJK")
    _circ = str.maketrans({"①": "(1)", "②": "(2)", "③": "(3)", "④": "(4)", "⑤": "(5)", "θ": "theta", "₀": "0", "₁": "1", "₂": "2"})
    esc = lambda s: xml_escape(str(s).translate(_circ)).replace("\n", "<br/>")
    W = 178 * mm
    el = []

    def heading(num, text):
        t = Table([[Paragraph(f"{num}. {esc(text)}", P(12, True, "#1F3B5C"))]], colWidths=[W])
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        el.append(t)

    def question(text):
        el.append(Spacer(1, 4))
        el.append(Paragraph(esc(text), P(9.5, True)))
        el.append(Spacer(1, 2))

    def student_box(text, label="[학생 작성]"):
        body = str(text).strip()
        inner = [Paragraph(label, P(7, False, "#9A7A1E")),
                 Paragraph(esc(body) if body else "(미작성)", P(9.5, False, "#222222" if body else "#C0392B"))]
        t = Table([[inner]], colWidths=[W])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), STU), ("BOX", (0, 0), (-1, -1), 0.9, STU_L),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        el.append(t)

    def auto_label(text="▣ 자동 생성 (앱 계산)"):
        el.append(Paragraph(esc(text), P(7.5, False, "#2E6DA4")))

    def grid(headers, rows, stu_cols=(), widths=None, size=8.5, left_cols=()):
        data = [[Paragraph(esc(h), P(size, True, "#1F3B5C", 1)) for h in headers]]
        for r in rows:
            line = []
            for j, v in enumerate(r):
                empty = j in stu_cols and not str(v).strip()
                line.append(Paragraph("(미작성)" if empty else esc(v),
                                      P(size, False, "#C0392B" if empty else "#222222", 0 if j in left_cols else 1)))
            data.append(line)
        cw = [w * mm for w in widths] if widths else [W / len(headers)] * len(headers)
        t = Table(data, colWidths=cw, repeatRows=1)
        sty = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D2")), ("BACKGROUND", (0, 0), (-1, 0), HEAD),
               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
               ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
        for j in stu_cols:
            sty.append(("BACKGROUND", (j, 1), (j, -1), STU))
        t.setStyle(TableStyle(sty))
        el.append(t)

    el += [
        Paragraph(esc(f"{COURSE} · {UNIT_INFO}"), P(8.5, False, "#5B6B7D", 1)),
        Paragraph(esc(TITLE), P(15, True, "#1F3B5C", 1, 21)),
        Spacer(1, 4),
    ]
    # 단원정보 / 성취기준 / 학습목표 / 탐구질문 표
    curr_data = [
        [Paragraph("단원정보", P(8.5, True, "#1F3B5C", 1)), Paragraph(esc(UNIT_INFO), P(8.5, True, "#222222", 0))],
        [Paragraph("성취기준", P(8.5, True, "#1F3B5C", 1)), Paragraph(esc(STD_INFO), P(8.5, False, "#222222", 0))],
        [Paragraph("학습목표", P(8.5, True, "#1F3B5C", 1)), Paragraph(esc(GOAL_INFO), P(8.5, True, "#1D4ED8", 0))],
        [Paragraph("탐구질문", P(8.5, True, "#1F3B5C", 1)), Paragraph(esc(INQUIRY_Q), P(8.5, True, "#1D4ED8", 0))],
    ]
    curr_t = Table(curr_data, colWidths=[26 * mm, 152 * mm])
    curr_t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#94A3B8")),
        ("BACKGROUND", (0, 0), (0, -1), HEAD),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    el.append(curr_t)
    el.append(Spacer(1, 5))

    grid(["학년", "반", "번호", "이름", "모둠원 (함께 실험한 친구)"],
         [[R["grade"], R["cls"], R["num"], R["name"], R["partner"]]],
         stu_cols=(0, 1, 2, 3, 4), widths=[22, 22, 22, 42, 70])
    el.append(Spacer(1, 3))
    el.append(Paragraph(esc(f"보고서 생성: {R['made']}"), P(8, False, "#5B6B7D")))

    D = R["d"]
    heading(1, "데이터 정리 (성분별 측정값)")
    if D is not None:
        auto_label()
        grid(["#", "t (s)", "x (m)", "vx (m/s)", "y (m)", "vy (m/s)"],
             [[i + 1, fnum(r.t), fnum(r.x), fnum(r.vx), fnum(r.y), fnum(r.vy)] for i, r in D.iterrows()],
             widths=[12, 33, 33, 33, 33, 34], size=7.5)

    if D is not None:
        mark = len(el)
        heading(2, "그래프")
        auto_label()
        el.append(Image(io.BytesIO(mpl_png(D)), width=W, height=W * 5.6 / 10))
        el[mark:] = [KeepTogether(el[mark:])]
    else:
        heading(2, "그래프")

    for img_key, cap in [("img_h_b64", "학생 첨부: 수평 방향 운동 그래프"), ("img_v_b64", "학생 첨부: 연직 방향 운동 그래프")]:
        if ss(img_key):
            try:
                from reportlab.lib.utils import ImageReader
                raw_img = base64.b64decode(ss(img_key))
                iw, ih = ImageReader(io.BytesIO(raw_img)).getSize()
                w_ = 135 * mm
                el.append(Paragraph(cap, P(8, True, "#1F3B5C")))
                el.append(Image(io.BytesIO(raw_img), width=w_, height=min(w_ * ih / iw, 95 * mm)))
            except Exception:
                pass

    heading(3, "분석 및 해석")
    question(Q["q3a"]); student_box(ss("q3a"))
    question(Q["q3b"]); student_box(ss("q3b"))
    question(Q["q3c_desc"]); student_box(ss("q3c_desc"))
    question(Q["q3d_reason"]); student_box(ss("q3d_reason"))
    question(Q["q3e_calc"])
    if R["ay_pts"] and D is not None and None not in R["ay_pts"]:
        i1, i2 = R["ay_pts"]
        auto_label(f"▣ 선택한 시각의 측정값: t1 = {D.t[i1]:.3f} s, vy1 = {D.vy[i1]:.3f} m/s  /  "
                   f"t2 = {D.t[i2]:.3f} s, vy2 = {D.vy[i2]:.3f} m/s")
    rows = [["(1) 식", ss("ay_formula")], ["(2) 값 대입", ss("ay_subst")], ["(3) 결과 ay", ss("ay_result")],
            ["(4) 중력 가속도와 비교", ss("ay_err")]]
    grid(["단계", "학생 작성"], rows, stu_cols=(1,), widths=[40, 138], size=9, left_cols=(1,))
    if ss("calc_img_b64"):
        try:
            from reportlab.lib.utils import ImageReader
            raw_img = base64.b64decode(ss("calc_img_b64"))
            iw, ih = ImageReader(io.BytesIO(raw_img)).getSize()
            w_ = 110 * mm
            el.append(Paragraph("손으로 쓴 계산 과정 (학생 제출 사진)", P(7.5, False, "#9A7A1E")))
            el.append(Image(io.BytesIO(raw_img), width=w_, height=min(w_ * ih / iw, 140 * mm)))
        except Exception:
            pass

    heading(4, "이론값과 실험값 비교")
    question(Q["q4a"])
    el.append(Paragraph("(1) 처음 속력 v0와 발사각 구하기", P(9, True)))
    grid(["처음 수평 속도 vx0 (m/s)", "처음 연직 속도 vy0 (m/s)", "처음 속력 v0 (m/s)", "발사각 (°)"],
         [[ss("v0x"), ss("v0y"), ss("v0"), ss("theta")]], stu_cols=(0, 1, 2, 3), widths=[44, 44, 45, 45])
    el.append(Spacer(1, 4))
    el.append(Paragraph("(2) 이론값(포물선 운동 시뮬레이션)과 실험값 비교", P(9, True)))
    comp_rows = [[COMP_ITEMS[j], ss(f"exp_{j}"), ss(f"th_{j}"), ss(f"er_{j}")] for j in range(4)]
    grid(["비교 항목", "실험값 (영상분석)", "이론값 (시뮬레이션)", "차이 |실험 - 이론|"],
         comp_rows, stu_cols=(1, 2, 3), widths=[50, 42, 43, 43], size=8.5)

    question(Q["q4b"])
    cell = lambda k: [Paragraph("[학생 작성]", P(7, False, "#9A7A1E")),
                      Paragraph(esc(ss(k)) if str(ss(k)).strip() else "(미작성)",
                                P(9.5, False, "#222222" if str(ss(k)).strip() else "#C0392B"))]
    t = Table([[Paragraph("측정 오차 (측정 과정에서 생긴 오차)", P(9, True, "#1F3B5C", 1)),
                Paragraph("모델의 가정 (이론이 무시한 요인)", P(9, True, "#1F3B5C", 1))],
               [cell("err_measure"), cell("err_model")]], colWidths=[W / 2, W / 2])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C4D2")),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("BACKGROUND", (0, 1), (-1, 1), STU),
                           ("VALIGN", (0, 1), (-1, 1), "TOP"), ("BOTTOMPADDING", (0, 1), (-1, 1), 8)]))
    el.append(t)

    heading(5, "결론")
    question(Q["q5"])
    student_box(ss("q5"))

    def footer(cv, doc_):
        cv.saveState()
        cv.setFont("NG", 7.5)
        cv.setFillColor(colors.HexColor("#8A97A6"))
        cv.drawString(16 * mm, 9 * mm, f"{R['grade']}학년 {R['cls']}반 {R['num']}번 {R['name']} (모둠원: {R['partner']})  |  {TITLE}")
        cv.drawRightString(194 * mm, 9 * mm, f"{doc_.page}쪽")
        cv.restoreState()

    bio = io.BytesIO()
    SimpleDocTemplate(bio, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm,
                      bottomMargin=16 * mm, title=TITLE, author=R["name"]).build(
        el, onFirstPage=footer, onLaterPages=footer)
    return bio.getvalue()


with st.container(border=True):
    st.markdown("<div class='card-t'>📤 보고서 파일 만들기</div>", unsafe_allow_html=True)
    b1, b2 = st.columns([1, 2])
    if b1.button("📄 보고서 파일 만들기", type="primary", **FULL):
        with st.spinner("보고서를 만드는 중입니다…"):
            R = report_dict()
            out = {"docx": build_docx(R), "pdf": None, "err": None}
            if os.path.exists(FONT_REG):
                try:
                    out["pdf"] = build_pdf(R)
                except Exception as e:
                    out["err"] = str(e)
            else:
                out["err"] = "fonts/NanumGothic.ttf 가 없어 PDF를 만들 수 없습니다."
            student_id = f"{ss('stu_grade')}{ss('stu_cls').zfill(2)}{ss('stu_num').zfill(2)}" if ss("stu_cls") or ss("stu_num") else ""
            out["name"] = f"{student_id}_{ss('stu_name')}_{ss('stu_partner')}_포물선운동_영상분석실습".strip("_").replace("__", "_")
            st.session_state["exports"] = out
    b2.markdown("<div class='tip' style='margin-top:4px'>💡 내용을 고친 뒤에는 이 버튼을 <b>다시</b> 눌러야 "
                "고친 내용이 보고서 파일(PDF / Word)에 반영됩니다.</div>", unsafe_allow_html=True)
    ex = st.session_state.get("exports")
    if ex:
        x1, x2 = st.columns(2)
        if ex.get("pdf"):
            x1.download_button("⬇️ PDF 보고서 받기", ex["pdf"], file_name=ex["name"] + ".pdf",
                               mime="application/pdf", **FULL, type="primary")
        else:
            x1.warning(ex.get("err") or "PDF를 만들지 못했습니다.")
        x2.download_button("⬇️ Word 보고서 받기 (.docx)", ex["docx"], file_name=ex["name"] + ".docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           **FULL)

st.caption("사곡고등학교 물리학Ⅱ · 지표면 역학 분석 - 포물선 운동 영상 분석 실습")
