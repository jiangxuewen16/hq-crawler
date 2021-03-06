# from spiders.items.spot.spot import Spot
import datetime
import json
import re
import queue
from django.utils.autoreload import logger

from apps.api.common.helper.helper import getDayList
from spiders.common import OTA
from spiders.items.association import douyin
from spiders.items.spot import spot

spot_queue = queue.Queue()
spot_queue_list = queue.Queue()


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


def get_three_type(spot_city_s):
    L = []
    for p in spot_city_s:
        L.append(dict(p))
    count_down = 0
    count_up = 0
    for m in L:
        score = m['_id']['c_score']
        count = m['count']
        if not score:
            count_down = count + count_down
        else:
            count_up = count + count_up
    K = {'total': count_down + count_up, 'count_up': count_up, 'count_down': count_down}
    return K


# class SpotModel(Spot):
#     pass


class SpotComment:
    @classmethod
    def today_total_comment(cls):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$gte': str(datetime.date.today())
                        # '$lt': '2018-12-05'
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}},
                  'count': {'$sum': 1}
                  }
             }]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L
        # return get_three_type(spot_city_s)

    @classmethod
    def yesterday_total_comment(cls):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$lt': str(datetime.date.today()),
                        '$gte': str(get_yesterday())
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}},
                  'count': {'$sum': 1}
                  }
             }]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L
        # return get_three_type(spot_city_s)

    @classmethod
    def ota_list_comment(cls, condition, skip, limit, sort):
        pipeline = [
            {
                '$lookup': {
                    'from': "spot",
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot"
                }
            },
            {
                '$unwind': {
                    'path': "$spot",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': "$_id",
                    'ota_id': "$ota_id",
                    'ota_spot_id': "$ota_spot_id",
                    'u_id': "$u_id",
                    'u_avatar': "$u_avatar",
                    'u_level': "$u_level",
                    'u_name': "$u_name",
                    'c_tag': "$c_tag",
                    'c_id': "$c_id",
                    'c_score': "$c_score",
                    'c_content': "$c_content",
                    'c_img': "$c_img",
                    'c_from': "$c_from",
                    'create_at': "$create_at",
                    'update_at': "$update_at",
                    'spot_name': "$spot.spot_name"
                }
            },
            {
                '$sort': {sort: -1}
            },
            {
                '$match': {
                    '$and': [
                        {'$or': [
                            {'u_name': {'$regex': '.*' + condition['check_name'] + '.*'}},
                            {'_id': {'$regex': '.*' + condition['check_name'] + '.*'}},
                        ]},
                        {
                            'create_at': {
                                '$gte': condition['begin_date'],
                                '$lt': condition['end_date']
                            }
                        },
                        {
                            'c_score': {
                                '$gt': condition['down_score'],
                                '$lte': condition['up_score']
                            }
                        },
                        {
                            'spot_name': condition['spot_name']
                        },
                        {
                            'ota_id': {'$in': condition['ota_id']}
                        }
                    ]
                }
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            p['_id'] = str(p['_id'])
            L.append(dict(p))
        return L

    @classmethod
    def list_comment(cls, condition, skip, limit, sort):
        pipeline = [
            {
                '$lookup': {
                    'from': "spot",
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot"
                }
            },
            {
                '$unwind': {
                    'path': "$spot",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': "$_id",
                    'ota_id': "$ota_id",
                    'ota_spot_id': "$ota_spot_id",
                    'u_id': "$u_id",
                    'u_avatar': "$u_avatar",
                    'u_level': "$u_level",
                    'u_name': "$u_name",
                    'c_tag': "$c_tag",
                    'c_id': "$c_id",
                    'c_score': "$c_score",
                    'c_content': "$c_content",
                    'c_img': "$c_img",
                    'c_from': "$c_from",
                    'create_at': "$create_at",
                    'update_at': "$update_at",
                    'spot_name': "$spot.spot_name"
                }
            },
            {
                '$sort': {sort: -1}
            },
            {
                '$match': {
                    '$and': [
                        {'$or': [
                            {'u_name': {'$regex': '.*' + condition['check_name'] + '.*'}},
                            {'_id': {'$regex': '.*' + condition['check_name'] + '.*'}},
                        ]},
                        {
                            'create_at': {
                                '$gte': condition['begin_date'],
                                '$lt': condition['end_date']
                            }
                        },
                        {
                            'c_score': {
                                '$gt': condition['down_score'],
                                '$lte': condition['up_score']
                            }
                        },
                        {
                            'ota_id': {'$in': condition['ota_id']}
                        }
                    ]
                }
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            p['_id'] = str(p['_id'])
            L.append(dict(p))
        return L

    @classmethod
    def total_comment(cls, condition):
        pipeline = [
            {
                '$match': {
                    '$and': [
                        {'$or': [
                            {'u_name': {'$regex': '.*' + condition['check_name'] + '.*'}},
                            {'_id': {'$regex': '.*' + condition['check_name'] + '.*'}},
                        ]},
                        {
                            'create_at': {
                                '$gte': condition['begin_date'],
                                '$lt': condition['end_date']
                            }
                        },
                        {
                            'c_score': {
                                '$gt': condition['down_score'],
                                '$lte': condition['up_score']
                            }
                        },
                        # {
                        #     'ota_id': condition['ota_id']
                        # }
                        {
                            'ota_id': {'$in': condition['ota_id']}
                        }
                    ]
                }
            },
            {
                '$count': "count"
            }

        ]
        count = spot.SpotComment.objects().aggregate(*pipeline)
        L = []
        for p in count:
            L.append(dict(p))
        if len(L) < 1:
            return 0
        else:
            return L[0]['count']


class Spot:
    @classmethod
    def list_spot_array(cls):
        pipeline = [
            {
                '$project': {
                    '_id': 0,
                    'ota_spot_id': 1,
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p)['ota_spot_id'])
        return L

    @classmethod
    def list_spot_select(cls):
        pipeline = [
            {
                '$project': {
                    '_id': 0,
                    'spot_name': 1,
                    'ota_spot_id': 1,
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def today_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot_comment',
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot_comments"
                }
            },
            {
                '$unwind': {
                    'path': "$spot_comments",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ota_spot_id': '$spot_comments.ota_spot_id',
                    'c_score': '$spot_comments.c_score',
                    'score_true': {'$cond': [{'$gt': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'score_false': {'$cond': [{'$lte': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'spot_name': '$spot_name',
                    'create_at': '$spot_comments.create_at'
                }
            },
            {
                '$match': {
                    'create_at': {'$gte': str(datetime.date.today())},
                    # 'spot_name': {'$ne': None}
                }
            },
            {
                '$group': {
                    '_id': {'spot_name': '$spot_name', 'ota_spot_id': '$ota_spot_id'},
                    'score_true_total': {'$sum': '$score_true'},
                    'score_false_total': {'$sum': '$score_false'}
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))

        return L

    @classmethod
    def yesterday_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot_comment',
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot_comments"
                }
            },
            {
                '$unwind': {
                    'path': "$spot_comments",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ota_spot_id': '$ota_spot_id',
                    'c_score': '$spot_comments.c_score',
                    'score_true': {'$cond': [{'$gt': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'score_false': {'$cond': [{'$lte': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'spot_name': '$spot_name',
                    'create_at': '$spot_comments.create_at'
                }
            },
            {
                '$match': {
                    'create_at': {'$lt': str(datetime.date.today()),
                                  '$gte': str(get_yesterday())},
                    # 'spot_name': {'$ne': None}
                }
            },
            {
                '$group': {
                    '_id': {'spot_name': '$spot_name', 'ota_spot_id': '$ota_spot_id'},
                    'score_true_total': {'$sum': '$score_true'},
                    'score_false_total': {'$sum': '$score_false'}
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))

        return L

    #

    @classmethod
    def list_spot(cls, s_name, skip, limit, sort):
        pipeline = [
            {
                '$sort': {sort: -1}
            },
            {
                '$match': {
                    's_name': {'$regex': '.*' + s_name + '.*'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'city_id': 1,
                    'city_name': 1,
                    'ota_spot_id': 1,
                    's_name': 1,
                    's_addr': 1,
                    's_level': 1,
                    's_score': 1,
                    's_comment_num': 1,
                    's_sale_num': 1,
                    's_ticket_num': 1,
                    's_img': 1,
                    'year': {'$year': "$create_at"},
                    'month': {'$month': "$create_at"},
                    'day': {'$dayOfMonth': "$create_at"},
                    'create_at': {'$toString': {'$toDate': "$create_at"}},
                    'update_at': {'$toString': {'$toDate': "$update_at"}}
                }
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            },
        ]
        spot_city_s = spot.SpotCity.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def total_spot(cls, s_name):
        pipeline = [
            {
                '$match': {
                    's_name': {'$regex': '.*' + s_name + '.*'}
                }
            },
            {
                '$count': "count"
            }

        ]
        count = spot.SpotCity.objects().aggregate(*pipeline)
        # return dict(count)
        L = []
        for p in count:
            L.append(dict(p))
        if len(L) < 1:
            return 0
        else:
            return L[0]['count']

    @classmethod
    def spot_comment_group(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': "spot_comment",
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot_comment"
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'spot_name': "$spot_name",
                    'ota_spot_id': "$ota_spot_id",
                    'c_score': "$spot_comment.c_score",
                    'comment_create_at': "$spot_comment.create_at",
                }
            }
            ,
            {
                '$match': {
                    '$and': [
                        {
                            '$or': [
                                {'ota_spot_id': {'$eq': 103113}},
                                {'ota_spot_id': {'$eq': 100025}},
                                {'ota_spot_id': {'$eq': 5427075}},
                                {'ota_spot_id': {'$eq': 339}},
                            ]
                        },
                        {
                            'comment_create_at': {
                                '$gte': '2017-12-04',
                                # '$lt': '2019-12-05'
                            }
                        }
                    ]

                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        # sum(i > 5 for i in j)
        for p in spot_city_s:
            p['total_up_score'] = sum(int(i) > 3 for i in p['c_score'])
            p['total_down_score'] = sum(int(i) <= 3 for i in p['c_score'])
            del p['c_score']
            L.append(dict(p))
        return L

    @classmethod
    def last_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot_comment',
                    'localField': 'ota_spot_id',
                    'foreignField': 'ota_spot_id',
                    'as': 'spot_comments'
                }
            },
            {
                '$unwind': {
                    'path': "$spot_comments",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$match': {
                    'spot_name': {'$ne': None}
                }
            },
            {
                '$group': {
                    '_id': {'ota_spot_id': '$ota_spot_id', 'spot_name': '$spot_name', 'ota_id': '$ota_id'},
                    'c_score': {'$first': "$spot_comments.c_score"},
                    'create_at': {'$first': "$spot_comments.create_at"}
                }
            },
            {
                '$sort': {'create_at': -1}
            },
            {
                '$group': {
                    '_id': {'ota_spot_id': '$_id.ota_spot_id', 'spot_name': '$_id.spot_name'},
                    'ota_10001_score': {'$sum': {'$cond': [{'$eq': ['$_id.ota_id', 10001]}, '$c_score', 0]}},
                    'ota_10002_score': {'$sum': {'$cond': [{'$eq': ['$_id.ota_id', 10002]}, '$c_score', 0]}},
                    'ota_10003_score': {'$sum': {'$cond': [{'$eq': ['$_id.ota_id', 10003]}, '$c_score', 0]}},
                    'ota_10004_score': {'$sum': {'$cond': [{'$eq': ['$_id.ota_id', 10004]}, '$c_score', 0]}},
                    'ota_10005_score': {'$sum': {'$cond': [{'$eq': ['$_id.ota_id', 10005]}, '$c_score', 0]}},
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def count_comment(cls, condition):
        pipeline = [
            {
                '$lookup': {
                    'from': "spot_comment",
                    'localField': "ota_spot_id",
                    'foreignField': "ota_spot_id",
                    'as': "spot_comments"
                }
            },
            {
                '$unwind': {
                    'path': "$spot_comments",
                    'preserveNullAndEmptyArrays': True
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'ota_id': '$spot_comments.ota_id',
                    'ota_spot_id': '$ota_spot_id',
                    'spot_name': '$spot_name',
                    'c_score': '$spot_comments.c_score',
                    'score_true': {'$cond': [{'$gt': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'score_false': {'$cond': [{'$lte': ['$spot_comments.c_score', 3]}, 1, 0]},
                    'score_total': {'$cond': [{'$lte': ['$spot_comments.c_score', 3]}, 1, 1]},
                    'create_at': '$spot_comments.create_at'
                }
            },
            {
                '$match': {
                    '$and': [
                        {
                            'create_at': {
                                '$gte': condition['begin_date'],
                                '$lt': condition['end_date']
                            }
                        },
                        {
                            'c_score': {
                                '$gt': condition['down_score'],
                                '$lte': condition['up_score']
                            }
                        },
                        {
                            'ota_id': {'$in': condition['ota_id']}
                        },
                        {
                            'ota_spot_id': {'$in': condition['ota_spot_id']}
                        }
                    ]
                }
            },
            {
                '$group': {
                    '_id': {'spot_name': '$spot_name', 'ota_spot_id': '$ota_spot_id', 'ota_id': '$ota_id'},
                    'score_true_total': {'$sum': '$score_true'},
                    'score_false_total': {'$sum': '$score_false'},
                    'score_total': {'$sum': '$score_total'}
                }
            }
        ]
        spot_city_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def all_comment(cls, condition, skip, limit):
        pipeline = [
            {
                "$lookup": {
                    "from": "spot_comment",
                    "localField": "ota_spot_id",
                    "foreignField": "ota_spot_id",
                    "as": "spot_comment"
                }
            },
            {
                "$unwind": {
                    "path": "$spot_comment",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "ota_spot_id": "$ota_spot_id",
                    "spot_name": "$spot_name",
                    "create_at": "$spot_comment.create_at",
                    "ota_id": "$spot_comment.ota_id",
                    "c_score": "$spot_comment.c_score"
                }
            },
            {
                "$match": {
                    "$and": [
                        {
                            "spot_name": {
                                "$exists": True
                            }
                        },
                        {
                            "ota_spot_id": {
                                "$in": condition['ota_spot_id']
                            }
                        },
                        # {
                        #     "c_score": {
                        #         "$ne": None
                        #     }
                        #
                        # }
                        # {
                        #     "create_at": {
                        #         "$gte": condition['begin_date'] + " 00:00:00"
                        #     }
                        # },
                        # {
                        #     "create_at": {
                        #         "$lte": condition['end_date'] + " 23:59:59"
                        #     }
                        # }
                    ]
                }
            },
            {
                "$group": {
                    "_id": {
                        "ota_spot_id": "$ota_spot_id",
                        "spot_name": "$spot_name"
                    },
                    "sum_score_ota_id_10000": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10000]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10000": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10000]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10000_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10000]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10000_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10000]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10001": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10001]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10001": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10001]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10001_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10001]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10001_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10001]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10002": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10002]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10002": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10002]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10002_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10002]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10002_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10002]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10003": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10003]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10003": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10003]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10003_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10003]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10003_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10003]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10004": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10004]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10004": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10004]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10004_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10004]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10004_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10004]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10005": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10005]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10005": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10005]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10005_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10005]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10005_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10005]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10006": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10006]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10006": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10006]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10006_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10006]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10006_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10006]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10007": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10007]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10007": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10007]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_ota_id_10007_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10007]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_score_ota_id_10007_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$eq": ["$ota_id", 10007]
                                }, {
                                    "$lte": ["$create_at", condition['end_date_pre'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date_pre'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "count_start_5": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$gte": ["$c_score", 5]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "count_start_4": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$gte": ["$c_score", 4]
                                }, {
                                    "$lt": ["$c_score", 5]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "count_start_3": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$gte": ["$c_score", 3]
                                }, {
                                    "$lt": ["$c_score", 4]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "count_start_2": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$gte": ["$c_score", 2]
                                }, {
                                    "$lt": ["$c_score", 3]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "count_start_1": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$gte": ["$c_score", 1]
                                }, {
                                    "$lt": ["$c_score", 2]
                                }, {
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_comment": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    },
                    "sum_score_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "count_comment_pre": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['end_date'] + " 23:59:59"]
                                }, {
                                    "$gte": ["$create_at", condition['begin_date'] + " 00:00:00"]
                                }]
                            }, 1, 0]
                        }
                    }
                }
            },
            {
                "$project": {
                    "avg_total": {
                        "$cond": [{
                            "$eq": ["$count_comment", 0]
                        }, 0, {
                            "$divide": ["$sum_score", "$count_comment"]
                        }]
                    },
                    "avg_total_pre": {
                        "$cond": [{
                            "$eq": ["$count_comment_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_pre", "$count_comment_pre"]
                        }]
                    },
                    "avg_10000": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10000", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10000", "$count_score_ota_id_10000"]
                        }]
                    },
                    "avg_10000_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10000_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10000_pre", "$count_score_ota_id_10000_pre"]
                        }]
                    },
                    "avg_10001": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10001", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10001", "$count_score_ota_id_10001"]
                        }]
                    },
                    "avg_10001_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10001_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10001_pre", "$count_score_ota_id_10001_pre"]
                        }]
                    },
                    "avg_10002": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10002", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10002", "$count_score_ota_id_10002"]
                        }]
                    },
                    "avg_10002_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10002_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10002_pre", "$count_score_ota_id_10002_pre"]
                        }]
                    },
                    "avg_10003": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10003", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10003", "$count_score_ota_id_10003"]
                        }]
                    },
                    "avg_10003_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10003_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10003_pre", "$count_score_ota_id_10003_pre"]
                        }]
                    },
                    "avg_10004": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10004", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10004", "$count_score_ota_id_10004"]
                        }]
                    },
                    "avg_10004_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10004_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10004_pre", "$count_score_ota_id_10004_pre"]
                        }]
                    },
                    "avg_10005": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10005", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10005", "$count_score_ota_id_10005"]
                        }]
                    },
                    "avg_10005_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10005_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10005_pre", "$count_score_ota_id_10005_pre"]
                        }]
                    },
                    "avg_10006": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10006", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10006", "$count_score_ota_id_10006"]
                        }]
                    },
                    "avg_10006_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10006_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10006_pre", "$count_score_ota_id_10006_pre"]
                        }]
                    },
                    "avg_10007": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10007", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10007", "$count_score_ota_id_10007"]
                        }]
                    },
                    "avg_10007_pre": {
                        "$cond": [{
                            "$eq": ["$count_score_ota_id_10007_pre", 0]
                        }, 0, {
                            "$divide": ["$sum_score_ota_id_10007_pre", "$count_score_ota_id_10007_pre"]
                        }]
                    },
                    "count_start_5": "$count_start_5",
                    "count_start_4": "$count_start_4",
                    "count_start_3": "$count_start_3",
                    "count_start_2": "$count_start_2",
                    "count_start_1": "$count_start_1",
                    "count_comment": "$count_comment",

                }
            },
            {
                "$project": {
                    "avg_total": "$avg_total",
                    "avg_total_percent": {
                        "$cond": [{
                            "$eq": ["$avg_total_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_total", "$avg_total_pre"]
                        }]
                    },
                    "avg_10000": "$avg_10000",
                    "avg_10000_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10000_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10000", "$avg_10000_pre"]
                        }]
                    },
                    "avg_10001": "$avg_10001",
                    "avg_10001_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10001_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10001", "$avg_10001_pre"]
                        }]
                    },
                    "avg_10002": "$avg_10002",
                    "avg_10002_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10002_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10002", "$avg_10002_pre"]
                        }]
                    },
                    "avg_10003": "$avg_10003",
                    "avg_10003_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10003_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10003", "$avg_10003_pre"]
                        }]
                    },
                    "avg_10004": "$avg_10004",
                    "avg_10004_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10004_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10004", "$avg_10004_pre"]
                        }]
                    },
                    "avg_10005": "$avg_10005",
                    "avg_10005_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10005_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10005", "$avg_10005_pre"]
                        }]
                    },
                    "avg_10006": "$avg_10006",
                    "avg_10006_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10006_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10006", "$avg_10006_pre"]
                        }]
                    },
                    "avg_10007": "$avg_10007",
                    "avg_10007_percent": {
                        "$cond": [{
                            "$eq": ["$avg_10006_pre", 0]
                        }, 0, {
                            "$subtract": ["$avg_10007", "$avg_10007_pre"]
                        }]
                    },
                    "count_start_5": "$count_start_5",
                    "count_start_4": "$count_start_4",
                    "count_start_3": "$count_start_3",
                    "count_start_2": "$count_start_2",
                    "count_start_1": "$count_start_1",
                    "count_comment": "$count_comment",

                }
            },
            {
                "$sort": {
                    "avg_total": -1
                }
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
            }
        ]
        spot_comment_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        i = 1
        for p in spot_comment_s:
            p['sort'] = i
            p['avg_total'] = round(p['avg_total'], 1)
            p['avg_total_percent'] = round(p['avg_total_percent'], 1)
            p['avg_10000'] = round(p['avg_10000'], 1)
            p['avg_10000_percent'] = round(p['avg_10000_percent'], 1)
            p['avg_10001'] = round(p['avg_10001'], 1)
            p['avg_10001_percent'] = round(p['avg_10001_percent'], 1)
            p['avg_10002'] = round(p['avg_10002'], 1)
            p['avg_10002_percent'] = round(p['avg_10002_percent'], 1)
            p['avg_10003'] = round(p['avg_10003'], 1)
            p['avg_10003_percent'] = round(p['avg_10003_percent'], 1)
            p['avg_10004'] = round(p['avg_10004'], 1)
            p['avg_10004_percent'] = round(p['avg_10004_percent'], 1)
            p['avg_10005'] = round(p['avg_10005'], 1)
            p['avg_10005_percent'] = round(p['avg_10005_percent'], 1)
            p['avg_10006'] = round(p['avg_10006'], 1)
            p['avg_10006_percent'] = round(p['avg_10006_percent'], 1)
            p['avg_10007'] = round(p['avg_10007'], 1)
            p['avg_10007_percent'] = round(p['avg_10007_percent'], 1)
            if p['avg_total'] >= 4.5:
                p['tags'] = '优秀'
            elif p['avg_total'] is 0:
                p['tags'] = '未知'
            elif p['avg_total'] < 4.0:
                p['tags'] = '不及格'
            else:
                p['tags'] = '合格'

            L.append(dict(p))
            i = i + 1
        return L

    @classmethod
    def spot_count(cls, condition):
        pipeline = [
            {
                "$match": {
                    "$and": [
                        {
                            "spot_name": {
                                "$exists": True
                            }
                        },
                        {
                            "ota_spot_id": {
                                "$in": condition['ota_spot_id']
                            }
                        }
                    ]
                }
            },
            {
                "$group": {
                    "_id": None,
                    "count": {
                        "$sum": 1
                    }
                }
            }
        ]
        spot_count = spot.Spot.objects.aggregate(*pipeline)
        L = list(spot_count)
        return L[0]['count']

    @classmethod
    def spot_score_count(cls, condition):
        pipeline = [
            {
                "$lookup": {
                    "from": "spot_comment",
                    "localField": "ota_spot_id",
                    "foreignField": "ota_spot_id",
                    "as": "spot_comment"
                }
            },
            {
                "$unwind": {
                    "path": "$spot_comment",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "ota_spot_id": "$ota_spot_id",
                    "spot_name": "$spot_name",
                    "create_at": "$spot_comment.create_at",
                    "c_score": "$spot_comment.c_score"
                }
            },
            {
                "$match": {
                    "$and": [
                        {
                            "spot_name": {
                                "$exists": True
                            }
                        },
                        {
                            "spot_name": {
                                "$regex": re.compile(condition['spot_name'])
                            }
                        },
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
                "$group": {

                    "_id": None,
                    "score_True": {
                        "$sum": {
                            "$cond": [{
                                "$gt": ["$c_score", 3]
                            }, 1, 0]
                        }
                    },
                    "score_false": {
                        "$sum": {
                            "$cond": [{
                                "$lte": ["$c_score", 3]
                            }, 1, 0]
                        }
                    },
                    "score_total": {
                        "$sum": 1
                    }
                }
            }
        ]
        spot_comment_s = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in spot_comment_s:
            L.append(dict(p))
        return L

    @classmethod
    def spot_complex(cls, condition):
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "now_month_total": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['now'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['now_month'] + ' 00:00:00']
                                }]
                            }, 1, 0]
                        }
                    },
                    "now_month_score": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['now'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['now_month'] + ' 00:00:00']
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "last_month_total": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['last_month_first'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['last_month_last'] + ' 00:00:00']
                                }]
                            }, 1, 0]
                        }
                    },
                    "last_month_score": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['last_month_first'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['last_month_last'] + ' 00:00:00']
                                }]
                            }, "$c_score", 0]
                        }
                    },
                    "lastyear_month_total": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['last_year_month_first'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['last_year_month_last'] + ' 00:00:00']
                                }]
                            }, 1, 0]
                        }
                    },
                    "lastyear_month_score": {
                        "$sum": {
                            "$cond": [{
                                "$and": [{
                                    "$lte": ["$create_at", condition['last_year_month_first'] + ' 23:59:59']
                                }, {
                                    "$gte": ["$create_at", condition['last_year_month_last'] + ' 00:00:00']
                                }]
                            }, "$c_score", 0]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "now_month_per_score": {
                        '$cond': [{
                            '$eq': ['$now_month_total', 0]
                        }, 4.7, {
                            '$multiply': [{
                                "$divide": ["$now_month_score", "$now_month_total"]
                            }, 1]
                        }]
                    },
                    "last_month_per_score": {
                        '$cond': [{
                            '$eq': ['$last_month_total', 0]
                        }, 4.7, {
                            '$multiply': [{
                                "$divide": ["$last_month_score", "$last_month_total"]
                            }, 1]
                        }]
                    },
                    "lastyear_month_per_score": {
                        '$cond': [{
                            '$eq': ['$lastyear_month_total', 0]
                        }, 4.7, {
                            '$multiply': [{
                                "$divide": ["$lastyear_month_score", "$lastyear_month_total"]
                            }, 1]
                        }]
                    }
                }
            }
        ]
        spot_complex = spot.SpotComment.objects.aggregate(*pipeline)

        L = list(spot_complex)
        tongbi_num = round(L[0]['now_month_per_score'] - L[0]['lastyear_month_per_score'], 2)
        huanbi_num = round(L[0]['now_month_per_score'] - L[0]['last_month_per_score'], 2)
        if L[0]['lastyear_month_per_score']:
            tongbi_per = round(
                (L[0]['now_month_per_score'] - L[0]['lastyear_month_per_score']) * 100 / L[0][
                    'lastyear_month_per_score'], 1)
        else:
            tongbi_per = None

        if L[0]['last_month_per_score']:
            huanbi_per = round(
                (L[0]['now_month_per_score'] - L[0]['last_month_per_score']) * 100 / L[0]['last_month_per_score'], 1)
        else:
            huanbi_per = None

        dic = {"now_month_per_score": round(L[0]['now_month_per_score'], 1),
               "tongbi_num": tongbi_num,
               "huanbi_num": huanbi_num,
               "tongbi_per": tongbi_per,
               "huanbi_per": huanbi_per
               }
        return dic

    @classmethod
    def comment_num(cls, condition):
        pipeline = [
            {
                "$unwind": {
                    "path": "$spot_comment",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$group": {
                    "_id": True,
                    "up_score_count": {
                        "$sum": {
                            "$cond": {
                                "if": {
                                    "$gt": ["$c_score", 3]
                                },
                                "then": 1,
                                "else": 0
                            }
                        }
                    },
                    "down_score_count": {
                        "$sum": {
                            "$cond": {
                                "if": {
                                    "$lte": ["$c_score", 3]
                                },
                                "then": 1,
                                "else": 0
                            }
                        }
                    },
                }
            }
        ]
        spot_complex = spot.SpotComment.objects.aggregate(*pipeline)
        L = list(spot_complex)
        up_score_count = L[0]['up_score_count']
        down_score_count = L[0]['down_score_count']
        up_score_per = round(up_score_count * 100 / (up_score_count + down_score_count), 1)
        down_score_per = round(down_score_count * 100 / (up_score_count + down_score_count), 1)
        dic = {"up_score_count": up_score_count, "down_score_count": down_score_count, "up_score_per": up_score_per,
               "down_score_per": down_score_per, "total": up_score_count + down_score_count}
        # spot_queue.put((dic, 'comment_num'))
        return dic

    @classmethod
    def now_month(cls, condition):
        pipeline = [
            {
                "$project": {
                    "create_at": "$create_at",
                    "day_substring": {
                        "$substr": ["$create_at", 8, 2]
                    },
                    "c_score": "$c_score"
                }
            },
            {
                "$match": {
                    "create_at": {
                        "$gte": condition['now_month']
                    }
                }
            },
            {
                "$group": {
                    "_id": "$day_substring",
                    "avg_score": {
                        "$avg": "$c_score"
                    }
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]
        now_month_bak = getDayList()
        now_month = spot.SpotComment.objects.aggregate(*pipeline)

        for p in now_month:
            for b in now_month_bak:
                if b['_id'] == p['_id']:
                    b['avg_score'] = p['avg_score']
                else:
                    pass

        L = []
        for p in now_month_bak:
            p['avg_score'] = round(p['avg_score'], 1)
            L.append(dict(p))
        return L

    @classmethod
    def star_percent(cls, condition):
        pipeline = [
            {
                "$project": {
                    "c_score": {
                        "$floor": "$c_score"
                    }
                }
            },
            {
                "$match": {
                    "c_score": {
                        "$ne": None
                    }
                }
            },
            {
                "$group": {
                    "_id": "$c_score",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id": -1
                }
            }]
        star_percent = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        total = 0
        for p in star_percent:
            L.append(dict(p))
            total = total + dict(p)['count']
        result = []
        for m in L:
            m['percent'] = round(m['count'] * 100 / total, 1)
            result.append(m)
        # spot_queue.put((L, 'star_percent'))
        return result  # 15221

    @classmethod
    def comment_tags(cls, condition):
        pipeline = [{
            "$unwind": {
                "path": "$tag_list",
                "preserveNullAndEmptyArrays": True
            }
        },
            {
                "$match": {
                    # "tag_list.tag_type": 1
                    'tag_list.tag_type': {'$in': condition}
                }
            },
            {
                "$group": {
                    "_id": "$tag_list.tag_name",
                    "count": {
                        "$sum": "$tag_list.tag_num"
                    }
                }
            },
            {
                "$sort": {
                    "count": - 1
                }
            }
        ]
        comment_tags = spot.Spot.objects.aggregate(*pipeline)
        L = []
        for p in comment_tags:
            L.append(dict(p))
        # return spot_queue.put((L, topic))
        return L

    @classmethod
    def get_param(cls, param, in_name, default):
        if in_name in param and param[in_name]:
            return param[in_name]
        else:
            return default

    @classmethod
    def group_true_false(cls):
        return 1


class SpotCity:
    @classmethod
    def detail_spot(cls, ota_spot_id):
        # spot_city = spot.SpotCity.objects(ota_spot_id=ota_spot_id).fields(slice__comments=[5, 10]).first()
        # logger.info(spot_city.to_mongo())
        pipeline = [
            {
                '$match': {
                    'ota_spot_id': {
                        '$eq': ota_spot_id
                    }
                }
            },
            {
                '$project': {
                    '_id': 0
                }
            }
        ]
        spot_city_s = spot.SpotCity.objects.aggregate(*pipeline)
        L = {}
        for p in spot_city_s:
            # logger.info(p)
            p['create_at'] = p['create_at'].strftime("%Y-%m-%d %H:%M:%S")
            p['update_at'] = p['update_at'].strftime("%Y-%m-%d %H:%M:%S")

            if p['ota_id'] == OTA.OtaCode.MEITUAN.value.id:
                p['s_notes'] = [item['text'] for note in p['s_notes'] for item in note['contents']]
            elif p['ota_id'] == OTA.OtaCode.CTRIP.value.id:
                p['s_notes'] = [note['subtitle'] + ':' + item['desc'] for note in p['s_notes'] for item in
                                note['desclist']]

            if p['ota_id'] == OTA.OtaCode.MEITUAN.value.id:
                s_desc = ''
                for desc in p['s_desc']:
                    contents = desc['contents']
                    for content in contents:
                        if 'type' not in content:
                            if 'text' in content:
                                logger.info('=' * 20, content)
                                s_desc += '<p>' + content['text'] + '</p>'
                            else:
                                logger.info(content)
                        elif content['type'] == 'text':
                            s_desc += '<p>' + content['content']['text'] + '</p>'
                        elif content['type'] == 'img':
                            s_desc += '<img src="' + content['content'] + '"/>'
                p['s_desc'] = s_desc

            # p['s_ticket'] =
            if p['ota_id'] == OTA.OtaCode.MEITUAN.value.id:
                ticket_info = {}
                for ticket in p['s_ticket']:
                    ticket_info[ticket['productType'].lower()] = []
                    for product in ticket['productModels']:
                        if 'title5' in product:
                            info = {'name': product['title5'], 'price': product['price'],
                                    'sale': product['newSoldsString']}
                            ticket_info[ticket['productType'].lower()].append(info)

                    # append(ticket_info)

                p['s_ticket'] = ticket_info
            elif p['ota_id'] == OTA.OtaCode.CTRIP.value.id:
                ticket_info = {}
                if 'spot_hotel' in p['s_ticket']:
                    ticket_info['tc'] = []
                    for item in p['s_ticket']['spot_hotel']:
                        ticket_info['tc'].append({'name': item['productname'], 'price': '未知', 'sale': '已售未知'})
                if 'spot_ticket' in p['s_ticket']:
                    ticket_info['mp'] = []
                    for item in p['s_ticket']['spot_ticket']:
                        ticket_info['mp'].append({'name': item['name'], 'price': '未知', 'sale': '已售未知'})
                p['s_ticket'] = ticket_info
            elif p['ota_id'] == OTA.OtaCode.LVMAMA.value.id:
                ticket_info = {}
                if 'ADULT' in p['s_ticket']:
                    ticket_info['mp'] = []
                    for item in p['s_ticket']['ADULT']:
                        ticket_info['mp'].append({'name': item['name'], 'price': item['pay_price'], 'sale': '已售未知'})
                if 'TC' in p['s_ticket']:
                    ticket_info['tc'] = []
                    for item in p['s_ticket']['TC']:
                        ticket_info['tc'].append({'name': item['name'], 'price': item['pay_price'], 'sale': '已售未知'})
                p['s_ticket'] = ticket_info

            L = p
            logger.info(p)
            # L.append(dict(p))
        return L


class MediaDetail:
    @classmethod
    def dou_yin_new(cls, condition):
        pipeline = [{
            "$unwind": {
                "path": "$tag_list",
                "preserveNullAndEmptyArrays": True
            }
        },
            {
                '$match': {
                    'create_at': {
                        '$eq': condition['create_at']
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "create_at": "$create_at"
                    },
                    "now_fans_count": {  # 今日总粉丝量
                        "$sum": "$fans_num"
                    },
                    "now_total_like_count": {  # 今日总获攒数
                        "$sum": "$total_like"
                    },
                    "now_comment_count": {  # 今日总评论数
                        "$sum": "$comment_num"
                    },
                    "now_broadcast_count": {  # 今日总直播数
                        "$sum": "$broadcast_num"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "now_fans_count": 1,
                    "now_total_like_count": 1,
                    "now_comment_count": 1,
                    "now_broadcast_count": 1,
                }

            }
        ]
        comment_tags = douyin.MediaDetail.objects.aggregate(*pipeline)
        L = []
        for p in comment_tags:
            L.append(dict(p))
        return L

    @classmethod
    def dou_yin_is_official(cls, condition):
        pipeline = [{
            "$unwind": {
                "path": "$tag_list",
                "preserveNullAndEmptyArrays": True
            }
        },
            {
                '$match': {
                    'is_official': {
                        '$eq': condition['is_official']
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "fans_count": {  # 总粉丝量
                        "$sum": "$fans_count"
                    },
                    "total_like_count": {  # 今日总获攒数
                        "$sum": "$total_like"
                    },
                    "broadcast_count": {  # 今日总直播数
                        "$sum": "$broadcast_num"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "fans_count": 1,
                    "total_like_count": 1,
                    "count": 1,
                    "broadcast_count": 1,
                }

            }
        ]
        comment_tags = douyin.MediaDetail.objects.aggregate(*pipeline)
        L = []
        for p in comment_tags:
            L.append(dict(p))
        return L

    @classmethod
    def dou_yin_user(cls, condition):
        pipeline = [{
            "$unwind": {
                "path": "$tag_list",
                "preserveNullAndEmptyArrays": True
            }
        },
            {
                '$match': {
                    'create_at': {
                        '$eq': condition['create_at']
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "create_at": "$create_at"
                    },
                    "fans_count": {  # 今日总粉丝量
                        "$sum": "$fans_num"
                    },
                    "total_like_count": {  # 今日总获攒数
                        "$sum": "$total_like"
                    },
                    "comment_count": {  # 今日总评论数
                        "$sum": "$comment_num"
                    },
                    "broadcast_count": {  # 今日总直播数
                        "$sum": "$broadcast_num"
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "fans_count": 1,
                    "total_like_count": 1,
                    "comment_count": 1,
                    "broadcast_count": 1,
                }

            }
        ]
        comment_tags = douyin.DouYinUser.objects.aggregate(*pipeline)
        print(comment_tags)
        L = []
        for p in comment_tags:
            L.append(dict(p))
        return L
