class Hqlx:
    @classmethod
    def exception(cls, ch, method, properties, body):
        print('='*30, ch)
        print('='*30, method.consumer_tag)
        print('='*30, properties)
        print('='*30, body)
        # with open('C:/python/test_add_celery/books.txt', 'a', encoding='utf-8') as f:
        #     f.write(ch)
        #     f.write(method)
        #     f.write(properties)
        #     f.write(body)
