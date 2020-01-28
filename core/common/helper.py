import configparser
import importlib
import os
import pkgutil
import random
import string
import sys
from django.utils.autoreload import logger


from scrapyd_api import ScrapydAPI

from hq_crawler import settings

"""
获取当前模块
"""


def get_module():
    def main_module_name():
        mod = sys.modules['__main__']
        file = getattr(mod, '__file__', None)
        return file and os.path.splitext(os.path.basename(file))[0]

    def modname(fvars):

        file, name = fvars.get('__file__'), fvars.get('__name__')
        if file is None or name is None:
            return None

        if name == '__main__':
            name = main_module_name()
        return name

    return modname(globals())


# 自动import指定模块的所有包
def auto_import_module(moduleName: str, maxLevel=2):
    maxLevel -= 1
    if maxLevel <= 0:
        return
    module = importlib.import_module(moduleName)
    for filefiner, name, ispkg in pkgutil.walk_packages(module.__path__):
        if ispkg:
            auto_import_module(moduleName + '.' + name)
        importlib.import_module(moduleName + '.' + name)
        # logger.info("{0} name: {1:12}, is_sub_package: {2}".format(filefiner, name, ispkg))


"""
获取scrapyd api客户端
"""


def get_scrapyd_cli() -> ScrapydAPI:
    spiderConf = configparser.ConfigParser()  # 爬虫项目配置
    spiderConf.read(f'{settings.BASE_DIR}/spiders/scrapy.cfg', encoding="utf-8")
    SCRAPYD_URL = spiderConf.get('deploy', 'url')  # scrapyd地址
    return ScrapydAPI(SCRAPYD_URL)


"""
获取一个随机字符串
length 字符串长度
mod 模式 1：字符 2：数字 3：符号 4：字符+数字 5：字符+符号 6：数字+符号 7：字符+数字+符号
"""


def random_str(length: int = 16, mod: int = 1) -> str:
    return {
        1: lambda x: ''.join(random.sample(string.ascii_letters, x)),
        2: lambda x: ''.join(random.sample(string.digits, x)),
        3: lambda x: ''.join(random.sample(string.ascii_letters + string.digits, x)),
        4: lambda x: ''.join(random.sample(string.punctuation, x)),
        5: lambda x: ''.join(random.sample(string.ascii_letters + string.punctuation, x)),
        6: lambda x: ''.join(random.sample(string.digits + string.punctuation, x)),
        7: lambda x: ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, x)),
    }[mod](length)
