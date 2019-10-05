import json

from apps.monitor.model.exception_log import ExceptionLog


def receive_exception(ch, method, properties, body):
    print(ch, method, properties, body)
    body = body.decode('utf-8')
    json_data = json.loads(body)
    print('+'*30, json_data)
    ExceptionLog.save(json_data, force_insert=False, validate=False, clean=True)
