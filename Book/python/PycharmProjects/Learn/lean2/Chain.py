class Chain(object):

    def __init__(self, path=''):
        self._path = path

    def __getattr__(self, path):
        return Chain("%s/%s" % (self._path, path))

    # 可调用对象，直接使用实例会回调此函数
    def __call__(self, param):
        return Chain('%s/%s' % (self._path, param))

    def __str__(self):
        return self._path

    __repr__ = __str__


# a = Chain().status.user.timeline.list
# print(a)
a = Chain().status.user.timeline.list
print(Chain().users('mechael').repos)