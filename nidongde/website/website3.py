#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import pyparsing as pp

import utils
import base
import website

class TitleAction:
    def __init__(self, tokens):
        self.tokens = tokens
        for key in ('chapter', 'option', 'author'):
            if key not in tokens:
                self.tokens[key] = ''

    def __getitem__(self, key):
        return self.tokens[key]


class web_novel(metaclass=website.WebsiteLike):

    home = "http://www.t077ee.com"
    styles = {'少妇小说':26, '人妻小说':27, '校园小说':31}

    # example '【分裂人妻之刘恋】（番外）（1）【作者：人后龌龊】'

    title = pp.QuotedString('【', endQuoteChar='】') | pp.Word(pp.pyparsing_unicode.Chinese.alphanums + '-+，')
    author = pp.QuotedString('【', endQuoteChar='】').setParseAction(lambda t:t[0].strip('作者：')) | (pp.Suppress('作者：') + pp.Word(pp.pyparsing_unicode.Chinese.alphanums))
    chapter = pp.QuotedString('（', endQuoteChar='）')
    option = pp.QuotedString('（', endQuoteChar='）')
    title_parser = title('title') + pp.Optional(option)('option') + pp.Optional(chapter)('chapter') + pp.Optional(author)('author')
    title_parser.setParseAction(TitleAction)

    @classmethod
    def get_page(cls, style='少妇小说'):
        URL = cls.style2url(style)
        soup = utils.url2soup(URL)

        # main = soup.find('div', {'class': 'main'})
        # url = main.find_all('tbody').a['href']

        p = soup.find('div', {'class': 'page'}).span
        pages = int(utils.page_rx.search(p.text)[1])
        return pages, 0

    @classmethod
    def index2url(cls, index):
        return cls.home + "/html/article/index%d.html" % index

    @classmethod
    def style2url(cls, style, page=1):
        if page ==1:
            return cls.home + "/html/part/index%d.html" % (cls.styles[style])
        else:
            return cls.home + "/html/part/index%d_%d.html" % (cls.styles[style], page)


    @classmethod
    def search_in_page(cls, keyword, URL, klass=None):
        soup = utils.url2soup(URL)
        for t in soup.find('div', {'class':'main'}).find_all('table', {'class':'listt'}):
            if t and keyword in t.text:
                t = t.a
                p = cls.title_parser.parseString(t.text)[0]
                date = t.font.text
                if klass:
                    yield klass(index=int(utils.digit_rx.search(t['href'])[0]), date=date, **p.tokens)
                else:
                    p = dict(p.tokens)
                    p.update({'index':int(utils.digit_rx.search(t['href'])[0]), 'date':date})
                    yield p


    @classmethod
    def get_novel(cls, URL, klass=None):
        soup = utils.url2soup(URL)
        main = soup.find('div', {'class':'main'})
        title = main.find('div', {'class':'title'})
        p = cls.title_parser.parseString(title.text)[0]
        body = main.find('div', {'class':'n_bd'}).text
        if klass:
            return klass(body=body, **p)
        else:
            p= dict(p.tokens)
            p.update({'body': body})
            return p

