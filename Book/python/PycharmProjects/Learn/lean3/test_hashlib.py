# -*- coding: utf-8 -*-
import hashlib
import hmac
import random

# 摘要算法，又称哈希算法，通过函数把任意长度的数据转换成固定长度字符串
# md5(128bit)
md5 = hashlib.md5()
md5.update('how to use md5 in python hashlib?'.encode('utf-8'))
md5.update('python hashlib?'.encode('utf-8'))
print(md5.hexdigest())

# sha1(160)
sha1 = hashlib.sha1()
sha1.update('how to use md5 in python hashlib?'.encode('utf-8'))
sha1.update('python hashlib?'.encode('utf-8'))
print(sha1.hexdigest())

db = {
    'michael': 'e10adc3949ba59abbe56e057f20f883e',
    'bob': '878ef96e86145580c38c87f0410ad153',
    'alice': '99b1c2188db85afee403b1536010c2c9'
}


def calc_md5(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def login(user, password):
    if user in db:
        md5_password = calc_md5(password)
        return md5_password == db[user]
    return False


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')


def get_md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


class User(object):
    def __init__(self, username, password):
        self.username = username
        self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        print("salt:", self.salt)
        self.password = get_md5(password + self.salt)


db = {
    'michael': User('michael', '123456'),
    'bob': User('bob', 'abc999'),
    'alice': User('alice', 'alice2008')
}


def login(username, password):
    if username in db:
        user = db[username]
        print('salt password: %s, password:%s' % (user.password, get_md5(password + user.salt)))
        return user.password == get_md5(password + user.salt)
    return False


# 测试:
assert login('michael', '123456')
assert login('bob', 'abc999')
assert login('alice', 'alice2008')
assert not login('michael', '1234567')
assert not login('bob', '123456')
assert not login('alice', 'Alice2008')
print('ok')

# Hmac(Keyed-Hashing for Message Authentication。它通过一个标准算法，在计算哈希的过程中，把key混入计算过程中)
message = b'Hello, world!'
key = b'secret'
hc = hmac.new(key, message, digestmod='MD5')
print(hc.hexdigest())


def hmac_md5(k, s):
    return hmac.new(k.encode('utf-8'), s.encode('utf-8'), digestmod='MD5').hexdigest()


class User1(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)

db1 = {
    'michael': User1('michael', '123456'),
    'bob': User1('bob', 'abc999'),
    'alice': User1('alice', 'alice2008')
}

def login1(username, password):
    user = db1[username]
    return user.password == hmac_md5(user.key, password)


# 测试:
assert login1('michael', '123456')
assert login1('bob', 'abc999')
assert login1('alice', 'alice2008')
assert not login1('michael', '1234567')
assert not login1('bob', '123456')
assert not login1('alice', 'Alice2008')
print('ok')
