#!/usr/local/bin/python
# -*- coding: utf-8 -*-


import re
import pickle
import pathlib

import base

rx_title = re.compile(r'【(?P<title>\w+)】（(?P<chapter>\w+)）')
rx_author = re.compile(r'【作者：(?P<author>\w+)】')

class Novel(object):
    """docstring for Novel"""
    def __init__(self, title, chapter, body='', author=''):
        super(Novel, self).__init__()
        self.title = title
        self.chapter = chapter
        self.body = body
        self.author = author

    def __str__(self):
        return '%s (%s)\n%s' % (self.title, self.chapter, self.body)

    def __getstate__(self):
        return self.title, self.chapter, self.body, self.author

    def __setstate__(self, state):
        self.title, self.chapter, self.body, self.author = state

    @staticmethod
    def fromIndex(index):

        URL = "http://www.bxmyly.com/html/article/index%d.html" % index

        soup = base.url2soup(URL)

        m = soup.find('div', {'class':'main'})
        title = m.find('div', {'class':'title'}).text
        m_title = rx_title.search(title)
        m_author = rx_author.search(title)
        title, chapter = m_title['title'], m_title['chapter']
        author = m_author['author']

        body = m.find('div', {'class':'content'}).text
        return Novel(title, chapter, body.strip(), author)

    @staticmethod
    def load(index, folder='ANs'):

        if isinstance(folder, str):
            folder = pathlib.Path(folder).expanduser()
        if not folder.exists():
            folder.mkdir(parents=True)
        path = folder / ('novel%d.txt' % index)

        if path.exists():
            raise Warning('%s exists already.' % path)
        else:
            obj = Novel.fromIndex(index)
            path.write_text(str(obj), encoding='utf-8')
        return obj


n = Novel.load(index=27626)
print(n)