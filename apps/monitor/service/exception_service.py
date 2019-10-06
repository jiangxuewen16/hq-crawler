import json
import time

from apps.models.crawler import ExceptionLog
from apps.models.passport import DocInterface, DocUser
from core.lib.emailer import Email


def receive_exception(ch, method, properties, body):
    print(ch, method, properties, body)
    body = body.decode('utf-8')
    json_data = json.loads(body)
    print('+' * 30, json_data)
    exception_log = ExceptionLog()
    exception_log.event = json_data['event']
    exception_log.system_name = json_data['system_name']
    exception_log.platform = json_data['platform']
    exception_log.level = json_data['level']
    exception_log.api_url = json_data['api_url']
    exception_log.trace = json_data['trace']
    exception_log.file = json_data['file']
    exception_log.msg = json_data['msg']
    exception_log.line = json_data['line']
    exception_log.request_id = json_data['request_id']
    exception_log.request_time = json_data['request_time']
    exception_log.request_param = json_data['request_param']
    exception_log.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    exception_log.save(force_insert=False, validate=False, clean=True)

    docInterface = DocInterface.objects(path=exception_log.api_url).fields(uid=1).first()
    docUser = DocUser.objects(_id=docInterface.uid).first()

    print('='*20, docUser.email)
    receivers = [docUser.email]
    Email('smtp.qq.com', 465, '445251692@qq.com', 'vadzhpbsercybhje') \
        .set_sender('445251692@qq.com', '惠趣运维中心').set_receiver(receivers) \
        .send('群发测试，勿回，如有打扰，在此致歉，谢谢', '群发测试，勿回，如有打扰，在此致歉，谢谢xxxxxx!')
