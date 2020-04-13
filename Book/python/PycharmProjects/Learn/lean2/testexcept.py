# 所有错误类型继承BaseException
def testexcept1():
    print("START")
    try:
        print("begin cal")
        r = 10 / 0
        print("end cal")
    except ZeroDivisionError as e:
        print("except:", e)
    finally:
        print('finally')
    print("END")

testexcept1()

class FooError(ValueError):
    pass

def foo(s):
    n = int(s)
    if n==0:
        raise FooError('invalid value: %s' % s)
    return 10 / n

from functools import reduce

def str2num(s):
    return float(s)

def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)

def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 7.6')
    print('99 + 88 + 7.6 =', r)

main()

# assert
def foo(s):
    n = int(s)
    assert n != 0, 'n is zero!'
    return 10 / n

# foo(0)
# logging, logging不会抛出异常，并且可以输出到文件中
import logging
logging.basicConfig(level=logging.INFO)
s = '0'
n = int(s)
logging.info('n = %d' % n)
print(10 / n)
print("sssss")