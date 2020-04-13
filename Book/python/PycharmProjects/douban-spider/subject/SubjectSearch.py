# -*- coding: utf-8 -*
import os
import random
import re
import threading
import time
from Queue import Queue, Empty
from multiprocessing import Process, freeze_support

import execjs  # 这个库是PyExecJS
import mysql.connector
import sys

import oss2
import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime

from Config import Config
from subject.Book import Book
from UserAgent import UserAgent
from IpAgent import IpAgent

reload(sys)
sys.setdefaultencoding('utf-8')
# 配置log日志文件
logging.basicConfig(
    filename='../log/' + datetime.strftime(datetime.now(), '%Y-%m-%d') + "_" + os.path.basename(__file__).split('.')[
        0] + '.log',
    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.INFO, filemode='a',
    datefmt='%Y-%m-%d %I:%M:%S %p')
# 豆瓣图书搜索页
DOU_BAN_SUBJECT_SEARCH_URL = "https://book.douban.com/subject_search"
# 请求队列
req_queue = Queue()
# 失败的请求队列
bad_queue = Queue()
# 详细页面请求队列
req_details_queue = Queue()
# 详细页面失败的请求队列
bad_details_queue = Queue()
DECRYPT_JS = None
SUCCESS_COUNT = 0

# oss bucket
BUCKET = oss2.Bucket(oss2.Auth(Config.OSS_ACCESS_KEY_ID, Config.OSS_ACCESS_KEY_SECRET), Config.OSS_ENDPOINT,
                     Config.OSS_BUCKET_NAME)
IMAGE_BUCKET = oss2.Bucket(oss2.Auth(Config.OSS_ACCESS_KEY_ID, Config.OSS_ACCESS_KEY_SECRET), Config.OSS_ENDPOINT,
                           Config.OSS_IMAGES_BUCKET_NAME)


def get_db_data():
    try:
        cnn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            passwd=Config.DB_PWD,
            db=Config.DB_NAME,
            charset=Config.DB_CHARSET)
        cur = cnn.cursor()
        cur.execute("SELECT * FROM book WHERE cover IS NULL OR intro='暂无'")
        result = cur.fetchall()
        cur.close()
        cnn.close()
        return result
    except Exception as e:
        logging.error("获取数据库图书书籍出错:{0}".format(e))
        return None
    return None
    # cnn = mysql.connector.connect(
    #     host=Config.DB_HOST,
    #     port=Config.DB_PORT,
    #     user=Config.DB_USER,
    #     passwd=Config.DB_PWD,
    #     db=Config.DB_NAME,
    #     charset=Config.DB_CHARSET)
    # cur = cnn.cursor()
    # cur.execute("SELECT * FROM book WHERE cover IS NULL OR intro='暂无';")
    # result = cur.fetchall()
    # cur.close()
    # cnn.close()
    # return result


def get_req_queue():
    data = get_db_data()
    if data:
        for item in data:
            book = Book(str(item[0]).decode('utf-8'), str(item[1]).decode('utf-8'), str(item[2]).decode('utf-8'),
                        str(item[3]).decode('utf-8'), str(item[4]).decode('utf-8'), str(item[5]).decode('utf-8'),
                        str(item[6]).decode('utf-8'), str(item[7]).decode('utf-8'), str(item[8]).decode('utf-8'),
                        str(item[9]).decode('utf-8'), str(item[10]).decode('utf-8'), str(item[11]).decode('utf-8'),
                        str(item[12]).decode('utf-8'))
            req_queue.put(book)


def process_req_queue(url, req_q, req_details_q, bad_q=None):
    while req_queue.qsize() > 0:
        try:
            rq_item = req_q.get()
            # 随机获取一个用户代理
            headers = {'User-Agent': UserAgent.get_user_agent()}
            # 随机获取一个ip代理
            proxies = IpAgent.random_get_one_agent(url, headers)
            rp = requests.get(url, headers=headers, proxies=proxies, params={'search_text': rq_item.name})
            response_code = rp.status_code
            if response_code == 200:
                logging.info('豆瓣搜索<<{0}>>书籍详情列表成功'.format(rq_item.name))
                details_url = decrypt_js_content(rp.text, rq_item.name)
                # 加入详情搜索页队列
                if details_url:
                    rq_item.attach_url = details_url
                    req_details_q.put(rq_item)
            elif bad_q:
                logging.info('豆瓣搜索<<{0}>>书籍详情列表失败，请求放入Bad队列'.format(rq_item.name))
                bad_q.put(rq_item)
            # 随机休眠1s到3s以内的时间，防止被封ip
            time.sleep(1 + random.random() * 2)
        except BaseException as e:
            logging.error("豆瓣搜索<<{0}>>书籍详情列表出错:{1}，请求放入Bad队列".format(rq_item.name, e))
            if bad_q:
                bad_q.put(rq_item)


