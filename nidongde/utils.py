#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import threading
import random

import requests
import bs4


digit_rx = re.compile(r'\d+')
page_rx = re.compile(r'\d+/(\d+)')
mp4_rx = re.compile('https://.*\\.mp4')

# index_rx = re.compile(r'(\d+)( *\- *(\d+))?( *, *(\d+)( *\- *(\d+))?)?')

# proxies = {
#   'http': 'http://172.18.101.221:3182',
#   'https': 'http://172.18.101.221:1080',
# }

def caesar(s, k=8):
    # Caesar cipher
    return ''.join(map(chr, map(lambda x: x+k, map(ord, s))))

def random_mask(s, prob=0.75, repl='*'):
    return ''.join(map(lambda x: repl if random.random()<prob else x, s))

try:
    from fake_useragent import UserAgent
except:
    pass


def get(url, headers={}, fake=None):
    """Get respond from url
    
    Arguments:
        url {str} -- url
    
    Keyword Arguments:
        headers {dict} -- header info (default: {{}})
        fake {None | str} -- fake user agent (default: {None})
    
    Returns:
        [type] -- [description]
    """
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


def str2index(s):
    """str -> index
    
    Arguments:
        s {str} --  such as '111, 222-333, 444'
    
    Returns:
        index -- such as [111, (222, 333), 444]
    """
    
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

def index2str(index):
    # inverse of str2index
    if isinstance(index, list):
        return ', '.join(map(index2str, index))
    elif isinstance(index, tuple):
        return '-'.join((str(min(index)), str(max(index))))
    else:
        return str(index)


class LoadingThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(LoadingThread, self).__init__(*args, **kwargs)
        self.index = kwargs['args'][1]

    def start(self):
        if isinstance(self.index, int):
            print('Start to load data [index: %d]'%(self.index))
        super(LoadingThread, self).start()

    def join(self):
        super(LoadingThread, self).join()
        if isinstance(self.index, int):
            print('Completed data [index: %d]'%(self.index))

    def run(self):
        try:
            super(LoadingThread, self).run()
        except:
            print('Item %d could not be loaded.' % self.index)


def generalize(f):
    """Decorator extending the domain of f
    such as
    f(int) -> f([int, (int, int), int])
    """
    def g(cls, index, *args, **kwargs):
        if isinstance(index, list):
            ths = (LoadingThread(target=g, args=(cls, n) + args, kwargs=kwargs) for n in index)
            for th in ths:
                th.start()
            for th in ths:
                th.join()
        elif isinstance(index, tuple): # tuple of ints
            a, b = min(index), max(index)
            ths = (LoadingThread(target=f, args=(cls, n) + args, kwargs=kwargs) for n in range(a, b+1))
            for th in ths:
                th.start()
            for th in ths:
                th.join()
        else:  # index: int
            f(cls, index, *args, **kwargs)
    return g
