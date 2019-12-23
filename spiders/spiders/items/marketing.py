import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem

"""
营销推广管理者
"""


class Admin(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    name = mongoengine.StringField(max_length=50)  # 管理者名字

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


"""
营销推广账号
"""


class Account(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    type = mongoengine.StringField(max_length=10)
    platform = mongoengine.StringField(max_length=50)
    name = mongoengine.StringField()

    recommend_num = mongoengine.IntField()
    read_num = mongoengine.IntField()
    follow_num = mongoengine.IntField()  # 关注（粉丝）
    income = mongoengine.DecimalField()  # 收入

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


"""
文章
"""


class Article(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    recommend_num = mongoengine.IntField()
    read_num = mongoengine.IntField()
    forward_num = mongoengine.IntField()  # 转发
    like_num = mongoengine.IntField()  # 点赞

    content = mongoengine.StringField()

    create_at = mongoengine.DateTimeField(null=True)  # 文章的创建时间
    update_at = mongoengine.DateTimeField(null=True)


"""
日报表
"""


class DailyReport(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    account_id = mongoengine.ObjectIdField()  # 账号id
    account_name = mongoengine.StringField()  # 账号名称
    recommend_num = mongoengine.IntField()
    read_num = mongoengine.IntField()
    follow_num = mongoengine.IntField()  # 关注（粉丝）
    unfollow_num = mongoengine.IntField()  # 取消关注（粉丝）
    income = mongoengine.DecimalField()  # 收入

