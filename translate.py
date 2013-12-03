#!/usr/bin/python
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <terry.yinzhe@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return to Terry Yin.
#
# The idea of this is borrowed from <mort.yao@gmail.com>'s brilliant work
# https://github.com/soimort/google-translate-cli
# He uses "THE BEER-WARE LICENSE". That's why I use it too. So you can buy him a
# beer too.
# ----------------------------------------------------------------------------
#
# Code updated to fit the purposes of our chatroom.
# Updates made by Tim Jassmann, David Kale, and Sina Tashakkori.
'''
This is a simple, yet powerful command line translator with google translate
behind it. You can also use it as a Python module in your code.
'''
import re
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

class Translator:
    string_pattern = r"\"(([^\"\\]|\\.)*)\""
    match_string =re.compile(
                        r"\,?\["
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern
                        +r"\]")

    def translate(self, source, fromlang, tolang):
        self.from_lang = fromlang
        self.to_lang = tolang
        json5 = self._get_json5_from_google(source)
        return self._unescape(self._get_translation_from_json5(json5))

    def _get_translation_from_json5(self, content):
        result = ""
        pos = 2
        while True:
            m = self.match_string.match(content, pos)
            if not m:
                break
            result += m.group(1)
            pos = m.end()
        return result

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        req = request.Request(
             url="http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8"
                 +"&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
                 , headers = headers)
        r = request.urlopen(req)
        return r.read().decode('utf-8')

    def _unescape(self, text):
        return re.sub(r"\\.?", lambda x:eval('"%s"'%x.group(0)), text)
