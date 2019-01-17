#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
load videos from adult website such as www.417mm.com
If you want to load movies or other types of data from other websites,
then you should override the methods: fromURL, _search
"""

import pathlib
import re

import base, utils, website

default_website = website.web417

defaultAVFolder = '~/Folders/生活/成人相关/AVs'

title_rx = re.compile(r'((?P<chapter>\d{1,2})-)?(?P<title>.+)')

class Movie(base.LoadItem):
    website = default_website
    chapter = None
    folder = pathlib.Path(defaultAVFolder).expanduser()

    def __str__(self):
        if self.chapter:
            return '%s(%d) # %d' % (self.title, self.chapter, self.index)
        else:
            return '%s # %d' % (self.title, self.index)

    def __format__(self, spec=None):
        if spec in {'mask', 'm'}:
            return '*' * len(self.title) + '(%d) # %d' % (self.chapter, self.index)
        elif '.' in spec:
            return '%s(%d) # %d' % (utils.random_mask(self.title, float(spec)), self.chapter, self.index)
        elif spec.isdigit():
            return '%s(%d) # %d' % (utils.caesar(self.title, int(spec)), self.chapter, self.index)
        else:
            return '%s(%d) # %d' % (self.title, self.chapter, self.index)

    def save(self, folder=None):
        filename = 'av%d.mp4' % self.index
        super(Movie, self).save(folder, filename)

    @classmethod
    def fromURL(cls, URL):
        """find movie in url, url -> movie
        
        Arguments:
            URL {str}
        
        Returns:
            Movie
        """
        soup = utils.url2soup(URL)
        title = soup.find('h2', {'class':'m_T2'})
        m = title_rx.match(title.text)
        chapter = int(m['chapter']) if m['chapter'] else 0
        for s in soup.find_all('script', {"type": "text/javascript"}):
            if 'video' in s.text:
                mp4 = utils.mp4_rx.search(s.text)[0]
                return Movie(title=m['title'], chapter=chapter, data=mp4)

    @staticmethod
    def _search(keyword, style, page=1):
        """Search movies in one page
        
        Arguments:
            keyword {str} -- keyword for searching movies
            style {str} -- the style of movies that you search
            page {int} -- in which page you search them
        
        Yields:
            Movie
        """
        URL = Movie.website.style2url(style, page)
        soup = utils.url2soup(URL)

        for div in soup.find_all('div', {'class':'con'}):
            t = div.find('a', {'class':'txt'})
            if t and keyword in t.text:
                m = title_rx.match(t.text)
                chapter = int(m['chapter']) if m['chapter'] else 0
                yield Movie(title=m['title'], chapter=chapter, index=int(utils.digit_rx.search(t['href'])[0]))


if __name__ == '__main__':

    # clever_load('日韩', lb=1, ub=7)
    # for m in Movie.search('教'):
    #     print(m)
    Movie.load([(32198, 32199), ], verbose=True, folder=defaultAVFolder)
    # Movie.load(31529)
