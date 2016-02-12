# -*- coding: utf-8 -*-
from sys import stdout

import re
from codecs import getwriter

sout = getwriter("utf8")(stdout)


class KahvedunyasiPipeline(object):
    header = u"original-id,name-tr,name-alt-tr,address-tr,country-tr,province-tr,district-tr,sub-district-tr,locality-tr,street-tr,street-side-tr,house,address-add-tr,landmark-tr,lon,lat,phone,url,rubric-id,working-time,actualization-date,rubric-keys,source-url,rubric-tr,chain-id"

    def __init__(self):
        sout.write(self.header + "\n")

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
        return int(val.strip())

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

        return val.strip()

    def validate_tel(self, value):
        if type(value) == list:
            for v in value:
                if v.strip() and v.strip() != 'T:':
                    val = v.strip()
                    break
                else:
                    val = None
            if val is None:
                return False
        else:
            val = value

        return u'+90 (' + val[1:4].strip() + u') ' + val[4:].strip()

    def process_item(self, item, spider):
        sout.write(','.join([
            '',  # original-id
            self.validate_str(item['name']),  # name-tr
            '',  # name-alt-tr
            self.validate_str(item['addr']),  # address-tr
            u'Türkiye',  # country-tr
            self.validate_str(item['city']),  # province-tr
            '',  # district-tr
            '',  # sub-district-tr
            '',  # locality-tr,
            '',  # street-tr,
            '',  # street-side-tr,
            '',  # house,
            '',  # address-add-tr,
            '',  # landmark-tr,
            self.validate_str(item['coordy']),  # lat,
            self.validate_str(item['coordx']),  # lon,
            self.validate_tel(item['tel']) or '',  # phone,
            u'http://www.kahvedunyasi.com/magazalarimiz/',  # url,
            '',  # rubric-id,
            '',  # working-time,
            '',  # actualization-date,
            '',  # rubric-keys,
            '',  # source-url,
            '',  # rubric-tr,
            '',  # chain-id
        ]) + "\n")
