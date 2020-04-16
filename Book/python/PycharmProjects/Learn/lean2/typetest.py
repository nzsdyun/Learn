class Hello(object):
    def hello(self, param='world'):
        print("hello, %s" % param)


h = Hello()
h.hello()
# 使用type查看类型或者变量的类型
print(type(Hello))
print(type(h))


# 创建新类型 class type(name, bases, dict)
def fn(self, param='world'):
    print("hello, %s" % param)


# 等价于class Hello(object)定义,动态创建类
Hello = type('Hello', (object,), dict(hello=fn))
h1 = Hello()
h1.hello()
print(type(h1))
