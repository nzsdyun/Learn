# -*- coding: utf-8 -*-
import itertools


# natuals = itertools.count(1)
# for n in natuals:
#     print(n)
#
# cs = itertools.cycle('ABC')
# for c in cs:
#     print(c)
# ns = itertools.repeat('A', 3)
# for n in ns:
#     print(n)
#
# for c in itertools.chain('ABC', 'XYZ'):
#     print(c)
#
# for key, group in itertools.groupby('AAABBBCCAAA'):
#     print(key, list(group))

def pi(N):
    # ' 计算pi的值 '
    # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...

    # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.

    # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...

    # step 4: 求和:
    # cs = itertools.cycle([4, -4])
    # odd = itertools.count(1, 2)
    # sum = 0
    # i = 0
    # while i < N:
    #     sum += next(cs) / next(odd)
    #     i = i + 1
    # return sum
    # 创建一个奇数序列: 1, 3, 5, 7, 9, ...并取前N项
    ns = itertools.takewhile(lambda x: x <= 2 * N - 1, itertools.count(1, 2))
    # 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...并直接sum
    return sum(map(lambda x: -4 / x * (-1) ** ((x + 1) / 2), ns))


# 测试:
print(pi(10))
print(pi(100))
print(pi(1000))
print(pi(10000))
assert 3.04 < pi(10) < 3.05
assert 3.13 < pi(100) < 3.14
assert 3.140 < pi(1000) < 3.141
assert 3.1414 < pi(10000) < 3.1415
print('ok')
