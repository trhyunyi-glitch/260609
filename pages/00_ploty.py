import streamlit as st
import requests
import tempfile
import os

# FPDF 임포트 에러 방지를 위한 안전한 로드 패턴
try:
    from fpdf import FPDF
    FPDF_AVAILABLE = True
except ModuleNotFoundError:
    FPDF_AVAILABLE = False

# Page Configuration
st.set_page_config(
    page_title="MBTI 진로 탐색 가이드",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------------
# CONSTANTS & DATA DEFINITIONS
# -------------------------------------------------------------------------

# MBTI 유형별 맞춤형 진로 데이터 및 이모지 스타일링
MBTI_DATA = {
    "ISTJ": {
        "emoji": "💼📏🔍📁",
        "title": "청렴결백한 논리주의자 (The Inspector)",
        "desc": "사실에 근거하여 사고하며, 행동이나 결정에 일관성이 있고 신뢰할 수 있는 사람입니다. 체계적이고 조직적인 환경에서 뛰어난 능력을 발휘합니다.",
        "bg_color": "#F3F4F6", # 차분한 그레이
        "accent_color": "#374151",
        "strengths": ["높은 책임감", "정확성과 철저함", "조직 및 규칙 준수", "현실적인 문제 해결력"],
        "careers": [
            {"name": "회계사 / 세무사", "reason": "숫자와 세부 명세의 정확성을 요구하는 직무에 최적화되어 있습니다."},
            {"name": "법률 전문가 (판사, 변무사)", "reason": "법률과 규정을 정확히 해석하고 공정하게 적용하는 일에 능숙합니다."},
            {"name": "시스템 분석가", "reason": "정보를 구조화하고 체계적인 데이터 분석을 통해 시스템을 안정화합니다."},
            {"name": "공무원 / 군장교", "reason": "명확한 체계 속에서 국가나 조직의 규칙을 준수하며 안정적으로 과업을 수행합니다."}
        ]
    },
    "ISFJ": {
        "emoji": "🌸🛡️🧸🩹",
        "title": "용감한 수호자 (The Defender)",
        "desc": "조용하고 차분하며 온화한 성품을 가졌습니다. 타인을 보호하고 돕는 일에 헌신적이며, 세심하게 사람들을 챙깁니다.",
        "bg_color": "#FDF2F8", # 따뜻한 핑크베이지
        "accent_color": "#BE185D",
        "strengths": ["세심한 관찰력", "헌신과 봉사 정신", "안정적인 지원 역량", "협조적인 태도"],
        "careers": [
            {"name": "간호사 / 의료 지원가", "reason": "환자의 세밀한 변화를 감지하고 따뜻하고 헌신적인 돌봄을 제공합니다."},
            {"name": "초등교사 / 보육교사", "reason": "아이들의 성장을 세심히 관찰하고 체계적이고 따뜻하게 지도합니다."},
            {"name": "사회복지사", "reason": "어려운 이웃의 현실적인 필요를 파악하고 꼼꼼하게 서비스를 연계합니다."},
            {"name": "인사(HR) 및 교육 담당자", "reason": "조직 내 구성원들이 필요한 시스템과 환경을 세심하게 지원합니다."}
        ]
    },
    "INFJ": {
        "emoji": "🔮📜✨🍃",
        "title": "선의의 옹호자 (The Advocate)",
        "desc": "조용하고 신비로우며 샘솟는 영감을 지녔습니다. 깊은 통찰력과 강한 도덕적 관념을 바탕으로 더 나은 세상을 만들고자 조용히 헌신합니다.",
        "bg_color": "#EEF2F6", # 신비로운 연보라/그레이
        "accent_color": "#4F46E5",
        "strengths": ["깊은 통찰력", "강한 신념과 이상주의", "뛰어난 공감 능력", "독창적인 언어적 표현력"],
        "careers": [
            {"name": "상담 심리사 / 치료사", "reason": "타인의 내면적 아픔을 깊이 이해하고 통찰력 있는 해결책을 제시합니다."},
            {"name": "작가 / 소설가", "reason": "자신의 깊은 가치관และ 이상향을 글이라는 매체를 통해 세상에 전합니다."},
            {"name": "환경 / 인권 운동가", "reason": "인류와 환경을 위한 숭고한 대의를 위해 지속적이고 헌신적으로 활동합니다."},
            {"name": "진로 커리어 코치", "reason": "사람들의 잠재된 가능성을 발견하고 영감을 주어 올바른 길로 안내합니다."}
        ]
    },
    "INTJ": {
        "emoji": "🧠♟️🚀📐",
        "title": "용의주도한 전략가 (The Architect)",
        "desc": "상상력이 풍부하면서도 결정이 빠르고 단호합니다. 야망이 있지만 겉으로 드러내지 않으며, 호기심이 많지만 쓸데없는 일에 에너지를 낭비하지 않습니다.",
        "bg_color": "#ECFDF5", # 지적인 딥그린/에메랄드 토닝
        "accent_color": "#047857",
        "strengths": ["논리적 분석력", "장기적 전략 수립", "독립적인 주도성", "높은 기준의 목표 지향"],
        "careers": [
            {"name": "소프트웨어 아키텍트", "reason": "복잡한 시스템의 전체 구조를 설계하고 논리적으로 구현합니다."},
            {"name": "경영 컨설턴트", "reason": "기업의 문제점을 예리하게 진단하고 장기적인 비즈니스 돌파구를 제시합니다."},
            {"name": "투자 분석가 (애널리스트)", "reason": "시장의 거시적 흐름을 읽고 데이터 기반의 과학적 투자 모델을 설계합니다."},
            {"name": "연구원 / 과학자", "reason": "특정 분야의 이론적 깊이를 파고들며 혁신적인 기술과 이론을 발굴합니다."}
        ]
    },
    "ISTP": {
        "emoji": "🛠️🏎️⚙️🧗",
        "title": "만능 재주꾼 (The Virtuoso)",
        "desc": "대담하면서도 현실적인 성향으로 모든 종류의 도구를 자유자재로 다루는 장인형입니다. 관찰력이 뛰어나고 실용적인 문제 해결에 능합니다.",
        "bg_color": "#FFFBEB", # 실용적인 옐로우/베이지
        "accent_color": "#D97706",
        "strengths": ["임기응변과 순발력", "도구 및 기계 조작 능력", "침착한 상황 대처", "실용주의적 접근"],
        "careers": [
            {"name": "엔지니어 / 메카닉", "reason": "기계와 시스템의 원리를 이해하고 고장난 부분을 신속하게 분석·수리합니다."},
            {"name": "데이터 포렌식 전문가", "reason": "디지털 단서를 실증적으로 추적하고 문제를 냉철하게 해결합니다."},
            {"name": "파일럿 / 카레이서 / 소방관", "reason": "긴박하고 위험한 상황에서도 뛰어난 신체 감각과 침착함을 유지합니다."},
            {"name": "소프트웨어 개발자 (백엔드)", "reason": "코드를 통해 실질적인 작동 시스템을 만들고 디버깅하는 일에 보람을 느낍니다."}
        ]
    },
    "ISFP": {
        "emoji": "🎨🎸🐈🍃",
        "title": "호기심 많은 예술가 (The Adventurer)",
        "desc": "따뜻하고 감성이 풍부하며 겸손합니다. 삶의 순간순간을 조용히 즐기며, 예술적이고 미적인 가치를 중요시합니다.",
        "bg_color": "#FEF2F2", # 따스한 피치
        "accent_color": "#DC2626",
        "strengths": ["뛰어난 미적 감각", "온화하고 타인을 배려하는 성품", "자유로운 적응력", "현재에 집중하는 몰입력"],
        "careers": [
            {"name": "시각 / 인테리어 디자이너", "reason": "남다른 미적 감각과 색채 감각을 발휘하여 공간과 시각물을 아름답게 꾸밉니다."},
            {"name": "파티시에 / 요리사", "reason": "손끝의 감각을 살려 사람들에게 즉각적인 오감의 기쁨을 선사합니다."},
            {"name": "동물 사육사 / 원예가", "reason": "말 없는 자연과 동식물들과 깊이 교감하며 세심하게 돌봅니다."},
            {"name": "순수 미술가 / 음악가", "reason": "자신의 감정과 세상의 아름다움을 예술적 매체로 자유롭게 표현합니다."}
        ]
    },
    "INFP": {
        "emoji": "🌈🦄🌌✍️",
        "title": "열정적인 중재자 (The Mediator)",
        "desc": "상냥하고 이타적인 성품으로, 마음이 따뜻하고 개방적입니다. 자신만의 확고한 가치관과 이상향을 마음속 깊이 간직하고 있습니다.",
        "bg_color": "#FAF5FF", # 몽환적인 연보라
        "accent_color": "#7C3AED",
        "strengths": ["풍부한 상상력", "확고한 개인적 신념", "타인의 감정에 대한 깊은 공감", "창의적 표현력"],
        "careers": [
            {"name": "소설가 / 시인 / 웹툰 작가", "reason": "내면의 풍부한 상상력과 서사를 작품으로 탄생시킵니다."},
            {"name": "예술 치료사", "reason": "예술적 매체를 활용해 상처받은 마음을 따뜻하게 치유합니다."},
            {"name": "도서관 사서 / 아카이빙 전문가", "reason": "다양한 지식과 스토리 속에서 사색하며 체계적으로 정보를 보존합니다."},
            {"name": "비영리 단체 기획자", "reason": "인도주의적 신념을 실현하기 위한 캠페인과 사회공헌 활동을 기획합니다."}
        ]
    },
    "INTP": {
        "emoji": "🧪🔭💬🔬",
        "title": "논리적인 사색가 (The Logician)",
        "desc": "지적 호기심이 매우 강하며, 문제를 분석하는 새로운 시각을 끊임없이 찾아냅니다. 지식의 축적 자체를 순수하게 즐깁니다.",
        "bg_color": "#F0FDFA", # 지적인 민트그린
        "accent_color": "#0D9488",
        "strengths": ["논리적 분석 및 추론", "독창적 아이디어 구상", "객관적이고 냉철한 관점", "비판적 사고력"],
        "careers": [
            {"name": "학술 연구원 (물리학, 수학 등)", "reason": "세상의 작동 원리와 논리적 법칙을 순수하게 탐구합니다."},
            {"name": "인공지능 연구원", "reason": "복잡한 알고리즘을 설계하고 머신러닝 모델의 이론적 배경을 분석합니다."},
            {"name": "게임 기획자 / 시스템 개발자", "reason": "정밀한 규칙과 매커니즘이 설계되어야 하는 가상 세계를 설계합니다."},
            {"name": "전략 연구 분석가", "reason": "트렌드와 데이터를 입체적으로 조망해 새로운 인사이트와 가설을 도출합니다."}
        ]
    },
    "ESTP": {
        "emoji": "🔥🎯🎰📣",
        "title": "모험을 즐기는 사업가 (The Entrepreneur)",
        "desc": "주변에 지대한 영향을 주는 활력소 같은 존재입니다. 이론보다는 실천을 선호하며 직관력이 뛰어나고 즉각적인 해결책을 제시합니다.",
        "bg_color": "#FFF7ED", # 역동적인 오렌지
        "accent_color": "#EA580C",
        "strengths": ["에너지 넘치는 추진력", "뛰어난 위기 대처", "사교성과 네트워크 형성", "실제적인 타협 및 협상력"],
        "careers": [
            {"name": "비즈니스 개발자 / 창업가", "reason": "기회를 빠르게 포착하고 과감하게 실행하여 비즈니스를 개척합니다."},
            {"name": "스포츠 마케터 / 이벤트 기획자", "reason": "역동적인 활동과 대중과의 소통을 주도하며 생생한 에너지를 전파합니다."},
            {"name": "전문 영업가 (바이어)", "reason": "현장감 있는 대화 능력과 협상력으로 계약을 성사시킵니다."},
            {"name": "뉴스 현장 취재 기자", "reason": "긴박하게 변하는 현장에 직접 뛰어들어 사실을 역동적으로 취재합니다."}
        ]
    },
    "ESFP": {
        "emoji": "🎉🎤🕺💅",
        "title": "자유로운 영혼의 연예인 (The Entertainer)",
        "desc": "흥이 많고 즉흥적이며 에너지가 넘칩니다. 인생의 매 순간을 축제처럼 즐기고자 하며, 주변 사람들을 즐겁게 만드는 천부적인 재능이 있습니다.",
        "bg_color": "#FFF1F2", # 러블리한 핫핑크/레드베이지
        "accent_color": "#E11D48",
        "strengths": ["현장 분위기 메이커", "탁월한 표현력과 소통", "실용적인 수용력", "긍정적인 삶의 태도"],
        "careers": [
            {"name": "공연 예술가 / 배우 / 유튜버", "reason": "자신의 끼와 매력을 사람들에게 발산하고 즉각적인 피드백을 즐깁니다."},
            {"name": "레크리에이션 지도자 / 가이드", "reason": "여러 사람을 한마음으로 모으고 웃음 가득한 여정을 이끕니다."},
            {"name": "이벤트 프로듀서", "reason": "파티, 페스티벌 등 감각적이고 화려한 이벤트를 창의적으로 디자인합니다."},
            {"name": "고객 경험(CX) 컨설턴트", "reason": "고객의 기분을 빠르게 파악하고 기분 좋은 서비스를 유쾌하게 제공합니다."}
        ]
    },
    "ENFP": {
        "emoji": "🌟🎈🌻💬",
        "title": "재기발랄한 활동가 (The Campaigner)",
        "desc": "자유로운 영혼의 소유자입니다. 활기차고 다정다감하며 타인과 정서적으로 유대하는 능력이 뛰어나고 아이디어가 넘칩니다.",
        "bg_color": "#FAF5FF", # 창의적인 라이트퍼플
        "accent_color": "#9333EA",
        "strengths": ["무한한 아이디어 생성", "강한 친화력과 공감", "열정적인 동기부여가", "열린 마음"],
        "careers": [
            {"name": "크리에이티브 디렉터", "reason": "브랜드나 캠페인의 참신하고 감성적인 아이디어를 구상하고 지휘합니다."},
            {"name": "카피라이터 / 마케터", "reason": "사람들의 마음을 움직이는 톡톡 튀는 문구와 매력적인 스토리를 개발합니다."},
            {"name": "상담 교사 / 청소년 지도사", "reason": "학습자들에게 영감과 따뜻한 공감을 건네며 자아실현을 돕습니다."},
            {"name": "스타트업 초기 기획자", "reason": "새로운 비즈니스 컨셉을 유연하게 발굴하고 가치를 창조합니다."}
        ]
    },
    "ENTP": {
        "emoji": "💡🧩🎙️💣",
        "title": "뜨거운 논쟁을 즐기는 변론가 (The Debater)",
        "desc": "지적인 도전과 토론을 마다하지 않는 똑똑하고 호기심 많은 지식인형입니다. 기존 시스템의 맹점을 찾아내고 파괴적 혁신을 이끄는 것을 좋아합니다.",
        "bg_color": "#EFF6FF", # 역동적인 스카이블루
        "accent_color": "#2563EB",
        "strengths": ["뛰어난 두뇌 회전과 변론술", "새로운 솔루션 창출", "도전 정신", "고정관념 타파"],
        "careers": [
            {"name": "스타트업 창업가 / 벤처 빌더", "reason": "새로운 틈새시장을 분석해 혁신적이고 도전적인 사업을 기획합니다."},
            {"name": "전략 기획 전문가", "reason": "기존 구조를 허물고 미래지향적인 포지셔닝 전략을 과감하게 수립합니다."},
            {"name": "토론 방송 기획자 / 정치 분석가", "reason": "현안의 찬반 논점을 예리하게 파고들어 지적 흥미를 유발하는 판을 짭니다."},
            {"name": "R&D 기술 특허 변리사", "reason": "독창적인 아이디어와 기술의 논리적 독점성을 법적으로 설계합니다."}
        ]
    },
    "ESTJ": {
        "emoji": "👮📈🔨🏛️",
        "title": "엄격한 관리자 (The Executive)",
        "desc": "사물이나 사람을 관리하는 데 탁월한 재능이 있는 대표적인 지도자형입니다. 체계적이고 효율적인 업무 환경을 만들고 유지하는 능력이 독보적입니다.",
        "bg_color": "#F8FAFC", # 단단한 슬레이트 그레이
        "accent_color": "#475569",
        "strengths": ["체계적인 조직 관리 능력", "뛰어난 실행 및 행정력", "강한 리더십과 추진력", "현실적 타당성 분석"],
        "careers": [
            {"name": "대기업 운영 임원 / COO", "reason": "기업의 경영 프로세스를 정교하게 최적화하고 생산성을 최대화합니다."},
            {"name": "프로젝트 관리자 (PM)", "reason": "예산과 자원, 일정을 정확하게 제어하여 목표 기한 내 산출물을 만들어 냅니다."},
            {"name": "정책 수립 공무원", "reason": "국가나 부처의 실효성 높은 장기 마일스톤과 규정을 정립합니다."},
            {"name": "품질 관리 전문가 (QA)", "reason": "엄격한 공정 및 평가 규격에 맞춰 결함을 잡아내고 효율을 극대화합니다."}
        ]
    },
    "ESFJ": {
        "emoji": "🤝🍰🎈📞",
        "title": "사교적인 외교관 (The Consul)",
        "desc": "사람들을 향한 관심이 많고 사교적입니다. 조화로운 공동체를 지향하며, 타인에게 현실적이고 실질적인 도움을 주며 큰 행복을 느낍니다.",
        "bg_color": "#FEF3C7", # 따스한 골드/앰버
        "accent_color": "#D97706",
        "strengths": ["뛰어난 친화력과 배려", "조화로운 공동체 형성", "섬세한 고객 맞춤 케어", "책임감 있는 지원력"],
        "careers": [
            {"name": "호텔리어 / 고객 관계 매니저 (CRM)", "reason": "고객 한 사람 한 사람을 세심하고 정성껏 대우하며 환대합니다."},
            {"name": "초등·유아 교육자", "reason": "사랑과 온화한 성품으로 아이들이 바르게 사회화되도록 도우며 올바른 삶의 가치관을 이끕니다."},
            {"name": "홍보(PR) 대행사 전문가", "reason": "조직의 우호적인 이미지를 구축하고 고객사 및 미디어와 활발히 네트워킹합니다."},
            {"name": "임상 치료 코디네이터", "reason": "치료 전후의 과정에서 환자가 편안함을 느끼도록 세심히 일정을 조율하고 상담을 돕습니다."}
        ]
    },
    "ENFJ": {
        "emoji": "👑📣🌟🧭",
        "title": "정의로운 사회운동가 (The Protagonist)",
        "desc": "카리스마와 열정을 지닌 리더입니다. 공동체의 성장을 위해 타인을 고무하고 독려하며 선한 영향력을 전파하기 위해 끊임없이 솔선수범합니다.",
        "bg_color": "#FFFBEB", # 영감을 주는 따뜻한 골드베이지
        "accent_color": "#B45309",
        "strengths": ["뛰어난 리더십과 카리스마", "타인의 성장을 이끄는 동기부여", "명확한 비전 소통력", "포용성"],
        "careers": [
            {"name": "기업 인재 육성 전문가 (L&D)", "reason": "인재 개발 프로그램을 기획하여 조직원들의 커리어 성장을 이끕니다."},
            {"name": "시민 단체 대표 / 정치가", "reason": "더 나은 사회적 가치를 위해 시민들을 응집시키고 긍정적인 사회 운동을 주도합니다."},
            {"name": "동기부여 강사 / 인문학 교수", "reason": "풍부한 공감과 지식을 토대로 청중들의 지각을 깨우고 긍정적 영감을 줍니다."},
            {"name": "성공적인 프로젝트 디렉터", "reason": "다양한 배경을 가진 구성원들을 조화롭게 통솔하여 거대한 프로젝트를 성공으로 이끕니다."}
        ]
    },
    "ENTJ": {
        "emoji": "⚔️🦁📊🏛️",
        "title": "대담한 통솔자 (The Commander)",
        "desc": "단호하고 철저한 계획성으로 집단을 이끄는 리더십이 탁월합니다. 불가능해 보이는 일도 장기적인 목표와 치밀한 전략으로 달성해냅니다.",
        "bg_color": "#F1F5F9", # 권위 있는 슬레이트블루
        "accent_color": "#0F172A",
        "strengths": ["전략적 기획 및 통솔력", "목표 지향적 추진력", "효율성과 결단력", "장기적인 안목"],
        "careers": [
            {"name": "전문 경영인 (CEO)", "reason": "회사의 전략을 주도하고 막강한 의사결정력을 바탕으로 시장 지배력을 넓힙니다."},
            {"name": "글로벌 경영 컨설턴트", "reason": "경영의 비효율을 가차 없이 도려내고 미래 가치 중심의 구조 개편을 선도합니다."},
            {"name": "벤처 캐피탈리스트 (심사역)", "reason": "미래 산업의 게임 체인저가 될 혁신적 비즈니스를 감별하고 전략적으로 투자합니다."},
            {"name": "정부/정당 전략가", "reason": "장기적 국가 정책과 선거 캠페인의 전반적 메인 프레임을 단단하게 설계합니다."}
        ]
    }
}

# -------------------------------------------------------------------------
# PDF GENERATION HELPER
# -------------------------------------------------------------------------
if FPDF_AVAILABLE:
    class MBTIPDF(FPDF):
        """
        한글 나눔바른고딕 폰트 적용 및 MBTI 진로 탐색 결과를 디자인한 PDF 생성기 클래스
        """
        def __init__(self, mbti_type, mbti_info):
            super().__init__()
            self.mbti_type = mbti_type
            self.mbti_info = mbti_info
            
            # NanumBarunGothic 폰트 다운로드 및 등록
            font_url = "https://github.com/google/fonts/raw/main/ofl/nanumbarungothic/NanumBarunGothic.ttf"
            font_bold_url = "https://github.com/google/fonts/raw/main/ofl/nanumbarungothic/NanumBarunGothicBold.ttf"
            
            try:
                self.regular_font_path = self._download_font(font_url, "NanumBarunGothic.ttf")
                self.bold_font_path = self._download_font(font_bold_url, "NanumBarunGothicBold.ttf")
                
                self.add_font("Nanum", "", self.regular_font_path)
                self.add_font("Nanum", "B", self.bold_font_path)
            except Exception as e:
                # 폰트 다운로드 실패 시 폰트 미설정으로 동작 (이모지 및 영어는 헬베티카 기본 대체 유도)
                st.warning("폰트를 불러오는 중 에러가 발생하여 PDF의 한글이 정상 출력되지 않을 수 있습니다.")
                self.add_font("Nanum", "", "")
                self.add_font("Nanum", "B", "")

        def _download_font(self, url, filename):
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            if not os.path.exists(filepath):
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        with open(filepath, "wb") as f:
                            f.write(response.content)
                    else:
                        raise Exception("Font download failed.")
                except Exception as e:
                    # 네트워크 타임아웃 예외 대응
                    raise e
            return filepath

        def header(self):
            self.set_fill_color(79, 70, 229) # 테마 포인트 컬러 (Indigo)
            self.rect(0, 0, 210, 15, "F")
            self.set_text_color(255, 255, 255)
            self.set_font("Nanum", "B", 10)
            self.cell(0, -2, "  🎓 MBTI Career Pathfinder - 미래를 설계하는 진로 교육", ln=1, align="L")
            self.ln(12)

        def footer(self):
            self.set_y(-20)
            self.set_text_color(156, 163, 175)
            self.set_font("Nanum", "", 9)
            self.cell(0, 10, "※ 본 결과는 교육용 진로 탐색 도구로 제공되며, 실제 선택 시 적성 검사 등을 동반하는 것이 좋습니다.", align="C")
            self.ln(5)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

        def build_report(self):
            self.add_page()
            
            # Title Section
            self.set_text_color(17, 24, 39)
            self.set_font("Nanum", "B", 24)
            self.cell(0, 15, f"{self.mbti_type} 유형 맞춤형 진로 리포트", ln=1, align="L")
            
            # Subtitle
            self.set_text_color(79, 70, 229)
            self.set_font("Nanum", "B", 14)
            self.cell(0, 10, f"★ {self.mbti_info['title']}", ln=1, align="L")
            self.ln(5)

            # Introduction Box
            self.set_fill_color(243, 244, 246)
            self.set_text_color(55, 65, 81)
            self.set_font("Nanum", "", 10)
            
            intro_text = f"성향 요약:\n{self.mbti_info['desc']}"
            self.multi_cell(0, 6, intro_text, border=1, fill=True, align="L")
            self.ln(8)

            # Core Strengths
            self.set_text_color(17, 24, 39)
            self.set_font("Nanum", "B", 13)
            self.cell(0, 8, "■ 핵심 강점 (Core Strengths)", ln=1)
            self.ln(2)
            
            self.set_font("Nanum", "", 10)
            for strength in self.mbti_info['strengths']:
                self.cell(5, 6, "-", ln=0)
                self.cell(0, 6, strength, ln=1)
            self.ln(8)

            # Career Recommendations
            self.set_text_color(17, 24, 39)
            self.set_font("Nanum", "B", 13)
            self.cell(0, 8, "■ 추천하는 어울리는 직업군 (Careers)", ln=1)
            self.ln(3)

            for career in self.mbti_info['careers']:
                # Job Title
                self.set_text_color(79, 70, 229)
                self.set_font("Nanum", "B", 11)
                self.cell(0, 6, f"▶ {career['name']}", ln=1)
                
                # Why it fits
                self.set_text_color(75, 85, 99)
                self.set_font("Nanum", "", 10)
                self.multi_cell(0, 5, f"추천 이유: {career['reason']}", align="L")
                self.ln(4)

# -------------------------------------------------------------------------
# UI STREAMLIT APP CODE
# -------------------------------------------------------------------------

# Title Hero Section
st.markdown(
    """
    <div style="text-align: center; padding: 2.5rem 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; color: white; margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">🎓 MBTI 진로 탐색 가이드</h1>
        <p style="font-size: 1.1rem; opacity: 0.9;">내 성격 유형에 딱 맞는 커리어를 탐색하고 나만의 PDF 진로 리포트를 다운로드하세요!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar - MBTI Choice & Personal info
with st.sidebar:
    st.markdown("### 🧬 내 성격 탐색 정보")
    
    mbti_selected = st.selectbox(
        "본인의 MBTI를 선택해 주세요:",
        options=list(MBTI_DATA.keys()),
        index=0
    )
    
    st.markdown("---")
    st.markdown("### ✍️ 사용자 정보 입력 (선택)")
    user_name = st.text_input("학생 / 사용자 이름:", placeholder="홍길동")
    school_name = st.text_input("학교 또는 소속 기관:", placeholder="나눔고등학교")
    
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #EEF2F6; padding: 1rem; border-radius: 0.5rem; font-size: 0.85rem; color: #374151;">
            💡 <b>교육적 참고사항:</b><br>
            이 가이드는 각 MBTI 유형이 선호하는 보편적인 작업 방식과 시너지가 잘 나는 대표적인 직무를 엄선하여 추천합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

# Active MBTI Details
mbti_info = MBTI_DATA[mbti_selected]

# Dynamic UI Style Configuration based on MBTI
accent_color = mbti_info["accent_color"]
bg_color = mbti_info["bg_color"]

st.markdown(
    f"""
    <style>
    .mbti-container {{
        background-color: {bg_color};
        padding: 2rem;
        border-radius: 1rem;
        border-left: 8px solid {accent_color};
        margin-bottom: 2rem;
    }}
    .career-card {{
        background-color: white;
        padding: 1.2rem;
        border-radius: 0.8rem;
        border: 1px solid #E5E7EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }}
    .accent-text {{
        color: {accent_color};
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Grid Layout: Left Details, Right Interaction
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(
        f"""
        <div class="mbti-container">
            <h2 style="color: {accent_color}; margin-top: 0;">
                <span style="font-size: 2.2rem; vertical-align: middle;">{mbti_info['emoji']}</span> 
                {mbti_selected} - {mbti_info['title']}
            </h2>
            <p style="font-size: 1.15rem; line-height: 1.6; color: #374151; font-weight: 500;">
                {mbti_info['desc']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f"### ✨ {mbti_selected}의 핵심 강점 (Core Strengths)")
    cols_strengths = st.columns(2)
    for i, strength in enumerate(mbti_info["strengths"]):
        col_idx = i % 2
        with cols_strengths[col_idx]:
            st.markdown(
                f"""
                <div style="background-color: #F9FAFB; padding: 0.8rem 1.2rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 4px solid {accent_color}; font-weight: 600; color: #1F2937;">
                    ✅ {strength}
                </div>
                """,
                unsafe_allow_html=True
            )

with col2:
    st.markdown("### 📥 맞춤 진로 보고서 발행")
    
    if not FPDF_AVAILABLE:
        st.warning("⚠️ `fpdf2` 패키지가 설치되지 않아 PDF 발행이 제한됩니다. 로컬 또는 클라우드 배포판에 `requirements.txt`를 생성하여 설치해 주세요.")
        st.code("fpdf2\nrequests", language="text")
    else:
        st.info("입력된 사용자 정보와 선택된 MBTI 분석 내용을 바탕으로 공식 수료 및 탐색 리포트를 PDF 문서로 발행할 수 있습니다.")
        
        # PDF Generation Trigger
        if st.button("📄 PDF 진로 리포트 생성하기", use_container_width=True):
            with st.spinner("전문 교육용 PDF를 생성하는 중입니다..."):
                try:
                    pdf = MBTIPDF(mbti_selected, mbti_info)
                    
                    # 추가 정보 입력 시 상단 웰컴 블록 보강
                    if user_name or school_name:
                        pdf.add_page()
                        pdf.set_text_color(17, 24, 39)
                        pdf.set_font("Nanum", "B", 20)
                        pdf.cell(0, 15, "진로 적성 탐색 완료 증서", ln=1, align="C")
                        pdf.ln(10)
                        
                        pdf.set_font("Nanum", "", 12)
                        pdf.cell(0, 10, f"소 속: {school_name if school_name else '(소속 없음)'}", ln=1, align="C")
                        pdf.cell(0, 10, f"성 명: {user_name if user_name else '미지정 학습자'}", ln=1, align="C")
                        pdf.cell(0, 10, f"진단 MBTI 유형: {mbti_selected}", ln=1, align="C")
                        
                        pdf.ln(15)
                        pdf.multi_cell(0, 7, 
                            "위 사람은 자신의 성격 유형(MBTI) 분석을 성실히 이행하고, "
                            "스스로의 강점과 이에 맞는 어울리는 직업 세계를 면밀히 탐색하여 "
                            "미래 지향적 자기 주도 진로 역량을 키웠음을 확인합니다.", 
                            align="C"
                        )
                        pdf.ln(20)
                        pdf.cell(0, 10, "MBTI Career Pathfinder 진로교육원", ln=1, align="C")
                        
                    # Main Report page
                    pdf.build_report()
                    
                    # output
                    pdf_output = pdf.output()
                    
                    st.success("🎉 PDF 리포트가 성공적으로 생성되었습니다!")
                    
                    st.download_button(
                        label="⬇️ PDF 리포트 다운로드",
                        data=bytes(pdf_output),
                        file_name=f"{mbti_selected}_진로_리포트_{user_name if user_name else '학습자'}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"PDF 생성에 실패했습니다: {e}")

st.markdown("---")
st.markdown(f"### 💼 {mbti_selected} 추천 직업 리스트 및 세부 탐색")

# Show Recommended Careers
for idx, career in enumerate(mbti_info["careers"]):
    st.markdown(
        f"""
        <div class="career-card">
            <h4 style="margin: 0 0 0.5rem 0; color: {accent_color}; font-size: 1.2rem;">
                📌 {idx+1}. {career['name']}
            </h4>
            <p style="margin: 0; color: #4B5563; font-size: 0.95rem; line-height: 1.5;">
                <strong>어울리는 이유:</strong> {career['reason']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
