# 从object继承，object所有类的父类
class Student(object):
    # 类变量
    count = 0
    # 构造函数， self 实例本身，调用时不需要传递
    def __init__(self, name, score, age):
        # 实例变量默认为public,private 需要使用__前缀
        self.name = name
        self.score = score
        self.__age = age
        Student.count += 1

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = age

    def print_info(self):
        print('name: %s, score: %s, age:%s, count:%s' % (self.name, self.score, self.__age, Student.count))
