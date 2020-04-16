# -*- coding: utf-8 -*-
from xml.parsers.expat import ParserCreate

xml_content = r'''<?xml version="1.0"?>
<ol>
    <li><a href="/python">Python</a></li>
    <li><a href="/ruby">Ruby</a></li>
</ol>
'''


class DefaultSaxHandler(object):
    def start_element(self, name, attrs):
        print('Start element:', name, attrs)

    def char_data(self, data):
        print('Character data:', repr(data))

    def end_element(self, name):
        print('End element:', name)


xmlparser = ParserCreate()
saxhandler = DefaultSaxHandler()
xmlparser.StartElementHandler = saxhandler.start_element
xmlparser.CharacterDataHandler = saxhandler.char_data
xmlparser.EndElementHandler = saxhandler.end_element
xmlparser.Parse(xml_content)

L = []
L.append(r'<?xml version="1.0"?>')
L.append(r'<root>')
L.append('some & data')
L.append(r'</root>')
xml_content1 = ''.join(str(L))
print(xml_content1)
