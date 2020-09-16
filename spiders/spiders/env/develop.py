import mongoengine

mongoengine.connect('hq_data_cloud', username='data-cloud-develop', password='123456',
                    host='mongodb://192.168.18.243:27017', alias='default')  # 连接hq_crawler.mongodb
