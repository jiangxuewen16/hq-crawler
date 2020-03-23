import time

from scrapy.item import BaseItem


class BaseData(BaseItem):
    distinctId: str = ''
    event: str = ''
    data: dict = {}
    createAt: str = ''

    def __init__(self, event: str, data: dict):
        self.distinctId = '1740009e-5946-44c4-acd7-e07af010a359'
        self.event = event
        self.data = data
        self.createAt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

