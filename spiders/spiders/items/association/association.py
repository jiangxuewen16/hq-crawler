import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class TAssociation(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    team_leader_id = mongoengine.StringField()  # 团长ID
    team_leader_name = mongoengine.StringField()  # 团长姓名
    team_leader_tel = mongoengine.StringField()  # 团长手机号
    charger_name = mongoengine.StringField()  # 负责人
    charger_id = mongoengine.StringField()  # 负责人ID
    team_group_id = mongoengine.StringField()  # 团长群编码
    custom_name = mongoengine.StringField()  # 地摊单位 （统计覆盖社区数 需要用到）
    belong_team = mongoengine.StringField()  # 所属团队
    belong_team_id = mongoengine.StringField()  # 所属团队ID
    chat_room_id = mongoengine.StringField()  # 群id
    chat_room_owner_wxid = mongoengine.StringField()  # 群所属人id
    chat_room_member_count = mongoengine.IntField()  # 群人数
    char_room_sum = mongoengine.IntField()  # 群数
    chat_room_nickname = mongoengine.StringField()  # 群名称
    chat_room_avatar = mongoengine.StringField()  # 群头像
    channel_id = mongoengine.StringField()  # 渠道id/部门id
    create_at = mongoengine.StringField()  # 创建时间
    update_at = mongoengine.StringField()  # 更新时间


class TContactor(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    charger_name = mongoengine.StringField()  # 负责人
    charger_id = mongoengine.StringField()  # 负责人ID

    create_at = mongoengine.StringField()  # 创建时间
    update_at = mongoengine.StringField()  # 更新时间
