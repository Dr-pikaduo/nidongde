#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
load videos from adult website such as www.417mm.com
If you want to load movies or other types of data from other websites,
then you should override the methods: fromURL, _search
"""

import pathlib

from nidongde import website, utils, Item

defaultWebsite = website.web417

defaultAVFolder = pathlib.Path('AVs')

class Movie(Item):
    website = defaultWebsite
    chapter = None
    folder = defaultAVFolder

    def __str__(self):
        if self.chapter:
            return '%s(%d) # %d' % (self.title, self.chapter, self.index)
        else:
            return '%s # %d' % (self.title, self.index)

    def __format__(self, spec=None):
        if spec in {'mask', 'm'}:
            return '*' * len(self.title) + '(%d) # %d' % (self.chapter, self.index)
        elif '.' in spec:
            return '%s(%d) # %d' % (utils.random_mask(self.title, float(spec)), self.chapter, self.index)
        elif spec.isdigit():
            return '%s(%d) # %d' % (utils.caesar(self.title, int(spec)), self.chapter, self.index)
        else:
            return '%s(%d) # %d' % (self.title, self.chapter, self.index)

    def save(self, folder=None):
        filename = 'Movie%d.mp4' % self.index
        super(Movie, self).save(folder, filename)

    @classmethod
    def fromURL(cls, URL):
        """find movie in url, url -> movie
        
        Arguments:
            URL {str}
        
        Returns:
            Movie
        """

        return cls.website.get_movie(URL, cls)


if __name__ == '__main__':

    # clever_load('日韩', lb=1, ub=7)
    # for m in Movie.search('教'):
    #     print(m)
    Movie.load([(33010, 33004), ], verbose=True, folder=defaultAVFolder)
    # Movie.load(31529)
