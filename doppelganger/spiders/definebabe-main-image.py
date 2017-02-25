# -*- coding: utf-8 -*-
import string
import re
import urlparse
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from doppelganger.items import Actress
from scrapy.shell import inspect_response


class DefinebabeSpider(CrawlSpider):
    name = "definebabe-main-image"
    allowed_domains = ["definebabe.com"]

    #start_urls = ['http://www.definebabe.com/models/a/']
    start_urls = []
    base_path = 'http://www.definebabe.com/models/'
    for letter in string.lowercase:
        start_urls.append(base_path + letter)

    rules = (
        # Only extracts next pages but not active, comment it and change parse_page to parse to get active pages
        #Rule(LinkExtractor(restrict_xpaths='//a[contains(@href, "page")]'), callback="parse_page", follow=True),
    )

    def parse_page(self, response):

        actress_list = response.css('.list-item')

        for actress in actress_list:
            yield self.get_main_image(actress)

    def get_main_image(self, actress):

        actress_name = actress.xpath('a/@href').extract_first().rsplit('/')[-2]

        item = Actress()
        item['name'] = actress_name

        image_urls = actress.css('.lazy').xpath('@data-original').extract()
        item['image_urls'] = image_urls

        print image_urls
        return item