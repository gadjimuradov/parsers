from unlulerinboylari.items import UnlulerinboylariItem

__author__ = 'PekopT'

import scrapy


class UnlulerinboylariSpider(scrapy.Spider):
    name = "Unlulerinboylari"
    allowed_domains = ["www.unlulerinboylari.com"]
    start_urls = [
        "http://www.unlulerinboylari.com/index.php",
    ]

    def parse(self, response):
        for href in response.xpath('//p[@class="harfler"]/a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_letter_page)

    def parse_letter_page(self, response):
        for href in response.xpath('//div[@class="sanatci"]/div[@class="aciklama"]//a/@href'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response):
        item = UnlulerinboylariItem()
        item['url'] = response.url
        item['name'] = response.xpath('//div[@class="aciklama"]/p[1]/text()').extract()
        item['height'] = response.xpath('//div[@class="aciklama"]/p[2]/text()').extract()
        item['weight'] = response.xpath('//div[@class="aciklama"]/p[3]/text()').extract()
        yield item