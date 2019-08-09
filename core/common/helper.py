import importlib
import os
import pkgutil
import sys

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
        # print("{0} name: {1:12}, is_sub_package: {2}".format(filefiner, name, ispkg))


"""
获取scrapyd api客户端
"""


def get_scrapyd_cli() -> ScrapydAPI:
    return ScrapydAPI(settings.SCRAPYD_URL)


