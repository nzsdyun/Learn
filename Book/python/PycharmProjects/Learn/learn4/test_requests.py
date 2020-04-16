# -*- coding: utf-8 -*-
import requests

# get
# rq = requests.get('https://book.douban.com/subject_search')
# print('status_code', rq.status_code)
# print('txt', rq.text)
# get by params
# rq = requests.get('https://book.douban.com/subject_search', params={'search_text': '大秦帝国'})
# print('url:%s, request:%s,encoding:%s' % (rq.url, rq.request, rq.encoding))
# get bytes content
# print('content', rq.content)
# rq = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20%3D%202151330&format=json')
# get by headers
# rq = requests.get('https://www.douban.com/', headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit'})
# post
# rq = requests.post('https://accounts.douban.com/login', data={'form_email': 'abc@example.com', 'form_password': '123456'})
# post by files
# upload_files = {'file': open('report.xls', 'rb')}
# rq = requests.post(url, files=upload_files)
# cookies
# cs = {'token': '12345', 'status': 'working'}
# r = requests.get(url, cookies=cs)