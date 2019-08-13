from collections import namedtuple

import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem

name_id_map = namedtuple('name_id_map', 'name id')

"""
景区信息
"""
MONGO_CONNECT = mongoengine.connect('hq_crawler', host='mongodb://11.75.1.20:27017')  # 连接mongodb


class Spot(BaseItem, mongoengine.Document):
    pk = 1
    id = ObjectId()
    spot_id = mongoengine.IntField()
    ota_id_map = mongoengine.DictField()  # ota名称与id的映射
    spot_name = mongoengine.StringField(max_length=50)
    desc = mongoengine.StringField(max_length=10000)
    tel = mongoengine.StringField(max_length=50)
    website = mongoengine.StringField(max_length=50)
    traffic = mongoengine.StringField(max_length=2000)
    ticket_num = mongoengine.IntField()
    open_time = mongoengine.StringField(max_length=100)
    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)
