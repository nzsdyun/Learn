class Animal(object):
    def run(self):
        print("Animal is running")

class Dog(Animal):
    # 方法重写
    def run(self):
        print("Dog is running")

class Cat(Animal):
    def run(self):
        print("Cat is running")

class Car(object):
    def run(self):
        print("Car is running")
# 多态，运行期确定对象方法，python是动态语言，只要对象拥有run方法就可以，而无需关心是不是animal类或子类（鸭子特性）
def run_twice(animal):
    animal.run()
    animal.run()

a = Animal()
d = Dog()
c = Cat()
a.run()
d.run()
c.run()

run_twice(a)
run_twice(d)
run_twice(c)

car = Car()
run_twice(car)

# 获取对象所有属性和方法
print(dir(car))
# setattr绑定属性, 等价于car.name = 'm'
setattr(car, 'name', 'm')
# getattr获取属性值
print(getattr(car, 'name', 'L'))
# type判断类型, isinstance判断对象是否是一个类和其父类
print(type('ABC'))
print(type('ABC') == str)
print(isinstance('ABC', (str, object)))
# hasattr判断是否有这个属性
print(hasattr(car, 'name'))