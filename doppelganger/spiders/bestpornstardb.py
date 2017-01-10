# -*- coding: utf-8 -*-
import string
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from doppelganger.items import Actress
from scrapy.shell import inspect_response


class BestpornstardbSpider(CrawlSpider):
    name = "bestpornstardb"
    allowed_domains = ["bestpornstardb.com"]

    #start_urls = ['http://www.bestpornstardb.com/stars/A']
    start_urls = []
    base_path = 'http://www.bestpornstardb.com/stars/'
    for letter in string.uppercase:
        start_urls.append(base_path + letter)

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//div[@class='float2']/a"), callback='parse_actress_response', follow=True),
    )

    def parse_actress_response(self, response):

        actress_name = response.request.url.rsplit('/')[-2]

        item = Actress()
        item['name'] = actress_name

        image_urls = response.xpath('//img[@class="t"]/@src').extract()
        item['image_urls'] = image_urls

        return item
