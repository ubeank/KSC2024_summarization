import torch
import json
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("allenai/led-base-16384-cochrane")
model = AutoModelForSeq2SeqLM.from_pretrained("allenai/led-base-16384-cochrane").to("cuda").half()

with open('testdata_for_led.json', 'r') as file:
    data = json.load(file)

dataset = Dataset.from_list(data)
json_data = [] 

def generate_summary(data):
    inputs_dict = tokenizer(data["Abstracts"], padding="max_length", max_length = 16384, return_tensors="pt", truncation=True)
    input_ids = inputs_dict.input_ids.to("cuda")
    attention_mask = inputs_dict.attention_mask.to("cuda")
    global_attention_mask = torch.zeros_like(attention_mask)
    
    global_attention_mask[:, 0] = 1
    
    predicted_summary_ids = model.generate(input_ids, attention_mask=attention_mask, global_attention_mask=global_attention_mask, max_length = 1024)
    data["generated_summary"] = tokenizer.batch_decode(predicted_summary_ids, skip_special_tokens=True)
    new_data = {
        'ReviewID' : data['ReviewID'],
        'generated_summary' : data['generated_summary']
    }
    json_data.append(new_data)
    return data

result = dataset.map(generate_summary, batched=True, batch_size=1)

with open('generated_summaries-addmin.json', 'w') as file:
    json.dump(json_data, file, indent=4)
