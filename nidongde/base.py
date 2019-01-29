#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

import utils


class Loadable(type):
    def __new__(cls, name, bases, attrs):
        if name != 'Item':
            if 'website' not in attrs:
                raise NotImplementedError('Recommanded to define website to handle with urls')
        return super(Loadable, cls).__new__(cls, name, bases, attrs)

    def __call__(self, *args, **kwargs):
        o = super(Loadable, self).__call__()
        for k, v in kwargs.items():
            if not hasattr(o, k) or getattr(o, k) is None:
                setattr(o, k, v)
        return o


class Item(metaclass=Loadable):
    # Loadable item
    folder = pathlib.Path('Data')

    @classmethod
    @utils.generalize
    def load(cls, index, folder=None, verbose=False):
        """Load moives with indexes
        
        Arguments:
            index {int|list[int]|tuple(int, int)} -- index
            folder -- where the data are saved
            verbose {bool} -- show the info of item

        Example:
            load([29964, (34533, 24543)])  # load index29964, 34533-24543
        """

        item = cls.fromIndex(index)
        if item:
            if verbose:
                print('Loading', item)
            item.save(folder)

    @classmethod
    def fromIndex(cls, index):
        URL = cls.website.index2url(index)
        m = cls.fromURL(URL)
        if m:
            m.index = index
            return m

    def save(self, folder=None, filename=None):
        if folder is None:
            folder = self.folder
        if not folder.exists():
            folder.mkdir(parents=True)
        path = folder / filename
        content = utils.get(self.data).content
        if isinstance(content, str):
            path.write_text(content, encoding='utf-8')
        else:
            path.write_bytes(content)


    @classmethod
    def search(cls, keyword, style=None, pages=None):
        if isinstance(style, str):
            if pages is None:
                pages, _ = cls.website.get_page(style)
            for page in range(1, pages+1):
                for x in cls._search(keyword, style, page):
                    yield x
                
        elif isinstance(style, (tuple, list)):
            for sty in style:
                for x in cls.search(keyword, sty, pages):
                    yield x
        else:
            for style in cls.website.styles:
                for x in cls.search(keyword, style, pages):
                    yield x

    @classmethod
    def _search(cls, keyword, style, page=1):
        """Search items in one page
        
        Arguments:
            keyword {str} -- keyword for searching movies
            style {str} -- the style of movies that you search
            page {int} -- in which page you search them
        
        Yields:
            Item
        """
        URL = cls.website.style2url(style, page)
        for m in cls.website.search_in_page(keyword, URL, cls):
            yield m

    @classmethod
    def clever_load(cls, style, lb, ub):
        # load items in some style from lb to ub
        (pages, index) = cls.website.get_page(style)
        index1 = index - ub + 1
        index2 = index - lb + 1
        for k in range(index1, index2+1):
            cls.load(k)

    @classmethod
    def fromURL(cls, URL):
        """find item in url, url -> item
        
        Arguments:
            URL {str}
        
        Returns:
            Item
        """

        return getattr(cls.website, 'get_' + cls.__name__.lower())(URL, cls)

