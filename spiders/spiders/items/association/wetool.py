import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class TWetool(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    chat_room_id = mongoengine.StringField()            # 群id
    chat_room_owner_wxid = mongoengine.StringField()    # 群所属人id
    chat_room_member_count = mongoengine.IntField()     # 群人数
    chat_room_nickname = mongoengine.StringField()      # 群名称
    chat_room_avatar = mongoengine.StringField()        # 群头像
    create_at = mongoengine.StringField()  # 创建时间
    update_at = mongoengine.StringField()  # 更新时间