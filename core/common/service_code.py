from collections import namedtuple
from enum import Enum, unique

"""
系统定义的service code
"""


@unique
class ServiceCode(Enum):
    value = namedtuple('value', 'code msg')  # 具名元组（code msg）

    param_not_exists = value(100132, '参数不能为空')
    insert_failure = value(100133, '新增失败')
    
    other_failure = value(100999, '操作失败')
    other_success = value(0, '操作成功')
