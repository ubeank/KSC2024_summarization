import json
import tiktoken
import os

# GPT 모델에 맞는 인코더를 불러옵니다.
def count_tokens(text, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)

# 입력 파일 경로
input_file = '/data/dntjd123kr/repos/lecture-summarizer/project_data/testdata_0.5_for_led.json'
output_file = '/data/dntjd123kr/repos/lecture-summarizer/project_data/tokenCalculator/token_0.5_testdata.json'

# JSON 파일 로드
with open(input_file, 'r') as file:
    data = json.load(file)

token_data = []
total_tokens = 0
max_tokens = 0

# 각 ReviewID마다 토큰 수 계산
for item in data:
    review_id = item['ReviewID']
    input_text = item['SummarizedAbstracts']
    
    # input_text에 대한 토큰 수 계산
    total_review_tokens = count_tokens(input_text)
    
    # 총 토큰 수 및 최대 토큰 수 갱신
    total_tokens += total_review_tokens
    max_tokens = max(max_tokens, total_review_tokens)
    
    token_data.append({
        "ReviewID": review_id,
        "TokenCount": total_review_tokens
    })

# 전체 리뷰의 평균 토큰 수 계산
average_tokens = total_tokens / len(token_data) if token_data else 0

# 결과를 JSON 형식으로 저장
output = {
    "ReviewID_TokenCounts": token_data,
    "AverageTokenCount": average_tokens,
    "MaxTokenCount": max_tokens
}

os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(output, f, indent=4)

print(f"Token counts have been calculated and saved to {output_file}")

