# -*- coding: utf-8 -*-
from belinvestbank.items import BelinvestbankAtmItem, BelinvestbankInfoItem, BelinvestbankOfficeItem
from belinvestbank.pipelines import BelinvestbankAtmPipeline, BelinvestbankInfoPipeline, BelinvestbankOfficePipeline
__author__ = 'PekopT'

from sys import stdout

import scrapy
from codecs import getwriter

sout = getwriter("utf8")(stdout)


class BelinvestbankAtmSpider(scrapy.Spider):
    name = "BelinvestbankAtms"
    allowed_domains = ["www.belinvestbank.by"]
    start_urls = [
        "http://www.belinvestbank.by/atm/",
    ]

    pipeline = set([
        BelinvestbankAtmPipeline,
    ])

    def parse(self, response):
        for href in response.xpath('//div[@class="region"]/p/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_atm_page)

    def parse_atm_page(self, response):

        for item in response.xpath('//div[@class="list"]/div[@class="item"]'):
            item_name = item.xpath('div[@class="name a"]/a/span/text()').extract()[0]
            if item_name.find(u'Банкомат') != -1:
                atm = BelinvestbankAtmItem()
                atm['name'] = item_name
                atm['url'] = response.url
                yield atm


class BelinvestbankInfoSpider(scrapy.Spider):
    name = "BelinvestbankInfos"
    allowed_domains = ["www.belinvestbank.by"]
    start_urls = [
        "http://www.belinvestbank.by/atm/",
    ]

    pipeline = set([
        BelinvestbankInfoPipeline,
    ])

    def parse(self, response):
        for href in response.xpath('//div[@class="region"]/p/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_atm_page)

    def parse_atm_page(self, response):
        for item in response.xpath('//div[@class="list"]/div[@class="item"]'):
            item_name = item.xpath('div[@class="name a"]/a/span/text()').extract()[0]
            if item_name.find(u'Инфокиоск') != -1:
                atm = BelinvestbankInfoItem()
                atm['name'] = item_name
                atm['url'] = response.url
                yield atm


class BelinvestbankOfficeSpider(scrapy.Spider):
    name = "BelinvestbankOffices"
    allowed_domains = ["www.belinvestbank.by"]
    start_urls = [
        "http://www.belinvestbank.by/geo/",
    ]

    pipeline = set([
        BelinvestbankOfficePipeline,
    ])

    def parse(self, response):
        for href in response.xpath('//div[@class="region"]/p/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_atm_page)

    def parse_atm_page(self, response):
        for item in response.xpath('//div[@class="list"]/div[@class="item"]'):
            item_name = item.xpath('div[@class="name a"]/a/span/text()').extract()[0]
            office = BelinvestbankOfficeItem()
            office['name'] = item_name
            office['url'] = response.url
            office['address'] = item.xpath('div[@class="addres"]/strong/text()').extract()[0]
            office['phones'] = item.xpath('div[@class="item_block"]//tr/td[1]/strong/text()').extract()
            yield office
