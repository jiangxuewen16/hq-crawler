import json
import time

import scrapy
from scrapy.http import HtmlResponse

from spiders.items.association.douyin import MediaDetail


class DYSpider(scrapy.Spider):
    name = "dy_sec"
    allowed_domains = ['www.iesdouyin.com']
    start_urls = [
        'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid=MS4wLjABAAAA5gAOTBEbNm2Y0C4YKuE03csdRevIIkF2EiRM-6mUigE&count=21&max_cursor=0&aid=1128&_signature=4lunVhAfvPAKgYUrY-sm4OJbp0&dytk=c317c0f77c57e903479188ccdb326133'
    ]

    def start_requests(self):
        url = self.start_urls[0]
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        # yield scrapy.http.Request(url=url, headers=headers, callback=self.parse)
        yield scrapy.FormRequest(url=url, method='GET', headers=headers,
                                 callback=self.parse)

    def parse(self, response: HtmlResponse):
        # str = response.body.decode('gb18030')
        # print(str)
        response_str = response.body.decode('utf-8')
        json_data = json.loads(response_str)

        media_detail = MediaDetail()

        media_detail.team_group_id = 111
        media_detail.account_id = 222
        media_detail.account = "account"
        media_detail.name = "name"
        media_detail.city = "city"
        media_detail.category_tags = "美食"
        media_detail.introduction = "introduction"
        media_detail.is_official = 1
        media_detail.department = "department"
        create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        media_detail.fans_num = 1
        media_detail.fans_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.total_play = 1
        media_detail.play_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.total_like = 1
        media_detail.like_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.comment_num = 1
        media_detail.comment_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.video_num = 1
        media_detail.video_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.broadcast_num = 1
        media_detail.broadcast_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]
        media_detail.repost_num = 1
        media_detail.repost_logs = [{'num': 1, 'create_at': create_at}, {'num': 2, 'create_at': create_at}]

        media_detail.create_at = create_at
        media_detail.update_at = create_at

        print(json_data)
        yield media_detail
