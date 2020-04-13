# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager, closing

cur_dir = os.path.abspath('.')


# try:
#     f = open(os.path.join(cur_dir, 'test_base64.py'), 'r', encoding='utf-8')
#     print(f.read())
# finally:
#     if f:
#         f.close()

# with open(os.path.join(cur_dir, 'test_base64.py'), 'r', encoding='utf-8') as f:
#     print(f.read())

# 任何对象，只要正确实现了上下文管理，就可以使用with。上下文管理是通过__enter__和__exit__实现的。
class Query(object):

    def __init__(self, name):
        self.name = name

    # def __enter__(self):
    #     print('Begin')
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, traceback):
    #     if exc_type:
    #         print('Error')
    #     else:
    #         print('End')

    def close(self):
        print('End')

    def query(self):
        print('Query info about %s...' % self.name)


# 使用@contextmanager decorator 简化,无需实现__enter__和__exit__
@contextmanager
def create_query(name):
    try:
        print('Begin')
        query = Query(name)
        yield query
    except TypeError:
        print('Error')
    finally:
        print('End')
# @closing简化@contextmanager，等价于, 对象必须有close方法
# @contextmanager
# def closing(thing):
#     try:
#         yield thing
#     finally:
#         thing.close()


# with Query('queue') as q:
#     q.query()

# with create_query('queue') as q:
#     q.query()
with closing(Query('queue')) as q:
    q.query()