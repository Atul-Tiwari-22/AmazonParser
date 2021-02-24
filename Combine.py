import json
import pandas as pd
from datetime import date,datetime
import smtplib
from email.message import EmailMessage

def email_notification(subject,body,to):
    msg = EmailMessage()
    msg.set_content(body)
    msg["subject"] = subject
    msg["to"] = to

    user = "hunt@mamaearth.in"
    msg['from'] = user
    password = "phvyauwrccsomine"

    server = smtplib.SMTP("smtp.gmail.com",port=587)
    server.starttls()
    server.login(user,password)
    server.send_message(msg)

    server.quit()

with open(r'C:\Users\atult\OneDrive\Desktop\Scrapy\Parser\data.json') as f:
    data = json.load(f)


dt = {}

for i in data:
    #print(i['Category'][0])
    #print(len(i['Product_list']))
    
    if i['Category'] not in dt.keys():
        dt[i['Category']] = pd.DataFrame()

    for j in i['Product_list']:
        dic = dict(j)
        dic['Category Name']=i['Category']
        dic['Date Time']= datetime.now()
        c_id = i['Category_id']
        if c_id.find('?') != -1:
            c_id = c_id[:c_id.find('?')]
        dic['Category_id'] = c_id
        dic['Category_link'] = i['Category_link']
        dt[i['Category']] = dt[i['Category']].append(dic, ignore_index=True)

    print ("joining == " , i['Category'])

master_dataframe = pd.concat(map(lambda x:dt[x],dt.keys()))

today = str(date.today())
with pd.ExcelWriter('output {}.xlsx'.format(today)) as writer:
    master_dataframe.to_excel(writer, sheet_name= '_Master')

#email_notification('Parser REPORT','Parshing Complet At {}\n Category added {}\n Products Added {}'.format(datetime.now(),len(dt.keys()),len(master_dataframe)),"harkirat.s@mamaearth.in")

print(datetime.now(),len(dt.keys()),len(master_dataframe))