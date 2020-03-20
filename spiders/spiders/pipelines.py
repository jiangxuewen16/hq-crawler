# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import mongoengine
from pykafka import KafkaClient
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem

from spiders import settings


class SpidersPipeline(object):
    def __init__(self):
        kafka_hosts = settings.KAFKA_HOSTS
        hosts = ",".join(kafka_hosts)

        # 初始化client
        self._client = KafkaClient(hosts=hosts)
        kafka_topic = settings.KAFKA_TOPIC.encode(encoding="UTF-8")
        if kafka_topic not in self._client.topics:
            raise Exception('scrapy kafka topic not exists')

        # 初始化Producer 需要把topic name变成字节的形式
        self._producer = self._client.topics[kafka_topic].get_producer()

    def process_item(self, item, spider: Crawler):
        if type(item).__name__ == 'BaseData':
            self._producer.produce(item.data.encode())
        else:
            item.save(force_insert=False, validate=False, clean=True, )

    def close_spider(self, spider):
        self._producer.stop()


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
        print('=' * 20, spider, '=' * 20)
        if type(item).__name__ == "str":
            kafka_client = settings.KAFKA_CLIENT
            kafka_client.topics(settings.KAFKA_TOPIC.encode())
            kafka_client.produce(item.encode())
        else:
            item.save(force_insert=False, validate=False, clean=True, )
