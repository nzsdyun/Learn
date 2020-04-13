# List: 可变有序集合
import time
from collections import Iterable, Iterator
from functools import reduce
from math import sqrt
import functools

classmates = ['x', 'y', 'z']
for cla in classmates:
    print(cla)
classmates.append(123)
print(classmates)
classmates.pop(-1)
print(classmates)
classmates.insert(2, 'a')
print(classmates)
classmates.sort()
print(classmates)
classmates.sort(reverse=True)
print(classmates)
L = classmates.__len__()
print(L)
# tuple: 有序列表，一旦初始化不能更改（指向对象不变，对象的内容可以改变）
t = ("a", "b", ['x', 'z'])
a = t.count('a')
b = t.index('a')
c = t[0]
d = t[2][0]
e = t[2][1]
t[2][0] = 'a'
print('t=%s,a=%s,b=%s,c=%s,d=%s,e=%s,t=%s' % (t, a, b, c, d, e, t))
# dict: dictionary or map
m = {'a': 65, 'b': 66, 'c': 67}
a = m.get('a')
b = m.pop('a')
c = m.pop('c')
print('m=%s,a=%s,b=%s,c=%s,t=%s' % (m, a, b, c, m))
m.update({'a': 65, 'c': 67})
print("m=%s" % m)
mp = m.fromkeys((1, 2, 3), "xx")
print("mp=%s" % mp)
its = mp.items()
print(its)
for (k, v) in its:
    print("key=%s, val=%s" % (k, v))
ks = mp.keys()
vs = mp.values()
print("ks=%s, vs=%s" % (ks, vs))
for k in ks:
    print("k=%s" % k)
tp = mp.popitem()
print(tp)
s = set([1, 2, 3])
s.update([3, 5, 6])
a = s.pop()
s.add(7)
s.remove(3)
print("s=%s, a=%s" % (s, a))
ds = s.difference(set(([2, 5, 8, 9])))
print("ds=%s" % ds)

def quadratic(a, b, c):
    if a == 0:
        if b == 0:
            return None
        else:
            return -c / b
    else:
        d = b ** 2 - 4 * a * c
        if d < 0:
            return None
        else:
            return (-b + sqrt(d)) / (2 * a), (-b - sqrt(d)) / (2 * a)

# 测试:
print('quadratic(2, 3, 1) =', quadratic(2, 3, 1))
print('quadratic(1, 3, -4) =', quadratic(1, 3, -4))

if quadratic(2, 3, 1) != (-0.5, -1.0):
    print('failed')
elif quadratic(1, 3, -4) != (1.0, -4.0):
    print('failed')
else:
    print('success')

# 必选参数
def my_abs(x):
    if x < 0:
        return -x
    else:
        return x
print("call my_abs(-2)= %s, my_abs(4)= %s" % (my_abs(-2), my_abs(4)))
# 默认参数,默认参数必须指向不变对象
# def my_pow(x):
#     return x * x
def my_pow(x, n = 2):
    s = 1
    while n > 0:
        s = s * x
        n = n - 1
    return s
print("call my_pow(2)= %s, my_pow(2, 4)=%s" % (my_pow(2), my_pow(2, 4)))
def add_end(L=[]):
    L.append('END')
    return L
