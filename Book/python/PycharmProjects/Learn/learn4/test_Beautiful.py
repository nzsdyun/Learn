# -*- coding: utf-8 -*-
import json
import os
# import requests

# headers = {
#     'User-Agent': 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25'
# }
# rq = requests.get('https://book.douban.com/subject_search', headers=headers, params={'search_text': '大秦帝国'})
# print("request:", rq.url)
# with open(os.path.join(os.path.abspath("."), 'douban.html'), mode='w', encoding='utf-8') as fq:
#     fq.write(rq.text)
import re
from datetime import datetime, time

import execjs
import requests
from bs4 import BeautifulSoup, CData
from idna import unicode

html_content = None

with open(os.path.join(os.path.abspath("."), 'douban.html'), mode='r', encoding='utf-8') as fq:
    html_content = str(fq.read())

bsp = BeautifulSoup(html_content, features="html.parser")
# example 1
# 格式化输出
print(bsp.prettify())
# title标签
print(bsp.title)
# title标签名字
print(bsp.title.name)
# title标签的父标签
print(bsp.title.parent)
# p标签
print(bsp.p)
# p标签class属性值
print(bsp.p['class'])
# 查找所有a标签
print(bsp.find_all('a'))
# 查找一条link标签
print(bsp.find('link'))

# example 2
for link in bsp.find_all('a'):
    print(link.get('href'))
# 获取文档中的所有文字内容
print(bsp.get_text)

# example 3
# tag 标签
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', features="html.parser")
print(soup.b)
print(type(soup.b))
# name, attrs属性
print(soup.b.name)
print(soup.b.attrs)
print(soup.b['class'])
# 属性可以添加，删除，修改跟dict操作一样
soup.b['class'] = 'verybold'
soup.b['id'] = 1
print(soup.b)
del soup.b['class']
del soup.b['id']
print(soup.b)
# print(soup.b['class']) # KeyError: 'class'
print(soup.b.get('class'))  # None
# 多值属性
css_soup = BeautifulSoup('<p class="body strikeout"></p>', features="html.parser")
# 返回list集合
print(css_soup.p['class'])
# 某个属性在任何版本的HTML定义中没有被定义, 返回字符串
id_soup = BeautifulSoup('<p id="my id"></p>', features="html.parser")
print(id_soup.p['id'])
# 将tag转换成字符串时,多值属性会合并为一个值
rel_soup = BeautifulSoup('<p>Back to the <a rel="index">homepage</a></p>', features="html.parser")
print(rel_soup.a['rel'])
rel_soup.a['rel'] = ['index', 'contents']
print(rel_soup)
# # 如果转换的文档是XML格式,那么tag中不包含多值属性
# xml_soup = BeautifulSoup('<p class="body strikeout"></p>', 'xml')
# xml_soup.p['class']

# example 4
# NavigableString, tag标签内的内容
soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', features="html.parser")
tag = soup.b
print(tag.string)
print(type(tag.string))
# NavigableString 同python的Unicode字符串相同，可以通过unicode转化成Unicode字符串
unicode_string = unicode(tag.string)
print(unicode_string)
print(type(unicode_string))
# NavigableString不能编辑，但可以替换成其他字符串
tag.string.replace_with("No longer bold")
print(tag)
# BeautifulSoup对象表示文档的全部内容
print(soup.name)
# Comment注释, Comment 对象是一个特殊类型的 NavigableString 对象:
markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup, features="html.parser")
comment = soup.b.string
print(comment)
print(type(comment))
# 其他 CData , ProcessingInstruction , Declaration , Doctype
cdata = CData("A CDATA block")
comment.replace_with(cdata)
print(soup.b.prettify())

