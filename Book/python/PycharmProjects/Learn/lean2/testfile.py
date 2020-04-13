# -*- coding: utf-8 -*-
# 文件操作由操作系统提供，不允许普通程序直接操作
import os
import shutil
from io import StringIO, BytesIO


def readfile():
    # f = None
    # try:
    #     pc = os.path.abspath(".")
    #     print('pc:', pc)
    #     f = open(os.path.join(pc, "Student.py"), 'r', encoding='utf-8')
    #     print(f.read())
    # except FileNotFoundError as e:
    #     print(e)
    # finally:
    #     # 文件必须关闭
    #     if f:
    #         f.close()
    pc = os.path.abspath(".")
    ps = os.path.join(pc, "Student.py")
    # with等价于f try: finally: if f: f.close
    # with open(ps, mode='r', encoding='utf-8') as f:
    #     print(f.read())

    with open(ps, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            print(line)


readfile()


def testStringIO():
    sio = StringIO()
    sio.write("hello")
    sio.write(",")
    sio.write("world!")
    print(sio.getvalue())
    # 游标重置为文件开始位置
    sio.seek(0)
    # 覆盖原有字串
    sio.write("Hi")
    sio.write("Good")
    print(sio.getvalue())
    sio.seek(0)
    # 读取当前游标后的所有文字
    print(sio.readlines())
    sio = StringIO('Hello!\nHi!\nGoodbye!')
    for s in sio:
        print(s.strip())


testStringIO()


def testBytesIO():
    byteio = BytesIO()
    byteio.write("中文".encode("utf-8"))
    print(byteio.getvalue())


testBytesIO()


def test_file():
    print('name:{}, environ:{}, environ path:{}'.format(os.name, os.environ, os.environ.get("PATH")))
    # 当前目录
    current_dir = os.path.abspath('.')
    print(current_dir)
    # join拼接路径
    test_log_dir = os.path.join(current_dir, "test_log")
    # 创建目录
    # os.mkdir(test_log_dir)
    # 删除目录
    # os.rmdir(test_log_dir)
    test_log = os.path.join(current_dir, "test_log.txt")
    # 创建空文件,nt不可用
    # os.mknod(test_log)
    open(test_log, "w")
    # 获取文件扩展名
    txt = os.path.splitext(test_log)
    print("txt:", txt)
    # 重命名
    # test_log1 = os.rename(test_log, "test_log1.txt")
    # 删除文件
    os.remove(test_log)
    # 列出当前目录下的所有文件
    fl = [x for x in os.listdir('.') if os.path.isfile(x)]
    print(fl)
    # shutil copyfile等


test_file()


def list_all_files(path):
    # 切换路径
    os.chdir(path)
    for x in os.listdir(path):
        # 切换路径
        os.chdir(path)
        if os.path.isfile(x):
            # 绝对路径
            abs_path = os.path.abspath(x)
            print("abs_path", abs_path)
            # 相对路径
            rel_path = os.path.relpath(x)
            print("rel_path", rel_path)
        elif os.path.isdir(x):
            list_all_files(os.path.join(path, x))


def search_file():
    # 切换到d盘
    os.chdir("F:/")
    # 获取当前路径
    current_path = os.getcwd()
    print("current_path:", current_path)
    # 列出当前路径的所有文件和文件夹
    current_dir = os.listdir(current_path)
    print("current_dir:", current_dir)
    ps = os.path.join(current_path, "Program_Files").replace("\\\\", "\\")
    print("ps:", ps)
    # 打印目录下所有文件
    # list_all_files(ps)


search_file()
