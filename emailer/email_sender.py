import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configDomain
import configEmail
import configTitle
import time
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
# HTML 템플릿 파일에서 내용을 읽어오는 함수

def load_template(selected_domain):
    # 템플릿 파일 경로 생성
    template_path = f"templates/{selected_domain}_email_template.html"

    # 템플릿 파일 열기
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
        return template
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")


def generate_section(news_list):
    # 입력 데이터가 리스트인지 확인
    if not isinstance(news_list, list) or not news_list:
        return "<div>No news available.</div>"

    # 뉴스 항목을 HTML로 변환
    section_html = "<div class='news-section'>\n"
    for article in news_list:
        section_html += f'''
        <div class="news-item">
            <p><strong><a href="{article["link"]}">{article["title"]}</a></strong> [{article["media_name"]}] ({article["date"]})</p>
            <p>{article["summary"]}</p>
            <p>* 해당 기사: <a href="{article["link"]}">{article["link"]}</a></p>
        '''
        if article["duplicated_article"]:  # 중복 기사가 있는 경우만 추가
            section_html += f'<p>* 다른 기사: <a href="{article["duplicated_article"]}">{article["duplicated_article"]}</a></p>'
        section_html += '</div><br>'
    section_html += '</div>'
    return section_html

def send_email(news_by_section, selected_domain):
    # 도메인별 이메일 설정 가져오기
    EMAIL_CONFIG = configEmail.DOMAINS.get(selected_domain.lower())
    if not EMAIL_CONFIG:
        raise ValueError(f"Invalid domain selected: {selected_domain}")

    sender = EMAIL_CONFIG['sender']
    receivers = EMAIL_CONFIG['receivers']
    password = EMAIL_CONFIG['password']

    # HTML 템플릿을 불러옴
    template = load_template(selected_domain)

    # 선택된 도메인에 따라 섹션 키워드 가져오기
    if selected_domain not in configDomain.DOMAINS:
        raise ValueError(f"Invalid domain selected: {selected_domain}")
    
    domain_keywords = configDomain.DOMAINS[selected_domain]
    domain_title = configTitle.DOMAINS[selected_domain]

    # 섹션별로 뉴스 HTML 생성
    section_html_map = {}
    for section, keyword in domain_keywords.items():
        section_html_map[section] = generate_section(news_by_section.get(section, []))

    # 템플릿에서 변수를 실제 뉴스 내용으로 치환
    body = template
    for section, html_content in section_html_map.items():
        body = body.replace(f"{{{{ {section} }}}}", html_content)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)

            for recipient in receivers:
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = recipient
                msg['Subject'] = f"{TODAY} {domain_title} 일일 주요 보도자료"
                
                msg.attach(MIMEText(body, "html"))

                server.sendmail(sender, recipient, msg.as_string())
                print(f"Email sent to {recipient}")
                time.sleep(3)
        print("All Emails sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

    return body