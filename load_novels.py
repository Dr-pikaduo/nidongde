#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import base

index = 27627
URL = "http://www.bxmyly.com/html/article/index%d.html" % index

soup = base.url2soup(URL)

m = soup.find('div', {'class':'main'})
title = m.find('div', {'class':'title'}).text
body = m.find('div', {'class':'content'}).text
print(title)
print(body)