import os
import json
import csv
import math
from openai import OpenAI

client = OpenAI()


def logprob_to_prob(logprob):
    return math.exp(logprob)

# 로그 확률을 받아 실제 확률로 변환하고, 종합 점수를 계산
def calculate_score(logprobs, token_range=(1, 5)):
    score = 0
    token_probs = {str(i): 0 for i in range(token_range[0], token_range[1] + 1)}
    
    # logprobs에서 상위 토큰들의 확률을 계산
    for logprob_item in logprobs:
        for top_logprob in logprob_item.top_logprobs:
            token_str = top_logprob.token  # 상위 토큰
            if token_str in token_probs:  # 토큰이 1~5 범위 내에 있는지 확인
                prob = logprob_to_prob(top_logprob.logprob)
                # 현재 저장된 확률보다 큰 경우에만 업데이트
                if prob > token_probs[token_str]:
                    token_probs[token_str] = prob

    # 점수 계산, 가중합을 사용
    score = sum(int(token) * prob for token, prob in token_probs.items())
    
    return score, token_probs

# 요약에서 각 평가 프롬프트에 대한 점수와 토큰 확률을 계산
def evaluate_review(review_id, source_text, generated_summary, prompts):
    scores = {}
    token_probs_all_metrics = {}

    for metric, prompt in prompts.items():

        cur_prompt = prompt.replace('{{Document}}', source_text).replace('{{Summary}}', generated_summary)

        #gpt api 호출
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=5,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assistant for evaluation of generated text summaries."
                },
                {
                    "role": "user",
                    "content": cur_prompt
                }
            ],
            temperature=0,
            logprobs=True,
            top_logprobs=10,
        )

        logprobs_content = completion.choices[0].logprobs.content  # 각 토큰별 로그 확률 데이터
        # 각 Review에 대해 실제 확률 및 점수 계산
        score, token_probs = calculate_score(logprobs_content)
        scores[metric] = score
        token_probs_all_metrics[metric] = token_probs

    return scores, token_probs_all_metrics

# 로그 기록
def log_review_success(review_id):
    log_path = "./logs/log2"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a') as log_file:
        log_file.write(f"Successfully processed ReviewID: {review_id}\n")

# ReviewID별로 평가 결과 저장
def evaluate_all_reviews(abstracts_file_path, summary_file_path, output_file):
    prompts = {}
    prompt_files = ["Completeness_prompt_v1.txt", "Conciseness_prompt_v1.txt", "Faithfulness_prompt_v1.txt"]
    for filename in prompt_files:
        metric = filename.split('_')[0].lower()  # 'completeness', 'conciseness', 'faithfulness'
        with open(f'./prompts_v1/{filename}', 'r') as prompt_file:
            prompts[metric] = prompt_file.read()

    with open(output_file, 'w') as output:
        output.write("{\n")
        output.write(f'  "Abstracts File": "{abstracts_file_path}",\n')
        output.write(f'  "Summary File": "{summary_file_path}",\n')
        output.write('  "Evaluations": [\n')

    with open(abstracts_file_path, 'r') as json_file:
        data = json.load(json_file)

    total_scores = {"completeness": 0, "conciseness": 0, "faithfulness": 0}
    review_count = 0

    with open(output_file, 'a') as output:
        # 각 ReviewID에 대해 평가
        for idx, item in enumerate(data):
            review_id = item["ReviewID"]
            source_text = item["Abstracts"]
            generated_summary = get_generated_summary_from_csv(summary_file_path, review_id)

            if source_text and generated_summary:
                # 하나의 review ID에 대해 3개의 prompt를 모두 수행해서 각 점수와 토큰 확률을 획득
                scores, token_probs_all_metrics = evaluate_review(review_id, source_text, generated_summary, prompts)

                # 각 지표별 점수와 토큰 확률을 저장
                review_result = {
                    "ReviewID": review_id,
                    "Completeness": scores['completeness'],
                    "Conciseness": scores['conciseness'],
                    "Faithfulness": scores['faithfulness'],
                    "Token Probabilities": {
                        "Completeness": token_probs_all_metrics['completeness'],
                        "Conciseness": token_probs_all_metrics['conciseness'],
                        "Faithfulness": token_probs_all_metrics['faithfulness']
                    }
                }

                json.dump(review_result, output, ensure_ascii=False, indent=4)
                if idx < len(data) - 1:
                    output.write(",\n")

                # 각 지표별 점수를 합산
                total_scores["completeness"] += scores["completeness"]
                total_scores["conciseness"] += scores["conciseness"]
                total_scores["faithfulness"] += scores["faithfulness"]
                review_count += 1

                log_review_success(review_id)

        # 각 지표별 평균 계산
        average_scores = {metric: total / review_count for metric, total in total_scores.items()}

        # 평균 점수 추가
        output.write(",\n") 
        json.dump({
            "Average Scores": {
                "Average Completeness": average_scores["completeness"],
                "Average Conciseness": average_scores["conciseness"],
                "Average Faithfulness": average_scores["faithfulness"],
                "Number of total reviews": review_count
            }
        }, output, ensure_ascii=False, indent=4)

        output.write("\n  ]\n}") 

# reviewID에 대응하는 generated summary 반환
def get_generated_summary_from_csv(file_path, review_id):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ReviewID"] == review_id:
                return row["Generated"]
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate summaries using GPT-4 with multiple prompts.")
    parser.add_argument("abstracts_file_path", type=str, help="Path to the JSON file containing abstracts.")
    parser.add_argument("summary_file_path", type=str, help="Path to the CSV file containing generated summaries.")
    parser.add_argument("output_file", type=str, help="Path to the output JSON file for storing evaluation results.")

    args = parser.parse_args()

    evaluate_all_reviews(args.abstracts_file_path, args.summary_file_path, args.output_file)
