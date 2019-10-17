import datetime
import json

from apps.models.crawler import ExceptionLog


class ExcLog:
    @classmethod
    def select_all(cls):
        pipeline = [
            {
                '$sort': {
                    "create_at": -1
                }
            },
            {
                '$match': {
                    'create_at': {
                        '$gte': '2000-12-04',
                        '$lt': '2019-12-05'
                    }
                }
            },
            {
                '$skip': 0
            },
            {
                '$limit': 20
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
    def count(cls):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$gte': '2000-12-04',
                        '$lt': '2019-12-05'
                    }
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
