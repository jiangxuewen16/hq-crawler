# import mongoengine
# from bson import ObjectId
# from django.core.cache import cache
# from scrapy.item import BaseItem
#
# from core.lib.command import Command
#
#
# class SServerItem(BaseItem, mongoengine.Document, Command):
#     pk = 1  # 必须定义
#     id = ObjectId()  # 必须定义
#
#     name = mongoengine.StringField()
#     key = mongoengine.StringField()
#     command = mongoengine.StringField()
#     pid = mongoengine.StringField()
#
#     remark = mongoengine.StringField()
#
#     create_at = mongoengine.DateTimeField(null=True)
#     update_at = mongoengine.DateTimeField(null=True)
#
#
# class ServerHandle(object):
#
#     def __init__(self):
#
#         pass
#
#     @classmethod
#     def get_list(cls) -> list:
#         return cache.get()
#
#     @classmethod
#     def reload(cls, key: str = None) -> bool:
#         if not key:
#             server_list = SServerItem.objects().all()
#             for item in server_list:
#
#         if key:
#             serverItem = SServerItem.objects(key=key).first()
#             if not serverItem:
#
#         # do something
#
#     @classmethod
#     def stop(self, key: str = None) -> bool:
#         pass
#
#     @classmethod
#     def start(self, key: str = None) -> bool:
#         pass
#
#     @classmethod
#     def add(self, info: ServerItem) -> bool:
#         pass
#
#     @classmethod
#     def delete(self, key: str) -> bool:
#         pass
#
#
#     def _do_command(self):
#
