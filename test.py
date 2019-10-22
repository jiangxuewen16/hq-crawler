# def foo():
#     print("foo")
#
#
# def bar(func):
#     func()


# Python 中的函数可以像普通变量一样当做参数传递给另外一个函数

# 装饰器的返回值也是一个函数/类对象  可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能  它经常用于有切面需求的场景

# bar(foo)
import logging

# def foo():
#     print('i am foo')
#
#
# def foo():
#     print('i am foo')
#     logging.info("foo is running")


# def use_logging(func):
#     logging.warning("%s is running" % func.__name__)
#     func()
#
#
# def foo():
#     print('i am foo')
#
#
# use_logging(foo)

# ------------------------------------------------------------------------------
# def use_logging(func):
#     def wrapper():
#         logging.warning("%s is running" % func.__name__)
#         return func()  # 把 foo 当做参数传递进来时，执行func()就相当于执行foo()
#
#     return wrapper
#
#
# def foo():
#     print('i am foo')
#
#
# foo = use_logging(foo)  # 因为装饰器 use_logging(foo) 返回的时函数对象 wrapper，这条语句相当于  foo = wrapper
# foo()  # 执行foo()就相当于执行 wrapper()

# ----------------------------------------------------------------------------------------------

# def use_logging(func):
#     def wrapper():
#         logging.warning("%s is running" % func.__name__)
#         return func()
#
#     return wrapper
#
#
# def use_logging_two(func):
#     def wrapper():
#         logging.warning("%s two is running " % func.__name__)
#         return func()
#
#     return wrapper
#
#
# @use_logging
# @use_logging_two
# def foo():
#     print("i am foo")
#
#
# foo()

# -----------------------------------带参数的装饰器--------------------------------------------------

# def use_logging(level):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             if level == "warn":
#                 logging.warning("%s is running" % func.__name__)
#             elif level == "error":
#                 logging.error("%s is running" % func.__name__)
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
#
#
# @use_logging(level="error")
# def foo(name='foo_oo'):
#     print("i am %s" % name)
#
#
# foo()

# ------------------------------------------类装饰器---------------------------------------------------------
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('class decorator running')
        self._func()
        print('class decorator ending')


@Foo
def bar():
    print('bar')


bar()

# -----------------------------------------__call__ 方法-----------------------------------------------------------------
# '''调用实体来改变实体的位置。'''
# class Entity:
#
#     def __init__(self, size, x, y):
#         self.x, self.y = x, y
#         self.size = size
#
#     def __call__(self, x, y):
#         # '''改变实体的位置'''
#         self.x, self.y = x, y
#
#
# e = Entity(1, 2, 3)
# # 创建实例
# e(4, 5)
# 实例可以象函数那样执行，并传入x y值，修改对象的x y


# -----------------------__call__ 和 __init__区别-------------------------------------
# class Foo:
#     def __init__(self, a, b, c):
#         print(a)
#         # ...
#
#
# x = Foo(1, 2, 3)  # __init__
#
#
# class Foo:
#     def __call__(self, a, b, c):
#         print(a)
# # ...
#
#
# x = Foo()
# x(1, 2, 3)  # __call__

# ----------------------------------------------------------------
# class Counter:
#     def __init__(self, func):
#         self.func = func
#         self.count = 0
#
#     def __call__(self, *args, **kwargs):
#         self.count += 1
#         self.func(*args, **kwargs)
#
#
# @Counter
# def foo():
#     pass
#
#
# for i in range(10):
#     foo()
#
# print(foo.count)  # 10
RECEIVE_FUNC_LIST: list = []
print(type(RECEIVE_FUNC_LIST))
