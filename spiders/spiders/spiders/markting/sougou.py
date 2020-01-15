import scrapy
from scrapy import Request

from spiders.common import helper
from spiders.common.marketing import WeMedia, WeMediaType


class SougouSpider(scrapy.Spider):
    name = 'sougou'
    allowed_domains = ['mp.sogou.com']
    start_urls = ['http://mp.sogou.com/api/home/dashboard-statistic']
    base_url = 'https://www.toutiao.com/'
    we_media_id = WeMedia.SOGOU.value.id
    we_media_type = WeMediaType.WE_MEDIA.value.id
    cookie_list = {}

    def parse(self, response):
        [account, cookie_list] = helper.get_media_account(self)
        user_url = 'https://mp.toutiao.com/user_login_status_api/'
        yield Request(url=user_url, callback=self.parse_user, dont_filter=True, cookies=cookie_list,
                      meta={'account': account})
