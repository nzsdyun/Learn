# -*- coding: utf-8 -*-
# Customized managers(分布式进程)
import queue
from datetime import time
from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager


class QueueManager(BaseManager):
    pass


def worker_manager():
    # 注册
    QueueManager.register('get_task_queue')
    QueueManager.register('get_result_queue')
    # 连接
    manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')
    manager.connect()
    # 获取queue对象
    task_queue = manager.get_task_queue()
    result_queue = manager.get_result_queue()
    for i in range(10):
        try:
            n = task_queue.get(timeout=1)
            print('run task %d * %d...' % (n, n))
            r = '%d * %d = %d' % (n, n, n * n)
            time.sleep(1)
            result_queue.put(r)
        except queue.Empty:
            print('task queue is empty.')


if __name__ == '__main__':
    worker_manager()
