import datetime
import json

from apps.models.crawler import ExceptionLog
from apps.models.passport import DocInterface, DocUser, DocProject


class ExcLog:
    @classmethod
    def select_all(cls, skip, limit, condition):
        pipeline = [
            {
                '$sort': {
                    "create_at": -1
                }
            },
            {
                '$match': {
                    "$and": [
                        {
                            "create_at": {
                                "$gte": condition['begin_date'] + " 00:00:00"
                            }
                        },
                        {
                            "create_at": {
                                "$lte": condition['end_date'] + " 23:59:59"
                            }
                        }
                    ]
                }
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            },
            {
                '$project': {
                    '_id': 0
                }
            }
        ]
        logs = ExceptionLog.objects.aggregate(*pipeline)
        L = []
        for p in logs:
            p['request_param'] = json.loads(p['request_param'])
            p['request_param'] = str(p['request_param'])
            L.append(dict(p))
        return L

    @classmethod
    def count(cls, condition):
        pipeline = [
            {
                '$match': {
                    "$and": [
                        {
                            "create_at": {
                                "$gte": condition['begin_date'] + " 00:00:00"
                            }
                        },
                        {
                            "create_at": {
                                "$lte": condition['end_date'] + " 23:59:59"
                            }
                        }
                    ]
                }
            },
            {
                '$count': "count"
            }
        ]
        logs = ExceptionLog.objects.aggregate(*pipeline)
        L = []
        for p in logs:
            L.append(dict(p))
        return L[0]['count']

    @classmethod
    def group_by_name(cls, condition):
        pipeline = [
            {
                '$group': {
                    '_id': {
                        'api_url': '$api_url'
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        logs = ExceptionLog.objects.aggregate(*pipeline)
        L = []
        for p in logs:
            detail = ExcLog.find_doc_detail(p['_id']['api_url'])
            # detail = ExcLog.find_doc_detail('/order/order_new/createNew')
            p['title'] = detail['title']
            p['username'] = detail['username']
            p['email'] = detail['email']
            p['project_username'] = detail['project_username']
            p['project_email'] = detail['project_email']
            L.append(dict(p))
        return L

    # 根据api_url获取 详细信息
    @classmethod
    def find_doc_detail(cls, url):
        docInterface = DocInterface.objects(path=url).fields(uid=1, title=1, _id=1).first()
        result = {"title": "未知", "username": "未知", "email": "未知", "project_username": "未知", "project_email": "未知"}
        if docInterface:
            result['title'] = docInterface.title
            docProject = DocProject.objects(docInterface.project_id).fields(uid=1).first()
            projectUser = DocUser.objects(_id=docProject.uid).fields(_id=1, email=1).first()
            docUser = DocUser.objects(_id=docInterface.uid).first()
            if docUser:
                result['username'] = docUser.username
                result['email'] = docUser.email
            else:
                pass
            if projectUser:
                result['project_username'] = projectUser.username
                result['project_email'] = projectUser.email
            else:
                pass
        else:
            pass
        return result
        # ExcLog.find_doc_detail()
