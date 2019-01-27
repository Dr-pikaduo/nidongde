#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

import website


class web_t077ee(metaclass=website.WebsiteLike):

    home = "http://www.t077ee.com"
    styles = ['亚洲风情', '日韩经典', '国内自拍', '欧美激情', '中文字幕', '强奸乱伦', '制服诱惑', '巨乳专区']

    movie_title_rx = re.compile(r'((?P<chapter>\d{1,2})-)?(?P<title>.+)')

    @classmethod
    def get_page(cls, style='亚洲风情'):
        URL = cls.style2url(style)
        soup = base.url2soup(URL)

        cl = soup.find('div', {'class': 'channellist box mb bg'})
        indexes =[int(base.digit_rx.search(li.a['href'])[0]) for li in cl.find_all('li')]

        p = soup.find('div', {'class': 'page'})
        pages = int(base.page_rx.search(p.text)[1])
        return pages, indexes

    @classmethod
    def index2url(cls, index):
        return cls.home + "/video/%d.html?%d-0-0" % (index, index)

    @classmethod
    def style2url(cls, style, page=1):
        if page ==1:
            return cls.home + "/list/index%d.html" % cls.styles.index(style)
        else:
            return cls.home + "/list/index%d_%d.html" % (cls.styles.index(style), index)


    @classmethod
    def search_in_page(cls, keyword, URL, klass=None):
        soup = utils.url2soup(URL)

        for li in soup.find('div', {'class':'channellist'}).find_all('li'):
            t = li.h2.a
            if t and keyword in t.text:
                m = klass.movie_title_rx.match(t.text)
                chapter = int(m['chapter']) if m['chapter'] else 0
                if klass:
                    yield klass(title=m['title'], chapter=chapter, index=int(utils.digit_rx.search(t['href'])[0]))
                else:
                    yield {'title': m['title'], 'chapter':chapter, 'index':int(utils.digit_rx.search(t['href'])[0])}


    @classmethod
    def get_movie(cls, URL, klass=None):
        soup = utils.url2soup(URL)
        title = soup.find('h2', {'class':'m_T2'})
        m = cls.movie_title_rx.match(title.text)
        chapter = int(m['chapter']) if m['chapter'] else 0
        for s in soup.find_all('script', {"type": "text/javascript"}):
            if 'video' in s.text:
                mp4 = utils.mp4_rx.search(s.text)[0]
                if klass:
                    return klass(title=m['title'], chapter=chapter, data=mp4)
                else:
                    return {'title': m['title'], 'chapter': chapter, 'data': mp4}