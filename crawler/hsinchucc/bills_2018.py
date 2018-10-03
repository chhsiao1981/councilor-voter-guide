# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import os
import re
import json
import time
import scrapy

from crawler_lib import parse
from crawler_lib import misc


# https://www.hsinchu-cc.gov.tw/search/Issuep.asp

class Spider(scrapy.Spider):
    name = "bills"
    allowed_domains = ["www.hsinchu-cc.gov.tw", ]
    start_urls = ["https://www.hsinchu-cc.gov.tw/"]
    download_delay = 0.5
    county_abbr = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]

    def parse(self, response):
        response = parse.get_decoded_response(response, 'big5')

        for node in response.css('.13-grey'):
            tds = node.xpath('td')
            tds = [td for td in tds]
            if len(tds) < 7:
                continue

            the_date = tds[1].xpath('text()')
            if the_date == '日期':
                continue

            category = tds[2].xpath('text()')[:2]
            abstract = tds[3].xpath('text()')
            proposed_by = tds[4].xpath('text()').split('、')
            petitioned_by = tds[5].xpath('text()').split('、')
            link = re.sub('\.\.', 'https://www.hsinchu-cc.gov.tw/', tds[6].xpath('@href').extract_first())

            item = {}
            item['election_year'] = '2014'
            item['county'] = u'新竹市'

            item['type'] = ''
            item['category'] = category
            item['abstract'] = abstract
            item['proposed_by'] = proposed_by
            item['petitioned_by'] = petitioned_by
            item['links'] = [
                {
                    'url': link,
                    'note': 'pdf',
                }
            ]

            yield item
