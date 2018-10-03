# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import time
import scrapy

# from crawler_lib import parse
# from crawler_lib import misc


# https://www.hsinchu-cc.gov.tw/search/Issuep.asp

class Spider(scrapy.Spider):
    name = "bills"
    start_urls = [
        "https://www.hsinchu-cc.gov.tw/search/Issuep.asp",
    ]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, encoding='big5')

    def parse(self, response):
        for node in response.xpath('//table/tr/td/table[2]/tr'):
            print 'node:', node
            the_cls = node.xpath('@class').extract_first()
            print "the_cls:", the_cls
            if the_cls != '13-grey':
                continue
            tds = node.xpath('td')
            tds = [td for td in tds]
            if len(tds) < 7:
                continue

            the_date = tds[1].xpath('text()').extract_first()
            print 'the_date:', the_date
            if the_date == u'日期':
                continue

            category = tds[2].xpath('text()').extract_first()
            print 'category:', category[:2]

            abstract = unicode.strip(tds[3].xpath('text()').extract_first())
            print 'abstract:', abstract
            proposed_by = tds[4].xpath('text()').extract_first().split(u'、')
            proposed_by = map(unicode.strip, proposed_by)
            proposed_by = filter(None, proposed_by)
            print 'proposed_by:', proposed_by
            petitioned_by = tds[5].xpath('text()').extract_first().split(u'、')
            petitioned_by = map(unicode.strip, petitioned_by)
            petitioned_by = filter(None, petitioned_by)
            print 'petitioned_by:', petitioned_by
            link = tds[6].xpath('a/@href').extract_first()
            print 'link:', link
            link = re.sub(u'^\.\.', 'https://www.hsinchu-cc.gov.tw/', link)

            item = {}
            item['election_year'] = '2014'
            item['county'] = u'新竹市'

            item['type'] = '-'
            item['category'] = category[:2]
            item['abstract'] = abstract
            item['proposed_by'] = proposed_by
            item['petitioned_by'] = petitioned_by
            item['links'] = [
                {
                    'url': link,
                    'note': 'pdf',
                }
            ]

            print 'item', item

            yield item
