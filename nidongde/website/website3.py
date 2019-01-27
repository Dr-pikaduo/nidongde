#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re

import utils
import base
import website


class web_novel(metaclass=website.WebsiteLike):

    home = "http://www.t077ee.com"
    styles = {'少妇小说':26, '人妻小说':27, '校园小说':31}

    novel_title_rx = re.compile(r'【?(?P<title>\w+)】?(（续）)?(?P<chapter>\d{1,2}-\d{1,2})?(【?作者：(?P<author>\w+)】?)?')

    @classmethod
    def get_page(cls, style='少妇小说'):
        URL = cls.style2url(style)
        soup = base.url2soup(URL)

        main = soup.find('div', {'class': 'main'})
        url = main.find_all('tbody').a['href']

        p = soup.find('div', {'class': 'page'}).span
        pages = int(base.page_rx.search(p.text)[1])
        return pages, 0

    @classmethod
    def index2url(cls, index):
        return cls.home + "/html/article/index%d.html" % index

    @classmethod
    def style2url(cls, style, page=1):
        if page ==1:
            return cls.home + "/html/part/index%d.html" % (cls.styles[style])
        else:
            return cls.home + "/html/part/index%d_%d.html" % (cls.styles[style], index)


    @classmethod
    def search_in_page(keyword, URL, cls=None):
        soup = utils.url2soup(URL)

        for t in soup.find('div', {'class':'main'}).find_all('tbody'):
            t = t.a
            if t and keyword in t.text:
                m = cls.novel_title_rx.match(t.text)
                date = t.font.text
                chapter = m['chapter'] or 0
                if cls:
                    yield cls(title=m['title'], chapter=chapter, index=int(utils.digit_rx.search(t['href'])[0]), date=date)
                else:
                    yield {'title': m['title'], 'chapter':chapter, 'index':int(utils.digit_rx.search(t['href'])[0]), 'date':date}


    @classmethod
    def get_novel(cls, URL, klass=None):
        soup = utils.url2soup(URL)
        main = soup.find('div', {'class':'main'})
        title = main.find('div', {'class':'title'})
        m = cls.novel_title_rx.match(title.text)
        chapter = int(m['chapter']) if m['chapter'] else 0
        body = main.find('div', {'class':'n_bd'}).text
        if klass:
            return klass(title=m['title'], chapter=chapter, body=body, author=m['author'])
        else:
            return {'title': m['title'], 'chapter': chapter, 'body': body, 'author':m['author']}

