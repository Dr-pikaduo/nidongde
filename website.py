#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import utils


# Define website: www.417mm.com
ll = b'\xe4\xb9\xb1\xe4\xbc\xa6'.decode('utf-8')
rq = b'\xe4\xba\xba\xe5\xa6\xbb'.decode('utf-8')
tp = b'\xe5\x81\xb7\xe6\x8b\x8d'.decode('utf-8')
jr = b'\xe5\xb7\xa8\xe4\xb9\xb3'.decode('utf-8')
xs = b'\xe5\xad\xa6\xe7\x94\x9f'.decode('utf-8')
rh = b'\xe6\x97\xa5\xe9\x9f\xa9'.decode('utf-8')
om = b'\xe6\xac\xa7\xe7\xbe\x8e'.decode('utf-8')
dm = b'\xe5\x8a\xa8\xe6\xbc\xab'.decode('utf-8')


class web417:
    """Define methods to operate urls
    
    Variables:
        name {str} -- the name of the website
        url {str} -- the home
        styles {dict} -- styles of the movies
        default_style {str}
    """
    name = '417mm'
    url = 'http://www.417mm.com'
    styles = {ll:27, rq:28, tp:29, xs:34, jr:54, rh:55, om:56, dm:58}
    default_style = rq

    @staticmethod
    def index2url(index):
        """Translate an index to a completed url
        
        Arguments:
            index {int} -- index of the movie
        
        Returns:
            str -- url of the movie
        """
        return web417.url + "/player/index%d.html?%d-0-0" % (index, index)

    @staticmethod
    def style2url(style, page=1):
        """Translate style to url
        
        Arguments:
            style {str} -- style of the movie
        
        Keyword Arguments:
            page {number} -- the number of the page (default: {1})
        
        Returns:
            str -- url
        """
        return web417.url + "/list/index%d_%d.html" % (web417.styles[style], page)

    @staticmethod
    def get_page(style):
        """get the number of pages and max index of the movies in certain style
        
        Arguments:
            style {str} -- style of the movie
        
        Returns:
            tuple -- (number of pages, max index)
        """

        URL = web417.url + "/list/index%d.html" % web417.styles[style]
        soup = utils.url2soup(URL)
        s = soup.find_all('div', {'class':'con'})[0]
        index = int(utils.digit_rx.search(s.a['href'])[0])
        p = soup.find('div', {'class': 'dede_pages'}).find('span')
        pages = int(utils.page_rx.search(p.text)[1])
        return pages, index