def process_req_details_queue(req_details_q, bad_details_q=None):
    while True:
        try:
            details_item = req_details_q.get(True, timeout=10)
            if details_item:
                print(details_item)
                if details_item.cover == 'None' or details_item.intro == '暂无' or details_item.intro == 'None':
                    print("details item attach_url:", details_item.attach_url)
                    # 随机获取一个用户代理
                    headers = {'User-Agent': UserAgent.get_user_agent()}
                    # 随机获取一个ip代理
                    proxies = IpAgent.random_get_one_agent(details_item.attach_url, headers)
                    rp = requests.get(details_item.attach_url, headers=headers, proxies=proxies)
                    response_code = rp.status_code
                    if response_code == 200:
                        logging.info("获取<<{0}>>详情页成功".format(details_item.name))
                        details_content = parse_details_content(rp.text, details_item)
                        if details_content:
                            # details_item.name = details_content['name'] if details_content[
                            #     'name'] else details_item.name
                            # details_item.author = details_content['author'] if details_content[
                            #     'author'] else details_item.author
                            # details_item.press = details_content['press'] if details_content[
                            #     'press'] else details_item.press
                            details_item.cover = details_content[
                                'cover'] if details_item.cover == 'None' else details_item.cover
                            details_item.intro = details_content[
                                'intro'] if details_item.intro == '暂无' else details_item.intro
                            details_item.update_time = details_content['update_time'] if details_content[
                                'update_time'] else details_item.update_time
                            print("details item:", details_item)
                            # 上传数据库
                            process_upload_db(details_item)
                    elif bad_details_q:
                        logging.info("获取<<{0}>>详情页失败，请求放入Bad队列".format(details_item.name))
                        bad_details_q.put(details_item)
                # 随机休眠1s到3s以内的时间，防止被封ip
                time.sleep(1 + random.random() * 2)
            else:
                # 上传数据库
                # process_upload_db(details_item)
                pass
        except Empty:
            logging.info('%s 执行完毕' % threading.current_thread().name)
            break


def process_upload_oss(image_name, image_content=None, image_local_file=None, file_name=None, file_content=None,
                       file_local_file=None):
    try:
        if image_name:
            result = None
            if image_content:
                result = IMAGE_BUCKET.put_object(image_name, image_content)
            elif image_local_file:
                with open(image_local_file, 'rb') as f:
                    result = IMAGE_BUCKET.put_object(image_name, f)
            if result.status == 200:
                logging.warning("上传{0}封面成功".format(image_name))
                return True
            else:
                logging.warning("上传{0}封面失败".format(image_name))
                return False
        if file_name:
            result = None
            if file_content:
                result = BUCKET.put_object(file_name, file_content)
            elif file_local_file:
                with open(file_local_file, 'rb') as f:
                    result = BUCKET.put_object(file_name, f)
            if result.status == 200:
                logging.warning("上传{0}文件成功".format(file_name))
                return True
            else:
                logging.warning("上传{0}封面失败".format(image_name))
                return False
    except Exception as e:
        if image_name:
            logging.error("上传{0}封面出错:{1}".format(image_name, e))
        if file_name:
            logging.error("上传{0}文件出错:{1}".format(file_name, e))
        return False
    return False


