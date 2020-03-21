from scrapy.item import BaseItem


class BaseData(BaseItem):
    event:str = ''
    str_data: str = ''
    dict_data: dict = {}
    create_at:str = ''
