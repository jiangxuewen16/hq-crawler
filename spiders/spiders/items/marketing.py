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
    platform = mongoengine.StringField()    # 平台名称
    account_name = mongoengine.StringField()  # 账号名称

    # 曝光
    exposure_num = mongoengine.IntField()  # 曝光量（推荐量 + 阅读量）
    recommend_num = mongoengine.IntField()  # 推荐量
    read_num = mongoengine.IntField()  # 阅读量（小程序访问人数）
    follow_num = mongoengine.IntField()  # 关注（粉丝）
    sex_proportion = mongoengine.IntField()  # 总粉丝男女比例

    # 收益
    total_income = mongoengine.DecimalField()  # 总收入
    drawing = mongoengine.DecimalField()  # 总提现
    balance = mongoengine.DecimalField()  # 总余额（实时）

    # 文章曝光
    forward_num = mongoengine.IntField()  # 转发
    like_num = mongoengine.IntField()  # 点赞
    comment_num = mongoengine.IntField()  # 评论量

    account_home = mongoengine.StringField()  # 个人中心地址
    authorization_information = mongoengine.StringField()  # 授权信息（用于爬虫）

    is_enable = mongoengine.BooleanField()  # 是否启用

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


"""
文章
"""


class Article(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    platform = mongoengine.StringField()  # 平台类型
    account_id = mongoengine.ObjectIdField()  # 账号id
    account_name = mongoengine.StringField()  # 账号名称
    admin_id = mongoengine.ObjectIdField()  # 管理者id
    admin_name = mongoengine.StringField()  # 管理者名字

    recommend_num = mongoengine.IntField()  # 推荐量
    read_num = mongoengine.IntField()  # 阅读量
    forward_num = mongoengine.IntField()  # 转发
    like_num = mongoengine.IntField()  # 点赞
    comment_num = mongoengine.IntField()  # 评论量

    content = mongoengine.StringField()  # 文章内容

    create_at = mongoengine.DateTimeField(null=True)  # 文章的创建时间
    update_at = mongoengine.DateTimeField(null=True)


"""
日报表
"""


class DailyReport(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    platform = mongoengine.StringField()  # 平台类型
    account_id = mongoengine.ObjectIdField()  # 账号id
    account_name = mongoengine.StringField()  # 账号名称
    admin_id = mongoengine.ObjectIdField()  # 管理者id
    admin_name = mongoengine.StringField()  # 管理者名字

    day_time = mongoengine.DateTimeField(null=True)  # 日期

    # 曝光
    exposure_num = mongoengine.IntField()  # 曝光量（推荐量 + 阅读量）
    recommend_num = mongoengine.IntField()  # 推荐量
    read_num = mongoengine.IntField()  # 阅读量（小程序访问人数）

    # 粉丝
    follow_num = mongoengine.IntField()  # 当日关注（粉丝）
    unfollow_num = mongoengine.IntField()  # 当日取消关注（粉丝）
    add_follow_num = mongoengine.IntField()  # 净增关注（粉丝）[当日关注 - 当日取消关注] [小程序新增用户]
    total_follow_num = mongoengine.IntField()  # 总关注（粉丝）[小程序累计用户]
    sex_proportion = mongoengine.IntField()  # 总粉丝男女比例

    # 文章曝光
    forward_num = mongoengine.IntField()  # 转发
    like_num = mongoengine.IntField()  # 点赞
    comment_num = mongoengine.IntField()  # 评论量

    # 平台流量

    # 营收
    income = mongoengine.DecimalField()  # 收入
    drawing = mongoengine.DecimalField()  # 提现
    balance = mongoengine.DecimalField()  # 余额（总金额）

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)