print(add_end())
print(add_end())
def add_end1(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
print(add_end1())
print(add_end1())
# 可变参数: 参数不固定，会被转换成tuple
# use list
def my_sum(numbers):
    sum = 0
    for number in numbers:
        sum = sum + number
    return sum
t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("call my_sum:%s" % my_sum(t))
#
def my_sum1(*numbers):
    sum = 0
    for number in numbers:
       sum = sum + number
    return sum
print("call my_sum1*:%s" % my_sum1(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
print("call my_sum1*:%s" % my_sum1(*t))
# 关键字参数，可传入0个或任意个含参数名的参数，会被转换成dict
def person(name, age, **other):
    print("name = %s, age = %s, other = %s" % (name, age, other))
person("zs", 16)
person("zs", 16, city= 'beijing')
person("zs", 16, city= 'beijing', gender = 'man')
other = {'city': 'beijing', 'gender': 'man'}
person("zs", 16, city= other['city'], gender = other['gender'])
person("zs", 16, **other)
# 命名关键字参数：只接受特定参数名的参数，以符号*和位置参数进行分割，如果有可变参数则可以省略
def person(name, age, *, city='beijing', gender):
    print("name:", name, ", age:", age, ",city:", city, ",gender:", gender)
def person1(name, age, *args, city, gender):
    print("name:", name, ", age:", age, ",args:", args,",city:", city, ",gender:", gender)
person('ls', 20, city='shanghai', gender='man')
person('ls', 20, gender='man')
person1('ls', 20, 'i love study', city='shanghai', gender='man')
# 参数组合：必须参数，默认参数，可变参数，命名关键字参数，关键字参数
def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

def f2(a, b, c=0, *, d, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'd =', d, 'kw =', kw)

print(f1(1, 2))
print(f1(1, 2, 3))
print(f1(1, 2, 3, 'a', 'b'))
print(f1(1, 2, 3, 'a', 'b', x=99))
print(f2(1, 2, 3, d = 'a', x=99))
args = (1, 2, 3, 4)
kw = {'d': 99, "x": '#'}
print(f1(*args, **kw))
args = [1, 2, 3]
print(f2(*args, **kw))

def product(x, *args):
    pt = x
    for arg in args:
        pt = pt * arg
    return pt
# 测试
print('product(5) =', product(5))
print('product(5, 6) =', product(5, 6))
print('product(5, 6, 7) =', product(5, 6, 7))
print('product(5, 6, 7, 9) =', product(5, 6, 7, 9))
if product(5) != 5:
    print('failed!')
elif product(5, 6) != 30:
    print('failed!')
elif product(5, 6, 7) != 210:
    print('failed!')
elif product(5, 6, 7, 9) != 1890:
    print('failed!')
else:
    try:
        product()
        print('failed!')
    except TypeError:
        print('success!')
def testSlice():
    l = list(range(100))
    print("list=%s" % l)
    oddNumber = l[1::2]
    firstTenNumbers = l[:10]
    print("add number=%s, first numbers=%s" % (oddNumber, firstTenNumbers))
    c = ['Bob', 'Jack']
    print("c[-2:-1]:", c[-2: -1])
testSlice()

def trim(s):
    # str = " xxx "
    # str1 = str.strip()
    # print("str=%s, str1=%s" % (str, str1))
    if s is None:
        raise TypeError
    while s != "" and s[0] == " ":
        s = s[1:]
    while s != "" and s[-1] == " ":
        s = s[:-1]
    return s
def trim1(s):
    L = len(s)
    i = 0
    j = L - 1
    while i < L:
        if s[i] == ' ':
            i = i + 1
        else:
            break
    while j >= 0:
        if s[j] == ' ':
            j = j - 1
        else:
            j = j + 1
            break
    print("i=%s, j=%s" % (i, j))
    return s[i:j]

# 测试:
# if trim('hello  ') != 'hello':
#     print('failed!')
# elif trim('  hello') != 'hello':
#     print('failed!')
# elif trim('  hello  ') != 'hello':
#     print('failed!')
# elif trim('  hello  world  ') != 'hello  world':
#     print('failed!')
# elif trim('') != '':
#     print('failed!')
# elif trim('    ') != '':
#     print('failed!')
# else:
#     print('success!')
if trim1('hello  ') != 'hello':
    print('failed!')
elif trim1('  hello') != 'hello':
    print('failed!')
elif trim1('  hello  ') != 'hello':
    print('failed!')
elif trim1('  hello  world  ') != 'hello  world':
    print('failed!')
elif trim1('') != '':
    print('failed!')
elif trim1('    ') != '':
    print('failed!')
else:
    print('success!')
def findMinAndMax(L):
    min  = None
    max = None
    for x in L:
        if min is None:
            min = x
        elif x < min:
            min = x
        if max is None:
            max = x
        elif x > max:
            max = x
    return (min, max)
# 测试
if findMinAndMax([]) != (None, None):
    print('failed!')
elif findMinAndMax([7]) != (7, 7):
    print('failed!')
elif findMinAndMax([7, 1]) != (1, 7):
    print('failed!')
elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
    print('failed!')
else:
    print('success!')
def testListComprehensions():
    l = list(range(100))
    print(l)
    l = [x * x for x in range(10)]
    print(l)
    l = [odd for odd in range(100) if odd % 2 != 0]
    print(l)
    l = [m + n for m in 'ABC' for n in 'XYZ']
    print(l)
    d = {'x': 'A', 'y': 'B', 'z': 'C'}
    l = [k + "=" + v for k, v in d.items()]
    print(l)
    L = ['Hello', 'World', 'IBM', 'Apple']
    l = [s.lower() for s in L]
    print(l)
    L1 = ['Hello', 'World', 18, 'Apple', None]
    l = [s.lower() for s in L1 if isinstance(s, str)]
    print(l)

testListComprehensions()
# generator
def fib(max):
    n, a, b = 0, 0 , 1
    while n < max:
        # print(b)
        yield b
        a , b = b, a + b
        n = n + 1
    return None
g = fib(6)
print(g)
for x in g:
    print(x)
while True:
    try:
        x = next(g)
        print(x)
    except StopIteration as e:
        print("Generator return value", e.value)
        break

def triangles():
    # L = [1]
    # while True:
    #     yield L
    #     L = [x + y for k, x in enumerate([0] + L) for j, y in enumerate(L + [0]) if k == j]
    # return L
    L = [1]
    n = 0
    while n < 10:
        print(L)
        # L = [1] + [L[i - 1] + L[i] for i in range(1, len(L))] +[1]
        L = [x + y for k, x in enumerate([0] + L) for j, y in enumerate(L + [0]) if k == j]
        n = n + 1

triangles()

# Iterable 可直接作用于for循环
# Iterator 可作用于next()的函数对象，list, dict,  str不是Iterator, 可使用iter转化
def testIterable():
    print(isinstance([], Iterable))
    print(isinstance({}, Iterable))
    print(isinstance((x for x in range(10)), Iterable))
    print(isinstance('abc', Iterable))
    print(isinstance([], Iterator))
    print(isinstance({}, Iterator))
    print(isinstance((x for x in range(10)), Iterator))
    print(isinstance('abc', Iterator))
    print(isinstance(iter([x for x in range(10)]), Iterator))

testIterable()

# Higher-order function
def testFunction():
     # 变量可以指向函数，函数名也是变量
    a = abs(-10)
    f = abs
    print(a)
    print(f)
    print(f(-10))
# 使用函数参数的函数叫做高级函数
def testFunction1(x, y , f):
    return f(x) + f(y)

def testFunction2():
    # map的第一个参数（函数）作用于第二个参数(Iterable)可迭代对象的每个元素，返回一个Iterator
    l = map(lambda x: x * x, (x for x in range(1, 5)))
    # reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
    # 将两个参数的函数作用于序列中，从左到右以便将序列作为为单个值
    s = reduce(lambda x, y: x * y, (x for x in range(1, 5)))
    print("l=%s, s=%s" % (list(l), s))

testFunction()
# 函数可以作为变量传入函数参数
b = testFunction1(10, -2, abs)
testFunction2()
print(b)

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))
print(str2int("12589"))

def str2int1(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))
print(str2int("12589"))

