Bash
pip install streamlit yfinance pandas plotly
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="글로벌 시총 Top 10 주식 대시보드",
    page_icon="📈",
    layout="wide"
)

# 타이틀 구성
st.title("🌐 글로벌 시가총액 Top 10 주식 대시보드")
st.markdown("""
이 대시보드는 **야후 파이낸스(yfinance)**와 **Plotly**를 활용하여 현재 세계를 선도하는 시가총액 상위 10개 기업의 최근 1개년 주가 데이터를 시각화합니다.
""")

# 2. 글로벌 Top 10 기업 정의 (2026년 시총 기준 리스트)
COMPANIES = {
    'NVIDIA (NVDA)': 'NVDA',
    'Apple (AAPL)': 'AAPL',
    'Alphabet (GOOGL)': 'GOOGL',
    'Microsoft (MSFT)': 'MSFT',
    'Amazon (AMZN)': 'AMZN',
    'TSMC (TSM)': 'TSM',
    'Broadcom (AVGO)': 'AVGO',
    'Tesla (TSLA)': 'TSLA',
    'Meta (META)': 'META',
    'Berkshire Hathaway (BRK-B)': 'BRK-B'
}

# 3. 사이드바 컨트롤러 구성
st.sidebar.header("⚙️ 대시보드 설정 변수")

# 시각화 테마 선택 기능
theme_choice = st.sidebar.radio("🎨 차트 테마 선택", ["Light Mode", "Dark Mode"])
plot_theme = "plotly_white" if theme_choice == "Light Mode" else "plotly_dark"

# 분석 기간 계산 (최근 1년)
end_date = datetime.now()
start_date = end_date - timedelta(days=365)

# 다중 기업 선택 툴
selected_names = st.sidebar.multiselect(
    "비교 분석할 기업을 선택하세요:",
    options=list(COMPANIES.keys()),
    default=list(COMPANIES.keys())
)

# 4. 안전한 데이터 로딩 함수 (캐싱 처리)
@st.cache_data(show_spinner="야후 파이낸스에서 데이터를 불러오는 중입니다...")
def load_stock_data(companies_dict, start, end):
    all_history = {}
    close_prices = pd.DataFrame()
    
    for name, ticker in companies_dict.items():
        try:
            df = yf.download(ticker, start=start, end=end)
            if not df.empty:
                # yfinance 버전에 따른 MultiIndex 구조 컬럼 단일화 보정
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.get_level_values(0)
                df = df.loc[:, ~df.columns.duplicated()]
                
                # 종가(Close) 데이터 안전하게 추출 후 병합
                close_series = df['Close'].squeeze()
                close_series.name = name
                
                close_prices = pd.concat([close_prices, close_series], axis=1)
                all_history[name] = df
        except Exception as e:
            st.error(f"{name} ({ticker}) 데이터 로드 실패: {e}")
            
    # 날짜 공백 데이터 전방 직전 값으로 채움 (결측치 방지)
    if not close_prices.empty:
        close_prices = close_prices.ffill()
        
    return close_prices, all_history

# 5. 메인 대시보드 렌더링 로직
if selected_names:
    # 선택된 기업 딕셔너리 필터링
    selected_dict = {name: COMPANIES[name] for name in selected_names}
    df_close, all_history = load_stock_data(selected_dict, start_date, end_date)
    
    if not df_close.empty:
        # ----------------------------------------------------
        # 차트 1: 1개년 누적 수익률 비교 (정규화 차트)
        # ----------------------------------------------------
        st.subheader("📊 1개년 누적 수익률 비교 (%)")
        st.caption("💡 각 주식의 시작 가격이 다르므로, 1년 전 첫 거래일의 주가를 0%로 정렬하여 등락률을 비교합니다.")
        
        # 첫 거래일 기준 수익률 변환
        df_returns = (df_close / df_close.iloc[0] - 1) * 100
        
        fig_returns = px.line(
            df_returns,
            x=df_returns.index,
            y=df_returns.columns,
            labels={'value': '누적 수익률 (%)', 'Date': '날짜', 'variable': '기업명'},
            title="선택 기업 1개년 누적 수익률 추이"
        )
        fig_returns.update_layout(
            hovermode="x unified",
            xaxis_title="날짜",
            yaxis_title="수익률 (%)",
            template=plot_theme
        )
        st.plotly_chart(fig_returns, use_container_width=True)
        
        # ----------------------------------------------------
        # 차트 2: 개별 기업 상세 분석 (캔들스틱 및 메트릭)
        # ----------------------------------------------------
        st.markdown("---")
        st.subheader("🔍 개별 기업 상세 주가 및 지표")
        
        detail_name = st.selectbox("상세히 살펴볼 기업을 선택하세요:", options=selected_names)
        
        if detail_name in all_history:
            df_detail = all_history[detail_name]
            ticker_symbol = COMPANIES[detail_name]
            
            # 주요 메트릭 지표 연산
            last_close = float(df_detail['Close'].iloc[-1])
            first_close = float(df_detail['Close'].iloc[0])
            highest_price = float(df_detail['High'].max())
            lowest_price = float(df_detail['Low'].min())
            total_return = ((last_close - first_close) / first_close) * 100
            
            # 상단 메트릭 박스 배치
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            m_col1.metric("최근 종가", f"${last_close:,.2f}")
            m_col2.metric("1년 전 종가", f"${first_close:,.2f}")
            m_col3.metric("1년 최고 / 최저가", f"${highest_price:,.2f} / ${lowest_price:,.2f}")
            m_col4.metric("1년간 총 변동률", f"{total_return:+.2f}%")
            
            # 캔들스틱 차트 생성
            fig_candle = go.Figure(data=[go.Candlestick(
                x=df_detail.index,
                open=df_detail['Open'],
                high=df_detail['High'],
                low=df_detail['Low'],
                close=df_detail['Close'],
                increasing_line_color='#26a69a', # 상승캔들 색상
                decreasing_line_color='#ef5350'  # 하락캔들 색상
            )])
            
            fig_candle.update_layout(
                title=f"{detail_name} ({ticker_symbol}) 1개년 상세 캔들스틱 차트",
                xaxis_title="날짜",
                yaxis_title="주가 (USD)",
                xaxis_rangeslider_visible=False,
                template=plot_theme
            )
            st.plotly_chart(fig_candle, use_container_width=True)
            
    else:
        st.error("데이터를 가져오는 데 실패했습니다.")
else:
    st.warning("⚠️ 하나 이상의 기업을 선택하셔야 차트가 활성화됩니다.")
