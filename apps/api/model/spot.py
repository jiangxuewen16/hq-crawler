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
                    'create_at': {
                        '$gte': '2018-12-04',
                        '$lt': '2018-12-05'
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}, 'spot_name': '$spot.spot_name'},
                  'count': {'$sum': 1}
                  }
             }]
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
                    'create_at': {
                        '$gte': '2019-01-30'
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}, 'spot_name': '$spot.spot_name'},
                  'count': {'$sum': 1}
                  }
             }]
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
                '$group': {
                    '_id': {
                        'ota_id': '$ota_id',
                        'spot_name': '$spot.spot_name'
                    },
                    'time': {
                        '$last': '$create_at'
                    },
                    'c_score': {
                        '$last': '$c_score'
                    }
                }
            }, {
                '$sort': {
                    'create_at': - 1
                }
            }]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L

    @classmethod
    def count_comment(cls):
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
                    'create_at': {
                        '$gte': '2018-11-24'
                    }
                }
            },
            {
                '$match': {
                    # 'ota_spot_id': {
                    #     '$eq': 62931
                    # },
                    # 'ota_id': {
                    #     '$eq': 10002
                    # }
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
                        '$sum': 1
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
    def list_comment(cls):
        pipeline = [
            {
                '$sort': {"create_at": -1}
            },
            {
                '$skip': 0
            },
            {
                '$limit': 5
            },
            {
                '$match': {
                    'c_score': {
                        '$gt': 3,
                        '$lte': 5
                    }
                }
            },
            {
                '$project': {
                    '_id': 0
                }
            }
        ]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        L = []
        for p in spot_city_s:
            L.append(dict(p))
        return L


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
        return L[0]['count']


class SpotCity:
    @classmethod
    def detail_spot(cls):
        pipeline = [
            {
                '$match': {
                    'ota_spot_id': {
                        '$eq': 6181785
                    },
                    'ota_id': {
                        '$eq': 10004
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
