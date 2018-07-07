#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base

default_style = '人妻'

def search(keyword, style=None, pages=100):
    if style:
        for page in range(pages):
            URL = "http://www.417mm.com/list/index%d_%d.html" % (base.STYLES[style], page)
            soup = base.url2soup(URL)

            for div in soup.find_all('div', {'class':'con'}):
                a = div.find('a', {'class':'txt'})
                if keyword in a.text:
                    yield (int(base.extract(base.digit_rx, a.get('href'))), a.text)
    else:
        for style in base.STYLES:
            yield search(keyword, style)

for a in search('淫', style=default_style):
    print(a)