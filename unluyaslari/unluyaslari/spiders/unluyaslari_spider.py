from unluyaslari.items import UnluyaslariItem

__author__ = 'PekopT'

import scrapy


class UnluyaslariSpider(scrapy.Spider):
    name = "unluyaslari"
    allowed_domains = ["www.unluyaslari.com"]
    start_urls = [
        "http://www.unluyaslari.com/a/",
    ]

    def parse(self, response):
        for href in response.xpath('//table[@id="AutoNumber2"]//table[@id="AutoNumber1"]//td//a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        for sel in response.xpath("//table[@id='table3']//table[@id='table4']"):
            item = UnluyaslariItem()
            item['url'] = response.url
            item['name'] = sel.xpath('tr[1]/td[3]/p/text() | tr[1]/td[3]/p/a/font/text()').extract()
            item['desc'] = sel.xpath('tr[2]/td//strong/text()').extract()
            item['weight'] = sel.xpath('tr[3]/td/strong[1]/text()').extract()
            item['height'] = sel.xpath('tr[3]/td/strong[2]/text()').extract()
            yield item