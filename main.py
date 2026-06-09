import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 교육 탐색기",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 각 MBTI별 특성, 이모지, 테마 컬러, 추천 직업 데이터를 정의합니다.
MBTI_DATA = {
    "INTJ": {
        "name": "용의주도한 전략가",
        "emojis": "🧠 ♟️ 🌌 🦉",
        "color": "#6B21A8", # Purple
        "bg_color": "#F3E8FF",
        "desc": "독창적인 아이디어와 논리적인 사고를 바탕으로 시스템을 설계하고 문제를 해결하는 데 탁월합니다.",
        "careers": [
            {"title": "경영 컨설턴트", "reason": "복잡한 비즈니스 문제를 분석하고 전략적인 해결책을 제시하는 능력이 뛰어납니다."},
            {"title": "소프트웨어 아키텍트", "reason": "전체적인 시스템 구조를 설계하고 논리적인 흐름을 만들어내는 데 적합합니다."},
            {"title": "데이터 과학자", "reason": "방대한 데이터 속에서 패턴을 찾아내고 미래를 예측하는 일에 흥미를 느낍니다."}
        ]
    },
    "INTP": {
        "name": "논리적인 사색가",
        "emojis": "🔬 💻 🧩 🧪",
        "color": "#4338CA", # Indigo
        "bg_color": "#E0E7FF",
        "desc": "지적 호기심이 많고, 복잡한 이론이나 원리를 파악하고 분석하는 것을 즐깁니다.",
        "careers": [
            {"title": "연구원 (과학/기술)", "reason": "새로운 지식을 탐구하고 깊이 있는 연구를 수행하는 환경에서 빛을 발합니다."},
            {"title": "프로그래머", "reason": "논리적인 코드를 작성하고 버그를 해결하는 과정에서 지적 성취감을 얻습니다."},
            {"title": "대학교수", "reason": "자신의 전문 분야를 깊이 연구하고 지식을 전달하는 일에 적합합니다."}
        ]
    },
    "ENTJ": {
        "name": "대담한 통솔자",
        "emojis": "👑 📈 🚀 🦁",
        "color": "#BE185D", # Pink/Red
        "bg_color": "#FCE7F3",
        "desc": "뛰어난 리더십과 결단력을 갖추고 있으며, 조직을 효율적으로 이끌어 목표를 달성합니다.",
        "careers": [
            {"title": "기업 임원 (CEO, 디렉터)", "reason": "큰 그림을 보고 조직의 방향성을 설정하며 사람들을 이끄는 능력이 탁월합니다."},
            {"title": "변호사", "reason": "논리적인 논쟁을 즐기고 목표 달성을 위해 치밀하게 전략을 세웁니다."},
            {"title": "프로젝트 매니저", "reason": "자원과 인력을 효율적으로 분배하여 프로젝트를 성공적으로 완수합니다."}
        ]
    },
    "ENTP": {
        "name": "뜨거운 논쟁을 즐기는 변론가",
        "emojis": "💡 🎭 🌪️ 🎙️",
        "color": "#C2410C", # Orange
        "bg_color": "#FFEDD5",
        "desc": "끊임없이 새로운 아이디어를 제안하고, 틀에 얽매이지 않는 창의적인 사고를 합니다.",
        "careers": [
            {"title": "발명가 / 기획자", "reason": "기존의 방식을 뒤집는 혁신적인 아이디어를 구안하는 데 천부적인 재능이 있습니다."},
            {"title": "마케팅 디렉터", "reason": "트렌드를 빠르게 읽고 사람들의 이목을 끄는 기발한 캠페인을 기획합니다."},
            {"title": "정치인 / 외교관", "reason": "협상과 토론에 능하며, 다양한 가능성을 열어두고 타협점을 찾습니다."}
        ]
    },
    "INFJ": {
        "name": "선의의 옹호자",
        "emojis": "🕊️ 🔮 📖 🌿",
        "color": "#0D9488", # Teal
        "bg_color": "#CCFBF1",
        "desc": "깊은 통찰력과 이상주의적인 성향을 가지며, 타인의 성장을 돕는 일에서 의미를 찾습니다.",
        "careers": [
            {"title": "심리 상담사", "reason": "타인의 감정에 깊이 공감하고 내면의 상처를 치유하는 데 탁월한 능력이 있습니다."},
            {"title": "작가", "reason": "풍부한 상상력과 인간 본성에 대한 통찰을 글이나 예술로 표현하는 것을 즐깁니다."},
            {"title": "비영리 단체 활동가", "reason": "자신의 이상과 가치관을 실현하며 사회에 긍정적인 영향을 미치고 싶어 합니다."}
        ]
    },
    "INFP": {
        "name": "열정적인 중재자",
        "emojis": "🌸 🎨 ☁️ 🦄",
        "color": "#059669", # Emerald
        "bg_color": "#D1FAE5",
        "desc": "자신만의 뚜렷한 가치관을 가지고 있으며, 예술적이고 창의적인 방법으로 자신을 표현합니다.",
        "careers": [
            {"title": "일러스트레이터 / 디자이너", "reason": "자신만의 독특한 감성과 상상력을 시각적으로 표현하는 데 능합니다."},
            {"title": "순수 예술가 / 시인", "reason": "내면의 깊은 감정과 가치를 예술 작품으로 승화시키는 것을 좋아합니다."},
            {"title": "특수교사", "reason": "따뜻한 마음으로 소외되거나 도움이 필요한 사람들의 성장을 진심으로 돕습니다."}
        ]
    },
    "ENFJ": {
        "name": "정의로운 사회운동가",
        "emojis": "🤝 🌟 🗣️ 🌻",
        "color": "#B45309", # Amber
        "bg_color": "#FEF3C7",
        "desc": "카리스마와 이타심을 겸비하여, 사람들을 동기부여하고 긍정적인 변화를 이끌어냅니다.",
        "careers": [
            {"title": "교사 / 교육자", "reason": "학생들의 잠재력을 발견하고 그들이 성장할 수 있도록 열정적으로 지도합니다."},
            {"title": "인사(HR) 관리자", "reason": "조직 내 사람들의 화합을 도모하고 개개인의 능력을 최대한 발휘하도록 돕습니다."},
            {"title": "홍보(PR) 전문가", "reason": "뛰어난 의사소통 능력으로 대중의 마음을 움직이고 긍정적인 이미지를 구축합니다."}
        ]
    },
    "ENFP": {
        "name": "재기발랄한 활동가",
        "emojis": "🎉 🌈 🚀 🦋",
        "color": "#E11D48", # Rose
        "bg_color": "#FFE4E6",
        "desc": "자유로운 영혼의 소유자로, 새로운 가능성을 탐험하고 사람들과 소통하는 것을 사랑합니다.",
        "careers": [
            {"title": "이벤트 기획자", "reason": "사람들에게 즐거움을 주는 새롭고 흥미로운 행사를 기획하고 실행하는 것을 즐깁니다."},
            {"title": "콘텐츠 크리에이터", "reason": "통통 튀는 아이디어로 대중과 소통하며 트렌드를 만들어갑니다."},
            {"title": "여행 가이드", "reason": "새로운 문화를 경험하고 낯선 사람들과 교류하며 에너지를 얻습니다."}
        ]
    },
    "ISTJ": {
        "name": "청렴결백한 논리주의자",
        "emojis": "📋 🏛️ 🔍 ⚖️",
        "color": "#1D4ED8", # Blue
        "bg_color": "#DBEAFE",
        "desc": "책임감이 강하고 꼼꼼하며, 규칙과 질서를 중요하게 여기는 신뢰할 수 있는 성격입니다.",
        "careers": [
            {"title": "회계사 / 재무 관리자", "reason": "숫자를 정확하게 다루고 세부적인 규칙을 준수하는 능력이 뛰어납니다."},
            {"title": "데이터베이스 관리자", "reason": "정보를 체계적으로 정리하고 시스템을 안정적으로 유지하는 데 적합합니다."},
            {"title": "공무원 / 행정직", "reason": "주어진 절차와 규정을 엄격히 따르며 사회적 책임을 다하는 것을 중요시합니다."}
        ]
    },
    "ISFJ": {
        "name": "용감한 수호자",
        "emojis": "🛡️ 🩺 🧸 🍵",
        "color": "#0369A1", # Sky Blue
        "bg_color": "#E0F2FE",
        "desc": "헌신적이고 따뜻한 마음을 가졌으며, 주변 사람들을 세심하게 챙기고 보호합니다.",
        "careers": [
            {"title": "간호사 / 의료 종사자", "reason": "아픈 사람들을 정성껏 돌보고 실질적인 도움을 제공하는 데서 큰 보람을 느낍니다."},
            {"title": "유치원 교사", "reason": "아이들에게 따뜻한 애정을 베풀고 안전한 환경에서 성장하도록 돕습니다."},
            {"title": "사회복지사", "reason": "지역 사회의 어려운 이웃들에게 공감하며 그들의 삶의 질을 개선하기 위해 노력합니다."}
        ]
    },
    "ESTJ": {
        "name": "엄격한 관리자",
        "emojis": "👔 📊 🏢 ⏱️",
        "color": "#334155", # Slate
        "bg_color": "#F1F5F9",
        "desc": "현실적이고 실용적이며, 사람과 사물을 효율적으로 조직하고 관리하는 능력이 탁월합니다.",
        "careers": [
            {"title": "경영자 / 총괄 매니저", "reason": "명확한 목표를 세우고 체계적인 시스템을 통해 조직을 효율적으로 운영합니다."},
            {"title": "판사 / 법조인", "reason": "객관적인 사실과 규칙에 근거하여 공정하게 판단하고 결정을 내립니다."},
            {"title": "경찰 / 군 장교", "reason": "질서를 유지하고 규범을 수호하며 강한 책임감으로 임무를 수행합니다."}
        ]
    },
    "ESFJ": {
        "name": "사교적인 외교관",
        "emojis": "🎈 🧁 🏡 🎀",
        "color": "#DB2777", # Pink
        "bg_color": "#FCE7F3",
        "desc": "친절하고 사교적이며, 타인을 배려하고 협력적인 환경을 만드는 데 재능이 있습니다.",
        "careers": [
            {"title": "고객 서비스 관리자", "reason": "사람들의 요구사항에 귀 기울이고 친절하게 문제를 해결해 주는 것을 즐깁니다."},
            {"title": "웨딩 플래너", "reason": "타인의 특별한 날을 섬세하게 기획하고 조율하여 기쁨을 선사합니다."},
            {"title": "의료 행정 관리자", "reason": "병원의 원활한 운영을 돕고 환자들에게 편안한 환경을 제공하는 데 기여합니다."}
        ]
    },
    "ISTP": {
        "name": "만능 재주꾼",
        "emojis": "🛠️ 🏍️ ⚙️ 🧭",
        "color": "#4B5563", # Gray
        "bg_color": "#F3F4F6",
        "desc": "상황 적응력이 뛰어나고, 도구를 다루거나 문제를 실용적으로 해결하는 데 관심이 많습니다.",
        "careers": [
            {"title": "기계 공학자 / 정비사", "reason": "기계의 작동 원리를 파악하고 도구를 능숙하게 다루어 문제를 해결합니다."},
            {"title": "응급구조사", "reason": "위기 상황에서 침착하고 빠르게 판단하여 실질적인 조치를 취합니다."},
            {"title": "소프트웨어 테스터", "reason": "시스템의 결함을 논리적으로 찾아내고 효율적인 해결책을 실험하는 것을 좋아합니다."}
        ]
    },
    "ISFP": {
        "name": "호기심 많은 예술가",
        "emojis": "🖌️ 🎸 🌿 🏕️",
        "color": "#65A30D", # Lime
        "bg_color": "#ECFCCB",
        "desc": "온화하고 감각적이며, 현재의 순간을 즐기고 아름다움을 탐구하는 미적 감각이 뛰어납니다.",
        "careers": [
            {"title": "패션 디자이너", "reason": "자신만의 감각적인 스타일과 색채 감각을 시각적으로 아름답게 구현합니다."},
            {"title": "음악가 / 연주자", "reason": "풍부한 감수성을 소리나 리듬을 통해 예술적으로 표현하는 데 재능이 있습니다."},
            {"title": "수의사 / 사육사", "reason": "동물 및 자연과 깊이 교감하며 부드럽고 섬세하게 그들을 돌봅니다."}
        ]
    },
    "ESTP": {
        "name": "모험을 즐기는 사업가",
        "emojis": "⚡ 🏎️ 🏄‍♂️ 💸",
        "color": "#DC2626", # Red
        "bg_color": "#FEE2E2",
        "desc": "에너지가 넘치고 행동 지향적이며, 짜릿한 스릴과 위험을 감수하는 것을 두려워하지 않습니다.",
        "careers": [
            {"title": "기업가 / 스타트업 창업", "reason": "빠르게 변화하는 환경에서 위험을 감수하고 기회를 포착하여 행동으로 옮깁니다."},
            {"title": "영업 사원", "reason": "타고난 설득력과 매력으로 사람들과 소통하며 빠른 시간 내에 성과를 냅니다."},
            {"title": "스포츠 코치 / 운동선수", "reason": "신체적인 활동을 즐기며 경쟁적인 환경에서 뛰어난 적응력과 승부욕을 발휘합니다."}
        ]
    },
    "ESFP": {
        "name": "자유로운 영혼의 연예인",
        "emojis": "🎤 🕺 ✨ 🍹",
        "color": "#D946EF", # Fuchsia
        "bg_color": "#FAEEFF",
        "desc": "주변에 에너지를 불어넣는 분위기 메이커로, 사람들의 관심을 즐기고 열정적으로 살아갑니다.",
        "careers": [
            {"title": "배우 / 연예인", "reason": "무대 위에서 스포트라이트를 받으며 타고난 끼와 매력을 마음껏 발산합니다."},
            {"title": "승무원", "reason": "다양한 사람들과 즐겁게 소통하고 친절한 서비스를 제공하며 에너지를 얻습니다."},
            {"title": "레크리에이션 강사", "reason": "사람들을 웃게 만들고 긍정적인 에너지를 전달하며 즐거운 분위기를 주도합니다."}
        ]
    }
}

