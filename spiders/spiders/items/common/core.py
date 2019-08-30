import mongoengine


class BaseMongoengineDoc(mongoengine.Document):
    def keys(self):
        return ('c_id', 'c_score', 'c_useful_num', 'c_content', 'c_img', 'c_from', 'create_at')

    def __getitem__(self, item):
        return getattr(self, item)