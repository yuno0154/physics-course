import streamlit as st
import os
import base64
from pathlib import Path

try:
    from streamlit_pdf_viewer import pdf_viewer
    HAS_PDF_VIEWER = True
except ImportError:
    HAS_PDF_VIEWER = False

# 스타일 커스텀 CSS (Streamlit Wide 화면에 최적화된 반응형 카드 & 테이블)
st.markdown("""
<style>
/* 카드 스타일 */
.plan-kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    margin-bottom: 12px;
    transition: all 0.2s ease;
}
.plan-kpi-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.1);
}
.plan-kpi-title {
    font-size: 13px;
    color: #64748b;
    font-weight: 600;
    margin-bottom: 4px;
}
.plan-kpi-num {
    font-size: 28px;
    font-weight: 800;
    color: #1e293b;
    line-height: 1.1;
}
.plan-kpi-num span {
    font-size: 16px;
    color: #3b82f6;
    font-weight: 600;
    margin-left: 2px;
}
.plan-kpi-sub {
    font-size: 11.5px;
    color: #94a3b8;
    margin-top: 6px;
}

/* 타임라인 배지 */
.timeline-box {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 10px 0 16px;
}
.timeline-item {
    flex: 1 1 200px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 14px;
    border-left: 4px solid #3b82f6;
}
.timeline-month {
    font-size: 12px;
    font-weight: 700;
    color: #2563eb;
}
.timeline-desc {
    font-size: 13px;
    font-weight: 600;
    color: #1e293b;
    margin-top: 2px;
}
.timeline-detail {
    font-size: 11.5px;
    color: #64748b;
}

/* 뱃지 */
.badge-tag {
    display: inline-block;
    padding: 2px 7px;
    font-size: 11px;
    font-weight: 600;
    border-radius: 4px;
    margin-right: 4px;
}
.badge-blue { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.badge-gray { background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }
.badge-green { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
.badge-amber { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }

/* 표 디자인 */
.custom-eval-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    margin-top: 8px;
    margin-bottom: 12px;
}
.custom-eval-table th {
    background: #f8fafc;
    color: #334155;
    font-weight: 700;
    padding: 10px 12px;
    border: 1px solid #e2e8f0;
    text-align: left;
}
.custom-eval-table td {
    padding: 9px 12px;
    border: 1px solid #e2e8f0;
    vertical-align: middle;
}
.custom-eval-table tr:hover {
    background-color: #f8fafc;
}
</style>
""", unsafe_allow_html=True)

# 1. 헤더 섹션
st.title("🏠 물리학습 지원 포털")

st.markdown("""
안녕하세요! **물리학습 지원 포털**에 오신 것을 환영합니다.
이 포털은 학생들이 물리학의 핵심 개념을 직관적으로 이해하고 탐구할 수 있도록 돕기 위해 제작되었습니다.
좌측의 네비게이션 메뉴를 사용하여 다양한 가상 실험과 시뮬레이션 도구를 탐색해 보세요.
""")

st.markdown("---")

# 2. 평가계획 타이틀 및 다운로드 상단 배치
pdf_file_name = "2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획서.pdf"
pdf_path = Path(__file__).parent / pdf_file_name

col_title, col_btn = st.columns([3, 1.2])
with col_title:
    st.subheader("📑 2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획")
    st.caption("사곡고등학교 2학년 · 담당교사 최연호 · 2022 개정 교육과정 기반 교수학습 및 평가 운영 계획")

with col_btn:
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        st.download_button(
            label="📥 평가계획서 전문(PDF) 다운로드",
            data=pdf_data,
            file_name=pdf_file_name,
            mime="application/pdf",
            use_container_width=True
        )
    else:
        st.warning("PDF 파일 없음")

