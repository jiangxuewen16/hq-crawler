import importlib
import os
import pkgutil
import sys


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
    # print globals()


moduleName = get_module()


def test(moduleName):
    module = importlib.import_module(moduleName)
    for filefiner, name, ispkg in pkgutil.walk_packages(module.__path__):
        if ispkg:
            test(moduleName + '.' + name)
        importlib.import_module(moduleName + '.' + name)
        print("{0} name: {1:12}, is_sub_package: {2}".format(filefiner, name, ispkg))


test(moduleName)
