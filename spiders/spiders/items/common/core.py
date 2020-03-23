from scrapy.item import BaseItem


class BaseData(BaseItem):
    distinctId: str = '1740009e-5946-44c4-acd7-e07af010a35'
    event: str = ''
    data: dict = {}
    create_at: str = ''
