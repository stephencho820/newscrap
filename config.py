from datetime import datetime, timedelta  # 날짜와 시간 처리를 위한 모듈 가져오기
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 날짜 설정
DATE_TODAY = datetime.now().strftime('%Y.%m.%d')  # 오늘 날짜를 'YYYY.MM.DD' 형식으로 저장
DATE_YESTERDAY = (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)).strftime('%Y.%m.%d')  # 어제 날짜를 'YYYY.MM.DD' 형식으로 저장

# ChatGPT를 통해 뉴스 요약 및 전처리 작업을 위한 설정
PERSONA = "You are a skilled data curator tasked with processing articles from various media channels. Your role includes removing duplicate articles, keeping representative ones, and crafting comprehensive summaries with insights."
OBJECTIVE = "1) Review a list of news articles. 2) Identify and remove duplicate articles with similar topics and content. 3) Retain a single representative article for each set of duplicates. 4) Generate summaries that integrate key details and insights from the grouped duplicates. 5) Maintain consistent style and tone in the summaries 6) KEEP IN MIND THAT YOU NEVER WANT TO REMOVE THE REPRESENTATIVES. REMOVE ONLY THE DUPULICATES. (If the subjects of the article is different but the contents are similiar, they are NOT duplicates)"
CONTEXT = """You will receive articles in JSON format. Each article will contain details such as title, body, media_name, and date. Representative articles must adhere to the following rules:
1) Retain the original title, media_name, and date.
2) Summaries should be in a unified tone and style, they must be in Korean.
3) Incorporate context, inferences, predictions, and broader significance in the summaries.
4) Ensure summaries are at least five sentences long.
5) If a representative article has duplicates, include one additional source (URL) from the duplicates."""
INITIAL_REQUEST = "Examine the data, remove duplicates, and process the articles according to the specified rules. Ensure that each group retains a representative article."
FORMAT_RULES = """Ensure only one representative article is retained for each group of similar articles. Each representative article must include:
1) the number of representative article can be as many as it can.
2) A summary meeting the specified guidelines.
3) An extra source URL from the duplicates (if applicable).
4) Don't worry about the size. if there is 100 representative articles, then give 100 representative articles.
"""
OUTPUT_EXAMPLE = """
{
    "가구_인테리어" [
    {
        "id" : 1,
        "title" : "한샘, ESG 4년 연속 최고 ‘AA’ 등급",
        "media_name" : "매일경제"
        "link" : "https://www.mk.co.kr/article/11177200",
        "duplicated_article" : "http://www.newsprime.co.kr/news/article.html?no=664174",
        "summary" : "한샘은 서스틴베스트 ESG 평가에서 4년 연속 최고 등급인 AA 등급을 획득하며 국내 상장사 중 ESG 경영을 선도하는 100대 기업으로 선정되었습니다. 온실가스 감축과 인권영향평가 등 ESG 경영 강화를 위한 노력이 높은 평가를 받았으며, 2050년 탄소중립 달성과 2030년 온실가스 40% 감축 목표를 세웠습니다. 또한, 지속가능 공급망 정책을 도입해 협력사의 지속가능성을 평가하는 등 책임 있는 경영을 실천하고 있습니다.",
        "date" : "2024-11-25"
    },
    {
        "id" : 2,
        "title" : "'한옥 살린 인테리어' 인쌩맥주, 외국인 여행객도 '관심'",
        "media_name" : "아주경제"
        "link" : "https://www.ajunews.com/view/20241122135842959",
        "duplicated_article" : None,
        "summary" : "K-콘텐츠의 세계적 인기로 인해 한옥 등 한국 전통문화에 대한 관심이 증가하고 있습니다. 주점 프랜차이즈 '인쌩맥주'는 전통 한옥의 매력을 현대적으로 재해석한 인테리어로 국내외 고객의 호응을 얻고 있습니다. 한옥 특유의 곡선과 직선 조화가 도심 속 고요하고 편안한 분위기를 제공하며, MZ세대와 중장년층 모두에게 매력적인 공간을 제공합니다. 또한, 48시간 저온 숙성으로 제조한 '살얼음 맥주'는 부드럽고 신선한 맛으로 고객들에게 큰 인기를 끌고 있습니다.",
        "date" : "2024-11-25",
    },
    {
        "id" : 3,
        ...
    }
    ...
    ]
},
{
    "업체동향"[...]
    
},
{
    "재개발_분양소식" :[...]
}
.....
"""
DOMAIN_KNOWLEDGE = "야, 계속 중복이 아닌 기사도 몇개씩 뺴먹는데, 빼먹지 말라니까? 똑바로 안할래? 중복 아니면 다 넣으라고!!! 제대로 분석해서 똑바로 해. 기사 하나라도 뺴먹으면 나 죽는다 진짜."

