# -*- coding: utf-8 -*-
import string
import re
import os
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from doppelganger.items import Actress
from scrapy.shell import inspect_response


class GoogleImagesSpider(CrawlSpider):

    name = "googleimages"
    allowed_domains = ["google.com"]

    start_urls = []
    #for directory_name in os.listdir("./images/bestpornstartdb/full/"):
    #for directory_name in os.listdir("./images/test/full/"):
        #actress_name = directory_name.replace('_', ' ')
        # google_url = 'https://www.google.com/search?q=' + actress_name + ' porn' + '&biw=1536&bih=776&tbm=isch&tbs=isz:m,itp:face&tbm=isch'
        #google_url = 'https://www.google.com/search?q=' + actress_name + ' porn' + '&biw=1536&bih=776&tbm=isch&tbs=isz:m&tbm=isch' # not faces
        #start_urls.append(google_url)

    #start_urls = ['file:///home/arodriguez/tsp/projects/personal/doppelganger/tmp8n_6z1.html']

    def parse(self, response):

        item = Actress()

        value_searched = response.xpath('//input[@id="lst-ib"]/@value').extract()[0]
        actress_name = value_searched.replace('""', '').replace(' ', '_').replace('_porn', '')
        item['name'] = actress_name

        item['image_urls'] = []
        actress_info_list = response.xpath('//div[@class="rg_meta"]/text()').extract()
        for actress_info in actress_info_list[:40]:

            picture_info_dic = json.loads(actress_info)

            item['image_urls'].append(picture_info_dic['tu'])

        return item
