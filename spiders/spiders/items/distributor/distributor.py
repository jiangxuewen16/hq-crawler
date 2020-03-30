import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class CDistributor(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    channel_id1 = mongoengine.StringField()  # 渠道ID
    mobile = mongoengine.StringField()  # 手机号
    create_at = mongoengine.StringField()  # 创建时间
    meta = {'strict': False}
