import json
import os
import re

import requests
from fontTools.ttLib import TTFont

from core.lib.route import Route
from core.lib.view import BaseView
from django.core.cache import cache
from bs4 import BeautifulSoup


@Route.route(path='api/dy/fk')
class PublicOpinion(BaseView):
    # 下载抖音字符字体
    @Route.route(path='/get/download')
    def download(self):
        url = 'https://s3.pstatp.com/ies/resource/falcon/douyin_falcon/static/font/iconfont_9eb9a50.woff'
        r = requests.get(url)
        with open("demo.woff", "wb") as code:
            code.write(r.content)
        font = TTFont(r'demo.woff')
        ss = font.saveXML('demo.xml')
        return self.success(ss)

    # 获取单个下的长度
    @Route.route(path='/get/count')
    def get_count(self):
        str_num = {'post_num': '', 'like_num': '', 'focus_num': '', 'follower_num': '', 'liked_num': ''}
        num_list = self.get_str_list()
        print(num_list)
        str_num['post_num'] = self.use_fk(num_list['post_str'])
        str_num['like_num'] = self.use_fk(num_list['like_str'])
        str_num['focus_num'] = self.use_fk(num_list['focus_str'])
        str_num['follower_num'] = self.use_fk(num_list['follower_str'])
        str_num['liked_num'] = self.use_fk(num_list['liked_str'])
        return self.success(str_num)

    @staticmethod
    def use_fk(pre_code_s):
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
            html = open("demo.xml")  # 返回一个文件对象
            page = html.read()  # 调用文件的 readline()方法
            soup = BeautifulSoup(page, "html.parser")
            for link in soup.find_all('map'):
                code = link.get('code')
                if code == input_code:
                    name = link.get('name')
                    out_num = glyphID[name]
            out_str = out_str + str(out_num)
        return int(out_str)

    def get_str_list(self):
        num_list = self.get_num_list()
        str_list = {'post_str': '', 'like_str': '', 'focus_str': '', 'follower_str': '', 'liked_str': ''}
        with open("test.html", "r", encoding="utf-8") as f:
            # print(num_list)
            line = f.read()
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

    def get_num_list(self):
        num_list = {'post_len': 0, 'like_len': 0, 'focus_len': 0, 'follower_len': 0, 'liked_len': 0}
        with open("test.html", "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
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

    # 尝试杀进程
    @Route.route(path='/get/pid')
    def pid(self):
        from psutil import process_iter
        from signal import SIGTERM  # or SIGKILL

        for proc in process_iter():
            for conns in proc.connections(kind='inet'):
                if conns.laddr.port == 8080:
                    proc.send_signal(SIGTERM)  # or SIGKILL

        return self.success(1)
