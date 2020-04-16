# -*- coding: utf-8 -*-
import os
import pickle
import json


def test_pickle():
    d = dict(name='blob', age=26, score=98)
    print("d", d)
    f = open(os.path.join(os.path.abspath("."), "test_log1.txt"), 'wb')
    pickle.dump(d, f)
    f.close()
    f = open(os.path.join(os.path.abspath("."), "test_log1.txt"), 'rb')
    r = pickle.load(f)
    print("r", r)
    f.close()


test_pickle()


def test_json():
    d = {'name': 'blob', 'age': 28}
    sd = json.dumps(d)
    print("sd", sd)
    jd = json.loads(sd)
    print("jd", jd)


test_json()


class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score

    def __str__(self):
        # print("(name:%s, age:%s, score:%s)" % (self.name, self.age, self.score))
        print("(cls:%s, name:%s, age:%s, score:%s)" % (str(self.__class__.__name__), self.name, self.age, self.score))
        return "(cls:%s, name:%s, age:%s, score:%s)" % (str(self.__class__.__name__), self.name, self.age, self.score)

    __repr__ = __str__


def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


def test_json_class():
    sd = Student("Ls", 28, 78)
    print("sd", sd)
    sdr = json.dumps(sd, default=student2dict)
    print("sdr", sdr)
    print(json.dumps(sd, default=lambda obj: obj.__dict__))
    sd1 = json.loads(sdr, object_hook=dict2student)
    print("sd1", sd1)


test_json_class()

obj = dict(name='小明', age=20)
s = json.dumps(obj, ensure_ascii=True)
print("s", s)