# -*- coding: utf-8 -*
import logging
import os
import random
import sys
import time

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


class IpAgent(object):

    @staticmethod
    def get_free_ip_agent():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        for i in range(1, 36):
            time.sleep(2)
            print('第' + str(i) + '页')
            url = 'http://www.xicidaili.com/nn/' + str(i)
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            all_trs = soup.find_all('tr')
            for tr in all_trs[1:]:
                all_tds = tr.find_all('td')
                ip = all_tds[1].get_text()
                port = all_tds[2].get_text()
                anonymous = all_tds[4].get_text()
                type = all_tds[5].get_text()
                for j in all_tds[6].find_all("div", attrs={"class": "bar"}):
                    speed = j.get('title')
                with open(os.path.join('../agent', 'ip.csv'), 'a+') as f:
                    f.write(ip + ',' + port + ',' + anonymous + ',' + type + ',' + speed + '\n')
            # random.randint产生随机整数
            time.sleep(2 + float(random.randint(1, 100)) / 20)

    @staticmethod
    def get_one_ip_agent(request_url, headers):
        df = pd.read_csv('../agent/ip.csv', header=None, names=["ip", "port", "anonymous", "proxy_type", "speed"])

        proxy_types = ["{}".format(i) for i in np.array(df['proxy_type'])]
        ips = ["{}".format(i) for i in np.array(df['ip'])]
        ports = ["{}".format(i) for i in np.array(df['port'])]
        proxy_url = ['{0}://{1}:{2}'.format(proxy_types[i], ips[i], ports[i]) for i in range(len(ips))]
        proxy_type = ['{}'.format(i) for i in proxy_types]
        for i in range(200):
            time.sleep(3)
            proxies = {
                proxy_type[i]: proxy_url[i]
            }
            try:
                response = requests.get(request_url, headers=headers, proxies=proxies)
                if response.status_code == 200:
                    print("ip:{0}:type:{1}".format(proxy_type[i], proxy_url[i]))
                    return proxies
                else:
                    continue
            except Exception as e:
                print('invalid ip and port', e)

    @staticmethod
    def random_get_one_agent(request_url, headers):
        df = pd.read_csv('../agent/ip.csv', header=None, names=["ip", "port", "anonymous", "proxy_type", "speed"])
        proxy_types = ["{}".format(i) for i in np.array(df['proxy_type'])]
        ips = ["{}".format(i) for i in np.array(df['ip'])]
        ports = ["{}".format(i) for i in np.array(df['port'])]
        proxy_url = ['{0}://{1}:{2}'.format(proxy_types[i], ips[i], ports[i]) for i in range(len(ips))]
        proxy_type = ['{}'.format(i) for i in proxy_types]
        # 重试5次
        for index in range(5):
            random_index = int(random.random() * len(ips))
            proxies = {
                proxy_type[random_index]: proxy_url[random_index]
            }
            # test ip valid
            try:
                response = requests.get(request_url, headers=headers, proxies=proxies)
                if response.status_code == 200:
                    return proxies
                else:
                    continue
            except Exception as e:
                logging.error("获取ip代理失败:{0}".format(e))
                return None
        return None

    @staticmethod
    def verify_ip_agent():
        df = pd.read_csv('../agent/ip.csv', header=None, names=["ip", "port", "anonymous", "proxy_type", "speed"])

        proxy_types = ["{}".format(i) for i in np.array(df['proxy_type'])]
        ips = ["{}".format(i) for i in np.array(df['ip'])]
        ports = ["{}".format(i) for i in np.array(df['port'])]

        proxy_url = ['{0}://{1}:{2}'.format(proxy_types[i], ips[i], ports[i]) for i in range(len(ips))]

        proxy_type = ['{}'.format(i) for i in proxy_types]
        for i in range(200):
            time.sleep(1)
            proxies = {
                proxy_type[i]: proxy_url[i]
            }
            try:
                response = requests.get('https://book.douban.com/', proxies=proxies)
            except Exception as e:
                print('invalid ip and port', e)
            else:
                code = response.status_code
                if code == 200:
                    print('effective ip')
                    with open(os.path.join('../agent', 'effective.csv'), 'a+') as f:
                        f.write(proxy_type[i] + ',' + proxy_url[i] + '\n')
                else:
                    print('invalid ip and port')


if __name__ == '__main__':
    # IpAgent.get_free_ip_agent()
    # IpAgent.verify_ip_agent()
    # ip_agent = IpAgent.get_one_ip_agent('https://book.douban.com/', {'User-Agent': UserAgent.get_user_agent()})
    ip_agent = IpAgent.random_get_one_agent()
    print(ip_agent)
    pass
