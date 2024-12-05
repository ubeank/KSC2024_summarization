import json
import re
import argparse
import csv
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

def load_target_summaries(file_path):
    target_summaries = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                review_id = row["ReviewID"]
                target_summary = row["Target"]
                target_summaries[review_id] = target_summary
    except FileNotFoundError:
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
    except KeyError:
        print(f"Error: {file_path} 파일에 'ReviewID' 또는 'Target' 열이 없습니다.")
    return target_summaries

def extract_spans(tagged_html):
    if not tagged_html:
        return []

    cleaned_html = re.sub(r"```html\n|```|\\|\n|\"", "", tagged_html)

    spans = re.findall(r"(<span class=([^\s>]+(?: [^\s>]+)*)>(.*?)</span>)", cleaned_html)
    return spans



def clean_error_documentation(error_doc):
    if not error_doc:
        return ""
    cleaned_doc = re.sub(r"```html\n|```|\\|\n|\"", "", error_doc)
    return cleaned_doc.strip()

def calculate_error_counts(spans):
    error_counts = defaultdict(int)
    for _, class_names, _ in spans:
        for class_name in class_names.split():
            error_counts[class_name] += 1
    return dict(error_counts)

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

def update_total_errors(total_errors, sample_errors):
    for category in total_errors:
        for error_type in total_errors[category]:
            total_errors[category][error_type] += sample_errors[category][error_type]

def insert_spans_and_calculate_errors(standard_text, *span_sources):
    spans_to_insert = []
    all_spans = []

    for source in span_sources:
        if source:
            spans = extract_spans(source)
            all_spans.extend(spans)
            spans_to_insert.extend(spans)

    spans_to_insert.sort(key=lambda x: len(x[2]), reverse=True)

    modified_text = standard_text
    for span, _, span_content in spans_to_insert:
        modified_text = modified_text.replace(span_content, span, 1)

    error_counts = calculate_error_counts(all_spans)

    return modified_text, error_counts

#샘플 유효성 검사
#샘플의 main category가 모두 0인 경우, 해당 main category의 error document는 No Error이어야 함
#위의 조건을 만족하지 않으면 잘못된 샘플로 분류
def is_sample_valid(sample_errors, error_docs):
    for category, sub_errors in sample_errors.items():
        if all(count == 0 for count in sub_errors.values()):  # No errors in this category
            if clean_error_documentation(error_docs[category]) != "No Error":
                return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Process JSON files to create ESE summaries with target summaries.")
    parser.add_argument("standard", type=str, help="Path to standard_summary.json file")
    parser.add_argument("completeness", type=str, help="Path to completeness_output.json file")
    parser.add_argument("conciseness", type=str, help="Path to conciseness_output.json file")
    parser.add_argument("faithfulness", type=str, help="Path to faithfulness_output.json file")
    parser.add_argument("target_summary_file", type=str, help="Path to the CSV file containing target summaries.")
    parser.add_argument("output", type=str, help="Path to the output file where ESE summaries will be saved")

    args = parser.parse_args()

    standard_summary = load_json(args.standard)
    completeness_output = load_json(args.completeness)
    conciseness_output = load_json(args.conciseness)
    faithfulness_output = load_json(args.faithfulness)
    target_summaries = load_target_summaries(args.target_summary_file)

    total_errors = initialize_total_errors()

    results = []
    removed_samples = []
    total_samples = len(standard_summary)

    for standard_entry in standard_summary:
        review_id = standard_entry["ReviewID"]
        standard_generated = standard_entry.get("Generated", "")

        completeness_summary = next((entry for entry in completeness_output if entry["ReviewID"] == review_id), None)
        conciseness_summary = next((entry for entry in conciseness_output if entry["ReviewID"] == review_id), None)
        faithfulness_summary = next((entry for entry in faithfulness_output if entry["ReviewID"] == review_id), None)

        if not (completeness_summary and conciseness_summary and faithfulness_summary):
            total_samples -= 1
            removed_samples.append(review_id)
            continue

        # Extract Error Documentation and clean
        error_docs = {
            "Completeness": clean_error_documentation(completeness_summary.get("Error Documentation", "")),
            "Conciseness": clean_error_documentation(conciseness_summary.get("Error Documentation", "")),
            "Faithfulness": clean_error_documentation(faithfulness_summary.get("Error Documentation", ""))
        }

        ese_summary, error_counts = insert_spans_and_calculate_errors(
            standard_generated,
            completeness_summary.get("HTML-tagged Generated Summary"),
            conciseness_summary.get("HTML-tagged Generated Summary"),
            faithfulness_summary.get("HTML-tagged Generated Summary")
        )

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

        if not is_sample_valid(sample_errors, error_docs):
            total_samples -= 1
            removed_samples.append(review_id)
            continue

        update_total_errors(total_errors, sample_errors)

        result_entry = {
            "ReviewID": review_id,
            "ESE Summary": ese_summary,
            "Target Summary": target_summaries.get(review_id, ""),
            "errors": sample_errors
        }
        results.append(result_entry)

    output = {
        "total_result": {
            "total_samples": total_samples,
            "removed_samples": {
                "number": len(removed_samples),
                "removed_samples list": removed_samples
            },
            "total_errors": total_errors
        },
        "samples": results
    }

    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(output, file, ensure_ascii=False, indent=4)

    print(f"ESE summaries with target summaries saved to {args.output}")

if __name__ == "__main__":
    main()