def get_custom_style(color, bg_color):
    """선택한 MBTI의 테마 컬러에 맞게 UI 스타일을 동적으로 생성하는 함수"""
    style = f"""
    <style>
        /* 메인 제목 색상 변경 */
        .mbti-title {{
            color: {color};
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }}
        /* 서브 텍스트 설명 */
        .mbti-desc {{
            font-size: 1.2rem;
            color: #4B5563;
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: {bg_color};
            border-radius: 15px;
            border: 2px dashed {color};
        }}
        /* 추천 직업 카드 스타일 */
        .career-card {{
            background-color: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            margin-bottom: 20px;
            border-left: 8px solid {color};
            transition: transform 0.2s ease-in-out;
        }}
        .career-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }}
        .career-title {{
            color: {color};
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .career-reason {{
            color: #374151;
            font-size: 1.1rem;
            line-height: 1.6;
        }}
    </style>
    """
    return style

st.markdown("<h1 style='text-align: center;'>✨ 나의 MBTI 진로 탐색기 ✨</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: gray;'>나의 성향에 딱 맞는 미래 직업은 무엇일까요? 아래에서 MBTI를 선택해보세요!</p>", unsafe_allow_html=True)
st.divider()

# 화면 분할: 왼쪽은 선택, 오른쪽은 결과
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🔍 MBTI 선택")
    
    # 4가지 지표를 설명해주는 교육용 아코디언 메뉴
    with st.expander("MBTI 알파벳의 의미가 궁금하다면?"):
        st.markdown("""
        * **E (외향) / I (내향)**: 에너지의 방향
        * **S (감각) / N (직관)**: 정보 수집 방식
        * **T (사고) / F (감정)**: 의사결정 방식
        * **J (판단) / P (인식)**: 생활 양식
        """)
    
    # MBTI 드롭다운 메뉴
    mbti_options = list(MBTI_DATA.keys())
    selected_mbti = st.selectbox("당신의 MBTI를 골라주세요!", mbti_options, index=0)
    
    # 재미 요소: 랜덤 선택 버튼 (선택 사항)
    if st.button("🎲 내 MBTI 다시 검사하러 가기"):
        st.link_button("무료 성격유형 검사", "https://www.16personalities.com/ko")

