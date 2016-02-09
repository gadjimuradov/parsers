# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from sys import stdout

import re
from scrapy.exceptions import DropItem
from codecs import getwriter


class UnlulerinboylariPipeline(object):
    def validate_int(self, value, length, suffix=False):
        if type(value) == list:
            val = value[0] if value else None
            if val is None:
                return False
        else:
            val = value

        if length is not False:
            val = re.sub("\D", "", val)
            if len(val) != length:
                return False
        return val.strip()

    def validate_str(self, value):
        if type(value) == list:
            for v in value:
                if v.strip():
                    val = v.strip()
                    break
                else:
                    val = None
            if val is None:
                return False
        else:
            val = value

        val = val.replace(':', '')
        if len(val.split('Boy Kilo')) > 1:
            val = val.split('Boy Kilo')[0]
        if len(val.split('Boyu Kilo')) > 1:
            val = val.split('Boyu Kilo')[0]
        return val.strip()

    def process_item(self, item, spider):
        height = float(self.validate_int(item['height'], length=3)) / 100
        weight = int(self.validate_int(item['weight'], length=2))
        name = self.validate_str(item['name']) or ''
        ontoid = u"ext_unlulerinboylari_" + name.replace(' ', '-')

        if height is None and weight is None:
            raise DropItem("Missing weight and height in %s" % item)

        human = {
            "ontoid": ontoid,
            "ids": (
                {
                    "type": u"url",
                    "value": item['url'],
                    "langua": u"tr"
                },
            ),
            "Title": (
                {
                    "value": name
                },
            ),
            "params": {
                "Height": (
                    {
                        "value": height,
                        "unit": u"m"
                    },
                ),
                "Weight": (
                    {
                        "value": weight,
                        "unit": u"kg"
                    },
                )
            },
            "isa": {
                "otype": (
                    {
                        "value": u"Hum"
                    },
                )
            }
        }
        sout = getwriter("utf8")(stdout)
        sout.write(json.dumps(human, ensure_ascii=False) + "\n")
