# -*- coding: utf-8 -*-
# @Time    : 2018/8/26 11:29
# @Author  : play4fun
# @File    : 订单查询1.py
# @Software: PyCharm

"""
订单查询1.py:
http://open.taobao.com/api.htm?docId=24527&docType=2
淘宝客订单查询
没有权限
"""

from top.api import TbkOrderGetRequest
from top import appinfo

appkey = '29241638'
secret = '8ecd37c8015c1d12771cc1d25cad34fc'

req = TbkOrderGetRequest()
req.set_app_info(appinfo(appkey, secret))

req.query_type = 1
req.position_index = "22223"
req.page_size = 20
req.member_type = 2
req.tk_status = 12
req.end_time = "2019-04-23 12:28:22"
req.start_time = "2019-04-05 12:18:22"
req.jump_type = 1
req.page_no = 1
req.order_scene = 1
try:
    resp = req.getResponse()
    print(resp)
except Exception as e:
    print(e)
    # http://open.taobao.com/doc.htm?spm=a219a.7386653.0.0.CudPbJ&docId=1&docType=18
    '''
    错误原因：应用没有权限访问当当前API
    解决方案：申请相应的API权限

    {"error_response":{"code":11,"msg":"Insufficient isv permissions","sub_code":"isv.permission-api-package-limit","sub_msg":"scope ids is 381 11655 13168 11998 12486 11653","request_id":"10enths0uz5vu"}}
    /usr/local/Python3.75/lib/python3.7/site-packages/top/api/rest

    '''
