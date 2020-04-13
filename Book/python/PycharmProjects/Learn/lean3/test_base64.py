# -*- coding: utf-8 -*-
import base64

# 三字节二进制数转换成四字节文本数据
be = base64.b64encode(b'binary\x00string')
print(be)
bd = base64.b64decode(b'YmluYXJ5AHN0cmluZw==')
print(bd)
# URL or filesystem safe base64 strings, '+', '-' covert to '-','_'
unsafe_be = base64.b64encode(b'i\xb7\x1d\xfb\xef\xff')
print(unsafe_be)
safe_be = base64.urlsafe_b64encode(b'i\xb7\x1d\xfb\xef\xff')
print(safe_be)
safe_de = base64.urlsafe_b64decode('abcd--__')
print(safe_de)


# Base64是一种任意二进制到文本字符串的编码方法，常用于在URL、Cookie、网页中传输少量二进制数据。
def safe_base64_decode(s):
    while len(s) % 4 > 0:
        s += b'='
    return base64.urlsafe_b64decode(s)


# 测试:
assert b'abcd' == safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
assert b'abcd' == safe_base64_decode(b'YWJjZA'), safe_base64_decode('YWJjZA')
print('ok')
