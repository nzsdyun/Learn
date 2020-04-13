# -*- coding: utf-8 -*-
import re

b = re.match(r'\d{3}-\d{4}', '010-4567')
print(b)
# 拆分
print('a b   c'.split(' '))
print(re.split(r'[\s]+', 'a b   c'))
# 分组
g = re.match(r'(\d{3})-(\d{3,8})', '010-4567')
print(g)
print("group(0):%s, group(1):%s, group(2):%s" % (g.group(0), g.group(1), g.group(2)))
# 贪婪匹配，尽可能的匹配多的字符，默认
print(re.match(r'^(\d+)(0*)$', '1023000').groups())
# 非贪婪匹配(*?, +?, ??)
print(re.match(r'^(\d+?)(0*)$', '1023000').groups())
# 预编译正则表达式
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
print(re_telephone.match('010-4567').groups())
print(re_telephone.match('012-456745').groups())


def is_valid_email(addr):
    return re.match(r'^[\w|.]+@\w+.com$', addr)


# 测试:
assert is_valid_email('someone@gmail.com')
assert is_valid_email('bill.gates@microsoft.com')
assert not is_valid_email('bob#example.com')
assert not is_valid_email('mr-bob@example.com')
print('ok')


def name_of_email(addr):
    return re.match(r'<?(\w+\s?\w+)>?\s?\w*?@(\w+)', addr).group(1)


# 测试:
assert name_of_email('<Tom Paris> tom@voyager.org') == 'Tom Paris'
assert name_of_email('tom@voyager.org') == 'tom'
print('ok')

print(re.match(r'4\d\d', str(403)).string)
print(re.match(r'4\d\d', str(404)))
print(re.match(r'4\d\d', str(408)))
