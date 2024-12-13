from datetime import datetime, timedelta  # 날짜와 시간 처리를 위한 모듈 가져오기
import os
from dotenv import load_dotenv

# 이메일 설정 (보안상 비밀번호는 환경변수 또는 보안 모듈 사용 권장)
SEMICONDUCTOR_EMAIL = {
    'sender': os.getenv('EMAIL_SENDER'),
    'receivers': ['asaac.corp@gmail.com'],
    'bcc': ['stephencho820@gmail.com', 'jxli917@naver.com', 'kehdgnsdl77@naver.com'],
    'password': os.getenv('EMAIL_PASSWORD')  # 환경변수로부터 비밀번호를 가져옴
}

INTERIOR_EMAIL = {
    'sender': os.getenv('EMAIL_SENDER'),
    'receivers': ['asaac.corp@gmail.com'],
    'bcc': ['stephencho820@gmail.com', 'glaubeaj@naver.com'],
    'password': os.getenv('EMAIL_PASSWORD')  # 환경변수로부터 비밀번호를 가져옴
}

ESG_EMAIL = {
    'sender': os.getenv('EMAIL_SENDER'),
    'receivers': ['asaac.corp@gmail.com', 'asaacco@naver.com'],
    # 'receivers': ['stephencho820@gmail.com', 'asaac.corp@gmail.com', 'kehdgnsdl77@naver.com', 
    #             'dkswjddls7@naver.com', 'dipshin@nate.com', 'dlgmlaud22@naver.com', 
    # 'receivers': ['dipshin@nate.com', 'dlgmlaud22@naver.com', 
    #             'my777.lee@samsung.com', 'pengdo@myorange.io', 'chahs0616@naver.com', 
    #             'sjun0623@naver.com', 'jylee@thecsr-center.com', 'ojm2976@naver.com', 
    #             'sh.lee@marcspon.com', 'bysfood@cj.net', 'Jylee19@shinwon.com', 
    #             'junghee84.kim@gmail.com', 'mahnchey@gmail.com', 'sgkwon@samsung.com', 
    #             'yedam0407@naver.com', 'sujinny424.SP@gmail.com', 'my777.lee@samsung.com', 
    #             's33on.lee@samsung.com', 'jiyeun.park@sk.com', 'sj.alex.park@gmail.com', 
    #             'seungjoon.park@macoll.com', 'kychoi082@kia.com', 'ggojing@gmail.com', 
    #             'kehin7@naver.com', 'jhwoang@naver.com', 'hyojinn309@gmail.com', 
    #             'jjker19@gmail.com', 'kyuwonchung61@gmail.com', 'hijeongsu2018@gmail.com', 
    #             'mookhiang@hanmail.net', 'halegina@i-sh.co.kr', 'insightjinhyeok@gmail.com', 
    #             'eseon0519@gmail.com', 'genuinektb@naver.com', 'hyunsk@qesg.co.kr', 
    #             'president@esgyouthforum.kr', 'birnp@daum.net', 'jwshim90@naver.com'],
    'password': os.getenv('EMAIL_PASSWORD')  # 환경변수로부터 비밀번호를 가져옴
}

STOCK_EMAIL = {
    'sender': os.getenv('EMAIL_SENDER'),
    'receivers': ['asaac.corp@gmail.com'],
    'bcc': ['stephencho820@gmail.com', 'jeihyuck@naver.com','infynylg@gmail.com'],
    'password': os.getenv('EMAIL_PASSWORD')  # 환경변수로부터 비밀번호를 가져옴
}

DOMAINS = {
    "semiconductor": SEMICONDUCTOR_EMAIL,
    "interior": INTERIOR_EMAIL,
    "esg": ESG_EMAIL,
}
