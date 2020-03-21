from scrapy.item import BaseItem


class BaseData(BaseItem):
    event: str = ''
    data: dict = {}
    create_at: str = ''
