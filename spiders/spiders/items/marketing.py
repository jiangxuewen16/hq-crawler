import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class Admin(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    uname = mongoengine.StringField(max_length=50)
    name = mongoengine.StringField(max_length=50)

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class Account(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    type = mongoengine.StringField(max_length=10)
    platform = mongoengine.StringField(max_length=50)
    name = mongoengine.StringField()

    recommend_num = mongoengine.IntField()
    read_num = mongoengine.IntField()

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class Article(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义