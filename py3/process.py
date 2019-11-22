"""
多进程
2019.11.10
"""

import time
from multiprocessing import Process
import os


# 通用进程类
class MyProcess(Process):
    def __init__(self, func, args, name=''):
        Process.__init__(self)
        self._func = func
        self._result = None
        self._args = args
        self._name = name

    def run(self):
        _result = self._func(*self._args)
        self._result = _result
        print('finish {} run'.format(self._name))

    @property
    def result(self):
        return self._result


def foo(a, b):
    time.sleep(1)
    print(a + b)


def add(a, b):
    time.sleep(2)
    print(a + b)
    return a + b


def mul_process():
    # 创建进程，指定函数和参数
    p = MyProcess(foo, args=(1, 2))
    p1 = MyProcess(add, args=(1, 2))

    # 设置为守护进程（守护进程会随主进程退出而退出）
    p.daemon = True
    # 启动进程
    p.start()
    p1.start()
    # 子进程阻塞主进程，执行完毕后主进程继续
    p.join(0.5)
    p1.join(3)
    print('进程执行完毕')
    print(p1.result)

