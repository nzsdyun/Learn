from types import MethodType

from lean2.Student import Student

student = Student("ls", 97, 28)
student.print_info()
# 不能直接修改实例的private属性，因为private属性被解析为_类名__name,下面语句只是绑定了一个新的属性
student.age = 17
student.print_info()
# 不建议修改，因为private属性解析后续版本可能更改
student._Student__age = 17
student.print_info()
student = Student("zs", 98, 25)
student.print_info()
# 不存在实例变量count会向上查找类变量count
print(student.count)
# 绑定实例变量count会屏蔽类变量Student.count
student.count = 1
print(student.count)
# 删除实例变量
del student.count
# 打印变量count
print(student.count)
# 绑定实例方法
def eat(self, s):
    print("eat", s)
student.eat = MethodType(eat, student)
# 调用绑定方法，调用实例方法默认会传入self实例引用
student.eat("rice")
def set_score(self, score):
    self.score = score
# 绑定类方法
Student.set_score = set_score
student.set_score(78)
student.print_info()

class Person(object):
    # 限制属性，只要tuple里面的属性才可以绑定
    # __slots__只对当前类有效，对子类不起效
    __slots__ = ('name', 'age')

p = Person()
p.name = "zz"
p.age = 25
# AttributeError: 'Person' object has no attribute 'ss'
# p.ss = "xx"

class Woman(Person):
    pass
wo = Woman()
# 运行正常
wo.ss = "woman"
print("woman=>", wo.ss)
class Man(Person):
    # __name私有属性会被自动转换为_类名__name
    __slots__ = ('__name')

man = Man()
# AttributeError: 'Man' object has no attribute '__name'
# man.__name = "xx"
# print("ss", man.__name)
man._Man__name = "man"
print("man=>", man._Man__name)

# 多重继承
class Child(Man, Woman):
    pass