# example 5
# 遍历
html_doc = """
<html><head><title>The Dormouse's story</title></head>

<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""
soup = BeautifulSoup(html_doc, features="html.parser")
# tag
print(soup.head)
print(soup.title)
print(soup.p.b)
# 第一个搜索的tag
print(soup.a)
print(soup.find_all('a'))
# .contents 和 .children
# .contents属性可以将tag以列表的形式输出
head_tag = soup.head
print(head_tag.contents)
title_tag = head_tag.contents[0]
print(title_tag)
print(title_tag.contents)
print(len(soup.contents))
print(soup.contents[1].name)
# 通过tag的 .children 生成器,可以对tag的子节点进行循环:
for child in soup.html.children:
    print(child)
# .contents和.children属性仅包含tag的直接子节点
# .descendants属性可以对tag的所有子孙节点进行递归循环
print(head_tag.contents)
for child in head_tag.descendants:
    print(child)
print(len(list(soup.children)))
print(len(list(soup.descendants)))
# .string取只要一个子节点的内容
print(title_tag.string)
# 如果tag包含了多个子节点,tag就无法确定 .string 方法应该调用哪个子节点的内容, .string 的输出结果是 None :
print(soup.html.string)
# .stripped_strings循环获取含有多个字符串的内容
for string in soup.strings:
    print(repr(string))
# .parent获取某个元素的父节点
title_tag = soup.title
print(title_tag)
print(title_tag.parent)
# .parents递归获取元素的所有父辈节点
link = soup.a
print(link)
for parent in link.parents:
    if parent is None:
        print(parent)
    else:
        print(parent.name)
# .next_sibling 和 .previous_sibling获取元素的兄弟节点
sibling_soup = BeautifulSoup("<a><b>text1</b><c>text2</c></b></a>", features="html.parser")
print(sibling_soup.prettify())
print(sibling_soup.b.next_sibling)
print(sibling_soup.b.previous_sibling)
# .next_siblings 和 .previous_siblings迭代获取元素的兄弟节点
for sibling in soup.a.next_siblings:
    print(repr(sibling))
# .next_element 和 .previous_element
# next_element 属性指向解析过程中下一个被解析的对象(字符串或tag),结果可能与 .next_sibling 相同,但通常是不一样的.
last_a_tag = soup.find("a", id="link3")
print(last_a_tag)
print(last_a_tag.next_sibling)
print(last_a_tag.next_element)

# example 6
# 搜索文档树
# find_all，可以是字符串，正则表达式， 列表， True, 方法
# find_all(self, name=None, attrs={}, recursive=True, text=None, limit=None, **kwargs)
# name:tag
# attrs: attrs
# recursive: 调用tag的 find_all() 方法时,Beautiful Soup会检索当前tag的所有子孙节点,如果只想搜索tag的直接子节点,可以使用参数 recursive=False
# text: 通过 text 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样, text 参数接受 字符串 , 正则表达式 , 列表, True
# limit: limit 参数限制返回结果的数量.
# **kwargs: 如果一个指定名字的参数不是搜索内置的参数名,搜索时会把该参数当作指定名字tag的属性来搜索,如果包含一个名字为 id 的参数,Beautiful Soup会搜索每个tag的”id”属性.
# 搜索指定名字的属性时可以使用的参数值包括 字符串 , 正则表达式 , 列表, True .
# 字符串
print(soup.find_all('b'))
# 正则表达式
for tag in soup.find_all(re.compile("^b")):
    print(tag.name)
# 列表，满足其一即可
print(soup.find_all(["a", "b"]))
# 匹配任何值
for tag in soup.find_all(True):
    print(tag.name)


# 根据方法返回值确定
def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


print(soup.find_all(has_class_but_no_id))
# find( name , attrs , recursive , text , **kwargs)返回一个结果
# find_parents() 和 find_parent() 搜索当前tag的父辈tag
# find_parents( name , attrs , recursive , text , **kwargs )
# find_parent( name , attrs , recursive , text , **kwargs )
# find_next_siblings() 合 find_next_sibling() 搜索当前tag的后面的兄弟tag
# find_previous_siblings() 和 find_previous_sibling() 搜索当前tag的前面的兄弟tag
# find_all_next() 和 find_next() 对当前tag的之后的 [5] tag和字符串进行迭代, find_all_next() 方法返回所有符合条件的节点, find_next() 方法返回第一个符合条件的节点:
# find_all_previous() 和 find_previous() 对当前节点前面 [5] 的tag和字符串进行迭代, find_all_previous() 方法返回所有符合条件的节点, find_previous() 方法返回第一个符合条件的节点.


# example 7 CSS选择器
print(soup.select("title"))
# print(soup.select("p nth-of-type(3)"))
# 通过tag标签逐层查找:
print(soup.select("p a"))
print(soup.select('html head title'))
# 找到某个tag标签下的直接子标签
print(soup.select("head > title"))
print(soup.select("p > a"))
print(soup.select("p > a:nth-of-type(2)"))
print(soup.select("p > #link1"))
print(soup.select("body > a"))
# 找到兄弟节点标签
print(soup.select("#link1 ~ .sister"))
print(soup.select("#link1 + .sister"))
# 通过CSS的类名查找:
print(soup.select(".sister"))
print(soup.select("[class~=sister]"))
# 通过tag的id查找:
print(soup.select("#link1"))
print(soup.select("a#link2"))
# 通过是否存在某个属性来查找:
print(soup.select('a[href]'))
# 通过属性的值来查找:
print(soup.select('a[href="http://example.com/elsie"]'))
print(soup.select('a[href^="http://example.com/"]'))
print(soup.select('a[href$="tillie"]'))
# 通过语言设置来查找:
multilingual_markup = """
 <p lang="en">Hello</p>
 <p lang="en-us">Howdy, y'all</p>
 <p lang="en-gb">Pip-pip, old fruit</p>
 <p lang="fr">Bonjour mes amis</p>
