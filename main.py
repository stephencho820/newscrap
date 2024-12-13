from crawler.news_crawler import fetch_news
from editor.preprocessor import preprocess_news
from editor.postprocessor import postprocess_news
from emailer.email_sender import send_email
from uploader.naver_uploader import post_to_naver_cafe
import json
import logging
import pandas as pd
from datetime import datetime


TODAY = datetime.now().strftime("%Y-%m-%d")

def main():
    logging.info("Starting the application...")
    try:
        select_domain = "esg" #configDomain에 DOMAINS에 있는 KEYWORD 입력

        fetched_news = fetch_news(select_domain) # 뉴스 크롤링(dict)
        logging.info("Fetching Completed...")

        preprocessed_news = preprocess_news(fetched_news) #크롤링된 뉴스 gpt로 중복제거 (전처리)
        logging.info("Preprocessing Completed...")

        postprocessed_news = postprocess_news(preprocessed_news) # 중복 제거 후 json 형태로 가공
        print("##########")
        print(type(postprocessed_news))
        print(postprocessed_news)

        result_html = send_email(postprocessed_news, select_domain) # json 형태의 data를 email로 보내기
        print(result_html)
        with open('output.html', "w", encoding="utf-8") as file:
            file.write(result_html)

        print("HTML file saved as 'output.html'")

        # if select_domain == "esg1":
        #     tags = ['ESG', 'DT', 'DX', '일일브리핑']
        #     post_to_naver_cafe(title, result_html, tags)

    except Exception as e:
        logging.error("An error occurred", exc_info=True)

if __name__ == "__main__":
    # Logging 초기화
    logging.basicConfig(
        level=logging.DEBUG,  # 로그 레벨 설정
        format="%(asctime)s [%(levelname)s] %(message)s",  # 로그 메시지 포맷
        handlers=[
            logging.FileHandler("app.log"),  # 로그를 파일에 저장
            logging.StreamHandler()         # 콘솔 출력
        ]
    )
    main()