def normalize(name):
    return name[0].upper() + name[1:].lower()
# 测试:
L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)
# 求积
def prod(L):
    def mul(x, y):
        return x * y
    return reduce(mul, L)
print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))
if prod([3, 5, 7, 9]) == 945:
    print('success!')
else:
    print('failed!')
digital_dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
def str2float(s):
    i, j = s.split('.')
    # lambda 表示匿名函数，冒号前面的表示函数参数
    left = reduce(lambda x, y: x * 10 + y, map(lambda x: digital_dict.get(x), i))
    s = list(map(lambda x: digital_dict.get(x), j));
    print("s=%s, -s=%s" % (s, s[::-1]))
    print(6 / 10)
    right = reduce(lambda x, y: x / 10 + y, list(map(lambda x: digital_dict.get(x), j))[::-1]) / 10
    return left + right
print('str2float(\'123.456\') =', str2float('123.456'))
if abs(str2float('123.456') - 123.456) < 0.00001:
    print('success!')
else:
    print('failed!')

# filter函数，函数作用于Iterable,根据函数的返回值觉得保留还是丢弃该元素，结果返回Iterator
def isOdd(x):
    return x % 2 != 0
def testFilter():
    r = list(filter(isOdd, [1, 2, 4, 5, 6]))
    print("r=", r)

