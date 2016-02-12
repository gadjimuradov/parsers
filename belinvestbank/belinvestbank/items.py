# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BelinvestbankAtmItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    add_address = scrapy.Field()
    time = scrapy.Field()
    info = scrapy.Field()
    curr = scrapy.Field()
    accept = scrapy.Field()
    region = scrapy.Field()



class BelinvestbankInfoItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    add_address = scrapy.Field()
    time = scrapy.Field()
    info = scrapy.Field()
    curr = scrapy.Field()
    accept = scrapy.Field()
    region = scrapy.Field()


class BelinvestbankOfficeItem(scrapy.Item):
    name = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    address = scrapy.Field()
    phones = scrapy.Field()
    region = scrapy.Field()
    add_address = scrapy.Field()
    time = scrapy.Field()
