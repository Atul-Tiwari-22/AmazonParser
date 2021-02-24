import scrapy
import pandas as pd
from ..items import ParserItem
from bs4 import BeautifulSoup
from datetime import date
import json

class ParserSpider(scrapy.Spider):
    products_count = 0 
    name = 'Parser'
    base_url = 'https://www.amazon.in/gp/bestsellers/{}/ref=zg_bs_pg_{}?ie=UTF8&pg={}'
    urls = []

    gsheetkey = '1wFUQnxKj_BWKJ2zJgyfJROkoqINLjK0P314bP3cALEQ'
    category_file_url=f'https://docs.google.com/spreadsheet/ccc?key={gsheetkey}&output=xlsx'
    category_file = pd.read_excel(category_file_url,sheet_name='Category')

    id = category_file['Cat_id']

    #id = pd.read_excel(r"C:\Users\atult\OneDrive\Desktop\Scrapy\Parser\Parser\Amaozn Category Links.xlsx")['Category ID']
    for i in id:
        urls.append(base_url.format(i,1,1))
        urls.append(base_url.format(i,2,2))
    
    print(len(urls))
    start_urls = urls
    #start_urls = ['https://www.amazon.in/gp/bestsellers/11364609031/ref=zg_bs_pg_1?ie=UTF8&pg=1']

    def parse(self, response):
        
        items = ParserItem()

        product_list = response.xpath("//*[@id='zg-ordered-list']//li").extract()
        Category_name = response.css('h1 span').css('::text').extract()
        if Category_name == []:
            print("Retry ......")
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
            return
        item_list = []


        for products in product_list:
            pos = products.find('></div></span>')
            xml = products[:pos] + '/' +products[pos:]
            soup = BeautifulSoup(xml, "xml")
            
    
            item = {}
            try:
                block = soup.find(class_='aok-inline-block zg-item')
                
                P_name = block.find(class_='a-link-normal').text.replace('\n','')#name
                link = block.find(class_='a-link-normal')['href']
                link = link[link.find('/dp/')+4:]
                ASIN = link[:link.find('/')] #asin
            except:
                print ('Error in name,asin block')
                P_name = '-'
                ASIN = '-'

            try:
                block = soup.find(class_='a-icon-row a-spacing-none')

                stars = block.find_all('a')[0]['title'] #stars
                ratings = block.find_all('a')[1].text # ratings
            except:
                #print(ASIN,'Error in stars,ratings block')
                stars = '-'
                ratings = '-'


            try:
                Rank = soup.find(class_='zg-badge-text').text[1:]
            except:
                Rank = '-'

            try:
                Price_range = soup.find(class_='p13n-sc-price').text
            except:
                Price_range = '-'


            item['ASIN'] = ASIN
            item['Name'] = P_name.strip()
            item['Star'] = stars
            item['Ratings'] = ratings
            item['Rank'] = Rank
            item['Link'] = 'https://www.amazon.in/dp/'+ASIN+'/'
            item['Price'] = Price_range
            
            item_list.append(item)


        ParserSpider.products_count += len(product_list)
        
        print(ParserSpider.products_count,'Done {} link = {}'.format(len(product_list),Category_name))

        print('products Done = ',ParserSpider.products_count)
        items['Product_list'] = item_list
        items['Category'] = Category_name[0]
        items['page_no'] = response.url[-1]


        i = response.request.url
        pos = i.find('/bestsellers/')+len('/bestsellers/')
        dt = i[pos:]
        id =  dt[dt.find('/')+1:]
        cat_id = ''
        pos = id.find('/')
        if pos != -1:
            cat_id =  str(id[:pos])
        else:
            cat_id =  str (dt[:dt.find('/')])

        if cat_id.find('?') != -1:
            cat_id = cat_id[:cat_id.find('?')]

        items['Category_id'] =  cat_id

        items['Category_link'] =  response.request.url
        
        
        yield items