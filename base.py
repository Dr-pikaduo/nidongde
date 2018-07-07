#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import bs4

STYLES = {'乱伦':27, '人妻':28, '偷拍':29, '学生':34, '巨乳':54, '日韩':55, '欧美':56, '动漫':58}

digit_rx = re.compile('\d+')
page_rx = re.compile('\d/(\d+)')
mp4_rx = re.compile('https://.*\\.mp4')


def url2soup(url):
    # url -> soup
    response = requests.get(url)
    if response.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(response.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = response.apparent_encoding
    encode_content = response.content.decode(encoding, 'replace')
    return bs4.BeautifulSoup(encode_content, "html.parser")


def extract(rx, s):
    return rx.search(s)[0]