import scrapy
from uuid import uuid1


class BaseSpider(scrapy.Spider):
    uuid = ''

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.uuid = uuid1()

    def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
