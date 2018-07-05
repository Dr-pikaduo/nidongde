#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests
import re
import pathlib

# style: number
STYLES = {'乱伦':27, '人妻':28, '偷拍':29, '学生':34, '巨乳':54, '日韩':55, '欧美':56, '动漫':58}

digit_rx = re.compile('\d+')
page_rx = re.compile('\d/(\d+)')

def get_page(style):
    """get the number of pages and max index of the movies in certain style
    
    Arguments:
        style {str} -- style of movie, one of the keys in STYLES
    
    Returns:
        tuple -- (number of pages, max index)
    """
    URL = "http://www.417mm.com/list/index%d.html" % STYLES[style]

    response = requests.get(URL)
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        encoding = encodings[0] if encodings else response.apparent_encoding

    content = response.content.decode(encoding, 'replace')

    soup = bs4.BeautifulSoup(content, "html.parser")
    s = soup.find_all('div', {'class':'con'})[0]
    index = int(digit_rx.search(s.a['href'])[0])
    p = soup.find('div', {'class': 'dede_pages'}).find('span')
    pages = int(page_rx.search(p.text)[1])
    return pages, index

mp4_rx = re.compile('https://.*\\.mp4')

def load(index, folder=None):
    """Load moives
    
    Arguments:
        index {int|[int]} -- index
    """

    if isinstance(index, list):
        for n in index:
            load(n)
        return
    elif isinstance(index, tuple):
        for n in range(index[0], index[1]+1):
            load(n)
        return

    URL = "http://www.417mm.com/player/index%d.html?%d-0-0" % (index, index)
    response = requests.get(URL)

    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
    content = response.content.decode(encoding, 'replace')

    soup = bs4.BeautifulSoup(content, "html.parser")
    for s in soup.find_all('script', {"type": "text/javascript"}):
        if 'video' in s.text:
            mp4 = mp4_rx.search(s.text)[0]
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
    (pages, index) = get_page(style)
    index1 = index - ub + 1
    index2 = index - lb + 1
    for k in range(index1, index2+1):
        load(k) 

if __name__ == '__main__':
    # clever_load('日韩', lb=1, ub=7)
    load(29964)
    load((34533, 24543))