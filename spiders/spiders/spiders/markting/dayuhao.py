import json
import time

import scrapy
from scrapy import Request

from spiders.common.marketing import WeMediaType, WeMedia
from spiders.items import marketing


class DayuAccountSpider(scrapy.Spider):
    # marketing.Account.objects(account_name='小惠带你去旅行').delete()
    name = 'dayu_account'
    allowed_domains = ['mp.dayu.com']
    account_list = [
        {
            'name': 'USER_TMP',
            'value': '9LD5PLHlQNipRKWErDsltA.HAAqExWdkazHystRZM6OyhxPP0xAmYWRikwaKEOpJyQwc5AAiNp-D6TsnfL9Bb1QtJ-anbfS55Ik4fxhqdr894_k38zQUyZhhwxOpDmrbx9lt3OEDqEQq8JvpFSwLR8p3eo2BeOYc6RkQofdJjwid-zrwnmLJBgK_F1lYTAnGUlPGxSrrcYFhsM7qnJ9UpjoSn7tdZSo0dH-Apm6b3ptESd84qFYeEq6j8SpJyY0mo0l9voOUoXzf-OZF86-Lp5D_UTZBVhKMJWfXWwtbGsN7Rp5Y_C5V9QYaqWuN9Cs5O9QqIBt7gwHpxsgE1SrTmL1AzEeVaf2N9Xte3Vqgpm1Q42Tqno4QLf0lct8_8cQDcfUY1kDBDBxd-iK3BC6HMhtIeeqMUaeCBlXB4qN-ovuG0cGpWQG_s7d1OjuQnthJiE1nVxnpqQhoswBAdOeGto0_3OZx8a8qEZkh8rWgwI7SpkYU2v9mDz33PvRwQGLQ1cBYnw3kiUxbBQmp9LHc_5aOdzKvsVD-lsBb6n7dq5pQ0vRpEmsA5Yy-4BIJBjHJ-aXyS_smCxRoIN7cX8KgfJaQpTcmLNB0gxJNKEZxm0MHGzF690TYUmz6A2Spf2mUancgoFgpqRMcYYMveECN0su-XxYxpFQkJdZKtSmMJrjMKHtIE-FSDyyKgQqExbZ6hBJ39iNreJlLsAOYec3xpQvPqUCUDfQ9KStD5LnK8i7Il6DPml4dz5ZTvGgUJ9YW5Ru-1y1aYioLXNHXAoMpz2TBsVxG3Kq1IDb-jzc_kH9GnzXW0Nq9JDtZrCOVD5KfCnkLcgC0YXRTFOLoXG8_SxwMzPFIQbjBlMKJ8C8R1tpxH-EBJ44uPgpB2c47o2rpsY1Oj9Vx9zzdX4HCewQhZ0sbhotyuUkd310Z7W4dT2RILjx66pOJZuTgx5dxPqaIU0QGJb3KiyfnK4fDrPrIrV05tvT_7HpaaMBjRBu4HHXAZK4OqtunouLb6tuW4JA4dkQRT7OO0Q3mGKxL-ZZsliNLezHGHjV1gd4wkl92OVzxuOyX2EUL1LcKyh0JDyhI2taCW_y9suaKqsAP4qW50p8.1577353888607.604800000.Jb9C_9_VKTtNevua21-S6sAMbSb_m5C4jWQnZAg4H9s',
            'domain': 'mp.dayu.com', 'path': '/', 'http': True, 'secure': False,
            'account_name': '小惠带你去旅行',
            'account_home': 'https://mp.dayu.com/dashboard/profit/settlement?spm=a2s0i.db_esign_mcn_contracts.menu.25.61c13caaDqhgWy',
            'login_url': 'https://mp.dayu.com/api/stat/article/all/summary_v2?_rid=58248757099844aebf7fbd07aed1bacd&_=1577175449429',
            'follow_url': 'https://mp.dayu.com/api/stat/user/fans/summary?_rid=a63e179bcd5f4b6da0ca64f00d2a976f&source=uc&_=1577244449655',
            'income_url': 'https://mp.dayu.com/dashboard/unifiedSettlement/getAccount?_rid=cd30ed5214a14463b4703a06bb33a2e6&_=0.730423583637466',

            'article_url': 'https://mp.dayu.com/dashboard/getArticleList?_rid=f827d5a127c34145a6fbede3f705392b&keyword=&currentView=all&source=all&articleCategory=&_=1577413781522',
            'article_detail': 'https://mp.dayu.com/api/stat/article/detail/summary_v2?_rid=f827d5a127c34145a6fbede3f705392b&_=1577417446313',
        },
        {
            'name': 'USER_TMP',
            'value': 'd2WmdpxNs9SRwxXp3T3hWg.1X6fEsEDSEpygjsRkPLOZ2t6wIhk87yIEMh4FBPTw6XY8Mo-PVr0gffjMAWET-oldXW49SceaLlEUF1xz4wLigjL_N1dj0tWvvIkn7oUoBi2fKc3sArrt96K1HSySb5MrzlHtCX1vnDe7ly2tszNskdwnsjS19rlfXsaH3KLWueQw9WTFUKOM7adffz0KOVZjDZcta5oh8xrfJM5_2mwkEB77HL5ycQCkDn8djTwoDpDovdOliAJW3lfd3PsfF5Z73nMcoX9ytgo1ExF6YfonBQy4DHuuis3FiCI6qL2b3j6SXmQKsBFmjblgFQT1evyqlEsee4KFZ5zSvyWYGdb6e7-Iw3jlJMocka6Mbg0l9aGkQUqg9bTsTsiEWn6MmPFvqLXllXjiGbySJJEuC07SKSIsM_9t5UZ144bMhYdEO45SNW272Fg3ty8T_aRyetrwU89cyZmADdwOqNL0XJ2FgfOt4eopOxRKsqOcPel6XHrhEDUxjcbsyN4CLGVDloRV_NqDmzoBXqfRvniaOzQu5iI6JOr1NvZ4_63WZLe_JJNWsOwTq6bzy0g4w3pzx1j1oFCJWr4dodvk3cuCIxOq5_pN-RPoRFTB0u8yh-Bie_x3-5Poq__MskFTUqGSCKZsSepbybQES-ZxebHsT2PrijgeOKf3qUGrYEd8j0vOl4cj78pj-NfnW3NoRLizH2fSDTgvaD8PyfVsPSWV6fFcRScuwZWquYsyJXgafssRUippFFZEZKoJ-j2xzpGOEdRn_T9v35ucff7tYEGoNwyrDzF_KsCBi_b-CYx7S8mNsklzlLBHPGoRNxcjReCK6DZ14NZHIOhV1tqyMp7D460z2OFyBHT-HAq2iDgEZfeuw0YIKwBoHr4yNE_6B8pVvVnacjZXq_o4I0qDaG2SwoZXvLJNFOUvgQz8JvdMkMHfempEUA8tY0OpTl2uAIsUuIfhDR8_pfkhB__vYzU052SJQDCCKE09DLxbnlsjMBGXAz28ynvYZhekDvY8algOT6UDtt-MizAXaN2l9FG2fgiBAtriwtwIHj2t1Uq3pgML_U.1577353897719.604800000.jmhFslojHBOaqRn3a_Mb59QJQJmjO0BNHsDm5Dd1f_0',
            'domain': 'mp.dayu.com', 'path': '/', 'http': True, 'secure': False,
            'account_name': '旅小达人',
            'account_home': 'https://mp.dayu.com/dashboard/stat/users?spm=a2s0i.db_stat_article.menu.14.7a683caaR1HaTz',
            'login_url': 'https://mp.dayu.com/api/stat/article/all/summary_v2?_rid=a753eca243004bfca7b8042d0c77bc42&_=1577263384282',
            'follow_url': 'https://mp.dayu.com/api/stat/user/fans/summary?_rid=15873b154af74c53a92b2af3318e5e75&source=uc&_=1577263415316',
            'income_url': 'https://mp.dayu.com/dashboard/unifiedSettlement/getAccount?_rid=d6511ecef631440c928e96244308bc16&_=0.16822544032787645',

            'article_url': 'https://mp.dayu.com/dashboard/getArticleList?_rid=03e5b08cd69f4f50ab74b02699b1dc63&beginDate=2019-12-20&endDate=2019-12-26&_=1577414994769',
            'article_detail': 'https://mp.dayu.com/api/stat/article/detail/summary_v2?_rid=03e5b08cd69f4f50ab74b02699b1dc63&_=1577417880867',
        },
        {
            'name': 'USER_TMP',
            'value': '6thzPEW37LbCevW49BYhYw.VHoELyARihcUd_29CrWNKPO3_pktIGLmsHG0rUugd8Lk0VLga9ppt1dR40xubv-M4Fzu-3eEFLgXnJjAbXBSc7r7ES72pFaT8ivIvkhpl7s8FZldd4GmqpNkLzxQLzLaxwZ4giXRTtnE4MPpiztyQs3V-XOKoquI98OldG6l1EMnv0UkRlxMYnNs1f97LkN5EOHLVu68sG11Ig5wyvqlYAjd6IA9AfL3l7awFSgysHXW9QJpswDwXXfwwQrAQqz508ciTo3UKecPzArevt5fkEiFd48dn8wrgM6QdtbM53bg0SZiLSOe7KJ_vHsdpcoYd3sb8KtJmbmScwAtsK_gjn4hodXhf_mxF_Gjaz-VOl9D9OkjzkzEwHgWuc1yUealMnjAB8dbv7vTlveDoqWIZiLFn06BJ7rhc-zuN-U0PybdeCpMQL0VgkXACwYy156OdVChZFXV4cKO0sMwJOJOLrZQH83cp6DWaC-_BnisBHtt9L9vTntI9hHAO2NfEUYp2hFuySTuwr3i0ZRW-AcOsDSyF5ZrNUYGdpy05hVSAFBij3q3N_7NgI1kI5p0egoGJecVovCEIvPZK4k79634tuSZ6TyNfCWwMN2szU0cm636XTj48YxASzGwioSJOGXMExKSMPgeY7xOzsYB330APUYqtnJypEKQ_GP43A5dxPq2NadJU5-DaH61gW-nYb2P82k8ts5lfReMpLgFobz9XMmg3POKjrpijEqPzuipw9Xt0tnkQ125yc-u3ANfoZgPO_ZOoTAx1LofWVi27KbLCazu8kOdrC1yJdgydLFGLj7JLZSbHw5MQtljR5_7fBRbDyvh_VDKjK1HGQ7K6vMF6AD5GDhAd1i3F29Gpt9CMkJRXxv-cuqIp5-vsFQ98Ha94Bl0Q1-MK9SIH4Xg2zj6Vlv6yH95ps7tXz8e_uSH3Z1VSJ4Wanfv41geCglzvVisSUmrmbvADz-P_Jrx5EqQ5dw7-AvpFiSCB9GsZRLOz2ByR4LaS56DhO6ySJyoS7BvvbaUqTVCfOP1bKYdr0VOOT9qY4lIGYop1Qkcs1sD170.1577353911710.604800000.Zxr_u6e7FYFtWfZjRJtrun1sp-pSNmMW7rJjJv8uICs',
            'domain': 'mp.dayu.com', 'path': '/', 'http': True, 'secure': False,
            'account_name': '中惠旅商城',
            'account_home': 'https://mp.dayu.com/dashboard/stat/article?spm=a2s0i.db_index.menu.10.15fb3caa7tXEWS',
            'login_url': 'https://mp.dayu.com/api/stat/article/all/summary_v2?_rid=9ba0fe7931994f3db8f0b3a7ed5f8e59&_=1577263735879',
            'follow_url': 'https://mp.dayu.com/api/stat/user/fans/summary?_rid=af0a59edf671443fa1da2a7e098e1f28&source=uc&_=1577267087326',
            'income_url': 'https://mp.dayu.com/dashboard/unifiedSettlement/getAccount?_rid=fc4ca6988ba64b578789d39d34932ac4&_=0.08561432160168625',

            'article_url': 'https://mp.dayu.com/dashboard/getArticleList?_rid=9e6c34c50b60409db6f63d3fe765662c&keyword=&currentView=all&source=all&articleCategory=&_=1577415080181',
            'article_detail': 'https://mp.dayu.com/api/stat/article/detail/summary_v2?_rid=9e6c34c50b60409db6f63d3fe765662c&_=1577418018358',
        }
    ]

    def start_requests(self):
        account = marketing.Account.objects(platform='大鱼号（移动端）')
        for v in self.account_list:
            print(v['account_name'])
            print('-' * 20)
            yield Request(url=v['login_url']  # login_url
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=[v]
                          , meta={'cookies': [v]}
                          , callback=self.after_login)

    def after_login(self, response):
        print('-*' * 20)
        print(response.meta['cookies'][0]['follow_url'])
        print('-*' * 20)
        result = json.loads(response.body)
        if 'data' in result:
            recommend_num = 0
            read_num = 0
            forward_num = 0
            comment_num = 0
            for k1, v1 in enumerate(result['data']):
                if v1['text'] == '推荐数':
                    recommend_num = v1['value']
                if v1['text'] == '阅读数':
                    read_num = v1['value']
                if v1['text'] == '分享数':
                    forward_num = v1['value']
                if v1['text'] == '评论数':
                    comment_num = v1['value']
            yield Request(url=response.meta['cookies'][0]['follow_url']
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=response.meta['cookies']
                          , meta={'recommend_num': recommend_num, 'read_num': read_num, 'forward_num': forward_num,
                                  'comment_num': comment_num,
                                  'cookies': response.meta['cookies']}
                          , callback=self.follow_me)

    def follow_me(self, response):
        result = json.loads(response.body)
        print(result)
        follow_num = 0
        if 'data' in result:
            for k1, v1 in enumerate(result['data']):
                if v1['text'] == '累计粉丝数':
                    follow_num = v1['value']
        yield Request(url=response.meta['cookies'][0]['article_url']
                      , method="GET"
                      , headers={'Content-Type': 'application/json'}
                      , cookies=response.meta['cookies']
                      ,
                      meta={'recommend_num': response.meta['recommend_num'], 'read_num': response.meta['read_num'],
                            'follow_num': follow_num, 'forward_num': response.meta['forward_num'],
                            'comment_num': response.meta['comment_num'],
                            'cookies': response.meta['cookies']}
                      , callback=self.now_article)

    def now_article(self, response):
        result = json.loads(response.body)
        publish_num = 0
        if 'dataList' in result and 'metadata' in result['dataList']:
            print(result['dataList']['metadata'], '-' * 20)
            publish_num = result['dataList']['metadata']['total']
        yield Request(url=response.meta['cookies'][0]['income_url']
                      , method="GET"
                      , headers={'Content-Type': 'application/json'}
                      , cookies=response.meta['cookies']
                      ,
                      meta={'recommend_num': response.meta['recommend_num'],
                            'read_num': response.meta['read_num'], 'follow_num': response.meta['follow_num'],
                            'publish_num': publish_num, 'forward_num': response.meta['forward_num'],
                            'comment_num': response.meta['comment_num'],
                            'cookies': response.meta['cookies']}
                      , callback=self.now_income)

    def now_income(self, response):
        result = json.loads(response.body)
        print(response.meta['cookies'][0]['account_name'])
        print(result['data']['balance'])
        print(response.meta['follow_num'])
        account = marketing.Account.objects(account_name=response.meta['cookies'][0]['account_name'])
        yield account.update(set__is_enable=False
                             , set__recommend_num=response.meta['recommend_num']  # 推荐
                             , set__read_num=response.meta['read_num']  # 阅读
                             , set__exposure_num=response.meta['read_num'] + response.meta['recommend_num']  # 曝光
                             , set__follow_num=response.meta['follow_num']  # 关注

                             , set__sex_proportion={'man': 0, 'women': 0, 'unknown': response.meta['follow_num']}
                             # 男女比例
                             , set__age_proportion={'<24': 0, '25-39': 0, '>40': 0,
                                                    'unknown': response.meta['follow_num']}
                             # 年龄比例
                             , set__comment_num=response.meta['comment_num']  # 评论量
                             , set__forward_num=response.meta['forward_num']  # 转发
                             , set__publish_num=response.meta['publish_num']  # 转发

                             , set__total_income=result['data']['income_pretax_amount']  # 总收入
                             , set__drawing=result['data']['withdrawal_amount']  # 总提现
                             , set__balance=result['data']['balance']  # 总余额（实时）
                             , set__account_home=response.meta['cookies'][0]['account_home']
                             , set__authorization_information=json.dumps(response.meta['cookies'])
                             , set__update_at=time.strftime("%Y-%m-%d", time.localtime())
                             )


