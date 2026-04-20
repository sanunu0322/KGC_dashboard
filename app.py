import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="KGC 마케팅 전략 보고서", layout="wide")

# ---------------------------------------------------------
# [데이터 연결 섹션] 구글 스프레드시트 연동
# ---------------------------------------------------------

# 실제 구글 스프레드시트 공유 URL을 아래에 입력하세요.
# (공유 설정이 '링크가 있는 모든 사용자 - 뷰어' 이상이어야 합니다.)
SHEET_URL = "https://docs.google.com/spreadsheets/d/19WpZV_lJbBR_vV6DU5La-Qs8b1XIOqvr4yIx5d5w5cw/edit?gid=0#gid=0"

def get_live_data():
    try:
        # 연결 생성
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # 데이터를 읽어옵니다. (제목 줄이 있다고 가정하여 첫 번째 행이 헤더가 됩니다)
        # 헤더가 1행이면, iloc[0]은 실제 시트의 2행이 됩니다.
        df = conn.read(spreadsheet=SHEET_URL, ttl="0") # 실시간 반영을 위해 캐시 ttl을 0으로 설정
        
        # A2는 0행 0열(첫 행의 첫 열), B2는 0행 1열(첫 행의 두 번째 열)
        raw_a2 = df.iloc[0, 0]
        raw_b2 = df.iloc[0, 1]
        
        # 데이터 타입 검증 함수 (실수형/정수형 확인)
        def validate(val):
            try:
                # 숫자로 변환 가능하면 수치 반환
                return float(val)
            except (ValueError, TypeError):
                # 숫자가 아니면 None 반환
                return None

        clean_a2 = validate(raw_a2)
        clean_b2 = validate(raw_b2)
        
        return clean_a2, clean_b2
    except Exception as e:
        return None, None

# 데이터 가져오기
val_a2, val_b2 = get_live_data()

# 화면 표시용 텍스트 변환
display_a2 = f"{val_a2}%" if val_a2 is not None else "None"
display_b2 = f"{val_b2}%" if val_b2 is not None else "None"

# ---------------------------------------------------------
# [UI 섹션] 기존 디자인 코드
# ---------------------------------------------------------

# CSS 스타일 정의
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans KR', sans-serif;
        background-color: #f8fafc;
    }
    .kgc-header {
        background: linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%);
        color: white; padding: 2rem; border-radius: 1rem; margin-bottom: 2rem;
    }
    .card {
        background: white; padding: 1.5rem; border-radius: 1rem;
        border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .metric-value { color: #b91c1c; font-size: 1.875rem; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("""
<div class="kgc-header">
    <h1 style="margin:0; color:white;">주간 마케팅 통찰 보고서</h1>
    <p style="margin:0.5rem 0 0 0; opacity:0.9;">2026년 3월 4주차 | 브랜드 전략실 마케팅 팀장</p>
</div>
""", unsafe_allow_html=True)

# KPI 카드 섹션 (수도권, 지방 데이터 변수 적용)
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("수도권 판매", display_a2, "실시간 데이터", "#10b981"),
    ("지방 판매", display_b2, "실시간 데이터", "#ef4444"),
    ("2030 비중", "45%", "● 타겟 도달", "#3b82f6"),
    ("아웃도어", "+30%", "▲ 트렌드 확산", "#f59e0b")
]

for i, col in enumerate([c1, c2, c3, c4]):
    with col:
        st.markdown(f"""
        <div class="card">
            <div style="color:#64748b; font-size:0.875rem;">{metrics[i][0]}</div>
            <div class="metric-value">{metrics[i][1]}</div>
            <div style="color:{metrics[i][3]}; font-size:0.75rem;">{metrics[i][2]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 상세 내용 및 차트 섹션
l, r = st.columns([1, 1])

with l:
    st.markdown("""
    <div class="card" style="min-height: 450px;">
        <h3 style="margin-top:0;">팀장 전략 제언</h3>
        <ul style="line-height:2.0; color:#475569; font-size:1rem;">
            <li><b>채널 전략:</b> 수도권 편의점의 성공 모델을 전국 거점 도시로 확산하십시오.</li>
            <li><b>아웃도어 마케팅:</b> 테니스/등산 연계 기획세트 출시를 즉시 추진하십시오.</li>
            <li><b>품질 관리:</b> 패키징 개봉 관련 VOC 해결을 위해 공정 개선을 요청했습니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with r:
    chart_html = """
    <div style="background:white; padding:1.5rem; border-radius:1rem; border:1px solid #e2e8f0; min-height:450px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <h4 style="margin-bottom:1rem; color:#1e293b;">구매 고객 연령대</h4>
        <div style="width:100%; height:300px;"><canvas id="kgcChart"></canvas></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const ctx = document.getElementById('kgcChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['2030대', '4050대', '기타'],
                datasets: [{
                    data: [45, 35, 20],
                    backgroundColor: ['#b91c1c', '#334155', '#e2e8f0'],
                    borderWidth: 0
                }]
            },
            options: {
                plugins: { legend: { position: 'bottom' } },
                maintainAspectRatio: false,
                cutout: '70%'
            }
        });
    </script>
    """
    components.html(chart_html, height=470)
