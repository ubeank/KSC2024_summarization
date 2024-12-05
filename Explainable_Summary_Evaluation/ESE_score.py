import json
import argparse

# 평가 기준 및 가중치 설정
SCORE_WEIGHTS = {
    "Completeness": {
        "Population_Mismatch": 25,
        "Intervention_Mismatch": 25,
        "Outcome_Mismatch": 25,
        "Omission_of_Key_Facts": 25
    },
    "Conciseness": {
        "Redundancy": 30,
        "Length": 25,
        "Lack_of_Focus": 25,
        "Excessive_Detail": 20
    },
    "Faithfulness": {
        "Intrinsic_Information": 30,
        "Extrinsic_Information": 25,
        "Ambiguity": 15,
        "Overgeneralization": 10,
        "Incorrect_Implication": 10,
        "Inaccurate_Emphasis": 10
    }
}

# ESE Score 계산
def calculate_ese_score(errors, ese_summary_length, target_summary_length):
    scores = {
        "Completeness": 0,
        "Conciseness": 0,
        "Faithfulness": 0
    }

    for category, sub_errors in errors.items():
        category_score = 100
        for sub_error, weight in SCORE_WEIGHTS[category].items():
            if sub_errors[sub_error] > 0:  # 에러가 1개라도 검출되면 0점
                category_score -= weight

        # 길이 패널티 적용
        length_ratio = min(1, ese_summary_length / target_summary_length)
        adjusted_score = category_score * length_ratio
        scores[category] = round(adjusted_score, 4)  # 반올림

    return scores

# 전체 평균 점수 계산
def calculate_dataset_scores(results):
    total_scores = {
        "Completeness": 0,
        "Conciseness": 0,
        "Faithfulness": 0
    }
    sample_count = len(results)

    for result in results:
        for category in total_scores:
            total_scores[category] += result["Scores"][category]

    # 평균 점수 계산
    average_scores = {category: round(total / sample_count, 4) for category, total in total_scores.items()}
    return average_scores

def main():

    parser = argparse.ArgumentParser(description="Calculate ESE Scores with length penalty from ESE summaries.")
    parser.add_argument("input", type=str, help="Path to the ESE summary JSON file")
    parser.add_argument("output", type=str, help="Path to save the ESE scores JSON file")

    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as file:
            ese_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: {args.input} 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print(f"Error: {args.input} 파일의 JSON 형식이 잘못되었습니다.")
        return

    # ESE Score 계산
    results = []
    for sample in ese_data["samples"]:
        review_id = sample["ReviewID"]
        errors = sample["errors"]
        ese_summary = sample["ESE Summary"]
        target_summary = sample["Target Summary"]

        ese_summary_length = len(ese_summary)
        target_summary_length = len(target_summary)

        category_scores = calculate_ese_score(errors, ese_summary_length, target_summary_length)

        results.append({
            "ReviewID": review_id,
            "Scores": category_scores
        })

    # 전체 데이터셋 평균 점수 계산
    dataset_scores = calculate_dataset_scores(results)

    output_data = {
        "Dataset Average Scores": dataset_scores,
        "Samples": results
    }

    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(output_data, file, ensure_ascii=False, indent=4)

    print(f"ESE scores with length penalty saved to {args.output}")

if __name__ == "__main__":
    main()
