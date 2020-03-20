import json

import scrapy
from scrapy import Request
from scrapy.http import HtmlResponse

from spiders.common import OTA, helper, marketing
from spiders.common.marketing import WeMedia, WeMediaType
from spiders.items.common import core


class MeituanSpider(scrapy.Spider):
    name = 'huiqulx'
    allowed_domains = ['api.huiqulx.com']
    start_urls = ['https://api.huiqulx.com/release/user/user/test']

    # def start_requests(self):
    #     formdata = {
    #         "head": {"token": "", "time": 1563965531895, "version": "1.0", "platform": "43", "excode": "", "qrcode": "",
    #                  "recode": ""}, "data": {}}
    #     yield Request(self.start_urls[0], method="POST", body=json.dumps(formdata),
    #                   headers={'Content-Type': 'application/json'},
    #                   callback=self.parse)

    def parse(self, response: HtmlResponse):
        # items = response.css('div.service_c ul li').extract_first()
        print("11111111111111111111111")
        data = core.BaseData()
        data.data = '{"name":"jiangxuewen","age":27}'
        yield data


if __name__ == '__main__':
    s = '大家在网上自行搜索相关题目，会有很多的文章啦。那，如果你跟我一样。作为一个小白，没有专业知识，但热衷想体验一番。可以看看以下内容，这是我刚踩完坑后的(粗略)经验，分享给大家';
    li = ['大家', '文章', '蒋雪文']
    x = helper.String.str_count_list(s, li, True)
    print(x)

