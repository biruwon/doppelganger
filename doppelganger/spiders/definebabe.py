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
    name = "definebabe"
    allowed_domains = ["definebabe.com"]

    #start_urls = ['http://www.definebabe.com/models/h/']
    start_urls = []
    base_path = 'http://www.definebabe.com/models/'
    for letter in string.lowercase:
        start_urls.append(base_path + letter)

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[contains(text(),'Next')]"), follow=True),
        Rule(LinkExtractor(restrict_css='.babes-letter-list'), callback='generate_galley_link', follow=True),
    )

    def generate_galley_link(self, response):

        yield Request(urlparse.urljoin(response.url, 'galleries'), callback=self.get_galleries)

    def get_galleries(self, response):
        actress_name = response.request.url.rsplit('/')[-3]
        selector = '.galleries-list a[href*=' + actress_name + ']::attr(href)'

        gallery_urls = response.css(selector).extract()
        for gallery_url in gallery_urls[0:5]:
            yield Request(urlparse.urljoin(response.url, gallery_url), callback=self.parse_gallery)

    def parse_gallery(self, response):

        actress_name = response.request.url.rsplit('/')[-2]

        item = Actress()
        item['name'] = actress_name

        image_urls = response.css('.gallery-block .thumb a::attr(href)').extract()
        item['image_urls'] = image_urls

        return item