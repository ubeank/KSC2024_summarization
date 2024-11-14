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
    
    for logprob_item in logprobs:
        for top_logprob in logprob_item.top_logprobs:
            token_str = top_logprob.token
            if token_str in token_probs:
                prob = logprob_to_prob(top_logprob.logprob) 
                if prob > token_probs[token_str]:
                    token_probs[token_str] = prob

    score = sum(int(token) * prob for token, prob in token_probs.items())
    
    return score, token_probs

def evaluate_review(review_id, source_text, generated_summary, target_summary, prompts):
    scores = {}
    token_probs_all_metrics = {}

    for metric, prompt in prompts.items():
        cur_prompt = prompt.replace('{{Document}}', source_text).replace('{{Summary}}', generated_summary).replace('{{Target Summary}}', target_summary)

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

        logprobs_content = completion.choices[0].logprobs.content
        score, token_probs = calculate_score(logprobs_content)
        scores[metric] = score
        token_probs_all_metrics[metric] = token_probs

    return scores, token_probs_all_metrics

def log_review_success(review_id):
    log_path = "./logs/log1"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)  
    with open(log_path, 'a') as log_file:
        log_file.write(f"Successfully processed ReviewID: {review_id}\n")

# ReviewID별로 평가 결과 저장
def evaluate_all_reviews(abstracts_file_path, summary_file_path, target_summary_file, output_file):
    prompts = {}
    prompt_files = ["Completeness_prompt_v2.txt", "Conciseness_prompt_v2.txt", "Faithfulness_prompt_v2.txt"]
    for filename in prompt_files:
        metric = filename.split('_')[0].lower()  # 'completeness', 'conciseness', 'faithfulness'
        with open(f'./prompts_v2/{filename}', 'r') as prompt_file:
            prompts[metric] = prompt_file.read()

    with open(output_file, 'w') as output:
        output.write("{\n")
        output.write(f'  "Abstracts File": "{abstracts_file_path}",\n')
        output.write(f'  "Summary File": "{summary_file_path}",\n')
        output.write(f'  "Target Summary File": "{target_summary_file}",\n')
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
            generated_summary = get_generated_summary_from_json(summary_file_path, review_id)
            target_summary = get_target_summary_from_csv(target_summary_file, review_id)

            if source_text and generated_summary and target_summary:
                scores, token_probs_all_metrics = evaluate_review(review_id, source_text, generated_summary, target_summary, prompts)

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

                total_scores["completeness"] += scores["completeness"]
                total_scores["conciseness"] += scores["conciseness"]
                total_scores["faithfulness"] += scores["faithfulness"]
                review_count += 1

                log_review_success(review_id)

        average_scores = {metric: total / review_count for metric, total in total_scores.items()}

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

def get_generated_summary_from_json(file_path, review_id):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            if item["ReviewID"] == review_id:
                return item["Generated"]
    return None

def get_target_summary_from_csv(file_path, review_id):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["ReviewID"] == review_id:
                return row["Target"]
    return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate summaries using GPT-4 with multiple prompts.")
    parser.add_argument("abstracts_file_path", type=str, help="Path to the JSON file containing abstracts.")
    parser.add_argument("summary_file_path", type=str, help="Path to the JSON file containing generated summaries.")
    parser.add_argument("target_summary_file", type=str, help="Path to the CSV file containing target summaries.")
    parser.add_argument("output_file", type=str, help="Path to the output JSON file for storing evaluation results.")

    args = parser.parse_args()

    evaluate_all_reviews(args.abstracts_file_path, args.summary_file_path, args.target_summary_file, args.output_file)
