# -*- coding: utf-8 -*-
import threading

# callback方式
from typing import Optional, Callable, Any, Iterable, Mapping


def long_time_task(args):
    print("threading %s start %s" % (threading.current_thread().name, args))
    n = 5
    while n > 0:
        print("threading %s >> %s" % (threading.current_thread().name, n))
        n = n - 1
    print("threading %s end %s" % (threading.current_thread().name, args))


def test_threading_callback():
    print("threading call back start")
    t = threading.Thread(target=long_time_task, name='Thread-T1', args=('fire',))
    t.start()
    t.join()
    print("threading call back end")


# 类方式

class MyThreading(threading.Thread):
    def __init__(self, target: Optional[Callable[..., Any]] = ..., name: Optional[str] = ...,
                 args: Iterable = ..., kwargs: Mapping[str, Any] = ..., *, daemon: Optional[bool] = ...) -> None:
        self.args = args
        super().__init__(None, target, name, args, kwargs, daemon=daemon)

    def run(self) -> None:
        long_time_task(*self.args)


def test_threading_class():
    print("threading class start")
    mt = MyThreading(name='Threading-class', args=('fire',))
    mt.start()
    mt.join()
    print("threading class end")


# Lock
balance = 0
lock = threading.Lock()


def change_balance(n):
    global balance
    balance = balance + n
    balance = balance - n


def run_thread(n):
    for i in range(1000000):
        lock.acquire()
        try:
            change_balance(n)
        finally:
            lock.release()


def test_lock():
    print('balance', balance)
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('balance', balance)


# ThreadLocal
# 创建全局ThreadLocal对象
thread_lock = threading.local()


def process_name():
    # 获取ThreadLocal的name
    name = thread_lock.name
    print("Hi %s in (%s)" % (name, threading.current_thread().name))


def process_thread(name):
    # 绑定ThreadLocal的name
    thread_lock.name = name
    process_name()


def test_thread_local():
    t1 = threading.Thread(target=process_thread, name='Thread-A', args=('Bob',))
    t2 = threading.Thread(target=process_thread, name='Thread-B', args=('Eby',))
    t1.start()
    t2.start()


if __name__ == '__main__':
    # test_threading_callback()
    # test_threading_class()
    # test_lock()
    test_thread_local()
    pass
