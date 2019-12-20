import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class OPrice(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()  # ota 的 id @see spiders.common.OTA
    ota_spot_id = mongoengine.IntField()  # ota 景区id

    low_price = mongoengine.DecimalField()  # 最低价
    high_price = mongoengine.DecimalField()  # 最高价
    low_cut = mongoengine.DecimalField()  # 最低立减
    high_back = mongoengine.DecimalField()  # 最多赠券
    ota_product = mongoengine.ListField()  # 产品详情列表
    create_at = mongoengine.DateTimeField()  # 创建时间
    update_at = mongoengine.DateTimeField()  # 更新时间
    seller_nick = mongoengine.StringField()  # 旅行社名称


class OPriceCalendar(BaseItem, mongoengine.Document):  # 价格日历
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    ota_id = mongoengine.IntField()  # ota 的 id @see spiders.common.OTA
    ota_spot_id = mongoengine.IntField()  # ota 景区id
    type_id = mongoengine.IntField()  # 票型id
    pre_price = mongoengine.DecimalField()  # 均价
    create_at = mongoengine.DateTimeField()  # 创建时间
    type_key = mongoengine.StringField()  # 类型关键字
