import pandas as pd

gsheetkey = '1wFUQnxKj_BWKJ2zJgyfJROkoqINLjK0P314bP3cALEQ'
category_file_url=f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
category_file = pd.read_excel(category_file_url,sheet_name='Category')
base_url = 'https://www.amazon.in/gp/bestsellers/{}/ref=zg_bs_pg_{}?ie=UTF8&pg={}'

id = category_file['Cat_id']
urls = []
for i in id:
    urls.append(base_url.format(i,1,1))
    urls.append(base_url.format(i,2,2))



temp =''
for i in urls:
    pos = i.find('/bestsellers/')+len('/bestsellers/')
    dt = i[pos:]
    id =  dt[dt.find('/')+1:]

    pos = id.find('/')
    if pos != -1:
        temp =  str(id[:pos])
    else:
        temp =  str (dt[:dt.find('/')])


    print(temp)