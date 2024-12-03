import os
import json
import csv
from openai import OpenAI

client = OpenAI()

def analyze_summary(review_id, source_text, reference_summary, synthesized_summary, prompt_template):
    prompt = prompt_template.replace('{{source_text}}', source_text)\
                            .replace('{{synthesized_summary}}', synthesized_summary)\
                            .replace('{{reference_summary}}', reference_summary)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an assistant that analyzes summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=1500
    )
    
    return completion.choices[0].message.content.strip()

def split_analysis(analysis_text):
    parts = analysis_text.split("2. Error Documentation", 1)
    if len(parts) == 2:
        html_summary = parts[0].replace("1. HTML-tagged Generated Summary:\n", "").strip()
        error_documentation = parts[1].strip()
        return html_summary, error_documentation
    return analysis_text, ""  # Default fallback if splitting fails


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


def log_review_success(review_id):
    log_path = "./logs/log_faithfulness"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, 'a') as log_file:
        log_file.write(f"Successfully processed ReviewID: {review_id}\n")


def evaluate_all_reviews(abstracts_file_path, summary_file_path, target_summary_file, output_file, prompt_template):
    with open(abstracts_file_path, 'r') as json_file:
        abstracts_data = json.load(json_file)

    # Output 파일 초기화
    with open(output_file, 'w', encoding='utf-8') as output_json:
        output_json.write("[\n")

    first_entry = True

    for item in abstracts_data:
        review_id = item["ReviewID"]
        source_text = item["Abstracts"]
        synthesized_summary = get_generated_summary_from_json(summary_file_path, review_id)
        target_summary = get_target_summary_from_csv(target_summary_file, review_id)

        if source_text and synthesized_summary and target_summary:
            analysis_result = analyze_summary(
                review_id, source_text, target_summary, synthesized_summary, prompt_template
            )

            # Split analysis into separate fields
            html_summary, error_documentation = split_analysis(analysis_result)

            result_entry = {
                "ReviewID": review_id,
                "HTML-tagged Generated Summary": html_summary,
                "Error Documentation": error_documentation
            }

            with open(output_file, 'a', encoding='utf-8') as output_json:
                if not first_entry:
                    output_json.write(",\n")
                json.dump(result_entry, output_json, ensure_ascii=False, indent=4)
                first_entry = False

            log_review_success(review_id)

    with open(output_file, 'a', encoding='utf-8') as output_json:
        output_json.write("\n]\n")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate summaries using GPT-4 with multiple prompts.")
    parser.add_argument("prompt_template", type=str, help="Path to the text file containing the GPT prompt template.")
    parser.add_argument("abstracts_file_path", type=str, help="Path to the JSON file containing abstracts.")
    parser.add_argument("summary_file_path", type=str, help="Path to the JSON file containing generated summaries.")
    parser.add_argument("target_summary_file", type=str, help="Path to the CSV file containing target summaries.")
    parser.add_argument("output_file", type=str, help="Path to the output JSON file for storing evaluation results.")


    args = parser.parse_args()

    with open(args.prompt_template, 'r') as prompt_file:
        prompt_template = prompt_file.read()

    evaluate_all_reviews(
        args.abstracts_file_path,
        args.summary_file_path,
        args.target_summary_file,
        args.output_file,
        prompt_template
    )
