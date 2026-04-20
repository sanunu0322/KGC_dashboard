import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="KGC 실시간 마케팅 대시보드", layout="wide")

# 1. 구글 스프레드시트 연결 설정
# 'url'에 실제 구글 시트 공유 링크를 입력하세요.
sheet_url = "https://docs.google.com/spreadsheets/d/19WpZV_lJbBR_vV6DU5La-Qs8b1XIOqvr4yIx5d5w5cw/edit?gid=0#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

def validate_and_format(value):
    """데이터가 숫자형(실수/정수)인지 확인하고 아니면 'None' 반환"""
    try:
        # 데이터가 비어있거나 NaN인 경우 처리
        if pd.isna(value):
            return "None"
        # 숫자로 변환 시도
        float_val = float(value)
        return f"{float_val}%"
    except (ValueError, TypeError):
        # 숫자가 아닌 데이터(문자열 등)일 경우
        return "None"

try:
    # 시트 전체 데이터 가져오기 (헤더가 1행에 있다고 가정하면 A2, B2는 0번 인덱스 행)
    # 데이터가 헤더 없이 시작한다면 header=None 옵션을 고려해야 함
    df = conn.read(spreadsheet=sheet_url)
    
    # pandas 데이터프레임에서 A2는 첫 번째 행의 첫 번째 열, B2는 첫 번째 행의 두 번째 열
    # 만약 시트에 제목 행(헤더)이 있다면 iloc[0]이 2행이 됩니다.
    raw_a2 = df.iloc[0, 0]  # A2 데이터
    raw_b2 = df.iloc[0, 1]  # B2 데이터

    # 데이터 검증 실행
    metropolitan_val = validate_and_format(raw_a2)
    rural_val = validate_and_format(raw_b2)
    
except Exception as e:
    st.error("데이터 소스에 연결할 수 없습니다.")
    metropolitan_val = "None"
    rural_val = "None"

# --- UI 레이아웃 ---

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Noto Sans KR', sans-serif; background-color: #f8fafc; }
    .kgc-header { background: linear-gradient(135deg, #b91c1c 0%, #7f1d1d 100%); color: white; padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; }
    .card { background: white; padding: 1.5rem; border-radius: 1rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.1); text-align: center; }
    .metric-label { color: #64748b; font-size: 0.875rem; font-weight: 700; margin-bottom: 0.5rem; }
    .metric-value { color: #b91c1c; font-size: 2rem; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="kgc-header"><h1 style="margin:0; color:white;">주간 판매 실시간 모니터링</h1></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">수도권 판매</div>
        <div class="metric-value">{metropolitan_val}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">지방 판매</div>
        <div class="metric-value">{rural_val}</div>
    </div>
    """, unsafe_allow_html=True)
