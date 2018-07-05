#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import bs4
import requests

index = 27627
URL = "http://www.bxmyly.com/html/article/index%d.html" % index

response = requests.get(URL)

if response.encoding == 'ISO-8859-1':
    encodings = requests.utils.get_encodings_from_content(response.text)
    if encodings:
        encoding = encodings[0]
    else:
        encoding = response.apparent_encoding
encode_content = response.content.decode(encoding, 'replace')
soup = bs4.BeautifulSoup(encode_content, "html.parser")
m = soup.find('div', {'class':'main'})
title = m.find('div', {'class':'title'}).text
body = m.find('div', {'class':'content'}).text
print(title)
print(body)