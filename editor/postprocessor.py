# GPT와 연동하여 Usecase 별로 추가 가공하는 단계# GPT와 연동하여 첫 가공을 하는 단계
import openai
import pandas as pd
import json
import re


def postprocess_news(contents):
    try:
        postprocessed_contents = json.loads(contents)
        print("Successfully changed to json format")
    except json.JSONDecodeError as e:
        print("Failed to change to json format, e")

    # 변환된 JSON을 확인
    print(json.dumps(postprocessed_contents, indent=4))
    
    return postprocessed_contents