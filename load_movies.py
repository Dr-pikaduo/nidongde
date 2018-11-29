#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''load videos from www.417mm.com
'''

import pathlib
import re

import base


HOME = 'http://www.417mm.com/'


def get_page(style):
    """get the number of pages and max index of the movies in certain style
    
    Arguments:
        style {str} -- style of movie, one of the keys in STYLES
    
    Returns:
        tuple -- (number of pages, max index)
    """

    URL = HOME + "/list/index%d.html" % base.STYLES[style]
    soup = base.url2soup(URL)
    s = soup.find_all('div', {'class':'con'})[0]
    index = int(base.digit_rx.search(s.a['href'])[0])
    p = soup.find('div', {'class': 'dede_pages'}).find('span')
    pages = int(base.page_rx.search(p.text)[1])
    return pages, index



def clever_load(style, lb, ub):
    # load movies in some style from lb to ub
    (pages, index) = get_page(style)
    index1 = index - ub + 1
    index2 = index - lb + 1
    for k in range(index1, index2+1):
        Movie.load(k)

def caesar(s, k=8):
    # Caesar cipher
    return ''.join(map(chr, map(lambda x: x+k, map(ord, s))))


default_style = '人妻'

title_rx = re.compile(r'((?P<chapter>\d{1,2})-)?(?P<title>.+)')

def index2url(index):
    return HOME + "/player/index%d.html?%d-0-0" % (index, index)

def style2url(style, page=1):
    return HOME + "list/index%d_%d.html" % (base.STYLES[style], page)

class Movie(base.LoadItem):

    def __init__(self, title, chapter=0, video='', actress='', index=0):
        super(Movie, self).__init__(title)
        self.chapter = chapter
        self.video = video
        self.actress = actress
        self.index = index

    def __str__(self):
        return '%s(%d) # %d' % (self.title, self.chapter, self.index)

    def __format__(self, spec=None):
        if spec == 'mask':
            return '*' * len(self.title) + '(%d) # %d' % (self.chapter, self.index)
        elif spce.isdigit():
            return '%s(%d) # %d' % (caesar(self.title, int(spec)), self.chapter, self.index)
        else:
            return '%s(%d) # %d' % (self.title, self.chapter, self.index)
    
    @staticmethod
    def fromIndex(index):
        URL = index2url(index)
        soup = base.url2soup(URL)
        title = soup.find('h2', {'class':'m_T2'})
        m = title_rx.match(title.text).groupdict()
        chapter = m.get('chapter', 0)

        for s in soup.find_all('script', {"type": "text/javascript"}):
            if 'video' in s.text:
                mp4 = base.mp4_rx.search(s.text)[0]
                break
        return Movie(title=m['title'], chapter=int(chapter), video=mp4, index=index)


    def save(self, folder=base.defaultAVFolder, agent=None):
        html = base.get(self.video).content

        if isinstance(folder, str):
            folder = pathlib.Path(folder).expanduser()
        elif folder is None:
            folder = pathlib.Path(base.defaultAVFolder).expanduser()
        if not folder.exists():
            folder.mkdir(parents=True)
        path = (folder / ('video%d.mp4' % self.index))
        path.write_bytes(html)


    @staticmethod
    @base.generalize
    def load(index, folder=base.defaultAVFolder, verbose=False):
        """Load moives with indexes
        
        Arguments:
            index {int|list[int]|tuple(int, int)} -- index
            folder -- the folder where videos are stored.
            verbose {bool} -- show the info of movie

        Example:
            load([29964, (34533, 24543)])  # load index29964, 34533-24543
        """

        # if isinstance(index, str):
        #     index = base.str2index(index)

        movie = Movie.fromIndex(index)
        if verbose:
            print('Loading', movie)
        movie.save(folder=base.defaultAVFolder)


    @staticmethod
    def search(keyword, style=None, pages=200):
        if isinstance(style, str):
            if pages is None:
                pages = get_page(style)
            for page in range(pages):
                URL = style2url(style, page)
                soup = base.url2soup(URL)

                for div in soup.find_all('div', {'class':'con'}):
                    a = div.find('a', {'class':'txt'})
                    if a and keyword in a.text:
                        yield Movie(title=a.text, index=int(base.extract(base.digit_rx, a.get('href'))))
        elif isinstance(style, (tuple, list)):
            for sty in style:
                for m in Movie.search(keyword, sty, pages):
                    yield m
        else:
            for style in base.STYLES:
                for m in Movie.search(keyword, style, pages):
                    yield m


if __name__ == '__main__':
    pass

    # clever_load('日韩', lb=1, ub=7)
    # for m in Movie.search('教'):
    #     print(m)
    #Movie.load([(8995,8997), (32197, 32198), ], verbose=True)
    Movie.load(31529)
