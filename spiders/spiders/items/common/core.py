import time

from scrapy.item import BaseItem
from spiders import settings


class BaseData(BaseItem):
    distinctId: str = ''
    event: str = ''
    data: dict = {}
    createAt: str = ''

    def __init__(self, event: str, data: dict):
        self.distinctId = settings.DISTINCT_ID
        self.event = event
        self.data = data
        self.createAt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

