#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''load videos from www.417mm.com
'''

import requests
import pathlib

import base

# style: number

def generalize(f):
    def g(index, *args, **kwargs):
        if isinstance(index, list):
            for n in index:
                g(n, *args, **kwargs)
        elif isinstance(index, tuple): # tuple of ints
            a, b = min(index), max(index)
            for n in range(a, b+1):
                f(n, *args, **kwargs)
        else:  # index: int
            f(index, *args, **kwargs)
    return g


def get_page(style):
    """get the number of pages and max index of the movies in certain style
    
    Arguments:
        style {str} -- style of movie, one of the keys in STYLES
    
    Returns:
        tuple -- (number of pages, max index)
    """

    URL = "http://www.417mm.com/list/index%d.html" % base.STYLES[style]
    soup = base.url2soup(URL)
    s = soup.find_all('div', {'class':'con'})[0]
    index = int(base.digit_rx.search(s.a['href'])[0])
    p = soup.find('div', {'class': 'dede_pages'}).find('span')
    pages = int(base.page_rx.search(p.text)[1])
    return pages, index


@generalize
def load(index, folder=None):
    """Load moives

    Find the indexes of movies wantted on www.417mm.com,
    then load it.
    
    Arguments:
        index {int|list[int]|tuple(int, int)} -- index
        folder -- the folder where videos are stored.

    Example:
        load([29964, (34533, 24543)])  # load index29964, 34533-24543
    """

    URL = "http://www.417mm.com/player/index%d.html?%d-0-0" % (index, index)
    soup = base.url2soup(URL)
    for s in soup.find_all('script', {"type": "text/javascript"}):
        if 'video' in s.text:
            mp4 = base.mp4_rx.search(s.text)[0]
            break

    html = requests.get(mp4)
    html = html.content

    if folder is None:
        folder = pathlib.Path('AVs')
    if not folder.exists():
        folder.mkdir(parents=True)
    path = (folder / ('video%d.mp4' % index))
    path.write_bytes(html)


def clever_load(style, lb, ub):
    # load movies in some style from lb to ub
    (pages, index) = get_page(style)
    index1 = index - ub + 1
    index2 = index - lb + 1
    for k in range(index1, index2+1):
        load(k) 

if __name__ == '__main__':
    # clever_load('日韩', lb=1, ub=7)
    load([29963, (29964, 29971), (34538, 34543)])