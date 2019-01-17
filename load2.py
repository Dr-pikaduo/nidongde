#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests

import base

HOME = "http://www.t077ee.com"

STYLES = ['亚洲风情', '日韩经典']

def get_page(style='亚洲风情'):
    """get the number of pages and max index of the movies in certain style
    
    Arguments:
        style {str} -- style of movie, one of the keys in STYLES
    
    Returns:
        tuple -- (number of pages, max index)
    """

    URL = HOME + "/list/index%d.html" % (STYLES.index(style) + 1)
    soup = base.url2soup(URL)

    cl = soup.find('div', {'class': 'channellist box mb bg'})
    indexes =[int(base.digit_rx.search(li.a['href'])[0]) for li in cl.find_all('li')]

    p = soup.find('div', {'class': 'page'})
    pages = int(base.page_rx.search(p.text)[1])
    return pages, indexes

print(get_page('日韩经典'))