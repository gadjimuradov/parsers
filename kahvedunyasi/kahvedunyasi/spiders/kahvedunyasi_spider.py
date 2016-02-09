# -*- coding: utf-8 -*-
import json

from kahvedunyasi.items import KahvedunyasiItem

import scrapy
from lxml import html


class KahvedunyasiSpiderSpider(scrapy.Spider):
    name = "kahvedunyasi_spider"
    allowed_domains = ["www.kahvedunyasi.com"]
    start_urls = (
        'http://www.kahvedunyasi.com/_ajaxhandler/StoresService.aspx/GetCities',
    )

    cities = dict()

    def parse(self, response):
        # get cities
        yield scrapy.Request("http://www.kahvedunyasi.com/_ajaxhandler/StoresService.aspx/GetCities",
                             callback=self.parse_cities,
                             method='POST',
                             body='{"countryId":1}',
                             headers={
                                 'Content-type': 'application/json',
                             }
                             )

    def parse_cities(self, responce):
        cities = json.loads(responce.body)
        for city in cities['d']['Data']:
            self.cities[city['Id']] = city['Name'].strip()
            body = {'args': {'Country': {'Id': 1},
                             'City': {"Id": city['Id']},
                             'Town': {"Id": -1},
                             'IsCorner': None,
                             "noStores": False
                             }
                    }
            yield scrapy.Request("http://www.kahvedunyasi.com/magazalarimiz/default.aspx/GetStores",
                                 callback=self.parse_magazines,
                                 meta={'city': city['Id']},
                                 method='POST',
                                 body=json.dumps(body),
                                 headers={
                                     'Content-type': 'application/json',
                                 }
                                 )

    def parse_magazines(self, responce):
        magazines = json.loads(responce.body)
        magz = html.fromstring(magazines['d']['Data'].strip())
        city = self.cities[responce.meta['city']]

        for mag in magz.xpath("//div[@class='item']"):
            name = mag.xpath('a//text()')
            coordx = mag.xpath('a/@data-coordx')
            coordy = mag.xpath('a/@data-coordy')
            addr = mag.xpath('p[1]//text()')
            tel = mag.xpath('p[2]//text()[normalize-space()][last()]')

            item = KahvedunyasiItem()

            item['coordx'] = coordx
            item['coordy'] = coordy
            item['name'] = name
            item['addr'] = addr
            item['tel'] = tel
            item['city'] = city

            yield item
