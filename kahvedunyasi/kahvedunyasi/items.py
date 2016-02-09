# -*- coding: utf-8 -*-

import scrapy


class KahvedunyasiItem(scrapy.Item):
    name = scrapy.Field()
    coordx = scrapy.Field()
    coordy = scrapy.Field()
    tel = scrapy.Field()
    addr = scrapy.Field()
    city = scrapy.Field()
