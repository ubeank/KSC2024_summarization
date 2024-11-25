from openai import OpenAI
import json

client = OpenAI()


# 입력 데이터
data = {
    "source_text":"",

    "synthesized_summary":"",

    "reference_summary": ""
}

# GPT 프롬프트 생성
def create_prompt(data):
    return f"""
You will be provided with three inputs: the source text, the synthesized summary (Summary), and the reference summary (Target Summary).

Your task is to categorize the potential errors in the synthesized summary (Summary) into three main categories: Faithfulness, Completeness, and Conciseness. Additionally, for each identified error, you will need to specify its corresponding sub error categories to provide a more granular breakdown of the errors.

Main error Categories:

Faithfulness - The summarizer does not manipulate the information in the input text (i.e., intrinsic) and add any information not directly inferable from the input text (i.e., extrinsic).
Completeness - The summarizer ensures the inclusion of all keyfacts from the input text in the output summary.
Conciseness - The summarizer refrains from incorporating information outside the keyfacts in the output, maintaining a succinct and focused summary.

Follow these steps to complete the task:

Carefully read the source text and identify the key facts and main points.
Read the synthesized summary (Summary) and compare it to the reference summary (Target Summary). Use the following questions to identify errors in each category: Faithfulness, Completeness, Conciseness.
For each error identified, record the main error category and provide exactly three sub categories under that main category.
Example:

Source Text:

{data['source_text']}

Target Summary:

{data['reference_summary']}

Summary:

{data['synthesized_summary']}

Example Answer Format:

Main Error Category:
Sub Categories:
1. text: reason
2. text: reason
3. text: reason
"""

# GPT 호출 함수
def call_gpt(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # GPT 모델 선택
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes summaries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return str(e)

# 프롬프트 생성 및 GPT 호출
prompt = create_prompt(data)
result = call_gpt(prompt)
print(result)

# 결과를 output.json에 저장
output_file = "output.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump({"result": result}, file, ensure_ascii=False, indent=4)

print(f"Results saved to {output_file}")