testFilter()

def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n
def _not_divisible(n):
    return lambda x: x % n > 0
def primes():
    yield 2
    it = _odd_iter() # 初始序列
    while True:
        x = next(it)
        print("x=%s" % x)
        n = x # 返回序列的第一个数
        yield n
        it = filter(_not_divisible(n), it) # 构造新序列

# 打印1000以内的素数:
for n in primes():
    if n < 30:
        print(n)
    else:
        break

# 排序 sorted 可以对list排序
def testSorted():
    l  = [12, -12, 45, 78, 23, 65]
    r = sorted(l)
    print("sored l:%s, r:%s" % (l, r))
    s1  = ['A', 'a', 'C', 'e', 'E']
    s2 = sorted(s1, key=str.lower)
    print("sored s1:%s, s2:%s" % (s1, s2))
    L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    # sorted by name
    L1 = sorted(L, key=lambda x: x[0])
    L2 = sorted(L, key=lambda x: x[1])
    print("L=%s, L1=%s, L2=%s" % (L, L1, L2))

testSorted()
# 函数返回
def calc_sum(*args):
    sum = 0
    for x in args:
        sum = sum + x
    return sum
print("sum1:", calc_sum(*[1,2,3,4,5,6,7,8,9]))

def lazy_sum(*args):
    # 内部函数可以引用外部函数的参数和局部变量，相关参数和变量保存在返回函数中（闭包（Closure））
    # 返回函数不要引用任何循环变量或者后续会发送变化的变量。
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum;
ls = lazy_sum(*[1,2,3,4,5,6,7,8,9])
print("sum1:%s, sumll:%s" % (ls, ls()))

def createCounter():
    i = 0
    def counter():
        nonlocal i
        i = i + 1
        return i
    return counter

# 测试:
counterA = createCounter()
print(counterA(), counterA(), counterA(), counterA(), counterA()) # 1 2 3 4 5
counterB = createCounter()
if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    print('测试通过!')
else:
    print('测试失败!')

# 装饰器(Decorator)：在代码运行期间动态增加功能，是返回函数的高级函数

def log(func):
    # 复制func函数对象属性到wrapper
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print("call %s():" % func.__name__)
        return func(*args, **kw)
    return wrapper

def log1(txt):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("%s %s():" % (txt, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

@log
def now():
    print("20190321")
@log1('execute')
def now1():
    print("20190322")
# now = log(now)
now()
print("now name", now.__name__)
# now = log('execute')(now)
now1()
print("now name", now1.__name__)

def log1(txt = ''):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print("begin call")
            print("%s %s():" % (txt, func.__name__))
            f = func(*args, **kw)
            print("end call")
            return f
        return wrapper
    return decorator

@log1()
def f():
    pass

@log1('execute')
def f1():
    pass

f()
f1()

# 偏函数(Partial function),把一个函数的某个某些参数固定住（也就是设定默认值），返回一个新函数
# def partial(func, *args, **keywords):
#     def newfunc(*fargs, **fkeywords):
#         newkeywords = keywords.copy()
#         newkeywords.update(fkeywords)
#         return func(*args, *fargs, **newkeywords)
#     newfunc.func = func
#     newfunc.args = args
#     newfunc.keywords = keywords
#     return newfunc

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
def test():
    args = sys.argv
    if len(args) == 1:
        print('Hello, world!')
    elif len(args) == 2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')
# 在交互环境中,__name__等于__main__，其他模块引入时为模块名字
if __name__ == '__main__':
    test()
# 作用域，默认函数或者变量为public,private函数或者变量使用_或者__前缀，特殊函数或变量使用__xx__