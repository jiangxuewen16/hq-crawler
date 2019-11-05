import mongoengine

mongoengine.connect('hq_data_cloud', username='hq_data_cloud', password='hqlxhqdatacloud2019', host='mongodb://dds-wz9542ab304a64a41.mongodb.rds.aliyuncs.com:3717', alias='default')  # 连接hq_crawler.mongodb