class DayuArticleSpider(scrapy.Spider):
    # marketing.Account.objects(account_name='小惠带你去旅行').delete()
    name = 'dayu_article'
    allowed_domains = ['mp.dayu.com', 'ff.dayu.com']
    account_list = DayuAccountSpider.account_list

    def start_requests(self):
        print(WeMediaType.WE_MEDIA.value.id)  # 平台类型
        print(WeMedia.DA_YU.value.id)  # 平台id
        for v in self.account_list:
            print(v['account_name'])
            print('-' * 20)
            # meta_data = {'account_name': v['account_name']}
            account_name = v['account_name']
            yield Request(url=v['article_url']  # login_url
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=[v]
                          , meta={'cookies': [v], 'account_name': account_name}
                          , callback=self.after_login)

    def after_login(self, response):
        result = json.loads(response.body)
        print('共：', result['dataList']['totalPage'], '页')  # 总页数
        for page in range(1, result['dataList']['totalPage'] + 1):
            print('第', page, '页', '-' * 20)
            yield Request(url=response.meta['cookies'][0]['article_url'] + '&page=' + str(page)  # login_url
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=response.meta['cookies']
                          , meta={'cookies': response.meta['cookies'], 'account_name': response.meta['account_name']}
                          , callback=self.article_list)

    def article_list(self, response):
        result = json.loads(response.body)  # 获取article_list文章列表
        for _, v in enumerate(result['dataList']['data']):
            print(v['origin_id'], v['title'])
            article_id = v['origin_id']
            title = v['title']
            yield Request(url='https://ff.dayu.com/contents/origin/' + v[
                'origin_id'] + '?biz_id=1002&_fetch_author=1&_incr_fields=click1,click2,click3,click_total,play,like'
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=response.meta['cookies']
                          , meta={'cookies': response.meta['cookies'], 'account_name': response.meta['account_name'],
                                  'article_id': article_id, 'title': title}
                          , callback=self.article_content)

    def article_content(self, response):
        result = json.loads(response.body)  # 获取到文章详情

        print(result['data']['created_at'])
        yield Request(url=response.meta['cookies'][0]['article_detail'] + '&aid=' + response.meta['article_id']
                      , method="GET"
                      , headers={'Content-Type': 'application/json'}
                      , cookies=response.meta['cookies']
                      , meta={'cookies': response.meta['cookies'], 'account_name': response.meta['account_name'],
                              'article_id': response.meta['article_id'], 'title': response.meta['title'],
                              'content': result['data']['body']['text'], 'create_at': result['data']['created_at']}
                      , callback=self.article_detail)

    def article_detail(self, response):
        print(response.meta['create_at'])
        print(response.meta['title'])
        result = json.loads(response.body)
        print(result)
        recommend_num = read_num = forward_num = like_num = comment_num = 0
        if 'data' in result:
            for _, v in enumerate(result['data']):
                if v['text'] == "推荐数":
                    if '万' in str(v['value']):
                        recommend_num = int(float(v['value'].replace('万', '')) * 10000)
                    else:
                        recommend_num = v['value']
                if v['text'] == "阅读数":
                    if '万' in str(v['value']):
                        read_num = int(float(v['value'].replace('万', '')) * 10000)
                    else:
                        read_num = v['value']
                if v['text'] == "评论数":
                    comment_num = v['value']
                if v['text'] == "点赞数":
                    like_num = v['value']
                if v['text'] == "分享数":
                    forward_num = v['value']
        exposure_num = int(recommend_num) + int(read_num)  # 曝光量

        print(WeMedia.DA_YU.value.id)
        # print(WeMediaType.WE_MEDIA.value.id)
        marketing.Article.objects(article_id=response.meta['article_id']).update_one(
            set__platform_type=WeMediaType.WE_MEDIA.value.id,  # 平台类型 详见：WeMediaType.id
            set__platform=WeMedia.DA_YU.value.id,  # 平台id 详见：WeMedia.id
            set__account_name=response.meta['account_name'],  # 账号名称
            set__exposure_num=exposure_num,  # 曝光量（推荐量 + 阅读量）
            set__recommend_num=recommend_num,  # 推荐量
            set__read_num=read_num,  # 阅读量
            set__forward_num=forward_num,  # 转发
            set__like_num=like_num,  # 点赞
            set__comment_num=comment_num,  # 评论量
            set__content=response.meta['content'],  # 内容
            set__title=response.meta['title'],  # 标题
            set__article_id=response.meta['article_id'],  # 标题id
            set__create_at=response.meta['create_at'],
            set__update_at=time.strftime("%Y-%m-%d", time.localtime()),
            upsert=True)


