import os
import json
import csv
import re
from openai import OpenAI

client = OpenAI()

def evaluate_review(review_id, source_text, generated_summary, prompts):
    scores_all_metrics = {}

    for metric, prompt in prompts.items():
        cur_prompt = prompt.replace('{{Document}}', source_text).replace('{{Summary}}', generated_summary)


        completion = client.chat.completions.create(
            model="gpt-4o-mini",
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
            temperature=0.5, # temperature 값을 낮춰 일관성 있는 결과 생성
            max_tokens=5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            n=20  # 20개의 응답을 한 번에 생성
        )


        scores_all_metrics[metric] = [clean_score(choice.message.content) for choice in completion.choices]

    return scores_all_metrics

def clean_score(score_str):
    """점수를 정제하는 함수: 비정상적인 문자열 제거 및 숫자만 반환"""
    # 문자열에서 숫자 부분만 추출
    match = re.search(r'\d+', score_str) 
    return match.group(0) if match else None

def compute_average(scores):
    """평균 계산 함수. 숫자로 변환 가능한 값만 평균 계산."""
    numeric_scores = []

    for score in scores:
        try:
            if score is not None:
                numeric_scores.append(float(score))
        except ValueError:
            # 숫자 변환 실패 시 해당 점수 무시
            continue

    if numeric_scores:
        return sum(numeric_scores) / len(numeric_scores)
    return None 

# ReviewID별로 평가 결과 저장
def evaluate_all_reviews(abstracts_file_path, summary_file_path, output_file):

    prompts = {}
    prompt_files = ["Completeness_prompt.txt", "Conciseness_prompt.txt", "Faithfulness_prompt.txt"]
    for filename in prompt_files:
        metric = filename.split('_')[0].lower()  # completeness, conciseness, faithfulness
        with open(f'./prompts/{filename}', 'r') as prompt_file:
            prompts[metric] = prompt_file.read()

    # 모든 review에 대해 평가 수행
    with open(abstracts_file_path, 'r') as json_file:
        data = json.load(json_file)

    evaluations = {}

    # 각 ReviewID에 대해 평가
    for item in data:
        review_id = item["ReviewID"]
        source_text = item["Abstracts"]
        generated_summary = get_generated_summary_from_csv(summary_file_path, review_id)

        if source_text and generated_summary:

            scores_all_metrics = evaluate_review(review_id, source_text, generated_summary, prompts)

            # 각 지표마다 20개의 결과에 대한 평균 계산
            averaged_scores = {}
            for metric, scores in scores_all_metrics.items():
                avg_score = compute_average(scores)
                averaged_scores[metric] = {
                    "scores": scores, 
                    "average": avg_score if avg_score is not None else "No valid numeric scores" 
                }


            evaluations[review_id] = averaged_scores

    with open(output_file, 'w') as outfile:
        json.dump(evaluations, outfile, indent=4)

# reviewID에 해당하는 generatedSummary 획득
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
