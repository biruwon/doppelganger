# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from doppelganger.items import Actress
from scrapy.shell import inspect_response
import re


class AdultfilmdatabaseSpider(CrawlSpider):
    name = "adultfilmdatabase"
    allowed_domains = ["adultfilmdatabase.com"]
    start_urls = [
        'http://www.adultfilmdatabase.com/browse.cfm?filter=&imageFlag=1&genderFilter=&eyeFilter=&hairFilter=&startFilter=&type=actor'
        #'http://www.adultfilmdatabase.com/browse.cfm?filter=an&imageFlag=1&genderFilter=&eyeFilter=&hairFilter=&startFilter=&type=actor' # 2 pages
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//td[@class='px11'][2]/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//tr[@class='bgLG']"), callback='parse_actress_links', follow=True),
    )

    def parse_actress_links(self, response):
        #inspect_response(response, self)
        actress_path = response.request.url.rsplit('/')[-2]
        actress_name = actress_path.rpartition('-')[0]
        #actress_id = re.search(r'\d+', actress_path).group()
        actress_id = re.search(r'\d+', response.url).group()
        image_url = 'http://www.adultfilmdatabase.com/ActorImage.cfm?ActorID=' + actress_id

        request = Request(image_url, callback=self.get_image)
        request.meta['actress_name'] = actress_name

        return request

    def get_image(self, response):
        item = Actress()
        item['image_urls'] = ['http://www.adultfilmdatabase.com' + response.xpath('//img/@src').extract_first()]
        item['name'] = response.meta['actress_name']
        return item
