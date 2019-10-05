import mongoengine


class ExceptionLog(mongoengine.Document):
    event = mongoengine.IntField()
    system_name = mongoengine.StringField()
    platform = mongoengine.StringField()
    level = mongoengine.IntField()
    api_url = mongoengine.StringField()
    trace = mongoengine.StringField()
    file = mongoengine.StringField()
    msg = mongoengine.StringField()
    line = mongoengine.StringField()
    request_id = mongoengine.StringField()
    request_time = mongoengine.StringField()
    request_param = mongoengine.StringField()
