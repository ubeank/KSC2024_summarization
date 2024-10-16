import json
import tiktoken

max_tokens = 16384

def count_cut_tokens(text, model="gpt-4o-mini"):
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if(len(tokens) > max_tokens):
        print(len(tokens))
        truncated_tokens = tokens[:max_tokens]
        truncated_text = encoding.decode(truncated_tokens)
        return truncated_text
    else:
        return text

input_file = 'testdata0.5_for_led.json'
#output_file = 'led_cutlimit_test-inputs.json'

# JSON 파일 로드
with open(input_file, 'r') as file:
    data = json.load(file)

new_json_data = []

for item in data:
    review_id = item['ReviewID']
    input_text = item['Summaries']

    new_Abstracts = count_cut_tokens(input_text)
    
    new_json_data.append({
        "ReviewID" : review_id,
        "Summaries" : new_Abstracts
    })

with open('led_cutlimit_test-inputs_0.5.json', 'w') as f:
    json.dump(new_json_data, f, indent=4)

    
    
    
    
    
    
