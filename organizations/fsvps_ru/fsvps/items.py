# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FsvpsItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    phone = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
