from collections import namedtuple
from enum import Enum


class OtaCode(Enum):
    ota = namedtuple('ota_info', 'name id')
    MAFENGWO = ota('马蜂窝', 10001)
    CTRIP = ota('携程', 10002)
    FLIGGY = ota('飞猪', 10003)
    MEITUAN = ota('美团', 10004)
