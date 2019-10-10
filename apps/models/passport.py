import mongoengine

"""
api用户模型
"""


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


"""
api接口模型
"""


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
    __v = mongoengine.IntField()
    api_type = mongoengine.IntField()
    desc = mongoengine.StringField()
    markdown = mongoengine.StringField()
    req_body_other = mongoengine.StringField()
    req_body_type = mongoengine.StringField()
    res_body = mongoengine.StringField()

    meta = {'db_alias': 'passport', 'strict': False}


"""
api项目模型
"""


class DocProject(mongoengine.Document):
    _id = mongoengine.IntField()
    switch_notice = mongoengine.BooleanField()
    is_mock_open = mongoengine.BooleanField()
    strice = mongoengine.BooleanField()
    is_json5 = mongoengine.BooleanField()
    name = mongoengine.StringField()
    desc = mongoengine.StringField()
    basepath = mongoengine.StringField()
    members = mongoengine.ListField()
    project_type = mongoengine.ListField()
    uid = mongoengine.IntField()
    group_id = mongoengine.IntField()
    icon = mongoengine.StringField()
    color = mongoengine.StringField()
    add_time = mongoengine.IntField()
    up_time = mongoengine.IntField()
    env = mongoengine.ListField()
    tag = mongoengine.ListField()
    __v = mongoengine.IntField()

    meta = {'db_alias': 'passport', 'strict': False}
