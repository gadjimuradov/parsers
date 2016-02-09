# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import phonenumbers
import re
from sys import stdout
import time

from belinvestbank.utils import check_spider_pipeline, check_spider_close
from lxml import etree
from codecs import getwriter

sout = getwriter("utf8")(stdout)


class BelinvestbankAtmPipeline(object):
    counter = 0

    def company_id(self):
        return u'0001' + unicode(self.counter)

    def __init__(self):
        self.ns = {"xmlns": 'http://www.w3.org/2001/XInclude'}
        self.xml = etree.Element('companies', version='2.1', nsmap=self.ns)

    @check_spider_pipeline
    def process_item(self, item, spider):
        # <companies xmlns:xi="http://www.w3.org/2001/XInclude" version="2.1"></companies>
        xml_item = etree.SubElement(self.xml, 'company')

        xml_id = etree.SubElement(xml_item, 'company-id')
        xml_id.text = self.company_id()  # TODO

        xml_name = etree.SubElement(xml_item, 'name')
        xml_name.text = u'Белинвестбанк, банкомат'

        xml_addr = etree.SubElement(xml_item, 'address', lang=u'by')  # TODO
        xml_addr.text = item['name']

        xml_country = etree.SubElement(xml_item, 'country', lang=u'by')
        xml_country.text = u'Беларусь'

        # <phone>
        #     <number>+7 (343) 375-13-99</number>
        #     <ext>555</ext>
        #     <info>секретарь</info>
        #     <type>phone</type>
        # </phone>
        xml_phone = etree.SubElement(xml_item, 'phone')
        xml_phone_number = etree.SubElement(xml_phone, 'number')
        xml_phone_number.text = u"+375 (17) 239-02-39"
        xml_phone_type = etree.SubElement(xml_phone, 'type')
        xml_phone_type.text = u'phone'
        xml_phone_ext = etree.SubElement(xml_phone, 'ext')
        xml_phone_info = etree.SubElement(xml_phone, 'info')

        # url
        xml_url = etree.SubElement(xml_item, 'url')
        xml_url.text = item['url']

        # <rubric-id>184106414</rubric-id>
        xml_rubric = etree.SubElement(xml_item, 'rubric-id')
        xml_rubric.text = u"184105402"  # Банкомат (184105402)

        # <actualization-date>1305705951000</actualization-date>
        xml_date = etree.SubElement(xml_item, 'actualization-date')
        xml_date.text = unicode(int(round(time.time() * 1000)))

        self.counter += 1

    @check_spider_close
    def close_spider(self, spider):
        doc = etree.tostring(self.xml, pretty_print=True, encoding='unicode')
        sout.write(doc)


class BelinvestbankInfoPipeline(object):
    counter = 0

    def company_id(self):
        return u'0002' + unicode(self.counter)

    def __init__(self):
        self.ns = {"xmlns": 'http://www.w3.org/2001/XInclude'}
        self.xml = etree.Element('companies', version='2.1', nsmap=self.ns)

    @check_spider_pipeline
    def process_item(self, item, spider):
        # <companies xmlns:xi="http://www.w3.org/2001/XInclude" version="2.1"></companies>
        xml_item = etree.SubElement(self.xml, 'company')

        xml_id = etree.SubElement(xml_item, 'company-id')
        xml_id.text = self.company_id()  # TODO

        xml_name = etree.SubElement(xml_item, 'name')
        xml_name.text = u'Белинвестбанк, инфокиоск'

        xml_addr = etree.SubElement(xml_item, 'address', lang=u'by')  # TODO
        xml_addr.text = item['name']

        xml_country = etree.SubElement(xml_item, 'country', lang=u'by')
        xml_country.text = u'Беларусь'

        # <phone>
        #     <number>+7 (343) 375-13-99</number>
        #     <ext>555</ext>
        #     <info>секретарь</info>
        #     <type>phone</type>
        # </phone>
        xml_phone = etree.SubElement(xml_item, 'phone')
        xml_phone_number = etree.SubElement(xml_phone, 'number')
        xml_phone_number.text = u"+375 (17) 239-02-39"
        xml_phone_type = etree.SubElement(xml_phone, 'type')
        xml_phone_type.text = u'phone'
        xml_phone_ext = etree.SubElement(xml_phone, 'ext')
        xml_phone_info = etree.SubElement(xml_phone, 'info')

        # url
        xml_url = etree.SubElement(xml_item, 'url')
        xml_url.text = item['url']

        # <rubric-id>184106414</rubric-id>
        xml_rubric = etree.SubElement(xml_item, 'rubric-id')
        xml_rubric.text = u"31320523497"  # Инфокиоск (31320523497)

        # <actualization-date>1305705951000</actualization-date>
        xml_date = etree.SubElement(xml_item, 'actualization-date')
        xml_date.text = unicode(int(round(time.time() * 1000)))

        self.counter += 1

    @check_spider_close
    def close_spider(self, spider):
        print spider.name
        doc = etree.tostring(self.xml, pretty_print=True, encoding='unicode')
        sout.write(doc)


