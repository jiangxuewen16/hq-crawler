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
    MAFENGWO = ota('马蜂窝', 10001)  # 不需要爬取
    CTRIP = ota('携程', 10002)
    FLIGGY = ota('飞猪', 10003)  # 不需要爬
    MEITUAN = ota('美团', 10004)
    LVMAMA = ota('驴妈妈', 10005)
    QUNAR = ota('去哪儿', 10006)
    LY = ota('同程', 10007)


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
                  sp_map(OtaCode.LY, 9513),
                  sp_map(OtaCode.CTRIP, 62931),
                  sp_map(OtaCode.QUNAR, 706176810),
                  sp_map(OtaCode.FLIGGY, [556487712203, 598531650805, 600223581229])
                  ]

    # 石牛寨
    SHI_NIU_ZHAI = [sp_map(OtaCode.HUIQULX, 10002),
                    sp_map(OtaCode.MAFENGWO, 5427075),
                    sp_map(OtaCode.MEITUAN, 30067),
                    sp_map(OtaCode.LVMAMA, 103113),
                    sp_map(OtaCode.LY, 25196),
                    sp_map(OtaCode.CTRIP, 127339),
                    sp_map(OtaCode.QUNAR, 1915618311),
                    sp_map(OtaCode.FLIGGY, [588794344226, 556745581062, 589094123107, 596577545337, 596343512896])
                    ]
    # 益阳嘉年华
    YI_YANG_JIA_NIAN_HUA = [
        sp_map(OtaCode.HUIQULX, 10003),
        sp_map(OtaCode.MAFENGWO, 34944996),
        sp_map(OtaCode.MEITUAN, 179283431),
        sp_map(OtaCode.LVMAMA, 11367356),
        sp_map(OtaCode.CTRIP, 4741361),
        sp_map(OtaCode.QUNAR, 2877753081),
        sp_map(OtaCode.FLIGGY, [584492512950])
    ]
    # 花田溪谷
    HUA_TIAN_XI_GU = [
        sp_map(OtaCode.HUIQULX, 10004),
        sp_map(OtaCode.MAFENGWO, 71460244),
        sp_map(OtaCode.MEITUAN, 188085997),
        sp_map(OtaCode.CTRIP, 5060343),
        sp_map(OtaCode.QUNAR, 2554926827),
        sp_map(OtaCode.FLIGGY, [586838811004])
    ]
    # 东浒寨
    DONG_HU_ZHAI = [
        sp_map(OtaCode.HUIQULX, 10005),
        sp_map(OtaCode.MAFENGWO, 33665644),
        sp_map(OtaCode.MEITUAN, 115915971),
        sp_map(OtaCode.LVMAMA, 10829578),
        sp_map(OtaCode.CTRIP, 1979030),
        sp_map(OtaCode.QUNAR, 225118749),
        sp_map(OtaCode.FLIGGY, [584799774465, 584799774465, 584668493687, 584161482247])
    ]
    # 马仁奇峰
    MA_REN_QI_FENG = [
        sp_map(OtaCode.HUIQULX, 10006),
        sp_map(OtaCode.MAFENGWO, 5436442),
        sp_map(OtaCode.MEITUAN, 1451152),
        sp_map(OtaCode.LVMAMA, 103177),
        sp_map(OtaCode.CTRIP, 65169),
        sp_map(OtaCode.QUNAR, 3821817759),
        sp_map(OtaCode.FLIGGY, [556756108062, 556837833893, 593398048461, 593790142866])
    ]
    # 大茅山
    DA_MAO_SHAN = [
        sp_map(OtaCode.HUIQULX, 10007),
        sp_map(OtaCode.MAFENGWO, 7689642),
        sp_map(OtaCode.MEITUAN, 41614694),
        sp_map(OtaCode.CTRIP, 1493248),
        sp_map(OtaCode.QUNAR, 420237024),
        sp_map(OtaCode.FLIGGY, [5840262534215, 84310398410, 584668141383, 584178969632])
    ]
    # 九龙江
    JIU_LONG_JIANG = [
        sp_map(OtaCode.HUIQULX, 10008),
        sp_map(OtaCode.MEITUAN, 41164719),
        sp_map(OtaCode.LVMAMA, 160416),
        sp_map(OtaCode.CTRIP, 140900),
        sp_map(OtaCode.QUNAR, 4123349957),
        sp_map(OtaCode.FLIGGY, [564239378083, 584355858057])
    ]

    TIAN_KONG_ZHI_CHENG = [
        sp_map(OtaCode.HUIQULX, 10009),
        sp_map(OtaCode.MEITUAN, 182573099),
        sp_map(OtaCode.LVMAMA, 11945662),
        sp_map(OtaCode.CTRIP, 5058354),
        sp_map(OtaCode.FLIGGY, [586483633204, 586613814791, 584164696714, 584644490539, 584372973470])
    ]

    LIAN_YUN_SHAN = [
        sp_map(OtaCode.HUIQULX, 10010),
        sp_map(OtaCode.MAFENGWO, 33673148),
        sp_map(OtaCode.MEITUAN, 5464367),
        sp_map(OtaCode.LVMAMA, 102525),
        sp_map(OtaCode.CTRIP, 1411376),
        sp_map(OtaCode.FLIGGY, [571936340529])
    ]
    # 侠天下
    XIA_TIAN_XIA = [
        sp_map(OtaCode.HUIQULX, 10011),
        sp_map(OtaCode.MAFENGWO, 24960734),
        sp_map(OtaCode.MEITUAN, 51575391),
        sp_map(OtaCode.LVMAMA, 10650528),
        sp_map(OtaCode.CTRIP, 1415157),
        sp_map(OtaCode.QUNAR, 2333288470),
        sp_map(OtaCode.FLIGGY, [575750404213])
    ]
    # 三翁花园
    SAN_FENG_HUA_YUAN = [
        sp_map(OtaCode.HUIQULX, 10012),
        sp_map(OtaCode.MAFENGWO, 70048608),
        sp_map(OtaCode.MEITUAN, 158907227),
        sp_map(OtaCode.LVMAMA, 12210014),
        sp_map(OtaCode.CTRIP, 3989530),
        sp_map(OtaCode.QUNAR, 3333064220),
        sp_map(OtaCode.FLIGGY, [599579181915])
    ]

    WU_JIN_SHAN = [
        sp_map(OtaCode.HUIQULX, 10013),
        sp_map(OtaCode.MAFENGWO, 964195),
        sp_map(OtaCode.MEITUAN, 2498352),
        sp_map(OtaCode.LVMAMA, 162027),
        sp_map(OtaCode.CTRIP, 3264963),
        sp_map(OtaCode.FLIGGY, [575750404213])
    ]

    KAI_ZHI_FENG = [
        sp_map(OtaCode.CTRIP, 1410449),
        sp_map(OtaCode.QUNAR, 63919496),
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
