# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mongoengine
from scrapy.exceptions import DropItem


class SpidersPipeline(object):
    def process_item(self, item, spider):
        return item


"""
mongoengine 存储爬取的数据
主要在模型创建自定的类，且继承 mongoengine.Document
"""


class MongoDBPipeline(object):

    # def __init__(self):
    #     self.ids_seen = set()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        item.save(force_insert=False, validate=False, clean=True, )