class DayuContentSpider(scrapy.Spider):
    # marketing.Account.objects(account_name='小惠带你去旅行').delete()
    name = 'dayu_content'
    allowed_domains = ['mp.dayu.com', 'ff.dayu.com']
    account_list = DayuAccountSpider.account_list

    def start_requests(self):
        print(WeMediaType.WE_MEDIA.value.id)  # 平台类型
        print(WeMedia.DA_YU.value.id)  # 平台id
        for v in self.account_list:
            print(v['account_name'])
            print('-' * 20)
            # meta_data = {'account_name': v['account_name']}
            account_name = v['account_name']
            yield Request(url=v['article_url']  # login_url
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=[v]
                          , meta={'cookies': [v], 'account_name': account_name}
                          , callback=self.after_login)

    def after_login(self, response):
        result = json.loads(response.body)
        print('共：', result['dataList']['totalPage'], '页')  # 总页数
        for page in range(51, result['dataList']['totalPage'] + 1):
            print('第', page, '页', '-' * 20)
            yield Request(url=response.meta['cookies'][0]['article_url'] + '&page=' + str(page)  # login_url
                          , method="GET"
                          , headers={'Content-Type': 'application/json'}
                          , cookies=response.meta['cookies']
                          , meta={'cookies': response.meta['cookies'], 'account_name': response.meta['account_name']}
                          , callback=self.article_list)

    def article_list(self, response):
        result = json.loads(response.body)
        for _, v in enumerate(result['dataList']['data']):
            print(v['origin_id'], v['title'])
            article_id = v['origin_id']
            yield Request(
                url='https://mp.dayu.com/api/stat/article/all/daylist_v2?beginDate=2010-12-21&endDate=' + time.strftime(
                    "%Y-%m-%d") + '&_=1577518280607&_rid=' +
                    v['origin_id']
                , method="GET"
                , headers={'Content-Type': 'application/json;charset=UTF-8'}
                , cookies=response.meta['cookies']
                , meta={'cookies': response.meta['cookies'], 'account_name': response.meta['account_name'],
                        'article_id': v['origin_id']}
                , callback=self.article_content)

    def article_content(self, response):
        result = json.loads(response.body)
        print(result)
        if 'data' in result:
            for _, v in enumerate(result['data']['list']):
                print(v)
                marketing.MarketingDailyReport.objects(account_id=response.meta['article_id']).update_one(
                    set__platform_type=WeMediaType.WE_MEDIA.value.id,  # 平台类型 详见：WeMediaType.id
                    set__platform=WeMedia.DA_YU.value.id,  # 平台id 详见：WeMedia.id
                    # set__account_id=response.meta['article_id'],  # 标题id
                    set__update_at=time.strftime("%Y-%m-%d", time.localtime()),
                    upsert=True)
