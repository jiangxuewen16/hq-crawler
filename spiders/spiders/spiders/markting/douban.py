import json
import time

import scrapy
from scrapy import Request

from spiders.items import marketing


class DoubanSpider(scrapy.Spider):
    name = 'douban_article'
    allowed_domains = ['mp.dayu.com']
    login_url = 'https://mp.dayu.com/api/stat/article/all/summary_v2?_rid=58248757099844aebf7fbd07aed1bacd&_=1577175449429'

    def start_requests(self):
        yield Request(url=self.login_url
                      , method="GET"
                      , headers={'Content-Type': 'application/json'}
                      , cookies=[{'name': 'USER_TMP',
                                  'value': 'oqZ49r_Lw5SIjQNywAkulA.jmCz4GDh8Yay91nDFuwOB35GcmVlI_ODrC3-vmhAuY6hhhzOmSU81rEjqF11sYQGeUwaFoBat6HCu4gCxOAg9aC9anA3JISbtmfz9seUY2LwEd7zOWxUEorrQtU8NaYZVwMIynds5XmORWIafgs1uXj6vf5aBhZDIveBuKq3rlRc-9FMYcKODvKdPuprBnhJC7ruAAD-ItD0jC5l6chsaDw3br1mAtDdidyXJ-HR-1NZV7Apa0iSRHbxdhjuy6bsEIRC0aXjirs55fqXyi6jmT9vyBd4wWNxhzHUKmy4xS4uDrNEs0x-zBlIiSbn1pKcGYtMiNRTA-2EzEz490sBB2-KbtaCaEImcvSWOlpmiEQ6TOtdBtRNBomvwx8cYfXzZSlwa1LfcPXSt3AM4tXdHmtDvpGd3g04ZRzadUpf8xDwpS1B_3HL-1nvIN9cfahouOf_m3b_rmKGwLXjIUxOt4iQlXaOGW0nYqLEPDEslcuwt9_4OgGe7FAuRLojtje_ijYNTVebYHtVhpKbDrojgScYv1e_-bpc58ufy396kq_hygMXK28t8OIXVVaHp0EjBcl8PnCpw7Y9rdz5B6JY_972mowr9hF_6L-icwDH3nIk5UI6ZZDeFrE3a-cK8BaHf1dhatbuWik7r5qe7S5foU3FTK88ecbCJORGSBXLLzcvbTfj8Gdh7HGZvfwjnWdMx5FBk9k_L-tYUvq_BDJ13JOJr7GpIxL4sz0HKJ6-exGhOg3EPGXSOX5ZJjEJdfWs7_bc4aLrZFEjporMJM6uU1AVs-bWH9UoxEuStI-UHij4tF0OPYlmi-hX-FoBzsJ6Hvgu0nMyjN0oXSFq1uRWNTFZCaf-EqFM7aAvvIHnmyhI6M9yj6uJn17lnQOMWs89BU5wOLe1c-0kvTn8GxLoWv__vGSOnU_QzVPv4vOCVvpEnSPCWGGeGHAJ_24nW4fqoYl1QtjaGDyYO6A6a8UI0Tng3zCGm7k6j5x9dkctnEA-OjtVIW_-hle2jtVZaMmtXbWo7Kd54V9ldsqhz9zcNpgdKZ5OGU7Q03Nbf7RDntRUm4pl7Roe2iSf8f-mTwDc.1577176653375.604800000.ltj2UPee66FX1bxefRJxSHg-DFlo8HdkesfGxU5yfPo',
                                  'domain': 'mp.dayu.com', 'path': '/', 'http': True, 'secure': False}]
                      , meta={'ota_spot_id': 1}
                      , callback=self.after_login)

    def after_login(self, response):
        price_calendar = marketing.Account()
        print(response.meta['ota_spot_id'])
        result = json.loads(response.body)
        print(result)
