# from spiders.items.spot.spot import Spot

from spiders.items.spot import spot


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
                        '$gte': '2018-12-04',
                        '$lt': '2018-12-05'
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
                        '$gte': '2019-01-30'
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
    def today_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot',
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
                    '_id': 0,
                    'ota_spot_id': '$ota_spot_id',
                    'c_score': '$c_score',
                    'score_true': {'$cond': [{'$gt': ['$c_score', 3]}, 1, 0]},
                    'score_false': {'$cond': [{'$lte': ['$c_score', 3]}, 1, 0]},
                    'spot_name': '$spot.spot_name',
                    'create_at': '$create_at'
                }
            },
            {
                '$match': {
                    'create_at': {'$gte': '2017-12-04', '$lt': '2018-12-05'}
                }
            },
            {
                '$group': {
                    '_id': '$spot_name',
                    'score_true_total': {'$sum': '$score_true'},
                    'score_false_total': {'$sum': '$score_false'}
                }
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))

        return L

    @classmethod
    def yesterday_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot',
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
                    '_id': 0,
                    'ota_spot_id': '$ota_spot_id',
                    'c_score': '$c_score',
                    'score_true': {'$cond': [{'$gt': ['$c_score', 3]}, 1, 0]},
                    'score_false': {'$cond': [{'$lte': ['$c_score', 3]}, 1, 0]},
                    'spot_name': '$spot.spot_name',
                    'create_at': '$create_at'
                }
            },
            {
                '$match': {
                    'create_at': {'$gte': '2019-01-30'}
                }
            },
            {
                '$group': {
                    '_id': '$spot_name',
                    'score_true_total': {'$sum': '$score_true'},
                    'score_false_total': {'$sum': '$score_false'}
                }
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))

        return L

    @classmethod
    def last_spot_comment(cls):
        pipeline = [
            {
                '$lookup': {
                    'from': 'spot',
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
                    '_id': 0,
                    'ota_spot_id': '$ota_spot_id',
                    'c_score': '$c_score',
                    'ota_id': '$ota_id',
                    'ota_10005': {'$cond': [{'$eq': ['$ota_id', 10005]}, 1, 0]},
                    'ota_10001': {'$cond': [{'$eq': ['$ota_id', 10001]}, 1, 0]},
                    'spot_name': '$spot.spot_name',
                    'create_at': '$create_at'
                }
            },
            {
                '$match': {
                    'create_at': {'$gte': '2017-12-04', '$lt': '2018-12-05'}
                }
            },
            {
                '$group': {
                    '_id': '$spot_name',
                    'ota_10001_total': {'$sum': '$ota_10001'},
                    'ota_10005_total': {'$sum': '$ota_10005'}
                }
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def count_comment(cls, condition):
        pipeline = [
            {
                '$lookup': {
                    'from': "spot",
                    'localField': "uid",
                    'foreignField': "uid",
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
                            'ota_id': condition['ota_id']
                        },
                        {
                            'ota_spot_id': condition['ota_spot_id']
                        }
                    ]
                }
            },
            {
                '$group': {
                    '_id': {
                        'c_score': {'$gt': ['$c_score', 3]},
                        'spot_name': '$spot.spot_name',
                        'ota_id': '$ota_id'
                    },
                    'count': {
                        '$sum': 1  # 尝试一下$sum 加条件
                    }
                }
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
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
                    'create_at': "$create_at",
                    'spot_name': "$spot.spot_name"
                }
            },
            {
                '$sort': {sort: -1}
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
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
                            'ota_id': condition['ota_id']
                        }
                    ]
                }
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
                        {
                            'ota_id': condition['ota_id']
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
        if 0 in L:
            return L[0]['count']
        else:
            return 0


class Spot:
    @classmethod
    def list_spot(cls, s_name, skip, limit, sort):
        pipeline = [
            {
                '$sort': {sort: -1}
            },
            {
                '$skip': skip
            },
            {
                '$limit': limit
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
                    'year': {'$year': "$create_at"},
                    'month': {'$month': "$create_at"},
                    'day': {'$dayOfMonth': "$create_at"},
                }
            }
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
        if 0 in L:
            return L[0]['count']
        else:
            return 0

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
    def get_param(cls, param, in_name, default):
        if in_name in param:
            return param[in_name]
        else:
            return default

    @classmethod
    def group_true_false(cls):
        return 1


class SpotCity:
    @classmethod
    def detail_spot(cls, ota_spot_id):
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
                    '_id': 0,
                    'create_at': 0,
                    'update_at': 0
                }
            }
        ]
        spot_city_s = spot.SpotCity.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L
