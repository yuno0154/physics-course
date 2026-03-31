import streamlit as st
import pandas as pd
import numpy as np

# 페이지 설정
# st.set_page_config(page_title="포물선 운동 영상 분석 실습", layout="wide") # main_app에서 설정됨

# CSS를 활용한 인쇄 최적화
st.markdown("""
    <style>
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
    st.title("📹 [포물선 운동 영상 분석 실습] 보고서")
with col_print:
    if st.button("🖨️ 보고서 인쇄 / PDF 저장", key="print_btn"):
        st.components.v1.html("<script>parent.window.print()</script>", height=0)

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
st.write("운동 분석 프로그램에서 생성된 데이터 표와 그래프를 다운로드하거나 캡처하여 아래에 업로드하세요.")

col_img1, col_img2 = st.columns(2)
with col_img1:
    st.markdown("##### 📋 분석 데이터 표")
    data_img = st.file_uploader("이미지 파일 선택 (데이터 표)", type=['png', 'jpg', 'jpeg'], key="data_img")
    if data_img:
        st.image(data_img, use_container_width=True)
    else:
        st.info("실습 프로그램에서 캡처한 데이터 표를 업로드하세요.")

with col_img2:
    st.markdown("##### 📈 분석 그래프")
    graph_img = st.file_uploader("이미지 파일 선택 (그래프)", type=['png', 'jpg', 'jpeg'], key="graph_img")
    if graph_img:
        st.image(graph_img, use_container_width=True)
    else:
        st.info("실습 프로그램에서 캡처한 그래프를 업로드하세요.")

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

st.divider()
st.caption("사곡고등학교 물리학 II 시뮬레이션 및 실습 지원 포털 | 본 보고서는 작성 후 상단 인쇄 버튼을 통해 PDF로 저장할 수 있습니다.")
