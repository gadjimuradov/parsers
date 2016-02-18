#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy

from fsvps.items import FsvpsItem


class FsvpsSpider(scrapy.Spider):
    name = "fsvps"
    allowed_domains = ["www.fsvps.ru"]
    start_urls = [
        "http://www.fsvps.ru/fsvps/structure/terorgs",
    ]

    def parse(self, response):
        for href in response.xpath('//table[@class="item"]//a[starts-with(@href,"/fsvps/structure/terorgs")]/@href'):
            url = response.urljoin(href.extract())
            if not url.encode('utf-8').endswith('.html'):
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        sel = response.xpath("//div[@class='nText']")
        address_pattern = "//p[re:test(@class,'noin?dent')][span[contains(text(),'%s')]]/span[@class='big']/text()" \
                          % u'Адрес'
        phone_pattern = "//p[re:test(@class,'noin?dent')][span[contains(text(),'%s')]]/span[@class='big']/text()" \
                        % u'Тел'
        email_pattern = "//p[re:test(@class,'noin?dent')][span[contains(text(),'%s')]]/a/text()" % 'mail'

        out_item = FsvpsItem()
        out_item['name'] = response.xpath("//td[@id='contenttd']/div/h2/text()").extract()
        out_item['url'] = response.url
        out_item['phone'] = sel.xpath(phone_pattern).extract()
        out_item['address'] = sel.xpath(address_pattern).extract()
        out_item['email'] = sel.xpath(email_pattern).extract()
        yield out_item
