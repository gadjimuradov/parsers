# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sys import stdout
import time

import re
from codecs import getwriter
from lxml import etree
from scrapy.exceptions import DropItem

sout = getwriter("utf8")(stdout)


class LifecomPipeline(object):
    counter = 0

    def company_id(self):
        return u'0004' + unicode(self.counter)

    def __init__(self):
        self.ns = {"xmlns": 'http://www.w3.org/2001/XInclude'}
        self.xml = etree.Element('companies', version='2.1', nsmap=self.ns)

    def validate_str(self, value):
        if type(value) == list:
            val = None
            for v in value:
                if v.strip():
                    val = v.strip()
                    break
            if val is None:
                return u''
        else:
            val = value
        return val.strip()

    def validate_tel(self, phone):
        phone = self.validate_str(phone)
        phone_list = phone.split(',')
        phones = []
        if phone_list:
            for phone in phone_list:
                phone = re.sub("\D", "", phone)
                phone = phone.strip()

                phones.append(u"+" + phone[:3] + u" ("+phone[3:5]+u") "+phone[5:])
        return phones

    def process_item(self, item, spider):

        name = self.validate_str(item['name'])
        address = self.validate_str(item['address'])
        phone = self.validate_tel(item['phone'])

        if name.find(u'Связной') >= 0:
            raise DropItem()

        if name.find(u'Евросеть') >= 0:
            raise DropItem()

        xml_item = etree.SubElement(self.xml, 'company')

        xml_id = etree.SubElement(xml_item, 'company-id')
        xml_id.text = self.company_id()  # TODO

        xml_name = etree.SubElement(xml_item, 'name')
        xml_name.text = name

        xml_addr = etree.SubElement(xml_item, 'address', lang=u'by')  # TODO
        xml_addr.text = u"город "+self.validate_str(item['city'])+u', '+address  # TODO: format

        xml_country = etree.SubElement(xml_item, 'country', lang=u'by')
        xml_country.text = u'Беларусь'

        # <phone>
        #     <number>+7 (343) 375-13-99</number>
        #     <ext>555</ext>
        #     <info>секретарь</info>
        #     <type>phone</type>
        # </phone>
        if type(phone) == list and phone:
            for ph in phone:
                xml_phone = etree.SubElement(xml_item, 'phone')
                xml_phone_number = etree.SubElement(xml_phone, 'number')
                xml_phone_number.text = ph
                xml_phone_type = etree.SubElement(xml_phone, 'type')
                xml_phone_type.text = u'phone'
                xml_phone_ext = etree.SubElement(xml_phone, 'ext')
                xml_phone_info = etree.SubElement(xml_phone, 'info')
        elif phone:
            xml_phone = etree.SubElement(xml_item, 'phone')
            xml_phone_number = etree.SubElement(xml_phone, 'number')
            xml_phone_number.text = phone
            xml_phone_type = etree.SubElement(xml_phone, 'type')
            xml_phone_type.text = u'phone'
            xml_phone_ext = etree.SubElement(xml_phone, 'ext')
            xml_phone_info = etree.SubElement(xml_phone, 'info')

        # url
        xml_url = etree.SubElement(xml_item, 'url')
        xml_url.text = item['url']

        # <rubric-id>184106414</rubric-id>
        xml_rubric = etree.SubElement(xml_item, 'rubric-id')
        xml_rubric.text = u"184107789"  # Салон связи(184107789)

        # <actualization-date>1305705951000</actualization-date>
        xml_date = etree.SubElement(xml_item, 'actualization-date')
        xml_date.text = unicode(int(round(time.time() * 1000)))

        self.counter += 1

    def close_spider(self, spider):
        doc = etree.tostring(self.xml, pretty_print=True, encoding='unicode')
        sout.write(doc)
