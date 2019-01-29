#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class WebsiteError(NotImplementedError):
    pass


class WebsiteLike(type):
    
    data = ('movie', 'data', 'novel')

    def __new__(cls, name, bases, attrs):
        if 'home' not in attrs:
            raise WebsiteError('Should define the url of the home of the website')
        if 'index2url' not in attrs:
            raise WebsiteError('Should define classmethod index2url: index->url')
        if 'style2url' not in attrs:
            raise WebsiteError('Should define classmethod style2url: style, page->url')
        if 'search_in_page' not in attrs:
            raise WebsiteError('Should define classmethod search_in_page: keyword, url->data')
        if all('get_'+d not in attrs for d in cls.data):
            raise WebsiteError('Should define classmethod extract the data from url')
        return super(WebsiteLike, cls).__new__(cls, name, bases, attrs)
