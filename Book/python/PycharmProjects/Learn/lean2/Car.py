# 定制类
from typing import Any


class Car(object):
    count = 0
    # 限制属性
    __slots__ = ('name', 'color', 'speed')

    # 构造函数
    def __init__(self, name, color, speed):
        self._name = name
        self._color = color
        self._speed = speed

    # 打印良好的字串表示，供用户使用
    def __str__(self) -> str:
        return "Car name:" + self._name + ", color:" + self._color + ", speed:" + self._speed

    # 偷懒写法
    # __repr__ = __str__

    # 打印良好的字串表示，通常开发时使用，可以提供更多信息，直接打印对象时调用
    def __repr__(self):
        return "Car name:" + self._name + ", color:" + self._color + ", speed:" + self._speed

    # 可迭代对象，for...in..
    def __iter__(self):
        return self

    def __next__(self):
        Car.count += 1
        if Car.count > 2:
            raise StopIteration
        return Car.name

    # 获取第几个元素(list, dict, tuple)
    def __getitem__(self, item):
        # 某个元素
        if isinstance(item, int):
            pass
        # 切片
        if isinstance(item, slice):
            pass
        pass

    # 设置第几个元素的值
    def __setitem__(self, key, value):
        pass

    # 删除第几个元素
    def __delitem__(self, key):
        pass

    # 调用类或者实例的属性时，不存在时回调，默认返回None
    def __getattr__(self, item):
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)

