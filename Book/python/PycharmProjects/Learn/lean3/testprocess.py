# -*- coding: utf-8 -*-
import os
import queue
import random
import time
from multiprocessing import Process, Pool, Queue, Pipe
import subprocess

# print("Process %s start" % os.getpid())
# # Only works on Unix/Linux/Mac:
# pid = os.fork()
# # return 0 in the child
# if pid == 0:
#     print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
# # return child's process id in the parent
# else:
#     print('I (%s) just created a child process (%s).' % (os.getpid(), pid))

# 跨平台使用multiprocessing
from multiprocessing.managers import BaseManager


def run_child_process(name):
    print("Run child process name: %s id: %s" % (name, os.getpid()))


def test_process():
    print("Parent process id %s" % os.getpid())
    p = Process(target=run_child_process, args=("child process",))
    print("Child process start")
    # 开始一个新进程
    p.start()
    # 父进程等待子进程任务完成
    p.join()
    print("Child process end")


# 进程池
def long_task_time(name):
    print("Run task %s (%s)..." % (name, os.getpid()))
    start_time = time.time()
    # 随机休眠3s以内时间
    time.sleep(random.random() * 3)
    end_time = time.time()
    print("Task %s run %0.2f seconds." % (name, (end_time - start_time)))
    return name + os.getpid()


def test_pool():
    print("Parent process %s" % os.getpid())
    p = Pool(4)
    for i in range(10):
        p.apply_async(long_task_time, args=('child pool',))
    print("Waiting all child process done")
    p.close()
    p.join()
    print("All child process done.")


def f(x):
    return x * x


def test_pool1():
    print("Parent process %s" % os.getpid())
    with Pool(processes=4) as pool:
        result = pool.apply_async(f, args=(10,))  # evaluate "f(10)" asynchronously in a single process
        print(result.get(timeout=1))  # prints "100" unless your computer is *very* slow
        print(pool.map(f, range(10)))  # prints "[0, 1, 4,..., 81]"

        it = pool.imap(f, range(10))
        print(next(it))  # prints "0"
        print(next(it))  # prints "1"
        print(it.next(timeout=1))  # prints "4" unless your computer is *very* slow

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))  # raises multiprocessing.TimeoutError


# 子进程
def test_subprocess():
    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)


def test_process1():
    print('$ nslookup')
    p = subprocess.Popen(['nslookup'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output)
    print('Exit code:', p.returncode)


#  进程间通信（Queue, Pipe）

# Queue
def f(q):
    q.put([42, None, 'Hello'])


def test_queue():
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())  # prints "[42, None, 'hello']"
    p.join()


def write(q):
    print("Process write: %s" % os.getpid())
    for value in ['A', 'B', 'C']:
        print("put %s into queue" % value)
        q.put(value)
        time.sleep(random.random())


def read(q):
    print("Process read: %s" % os.getpid())
    while True:
        print("get %s from queue" % q.get())


def test_queue1():
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    # 终止进程
    pr.terminate()


# Pipe
def fp(con):
    con.send([42, 'Hello', None])
    con.close()


def test_pipe():
    send_pipe, rev_pipe = Pipe()
    p = Process(target=fp, args=(send_pipe,))
    p.start()
    print(rev_pipe.recv())
    p.join()


if __name__ == '__main__':
    # test_process()
    # test_pool()
    # test_pool1()
    # test_subprocess()
    # test_process1()
    # test_queue()
    # test_queue1()
    test_pipe()
