#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import bs4

defaultAVFolder = '~/Folders/生活/成人相关/AVs'

ll = b'\xe4\xb9\xb1\xe4\xbc\xa6'.decode('utf-8')
rq = b'\xe4\xba\xba\xe5\xa6\xbb'.decode('utf-8')
tp = b'\xe5\x81\xb7\xe6\x8b\x8d'.decode('utf-8')
jr = b'\xe5\xb7\xa8\xe4\xb9\xb3'.decode('utf-8')
xs = b'\xe5\xad\xa6\xe7\x94\x9f'.decode('utf-8')
rh = b'\xe6\x97\xa5\xe9\x9f\xa9'.decode('utf-8')
om = b'\xe6\xac\xa7\xe7\xbe\x8e'.decode('utf-8')
dm = b'\xe5\x8a\xa8\xe6\xbc\xab'.decode('utf-8')

STYLES = {ll:27, rq:28, tp:29, xs:34, jr:54, rh:55, om:56, dm:58}

digit_rx = re.compile(r'\d+')
page_rx = re.compile(r'\d+/(\d+)')
mp4_rx = re.compile('https://.*\\.mp4')
# index_rx = re.compile(r'(\d+)( *\- *(\d+))?( *, *(\d+)( *\- *(\d+))?)?')

# proxies = {
#   'http': 'http://172.18.101.221:3182',
#   'https': 'http://172.18.101.221:1080',
# }

from fake_useragent import UserAgent


def get(url, headers={}, fake=None):
    '''Get respond from url
    
    Arguments:
        url {str} -- url
    
    Keyword Arguments:
        headers {dict} -- header info (default: {{}})
        fake {None | str} -- fake user agent (default: {None})
    
    Returns:
        [type] -- [description]
    '''
    if fake:
        ua = UserAgent()
        headers.update({'User-Agent': getattr(ua, fake)})
    return requests.get(url, headers)


def url2soup(url, headers={}):
    # url -> soup
    response = get(url, headers=headers)
    # response.encoding == 'ISO-8859-1':
    encodings = requests.utils.get_encodings_from_content(response.text)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = response.apparent_encoding
    encode_content = response.content.decode(encoding, 'replace')
    return bs4.BeautifulSoup(encode_content, "lxml")


def extract(rx, s):
    return rx.search(s)[0]


def str2index(s):
    '''str -> index
    
    Arguments:
        s {str} --  such as '111, 222-333, 444'
    
    Returns:
        index
    '''
    
    if s.isdigit():
        return int(s)
    index = []
    for a in s.split(','):
        a = a.strip()
        if '-' in a:
            i = tuple(int(i) for i in a.split('-'))
        else:
            i = int(a)
        index.append(i)

    return index


def generalize(f):
    # decorator extending the domain of f
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


class LoadItem:
    # Load item
    def __init__(self, title):
        self.title = title

