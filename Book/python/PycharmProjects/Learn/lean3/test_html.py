# -*- coding: utf-8 -*-
import re
from urllib import request
from html.parser import HTMLParser
from html.entities import name2codepoint


# class MyHTMLParser(HTMLParser):
#     def __init__(self, *, convert_charrefs=True):
#         super().__init__(convert_charrefs=convert_charrefs)
#
#     def handle_starttag(self, tag, attrs):
#         super().handle_starttag(tag, attrs)
#         print("handle_starttag tag:%s,attrs:%s" % (tag, attrs))
#
#     def handle_endtag(self, tag):
#         super().handle_endtag(tag)
#         print("handle_endtag tag:%s" % tag)
#
#     def handle_charref(self, name):
#         super().handle_charref(name)
#         print("handle_charref name:%s" % name)
#
#     def handle_entityref(self, name):
#         super().handle_entityref(name)
#         print("handle_entityref name:%s" % name)
#
#     def handle_data(self, data):
#         super().handle_data(data)
#         print("handle_data data:%s" % data)
#
#     def handle_comment(self, data):
#         super().handle_comment(data)
#         print("handle_comment data:%s" % data)
#
#
# html_parser = MyHTMLParser()
# # html_parser.feed('<html><head><title>Test</title></head>'
# #             '<body><h1>Parse me!</h1></body></html>')
# html_parser.feed('''<html>
# <head></head>
# <body>
# <!-- test html parser -->
#     <p>Some <a href=\"#\">html</a> HTML&nbsp;tutorial...<br>END</p>
# </body></html>''')

# class Event(object):
#
#     def __init__(self, title, location, time) -> None:
#         super().__init__()
#         self.__title = title
#         self.__location = location
#         self.__time = time
#
#     def __str__(self) -> str:
#         return "(title:%s, location:%s, time:%s)" % (self.__title, self.__location, self.__time)
#
#     __repr__ = __str__


class MHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.__tag = ''

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if ('class', 'event-title') in attrs:
            self.__tag = 'title'
        if tag == 'time':
            self.__tag = 'time'
        if ('class', 'say-no-more') in attrs:
            self.__tag = 'year'
        if ('class', 'event-location') in attrs:
            self.__tag = 'location'

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        self.__tag = ''

    def handle_data(self, data):
        super().handle_data(data)
        if self.__tag == 'title':
            print('title :%s' % data)
        if self.__tag == 'time':
            print('time :%s' % data)
        if self.__tag == 'year':
            if re.match(r'\s\d{4}', data):
                print('year :%s' % data)
        if self.__tag == 'location':
            print('location :%s' % data)
            print('----------------------------------')

    def handle_comment(self, data):
        super().handle_comment(data)


URL = 'https://www.python.org/events/python-events/'

parser = MHTMLParser()
with request.urlopen(URL, timeout=10) as f:
    data = f.read().decode('utf-8')
    parser.feed(data)
