# -*- coding: utf-8 -*-
"""
[수행평가] 지표면 역학 분석 — 포물선 운동 영상 분석 및 데이터 해석
2026학년도 2학기 · 2학년 역학과 에너지 · 사곡고등학교

필요 패키지(requirements.txt):
    streamlit>=1.36  pandas  numpy  plotly  python-docx  openpyxl  matplotlib  reportlab
PDF·그래프 한글 표시용 글꼴(저장소에 함께 올리기):
    fonts/NanumGothic.ttf, fonts/NanumGothicBold.ttf   (SIL OFL, 무료 배포 가능)
교사 코드(제공 데이터 열기·교사용 확인):
    .streamlit/secrets.toml 에  teacher_code = "원하는코드"  를 넣어 두면 그 값을 사용
    (넣지 않으면 아래 DEFAULT_TEACHER_CODE 사용 — 공개 저장소라면 반드시 secrets 사용)
"""
import base64
import io
import json
import os
import re
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

# ════════════════════════════════════════════════════════════════════
# 0. 설정값 (매년 바뀌는 값은 여기만 고치면 됨)
# ════════════════════════════════════════════════════════════════════
TITLE = "지표면 역학 분석 — 포물선 운동 영상 분석 및 데이터 해석"
COURSE = "2026학년도 2학기 · 2학년 역학과 에너지"
AREA = "역학과 에너지로 증명하는 최적의 위성 임무 궤도 설계 탐구 ①"
VA_URL = "https://videoanalysis.app?key=tvampus85n"
VA_KEY = "tvampus85n"
VA_EXPIRE = "2026년 11월 2일(월)"
CLIP = "207 ~ 233"
N_POINTS = 29
PADLET_URL = "https://padlet.app/qr-code/s024pudcl47khfjoa5j7?source=image"   # 분석 영상 내려받기
PADLET_QR_B64 = "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"
MASS = 0.1   # kg (계산 편의를 위한 가정값)
G = 9.8      # m/s²
DEFAULT_TEACHER_CODE = "sagok-physics"
SIM_URL = "https://physics-course.streamlit.app/projectile_analysis_excel"   # 이론값 계산용 시뮬레이션 페이지
KST = ZoneInfo("Asia/Seoul")

PADLET_SUBMIT_URL = "https://padlet.com/sgh/submission-request/oO6VvPdgOPMmvrwD"   # 모둠 과제 제출방 (모든 모둠 공통)
PADLET_INFO_URL = "https://padlet.com/sgh/padlet-s024pudcl47khfjoa5j7"            # 공통 안내방
PADLET_INDIV_URL = "https://padlet.com/sgh/submission-request/1JkMb03PA7RNvdD8"   # 개인 과제 제출방
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_REG = os.path.join(HERE, "fonts", "NanumGothic.ttf")
FONT_BOLD = os.path.join(HERE, "fonts", "NanumGothicBold.ttf")

ROLES = ["영상 조작·데이터 추출", "계산·보고서 서술", "(공동)"]
BACKUP_REASONS = ["질점·교정·좌표축 설정 오류 (학생)", "기기·네트워크·프로그램 오류"]

# 문항 문구 (화면·DOCX·PDF가 같은 문구를 사용)
Q = {
    "q3a": "가. 수평 방향: x-t 그래프의 기울기와 vx-t 그래프의 모양을 근거로 수평 방향 운동의 종류를 쓰고, "
           "수평 방향으로 알짜힘이 작용하는지 설명하시오.",
    "q3b": "나. 연직 방향: y-t 그래프의 기울기 변화와 vy-t 그래프의 모양을 근거로 연직 방향 운동의 종류를 쓰고, "
           "연직 방향으로 작용하는 알짜힘이 무엇인지 설명하시오.",
    "q3c": "다. 연직 가속도 산출: 연직 방향 가속도 ay를 직접 계산하고 중력 가속도와 비교하시오. "
           "(식 → 값 대입 → 결과(단위) 순서로 쓸 것)",
    "q4": "위 표의 세 지점의 E 값을 근거로 역학적 에너지가 보존된다고 볼 수 있는지 판단하시오. "
          "판단의 근거가 된 수치를 함께 쓰고, 높이에 따라 Ek와 Ep가 어떻게 바뀌는지 표의 값과 연결하여 설명하시오. "
          "(※ 본 실험은 공기가 있는 실제 상황에서의 측정 데이터이므로, 표의 구체적인 수치(데이터 기반)를 근거로 제시하고 물리 이론을 바탕으로 종합하여 서술하시오.)",
    "q5a": "가. 1번 표 첫 번째 점의 vx, vy로 처음 속력 v0와 발사각을 구하시오. (영상 분석 야구공의 발사각은 근사적으로 약 19°입니다.) "
           "이 값을 [포물선 운동 시뮬레이션]에 입력하여 얻은 이론값을 실험값과 비교하고, 두 값의 차이를 구하시오.",
    "q5b": "나. 이론값과 실험값이 차이 나는 원인을 '측정 오차'와 '모델의 가정' 두 가지로 나누어 쓰시오.",
    "q6a": "Q1. 비스듬히 던진 공의 운동을 수평·연직 두 방향으로 나누어 설명할 수 있는 이유를 쓰시오. "
           "연직 방향 속도가 변하는 동안 수평 방향 속도(vx)가 어떠했는지 1번 표와 3-다의 수치를 근거로 쓸 것.",
    "q6b": "Q2. 포물선 경로에서 운동 에너지와 위치 에너지는 어떻게 바뀌며, 그 합은 일정하게 유지되는가? (4번 결과를 근거로)",
}
COMP_ITEMS = ["최고점 도달 시간(s)", "최고점 높이(m)", "수평 도달 거리(m)"]

# 저장(JSON)·불러오기 대상 키
SAVE_KEYS = [
    "cls", "s1_num", "s1_name", "s1_role", "s2_num", "s2_name", "s2_role",
    "input_mode", "raw_data", "raw_file_text", "raw_file_name",
    "map_t", "map_x", "map_y", "map_vx", "map_vy",
    "backup_used", "backup_reason", "backup_time", "own_raw_backup",
    "q3a", "q3b", "ay_i1", "ay_i2", "ay_formula", "ay_subst",
    "ay_result", "ay_err", "calc_img_b64", "calc_img_name",
    "e_top", "e_after", "q4",
    "v0x", "v0y", "v0", "theta", "err_measure", "err_model", "q6a", "q6b",
    *[f"exp_{i}" for i in range(3)], *[f"th_{i}" for i in range(3)], *[f"er_{i}" for i in range(3)],
]

# ════════════════════════════════════════════════════════════════════
# 1. 불러오기 대기 데이터 반영 (위젯 생성 전에 실행)
# ════════════════════════════════════════════════════════════════════
if "_pending_load" in st.session_state:
    for k, v in st.session_state.pop("_pending_load").items():
        if k in SAVE_KEYS:
            st.session_state[k] = v
    st.session_state["_loaded_msg"] = True

for k, v in {"backup_used": False, "raw_file_text": "", "raw_file_name": "",
             "own_raw_backup": "", "backup_time": "", "calc_img_b64": None,
             "calc_img_name": None, "exports": None}.items():
    st.session_state.setdefault(k, v)

