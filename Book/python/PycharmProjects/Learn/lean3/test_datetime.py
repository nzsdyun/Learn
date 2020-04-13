# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta, timezone

print(datetime.now())
print(type(datetime))
d = datetime(2019, 4, 15, 17, 56)
print(d)
print(d.timestamp())
t = 1429417200.0
print(datetime.fromtimestamp(t))
print(datetime.utcfromtimestamp(t))
d = datetime.strptime('2019-04-15 18:21:05', '%Y-%m-%d %H:%M:%S')
print(d)
print(datetime.strftime(datetime.now(), '%a %b %Y %m %d %p'))
# timedelta
d = datetime.now() - timedelta(hours=3)
print(d)
tz_utc_8 = timezone(timedelta(hours=8))
now = datetime.now()
print(now)
now = now.replace(tzinfo=tz_utc_8)
print(now)

utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
dj_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(dj_dt)
dj_dt1 = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(dj_dt1)


def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    print("dt", dt)
    g = re.match(r"UTC([+|-])(\d+):(\d+)", tz_str)
    print("groups():%s, group(1):%s,group(2):%s" % (g.groups(), g.group(1), g.group(2)))
    if g.group(1) is '+':
        delta = int(g.group(2))
    if g.group(1) is '-':
        delta = -int(g.group(2))
    return dt.replace(tzinfo=timezone(timedelta(hours=delta))).timestamp()


# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')
