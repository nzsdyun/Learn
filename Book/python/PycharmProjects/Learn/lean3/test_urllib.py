# -*- coding: utf-8 -*-
import json
from urllib import request
import urllib.parse


# with request.urlopen('http://www.baidu.com/') as f:
#     print("status:%s, reason:%s" % (f.status, f.reason))
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print(f.read().decode('utf-8'))

# req = request.Request('http://www.douban.com/')
# req.add_header('User-Agent',
#                'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# with request.urlopen(req) as f:
#     print("status:%s, reason:%s" % (f.status, f.reason))
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print(f.read().decode('utf-8'))

# req = request.Request('https://book.douban.com/subject_search')
# req.add_header('User-Agent',
#                'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
# params = urllib.parse.urlencode({'search_text': '大秦帝国'})
# with request.urlopen(req, data=params.encode('utf-8')) as f:
#     print("status:%s, reason:%s" % (f.status, f.reason))
#     for k, v in f.getheaders():
#         print('%s: %s' % (k, v))
#     print(f.read().decode('utf-8'))
def fetch_data(url):
    with urllib.request.urlopen(url) as f:
        content = f.read().decode('utf-8')
        print("content:", content)
        return json.loads(content, encoding='utf-8')
    return None


# 测试
URL = 'https://news-at.zhihu.com/api/4/news/latest'
data = fetch_data(URL)
print(data)
# assert data['query']['results']['channel']['location']['city'] == 'Beijing'
print('ok')
