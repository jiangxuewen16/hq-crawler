from collections import namedtuple
from enum import unique, Enum

we_media = namedtuple('we_media', 'id type name')
kv = namedtuple('kv', 'id name')


@unique
class WeMediaType(Enum):
    MP = kv(1001, '公众号平台')
    WEI_BO = kv(1002, '微博平台')
    TIE_BA = kv(1003, '贴吧平台')
    WE_MEDIA = kv(1004, '自媒体平台')
    GUIDE = kv(1005, '攻略平台')
    KNOW = kv(1006, '问答平台')
    MINI_APPS = kv(1007, '小程序平台')
    FORUM = kv(1007, '论坛平台')


@unique
class WeMedia(Enum):
    # 攻略
    MAFENGWO = we_media(10001, WeMediaType.GUIDE, '马蜂窝')
    CTRIP = we_media(10002, WeMediaType.GUIDE, '携程')
    LVMAMA = we_media(10005, WeMediaType.GUIDE, '驴妈妈')
    DOCIN = we_media(10101, WeMediaType.GUIDE, '豆丁网')
    DOC88 = we_media(10102, WeMediaType.GUIDE, '道客巴巴')
    DOC_360 = we_media(10103, WeMediaType.GUIDE, '360图书馆')
    BAIDU_WEN_KU = we_media(10104, WeMediaType.GUIDE, '百度文库')
    WECHAT = we_media(10105, WeMediaType.MP, '微信公众号')

    # 自媒体
    TOU_TIAO = we_media(20001, WeMediaType.WE_MEDIA, '今日头条')
    SOHU = we_media(20002, WeMediaType.WE_MEDIA, '搜狐号')
    DA_YU = we_media(20003, WeMediaType.WE_MEDIA, '大鱼号')
    WANG_YI = we_media(20004, WeMediaType.WE_MEDIA, '网易号')
    OM_QQ = we_media(20005, WeMediaType.WE_MEDIA, '企鹅自媒体')
    YI_DIAN = we_media(20006, WeMediaType.WE_MEDIA, '一点号')
    BAI_JIA_HAO = we_media(20007, WeMediaType.WE_MEDIA, '百家号')
    QU_TOU_TIAO = we_media(20008, WeMediaType.WE_MEDIA, '趣头条')
    IFENG = we_media(20009, WeMediaType.WE_MEDIA, '大风号')
    JIAN_SHU = we_media(20010, WeMediaType.WE_MEDIA, '简书')
    SOGOU = we_media(20011, WeMediaType.WE_MEDIA, '搜狗号')
    DOU_BAN = we_media(20012, WeMediaType.WE_MEDIA, '豆瓣')

    # 信息流
    CNCN = we_media(30001, WeMediaType.FORUM, '欣欣旅游网')
    REDNET = we_media(30002, WeMediaType.FORUM, '红网')
    QQZSH = we_media(30003, WeMediaType.FORUM, '企鹅最生活')
    HOME_SPACE = we_media(30004, WeMediaType.FORUM, '户外资料网')
    MOP = we_media(30005, WeMediaType.FORUM, '猫扑大杂烩')
    CNHUBEI = we_media(30006, WeMediaType.FORUM, '东湖社区')
    XIN_YANG = we_media(30007, WeMediaType.FORUM, '阳新论坛')

    SINA_WEI_BO = we_media(30008, WeMediaType.WEI_BO, '新浪微博')

    # 问答
    WUKONG = we_media(40001, WeMediaType.KNOW, '悟空问答')
    BAIDU_ZHIDAO = we_media(40002, WeMediaType.KNOW, '百度知道')
    ZHIHU = we_media(40003, WeMediaType.KNOW, '知乎')

    # 小程序
    MINI_PROGRAM = we_media(50001, WeMediaType.MINI_APPS, '微信小程序')

    # 网站

    """
    用平台类型获取平台id列表
    """

    @classmethod
    def get_id_list_by_type(cls, we_media_type: WeMediaType) -> list:
        return [item.id for _, member in cls.__members__.items() for item in member.value if
                item.type == we_media_type]


@unique
class ActivityType(Enum):
    SPORT = kv(2001, '景区活动'),
    SHOP = kv(2002, '店铺活动'),
    MP = kv(2003, '店铺活动'),
