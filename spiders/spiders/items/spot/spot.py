from collections import namedtuple

import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem

name_id_map = namedtuple('name_id_map', 'name id')

"""
景区信息
"""


class Spot(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()
    spot_id = mongoengine.IntField()
    ota_spot_id = mongoengine.DictField()  # ota名称与id的映射
    spot_name = mongoengine.StringField(max_length=50)
    desc = mongoengine.StringField(max_length=10000)
    tel = mongoengine.StringField(max_length=50)
    website = mongoengine.StringField(max_length=50)
    traffic = mongoengine.StringField(max_length=2000)
    ticket_num = mongoengine.IntField()
    open_time = mongoengine.StringField(max_length=100)
    comment_num = mongoengine.IntField()

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class SpotComment(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()
    ota_spot_id = mongoengine.IntField()
    u_id = mongoengine.IntField()
    u_avatar = mongoengine.StringField(max_length=500)
    u_url = mongoengine.StringField(max_length=50)
    u_level = mongoengine.StringField(max_length=10)
    u_name = mongoengine.StringField(max_length=50)
    u_avg_price = mongoengine.DecimalField()

    c_tag = mongoengine.DictField()
    c_id = mongoengine.IntField()
    c_score = mongoengine.IntField()
    c_useful_num = mongoengine.IntField()
    c_content = mongoengine.StringField(max_length=2000)
    c_img = mongoengine.ListField()
    c_from = mongoengine.StringField(max_length=50)

    create_at = mongoengine.StringField(max_length=50)
