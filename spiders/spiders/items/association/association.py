import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class Association(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    team_leader_id = mongoengine.IntField()  # 团长ID
    team_leader_name = mongoengine.StringField()  # 团长姓名
    team_leader_tel = mongoengine.StringField()  # 团长手机号
    charger_name = mongoengine.StringField()  # 负责人

    create_at = mongoengine.DateTimeField()  # 创建时间
    update_at = mongoengine.DateTimeField()  # 更新时间
