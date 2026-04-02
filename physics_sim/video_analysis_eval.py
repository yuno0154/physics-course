import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
# st.set_page_config(page_title="수행평가 1-1: 포물선 운동 영상 분석 및 데이터 해석", layout="wide") # main_app에서 설정됨

# CSS를 활용한 인쇄 최적화 및 폰트 크기 설정
st.markdown("""
    <style>
    /* 기본 폰트 및 본문 크기 (12pt) */
    html, body, [class*="css"], [class*="st-"] {
        font-size: 12pt !important;
    }
    
    /* 제목 크기 (18pt) */
    h1 {
        font-size: 18pt !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 주요 섹션 제목 (13pt) */
    h2, h3 {
        font-size: 13pt !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* 질문 및 소제목 (12pt Bold) */
    h4, h5, h6 {
        font-size: 12pt !important;
        font-weight: bold !important;
    }

    @media print {
        header, [data-testid="stSidebar"], [data-testid="stToolbar"], .stActionButton { display: none !important; }
        .main .block-container { padding: 0 !important; }
        .stMarkdown, .stTable, .stPlotlyChart { page-break-inside: avoid; }
    }
    .answer-box { border: 1px solid #ccc; min-height: 80px; padding: 10px; margin-bottom: 20px; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

# 상단 인쇄 버튼 및 제목
col_title, col_print = st.columns([4, 1])
with col_title:
    st.title("📹 [수행평가 1-1] 포물선 운동 영상 분석 및 데이터 해석")
with col_print:
    if st.button("🖨️ 보고서 인쇄 / PDF 저장", key="print_btn"):
        st.components.v1.html("<script>parent.window.print()</script>", height=0)

st.divider()

# --- 학생 정보 입력부 ---
st.markdown("### 👤 학생 정보")
info_c1, info_c2, info_c3 = st.columns(3)
with info_c1:
    class_num = st.text_input("반 (Class)", placeholder="예: 3-1", key="class_num")
with info_c2:
    student_num = st.text_input("번호 (Number)", placeholder="예: 01", key="student_num")
with info_c3:
    student_name = st.text_input("성함 (Name)", placeholder="홍길동", key="student_name")

st.divider()

# --- 탐구 기본 정보 ---
st.markdown("### 📝 탐구 개요")
c1, c2 = st.columns(2)
with c1:
    st.info("**탐구 주제**: 운동 분석 프로그램으로 운동 분석")
with c2:
    st.success("**탐구 목표**: 비스듬히 위로 던진 물체의 운동을 분석하고 뉴턴의 운동 법칙으로 설명할 수 있다.")

st.markdown("---")

# --- 준비물 및 과정 ---
st.subheader("🛠️ 준비물 및 탐구 과정")
st.markdown("""
**[준비물]**
- **동영상 분석 프로그램**: [웹 서비스 접속 (https://videoanalysis.app?key=tvavTYNBRc)](https://videoanalysis.app?key=tvavTYNBRc)
- **분석용 영상**: 야구공 또는 농구공의 포물선 운동 영상

**[탐구 과정]**
1. **프로그램 접속**: 상단 링크를 통해 동영상 분석 프로그램에 접속합니다.
2. **영상 재생 및 설정**:
    - 분석할 영상을 프로그램에서 재생시킵니다.
    - 운동 분석을 위해 **클립 설정, 교정막대자 설정, 좌표축 설정, 질점 설정**을 수행합니다.
3. **데이터 추출**: 물체의 위치 변화를 추적하여 데이터와 그래프를 생성합니다.
""")

st.divider()

# --- 탐구 결과 1: 데이터 및 그래프 ---
st.subheader("📊 탐구 결과 1: 데이터 및 그래프 기록")
st.write("동영상 분석 프로그램에서 추출한 데이터 표와 5가지 종류의 그래프를 각각 캡처하여 업로드하세요.")

# 1. 데이터 표 업로드
st.markdown("#### 📋 1. 분석 데이터 표 기록")
data_file = st.file_uploader("데이터 표 이미지 또는 CSV 파일 업로드", type=['png', 'jpg', 'jpeg', 'csv'], key="data_file")

if data_file:
    if data_file.name.lower().endswith('.csv'):
        try:
            df = pd.read_csv(data_file)
            st.dataframe(df, use_container_width=True)
            st.caption("[기록] 분석 데이터 (CSV)")
        except Exception as e:
            st.error(f"CSV 파일을 읽는데 실패했습니다: {e}")
    else:
        st.image(data_file, use_container_width=True, caption="[기록] 분석 데이터 표 이미지")
else:
    st.info("실습 프로그램에서 다운로드한 CSV 파일 또는 캡처한 데이터 표 이미지를 업로드해 주세요.")

st.divider()

# 2. 분석 그래프 기록
st.markdown("#### 📈 2. 분석 그래프 기록")
st.caption("실습 프로그램의 그래프 화면을 캡처하여 업로드해 주세요.")

graph_sections = [
    ("track", "① 운동 궤적 (Position Track)"),
    ("pos", "② 시간-위치 (x-t, y-t) 그래프"),
    ("vel", "③ 시간-속도 (vx-t, vy-t) 그래프"),
    ("accel", "④ 시간-가속도 (ay-t) 그래프")
]

for key, label in graph_sections:
    with st.container():
        st.write(f"**{label}**")
        g_img = st.file_uploader(f"{label} 이미지 업로드", type=['png', 'jpg', 'jpeg'], key=f"g_img_{key}", label_visibility="collapsed")
        if g_img:
            st.image(g_img, use_container_width=True, caption=label)
        else:
            st.info(f"{label} 이미지를 업로드해 주세요.")
        st.write("") # 간격 조절

st.divider()

# --- 탐구 결과 2: 분석 결과 질문 ---
st.subheader("🤔 탐구 결과 2: 분석 결과 정리")
st.write("분석 데이터를 바탕으로 다음 질문에 답해 보세요.")

# 질문 및 답변 입력 영역
st.markdown("#### 가. 수평 방향 운동에서 속력은 시간에 따라 어떻게 변하는가?")
a1 = st.text_area("답변 입력 (가)", placeholder="실험 데이터를 통해 관찰한 내용을 적어주세요.", height=100, label_visibility="collapsed")

st.markdown("#### 나. 수평 방향 운동이 가와 같이 일어나는 이유는 무엇인가?")
a2 = st.text_area("답변 입력 (나)", placeholder="뉴턴의 운동 법칙을 적용하여 설명하세요.", height=100, label_visibility="collapsed")

st.markdown("#### 다. 연직 방향의 운동에서 속력은 시간에 따라 어떻게 변하는가?")
a3 = st.text_area("답변 입력 (다)", placeholder="최고점 도달 전후의 속력 변화를 포함하여 설명하세요.", height=100, label_visibility="collapsed")

st.markdown("#### 라. 연직 방향 운동에서 다와 같이 일어나는 이유는 무엇인가?")
a4 = st.text_area("답변 입력 (라)", placeholder="작용하는 힘(알짜힘)의 관점에서 설명하세요.", height=100, label_visibility="collapsed")

# --- 추가 질문 마, 바 ---
st.markdown("#### 마. 다음 표에 최고점 도달 시간, 최고점의 높이, 수평 도달 거리를 기록하시오.")
m_cols = st.columns(3)
m_labels = ["최고점의 도달 시간(s)", "최고점의 높이(h)", "수평도달 거리(m)"]
for i, label in enumerate(m_labels):
    with m_cols[i]:
        st.markdown(f"<div style='background-color:#fce4d6; padding:5px; text-align:center; font-weight:bold; border:1px solid #000; font-size:12pt; color:black;'>{label}</div>", unsafe_allow_html=True)
        st.text_input(label, label_visibility="collapsed", key=f"m_input_{i}")

st.write("") # 간격

st.markdown("#### 바. 엑셀 파일에서 최고점 도달 시간관을 기준으로 이론적으로 계산한 수평도달 거리와 최고점의 높이를 야구공의 값과 비교하고, 차이가 나는 이유를 추론해보자.")
st.write("**[이론값]**")
b_cols = st.columns(3)
for i, label in enumerate(m_labels):
    with b_cols[i]:
        st.markdown(f"<div style='background-color:#fce4d6; padding:5px; text-align:center; font-weight:bold; border:1px solid #000; font-size:12pt; color:black;'>{label}</div>", unsafe_allow_html=True)
        st.text_input(label + " (이론)", label_visibility="collapsed", key=f"b_theory_{i}")

st.write("**[추론 및 결과 비교 기록]**")
a5 = st.text_area("결과 비교 및 추론", placeholder="이론값과 실제값의 차이가 발생하는 원인(공기 저항 등)을 물리적 원리와 함께 추론하여 적어주세요.", height=150, label_visibility="collapsed")

st.divider()
st.caption("사곡고등학교 물리학 II 시뮬레이션 및 실습 지원 포털 | 본 보고서는 작성 후 상단 인쇄 버튼을 통해 PDF로 저장할 수 있습니다.")
