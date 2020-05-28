import csv
import json
import re

import requests
import time

import scrapy
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from scrapy.http import HtmlResponse

from spiders.items.association import douyin
from spiders.items.association.douyin import MediaDetail, MediaError


class DYSpider(scrapy.Spider):
    _signature = 'O6WAexAaZSDTf6IGD9XMKjulgG'
    name = "dy_sec"
    allowed_domains = ['www.iesdouyin.com', '192.168.18.243']
    start_urls = [
        'http://192.168.18.243:5000/data?uid=110296954063'
    ]

    def start_requests(self):
        url = self.start_urls[0]
        headers = {
            'Accept': '*/*',
            'sec-fetch-dest': 'empty',
            'sec-fetch-site': 'cors',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-requested-with': 'XMLHttpRequest'
        }
        all_user = DouYinUser.select_all()
        print(all_user)
        # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse)
        yield scrapy.FormRequest(url=url, method='GET', headers=headers,
                                 callback=self.parse)

    def parse(self, response: HtmlResponse):
        # str = response.body.decode('gb18030')
        # print(str)
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        lenth = len(json_data['aweme_list'])
        print(lenth)


def download():
    url = 'https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/static/font/iconfont_9eb9a50.woff'
    r = requests.get(url)
    with open("dy.woff", "wb") as code:
        code.write(r.content)
    font = TTFont(r'dy.woff')
    ss = font.saveXML('dy_font.xml')
    return ss