# 3. 핵심 KPI 메트릭 4분할 카드 (와이드 화면 밸런스 확보)
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="plan-kpi-card">
        <div class="plan-kpi-title">지필평가 (정기시험)</div>
        <div class="plan-kpi-num">60<span>%</span></div>
        <div class="plan-kpi-sub">1차 30% · 2차 30% (선택형 100%)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="plan-kpi-card">
        <div class="plan-kpi-title">수행평가 (과정중심)</div>
        <div class="plan-kpi-num">40<span>%</span></div>
        <div class="plan-kpi-sub">수행 ① 20% · 수행 ② 20% (총 2개 영역)</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="plan-kpi-card">
        <div class="plan-kpi-title">서·논술형 평가</div>
        <div class="plan-kpi-num">20<span>%</span></div>
        <div class="plan-kpi-sub">수행평가 영역 내 사고·논증 측정</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="plan-kpi-card">
        <div class="plan-kpi-title">최소 성취 보장 기준</div>
        <div class="plan-kpi-num">40<span>%</span></div>
        <div class="plan-kpi-sub">학기말 성취율 미도달자 예방·보장 지도</div>
    </div>
    """, unsafe_allow_html=True)

# 4. Streamlit 네이티브 탭 인터페이스 (내용에 맞춰 유연하게 반응)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 1. 평가 개요 및 시기",
    "🎯 2. 성취도 기준 (A~E)",
    "🛰️ 3. 수행평가 ① 위성 궤도 설계",
    "🔊 4. 수행평가 ② 파동·음향 제어",
    "📋 5. 운영 원칙 및 결시 처리"
])

# ----------------- TAB 1 -----------------
with tab1:
    st.markdown("#### 🗓️ 학기 중 평가 진행 타임라인")
    st.markdown("""
    <div class="timeline-box">
        <div class="timeline-item" style="border-left-color: #0ea5e9;">
            <div class="timeline-month">9월 실시</div>
            <div class="timeline-desc">수행평가 ①</div>
            <div class="timeline-detail">위성 임무 궤도 설계 탐구 (20%)</div>
        </div>
        <div class="timeline-item" style="border-left-color: #2563eb;">
            <div class="timeline-month">10월 실시</div>
            <div class="timeline-desc">정기시험 1차</div>
            <div class="timeline-detail">선택형 지필평가 (30%)</div>
        </div>
        <div class="timeline-item" style="border-left-color: #8b5cf6;">
            <div class="timeline-month">11월 실시</div>
            <div class="timeline-desc">수행평가 ②</div>
            <div class="timeline-detail">모빌리티 음향·파동 제어 탐구 (20%)</div>
        </div>
        <div class="timeline-item" style="border-left-color: #ef4444;">
            <div class="timeline-month">12월 실시</div>
            <div class="timeline-desc">정기시험 2차</div>
            <div class="timeline-detail">선택형 지필평가 (30%) · <span class="badge-tag badge-blue">동점 1순위</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📋 평가 종류 · 반영 비율 · 동점자 순위")
    st.markdown("""
    <table class="custom-eval-table">
        <thead>
            <tr>
                <th style="width: 25%;">평가 유형</th>
                <th style="width: 25%;">평가 방법</th>
                <th style="width: 15%; text-align: center;">만점(반영비율)</th>
                <th style="width: 15%; text-align: center;">실시 시기</th>
                <th style="width: 20%; text-align: center;">동점자 처리 순위</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>정기시험 1차</b></td>
                <td>선택형 (지필평가)</td>
                <td style="text-align: center;">100점 (30%)</td>
                <td style="text-align: center;">10월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">2순위</span></td>
            </tr>
            <tr>
                <td><b>정기시험 2차</b></td>
                <td>선택형 (지필평가)</td>
                <td style="text-align: center;">100점 (30%)</td>
                <td style="text-align: center;">12월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-blue">★ 1순위</span></td>
            </tr>
            <tr>
                <td><b>수행평가 ①</b><br><span style="font-size: 11px; color:#64748b;">위성 임무 궤도 설계 탐구</span></td>
                <td>실험·실습 / 서·논술형</td>
                <td style="text-align: center;">100점 (20%)</td>
                <td style="text-align: center;">9월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">3순위</span></td>
            </tr>
            <tr>
                <td><b>수행평가 ②</b><br><span style="font-size: 11px; color:#64748b;">모빌리티 음향·파동 제어 탐구</span></td>
                <td>실험·실습 / 서·논술형</td>
                <td style="text-align: center;">100점 (20%)</td>
                <td style="text-align: center;">11월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">4순위</span></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    st.info("💡 **평가 원칙:** 정기시험 60% + 수행평가 40%(서·논술형 20% 포함)로 운영되며, 동점자 발생 시 **2차 정기시험 ➔ 1차 정기시험 ➔ 수행 ① ➔ 수행 ②** 순으로 우선순위를 부여합니다.")

# ----------------- TAB 2 -----------------
with tab2:
    col_t2_1, col_t2_2 = st.columns([1, 1.2])
    with col_t2_1:
        st.markdown("#### 🎯 기준 성취율과 성취도 평정")
        st.markdown("""
        <table class="custom-eval-table">
            <thead>
                <tr>
                    <th style="text-align: center;">성취도</th>
                    <th>성취율(환산 점수 기준)</th>
                    <th style="text-align: center;">구분</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="text-align: center; font-weight: 800; color: #2563eb;">A</td>
                    <td><b>90% 이상 ~ 100%</b></td>
                    <td style="text-align: center;"><span class="badge-tag badge-blue">탁월</span></td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: 800; color: #0284c7;">B</td>
                    <td><b>80% 이상 ~ 90% 미만</b></td>
                    <td style="text-align: center;"><span class="badge-tag badge-blue">우수</span></td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: 800; color: #16a34a;">C</td>
                    <td><b>70% 이상 ~ 80% 미만</b></td>
                    <td style="text-align: center;"><span class="badge-tag badge-green">보통</span></td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: 800; color: #d97706;">D</td>
                    <td><b>60% 이상 ~ 70% 미만</b></td>
                    <td style="text-align: center;"><span class="badge-tag badge-amber">기초</span></td>
                </tr>
                <tr>
                    <td style="text-align: center; font-weight: 800; color: #64748b;">E</td>
                    <td><b>60% 미만</b></td>
                    <td style="text-align: center;"><span class="badge-tag badge-gray">노력요함</span></td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_t2_2:
        st.markdown("#### 📌 분할점수 산출 및 최소 성취수준 보장")
        st.markdown("""
        <div class="plan-kpi-card" style="margin-top: 8px;">
            <div style="font-weight: 700; color: #1e293b; margin-bottom: 6px;">📐 성취도 산출 방식</div>
            <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                본 교과는 교육과정 성취수준에 따라 <b>추정 분할점수</b> 산출 방식을 적용하여 평정합니다. 정기시험(1차·2차)과 수행평가(1·2)의 반영 비율 환산 점수 합계를 기준으로 최종 성취도(A~E)가 부여됩니다.
            </div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #f1f5f9;">
            <div style="font-weight: 700; color: #dc2626; margin-bottom: 6px;">🛡️ 최소성취수준 보장지도 계획</div>
            <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                학기말 최종 성취율 <b>40% 미도달 예상자 및 미도달자</b>를 대상으로 보충 학습 자료 제공, 1:1 맞춤 지도, 추가 과제 피드백 등 학교 자체 <b>최소성취수준 보장지도 프로그램</b>을 운영합니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3 -----------------
with tab3:
    st.markdown("#### 🛰️ 수행평가 ① 세부 채점기준 (최고 수준 요약)")
    st.caption("주제: 역학과 에너지로 증명하는 최적의 위성 임무 궤도 설계 탐구 · 관련 성취기준: [12역학01-02], [12역학01-04], [12역학01-05] · 9월 실시 · 100점 만점 (반영 20%)")

    st.markdown("""
    <table class="custom-eval-table">
        <thead>
            <tr>
                <th style="width: 25%;">평가 요소 및 방법</th>
                <th style="width: 65%;">최고 수준(만점) 채점 기준</th>
                <th style="width: 10%; text-align: center;">배점</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>1. 지표면 역학 분석</b><br><span class="badge-tag badge-blue">실험·보고서</span> <span class="badge-tag badge-gray">모둠</span></td>
                <td>측정값을 수평·연직별 표·그래프로 명확히 나타내고 연직 가속도를 직접 산출하여 수평 등속·연직 등가속 운동의 <b>독립성을 수식·계산과 함께 오류 없이 정량 입증</b>하며, 이론값과 실험값 간의 오차 원인을 공기 저항 등 물리적 요인과 연계하여 논리적으로 서술함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
            <tr>
                <td><b>2. 케플러 법칙·관계식 유도</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>중력과 구심 가속도 조건을 물리 기호로 표현하고 <b>공전 주기-궤도 반지름 간의 거듭제곱 비례식을 단계별 논리적 비약 없이 완전 유도</b>하며 상수의 물리적 의미를 서술함. 원 궤도 유지의 원인이 중력임을 설명하고 반지름 변화에 따른 속도·주기 관계를 완벽히 논증함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
            <tr>
                <td><b>3. 실제 위성 데이터 검증</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>실제 인공위성 및 ISS의 관측 데이터(궤도 반지름, 주기, 속력)를 표로 바르게 작성하고 <b>수학적 계산 과정을 거쳐 정량적 관계를 명확히 입증</b>하며, 수치 경향성을 근거로 궤도 반지름과 주기·속력의 상관관계를 체계적으로 설명함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
            <tr>
                <td><b>4. 임무 궤도 선정·에너지</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>임무 환경 제약 조건을 종합 추출하여 최적 궤도를 선정하고, 정지궤도 위성과 비교하여 목표 고도와 역학적 에너지(위치+운동)의 크기 및 전환 관계를 <b>역학적 에너지 보존 법칙을 적용해 오개념 없이 논리적으로 설명</b>함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
            <tr>
                <td><b>5. 로켓 발사·궤도 전이 논증</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>다단 로켓 발사 과정(연소 및 단분리)에서의 <b>운동량 보존 법칙을 명확히 제시</b>하고, 타원 전이 궤도에서 목표 원 궤도로 진입하기 위한 속도 조정 과정을 <b>역학적 에너지 보존과 유기적으로 연결하여 논리적으로 입증</b>함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

# ----------------- TAB 4 -----------------
with tab4:
    st.markdown("#### 🔊 수행평가 ② 세부 채점기준 (최고 수준 요약)")
    st.caption("주제: 탄성파와 소리 원리를 적용한 미래형 모빌리티 음향 역학 및 파동 제어 탐구 · 관련 성취기준: [12역학03-03], [12역학03-04], [12역학03-05] · 11월 실시 · 100점 만점 (반영 20%)")

    st.markdown("""
    <table class="custom-eval-table">
        <thead>
            <tr>
                <th style="width: 25%;">평가 요소 및 방법</th>
                <th style="width: 65%;">최고 수준(만점) 채점 기준</th>
                <th style="width: 10%; text-align: center;">배점</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>1. 정상파 공명·음속 산출</b><br><span class="badge-tag badge-blue">실험·실습</span> <span class="badge-tag badge-gray">모둠</span></td>
                <td>관의 경계 조건(막힌 끝 마디, 열린 끝 배)과 공기 입자의 진동을 연계하여 파장 변화를 정량적으로 설명하고, 스마트 기기 센서 측정값으로부터 <b>차내 음속을 비약·오류 없이 정량 산출</b>하며, 개구단 보정·온도 등 실측-이론 오차 요인을 인과적으로 완벽히 서술함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">40점</td>
            </tr>
            <tr>
                <td><b>2. 도플러 효과·상대속도 역산</b><br><span class="badge-tag badge-blue">실험·실습</span> <span class="badge-tag badge-gray">모둠</span></td>
                <td>파원의 상대 운동에 따른 파면 압축 기하학적 모델을 바탕으로 <b>도플러 관측 진동수 관계식을 논리적으로 유도</b>하고, 접근하는 긴급차량 사이렌의 주파수 변화 데이터로부터 <b>상대 속도를 수식과 함께 정량적으로 역산</b>함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
            <tr>
                <td><b>3. 에너지 최적화 (ANC 소음 제어)</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>파동의 중첩과 간섭 원리를 토대로 <b>상쇄 간섭 조건(역위상, 경로차 ΔL = λ/2)을 정량 유도</b>하여 최적 스피커 경로차를 계산하고, 차량 내 저주파 소음을 능동 소음 제어(ANC) 기술로 상쇄 소멸시키는 작동 메커니즘을 인과적으로 완벽히 논증함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.warning("⚠️ **원문 확인 안내:** 수행평가 ②의 2번 요소(도플러 효과 상대속도 역산, 30점) 채점기준 문구가 원본 문서 일부에서 '전기 에너지-열량 변환' 내용으로 기재되어 있어, 평가계획 본래의 취지(도플러 효과 및 상대속도 역산)에 맞게 정정 안내합니다.")

# ----------------- TAB 5 -----------------
with tab5:
    col_t5_1, col_t5_2 = st.columns(2)
    with col_t5_1:
        st.markdown("#### ⚖️ 평가 운영 5대 원칙")
        st.markdown("""
        <div class="plan-kpi-card">
            <ul style="padding-left: 18px; margin: 0; font-size: 13px; color: #334155; line-height: 1.8;">
                <li><b>사전 예고제:</b> 평가 시기, 반영 비율, 평가 방법, 세부 채점기준을 학생들에게 사전 공지합니다.</li>
                <li><b>수업 연계 원칙:</b> 수행평가는 정규 수업 시간 내에 실시하며, 과제형(가정 학습형) 평가는 일체 지양합니다.</li>
                <li><b>공정성 및 신뢰성:</b> AI 도구 활용 시 공정성 가이드라인을 준수하며 표절 및 대리 작성을 방지합니다.</li>
                <li><b>즉시 공개 및 확인:</b> 채점 완료 즉시 결과를 공개하여 학생 개별 확인 및 성적 일람표 서명을 진행합니다.</li>
                <li><b>이의신청 기간 운영:</b> 결과 공개 후 공식 이의신청 기간을 두어 객관성과 투명성을 확보합니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_t5_2:
        st.markdown("#### 🏥 결시생 및 학적 변동자 성적 처리")
        st.markdown("""
        <div class="plan-kpi-card">
            <ul style="padding-left: 18px; margin: 0; font-size: 13px; color: #334155; line-height: 1.8;">
                <li><b>정기시험 결시:</b> 본교 학업성적관리규정에 의거하여 인정점(공결 100%, 병결 80% 등)을 환산 부여합니다.</li>
                <li><b>수행평가 결시:</b> 정당한 사유(공결, 병결 등)가 있는 경우 1회의 추가 응시 기회를 제공하며, 정당 사유 없이 불응 시 0점 처리합니다.</li>
                <li><b>전입생 처리:</b> 원적교 성적이 있는 경우 반영 비율로 환산 적용하며, 없는 경우 본교 추가 평가 기준에 따릅니다.</li>
                <li><b>장기 미인정 결석자:</b> 해당 영역 평가 미응시 시 영역별 최하점의 차하점(-1점)을 부여합니다.</li>
                <li><b>기타 예외 사항:</b> 교과협의회 및 학업성적관리위원회의 심의를 거쳐 결정합니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# 5. 원본 PDF 펼쳐보기 섹션
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
if os.path.exists(pdf_path):
    with st.expander("📖 2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획서 원본 전문(PDF) 펼쳐보기", expanded=False):
        if HAS_PDF_VIEWER:
            pdf_viewer(str(pdf_path), width=850)
        else:
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("---")

# 6. 하단 학습 자료 및 가상실험 바로가기
st.markdown("""
### 📂 역학과 에너지 학습 자료 및 시뮬레이션 안내
교과 수업 및 수행평가 탐구 보고서 작성과 관련된 추가 학습 자료는 아래 구글 드라이브에서 확인하실 수 있습니다.

* **[구글 드라이브 바로가기](https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link)**

| 학습 자료실 QR 코드 | 📍 역학과 에너지 핵심 가상 실험실 |
| :---: | :--- |
| ![DRIVE_QR](https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://drive.google.com/drive/folders/1C_LpA1TGeVk6sNhMSYe-azp67Sp1Y0eT?usp=drive_link) | • **[수행① 대비]** 포물선 운동 분석 및 역학적 에너지 보존 탐구 <br> • **[수행① 대비]** 케플러 법칙 수학적 유도 및 실제 위성 궤도 데이터 분석 <br> • **[심화 탐구]** 일반 상대성 이론과 등가원리, 중력장 및 블랙홀 시뮬레이션 <br> • **[수행② 대비]** 정상파 공명 및 파동의 중첩·간섭 음향 제어 시뮬레이션 |

제작: 사곡고등학교 물리실
""")
