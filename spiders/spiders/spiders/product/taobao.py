import scrapy
from scrapy.http import HtmlResponse


class TBSpider(scrapy.Spider):
    name = "tb_product"
    allowed_domains = ['item.taobao.com']
    start_urls = [
        'https://item.taobao.com/item.htm?spm=a1z10.1-c-s.w16909182-22661432006.20.25776a74LJcbAY&id=611373306421',
    ]

    def start_requests(self):
        url = self.start_urls[0]
        headers = {
            'Content-Type': 'text/html;charset=gb18030',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        yield scrapy.http.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response: HtmlResponse):
        str = response.body.decode('gb18030')
        print(str)