def process_upload_db(details_item, insert=False):
    try:
        cnn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            passwd=Config.DB_PWD,
            db=Config.DB_NAME,
            charset=Config.DB_CHARSET)
        cur = cnn.cursor()
        if insert:
            pass
        else:
            # 只更新 cover, intro, update_time
            cur.execute(
                "UPDATE book SET cover=%s,intro=%s,update_time=%s WHERE book_id=%s",
                params=(str(details_item.cover).encode('utf-8'), str(details_item.intro).encode('utf-8'),
                        str(details_item.update_time).encode('utf-8'), str(details_item.book_id).encode('utf-8')))
        cnn.commit()
        cur.close()
        cnn.close()
        logging.info("书籍<<{0}>>存入数据库成功".format(details_item.name))
        global SUCCESS_COUNT
        SUCCESS_COUNT = SUCCESS_COUNT + 1
    except Exception as e:
        logging.error("书籍<<{0}>>存入数据库出错:{1}".format(details_item.name, e))


def parse_details_content(content, details_item):
    try:
        logging.info("开始解析<<{0}>>书籍详情页".format(details_item.name))
        bsp = BeautifulSoup(content, features="html.parser")
        name = ''
        author = ''
        press = ''
        cover = ''
        intro = ''
        if bsp.select('#wrapper > h1 > span'):
            name = bsp.select('#wrapper > h1 > span')[0].string
        elif bsp.find('span', property='v:itemreviewed'):
            name = bsp.find('span', property='v:itemreviewed').string
        if bsp.select("#mainpic > a > img"):
            cover = bsp.select("#mainpic > a > img")[0]['src']
        if bsp.select('div.intro'):
            for pc in bsp.select('div.intro')[0].find_all('p'):
                if not re.match(r'.*\s*[(|（]*展开全部[)|）]*\s*.*', pc.string):
                    intro += '\n\t' + unicode(pc.string) + '\n'
        else:
            intro = '暂无'
        # 如果正则没有过滤掉，直接replace替换空字符
        if intro and intro.find('展开全部'):
            intro = intro.replace('(展开全部)', '').replace('展开全部', '').replace('（展开全部）', '')
        update_time = str(long(time.mktime(datetime.now().timetuple())))
        logging.info(
            "({0},{1},{2},{3},{4},{5})".format(name, author, cover, press, intro, update_time))
        save_cover_name = name + "_" + update_time + cover[cover.rindex("."):]
        # 保存cover
        upload_result = False
        with open(
                os.path.join("D:\\douban\\images", save_cover_name),
                mode='wb') as fq:
            cq = requests.get(cover)
            fq.write(cq.content)
            logging.info("保存<<{0}>>图书封面成功!!!".format(name))
            # 只有数据库不存在cover才上传oss
            if details_item.cover == 'None':
                # 上传oss,重试三次
                for count in range(3):
                    upload_result = process_upload_oss(save_cover_name, image_content=cq.content)
                    if upload_result:
                        break
                if upload_result:
                    # 上传成功使用oss链接
                    cover = Config.OSS_IMAGES_BASE_URL + "/" + save_cover_name
        return {"name": name, "author": author, "cover": cover, "press": unicode(press), "intro": intro,
                "update_time": update_time}
        # process_upload_db(details_item)
    except Exception as e:
        logging.error("解析书籍<<{0}>>详情出错:{1}".format(details_item.name, e))
        return None
    return None


def decrypt_js_content(data_content, name):
    try:
        logging.info("开始解密<<{0}>>搜索详情列表".format(name))
        # 豆瓣js加密内容
        enc_data = re.search('window.__DATA__ = "([^"]+)"', data_content).group(1)
        # 解密js
        dec_js = decrypt_js()
        ctx = execjs.compile(dec_js)
        data = ctx.call('decrypt', enc_data)
        # 搜索的书籍详情列表
        if data['payload']['items']:
            # 搜索符合条件的第一个实际详情页
            details_url = None
            for item in data['payload']['items']:
                s = re.match(r".*subject.*", item['url'])
                if s:
                    details_url = item['url']
                    break
            if details_url:
                logging.info('成功解密<<{0}>>详情页URL:{1}'.format(name, details_url))
                return details_url
            else:
                logging.info('豆瓣没有<<{0}>>书籍详情列表'.format(name))
                return None
        else:
            logging.info('豆瓣没有<<{0}>>书籍详情列表'.format(name))
            return None
    except Exception as e:
        logging.error('解密<<{0}>>搜索详情列表出错:{1}'.format(name, e))
        return None


