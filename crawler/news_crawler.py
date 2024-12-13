import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import logging
from config import DATE_YESTERDAY, DATE_TODAY
from configDomain import DOMAINS

def convert_relative_date(relative_date):
    if "일 전" in relative_date:
        days_ago = int(relative_date.split("일 전")[0].strip())
        return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    elif "시간 전" in relative_date:
        hours_ago = int(relative_date.split("시간 전")[0].strip())
        return (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d')
    # 필요하다면 분, 주 등 추가 처리
    return datetime.now().strftime('%Y-%m-%d')

def crawl_news(query, yesterday, today):
    news_list = []
    page = 1  # Start from page 1

    while True:
        # 일 단위로 필터링된 URL을 생성, 페이지 번호 추가
        url = f"https://search.naver.com/search.naver?where=news&query={query}&sm=tab_pge&sort=0&photo=0&field=1&pd=3&ds={yesterday}&de={today}&docid=&related=0&mynews=1&office_type=1&office_section_code=1011&nso=so:r,p:from{yesterday.replace('.', '')}to{today.replace('.', '')}&is_sug_officeid=0&office_category=3&service_area=0&start={page}"
        #logging.debug(url)
        print(url)
        logging.debug(f"Fetching page {page}...")
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 뉴스 제목, 링크, 요약, 날짜, 매체명 추출
        items = soup.select(".news_wrap")
        
        if not items:
            # 더 이상 결과가 없으면 반복 종료
            logging.info("No more news articles found.")
            break

        for item in items:
            title = item.select_one(".news_tit").text
            link = item.select_one(".news_tit")["href"]
            summary = item.select_one(".news_dsc").text
            date_element = item.select_one(".info_group .info")
            if date_element:
                relative_date = date_element.text.strip()
                date = convert_relative_date(relative_date)
            else:
                date = "날짜 없음"
            media_name = item.select_one(".info_group .press").text.strip()  # 매체명 추출
            
            news_list.append({
                "title": title,
                "link": link,
                "summary": summary,
                "date": date,
                "media_name": media_name
            })
        
        # 잠시 대기 후 다음 페이지로 넘어감
        time.sleep(0.5)  # 서버 과부하 방지를 위해 지연시간 추가
        page += 10  # 네이버 뉴스는 페이지 당 10개의 결과를 표시하므로, 페이지 번호를 10씩 증가
        if page >= 100:
            break

    return news_list


def fetch_news(selected_domain):
    # 도메인별 키워드 가져오기
    domain_keywords = DOMAINS.get(selected_domain.lower())
    if not domain_keywords:
        raise ValueError(f"Invalid domain selected: {selected_domain}")
    
    fetched_news_dict = {}
    for section, keywords in domain_keywords.items():
        all_news = []
        for keyword in keywords:
            logging.debug(f"Crawling news for keyword: {keyword}")  # 키워드에 대한 크롤링 상태 확인
            news_list = crawl_news(keyword, DATE_YESTERDAY, DATE_TODAY)

            # 크롤링 결과 디버깅
            if news_list:
                logging.debug(f"News found for {keyword}: {len(news_list)} articles")  # 뉴스 개수 출력
            else:
                logging.debug(f"No news found for {keyword}")  # 뉴스가 없을 경우 디버깅 정보 출력

            all_news.extend(news_list)
        fetched_news_dict[section] = all_news
        
    return fetched_news_dict
