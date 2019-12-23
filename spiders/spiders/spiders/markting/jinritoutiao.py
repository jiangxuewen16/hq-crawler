import scrapy


class JinritoutiaoSpider(scrapy.Spider):
    name = 'jinritoutiao'
    allowed_domains = ['www.toutiao.com/']
    start_urls = ['https://www.toutiao.com/']
    base_url = 'https://www.toutiao.com/'
    def parse(self, response):
        print(111)
