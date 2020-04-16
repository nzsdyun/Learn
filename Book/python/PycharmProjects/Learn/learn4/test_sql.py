# -*- coding: utf-8 -*-
import sqlite3
# 连接sqlite3数据库，如果不存在自动创建
conn = sqlite3.connect('example.db')
# 创建cursor
c = conn.cursor()
# # 创建表
# c.execute('''CREATE TABLE stocks
#              (date text, trans text, symbol text, qty real, price real)''')
# # 插入一行数据
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# # 保存更改
# conn.commit()
# # 关闭数据库
# conn.close()
# Never do this -- insecure! 容易SQL注入
symbol = 'RHAT'
c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)
# Do this instead, 使用占位符?
t = ('RHAT',)
c.execute('SELECT * FROM stocks WHERE symbol=?', t)
# 输出一行数据
print(c.fetchone())
# Larger example that inserts many records at a time， 重复执行sql语句
purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
             ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
             ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
            ]
c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
# iterator 迭代输出
for row in c.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)