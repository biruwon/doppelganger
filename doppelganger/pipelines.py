# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import hashlib

from scrapy.http import Request
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes

from scrapy.shell import inspect_response


class DoppelgangerPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):

        url = request.url
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation

        folder_name = request.meta['name']

        return 'full/%s/%s.jpg' % (folder_name, image_guid)

    def get_media_requests(self, item, info):
        return [Request(x, meta=item) for x in item.get(self.images_urls_field, [])]