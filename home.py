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
pdf_file_name = "2026학년도 사곡고 2학기 2학년 역학과 에너지 과목 교수학습-평가계획(최연호)-수정본(10.19.).pdf"
pdf_path = Path(__file__).parent / pdf_file_name
# 파일이 없을 경우 대체 경로
if not os.path.exists(pdf_path):
    pdf_path = Path(__file__).parent / "2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획서.pdf"

col_title, col_btn = st.columns([3, 1.2])
with col_title:
    st.subheader("📑 2026학년도 사곡고 2학기 2학년 역학과 에너지 평가계획 (수정본)")
    st.caption("사곡고등학교 2학년 · 담당교사 최연호 · 2022 개정 교육과정 기반 교수학습 및 평가 운영 계획")

with col_btn:
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        st.download_button(
            label="📥 수정 평가계획서(PDF) 다운로드",
            data=pdf_data,
            file_name="2026학년도 사곡고 2학기 2학년 역학과 에너지 과목 교수학습-평가계획(최연호)-수정본.pdf",
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
        <div class="plan-kpi-num">28<span>%</span></div>
        <div class="plan-kpi-sub">수행평가 내 사고·논증 측정 비율 (16%+12%)</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="plan-kpi-card">
        <div class="plan-kpi-title">최소 성취수준 기준</div>
        <div class="plan-kpi-num" style="font-size: 22px; color: #64748b; margin-top: 6px; margin-bottom: 2px;">기준 없음</div>
        <div class="plan-kpi-sub">성취도 5단계(A~E) 평정 · 최소성취수준 미적용</div>
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
            <div class="timeline-detail">위성 임무 궤도 설계 탐구 (20%, 서·논술형 16%)</div>
        </div>
        <div class="timeline-item" style="border-left-color: #2563eb;">
            <div class="timeline-month">10월 실시</div>
            <div class="timeline-desc">정기시험 1차</div>
            <div class="timeline-detail">선택형 지필평가 (30%) · <span class="badge-tag badge-gray">동점 2순위</span></div>
        </div>
        <div class="timeline-item" style="border-left-color: #8b5cf6;">
            <div class="timeline-month">11월 실시</div>
            <div class="timeline-desc">수행평가 ②</div>
            <div class="timeline-detail">모빌리티 음향·파동 제어 탐구 (20%, 서·논술형 12%)</div>
        </div>
        <div class="timeline-item" style="border-left-color: #ef4444;">
            <div class="timeline-month">12월 실시</div>
            <div class="timeline-desc">정기시험 2차</div>
            <div class="timeline-detail">선택형 지필평가 (30%) · <span class="badge-tag badge-blue">★ 동점 1순위</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📋 평가 종류 · 반영 비율 · 동점자 순위")
    st.markdown("""
    <table class="custom-eval-table">
        <thead>
            <tr>
                <th style="width: 25%;">평가 유형</th>
                <th style="width: 23%;">평가 방법</th>
                <th style="width: 17%; text-align: center;">만점(반영비율)</th>
                <th style="width: 15%; text-align: center;">서·논술형 비율</th>
                <th style="width: 10%; text-align: center;">실시 시기</th>
                <th style="width: 10%; text-align: center;">동점 순위</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>정기시험 1차</b></td>
                <td>선택형 (지필평가)</td>
                <td style="text-align: center;">100점 (30%)</td>
                <td style="text-align: center;">-</td>
                <td style="text-align: center;">10월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">2순위</span></td>
            </tr>
            <tr>
                <td><b>정기시험 2차</b></td>
                <td>선택형 (지필평가)</td>
                <td style="text-align: center;">100점 (30%)</td>
                <td style="text-align: center;">-</td>
                <td style="text-align: center;">12월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-blue">★ 1순위</span></td>
            </tr>
            <tr>
                <td><b>수행평가 ①</b><br><span style="font-size: 11px; color:#64748b;">위성 임무 궤도 설계 탐구</span></td>
                <td>실험·실습 / 서·논술형</td>
                <td style="text-align: center;">100점 (20%)</td>
                <td style="text-align: center; font-weight: 600; color: #2563eb;">16%</td>
                <td style="text-align: center;">9월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">3순위</span></td>
            </tr>
            <tr>
                <td><b>수행평가 ②</b><br><span style="font-size: 11px; color:#64748b;">미래형 모빌리티 음향·파동 제어 탐구</span></td>
                <td>실험·실습 / 서·논술형</td>
                <td style="text-align: center;">100점 (20%)</td>
                <td style="text-align: center; font-weight: 600; color: #2563eb;">12%</td>
                <td style="text-align: center;">11월 중</td>
                <td style="text-align: center;"><span class="badge-tag badge-gray">4순위</span></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)
    st.info("💡 **평가 운영 원칙:** 정기시험 60% + 수행평가 40%(서·논술형 평가 28% 포함)로 운영되며, 동점자 발생 시 **2차 정기시험 ➔ 1차 정기시험 ➔ 수행 ① ➔ 수행 ②** 순으로 우선순위를 부여합니다.")

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
        st.markdown("#### 📌 분할점수 산출 및 성취수준 평정 방식")
        st.markdown("""
        <div class="plan-kpi-card" style="margin-top: 8px;">
            <div style="font-weight: 700; color: #1e293b; margin-bottom: 6px;">📐 성취도 산출 방식</div>
            <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                본 교과는 교육과정 성취수준에 따라 <b>고정 분할점수</b>(90%-80%-70%-60%) 방식을 적용하여 평정합니다. 정기시험(1차·2차)과 수행평가(1·2)의 반영 비율 환산 점수 합계를 기준으로 최종 성취도(A~E 5단계)가 부여됩니다.
            </div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #f1f5f9;">
            <div style="font-weight: 700; color: #475569; margin-bottom: 6px;">ℹ️ 최소 성취수준 기준 안내</div>
            <div style="font-size: 12.5px; color: #475569; line-height: 1.6;">
                <b>본 교과(역학과 에너지)는 최소성취수준 기준이 적용되지 않습니다.</b> (최소성취수준 기준 없음 · 미적용 과목)
            </div>
        </div>
        """, unsafe_allow_html=True)

# ----------------- TAB 3 -----------------
with tab3:
    st.markdown("#### 🛰️ 수행평가 ① 세부 채점기준 (최고 수준 요약)")
    st.caption("주제: 역학과 에너지로 증명하는 최적의 위성 임무 궤도 설계 탐구 · 관련 성취기준: [12역학01-02], [12역학01-04], [12역학01-05] · 9월 실시 · 100점 만점 (반영 20%, 서·논술형 16%)")

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
                <td><b>1. 지표면 역학 분석</b><br><span class="badge-tag badge-blue">실험 및 보고서</span> <span class="badge-tag badge-gray">모둠</span></td>
                <td>영상 분석 프로그램을 통해 추출한 측정값을 수평·연직별 표와 그래프로 나타내고, 연직 가속도 값을 직접 산출하여 수평 등속 및 연직 등가속도 운동의 <b>독립성을 수식 및 계산 과정과 함께 오류 없이 정량적으로 입증</b>하며, 대표 지점의 운동 에너지와 위치 에너지로 역학적 에너지 보존을 확인하고, 이론값과 실험값의 오차 원인을 측정 오차와 모델의 가정(공기 저항 무시)으로 나누어 논리적으로 서술함. (※ 개념적 오류나 유도 과정의 오류가 하나도 없는 경우)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
            <tr>
                <td><b>2. 케플러 법칙과 궤도 관계식 유도</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>중심 천체와 위성 사이에 작용하는 상호작용과 구심 조건의 관계를 기호로 올바르게 표현하고, 이를 바탕으로 <b>공전 주기와 궤도 반지름 사이의 거듭제곱 비례 관계식을 단계별 오류 없이 유도</b>하며, 상수의 의미와 보편성을 논리적으로 서술함. 인공위성이 원 궤도를 유지하는 근본 원인이 중력임을 설명하고 반지름 변화에 따른 속도와 주기의 관계를 명확히 논증함. (※ 한 가지의 개념적 오류나 유도 과정의 오류가 없는 경우)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
            <tr>
                <td><b>3. 실제 인공위성 궤도 데이터 분석 및 정량적 검증</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>실제 인공위성 및 ISS의 관측 데이터(궤도 반지름, 공전 주기, 속력 등)를 표를 바르게 작성하고, <b>데이터 간의 정량적 관계를 계산 과정을 통해 정확히 입증</b>함. 데이터의 수치적 경향성을 근거로 궤도 반지름과 주기·속력의 상관관계를 논리적으로 설명함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
            <tr>
                <td><b>4. 위성 궤도별 역학적 에너지 비교</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>제시된 목표 궤도와 정지궤도 위성의 운동 에너지, 위치 에너지, 역학적 에너지를 궤도 반지름으로 비교하고, <b>목표 궤도로 옮기는 데 에너지가 더 필요한지 줄어드는지를 근거와 함께 바르게 설명</b>함.</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">10점</td>
            </tr>
            <tr>
                <td><b>5. 다단 로켓 발사와 궤도 전이 논증</b><br><span class="badge-tag badge-green">서술형 (운동량·역학적 에너지 보존)</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>제시된 발사 상황에 운동량 보존 법칙을 적절한 계 설정과 함께 적용하여 로켓의 가속 원리와 다단 구조의 효과를 인과적으로 설명함. 뉴턴 운동 법칙을 적용하여 위성이 궤도에 진입하고 이를 유지하는 조건을 근거와 함께 논증함. 발사 단계와 궤도 단계의 설명이 <b>하나의 일관된 논리로 연결됨</b>. (※ 개념적 오류나 논리적 비약이 없는 경우)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">20점</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    with st.expander("🚀 전이 가능한 자기주도적 탐구 안내 (평가 점수 미반영)", expanded=False):
        st.markdown("""
        * **[과제 1] 화성 탐사를 위한 궤도 전이:** 지구 궤도에서 화성 궤도로 가기 위해 필요한 속도 변화량을 역학적 에너지 보존 법칙과 케플러 법칙을 이용해 추론
        * **[과제 2] 우주 쓰레기와 충돌의 물리학:** 고도 400km에서 공전하는 10g의 파편이 가진 운동 에너지를 계산하고 지상 포물선 운동 물체의 에너지와 비교
        * **[과제 3] 블랙홀 주위의 빛의 궤도:** 위성 대신 빛이 블랙홀 주위를 원운동 할 때의 궤도 반지름 계산
        """)

# ----------------- TAB 4 -----------------
with tab4:
    st.markdown("#### 🔊 수행평가 ② 세부 채점기준 (최고 수준 요약)")
    st.caption("주제: 탄성파와 소리 원리를 적용한 미래형 모빌리티 음향 역학 및 파동 제어 탐구 · 관련 성취기준: [12역학03-03], [12역학03-04], [12역학03-05] · 11월 실시 · 100점 만점 (반영 20%, 서·논술형 12%)")

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
                <td><b>1. 정상파 공명 데이터 분석 및 관 경계 조건 기반 차내 음속 구하기</b><br><span class="badge-tag badge-blue">실험</span> <span class="badge-tag badge-gray">모둠</span></td>
                <td>파동의 간섭으로 형성되는 정상파의 원리를 이용하여 관의 길이 변화에 따라 정상파의 파장이 달라짐을 관의 경계 조건과 매질 입자의 진동 가능 여부로 정량적으로 설명함. 스마트 기기를 활용하여 음파의 특성을 분석하고 정상파를 이용하여 <b>차내 음파의 진행 속력을 계산 과정의 비약 없이 정량적으로 오류 없이 산출</b>함. 실험을 통해 산출한 음속과 이론적 음속 간 오차가 발생한 물리적 요인을 들고, 이것이 측정값에 미친 영향을 인과적으로 바르게 서술함. (※ 한 가지의 개념적 오류나 수식·단위 누락이 없어야 함)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">40점</td>
            </tr>
            <tr>
                <td><b>2. 도플러 효과 파면 압축 모델링 및 긴급차량 상대 속도 역산 논증</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>제시된 상황에서 파원의 운동에 따른 파면 간격의 변화를 근거로 <b>도플러 효과의 관측 진동수 관계를 논리적으로 도출</b>하고, 이를 측정 자료에 적용하여 <b>긴급차량의 속도를 정량적으로 산출</b>함. 산출 결과의 타당성을 검토하고, 도플러 효과가 속도 측정 장치에 이용되는 원리와 연결하여 설명함. (※ 개념적 오류나 수식·단위 누락이 없는 경우)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
            <tr>
                <td><b>3. 음파의 간섭을 이용한 능동 소음 제어(ANC) 원리 논증</b><br><span class="badge-tag badge-green">서술형</span> <span class="badge-tag badge-gray">개별</span></td>
                <td>파동의 중첩과 간섭 원리를 근거로 <b>상쇄 간섭이 일어나는 조건을 설명</b>하고, 이를 제시된 차내 소음 상황에 적용하여 <b>능동 소음 제어(ANC) 시스템이 소음을 줄이는 과정을 인과적으로 논증</b>함. 소음 제어 기술의 활용 사례와 한계를 과학적 근거로 판단함. (※ 개념적 오류가 없는 경우)</td>
                <td style="text-align: center; font-weight: 700; color:#2563eb;">30점</td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    with st.expander("🔊 전이 가능한 자기주도적 탐구 안내 (평가 점수 미반영)", expanded=False):
        st.markdown("""
        * **[과제 1] 초음속 비행과 소닉 붐(Sonic Boom)의 충격파 메커니즘:** 마하 원뿔(Mach Cone) 및 소닉 붐의 원리를 도플러 효과 및 파면 상호작용 관점에서 분석
        * **[과제 2] 3차원 공간 능동 소음 제어(3D ANC)의 한계와 위상 제어:** 3차원 공간 전체 소음 상쇄의 어려움을 파동의 입사각, 경로차, 맥동(Beat) 현상을 중심으로 추론
        * **[과제 3] 전기차 가상 엔진 사운드(AVAS) 감성 음향과 맥동 현상:** 주파수 맥동 공식 유도 및 음향 합성 원리 논증
        * **[과제 4] 의료용 도플러 초음파 진단과 고강도 집속 초음파(HIFU)의 파동 제어:** 혈류 측정 초음파와 HIFU의 반사, 간섭, 도플러 효과 원리 비교 분석
        """)

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
    with st.expander("📖 2026학년도 사곡고 2학기 2학년 역학과 에너지 교수학습 및 평가 운영 계획 원본 전문(수정본 PDF) 펼쳐보기", expanded=False):
        if HAS_PDF_VIEWER:
            pdf_viewer(str(pdf_path), width=850)
        else:
            base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("---")

# 6. 하단 가상실험 및 핵심 탐구 시뮬레이션 안내 (구글 드라이브 자료실 삭제 완료)
st.markdown("""
### 🔬 역학과 에너지 핵심 가상 실험실 및 시뮬레이션 안내
교과 수업 및 수행평가 탐구와 연계된 핵심 가상 실험실 시뮬레이션 목록입니다. 좌측 네비게이션 메뉴를 통해 직접 인터랙티브하게 실험을 조작하고 데이터를 분석할 수 있습니다.

| 영역 | 연계 탐구 및 시뮬레이션 안내 |
| :---: | :--- |
| **수행평가 ①** | • **[수행① 대비]** 포물선 운동 분석 및 역학적 에너지 보존 탐구 (독립성 수식 입증 및 오차 분석)<br>• **[수행① 대비]** 케플러 제3법칙 수학적 유도 및 실제 인공위성/ISS 궤도 데이터 분석<br>• **[수행① 대비]** 목표 궤도별 역학적 에너지 비교 및 다단 로켓 발사·궤도 전이 논증 |
| **핵심·심화 탐구** | • **[핵심 탐구]** 누리호 5차 발사 기반 다단·페어링 분리 및 운동량 보존 ([▶️ 관련 영상 보기](https://youtu.be/YeM0G_BEBzY))<br>• **[심화 탐구]** 일반 상대성 이론과 등가원리, 중력장 및 블랙홀 시뮬레이션 |
| **수행평가 ②** | • **[수행② 대비]** 정상파 공명 데이터 분석 및 관 경계 조건 기반 차내 음속 구하기<br>• **[수행② 대비]** 도플러 효과 파면 압축 모델링 및 긴급차량 상대 속도 역산 논증<br>• **[수행② 대비]** 음파의 중첩·간섭을 이용한 미래형 모빌리티 능동 소음 제어(ANC) 시스템 시뮬레이션 |

<div style="font-size: 12px; color: #64748b; margin-top: 8px;">제작: 사곡고등학교 물리실 · 담당교사 최연호</div>
""", unsafe_allow_html=True)
