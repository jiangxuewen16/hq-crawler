# -*- coding: utf-8 -*-

import time

timestamp = int(1565587838420/1000)

# 转换成localtime
time_local = time.localtime(int(1565587838420/1000))
a = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
print(a)

