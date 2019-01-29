#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from nidongde import utils
from nidongde.website.website import *

# Define website: www.417mm.com
ll = b'\xe4\xb9\xb1\xe4\xbc\xa6'.decode('utf-8')
rq = b'\xe4\xba\xba\xe5\xa6\xbb'.decode('utf-8')
tp = b'\xe5\x81\xb7\xe6\x8b\x8d'.decode('utf-8')
jr = b'\xe5\xb7\xa8\xe4\xb9\xb3'.decode('utf-8')
xs = b'\xe5\xad\xa6\xe7\x94\x9f'.decode('utf-8')
rh = b'\xe6\x97\xa5\xe9\x9f\xa9'.decode('utf-8')
om = b'\xe6\xac\xa7\xe7\xbe\x8e'.decode('utf-8')
dm = b'\xe5\x8a\xa8\xe6\xbc\xab'.decode('utf-8')


class web417(metaclass=WebsiteLike):
    """Define methods to operate urls
    
    Variables:
        home {str} -- the home
        styles {dict} -- styles of the movies
        default_style {str}
    """

    home = 'http://www.417mm.com'
    _alt = 'http://www.434mm.com'

    styles = {ll:27, rq:28, tp:29, xs:34, jr:54, rh:55, om:56, dm:58}
    default_style = rq

    movie_title_rx = re.compile(r'((?P<chapter>\d{1,2})-)?(?P<title>.+)')

    @classmethod
    def index2url(cls, index):
        """Translate an index to a completed url
        
        Arguments:
            index {int} -- index of the movie
        
        Returns:
            str -- url of the movie
        """
        return cls.home + "/player/index%d.html?%d-0-0" % (index, index)

    @classmethod
    def style2url(cls, style, page=1):
        """Translate style to url
        
        Arguments:
            style {str} -- style of the movie
        
        Keyword Arguments:
            page {number} -- the number of the page (default: {1})
        
        Returns:
            str -- url
        """
        if page:
            return cls.home + "/list/index%d_%d.html" % (cls.styles[style], page)
        else:
            return cls.home + "/list/index%d.html" % cls.styles[style]

    @classmethod
    def get_page(cls, style):
        """get the number of pages and max index of the movies in certain style
        
        Arguments:
            style {str} -- style of the movie
        
        Returns:
            tuple -- (number of pages, max index)
        """

        URL = web417.style2url(style, page=None)
        soup = utils.url2soup(URL)
        s = soup.find_all('div', {'class':'con'})[0]
        index = int(utils.digit_rx.search(s.a['href'])[0])
        p = soup.find('div', {'class': 'dede_pages'}).find('span')
        pages = int(utils.page_rx.search(p.text)[1])
        return pages, index

    @classmethod
    def get_movie(cls, URL, klass=None):
        """find movie in url, url -> movie
        
        Arguments:
            URL {str}
        
        Returns:
            klass
        """
        soup = utils.url2soup(URL)
        title = soup.find('h2', {'class':'m_T2'})
        m = web417.movie_title_rx.match(title.text)
        chapter = int(m['chapter']) if m['chapter'] else 0
        for s in soup.find_all('script', {"type": "text/javascript"}):
            if 'video' in s.text:
                mp4 = utils.mp4_rx.search(s.text)[0]
                if klass:
                    return klass(title=m['title'], chapter=chapter, data=mp4)
                else:
                    return {'title': m['title'], 'chapter': chapter, 'data': mp4}

    @classmethod
    def search_in_page(cls, keyword, URL, klass=None):
        soup = utils.url2soup(URL)

        for div in soup.find_all('div', {'class':'con'}):
            t = div.find('a', {'class':'txt'})
            if t and keyword in t.text:
                m = cls.movie_title_rx.match(t.text)
                chapter = int(m['chapter']) if m['chapter'] else 0
                if klass:
                    yield klass(title=m['title'], chapter=chapter, index=int(utils.digit_rx.search(t['href'])[0]))
                else:
                    yield {'title': m['title'], 'chapter':chapter, 'index':int(utils.digit_rx.search(t['href'])[0])}

