import os
import json
from openai import OpenAI

client = OpenAI()

def generate_summarizer(abstracts):
    
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    max_tokens=1024,
    # messages=[
    #     {
    #         "role": "system",
    #         "content": "You are a helpful assistant for multidocument abstractive summarization. Each documents are separated by <s> and </s> tokens."
    #     },
    #     {
    #         "role": "system",
    #         "name": "example_user",
    #         "content" : "<s> Intravenous methylprednisolone pulse therapy in minimal change nephrotic syndrome. The effectiveness of intravenous methylprednisolone pulses in 20 mg/kg/day for three consecutive days was compared with a more conventional oral prednisone regime in inducing remission in adult patients presenting with first episodes of minimal change nephrotic syndrome. Methylprednisolone was significantly less effective and failed to induce remission in six of nine patients within two weeks of treatment, while the oral prednisone regime was uniformly effective in all eight patients within five weeks. Of the six non-responders to methylprednisolone five subsequently remitted with oral prednisone, and one with cyclophosphamide. Except for one patient in the oral prednisone group who had acute gastritis with bleeding, no serious side-effect was seen with either treatment regimes.</s> <s> Controlled trial of methylprednisolone pulses and low dose oral prednisone for the minimal change nephrotic syndrome. In a multicentre, randomised, prospective trial 89 patients (67 children and 22 adults) with the minimal change nephrotic syndrome were treated with three intravenous pulses of methylprednisolone followed by low dose oral prednisone for six months (group given methylprednisolone) or with high dose oral prednisone for four weeks followed by low dose oral prednisone for five months (control group). Five patients in the group given methylprednisolone and one in the control group did not respond initially. The time to response was shorter in children treated with methylprednisolone. No significant differences between the two groups were observed in the number of patients who relapsed or number of relapses per patient per year. Patients given methylprednisolone tended to relapse earlier than patients in the control group. Side effects related to treatment were significantly fewer in the group given methylprednisolone than in the control group. These data suggest that a short course of methylprednisolone pulses followed by low dose oral prednisone is only marginally less effective than a regimen of high dose oral steroids but can improve the ratio of risk to benefit associated with treatment of the minimal change nephrotic syndrome.</s> <s> Adult minimal change nephropathy: experience of the collaborative study of glomerular disease. Adult minimal change nephropathy: experience of the collaborative study of glomerular disease.</s> "  
    #     },
    #     {
    #         "role": "system",
    #         "name": "example_assistant",
    #         "content" : "Further comparative studies are required to examine the efficacy of immunosuppressive agents for achievement of sustained remission of nephrotic syndrome caused by minimal change disease."
             
    #     },
    #     {
    #         "role": "user",
    #         "content": f"Summarize this for a doctor: {abstracts}"
    #     },
    #     ]
    messages=[
        {
            "role": "system",
            "content": "You are an expert assistant for generating clinical conclusions from multiple biomedical studies. Each document is separated by <s> and </s> tokens. Produce a concise and well-supported conclusion directly. Clearly state the level of evidence supporting treatment effectiveness, summarize effects observed across relevant patient groups, and include any specific recommendations or areas where further research is needed. Make the conclusion practical for clinical decision-making, emphasizing key findings, consensus or variability in treatment outcomes, and considerations for future study design to improve clinical outcomes."
        },
        {
            "role": "system",
            "name": "example_user",
            "content" : "<s> Intravenous methylprednisolone pulse therapy in minimal change nephrotic syndrome. The effectiveness of intravenous methylprednisolone pulses in 20 mg/kg/day for three consecutive days was compared with a more conventional oral prednisone regime in inducing remission in adult patients presenting with first episodes of minimal change nephrotic syndrome. Methylprednisolone was significantly less effective and failed to induce remission in six of nine patients within two weeks of treatment, while the oral prednisone regime was uniformly effective in all eight patients within five weeks. Of the six non-responders to methylprednisolone five subsequently remitted with oral prednisone, and one with cyclophosphamide. Except for one patient in the oral prednisone group who had acute gastritis with bleeding, no serious side-effect was seen with either treatment regimes.</s> <s> Controlled trial of methylprednisolone pulses and low dose oral prednisone for the minimal change nephrotic syndrome. In a multicentre, randomised, prospective trial 89 patients (67 children and 22 adults) with the minimal change nephrotic syndrome were treated with three intravenous pulses of methylprednisolone followed by low dose oral prednisone for six months (group given methylprednisolone) or with high dose oral prednisone for four weeks followed by low dose oral prednisone for five months (control group). Five patients in the group given methylprednisolone and one in the control group did not respond initially. The time to response was shorter in children treated with methylprednisolone. No significant differences between the two groups were observed in the number of patients who relapsed or number of relapses per patient per year. Patients given methylprednisolone tended to relapse earlier than patients in the control group. Side effects related to treatment were significantly fewer in the group given methylprednisolone than in the control group. These data suggest that a short course of methylprednisolone pulses followed by low dose oral prednisone is only marginally less effective than a regimen of high dose oral steroids but can improve the ratio of risk to benefit associated with treatment of the minimal change nephrotic syndrome.</s> <s> Adult minimal change nephropathy: experience of the collaborative study of glomerular disease. Adult minimal change nephropathy: experience of the collaborative study of glomerular disease.</s> "  
        },
        {
            "role": "system",
            "name": "example_assistant",
            "content" : "Further comparative studies are required to examine the efficacy of immunosuppressive agents for achievement of sustained remission of nephrotic syndrome caused by minimal change disease."
             
        },
        {
            "role": "user",
            "content": f"Summarize the abstracts to be similar in length to the target summaries, approximately 85 words : {abstracts}" 
        },
        ]
    )
    
    return completion.choices[0].message.content


with open('testdata_for_led.json', 'r') as file:
    data = json.load(file)

json_data = []

for item in data:
    new_data = {}
    abstracts = item["Abstracts"]
    summary = generate_summarizer(abstracts)
    new_data["ReviewID"] = item["ReviewID"]
    new_data["Generated"] = summary
    json_data.append(new_data)

with open('gpt_full_summarization.json', 'w') as file:
    json.dump(json_data, file, indent=4)
