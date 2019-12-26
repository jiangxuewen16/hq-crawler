from collections import namedtuple

import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem

# name_id_map = namedtuple('name_id_map', 'name id')

"""
景区信息
"""


# todo 景区用城市景区的,停止维护
class Spot(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()  # OTA 定义的id
    spot_id = mongoengine.IntField()  # 景区id
    spot_img = mongoengine.ListField()  # 景区图片
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
    spot_favorable = mongoengine.StringField(max_length=100)  # 好评率
    spot_rank = mongoengine.IntField()  # 必玩榜排名
    spot_introduction = mongoengine.StringField()  # 必玩理由
    tag_list = mongoengine.ListField()  # 评论tag

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class CSpot(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    spot_id = mongoengine.StringField()     # 景区ID
    province = mongoengine.StringField()    # 省
    city = mongoengine.StringField()        # 市
    area = mongoengine.StringField()        # 区
    create_at = mongoengine.IntField()      # 创建时间
    name = mongoengine.StringField()        # 景区名
    level = mongoengine.IntField()          # 等级
    t_id = mongoengine.IntField()           # 租户id
    c_id = mongoengine.IntField()           # 客户端id
    is_sale = mongoengine.IntField()        # 是否正在售卖
    promoter_id = mongoengine.StringField()  # 推广者id
    self_employed = mongoengine.IntField()   # 是否自营


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
    c_reply_content = mongoengine.StringField(max_length=2000)  # 回复内容
    c_content = mongoengine.StringField(max_length=2000)  # 评论内容
    c_img = mongoengine.ListField()  # 评论图片列表
    c_from = mongoengine.StringField(max_length=50)  # 评论来源
    # c_tag_list = mongoengine.ListField()  # 评论tag

    create_at = mongoengine.StringField(max_length=50)  # 评论创建时间


class SpotCity(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    city_id = mongoengine.IntField()  # 城市id
    area_pinyin = mongoengine.StringField(max_length=200)  # 城市名称拼音
    area_id = mongoengine.IntField()  # 地区id
    area_name = mongoengine.StringField(max_length=100)  # 地区名称
    city_name = mongoengine.StringField(max_length=100)  # 城市名称

    ota_id = mongoengine.IntField()  # ota 的 id @see spiders.common.OTA
    ota_spot_id = mongoengine.IntField()  # ota 景区id

    s_name = mongoengine.StringField(max_length=100)  # 商品名称
    s_notes = mongoengine.DictField()  # 景区须知
    s_desc = mongoengine.DictField()  # 景区简介
    s_level = mongoengine.StringField(max_length=20)  # 景区级别

    s_img = mongoengine.StringField(max_length=250)  # 景区封面图
    s_score = mongoengine.FloatField()  # 景区评分
    s_comment_num = mongoengine.IntField()  # 评价数量
    s_sale_num = mongoengine.IntField()  # 销量

    s_ticket_num = mongoengine.IntField()  # 门票数量
    s_ticket = mongoengine.DictField()  # 门票列表
    # s_ticket_hotel = mongoengine.DictField()  # 门票+酒店列表
    s_addr = mongoengine.StringField(max_length=500)  # 地区名称
    lat = mongoengine.FloatField()  # 经度
    lng = mongoengine.FloatField()  # 纬度

    create_at = mongoengine.DateTimeField()  # 创建时间
    update_at = mongoengine.DateTimeField()  # 更新时间
