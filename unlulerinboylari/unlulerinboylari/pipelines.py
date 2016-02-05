# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import re
from scrapy.exceptions import DropItem


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

        if suffix:
            val = val.strip() + ' ' + suffix
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
        return val.strip()

    def process_item(self, item, spider):
        print item
        height = self.validate_int(item['height'], length=3, suffix='cm')
        weight = self.validate_int(item['weight'], length=2, suffix='kg')
        name = self.validate_str(item['name']) or ''

        if height is None and weight is None:
            raise DropItem("Missing price in %s" % item)

        human = {
            "ontoid": "ext_unlulerinboylari_zihni-goktay",
            "ids": (
                {
                    "type": "url",
                    "value": item['url'],
                    "langua": "tr"
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
                        "value": height
                    },
                ),
                "Weight": (
                    {
                        "value": weight
                    },
                )
            },
            "isa": {
                "otype": (
                    {
                        "value": "Hum"
                    },
                )
            }
        }

        print json.dumps(human, sort_keys=True)
