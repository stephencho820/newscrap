import openai
import os
import json
import pandas as pd
from dotenv import load_dotenv
import logging
from config import PERSONA, OBJECTIVE, CONTEXT, INITIAL_REQUEST, FORMAT_RULES, DOMAIN_KNOWLEDGE, OUTPUT_EXAMPLE
# .env 파일 로드 및 OpenAI API 키 설정
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
import json
import pandas as pd
import logging
from openai import OpenAI
import re



def get_chatgpt4o_response_newsletter(persona, objective, context, initial_request, format_rules, output_example, domain_knowledge, data):

    client = OpenAI()

    logging.info("Generated message for ChatGPT.")
    
    # ChatGPT 요청 메시지 생성
    messages = [
        {"role": "system", "content": f"{persona}"},
        {"role": "user", "content": f"### Objective:\n{objective}"},
        {"role": "user", "content": f"### Context:\n{context}"},
        {"role": "user", "content": f"### Initial Request:\n{initial_request}"},
        {"role": "user", "content": f"### Follow these format/rules:\n{format_rules}"},
        {"role": "user", "content": f"### This is the example json format of the output. Ignore the contents inside and numbers of Categories and articles.:\n{output_example}"},
        {"role": "user", "content": f"### Domain knowledge you should consider:\n{domain_knowledge}"},
        {"role": "user", "content": f"### Here is the dataset(json) you MUST consider:\n{data}"},
    ]

    try:
        # ChatGPT API 호출
        completion = client.chat.completions.create(
        model="gpt-4o",  # GPT-4 모델
        messages=messages,
        response_format = {'type':"json_object"},
        temperature=0.7  # 답변의 창의성 조정
        )
        response = completion.choices[0].message.content
        logging.info("Received response from ChatGPT.")
        return response

    except Exception as e:
        logging.error(f"Error calling ChatGPT API: {e}", exc_info=True)
        raise

def preprocess_news(contents_dict):

    logging.info("Processing news with ChatGPT...")

    try:
        # 입력 데이터 타입 확인 및 변환
        if isinstance(contents_dict, dict):
            contents_df = pd.DataFrame([contents_dict])
            logging.info("Converted single dict to DataFrame.")

        elif contents_dict.empty:
            logging.warning("Fetched news is empty. No data to process.")
            return None

        # DataFrame을 JSON 형식으로 변환
        print(contents_df)
        contents_json = contents_df.to_json(orient="records", force_ascii=False)
        print(type(contents_json))
        print(contents_json)

        # ChatGPT API에 데이터 전달
        response = get_chatgpt4o_response_newsletter(
            persona=PERSONA,
            objective=OBJECTIVE,
            context=CONTEXT,
            initial_request=INITIAL_REQUEST,
            format_rules=FORMAT_RULES,
            output_example = OUTPUT_EXAMPLE,
            domain_knowledge = DOMAIN_KNOWLEDGE,
            data=contents_json
        )
    except Exception as e:
        logging.error(f"Error occurred during news processing: {e}", exc_info=True)
        raise

    return response