"""
multilingual_soup = BeautifulSoup(multilingual_markup, features="html.parser")
print(multilingual_soup.select('p[lang|=en]'))


# # test
# r = re.search('window.__DATA__ = "([^"]+)"', html_content).group(1)
# print(r)
# with open(os.path.join(os.path.abspath('.'), 'main.js'), 'r', encoding='gbk') as f:
#     decrypt_js = f.read()
# print(decrypt_js)
# ctx = execjs.compile(decrypt_js)
# data = ctx.call('decrypt', r)
# for item in data['payload']['items']:
#     print(item)


response = requests.get('https://book.douban.com/subject_search?search_text=%E9%80%89%E8%82%A1%E5%85%B6%E5%AE%9E%E5%BE%88%E7%AE%80%E5%8D%95-%E4%B8%BB%E4%BD%93%E6%80%9D%E7%BB%B4%E9%80%89%E8%82%A1%E6%B3%95+%28%E7%BB%99%E6%95%A3%E6%88%B7%E6%94%AF%E6%8B%9B%E7%B3%BB%E5%88%97%29&cat=1001')
txt = response.text
print(txt)
# with open(os.path.join(os.path.abspath("."), 'douban.html'), mode='r', encoding='utf-8') as fq:
#     txt = fq.read()
r = re.search('window.__DATA__ = "([^"]+)"', txt).group(1)  # 加密的数据
print("rrrrr", r)
# # 导入js
with open(os.path.join(os.path.abspath('.'), 'main.js'), 'r', encoding='gbk') as f:
    decrypt_js = f.read()
ctx = execjs.compile(decrypt_js)
data = ctx.call('decrypt', r)
for item in data['payload']['items']:
    s = re.match(r".*subject.*", item['url'])
    if s:
        print("aaaaaaaaaaaaaa", item['url'], type(s))
#
#
# js = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
# print("aaaa", js)
# for item in data['payload']['items']:
#     print(item)

# rq = requests.get('https://book.douban.com/subject/3079029/')
# with open(os.path.join(os.path.abspath("."), 'douban_details.html'), mode='w', encoding='utf-8') as fq:
#     fq.write(rq.text)
# rq = requests.get('https://book.douban.com/subject/26662573/')
# with open(os.path.join(os.path.abspath("."), 'douban_details_null.html'), mode='w', encoding='utf-8') as fq:
#     fq.write(rq.text)
# html_content = None

# with open(os.path.join(os.path.abspath("."), 'douban_details_null.html'), mode='r', encoding='utf-8') as fq:
#     html_content = str(fq.read())
# bsp = BeautifulSoup(html_content, features="html.parser")
# print("title:", bsp.select('#wrapper > h1'))
# print("author:", bsp.select('#info > a'))
# print("cover:", bsp.select('#mainpic > a > img'))
# print("press:", bsp.select('#info > span:nth-child(3)'))
# print("content:", bsp.select('#link-report > span.short > div'))
# title = bsp.select('#wrapper > h1 > span')[0].string if bsp.select('#wrapper > h1 > span')[0] else ""
# author = bsp.select('#info > a')[0].string.strip() if bsp.select('#info > a') else ""
# cover = bsp.select('#mainpic > a > img')[0]['src'] if bsp.select('#mainpic > a > img') else ""
# press = bsp.select('#info > span:nth-child(3)')[0].next_sibling if bsp.select('#info > span:nth-child(3)') else bsp.select('#info > span:nth-child(4)')[0].next_sibling if bsp.select('#info > span:nth-child(4)') else ""
# content = ''
# if bsp.select('#link-report > span.short > div'):
#     for pc in bsp.select('#link-report > span.short > div')[0].find_all('p')[:-1]:
#         content += '\n\t' + pc.string + '\n'
# print("title:", title)
# print("author:", author)
# print("cover:", cover)
# print("press:", press)
# print("content:", content)
# cover = bsp.select('#mainpic > a > img')[0]['src']
# with open(
#         os.path.join("D:\\douban_image", bsp.select('#wrapper > h1 > span')[0].string + "_" + str(datetime.now().timestamp()) + ".jpg"),
#         mode='wb') as fq:
#     cq = requests.get(cover)
#     fq.write(cq.content)
#     print("保存封面成功")

# spi = "https://img3.doubanio.com/view/subject/l/public/s27508060.jpg"
# t = spi[spi.rindex("."):]
# print(t)
# print("content:", bsp.select('#link-report > span.short > div')[0].find_all('p')[:-1])

def parse_details_content(content, name):
    try:
        print("开始解析<<{0}>>书籍详情页".format(name))
        bsp = BeautifulSoup(content, features="html.parser")
        # title
        # name = bsp.select('#wrapper > h1 > span')[0].string
        # author = bsp.select('#info > a')[0].string.strip()
        # cover = bsp.select('#mainpic > a > img')[0]['src']
        # press = unicode(bsp.select('#info > span:nth-child(4)')[0].next_sibling)
        # intro = ''
        # for pc in bsp.select('#link-report > span.short > div')[0].find_all('p')[:-1]:
        #     intro += '\n\t' + pc.string + '\n'
        # name = bsp.select('#wrapper > h1 > span')[0].string if \
        #     bsp.select('#wrapper > h1 > span')[
        #         0] else ""
        # author = bsp.select('#info > a')[0].string.strip() if bsp.select('#info > a') else ""
        # cover = bsp.select('#mainpic > a > img')[0]['src'] if bsp.select(
        #     '#mainpic > a > img') else ""
        # press = bsp.select('#info > span:nth-child(3)')[0].next_sibling if bsp.select(
        #     '#info > span:nth-child(3)') else bsp.select('#info > span:nth-child(4)')[
        #     0].next_sibling if bsp.select('#info > span:nth-child(4)') else ""
        # if bsp.select('#link-report > div:nth-child(1) > div'):
        #     for pc in bsp.select('#link-report > div:nth-child(1) > div')[0].find_all('p')[:-1]:
        #         intro += '\n\t' + pc.string + '\n'
        # elif #link-report > div:nth-child(1) > div
        # print(bsp.select('#wrapper > h1 > span').get_text)
        name = "N/A"
        author = 'N/A'
        press = 'N/A'
        cover = 'N/A'
        intro = 'N/A'
        if bsp.select('#wrapper > h1 > span'):
            name = bsp.select('#wrapper > h1 > span')[0].string
        elif bsp.find('span', property='v:itemreviewed'):
            name = bsp.find('span', property='v:itemreviewed').string
        if bsp.select("#mainpic > a > img"):
            cover = bsp.select("#mainpic > a > img")[0]['src']
        new_intro = ''
        if bsp.select('div.intro'):
            for pc in bsp.select('div.intro')[0].find_all('p'):
                if not re.match(r'.*[(|（]*展开全部[)|）]*.*', pc.string):
                    new_intro += '\n\t' + pc.string + '\n'
        intro = new_intro if new_intro else intro
        update_time = str(datetime.now().timestamp())
        print(
            "({0},{1},{2},{3},{4},{5})".format(name, author, cover, press, intro, update_time))
        # with open(
        #         os.path.join("D:\\douban_image", name + "_" + update_time + cover[cover.rindex("."):]),
        #         mode='wb') as fq:
        #     cq = requests.get(cover)
        #     fq.write(cq.content)
        #     print("保存<<{0}>>图书封面成功!!!".format(name))
        return {"name": name, "author": author, "cover": cover, "press": unicode(press), "intro": intro,
                "update_time": update_time}
        # process_upload_db(details_item)
    except Exception as e:
        print("解析书籍<<{0}>>详情出错:{1}".format(name, e))
        return None
    return None


html_content = None

# 'douban_details.html'
# 26292964_details.html
with open(os.path.join(os.path.abspath("."), 'ASA.html'), mode='r', encoding='utf-8') as fq:
    html_content = str(fq.read())

parse_details_content(html_content, "世界小史")


# sss = '''
#
# 	《做单:成交的秘密(再版)》内容简介：谢正是世界顶级企业IBM的金牌销售，已连续多年单单不败。殊不知，突如其来的IBM和远想的世纪大并购却在他升职的最关键时期发生，这使他不得不跳到最新成立的部门，一切重头开始……IBM特别成立win back 团队，要夺回被对手普惠占领多年的客户——中国移通。他被安排负责三个最重要省份之一湖南，但是那里是普惠的大本营。当谢正第一次上门拜访时，客户毫不留情地让他“滚”出去……移通总部在价格谈判中请来了“谈判之神”王芸生，将谢正等人折腾得死去活来……准备最后拍板时，人敬人畏的IBM大中华总经理詹姆斯到了现场。王芸山出人意料地将MBI报价扔到门外，并宣称要废掉他们的投标资格，这下几乎让所有人崩溃……是放弃？还是生死一搏？顶级高层经理的如何腾挪资源，锁定客户的真实需求，拿下不可能拿下的单？顶着越演越烈的政治斗争，金牌销售是否...
#
# 	(展开全部)
#
# '''
# sss1 = '''
#
# 	通史的意境，全在通古今之变，历史由此才显示出它的节律脉动，是一个活泼泼跳动着的“集体生命体”，有它特殊的生命历程和内在的新陈代谢机制。本书以勾勒轮廓、阐释整体特征为限，又包含着对百年来“传统”向“现代”转型的“中国情结”的特殊关注。在统合百家的基础上，从通贯和整体全是的角度，对历史中的重大问题做出个性化的解读，进而揭示中国历史变迁的内在脉络。
#
# 	本《通论》初版分前篇和后篇两部分。前篇从纵横交错的角度，围绕中国历史发展的基本特征和演进脉络两大主题，通过若干专题，进行研讨。纵向的，对发展线索作讨论；横向的，多围绕中国历史的特点展开。后篇则重在回顾和反思《通史》的百年经历。增订本新加入的“续编”，收进了初版后十年写的一些相关文章，如〈阅读历史：前现代、现代与后现代〉〈明清易代的偶然性与必然性〉〈农业、农民与乡村社会：农耕文明新审视〉等等，大体沿袭原来的风格，...
#
# 	(展开全部)
#
#
# '''
# sss1 = None
# if sss1 and sss1.find('展开全部'):
#     print(sss1.replace('(展开全部)', '').replace('展开全部', '').replace('（展开全部）', ''))


