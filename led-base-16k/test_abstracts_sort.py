import pandas as pd
import json

file_path = '/data/kyb0314/repos/cochrane/cochrane/test-inputs.csv'
df = pd.read_csv(file_path)

first_abstract = df['ReviewID'].iloc[5677]
print(first_abstract)


def same_ReviewID_sort(df):
    json_data = []
    count = 0

    while count < len(df): 
        review_ID = df['ReviewID'].iloc[count]


        study = "<s> "
        study += str(df['Title'].iloc[count])
        
        if pd.isnull(df['Abstract'].iloc[count]):
            study += str(df['Title'].iloc[count])
        else:
            study += str(df['Abstract'].iloc[count])
        study += " </s>"
        
 
        while count + 1 < len(df) and df['ReviewID'].iloc[count + 1] == review_ID:
            count += 1 
            
            study += "<s>"
            study += str(df['Title'].iloc[count])
            if pd.isnull(df['Abstract'].iloc[count]):
                study += str(df['Title'].iloc[count])
            else:
                study += str(df['Abstract'].iloc[count])
            study += " </s>"

  
        data = {
            'ReviewID': review_ID,
            'Abstracts': study
        }
        json_data.append(data)
        
        count += 1  

    return json_data

json_data = same_ReviewID_sort(df)

with open('testdata_for_led.json', 'w') as file:
    json.dump(json_data, file, indent=4)
