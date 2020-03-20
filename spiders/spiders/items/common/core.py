from scrapy.item import BaseItem


class BaseData(BaseItem):
    str_data: str = ''
    dict_data: dict = {}
