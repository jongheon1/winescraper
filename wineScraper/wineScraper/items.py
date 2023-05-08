# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WinescraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class WineItem(scrapy.Item):
    
    name_ko = scrapy.Field()
    name_en = scrapy.Field()
    img = scrapy.Field()
    details = scrapy.Field()
    sugar = scrapy.Field()
    acidaty = scrapy.Field()
    body = scrapy.Field()
    awards = scrapy.Field()
    info = scrapy.Field()
