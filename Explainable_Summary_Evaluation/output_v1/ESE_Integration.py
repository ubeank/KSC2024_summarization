import json
import re
import argparse
from collections import defaultdict

def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        print(f"Error: {file_path} 파일의 JSON 형식이 잘못되었습니다.")
        return []

def extract_spans(tagged_html):
    if not tagged_html:
        return []

    cleaned_html = re.sub(r"```html\n|```|\\|\n", "", tagged_html)

    spans = re.findall(r"(<span class=\"([^\"]+)\">(.*?)</span>)", cleaned_html)
    return spans

def calculate_error_counts(spans):
    error_counts = defaultdict(int)
    for _, class_names, _ in spans:
        for class_name in class_names.split():
            error_counts[class_name] += 1
    return dict(error_counts)

# 전체 에러를 담기 위한 최기화 함수
def initialize_total_errors():
    return {
        "Completeness": {
            "Population_Mismatch": 0,
            "Intervention_Mismatch": 0,
            "Outcome_Mismatch": 0,
            "Omission_of_Key_Facts": 0
        },
        "Conciseness": {
            "Redundancy": 0,
            "Length": 0,
            "Lack_of_Focus": 0,
            "Excessive_Detail": 0
        },
        "Faithfulness": {
            "Intrinsic_Information": 0,
            "Extrinsic_Information": 0,
            "Ambiguity": 0,
            "Overgeneralization": 0,
            "Incorrect_Implication": 0,
            "Inaccurate_Emphasis": 0
        }
    }

# 전체 에러 산출
def update_total_errors(total_errors, sample_errors):
    for category in total_errors:
        for error_type in total_errors[category]:
            total_errors[category][error_type] += sample_errors[category][error_type]

# standard_summary에 <span> 태그 삽입 및 에러 계산
def insert_spans_and_calculate_errors(standard_text, *span_sources):
    spans_to_insert = []
    all_spans = []

    # 각 source에서 <span> 태그 추출
    for source in span_sources:
        if source:
            spans = extract_spans(source)
            all_spans.extend(spans)
            spans_to_insert.extend(spans)

    # replace를 사용할 예정이니 긴 텍스트부터 처리
    spans_to_insert.sort(key=lambda x: len(x[2]), reverse=True)

    # standard 기준으로 태그 삽입
    modified_text = standard_text
    for span, _, span_content in spans_to_insert:
        modified_text = modified_text.replace(span_content, span, 1)

    # 에러 개수 계산
    error_counts = calculate_error_counts(all_spans)

    return modified_text, error_counts

def main():
    parser = argparse.ArgumentParser(description="Process JSON files to create ESE summaries.")
    parser.add_argument("standard", type=str, help="Path to standard_summary.json file")
    parser.add_argument("completeness", type=str, help="Path to completeness_output.json file")
    parser.add_argument("conciseness", type=str, help="Path to conciseness_output.json file")
    parser.add_argument("faithfulness", type=str, help="Path to faithfulness_output.json file")
    parser.add_argument("output", type=str, help="Path to the output file where ESE summaries will be saved")

    args = parser.parse_args()

    standard_summary = load_json(args.standard)
    completeness_output = load_json(args.completeness)
    conciseness_output = load_json(args.conciseness)
    faithfulness_output = load_json(args.faithfulness)

    total_errors = initialize_total_errors()

    results = []

    for standard_entry in standard_summary:
        review_id = standard_entry["ReviewID"]
        standard_generated = standard_entry.get("Generated", "")

        completeness_summary = next((entry["HTML-tagged Generated Summary"] for entry in completeness_output if entry["ReviewID"] == review_id), None)
        conciseness_summary = next((entry["HTML-tagged Generated Summary"] for entry in conciseness_output if entry["ReviewID"] == review_id), None)
        faithfulness_summary = next((entry["HTML-tagged Generated Summary"] for entry in faithfulness_output if entry["ReviewID"] == review_id), None)

        # ESE Summary 생성 및 에러 계산
        ese_summary, error_counts = insert_spans_and_calculate_errors(
            standard_generated, completeness_summary, conciseness_summary, faithfulness_summary
        )

        # 에러 필드 구성
        sample_errors = {
            "Completeness": {
                "Population_Mismatch": error_counts.get("Population_Mismatch", 0),
                "Intervention_Mismatch": error_counts.get("Intervention_Mismatch", 0),
                "Outcome_Mismatch": error_counts.get("Outcome_Mismatch", 0),
                "Omission_of_Key_Facts": error_counts.get("Omission_of_Key_Facts", 0)
            },
            "Conciseness": {
                "Redundancy": error_counts.get("Redundancy", 0),
                "Length": error_counts.get("Length", 0),
                "Lack_of_Focus": error_counts.get("Lack_of_Focus", 0),
                "Excessive_Detail": error_counts.get("Excessive_Detail", 0)
            },
            "Faithfulness": {
                "Intrinsic_Information": error_counts.get("Intrinsic_Information", 0),
                "Extrinsic_Information": error_counts.get("Extrinsic_Information", 0),
                "Ambiguity": error_counts.get("Ambiguity", 0),
                "Overgeneralization": error_counts.get("Overgeneralization", 0),
                "Incorrect_Implication": error_counts.get("Incorrect_Implication", 0),
                "Inaccurate_Emphasis": error_counts.get("Inaccurate_Emphasis", 0)
            }
        }

        update_total_errors(total_errors, sample_errors)

        result_entry = {
            "ReviewID": review_id,
            "ESE Summary": ese_summary,
            "errors": sample_errors
        }
        results.append(result_entry)

    # 최종 결과 저장
    output = {
        "total_errors": total_errors,
        "samples": results
    }

    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    print(f"ESE summaries with total errors saved to {args.output}")

if __name__ == "__main__":
    main()
