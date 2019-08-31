from collections import namedtuple
from enum import Enum, unique

ota = namedtuple('ota_info', 'name id')  # ota 定义 id

sp_map = namedtuple('sp_map', 'ota ota_spot_id')  # ota平台景区id

"""
ota的id定义
"""


@unique
class OtaCode(Enum):
    HUIQULX = ota('惠趣旅行', 10000)
    MAFENGWO = ota('马蜂窝', 10001)
    CTRIP = ota('携程', 10002)
    FLIGGY = ota('飞猪', 10003)
    MEITUAN = ota('美团', 10004)
    LVMAMA = ota('驴妈妈', 10005)


"""
各个景区在每个ota的id映射
"""


@unique
class OtaSpotIdMap(Enum):
    # 石燕湖
    SHI_YAN_HU = [sp_map(OtaCode.HUIQULX, 10001),
                  sp_map(OtaCode.MAFENGWO, 339),
                  sp_map(OtaCode.MEITUAN, 1515791),
                  sp_map(OtaCode.LVMAMA, 100025),
                  sp_map(OtaCode.CTRIP, 62931),
                  sp_map(OtaCode.FLIGGY, [556487712203, 598531650805, 600223581229])
                  ]

    # 石牛寨
    SHI_NIU_ZHAI = [sp_map(OtaCode.HUIQULX, 10002),
                    sp_map(OtaCode.MAFENGWO, 5427075),
                    sp_map(OtaCode.MEITUAN, 30067),
                    sp_map(OtaCode.LVMAMA, 103113),
                    sp_map(OtaCode.CTRIP, 127339),
                    sp_map(OtaCode.FLIGGY, [588794344226, 556745581062, 589094123107, 596577545337, 596343512896])
                    ]

    @classmethod
    def get_ota_spot_id(cls, spot_name: str, ota_code: OtaCode) -> int:
        if spot_name not in cls.__members__:
            raise Exception('景区名称未定义！')
        for map_item in cls[spot_name].value:
            if map_item.ota == ota_code:
                return map_item.ota_spot_id

    @classmethod
    def get_ota_spot_list(cls, ota_code: OtaCode) -> list:
        return [item.ota_spot_id for _, member in cls.__members__.items() for item in member.value if
                item.ota == ota_code]