# ════════════════════════════════════════════════════════════════════
# 2. 디자인 (노란 칸 = 학생 작성 영역 : 화면과 보고서 파일에서 같은 색)
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
:root { --navy:#1F3B5C; --blue:#2E6DA4; --soft:#EEF4FA; --line:#D5DEE8; --stu:#FFF8DC; --stu-line:#E8C766; }
[data-testid="stAppViewMainContent"], .main { font-size: 15px; }
.hero { background: linear-gradient(135deg,#1F3B5C 0%,#2E6DA4 100%); color:#fff; border-radius:14px;
        padding:20px 24px; margin-bottom:6px; }
.hero .k { font-size:13px; opacity:.85; letter-spacing:.3px; }
.hero h1 { color:#fff !important; font-size:24px !important; margin:4px 0 6px 0 !important; padding:0 !important; }
.hero .m { font-size:13px; opacity:.9; }
.sec { display:flex; align-items:center; gap:10px; margin:26px 0 6px 0; padding-bottom:6px;
       border-bottom:2px solid var(--navy); }
.sec .b { background:var(--navy); color:#fff; border-radius:8px; min-width:30px; height:30px; display:flex;
          align-items:center; justify-content:center; font-weight:700; }
.sec .t { font-size:19px; font-weight:700; color:var(--navy); }
.sec .s { font-size:13px; color:#6B7A8C; margin-left:auto; }
.q { font-weight:600; margin:14px 0 4px 0; line-height:1.55; }
.tip { font-size:13px; color:#5B6B7D; background:#F4F7FA; border-left:3px solid #9DB3C9;
       padding:6px 10px; border-radius:4px; margin:4px 0 8px 0; }
.legend { font-size:13px; color:#5B6B7D; }
.legend .sw { display:inline-block; width:14px; height:14px; border-radius:3px; vertical-align:-2px; margin-right:4px; }
.card-t { font-weight:700; color:var(--navy); font-size:16px; margin-bottom:6px; }
.goal li, .steps li { margin-bottom:4px; line-height:1.55; }
.score { width:100%; border-collapse:collapse; font-size:14px; }
.score td, .score th { border:1px solid var(--line); padding:6px 8px; vertical-align:top; }
.score th { background:var(--soft); color:var(--navy); text-align:left; }
.pill { display:inline-block; background:var(--soft); color:var(--navy); border-radius:20px; padding:2px 10px;
        font-size:13px; margin:2px 4px 2px 0; border:1px solid var(--line); }
.src-own { background:#E8F5E9; border:1px solid #A5D6A7; color:#1B5E20; border-radius:8px; padding:8px 12px; }
.src-bk  { background:#FFF3E0; border:1px solid #FFCC80; color:#8A4B00; border-radius:8px; padding:8px 12px; }
/* 학생 작성 칸 */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
    background: var(--stu) !important; border:1px solid var(--stu-line) !important; color:#222 !important; }
button[kind="primary"] { background:#1F3B5C !important; border-color:#1F3B5C !important; }
button[kind="primary"]:hover { background:#2E6DA4 !important; border-color:#2E6DA4 !important; }
.auto-label { font-size:12px; color:#2E6DA4; font-weight:600; }
@media print {
  @page { margin: 14mm; size: A4; }
  header, [data-testid="stSidebar"], [data-testid="stToolbar"], [data-testid="stExpander"],
  [data-testid="stFileUploader"], [data-testid="stPopover"], button, .tip, .noprint { display:none !important; }
  .stMarkdown, .stPlotlyChart, .stImage, .stDataFrame { page-break-inside: avoid !important; }
}
</style>
""", unsafe_allow_html=True)


# 버전에 따라 너비 옵션 이름이 다름 (1.46 이상: width="stretch")
_VER = tuple(int(x) for x in re.findall(r"\d+", st.__version__)[:2])
FULL = {"width": "stretch"} if _VER >= (1, 46) else {"use_container_width": True}


def sec(num, title, sub=""):
    st.markdown(f"<div class='sec'><div class='b'>{num}</div><div class='t'>{title}</div>"
                f"<div class='s'>{sub}</div></div>", unsafe_allow_html=True)


def tip(text):
    st.markdown(f"<div class='tip'>💡 {text}</div>", unsafe_allow_html=True)


def qtext(text):
    st.markdown(f"<div class='q'>{text}</div>", unsafe_allow_html=True)


def ss(k, default=""):
    v = st.session_state.get(k, default)
    return default if v is None else v


def teacher_code():
    try:
        return str(st.secrets["teacher_code"])
    except Exception:
        return DEFAULT_TEACHER_CODE


def now_kst():
    return datetime.now(KST).strftime("%Y-%m-%d %H:%M")


def load_submission_html():
    candidates = [
        os.path.join(HERE, "..", "static", "submission_list_1.html"),
        os.path.join(HERE, "..", "1차시_JSON_제출목록.html"),
        os.path.join(HERE, "1차시_JSON_제출목록.html"),
        os.path.join(os.getcwd(), "1차시_JSON_제출목록.html"),
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    return None


def _render_submission_content():
    st.markdown("""
<div style="background:#EEF6FB;border:1px solid #C5DFEE;border-radius:8px;padding:12px 14px;margin-bottom:12px;font-size:13.5px;color:#1B3555;line-height:1.6;">
  <b>💡 1차시 제출 파일 활용 안내:</b><br>
  • <b>원클릭 즉시 불러오기:</b> 아래 선택창에서 본인 모둠을 고르고 <b>[⚡ 이 파일로 즉시 불러오기]</b>를 누르면 다운로드/업로드 과정 없이 <b>보고서에 바로 반영</b>됩니다.<br>
  • <b>직접 다운로드:</b> 아래 목록 표에서 <b>[JSON ⬇]</b> 버튼을 누르면 PC로 즉시 안전하게 저장됩니다. (Google Cloud 권한 오류 해결 완료)<br>
  • <b>원문 확인:</b> 모둠의 패들렛 원문(제출 사진·메모 등)을 보려면 <b>[게시물]</b> 링크를 누르세요.
</div>
""", unsafe_allow_html=True)

    sub_dir = os.path.join(HERE, "..", "static", "submissions_1")
    if os.path.isdir(sub_dir):
        files = sorted(os.listdir(sub_dir))
        file_map = {}
        for f in files:
            if f.endswith(".json") and "_" in f:
                wid, rest = f.split("_", 1)
                team_name = rest.replace(".json", "")
                label = f"[{team_name}] (제출 ID: {wid})"
                file_map[label] = os.path.join(sub_dir, f)

        if file_map:
            with st.container(border=True):
                st.markdown("<b>🚀 내 모둠 선택해서 보고서로 즉시 불러오기</b>", unsafe_allow_html=True)
                sc1, sc2 = st.columns([3, 1.3])
                with sc1:
                    sel_opt = st.selectbox("불러올 모둠 제출본 선택", list(file_map.keys()), label_visibility="collapsed")
                with sc2:
                    if st.button("⚡ 이 파일로 즉시 불러오기", key="eval_direct_sub_load_btn", type="primary", **FULL):
                        try:
                            with open(file_map[sel_opt], "r", encoding="utf-8") as jf:
                                st.session_state["_pending_load"] = json.load(jf)
                            st.rerun()
                        except Exception as e:
                            st.error(f"불러오기 실패: {e}")

    html_code = load_submission_html()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.link_button("🌐 원본 패들렛 열기 ↗", "https://padlet.com/sgh/padlet-s024ptsns1f0aj91uyqt", **FULL)
    with c2:
        st.link_button("📄 새 창(페이지)에서 전체보기 ↗", "/submission_list_1", **FULL)
    with c3:
        if html_code:
            st.download_button("💾 목록 HTML 다운로드", data=html_code, file_name="1차시_JSON_제출목록.html", mime="text/html", **FULL)
        else:
            st.link_button("🐙 GitHub에서 보기 ↗", "https://htmlpreview.github.io/?https://github.com/yuno0154/physics-course/blob/main/1%EC%B0%A8%EC%8B%9C_JSON_%EC%A0%9C%EC%B6%9C%EB%AA%A9%EB%A1%9D.html", **FULL)

    if html_code:
        import streamlit.components.v1 as components
        components.html(html_code, height=580, scrolling=True)
    else:
        st.warning("1차시 제출 목록 파일(1차시_JSON_제출목록.html)을 찾을 수 없습니다.")


if hasattr(st, "dialog"):
    @st.dialog("📋 1차시 JSON 제출 목록 (A반·B반 모둠)", width="large")
    def show_submission_modal():
        _render_submission_content()
else:
    def show_submission_modal():
        _render_submission_content()



# ════════════════════════════════════════════════════════════════════
# 3. 데이터 처리
# ════════════════════════════════════════════════════════════════════
# 교사용 실제 영상 분석 측정 데이터 (야구공 포물선 운동 29개 프레임 실측 데이터)
TEACHER_CSV = """Time (s),X (m),Y (m),X Velocity (m/s),Y Velocity (m/s)
0.000,-0.011,0.019,16.182,3.519
0.033,0.529,0.136,16.299,3.519
0.067,1.076,0.254,16.182,3.519
0.100,1.608,0.371,15.830,3.519
0.133,2.132,0.488,16.065,2.932
0.167,2.680,0.567,16.065,2.346
0.200,3.204,0.645,15.478,2.229
0.233,3.712,0.715,15.830,1.759
0.267,4.259,0.762,16.182,1.408
0.300,4.791,0.809,15.947,1.173
0.334,5.323,0.840,16.065,1.056
0.367,5.863,0.879,15.830,0.469
0.400,6.379,0.872,15.596,0.000
0.434,6.903,0.879,15.830,-0.117
0.467,7.435,0.864,16.065,-0.587
0.500,7.974,0.840,15.947,-0.821
0.534,8.498,0.809,16.234,-1.395
0.567,9.057,0.747,16.091,-1.342
0.600,9.571,0.720,15.426,-1.668
0.634,10.086,0.636,16.260,-2.502
0.667,10.656,0.553,16.052,-2.502
0.700,11.156,0.469,16.260,-3.128
0.734,11.740,0.344,16.468,-3.336
0.767,12.255,0.247,16.468,-3.336
0.800,12.839,0.122,17.094,-4.170
0.834,13.395,-0.032,16.468,-4.587
0.867,13.937,-0.185,16.052,-4.587
0.900,14.465,-0.337,16.052,-5.004
0.934,15.007,-0.518,16.260,-5.422"""

BACKUP_CSV = TEACHER_CSV



def parse_table(text):
    """붙여넣은 표(탭·쉼표·세미콜론·공백 구분)를 DataFrame으로 변환.
    제목 행 위에 'Data Set 1' 같은 안내 줄이 있어도 건너뛴다."""
    lines = [l for l in str(text).replace("\r", "").split("\n") if l.strip()]
    if len(lines) < 2:
        return None
    head = "\n".join(lines[:8])
    sep = "\t" if "\t" in head else (";" if ";" in head else ("," if "," in head else r"\s+"))

    def fields(line):
        return [f.strip().strip('"') for f in re.split(sep, line.strip())]

    def isnum(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def numeric_line(line):
        f = [x for x in fields(line) if x != ""]
        return len(f) >= 2 and sum(isnum(x) for x in f) >= max(2, int(len(f) * 0.6))

    first_num = next((i for i, l in enumerate(lines) if numeric_line(l)), None)
    if first_num is None:
        return None
    header = None
    if first_num > 0 and len(fields(lines[first_num - 1])) >= 2:
        header = fields(lines[first_num - 1])
    body = [fields(l) for l in lines[first_num:] if numeric_line(l)]
    width = max(len(r) for r in body)
    body = [r + [""] * (width - len(r)) for r in body]
    if header is None or len(header) < width:
        header = (header or []) + [f"열{i + 1}" for i in range(len(header or []), width)]
    header = header[:width]
    seen = {}
    for i, h in enumerate(header):  # 중복 열 이름 방지
        h = h or f"열{i + 1}"
        seen[h] = seen.get(h, 0) + 1
        header[i] = h if seen[h] == 1 else f"{h}_{seen[h]}"
    df = pd.DataFrame(body, columns=header).apply(lambda c: pd.to_numeric(c, errors="coerce"))
    df = df.dropna(axis=1, how="all").dropna(axis=0, how="all")
    return df if len(df) >= 2 and df.shape[1] >= 2 else None


def sel_kw(key, index):
    """세션에 값이 이미 있으면 index를 넘기지 않음(Streamlit 경고 방지)."""
    return {} if key in st.session_state else {"index": index}


def guess_columns(cols):
    g = {"t": None, "x": None, "y": None, "vx": None, "vy": None}
    for c in cols:
        n = re.sub(r"^.*:", "", c.lower())
        n = re.sub(r"[\s_]", "", n)
        is_v = any(s in n for s in ["vel", "속도", "m/s"]) or re.match(r"^v[xy]", n)
        if g["t"] is None and (any(s in n for s in ["time", "시간"]) or re.match(r"^t(\(|$)", n)):
            g["t"] = c
        elif is_v and "x" in n and g["vx"] is None:
            g["vx"] = c
        elif is_v and "y" in n and g["vy"] is None:
            g["vy"] = c
        elif not is_v and re.match(r"^(x|x위치|xposition)", n) and g["x"] is None:
            g["x"] = c
        elif not is_v and re.match(r"^(y|y위치|yposition)", n) and g["y"] is None:
            g["y"] = c
    return g


def build_data(raw, mapping):
    """표준 열(t,x,y,vx,vy,ay,v,Ek,Ep,E)을 가진 데이터 생성."""
    t = raw[mapping["t"]].to_numpy(float)
    x = raw[mapping["x"]].to_numpy(float)
    y = raw[mapping["y"]].to_numpy(float)
    d = pd.DataFrame({"t": t, "x": x, "y": y})
    d["vx"] = raw[mapping["vx"]].to_numpy(float) if mapping.get("vx") else np.nan
    d["vy"] = raw[mapping["vy"]].to_numpy(float) if mapping.get("vy") else np.nan
    d = d.dropna(subset=["t", "x", "y"]).sort_values("t").reset_index(drop=True)
    if len(d) < 3:
        return None
    if d["vx"].isna().all():
        d["vx"] = np.gradient(d["x"], d["t"])
    if d["vy"].isna().all():
        d["vy"] = np.gradient(d["y"], d["t"])
    d["vx"] = d["vx"].interpolate(limit_direction="both")
    d["vy"] = d["vy"].interpolate(limit_direction="both")
    d["ay"] = np.gradient(d["vy"], d["t"])
    d["v"] = np.hypot(d["vx"], d["vy"])
    d["Ek"] = 0.5 * MASS * d["v"] ** 2
    d["Ep"] = MASS * G * d["y"]
    d["E"] = d["Ek"] + d["Ep"]
    return d


def make_xlsx(d):
    """엑셀 파일: 측정값 + 에너지 계산 수식(셀 수식 그대로) + 조건."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "분석 데이터"
    heads = ["t (s)", "x (m)", "y (m)", "vx (m/s)", "vy (m/s)", "v (m/s)", "Ek (J)", "Ep (J)", "E (J)"]
    ws.append(heads)
    for i, r in d.iterrows():
        n = i + 2
        ws.append([round(r.t, 4), round(r.x, 4), round(r.y, 4), round(r.vx, 4), round(r.vy, 4),
                   f"=SQRT(D{n}^2+E{n}^2)", f"=0.5*$L$2*F{n}^2", f"=$L$2*$L$3*C{n}", f"=G{n}+H{n}"])
    ws["K1"], ws["L1"] = "계산 조건", ""
    ws["K2"], ws["L2"] = "m (kg)", MASS
    ws["K3"], ws["L3"] = "g (m/s²)", G
    hdr = PatternFill("solid", fgColor="1F3B5C")
    for c in ws[1][:9]:
        c.font, c.fill, c.alignment = Font(bold=True, color="FFFFFF"), hdr, Alignment(horizontal="center")
    ws["K1"].font = Font(bold=True)
    for col, w in zip("ABCDEFGHIJKL", [9, 9, 9, 10, 10, 10, 10, 10, 10, 3, 11, 8]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2, max_col=9):
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
    """0과 평균의 2배 사이를 보여 주는 넓은 축 (일정한 값의 작은 흔들림이 과장되지 않게).
    값이 그 범위를 넘으면 범위를 넓힘."""
    v = np.asarray(v, float)
    c = float(np.nanmean(v))
    half = max(abs(c), 1e-6)
    lo, hi = c - half, c + half
    pad = 0.08 * (hi - lo)
    return [min(lo, float(np.nanmin(v)) - pad), max(hi, float(np.nanmax(v)) + pad)]


def ay_range(v):
    """가속도-시간(ay-t) 그래프의 급간을 넓게 잡아 등가속도 운동(ay ≈ -9.8 m/s²)으로 거의 일정하게 보이도록 축 범위 대폭 확장."""
    v = np.asarray(v, float)
    min_v = float(np.nanmin(v)) if len(v) > 0 else -10.0
    max_v = float(np.nanmax(v)) if len(v) > 0 else -10.0
    lo = min(-60.0, float(np.floor((min_v - 10.0) / 20.0) * 20.0))
    hi = max(40.0, float(np.ceil((max_v + 10.0) / 20.0) * 20.0))
    return [lo, hi]


def energy_range(d):
    """에너지(Ek, Ep, E) 그래프의 급간을 크게 하여 작은 변동이 과장되지 않고 역학적 에너지 보존 경향이 잘 보이도록 축 범위 확장."""
    vals = []
    for col in ("Ek", "Ep", "E"):
        if hasattr(d, col):
            arr = np.asarray(getattr(d, col), float)
            arr = arr[~np.isnan(arr)]
            if len(arr) > 0:
                vals.append(arr)
        elif isinstance(d, dict) or hasattr(d, "__getitem__"):
            try:
                arr = np.asarray(d[col], float)
                arr = arr[~np.isnan(arr)]
                if len(arr) > 0:
                    vals.append(arr)
            except Exception:
                pass
    if not vals:
        return [0.0, 20.0]
    all_v = np.concatenate(vals)
    min_v = float(np.min(all_v))
    max_v = float(np.max(all_v))
    lo = min(0.0, float(np.floor(min_v / 5.0) * 5.0))
    hi = max(20.0, float(np.ceil((max_v + 1.0) / 5.0) * 5.0))
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


def plotly_energy(d):
    rng = energy_range(d)
    f = make_subplots(rows=1, cols=3, horizontal_spacing=0.09,
                      subplot_titles=("운동 에너지 Ek", "위치 에너지 Ep", "역학적 에너지 E = Ek + Ep"))
    for j, (col, color) in enumerate([("Ek", "#2E6DA4"), ("Ep", "#C0504D"), ("E", "#2D2D2D")], start=1):
        f.add_trace(go.Scatter(x=d.t, y=d[col], mode="lines+markers", line=dict(color=color)), 1, j)
        f.update_yaxes(range=rng, dtick=5, title_text="J" if j == 1 else None, row=1, col=j)
    f.update_xaxes(title_text="t (s)")
    f.update_yaxes(tickformat=".1f", zeroline=True, zerolinecolor="#9AA8B8")
    f.update_layout(height=320, showlegend=False, margin=dict(l=40, r=20, t=40, b=40), plot_bgcolor="#FAFBFC")
    return f


def mpl_png(d, kind):
    """보고서 파일용 그래프 이미지 (matplotlib) — 화면 그래프와 같은 축 범위 사용."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    ko = os.path.exists(FONT_REG)
    if ko:
        font_manager.fontManager.addfont(FONT_REG)
        plt.rcParams["font.family"] = font_manager.FontProperties(fname=FONT_REG).get_name()
    plt.rcParams["axes.unicode_minus"] = False

    def style(a, yl, title):
        a.set_title(title, fontsize=10)
        a.set_xlabel("t (s)", fontsize=8); a.set_ylabel(yl, fontsize=8)
        a.tick_params(labelsize=7); a.grid(alpha=.3)
        a.ticklabel_format(useOffset=False, axis="y")
        a.axhline(0, color="#9AA8B8", lw=0.8)

    if kind == "motion":
        fig, ax = plt.subplots(2, 3, figsize=(10, 5.6))
        spec = [(0, 0, "x", "x (m)", C_H, "x-t", None), (0, 1, "vx", "vx (m/s)", C_H, "vx-t", zero_range(d.vx)),
                (1, 0, "y", "y (m)", C_V, "y-t", None), (1, 1, "vy", "vy (m/s)", C_V, "vy-t", None),
                (1, 2, "ay", "ay (m/s²)", C_A, "ay-t", ay_range(d.ay))]
        for r, c, col, yl, color, ttl, rng in spec:
            a = ax[r][c]
            a.plot(d.t, d[col], "o-", color=color, ms=3, lw=1.2)
            style(a, yl, (("수평 " if r == 0 else "연직 ") + ttl) if ko else ttl)
            if rng:
                a.set_ylim(*rng)
                if col == "ay":
                    import matplotlib.ticker as ticker
                    a.yaxis.set_major_locator(ticker.MultipleLocator(20))
        ax[0][2].axis("off")
    else:
        rng = energy_range(d)
        fig, ax = plt.subplots(1, 3, figsize=(10, 3.2))
        import matplotlib.ticker as ticker
        for a, (col, color, ttl) in zip(ax, [("Ek", "#2E6DA4", "Ek"), ("Ep", "#C0504D", "Ep"),
                                             ("E", "#2D2D2D", "E = Ek + Ep")]):
            a.plot(d.t, d[col], "o-", ms=3, lw=1.2, color=color)
            style(a, "J", ttl)
            a.set_ylim(*rng)
            a.yaxis.set_major_locator(ticker.MultipleLocator(5))
    fig.tight_layout()
    bio = io.BytesIO()
    fig.savefig(bio, format="png", dpi=160)
    plt.close(fig)
    return bio.getvalue()


# ════════════════════════════════════════════════════════════════════
# 5. 콜백 (위젯 값 변경은 콜백에서만)
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


def cb_unlock():
    if st.session_state.get("unlock_code", "") == teacher_code():
        st.session_state["own_raw_backup"] = (st.session_state.get("raw_file_text", "")
                                              if st.session_state.get("input_mode") == "CSV 파일"
                                              else st.session_state.get("raw_data", ""))
        st.session_state["backup_used"] = True
        st.session_state["backup_time"] = now_kst()
        st.session_state["unlock_code"] = ""
        st.session_state["_unlock_msg"] = "ok"
        for k in ("map_t", "map_x", "map_y", "map_vx", "map_vy"):
            st.session_state.pop(k, None)
    else:
        st.session_state["_unlock_msg"] = "bad"


def cb_calc_img():
    f = st.session_state.get("calc_upload")
    if f is not None:
        st.session_state["calc_img_b64"] = base64.b64encode(f.getvalue()).decode()
        st.session_state["calc_img_name"] = f.name


def cb_clear_exports():
    st.session_state["exports"] = None


# ════════════════════════════════════════════════════════════════════
# 6. 화면 — 머리
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='hero'>
  <div class='k'>{COURSE} · 수행평가 (실험 및 보고서 · 2인 모둠 · 30점)</div>
  <h1>📹 {TITLE}</h1>
  <div class='m'>평가영역: {AREA}</div>
</div>""", unsafe_allow_html=True)

bar1, bar2, bar3, bar4 = st.columns([3.5, 1.0, 1.2, 1.4])
with bar1:
    st.markdown("<div class='legend'><span class='sw' style='background:#FFF8DC;border:1px solid #E8C766'></span>"
                "노란 칸 = 학생이 작성하는 곳 &nbsp;&nbsp; <span class='sw' style='background:#EEF4FA;border:1px solid #D5DEE8'>"
                "</span>파란 표·그래프 = 앱이 자동으로 만드는 곳</div>", unsafe_allow_html=True)
with bar2:
    save_payload = {k: st.session_state.get(k) for k in SAVE_KEYS}
    save_payload["_saved_at"] = now_kst()
    st.download_button("💾 저장", json.dumps(save_payload, ensure_ascii=False, default=str).encode("utf-8"),
                       file_name=f"{ss('cls')}_{ss('s1_name')}_{ss('s2_name')}_작성중.json".replace("__", "_"),
                       mime="application/json", **FULL,
                       help="지금까지 입력한 내용을 파일로 내려받습니다.")
with bar3:
    with st.popover("📂 불러오기", **FULL):
        up = st.file_uploader("저장한 JSON 파일", type=["json"], key="load_json")
        if up is not None and st.button("이 파일로 이어서 작성", **FULL):
            try:
                st.session_state["_pending_load"] = json.load(up)
                st.rerun()
            except Exception as e:
                st.error(f"파일을 읽을 수 없습니다: {e}")
        st.markdown("<hr style='margin:10px 0 8px 0;'>", unsafe_allow_html=True)
        st.caption("💡 1차시에 제출한 JSON 파일 링크가 필요하신가요?")
        if st.button("📋 1차시 제출 목록 확인", key="pop_sub_list_btn", **FULL):
            show_submission_modal()
with bar4:
    if st.button("📋 1차시 제출목록", key="main_sub_list_btn", **FULL, help="1차시에 제출된 모둠별 JSON 파일 다운로드 및 게시물 링크 목록을 확인합니다."):
        show_submission_modal()
if st.session_state.pop("_loaded_msg", False):
    st.success("저장한 내용을 불러왔습니다. 이어서 작성하세요.")

# ── 모둠 정보 ──────────────────────────────────────────────────────
with st.container(border=True):
    st.markdown("<div class='card-t'>👥 모둠 정보</div>", unsafe_allow_html=True)
    c0, c1, c2, c3 = st.columns([1, 1, 1.4, 2])
    c0.text_input("수강반", key="cls", placeholder="예: A")
    c1.text_input("반-번호 ①", key="s1_num", placeholder="예: 2-3")
    c2.text_input("이름 ①", key="s1_name")
    c3.selectbox("역할 ①", ROLES, key="s1_role")
    d0, d1, d2, d3 = st.columns([1, 1, 1.4, 2])
    d0.markdown("")
    d1.text_input("반-번호 ②", key="s2_num", placeholder="예: 2-15")
    d2.text_input("이름 ②", key="s2_name")
    d3.selectbox("역할 ②", ROLES, key="s2_role", **sel_kw("s2_role", 1))
    tip("반-번호는 <b>반-번호</b> 형식으로 씁니다 (2반 3번 → 2-3). "
        "중간에 창을 닫아야 할 때는 위의 <b>💾 저장</b>으로 파일을 받아 두고, <b>📂 불러오기</b>로 열면 이어서 작성할 수 있습니다. "
        "(인터넷 창을 닫거나 새로고침하면 입력한 내용이 사라집니다.)")

# ── 탐구 안내 (목표 · 과정 · 평가) ─────────────────────────────────
g1, g2 = st.columns([1, 1])
with g1:
    with st.container(border=True):
        st.markdown("<div class='card-t'>🎯 탐구 질문과 목표</div>", unsafe_allow_html=True)
        st.markdown("""
<div class='goal'>
<b>탐구 질문</b>
<ul>
<li><b>Q1.</b> 비스듬히 던진 공은 속력과 방향이 매 순간 변하는데, 왜 수평·연직 두 방향의 단순한 운동으로 나누어 설명할 수 있을까?</li>
<li><b>Q2.</b> 포물선 경로의 각 위치에서 운동 에너지와 위치 에너지는 어떻게 바뀌며, 그 합은 일정하게 유지될까?</li>
</ul>
<b>탐구 목표</b> — 이 탐구를 마치면 나는…
<ul>
<li>① 측정값을 수평·연직 성분별 표와 그래프로 나타내고, 두 성분의 운동이 서로 독립적임을 수치로 보일 수 있다.</li>
<li>② 연직 가속도를 직접 계산하여 중력 가속도와 비교할 수 있다.</li>
<li>③ 역학적 에너지 보존을 확인하고, 이론값과 실험값의 차이를 측정 오차와 모델의 가정으로 나누어 설명할 수 있다.</li>
</ul>
<span class='pill'>성취기준 [12역학01-02]</span>
</div>""", unsafe_allow_html=True)
with g2:
    with st.container(border=True):
        st.markdown("<div class='card-t'>🧪 탐구 과정</div>", unsafe_allow_html=True)
        st.markdown(f"""
<div class='steps'>
<ol>
<li><b>분석 영상 내려받기</b> — <a href='{PADLET_URL}' target='_blank'>패들렛에서 영상 받기 ↗</a>
    <br><img src='data:image/png;base64,{PADLET_QR_B64}' width='92' style='margin-top:4px;border:1px solid #D5DEE8;border-radius:6px'>
    <span style='font-size:12px;color:#6B7A8C'>&nbsp;휴대폰으로 받을 때는 QR</span></li>
<li><b>프로그램 접속</b> — <a href='{VA_URL}' target='_blank'>동영상 분석 프로그램 열기 ↗</a>
    <br><span class='pill'>제품키 {VA_KEY}</span><span class='pill'>사용 기한 {VA_EXPIRE}</span></li>
<li><b>설정</b> — 아래 값대로 설정합니다.
    <br><span class='pill'>프레임 범위 {CLIP}</span><span class='pill'>질점 {N_POINTS}개</span>
    <span class='pill'>교정 막대자·좌표축: 선생님 안내</span></li>
<li><b>데이터 붙여넣기</b> — 분석 표를 복사해 이 페이지 <b>1번</b>에 붙여 넣습니다. 표·그래프·엑셀 파일은 자동으로 만들어집니다.</li>
<li><b>분석·서술</b> — 2~6번 노란 칸을 작성합니다.</li>
<li><b>제출</b> — 맨 아래에서 보고서 PDF를 받아 <b>모둠 과제 제출방(패들렛)</b>에 올립니다. (모든 모둠 공통 제출방 사용 · 학급·모둠·모둠원을 정확히 입력)</li>
</ol>
<span class='pill'>계산 조건: m = {MASS} kg(가정), g = {G} m/s²</span>
</div>""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("<div class='card-t'>📋 평가 안내 — 지표면 역학 분석 [실험 및 보고서, 모둠별] 30점</div>",
                unsafe_allow_html=True)
    st.markdown("""
<table class='score'>
<tr><th style='width:22%'>만점(30점) 조건</th><td>
① 측정값을 수평·연직별 표와 그래프로 나타낸다 &nbsp;·&nbsp; ② 연직 가속도를 식과 계산 과정으로 직접 산출한다<br>
③ 결론에서 수평 등속·연직 등가속도 운동의 독립성을 측정 수치를 근거로 입증한다<br>
④ 대표 지점의 운동 에너지와 위치 에너지로 역학적 에너지 보존을 확인한다<br>
⑤ 오차 원인을 '측정 오차'와 '모델의 가정(공기 저항 무시)'으로 나누어 서술한다</td></tr>
<tr><th>점수가 낮아지는 경우</th><td>
• 가속도 산출 식이 빠지면 → 24점 &nbsp;&nbsp; • '운동의 독립성'에 오개념이 있으면(표·그래프가 완벽해도) → 18점<br>
• 데이터가 미완성이거나 빠진 채로 제출하면 → 18점</td></tr>
<tr><th>제공 데이터 사용</th><td>
• 교사 점검 결과 분석을 진행할 수 없을 때 선생님이 제공 데이터를 열어 줍니다. 이 경우 <b>최고 24점</b>입니다.<br>
• 단, 기기·네트워크·프로그램 오류처럼 학생 책임이 아닌 경우는 30점까지 인정합니다.<br>
• 실패한 원래 데이터는 자동으로 함께 보관되며, 5-나 '측정 오차'의 근거로 쓸 수 있습니다.</td></tr>
</table>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# 7. [1] 데이터
# ════════════════════════════════════════════════════════════════════
sec(1, "데이터 정리")

d = None
if st.session_state.get("backup_used"):
    st.markdown(f"<div class='src-bk'>📦 <b>제공 데이터 사용 중</b> · 열린 시각 {ss('backup_time')} · "
                f"사유: {ss('backup_reason', '-')} — 처음에 측정한 데이터는 함께 보관됩니다.</div>",
                unsafe_allow_html=True)
    raw_text = BACKUP_CSV
else:
    mode = st.radio("입력 방식", ["붙여넣기", "CSV 파일"], key="input_mode", horizontal=True)
    if mode == "붙여넣기":
        st.text_area("분석 프로그램의 데이터 표를 붙여 넣으세요", key="raw_data", height=170,
                     on_change=cb_paste, placeholder="여기에 붙여넣기 (Ctrl+V)")
        tip("분석 프로그램의 데이터 표를 클릭 → <b>Ctrl+A</b>(전체 선택) → <b>Ctrl+C</b>(복사) → 위 칸에 <b>Ctrl+V</b>. "
            "제목 행(Time, X …)이 함께 붙어도 됩니다. 붙여 넣은 뒤 칸 바깥을 클릭하면 표로 바뀝니다.")
        raw_text = ss("raw_data")
    else:
        st.file_uploader("내보낸 CSV 파일", type=["csv", "txt"], key="data_upload", on_change=cb_file)
        if ss("raw_file_name"):
            st.caption(f"불러온 파일: {ss('raw_file_name')}")
        tip("분석 프로그램에서 데이터를 CSV로 내보낸 뒤 올리세요. 한 번 올린 파일은 💾 저장에도 함께 들어갑니다.")
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

if d is not None:
    n = len(d)
    if n != N_POINTS and not st.session_state.get("backup_used"):
        st.warning(f"인식된 데이터는 {n}개입니다. (안내된 질점 수: {N_POINTS}개)")
    else:
        st.success(f"데이터 {n}개를 인식했습니다.")
    st.markdown("<span class='auto-label'>▣ 자동 생성 — 성분별 측정값 표</span>", unsafe_allow_html=True)
    tc1, tc2 = st.columns(2)
    fmt = {"t (s)": "{:.3f}", "x (m)": "{:.3f}", "vx (m/s)": "{:.3f}", "y (m)": "{:.3f}", "vy (m/s)": "{:.3f}"}
    with tc1:
        st.markdown("**수평 방향**")
        st.dataframe(d[["t", "x", "vx"]].rename(columns={"t": "t (s)", "x": "x (m)", "vx": "vx (m/s)"})
                     .style.format(fmt), hide_index=True, **FULL, height=260)
    with tc2:
        st.markdown("**연직 방향**")
        st.dataframe(d[["t", "y", "vy"]].rename(columns={"t": "t (s)", "y": "y (m)", "vy": "vy (m/s)"})
                     .style.format(fmt), hide_index=True, **FULL, height=260)
    st.download_button("📊 엑셀 파일 받기 (에너지 계산 수식 포함)", make_xlsx(d),
                       file_name=f"{ss('cls')}_{ss('s1_name')}_분석데이터.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("데이터를 붙여 넣으면 성분별 표와 그래프가 자동으로 만들어집니다.")

if not st.session_state.get("backup_used"):
    with st.expander("⚠️ 데이터 분석이 어려운가요? (선생님 확인 후 사용)"):
        tip("이 칸은 선생님이 모둠의 화면을 확인한 뒤 직접 입력합니다. 제공 데이터를 쓰면 지금 입력한 데이터는 "
            "'처음 측정 데이터'로 함께 보관됩니다.")
        u1, u2, u3 = st.columns([2, 1.5, 1])
        u1.selectbox("사유", BACKUP_REASONS, key="backup_reason")
        u2.text_input("교사 코드", type="password", key="unlock_code")
        u3.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        u3.button("제공 데이터 열기", on_click=cb_unlock, **FULL)
        msg = st.session_state.pop("_unlock_msg", None)
        if msg == "bad":
            st.error("코드가 맞지 않습니다.")
if st.session_state.pop("_unlock_msg", None) == "ok":
    st.success("제공 데이터가 열렸습니다.")

# ════════════════════════════════════════════════════════════════════
# 8. [2] 그래프
# ════════════════════════════════════════════════════════════════════
sec(2, "그래프", "자동 생성")
if d is not None:
    f1, f2 = plotly_graphs(d)
    st.markdown("**[수평 방향 운동]**")
    st.plotly_chart(f1, **FULL, config={"displaylogo": False})
    st.markdown("**[연직 방향 운동]**")
    st.plotly_chart(f2, **FULL, config={"displaylogo": False})
    st.markdown("<span class='auto-label'>▣ 그래프 눈금: vx-t와 ay-t 그래프는 측정값의 작은 흔들림이 과장되지 않도록 "
                "0이 보이는 넓은 눈금으로 그렸습니다.</span>", unsafe_allow_html=True)
    tip("그래프 위에 마우스를 올리면 각 점의 값이 보입니다. 그래프 영역을 드래그하면 확대되고, 더블클릭하면 원래대로 돌아옵니다.")
else:
    st.info("1번에 데이터를 넣으면 그래프 5개(x-t, vx-t, y-t, vy-t, ay-t)가 여기에 나타납니다.")

# ════════════════════════════════════════════════════════════════════
# 9. [3] 분석 및 해석
# ════════════════════════════════════════════════════════════════════
sec(3, "분석 및 해석")
qtext(Q["q3a"])
st.text_area("3-가", key="q3a", height=110, label_visibility="collapsed")
qtext(Q["q3b"])
st.text_area("3-나", key="q3b", height=110, label_visibility="collapsed")

qtext(Q["q3c"])
with st.container(border=True):
    if True:
        if d is not None:
            idx = list(range(len(d)))
            lab = lambda i: f"{i + 1}번째 점 · t = {d.t[i]:.3f} s"
            for kk in ("ay_i1", "ay_i2"):
                if st.session_state.get(kk) is not None and st.session_state[kk] not in idx:
                    st.session_state.pop(kk)
            a1, a2 = st.columns(2)
            i1 = a1.selectbox("시각 ①", idx, format_func=lab, key="ay_i1")
            i2 = a2.selectbox("시각 ②", idx, format_func=lab, key="ay_i2", **sel_kw("ay_i2", min(len(d) - 1, 5)))
            if i1 is not None and i1 < len(d) and i2 is not None and i2 < len(d):
                a1.markdown(f"<span class='auto-label'>▣ t1 = {d.t[i1]:.3f} s, vy1 = {d.vy[i1]:.3f} m/s</span>",
                            unsafe_allow_html=True)
                a2.markdown(f"<span class='auto-label'>▣ t2 = {d.t[i2]:.3f} s, vy2 = {d.vy[i2]:.3f} m/s</span>",
                            unsafe_allow_html=True)
            tip("시각을 고르면 그 시각의 측정값이 선택 칸 바로 아래에 표시됩니다. 이 값을 사용해 직접 계산하세요.")
        else:
            st.caption("1번 데이터를 먼저 넣으세요.")
    st.text_input("① 식", key="ay_formula")
    st.text_input("② 값 대입", key="ay_subst")
    r1, r2 = st.columns([1, 2])
    r1.text_input("③ 결과 ay (단위 포함)", key="ay_result")
    r2.text_input("④ 중력 가속도와 비교 (차이 = |ay| - g)", key="ay_err")
    tip("키보드 입력 방법: 제곱은 <b>^</b> (예: v^2), 곱하기는 <b>*</b>, 나누기는 <b>/</b>, 아래첨자는 그냥 이어서 (예: vy2, t1).")
    st.file_uploader("(선택) 손으로 쓴 계산 과정 사진", type=["png", "jpg", "jpeg"], key="calc_upload",
                     on_change=cb_calc_img)
    if st.session_state.get("calc_img_b64"):
        st.image(base64.b64decode(st.session_state["calc_img_b64"]), width=380, caption="올린 계산 과정 사진")
    tip("종이에 푼 경우 사진을 올려도 됩니다. 이때도 ③ 결과 칸은 꼭 입력하세요. 글씨가 잘 보이도록 밝은 곳에서 찍으세요.")

# ════════════════════════════════════════════════════════════════════
# 10. [4] 역학적 에너지
# ════════════════════════════════════════════════════════════════════
sec(4, "역학적 에너지 보존 확인", f"m = {MASS} kg(가정), g = {G} m/s²")
st.markdown(f"<span class='auto-label'>▣ Ek = ½mv², Ep = mgy, E = Ek + Ep 는 앱이 계산합니다. "
            f"지점 선택과 판단은 학생이 합니다.</span>", unsafe_allow_html=True)
if d is not None:
    idx = list(range(len(d)))
    lab = lambda i: f"{i + 1}번째 점 · t = {d.t[i]:.3f} s"
    e1, e2 = st.columns(2)
    for kk in ("e_top", "e_after"):
        if st.session_state.get(kk) is not None and st.session_state[kk] not in idx:
            st.session_state.pop(kk)
    top = e1.selectbox("내가 판단한 최고점", [None] + idx, key="e_top",
                       format_func=lambda i: "— 선택 —" if i is None else lab(i))
    aft = e2.selectbox("최고점 이후 임의 지점", [None] + idx, key="e_after",
                       format_func=lambda i: "— 선택 —" if i is None else lab(i))
    rows = [("처음 위치", 0), ("최고점", top), ("최고점 이후 임의 지점", aft)]
    et = pd.DataFrame([{"지점": nm, "t (s)": fnum(d.t[i]) if i is not None and i < len(d) else "",
                        "y (m)": fnum(d.y[i]) if i is not None and i < len(d) else "",
                        "v (m/s)": fnum(d.v[i]) if i is not None and i < len(d) else "",
                        "Ek (J)": fnum(d.Ek[i]) if i is not None and i < len(d) else "",
                        "Ep (J)": fnum(d.Ep[i]) if i is not None and i < len(d) else "",
                        "E (J)": fnum(d.E[i]) if i is not None and i < len(d) else ""} for nm, i in rows])
    st.dataframe(et, hide_index=True, **FULL)
    st.plotly_chart(plotly_energy(d), **FULL, config={"displaylogo": False})
    st.markdown("<span class='auto-label'>▣ 그래프 눈금: 역학적 에너지 보존 경향과 상호 변환을 한눈에 비교할 수 있도록 "
                "세 에너지(Ek, Ep, E)의 y축 급간을 0부터 동일한 큰 눈금(5 J 단위)으로 맞추었습니다.</span>", unsafe_allow_html=True)
    tip("지점을 고르면 표가 자동으로 채워집니다. 그래프 위에 마우스를 올리면 각 점의 값이 보입니다. "
        "※ 영상 분석 데이터는 <b>공기 저항이 있는 실제 환경</b>의 측정값이므로, "
        "표의 구체적인 수치를 제시(데이터 기반)하고 물리 이론을 바탕으로 보존 여부를 해석하세요.")
else:
    st.info("1번 데이터를 넣으면 에너지 표와 그래프가 나타납니다.")
qtext(Q["q4"])
st.text_area("4", key="q4", height=120, label_visibility="collapsed",
             placeholder="예: 공기가 있는 실제 상황에서의 측정이므로 표의 세 지점 E 값(처음: … J, 최고점: … J, 이후: … J)을 비교하면 … 이론상 역학적 에너지 보존 및 에너지 상호 전환(Ek ↔ Ep) 관점에서 볼 때 …")

# ════════════════════════════════════════════════════════════════════
# 11. [5] 이론값과 실험값 비교
# ════════════════════════════════════════════════════════════════════
sec(5, "이론값과 실험값 비교")
qtext(Q["q5a"])
st.markdown("**① 처음 속력과 발사각 구하기**")
v1, v2, v3, v4 = st.columns(4)
v1.text_input("v0x (m/s) = 첫 점의 vx", key="v0x")
v2.text_input("v0y (m/s) = 첫 점의 vy", key="v0y")
v3.text_input("처음 속력 v0 (m/s)", key="v0")
v4.text_input("발사각 θ (°)", key="theta", placeholder="약 19°")
tip("※ <b>영상 분석 야구공의 발사각은 근사적으로 약 19°(약 18°~20°)</b> 입니다.")

st.markdown("**② 시뮬레이션으로 이론값 구하기**")
st.markdown(f"""<a href="{SIM_URL}" target="_blank" style="text-decoration:none;">
<div style="background:#1F3B5C;color:#fff;border-radius:8px;padding:10px;text-align:center;font-weight:600;">
🚀 [포물선 운동 시뮬레이션] 새 창에서 열기</div></a>""", unsafe_allow_html=True)
tip("시뮬레이션은 새 창(새 탭)으로 열리므로 이 페이지의 입력 내용은 그대로 남아 있습니다. "
    "시뮬레이션에 ①에서 구한 발사각(약 19°)과 처음 속력을 넣고, 중력 가속도는 <b>9.8</b>을 선택한 뒤 "
    "최고점 도달 시간·최고점 높이·수평 도달 거리를 아래 '이론값' 칸에 옮겨 적으세요.")

st.markdown("**③ 실험값과 비교하기**")
hc = st.columns([1.2, 1, 1, 1])
hc[0].markdown("**구분**")
for j, it in enumerate(COMP_ITEMS):
    hc[j + 1].markdown(f"**{it}**")
for rlab, pre in [("실험값 (영상 측정)", "exp"), ("이론값 (시뮬레이션)", "th"), ("차이 (실험값 - 이론값)", "er")]:
    rc = st.columns([1.2, 1, 1, 1])
    rc[0].markdown(f"<div style='padding-top:8px'>{rlab}</div>", unsafe_allow_html=True)
    for j in range(3):
        rc[j + 1].text_input(f"{rlab} {COMP_ITEMS[j]}", key=f"{pre}_{j}", label_visibility="collapsed")
tip("숫자 칸에는 숫자만 쓰고 단위는 쓰지 않아도 됩니다(단위는 표 머리에 있습니다).")

qtext(Q["q5b"])
o1, o2 = st.columns(2)
o1.text_area("측정 오차 (측정 과정에서 생긴 오차)", key="err_measure", height=150)
o2.text_area("모델의 가정 (이론이 무시한 요인)", key="err_model", height=150)

# ════════════════════════════════════════════════════════════════════
# 12. [6] 결론
# ════════════════════════════════════════════════════════════════════
sec(6, "결론")
qtext(Q["q6a"])
st.text_area("6-Q1", key="q6a", height=130, label_visibility="collapsed")
qtext(Q["q6b"])
st.text_area("6-Q2", key="q6b", height=130, label_visibility="collapsed")


# ════════════════════════════════════════════════════════════════════
# 13. 제출 전 점검 · 보고서 파일
# ════════════════════════════════════════════════════════════════════
def filled(*keys, min_len=1):
    return all(len(str(ss(k)).strip()) >= min_len for k in keys)


checks = [
    ("모둠 정보", filled("cls", "s1_num", "s1_name")),
    ("1. 데이터", d is not None),
    ("3-가·나 서술", filled("q3a", "q3b", min_len=10)),
    ("3-다 가속도 계산 (식·대입·결과)", filled("ay_result") and (filled("ay_formula", "ay_subst") or bool(ss("calc_img_b64")))),
    ("4. 지점 선택·판단", ss("e_top", None) is not None and ss("e_after", None) is not None and filled("q4", min_len=10)),
    ("5-가 v0·발사각·비교표", filled("v0x", "v0y", "v0", "theta", *[f"exp_{i}" for i in range(3)],
                            *[f"th_{i}" for i in range(3)], *[f"er_{i}" for i in range(3)])),
    ("5-나 오차 원인 2분류", filled("err_measure", "err_model", min_len=5)),
    ("6. 결론 Q1·Q2", filled("q6a", "q6b", min_len=10)),
]

sec("✓", "제출 전 점검 · 보고서 만들기")
done = sum(ok for _, ok in checks)
st.progress(done / len(checks), text=f"작성 완료 {done} / {len(checks)}")
ck = st.columns(4)
for i, (name, ok) in enumerate(checks):
    ck[i % 4].markdown(("✅ " if ok else "⬜ ") + name)
tip("⬜ 표시가 남아 있어도 보고서 파일은 만들 수 있지만, 빈 칸은 보고서에 '(미작성)'으로 표시됩니다.")


def report_dict():
    sel = lambda k: (None if ss(k, None) is None or d is None or ss(k, None) >= len(d) else int(ss(k)))
    return dict(
        cls=ss("cls"), members=[(ss("s1_num"), ss("s1_name"), ss("s1_role")), (ss("s2_num"), ss("s2_name"), ss("s2_role"))],
        source=("제공 데이터 (" + ss("backup_reason", "-") + ", " + ss("backup_time") + ")")
        if st.session_state.get("backup_used") else "자체 측정 데이터",
        made=now_kst(), d=d, top=sel("e_top"), after=sel("e_after"),
        ay_pts=(sel("ay_i1"), sel("ay_i2")),
        own_backup=ss("own_raw_backup") if st.session_state.get("backup_used") else "",
    )


# ── DOCX ───────────────────────────────────────────────────────────
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
        shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), hexcolor)
        tcPr.append(shd)

    def borders(cell, color, sz="8"):
        tcPr = cell._tc.get_or_add_tcPr()
        b = OxmlElement("w:tcBorders")
        for side in ("top", "left", "bottom", "right"):
            e = OxmlElement(f"w:{side}")
            e.set(qn("w:val"), "single"); e.set(qn("w:sz"), sz); e.set(qn("w:color"), color)
            b.append(e)
        tcPr.append(b)

    def run(p, text, bold=False, size=None, color=None):
        r = p.add_run(text)
        r.bold = bold
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = RGBColor.from_string(color)
        return r

    def heading(num, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.keep_with_next = True
        run(p, f"{num}. {text}", bold=True, size=12.5, color="1F3B5C")
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
        bt.set(qn("w:val"), "single"); bt.set(qn("w:sz"), "10"); bt.set(qn("w:color"), "1F3B5C")
        bdr.append(bt); pPr.append(bdr)

    def question(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.keep_with_next = True
        run(p, text, bold=True, size=10)

    def student_box(text, label="학생 작성", min_lines=0):
        t = doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.cell(0, 0)
        shade(c, "FFF8DC"); borders(c, "E0B84A", "10")
        p = c.paragraphs[0]
        run(p, f"[{label}]", size=7.5, color="9A7A1E")
        body = str(text).strip()
        p2 = c.add_paragraph()
        if body:
            run(p2, body, size=10)
        else:
            run(p2, "(미작성)", size=10, color="C0392B")
        for _ in range(min_lines):
            c.add_paragraph()
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
            c = t.cell(0, j); c.text = ""
            run(c.paragraphs[0], h, bold=True, size=font, color="1F3B5C")
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            shade(c, "E3ECF6")
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                c = t.cell(i + 1, j); c.text = ""
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
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, COURSE + " · 수행평가 보고서", size=9, color="5B6B7D")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, TITLE, bold=True, size=15, color="1F3B5C")
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run(p, "평가영역: " + AREA + "  |  실험 및 보고서 · 모둠별 · 30점", size=8.5, color="5B6B7D")

    m = R["members"]
    grid(["수강반", "반-번호·이름 ①", "역할 ①", "반-번호·이름 ②", "역할 ②"],
         [[R["cls"], f"{m[0][0]} {m[0][1]}", m[0][2], f"{m[1][0]} {m[1][1]}", m[1][2]]],
         stu_cols=(0, 1, 2, 3, 4), font=9)
    p = doc.add_paragraph()
    run(p, f"데이터 출처: {R['source']}   ·   보고서 생성: {R['made']}", size=8.5, color="5B6B7D")
    p = doc.add_paragraph()
    run(p, "■ ", size=9, color="E0B84A"); run(p, "노란 칸 = 학생 작성     ", size=8.5)
    run(p, "■ ", size=9, color="2E6DA4"); run(p, "파란 머리 표·그래프 = 앱 자동 생성", size=8.5)

    D = R["d"]
    heading(1, "데이터 정리 (성분별 측정값)")
    if D is not None:
        auto_label()
        rows = [[i + 1, fnum(r.t), fnum(r.x), fnum(r.vx), fnum(r.y), fnum(r.vy)] for i, r in D.iterrows()]
        grid(["#", "t (s)", "x (m)", "vx (m/s)", "y (m)", "vy (m/s)"], rows, font=8,
             widths=[10, 26, 30, 30, 30, 30])
    else:
        student_box("", "데이터 없음")

    heading(2, "그래프")
    if D is not None:
        auto_label()
        doc.add_picture(io.BytesIO(mpl_png(D, "motion")), width=Mm(176))

    heading(3, "분석 및 해석")
    question(Q["q3a"]); student_box(ss("q3a"))
    question(Q["q3b"]); student_box(ss("q3b"))
    question(Q["q3c"])
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
        p = doc.add_paragraph(); run(p, "손으로 쓴 계산 과정 (학생 제출 사진)", size=8, color="9A7A1E")
        try:
            doc.add_picture(io.BytesIO(base64.b64decode(ss("calc_img_b64"))), width=Mm(110))
        except Exception:
            run(doc.add_paragraph(), "(사진을 넣을 수 없습니다)", size=8)

    heading(4, f"역학적 에너지 보존 확인 (m = {MASS} kg 가정, g = {G} m/s²)")
    if D is not None:
        auto_label("자동 생성 (앱 계산) — 지점 선택은 학생")
        erows = []
        for nm, i in [("처음 위치", 0), ("최고점 (학생 선택)", R["top"]), ("최고점 이후 임의 지점 (학생 선택)", R["after"])]:
            if i is None:
                erows.append([nm, "", "", "", "", "", ""])
            else:
                erows.append([nm, fnum(D.t[i]), fnum(D.y[i]), fnum(D.v[i]), fnum(D.Ek[i]), fnum(D.Ep[i]), fnum(D.E[i])])
        grid(["지점", "t (s)", "y (m)", "v (m/s)", "Ek (J)", "Ep (J)", "E (J)"], erows, font=8.5,
             widths=[46, 20, 22, 22, 22, 22, 24])
        doc.add_picture(io.BytesIO(mpl_png(D, "energy")), width=Mm(176))
    question(Q["q4"]); student_box(ss("q4"))

    heading(5, "이론값과 실험값 비교")
    question(Q["q5a"])
    p = doc.add_paragraph()
    run(p, "① 처음 속력과 발사각", bold=True, size=9.5)
    grid(["v0x (m/s)", "v0y (m/s)", "처음 속력 v0 (m/s)", "발사각 (°)"],
         [[ss("v0x"), ss("v0y"), ss("v0"), ss("theta")]], stu_cols=(0, 1, 2, 3), widths=[40, 40, 48, 48])
    p = doc.add_paragraph(); run(p, "② 이론값(포물선 운동 시뮬레이션)과 실험값 비교", bold=True, size=9.5)
    grid(["구분"] + COMP_ITEMS,
         [["실험값 (영상 측정)"] + [ss(f"exp_{j}") for j in range(3)],
          ["이론값 (시뮬레이션)"] + [ss(f"th_{j}") for j in range(3)],
          ["차이 (실험값 - 이론값)"] + [ss(f"er_{j}") for j in range(3)]],
         stu_cols=(1, 2, 3), widths=[40, 46, 46, 46], font=9.5)
    question(Q["q5b"])
    t = doc.add_table(rows=2, cols=2); t.style = "Table Grid"
    for j, (h, k) in enumerate([("측정 오차 (측정 과정에서 생긴 오차)", "err_measure"),
                                ("모델의 가정 (이론이 무시한 요인)", "err_model")]):
        hcell = t.cell(0, j); hcell.text = ""
        run(hcell.paragraphs[0], h, bold=True, size=9, color="1F3B5C"); shade(hcell, "E3ECF6")
        c = t.cell(1, j); c.text = ""; shade(c, "FFF8DC")
        run(c.paragraphs[0], "[학생 작성]", size=7.5, color="9A7A1E")
        body = str(ss(k)).strip()
        run(c.add_paragraph(), body or "(미작성)", size=10, color=None if body else "C0392B")

    heading(6, "결론")
    question(Q["q6a"]); student_box(ss("q6a"))
    question(Q["q6b"]); student_box(ss("q6b"))

    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10)
    run(p, "제출 전 점검: " + "   ".join(("■ " if ok else "□ ") + nm for nm, ok in checks), size=8, color="5B6B7D")
    if R["own_backup"]:
        p = doc.add_paragraph(); run(p, "[참고] 처음 측정 데이터 (제공 데이터 사용 전)", bold=True, size=8.5)
        run(doc.add_paragraph(), R["own_backup"][:4000], size=7, color="5B6B7D")
    bio = io.BytesIO(); doc.save(bio)
    return bio.getvalue()


# ── PDF ────────────────────────────────────────────────────────────
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
    _circ = str.maketrans({"①": "(1)", "②": "(2)", "③": "(3)", "④": "(4)", "⑤": "(5)", "θ": "theta"})
    esc = lambda s: xml_escape(str(s).translate(_circ)).replace("\n", "<br/>")
    W = 178 * mm
    el = []

    def heading(num, text):
        t = Table([[Paragraph(f"{num}. {esc(text)}", P(12, True, "#1F3B5C"))]], colWidths=[W])
        t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 1.2, NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        el.append(t)

    def question(text):
        el.append(Spacer(1, 4)); el.append(Paragraph(esc(text), P(9.5, True)))
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

    m = R["members"]
    el += [Paragraph(esc(COURSE + " · 수행평가 보고서"), P(8.5, False, "#5B6B7D", 1)),
           Paragraph(esc(TITLE), P(15, True, "#1F3B5C", 1, 21)),
           Paragraph(esc("평가영역: " + AREA + "  |  실험 및 보고서 · 모둠별 · 30점"), P(8, False, "#5B6B7D", 1)),
           Spacer(1, 6)]
    grid(["수강반", "반-번호·이름 ①", "역할 ①", "반-번호·이름 ②", "역할 ②"],
         [[R["cls"], f"{m[0][0]} {m[0][1]}", m[0][2], f"{m[1][0]} {m[1][1]}", m[1][2]]], stu_cols=(0, 1, 2, 3, 4),
         widths=[20, 38, 41, 38, 41])
    el.append(Spacer(1, 3))
    el.append(Paragraph(esc(f"데이터 출처: {R['source']}   ·   보고서 생성: {R['made']}"), P(8, False, "#5B6B7D")))
    el.append(Paragraph("<font color='#E0B84A'>■</font> 노란 칸 = 학생 작성 &nbsp;&nbsp; "
                        "<font color='#2E6DA4'>■</font> 파란 머리 표·그래프 = 앱 자동 생성", P(8)))

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
        el.append(Image(io.BytesIO(mpl_png(D, "motion")), width=W, height=W * 5.6 / 10))
        el[mark:] = [KeepTogether(el[mark:])]
    else:
        heading(2, "그래프")
    heading(3, "분석 및 해석")
    question(Q["q3a"]); student_box(ss("q3a"))
    question(Q["q3b"]); student_box(ss("q3b"))
    question(Q["q3c"])
    if R["ay_pts"] and D is not None and None not in R["ay_pts"]:
        i1, i2 = R["ay_pts"]
        auto_label(f"▣ 선택한 시각의 측정값: t1 = {D.t[i1]:.3f} s, vy1 = {D.vy[i1]:.3f} m/s  /  "
                   f"t2 = {D.t[i2]:.3f} s, vy2 = {D.vy[i2]:.3f} m/s")
    rows = [["① 식", ss("ay_formula")], ["② 값 대입", ss("ay_subst")], ["③ 결과 ay", ss("ay_result")],
             ["④ 중력 가속도와 비교", ss("ay_err")]]
    grid(["단계", "학생 작성"], rows, stu_cols=(1,), widths=[40, 138], size=9, left_cols=(1,))
    if ss("calc_img_b64"):
        try:
            from reportlab.lib.utils import ImageReader
            raw_img = base64.b64decode(ss("calc_img_b64"))
            iw, ih = ImageReader(io.BytesIO(raw_img)).getSize()
            w_ = 110 * mm
            el.append(Paragraph("손으로 쓴 계산 과정 (학생 제출 사진)", P(7.5, False, "#9A7A1E")))
            el.append(Image(io.BytesIO(raw_img), width=w_, height=min(w_ * ih / iw, 150 * mm)))
        except Exception:
            pass
    heading(4, f"역학적 에너지 보존 확인 (m = {MASS} kg 가정, g = {G} m/s²)")
    if D is not None:
        auto_label("▣ 자동 생성 (앱 계산) — 지점 선택은 학생")
        erows = []
        for nm, i in [("처음 위치", 0), ("최고점 (학생 선택)", R["top"]), ("최고점 이후 임의 지점 (학생 선택)", R["after"])]:
            erows.append([nm] + ([""] * 6 if i is None else
                                 [fnum(D.t[i]), fnum(D.y[i]), fnum(D.v[i]), fnum(D.Ek[i]), fnum(D.Ep[i]), fnum(D.E[i])]))
        grid(["지점", "t (s)", "y (m)", "v (m/s)", "Ek (J)", "Ep (J)", "E (J)"], erows,
             widths=[52, 20, 20, 22, 21, 21, 22], size=8)
        el.append(Spacer(1, 3))
        el.append(Image(io.BytesIO(mpl_png(D, "energy")), width=W, height=W * 3.2 / 10))
    question(Q["q4"]); student_box(ss("q4"))
    heading(5, "이론값과 실험값 비교")
    question(Q["q5a"])
    el.append(Paragraph("(1) 처음 속력과 발사각", P(9, True)))
    grid(["v0x (m/s)", "v0y (m/s)", "처음 속력 v0 (m/s)", "발사각 (°)"],
         [[ss("v0x"), ss("v0y"), ss("v0"), ss("theta")]], stu_cols=(0, 1, 2, 3), widths=[40, 40, 49, 49])
    el.append(Spacer(1, 4)); el.append(Paragraph("(2) 이론값(포물선 운동 시뮬레이션)과 실험값 비교", P(9, True)))
    grid(["구분"] + COMP_ITEMS, [["실험값 (영상 측정)"] + [ss(f"exp_{j}") for j in range(3)],
                               ["이론값 (시뮬레이션)"] + [ss(f"th_{j}") for j in range(3)],
                               ["차이 (실험값 - 이론값)"] + [ss(f"er_{j}") for j in range(3)]],
         stu_cols=(1, 2, 3), widths=[43, 45, 45, 45], size=9)
    question(Q["q5b"])
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
    heading(6, "결론")
    question(Q["q6a"]); student_box(ss("q6a"))
    question(Q["q6b"]); student_box(ss("q6b"))
    el.append(Spacer(1, 8))
    el.append(Paragraph(esc("제출 전 점검: " + "   ".join(("■ " if ok else "□ ") + nm for nm, ok in checks)),
                        P(7.5, False, "#5B6B7D")))
    if R["own_backup"]:
        el.append(Spacer(1, 6)); el.append(Paragraph("[참고] 처음 측정 데이터 (제공 데이터 사용 전)", P(8, True)))
        el.append(Paragraph(esc(R["own_backup"][:4000]), P(6.5, False, "#5B6B7D")))

    def footer(cv, doc_):
        cv.saveState(); cv.setFont("NG", 7.5); cv.setFillColor(colors.HexColor("#8A97A6"))
        cv.drawString(16 * mm, 9 * mm, f"{R['cls']}반  {m[0][0]} {m[0][1]} · {m[1][0]} {m[1][1]}  |  {TITLE}")
        cv.drawRightString(194 * mm, 9 * mm, f"{doc_.page}쪽")
        cv.restoreState()

    bio = io.BytesIO()
    SimpleDocTemplate(bio, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm, topMargin=14 * mm,
                      bottomMargin=16 * mm, title=TITLE, author=f"{m[0][1]} {m[1][1]}").build(
        el, onFirstPage=footer, onLaterPages=footer)
    return bio.getvalue()


with st.container(border=True):
    st.markdown("<div class='card-t'>📤 보고서 파일 만들기와 제출</div>", unsafe_allow_html=True)
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
                out["err"] = "fonts/NanumGothic.ttf 가 없어 PDF를 만들 수 없습니다. (선생님께 알려 주세요)"
            out["name"] = f"{ss('cls')}_{ss('s1_name')}_{ss('s2_name')}_영상분석보고서"
            st.session_state["exports"] = out
    b2.markdown("<div class='tip' style='margin-top:4px'>💡 내용을 고친 뒤에는 이 버튼을 <b>다시</b> 눌러야 "
                "고친 내용이 파일에 들어갑니다.</div>", unsafe_allow_html=True)
    ex = st.session_state.get("exports")
    if ex:
        x1, x2 = st.columns(2)
        if ex.get("pdf"):
            x1.download_button("⬇️ PDF 받기 (제출용)", ex["pdf"], file_name=ex["name"] + ".pdf",
                               mime="application/pdf", **FULL, type="primary")
        else:
            x1.warning(ex.get("err") or "PDF를 만들지 못했습니다.")
        x2.download_button("⬇️ Word 받기 (참고용)", ex["docx"], file_name=ex["name"] + ".docx",
                           mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           **FULL)
    st.markdown(f"""
**제출 방법 (모둠 과제 제출방 · 패들렛)**
1. 위 버튼으로 **PDF**를 받습니다. 파일 이름은 자동으로 `수강반_이름_이름_영상분석보고서.pdf`가 됩니다.
2. 아래 **[모둠 과제 제출방]** 링크를 열고 **보고서 PDF**와 **영상 분석 파일**(`.vmbl`)을 함께 올립니다.
   - **모든 모둠이 이 제출함**을 사용합니다. 학급·모둠·모둠원을 정확히 입력하세요.
   - **모둠 제목 형식**: `A반_1모둠_영상분석보고서_최종` (1모둠 내 2인 1조 각 조별 제출)
   - 파일이 2개라면 각각 제출하거나 ZIP 파일 하나로 묶어 제출하세요. 수정할 때는 제목에 ‘재제출’을 표시하세요.
   - 비공개 제출방이므로 제출물은 다른 학생에게 보이지 않습니다.
""")

    st.markdown(f"""<a href="{PADLET_SUBMIT_URL}" target="_blank" style="text-decoration:none;">
<div style="background:#1F3B5C;color:#fff;border-radius:10px;padding:14px;text-align:center;font-weight:700;font-size:16px;box-shadow:0 2px 6px rgba(0,0,0,0.15);margin:10px 0 16px;">
🚀 [모둠 과제 제출방 (패들렛)] 새 창에서 열기 ↗
<div style="font-size:12px;font-weight:normal;color:#B8C9E0;margin-top:5px;">모든 모둠 공통 제출함 · 학급·모둠·모둠원 입력 · 비공개 제출방</div>
</div></a>""", unsafe_allow_html=True)

    tip("제출 후에도 💾 저장 파일은 지우지 마세요. 이의 신청이나 수정 확인 때 필요할 수 있습니다.")

# ════════════════════════════════════════════════════════════════════
# 14. 교사용 (화면 맨 아래, 인쇄 제외)
# ════════════════════════════════════════════════════════════════════
with st.expander("🔒 교사용 확인"):
    if st.text_input("교사 코드", type="password", key="teacher_view") == teacher_code():
        st.markdown("#### 🎯 학생 입력 데이터 분석")
        if d is not None:
            slope = np.polyfit(d.t, d.vy, 1)[0]
            v0x, v0y = float(d.vx.iloc[0]), float(d.vy.iloc[0])
            tt = v0y / G
            v0_, th_ = float(np.hypot(v0x, v0y)), float(np.degrees(np.arctan2(v0y, v0x)))
            E0, E1 = float(d.E.iloc[0]), float(d.E.iloc[-1])
            st.markdown(f"""
- 데이터 출처: **{report_dict()['source']}** · 점 개수 {len(d)}
- vy-t 1차 추세선 기울기 ay ≈ **{slope:.2f} m/s²** (g 대비 {abs(abs(slope) - G) / G * 100:.1f}%)
- 첫 점 기준 v0x ≈ {v0x:.2f}, v0y ≈ {v0y:.2f} m/s → v0 ≈ {v0_:.2f} m/s, 발사각 ≈ {th_:.1f}° → 이론 t ≈ {tt:.3f} s, H ≈ {v0y ** 2 / (2 * G):.3f} m, R ≈ {v0x * 2 * tt:.3f} m
- 실측 최고점: t = {d.t[d.y.idxmax()]:.3f} s, y = {d.y.max():.3f} m
- 역학적 에너지 처음→마지막 변화율 ≈ {(E1 - E0) / E0 * 100 if E0 else float('nan'):.1f}%
""")
        else:
            st.caption("현재 화면에 학생 입력 데이터가 없습니다.")

        st.markdown("---")
        st.markdown("#### 📋 교사용 기준 실측 데이터셋 (정답 기준값)")
        st.markdown("""
- **영상 분석 교사용 실측값 (야구공 29개 프레임)**:
  - vy-t 기울기 ay ≈ **-10.12 m/s²** (g = 9.8 m/s² 대비 오차 3.2%)
  - 첫 점: $v_{0x} = 16.182\\text{ m/s}$, $v_{0y} = 3.519\\text{ m/s}$ → $v_0 = 16.560\\text{ m/s}$
  - 최고점: 실측 $t = 0.367\\text{ s}$, $y = 0.879\\text{ m}$ / 이론 $t = 0.359\\text{ s}$, $H = 0.632\\text{ m}$
  - 역학적 에너지 $E$: 평균 약 $13.8\\text{ J}$ (보존 경향)
""")
        raw_t = parse_table(TEACHER_CSV)
        if raw_t is not None:
            g_t = guess_columns(list(raw_t.columns))
            d_t = build_data(raw_t, g_t)
            if d_t is not None:
                st.download_button("📊 교사용 정답 엑셀 파일 받기", make_xlsx(d_t),
                                   file_name="교사용_포물선운동_기준데이터.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        st.markdown("---")
        st.markdown("#### 📋 학생 1차시 JSON 제출 현황")
        t_c1, t_c2 = st.columns([1, 1])
        with t_c1:
            if st.button("📋 1차시 JSON 제출 목록 모달 열기", key="teacher_sub_modal", **FULL):
                show_submission_modal()
        with t_c2:
            st.link_button("📄 1차시 제출 목록 새 창 열기 ↗", "/app/static/submission_list_1.html", **FULL)

st.caption("사곡고등학교 역학과 에너지 · 시뮬레이션 및 실습 지원 포털")
