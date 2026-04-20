# 1. 환경 정리 및 라이브러리 설치
import urllib.request
import os

print("환경 초기화 및 필수 라이브러리 설치 중...")
get_ipython().system('pip install -q streamlit')
get_ipython().system('npm install -g localtunnel')
get_ipython().system('fuser -k 8501/tcp') # 기존 포트 강제 종료

# 2. app.py 파일 생성
# 들여쓰기 에러를 방지하기 위해 텍스트 파일로 직접 기록합니다.
with open('app.py', 'w', encoding='utf-8') as f:
    f.write('''
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="KGC 마케팅 전략 보고서", layout="wide")

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

st.markdown("""
<div class="kgc-header">
    <h1 style="margin:0;">주간 마케팅 통찰 보고서</h1>
    <p style="margin:0.5rem 0 0 0; opacity:0.9;">2026년 3월 4주차 | 브랜드 전략실 마케팅 팀장</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("수도권 판매", "+15%", "▲ 편의점 강세", "#10b981"),
    ("지방 판매", "-2%", "▼ 마트 정체", "#ef4444"),
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
l, r = st.columns([1, 1])

with l:
    st.markdown("""
    <div class="card" style="min-height: 450px;">
        <h3 style="margin-top:0;">팀장 전략 제언</h3>
        <ul style="line-height:1.8; color:#475569;">
            <li><b>채널 전략:</b> 수도권 편의점의 성공 모델을 전국 거점 도시로 확산하십시오.</li>
            <li><b>아웃도어 마케팅:</b> 테니스/등산 연계 기획세트 출시를 즉시 추진하십시오.</li>
            <li><b>품질 관리:</b> 패키징 개봉 관련 VOC 해결을 위해 공정 개선을 요청했습니다.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with r:
    chart_html = \"\"\"
    <div class="card" style="min-height: 450px; display:flex; flex-direction:column; align-items:center; justify-content:center;">
        <h4 style="margin-bottom:1rem;">구매 고객 연령대</h4>
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
    \"\"\"
    components.html(chart_html, height=470)
''')

# 3. 접속 정보 확인 및 실행
ip = urllib.request.urlopen('https://ipv4.icanhazip.com').read().decode('utf8').strip()
print("\n" + "="*60)
print(f"1. 복사할 IP 주소 (Password): {ip}")
print("2. 잠시 후 나타나는 '...loca.lt' 링크를 클릭하세요.")
print("3. 접속 후 'TypeError' 발생 시 브라우저를 새로고침(F5) 하세요.")
print("="*60 + "\n")

# 실행
get_ipython().system('streamlit run app.py --server.port 8501 --server.address 0.0.0.0 & npx localtunnel --port 8501')
