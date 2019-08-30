import datetime

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
        if score == False:
            count_down = count + count_down
        else:
            count_up = count + count_up
    K = {'total': count_down + count_up, 'count_up': count_up, 'count_down': count_down}
    return K


def get_yesterday(self):
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


class spot_comment_helper:

    def today_total_comment(self):
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
        # L = []
        # for p in spot_city_s:
        #     L.append(dict(p))
        # return L
        return get_three_type(spot_city_s)

    def yesterday_total_comment(self):
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
        # L = []
        # for p in spot_city_s:
        #     L.append(dict(p))
        # return L
        return get_three_type(spot_city_s)

    def today_spot_commet(self):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$gte': '2017-12-04',
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

    def yesterday_spot_comment(self):
        return 2
