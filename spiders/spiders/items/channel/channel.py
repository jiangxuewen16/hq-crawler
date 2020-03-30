import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class CChannel(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    channel_id = mongoengine.StringField()  # 渠道ID
    name = mongoengine.StringField()  # 所属团队name
    create_at = mongoengine.StringField()  # 创建时间
    meta = {'strict': False}
