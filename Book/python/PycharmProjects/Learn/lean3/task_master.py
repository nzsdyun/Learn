# -*- coding: utf-8 -*-
# Customized managers(分布式进程)
import queue
import random
from multiprocessing.managers import BaseManager

task_queue = queue.Queue()
result_queue = queue.Queue()


def return_task_queue():
    global task_queue
    return task_queue


def return_result_queue():
    global result_queue
    return task_queue


class QueueManager(BaseManager):
    pass


def master_manager():
    # 将两个Queue注册到网上，callable参数关联了Queue对象：
    QueueManager.register('get_task_queue', callable=return_task_queue)
    QueueManager.register('get_result_queue', callable=return_result_queue)
    # 绑定端口5000，设置验证码'abc'  windows必须填写地址
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    # server = manager.get_server()
    # server.serve_forever()
    # 启动Queue
    manager.start()
    # 不能直接获取原始Queue,需要通过Manager获取
    task = manager.get_task_queue()
    result = manager.get_result_queue()
    for i in range(10):
        value = random.randint(0, 1000)
        print('Put task %d ...' % value)
        task.put(value)
    for i in range(10):
        try:
            r = result.get(timeout=10)
            print('Result: %s.' % r)
        except queue.Empty:
            print('Result queue is empty')
    manager.shutdown()
    print('master exit.')


if __name__ == '__main__':
    master_manager()
