import mongoengine


class DocUser(mongoengine.Document):
    _id = mongoengine.IntField()
    study = mongoengine.BooleanField()
    type = mongoengine.StringField()
    username = mongoengine.StringField()
    real_name = mongoengine.StringField()
    password = mongoengine.StringField()
    email = mongoengine.StringField()
    passsalt = mongoengine.StringField()
    role = mongoengine.StringField()
    add_time = mongoengine.IntField()
    up_time = mongoengine.IntField()
    __v = mongoengine.IntField()

    meta = {'db_alias': 'passport', 'strict': False}


class DocInterface(mongoengine.Document):
    _id = mongoengine.IntField()
    edit_uid = mongoengine.IntField()
    status = mongoengine.StringField()
    type = mongoengine.StringField()
    req_body_is_json_schema = mongoengine.BooleanField()
    res_body_is_json_schema = mongoengine.BooleanField()
    api_opened = mongoengine.BooleanField()
    index = mongoengine.IntField()
    tag = mongoengine.ListField()
    method = mongoengine.StringField()
    catid = mongoengine.IntField()
    title = mongoengine.StringField()
    path = mongoengine.StringField()
    project_id = mongoengine.IntField()
    req_params = mongoengine.ListField()
    res_body_type = mongoengine.StringField()
    query_path = mongoengine.DictField()
    uid = mongoengine.IntField()
    add_time = mongoengine.IntField()
    up_time = mongoengine.IntField()
    req_query = mongoengine.ListField()
    req_headers = mongoengine.ListField()
    req_body_form = mongoengine.ListField()
    # __v = mongoengine.IntField()
    api_type = mongoengine.IntField()
    desc = mongoengine.StringField()
    markdown = mongoengine.StringField()
    req_body_other = mongoengine.StringField()
    req_body_type = mongoengine.StringField()
    res_body = mongoengine.StringField()

    meta = {'db_alias': 'passport', 'strict': False}