with col2:
    # 선택된 MBTI의 데이터 불러오기
    data = MBTI_DATA[selected_mbti]
    
    # 동적 CSS 스타일 적용
    st.markdown(get_custom_style(data["color"], data["bg_color"]), unsafe_allow_html=True)
    
    # MBTI 타이틀 및 이모지 출력
    st.markdown(f"<div class='mbti-title'>{data['emojis']} {selected_mbti} : {data['name']}</div>", unsafe_allow_html=True)
    
    # 성향 설명 출력
    st.markdown(f"<div class='mbti-desc'><strong>{selected_mbti}의 특징:</strong><br><br>{data['desc']}</div>", unsafe_allow_html=True)
    
    # 추천 직업 섹션 헤더
    st.subheader(f"💼 {selected_mbti}에게 추천하는 찰떡 직업 베스트 3")
    
    # 추천 직업 카드 HTML 생성 및 출력
    for career in data['careers']:
        card_html = f"""
        <div class="career-card">
            <div class="career-title">✨ {career['title']}</div>
            <div class="career-reason">{career['reason']}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px;'>
    <strong>💡 팁:</strong> MBTI는 나를 알아가는 여러 도구 중 하나일 뿐입니다. 가장 중요한 것은 본인의 진짜 관심사와 열정이라는 것을 잊지 마세요! 화이팅! 🚀
</div>
""", unsafe_allow_html=True)
