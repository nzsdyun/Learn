# -*- coding: utf-8 -*-
from collections import namedtuple, deque, defaultdict, OrderedDict, ChainMap, Counter

# namedtuple
# 定义namedtuple类型
Point = namedtuple('Point', ['x', 'y'])
# 使用新创建的namedtuple类型创建对象
point = Point(1, 2)
# 使用属性访问
print("(x:%s, y:%s)" % (point.x, point.y))
# 下标访问
print("(x:%s, y:%s)" % (point[0], point[1]))
x, y = point
# unpack like a regular tuple
print("(x:%s, y:%s)" % (x, y))
# 创建一个新实例从序列或者迭代
t = [11, 12]
point2 = Point._make(t)
print('point2', point2)
print(isinstance(point2, Point))
print(isinstance(point2, tuple))

# Deque双端队列
dq = deque('bcd')
for v in dq:
    print("v:", v)
# 右侧添加
dq.append('e')
print(dq)
# 左侧添加
dq.appendleft('a')
print(dq)
# 右侧删除
itemR = dq.pop()
print(itemR)
# 左侧删除
itemL = dq.popleft()
print(itemL)
print(dq)
# 转化列表
ldq = list(dq)
print(ldq)
# 右旋等价于dq.appendleft(dq.pop())
dq.rotate(1)
print(dq)
# 左旋等价于de.append(dq.popleft())
dq.rotate(-1)
print(dq)
# 插入
dq.insert(1, 'f')
print(dq)
# 删除
dq.remove('f')
print(dq)

# defaultdict
dt = defaultdict(lambda: 'N/A')
dt['key1'] = 'abc'
print(dt['key1'])
print(dt['key2'])


# OrderedDict
class LRU(OrderedDict):

    def __init__(self, maxsize=128, *args, **kwargs) -> None:
        self.maxsize = maxsize
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        value = super().__getitem__(key)
        # 将key对应的值移到dict右侧
        self.move_to_end(key)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, key)
        if len(self) > self.maxsize:
            oldest = next(iter(self))
            del self[oldest]


lru_dict = LRU(3, {'a': 65, 'b': 66, 'c': 67})
print(lru_dict)
lru_dict['a']
print(lru_dict)
lru_dict['d'] = 59
print(lru_dict)


class LastUpdatedOrderedDict(OrderedDict):

    def __init__(self, capacity, *args, **kwargs):
        self._capacity = capacity
        super(LastUpdatedOrderedDict, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        # containsKey = 1 if key in self else 0
        # if len(self) - containsKey >= self._capacity:
        #     last = self.popitem(last=False)
        #     print('remove:', last)
        # if containsKey:
        #     del self[key]
        #     print('set:', (key, value))
        # else:
        #     print('add:', (key, value))
        # OrderedDict.__setitem__(self, key, value)
        super().__setitem__(key, value)
        if len(self) > self._capacity:
            oldest = next(iter(self))
            del self[oldest]


lud_dict = LastUpdatedOrderedDict(3, {'a': 65, 'b': 66, 'c': 67})
print(lud_dict)
lud_dict['a']
print(lud_dict)
lud_dict['d'] = 59
print(lud_dict)

# ChainMap 组合多个map到一个map中
baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
lp = list(ChainMap(adjustments, baseline))
print(lp)
combined = baseline.copy()
combined.update(adjustments)
print(list(combined))

# Counter
c = Counter()
c.update('asasdasdaaa')
print(c)
