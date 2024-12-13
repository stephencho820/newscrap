# 반도체, 배터리, AI/로봇 관련 키워드 설정


SEMICONDUCTOR_KEYWORD = {
    "반도체": ["반도체"],
    "배터리": ["배터리", "2차 전지", "전기차", "테슬라"],
    "AI/로봇": ["AI", "인공지능", "로봇", "robot", "OPENAI", "오픈AI"]
}

# 인테리어 관련 키워드 설정
INTERIOR_KEYWORD = {
    "가구_인테리어": ["가구용", "특판가구", "인테리어", "주거공간", "건자재"],
    "업체동향": ["한샘", "리바트", "넵스", "에넥스", "LX지인", "LX하우시스"],
    "재건축_분양소식": ["분양", "재개발", "재건축"]
}
# ESG 관련 키워드 설정
ESG_KEYWORD = {
    "ESG_소식": ["ESG | 지속가능경영 | 넷제로 | 재생에너지 | 탄소배출권 | ESRS | CSRD | CSDDD | CBAM | RE100 | TCFD | TNFD | EcoVadis | CDP | SBTi | 탄소중립 | RBA VA | 공급망실사"],
    "DX_소식": ["디지털전환 | DigitalTransformation"]
}

DOMAINS = {
    "semiconductor": SEMICONDUCTOR_KEYWORD,
    "interior": INTERIOR_KEYWORD,
    "esg": ESG_KEYWORD,
}
