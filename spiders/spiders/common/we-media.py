from collections import namedtuple
from enum import unique, Enum

we_media = namedtuple('we_media', 'id name')


@unique
class WeMedia(Enum):
    # 攻略
    MAFENGWO = we_media(10001, '马蜂窝')
    CTRIP = we_media(10002, '携程'),
    LVMAMA = we_media(10005, '驴妈妈'),
    DOCIN = we_media(10101, '豆丁网'),
    DOC88 = we_media(10102, '道客巴巴'),
    DOC_360 = we_media(10103, '360图书馆'),
    BAIDU_WEN_KU = we_media(10104, '百度文库'),

    # 自媒体
    TOU_TIAO = we_media(20001, '今日头条'),
    SOHU = we_media(20002, '搜狐号'),
    DA_YU = we_media(20003, '大鱼号'),
    WANG_YI = we_media(20004, '网易号'),
    OM_QQ = we_media(20005, '企鹅自媒体'),
    YI_DIAN = we_media(20006, '一点号'),
    BAI_JIA_HAO = we_media(20007, '百家号'),
    QU_TOU_TIAO = we_media(20008, '趣头条'),
    IFENG = we_media(20009, '大风号'),
    JIAN_SHU = we_media(20010, '简书'),
    SOGOU = we_media(20011, '搜狗号'),
    DOU_BAN = we_media(20012, '豆瓣'),

    # 信息流
    CNCN = we_media(30001, '欣欣旅游网'),
    REDNET = we_media(30002, '红网'),
    QQZSH = we_media(30003, '企鹅最生活'),
    HOME_SPACE = we_media(30004, '户外资料网'),
    MOP = we_media(30005, '猫扑大杂烩'),
    CNHUBEI = we_media(30006, '东湖社区'),
    XIN_YANG = we_media(30007, '阳新论坛'),
    WEI_BO = we_media(30008, '微博'),

    # 问答
    wukong = we_media(40001, '悟空问答'),
    BAIDU_ZHIDAO = we_media(40002, '百度知道'),
    ZHIHU = we_media(40003, '知乎'),

    # 网站
