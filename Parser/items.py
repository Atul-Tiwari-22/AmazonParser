# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Product_list = scrapy.Field()
    Category = scrapy.Field()
    page_no =scrapy.Field() 
    Category_id = scrapy.Field() 
    Category_link = scrapy.Field() 