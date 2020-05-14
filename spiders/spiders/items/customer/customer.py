import mongoengine
from bson import ObjectId
from scrapy.item import BaseItem


class CustomerDailyReport(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义

    agent = mongoengine.StringField(max_length=50)  # 管理者名字
    work_id = mongoengine.StringField()  # 工号
    stat_at = mongoengine.StringField()  # 时间
    telephone_proportion = mongoengine.DictField()  # 电话接待数据  {'callin_count':20.00,
    # 'callin_answered_total_time':60.00, 'callout_count':10.00, 'callout_answered_total_time': '',
    # 'callin_ringing_answered_avg_time':'', 'callin_answered_rate':'', 'satisfied':''}
    im_proportion = mongoengine.DictField()  # im接待数据  {
    # 'customer_message_count':60.00, 'agent_message_count':10.00,
    # 'avg_first_answered_seconds':'', 'appraise_avg_score':''}

    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)


class CustomerConsultation(BaseItem, mongoengine.Document):
    pk = 1  # 必须定义
    id = ObjectId()  # 必须定义
    udesk_id = mongoengine.StringField()
    agent = mongoengine.StringField(max_length=50)  # 管理者名字
    work_id = mongoengine.StringField()  # 工号
    nick_name = mongoengine.StringField(max_length=50)  # 客户名称
    stat_at = mongoengine.StringField()  # 时间
    cellphone = mongoengine.StringField()  # 客户电话号码
    tags = mongoengine.StringField()  #
    source_channel = mongoengine.StringField()  # 售前售后
    source_platform = mongoengine.StringField()  # 来源平台
    consulting_scenic_spot = mongoengine.StringField()  # 咨询景区
    consulting_type = mongoengine.StringField()  # 咨询类型
    phone_service_provider = mongoengine.StringField()  # 手机运营商
    province = mongoengine.StringField()  # 省
    city = mongoengine.StringField()  # 市
    create_at = mongoengine.DateTimeField(null=True)
    update_at = mongoengine.DateTimeField(null=True)
