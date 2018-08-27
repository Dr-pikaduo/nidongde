#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base

default_style = '人妻'

def search(keyword, style=None, pages=200):
    if isinstance(style, str):
        for page in range(pages):
            URL = "http://www.417mm.com/list/index%d_%d.html" % (base.STYLES[style], page)
            soup = base.url2soup(URL)

            for div in soup.find_all('div', {'class':'con'}):
                a = div.find('a', {'class':'txt'})
                if a and keyword in a.text:
                    yield (int(base.extract(base.digit_rx, a.get('href'))), a.text)
    elif isinstance(style, (tuple, list)):
        for sty in style:
            for a in search(keyword, sty, pages):
                yield a
    else:
        for style in base.STYLES:
            for a in search(keyword, style, pages):
                yield a


if __name__ == '__main__':
    for a in search('獄', style='乱伦'):
        print(a)