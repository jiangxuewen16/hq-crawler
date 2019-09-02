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
                '$match': {
                    'create_at': {
                        '$gte': '2018-12-04',
                        '$lt': '2018-12-05'
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}, 'ota_spot_id': '$ota_spot_id'},
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
                '$match': {
                    'create_at': {
                        '$gte': '2019-01-30'
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': {'$gt': ['$c_score', 3]}, 'ota_spot_id': '$ota_spot_id'},
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
        pipeline = [{
            '$group': {
                '_id': {
                    'ota_id': '$ota_id',
                    'ota_spot_id': '$ota_spot_id'
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
                '$match': {
                    'create_at': {
                        '$gte': '2018-11-24'
                    }
                }
            },
            {
                '$match': {
                    'ota_spot_id': {
                        '$eq': 62931
                    },
                    'ota_id': {
                        '$eq': 10002
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'c_score': {'$gt': ['$c_score', 3]},
                        'ota_spot_id': '$ota_spot_id',
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

# 评论列表
# db.spot_comment.find(
# {
# 	ota_id:10002,
# 	c_score:{
#         $gt: 3,
#         $lte: 5
#     }
# }
# ).sort({'create_at':-1}).skip(0).limit(5);
