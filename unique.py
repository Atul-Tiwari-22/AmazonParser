import json
import pandas as pd

with open(r'C:\Users\atult\OneDrive\Desktop\Scrapy\Parser\data.json') as f:
  data = json.load(f)


dt = []

for i in data:
    #print(i['Category'][0])
    #print(len(i['Product_list']))
    if i['Category'] not in dt:
        dt.append(i['Category'])

print(len(dt))

'''
with pd.ExcelWriter('output {}.xlsx'.format('unique cat')) as writer:
    master_dataframe.to_excel(writer, sheet_name= '_Master')
'''
