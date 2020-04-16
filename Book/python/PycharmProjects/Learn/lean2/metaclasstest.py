# -*- coding: utf-8 -*-
# metaclass 元类, 可以使用metaclass 创建类和修改类，可以把类看成由metaclass创建出来的'实例'
# metaclass 是类的模板，必须从'type'继承
class ListMyMetaclass(type):
    # 创建类时调用
    # cls:类对象
    # name: 类名字
    # bases:父类集合
    # attrs:类属性和方法集合
    def __new__(cls, name, bases, attrs):
        print("cls:%s,name:%s,bases:%s,attrs:%s" % (cls, name, bases, attrs))
        attrs['add'] = lambda self, value: self.append(value)
        return super().__new__(cls, name, bases, attrs)


class MyList(list, metaclass=ListMyMetaclass):
    pass


L = MyList()
L.append(1)
print(L)


# orm简单实现

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        print('<cla:%s,name:%s,bases:%s,attrs:%s>' % (cls, name, bases, attrs))
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        print("attrs", attrs)
        for k in mappings.keys():
            attrs.pop(k)
        print("attrs", attrs)
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = name  # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        print('**kw', kw)
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))


class Field(object):

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')


class IntegerField(Field):
    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')


class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

    def sayhello(self):
        print("hello world")


u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')
u.save()
