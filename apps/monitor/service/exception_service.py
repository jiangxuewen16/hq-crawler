import hashlib
import time
from collections import namedtuple

from apps.models.crawler import ExceptionLog
from apps.models.passport import DocInterface, DocUser, DocProject
from apps.monitor.common import helper
from django.utils.autoreload import logger

exception_api = namedtuple('exception_api', 'num exception_item')

default_email = '445251692@qq.com'
end_time_step = 10 * 60



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

    # pre_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - end_time_step))
    # count_num = exception_log.objects(api_url=exception_log.api_url, create_at__gte=pre_time).count()
    #
    # docInterface = DocInterface.objects(path=exception_log.api_url).fields(uid=1).first()
    # receivers = []  # 默认必填一个邮箱，管理员邮箱
    # cc_list = [default_email]
    # if docInterface:
    #     # 查询开发者邮箱
    #     docUser = DocUser.objects(_id=docInterface.uid).first()
    #     title = docInterface.title
    #     if docUser:
    #         receivers.append(docUser.email)
    #
    #     # 查询项目负责人邮箱
    #     doc_project = DocProject.objects(docInterface.project_id).fields(uid=1).first()
    #     docUser = DocUser.objects(_id=doc_project.uid).first()
    #     if docUser:
    #         cc_list.append(docUser.email)
    # else:
    #     title = '未知'
    #
    # content = f"""
    #         <h1>{exception_log.system_name}异常通知</h1>
    #         <h2 style="color:red">惠趣异常通知</h1>
    #         <a href="#">地址</a><br>
    #         <p>异常API：{exception_log.api_url}</p>
    #         <p>异常API名称：{title}</p>
    #         <p>异常频次：{end_time_step / 60}分钟出现频次{count_num}</p>
    #         <p>异常时间：{time.strftime("%Y-%m-%d %H:%M:%S", exception_log.request_time)}</p>
    #         <p>异常文件：{exception_log.file}</p>
    #         <p>异常行：{exception_log.line}</p>
    #         <p>异常原因：{exception_log.msg}</p>
    #         <p>异常详情：{exception_log.trace}</p>
    #         <p>原因：{exception_log.msg}</p>
    #         <p>请求参数：{exception_log.request_param}</p>
    #         <p>图片演示：</p>
    #         <p><img src="cid:image1"></p>
    # """
    #
    # helper.send_email(receivers, cc_list, '惠趣异常通知', content)


def send_email():
    pre_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - end_time_step))
    exception_log_list = ExceptionLog.objects(create_at__gte=pre_time).all()
    logger.info('=' * 20, exception_log_list)

    if exception_log_list:
        send_list = {}
        for item in exception_log_list:
            s = item.api_url + item.file + str(item.line)
            key = hashlib.md5(s.encode()).hexdigest()
            if key in send_list:
                num = send_list[key].num + 1
            else:
                num = 1
            send_list[key] = exception_api(num, item)

        for _, item in send_list.items():
            logger.info('=' * 20, item)
            exception_item = item.exception_item
            api_doc_url = ''
            docInterface = DocInterface.objects(path=exception_item.api_url).fields(uid=1, title=1, _id=1).first()
            receivers = []  # 默认必填一个邮箱，管理员邮箱
            cc_list = [default_email]
            if docInterface:
                # api_doc_url = f'https://yapi.huiqulx.com/project/{docInterface._id}/interface/api/{}'
                # 查询开发者邮箱
                docUser = DocUser.objects(_id=docInterface.uid).first()
                title = docInterface.title
                if docUser:
                    receivers.append(docUser.email)

                # 查询项目负责人邮箱
                doc_project = DocProject.objects(docInterface.project_id).fields(uid=1).first()
                docUser = DocUser.objects(_id=doc_project.uid).fields(_id=1, email=1).first()
                if docUser:
                    #api_doc_url = f'https://yapi.huiqulx.com/project/{docInterface._id}/interface/api/{docUser._id}'
                    cc_list.append(docUser.email)
            else:
                title = '未知'

            content = f"""
                        <h1>{exception_item.system_name}异常通知</h1>
                        <a href="{api_doc_url}">api文档地址</a><br>
                        <p>异常API：{exception_item.api_url}</p>
                        <p>异常API名称：{title}</p>
                        <p style="color:#ff561b">异常频次：{end_time_step / 60}分钟内出现频次{item.num}</p>
                        <p>异常时间：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exception_item.request_time))}</p>
                        <p>异常文件：{exception_item.file}</p>
                        <p>异常行：{exception_item.line}</p>
                        <p>异常原因：{exception_item.msg}</p>
                        <p>异常详情：{exception_item.trace}</p>
                        <p style="color:#ff561b">原因：{exception_item.msg}</p>
                        <p>请求参数：{exception_item.request_param}</p>
                """
            helper.send_email(receivers, cc_list, '惠趣异常通知', content)
