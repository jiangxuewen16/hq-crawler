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

    ota_id = mongoengine.IntField()  # OTA 定义的id
    spot_id = mongoengine.IntField()  # 景区id
    ota_spot_id = mongoengine.DictField()  # ota名称与id的映射
    spot_name = mongoengine.StringField(max_length=50)
    spot_score = mongoengine.FloatField()  # ota平台景区评分
    avg_price = mongoengine.FloatField()  # 景区的平均消费
    desc = mongoengine.StringField(max_length=10000)
    tel = mongoengine.StringField(max_length=50)
    website = mongoengine.StringField(max_length=50)
    traffic = mongoengine.StringField(max_length=2000)
    ticket_num = mongoengine.IntField()
    open_time = mongoengine.StringField(max_length=100)
    comment_num = mongoengine.IntField()
    addr = mongoengine.StringField(max_length=100)

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class SpotComment(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()  # ota 的 id @see spiders.common.OTA
    ota_spot_id = mongoengine.IntField()  # ota 景区id
    goods_name = mongoengine.StringField(max_length=100)  # 评价的商品名称
    goods_id = mongoengine.IntField()  # 评价的商品id

    u_id = mongoengine.IntField()  # 用户id
    u_avatar = mongoengine.StringField(max_length=500)  # 用户头像
    u_url = mongoengine.StringField(max_length=50)  # 用户个人中心（空间）
    u_level = mongoengine.StringField(max_length=10)  # 用户等级
    u_name = mongoengine.StringField(max_length=50)  # 用户昵称
    u_avg_price = mongoengine.DecimalField()  # 用户的平均消费

    c_tag = mongoengine.DictField()  # tag列表
    c_id = mongoengine.IntField()  # 评论id
    c_score = mongoengine.FloatField()  # 评分
    c_useful_num = mongoengine.IntField()  # 赞数量
    c_reply_num = mongoengine.IntField()  # 回复数量
    c_content = mongoengine.StringField(max_length=2000)  # 评论内容
    c_img = mongoengine.ListField()  # 评论图片列表
    c_from = mongoengine.StringField(max_length=50)  # 评论来源

    create_at = mongoengine.StringField(max_length=50)  # 评论创建时间
