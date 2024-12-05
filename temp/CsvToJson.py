import pandas as pd
import json

# CSV 파일 경로
csv_file_path = './test-predictions.csv'

# JSON 파일 저장 경로
json_file_path = './test-predictions.json'

df = pd.read_csv(csv_file_path).loc[:, ~pd.read_csv(csv_file_path).columns.str.contains('^Unnamed')]

json_data = df.to_dict(orient='records')

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)