class DYPageSpider(scrapy.Spider):
    name = "dy_page"
    # allowed_domains = ['www.iesdouyin.com' '192.168.18.243']
    allowed_domains = ['www.iesdouyin.com' '172.18.113.141']
    start_urls = [
        'https://v.douyin.com/oN7DB7/',
    ]

    def start_requests(self):
        url = self.start_urls[0]
        headers = {
            'Accept': '*/*',
            'sec-fetch-dest': 'empty',
            'sec-fetch-site': 'cors',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-requested-with': 'XMLHttpRequest'
        }

        """
        读取csv文件
        0 姓名 1部门 2分享链接 3 群编码
        """
        # 更新抖音字体加密文件
        download()

        # csvFile = open("xinxi.csv", "r")
        # reader = csv.reader(csvFile)
        all_user = DouYinUser.select_all()
        # for info in all_user:
        #     print(info['name'])
        #     print(info['team_name'])
        #     print(info['url'])
        #     print(info['team_group_id'])
        for info in all_user:
            if 'url' in info:
                person_info = {'name': info['name'], 'department': info['team_name'], 'url': info['url'],
                               'team_group_id': info['team_group_id']}
                yield scrapy.http.Request(url=info['url'], headers=headers, callback=self.parse,
                                          meta={'info': person_info, 'url': info['url']})
            # break
        # csvFile.close()

    def parse(self, response: HtmlResponse):
        # 获取url信息code
        print('let me see see.....................................')
        print(response.url)
        print(response.meta['info'])
        info = response.meta['info']
        try:

            url_code = re.search(r'(?<=user\/).*(?=\?)', response.url).group(0)
            '''
            url_code反填回去
            '''
            douyin.DouYinUser.objects(url=response.meta['url']).update_one(  # 团长群编码
                set__uid=url_code,
                upsert=True)

            info['url_code'] = url_code
            pre_line = response.body.decode('utf-8')
            is_ms = self.is_miss(pre_line)
            if is_ms:
                line = pre_line.replace('>.<', '><i class="icon iconfont follow-num"> .; </i><',
                                        (pre_line.count('>.<') - 1))
            else:
                line = pre_line.replace('>.<', '><i class="icon iconfont follow-num"> .; </i><')
            like_all = self.get_count(line)
            info['like_all'] = like_all
            # url = 'http://192.168.18.243:5000/data?uid=' + url_code
            url = 'http://172.18.113.141:5000/data?uid=' + url_code

            yield scrapy.FormRequest(url=url, method='GET',
                                     callback=self.second_parse, meta={'info': info}, dont_filter=True)
        except Exception as e:
            # create_at = time.strftime("%Y-%m-%d", time.localtime())
            # MediaError.objects(url=info['url']).update_one(  # 团长群编码
            #     set__name=info['name'],
            #     set__department=info['department'],
            #     set__team_group_id=info['team_group_id'],
            #     set__url=info['url'],
            #     set__create_at=create_at,  # 创建时间
            #     upsert=True)
            print(e)

    def second_parse(self, response: HtmlResponse):
        # str = response.body.decode('gb18030')
        # print(response.meta['info'])
        info = response.meta['info']
        print(info)
        like_all = info['like_all']
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)
        unique_id = enterprise_verify_reason = ''
        comment_count = digg_count = share_count = 0
        if 'aweme_list' in json_data:
            for key, value in enumerate(json_data['aweme_list']):
                unique_id = value['author']['unique_id']  # 抖音id
                short_id = value['author']['short_id']  # 抖音short_id
                uid = value['author']['uid']  # 抖音short_id
                enterprise_verify_reason = value['author']['enterprise_verify_reason']  # 官方与否

                comment_count = comment_count + value['statistics']['comment_count']  # 评论数
                digg_count = digg_count + value['statistics']['digg_count']  # 点赞数
                share_count = share_count + value['statistics']['share_count']  # 分享数
                if not unique_id:
                    unique_id = short_id

        if enterprise_verify_reason:
            is_official = 1
        else:
            is_official = 0

        print(unique_id, is_official, comment_count, share_count)
        # 获取基本信息
        # line = response.body.decode('utf-8')
        # like_all = self.get_count(line)
        # print(like_all)
        create_at = time.strftime("%Y-%m-%d", time.localtime())
        yield MediaDetail.objects(uid=info['url_code'], create_at=create_at).update_one(  # 团长群编码
            set__name=info['name'],
            set__department=info['department'],
            set__team_group_id=info['team_group_id'],

            set__avatar=like_all['src'],
            set__account=like_all['nickname'],
            set__introduction=like_all['signature'],
            set__video_num=like_all['post_num'],  # 文章数
            set__fans_num=like_all['follower_num'],  # 粉丝数
            set__total_like=like_all['liked_num'],  # 获赞数

            set__account_id=unique_id,  # 抖音id
            set__is_official=is_official,  # 官方
            set__comment_num=comment_count,  # 评论数
            set__repost_num=share_count,  # 转发

            # set__create_at=create_at,  # 创建时间
            set__update_at=create_at,  # 创建时间
            upsert=True)

    def get_count(self, line):
        num_list = self.get_str_list(line)
        str_num = {'post_num': self.use_fk(num_list['post_str']), 'like_num': self.use_fk(num_list['like_str']),
                   'focus_num': self.use_fk(num_list['focus_str']),
                   'follower_num': self.use_fk(num_list['follower_str']),
                   'liked_num': self.use_fk(num_list['liked_str']), 'src': num_list['src'],
                   'nickname': num_list['nickname'], 'signature': num_list['signature']}
        # print(num_list)
        return str_num

    def use_fk(self, pre_code_s):
        #  &#xe618  num_;  &#xe616   num_1; &#xe61b num_5;
        out_num = 0
        out_str = ''
        # pre_code_s = pre_code_s
        for pre_code in pre_code_s:
            input_code = pre_code.replace("&#", "0")
            glyphID = {
                'x': '',
                'num_': 1,
                'num_1': 0,
                'num_2': 3,
                'num_3': 2,
                'num_4': 4,
                'num_5': 5,
                'num_6': 6,
                'num_7': 9,
                'num_8': 7,
                'num_9': 8,
            }
            html = open("dy_font.xml")  # 返回一个文件对象
            page = html.read()  # 调用文件的 readline()方法
            soup = BeautifulSoup(page, "html.parser")
            for link in soup.find_all('map'):
                code = link.get('code')
                if code == input_code:
                    name = link.get('name')
                    out_num = glyphID[name]
                elif input_code == '.':
                    out_num = '.'
            out_str = out_str + str(out_num)

        if out_str.find('.') > 0:
            out_str = float(out_str) * 10000
            print('out_str-----------------------------')
            print(out_str)
        return int(out_str)

    def get_str_list(self, line):
        num_list = self.get_num_list(line)
        str_list = {'post_str': '', 'like_str': '', 'focus_str': '', 'follower_str': '', 'liked_str': '',
                    'src': num_list['src'], 'nickname': num_list['nickname'], 'signature': num_list['signature']}

        # print('作品数、喜欢数-------------------------------------------------')
        like_all = re.findall('class="icon iconfont tab-num"> (.*?);', line)  # 怎么分开
        str_list['post_str'] = like_all[0:num_list['post_len']]  # post_len 作品数
        str_list['like_str'] = like_all[-num_list['like_len']:]  # like_len 喜欢数
        # print(like_all)

        # print('关注数、粉丝数、赞数-------------------------------------------------')
        flower_all = re.findall('class="icon iconfont follow-num"> (.*?);', line)  # 怎么分开
        str_list['focus_str'] = flower_all[0:num_list['focus_len']]  # focus_len 关注数
        str_list['follower_str'] = flower_all[num_list['focus_len']:num_list['focus_len'] + num_list[
            'follower_len']]  # follower_len 粉丝数
        str_list['liked_str'] = flower_all[-num_list['liked_len']:]  # liked_len 赞数
        # print(flower_all)

        return str_list

    def get_num_list(self, line):
        num_list = {'post_len': 0, 'like_len': 0, 'focus_len': 0, 'follower_len': 0, 'liked_len': 0, 'src': '',
                    'nickname': '', 'signature': ''}

        soup = BeautifulSoup(line, "html.parser")
        src = soup.find(class_='avatar').get('src')
        nickname = soup.find(class_='nickname').text
        signature = soup.find(class_='signature').text

        num_list['src'] = src
        num_list['nickname'] = nickname
        num_list['signature'] = signature
        # print('作品数--------------------------------------')
        post_len = self.get_num_len(soup, 'user-tab active tab get-list', 'icon iconfont tab-num')
        num_list['post_len'] = post_len
        # print('喜欢数--------------------------------------')
        like_len = self.get_num_len(soup, 'like-tab tab get-list', 'icon iconfont tab-num')
        num_list['like_len'] = like_len

        # print('关注数--------------------------------------')
        focus_len = self.get_num_len(soup, 'focus block', 'icon iconfont follow-num')
        num_list['focus_len'] = focus_len
        # print('粉丝数--------------------------------------')
        follower_len = self.get_num_len(soup, 'follower block', 'icon iconfont follow-num')
        num_list['follower_len'] = follower_len
        # print('点赞数--------------------------------------')
        liked_len = self.get_num_len(soup, 'liked-num block', 'icon iconfont follow-num')
        num_list['liked_len'] = liked_len
        return num_list

    @staticmethod
    def get_num_len(soup, class_1, class_2):
        liked_list = soup.find(class_=class_1)
        liked_len = liked_list.find_all(class_=class_2)
        return len(liked_len)

    @staticmethod
    def is_miss(line):
        soup = BeautifulSoup(line, "html.parser")
        is_miss = soup.find("div", {"class": "tab-wrap"}).find("i", {"class": "icon iconfont follow-num"})
        return is_miss


class DouYinUser:
    @classmethod
    def select_all(cls):
        pipeline = [
            {'$project':
                 {'_id': 0}
             }]
        dy_user = douyin.DouYinUser.objects.aggregate(*pipeline)
        L = []
        for p in dy_user:
            L.append(dict(p))
        return L
