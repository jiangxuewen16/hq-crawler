import time

from apps.models.crawler import ExceptionLog
from apps.models.passport import DocInterface, DocUser
from apps.monitor.common import helper


def receive_exception(data: dict):
    exception_log = ExceptionLog()
    exception_log.event = data['event']
    exception_log.system_name = data['system_name']
    exception_log.platform = data['platform']
    exception_log.level = data['level']
    exception_log.api_url = data['api_url']
    exception_log.trace = data['trace']
    exception_log.file = data['file']
    exception_log.msg = data['msg']
    exception_log.line = data['line']
    exception_log.request_id = data['request_id']
    exception_log.request_time = data['request_time']
    exception_log.request_param = data['request_param']
    exception_log.create_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    exception_log.save(force_insert=False, validate=False, clean=True)

    docInterface = DocInterface.objects(path=exception_log.api_url).fields(uid=1).first()
    docUser = DocUser.objects(_id=docInterface.uid).first()

    print('=' * 20, docUser.email)
    content = f"""
            <h1>{exception_log.system_name}异常通知</h1>
            <h2 style="color:red">惠趣异常通知</h1>
            <a href="#">地址</a><br>
            <p>异常API：{exception_log.api_url}</p>
            <p>异常时间：{exception_log.request_time}</p>
            <p>异常文件：{exception_log.file}</p>
            <p>异常行：{exception_log.line}</p>
            <p>异常原因：{exception_log.msg}</p>
            <p>异常详情：{exception_log.trace}</p>
            <p>原因：{exception_log.msg}</p>
            <p>请求参数：{exception_log.request_param}</p>
            <p>图片演示：</p>
            <p><img src="cid:image1"></p>
    """
    receivers = [docUser.email]
    cc_list = ['445251692@qq.com']
    helper.send_email(receivers, cc_list, '惠趣异常通知', content)