class BelinvestbankOfficePipeline(object):
    counter = 0

    def company_id(self):
        return u'0003' + unicode(self.counter)

    def __init__(self):
        self.ns = {"xmlns": 'http://www.w3.org/2001/XInclude'}
        self.xml = etree.Element('companies', version='2.1', nsmap=self.ns)

    def validate_tel(self, phs):
        phones = []
        if phs:
            for phone in phs:
                parts = phone.split(')')
                number = re.sub("\D", '', parts[1]).strip()
                parsed = phonenumbers.parse(phone, "BY")
                city_code = unicode(parsed.national_number).replace(number, '').strip()

                phones.append(u"+375" + u" ("+city_code+u") "+number)
        return phones

    @check_spider_pipeline
    def process_item(self, item, spider):
        xml_item = etree.SubElement(self.xml, 'company')

        xml_id = etree.SubElement(xml_item, 'company-id')
        xml_id.text = self.company_id()

        xml_name = etree.SubElement(xml_item, 'name')
        xml_name.text = u'Белинвестбанк, ' + item['name']

        xml_addr = etree.SubElement(xml_item, 'address', lang=u'by')  # TODO
        xml_addr.text = item['address']  # TODO: format

        xml_country = etree.SubElement(xml_item, 'country', lang=u'by')
        xml_country.text = u'Беларусь'

        # <phone>
        #     <number>+7 (343) 375-13-99</number>
        #     <ext>555</ext>
        #     <info>секретарь</info>
        #     <type>phone</type>
        # </phone>
        for phone in self.validate_tel(item['phones']):
            xml_phone = etree.SubElement(xml_item, 'phone')
            xml_phone_number = etree.SubElement(xml_phone, 'number')
            xml_phone_number.text = phone  # TODO: format
            xml_phone_type = etree.SubElement(xml_phone, 'type')
            xml_phone_type.text = u'phone'
            xml_phone_ext = etree.SubElement(xml_phone, 'ext')
            xml_phone_info = etree.SubElement(xml_phone, 'info')

        # url
        xml_url = etree.SubElement(xml_item, 'url')
        xml_url.text = item['url']

        # <rubric-id>184106414</rubric-id>
        xml_rubric = etree.SubElement(xml_item, 'rubric-id')
        xml_rubric.text = u"184105398"  # Банк (31320523497)

        # <actualization-date>1305705951000</actualization-date>
        xml_date = etree.SubElement(xml_item, 'actualization-date')
        xml_date.text = unicode(int(round(time.time() * 1000)))

        self.counter += 1

    @check_spider_close
    def close_spider(self, spider):
        print spider.name
        doc = etree.tostring(self.xml, pretty_print=True, encoding='unicode')
        sout.write(doc)
