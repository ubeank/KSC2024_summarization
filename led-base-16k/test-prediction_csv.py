import json
import csv

with open('test_target-generated.json', 'r') as file:
    data = json.load(file)
    
selected_keys = ["ReviewID", "Generated"]
    
with open('test-predictions.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    header = [''] + selected_keys
    csv_writer.writerow(header)
    
    for index, row in enumerate(data):
        csv_writer.writerow([index] + [row[key] for key in selected_keys])