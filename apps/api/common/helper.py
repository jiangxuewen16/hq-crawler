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
        if score <= 3:
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

    def today_comment(self):
        pipeline = [
            {
                '$match': {
                    'create_at': {
                        '$gte': '2020-08-30'
                    },
                    'create_at': {
                        '$lt': str(datetime.date.today())
                    }
                }
            },
            {'$group':
                 {'_id': {'c_score': '$c_score'},
                  'count': {'$sum': 1}
                  }
             }]
        spot_city_s = spot.SpotComment.objects.aggregate(*pipeline)
        return get_three_type(spot_city_s)
