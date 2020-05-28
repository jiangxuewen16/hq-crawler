import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class MediaDetail(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    team_group_id = mongoengine.StringField()  # 团长群编码id
    account_id = mongoengine.StringField()  # 抖音id
    uid = mongoengine.StringField()  # 抖音唯一标识
    account = mongoengine.StringField()  # 抖音账号
    name = mongoengine.StringField()  # 姓名/官方账号名
    city = mongoengine.StringField()  # 所在城市
    category_tags = mongoengine.StringField()  # 类别（搞笑 美食）
    introduction = mongoengine.StringField()  # 简介
    is_official = mongoengine.IntField()  # 是否是官方 【0不是1是】
    department = mongoengine.StringField()  # 所属部门
    avatar = mongoengine.StringField()  # 头像

    fans_num = mongoengine.IntField()  # 粉丝数
    fans_logs = mongoengine.ListField()  # 粉丝数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    total_play = mongoengine.IntField()  # 播放量
    play_logs = mongoengine.ListField()  # 播放量爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    total_like = mongoengine.IntField()  # 获赞数
    like_logs = mongoengine.ListField()  # 获赞数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    comment_num = mongoengine.IntField()  # 评论数
    comment_logs = mongoengine.ListField()  # 评论数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    video_num = mongoengine.IntField()  # 作品数
    video_logs = mongoengine.ListField()  # 作品数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    broadcast_num = mongoengine.IntField()  # 直播数
    broadcast_logs = mongoengine.ListField()  # 直播数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]
    repost_num = mongoengine.IntField()  # 转发数
    repost_logs = mongoengine.ListField()  # 转发数爬取日志 [{'num':2,'create_at':'xxx'},{'num':4,'create_at':'xxx'}]

    create_at = mongoengine.StringField()  # 创建时间
    update_at = mongoengine.StringField()  # 更新时间


# 抖音用户表
class DouYinUser(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    uid = mongoengine.StringField()  # 抖音唯一标识
    name = mongoengine.StringField()  # 姓名
    nick_name = mongoengine.StringField()  # 抖音昵称
    account = mongoengine.StringField()  # 抖音账号
    team_name = mongoengine.StringField()  # 部门
    url = mongoengine.StringField()  # 抖音个人中心主页链接
    team_group_id = mongoengine.StringField()  # 团长群编码id
    remarks = mongoengine.StringField()  # 备注

    create_at = mongoengine.StringField()  # 创建时间
    update_at = mongoengine.StringField()  # 更新时间


# 抖音错误表
class MediaError(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    name = mongoengine.StringField()  # 姓名
    department = mongoengine.StringField()  # 部门
    url = mongoengine.StringField()  # url
    team_group_id = mongoengine.StringField()  # 群编码
    create_at = mongoengine.StringField()  # 创建时间