def decrypt_js():
    global DECRYPT_JS
    if DECRYPT_JS is None:
        with open(os.path.join(os.path.abspath('.'), 'main.js'), 'r') as f:
            DECRYPT_JS = f.read().decode('utf-8')
    return DECRYPT_JS


def search_db_book():
    # logging.info("开启新的进程{0}处理豆瓣图书搜索, ".format(os.name))
    # 开启新线程处理豆瓣图书搜索页
    process_req_thread = threading.Thread(target=process_req_queue, name='Thread-req_queue',
                                          args=(DOU_BAN_SUBJECT_SEARCH_URL, req_queue,
                                                req_details_queue, bad_queue))
    process_req_thread1 = threading.Thread(target=process_req_queue, name='Thread-req_queue',
                                           args=(DOU_BAN_SUBJECT_SEARCH_URL, req_queue,
                                                 req_details_queue, bad_queue))
    process_req_thread2 = threading.Thread(target=process_req_queue, name='Thread-req_queue',
                                           args=(DOU_BAN_SUBJECT_SEARCH_URL, req_queue,
                                                 req_details_queue, bad_queue))
    process_req_thread.start()
    process_req_thread1.start()
    process_req_thread2.start()
    time.sleep(10)
    process_req_details_thread = threading.Thread(target=process_req_details_queue, name='Thread-req_details_queue',
                                                  args=(req_details_queue, bad_details_queue))
    process_req_details_thread.start()

    process_req_details_thread.join()
    # 处理失败的队列
    process_req_bad_thread = threading.Thread(target=process_req_queue, name='Thread-req_bad_queue',
                                              args=(DOU_BAN_SUBJECT_SEARCH_URL, bad_queue,
                                                    req_details_queue,))
    process_req_bad_thread.start()
    time.sleep(5)
    process_req_details_bad_thread = threading.Thread(target=process_req_details_queue,
                                                      name='Thread-req_details_bad_queue',
                                                      args=(bad_details_queue,))
    process_req_details_bad_thread.start()

    process_req_details_bad_thread.join()
    logging.info("成功处理{0}本书".format(SUCCESS_COUNT))


def process_db_process():
    # 处理数据库书籍进程
    get_req_queue()
    if req_queue.qsize() > 0:
        logging.info("数据库有{0}本书籍需要处理".format(req_queue.qsize()))
        # request_pro = Process(target=search_db_book, args=('request_pro_process',))
        # request_pro.start()
        search_db_book()
    else:
        logging.info("数据库暂无需要处理的书籍")


def insert_category_db(category):
    try:
        cnn = mysql.connector.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            passwd=Config.DB_PWD,
            db=Config.DB_NAME,
            charset=Config.DB_CHARSET)
        cur = cnn.cursor()
        cur.execute('SELECT * FROM CATEGORY WHERE name LIKE "%{0}%"'.format(category))
        result = cur.fetchall()
        if result:
            return True
        else:
            create_time = update_time = str(long(time.mktime(datetime.now().timetuple())))
            cur.execute('INSERT INTO CATEGORY(name, create_time, update_time) VALUES (%s, %s, %s)',
                        params={category, create_time, update_time})
            return True
    except Exception as e:
        logging.error("操作数据库目录<{0}>出错:{1}".format(category, e))
        return None
    return None


def get_file_category(path):
    # 切换路径
    os.chdir(path)
    for category in os.listdir(path):
        # category
        if os.path.isdir(category):
            logging.info("目录<0>".format(category))
            # result = insert_category_db(category)
            # if result:
            #     yield category
            yield category


def get_file_list(category, category_id , book_list):
    os.chdir(category)
    for x in os.listdir(category):
        if os.path.isdir(x):
            get_file_list(x, book_list)
        elif os.path.isfile(x):
            print("file:{0}, ext name:{1}".format(x, os.path.splitext(x)[1]))
            book_list.append(Book(name=os.path.splitext(x)[1], category= category, category_ids = category_id, ))



def get_req_queue_by_local_files():
    try:
        L = []
        categories = get_file_category("D:\\jtyd\\书籍整理")
        category = categories.next()
        get_file_category(category, L)
    except Exception as e:
        pass

    pass


def process_file_process():
    # 处理文件书籍进程
    pass


if __name__ == '__main__':
    freeze_support()
    # process_db_process()
    pass
